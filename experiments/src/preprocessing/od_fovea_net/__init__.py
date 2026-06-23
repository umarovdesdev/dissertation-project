"""Learned OD/fovea heatmap-regression detector (in-repo inference port).

This package is the production home of the trained detector (Phase 2). It is the
inference half of ``experiments/od_fovea_detector/`` ported into the monorepo so
the live preprocessing pipeline can use it via the
``src/preprocessing/od_fovea_detect`` facade. Training / evaluation still live in
the standalone ``od_fovea_detector`` project; only the frozen weights are shared.
"""

from .infer import ODFoveaNetResult, detect_od_fovea, reset_cache

__all__ = ["ODFoveaNetResult", "detect_od_fovea", "reset_cache"]
