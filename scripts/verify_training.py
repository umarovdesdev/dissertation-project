#!/usr/bin/env python3
"""Stage 4 verification: losses, metrics, trainer mini-loop."""

import sys
from pathlib import Path

import numpy as np
import torch

from src.training.losses import compute_class_weights, create_weighted_loss
from src.evaluation.metrics import (
    compute_primary_metrics,
    compute_secondary_metrics,
    compute_clinical_metrics,
    check_dominance,
    check_overfitting,
)
from src.evaluation.calibration import compute_ece, compute_brier_score

SEP = "=" * 60


# ── Test 1 — Class weights ────────────────────────────────────
print(SEP)
print("Test 1 — Class weights (inverse frequency)")
print(SEP)

labels_imb = [0] * 500 + [1] * 100 + [2] * 50 + [3] * 30 + [4] * 20
weights = compute_class_weights(labels_imb, num_classes=5)
print(f"  Weights: {[round(float(w), 4) for w in weights]}")
assert weights[0] < weights[1] < weights[2] < weights[3] < weights[4], \
    "Class 0 should have lowest weight, class 4 highest"
print(f"  Order check (0 < 1 < 2 < 3 < 4): OK")

loss_fn = create_weighted_loss(weights, device="cpu")
dummy_logits = torch.randn(4, 5)
dummy_labels = torch.tensor([0, 1, 2, 3])
loss_val = loss_fn(dummy_logits, dummy_labels)
print(f"  Weighted CrossEntropyLoss on dummy batch: {loss_val.item():.4f} (non-NaN OK)")
assert not torch.isnan(loss_val)


# ── Test 2 — Metrics ─────────────────────────────────────────
print(f"\n{SEP}")
print("Test 2 — Metrics computation")
print(SEP)

y_true = np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4])
y_pred = np.array([0, 1, 1, 1, 2, 3, 3, 3, 4, 4])
rng = np.random.default_rng(42)
raw = rng.random((10, 5))
y_prob = raw / raw.sum(axis=1, keepdims=True)   # proper softmax-like

primary = compute_primary_metrics(y_true, y_pred, y_prob, num_classes=5)
print(f"  Primary metrics:")
for k, v in primary.items():
    print(f"    {k}: {v:.4f}")
assert "weighted_f1" in primary
assert "roc_auc" in primary
assert "cohen_kappa_quadratic" in primary
assert "accuracy" in primary

secondary = compute_secondary_metrics(y_true, y_pred, num_classes=5)
print(f"  Secondary — macro_f1: {secondary['macro_f1']:.4f}")
print(f"  Secondary — per_class_f1: {[round(x,3) for x in secondary['per_class_f1']]}")
assert len(secondary["confusion_matrix"]) == 5

clinical = compute_clinical_metrics(y_true, y_pred, referable_threshold=2)
print(f"  Clinical — sensitivity: {clinical['sensitivity']:.4f}, "
      f"specificity: {clinical['specificity']:.4f}, "
      f"ppv: {clinical['ppv']:.4f}, npv: {clinical['npv']:.4f}")

ece = compute_ece(y_true, y_prob)
brier = compute_brier_score(y_true, y_prob)
print(f"  ECE: {ece:.4f}  |  Brier: {brier:.4f}")


# ── Test 3 — Dominance check ─────────────────────────────────
print(f"\n{SEP}")
print("Test 3 — check_dominance (EH-3)")
print(SEP)

baseline  = {"weighted_f1": 0.70, "roc_auc": 0.85, "cohen_kappa_quadratic": 0.60}
improved  = {"weighted_f1": 0.76, "roc_auc": 0.88, "cohen_kappa_quadratic": 0.65}
result = check_dominance(improved, baseline)
for k, v in result.items():
    print(f"  {k}: {v}")
assert result["overall_dominant"] is True, "Expected overall_dominant=True"
print(f"  overall_dominant: {result['overall_dominant']} ✓")

# Test a failing case
borderline = {"weighted_f1": 0.72, "roc_auc": 0.87, "cohen_kappa_quadratic": 0.62}
result_fail = check_dominance(borderline, baseline)
assert result_fail["overall_dominant"] is False, "Should fail: Δf1=2pp < 5pp"
print(f"  Failing case (Δf1=2pp): overall_dominant={result_fail['overall_dominant']} ✓")

