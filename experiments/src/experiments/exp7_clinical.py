"""Experiment 7: Small Data Training.

5-fold CV on IDRiD as training data, Clinical dataset as held-out test.
Report mean +/- std across folds.
Tests trainability on small clinical datasets.

Normalization (TASK-fix #3): Exp 7 is the only experiment that *trains* on
IDRiD, so it needs IDRiD-specific Stage 7 stats rather than the EyePACS train
stats reused by the cross-dataset transfer runs (Exp 3–6). Those stats are
produced by ``scripts/compute_dataset_stats.py --dataset idrid`` →
``data/processed/idrid_norm_stats.json`` and loaded here by
:func:`load_idrid_norm_stats` (mirrors how ``exp1_factorial`` auto-loads the
EyePACS file for Configs B/D).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_idrid_norm_stats(
    config: dict[str, Any],
) -> tuple[tuple[float, float, float], tuple[float, float, float]] | None:
    """Load IDRiD Stage 7 normalize stats, mirroring ``exp1_factorial``.

    Resolves ``data/processed/idrid_norm_stats.json`` relative to the
    configured output directory (same convention as the EyePACS loader in
    ``exp1_factorial``) and returns the per-channel ``(mean, std)`` tuples for
    the full pipeline (Stage 7, ``normalize_mode="dataset_specific"``).

    Args:
        config: Parsed experiment config dict (reads ``paths.output_dir``).

    Returns:
        ``(mean, std)`` 3-tuples in the [0, 1] scale, or ``None`` if the stats
        file is absent (caller should fall back to ImageNet and warn — NOT
        thesis-faithful for a train-on-IDRiD run).
    """
    processed_dir = (
        Path(config.get("paths", {}).get("output_dir", "outputs/")).parent
        / "data" / "processed"
    )
    stats_path = processed_dir / "idrid_norm_stats.json"
    if not stats_path.exists():
        print(f"  IDRiD normalize stats not found at {stats_path} — run "
              "scripts/compute_dataset_stats.py --dataset idrid to fix.")
        return None

    with open(stats_path) as f:
        stats = json.load(f)
    mean = tuple(float(x) for x in stats["mean"])
    std = tuple(float(x) for x in stats["std"])
    print(f"  IDRiD normalize stats loaded from {stats_path}")
    print(f"    mean={[round(x, 4) for x in mean]} std={[round(x, 4) for x in std]}")
    return mean, std  # type: ignore[return-value]


def run(config: dict[str, Any], *, fold: int | None = None,
        resume: bool = False, _configs_to_run: list[str] | None = None) -> None:
    """Run Experiment 7: Small Data Training."""
    # Stage 7 stats are wired here so the full training loop (when built) uses
    # IDRiD-specific normalization. Loading them up front also makes the
    # consumption verifiable (TASK-fix #3 acceptance).
    load_idrid_norm_stats(config)
    raise NotImplementedError(
        "Experiment 7 (small data clinical) not yet implemented. "
        "5-fold CV on IDRiD, test on Clinical held-out. IDRiD Stage 7 "
        "normalize stats are loaded via load_idrid_norm_stats()."
    )
