#!/usr/bin/env python3
"""Quick smoke-test for Experiment 1 — 200 images, 2 epochs, config A, fold 0."""

import json
from pathlib import Path

from src.utils.config import load_config, get_experiment_config
from src.utils.seed import set_seed
from src.experiments.exp1_factorial import run

# ── Load and patch config ──────────────────────────────────────────────────
config = load_config("configs/default.yaml")
exp_config = get_experiment_config(config, "exp1")

# Speed overrides (do NOT modify actual config file)
exp_config["training"]["max_epochs"]                   = 2
exp_config["training"]["batch_size"]                   = 8
exp_config["training"]["num_workers"]                  = 0
exp_config["training"]["early_stopping"]["patience"]   = 99
exp_config["cross_validation"]["n_folds"]              = 5  # kept for split logic

set_seed(exp_config.get("seed", 42))

print("=" * 65)
print("Exp1 smoke test: 200 EyePACS images | 2 epochs | config A | fold 0")
print("=" * 65)

run(
    config=exp_config,
    fold=0,               # single fold only
    resume=False,
    _subset_size=200,     # first 200 CSV rows
    _configs_to_run=["A"],  # config A only
)

# ── Verify outputs ─────────────────────────────────────────────────────────
output_dir = Path(exp_config["paths"]["output_dir"]) / "exp1"

metrics_csv = output_dir / "metrics.csv"
assert metrics_csv.exists(), f"metrics.csv not found at {metrics_csv}"
rows = metrics_csv.read_text().strip().split("\n")
print(f"\nmetrics.csv — {len(rows)} lines (header + {len(rows)-1} epoch rows)")
print(f"  Header : {rows[0]}")
for r in rows[1:]:
    print(f"  Row    : {r}")

ckpt_best = output_dir / "checkpoints" / "A_fold0" / "best_model.pt"
ckpt_last = output_dir / "checkpoints" / "A_fold0" / "last_checkpoint.pt"
assert ckpt_best.exists(), f"best_model.pt missing at {ckpt_best}"
assert ckpt_last.exists(), f"last_checkpoint.pt missing at {ckpt_last}"
print(f"\nCheckpoints OK:")
print(f"  {ckpt_best}")
print(f"  {ckpt_last}")

print("\nAll smoke-test assertions passed.")
