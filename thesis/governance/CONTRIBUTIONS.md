# CONTRIBUTIONS.md

## Scientific Contributions of the Dissertation

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Formal contributions register
**Version:** 5.3 | **Date:** 2026-05-28 | **Binding Reference:** INVARIANTS.md v5.3

---

## Conceptual Framing of the Primary Contributions

The principal conceptual contribution of this dissertation is a **paradigm shift** — from paradigm P1 (the end-to-end CNN paradigm, in which preprocessing is treated as ancillary data preparation; Gulshan et al. 2016 is its canonical representative) to paradigm P2 (the integrated preprocessing-CNN paradigm, in which preprocessing is an integral model component that co-determines the feature space available to the network). The four primary contributions (C-1 through C-3) and the supporting contributions (SC-A through SC-G) operationalise P2: each is, at one level, an engineering result on the 8-stage V5 pipeline and, at a second level, evidence for the productivity of P2 as a methodological stance. The contributions therefore have a dual character — engineering and conceptual — and the dissertation reports them under both readings, in line with SB-1.12, CFC-2.8, CFC-2.9, and SIR-9 in INVARIANTS v5.3.

---

## Primary Contributions

### C-1: Integrated Preprocessing-CNN Pipeline (Operationalisation of Paradigm P2)

**Contribution:** Design, implementation, and experimental validation of an 8-stage V5 fundus image preprocessing pipeline that standardizes retinal image appearance across diverse imaging devices and acquisition conditions while preserving diagnostically relevant retinal features. The pipeline outputs 4-channel tensors (RGB + binary FOV mask) with dataset-specific normalization. At the **conceptual** level, the contribution is the formalisation of preprocessing as a binding part of the model specification — the operationalisation of paradigm P2 — and the explicit placement of this paradigm under controlled experimental contrast against the paradigm represented by Gulshan et al. (2016) and the broader P1 literature. At the **engineering** level, the contribution is the specific 8-stage realisation enumerated below.

**Evidence:** Experiment 1 (preprocessing dominance via 2×2 factorial ablation A–D, ResNet-50 and EfficientNet-B3), Experiment 2 (component-level ablation across 7 V5 levels + CLAHE sweep + flat-field σ sweep), and Experiment 6 (device domain shift evaluation across Canon, Topcon, Kowa, Zeiss camera hardware).

**Novelty:** Novelty is twofold.
- *Conceptual:* The dissertation reframes preprocessing as an integral model component (paradigm P2) and places this reframing under direct empirical test, in contrast to the P1 tradition (Gulshan, Pratt, Rakhlin, Saxena, Ting, Voets) in which preprocessing is unformalised in the main text or deferred to supplementary material. Per CFC-2.9, this is a claim about the observable methodological practice of those works, not an attribution to them of an explicit "preprocessing is unimportant" thesis.
- *Engineering:* The V5 pipeline introduces: (a) isotropic resize with centered zero-padding preserving fundus circle geometry, (b) explicit FOV mask as a 4th input channel informing the CNN of valid pixel regions, (c) adaptive flat-field correction with σ proportional to FOV diameter (σ = 0.07·D) rather than a fixed global σ, (d) dataset-specific normalization computed from training set mask=1.0 pixels rather than ImageNet defaults, (e) canonical orientation via OD-fovea rotation normalization with adaptive augmentation σ. The pipeline is validated across a multi-dataset architecture (EyePACS, APTOS 2019, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD, Clinical) and across multiple CNN architectures (ResNet-50, EfficientNet-B3).

---

### C-2: Cross-Dataset Generalization Evidence

**Contribution:** Empirical demonstration that CNN models trained with the V5 preprocessing pipeline on EyePACS generalize to APTOS 2019 without retraining, achieving generalization ratio G ≥ 0.85.

**Evidence:** Experiment 3 (cross-dataset transferability). Generalization ratio G = F1_APTOS / F1_EyePACS computed on zero-shot transfer.

**Novelty:** Systematic cross-dataset transferability evaluation with a pre-registered generalization threshold on an independent 5-class DR dataset from mixed camera sources.

---

### C-3: Lesion Feature Preservation Analysis

**Contribution:** Quantitative demonstration via Grad-CAM explainability analysis that the preprocessing pipeline directs CNN attention toward clinically relevant lesion regions (microaneurysms, hemorrhages, hard exudates, soft exudates), measured by Attention–Lesion Overlap (ALO) as primary metric on IDRiD, with qualitative Grad-CAM overlays on a Kazakh clinical dataset.

**Evidence:** Experiment 4 (explainability analysis with ALO and IoU against IDRiD pixel-level lesion masks; Grad-CAM overlays on Clinical dataset).

