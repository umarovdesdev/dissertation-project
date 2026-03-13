#!/usr/bin/env python3
"""Verify Experiments 5 and 6 — label harmonization + smoke evaluation pipeline.

Test 1 — Label harmonization utilities (no dataset needed).
Test 2 — Exp5 smoke: evaluate pretrained ResNet-50 on 50 IDRiD images.
Test 3 — Exp6 smoke: evaluate same model on 50 DDR images, verify JSON structure.

No training is performed.  Both tests verify the inference pipeline by using
ImageNet pretrained weights (metrics will be meaningless without DR training —
the purpose is to confirm the plumbing, not the numbers).
"""

import json
import warnings
from pathlib import Path

import numpy as np
import torch

from src.data.datasets import DDRDataset, IDRiDDataset
from src.data.label_harmonization import (
    DR_CLASSES,
    get_dataset_camera_groups,
    harmonize_messidor2_labels,
    to_binary_referable,
)
from src.experiments._eval_utils import build_full_pipeline, evaluate_dataset
from src.models.factory import create_model
from src.utils.config import load_config
from src.utils.seed import set_seed

SEP = "=" * 65

config = load_config("configs/default.yaml")
set_seed(config.get("seed", 42))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Test 1: Label harmonization ───────────────────────────────────────────────
print(SEP)
print("Test 1: label harmonization utilities")
print(SEP)

print("\n  DR_CLASSES:")
for grade, name in DR_CLASSES.items():
    binary = to_binary_referable(grade)
    print(f"    grade {grade}: {name!r:<22} → binary={binary}")

# Assertions
assert to_binary_referable(0) == 0
assert to_binary_referable(1) == 0
assert to_binary_referable(2) == 1
assert to_binary_referable(3) == 1
assert to_binary_referable(4) == 1
assert to_binary_referable(1, threshold=1) == 1
print("\n  to_binary_referable assertions passed.")

camera_groups = get_dataset_camera_groups()
print(f"\n  Camera groups: {camera_groups}")
assert "canon" in camera_groups
assert "kowa" in camera_groups
assert "eyepacs" in camera_groups["canon"]
assert "idrid" in camera_groups["kowa"]
print("  get_dataset_camera_groups assertions passed.")

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    paths, labels = harmonize_messidor2_labels("/nonexistent/messidor2.csv")
assert paths == [] and labels == []
assert len(w) >= 1 and "messidor" in str(w[0].message).lower()
print("  harmonize_messidor2_labels stub warning raised as expected.")

# ── Shared: load pretrained ResNet-50 (no DR training) ───────────────────────
print(f"\n{SEP}")
print("Creating pretrained ResNet-50 (ImageNet weights, no DR training)")
print(SEP)

model_cfg = config["models"]["resnet50"]
model = create_model("resnet50", model_cfg)
model = model.to(device).eval()
print(f"  Model on {device}")

pipeline    = build_full_pipeline(config["preprocessing"])
SUBSET_SIZE = 50

# ── Test 2: Exp5 smoke — IDRiD evaluation ────────────────────────────────────
print(f"\n{SEP}")
print(f"Test 2: Exp5 smoke — evaluate on first {SUBSET_SIZE} IDRiD images")
print(SEP)

idrid_root = config["paths"]["idrid"]
idrid_ds = IDRiDDataset.from_directory(
    root=str(Path(idrid_root) / "B. Disease Grading" /
             "1. Original Images" / "a. Training Set"),
    labels_csv=str(Path(idrid_root) / "B. Disease Grading" / "2. Groundtruths" /
                   "a. IDRiD_Disease Grading_Training Labels.csv"),
    subset_indices=list(range(SUBSET_SIZE)),
    preprocessing=pipeline,
)
print(f"  IDRiD subset: {len(idrid_ds)} images")

# Override num_workers and batch_size for the smoke test
smoke_config = dict(config)
smoke_config["training"] = dict(config["training"])
smoke_config["training"]["num_workers"] = 0
smoke_config["training"]["batch_size"]  = 8

idrid_metrics = evaluate_dataset(model, idrid_ds, smoke_config, device)

print(f"\n  IDRiD metrics (ImageNet pretrained — not meaningful, just pipeline check):")
print(f"    F1={idrid_metrics.get('weighted_f1', float('nan')):.4f}  "
      f"AUC={idrid_metrics.get('roc_auc', float('nan')):.4f}  "
      f"Acc={idrid_metrics.get('accuracy', float('nan')):.4f}")
print(f"    Sensitivity={idrid_metrics.get('sensitivity', float('nan')):.4f}  "
      f"Specificity={idrid_metrics.get('specificity', float('nan')):.4f}")
print(f"    binary_ROC-AUC={idrid_metrics.get('binary_roc_auc', float('nan')):.4f}")

# Structural assertions — just check keys and ranges, not values
required_keys = {"weighted_f1", "roc_auc", "accuracy", "sensitivity", "specificity",
                 "ppv", "npv", "binary_roc_auc"}
missing = required_keys - idrid_metrics.keys()
assert not missing, f"Missing keys in IDRiD metrics: {missing}"

# Build a minimal generalization_results.json for structural verification
eyepacs_f1 = 0.70  # placeholder — no exp1 checkpoint in smoke test
g_ratio = idrid_metrics["weighted_f1"] / eyepacs_f1 if eyepacs_f1 > 0 else float("nan")

