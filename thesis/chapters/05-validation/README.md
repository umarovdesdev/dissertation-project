# Chapter 5: Reliability Validation

**Status:** Not started — depends on Chapter 4 completion
**Chapter function:** Statistical validation, comparative analysis, limitations
**Governance bindings:** EH-3, EH-4, CFC-2.2, NC-2, SB-1 through SB-4, DGL-1 through DGL-6, **SB-1.12, CFC-2.9 (v5.3)**

## Paradigmatic framing insertion (v5.3) — Task 2.7

### §5.1 (Cross-Dataset Generalization) and §5.5 (Comparative Analysis with Published Systems) — Task 2.7

- **2.7.1** In §5.5, when comparing the dissertation's results against the literature, use the **paradigmatic framing** explicitly. Numerical values from Gulshan 2016 (AUC 0.991 EyePACS-1; AUC 0.990 Messidor-2) may be reported only as **contextual / historical reference**, never as a direct benchmark. The dissertation reports five-class metrics; Gulshan reports binary referable-DR AUC; the two are not commensurable.
- **2.7.2** Every mention of Gulshan's numerical figures must be accompanied by an explicit **caveat block** noting the methodological differences: classification task (binary vs. five-class), backbone (Inception-v3 ensemble vs. ResNet-50 / EfficientNet-B3), pretraining source (ImageNet vs. ImageNet/ophthalmology-specific SSL), dataset partition (private composite + private clinical-validation vs. EyePACS public partition), reference standard (multi-grader majority vote vs. public five-class labels), validation protocol (operating-point sensitivity/specificity vs. weighted F1 / ROC-AUC / Cohen's Kappa).

### Forbidden phrasings (Chapter 5)
"We outperform Gulshan" — forbidden (CFC-2.2, SB-1.12). "Our AUC exceeds Gulshan's" — forbidden (incommensurable endpoints). "Gulshan's baseline is surpassed" — forbidden (conflates Gulshan with the operational baseline).

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

> Note: the comparative-analysis section is **§5.3** in the v6.0.0 TOC (the §5.5 references in the framing notes above predate the renumbering).

# 5 RELIABILITY VALIDATION AND COMPARATIVE ANALYSIS

## 5.1 Explainability Results

## 5.2 Statistical Validation
- 5.2.1 Bootstrap Confidence Intervals and Mixed-Effects Model
- 5.2.2 Final Claim Strength Classifications

## 5.3 Comparative Analysis with Published Systems
- 5.3.1 Benchmarking Against Published Results: IDx-DR, EyeNuk, DeepMind
- 5.3.2 Performance-Complexity Trade-Off Analysis

## 5.4 Limitations and Boundary Conditions of the Proposed Approach

- Conclusions to Chapter 5
