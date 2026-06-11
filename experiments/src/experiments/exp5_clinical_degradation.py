"""Experiment 5: Clinical Degradation Resistance (H-7).

A CNN trained on EyePACS is evaluated **without retraining** on the external
clinical datasets IDRiD and Messidor-2, both *with* the full preprocessing
pipeline and *without* it (stretch-resize + ImageNet-norm baseline).

For each external dataset and each model the cross-dataset degradation is
    Δ = F1_EyePACS_val − F1_external.
H-7 holds when the full-pipeline model degrades **statistically less** than the
baseline model, i.e. d = Δ_baseline − Δ_full > 0. d is tested per dataset with
a paired bootstrap over the external images (both models are scored on the same
images), and H-7 is supported when every evaluable dataset has a bootstrap CI
lower bound above zero.

Output: <output_dir>/exp5/clinical_degradation_results.json
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.metrics import f1_score

from src.data.datasets import IDRiDDataset
from src.data.messidor2_dataset import Messidor2Dataset
from src.experiments._eval_utils import (
    build_full_pipeline,
    infer_dataset,
    load_baseline_model,
    load_or_train_model,
)
from src.preprocessing.pipeline import PreprocessingPipeline
from src.utils.seed import set_seed

_BOOTSTRAP_ITERS = 1000
_CONFIDENCE = 0.95


# ── Entry point ───────────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _configs_to_run: list[str] | None = None,
) -> None:
    """Run Experiment 5: clinical degradation resistance (H-7).

    Args:
        config: Full merged config dict (global + ``experiment`` section).
        fold: Unused — included for CLI/dispatch interface consistency.
        resume: Resume from checkpoint when training a fresh full model.
        _subset_size: Limit external-dataset rows (and any fresh-train EyePACS
            rows) for smoke tests. ``None`` uses the full datasets.
        _configs_to_run: Unused — included for dispatch interface consistency.
    """
    set_seed(config.get("seed", 42))

    output_dir = Path(config["paths"]["output_dir"]) / "exp5"
    output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ── Models: full pipeline (D/B) + baseline (C/A) ──────────────────────────
    print(f"\n{'='*65}")
    print("Exp5 — Loading full-pipeline model (EyePACS) …")
    print(f"{'='*65}")
    full_model, eyepacs_f1_full = load_or_train_model(
        config, output_dir, subset_size=_subset_size, resume=resume
    )
    full_model = full_model.to(device).eval()
    full_pipeline = build_full_pipeline(config["preprocessing"])
    print(f"  In-domain EyePACS F1 (full pipeline) = {eyepacs_f1_full:.4f}")

    print(f"\n{'='*65}")
    print("Exp5 — Loading baseline (3ch) model …")
    print(f"{'='*65}")
    base_model, eyepacs_f1_base, base_arch, base_tag = load_baseline_model(config)
    if base_model is None:
        raise RuntimeError(
            "Experiment 5 requires a baseline checkpoint (exp1 C_fold0 or "
            "A_fold0) to compare degradation against the full pipeline. "
            "Run exp1 config C (or A) first."
        )
    base_model = base_model.to(device).eval()
    baseline_pipeline = PreprocessingPipeline.create_baseline(
        target_size=512, is_training=False
    )
    print(f"  Baseline checkpoint: {base_tag} ({base_arch})")
    print(f"  In-domain EyePACS F1 (baseline) = {eyepacs_f1_base:.4f}")

    # ── External datasets ─────────────────────────────────────────────────────
    builders = {
        "idrid":     _build_idrid,
        "messidor2": _build_messidor2,
    }

    results: dict[str, Any] = {
        "hypothesis": "H-7",
        "metric": "delta_f1 = F1_EyePACS_val - F1_external",
        "in_domain": {
            "eyepacs_f1_full":     float(eyepacs_f1_full),
            "eyepacs_f1_baseline": float(eyepacs_f1_base),
        },
        "baseline_model": {"arch": base_arch, "checkpoint": base_tag},
        "external": {},
    }

    for ds_name, builder in builders.items():
        print(f"\n{'='*65}")
        print(f"Evaluating external dataset: {ds_name} …")
        print(f"{'='*65}")
        results["external"][ds_name] = _eval_dataset(
            config, ds_name, builder,
            full_model, full_pipeline, eyepacs_f1_full,
            base_model, baseline_pipeline, eyepacs_f1_base,
            device, _subset_size,
        )

    # ── H-7 aggregation ───────────────────────────────────────────────────────
    evaluable = [
        v for v in results["external"].values()
        if isinstance(v.get("degradation_diff"), dict)
        and not np.isnan(v["degradation_diff"]["mean"])
    ]
    h7_supported = (
        len(evaluable) > 0
        and all(v["degradation_diff"]["supported"] for v in evaluable)
    )
    results["h7_supported"] = h7_supported
    results["n_datasets_evaluated"] = len(evaluable)

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = output_dir / "clinical_degradation_results.json"
    with open(out_path, "w") as f:
        json.dump(
            results, f, indent=2,
            default=lambda x: float(x) if isinstance(x, np.floating) else x,
        )
    print(f"\nResults saved → {out_path}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Experiment 5 — Clinical Degradation Resistance (H-7) Summary")
    print(f"{'='*65}")
    print(f"  EyePACS val F1 — full={eyepacs_f1_full:.4f}  "
          f"baseline={eyepacs_f1_base:.4f}")
    for ds_name, res in results["external"].items():
        if "degradation_diff" not in res:
            print(f"  {ds_name:<12}: {res.get('status', 'unknown')}")
            continue
        dd = res["degradation_diff"]
        ok = "✓" if dd["supported"] else "✗"
        print(f"  {ds_name:<12}: F1_full={res['f1_full']:.4f} "
              f"(Δ={res['delta_full']:.4f})  "
              f"F1_base={res['f1_baseline']:.4f} (Δ={res['delta_baseline']:.4f})  "
              f"d={dd['mean']:.4f} [CI {dd['ci_lower']:.4f},{dd['ci_upper']:.4f}] {ok}")
    label = "SUPPORTED" if h7_supported else "NOT SUPPORTED"
    print(f"\n  H-7: {label} "
          f"({len(evaluable)} dataset(s) evaluated)")


# ── External-dataset evaluation ───────────────────────────────────────────────

def _eval_dataset(
    config: dict[str, Any],
    ds_name: str,
    builder: Any,
    full_model: torch.nn.Module,
    full_pipeline: Any,
    eyepacs_f1_full: float,
    base_model: torch.nn.Module,
    baseline_pipeline: Any,
    eyepacs_f1_base: float,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
    """Evaluate both models on one external dataset and compute degradation.

    Both models are scored on the SAME external images (identical CSV order,
    only the preprocessing differs), so the bootstrap over external indices is
    paired.

    Returns:
        Dict with full/baseline F1, deltas, and the paired-bootstrap
        degradation-difference statistics; or ``{"status": ...}`` on failure.
    """
    try:
        full_ds = builder(config, full_pipeline, subset_size)
        base_ds = builder(config, baseline_pipeline, subset_size)
    except Exception as e:  # noqa: BLE001 — surface as skip, don't crash the run
        warnings.warn(f"{ds_name} dataset build failed: {e}", UserWarning)
        return {"status": "failed", "error": str(e)}

    if len(full_ds) == 0:
        return {"status": "skipped", "reason": f"{ds_name} has 0 usable images"}
    print(f"  {ds_name}: {len(full_ds)} images")

    y_true_f, y_pred_full, _, _ = infer_dataset(full_model, full_ds, config, device)
    y_true_b, y_pred_base, _, _ = infer_dataset(base_model, base_ds, config, device)

    # Sanity: both runs must align on the same ground-truth ordering.
    if not np.array_equal(y_true_f, y_true_b):
        warnings.warn(
            f"{ds_name}: full/baseline label ordering differs — bootstrap "
            "pairing invalid; reporting point estimates only.",
            UserWarning,
        )

    f1_full = float(f1_score(y_true_f, y_pred_full, average="weighted", zero_division=0))
    f1_base = float(f1_score(y_true_b, y_pred_base, average="weighted", zero_division=0))
    delta_full = eyepacs_f1_full - f1_full
    delta_base = eyepacs_f1_base - f1_base

    dd = _bootstrap_degradation_diff(
        y_true_f, y_pred_full, y_pred_base,
        eyepacs_f1_full, eyepacs_f1_base,
    )

    return {
        "n_images":        int(len(full_ds)),
        "f1_full":         f1_full,
        "f1_baseline":     f1_base,
        "delta_full":      float(delta_full),
        "delta_baseline":  float(delta_base),
        "degradation_diff": dd,
    }


def _bootstrap_degradation_diff(
    y_true: np.ndarray,
    y_pred_full: np.ndarray,
    y_pred_base: np.ndarray,
    eyepacs_f1_full: float,
    eyepacs_f1_base: float,
    n_iterations: int = _BOOTSTRAP_ITERS,
    confidence: float = _CONFIDENCE,
    seed: int = 42,
) -> dict[str, float | bool]:
    """Paired bootstrap of d = Δ_baseline − Δ_full over external images.

    d > 0 means the full-pipeline model degrades less than the baseline. The
    in-domain EyePACS F1 terms are constants; only the external F1 terms are
    resampled (paired on the same indices for both models).

    Returns:
        Dict with mean, ci_lower, ci_upper, p_value_one_sided (bootstrap mass at
        d <= 0), and ``supported`` (ci_lower > 0). NaN-filled if in-domain F1 is
        unknown.
    """
    if np.isnan(eyepacs_f1_full) or np.isnan(eyepacs_f1_base):
        return {
            "mean": float("nan"), "ci_lower": float("nan"),
            "ci_upper": float("nan"), "p_value_one_sided": float("nan"),
            "supported": False,
        }

    rng = np.random.default_rng(seed)
    n = len(y_true)
    diffs: list[float] = []
    for _ in range(n_iterations):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        f1_full_b = f1_score(yt, y_pred_full[idx], average="weighted", zero_division=0)
        f1_base_b = f1_score(yt, y_pred_base[idx], average="weighted", zero_division=0)
        delta_full_b = eyepacs_f1_full - f1_full_b
        delta_base_b = eyepacs_f1_base - f1_base_b
        diffs.append(float(delta_base_b - delta_full_b))

    diffs_arr = np.asarray(diffs)
    tail = (1.0 - confidence) / 2
    ci_lower = float(np.percentile(diffs_arr, 100 * tail))
    ci_upper = float(np.percentile(diffs_arr, 100 * (1 - tail)))
    return {
        "mean":              round(float(np.mean(diffs_arr)), 6),
        "ci_lower":          round(ci_lower, 6),
        "ci_upper":          round(ci_upper, 6),
        "p_value_one_sided": round(float(np.mean(diffs_arr <= 0.0)), 6),
        "supported":         bool(ci_lower > 0.0),
    }


# ── Dataset builders (pipeline-parametrised) ──────────────────────────────────

def _build_idrid(config: dict[str, Any], pipeline: Any, subset_size: int | None):
    """Build the IDRiD training-set grading dataset with ``pipeline``."""
    idrid_root = Path(config["paths"]["idrid"])
    subset = list(range(subset_size)) if subset_size else None
    return IDRiDDataset.from_directory(
        root=str(idrid_root / "B. Disease Grading" / "1. Original Images" /
                 "a. Training Set"),
        labels_csv=str(idrid_root / "B. Disease Grading" / "2. Groundtruths" /
                       "a. IDRiD_Disease Grading_Training Labels.csv"),
        subset_indices=subset,
        preprocessing=pipeline,
    )


def _build_messidor2(config: dict[str, Any], pipeline: Any, subset_size: int | None):
    """Build the Messidor-2 dataset with ``pipeline``."""
    messidor_root = Path(config["paths"]["messidor2"])
    subset = list(range(subset_size)) if subset_size else None
    return Messidor2Dataset.from_directory(
        root=messidor_root / "IMAGES",
        labels_csv=messidor_root / "messidor_data.csv",
        subset_indices=subset,
        preprocessing=pipeline,
    )
