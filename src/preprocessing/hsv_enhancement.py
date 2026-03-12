"""
Stage 5: HSV Contrast Enhancement.

Scales the S (saturation) and V (value/brightness) channels of the HSV
representation independently, then clips to the valid [0, 255] range before
converting back to BGR.  This provides additional contrast adjustment on top
of CLAHE without altering hue.
"""

import cv2
import numpy as np


def enhance_hsv(
    image: np.ndarray,
    saturation_scale: float = 1.2,
    value_scale: float = 1.1,
) -> np.ndarray:
    """
    Scale the S and V channels in HSV color space for contrast enhancement.

    Args:
        image: BGR uint8 image as a NumPy array.
        saturation_scale: Multiplicative factor for the S channel (>1 boosts saturation).
        value_scale: Multiplicative factor for the V channel (>1 brightens the image).

    Returns:
        Contrast-enhanced BGR uint8 image.
    """
    # Ensure uint8 input
    if image.dtype != np.uint8:
        image = np.clip(image * 255.0, 0, 255).astype(np.uint8)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)

    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value_scale, 0, 255)

    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