overfit_result = check_overfitting(
    {"weighted_f1": 0.92, "accuracy": 0.93},
    {"weighted_f1": 0.72, "accuracy": 0.74},
)
print(f"  Overfitting check: {overfit_result}")
assert overfit_result["overall_is_overfitting"] is True


# ── Test 4 — Mini training loop ───────────────────────────────
print(f"\n{SEP}")
print("Test 4 — Mini training loop (2 epochs, 50 APTOS images, GPU)")
print(SEP)

from src.data.datasets import APTOS2019Dataset
from src.models.factory import create_model
from src.training.trainer import Trainer
from src.utils.config import load_config
from src.utils.seed import set_seed
from src.preprocessing.pipeline import PreprocessingPipeline

set_seed(42)
config = load_config("configs/default.yaml")

# Override for speed
config["training"]["max_epochs"] = 2
config["training"]["batch_size"] = 4
config["training"]["num_workers"] = 0
config["training"]["early_stopping"]["patience"] = 99

device_str = "cuda" if torch.cuda.is_available() else "cpu"
print(f"  Device: {device_str}")

# Baseline preprocessing (resize only — fast)
preprocessing = PreprocessingPipeline.create_baseline(target_size=512)

ds = APTOS2019Dataset.from_directory(
    root="/mnt/d/datasets/APTOS 2019/train_images",
    labels_csv="/mnt/d/datasets/APTOS 2019/train.csv",
    subset_indices=list(range(50)),
    preprocessing=preprocessing,
)
print(f"  Dataset size: {len(ds)}")

# Split 40 train / 10 val (no patient-level needed for smoke test)
train_idx = list(range(40))
val_idx   = list(range(40, 50))

from torch.utils.data import DataLoader, Subset
train_loader = DataLoader(Subset(ds, train_idx), batch_size=4, shuffle=True,  num_workers=0)
val_loader   = DataLoader(Subset(ds, val_idx),   batch_size=4, shuffle=False, num_workers=0)

model_cfg = config["models"]["resnet50"]
model = create_model("resnet50", model_cfg)

trainer = Trainer(config, device=device_str)

# Override metrics csv path to outputs/smoke_test/
smoke_dir = Path("outputs/smoke_test")
smoke_dir.mkdir(parents=True, exist_ok=True)
(smoke_dir / "checkpoints" / "fold_0").mkdir(parents=True, exist_ok=True)

from src.training.checkpoint import CheckpointManager
ckpt_mgr = CheckpointManager(smoke_dir / "checkpoints" / "fold_0", max_keep=2)
metrics_csv = smoke_dir / "metrics.csv"

# Patch max_epochs directly
trainer.max_epochs = 2

# Grab class weights manually for this tiny split
train_labels = [ds.labels[i] for i in train_idx]
weights = compute_class_weights(train_labels, num_classes=5)
criterion = create_weighted_loss(weights, device=device_str)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", patience=5)
scaler = torch.amp.GradScaler("cuda", enabled=(device_str == "cuda"))

model = model.to(device_str)
prev_loss = float("inf")

for epoch in range(2):
    train_m = trainer.train_one_epoch(model, train_loader, criterion, optimizer, scaler)
    val_m, preds, probs, lbls = trainer.evaluate(model, val_loader, criterion)
    scheduler.step(val_m.get("val_weighted_f1", 0.0))

    all_m = {**train_m, **val_m}
    ckpt_mgr.save_epoch(epoch, model, optimizer, scheduler, all_m, fold=0, config=config)
    trainer._append_metrics_csv(
        metrics_csv, epoch, 0, "smoke_test",
        train_m["train_loss"], val_m["val_loss"], val_m,
    )

    print(f"  Epoch {epoch}: train_loss={train_m['train_loss']:.4f}  "
          f"val_loss={val_m['val_loss']:.4f}  "
          f"val_F1={val_m.get('val_weighted_f1', float('nan')):.4f}")
    prev_loss = train_m["train_loss"]

# Verify outputs
assert metrics_csv.exists(), "metrics.csv not written"
assert (smoke_dir / "checkpoints" / "fold_0" / "best_model.pt").exists(), "best_model.pt missing"
assert (smoke_dir / "checkpoints" / "fold_0" / "last_checkpoint.pt").exists(), "last_checkpoint.pt missing"

csv_lines = metrics_csv.read_text().strip().split("\n")
print(f"\n  metrics.csv rows (incl. header): {len(csv_lines)}")
print(f"  Header: {csv_lines[0]}")
print(f"  Row 0:  {csv_lines[1]}")

print(f"\nAll 4 tests passed.")
