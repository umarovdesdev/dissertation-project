# DR-Classifier

Automated Diabetic Retinopathy classification via fundus image preprocessing + CNN.
PhD dissertation project (Yesmukhamedov N.S.).

## Stack
- Python 3.10, PyTorch 2.5, timm (EfficientNet), OpenCV, scikit-learn
- Conda env: `conda activate dr-classifier`
- GPU: NVIDIA RTX 3060 12GB VRAM — use mixed precision (fp16)
- OS: WSL2 Ubuntu on Windows

## Project Structure
configs/default.yaml          — all hyperparameters and experiment specs
configs/smoke_test_1pct.yaml  — 1% subset for fast smoke testing
src/data/datasets.py          — dataset loaders (EyePACS, APTOS, IDRiD, Messidor, DDR, ODIR, RFMiD)
src/data/splits.py            — patient-level k-fold CV
src/data/augmentation.py      — V3 augmentation (flip, rotate, zoom, brightness)
src/data/augmentation_v4.py   — V4 augmentation (unified affine + PCA color + brightness/contrast)
src/data/label_harmonization.py — taxonomy mapping for Messidor, RFMiD, ODIR
src/preprocessing/pipeline.py     — V3 5-component pipeline (toggleable for ablation)
src/preprocessing/pipeline_v4.py  — V4 6-stage pipeline (Exp1 configs A–F)
src/preprocessing/config.py       — V4 config dataclass + pipeline presets (resnet, efficientnet)
src/preprocessing/fov.py              — V3 Stage 1: FOV standardization (Hough circle)
src/preprocessing/clahe.py            — V3 Stage 2: CLAHE in LAB color space
src/preprocessing/hsv_enhancement.py  — V3 Stage 3: HSV contrast enhancement
src/preprocessing/green_channel.py    — V3 Stage 4: green channel extraction
src/preprocessing/normalization.py    — V3 Stage 5: pixel normalization [0,1]
src/preprocessing/od_fovea_detect.py  — V4 Stage 0b: OD/fovea detection (classical CV)
src/preprocessing/canonical_orientation.py — V4 Stage 0: canonical flip + OD-fovea rotation
src/preprocessing/canonical_flip.py   — backward-compat shim → canonical_orientation.py
src/preprocessing/crop_resize.py      — V4 Stage 1: PIL-based FOV crop + resize
src/preprocessing/flat_field.py       — V4 Stage 2: Gaussian flat-field correction
src/preprocessing/upgraded_clahe.py   — V4 Stage 3: dual-constraint CLAHE (L-channel)
src/preprocessing/imagenet_normalize.py — V4 Stage 4: ImageNet mean/std normalization → tensor
src/models/factory.py         — model creation factory (create_model, create_patient_model)
src/models/resnet.py          — ResNet-50 with 5-class head
src/models/efficientnet.py    — EfficientNet-B0/B3/B4 with 5-class head (via timm)
src/models/patient_model.py   — Backbone + PatientHead for binocular fusion
src/models/two_stage.py       — two-stage fine-tuning protocol
src/training/trainer.py         — main training loop with k-fold CV
src/training/patient_trainer.py — two-stage patient-level training (blending configs E/F)
src/training/losses.py          — weighted cross-entropy for class imbalance
src/training/checkpoint.py      — CheckpointManager (save/load/keep-best)
src/training/train.py           — standalone training script
src/evaluation/metrics.py           — primary + secondary + clinical metrics, dominance check
src/evaluation/calibration.py       — ECE, Brier score
src/evaluation/statistical_tests.py — McNemar, DeLong, bootstrap CI
src/explainability/gradcam.py       — Grad-CAM activation maps
src/explainability/iou.py           — IoU/ALO vs IDRiD lesion masks
src/explainability/visualization.py — Grad-CAM overlay rendering
src/degradation/perturbations.py — Gaussian noise, blur, low illumination
src/experiments/exp1_factorial.py     — Experiment 1: 2×2 factorial + blending (H-1) [V4 pipeline]
src/experiments/exp2_ablation.py      — Experiment 2: component ablation (H-2) [V3 pipeline]
src/experiments/exp3_robustness.py    — Experiment 3: degradation robustness
src/experiments/exp4_explainability.py — Experiment 4: Grad-CAM (H-5)
src/experiments/exp5_generalization.py — Experiment 5: cross-database (H-4)
src/experiments/exp6_device_shift.py  — Experiment 6: device domain shift (H-6)
src/experiments/_eval_utils.py        — shared inference helpers for exp5/exp6
src/utils/config.py        — config loading and merging
src/utils/seed.py           — reproducibility (fixed seeds)
src/utils/image_quality.py  — CNR, entropy, SSIM quality metrics
run_experiment.py           — CLI entry point
scripts/compute_pca_eigvecs.py — offline PCA eigenvector computation for V4 color aug
scripts/generate_report.py     — experiment report generation
scripts/smoke_test_v4.py       — V4 pipeline smoke test
data/raw/                      — raw datasets (not in git)
data/processed/                — preprocessed data cache, PCA eigenvecs

