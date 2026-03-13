# CONTRIBUTIONS.md

## Scientific Contributions of the Dissertation

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Formal contributions register
**Binding Reference:** DISSERTATION_INVARIANTS.md v3.0, ARGUMENT_MAP.md v3.0

---

## Primary Contributions

### C-1: Cross-Device Normalization Pipeline

**Contribution:** Design, implementation, and experimental validation of a 5-component fundus image preprocessing pipeline that standardizes retinal image appearance across diverse imaging devices and acquisition conditions while preserving diagnostically relevant retinal features.

**Evidence:** Experiments 1 (preprocessing dominance via 2×2 factorial ablation), 2 (component-level ablation), and 3 (V3) (device domain shift evaluation across Canon, Topcon, Kowa, Zeiss camera hardware).

**Novelty:** The pipeline is validated not only for classification improvement on a single dataset (as in prior work) but across a multi-dataset architecture (EyePACS, APTOS, IDRiD, Messidor/Messidor-2, RFMiD, DDR, ODIR-5K) and across multiple CNN architectures (ResNet-50, EfficientNet-B3), establishing preprocessing as an integral model component rather than an ancillary data preparation step.

---

### C-2: Cross-Dataset Generalization Evidence

**Contribution:** Empirical demonstration that CNN models trained with the preprocessing pipeline on EyePACS generalize to independent clinical datasets (Messidor-2, IDRiD) without retraining, achieving generalization ratio G ≥ 0.85.

**Evidence:** Experiment 3 (V3) (cross-dataset generalization and device domain shift). Generalization ratio G = F1_external / F1_EyePACS computed per external dataset.

**Novelty:** While individual preprocessing techniques (CLAHE, normalization) have been used in prior DR classification work, systematic cross-dataset transferability evaluation with a pre-registered generalization threshold across 3+ independent datasets and 4+ camera manufacturers has not been previously reported in the literature.

---

### C-3: Lesion Feature Preservation Analysis

**Contribution:** Quantitative demonstration via Grad-CAM explainability analysis that the preprocessing pipeline directs CNN attention toward clinically relevant lesion regions (microaneurysms, hemorrhages, hard exudates, soft exudates), measured by Attention–Lesion Overlap (ALO) as primary metric.

**Evidence:** Experiment 4 (explainability analysis with ALO and IoU against IDRiD pixel-level lesion masks).

**Novelty:** Prior Grad-CAM studies in DR classification report qualitative attention maps. This dissertation introduces ALO as a quantitative, asymmetric metric that directly measures lesion coverage by model attention — answering the clinically relevant question "Does the model attend to the lesion?" — and systematically compares ALO scores between preprocessed and unprocessed conditions per lesion type.

---

## Supporting Contributions

### SC-A: Adaptive CLAHE Variant

**Contribution:** Adaptation and validation of a modified CLAHE formulation with optimized clip limit (selected via parameter sweep) in LAB color space for fundus image enhancement, extending the T/80 threshold control proposed for STARE (LC-AlTimemy-2021) to the EyePACS/IDRiD context with independent parameter validation.

**Evidence:** Experiment 2 (CLAHE threshold sensitivity on IDRiD).

---

### SC-B: CLAHE Sensitivity Characterization

**Contribution:** Identification and characterization of the CLAHE clip limit sensitivity profile for DR classification, demonstrating that per-class F1-score (particularly for DR 1 and DR 2) exhibits a non-trivial parameter-dependent sensitivity curve with an identifiable local optimum.

**Evidence:** Experiment 2 (parameter sweep on IDRiD).

---

### SC-C: Cross-Device Robustness Evaluation

**Contribution:** Systematic evaluation of preprocessing pipeline robustness across four fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss) using five datasets with documented camera metadata, producing a cross-device performance matrix.

**Evidence:** Experiment 3 (V3) (device domain shift evaluation on RFMiD, DDR, ODIR-5K, IDRiD, Messidor).

---

## Relationship to Primary Claims

| Contribution | Primary Claims Supported |
|---|---|
| C-1 | PC-1, PC-8 |
| C-2 | PC-6, PC-9 |
| C-3 | PC-7 |
| SC-A | PC-2 |
| SC-B | PC-2 |
| SC-C | PC-9 |

---

## Boundary Conditions

All contributions are bounded by the scope constraints defined in INVARIANTS.md (Section IV: Scope Boundaries) and the non-claims listed in ARGUMENT_MAP.md (Section VII). In particular:

- Contributions do not extend to general retinal disease classification or imaging modalities other than fundus photography (SB-1.1, SB-1.4)
- Contributions do not constitute clinical device certification or regulatory compliance (NC-16)
- Contributions are bounded to the tested architectures and datasets as specified in the experimental protocol
