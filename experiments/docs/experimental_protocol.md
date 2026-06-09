# Experimental Protocol

See `docs/RESEARCH_ARCHITECTURE.md` for the full experimental design.

## Quick Start
```bash
conda activate dr-classifier

# Run Experiment 1 (2×2 factorial A-D, pipeline)
python run_experiment.py --experiment exp1 --config configs/default.yaml

# Run specific configs only
python run_experiment.py --experiment exp1 --config configs/default.yaml --configs A,B

# Run Experiment 2 (component ablation, pipeline stages + CLAHE/flat-field sweeps)
python run_experiment.py --experiment exp2 --config configs/default.yaml

# Run Experiment 3 (cross-dataset transferability, APTOS 2019)
python run_experiment.py --experiment exp3 --config configs/default.yaml

# Run Experiment 4 (Grad-CAM explainability, IDRiD + Clinical)
python run_experiment.py --experiment exp4 --config configs/default.yaml

# Run Experiment 5 (clinical degradation resistance, IDRiD + Messidor-2)
python run_experiment.py --experiment exp5 --config configs/default.yaml

# Run Experiment 6 (device domain shift, DDR + ODIR-5K + RFMiD)
python run_experiment.py --experiment exp6 --config configs/default.yaml

# Run Experiment 7 (small data training, IDRiD → Clinical)
python run_experiment.py --experiment exp7 --config configs/default.yaml
```

## Datasets

All datasets stored at `/mnt/d/datasets/` (Windows NTFS, accessed via WSL2).
Paths configured in `configs/default.yaml`.

| Dataset | ~Images | Classes | Camera | Role |
|---------|---------|---------|--------|------|
| EyePACS | ~35,126 | 5-class (DR 0–4) | Canon CR-1 | Primary training (Exp 1,2,3,4,5,6) |
| APTOS 2019 | ~3,662 | 5-class | Mixed | Cross-dataset transferability (Exp 3) |
| IDRiD | 516 | 5-class + lesion masks | Kowa | Explainability, degradation (Exp 4,5,7 train) |
| Messidor-2 | ~1,748 | Referable/non-referable | Topcon | Clinical degradation (Exp 5) |
| DDR | ~13,673 | 5-class | Canon, Topcon | Device domain shift (Exp 6) |
| ODIR-5K | ~5,000 bilateral | Multi-disease → DR subset | Canon, Zeiss | Device domain shift (Exp 6) |
| RFMiD | ~3,200 | Binary DR | Topcon, Kowa | Device domain shift (Exp 6) |
| Clinical (Kazakh) | 60 | 5-class balanced | TBD | Clinical validation (Exp 4,5,7 test) |

## Cross-Validation

5-fold CV with patient-level stratified split. No patient leakage across folds.

## Grading Scale

| Grade | Clinical Stage | Approximate Prevalence (EyePACS) |
|-------|---------------|----------------------------------|
| 0 | No DR | ~73% |
| 1 | Mild NPDR | ~7% |
| 2 | Moderate NPDR | ~15% |
| 3 | Severe NPDR | ~2% |
| 4 | Proliferative DR | ~3% |

Class imbalance addressed via Focal Loss (γ=2, inverse-frequency α weights).

## Stage 7 Normalization Stats (per-dataset)

Stage 7 normalises with per-channel mean/std computed over Stages 0–4 (no CLAHE,
FOV-mask pixels only), produced by `scripts/compute_dataset_stats.py --dataset <name>`
into `data/processed/<name>_norm_stats.json`.

**Convention (a) — train-set stats everywhere (no leakage, standard transfer
protocol):** experiments normalise with the **training-set** mean/std the model
was trained on, never re-centring the test set. Concretely:

| Experiments | Trains on | Normalize stats used |
|-------------|-----------|----------------------|
| Exp 1 A/C (baseline, 3ch) | EyePACS | ImageNet mean/std |
| Exp 1 B/D, Exp 2 (full, 4ch) | EyePACS | `eyepacs_norm_stats.json` |
| Exp 3–6 (cross-dataset transfer) | EyePACS | `eyepacs_norm_stats.json` (test sets reuse EyePACS train stats) |
| Exp 7 (small-data) | IDRiD | `idrid_norm_stats.json` |

Exp 3–6 deliberately do **not** compute per-target-dataset stats: re-centring a
test set with its own mean/std would standardise away the device/intensity
domain shift those experiments (H-4/H-6/H-7) exist to measure. The only
train-on-X run that needs its own stats is **Exp 7 (trains on IDRiD)**.

```bash
# EyePACS train stats (Exp 1–6)
python scripts/compute_dataset_stats.py --dataset eyepacs \
    --images-root <EyePACS/train> --labels-csv <trainLabels.csv> --n-samples 5000
# IDRiD train stats (Exp 7)
python scripts/compute_dataset_stats.py --dataset idrid \
    --images-root "<IDRiD/B. Disease Grading/1. Original Images/a. Training Set>" \
    --labels-csv  "<...2. Groundtruths/a. IDRiD_Disease Grading_Training Labels.csv>" \
    --n-samples 0
```

## OD/fovea detector accuracy (IDRiD ground-truth)

`scripts/validate_od_fovea_idrid.py` quantifies the Stage 1 detector against
IDRiD localization GT (516 images). Result (native-resolution detection, as in
the pipeline): **OD** median ≈0.67 OD-radii error (~65% within 1 OD-radius);
**fovea** median ≈5 OD-radii error (~0% within 2 OD-radii) — the darkest-in-
annulus fovea search latches onto the dark vignette at full resolution. The
detector `confident` flag is `True` for 100% of images, so it does **not** gate
these failures. Implication: any consumer of the fovea centre (polar CLAHE
pivot, rotation) must default to a deterministic geometric fallback rather than
trust the detected fovea or the `confident` flag.

## Reproducibility
- seed: 42, deterministic=true
- All configs committed in `configs/`
- Checkpoints saved per fold per config
