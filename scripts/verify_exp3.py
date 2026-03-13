#!/usr/bin/env python3
"""Exp3 smoke test: visual degradation samples + tiny training run.

Steps
-----
1. Visual check — apply all 3 degradation types × 3 severities to one APTOS
   image; save a comparison grid to outputs/figures/degradation_samples.png.
2. Smoke training — 100 APTOS images, 2 epochs, fold 0, gaussian_noise only
   (low & medium) to keep runtime short.
3. Verify JSON structure and required keys.
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np

from src.degradation import (
    apply_degradation,
    apply_gaussian_blur,
    apply_gaussian_noise,
    apply_low_illumination,
)
from src.experiments.exp3_robustness import run
from src.preprocessing.pipeline import PreprocessingPipeline
from src.utils.config import load_config, get_experiment_config
from src.utils.seed import set_seed

SEP = "=" * 65

# ── 1. Visual degradation check ───────────────────────────────────────────────
print(SEP)
print("Test 1: visual degradation samples (APTOS sample image)")
print(SEP)

sample_path = "/mnt/d/datasets/APTOS 2019/train_images/000c1434d8d7.png"
raw = cv2.imread(sample_path)
assert raw is not None, f"Cannot load {sample_path}"

# Resize for display grid (256×256 tiles)
TILE = 256
raw_tile = cv2.resize(raw, (TILE, TILE))

degradation_configs = [
    ("gaussian_noise",   "low"),
    ("gaussian_noise",   "medium"),
    ("gaussian_noise",   "high"),
    ("gaussian_blur",    "low"),
    ("gaussian_blur",    "medium"),
    ("gaussian_blur",    "high"),
    ("low_illumination", "low"),
    ("low_illumination", "medium"),
    ("low_illumination", "high"),
]

tiles: list[np.ndarray] = [raw_tile]
for deg_type, severity in degradation_configs:
    degraded = apply_degradation(raw_tile, deg_type, severity)
    tiles.append(degraded)

# Build a 2×5 grid (original + 9 degraded = 10 tiles; pad to 10)
n_cols = 5
n_rows = 2
grid_rows = []
for r in range(n_rows):
    row_tiles = tiles[r * n_cols: (r + 1) * n_cols]
    # Pad row if needed
    while len(row_tiles) < n_cols:
        row_tiles.append(np.zeros_like(raw_tile))
    grid_rows.append(np.hstack(row_tiles))
grid = np.vstack(grid_rows)

figures_dir = Path("outputs/figures")
figures_dir.mkdir(parents=True, exist_ok=True)
out_img = figures_dir / "degradation_samples.png"
cv2.imwrite(str(out_img), grid)
print(f"  Saved degradation grid → {out_img}")

# Sanity-check individual functions
noisy  = apply_gaussian_noise(raw_tile, sigma=30)
blured = apply_gaussian_blur(raw_tile, kernel_size=11)
dark   = apply_low_illumination(raw_tile, factor=0.5)
assert noisy.dtype  == np.uint8, "gaussian_noise must return uint8"
assert blured.dtype == np.uint8, "gaussian_blur must return uint8"
assert dark.dtype   == np.uint8, "low_illumination must return uint8"
assert noisy.shape  == raw_tile.shape
assert blured.shape == raw_tile.shape
assert dark.shape   == raw_tile.shape
print("  Function output shape/dtype assertions passed.")

# ── 2. Smoke training run ─────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 2: Exp3 smoke run (100 images, 2 epochs, fold 0, gaussian_noise)")
print(SEP)

config     = load_config("configs/default.yaml")
exp_config = get_experiment_config(config, "exp3")

# Speed overrides
exp_config["training"]["max_epochs"]                 = 2
exp_config["training"]["batch_size"]                 = 8
exp_config["training"]["num_workers"]                = 0
exp_config["training"]["early_stopping"]["patience"] = 99

set_seed(exp_config.get("seed", 42))

run(
    config=exp_config,
    fold=0,
    resume=False,
    _subset_size=100,
    _deg_types=["gaussian_noise"],
    _severity_levels=["low", "medium"],
)

# ── 3. Verify JSON structure ──────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 3: verify degradation_results.json structure")
print(SEP)

output_dir  = Path(exp_config["paths"]["output_dir"]) / "exp3"
results_json = output_dir / "degradation_results.json"

assert results_json.exists(), f"degradation_results.json missing at {results_json}"
with open(results_json) as f:
    results = json.load(f)

# Top-level keys
required_top = {"model", "pipeline", "dataset", "n_folds", "clean", "degradations"}
missing = required_top - results.keys()
assert not missing, f"Missing top-level keys: {missing}"

# Clean section keys
clean = results["clean"]
assert "mean" in clean,                 "'mean' missing from clean section"
assert "weighted_f1" in clean["mean"],  "'weighted_f1' missing from clean.mean"
assert "binary_roc_auc_mean" in clean,  "'binary_roc_auc_mean' missing from clean"
print(f"  Clean section OK — weighted_F1={clean['mean']['weighted_f1']:.4f}")

# Degradations section structure
deg = results["degradations"]
assert "gaussian_noise" in deg, "gaussian_noise missing from degradations"
for severity in ["low", "medium"]:
    entry = deg["gaussian_noise"][severity]
    assert "mean"       in entry, f"mean missing for gaussian_noise/{severity}"
    assert "delta_mean" in entry, f"delta_mean missing for gaussian_noise/{severity}"
    f1    = entry["mean"].get("weighted_f1", float("nan"))
    delta = entry["delta_mean"].get("weighted_f1", float("nan"))
    print(f"  gaussian_noise/{severity}: F1={f1:.4f}  ΔF1={delta:+.4f}")

# Checkpoint present
ckpt = output_dir / "checkpoints" / "full_pipeline_fold0" / "best_model.pt"
assert ckpt.exists(), f"Missing checkpoint: {ckpt}"
print(f"\nCheckpoint OK: {ckpt}")

print(f"\nAll Exp3 smoke-test assertions passed.")
