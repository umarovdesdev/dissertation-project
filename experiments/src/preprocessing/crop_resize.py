"""
Stage 1: FOV Crop + Isotropic Resize + FOV Mask generation.

Replaces Hough-circle FOV detection (``fov.py``) with PIL-based foreground
detection from the spec.  Left/right edge pixels are sampled to estimate
background intensity; any pixel brighter than background + 10 is foreground.
The bounding box of the foreground mask is used as the crop region.

Isotropic scaling preserves the fundus circle geometry: the cropped region is
scaled to fit within ``target_size`` while maintaining aspect ratio, then
centered on a zero-padded canvas.  A binary mask (1.0 = real data, 0.0 =
padding) is returned alongside the image.

Fallback: center-square crop when FOV detection fails (non-landscape image or
bounding box too small).

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import cv2
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


def detect_is_cropped(image: np.ndarray) -> bool:
    """Detect whether the fundus circle is cropped by the camera frame.

    Uses three concordant checks:
    1. Circle fit test — max inscribed circle extends beyond image bounds.
    2. Border touch test — foreground mask touches image edges.
    3. Arc coverage test — contour arc length < 90% of expected circumference.

    Final decision: is_cropped = (not fits) OR touches_border OR (coverage < 0.9).

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).

    Returns:
        True if the fundus circle appears cropped.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Threshold to separate fundus from background
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)

    h, w = binary.shape

    # Check 1: Circle fit test via distance transform
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, max_r, _, max_loc = cv2.minMaxLoc(dist)
    cx, cy = max_loc
    margin = 2
    fits = (cx - max_r >= -margin and cx + max_r <= w + margin and
            cy - max_r >= -margin and cy + max_r <= h + margin)

    # Check 2: Border touch test
    touches_border = (
        binary[0, :].any() or           # top row
        binary[-1, :].any() or          # bottom row
        binary[:, 0].any() or           # left column
        binary[:, -1].any()             # right column
    )

    # Check 3: Arc coverage test
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    coverage = 1.0  # default: assume full circle
    if contours and max_r > 10:
        largest = max(contours, key=cv2.contourArea)
        arc_length = cv2.arcLength(largest, closed=False)
        expected_circumference = 2.0 * np.pi * max_r
        coverage = arc_length / expected_circumference if expected_circumference > 0 else 1.0

    return (not fits) or touches_border or (coverage < 0.9)


def crop_and_resize(
    image: np.ndarray,
    target_size: int = 512,
) -> tuple[np.ndarray, np.ndarray]:
    """Crop to the FOV region and resize to target_size × target_size.

    Uses isotropic scaling with centered padding to preserve the fundus
    circle geometry. Returns a binary mask indicating real pixel data
    (1.0) vs padding (0.0).

    FOV detection is attempted first; if it fails (non-landscape image or
    bounding box too small) a center-square crop is used as fallback.

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).
        target_size: Output spatial resolution in pixels (square).

    Returns:
        Tuple of:
          - image: RGB uint8 NumPy array of shape (target_size, target_size, 3).
          - mask: float32 NumPy array of shape (target_size, target_size)
                  with 1.0 where real data exists and 0.0 for padding.
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
    crop_w, crop_h = cropped.size

    # Isotropic resize: scale to fit within target_size, then pad
    scale = target_size / max(crop_h, crop_w)
    new_w = int(crop_w * scale)
    new_h = int(crop_h * scale)

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    resized_arr = np.array(resized, dtype=np.uint8)

    # Create canvas with zero padding
    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    y_off = (target_size - new_h) // 2
    x_off = (target_size - new_w) // 2
    canvas[y_off : y_off + new_h, x_off : x_off + new_w] = resized_arr

    # Binary mask: 1.0 where real data, 0.0 where padding
    mask = np.zeros((target_size, target_size), dtype=np.float32)
    mask[y_off : y_off + new_h, x_off : x_off + new_w] = 1.0

    return canvas, mask
