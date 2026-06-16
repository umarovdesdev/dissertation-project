# Chapter 4: Experimental Research

**Status:** Not started — BLOCKED on dr-classifier experiment completion
**Chapter function:** Experiments 1–4 execution, results, analysis
**Governance bindings:** H-1, H-2, H-4, H-5, H-6, PC-1, PC-2, PC-6, PC-7, PC-8, PC-9, EH-3, EH-4, **SB-1.12, CFC-2.9, PC-0 (v5.3)**
**Key sources:** dr-classifier experiment outputs (training logs, metrics, confusion matrices)

## Paradigmatic framing insertion (v5.3) — Task 2.6

### §4.2 (Experiment 1 — Causal Improvement) — Task 2.6
- **2.6.1 — Configs A/C (baseline arm).** In the configuration description, state explicitly: *"The baseline configuration of Experiment 1 (configs A and C) operationally instantiates the end-to-end CNN classification paradigm (P1), of which Gulshan et al. (2016) is the canonical representative in this dissertation. It is not Gulshan's system; it is an internal operational construct defined by OD-3 (stretch-resize + ImageNet normalize, 3 channels)."*
- **2.6.2 — Configs B/D (integrated arm).** State: *"The integrated configuration of Experiment 1 (configs B and D) operationalises the integrated preprocessing-CNN paradigm (P2), in which preprocessing is treated as an integral model component co-determining the feature space available to the CNN. The 8 stages of OD-3 are the engineering realisation of this paradigm."*
- **2.6.3 — Discussion.** State explicitly that the A-vs-B (and C-vs-D) result is interpreted as an **empirical contrast between two paradigms under matched conditions**, *not* as a numerical comparison against Gulshan's reported figures. Per CFC-2.2 and SB-1.12, no direct numerical claim against Gulshan is permissible. Per CFC-2.8 v5.1, the A-vs-B difference reflects the joint contribution of preprocessing and pretraining source.

### Cross-cutting forbidden phrasings
"Gulshan is our baseline" / "we outperform Gulshan" / "configs A/C reproduce Gulshan." The operational baseline must always be referred to as "configs A/C" or "the baseline configuration" (operational, OD-3) — never as "Gulshan."

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

# 4 EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

## 4.1 Datasets and Experimental Configuration
- 4.1.1 Tiered Dataset Architecture
- 4.1.2 Class Distribution Analysis and Data Partitioning Strategy
- 4.1.3 Hardware Specification and Reproducibility Protocol

## 4.2 Experiment 1: Integrated Pipeline Dominance — Pipeline + In-Domain Pretraining vs. Baseline on EyePACS (H-1)
- 4.2.1 Restored 2×2 Factorial Design (Configurations A–D)
- 4.2.2 Training Dynamics and Convergence Analysis
- 4.2.3 Quantitative Comparison of Diagnostic Metrics

## 4.3 Experiment 2: Stage Ablation + CLAHE/σ Sweeps (H-2)
- 4.3.1 Ablation Design (Levels 0–6)
- 4.3.2 CLAHE Threshold Sensitivity Analysis (H-2 Sub-Analysis)
- 4.3.3 Flat-Field σ Sweep and Image Quality Metrics

## 4.4 Experiment 3: Cross-Dataset Transferability on APTOS 2019 (H-4)
- 4.4.1 Zero-Shot Transfer to APTOS 2019
- 4.4.2 Baseline vs Pipeline Comparison

## 4.5 Experiment 4: Grad-CAM Explainability on IDRiD + Clinical (H-5)
- 4.5.1 Grad-CAM Generation Protocol
- 4.5.2 Quantitative ALO and IoU with IDRiD Lesion Masks
- 4.5.3 Attention Consistency Across Datasets

## 4.6 Experiment 5: Clinical Degradation Resistance on IDRiD + Messidor-2 (H-7)

## 4.7 Experiment 6: Device Domain Shift on DDR + ODIR-5K + RFMiD (H-6)

## 4.8 Experiment 7: Small Data Training (IDRiD → Clinical)

- Conclusions to Chapter 4
