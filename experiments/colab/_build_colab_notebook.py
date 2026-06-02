#!/usr/bin/env python3
"""Generate train_config_d_colab.ipynb.

One-shot authoring helper (kept for reproducibility), mirroring
kaggle/_build_notebook.py but targeting Google Colab:

* No auto-mounted dataset -> download via the Kaggle API (kaggle.json / Colab
  Secrets). A DATASET switch picks APTOS (quick functional test, ~3.7k imgs) or
  EyePACS (the real Config-D run, ~35k imgs).
* Ephemeral /content disk -> checkpoints + processed artifacts persist on a
  mounted Google Drive so the per-fold `--resume` survives Colab's ~12 h cap and
  idle disconnects (no dataset re-attach dance like Kaggle).

Run:  python experiments/colab/_build_colab_notebook.py
"""
import json
from pathlib import Path


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": src.splitlines(keepends=True)}


cells = []

cells.append(md(
"""# Train Config D (Full V5 + EfficientNet-B3) on Google Colab

Same Experiment-1 / Config-D run as the Kaggle notebook, ported to Colab.

**Why Colab:** to run alongside the Kaggle session (Kaggle caps GPU at 12 h).
Colab free *also* caps ~12 h and disconnects on idle, so the strategy is
unchanged: **one fold per session, `--resume`**. The difference is persistence —
checkpoints + dataset-stats live on **Google Drive**, so the next session resumes
automatically (no Kaggle "attach previous output" dance).

## Two modes (set `DATASET` in the config cell)
* `"aptos"`  — APTOS 2019 (~3.7k imgs). **Quick functional test** that the Colab
  pipeline works end-to-end in minutes. The adapter auto-converts APTOS into the
  EyePACS layout; Config D / Full V5 / EfficientNet-B3 are otherwise identical.
* `"eyepacs"` — EyePACS (~35k imgs). **The real Config-D run.**

## What you must provide (one-time, minimal)
1. **Kaggle API token** — to download the dataset. Either:
   * add `KAGGLE_USERNAME` + `KAGGLE_KEY` to **Colab Secrets** (🔑 left sidebar) —
     preferred, no upload; **or**
   * upload `kaggle.json` when the credentials cell prompts (Kaggle → Account →
     *Create New API Token*).
2. **Google Drive** — click *Authorize* on the mount cell (OAuth popup).
3. For `DATASET="aptos"`: accept the competition rules once at
   <https://www.kaggle.com/competitions/aptos2019-blindness-detection/rules>
   (the EyePACS dataset `dreamer07/eyepacs` needs no rule acceptance).

Source repo (cloned below): https://github.com/yesmukhamedov/dr-classifier
"""))

cells.append(md("## 0. Runtime check\n\n`Runtime → Change runtime type → T4 GPU` first."))
cells.append(code(
"""!nvidia-smi
import torch
print("torch", torch.__version__, "| cuda:", torch.cuda.is_available())
"""))

cells.append(md(
"""## 1. Config switches

`DATASET`  — `"aptos"` (quick test) or `"eyepacs"` (real run).
`FOLD`     — change per session: `0 -> 1 -> 2 -> 3 -> 4`.
`DRIVE_DIR`— where checkpoints + stats persist on Google Drive."""))
cells.append(code(
r'''DATASET   = "aptos"     # "aptos" (quick test) | "eyepacs" (real Config-D run)
FOLD      = 0           # change per session: 0,1,2,3,4
DRIVE_DIR = "/content/drive/MyDrive/dr-config-d"   # persistent root on Google Drive

# Kaggle source per dataset (download handled in the credentials/download cell).
KAGGLE_SOURCE = {
    "aptos":   ("competition", "aptos2019-blindness-detection"),  # needs 1-time rule accept
    "eyepacs": ("dataset",     "dreamer07/eyepacs"),              # no rule accept
}[DATASET]
print("DATASET =", DATASET, "| source =", KAGGLE_SOURCE, "| FOLD =", FOLD)
'''))

cells.append(md("## 2. Mount Google Drive (persistent checkpoints + stats)"))
cells.append(code(
r'''from google.colab import drive
from pathlib import Path
import os

drive.mount("/content/drive")

DRIVE_ROOT = Path(DRIVE_DIR)
OUTPUT_DIR = DRIVE_ROOT / "outputs"          # exp1 writes checkpoints here (persists)
PROCESSED  = DRIVE_ROOT / "processed"        # eyepacs_norm_stats.json + PCA eigvecs (persist)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)
print("checkpoints ->", OUTPUT_DIR)
print("processed   ->", PROCESSED)
'''))

