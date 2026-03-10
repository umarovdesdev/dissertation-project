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
model = preprocessing_pipeline + CNN_classifier
```

**Stage 1 — Preprocessing Pipeline:** The 6-stage ordered pipeline (see `methods/preprocessing-pipeline.md`) transforms raw fundus images into a standardized feature space. The preprocessing pipeline is an integral component of the model, not an external data preparation step. It defines the feature space available to the CNN.

**Stage 2 — CNN Classifier:** A pre-trained CNN backbone adapted via transfer learning for 5-class DR classification (DR 0–4).

### CNN Architectures

| Architecture | Role | Pre-training |
|---|---|---|
| ResNet-50 | Factorial design Arm A (Experiment 1) | ImageNet |
| EfficientNet-B3 | Factorial design Arm B (Experiment 1) | ImageNet |
| EfficientNet-B4 | Explainability analysis (Experiment 4) | ImageNet |
| EfficientNetB0 | Two-stage fine-tuning (Experiment 3) | ImageNet |

---

## 4. CLAHE Configuration

| Parameter | Value |
|---|---|
| Color space | LAB (L-channel) |
| Tile grid size | 8×8 |
| Clip limit | Dynamic (optimized within experimental framework) |
| Theoretical reference | CL = T/80 (LC-AlTimemy-2021, STARE dataset) |

The clip limit is treated as an optimizable parameter rather than a fixed constant. The T/80 formulation from LC-AlTimemy-2021 serves as theoretical reference; the dissertation validates its own clip limit configuration independently (DGL-5).

---

## 5. Training Configuration

| Parameter | Value |
|---|---|
| Optimizer | Adam |
| Learning rate | 1e-4 |
| Batch size | 16 |
| Maximum epochs | 50 |
| Loss function | Cross-entropy |
| Early stopping | Monitored on validation loss; patience TBD |
| Input resolution | 512×512 |

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

**Strategy:** 5-fold cross-validation with patient-level split.

- No patient's images appear in both training and test partitions within any fold
- All metrics reported as mean ± standard deviation across folds
- Data augmentation applied only to training partitions

**Augmentation (training only):**
- Horizontal flip
- Vertical flip
- Rotation ±15°
- Zoom ±10%
- Brightness variation

Augmentation is a separate layer from preprocessing (see `methods/preprocessing-pipeline.md`).

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

## 8. Reproducibility

| Control | Implementation |
|---|---|
| Random seed | Fixed across all experiments |
| Deterministic mode | PyTorch deterministic operations enabled |
| Augmentation parameters | Fixed (not randomized per run) |
| Learning rate schedule | Documented and reproducible |
| Software versions | Pinned in requirements.txt |
