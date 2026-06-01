#!/usr/bin/env python3
"""Generate train_config_d.ipynb. One-shot authoring helper (kept for reproducibility)."""
import json
from pathlib import Path

def md(src): return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}
def code(src): return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src.splitlines(keepends=True)}

cells = []

cells.append(md(
"""# Train Config D (Full V5 + EfficientNet-B3) on EyePACS

Single-fold-per-session training to fit Kaggle's 12 h limit. Change `FOLD`
between sessions: `0 -> 1 -> 2 -> 3 -> 4`, attaching the previous session's
output as an input each time so `--resume` can pick up.

**Before running:** Add Input ->
1. Competition `diabetic-retinopathy-detection` (the 2015 EyePACS DR detection),
   **or** any attached dataset that contains EyePACS `trainLabels.csv` + `*.jpeg`
   train images.
2. (folds 1-4 only) the previous fold's saved output, so checkpoints resume.

Source repo: https://github.com/yesmukhamedov/dr-classifier
"""))

cells.append(md("## 1. Clone repo + install deps"))
cells.append(code(
"""!git clone --depth 1 https://github.com/yesmukhamedov/dr-classifier.git /kaggle/working/repo
%cd /kaggle/working/repo
!pip install -q -r requirements.txt
!pip install -q timm        # required by src/models/efficientnet.py, not in requirements.txt
"""))

cells.append(md("## 2. Sanity checks"))
cells.append(code(
"""!nvidia-smi
import torch
print("torch", torch.__version__, "| cuda:", torch.cuda.is_available())
!ls /kaggle/input
"""))

cells.append(md(
"""## 3. EyePACS layout adapter

`exp1` expects a root dir containing `trainLabels.csv` (columns: `image`,`level`)
and a `train/` subfolder of `<image>.jpeg` files. This cell auto-detects those
across every attached input and assembles `EYEPACS_ROOT` via symlinks (no copy,
no extra disk). If only the competition's multi-part zips are present it falls
back to extraction (slow + disk-heavy — see README)."""))
cells.append(code(
r'''import os, sys, subprocess
from pathlib import Path

INPUT = Path("/kaggle/input")
WORK  = Path("/kaggle/working/eyepacs")

def first(gen):
    for x in gen:
        return x
    return None

labels    = first(p for p in INPUT.rglob("trainLabels.csv") if p.is_file())
train_jpeg = first(p for p in INPUT.rglob("*.jpeg") if p.is_file())  # any EyePACS train image
train_dir  = train_jpeg.parent if train_jpeg else None

print("labels   :", labels)
print("train dir:", train_dir)

if labels is None or train_dir is None:
    # Fallback: extract the competition's zip parts. Heavy on disk/time.
    comp = INPUT / "diabetic-retinopathy-detection"
    print("\nNo ready-to-use layout found. Attempting extraction from", comp)
    WORK.mkdir(parents=True, exist_ok=True)
    if labels is None and (comp / "trainLabels.csv.zip").exists():
        subprocess.run(f"unzip -o -q '{comp}/trainLabels.csv.zip' -d '{WORK}'", shell=True, check=True)
        labels = WORK / "trainLabels.csv"
    parts = sorted(comp.glob("train.zip.0*"))
    if parts and not (WORK / "train").exists():
        print(f"Concatenating {len(parts)} train.zip parts and extracting (this is slow)...")
        subprocess.run(f"cat {comp}/train.zip.0* > /kaggle/working/train.zip", shell=True, check=True)
        subprocess.run(f"unzip -o -q /kaggle/working/train.zip -d '{WORK}'", shell=True, check=True)
        os.remove("/kaggle/working/train.zip")
        train_dir = WORK / "train"
    train_jpeg = first(p for p in WORK.rglob("*.jpeg") if p.is_file())
    train_dir  = train_jpeg.parent if train_jpeg else train_dir

assert labels is not None and train_dir is not None, \
    "Could not locate EyePACS labels/images. Check the attached inputs (see README)."

# Assemble EYEPACS_ROOT = {WORK}/ with a 'train' subdir + trainLabels.csv via symlinks.
WORK.mkdir(parents=True, exist_ok=True)
tgt_train  = WORK / "train"
tgt_labels = WORK / "trainLabels.csv"
if not tgt_train.exists():
    os.symlink(train_dir, tgt_train)
if not tgt_labels.exists():
    os.symlink(labels, tgt_labels)

EYEPACS_ROOT = str(WORK)
n_imgs = sum(1 for _ in tgt_train.glob("*.jpeg"))
print(f"\nEYEPACS_ROOT = {EYEPACS_ROOT}")
print(f"train images visible: {n_imgs}")
print(f"labels: {tgt_labels} -> {os.readlink(tgt_labels)}")
'''))

