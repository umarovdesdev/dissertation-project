# Implementation Details

## 1. Software Stack

| Component | Version | Purpose |
|---|---|---|
| Python | 3.11 | Primary programming language |
| PyTorch | Latest stable | Deep learning framework; model training and inference |
| Torchvision | Compatible with PyTorch | Pre-trained model weights (ImageNet); image transforms |
| OpenCV | Latest stable | Image preprocessing (CLAHE, Hough transform, color space conversion) |
| NumPy | Latest stable | Numerical operations; array manipulation |
| Scikit-learn | Latest stable | Evaluation metrics (F1, Kappa, ROC-AUC); cross-validation utilities |
| Matplotlib | Latest stable | Visualization; Grad-CAM overlays; training curves |

---

## 2. Hardware Configuration

| Parameter | Value |
|---|---|
| GPU | TBD (to be documented at experiment execution) |
| CUDA Version | TBD |
| RAM | TBD |
| Storage | TBD |

All hardware conditions are documented at experiment execution time per DGL-2 (hardware-specific reproducibility). Results are bounded to the specific hardware configuration used.

---

## 3. Model Definition

The proposed model is defined as a **two-stage system**:

```
model = V4_preprocessing + CNN_classifier
```

**Stage 1 — Preprocessing Pipeline:** The 6-stage V4 pipeline (see `methods/preprocessing-pipeline.md`) transforms raw fundus images into a standardized feature space. The preprocessing pipeline is an integral component of the model, not an external data preparation step. It defines the feature space available to the CNN.

**Stage 2 — CNN Classifier:** A pre-trained CNN backbone adapted via transfer learning for 5-class DR classification (DR 0–4).

### CNN Architectures

| Architecture | Role | Pre-training |
|---|---|---|
| ResNet-50 | Factorial design Arm A (Experiment 1) | ImageNet |
| EfficientNet-B3 | Factorial design Arm B (Experiment 1) | ImageNet |
| EfficientNet-B4 | Explainability analysis (Experiment 4) | ImageNet |
| EfficientNet-B0 | Two-stage fine-tuning training strategy (training method; H-3 dropped in V3 — retained as training protocol only, not an independently tested hypothesis) | ImageNet |

---

## 4. CLAHE Configuration (V4 Dual-Constraint)

| Parameter | Value |
|---|---|
| Color space | LAB (L-channel) |
| Tile grid size | 8×8 |
| Clip limit formula | CL_tile = min(clip_factor × tile_area/256, global_threshold × tile_area) |
| clip_factor | Tunable hyperparameter (optimized via parameter sweep, Experiment 2; per DGL-5) |
| global_threshold | Tunable hyperparameter (optimized via parameter sweep, Experiment 2; per DGL-5) |
| Train-time application | Stochastic — 80% probability |
| Inference-time application | Deterministic |
| Theoretical reference | CL = T/80 (LC-AlTimemy-2021, STARE dataset) |

The dual-constraint clip limit is treated as a two-parameter optimizable formulation rather than a single fixed constant. The T/80 formulation from LC-AlTimemy-2021 serves as theoretical reference; the dissertation validates its own clip limit configuration independently (DGL-5).

---

## 5. Training Configuration

| Parameter | Value |
|---|---|
| Optimizer | Adam |
| Learning rate | 1e-4 |
| Batch size | 16 |
| Maximum epochs | 20 |
| Loss function | Cross-entropy |
| Early stopping | Monitored on validation loss; patience=5 (ResNet-50), patience=3 (EfficientNet) |
| Input resolution | 512×512 |
| Mixed precision | Enabled for ResNet-50; **DISABLED for EfficientNet** (fp16 overflow) |
| DataLoader workers | num_workers=4; persistent_workers=True; prefetch_factor=2 |

### Two-Stage Fine-Tuning Protocol (EfficientNetB0)

**Stage 1 — Frozen base:**
- Freeze all backbone layers
- Train classification head only
- Learning rate: 1e-4

**Stage 2 — Progressive unfreezing:**
- Unfreeze upper backbone layers progressively
- Reduced learning rate for unfrozen layers (1e-5)
- Continue training until convergence or early stopping

---

## 6. Data Splitting

**Strategy:** 3-fold cross-validation with patient-level split.

- No patient's images appear in both training and test partitions within any fold
- All metrics reported as mean ± standard deviation across 3 folds
- Data augmentation applied only to training partitions

**Augmentation (V4 — integrated into pipeline as Stage 5, training only):**
- Unified affine: rotation + zoom + stretch + shear
- Brightness/contrast adjustment
- PCA color jitter
- Model-specific presets: "resnet" (full augmentation) vs. "efficientnet" (reduced augmentation)

Augmentation is integrated into the V4 pipeline as Stage 5 (not a separate layer). See `methods/preprocessing-pipeline.md` for full specification.

---

## 7. Grad-CAM Explainability

**Method:** Gradient-weighted Class Activation Mapping (Grad-CAM) applied to the final convolutional layer of the CNN.

**Primary metric — Attention–Lesion Overlap (ALO):**

```
ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)
```

ALO measures what fraction of the lesion is covered by model attention. This is the clinically relevant metric — it answers "Does the model attend to the lesion?"

**Secondary metric — Intersection-over-Union (IoU):**

```
IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)
```

IoU measures symmetric spatial precision of attention overlap.

**Lesion types evaluated:** Microaneurysms, hemorrhages, hard exudates, soft exudates (from IDRiD pixel-level annotations).

---

## 8. Per-Patient Binocular Blending (Configs E and F)

**Purpose:** Optional extension to patient-level inference by combining left-eye and right-eye feature representations.

**Architecture — PatientHead:**
1. Backbone CNN processes left-eye and right-eye images independently → two feature vectors (f_L, f_R)
2. Fusion: concatenate(f_L, f_R) + element-wise absolute difference |f_L − f_R| → MLP
3. MLP → 5-class softmax logits

**Prerequisite:** Canonical flip (Stage 0) must be applied to ensure consistent right-eye orientation before bilateral feature comparison. Without Stage 0, left/right feature alignment is undefined.

**Experiment 1 role:** Configs E (PatientHead + ResNet-50) and F (PatientHead + EfficientNet-B3) are optional supplementary extensions to the core 2×2 factorial (A–D). EH-3 satisfaction requires only A–D; E and F provide additional evidence per EH-4 (Configs E and F are not required for EH-4 satisfaction).

---

## 9. Reproducibility

| Control | Implementation |
|---|---|
| Random seed | 42 (fixed across all experiments) |
| Deterministic mode | PyTorch deterministic operations enabled (deterministic=True) |
| Augmentation parameters | Fixed (not randomized per run) |
| Learning rate schedule | Documented and reproducible |
| Software versions | Pinned in requirements.txt |
