"""Vendored DSNT (Differentiable Spatial-to-Numerical Transform) primitives.

DSNT (Nibali et al., 2018; reused in ``anibali/dsntnn`` and
``kornia.geometry.dsnt``) decodes a spatial heatmap into sub-pixel coordinates
via a differentiable soft-argmax, with no learnable parameters. We vendor a
compact implementation (Apache-2.0-compatible; the algorithm is from the
public paper) so the project runs without requiring ``kornia``/``dsntnn`` to
be installed, while remaining a drop-in for either.

Coordinate convention: normalized coordinates in ``[-1, 1]`` along each axis
(``-1`` = first pixel center region, ``+1`` = last), matching dsntnn. Helpers
are provided to convert to/from absolute heatmap-pixel coordinates.

Two layers of API:
  * torch functions (``spatial_softmax``, ``dsnt`` , ``js_reg_loss``,
    ``dsnt_second_moments``) — used by the model and losses;
  * a pure-numpy mirror (``np_*``) — used by ``confidence.py`` and tests so the
    decoding logic can be exercised without torch.
"""

from __future__ import annotations

import numpy as np

try:  # torch is optional at import time (torch-free tests + numpy path).
    import torch
    import torch.nn.functional as F
    _HAS_TORCH = True
except Exception:  # pragma: no cover - exercised only when torch absent
    torch = None  # type: ignore
    F = None  # type: ignore
    _HAS_TORCH = False


# ---------------------------------------------------------------------------
# Normalized coordinate grids
# ---------------------------------------------------------------------------
def _linspace_centers(n: int) -> np.ndarray:
    """Normalized centers in ``[-1, 1]`` for ``n`` pixels (dsntnn convention).

    Args:
        n: Number of pixels along the axis.

    Returns:
        float64 array of length ``n`` with values ``(2*i + 1)/n - 1``.
    """
    i = np.arange(n, dtype=np.float64)
    return (2.0 * i + 1.0) / n - 1.0


def norm_to_pixel(coord_norm: np.ndarray | float, n: int) -> np.ndarray:
    """Convert a normalized coordinate in ``[-1, 1]`` to pixel index space."""
    return (np.asarray(coord_norm) + 1.0) * n / 2.0 - 0.5


def pixel_to_norm(coord_px: np.ndarray | float, n: int) -> np.ndarray:
    """Convert a pixel-index coordinate to normalized ``[-1, 1]`` space."""
    return (2.0 * (np.asarray(coord_px) + 0.5)) / n - 1.0


# ---------------------------------------------------------------------------
# Pure-numpy mirror (no torch) — used by confidence.py and tests
# ---------------------------------------------------------------------------
def np_spatial_softmax(heatmap: np.ndarray) -> np.ndarray:
    """Softmax-normalize a ``(..., H, W)`` heatmap over its spatial dims.

    Args:
        heatmap: Array with the last two axes spatial.

    Returns:
        Array of the same shape summing to 1 over the last two axes.
    """
    h = heatmap.astype(np.float64)
    flat = h.reshape(*h.shape[:-2], -1)
    flat = flat - flat.max(axis=-1, keepdims=True)
    e = np.exp(flat)
    e /= e.sum(axis=-1, keepdims=True)
    return e.reshape(h.shape)


def np_dsnt(prob: np.ndarray) -> tuple[float, float]:
    """Soft-argmax of a single normalized 2D heatmap (numpy).

    Args:
        prob: float array ``(H, W)`` summing to 1.

    Returns:
        ``(x_norm, y_norm)`` expected coordinate in ``[-1, 1]``.
    """
    h, w = prob.shape
    xs = _linspace_centers(w)
    ys = _linspace_centers(h)
    px = prob.sum(axis=0)  # marginal over rows -> length w
    py = prob.sum(axis=1)  # marginal over cols -> length h
    x = float((px * xs).sum())
    y = float((py * ys).sum())
    return x, y


def np_second_moments(prob: np.ndarray) -> tuple[float, float]:
    """Spatial variances (Var_x, Var_y) of a 2D heatmap in pixel^2 units.

    Args:
        prob: float array ``(H, W)`` summing to 1.

    Returns:
        ``(var_x, var_y)`` in heatmap-pixel^2.
    """
    h, w = prob.shape
    xs = np.arange(w, dtype=np.float64)
    ys = np.arange(h, dtype=np.float64)
    px = prob.sum(axis=0)
    py = prob.sum(axis=1)
    mx = (px * xs).sum()
    my = (py * ys).sum()
    var_x = float((px * (xs - mx) ** 2).sum())
    var_y = float((py * (ys - my) ** 2).sum())
    return var_x, var_y


