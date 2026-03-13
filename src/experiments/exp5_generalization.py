"""Experiment 5: Clinical Generalization (H-4, PC-6).

Tests H-4 (Cross-Database Transferability): model trained on EyePACS with full
preprocessing is applied WITHOUT retraining to external clinical datasets.
Generalization ratio G = F1_external / F1_EyePACS must satisfy G >= 0.85.

Evaluation datasets:
  - IDRiD: clinical validation (Indian population, Kowa camera)
  - DDR test split: large multi-centre dataset (Canon + Topcon)
  - Messidor-2: SKIPPED until DR grade file is available (warning emitted)

Output: <output_dir>/exp5/generalization_results.json
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.data.datasets import DDRDataset, IDRiDDataset
from src.data.label_harmonization import harmonize_messidor2_labels
from src.experiments._eval_utils import (
    build_full_pipeline,
    evaluate_dataset,
    load_or_train_model,
)
from src.utils.seed import set_seed

_G_THRESHOLD = 0.85


# ── Entry point ───────────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
) -> None:
    """Run Experiment 5: cross-database generalization evaluation.

    Args:
        config: Full merged config dict.
        fold: Unused — included for CLI interface consistency.
        resume: Resume from checkpoint if training fresh.
        _subset_size: Limit EyePACS + external dataset rows (smoke test).
    """
    set_seed(config.get("seed", 42))

    output_dir = Path(config["paths"]["output_dir"]) / "exp5"
    output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ── Load / train model ────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Exp5 — Loading trained EfficientNet-B3 model …")
    print(f"{'='*65}")
    model, eyepacs_f1 = load_or_train_model(
        config, output_dir, subset_size=_subset_size, resume=resume
    )
    model = model.to(device).eval()
    print(f"  EyePACS baseline F1 = {eyepacs_f1:.4f}")

    pipeline = build_full_pipeline(config["preprocessing"])

    results: dict[str, Any] = {
        "model":         "efficientnet_b3",
        "pipeline":      "full_pipeline",
        "g_threshold":   _G_THRESHOLD,
        "eyepacs_baseline": {
            "weighted_f1": float(eyepacs_f1),
            "source":      "exp1 checkpoint or freshly trained fold 0",
        },
        "external_datasets": {},
    }

    # ── Messidor-2 (stub — skip until grade file available) ───────────────────
    messidor2_csv = str(Path(config["paths"].get("messidor2", "")) / "messidor2.csv")
    m2_paths, m2_labels = harmonize_messidor2_labels(messidor2_csv)
    if not m2_paths:
        print("\nMessidor-2: SKIPPED — DR grade file not available (see harmonize_messidor2_labels)")
        results["external_datasets"]["messidor2"] = {
            "status": "skipped",
            "reason": "DR grades not available — see harmonize_messidor2_labels()",
        }

    # ── IDRiD ─────────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Evaluating on IDRiD …")
    print(f"{'='*65}")
    idrid_results = _eval_idrid(config, model, pipeline, device, _subset_size)
    results["external_datasets"]["idrid"] = idrid_results

    # ── DDR ───────────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Evaluating on DDR (test split) …")
    print(f"{'='*65}")
    ddr_results = _eval_ddr(config, model, pipeline, device, _subset_size)
    results["external_datasets"]["ddr"] = ddr_results

    # ── Compute generalization ratios ─────────────────────────────────────────
    if not np.isnan(eyepacs_f1) and eyepacs_f1 > 0:
        for ds_name, ds_res in results["external_datasets"].items():
            if "weighted_f1" in ds_res:
                g = float(ds_res["weighted_f1"]) / eyepacs_f1
                ds_res["g_ratio"] = round(g, 4)
    else:
        for ds_res in results["external_datasets"].values():
            if "weighted_f1" in ds_res:
                ds_res["g_ratio"] = float("nan")

    # ── H-4 test ──────────────────────────────────────────────────────────────
    g_ratios = [
        v["g_ratio"]
        for v in results["external_datasets"].values()
        if isinstance(v.get("g_ratio"), float) and not np.isnan(v["g_ratio"])
    ]
    datasets_meeting_threshold = [
        ds for ds, v in results["external_datasets"].items()
        if isinstance(v.get("g_ratio"), float)
        and not np.isnan(v["g_ratio"])
        and v["g_ratio"] >= _G_THRESHOLD
    ]
    h4_supported = len(datasets_meeting_threshold) >= 2
    results["h4_supported"]              = h4_supported
    results["datasets_meeting_threshold"] = datasets_meeting_threshold

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = output_dir / "generalization_results.json"
    with open(out_path, "w") as f:
        json.dump(
            results, f, indent=2,
            default=lambda x: float(x) if isinstance(x, np.floating) else x,
        )
    print(f"\nResults saved → {out_path}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Experiment 5 — Generalization Summary")
    print(f"{'='*65}")
    print(f"  EyePACS baseline F1: {eyepacs_f1:.4f}")
    for ds_name, ds_res in results["external_datasets"].items():
        if "weighted_f1" not in ds_res:
            print(f"  {ds_name}: {ds_res.get('status', 'unknown')}")
            continue
        f1  = ds_res["weighted_f1"]
        g   = ds_res.get("g_ratio", float("nan"))
        auc = ds_res.get("roc_auc", float("nan"))
        ok  = "✓" if g >= _G_THRESHOLD else "✗"
        print(f"  {ds_name:<12}: F1={f1:.4f}  G={g:.3f} {ok}  AUC={auc:.4f}")
    print(f"\n  H-4 supported: {h4_supported} "
          f"({len(datasets_meeting_threshold)}/{len(g_ratios)} datasets G≥{_G_THRESHOLD})")


# ── Dataset-specific evaluators ───────────────────────────────────────────────

def _eval_idrid(
    config: dict,
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
    """Evaluate on IDRiD training set (full, no retraining)."""
    idrid_root = config["paths"]["idrid"]
    try:
        subset = list(range(subset_size)) if subset_size else None
        ds = IDRiDDataset.from_directory(
            root=str(Path(idrid_root) / "B. Disease Grading" /
                      "1. Original Images" / "a. Training Set"),
            labels_csv=str(Path(idrid_root) / "B. Disease Grading" /
                           "2. Groundtruths" /
                           "a. IDRiD_Disease Grading_Training Labels.csv"),
            subset_indices=subset,
            preprocessing=pipeline,
        )
        print(f"  IDRiD: {len(ds)} images")
        metrics = evaluate_dataset(model, ds, config, device)
        _print_metrics("IDRiD", metrics)
        return metrics
    except Exception as e:
        msg = f"IDRiD evaluation failed: {e}"
        warnings.warn(msg, UserWarning)
        return {"status": "failed", "error": str(e)}


def _eval_ddr(
    config: dict,
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
    """Evaluate on DDR test split (no retraining)."""
    ddr_root = config["paths"]["ddr"]
    try:
        subset = list(range(subset_size)) if subset_size else None
        ds = DDRDataset.from_directory(
            root=str(Path(ddr_root) / "DR_grading"),
            split="test",
            subset_indices=subset,
            preprocessing=pipeline,
        )
        print(f"  DDR test: {len(ds)} images")
        metrics = evaluate_dataset(model, ds, config, device)
        _print_metrics("DDR", metrics)
        return metrics
    except Exception as e:
        msg = f"DDR evaluation failed: {e}"
        warnings.warn(msg, UserWarning)
        return {"status": "failed", "error": str(e)}


def _print_metrics(name: str, m: dict[str, float]) -> None:
    print(f"  {name}: F1={m.get('weighted_f1', float('nan')):.4f}  "
          f"AUC={m.get('roc_auc', float('nan')):.4f}  "
          f"Kappa={m.get('cohen_kappa_quadratic', float('nan')):.4f}  "
          f"Acc={m.get('accuracy', float('nan')):.4f}  "
          f"Sens={m.get('sensitivity', float('nan')):.4f}  "
          f"Spec={m.get('specificity', float('nan')):.4f}")
