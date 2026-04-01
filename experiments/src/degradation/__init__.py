"""Image degradation perturbations for robustness evaluation (Experiment 3)."""

from src.degradation.perturbations import (
    DegradedDataset,
    apply_degradation,
    apply_gaussian_blur,
    apply_gaussian_noise,
    apply_low_illumination,
)

__all__ = [
    "apply_gaussian_noise",
    "apply_gaussian_blur",
    "apply_low_illumination",
    "apply_degradation",
    "DegradedDataset",
]
