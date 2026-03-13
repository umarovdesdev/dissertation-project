"""Data augmentation for fundus images (separate from preprocessing per OD-3)."""

import random

import cv2
import numpy as np


class FundusAugmentation:
    """Augmentation transforms for fundus images during training.

    Applies spatial and photometric transforms using OpenCV only.
    Augmentation is intentionally separate from the preprocessing
    pipeline to enable clean ablation studies (OD-3).

    Args:
        config: Dict with augmentation parameters:
            - horizontal_flip (bool): Mirror left-right.
            - vertical_flip (bool): Mirror top-bottom.
            - rotation_degrees (float): Max rotation in degrees (±value).
            - zoom_range (float): Zoom fraction (±value, e.g. 0.1 = ±10%).
            - brightness_range (list[float, float]): Multiplicative
              brightness scale range, e.g. [0.9, 1.1].
    """

    def __init__(self, config: dict) -> None:
        self.horizontal_flip: bool = config.get("horizontal_flip", True)
        self.vertical_flip: bool = config.get("vertical_flip", False)
        self.rotation_degrees: float = float(config.get("rotation_degrees", 15))
        self.zoom_range: float = float(config.get("zoom_range", 0.10))
        brightness = config.get("brightness_range", [0.9, 1.1])
        self.brightness_min: float = float(brightness[0])
        self.brightness_max: float = float(brightness[1])

    def __call__(self, image: np.ndarray) -> np.ndarray:
        """Apply random augmentation transforms to one image.

        Args:
            image: HWC numpy array, uint8 or float32 [0,1].

        Returns:
            Augmented image with same shape, dtype, and value range.
        """
        image = self._maybe_flip(image)
        image = self._maybe_rotate(image)
        image = self._maybe_zoom(image)
        image = self._maybe_brightness(image)
        return image

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _maybe_flip(self, image: np.ndarray) -> np.ndarray:
        if self.horizontal_flip and random.random() < 0.5:
            image = cv2.flip(image, 1)
        if self.vertical_flip and random.random() < 0.5:
            image = cv2.flip(image, 0)
        return image

    def _maybe_rotate(self, image: np.ndarray) -> np.ndarray:
        if self.rotation_degrees == 0:
            return image
        angle = random.uniform(-self.rotation_degrees, self.rotation_degrees)
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REFLECT_101)

    def _maybe_zoom(self, image: np.ndarray) -> np.ndarray:
        if self.zoom_range == 0:
            return image
        factor = random.uniform(1 - self.zoom_range, 1 + self.zoom_range)
        h, w = image.shape[:2]
        new_h, new_w = int(h * factor), int(w * factor)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        if factor > 1:
            # Crop centre back to original size
            y0 = (new_h - h) // 2
            x0 = (new_w - w) // 2
            image = resized[y0: y0 + h, x0: x0 + w]
        else:
            # Pad centre with zeros to original size
            canvas = np.zeros_like(image)
            y0 = (h - new_h) // 2
            x0 = (w - new_w) // 2
            canvas[y0: y0 + new_h, x0: x0 + new_w] = resized
            image = canvas
        return image

    def _maybe_brightness(self, image: np.ndarray) -> np.ndarray:
        if self.brightness_min == self.brightness_max == 1.0:
            return image
        scale = random.uniform(self.brightness_min, self.brightness_max)
        if image.dtype == np.uint8:
            image = np.clip(image.astype(np.float32) * scale, 0, 255).astype(np.uint8)
        else:
            image = np.clip(image * scale, 0.0, 1.0)
        return image