cells.append(md(
"""## 3. Kaggle credentials

Tries **Colab Secrets** (`KAGGLE_USERNAME`, `KAGGLE_KEY`) first; falls back to a
`kaggle.json` upload. Writes `~/.kaggle/kaggle.json` (chmod 600) for the CLI."""))
cells.append(code(
r'''import os, json
from pathlib import Path

KDIR = Path.home() / ".kaggle"
KDIR.mkdir(exist_ok=True)
creds = None
try:
    from google.colab import userdata
    u, k = userdata.get("KAGGLE_USERNAME"), userdata.get("KAGGLE_KEY")
    if u and k:
        creds = {"username": u, "key": k}
        print("Kaggle creds loaded from Colab Secrets.")
except Exception:
    pass

if not creds:
    from google.colab import files
    print("No Colab Secrets found. Upload kaggle.json (Kaggle -> Account -> Create New API Token):")
    up = files.upload()
    creds = json.loads(up[next(iter(up))].decode())

(KDIR / "kaggle.json").write_text(json.dumps(creds))
os.chmod(KDIR / "kaggle.json", 0o600)
os.environ["KAGGLE_USERNAME"] = creds["username"]
os.environ["KAGGLE_KEY"] = creds["key"]
print("Kaggle ready for user:", creds["username"])
'''))

cells.append(md(
"""## 4. Download the dataset into ephemeral `/content/data`

EyePACS (~35 GB) needs ~70 GB peak (zip + unzipped) — Colab GPU runtimes give
~78–112 GB disk, usually enough; the zip is deleted right after extraction to
reclaim space. APTOS is small (~10 GB). To avoid re-downloading each session you
*can* cache the extracted folder on Drive, but EyePACS won't fit on the free
15 GB Drive tier, so this re-downloads per session (a fresh ~10–20 min)."""))
cells.append(code(
r'''import subprocess, glob, os
from pathlib import Path

!pip install -q kaggle

DATA = Path("/content/data")
DATA.mkdir(parents=True, exist_ok=True)
kind, slug = KAGGLE_SOURCE

if not any(DATA.iterdir()):
    if kind == "competition":
        subprocess.run(["kaggle", "competitions", "download", "-c", slug, "-p", str(DATA)], check=True)
    else:
        subprocess.run(["kaggle", "datasets", "download", "-d", slug, "-p", str(DATA)], check=True)
    # Unzip every archive, then delete it to reclaim disk (EyePACS is tight).
    for zf in glob.glob(str(DATA / "*.zip")):
        subprocess.run(["unzip", "-q", "-o", zf, "-d", str(DATA)], check=True)
        os.remove(zf)
else:
    print("DATA already populated; skipping download.")

print("contents of", DATA, ":")
!ls -la /content/data | head -n 20
'''))

cells.append(md("## 5. Clone repo + install deps"))
cells.append(code(
"""!git clone --depth 1 https://github.com/yesmukhamedov/dr-classifier.git /content/repo
%cd /content/repo
!pip install -q -r requirements.txt
!pip install -q timm        # required by src/models/efficientnet.py, not in requirements.txt
"""))

cells.append(md(
"""## 6. Dataset layout adapter (EyePACS native **or** APTOS 2019)

Identical logic to the Kaggle notebook, but `INPUT` points at `/content/data`.
`exp1` expects a root with `trainLabels.csv` (`image`,`level`) + a `train/`
subfolder of `<image>.jpeg`. This cell auto-detects the download and assembles
`EYEPACS_ROOT` via symlinks (no copy):

* **EyePACS** — uses `trainLabels.csv` + `*.jpeg` directly.
* **APTOS 2019** — synthesizes the layout from `train.csv` (`id_code`,`diagnosis`)
  + `train_images/*.png`: writes a derived `trainLabels.csv` and symlinks each
  `<id_code>.png` as `<id_code>.jpeg` (`cv2.imread` decodes by content)."""))
