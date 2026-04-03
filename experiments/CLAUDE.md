# experiments/ — DR-Classifier

Automated Diabetic Retinopathy classification via fundus image preprocessing + CNN.
PhD dissertation project (Yesmukhamedov N.S.).

## Stack

- Python 3.10, PyTorch 2.5, timm (EfficientNet), OpenCV, scikit-learn
- Conda env: `conda activate dr-classifier`
- GPU: NVIDIA RTX 3060 12GB VRAM
- OS: WSL2 Ubuntu on Windows

## Governance

All governance documents (INVARIANTS, HYPOTHESIS, ARGUMENT_MAP, etc.) live in `../thesis/governance/` — that is the single source of truth. Do not create or maintain governance copies here. The only local doc is `docs/experimental_protocol.md` (quick-start guide).

## Project Structure

```
configs/default.yaml          — all hyperparameters and experiment specs
configs/smoke_test_1pct.yaml  — 1% subset for fast smoke testing
run_experiment.py             — CLI entry point
```

### Preprocessing

```
src/preprocessing/pipeline_v4.py        — V4 6-stage pipeline orchestrator (canonical)
src/preprocessing/config.py             — PreprocessingV4Config dataclass + presets
src/preprocessing/canonical_orientation.py — Stage 0: canonical flip + OD-fovea rotation
src/preprocessing/canonical_flip.py     — backward-compat shim → canonical_orientation.py
src/preprocessing/od_fovea_detect.py    — Stage 0b: OD/fovea detection (classical CV)
src/preprocessing/crop_resize.py        — Stage 1: PIL-based FOV crop + resize
src/preprocessing/flat_field.py         — Stage 2: Gaussian flat-field correction
src/preprocessing/upgraded_clahe.py     — Stage 3: dual-constraint CLAHE (L-channel)
src/preprocessing/imagenet_normalize.py — Stage 4: ImageNet mean/std → tensor
src/preprocessing/pipeline.py           — V3 5-component pipeline (legacy, exp2 compat)
src/preprocessing/fov.py                — V3: FOV standardization (Hough circle)
src/preprocessing/clahe.py              — V3: CLAHE in LAB color space
src/preprocessing/hsv_enhancement.py    — V3: HSV contrast enhancement
src/preprocessing/green_channel.py      — V3: green channel extraction
src/preprocessing/normalization.py      — V3: pixel normalization [0,1]
```

### Data

```
src/data/datasets.py            — dataset loaders (EyePACS, IDRiD, Messidor, DDR, ODIR, RFMiD)
src/data/splits.py              — PatientLevelKFold (patient-level stratified k-fold CV)
src/data/augmentation.py        — V3 augmentation (flip, rotate, zoom, brightness)
src/data/augmentation_v4.py     — V4 augmentation (unified affine + PCA color)
src/data/label_harmonization.py — taxonomy mapping for Messidor, RFMiD, ODIR
```

### Models

```
src/models/factory.py        — create_model() and create_patient_model()
src/models/resnet.py         — ResNet-50 with configurable in_channels and 5-class head
src/models/efficientnet.py   — EfficientNet-B0/B3/B4 via timm
src/models/patient_model.py  — Backbone + PatientHead for binocular fusion (configs E/F)
src/models/two_stage.py      — two-stage fine-tuning protocol
```

### Training

```
src/training/trainer.py         — main training loop (mixed precision, early stopping, k-fold CV)
src/training/patient_trainer.py — patient-level training (binocular blending configs E/F)
src/training/losses.py          — FocalLoss (γ=2) + inverse-frequency class weights
src/training/checkpoint.py      — CheckpointManager (save/load/keep-best)
src/training/train.py           — standalone training script
```

### Evaluation

```
src/evaluation/metrics.py           — primary (F1, AUC, κ, acc) + secondary + clinical + dominance check
src/evaluation/calibration.py       — ECE, Brier score
src/evaluation/statistical_tests.py — McNemar, DeLong, bootstrap CI
```

### Explainability

```
src/explainability/gradcam.py       — Grad-CAM activation maps
src/explainability/iou.py           — IoU/ALO vs IDRiD lesion masks
src/explainability/visualization.py — Grad-CAM overlay rendering
```

### Experiments

