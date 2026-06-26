"""SSL training loop — EMA, LR/momentum schedules, AMP, collapse monitor (§9).

A single :class:`SSLTrainer` drives any pluggable SSL method (BYOL primary).
Per-backbone AMP rule is enforced: ResNet-50 uses mixed precision, EfficientNet
runs fp32 (the same fp16-overflow rule as supervised training — CLAUDE.md /
brief §5.4).
"""

from __future__ import annotations

import math
from typing import Any, Callable

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.ssl.encoder import build_ssl_encoder
from src.ssl.methods import SSLMethod, build_method, feature_std


# ---------------------------------------------------------------------------
# LARS optimizer (large-batch-style BYOL/DINO; brief §5.4)
# ---------------------------------------------------------------------------

class LARS(torch.optim.Optimizer):
    """Layer-wise Adaptive Rate Scaling (You et al. 2017).

    Standard SSL LARS: trust-ratio-scaled SGD-with-momentum, excluding 1-D
    parameters (biases / BatchNorm) from both weight decay and adaptation.

    Args:
        params: Iterable of parameters or parameter groups.
        lr: Base learning rate.
        momentum: Momentum factor. Default 0.9.
        weight_decay: Weight decay (L2). Default 1e-6.
        trust_coefficient: LARS trust coefficient ``eta``. Default 0.001.
        eps: Numerical floor for the trust ratio denominator.
    """

    def __init__(
        self,
        params: Any,
        lr: float,
        momentum: float = 0.9,
        weight_decay: float = 1e-6,
        trust_coefficient: float = 0.001,
        eps: float = 1e-8,
    ) -> None:
        defaults = dict(
            lr=lr, momentum=momentum, weight_decay=weight_decay,
            trust_coefficient=trust_coefficient, eps=eps,
        )
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure: Callable[[], float] | None = None) -> float | None:
        """Perform one LARS optimization step.

        Args:
            closure: Optional closure re-evaluating the loss.

        Returns:
            The loss returned by ``closure`` if provided, else ``None``.
        """
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None:
                    continue
                grad = p.grad
                # Exclude 1-D params (bias/BN) from WD + adaptation.
                if p.ndim > 1:
                    grad = grad.add(p, alpha=group["weight_decay"])
                    param_norm = torch.norm(p)
                    grad_norm = torch.norm(grad)
                    trust = torch.where(
                        (param_norm > 0) & (grad_norm > 0),
                        group["trust_coefficient"] * param_norm / (grad_norm + group["eps"]),
                        torch.ones_like(param_norm),
                    )
                    grad = grad.mul(trust)

                state = self.state[p]
                if "mu" not in state:
                    state["mu"] = torch.zeros_like(p)
                mu = state["mu"]
                mu.mul_(group["momentum"]).add_(grad)
                p.add_(mu, alpha=-group["lr"])

        return loss


# ---------------------------------------------------------------------------
# Schedules
# ---------------------------------------------------------------------------

def cosine_warmup_lr(step: int, total_steps: int, warmup_steps: int, base_lr: float) -> float:
    """Linear warmup then cosine decay to 0 (brief §5.4).

    Args:
        step: Current global step (0-based).
        total_steps: Total optimization steps over the run.
        warmup_steps: Number of linear-warmup steps.
        base_lr: Peak learning rate after warmup.

    Returns:
        Learning rate for ``step``.
    """
    if warmup_steps > 0 and step < warmup_steps:
        return base_lr * (step + 1) / warmup_steps
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    progress = min(1.0, max(0.0, progress))
    return 0.5 * base_lr * (1.0 + math.cos(math.pi * progress))


def cosine_momentum(step: int, total_steps: int, base_momentum: float) -> float:
    """Cosine ramp of EMA momentum from ``base_momentum`` to 1.0 (brief §5.4).

    Args:
        step: Current global step (0-based).
        total_steps: Total optimization steps over the run.
        base_momentum: Starting EMA momentum (e.g. 0.996).

    Returns:
        EMA momentum for ``step``.
    """
    progress = min(1.0, max(0.0, step / max(1, total_steps)))
    return 1.0 - (1.0 - base_momentum) * 0.5 * (1.0 + math.cos(math.pi * progress))


# ---------------------------------------------------------------------------
# Trainer
# ---------------------------------------------------------------------------

