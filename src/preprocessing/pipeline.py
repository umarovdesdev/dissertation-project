"""
Preprocessing pipeline orchestrator.

PreprocessingPipeline applies the five ordered components:
  1. FOV Standardization
  2. Green Channel Extraction
  3. Pixel Normalization
  4. CLAHE Enhancement (LAB color space)
  5. HSV Contrast Enhancement

Each component can be toggled individually via a config dict.  Factory
class-methods produce common configurations (baseline, full, ablation).
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .clahe import apply_clahe
from .fov import standardize_fov
from .green_channel import extract_green_channel
from .hsv_enhancement import enhance_hsv
from .normalization import normalize_pixels

# Ordered canonical component keys
_COMPONENT_KEYS: tuple[str, ...] = (
    "fov_standardization",
    "green_channel",
    "normalize",
    "clahe",
    "hsv_enhancement",
)


class PreprocessingPipeline:
    """
    Configurable 5-component fundus image preprocessing pipeline.

    Args:
        config: Dict with boolean toggles for each component and optional
            parameter overrides.  Expected keys (all optional, default True):
            - fov_standardization (bool)
            - green_channel (bool)
            - normalize (bool)
            - clahe (bool)
            - hsv_enhancement (bool)
            - target_size (int, default 512)
            - clahe_clip_limit (float, default 2.0)
            - clahe_grid_size (tuple[int,int], default (8,8))
            - saturation_scale (float, default 1.2)
            - value_scale (float, default 1.1)
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        cfg = config or {}

        # Component toggles — all on by default
        self._enabled: dict[str, bool] = {
            key: bool(cfg.get(key, True)) for key in _COMPONENT_KEYS
        }

        # Parameters
        self._target_size: int = int(cfg.get("target_size", 512))
        self._clahe_clip_limit: float = float(cfg.get("clahe_clip_limit", 2.0))
        self._clahe_grid_size: tuple[int, int] = tuple(cfg.get("clahe_grid_size", (8, 8)))  # type: ignore[arg-type]
        self._saturation_scale: float = float(cfg.get("saturation_scale", 1.2))
        self._value_scale: float = float(cfg.get("value_scale", 1.1))

    # ------------------------------------------------------------------
    # Core callable
    # ------------------------------------------------------------------

    def __call__(self, image: np.ndarray) -> np.ndarray:
        """
        Apply all enabled pipeline components in order.

        Args:
            image: BGR uint8 NumPy array.

        Returns:
            Processed image.  dtype is float32 if normalize is enabled,
            uint8 otherwise.
        """
        if self._enabled["fov_standardization"]:
            image = standardize_fov(image, target_size=self._target_size)

        if self._enabled["green_channel"]:
            image = extract_green_channel(image)

        if self._enabled["normalize"]:
            image = normalize_pixels(image)

        if self._enabled["clahe"]:
            image = apply_clahe(
                image,
                clip_limit=self._clahe_clip_limit,
                grid_size=self._clahe_grid_size,
            )

        if self._enabled["hsv_enhancement"]:
            image = enhance_hsv(
                image,
                saturation_scale=self._saturation_scale,
                value_scale=self._value_scale,
            )

        return image

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Return True if all five components are enabled (full pipeline)."""
        return all(self._enabled[k] for k in _COMPONENT_KEYS)

    def is_absent(self) -> bool:
        """Return True if only FOV standardization is enabled (baseline)."""
        return (
            self._enabled["fov_standardization"]
            and not self._enabled["green_channel"]
            and not self._enabled["normalize"]
            and not self._enabled["clahe"]
            and not self._enabled["hsv_enhancement"]
        )

    @property
    def enabled_components(self) -> dict[str, bool]:
        """Return a copy of the component toggle state."""
        return dict(self._enabled)

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def create_baseline(cls, target_size: int = 512) -> "PreprocessingPipeline":
        """
        Create baseline pipeline: FOV standardization (resize only), no further processing.

        Args:
            target_size: Output image resolution in pixels.

        Returns:
            PreprocessingPipeline with only fov_standardization enabled.
        """
        return cls(
            {
                "fov_standardization": True,
                "green_channel": False,
                "normalize": False,
                "clahe": False,
                "hsv_enhancement": False,
                "target_size": target_size,
            }
        )

    @classmethod
    def create_full(cls, config: dict[str, Any] | None = None) -> "PreprocessingPipeline":
        """
        Create the full 5-component pipeline with optional parameter overrides.

        Args:
            config: Optional dict of parameter overrides (component toggles are
                ignored — all five components are always enabled).

        Returns:
            PreprocessingPipeline with all five components enabled.
        """
        cfg: dict[str, Any] = dict(config or {})
        for key in _COMPONENT_KEYS:
            cfg[key] = True
        return cls(cfg)

    @classmethod
    def create_ablation(
        cls,
        config: dict[str, Any] | None = None,
        components: list[str] | None = None,
    ) -> "PreprocessingPipeline":
        """
        Create an ablation pipeline with a specific subset of components enabled.

        fov_standardization is always kept on (resize is the minimum baseline).

        Args:
            config: Optional dict of parameter overrides.
            components: List of component keys to enable.  Keys not in this
                list are disabled.  fov_standardization is always included.

        Returns:
            PreprocessingPipeline with only the requested components active.

        Example:
            # resize + normalize + CLAHE ablation (Experiment 2 level 4)
            pipeline = PreprocessingPipeline.create_ablation(
                components=["fov_standardization", "normalize", "clahe"]
            )
        """
        cfg: dict[str, Any] = dict(config or {})
        active = set(components or []) | {"fov_standardization"}
        for key in _COMPONENT_KEYS:
            cfg[key] = key in active
        return cls(cfg)
