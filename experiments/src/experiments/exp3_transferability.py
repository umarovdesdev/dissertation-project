"""Experiment 3: Cross-Dataset Transferability (H-4).

Train on EyePACS with the full preprocessing pipeline, evaluate **zero-shot**
(no retraining, no fine-tuning) on APTOS 2019. Compute the generalization
ratio G = F1_APTOS / F1_EyePACS.

H-4 criterion: the full-pipeline model achieves G >= 0.85.

Secondary (not required by H-4): the same evaluation is run for the baseline
(stretch-resize + ImageNet-norm, 3ch) model when an exp1 baseline checkpoint
(C_fold0 / A_fold0) is available, so that G_full can be contrasted with
G_baseline — strengthening the argument that preprocessing improves
cross-dataset transferability. The baseline branch is skipped (not trained
fresh) when no checkpoint exists.

Output: <output_dir>/exp3/transferability_results.json
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.data.datasets import APTOS2019Dataset
from src.experiments._eval_utils import (
    build_full_pipeline,
    evaluate_dataset,
    load_baseline_model,
    load_or_train_model,
)
from src.preprocessing.pipeline import PreprocessingPipeline
from src.utils.seed import set_seed

# Fallback when the exp3 config block omits the threshold (H-4 default).
_DEFAULT_G_THRESHOLD = 0.85


# ── Entry point ───────────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _configs_to_run: list[str] | None = None,
) -> None:
    """Run Experiment 3: cross-dataset transferability EyePACS → APTOS 2019.

    Args:
        config: Full merged config dict (global + ``experiment`` section).
        fold: Unused — included for CLI/dispatch interface consistency.
        resume: Resume from checkpoint when training a fresh full model.
        _subset_size: Limit APTOS rows (and any fresh-train EyePACS rows) for
            smoke tests. ``None`` uses the full datasets.
        _configs_to_run: Unused — included for dispatch interface consistency.
    """
    set_seed(config.get("seed", 42))

    output_dir = Path(config["paths"]["output_dir"]) / "exp3"
    output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    threshold = float(
        config.get("experiment", {}).get(
            "generalization_threshold", _DEFAULT_G_THRESHOLD
        )
    )

    # ── Full-pipeline model (H-4 primary) ─────────────────────────────────────
    print(f"\n{'='*65}")
    print("Exp3 — Loading full-pipeline model (EyePACS) …")
    print(f"{'='*65}")
    model, eyepacs_f1 = load_or_train_model(
        config, output_dir, subset_size=_subset_size, resume=resume
    )
    model = model.to(device).eval()
    print(f"  In-domain EyePACS F1 (full pipeline) = {eyepacs_f1:.4f}")

    full_pipeline = build_full_pipeline(config["preprocessing"])

    print(f"\n{'='*65}")
    print("Evaluating full-pipeline model on APTOS 2019 (zero-shot) …")
    print(f"{'='*65}")
    aptos_full = _eval_aptos(config, model, full_pipeline, device, _subset_size)

    results: dict[str, Any] = {
        "hypothesis": "H-4",
        "generalization_threshold": threshold,
        "full_pipeline": {
            "model":            "efficientnet_b3",
            "pipeline":         "full_pipeline",
            "in_domain_eyepacs_f1": float(eyepacs_f1),
            "aptos":            aptos_full,
        },
        "baseline": None,
    }

    g_full = _g_ratio(aptos_full.get("weighted_f1"), eyepacs_f1)
    results["full_pipeline"]["g_ratio"] = g_full
    h4_supported = (
        isinstance(g_full, float) and not np.isnan(g_full) and g_full >= threshold
    )
    results["h4_supported"] = h4_supported

    # ── Baseline model (secondary, optional) ──────────────────────────────────
    print(f"\n{'='*65}")
    print("Exp3 — Loading baseline (3ch) model for transfer comparison …")
    print(f"{'='*65}")
    base_model, base_eyepacs_f1, base_arch, base_tag = load_baseline_model(config)
    if base_model is not None:
        base_model = base_model.to(device).eval()
        print(f"  Baseline checkpoint: {base_tag} ({base_arch})")
        print(f"  In-domain EyePACS F1 (baseline) = {base_eyepacs_f1:.4f}")
        baseline_pipeline = PreprocessingPipeline.create_baseline(
            target_size=512, is_training=False
        )
        print("\nEvaluating baseline model on APTOS 2019 (zero-shot) …")
        aptos_base = _eval_aptos(
            config, base_model, baseline_pipeline, device, _subset_size
        )
        g_base = _g_ratio(aptos_base.get("weighted_f1"), base_eyepacs_f1)
        results["baseline"] = {
            "model":            base_arch,
            "pipeline":         "baseline",
            "checkpoint":       base_tag,
            "in_domain_eyepacs_f1": float(base_eyepacs_f1),
            "aptos":            aptos_base,
            "g_ratio":          g_base,
        }
    else:
        print("  No baseline checkpoint (C_fold0 / A_fold0) found — "
              "skipping baseline comparison.")
        results["baseline"] = {
            "status": "skipped",
            "reason": "No exp1 baseline checkpoint (C_fold0 / A_fold0) found.",
        }

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = output_dir / "transferability_results.json"
    with open(out_path, "w") as f:
        json.dump(
            results, f, indent=2,
            default=lambda x: float(x) if isinstance(x, np.floating) else x,
        )
    print(f"\nResults saved → {out_path}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Experiment 3 — Cross-Dataset Transferability (H-4) Summary")
    print(f"{'='*65}")
    f1_aptos_full = aptos_full.get("weighted_f1", float("nan"))
    print(f"  Full pipeline : F1_EyePACS={eyepacs_f1:.4f}  "
          f"F1_APTOS={f1_aptos_full:.4f}  "
          f"G={_fmt(g_full)} (threshold {threshold:.2f})")
    if isinstance(results["baseline"], dict) and "g_ratio" in results["baseline"]:
        b = results["baseline"]
        print(f"  Baseline      : F1_EyePACS={b['in_domain_eyepacs_f1']:.4f}  "
              f"F1_APTOS={b['aptos'].get('weighted_f1', float('nan')):.4f}  "
              f"G={_fmt(b['g_ratio'])}")
    ok = "SUPPORTED" if h4_supported else "NOT SUPPORTED"
    print(f"\n  H-4: {ok} (G_full {_fmt(g_full)} "
          f"{'>=' if h4_supported else '<'} {threshold:.2f})")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _eval_aptos(
    config: dict[str, Any],
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
    """Build the APTOS 2019 dataset with ``pipeline`` and evaluate ``model``.

    Args:
        config: Merged config (reads ``paths.aptos``, training params).
        model: Trained model in eval mode.
        pipeline: Preprocessing pipeline (full or baseline) for APTOS images.
        device: Inference device.
        subset_size: Limit APTOS rows for smoke tests; ``None`` for all.

    Returns:
        Metrics dict from :func:`evaluate_dataset`, or a ``{"status": "failed"}``
        dict when the dataset cannot be loaded / evaluated.
    """
    aptos_root = Path(config["paths"]["aptos"])
    try:
        subset = list(range(subset_size)) if subset_size else None
        ds = APTOS2019Dataset.from_directory(
            root=aptos_root / "train_images",
            labels_csv=aptos_root / "train.csv",
            subset_indices=subset,
            preprocessing=pipeline,
        )
        print(f"  APTOS 2019: {len(ds)} images")
        return evaluate_dataset(model, ds, config, device)
    except Exception as e:  # noqa: BLE001 — surface as skip, don't crash the run
        warnings.warn(f"APTOS evaluation failed: {e}", UserWarning)
        return {"status": "failed", "error": str(e)}


def _g_ratio(f1_external: float | None, f1_in_domain: float) -> float:
    """Compute G = F1_external / F1_in_domain, guarding NaN / zero divisor."""
    if (
        f1_external is None
        or not isinstance(f1_external, (int, float))
        or np.isnan(float(f1_external))
        or np.isnan(float(f1_in_domain))
        or float(f1_in_domain) <= 0.0
    ):
        return float("nan")
    return round(float(f1_external) / float(f1_in_domain), 4)


def _fmt(x: float) -> str:
    """Format a possibly-NaN ratio for console output."""
    return "nan" if not isinstance(x, float) or np.isnan(x) else f"{x:.3f}"
