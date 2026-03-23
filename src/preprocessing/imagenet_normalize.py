"""
Stage 4 (V4): ImageNet Normalisation.

Replaces simple ÷255 normalisation (V3 ``normalization.py``) with the
ImageNet-standard pipeline:

    1. ``ToTensor``  — HWC uint8 → CHW float32 in [0, 1]
    2. ``Normalize`` — channel-wise (x − mean) / std

Output is a ``torch.Tensor`` of shape ``(3, H, W)``, ready for CNN input.

Input images must be RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import numpy as np
import torch
from torchvision import transforms


def imagenet_normalize(
    image: np.ndarray,
    mean: tuple[float, float, float] = (0.485, 0.456, 0.406),
    std: tuple[float, float, float] = (0.229, 0.224, 0.225),
) -> torch.Tensor:
    """
    Convert an RGB uint8 image to a normalised float32 CHW tensor.

    Applies ``ToTensor`` (HWC uint8 → CHW float32 in [0, 1]) followed by
    channel-wise normalisation with ImageNet mean and std.

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        mean: Per-channel mean for normalisation.
        std: Per-channel standard deviation for normalisation.

    Returns:
        Float32 tensor of shape ``(3, H, W)``.
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=list(mean), std=list(std)),
    ])
    return transform(image)
