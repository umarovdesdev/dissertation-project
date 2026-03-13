"""Experiment 6: Device Domain Shift (H-6, PC-9).

Tests H-6: model trained on EyePACS (Canon CR-1) is evaluated WITHOUT
retraining on datasets captured by other camera manufacturers to assess
preprocessing-induced device normalization.

Camera groups (per RESEARCH_ARCHITECTURE §5.6):
  Canon  (in-domain):  EyePACS training/val
  Kowa   (out-domain): IDRiD
  Mixed  (out-domain): DDR  (Canon + Topcon, no per-image metadata)
  Mixed  (out-domain): ODIR-5K (Canon + Zeiss, no per-image metadata)
  Topcon (out-domain): Messidor — SKIPPED until loader available
  Mixed  (out-domain): RFMiD   — SKIPPED if dataset directory not found

H-6 criterion: weighted-F1 variance across camera groups is within
acceptable bounds (no single group drops below G_threshold = 0.70).

Output: <output_dir>/exp6/device_shift_results.json
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.data.datasets import DDRDataset, IDRiDDataset, ODIR5KDataset
from src.data.label_harmonization import get_dataset_camera_groups
from src.experiments._eval_utils import (
    build_full_pipeline,
    evaluate_dataset,
    load_or_train_model,
)
from src.utils.seed import set_seed

# Minimum G ratio to consider H-6 "acceptable" per camera group
_G_FLOOR = 0.70


# ── Entry point ───────────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
) -> None:
    """Run Experiment 6: device domain shift evaluation.

    Args:
        config: Full merged config dict.
        fold: Unused — included for CLI interface consistency.
        resume: Resume from checkpoint if training fresh.
        _subset_size: Limit dataset rows for each group (smoke test).
    """
    set_seed(config.get("seed", 42))

    output_dir = Path(config["paths"]["output_dir"]) / "exp6"
    output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ── Load / train model ────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Exp6 — Loading trained EfficientNet-B3 model …")
    print(f"{'='*65}")
    model, eyepacs_f1 = load_or_train_model(
        config, output_dir, subset_size=_subset_size, resume=resume
    )
    model = model.to(device).eval()
    print(f"  Canon (EyePACS) in-domain F1 = {eyepacs_f1:.4f}")

    pipeline = build_full_pipeline(config["preprocessing"])

    results: dict[str, Any] = {
        "model":    "efficientnet_b3",
        "pipeline": "full_pipeline",
        "g_floor":  _G_FLOOR,
        "camera_groups": get_dataset_camera_groups(),
        "in_domain": {
            "canon_eyepacs": {
                "weighted_f1": float(eyepacs_f1),
                "source":      "exp1 checkpoint or freshly trained fold 0",
            }
        },
        "cross_device": {},
    }

    in_domain_f1 = eyepacs_f1

    # ── Kowa — IDRiD ──────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Evaluating camera group: Kowa (IDRiD) …")
    print(f"{'='*65}")
    results["cross_device"]["kowa_idrid"] = _eval_idrid(
        config, model, pipeline, device, _subset_size
    )

    # ── Mixed — DDR ───────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Evaluating camera group: Mixed Canon+Topcon (DDR test split) …")
    print(f"{'='*65}")
    results["cross_device"]["mixed_ddr"] = _eval_ddr(
        config, model, pipeline, device, _subset_size
    )

    # ── Mixed — ODIR-5K ───────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Evaluating camera group: Mixed Canon+Zeiss (ODIR-5K) …")
    print(f"{'='*65}")
    results["cross_device"]["mixed_odir5k"] = _eval_odir5k(
        config, model, pipeline, device, _subset_size
    )

    # ── Topcon — Messidor (skipped — no loader) ───────────────────────────────
    print("\nTopcon (Messidor): SKIPPED — no DR grade file; "
          "implement harmonize_messidor2_labels() to enable.")
    results["cross_device"]["topcon_messidor"] = {
        "status": "skipped",
        "reason": "Messidor DR grades not available — see harmonize_messidor2_labels()",
    }

    # ── RFMiD (skipped if directory not found) ────────────────────────────────
    rfmid_root = Path(config["paths"].get("rfmid", ""))
    if rfmid_root.exists():
        print(f"\n{'='*65}")
        print("Evaluating camera group: Mixed Topcon+Kowa (RFMiD) …")
        print(f"{'='*65}")
        results["cross_device"]["mixed_rfmid"] = _eval_rfmid(
            config, model, pipeline, device, _subset_size
        )
    else:
        print(f"\nRFMiD: SKIPPED — dataset directory not found at {rfmid_root}")
        results["cross_device"]["mixed_rfmid"] = {
            "status": "skipped",
            "reason": f"RFMiD not found at {rfmid_root}",
        }

    # ── Generalization ratios ─────────────────────────────────────────────────
    if not np.isnan(in_domain_f1) and in_domain_f1 > 0:
        for group_name, group_res in results["cross_device"].items():
            if "weighted_f1" in group_res:
                g = float(group_res["weighted_f1"]) / in_domain_f1
                group_res["g_ratio"] = round(g, 4)
    else:
        for group_res in results["cross_device"].values():
            if "weighted_f1" in group_res:
                group_res["g_ratio"] = float("nan")

    # ── Cross-device variance ─────────────────────────────────────────────────
    f1_values = [
        v["weighted_f1"]
        for v in results["cross_device"].values()
        if isinstance(v.get("weighted_f1"), float) and not np.isnan(v["weighted_f1"])
    ]
    auc_values = [
        v["roc_auc"]
        for v in results["cross_device"].values()
        if isinstance(v.get("roc_auc"), float) and not np.isnan(v["roc_auc"])
    ]
    results["cross_device_variance"] = {
        "weighted_f1_std": float(np.std(f1_values))  if f1_values  else float("nan"),
        "roc_auc_std":     float(np.std(auc_values)) if auc_values else float("nan"),
        "n_groups":        len(f1_values),
    }

    # ── H-6 test ──────────────────────────────────────────────────────────────
    # H-6: all evaluated groups maintain G >= _G_FLOOR (no severe drop)
    groups_below_floor = [
        g for g, v in results["cross_device"].items()
        if isinstance(v.get("g_ratio"), float)
        and not np.isnan(v["g_ratio"])
        and v["g_ratio"] < _G_FLOOR
    ]
    h6_supported = len(groups_below_floor) == 0 and len(f1_values) > 0
    results["h6_supported"]       = h6_supported
    results["groups_below_floor"] = groups_below_floor

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = output_dir / "device_shift_results.json"
    with open(out_path, "w") as f:
        json.dump(
            results, f, indent=2,
            default=lambda x: float(x) if isinstance(x, np.floating) else x,
        )
    print(f"\nResults saved → {out_path}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Experiment 6 — Device Domain Shift Summary")
    print(f"{'='*65}")
    print(f"  In-domain Canon (EyePACS) F1: {in_domain_f1:.4f}")
    for group, res in results["cross_device"].items():
        if "weighted_f1" not in res:
            print(f"  {group}: {res.get('status', 'unknown')}")
            continue
        g  = res.get("g_ratio", float("nan"))
        f1 = res["weighted_f1"]
        ok = "✓" if g >= _G_FLOOR else "✗"
        print(f"  {group:<20}: F1={f1:.4f}  G={g:.3f} {ok}")
    var_f1  = results["cross_device_variance"]["weighted_f1_std"]
    var_auc = results["cross_device_variance"]["roc_auc_std"]
    print(f"\n  Cross-device F1 std={var_f1:.4f}  AUC std={var_auc:.4f}")
    print(f"  H-6 supported: {h6_supported}")


# ── Dataset-specific evaluators ───────────────────────────────────────────────

def _eval_idrid(
    config: dict,
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
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
        return evaluate_dataset(model, ds, config, device)
    except Exception as e:
        warnings.warn(f"IDRiD evaluation failed: {e}", UserWarning)
        return {"status": "failed", "error": str(e)}


def _eval_ddr(
    config: dict,
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
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
        return evaluate_dataset(model, ds, config, device)
    except Exception as e:
        warnings.warn(f"DDR evaluation failed: {e}", UserWarning)
        return {"status": "failed", "error": str(e)}


def _eval_odir5k(
    config: dict,
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
    odir_root = config["paths"]["odir"]
    try:
        ds_full = ODIR5KDataset.from_directory(
            root=str(Path(odir_root) / "Training Set"),
            preprocessing=pipeline,
        )
        if subset_size is not None:
            from src.data.datasets import BaseFundusDataset
            import copy
            ds = copy.copy(ds_full)
            ds.image_paths = ds_full.image_paths[:subset_size]
            ds.labels      = ds_full.labels[:subset_size]
            ds.patient_ids = ds_full.patient_ids[:subset_size]
        else:
            ds = ds_full
        print(f"  ODIR-5K DR subset: {len(ds)} images")
        return evaluate_dataset(model, ds, config, device)
    except Exception as e:
        warnings.warn(f"ODIR-5K evaluation failed: {e}", UserWarning)
        return {"status": "failed", "error": str(e)}


def _eval_rfmid(
    config: dict,
    model: torch.nn.Module,
    pipeline: Any,
    device: torch.device,
    subset_size: int | None,
) -> dict[str, Any]:
    """Evaluate on RFMiD DR subset.  Returns skipped dict if unavailable."""
    # RFMiD does not have a dedicated loader yet — stub to be filled when
    # the dataset is added to DATASET_REGISTRY.
    warnings.warn(
        "RFMiD evaluation not yet implemented — dataset loader not available.",
        UserWarning,
    )
    return {"status": "skipped", "reason": "RFMiD loader not yet implemented"}
