"""
Stage 2: Green Channel Extraction.

The green channel provides the highest vessel-to-background contrast in
retinal fundus images.  The extracted channel is replicated across three
channels so downstream CNN models receive a standard 3-channel input.
"""

import cv2
import numpy as np


def extract_green_channel(image: np.ndarray) -> np.ndarray:
    """
    Extract the green channel (index 1 in BGR) and return a 3-channel image.

    All three output channels are filled with the green channel values so
    that models expecting RGB input continue to work without modification.

    Args:
        image: BGR image as a NumPy uint8 array.

    Returns:
        BGR uint8 image where B == G == R == original green channel.
    """
    green = image[:, :, 1]
    return cv2.merge([green, green, green])
