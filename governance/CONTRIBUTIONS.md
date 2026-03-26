# CONTRIBUTIONS.md

## Scientific Contributions of the Dissertation

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Formal contributions register
**Binding Reference:** DISSERTATION_INVARIANTS.md v4.0, ARGUMENT_MAP.md v4.0

---

## Primary Contributions

### C-1: Cross-Device Normalization Pipeline

**Contribution:** Design, implementation, and experimental validation of a 6-stage V4 fundus image preprocessing pipeline that standardizes retinal image appearance across diverse imaging devices and acquisition conditions while preserving diagnostically relevant retinal features.

**Evidence:** Experiment 1 (preprocessing dominance via 6-config factorial ablation A–F, ResNet-50 and EfficientNet-B3), Experiment 2 (component-level ablation, V4 Levels 0–4), and Experiment 6 (device domain shift evaluation across Canon, Topcon, Kowa, Zeiss camera hardware).

**Novelty:** The V4 pipeline introduces canonical orientation (Stage 0a: canonical flip; Stage 0b: OD-fovea rotation normalization), flat-field correction (Stage 2) as novel stages, upgrades CLAHE to a dual-constraint stochastic formulation, and integrates augmentation as a pipeline stage (not a separate layer). The pipeline is validated not only for classification improvement on a single dataset (as in prior work) but across a multi-dataset architecture (EyePACS, IDRiD, Messidor/Messidor-2, RFMiD, DDR, ODIR-5K) and across multiple CNN architectures (ResNet-50, EfficientNet-B3), establishing preprocessing as an integral model component rather than an ancillary data preparation step.

---

### C-2: Cross-Dataset Generalization Evidence

**Contribution:** Empirical demonstration that CNN models trained with the preprocessing pipeline on EyePACS generalize to independent clinical datasets (Messidor-2, IDRiD) without retraining, achieving generalization ratio G ≥ 0.85.

**Evidence:** Experiment 5 (V4) (cross-dataset generalization). Generalization ratio G = F1_external / F1_EyePACS computed per external dataset (Messidor, Messidor-2, IDRiD).

**Novelty:** While individual preprocessing techniques (CLAHE, normalization) have been used in prior DR classification work, systematic cross-dataset transferability evaluation with a pre-registered generalization threshold across 3+ independent datasets and 4+ camera manufacturers has not been previously reported in the literature.

---

### C-3: Lesion Feature Preservation Analysis

**Contribution:** Quantitative demonstration via Grad-CAM explainability analysis that the preprocessing pipeline directs CNN attention toward clinically relevant lesion regions (microaneurysms, hemorrhages, hard exudates, soft exudates), measured by Attention–Lesion Overlap (ALO) as primary metric.

**Evidence:** Experiment 4 (explainability analysis with ALO and IoU against IDRiD pixel-level lesion masks).

**Novelty:** Prior Grad-CAM studies in DR classification report qualitative attention maps. This dissertation introduces ALO as a quantitative, asymmetric metric that directly measures lesion coverage by model attention — answering the clinically relevant question "Does the model attend to the lesion?" — and systematically compares ALO scores between preprocessed and unprocessed conditions per lesion type.

---

## Supporting Contributions

### SC-A: Adaptive CLAHE Variant

**Contribution:** Adaptation and validation of a modified CLAHE formulation with dual-constraint clip limit (clip_factor × tile_area/256, capped by global_threshold × tile_area; selected via parameter sweep) in LAB color space for fundus image enhancement, extending the T/80 threshold control proposed for STARE (LC-AlTimemy-2021) to the EyePACS/IDRiD context with independent parameter validation. Stochastic application at train time (80% probability) provides additional regularization.

**Evidence:** Experiment 2 (CLAHE threshold sensitivity on IDRiD).

---

### SC-B: CLAHE Sensitivity Characterization

**Contribution:** Identification and characterization of the CLAHE clip limit sensitivity profile for DR classification, demonstrating that per-class F1-score (particularly for DR 1 and DR 2) exhibits a non-trivial parameter-dependent sensitivity curve with an identifiable local optimum.

