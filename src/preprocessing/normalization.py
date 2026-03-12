"""
Stage 3: Pixel Normalization.

Converts a uint8 BGR image to float32 with pixel values in [0, 1].
"""

import numpy as np


def normalize_pixels(image: np.ndarray) -> np.ndarray:
    """
    Normalize pixel intensities to the [0, 1] range.

    Args:
        image: BGR uint8 image as a NumPy array.

    Returns:
        Float32 array of the same spatial shape with values in [0.0, 1.0].
    """
    return image.astype(np.float32) / 255.0
