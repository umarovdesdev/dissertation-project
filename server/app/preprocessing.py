"""Inference-time V5 preprocessing — reuses experiments/src/preprocessing.

Critical: Config D trained with **dataset-specific** Stage 7 normalize (D-2).
The preset path leaves ``dataset_mean/std = None`` (→ ImageNet), so to avoid
train/inference preprocessing drift we inject the same EyePACS-computed stats
the checkpoint was trained with, loaded from ``eyepacs_norm_stats.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

# app/__init__.py has already put experiments/ on sys.path.
from src.preprocessing.config import PreprocessingV5Config
from src.preprocessing.pipeline_v5 import PreprocessingPipelineV5


def load_norm_stats(stats_path: Path) -> tuple[tuple[float, ...], tuple[float, ...]] | None:
    """Load dataset-specific normalize stats if the file exists.

    Args:
        stats_path: Path to ``eyepacs_norm_stats.json`` (keys ``mean``/``std``).

    Returns:
        ``(mean, std)`` tuples, or ``None`` if the file is absent.
    """
    if not stats_path.exists():
        return None
    with open(stats_path) as f:
        data = json.load(f)
    return tuple(data["mean"]), tuple(data["std"])


def build_inference_pipeline(
    preset: str,
    norm_stats_path: Path,
    input_color_space: str = "rgb",
) -> PreprocessingPipelineV5:
    """Build a deterministic (no-augmentation) full-V5 inference pipeline.

    Args:
        preset: Preprocessing preset name (``"efficientnet"`` for Config D).
        norm_stats_path: Path to the dataset-specific normalize stats JSON.
        input_color_space: ``"rgb"`` (we decode uploads to RGB) or ``"bgr"``.

    Returns:
        A :class:`PreprocessingPipelineV5` in inference mode (deterministic
        CLAHE, no augmentation), producing a ``(4, 512, 512)`` tensor.
    """
    config = PreprocessingV5Config.from_preset(preset)

    stats = load_norm_stats(norm_stats_path)
    if stats is not None:
        config.dataset_mean, config.dataset_std = stats
    # else: pipeline falls back to ImageNet — logged by the caller.

    return PreprocessingPipelineV5.create_for_inference(
        config, input_color_space=input_color_space
    )
