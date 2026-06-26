"""SSL method strategies — BYOL (primary), MoCo-v2, SimSiam, DINO (brief §5).

All four share the same trunk (built by :func:`build_ssl_encoder`) and the same
two-view input; they differ only in the loss / head / momentum wiring. Each
strategy is an ``nn.Module`` whose ``forward(view1, view2)`` returns a scalar
loss, and which exposes:

- ``backbone``         — the trunk to checkpoint & probe (online/student/query).
- ``extract_features`` — pooled features for the collapse monitor / probe.
- ``uses_ema``         — whether ``momentum_update`` must be called each step.
- ``momentum_update``  — EMA target/key/teacher update (no-op when not EMA-based).

The trunk that downstream Exp-1 consumes is always ``method.backbone``, whose
``state_dict`` keys match a factory model's trunk keys (head excluded).

Method-family restriction (INV-SSL-6): BYOL / MoCo-v2 / SimSiam / DINO only.
MAE / RETFound / SimCLR-style large-batch contrastive are excluded.
"""

from __future__ import annotations

import copy
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F

from src.ssl.heads import DINOHead, MLPHead


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def feature_std(features: torch.Tensor) -> float:
    """Mean per-dimension std of L2-normalized features (collapse monitor).

    A healthy (non-collapsed) representation keeps this well above 0; a value
    near ``1/sqrt(d)`` indicates uniformly-spread unit features, while a value
    near 0 signals representational collapse (brief §9.1).

    Args:
        features: Pooled features of shape ``(N, d)``.

    Returns:
        Scalar mean standard deviation across the batch dimension.
    """
    with torch.no_grad():
        z = F.normalize(features, dim=-1, p=2)
        return float(z.std(dim=0).mean().item())


def _set_requires_grad(module: nn.Module, flag: bool) -> None:
    """Set ``requires_grad`` on every parameter of ``module``."""
    for p in module.parameters():
        p.requires_grad = flag


@torch.no_grad()
def _ema_update(online: nn.Module, target: nn.Module, momentum: float) -> None:
    """In-place EMA: ``target = m·target + (1-m)·online`` over all parameters."""
    for online_p, target_p in zip(online.parameters(), target.parameters()):
        target_p.data.mul_(momentum).add_(online_p.data, alpha=1.0 - momentum)
    for online_b, target_b in zip(online.buffers(), target.buffers()):
        target_b.data.copy_(online_b.data)


class SSLMethod(nn.Module):
    """Base class for SSL strategies.

    Subclasses set ``self.backbone`` (the trunk to checkpoint/probe) and
    ``self.uses_ema``, and implement :meth:`forward`.

    Args:
        backbone: The trunk (head-stripped) used as the online/student/query
            encoder.
        feature_dim: Trunk output dimension.
    """

    def __init__(self, backbone: nn.Module, feature_dim: int) -> None:
        super().__init__()
        self.backbone = backbone
        self.feature_dim = feature_dim
        self.uses_ema: bool = False

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Return pooled trunk features ``(N, feature_dim)`` (no head)."""
        return self.backbone(x)

    @torch.no_grad()
    def momentum_update(self, momentum: float) -> None:
        """Update EMA target/key/teacher network(s). No-op by default."""
        return None

    def forward(
        self, view1: torch.Tensor, view2: torch.Tensor
    ) -> torch.Tensor:  # pragma: no cover - abstract
        """Compute the SSL loss for a positive pair of views.

        Args:
            view1: First augmented view ``(N, C, H, W)``.
            view2: Second augmented view ``(N, C, H, W)``.

        Returns:
            Scalar loss tensor.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# BYOL (primary)
# ---------------------------------------------------------------------------

def _byol_regression_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """Normalized MSE loss ``2 - 2·cos(pred, target)`` (BYOL), per-sample mean."""
    pred = F.normalize(pred, dim=-1, p=2)
    target = F.normalize(target, dim=-1, p=2)
    return (2.0 - 2.0 * (pred * target).sum(dim=-1)).mean()


