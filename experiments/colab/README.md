# Google Colab — Train Config D (Full V5 + EfficientNet-B3)

The Colab port of `experiments/kaggle/`. Same Experiment-1 / Config-D run
(Full V5 + EfficientNet-B3, 4-channel, Focal Loss, 5-fold patient-level CV),
ported to run on Colab **alongside** the Kaggle session.

The notebook clones the standalone repo
**https://github.com/yesmukhamedov/dr-classifier** (code lives at its root) and
imports nothing from this folder at runtime — it is **self-contained**.

## Files

| File | Purpose |
|---|---|
| `train_config_d_colab.ipynb` | Main notebook (mount Drive → Kaggle download → adapt data → merge config → train one fold). |
| `_build_colab_notebook.py` | One-shot generator for the `.ipynb` (kept for reproducibility). Re-run after edits. |

## Two modes

Set `DATASET` in **cell 1**:

| `DATASET` | Source (Kaggle) | Size | Use |
|---|---|---|---|
| `"aptos"` | competition `aptos2019-blindness-detection` | ~3.7k imgs | **Quick functional test** — a full Config-D pass in minutes to prove the Colab pipeline works. |
| `"eyepacs"` | dataset `dreamer07/eyepacs` | ~35k imgs | **The real Config-D run.** |

The dataset-layout adapter auto-detects which one was downloaded and converts
APTOS into the EyePACS layout — Config D / Full V5 / EfficientNet-B3 are
otherwise identical across modes.

> Switching APTOS → EyePACS: **delete the cached `eyepacs_norm_stats.json`** on
> Drive first (`<DRIVE_DIR>/processed/`), otherwise the APTOS-computed Stage-7
> stats get reused and the EyePACS checkpoint is **not** thesis-faithful.

## What you must provide (one-time, minimal)

1. **Kaggle API token** — for the dataset download. Either (preferred) add
   `KAGGLE_USERNAME` + `KAGGLE_KEY` to **Colab Secrets** (🔑 in the left
   sidebar), or upload `kaggle.json` when cell 3 prompts (Kaggle → *Account* →
   *Create New API Token*).
2. **Google Drive** — click *Authorize* on the mount cell (OAuth). Checkpoints,
   dataset-stats and PCA eigvecs persist under `<DRIVE_DIR>` so the per-fold
   `--resume` survives Colab disconnects.
3. **APTOS only:** accept the competition rules once at
   <https://www.kaggle.com/competitions/aptos2019-blindness-detection/rules>.
   (`dreamer07/eyepacs` needs no rule acceptance.)

Nothing secret is handed to the repo or to Claude — credentials are read at
runtime inside your Colab session.

## How to run

1. Open `train_config_d_colab.ipynb` in Colab. `Runtime → Change runtime type →
   T4 GPU`.
2. In **cell 1**: set `DATASET` and `FOLD`.
3. Run all cells. First run computes + caches the dataset-stats / PCA on Drive;
   later folds reuse them.
4. For the next fold: change `FOLD` in cell 1 and run all again — `--resume`
   picks up the checkpoint from Drive automatically.

## Persistence model (vs Kaggle)

* **Kaggle:** outputs persist via *Save Version*; resuming a fold means attaching
  the previous session's output as a dataset input.
* **Colab:** outputs persist on **Google Drive** (`output_dir` points there), so
  the next session resumes with zero extra setup. The trade-off: the dataset
  lives on ephemeral `/content` and **re-downloads each session** (EyePACS won't
  fit on the free 15 GB Drive tier) — a fresh ~10–20 min per EyePACS session.

## Colab caveats

* Free Colab disconnects on idle (~90 min) and caps ~12 h/session — so the
  **one-fold-per-session + `--resume`** strategy is the same as Kaggle. Colab
  Pro+ adds background execution.
* EyePACS needs ~70 GB peak disk (zip + unzipped). Colab GPU runtimes give
  ~78–112 GB; the zip is deleted right after extraction. If disk is tight, run
  the APTOS test first.
* EfficientNet runs **fp32** (mixed precision stays disabled — fp16 overflow).
  If the T4 OOMs at 512px, uncomment `training.batch_size=8` in the merge cell.

## Outputs

`<DRIVE_DIR>/outputs/exp1/checkpoints/D_fold{0..4}/best_model.pt` (monitored on
`weighted_f1`) + `<DRIVE_DIR>/outputs/exp1/metrics.csv`.

When all five folds finish, copy `outputs/exp1/` from Drive to
`experiments/outputs/exp1/`, then run `python scripts/verify_exp1.py`.

## ⚠ Prerequisite: the cloned repo must be current

The notebook clones `yesmukhamedov/dr-classifier`. That repo must already contain
the up-to-date `experiments/` code — in particular `scripts/compute_dataset_stats.py`
(real implementation, not the old stub), `kaggle/merge_config.py`, and the
EyePACS adapter `is_file()` fix. If it is stale, mirror the latest `experiments/`
tree into it first (the same outstanding TODO noted in `TASK-Config-D.md`).
