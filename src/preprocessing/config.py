"""
V4 preprocessing configuration dataclass and pipeline presets.

All V4 pipeline stages are parameterised through :class:`PreprocessingV4Config`.
Use :meth:`PreprocessingV4Config.from_dict` to load from a YAML-parsed dict and
:meth:`PreprocessingV4Config.from_preset` to start from a named model preset.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Any

import cv2


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class PreprocessingV4Config:
    """
    Unified configuration for the V4 preprocessing + augmentation pipeline.

    Fields are grouped by pipeline stage.  Boolean toggles allow individual
    stages/sub-stages to be disabled (e.g. for ablation experiments).

    Args:
        use_canonical_flip: Enable Stage 0 horizontal flip for left-eye images.
        use_flat_field: Enable Stage 2 Gaussian flat-field correction.
        use_clahe: Enable Stage 3 upgraded CLAHE L-channel enhancement.
        use_pca_color: Enable Stage 5 PCA colour jitter augmentation.
        use_brightness_contrast: Enable Stage 5 brightness/contrast augmentation.
        use_shear: Enable Stage 5 shear component of the affine transform.
        use_stretch: Enable Stage 5 anisotropic stretch component.
        target_size: Output spatial resolution in pixels (square).
        flat_field_sigma: Gaussian σ for flat-field blur subtraction.
        clahe_tile_grid_size: CLAHE tile grid as (rows, cols).
        clahe_clip_factor: Clip-limit scale factor (× tile_area / 256).
        clahe_global_threshold: Additional global clip limit (× tile_area).
        clahe_train_prob: Probability of applying CLAHE at train time.
        rotation_sigma: σ of the truncated Gaussian rotation distribution (°).
        rotation_clip: Hard clip on sampled rotation angle (°).
        zoom_range: Log-uniform zoom range [min, max].
        stretch_range: Log-uniform anisotropic stretch range [min, max].
        shear_range: Uniform shear range [min_deg, max_deg].
        shear_prob: Probability of applying shear augmentation.
        interp_weights: Sampling weights for (LINEAR, CUBIC, NEAREST).
        border_mode: OpenCV border mode for warpAffine (default BORDER_REFLECT).
        pca_color_sigma: σ of Normal distribution for PCA colour noise.
        pca_color_prob: Probability of applying PCA colour jitter.
        brightness_alpha_range: Contrast multiplier range [min, max].
        brightness_beta_range: Brightness additive range [min, max] (uint8 scale).
        bc_prob: Probability of applying brightness/contrast augmentation.
        normalize_mean: Per-channel mean for ImageNet normalisation.
        normalize_std: Per-channel std for ImageNet normalisation.
    """

    # --- Toggles ---
    use_canonical_flip: bool = True
    use_flat_field: bool = True
    use_clahe: bool = True
    use_pca_color: bool = True
    use_brightness_contrast: bool = True
    use_shear: bool = True
    use_stretch: bool = True

    # --- Stage 1: Crop + Resize ---
    target_size: int = 512

    # --- Stage 2: Flat-Field Correction ---
    flat_field_sigma: float = 45.0

    # --- Stage 3: Upgraded CLAHE ---
    clahe_tile_grid_size: tuple[int, int] = (8, 8)
    clahe_clip_factor: float = 2.0
    clahe_global_threshold: float = 0.01
    clahe_train_prob: float = 0.8

    # --- Stage 5: Augmentation ---
    rotation_sigma: float = 13.0
    rotation_clip: float = 40.0
    zoom_range: tuple[float, float] = (0.9, 1.1)
    stretch_range: tuple[float, float] = (1 / 1.05, 1.05)
    shear_range: tuple[float, float] = (-2.0, 2.0)
    shear_prob: float = 0.3
    interp_weights: tuple[float, float, float] = (0.6, 0.3, 0.1)  # LINEAR, CUBIC, NEAREST
    border_mode: int = cv2.BORDER_REFLECT
    pca_color_sigma: float = 0.1
    pca_color_prob: float = 0.5
    brightness_alpha_range: tuple[float, float] = (0.9, 1.1)
    brightness_beta_range: tuple[float, float] = (-10.0, 10.0)
    bc_prob: float = 0.5

    # --- Stage 4: Normalise ---
    normalize_mean: tuple[float, float, float] = (0.485, 0.456, 0.406)
    normalize_std: tuple[float, float, float] = (0.229, 0.224, 0.225)

    # ------------------------------------------------------------------
    # Factory: from dict
    # ------------------------------------------------------------------

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreprocessingV4Config":
        """
        Build a :class:`PreprocessingV4Config` from a plain dict.

        Keys absent from *d* retain their dataclass defaults.  List values
        are coerced to tuples for tuple-annotated fields (e.g. when loading
        from a YAML file where sequences are represented as lists).

        Args:
            d: Dict of field overrides, typically from a YAML ``preprocessing_v4``
               section.

        Returns:
            PreprocessingV4Config instance.
        """
        kwargs: dict[str, Any] = {}
        for f in dataclasses.fields(cls):
            if f.name not in d:
                continue
            val = d[f.name]
            # Coerce list → tuple for tuple-annotated fields.
            # With `from __future__ import annotations`, f.type is always a str.
            type_str: str = f.type if isinstance(f.type, str) else str(f.type)
            if type_str.startswith("tuple") and isinstance(val, list):
                val = tuple(val)
            kwargs[f.name] = val
        return cls(**kwargs)

    # ------------------------------------------------------------------
    # Factory: from preset
    # ------------------------------------------------------------------

    @classmethod
    def from_preset(cls, preset_name: str) -> "PreprocessingV4Config":
        """
        Build a :class:`PreprocessingV4Config` from a named preset.

        The preset supplies a partial dict of overrides applied on top of
        dataclass defaults; unspecified fields keep their default values.

        Args:
            preset_name: Key into :data:`PIPELINE_PRESETS`
                (currently ``"resnet"`` or ``"efficientnet"``).

        Returns:
            PreprocessingV4Config instance.

        Raises:
            ValueError: If *preset_name* is not found in :data:`PIPELINE_PRESETS`.
        """
        if preset_name not in PIPELINE_PRESETS:
            available = list(PIPELINE_PRESETS)
            raise ValueError(
                f"Unknown preset '{preset_name}'. Available presets: {available}"
            )
        return cls.from_dict(PIPELINE_PRESETS[preset_name])


# ---------------------------------------------------------------------------
# Pipeline presets
# ---------------------------------------------------------------------------

PIPELINE_PRESETS: dict[str, dict[str, Any]] = {
    "resnet": {
        "use_flat_field": True,
        "use_clahe": True,
        "clahe_train_prob": 0.8,
        "use_pca_color": True,
        "pca_color_prob": 0.5,
        "use_brightness_contrast": True,
        "bc_prob": 0.5,
        "use_shear": True,
        "shear_prob": 0.3,
        "use_stretch": True,
    },
    "efficientnet": {
        "use_flat_field": True,
        "use_clahe": True,
        "clahe_train_prob": 0.5,
        "use_pca_color": False,
        "use_brightness_contrast": True,
        "bc_prob": 0.3,
        "use_shear": False,
        "use_stretch": True,
    },
}
