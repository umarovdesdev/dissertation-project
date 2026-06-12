---
name: config-d-kaggle-source
description: "Which Kaggle EyePACS dataset Config-D trains on and the notebook adapter is_file() fix; Kaggle run outcomes"
metadata:
  type: project
---

Config-D Kaggle training (`experiments/kaggle/train_config_d.ipynb`) uses the
Kaggle dataset **`dreamer07/eyepacs`** as the EyePACS source: 35,126 `*.jpeg`
with original `<id>_<side>` filenames + `trainLabels.csv` (`image,level`),
~35 GB, pre-extracted. Layout on Kaggle: CSV at
`.../eyepacs/trainLabels.csv/trainLabels.csv` (a folder *named* `trainLabels.csv`
wrapping the file), images flat under `.../eyepacs/data/data/`.

**Why:** `tantai31124/eyepacs-original` (98 GB) is ImageFolder
`{train,val,test}/{0..4}` with **no CSV** and an author re-split → patient-leak +
relabel-provenance risk; rejected. The raw competition
`diabetic-retinopathy-detection` is canonical but its multi-part `train.zip.00x`
extraction can blow the `/kaggle/working` quota; kept only as fallback.

**How to apply:** The notebook adapter (Cell 6) auto-detects via
`rglob`. Because the CSV is wrapped in a same-named folder, `rglob("trainLabels.csv")`
matched the directory first → `read_csv` would hit `IsADirectoryError`. Fixed by
filtering `first(p for p in ... if p.is_file())` for both the CSV and `*.jpeg`
probes. Patched in `_build_notebook.py` + regenerated `train_config_d.ipynb`
(2026-06-01). See [[config-d-pretraining]].

**Run #1 outcome (verified 2026-06-02):** fold-0 kernel **FAILED** — status
`CANCEL_ACKNOWLEDGED`, "exceeded the max allowed execution duration" (12 h wall
limit). No `.pt` checkpoint; `metrics.csv` header only (zero epochs). Only good
artifact: `eyepacs_norm_stats.json` (5000-img sample, stages 0–4) → saved to
`experiments/data/processed/eyepacs_norm_stats.json`. Root cause: one epoch
(35,126 imgs, EfficientNet-B3 fp32 @512px, heavy CPU V5 preprocessing,
`num_workers=2`) does not fit in 12 h. `checkpoint.py` saves only at epoch end →
nothing persisted. **Fix tracked in** [[v5-cache-throughput]].

**TEMPORARY APTOS swap (2026-06-02, kernel v2):** to verify pipeline functionality
with a small dataset, kernel `yesmukhamedov/config-d` switched EyePACS →
**`aptos2019-blindness-detection`** (~3.7k imgs). The adapter now auto-detects
**either** EyePACS native (`trainLabels.csv`+`*.jpeg`) **or** APTOS (`train.csv`
id_code/diagnosis + `*.png`), synthesizing the EyePACS layout from APTOS. Throwaway
functionality test — revert to EyePACS by re-attaching `dreamer07/eyepacs`.

**Run #2 outcome — APTOS SUCCEEDED (verified 2026-06-03):** Config-D fold 0 ran 10
epochs, early-stopped (patience=5); **best epoch 4, val weighted_f1=0.8206** (roc_auc
0.931, kappa 0.903, acc 0.823). `best_model.pt` (~129 MB, EfficientNet-B3 4-ch) under
`outputs/exp1/checkpoints/D_fold0/`, plus APTOS `eyepacs_norm_stats.json`
(n_images=3662 confirms APTOS, not EyePACS). **Interim plumbing checkpoint only** —
NOT thesis-faithful; must be swapped for the EyePACS/Colab checkpoint (blocked on the
V5 cache, see [[v5-cache-throughput]]) before defense. kaggle CLI not on PATH locally;
use `python -m kaggle ...` (exits non-zero on stderr noise but files download fine).
