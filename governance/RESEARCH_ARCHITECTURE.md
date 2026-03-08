# RESEARCH_ARCHITECTURE_MASTER.md

## Integrated Preprocessing–CNN Framework for Multi-Stage Diabetic Retinopathy Classification

**Candidate:** Yesmukhamedov N.S.
**Status:** Binding Methodological Blueprint
**Function:** Experimental, statistical, and architectural formalization of the dissertation research

---

# 1. RESEARCH LOGIC STRUCTURE

## 1.1 Central Causal Chain

Contrast-Adaptive Preprocessing
→ Improved Microvascular Feature Visibility
→ Stabilized CNN Feature Extraction
→ Improved Multi-Class DR Classification
→ Measurable Statistical Dominance (EH-3 criteria)

Dominance is defined strictly per Invariants (Δ weighted F1 ≥ 5 pp; Δ ROC-AUC ≥ 0.02; no Cohen’s Kappa degradation) .

---

# 2. DATA ARCHITECTURE

## 2.1 Primary Dataset

**APTOS 2019**

* 3,662 labeled fundus images
* Five DR stages (0–4)
* Severe class imbalance (see SB-2.1) 

Split strategy:

* Train: 80%
* Validation: 10%
* Test: 10%
* Stratified by class
* Patient-level leakage control (mandatory)

---

## 2.2 Secondary Dataset (Cross-Database Generalization)

**STARE dataset**

* Used for CLAHE theoretical validation context
* Used for cross-database F1 ratio testing

Cross-database generalization defined as:

[
G = \frac{F1_{secondary}}{F1_{primary}}
]

Bounded strictly per OD-4 .

---

# 3. PREPROCESSING PIPELINE ARCHITECTURE

Defined per OD-3 .

## 3.1 Ordered Pipeline

1. Resizing (256×256 or 512×512)
2. Pixel normalization to [0,1]
3. CLAHE (clip limit ≥ 2.0, grid ≥ 8×8)
4. Data augmentation:

   * Flip (H/V)
   * Rotation ±15°
   * Zoom ±10%
   * Brightness variation

Pipeline considered ACTIVE only if all four stages applied.

---

## 3.2 CLAHE Mathematical Formalization

Conventional:

[
CL = \lceil L/T \rceil + \beta(\phi - \lceil L/T \rceil)
]

Modified:

[
CL = T / 80
]

Transferability from STARE to APTOS is NOT assumed (DGL-5) .

---

# 4. MODEL ARCHITECTURE LAYER

## 4.1 Baseline CNN (Low Complexity Reference)

* 2 convolution blocks (32–64 filters)
* MaxPooling 2×2
* Sigmoid output
* Binary cross-entropy
* No batch normalization
* No dropout

Defined per OD-2 .

---

## 4.2 Enhanced CNN (High Complexity Reference)

* 4 convolution blocks (32–256 filters)
* Batch normalization
* Dropout 0.4
* Softmax (5-class)
* Categorical cross-entropy
* Adam (lr=0.0001)

---

## 4.3 Transfer Learning Layer

Backbone: EfficientNetB0 (ImageNet pre-trained)

Two strategies:

### Method 1 — Frozen

* Train classification head only

### Method 2 — Progressive Fine-Tuning

* Stage 1: Frozen
* Stage 2: Unfreeze upper layers

Expected empirical baseline (self-publications) :

* Frozen F1 ≈ 0.62
* Fine-tuned F1 ≈ 0.74

---

# 5. EXPERIMENTAL DESIGN

## 5.1 Experiment 1 — Preprocessing Dominance

Baseline CNN:

* With preprocessing
* Without preprocessing

Enhanced CNN:

* With preprocessing
* Without preprocessing

Primary test: EH-3 compliance.

---

## 5.2 Experiment 2 — CLAHE Threshold Sensitivity

Independent variable:

* Clip limit parameter range

Dependent:

* Per-class F1 (DR 1, DR 2)

Requirement:

* Non-trivial sensitivity curve
* At least one local optimum
* No extrapolation beyond tested range

---

## 5.3 Experiment 3 — Fine-Tuning Strategy

Compare:

* Frozen vs Progressive

Metrics:

* Precision (Test)
* Recall (Test)
* F1 (Test)
* Cohen’s Kappa

---

# 6. STATISTICAL VALIDATION FRAMEWORK

## 6.1 Primary Metrics (EH-1) 

* Weighted F1
* ROC-AUC
* Cohen’s Kappa (quadratic)
* Accuracy

---

## 6.2 Secondary Metrics

* Per-class F1
* Confusion matrix
* Sensitivity / Specificity
* Training–Test gap (overfitting threshold = 15 pp)

---

## 6.3 Statistical Tests

Mandatory:

* McNemar test (paired classification comparison)
* DeLong test (ROC comparison)
* 95% confidence intervals (bootstrap ≥ 1000 iterations)

---

# 7. ABLATION PROTOCOL

To isolate driver of improvement:

| Configuration | Preprocessing | Architecture |
| ------------- | ------------- | ------------ |
| A             | No            | Baseline     |
| B             | Yes           | Baseline     |
| C             | No            | Enhanced     |
| D             | Yes           | Enhanced     |

Dominance validated if:

(B − A) > (C − A)

in weighted F1 and ROC-AUC.

---

# 8. COMPUTATIONAL CONSTRAINT MODEL

Resource-limited defined per OD-6 :

* No guaranteed GPU
* <16GB RAM
* Real-time constraint
* Limited network access

All experiments bounded to actual hardware conditions.

---

# 9. RISK CONTROL LAYER

## 9.1 Leakage Control

* No augmented images in validation/test
* No patient overlap across splits

## 9.2 Overfitting Control

* Early stopping
* Dropout
* Batch normalization
* Weighted loss

## 9.3 Reproducibility

* Fixed random seed
* Fixed augmentation parameters
* Fixed learning rate schedule

---

# 10. FORMAL NOVELTY LAYER

Novelty does NOT claim:

* Global SOTA
* Clinical deployment validation
* Cross-modality transfer
* Replacement of ophthalmologist

Boundaries enforced per SB-1 .

Novelty IS:

* Formalization of preprocessing dominance hypothesis
* Threshold-controlled CLAHE validation within DR multi-class context
* Unified ablation-driven causal validation
* Architecture constrained to resource-limited environments

---

# 11. DEFENSE-READY CLAIM MATRIX

| Claim | Validated By            |
| ----- | ----------------------- |
| PC-1  | Exp 1 + EH-3            |
| PC-2  | Exp 2 curve             |
| PC-3  | Exp 3 metrics           |
| PC-4  | Mathematical derivation |
| PC-5  | UML + system design     |

Mapped to ARGUMENT_MAP .

---

# 12. FUNCTION OF THIS DOCUMENT

This file is:

* The methodological backbone of Chapter 2
* The execution blueprint for Chapter 4
* The validation structure for Chapter 5
* The defense shield during committee questioning

---
