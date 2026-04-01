#!/usr/bin/env python3
"""Exp2 smoke test: quality metrics + ablation (levels 1&5, fold 0) + CLAHE sweep (2 values)."""

import cv2
import numpy as np
from pathlib import Path

from src.utils.config import load_config, get_experiment_config
from src.utils.seed import set_seed
from src.utils.image_quality import compute_all_quality_metrics
from src.preprocessing.pipeline import PreprocessingPipeline
from src.experiments.exp2_ablation import run

SEP = "=" * 65

# ── Test image quality metrics ────────────────────────────────────────────────
print(SEP)
print("Test: image quality metrics (APTOS sample image)")
print(SEP)

sample_path = "/mnt/d/datasets/APTOS 2019/train_images/000c1434d8d7.png"
raw = cv2.imread(sample_path)
assert raw is not None, f"Cannot load {sample_path}"

baseline = PreprocessingPipeline.create_baseline(target_size=512)
full     = PreprocessingPipeline.create_full()

raw_resized   = baseline(raw)
full_processed = full(raw)

q_raw  = compute_all_quality_metrics(raw_resized, original=raw_resized)
q_full = compute_all_quality_metrics(full_processed, original=raw_resized)

print(f"  Baseline (resize only):")
print(f"    CNR={q_raw['cnr']:.4f}  Entropy={q_raw['entropy']:.4f}  SSIM={q_raw['ssim']:.4f}")
print(f"  Full pipeline:")
print(f"    CNR={q_full['cnr']:.4f}  Entropy={q_full['entropy']:.4f}  SSIM={q_full['ssim']:.4f}")

assert q_raw["cnr"] >= 0, "CNR must be non-negative"
assert 0 < q_raw["entropy"] < 9, "Entropy should be in (0, 8] bits for 256 bins"
assert 0 <= q_raw["ssim"] <= 1, "SSIM self-comparison should be 1"
print("  Assertions passed.")

# ── Exp2 smoke test ───────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Exp2 smoke test: 100 EyePACS images | 2 epochs | levels 1&5 | fold 0")
print(f"         + CLAHE sweep clip=[2.0, 4.0] on IDRiD (2 epochs)")
print(SEP)

config = load_config("configs/default.yaml")
exp_config = get_experiment_config(config, "exp2")

# Speed overrides
exp_config["training"]["max_epochs"]                  = 2
exp_config["training"]["batch_size"]                  = 8
exp_config["training"]["num_workers"]                 = 0
exp_config["training"]["early_stopping"]["patience"]  = 99

set_seed(exp_config.get("seed", 42))

run(
    config=exp_config,
    fold=0,
    resume=False,
    _subset_size=100,
    _levels_to_run=["resize_only", "full_pipeline"],
    _clahe_values=[2.0, 4.0],
    _quality_n_samples=10,
)

# ── Verify outputs ────────────────────────────────────────────────────────────
output_dir = Path(exp_config["paths"]["output_dir"]) / "exp2"

metrics_csv = output_dir / "metrics.csv"
assert metrics_csv.exists(), f"metrics.csv missing at {metrics_csv}"
rows = metrics_csv.read_text().strip().split("\n")
print(f"\nmetrics.csv — {len(rows)} lines (header + {len(rows)-1} epoch rows)")
print(f"  Header: {rows[0]}")

clahe_json = output_dir / "clahe_sweep.json"
assert clahe_json.exists(), f"clahe_sweep.json missing"
import json
sweep = json.loads(clahe_json.read_text())
assert "2.0" in sweep and "4.0" in sweep, "Expected clip_limit keys 2.0 and 4.0"
print(f"\nclahe_sweep.json — keys: {list(sweep.keys())}")
for k, v in sweep.items():
    print(f"  clip={k}: weighted_F1={v.get('weighted_f1', float('nan')):.4f}  "
          f"DR1_F1={v.get('dr1_f1', float('nan')):.4f}  "
          f"DR2_F1={v.get('dr2_f1', float('nan')):.4f}")

# Checkpoints for both levels
for level in ["resize_only", "full_pipeline"]:
    ckpt = output_dir / "checkpoints" / f"{level}_fold0" / "best_model.pt"
    assert ckpt.exists(), f"Missing checkpoint: {ckpt}"
    print(f"\nCheckpoint OK: {ckpt}")

print(f"\nAll Exp2 smoke-test assertions passed.")
