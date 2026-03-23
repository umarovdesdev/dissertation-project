"""
Stage 2 (V4): Flat-Field Correction.

Reduces uneven illumination by subtracting a heavily blurred version of the
image and re-centering at 128:

    corrected = image − GaussianBlur(image, σ) + 128

A large σ (default 45) captures only the low-frequency illumination gradient,
so the subtraction removes broad brightness variation while preserving local
vessel and lesion detail.

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import cv2
import numpy as np


def apply_flat_field(
    image: np.ndarray,
    sigma: float = 45.0,
) -> np.ndarray:
    """
    Apply flat-field correction to reduce uneven illumination.

    Algorithm::

        blur      = GaussianBlur(image, σ)
        corrected = image − blur + 128

    Kernel size is derived automatically from *sigma* (passed as ``(0, 0)``
    to :func:`cv2.GaussianBlur`).

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        sigma: Gaussian blur σ controlling the spatial scale of the
            illumination estimate.  Default ``45.0`` from V4 spec.

    Returns:
        Corrected RGB uint8 NumPy array of shape ``(H, W, 3)``.
    """
    blur = cv2.GaussianBlur(image, (0, 0), sigma)
    corrected = image.astype(np.float32) - blur.astype(np.float32) + 128.0
    return np.clip(corrected, 0, 255).astype(np.uint8)