**Novelty:** This dissertation introduces ALO as a quantitative, asymmetric metric that directly measures lesion coverage by model attention and systematically compares ALO scores between preprocessed and unprocessed conditions per lesion type. The addition of qualitative clinical validation on Kazakh data extends the analysis beyond benchmark datasets.

---

## Supporting Contributions

### SC-A: Adaptive CLAHE Variant

**Contribution:** Adaptation and validation of a modified CLAHE formulation with dual-constraint clip limit (clip_factor × tile_area/256, capped by global_threshold × tile_area; selected via parameter sweep) in LAB color space for fundus image enhancement. Stochastic application at train time (80% probability) provides additional regularization.

**Evidence:** Experiment 2 (CLAHE threshold sensitivity on EyePACS).

---

### SC-B: CLAHE Sensitivity Characterization

**Contribution:** Identification and characterization of the CLAHE clip limit sensitivity profile for DR classification, demonstrating that per-class F1-score (particularly for DR 1 and DR 2) exhibits a non-trivial parameter-dependent sensitivity curve with an identifiable local optimum.

**Evidence:** Experiment 2 (parameter sweep on EyePACS).

---

### SC-C: Cross-Device Robustness Evaluation

**Contribution:** Systematic evaluation of preprocessing pipeline robustness across four fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss) using five datasets with documented camera metadata, producing a cross-device performance matrix. DR labels only; non-DR disease labels ignored or mapped.

**Evidence:** Experiment 6 (device domain shift evaluation on DDR, ODIR-5K, RFMiD).

---

### SC-D: Adaptive Flat-Field Illumination Normalization

**Contribution:** Design and validation of an adaptive Gaussian blur subtraction stage (corrected = image − GaussianBlur(image, σ) + 128, σ = 0.07 × FOV diameter) for uneven illumination correction in fundus images. The adaptive σ scales with image geometry rather than using a fixed value, and correction is applied only inside the FOV mask to prevent padding artifacts.

**Evidence:** Experiment 2 (component-level ablation + flat-field σ sweep across 0.05–0.10·D). Image quality metrics (CNR, VVI, SSIM) measured before and after Stage 4.

**Novelty:** Adaptive flat-field correction scales with per-image FOV diameter rather than using a global fixed σ, accommodating variability in fundus image size and FOV coverage across imaging devices.

---

### SC-E: FOV Mask as Explicit Pipeline Component

**Contribution:** Explicit generation of a binary FOV mask (1.0 = real fundus data, 0.0 = zero-padding) as a dedicated pipeline stage (Stage 3), appended as the 4th input channel. This informs the CNN of valid pixel regions, preventing the model from learning padding artifacts as features.

**Evidence:** Experiment 1 (full V5 configs B/D use 4-channel input) and Experiment 2 (ablation level including isotropic resize + mask).

---

### SC-F: OD-Fovea Rotation Normalization (Stage 1)

**Contribution:** Design and implementation of classical-CV-based optic disc (OD) and fovea detection for fundus image rotation normalization (Stage 1). The image is rotated so the OD→fovea axis is horizontal. When detection confidence is low, rotation is skipped (fallback). The rotation σ for Stage 6 augmentation is adapted per-image from OD/fovea detection uncertainty (fallback: σ = 13.0°).

**Evidence:** Experiment 2 (component-level ablation, Stage 1 contribution). Implementation: `src/preprocessing/od_fovea_detect.py`, `src/preprocessing/canonical_orientation.py`.

---

### SC-G: Clinical Degradation Resistance

**Contribution:** Empirical demonstration that V5 preprocessing reduces cross-dataset performance degradation. The metric Δ = F1_EyePACS_val − F1_external is computed for both baseline and V5 models on IDRiD and Messidor-2. Smaller Δ with V5 indicates more robust transfer.

**Evidence:** Experiment 5 (clinical degradation resistance, H-7).

---

## Relationship to Primary Claims

| Contribution | Primary Claims Supported |
|---|---|
| C-1 | PC-1, PC-8 |
| C-2 | PC-6 |
| C-3 | PC-7 |
| SC-A | PC-2 |
| SC-B | PC-2 |
| SC-C | PC-9 |
| SC-D | PC-1, PC-8 |
| SC-E | PC-1, PC-8 |
| SC-F | PC-1, PC-8 |
| SC-G | PC-10 |

---

## Boundary Conditions

All contributions are bounded by the scope constraints defined in INVARIANTS.md (Section IV: Scope Boundaries) and the non-claims listed in ARGUMENT_MAP.md (Section VII). In particular:

- Contributions do not extend to general retinal disease classification or imaging modalities other than fundus photography
- Contributions do not constitute clinical device certification or regulatory compliance
- Contributions are bounded to the tested architectures (ResNet-50, EfficientNet-B3, EfficientNet-B4) and datasets as specified in the experimental protocol
