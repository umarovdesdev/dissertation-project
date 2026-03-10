# DR-Classifier

Automated Diabetic Retinopathy classification via fundus image preprocessing + CNN.
PhD dissertation project (Yesmukhamedov N.S.).

## Stack
- Python 3.10, PyTorch 2.5, timm (EfficientNet), OpenCV, scikit-learn
- Conda env: `conda activate dr-classifier`
- GPU: NVIDIA RTX 3060 12GB VRAM — use mixed precision (fp16)
- OS: WSL2 Ubuntu on Windows

## Project Structure
```
configs/default.yaml          — all hyperparameters and experiment specs
src/data/datasets.py          — dataset loaders (EyePACS, APTOS, IDRiD, Messidor, etc.)
src/data/splits.py            — patient-level 5-fold CV
src/data/label_harmonization.py — taxonomy mapping for Messidor, RFMiD, ODIR
src/preprocessing/pipeline.py — 5-component pipeline (toggleable for ablation)
src/preprocessing/fov.py      — Stage 1: FOV standardization
src/preprocessing/green_channel.py — Stage 2: green channel extraction
src/preprocessing/normalization.py — Stage 3: pixel normalization
src/preprocessing/clahe.py    — Stage 4: CLAHE in LAB color space
src/preprocessing/hsv_enhancement.py — Stage 5: HSV contrast enhancement
src/models/factory.py         — model creation factory
src/models/resnet.py          — ResNet-50 with 5-class head
src/models/efficientnet.py    — EfficientNet-B0/B3/B4 with 5-class head
src/models/two_stage.py       — two-stage fine-tuning protocol
src/training/trainer.py       — training loop with 5-fold CV
src/training/losses.py        — weighted cross-entropy for class imbalance
src/training/callbacks.py     — early stopping, checkpointing
src/evaluation/metrics.py     — primary + secondary + clinical metrics
src/evaluation/calibration.py — ECE, Brier score
src/evaluation/statistical_tests.py — McNemar, DeLong, bootstrap CI
src/explainability/gradcam.py — Grad-CAM activation maps
src/explainability/iou.py     — IoU vs IDRiD lesion masks
src/degradation/perturbations.py — Gaussian noise, blur, low illumination
src/experiments/exp1_factorial.py     — Experiment 1: 2x2 factorial (H-1)
src/experiments/exp2_ablation.py      — Experiment 2: component ablation (H-2)
src/experiments/exp3_robustness.py    — Experiment 3: degradation robustness
src/experiments/exp4_explainability.py — Experiment 4: Grad-CAM (H-5)
src/experiments/exp5_generalization.py — Experiment 5: cross-database (H-4)
src/experiments/exp6_device_shift.py  — Experiment 6: device domain shift (H-6)
scripts/run_experiment.py     — CLI entry point
data/raw/                     — raw datasets (not in git)
data/processed/               — preprocessed data cache
```

## Preprocessing Pipeline (5 ordered components)
1. FOV Standardization — Hough circle detection, border removal, resize to 512x512
2. Green Channel — extract green channel (best vessel contrast)
3. Normalization — pixel values to [0, 1]
4. CLAHE — applied to L-channel of LAB color space, dynamic clip limit
5. HSV Enhancement — saturation/value scaling in HSV space

Pipeline = "active" when all 5 on. Baseline = resize only.
Data augmentation (flip, rotate +/-15deg, zoom +/-10%, brightness) is SEPARATE from preprocessing.

## Experiment 1: 2x2 Factorial (CRITICAL — everything depends on this)
Dataset: EyePACS (~88K images). 4 configurations:
- A: resize only + ResNet-50
- B: full preprocessing + ResNet-50
- C: resize only + EfficientNet-B3
- D: full preprocessing + EfficientNet-B3

Dominance criterion (EH-3) — ALL THREE must hold:
- Delta weighted F1 >= 5 percentage points
- Delta ROC-AUC >= 0.02
- No Cohen Kappa degradation

## Cross-Validation
ALL experiments: 5-fold CV with patient-level split.
MANDATORY: no patient images in both train and test within any fold.
Report: mean +/- std across folds.

## Hardware Constraints
- batch_size: 16 (RTX 3060 12GB limit at 512x512)
- mixed_precision: true (torch.cuda.amp)
- image_size: 512x512
- optimizer: Adam, lr=0.0001, weight_decay=0.0001
- early_stopping: patience=10, monitor=val_weighted_f1
- class_weights: inverse frequency
- seed: 42

## Primary Metrics (descending importance)
1. Weighted F1-score
2. ROC-AUC (one-vs-rest, macro)
3. Cohen Kappa (quadratic weights)
4. Accuracy

## Commands
```bash
conda activate dr-classifier
python scripts/run_experiment.py --experiment exp1 --config configs/default.yaml
python -m pytest tests/
```

## Code Rules
- Type hints on all function signatures
- Docstrings with Args/Returns for every public function
- No hardcoded paths — all paths from config YAML
- Every module independently testable
- Use pathlib.Path not os.path

## Detailed specs in docs/:
- docs/RESEARCH_ARCHITECTURE.md — full experimental protocol with 6 experiments
- docs/INVARIANTS.md — hypotheses, scope boundaries, forbidden claims
- docs/HYPOTHESIS.md — H-1 through H-6 formal definitions
- docs/ARGUMENT_MAP.md — claim-evidence dependency structure
ENDOFFILE