class BYOL(SSLMethod):
    """Bootstrap Your Own Latent (Grill et al. 2020) — primary method (§5.1).

    Online: trunk → projector → predictor. Target: EMA of (trunk, projector),
    no predictor, no gradient. Loss is the symmetrized normalized-MSE between
    the online prediction of one view and the target projection of the other.

    Args:
        backbone: Online trunk (head-stripped).
        feature_dim: Trunk output dimension.
        proj_hidden: Projector hidden width. Default 4096.
        proj_out: Projector / predictor output dimension. Default 256.
        pred_hidden: Predictor hidden width. Default 4096.
    """

    def __init__(
        self,
        backbone: nn.Module,
        feature_dim: int,
        proj_hidden: int = 4096,
        proj_out: int = 256,
        pred_hidden: int = 4096,
    ) -> None:
        super().__init__(backbone, feature_dim)
        self.uses_ema = True
        self.online_projector = MLPHead(feature_dim, proj_hidden, proj_out)
        self.online_predictor = MLPHead(proj_out, pred_hidden, proj_out)

        self.target_backbone = copy.deepcopy(backbone)
        self.target_projector = copy.deepcopy(self.online_projector)
        _set_requires_grad(self.target_backbone, False)
        _set_requires_grad(self.target_projector, False)

    def _online_forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.online_predictor(self.online_projector(self.backbone(x)))

    @torch.no_grad()
    def _target_forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.target_projector(self.target_backbone(x))

    def forward(self, view1: torch.Tensor, view2: torch.Tensor) -> torch.Tensor:
        p1 = self._online_forward(view1)
        p2 = self._online_forward(view2)
        with torch.no_grad():
            z1 = self._target_forward(view1)
            z2 = self._target_forward(view2)
        loss = _byol_regression_loss(p1, z2) + _byol_regression_loss(p2, z1)
        return loss

    @torch.no_grad()
    def momentum_update(self, momentum: float) -> None:
        _ema_update(self.backbone, self.target_backbone, momentum)
        _ema_update(self.online_projector, self.target_projector, momentum)


# ---------------------------------------------------------------------------
# SimSiam
# ---------------------------------------------------------------------------

class SimSiam(SSLMethod):
    """SimSiam (Chen & He 2021) — no EMA, no queue; stop-grad + predictor.

    Args:
        backbone: Trunk (head-stripped).
        feature_dim: Trunk output dimension.
        proj_hidden: Projector hidden width. Default 2048.
        proj_out: Projector output dimension. Default 2048.
        pred_hidden: Predictor hidden (bottleneck) width. Default 512.
    """

    def __init__(
        self,
        backbone: nn.Module,
        feature_dim: int,
        proj_hidden: int = 2048,
        proj_out: int = 2048,
        pred_hidden: int = 512,
    ) -> None:
        super().__init__(backbone, feature_dim)
        self.uses_ema = False
        self.projector = MLPHead(feature_dim, proj_hidden, proj_out, last_bn=True)
        self.predictor = MLPHead(proj_out, pred_hidden, proj_out)

    @staticmethod
    def _neg_cosine(p: torch.Tensor, z: torch.Tensor) -> torch.Tensor:
        z = z.detach()
        p = F.normalize(p, dim=-1, p=2)
        z = F.normalize(z, dim=-1, p=2)
        return -(p * z).sum(dim=-1).mean()

    def forward(self, view1: torch.Tensor, view2: torch.Tensor) -> torch.Tensor:
        z1 = self.projector(self.backbone(view1))
        z2 = self.projector(self.backbone(view2))
        p1 = self.predictor(z1)
        p2 = self.predictor(z2)
        return 0.5 * (self._neg_cosine(p1, z2) + self._neg_cosine(p2, z1))


# ---------------------------------------------------------------------------
# MoCo-v2
# ---------------------------------------------------------------------------

