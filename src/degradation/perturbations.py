"""Image degradation perturbations for robustness evaluation (Experiment 3).

Three distortion types, each at three severity levels (low / medium / high):
  - gaussian_noise  : additive Gaussian noise (σ controls noise level)
  - gaussian_blur   : Gaussian blur (kernel_size controls blurring)
  - low_illumination: multiplicative brightness reduction (factor < 1)

Severity parameter values come from the experiment config
  config["degradation"][deg_type]["low" / "medium" / "high"].
"""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

from src.data.datasets import BaseFundusDataset

# Default severity parameter tables (overridable via config)
_DEFAULT_PARAMS: dict[str, dict[str, Any]] = {
    "gaussian_noise": {
        "low":    {"sigma": 15},
        "medium": {"sigma": 30},
        "high":   {"sigma": 60},
    },
    "gaussian_blur": {
        "low":    {"kernel_size": 5},
        "medium": {"kernel_size": 11},
        "high":   {"kernel_size": 21},
    },
    "low_illumination": {
        "low":    {"factor": 0.7},
        "medium": {"factor": 0.5},
        "high":   {"factor": 0.3},
    },
}


def apply_gaussian_noise(image: np.ndarray, sigma: float) -> np.ndarray:
    """Add zero-mean Gaussian noise to an image.

    Args:
        image: BGR uint8 image (H×W×3).
        sigma: Standard deviation of the noise (0–255 scale).

    Returns:
        Noisy BGR uint8 image, clipped to [0, 255].
    """
    if image.dtype != np.uint8:
        image = (np.clip(image, 0, 1) * 255).astype(np.uint8)
    noise = np.random.normal(0.0, sigma, image.shape).astype(np.float32)
    noisy = image.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def apply_gaussian_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
    """Apply Gaussian blur to an image.

    Args:
        image: BGR uint8 image (H×W×3).
        kernel_size: Kernel size (must be a positive odd integer).

    Returns:
        Blurred BGR uint8 image.
    """
    if image.dtype != np.uint8:
        image = (np.clip(image, 0, 1) * 255).astype(np.uint8)
    # Ensure odd kernel size
    k = int(kernel_size)
    if k % 2 == 0:
        k += 1
    return cv2.GaussianBlur(image, (k, k), sigmaX=0)


def apply_low_illumination(image: np.ndarray, factor: float) -> np.ndarray:
    """Reduce image brightness by a multiplicative factor.

    Args:
        image: BGR uint8 image (H×W×3).
        factor: Multiplier in (0, 1]. Values close to 0 produce very dark images.

    Returns:
        Darkened BGR uint8 image, clipped to [0, 255].
    """
    if image.dtype != np.uint8:
        image = (np.clip(image, 0, 1) * 255).astype(np.uint8)
    darkened = image.astype(np.float32) * float(factor)
    return np.clip(darkened, 0, 255).astype(np.uint8)


def apply_degradation(
    image: np.ndarray,
    deg_type: str,
    severity: str,
    config: dict[str, Any] | None = None,
) -> np.ndarray:
    """Apply a named degradation at a specified severity level.

    Args:
        image: BGR uint8 or float32 image.
        deg_type: One of "gaussian_noise", "gaussian_blur", "low_illumination".
        severity: One of "low", "medium", "high".
        config: Optional config dict with a "degradation" key.  If present,
            config["degradation"][deg_type][severity] overrides the defaults.

    Returns:
        Degraded BGR uint8 image.

    Raises:
        ValueError: If deg_type or severity is unrecognized.
    """
    valid_types = {"gaussian_noise", "gaussian_blur", "low_illumination"}
    if deg_type not in valid_types:
        raise ValueError(f"Unknown degradation type: '{deg_type}'. Choose from {valid_types}")

    valid_sevs = {"low", "medium", "high"}
    if severity not in valid_sevs:
        raise ValueError(f"Unknown severity: '{severity}'. Choose from {valid_sevs}")

    # Resolve parameters from config or defaults
    params: dict[str, Any] = dict(_DEFAULT_PARAMS[deg_type][severity])
    if config is not None:
        deg_cfg = config.get("degradation", {})
        type_cfg = deg_cfg.get(deg_type, {})
        sev_cfg = type_cfg.get(severity, {})
        params.update(sev_cfg)

    if deg_type == "gaussian_noise":
        return apply_gaussian_noise(image, sigma=float(params["sigma"]))
    if deg_type == "gaussian_blur":
        return apply_gaussian_blur(image, kernel_size=int(params["kernel_size"]))
    # low_illumination
    return apply_low_illumination(image, factor=float(params["factor"]))


class DegradedDataset(Dataset):
    """Wraps a BaseFundusDataset, applying a fixed degradation before preprocessing.

    The degradation is applied to the raw BGR uint8 image *before* the
    dataset's own preprocessing callable runs.  This mirrors real acquisition
    noise that occurs before any signal processing.

    Args:
        base_dataset: A BaseFundusDataset instance (or subclass).  Must
            expose ``image_paths`` and ``labels`` attributes.
        deg_type: Degradation type — "gaussian_noise", "gaussian_blur",
            or "low_illumination".
        severity: Severity level — "low", "medium", or "high".
        config: Optional config dict passed to apply_degradation.
    """

    def __init__(
        self,
        base_dataset: BaseFundusDataset,
        deg_type: str,
        severity: str,
        config: dict[str, Any] | None = None,
    ) -> None:
        self.base_dataset = base_dataset
        self.deg_type = deg_type
        self.severity = severity
        self.config = config

        # Expose the same attributes as the wrapped dataset for compatibility
        self.image_paths: list[str] = base_dataset.image_paths
        self.labels: list[int] = base_dataset.labels

    def __len__(self) -> int:
        return len(self.base_dataset)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        """Load, degrade, preprocess, and return one sample.

        The raw image is degraded first; then the base dataset's preprocessing
        and augmentation callables (if any) are applied exactly as usual.

        Args:
            idx: Sample index.

        Returns:
            Tuple of (image_tensor, label), same dtype/shape as the wrapped dataset.
        """
        import cv2  # local import avoids circular dependency at module level

        raw = cv2.imread(str(self.image_paths[idx]))
        if raw is None:
            raise FileNotFoundError(f"Could not load image: {self.image_paths[idx]}")

        # Apply degradation to raw image first
        degraded = apply_degradation(raw, self.deg_type, self.severity, self.config)

        # Then run the base dataset's preprocessing pipeline (if any)
        image: np.ndarray = degraded
        if self.base_dataset.preprocessing is not None:
            image = self.base_dataset.preprocessing(image)

        # Augmentation is intentionally skipped — evaluation only
        # (augmentation would randomise the degraded test set unfairly)

        # Normalise to [0, 1] float32 only if still uint8
        if image.dtype == np.uint8:
            image = image.astype(np.float32) / 255.0
        else:
            image = image.astype(np.float32)

        # HWC → CHW
        tensor = torch.from_numpy(np.ascontiguousarray(image.transpose(2, 0, 1)))
        return tensor, self.labels[idx]