```
src/experiments/exp1_factorial.py     — Exp 1: 2×2 factorial + blending (H-1)
src/experiments/exp2_ablation.py      — Exp 2: component ablation + CLAHE sweep (H-2)
src/experiments/exp3_robustness.py    — Exp 3: degradation robustness (DROPPED)
src/experiments/exp4_explainability.py — Exp 4: Grad-CAM (H-5)
src/experiments/exp5_generalization.py — Exp 5: cross-database (H-4)
src/experiments/exp6_device_shift.py  — Exp 6: device domain shift (H-6)
src/experiments/_eval_utils.py        — shared inference helpers
```

### Utilities

```
src/utils/config.py        — YAML config loading and merging
src/utils/seed.py           — reproducibility (fixed seeds, deterministic mode)
src/utils/image_quality.py  — CNR, entropy, SSIM quality metrics
src/degradation/perturbations.py — Gaussian noise, blur, low illumination
```

## V4 Preprocessing Pipeline (6-stage, canonical)

Stage 0a: Canonical flip (left→right eye orientation) — toggleable
Stage 0b: OD-fovea rotation normalization — toggleable
Stage 1:  FOV crop + isotropic resize + padding + FOV mask (4th channel) — always on
Stage 2:  Flat-field correction (Gaussian σ=45) — toggleable
Stage 3:  Upgraded CLAHE (dual-constraint, LAB L-channel, stochastic p=0.8 at train) — toggleable
Stage 5:  Augmentation (unified affine + brightness/contrast + PCA color) — train only
Stage 4:  ImageNet normalize → tensor — always last

V4 augmentation is INTEGRATED into the pipeline (Stage 5 before Stage 4).
Presets: "resnet" (full preprocessing + full aug), "efficientnet" (reduced aug).
Baseline = Stages 1 + 4 only (crop + resize + ImageNet normalize).

## V3 Pipeline (legacy, exp2 compat only)

5 ordered components: FOV → CLAHE → HSV → Green Channel → Normalize.
CLAHE and HSV run BEFORE green channel (full-color image).
V3 augmentation (flip, rotate ±15°, zoom ±10%, brightness) is SEPARATE from preprocessing.

## Experiment 1: 2×2 Factorial (COMPLETED)

Dataset: EyePACS 40% subset (~14,050 images). 6 configurations:
- A: baseline + ResNet-50
- B: full V4 pipeline + ResNet-50
- C: baseline + EfficientNet-B3
- D: full V4 pipeline + EfficientNet-B3 ← BEST (F1=0.780, AUC=0.865, κ=0.700)
- E: full V4 + ResNet-50 + per-patient blending (optional)
- F: full V4 + EfficientNet-B3 + per-patient blending (optional)

Dominance criterion (EH-3) — ALL THREE must hold:
- ΔF1 ≥ 5 percentage points
- ΔAUC ≥ 0.02
- No Cohen κ degradation

## Cross-Validation

3-fold CV with patient-level stratified split. No patient images in both train and val within any fold.

## Hardware Constraints

```yaml
batch_size: 16
image_size: 512×512
input_channels: 4           # RGB + FOV mask
mixed_precision: true        # DISABLED for EfficientNet (fp16 overflow)
loss: Focal Loss (γ=2, α=inverse-frequency)
optimizer: Adam (lr=1e-4, weight_decay=1e-4)
early_stopping: patience=5, monitor=val_weighted_f1
scheduler: ReduceOnPlateau (factor=0.5, patience=3, min_lr=1e-6)
max_epochs: 20
seed: 42, deterministic=true
num_workers: 4
```

## Primary Metrics (descending importance)

1. Weighted F1-score
2. ROC-AUC (one-vs-rest, macro)
3. Cohen Kappa (quadratic weights)
4. Accuracy

## Commands

```bash
conda activate dr-classifier
python run_experiment.py exp1 --config configs/default.yaml
python run_experiment.py exp1 --config configs/default.yaml --configs A,B
python run_experiment.py exp2 --config configs/default.yaml
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml
```

## Code Rules

- Type hints on all function signatures
- Docstrings with Args/Returns for every public function
- No hardcoded paths — all paths from config YAML
- Every module independently testable
- Use pathlib.Path, not os.path
- All internal image processing in RGB (cv2.imread returns BGR — convert on entry)

## Known Issues and Fixes

- EfficientNet-B3 fp16 overflow → mixed precision DISABLED for EfficientNet configs
- Gradient explosion in early training → gradient clipping added
- V3 pipeline ordering bug: green channel ran before CLAHE/HSV → reordered to FOV→CLAHE→HSV→Green→Normalize