cells.append(code(
r'''import os, sys, subprocess
import pandas as pd
from pathlib import Path

INPUT = Path("/content/data")             # Colab download dir
WORK  = Path("/content/eyepacs")          # synthesized EyePACS-shaped root (both sources)

def first(gen):
    for x in gen:
        return x
    return None

# 1) Native EyePACS layout: trainLabels.csv (image,level) + *.jpeg train images.
labels     = first(p for p in INPUT.rglob("trainLabels.csv") if p.is_file())
train_jpeg = first(p for p in INPUT.rglob("*.jpeg") if p.is_file())
train_dir  = train_jpeg.parent if train_jpeg else None
SOURCE     = "eyepacs" if (labels is not None and train_dir is not None) else None

# 2) APTOS 2019 layout: train.csv (id_code,diagnosis) + *.png -> synthesize EyePACS layout.
if SOURCE is None:
    def _is_aptos_csv(p):
        try:
            cols = set(pd.read_csv(p, nrows=0).columns)
        except Exception:
            return False
        return {"id_code", "diagnosis"}.issubset(cols)

    aptos_csv = first(p for p in INPUT.rglob("train.csv") if p.is_file() and _is_aptos_csv(p))
    if aptos_csv is not None:
        df  = pd.read_csv(aptos_csv)
        png = first(p for p in aptos_csv.parent.rglob("*.png") if p.is_file()) \
              or first(p for p in INPUT.rglob("*.png") if p.is_file())
        assert png is not None, "APTOS train.csv found but no .png images under /content/data."
        src_dir = png.parent
        WORK.mkdir(parents=True, exist_ok=True)
        tgt_train = WORK / "train"
        tgt_train.mkdir(exist_ok=True)
        n_linked = 0
        for code_id in df["id_code"].astype(str):
            src = src_dir / f"{code_id}.png"
            lnk = tgt_train / f"{code_id}.jpeg"   # cv2 decodes PNG bytes regardless of suffix
            if src.exists() and not lnk.exists():
                os.symlink(src, lnk)
                n_linked += 1
        (df.rename(columns={"id_code": "image", "diagnosis": "level"})[["image", "level"]]
           .to_csv(WORK / "trainLabels.csv", index=False))
        labels    = WORK / "trainLabels.csv"
        train_dir = tgt_train
        SOURCE    = "aptos2019"
        print(f"APTOS detected: linked {n_linked} png->jpeg from {src_dir}")

print("source   :", SOURCE)
print("labels   :", labels)
print("train dir:", train_dir)

assert labels is not None and train_dir is not None, \
    "Could not locate a usable dataset under /content/data. Check the download cell."

# Assemble EYEPACS_ROOT = {WORK}/ with a 'train' subdir + trainLabels.csv via symlinks.
# (For APTOS these already exist as real dir/file, so the guards just skip.)
WORK.mkdir(parents=True, exist_ok=True)
tgt_train  = WORK / "train"
tgt_labels = WORK / "trainLabels.csv"
if not tgt_train.exists():
    os.symlink(train_dir, tgt_train)
if not tgt_labels.exists():
    os.symlink(labels, tgt_labels)

EYEPACS_ROOT = str(WORK)
n_imgs = sum(1 for _ in tgt_train.glob("*.jpeg"))
print(f"\nsource = {SOURCE}")
print(f"EYEPACS_ROOT = {EYEPACS_ROOT}")
print(f"train images visible: {n_imgs}")
'''))

cells.append(md(
"""## 7. Persist `data/processed` on Drive

Symlink the repo's `data/processed` to the Drive `processed/` folder so the
one-shot dataset-stats + PCA artifacts survive across sessions (computed once,
reused on every later fold)."""))
cells.append(code(
r'''import os
from pathlib import Path

repo_proc = Path("/content/repo/data/processed")
repo_proc.parent.mkdir(parents=True, exist_ok=True)
if repo_proc.is_symlink() or repo_proc.exists():
    if not repo_proc.is_symlink():
        # an empty real dir from a fresh clone -> replace with the Drive symlink
        try: repo_proc.rmdir()
        except OSError: pass
if not repo_proc.exists():
    os.symlink(PROCESSED, repo_proc)
print("data/processed ->", os.path.realpath(repo_proc))
!ls -la /content/repo/data/processed
'''))

cells.append(md(
"""## 8. Build merged config

Self-contained — does **not** depend on a `colab_paths.yaml` existing in the
cloned repo. Reuses the repo's `kaggle/merge_config.py` (deep-merge helper) and
passes every Colab-specific value as a dotted override:
`paths.eyepacs`, `paths.output_dir` (Drive), `training.num_workers=2`.
Writes `configs/colab_merged.yaml`."""))
cells.append(code(
r'''merge_cmd = [
    sys.executable, "kaggle/merge_config.py",
    "--base", "configs/default.yaml",
    "--out", "configs/colab_merged.yaml",
    f"paths.eyepacs={EYEPACS_ROOT}",
    f"paths.output_dir={OUTPUT_DIR}",
    "training.num_workers=2",
    # If you hit CUDA OOM at 512px (EfficientNet runs fp32), uncomment:
    # "training.batch_size=8",
]
subprocess.run(merge_cmd, check=True)
'''))

