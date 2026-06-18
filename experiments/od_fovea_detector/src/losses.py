"""Training losses: DSNT (euclidean + JS) and a heatmap-MSE/BCE baseline.

Two losses behind a config flag (``loss.type``):

  * ``"dsnt"`` — the recommended recipe (Nibali et al.): Euclidean distance
    between the predicted soft-argmax coordinate and the GT coordinate, plus a
    Jensen-Shannon divergence regularizer keeping each heatmap a compact
    Gaussian. No per-pixel target needed.

  * ``"heatmap"`` — the FundusPosNet-style per-pixel loss (MSE or BCE) on the
    rendered Gaussian target heatmaps. Useful as a comparison baseline.

Requires torch.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from .dsnt import js_reg_loss


class DSNTLoss(nn.Module):
    """Euclidean coordinate loss + JS-divergence heatmap regularizer."""

    def __init__(self, js_weight: float = 1.0, sigma_norm: float = 0.04) -> None:
        """Initialize.

        Args:
            js_weight: Weight on the JS regularization term.
            sigma_norm: Target Gaussian sigma (normalized units) for JS.
        """
        super().__init__()
        self.js_weight = js_weight
        self.sigma_norm = sigma_norm

    def forward(
        self,
        out: dict[str, torch.Tensor],
        coords_gt: torch.Tensor,
    ) -> tuple[torch.Tensor, dict[str, float]]:
        """Compute the DSNT loss.

        Args:
            out: Model output dict (needs ``coords`` and ``heatmap``).
            coords_gt: GT coords ``(B, C, 2)`` in normalized ``[-1, 1]``.

        Returns:
            ``(loss, parts)`` where ``parts`` logs the euclidean and JS terms.
        """
        coords = out["coords"]
        prob = out["heatmap"]
        euc = torch.sqrt(((coords - coords_gt) ** 2).sum(dim=-1) + 1e-12).mean()
        js = js_reg_loss(prob, coords, self.sigma_norm)
        loss = euc + self.js_weight * js
        return loss, {"euclidean": float(euc.detach()),
                      "js": float(js.detach())}


class HeatmapLoss(nn.Module):
    """Per-pixel MSE or BCE on the rendered Gaussian target heatmaps."""

    def __init__(self, mode: str = "mse") -> None:
        """Initialize.

        Args:
            mode: ``"mse"`` or ``"bce"``.
        """
        super().__init__()
        if mode not in {"mse", "bce"}:
            raise ValueError(f"unknown heatmap loss mode: {mode}")
        self.mode = mode

    def forward(
        self,
        out: dict[str, torch.Tensor],
        target_heatmaps: torch.Tensor,
    ) -> tuple[torch.Tensor, dict[str, float]]:
        """Compute the heatmap loss.

        Args:
            out: Model output dict (needs ``heatmap`` and ``heatmap_logits``).
            target_heatmaps: Target maps ``(B, C, H, W)`` summing to 1.

        Returns:
            ``(loss, parts)``.
        """
        if self.mode == "mse":
            pred = out["heatmap"]
            loss = F.mse_loss(pred, target_heatmaps)
        else:
            # BCE on a normalized target rescaled to its own peak (in [0, 1]).
            tgt = target_heatmaps / target_heatmaps.amax(
                dim=(-2, -1), keepdim=True).clamp_min(1e-12)
            loss = F.binary_cross_entropy_with_logits(
                out["heatmap_logits"], tgt)
        return loss, {self.mode: float(loss.detach())}


def build_loss(loss_cfg: dict, sigma_norm: float) -> nn.Module:
    """Construct the configured loss module.

    Args:
        loss_cfg: The ``loss`` section of the config.
        sigma_norm: Target Gaussian sigma in normalized units (for DSNT JS).

    Returns:
        A loss ``nn.Module``. Its ``forward`` takes ``(out, target)`` where
        ``target`` is normalized coords for DSNT or target heatmaps otherwise.
    """
    if loss_cfg.get("type", "dsnt") == "dsnt":
        return DSNTLoss(js_weight=loss_cfg.get("js_weight", 1.0),
                        sigma_norm=sigma_norm)
    return HeatmapLoss(mode=loss_cfg.get("heatmap_loss", "mse"))
