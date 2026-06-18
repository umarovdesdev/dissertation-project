"""Heatmap -> coordinate + genuine confidence.

Per brief §7, confidence is a real quantity derived from the predicted
heatmap, not a boolean that is always true (the failure mode of the old
classical detector). From the softmax-normalized heatmap ``H`` (sums to 1):

  * peak ``p_max = max(H)``;
  * spread ``sigma_eff = sqrt(Var_x + Var_y)`` from DSNT second moments;
  * ``confidence = exp(-sigma_eff / sigma_ref)`` in ``(0, 1]``.

A sharp, unimodal peak -> small ``sigma_eff`` -> confidence near 1. A diffuse
or multi-modal map -> large ``sigma_eff`` -> confidence near 0. The threshold
is calibrated on a held-out slice (see ``eval.py`` for the sigma_eff-vs-error
Spearman correlation that justifies it).

This module is pure numpy (no torch) so it can run inside the inference path
and be unit-tested without torch.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dsnt import np_dsnt, np_second_moments, np_spatial_softmax, norm_to_pixel


@dataclass
class HeatmapDecode:
    """Decoded landmark from a single heatmap.

    Attributes:
        x: Sub-pixel x in heatmap-grid pixels.
        y: Sub-pixel y in heatmap-grid pixels.
        p_max: Peak probability of the softmax-normalized map.
        sigma_eff: ``sqrt(Var_x + Var_y)`` spatial spread (heatmap pixels).
        confidence: Confidence in ``[0, 1]`` (high peak + low spread).
    """

    x: float
    y: float
    p_max: float
    sigma_eff: float
    confidence: float


def decode_heatmap(
    heatmap: np.ndarray,
    sigma_ref: float,
    already_prob: bool = True,
) -> HeatmapDecode:
    """Decode one heatmap to a coordinate + confidence (numpy DSNT).

    Args:
        heatmap: float array ``(H, W)``. If ``already_prob`` it must sum to 1;
            otherwise it is treated as logits and softmax-normalized first.
        sigma_ref: Reference spread for ``confidence = exp(-sigma_eff/sigma_ref)``,
            in heatmap-grid pixels.
        already_prob: Whether ``heatmap`` is already a probability map.

    Returns:
        A :class:`HeatmapDecode`.
    """
    if heatmap.ndim != 2:
        raise ValueError(f"expected 2D heatmap, got shape {heatmap.shape}")
    prob = heatmap.astype(np.float64)
    if already_prob:
        s = prob.sum()
        prob = prob / s if s > 0 else np_spatial_softmax(prob)
    else:
        prob = np_spatial_softmax(prob)

    h, w = prob.shape
    x_norm, y_norm = np_dsnt(prob)
    x_px = float(norm_to_pixel(x_norm, w))
    y_px = float(norm_to_pixel(y_norm, h))

    var_x, var_y = np_second_moments(prob)
    sigma_eff = float(np.sqrt(max(var_x + var_y, 0.0)))
    p_max = float(prob.max())

    sigma_ref = max(float(sigma_ref), 1e-6)
    confidence = float(np.exp(-sigma_eff / sigma_ref))
    confidence = max(0.0, min(1.0, confidence))

    return HeatmapDecode(
        x=x_px, y=y_px, p_max=p_max, sigma_eff=sigma_eff, confidence=confidence,
    )