class MoCoV2(SSLMethod):
    """MoCo-v2 (Chen et al. 2020) — momentum encoder + negative queue (§5.2).

    Stable at small batch (the queue supplies negatives), a good fallback if
    BYOL collapses. ``view1`` is the query, ``view2`` the key.

    Args:
        backbone: Query trunk (head-stripped).
        feature_dim: Trunk output dimension.
        queue_size: Number of negative keys held in the queue.
        moco_dim: Projection dimension.
        temperature: InfoNCE softmax temperature.
        ema: Key-encoder EMA momentum (constant in MoCo, ramped by the trainer
            only if ``uses_ema`` scheduling is enabled).
    """

    def __init__(
        self,
        backbone: nn.Module,
        feature_dim: int,
        queue_size: int = 8192,
        moco_dim: int = 128,
        temperature: float = 0.2,
        ema: float = 0.999,
    ) -> None:
        super().__init__(backbone, feature_dim)
        self.uses_ema = True
        self.temperature = float(temperature)
        self.default_ema = float(ema)

        self.query_projector = MLPHead(feature_dim, feature_dim, moco_dim, use_bn=False)
        self.key_backbone = copy.deepcopy(backbone)
        self.key_projector = copy.deepcopy(self.query_projector)
        _set_requires_grad(self.key_backbone, False)
        _set_requires_grad(self.key_projector, False)

        self.register_buffer("queue", F.normalize(torch.randn(moco_dim, queue_size), dim=0))
        self.register_buffer("queue_ptr", torch.zeros(1, dtype=torch.long))

    @torch.no_grad()
    def _dequeue_and_enqueue(self, keys: torch.Tensor) -> None:
        batch = keys.shape[0]
        ptr = int(self.queue_ptr.item())
        capacity = self.queue.shape[1]
        if batch >= capacity:
            self.queue.copy_(keys[:capacity].t())
            self.queue_ptr[0] = 0
            return
        end = ptr + batch
        if end <= capacity:
            self.queue[:, ptr:end] = keys.t()
        else:
            first = capacity - ptr
            self.queue[:, ptr:] = keys[:first].t()
            self.queue[:, : batch - first] = keys[first:].t()
        self.queue_ptr[0] = end % capacity

    def forward(self, view1: torch.Tensor, view2: torch.Tensor) -> torch.Tensor:
        q = F.normalize(self.query_projector(self.backbone(view1)), dim=-1, p=2)
        with torch.no_grad():
            k = F.normalize(self.key_projector(self.key_backbone(view2)), dim=-1, p=2)

        l_pos = (q * k).sum(dim=-1, keepdim=True)               # (N, 1)
        l_neg = q @ self.queue.clone().detach()                  # (N, K)
        logits = torch.cat([l_pos, l_neg], dim=1) / self.temperature
        labels = torch.zeros(logits.shape[0], dtype=torch.long, device=logits.device)
        loss = F.cross_entropy(logits, labels)
        self._dequeue_and_enqueue(k)
        return loss

    @torch.no_grad()
    def momentum_update(self, momentum: float) -> None:
        # MoCo conventionally uses a constant key momentum; honour the trainer's
        # schedule but never let it fall below the configured default.
        m = max(momentum, self.default_ema) if momentum < 1.0 else self.default_ema
        _ema_update(self.backbone, self.key_backbone, m)
        _ema_update(self.query_projector, self.key_projector, m)


# ---------------------------------------------------------------------------
# DINO
# ---------------------------------------------------------------------------

