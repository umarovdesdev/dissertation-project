"""
Stage 2: CLAHE Enhancement in LAB Color Space.

CLAHE (Contrast Limited Adaptive Histogram Equalization) is applied to the
L-channel of the LAB representation.  Operating on L only preserves hue and
saturation while enhancing local contrast in the luminance dimension.

Also provides apply_clahe_sweep() for the H-2 parameter sweep experiment
(Experiment 2: component ablation with varying clip limits).
"""

from __future__ import annotations

import cv2
import numpy as np


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """
    Apply CLAHE to the L-channel of a BGR image converted to LAB color space.

    Args:
        image: BGR uint8 image as a NumPy array.
        clip_limit: Threshold for contrast limiting (higher → stronger enhancement).
        grid_size: Size of the grid tiles for local histogram equalization (rows, cols).

    Returns:
        Contrast-enhanced BGR uint8 image.
    """
    # Convert to uint8 if float input provided (pipeline may pass float after normalize)
    if image.dtype != np.uint8:
        image = np.clip(image * 255.0, 0, 255).astype(np.uint8)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    l_enhanced = clahe.apply(l_ch)

    enhanced_lab = cv2.merge([l_enhanced, a_ch, b_ch])
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)


def apply_clahe_sweep(
    image: np.ndarray,
    clip_limits: list[float] | None = None,
    grid_size: tuple[int, int] = (8, 8),
) -> dict[float, np.ndarray]:
    """
    Apply CLAHE at multiple clip limits for the H-2 parameter sweep experiment.

    Used in Experiment 2 (component ablation) to identify the optimal clip
    limit configuration as required by the dynamic clip limit specification
    (RESEARCH_ARCHITECTURE §3.2).

    Args:
        image: BGR uint8 image as a NumPy array.
        clip_limits: List of clip limit values to sweep.  Defaults to
            [1.0, 2.0, 3.0, 4.0, 6.0, 8.0].
        grid_size: Tile grid size passed to each CLAHE instance.

    Returns:
        Dict mapping each clip_limit value to the corresponding enhanced image.
    """
    if clip_limits is None:
        clip_limits = [1.0, 2.0, 3.0, 4.0, 6.0, 8.0]

    return {cl: apply_clahe(image, clip_limit=cl, grid_size=grid_size) for cl in clip_limits}
