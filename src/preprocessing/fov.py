"""
Stage 1: FOV Standardization.

Detects the circular fundus region via Hough transform, crops to the circle
bounding box to remove black borders, centers and resizes to target_size×target_size.
Falls back to a center-crop + resize if no circle is detected.
"""

import cv2
import numpy as np


def standardize_fov(image: np.ndarray, target_size: int = 512) -> np.ndarray:
    """
    Detect the fundus circle and crop/resize to target_size×target_size.

    Detection uses HoughCircles on a blurred grayscale image.  If no circle
    is found the image is center-cropped to a square and resized.

    Args:
        image: BGR image as a NumPy uint8 array.
        target_size: Output spatial resolution (pixels, square).

    Returns:
        BGR image of shape (target_size, target_size, 3).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    h, w = image.shape[:2]
    min_radius = int(min(h, w) * 0.3)
    max_radius = int(min(h, w) * 0.6)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=min(h, w) * 0.5,
        param1=50,
        param2=30,
        minRadius=min_radius,
        maxRadius=max_radius,
    )

    if circles is not None:
        cx, cy, r = np.round(circles[0, 0]).astype(int)
        # Bounding box with small padding
        pad = int(r * 0.02)
        x1 = max(cx - r - pad, 0)
        y1 = max(cy - r - pad, 0)
        x2 = min(cx + r + pad, w)
        y2 = min(cy + r + pad, h)
        cropped = image[y1:y2, x1:x2]
    else:
        # Fallback: center-crop to the largest square
        side = min(h, w)
        y1 = (h - side) // 2
        x1 = (w - side) // 2
        cropped = image[y1 : y1 + side, x1 : x1 + side]

    return cv2.resize(cropped, (target_size, target_size), interpolation=cv2.INTER_LANCZOS4)
