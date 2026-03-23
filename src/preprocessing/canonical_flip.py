"""
Stage 0 (V4): Canonical Orientation.

Detects left/right eye from the image filename and dataset convention, then
horizontally flips left-eye images so all images share right-eye canonical
orientation (optic disc on the right, macula on the left).

Input/output images are RGB uint8 NumPy arrays.  Callers must convert
BGR→RGB before entering the V4 pipeline.

Dataset support
---------------
- eyepacs   — filename contains ``_left`` or ``_right`` before the extension
- aptos2019 — no L/R info in filename → ``"unknown"``
- idrid     — no L/R info in filename → ``"unknown"``
- ddr       — no L/R info in filename → ``"unknown"``
- odir5k    — L/R determined by CSV columns at dataset level → ``"unknown"``
- rfmid     — no L/R info in filename → ``"unknown"``
"""

from __future__ import annotations

import pathlib

import cv2
import numpy as np

# Datasets whose filenames encode left/right
_FILENAME_ENCODED: frozenset[str] = frozenset({"eyepacs"})


def detect_eye_side(filename: str, dataset_name: str) -> str:
    """
    Detect whether an image is a left or right eye fundus photograph.

    Args:
        filename: Image filename (e.g. ``"10_left.jpeg"``, ``"IDRiD_001.jpg"``).
            Only the stem (filename without extension) is inspected.
        dataset_name: One of ``"eyepacs"``, ``"aptos2019"``, ``"idrid"``,
            ``"ddr"``, ``"odir5k"``, ``"rfmid"``.

    Returns:
        ``"left"``, ``"right"``, or ``"unknown"`` when the side cannot be
        determined from the filename.
    """
    if dataset_name not in _FILENAME_ENCODED:
        return "unknown"

    stem = pathlib.Path(filename).stem.lower()
    if "_left" in stem:
        return "left"
    if "_right" in stem:
        return "right"
    return "unknown"


def canonical_flip(image: np.ndarray, eye_side: str) -> np.ndarray:
    """
    Flip a left-eye image to right-eye canonical orientation.

    Right-eye canonical: optic disc on the right, macula on the left.
    Left-eye images are mirrored horizontally.  Right-eye and unknown
    images are returned unchanged (no copy is made).

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        eye_side: ``"left"``, ``"right"``, or ``"unknown"``.

    Returns:
        Horizontally flipped array for ``"left"``; original array otherwise.
    """
    if eye_side == "left":
        return cv2.flip(image, 1)
    return image
