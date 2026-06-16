# Chapter 3: Methodology

**Status:** Not started
**Chapter function:** Pipeline specification, architecture design, evaluation framework
**Governance bindings:** OD-3, OD-4, OD-5, EH-1 through EH-4, SB-3.1, DGL-5, **SB-1.12, CFC-2.9, SIR-9 (v5.3)**

## Paradigmatic framing insertion (v5.3) — Task 2.5

### §3.1 (Pipeline Formalisation) — Task 2.5
- **2.5.1** In the preamble to §3.1 explicitly note that **the decision to formalise preprocessing as part of the model is conceptual**, motivated by paradigm P2 (INVARIANTS v5.3 §I; CENTRAL_THESIS §Paradigmatic framing). The mathematical content that follows (the 8 stages of OD-3) is the *engineering realisation* of P2.
- **2.5.2** Provide a one-paragraph contrast with the Gulshan paradigm (P1; "preprocessing as ancillary data preparation"). Cite gulshan-2016.md §15 *Paradigmatic Role* and §18 *Analytical Synthesis (Paradigmatic Synthesis)* as the literature-card sources of the framing. Per CFC-2.9, no theoretical claim is attributed to Gulshan; the contrast is between two *methodological practices*.

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

# 3 METHODOLOGY OF INTEGRATED PREPROCESSING-CNN PIPELINE DESIGN

## 3.1 Formalization of the Unified Preprocessing Pipeline
- 3.1.1 Pipeline Stage Specification: 8-Stage System
- 3.1.2 Modified CLAHE Algorithm with Dual-Constraint Clip Limit
- 3.1.3 Augmentation Strategy for Class Imbalance Mitigation
- 3.1.4 External Image Ingestion Protocol

## 3.2 Design of CNN Architectures for DR Classification
- 3.2.1 ResNet-50 and EfficientNet-B3 as Primary Experimental Architectures
- 3.2.2 Historical Reference Architectures (Reference Only)

## 3.3 Transfer Learning and Pretraining Methodology
- 3.3.1 Architecture Adaptation for Five-Class DR Classification
- 3.3.2 Ophthalmology-Specific Self-Supervised Pretraining of the CNN Backbone (integrated Arm)
- 3.3.3 Two-Stage Fine-Tuning Protocol Design
- 3.3.4 Weighted Loss Function Formulation for Ordinal Class Structure

## 3.4 Evaluation Framework and Performance Metrics
- 3.4.1 Multi-Metric Assessment Framework
- 3.4.2 Cross-Validation and Statistical Reliability Protocols

- Conclusions to Chapter 3
