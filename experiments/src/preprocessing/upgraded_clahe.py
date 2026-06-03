"""
Stage 3: Upgraded CLAHE on the L-Channel.

Replaces cv2.createCLAHE-based CLAHE (``clahe.py``) with a custom
tile-by-tile implementation that enforces a *dual* clip constraint:

    clip_limit = min(clip_factor × tile_area / 256,
                     global_threshold × tile_area)

Excess histogram counts are redistributed uniformly across all 256 bins
before CDF-based equalisation.  Operates on the L-channel of LAB color space;
input and output are RGB uint8 arrays.

At train time CLAHE is applied stochastically (default 80 % probability)
via :func:`maybe_apply_clahe`; at inference it is always applied.

References
----------
Work 1: retinal-disease-upgraded-clahe (STARE dataset, ResNet-50 TL).
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

@dataclass
class ClaheParams:
    """
    Parameters for the upgraded CLAHE algorithm.

    Args:
        tile_grid_size: Number of tiles along (rows, cols).
        clip_factor: Scale factor for the per-tile clip limit
            (``clip_factor × tile_area / 256``).
        global_threshold: Additional global constraint expressed as a
            fraction of tile area (``global_threshold × tile_area``).
            Set to ``0`` to disable the global constraint.
    """

    tile_grid_size: tuple[int, int] = (8, 8)
    clip_factor: float = 2.0
    global_threshold: float = 0.01


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _clip_histogram(
    hist: np.ndarray,
    clip_limit: float,
) -> np.ndarray:
    """
    Clip a histogram at *clip_limit* and redistribute the excess uniformly.

    Excess counts are spread evenly across all 256 bins; any integer
    remainder is added to the lowest bins first.

    Args:
        hist: Float32 array of length 256.
        clip_limit: Maximum allowed count per bin before redistribution.

    Returns:
        Clipped and redistributed float32 histogram of length 256.
    """
    excess = np.maximum(hist - clip_limit, 0.0)
    clipped = hist - excess
    redistribute = excess.sum()

    if redistribute > 0:
        clipped += redistribute // 256
        remainder = int(redistribute % 256)
        if remainder > 0:
            clipped[:remainder] += 1

    return clipped


def _tile_histogram_equalization(
    tile: np.ndarray,
    clip_limit: float,
) -> np.ndarray:
    """
    Equalise a single image tile using a clipped, redistributed histogram.

    Args:
        tile: 2-D uint8 array (a sub-region of the L-channel).
        clip_limit: Clip limit passed to :func:`_clip_histogram`.

    Returns:
        Equalised uint8 array with the same shape as *tile*.
    """
    hist, _ = np.histogram(tile.flatten(), bins=256, range=(0, 256))
    hist = hist.astype(np.float32)

    clipped = _clip_histogram(hist, clip_limit)

    cdf = np.cumsum(clipped)
    cdf_min = cdf.min()
    cdf_range = cdf.max() - cdf_min
    cdf_norm = (cdf - cdf_min) / (cdf_range + 1e-6)
    lut = np.clip(cdf_norm * 255.0, 0, 255).astype(np.uint8)

    return lut[tile]


def upgraded_clahe_l_channel(
    l_channel: np.ndarray,
    params: ClaheParams,
) -> np.ndarray:
    """
    Apply upgraded CLAHE tile-by-tile to a single-channel luminance image.

    Each tile's clip limit is computed with the dual constraint::

        clip_limit = clip_factor × tile_area / 256
        if global_threshold > 0:
            clip_limit = min(clip_limit, global_threshold × tile_area)

    Args:
        l_channel: 2-D uint8 array (L-channel from LAB conversion).
        params: :class:`ClaheParams` controlling tile size and clip limits.

    Returns:
        Enhanced 2-D uint8 array with the same shape as *l_channel*.
    """
    height, width = l_channel.shape
    tiles_y, tiles_x = params.tile_grid_size
    tile_h = max(height // tiles_y, 1)
    tile_w = max(width // tiles_x, 1)
    enhanced = np.zeros_like(l_channel)

    for y in range(0, height, tile_h):
        for x in range(0, width, tile_w):
            tile = l_channel[y : y + tile_h, x : x + tile_w]
            tile_area = tile.size

            clip_limit = params.clip_factor * (tile_area / 256)
            if params.global_threshold > 0:
                clip_limit = min(clip_limit, params.global_threshold * tile_area)

            enhanced[y : y + tile_h, x : x + tile_w] = _tile_histogram_equalization(
                tile, clip_limit
            )

    return enhanced


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def apply_upgraded_clahe(
    image_rgb: np.ndarray,
    params: ClaheParams | None = None,
) -> np.ndarray:
    """
    Apply upgraded CLAHE to the L-channel of an RGB image.

    Converts RGB→LAB, enhances the L-channel with tile-level clipped
    histogram equalisation, then converts LAB→RGB.

    Args:
        image_rgb: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        params: :class:`ClaheParams` instance.  Uses default values if
            ``None``.

    Returns:
        Enhanced RGB uint8 NumPy array of shape ``(H, W, 3)``.
    """
    if params is None:
        params = ClaheParams()

    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)

    l_enhanced = upgraded_clahe_l_channel(l_ch, params)

    merged = cv2.merge((l_enhanced, a_ch, b_ch))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)


def maybe_apply_clahe(
    image_rgb: np.ndarray,
    params: ClaheParams | None = None,
    is_training: bool = True,
    train_prob: float = 0.8,
) -> np.ndarray:
    """
    Apply upgraded CLAHE with stochastic skip during training.

    At inference (``is_training=False``) CLAHE is always applied.
    During training it is applied with probability *train_prob*; the image
    is returned unchanged for the remaining ``1 - train_prob`` fraction.

    Args:
        image_rgb: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        params: :class:`ClaheParams` instance.  Uses defaults if ``None``.
        is_training: ``True`` during training, ``False`` at inference.
        train_prob: Probability of applying CLAHE at train time (default 0.8).

    Returns:
        Processed (or unchanged) RGB uint8 NumPy array.
    """
    if is_training and np.random.rand() > train_prob:
        return image_rgb  # skip
    return apply_upgraded_clahe(image_rgb, params)