## V3 Preprocessing Pipeline (5 ordered components) — LEGACY (used by Exp2 ablation in V3 compat mode only)
Used by: Exp2 ablation, Exp3–Exp6.
1. FOV Standardization — Hough circle detection, border removal, resize to 512×512 (BGR uint8)
2. CLAHE — applied to L-channel of LAB color space, dynamic clip limit (BGR uint8)
3. HSV Enhancement — saturation ×1.2, value ×1.1 scaling in HSV space (BGR uint8)
4. Green Channel — extract green channel, replicate to 3ch (BGR uint8, grayscale)
5. Normalize — pixel values to [0, 1] (float32)

CLAHE and HSV run BEFORE green channel so they operate on the full-color image.
Pipeline = "active" when all 5 on. Baseline = crop + resize + ImageNet normalize.
V3 augmentation (flip, rotate ±15°, zoom ±10%, brightness) is SEPARATE from preprocessing.

## V4 Preprocessing Pipeline (6-stage) — CANONICAL (used by all V4 experiments)
Used by: Exp1 configs A–F.
Stage 0: Canonical Orientation
  0a. Canonical flip (left→right eye orientation) — toggleable
  0b. OD-fovea rotation normalization (classical CV detection) — toggleable
      Detects OD (brightest region) and fovea (darkest region with distance prior)
      Rotates image so OD→fovea axis is horizontal
      When detection confidence is low, rotation is skipped (fallback)
Stage 1: FOV crop + isotropic resize + padding + mask generation — always
  - Isotropic scaling preserves fundus circle geometry
  - Centered padding fills unused canvas with zeros
  - Binary FOV mask (4th channel) marks real data (1.0) vs padding (0.0)
Stage 2: Flat-field correction (Gaussian blur subtraction, σ=45) — toggleable
Stage 3: Upgraded CLAHE (dual-constraint, L-channel, stochastic at train time) — toggleable
Stage 5: Augmentation (unified affine + brightness/contrast + PCA color) — train only
  rotation_sigma: adaptive per-image (from OD/fovea uncertainty) or fallback 13.0°
Stage 4: ImageNet normalize → tensor — always last

V4 augmentation is INTEGRATED into the pipeline (not separate).
Presets: "resnet" (full preprocessing + full aug), "efficientnet" (reduced aug).

## Experiment 1: 2×2 Factorial (CRITICAL — everything depends on this)
Dataset: EyePACS (~35,126 labeled images, 40% subset = ~14,050). 6 configurations:
- A: baseline (crop+resize+normalize) + ResNet-50
- B: full V4 pipeline + ResNet-50
- C: baseline (crop+resize+normalize) + EfficientNet-B3
- D: full V4 pipeline + EfficientNet-B3
- E: full V4 pipeline + ResNet-50 + per-patient blending (optional)
- F: full V4 pipeline + EfficientNet-B3 + per-patient blending (optional)

Dominance criterion (EH-3) — ALL THREE must hold:
- Delta weighted F1 >= 5 percentage points
- Delta ROC-AUC >= 0.02
- No Cohen Kappa degradation

## Cross-Validation
Current config: 3-fold CV with patient-level split (stratified). (changed from 5-fold; 5-fold used in original V3 governance documents)
MANDATORY: no patient images in both train and val within any fold.
Report: mean ± std across folds.

## Hardware Constraints
- batch_size: 16 (RTX 3060 12GB limit at 512×512)
- mixed_precision: true for ResNet-50, DISABLED for EfficientNet (fp16 overflow fix)
- image_size: 512×512
- input_channels: 4 (RGB + FOV mask)
- loss_function: Focal Loss (γ=2, α=inverse-frequency class weights)
- optimizer: Adam, lr=0.0001, weight_decay=0.0001
- early_stopping: patience=5, monitor=val_weighted_f1, mode=max
- scheduler: ReduceOnPlateau, factor=0.5, patience=3, min_lr=1e-6
- max_epochs: 20
- class_weights: inverse frequency
- seed: 42, deterministic=true
- num_workers: 4, persistent_workers=True, prefetch_factor=2

## Primary Metrics (descending importance)
1. Weighted F1-score
2. ROC-AUC (one-vs-rest, macro)
3. Cohen Kappa (quadratic weights)
4. Accuracy

## Commands
```bash
conda activate dr-classifier
python run_experiment.py --experiment exp1 --config configs/default.yaml
python run_experiment.py --experiment exp1 --config configs/default.yaml --configs A,B
python run_experiment.py --experiment exp2 --config configs/default.yaml
```

## Code Rules
- Type hints on all function signatures
- Docstrings with Args/Returns for every public function
- No hardcoded paths — all paths from config YAML
- Every module independently testable
- Use pathlib.Path not os.path

## Detailed specs in docs/:
- docs/RESEARCH_ARCHITECTURE.md — full experimental protocol with 6 experiments (V4)
- docs/INVARIANTS.md — hypotheses, scope boundaries, forbidden claims
- docs/HYPOTHESIS.md — H-1 through H-6 formal definitions
- docs/ARGUMENT_MAP.md — claim-evidence dependency structure

## Active Implementation Plan
OD–Fovea alignment implementation is COMPLETE (all 11 steps from PROMPT_OD_FOVEA_MINIMAL.md).
See PROMPT_OD_FOVEA_MINIMAL.md and IMPLEMENTATION_PLAN_OD_FOVEA_v2.md for reference.
Next step: run `python scripts/visualize_od_fovea.py` on EyePACS images for visual validation.