**Evidence:** Experiment 2 (parameter sweep on IDRiD).

---

### SC-C: Cross-Device Robustness Evaluation

**Contribution:** Systematic evaluation of preprocessing pipeline robustness across four fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss) using five datasets with documented camera metadata, producing a cross-device performance matrix.

**Evidence:** Experiment 6 (V4) (device domain shift evaluation on RFMiD, DDR, ODIR-5K, IDRiD, Messidor).

---

### SC-D: Flat-Field Illumination Normalization

**Contribution:** Design and validation of a Gaussian blur subtraction stage (corrected = image − GaussianBlur(image, σ=45) + 128) for uneven illumination correction in fundus images, reducing device-dependent illumination gradients while preserving local vessel and lesion detail.

**Evidence:** Experiment 2 (component-level ablation, V4 Level 2: +flat-field correction). Image quality metrics (CNR, VVI, SSIM) measured before and after Stage 2.

**Novelty:** Flat-field correction is introduced as Stage 2 of the V4 pipeline. Unlike global intensity normalization, Gaussian blur subtraction corrects spatially non-uniform illumination (common in wide-field fundus cameras) without destroying the local contrast structure required for lesion detection.

---

### SC-E: Per-Patient Binocular Fusion

**Contribution:** Design and experimental evaluation of a per-patient binocular fusion model (PatientHead) that combines left-eye and right-eye feature vectors for patient-level DR classification, leveraging canonical flip (Stage 0) to standardize eye orientation as a prerequisite for meaningful bilateral feature comparison.

**Evidence:** Experiment 1, Configs E and F (V4) — PatientHead with ResNet-50 backbone (E) and EfficientNet-B3 backbone (F). Results reported as optional extension supplementing the core 2×2 factorial (A–D).

**Novelty:** The PatientHead architecture combines backbone features from bilateral image pairs via concatenation + element-wise absolute difference → MLP → 5-class logits. This exploits the bilateral symmetry of DR grading (where left and right eye DR severity is correlated but not identical) and enables patient-level rather than image-level inference. The canonical flip prerequisite (Stage 0) is a necessary condition for interpretable bilateral feature alignment.

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
| SC-D | PC-1, PC-8 |
| SC-E | PC-1 |

---

### SC-F: OD-Fovea Rotation Normalization (Stage 0b)

**Contribution:** Design and implementation of classical-CV-based optic disc (OD) and fovea detection for fundus image rotation normalization (Stage 0b). The optic disc is identified as the brightest region; the fovea is identified as the darkest region with a distance prior from the OD. The image is rotated so the OD→fovea axis is horizontal. When detection confidence is low, rotation is skipped (fallback). The rotation sigma for Stage 5 augmentation is adapted per-image from OD/fovea detection uncertainty (fallback: σ = 13.0°).

**Evidence:** Experiment 2 (component-level ablation, Stage 0b contribution isolated from Stage 0a). Implementation: `src/preprocessing/od_fovea_detect.py`, `src/preprocessing/canonical_orientation.py`.

**Novelty:** OD-fovea rotation normalization standardizes the retinal axis orientation across images from different cameras and acquisition angles, reducing orientation-induced distribution shift beyond what horizontal flip (Stage 0a) alone achieves. The adaptive rotation_sigma links anatomical detection confidence to augmentation intensity, providing principled uncertainty-aware augmentation.

---

## Boundary Conditions

All contributions are bounded by the scope constraints defined in INVARIANTS.md (Section IV: Scope Boundaries) and the non-claims listed in ARGUMENT_MAP.md (Section VII). In particular:

- Contributions do not extend to general retinal disease classification or imaging modalities other than fundus photography (SB-1.1, SB-1.4)
- Contributions do not constitute clinical device certification or regulatory compliance (NC-16)
- Contributions are bounded to the tested architectures and datasets as specified in the experimental protocol