class DINO(SSLMethod):
    """DINO self-distillation (Caron et al. 2021) — two-global-crop form.

    Student (trunk + head) is distilled toward an EMA teacher with output
    centering and temperature sharpening.

    NOTE / documented simplification (brief §4.2/§5.2 allows method-internal
    deviation with reason): multi-crop *local* views are not wired here. BYOL is
    the mandated primary method and verification is CPU-only with synthetic
    tensors, so DINO is implemented over the two global crops only. The
    ``n_local_crops`` config knob is therefore accepted but inert; full
    multi-crop is left as a follow-up if DINO wins screening (§5.3).

    Args:
        backbone: Student trunk (head-stripped).
        feature_dim: Trunk output dimension.
        out_dim: DINO prototype count. Default 65536.
        student_temp: Student softmax temperature. Default 0.1.
        teacher_temp: Teacher softmax temperature. Default 0.07.
        center_momentum: EMA momentum for the output center. Default 0.9.
    """

    def __init__(
        self,
        backbone: nn.Module,
        feature_dim: int,
        out_dim: int = 65536,
        student_temp: float = 0.1,
        teacher_temp: float = 0.07,
        center_momentum: float = 0.9,
    ) -> None:
        super().__init__(backbone, feature_dim)
        self.uses_ema = True
        self.student_temp = float(student_temp)
        self.teacher_temp = float(teacher_temp)
        self.center_momentum = float(center_momentum)

        self.student_head = DINOHead(feature_dim, out_dim)
        self.teacher_backbone = copy.deepcopy(backbone)
        # weight_norm tensors are non-leaf and cannot be deepcopied; build a fresh
        # head and copy the student's weights instead (PyTorch issue #103001).
        self.teacher_head = DINOHead(feature_dim, out_dim)
        self.teacher_head.load_state_dict(self.student_head.state_dict())
        _set_requires_grad(self.teacher_backbone, False)
        _set_requires_grad(self.teacher_head, False)

        self.register_buffer("center", torch.zeros(1, out_dim))

    def _student(self, x: torch.Tensor) -> torch.Tensor:
        return self.student_head(self.backbone(x))

    @torch.no_grad()
    def _teacher(self, x: torch.Tensor) -> torch.Tensor:
        return self.teacher_head(self.teacher_backbone(x))

    def _cross_entropy(self, teacher_out: torch.Tensor, student_out: torch.Tensor) -> torch.Tensor:
        t = F.softmax((teacher_out - self.center) / self.teacher_temp, dim=-1)
        s = F.log_softmax(student_out / self.student_temp, dim=-1)
        return -(t * s).sum(dim=-1).mean()

    @torch.no_grad()
    def _update_center(self, teacher_out: torch.Tensor) -> None:
        batch_center = teacher_out.mean(dim=0, keepdim=True)
        self.center.mul_(self.center_momentum).add_(
            batch_center, alpha=1.0 - self.center_momentum
        )

    def forward(self, view1: torch.Tensor, view2: torch.Tensor) -> torch.Tensor:
        s1 = self._student(view1)
        s2 = self._student(view2)
        with torch.no_grad():
            t1 = self._teacher(view1)
            t2 = self._teacher(view2)
        loss = 0.5 * (self._cross_entropy(t1, s2) + self._cross_entropy(t2, s1))
        self._update_center(torch.cat([t1, t2], dim=0))
        return loss

    @torch.no_grad()
    def momentum_update(self, momentum: float) -> None:
        _ema_update(self.backbone, self.teacher_backbone, momentum)
        _ema_update(self.student_head, self.teacher_head, momentum)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_METHODS = {"byol", "mocov2", "simsiam", "dino"}


def build_method(
    method_name: str,
    backbone: nn.Module,
    feature_dim: int,
    ssl_config: dict[str, Any],
) -> SSLMethod:
    """Construct an SSL strategy by name from the resolved ``ssl`` config block.

    Args:
        method_name: One of ``"byol"``, ``"mocov2"``, ``"simsiam"``, ``"dino"``.
        backbone: Trunk built by :func:`build_ssl_encoder`.
        feature_dim: Trunk output dimension.
        ssl_config: The resolved ``ssl`` config dict (per-method sub-blocks read
            from ``ssl_config[method_name]`` when present).

    Returns:
        A configured :class:`SSLMethod` subclass instance.

    Raises:
        ValueError: If ``method_name`` is not a recognised SSL family member.
    """
    name = method_name.lower()
    if name not in _METHODS:
        raise ValueError(
            f"Unknown SSL method '{method_name}'. Allowed (INV-SSL-6): "
            f"{sorted(_METHODS)}."
        )

    if name == "byol":
        cfg = ssl_config.get("byol", {})
        return BYOL(
            backbone, feature_dim,
            proj_hidden=int(cfg.get("proj_hidden", 4096)),
            proj_out=int(cfg.get("proj_out", 256)),
            pred_hidden=int(cfg.get("pred_hidden", 4096)),
        )
    if name == "simsiam":
        cfg = ssl_config.get("simsiam", {})
        return SimSiam(
            backbone, feature_dim,
            proj_hidden=int(cfg.get("proj_hidden", 2048)),
            proj_out=int(cfg.get("proj_out", 2048)),
            pred_hidden=int(cfg.get("pred_hidden", 512)),
        )
    if name == "mocov2":
        cfg = ssl_config.get("mocov2", {})
        return MoCoV2(
            backbone, feature_dim,
            queue_size=int(cfg.get("queue_size", 8192)),
            moco_dim=int(cfg.get("moco_dim", 128)),
            temperature=float(cfg.get("temperature", 0.2)),
            ema=float(cfg.get("ema", 0.999)),
        )
    # dino
    cfg = ssl_config.get("dino", {})
    return DINO(
        backbone, feature_dim,
        out_dim=int(cfg.get("out_dim", 65536)),
        student_temp=float(cfg.get("student_temp", 0.1)),
        teacher_temp=float(cfg.get("teacher_temp", 0.07)),
        center_momentum=float(cfg.get("center_momentum", 0.9)),
    )