class SSLTrainer:
    """Self-supervised pretraining loop for one backbone.

    Builds the trunk + SSL method from the ``ssl`` config block, trains with the
    configured optimizer/schedules, applies per-backbone AMP, and monitors
    feature std for representational collapse.

    Args:
        ssl_config: The resolved ``ssl`` config dict (brief §6).
        backbone_name: ``"resnet50"`` or ``"efficientnet_b3"`` (etc.).
        device: ``"auto"`` / ``"cpu"`` / ``"cuda"``. Default ``"auto"``.
        pretrained_init: Start the trunk from ImageNet (the §11 continual-SSL
            fallback). Default ``False`` (from-scratch — locked default).
    """

    def __init__(
        self,
        ssl_config: dict[str, Any],
        backbone_name: str,
        device: str = "auto",
        pretrained_init: bool = False,
    ) -> None:
        self.ssl_config = ssl_config
        self.backbone_name = backbone_name
        self.pretrained_init = bool(pretrained_init)

        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)

        # Per-backbone AMP rule (brief §5.4): ResNet on, EfficientNet off.
        amp_cfg = ssl_config.get("mixed_precision", {})
        self.mixed_precision = bool(amp_cfg.get(backbone_name, False)) and self.device.type == "cuda"

        self.in_channels = int(ssl_config.get("in_channels", 4))
        self.image_size = int(ssl_config.get("image_size", 256))
        self.method_name = str(ssl_config.get("method", "byol")).lower()

        trunk, feature_dim = build_ssl_encoder(
            backbone_name, in_channels=self.in_channels, pretrained=self.pretrained_init,
        )
        self.feature_dim = feature_dim
        self.method: SSLMethod = build_method(
            self.method_name, trunk, feature_dim, ssl_config
        ).to(self.device)

        self.optimizer = self._build_optimizer()
        self.scaler = torch.amp.GradScaler("cuda", enabled=self.mixed_precision)
        self.grad_clip = float(ssl_config.get("grad_clip", 1.0))

        opt_cfg = ssl_config.get("optimizer", {})
        byol_cfg = ssl_config.get("byol", {})
        self.base_lr = float(opt_cfg.get("base_lr", 0.45))
        self.warmup_epochs = int(opt_cfg.get("warmup_epochs", 10))
        self.base_momentum = float(byol_cfg.get("ema_base", 0.996))

    # -- optimizer construction ------------------------------------------------

    def _build_optimizer(self) -> torch.optim.Optimizer:
        """Build the optimizer named in ``ssl.optimizer.name`` (LARS/SGD/AdamW)."""
        opt_cfg = self.ssl_config.get("optimizer", {})
        name = str(opt_cfg.get("name", "lars")).lower()
        lr = float(opt_cfg.get("base_lr", 0.45))
        wd = float(opt_cfg.get("weight_decay", 1e-6))
        params = [p for p in self.method.parameters() if p.requires_grad]
        if name == "lars":
            return LARS(params, lr=lr, weight_decay=wd)
        if name == "sgd":
            return torch.optim.SGD(params, lr=lr, momentum=0.9, weight_decay=wd)
        if name == "adamw":
            return torch.optim.AdamW(params, lr=lr, weight_decay=wd)
        raise ValueError(f"Unknown optimizer '{name}'. Use lars | sgd | adamw.")

    # -- training --------------------------------------------------------------

    def train(
        self,
        dataloader: DataLoader,
        epochs: int,
        log_every: int = 50,
        on_epoch_end: Callable[[int, dict[str, float]], None] | None = None,
        max_steps: int | None = None,
    ) -> list[dict[str, float]]:
        """Run SSL pretraining.

        Args:
            dataloader: Yields ``(view1, view2)`` batches from
                :class:`EyePACSSSLDataset`.
            epochs: Number of epochs to train.
            log_every: Step interval for the collapse-monitor / log readout.
            on_epoch_end: Optional callback ``(epoch, metrics)`` after each epoch
                (e.g. for periodic checkpointing).
            max_steps: Optional hard cap on optimizer steps (smoke tests).

        Returns:
            Per-epoch history dicts ``{epoch, loss, feat_std, lr, ema_momentum}``.
        """
        steps_per_epoch = max(1, len(dataloader))
        total_steps = steps_per_epoch * epochs
        warmup_steps = self.warmup_epochs * steps_per_epoch

        history: list[dict[str, float]] = []
        global_step = 0
        self.method.train()

        for epoch in range(epochs):
            running_loss = 0.0
            last_feat_std = 0.0
            n_batches = 0

            for view1, view2 in dataloader:
                view1 = view1.to(self.device, non_blocking=True)
                view2 = view2.to(self.device, non_blocking=True)

                lr = cosine_warmup_lr(global_step, total_steps, warmup_steps, self.base_lr)
                for group in self.optimizer.param_groups:
                    group["lr"] = lr
                momentum = cosine_momentum(global_step, total_steps, self.base_momentum)

                self.optimizer.zero_grad(set_to_none=True)
                with torch.amp.autocast("cuda", enabled=self.mixed_precision):
                    loss = self.method(view1, view2)

                self.scaler.scale(loss).backward()
                if self.grad_clip > 0:
                    self.scaler.unscale_(self.optimizer)
                    nn.utils.clip_grad_norm_(self.method.parameters(), self.grad_clip)
                self.scaler.step(self.optimizer)
                self.scaler.update()

                if self.method.uses_ema:
                    self.method.momentum_update(momentum)

                running_loss += float(loss.detach().item())
                n_batches += 1

                if global_step % log_every == 0:
                    with torch.no_grad():
                        feats = self.method.extract_features(view1)
                    last_feat_std = feature_std(feats)
                    print(
                        f"  [ep {epoch} step {global_step}] loss={loss.item():.4f} "
                        f"feat_std={last_feat_std:.4f} lr={lr:.5f} m={momentum:.5f}",
                        flush=True,
                    )

                global_step += 1
                if max_steps is not None and global_step >= max_steps:
                    break

            epoch_metrics = {
                "epoch": float(epoch),
                "loss": running_loss / max(1, n_batches),
                "feat_std": last_feat_std,
                "lr": cosine_warmup_lr(global_step, total_steps, warmup_steps, self.base_lr),
                "ema_momentum": cosine_momentum(global_step, total_steps, self.base_momentum),
            }
            history.append(epoch_metrics)
            if on_epoch_end is not None:
                on_epoch_end(epoch, epoch_metrics)
            if max_steps is not None and global_step >= max_steps:
                break

        return history

    # -- checkpoint export -----------------------------------------------------

    def trunk_state_dict(self) -> dict[str, torch.Tensor]:
        """Return the **trunk-only** state dict for checkpointing (brief §9.2).

        These are the online/student/query backbone weights, keyed to load
        directly into a factory model's trunk (head excluded). Moved to CPU.

        Returns:
            State dict of the trunk's parameters and buffers.
        """
        return {k: v.detach().cpu() for k, v in self.method.backbone.state_dict().items()}