exp5_results = {
    "model":    "resnet50",
    "pipeline": "full_pipeline",
    "g_threshold": 0.85,
    "eyepacs_baseline": {"weighted_f1": eyepacs_f1, "source": "smoke_test_placeholder"},
    "external_datasets": {
        "idrid": {**idrid_metrics, "g_ratio": round(g_ratio, 4)},
    },
    "h4_supported": g_ratio >= 0.85,
    "datasets_meeting_threshold": ["idrid"] if g_ratio >= 0.85 else [],
}

output_dir = Path(config["paths"]["output_dir"]) / "exp5"
output_dir.mkdir(parents=True, exist_ok=True)
smoke_json = output_dir / "generalization_results_smoke.json"
with open(smoke_json, "w") as f:
    json.dump(exp5_results, f, indent=2,
              default=lambda x: float(x) if isinstance(x, np.floating) else x)

assert smoke_json.exists()
loaded = json.loads(smoke_json.read_text())
assert "h4_supported" in loaded
assert "external_datasets" in loaded
assert "idrid" in loaded["external_datasets"]
print(f"\n  generalization_results structure OK → {smoke_json}")
print("  IDRiD pipeline smoke test passed.")

# ── Test 3: Exp6 smoke — DDR evaluation ──────────────────────────────────────
print(f"\n{SEP}")
print(f"Test 3: Exp6 smoke — evaluate on first {SUBSET_SIZE} DDR test images")
print(SEP)

ddr_root = config["paths"]["ddr"]
ddr_ds = DDRDataset.from_directory(
    root=str(Path(ddr_root) / "DR_grading"),
    split="test",
    subset_indices=list(range(SUBSET_SIZE)),
    preprocessing=pipeline,
)
print(f"  DDR test subset: {len(ddr_ds)} images")

ddr_metrics = evaluate_dataset(model, ddr_ds, smoke_config, device)
print(f"\n  DDR metrics (ImageNet pretrained — pipeline check only):")
print(f"    F1={ddr_metrics.get('weighted_f1', float('nan')):.4f}  "
      f"AUC={ddr_metrics.get('roc_auc', float('nan')):.4f}  "
      f"Acc={ddr_metrics.get('accuracy', float('nan')):.4f}")

# Build device_shift_results structure
g_idrid = idrid_metrics["weighted_f1"] / eyepacs_f1 if eyepacs_f1 > 0 else float("nan")
g_ddr   = ddr_metrics["weighted_f1"]   / eyepacs_f1 if eyepacs_f1 > 0 else float("nan")

exp6_results = {
    "model":    "resnet50",
    "pipeline": "full_pipeline",
    "g_floor":  0.70,
    "camera_groups": get_dataset_camera_groups(),
    "in_domain": {
        "canon_eyepacs": {"weighted_f1": eyepacs_f1, "source": "smoke_test_placeholder"},
    },
    "cross_device": {
        "kowa_idrid":  {**idrid_metrics, "g_ratio": round(g_idrid, 4)},
        "mixed_ddr":   {**ddr_metrics,   "g_ratio": round(g_ddr,   4)},
        "mixed_odir5k":  {"status": "skipped", "reason": "smoke test"},
        "topcon_messidor": {"status": "skipped", "reason": "smoke test"},
    },
    "cross_device_variance": {
        "weighted_f1_std": float(np.std([idrid_metrics["weighted_f1"],
                                          ddr_metrics["weighted_f1"]])),
        "roc_auc_std": float(np.std([idrid_metrics.get("roc_auc", 0),
                                      ddr_metrics.get("roc_auc", 0)])),
        "n_groups": 2,
    },
    "h6_supported": all(g >= 0.70 for g in [g_idrid, g_ddr] if not np.isnan(g)),
    "groups_below_floor": [],
}

exp6_dir = Path(config["paths"]["output_dir"]) / "exp6"
exp6_dir.mkdir(parents=True, exist_ok=True)
shift_json = exp6_dir / "device_shift_results_smoke.json"
with open(shift_json, "w") as f:
    json.dump(exp6_results, f, indent=2,
              default=lambda x: float(x) if isinstance(x, np.floating) else x)

assert shift_json.exists()
loaded6 = json.loads(shift_json.read_text())

# Verify required top-level keys
for key in ["in_domain", "cross_device", "cross_device_variance",
            "h6_supported", "camera_groups"]:
    assert key in loaded6, f"Missing key in device_shift_results: {key}"

# Verify variance section
var = loaded6["cross_device_variance"]
assert "weighted_f1_std" in var
assert "roc_auc_std" in var
assert "n_groups" in var

print(f"\n  device_shift_results structure OK → {shift_json}")
f1_std  = var["weighted_f1_std"]
auc_std = var["roc_auc_std"]
print(f"  cross-device F1 std={f1_std:.4f}  AUC std={auc_std:.4f}")

missing_keys = required_keys - ddr_metrics.keys()
assert not missing_keys, f"Missing keys in DDR metrics: {missing_keys}"
print("  DDR pipeline smoke test passed.")

print(f"\n{'='*65}")
print("All Exp5/Exp6 smoke-test assertions passed.")
