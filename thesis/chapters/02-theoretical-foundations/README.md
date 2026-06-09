# Chapter 2: Theoretical Foundations

**Status:** Not started
**Chapter function:** Mathematical and theoretical grounding for methods in Chapters 3–4
**Governance bindings:** OD-1 through OD-6, DGL-5, DGL-6, SIR-3, SIR-6, **SB-1.12, SIR-9 (v5.3 — minor; main paradigmatic discussion lives in Ch 1.4)**

**Paradigmatic framing note (v5.3).** Chapter 2 provides mathematical and theoretical grounding; the paradigmatic discussion itself is sited in Chapter 1.4. Where Chapter 2 discusses CNN feature hierarchies, transfer learning theory, or preprocessing methods (histogram equalisation, flat-field correction, CLAHE), it must be consistent with the paradigm P2 reading: preprocessing is treated as a component of the model whose mathematical properties co-determine the feature space presented to the convolutional layers. Forbidden phrasings from INVARIANTS v5.3 CFC-2.9 apply throughout.

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

# 2 THEORETICAL FOUNDATIONS OF IMAGE PREPROCESSING AND DEEP LEARNING FOR FUNDUS IMAGE ANALYSIS

## 2.1 Mathematical Foundations of Image Enhancement Techniques
- 2.1.1 Histogram Equalization and Adaptive Contrast Enhancement
- 2.1.2 Formalization of CLAHE with Dual-Constraint Clip Limit
- 2.1.3 Spatial Filtering and Noise Reduction Methods

## 2.2 Theoretical Framework of Convolutional Neural Networks
- 2.2.1 Convolution, Pooling, and Feature Extraction Operations
- 2.2.2 Loss Functions and Optimization for Imbalanced Medical Datasets
- 2.2.3 Regularization Techniques: Dropout, Batch Normalization, and Data Augmentation

## 2.3 Transfer Learning and Self-Supervised Representation Learning Theory
- 2.3.1 Feature Transferability Across Visual Domains
- 2.3.2 Frozen-Layer versus Progressive Fine-Tuning Strategies
- 2.3.3 In-Domain Self-Supervised Pretraining for Retinal Imaging

## 2.4 Mathematical Modeling of Laser-Tissue Interaction in Retinal Therapy
- 2.4.1 Coupled Thermal-Optical Model of Fundus Tissue Response
- 2.4.2 Implications for Diagnostic Image Feature Interpretation

## 2.5 Explainability in Deep Learning for Medical Imaging
- 2.5.1 Class Activation Mapping (CAM) and Grad-CAM Mathematical Formulation
- 2.5.2 Interpretation of Attention Maps in Ophthalmic Context
- 2.5.3 ALO and IoU as Quantitative Explainability Metrics

## 2.6 Image Quality Metrics for Preprocessing Evaluation

- Conclusions to Chapter 2