cells.append(md("## 4. Build merged config\n\nDeep-merges `default.yaml` <- `kaggle_paths.yaml` and injects the resolved EyePACS path. Writes `configs/kaggle_merged.yaml`, used by every command below."))
cells.append(code(
r'''subprocess.run([
    sys.executable, "kaggle/merge_config.py",
    "--base", "configs/default.yaml",
    "--override", "kaggle/kaggle_paths.yaml",
    "--out", "configs/kaggle_merged.yaml",
    f"paths.eyepacs={EYEPACS_ROOT}",
    # If you hit CUDA OOM at 512px (EfficientNet runs fp32), uncomment:
    # "training.batch_size=8",
], check=True)
'''))

cells.append(md(
"""## 5. (Optional) PCA eigenvectors for colour augmentation

One-shot. If skipped, colour augmentation is simply disabled (exp1 prints a
notice and continues). Output dir matches where exp1 looks:
`/kaggle/working/data/processed`. Comment out the cell to skip."""))
cells.append(code(
r'''subprocess.run([
    sys.executable, "scripts/compute_pca_eigvecs.py",
    "--dataset", "eyepacs",
    "--images-root", str(Path(EYEPACS_ROOT) / "train"),
    "--labels-csv", str(Path(EYEPACS_ROOT) / "trainLabels.csv"),
    "--output-dir", "/kaggle/working/data/processed",
    "--n-samples", "5000",
    "--seed", "42",
], check=True)
'''))

cells.append(md(
"""## 6. Dataset-specific normalization stats (Stage 7, D-2) — REQUIRED for Config D

The thesis (`methods/preprocessing-pipeline.md`, Stage 7) specifies that the
full configs (B/D) normalize with mean/std **computed from the EyePACS training
set after Stages 0–4, mask=1.0 pixels only** — *not* ImageNet (that is the
baseline-only fallback). This cell computes those stats and writes
`/kaggle/working/data/processed/eyepacs_norm_stats.json`, which
`exp1_factorial.py` loads automatically for Config D.

One-shot per dataset. `--n-samples 5000` gives a stable estimate; use `0` for
the full train set (much slower — Stage 1 OD-fovea rotation is the bottleneck)."""))
cells.append(code(
r'''subprocess.run([
    sys.executable, "scripts/compute_dataset_stats.py",
    "--images-root", str(Path(EYEPACS_ROOT) / "train"),
    "--labels-csv", str(Path(EYEPACS_ROOT) / "trainLabels.csv"),
    "--output-dir", "/kaggle/working/data/processed",
    "--n-samples", "5000",
    "--seed", "42",
], check=True)
'''))

cells.append(md("## 7. Train one fold\n\nSet `FOLD` per session. `--resume` continues from `last_checkpoint.pt` if the previous output is attached."))
cells.append(code(
r'''FOLD = 0   # <-- change to 1, 2, 3, 4 in subsequent sessions

subprocess.run([
    sys.executable, "run_experiment.py", "exp1",
    "--config", "configs/kaggle_merged.yaml",
    "--configs", "D",
    "--fold", str(FOLD),
    "--resume",
], check=True)
'''))

cells.append(md("## 8. Inspect outputs\n\nOutputs already live under `/kaggle/working/outputs`, which persists with *Save Version* — no copy needed. Best checkpoint is `best_model.pt`."))
cells.append(code(
r'''ckpt_dir = Path("/kaggle/working/outputs/exp1/checkpoints") / f"D_fold{FOLD}"
print("checkpoint dir:", ckpt_dir)
!ls -la {ckpt_dir}
print("\n--- metrics.csv (tail) ---")
!tail -n 15 /kaggle/working/outputs/exp1/metrics.csv
'''))

cells.append(md(
"""## 9. Multi-fold strategy

Run this notebook five times, once per fold:

| Session | `FOLD` | Add Input |
|---|---|---|
| 1 | 0 | competition (or EyePACS dataset) |
| 2 | 1 | + session-1 output dataset |
| 3 | 2 | + session-2 output dataset |
| 4 | 3 | + session-3 output dataset |
| 5 | 4 | + session-4 output dataset |

After each session: *Save Version -> Save & Run All (Commit)*. The committed
output (`/kaggle/working/outputs/...`) becomes a dataset you attach to the next
session so the adapter sees prior checkpoints and `--resume` continues.

When all five folds are done, download `/kaggle/working/outputs/exp1/` and place
it locally at `experiments/outputs/exp1/`, then run
`python scripts/verify_exp1.py`."""))

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path(__file__).parent / "train_config_d.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out)
