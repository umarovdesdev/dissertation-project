# Experimental Protocol

See `docs/RESEARCH_ARCHITECTURE.md` for the full experimental design.

## Quick Start
```bash
conda activate dr-classifier

# Run Experiment 1 (6-config factorial A-F, V4 pipeline)
python run_experiment.py --experiment exp1 --config configs/default.yaml

# Run specific configs only
python run_experiment.py --experiment exp1 --config configs/default.yaml --configs A,B

# Run Experiment 2 (component ablation, V4 pipeline stages)
python run_experiment.py --experiment exp2 --config configs/default.yaml

# Smoke test (1% subset)
python run_experiment.py --experiment exp1 --config configs/smoke_test_1pct.yaml
```

## Datasets

All datasets stored at `/mnt/d/datasets/` (Windows NTFS, accessed via WSL2).
Paths configured in `configs/default.yaml`.

| Dataset | Images | Classes | Role |
|---------|--------|---------|------|
| EyePACS | ~35,126 labeled | 5 (DR 0–4) | Primary training |
| IDRiD | 516 | 5 + lesion masks | Clinical validation, Grad-CAM |
| Messidor/Messidor-2 | ~1,748 | 4 (mapped to 5) | External generalization |
| DDR | ~13,673 | 5 | Device domain shift |
| ODIR-5K | ~7,000 | multi-label | Device domain shift |
| RFMiD | ~3,200 | binary DR | Device domain shift |

## Cross-Validation

3-fold CV with patient-level stratified split. No patient leakage across folds.

## Grading Scale

| Grade | Clinical Stage | Approximate Prevalence (EyePACS) |
|-------|---------------|----------------------------------|
| 0 | No DR | ~73% |
| 1 | Mild NPDR | ~7% |
| 2 | Moderate NPDR | ~15% |
| 3 | Severe NPDR | ~2% |
| 4 | Proliferative DR | ~3% |

Class imbalance addressed via inverse-frequency weighted cross-entropy loss.

## Reproducibility
- seed: 42, deterministic=true
- All configs committed in `configs/`
- Checkpoints saved per fold per config