cells.append(md(
"""## 9. (Optional) PCA eigenvectors for colour augmentation

One-shot; cached on Drive (skipped if already present). If skipped entirely,
colour augmentation is simply disabled (exp1 prints a notice and continues)."""))
cells.append(code(
r'''pca_out = PROCESSED / "eyepacs_pca_eigvecs.npz"
if pca_out.exists() or any(PROCESSED.glob("*pca*")):
    print("PCA eigvecs already on Drive; skipping.")
else:
    subprocess.run([
        sys.executable, "scripts/compute_pca_eigvecs.py",
        "--dataset", "eyepacs",
        "--images-root", str(Path(EYEPACS_ROOT) / "train"),
        "--labels-csv", str(Path(EYEPACS_ROOT) / "trainLabels.csv"),
        "--output-dir", "/content/repo/data/processed",   # symlinked -> Drive
        "--n-samples", "5000",
        "--seed", "42",
    ], check=True)
'''))

cells.append(md(
"""## 10. Dataset-specific normalization stats (Stage 7, D-2) — REQUIRED for Config D

The thesis (Stage 7) requires the full configs (B/D) to normalize with mean/std
computed from the **training set after Stages 0–4, mask=1.0 pixels only** — not
ImageNet (baseline-only fallback). Writes
`data/processed/eyepacs_norm_stats.json` (symlinked to Drive), which
`exp1_factorial.py` loads automatically for Config D. One-shot; cached on Drive.

> Note: for `DATASET="aptos"` these stats are computed over APTOS, which is fine
> for a **functional test** but not the thesis EyePACS stats — recompute (delete
> the cached json) when you switch to `DATASET="eyepacs"`."""))
cells.append(code(
r'''stats_out = PROCESSED / "eyepacs_norm_stats.json"
if stats_out.exists():
    print("norm stats already on Drive; skipping. (Delete to recompute for a new DATASET.)")
else:
    subprocess.run([
        sys.executable, "scripts/compute_dataset_stats.py",
        "--images-root", str(Path(EYEPACS_ROOT) / "train"),
        "--labels-csv", str(Path(EYEPACS_ROOT) / "trainLabels.csv"),
        "--output-dir", "/content/repo/data/processed",   # symlinked -> Drive
        "--n-samples", "5000",
        "--seed", "42",
    ], check=True)
print("stats:", stats_out, "exists:", stats_out.exists())
'''))

cells.append(md("## 11. Train one fold\n\n`--resume` continues from `last_checkpoint.pt` on Drive if a previous session left one. Set `FOLD` in cell 1."))
cells.append(code(
r'''subprocess.run([
    sys.executable, "run_experiment.py", "exp1",
    "--config", "configs/colab_merged.yaml",
    "--configs", "D",
    "--fold", str(FOLD),
    "--resume",
], check=True)
'''))

cells.append(md("## 12. Inspect outputs (on Drive)"))
cells.append(code(
r'''ckpt_dir = OUTPUT_DIR / "exp1" / "checkpoints" / f"D_fold{FOLD}"
print("checkpoint dir:", ckpt_dir)
!ls -la "{ckpt_dir}"
print("\n--- metrics.csv (tail) ---")
!tail -n 15 "{OUTPUT_DIR}/exp1/metrics.csv"
'''))

cells.append(md(
"""## 13. Multi-fold strategy & keep-alive

Run this notebook once per fold (`FOLD = 0..4` in cell 1). Because outputs live
on **Google Drive**, the next session's `--resume` finds the checkpoint
automatically — no Kaggle-style "attach previous output". Just rerun all cells
with the next `FOLD`.

**Colab caveats vs Kaggle**
* Free Colab disconnects on idle (~90 min) and caps ~12 h/session. Keep the tab
  active; Colab Pro+ adds background execution.
* EyePACS re-downloads each session (~10–20 min) — it won't fit on free Drive.
* When all 5 folds are done, copy `outputs/exp1/` from Drive to the repo at
  `experiments/outputs/exp1/`, then run `python scripts/verify_exp1.py`.

**Quick-test recipe:** set `DATASET="aptos"`, `FOLD=0`, run all → a full
Config-D pass in minutes confirms the Colab pipeline before committing to the
~35 GB EyePACS run (`DATASET="eyepacs"`, delete the cached APTOS
`eyepacs_norm_stats.json` first)."""))

nb = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {"provenance": [], "gpuType": "T4"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path(__file__).parent / "train_config_d_colab.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out)