# ---------------------------------------------------------------------------
# Torch path — used by model.py and losses.py
# ---------------------------------------------------------------------------
if _HAS_TORCH:

    def spatial_softmax(heatmap: "torch.Tensor") -> "torch.Tensor":
        """Softmax-normalize ``(B, C, H, W)`` heatmaps over spatial dims.

        Args:
            heatmap: Raw logits ``(B, C, H, W)``.

        Returns:
            Probability maps ``(B, C, H, W)`` summing to 1 over ``(H, W)``.
        """
        b, c, h, w = heatmap.shape
        flat = heatmap.reshape(b, c, h * w)
        flat = F.softmax(flat, dim=-1)
        return flat.reshape(b, c, h, w)

    def _coord_grids(h: int, w: int, device, dtype):
        xs = torch.from_numpy(_linspace_centers(w)).to(device=device, dtype=dtype)
        ys = torch.from_numpy(_linspace_centers(h)).to(device=device, dtype=dtype)
        return xs, ys

    def dsnt(prob: "torch.Tensor") -> "torch.Tensor":
        """Differentiable soft-argmax of normalized heatmaps.

        Args:
            prob: Probability maps ``(B, C, H, W)`` summing to 1 spatially.

        Returns:
            Coordinates ``(B, C, 2)`` in normalized ``[-1, 1]`` space (x, y).
        """
        b, c, h, w = prob.shape
        xs, ys = _coord_grids(h, w, prob.device, prob.dtype)
        px = prob.sum(dim=2)          # (B, C, W)
        py = prob.sum(dim=3)          # (B, C, H)
        x = (px * xs).sum(dim=-1)     # (B, C)
        y = (py * ys).sum(dim=-1)     # (B, C)
        return torch.stack([x, y], dim=-1)

    def dsnt_second_moments(prob: "torch.Tensor") -> "torch.Tensor":
        """Spatial variances (Var_x, Var_y) per heatmap, in pixel^2 units.

        Args:
            prob: Probability maps ``(B, C, H, W)`` summing to 1 spatially.

        Returns:
            ``(B, C, 2)`` tensor of ``(var_x, var_y)`` in heatmap-pixel^2.
        """
        b, c, h, w = prob.shape
        xs = torch.arange(w, device=prob.device, dtype=prob.dtype)
        ys = torch.arange(h, device=prob.device, dtype=prob.dtype)
        px = prob.sum(dim=2)
        py = prob.sum(dim=3)
        mx = (px * xs).sum(dim=-1, keepdim=True)
        my = (py * ys).sum(dim=-1, keepdim=True)
        var_x = (px * (xs - mx) ** 2).sum(dim=-1)
        var_y = (py * (ys - my) ** 2).sum(dim=-1)
        return torch.stack([var_x, var_y], dim=-1)

    def _make_gauss(coords: "torch.Tensor", h: int, w: int, sigma_norm: float):
        """Render normalized-coordinate Gaussians for the JS regularizer."""
        xs, ys = _coord_grids(h, w, coords.device, coords.dtype)
        cx = coords[..., 0:1].unsqueeze(-1)   # (B, C, 1, 1)
        cy = coords[..., 1:2].unsqueeze(-1)
        gx = torch.exp(-((xs.view(1, 1, 1, w) - cx) ** 2) / (2 * sigma_norm ** 2))
        gy = torch.exp(-((ys.view(1, 1, h, 1) - cy) ** 2) / (2 * sigma_norm ** 2))
        g = gx * gy
        g = g / g.sum(dim=(-2, -1), keepdim=True).clamp_min(1e-12)
        return g

    def js_reg_loss(
        prob: "torch.Tensor",
        coords: "torch.Tensor",
        sigma_norm: float,
    ) -> "torch.Tensor":
        """Jensen-Shannon divergence regularizer (dsntnn recipe).

        Encourages each predicted heatmap to stay a compact Gaussian centered
        on its soft-argmax coordinate.

        Args:
            prob: Probability maps ``(B, C, H, W)``.
            coords: Soft-argmax coords ``(B, C, 2)`` in ``[-1, 1]``.
            sigma_norm: Target Gaussian sigma in normalized units.

        Returns:
            Scalar JS divergence averaged over batch and channels.
        """
        b, c, h, w = prob.shape
        target = _make_gauss(coords.detach(), h, w, sigma_norm)
        eps = 1e-12
        m = 0.5 * (prob + target)
        kl_pm = (prob * (torch.log(prob + eps) - torch.log(m + eps))).sum(dim=(-2, -1))
        kl_tm = (target * (torch.log(target + eps) - torch.log(m + eps))).sum(dim=(-2, -1))
        js = 0.5 * (kl_pm + kl_tm)
        return js.mean()
