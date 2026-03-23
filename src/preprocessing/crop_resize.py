"""
Stage 1 (V4): FOV Crop + Resize.

Replaces Hough-circle FOV detection (V3 ``fov.py``) with PIL-based foreground
detection from the V4 spec.  Left/right edge pixels are sampled to estimate
background intensity; any pixel brighter than background + 10 is foreground.
The bounding box of the foreground mask is used as the crop region.

Fallback: center-square crop when FOV detection fails (non-landscape image or
bounding box too small).

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter


def detect_fov_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    """
    Detect the fundus FOV bounding box using PIL-based foreground detection.

    Samples the leftmost and rightmost ``w // 32`` columns to estimate the
    background level per channel, then finds the bounding box of all pixels
    that exceed ``max_bg + 10``.  Detection is only attempted for landscape
    images (``w > 1.2 * h``); returns ``None`` for square/portrait images.

    Args:
        image: PIL Image in RGB mode.

    Returns:
        ``(left, upper, right, lower)`` bounding box, or ``None`` if
        detection fails or the detected region is too small (< 0.8 × h in
        either dimension).
    """
    blurred = image.filter(ImageFilter.BLUR)
    ba = np.array(blurred)          # (H, W, 3) uint8
    h, w, _ = ba.shape

    if w > 1.2 * h:
        left_max = ba[:, : w // 32, :].max(axis=(0, 1)).astype(int)   # (3,)
        right_max = ba[:, -w // 32 :, :].max(axis=(0, 1)).astype(int) # (3,)
        max_bg = np.maximum(left_max, right_max)                       # (3,)

        # Foreground: any channel exceeds background + 10
        foreground = (ba > max_bg + 10).any(axis=2).astype(np.uint8)  # (H, W)

        bbox = Image.fromarray(foreground).getbbox()

        if bbox is not None:
            left, upper, right, lower = bbox
            if (right - left) < 0.8 * h or (lower - upper) < 0.8 * h:
                bbox = None

        return bbox  # may be None after the size check

    return None


def crop_and_resize(
    image: np.ndarray,
    target_size: int = 512,
) -> np.ndarray:
    """
    Crop to the FOV region and resize to ``target_size × target_size``.

    FOV detection is attempted first; if it fails (non-landscape image or
    bounding box too small) a center-square crop is used as fallback.

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        target_size: Output spatial resolution in pixels (square).

    Returns:
        RGB uint8 NumPy array of shape ``(target_size, target_size, 3)``.
    """
    pil_img = Image.fromarray(image)
    w, h = pil_img.size  # PIL: (width, height)

    bbox = detect_fov_bbox(pil_img)

    if bbox is None:
        # Fallback: center-square crop
        left = max((w - h) // 2, 0)
        upper = 0
        right = min(w - (w - h) // 2, w)
        lower = h
        bbox = (left, upper, right, lower)

    cropped = pil_img.crop(bbox)
    resized = cropped.resize([target_size, target_size])
    return np.array(resized, dtype=np.uint8)
