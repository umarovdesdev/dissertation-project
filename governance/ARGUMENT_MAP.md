# ARGUMENT MAP
## PhD Dissertation: Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Document Type:** Formal Claim-Evidence-Dependency Structure
**Binding Reference:** DISSERTATION_INVARIANTS.md v2.1

---

## I. MAIN THESIS NODE

**IT-1 (Verbatim from Invariants, Section I):**

> An integrated preprocessing-CNN pipeline — comprising FOV standardization, green channel imaging, pixel normalization, CLAHE enhancement (LAB color space, dynamic clip limit), and HSV contrast enhancement — applied to fundus images sourced from EyePACS (primary training), APTOS 2019 (robustness), IDRiD (clinical validation and lesion localization), Messidor/Messidor-2 (external generalization), and RFMiD/DDR/ODIR-5K (device domain shift), produces statistically measurable improvement in five-class diabetic retinopathy classification performance relative to a baseline CNN trained without preprocessing, under constrained computational conditions defined by hardware limitations operative during experimental execution.

**Scope boundary:**
- Five-stage DR classification (DR 0–4 per standard clinical grading).
- Dataset architecture: EyePACS (~88,000 labeled images, primary training), APTOS 2019 (robustness testing under image degradation), IDRiD (clinical validation with pixel-level lesion annotations), Messidor/Messidor-2 (external generalization), RFMiD/DDR/ODIR-5K (device domain shift evaluation across Topcon, Kowa, Canon, Zeiss camera hardware).
- "Improvement" = measurable difference in primary metrics (weighted F1-score, ROC-AUC, Cohen's Kappa, Accuracy) under matched experimental conditions.
- Scope extends to cross-database transferability evaluation (Messidor/Messidor-2, IDRiD), explainability via Grad-CAM with lesion mask comparison (IDRiD), device domain shift across camera hardware (RFMiD, DDR, ODIR-5K), and robustness testing under synthetic image degradation (APTOS 2019).
- Does not extend to: general retinal disease classification, other ophthalmological imaging modalities, imaging contexts not representable by the dataset architecture specified above.

---

## II. PRIMARY CLAIMS (Level 1)

---

### PC-1
**Claim ID:** PC-1
**Formal Statement:** The integrated 5-component preprocessing pipeline (FOV standardization → green channel imaging → normalization → CLAHE enhancement (LAB color space, dynamic clip limit) → HSV contrast enhancement) produces statistically measurable improvement in five-class DR classification performance relative to a baseline CNN trained on unprocessed fundus images (resize only) from EyePACS, independently for both ResNet-50 and EfficientNet-B3, on the metrics: weighted F1-score, ROC-AUC, Cohen's Kappa, and Accuracy.
**Claim Type:** Empirical
**Required Evidence Type:** 2×2 factorial ablation on EyePACS (Experiment 1); four configurations — (A) resize only + ResNet-50, (B) preprocessing + ResNet-50, (C) resize only + EfficientNet-B3, (D) preprocessing + EfficientNet-B3; 5-fold cross-validation with patient-level split; mixed-effects model. Preprocessing dominance validated if Performance(B) > Performance(A) AND Performance(D) > Performance(C) with EH-3 criteria satisfied independently for both architectures.
**Dependency:** None (foundational claim; corresponds to H-1)

---

### PC-2
**Claim ID:** PC-2
**Formal Statement:** The CLAHE clip limit parameter, varied across controlled values within the tested range on IDRiD, produces a parameter-dependent sensitivity profile in downstream CNN classification performance, with at least one identifiable local optimum within the tested range, particularly in per-class F1-score for DR 1 and DR 2 (microaneurysm and small vessel features). CLAHE is applied in LAB color space with dynamic clip limit.
**Claim Type:** Empirical
**Required Evidence Type:** Parameter sweep experiment; per-class F1-score across clip limit values; IDRiD as the CLAHE threshold sensitivity test dataset.
**Dependency:** Depends on PC-1 (CLAHE is a component of the pipeline validated in PC-1)

---

### PC-3
**Claim ID:** PC-3
**Formal Statement:** A two-stage fine-tuning protocol — (1) frozen EfficientNetB0 base with classification head training, followed by (2) progressive unfreezing of upper layers — applied under the preprocessing regime of PC-1, yields higher test-set Precision, Recall, F1-score, and Cohen's Kappa than the frozen-only strategy (Stage 1 alone), under the same dataset and hardware conditions.
**Claim Type:** Empirical
**Required Evidence Type:** Comparative experiment; matched preprocessing; EfficientNetB0 on APTOS 2019 + supplementary clinical images; metric values: Precision, Recall, F1, Macro Avg, Weighted Avg, Cohen's Kappa for both strategies.
**Dependency:** Depends on PC-1 (preprocessing regime must be active for this comparison)
**Note:** This claim is now replicated on EyePACS (in addition to prior APTOS 2019 self-publication results from LC-SAPAKOVA-2025 / LC-Yesmukhamedov-2025-SELF).

---

### PC-4
**Claim ID:** PC-4
**Formal Statement:** A coupled thermal-optical mathematical model of laser-fundus tissue interaction — comprising Beer's law for radiation attenuation, an energy balance equation, and the general heat conduction equation solved by finite difference methods — provides a theoretical computational grounding for the thermal effects of laser coagulation on retinal tissue layers (cornea, choroid, retina). This model provides qualitative support for diagnostic image feature interpretation in the context of laser-treated retinopathy. The model does not constitute an experimentally validated clinical model.
**Claim Type:** Theoretical
**Required Evidence Type:** Mathematical derivation; computational simulation results; qualitative heat map outputs for three tissue layers.
**Dependency:** None (independent theoretical contribution; does not condition PC-1, PC-2, or PC-3)

---

### PC-5
**Claim ID:** PC-5
**Formal Statement:** A modular, scalable AI-driven information system architecture — specifying components for image capture, preprocessing, inference, reporting, data management, PACS/EHR integration, and physician-in-the-loop decision support — constitutes a design specification for automated DR screening deployable in resource-limited environments. The architecture has not been prototype-implemented or field-tested. All stated deployment benefits are design specifications, not demonstrated outcomes.
**Claim Type:** System-level
**Required Evidence Type:** UML architecture diagrams; component specification; comparative analysis of existing DR screening systems; design feasibility framing for Kazakhstan healthcare context.
**Dependency:** Depends on PC-1 (the preprocessing-CNN pipeline validated in PC-1 constitutes the AI processing module of the architecture)

---

### PC-6
**Claim ID:** PC-6
**Formal Statement:** Models trained on EyePACS with the 5-component preprocessing pipeline generalize to Messidor, Messidor-2, and IDRiD without retraining, achieving generalization ratio G ≥ 0.85 per OD-4 (G = F1_external / F1_EyePACS).
**Claim Type:** Empirical
**Required Evidence Type:** Experiment 5 — cross-database transferability evaluation. Trained models (ResNet-50, EfficientNet-B3) applied to Messidor, Messidor-2, and IDRiD without retraining; generalization ratio G computed per external dataset.
**Dependency:** Depends on PC-1 (pipeline must be validated before transferability is tested)

---

### PC-7
**Claim ID:** PC-7
**Formal Statement:** Grad-CAM analysis on EfficientNet-B4 demonstrates that models trained with the 5-component preprocessing pipeline exhibit higher IoU between activation regions and IDRiD pixel-level lesion masks (microaneurysms, hemorrhages, hard exudates, soft exudates) than models trained with resize-only baseline.
**Claim Type:** Empirical
**Required Evidence Type:** Experiment 4 — Grad-CAM explainability analysis. IoU between Grad-CAM activation maps and IDRiD lesion masks computed per lesion type for preprocessing vs. baseline conditions on EfficientNet-B4.
**Dependency:** Depends on PC-1 (preprocessing pipeline validity) and PC-6 (cross-database generalization to IDRiD)

---

### PC-8
**Claim ID:** PC-8
**Formal Statement:** Component-level ablation of the 5-component pipeline identifies a ranked contribution hierarchy among FOV standardization, green channel imaging, normalization, CLAHE enhancement, and HSV contrast enhancement, measured by incremental weighted F1 improvement on EyePACS.
**Claim Type:** Empirical
**Required Evidence Type:** Experiment 2 — component-level ablation. Sequential addition/removal of individual pipeline components; weighted F1 measured at each ablation level (resize only → full pipeline) on EyePACS.
**Dependency:** Depends on PC-1 (full pipeline must be established before component-level ablation is meaningful)

---

### PC-9
**Claim ID:** PC-9
**Formal Statement:** Models trained on EyePACS with the 5-component preprocessing pipeline maintain classification performance across images from different fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss), as evaluated on RFMiD, DDR, ODIR-5K, IDRiD, and Messidor subsets grouped by camera model.
**Claim Type:** Empirical
**Required Evidence Type:** Experiment 6 — device domain shift evaluation. F1-score and ROC-AUC computed per camera group across RFMiD, DDR, ODIR-5K, IDRiD, and Messidor subsets.
**Dependency:** Depends on PC-1 (pipeline validity) and PC-6 (cross-database generalization established)

---

## III. SUB-CLAIMS (Level 2)

---

### SC-1.1
**Parent Claim:** PC-1
**Sub-Claim ID:** SC-1.1
**Formal Statement:** Fundus image preprocessing combining resizing to 512×512, pixel normalization to [0,1], CLAHE (clip limit 2.0, grid 8×8), and augmentation (horizontal/vertical flip, rotation ±15°, zoom ±10%, brightness variation) raises validation accuracy from 71% to 86% and classification accuracy from 88% to 91% relative to no-preprocessing baseline on the APTOS 2019 and supplementary clinical dataset.

**Evidence Reference:**
- Literature Card: LC-SAPAKOVA-2025-01, Extraction Block EB-LC-SAPAKOVA-2025-01-01
- Dissertation Section: §4.2 (Experiment 1: Baseline CNN vs. Enhanced CNN)
- Dataset: APTOS 2019 + supplementary clinical images (25,000 labeled images; 80/10/10 split)
- Metrics: Validation accuracy (71% → 86%); Classification accuracy (88% → 91%); Weighted F1 = 0.91; ROC-AUC = 0.9638 (LC-SAPAKOVA-2025-01, p. 84)

**Boundary Conditions:**
- Results are bounded to the APTOS 2019 image distribution and the specific pipeline parameters cited.
- Supplementary clinical dataset is not publicly available; reproducibility is structurally limited (SB-2.2).
- Hardware overheating constrained epoch count; full learning potential may not have been reached (LC-SAPAKOVA-2025-01, p. 86).
- Binary classification performance reported in Figs. 4–5 of LC-SAPAKOVA-2025-01; multiclass performance relationship requires explicit clarification in dissertation (LC-SAPAKOVA-2025-01, II.7 Assumption 3).

---

### SC-1.2
**Parent Claim:** PC-1
**Sub-Claim ID:** SC-1.2
**Formal Statement:** The enhanced four-block CNN (filters: 32–256, batch normalization, dropout 0.4, softmax 5-class, Adam lr=0.0001, categorical cross-entropy) achieves 94.5% training accuracy and 91.3% validation accuracy, converging within 35–40 epochs, with validation loss stabilizing at 0.18–0.20, compared to the baseline two-block CNN (32–64 filters, sigmoid, binary cross-entropy) stabilizing at validation loss 0.27–0.30.

**Evidence Reference:**
- Literature Card: LC-SAPAKOVA-2025-01, §II.5
- Dissertation Section: §4.2.1 (Training Dynamics and Convergence Analysis)
- Dataset: APTOS 2019 + supplementary clinical images
- Metrics: Training accuracy 94.5%; Validation accuracy 91.3% (Epoch 9: val_acc 93.41%, val_loss 0.1833 vs. baseline val_acc 91.71%, val_loss 0.2288) (LC-SAPAKOVA-2025-01, p. 86, Table 2)

**Boundary Conditions:**
- Results are bounded to the specific hyperparameter configuration documented (Adam, lr=0.0001, batch 32, dropout 0.4, early stopping).
- Hardware-specific computational constraints apply (DGL-2).
- Training accuracy significantly exceeds test accuracy on Method 1 in parallel EfficientNetB0 experiment; overfitting remains a documented risk (LC-SAPAKOVA-2025, p. 499; LC-Yesmukhamedov-2025-SELF, p. 119).

---

### SC-1.3
**Parent Claim:** PC-1
**Sub-Claim ID:** SC-1.3
**Formal Statement:** Preprocessing with CLAHE reduces per-step processing time relative to unprocessed input (1s 108ms/step with preprocessing vs. 8s 986ms/step without preprocessing), under the same hardware configuration.

**Evidence Reference:**
- Literature Card: LC-SAPAKOVA-2025-01, §II.5, p. 84
- Dissertation Section: §4.1.3 (Hardware Constraints and Computational Resource Limitations)
- Dataset: APTOS 2019 + supplementary clinical images
- Metric: Processing time per step

**Boundary Conditions:**
- Processing time difference is hardware-specific; does not generalize to different hardware configurations (DGL-2).
- This finding is a secondary metric (EH-2); it does not independently validate the preprocessing dominance hypothesis.

---

### SC-1.4
**Parent Claim:** PC-1
**Sub-Claim ID:** SC-1.4
**Formal Statement:** The APTOS 2019 dataset exhibits severe class imbalance (Class 0: 73.5% training / 49.3% test; Classes 3 and 4: 4.5% combined training / 13.3% combined test), which constitutes a primary confounding factor in the interpretation of accuracy-based performance claims and necessitates weighted F1-score and Cohen's Kappa as primary evaluation metrics.

**Evidence Reference:**
- Literature Card: LC-SAPAKOVA-2025, §II.3 (p. 498); LC-Yesmukhamedov-2025-SELF, §II.3; LC-SAPAKOVA-2025-01, §II.3
- Dissertation Section: §4.1.2 (Class Distribution Analysis)
- Dataset: APTOS 2019
- Metric: Class distribution (percentage per class, training and test partitions)

**Boundary Conditions:**
- Class imbalance figures are specific to the APTOS 2019 + supplementary clinical dataset split as documented in the cited sources.
- Per-class precision and recall for minority classes (DR 3, DR 4) are subject to instability under severe imbalance (EH-2).

---

### SC-2.1
**Parent Claim:** PC-2
**Sub-Claim ID:** SC-2.1
**Formal Statement:** The modified CLAHE formulation CLIP LIMIT = T/80, proposed in LC-AlTimemy-2021 as an upgrade to conventional CLAHE (CLIP LIMIT = ⌈L/T⌉ + β·(φ−⌈L/T⌉)), provides controllable adaptive contrast enhancement that addresses excessive enhancement artifacts and poor manifestation of small vessels and microaneurysm-like features in fundus images. This formulation was adapted and validated within the dissertation's preprocessing pipeline.

**Evidence Reference:**
- Literature Card: LC-AlTimemy-2021, §3 (Equation 2, p. 5); §4 (Conceptual Contributions)
- Dissertation Section: §3.1.2 (Modified CLAHE Algorithm with Simplified Threshold Control); §4.3 (Experiment 2: Modified CLAHE Threshold Optimization)
- Dataset: STARE (LC-AlTimemy-2021 context: 157 images, five-class taxonomy); APTOS 2019 (dissertation validation)
- Metric: Per-class F1-score for DR 1 and DR 2; classification accuracy

**Boundary Conditions:**
- CLAHE T/80 formulation was derived on STARE dataset with different image characteristics and different five-class taxonomy (BDR, CRVO, CNV, PDR, Normal ≠ DR 0–4). No parameter-level equivalence between STARE-optimized and APTOS-optimized parameters is asserted (DGL-5).
- The sensitivity formula in LC-AlTimemy-2021 (Eq. 3: Sen = TP/(TP+TN)) deviates from standard (TP/(TP+FN)); this anomaly must be noted if that source's sensitivity figure is cited (SIR-3).
- 100% accuracy reported in LC-AlTimemy-2021 is not transferable to the dissertation's APTOS 2019 framework (SB-1.2).
- CLAHE parameters must be independently validated within the dissertation's experimental framework (DGL-5).

---

### SC-2.2
**Parent Claim:** PC-2
**Sub-Claim ID:** SC-2.2
**Formal Statement:** Within the CLAHE clip limit range tested experimentally on the small fundus image dataset, downstream CNN classification performance on per-class F1-score for DR 1 and DR 2 exhibits a parameter-dependent sensitivity profile. The profile has at least one local optimum identifiable within the tested range. No extrapolation to untested parameter values is permissible.

**Evidence Reference:**
- Literature Card: LC-SAPAKOVA-2025-01, §II.3 (CLAHE parameters: clip limit 2.0, grid 8×8); LC-AlTimemy-2021, §3
- Dissertation Section: §4.3.1 (Threshold Parameter Sensitivity Analysis); §4.3.2 (Impact on Feature Preservation)
- Dataset: Small fundus image dataset (experiment-specific; bounded per Invariants H-2)
- Metric: Per-class F1-score, DR 1 and DR 2 classes

**Boundary Conditions:**
- Claim is bounded strictly to the parameter range tested experimentally (Invariants H-2).
- Extrapolation to clip limit values outside the tested range is forbidden (CFC-1.2).

---

### SC-3.1
**Parent Claim:** PC-3
**Sub-Claim ID:** SC-3.1
**Formal Statement:** EfficientNetB0 two-stage fine-tuning (Method 2: progressive unfreezing of upper layers) achieves test-set Precision = 0.75, Recall = 0.74, F1 = 0.74, Macro Average = 0.77, Weighted Average = 0.81, compared to frozen-only strategy (Method 1) achieving Precision = 0.65, Recall = 0.60, F1 = 0.62, Macro Average = 0.72, Weighted Average = 0.74, with Accuracy = 0.80 for both methods on the APTOS 2019 + supplementary clinical test partition.

**Evidence Reference:**
- Literature Card: LC-SAPAKOVA-2025, §II.5, p. 499, Table 3 (prior self-publication — must be cited as previously published results per SIR-4)
- Literature Card: LC-Yesmukhamedov-2025-SELF, §II.5 (identical experimental configuration — may not be cited as independent confirmation per SIR-5)
- Dissertation Section: §4.4.1 (EfficientNetB0: Frozen versus Progressive Fine-Tuning); §4.4.3
- Dataset: APTOS 2019 + supplementary clinical images (training: 35,126; test: 3,662)
- Metrics: Precision, Recall, F1-Score, Macro Average, Weighted Average (Test partition)

**Boundary Conditions:**
- These values are the published empirical baseline from prior self-publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF). Dissertation must replicate and extend, not simply reproduce.
- LC-SAPAKOVA-2025 and LC-Yesmukhamedov-2025-SELF share identical experimental data; they cannot be cited as independent confirmatory sources (SIR-5).
- Alternative architectures (ResNet, VGG, DenseNet) were not evaluated; results cannot be generalized to the class of efficient CNN architectures (SIR-7; SB-1.7).
- Method 1 (Frozen) exhibits overfitting: training F1 = 0.87 vs. test F1 = 0.62 (LC-SAPAKOVA-2025, p. 499, Tables 1–2).

---

### SC-3.2
**Parent Claim:** PC-3
**Sub-Claim ID:** SC-3.2
**Formal Statement:** ResNet50, under feature extraction strategy versus end-to-end fine-tuning, produces a performance differential on the APTOS 2019 test partition, evaluated on the same primary metric set (Accuracy, weighted F1, ROC-AUC, Cohen's Kappa).

**Evidence Reference:**
- Literature Card: LC-AlTimemy-2021, §3 (ResNet50 as transfer learning base on STARE; training parameters: 100 epochs, lr=0.0003, 262 min elapsed)
- Dissertation Section: §4.4.2 (ResNet50: Feature Extraction versus End-to-End Fine-Tuning)
- Dataset: APTOS 2019 (dissertation); STARE (LC-AlTimemy-2021 context — different taxonomy)
- Metric: Accuracy, weighted F1, ROC-AUC, Cohen's Kappa

**Boundary Conditions:**
- LC-AlTimemy-2021 results are on STARE with different five-class taxonomy; they cannot be directly compared to APTOS 2019 results without explicit acknowledgment of taxonomic non-equivalence (SB-2.3).
- ResNet50 results from dissertation experiments (§4.4.2) constitute the primary evidence; LC-AlTimemy-2021 provides only methodological precedent for ResNet50 use.

---

### SC-4.1
**Parent Claim:** PC-4
**Sub-Claim ID:** SC-4.1
**Formal Statement:** The heat conduction equation Coσ(x,y,z,T)∂T/∂t = div(k(x,y,z,T)·grad(T)), combined with Beer's law for laser intensity attenuation I(r,z) = I₀(r)e^(−∫₀ᶻβ(r,ξ)dξ) and a Gaussian beam intensity profile I₀(r) = (P/πa²)e^(−(r/a)²), provides a mathematical framework for numerically modeling temperature distribution across retinal tissue layers (cornea, choroid, retina) during laser coagulation. Surface layers (cornea) exhibit faster temperature rise than deeper layers (choroid, retina). Temperature stabilizes in deep layers after continued laser exposure.

**Evidence Reference:**
- Literature Card: LC-Sapakova-2024-01, §II.3 (Equations 2, 3, 4, 7, 8); §II.5
- Dissertation Section: §2.4.1 (Coupled Thermal-Optical Model of Fundus Tissue Response)
- Dataset: Simulation only (no clinical data; no APTOS 2019 involvement)
- Metric: Qualitative temperature distribution (heat maps; depth-time graphs); no quantitative temperature thresholds reported

**Boundary Conditions:**
- Results are computational simulation only. No quantitative validation against experimental or clinical data exists (LC-Sapakova-2024-01, §II.5; SIR-6).
- Model omits blood perfusion term despite Pennes bioheat equation reference in source introduction (LC-Sapakova-2024-01, §II.7 Assumption 4).
- Tissue optical and thermal properties treated as static during exposure; no temperature-dependent modification modeled (LC-Sapakova-2024-01, §II.7 Assumption 1).
- The claim that simulation "confirms effectiveness of laser therapy" is the source's claim; it is not absorbed into dissertation's validated findings (SIR-6; CFC-2.4).

---

### SC-5.1
**Parent Claim:** PC-5
**Sub-Claim ID:** SC-5.1
**Formal Statement:** A modular AI-driven diagnostic system architecture for ophthalmological screening — specifying components including Image Capture, Image Processing, Recognition Model, Diagnosis, Reporting, User Interface, Data Storage, Error Handling, and a Doctor-AI Feedback Loop — can be formally specified using UML component, sequence, class, activity, and ER diagrams. This specification addresses functional and non-functional requirements for deployment in resource-limited environments including PACS/EHR integration, telemedicine support, and physician-in-the-loop decision support.

**Evidence Reference:**
- Literature Card: LC-2025-Yesmukhamedov-01, §II.4 (UML diagrams; Fig. 1 p. 83; Fig. 4 p. 87; Fig. 5 p. 88; Tables 2–5)
- Dissertation Section: §6.1 (System Requirements); §6.2 (AI Processing Module Design); §6.3 (Clinical Workflow Integration); §6.4 (Data Security and Regulatory Compliance)
- Dataset: No experimental dataset; epidemiological statistics from IDF Diabetes Atlas 2021 (LC-2025-Yesmukhamedov-01, p. 86–87)
- Metric: Not applicable (design specification)

**Boundary Conditions:**
- System architecture is a design specification only. No prototype implementation or field testing has been conducted (SB-4.1; DGL-4).
- GDPR/HIPAA compliance framing is a design specification, not certified compliance status (SB-4.2).
- Infrastructure prerequisites for Kazakhstan deployment (equipment investment, algorithm adaptation, national standards, specialist training) acknowledged but not resolved (LC-2025-Yesmukhamedov-01, p. 90; DGL-4).
- Internet connectivity dependency noted for telemedicine components (LC-2025-Yesmukhamedov-01, Table 1, p. 81).

---

### SC-5.2
**Parent Claim:** PC-5
**Sub-Claim ID:** SC-5.2
**Formal Statement:** Existing commercial DR screening systems (IDx-DR, EyeNuk, DeepMind, Retina-AI Health, Visulytix Pegasus, ZEISS VISUHEALTH, NVIDIA Clara AI, Orbis Cybersight AI, Heidelberg AI Tools) exhibit identified limitations (data security dependencies, internet connectivity requirements, lack of adaptation to local datasets, infrastructure prerequisites) that the proposed system architecture design explicitly addresses in its specification.

**Evidence Reference:**
- Literature Card: LC-2025-Yesmukhamedov-01, §II.3 (comparative analysis, Table 1, pp. 80–81)
- Dissertation Section: §1.4 (Critical Analysis of Existing DR Screening Systems); §5.3 (Comparative Analysis with Existing DR Diagnostic Systems)
- Dataset: Published system specifications and peer-reviewed performance reports (external benchmarks; no direct controlled experiment)
- Metric: Qualitative comparative analysis; tabular decomposition

**Boundary Conditions:**
- The comparison is qualitative and based on published specifications, not a controlled experiment against named systems under identical evaluation conditions (CFC-2.2).
- Claims of superiority over existing systems without direct controlled comparison are forbidden (CFC-2.2).
- Published performance metrics of existing systems (e.g., IDx-DR sensitivity ≥ 96%) are cited as external benchmarks, not as validated results of this dissertation (LC-2025-Yesmukhamedov-01, §II.5).

---

### SC-6.1
**Parent Claim:** PC-6
**Sub-Claim ID:** SC-6.1
**Formal Statement:** Generalization ratio G = F1_external / F1_EyePACS is computed for models trained on EyePACS with the 5-component preprocessing pipeline and evaluated without retraining on Messidor, Messidor-2, and IDRiD. Specific G values on each external dataset constitute the primary evidence for PC-6.

**Evidence Reference:**
- Dissertation Section: Experiment 5 (Cross-Database Transferability)
- Dataset: EyePACS (training), Messidor, Messidor-2, IDRiD (external evaluation)
- Metrics: Weighted F1-score, ROC-AUC, generalization ratio G per external dataset
- Comparison benchmarks: Gulshan et al. 2016 AUC 0.990 (EyePACS/Messidor-2); Rakhlin 2018 AUC 0.967 (Kaggle DR); Saxena et al. AUC 0.92; Ting et al. 2017 AUC 0.936 (multi-ethnic)

**Boundary Conditions:**
- No retraining is performed on external datasets; results are bounded to the tested preprocessing configuration and trained model weights.
- Messidor uses a different grading scale (binary referable/non-referable); label harmonization methodology must be documented.
- G ≥ 0.85 is a pre-registered success criterion, not a guaranteed outcome (Invariants H-4).

---

### SC-7.1
**Parent Claim:** PC-7
**Sub-Claim ID:** SC-7.1
**Formal Statement:** IoU between Grad-CAM activation regions and IDRiD pixel-level lesion masks is computed per lesion type (microaneurysms, hemorrhages, hard exudates, soft exudates) for EfficientNet-B4 models trained with preprocessing vs. resize-only baseline. IoU(preprocessing) > IoU(baseline) constitutes the quantitative evidence for PC-7.

**Evidence Reference:**
- Dissertation Section: Experiment 4 (Grad-CAM Explainability Analysis)
- Dataset: IDRiD (pixel-level lesion annotations)
- Metrics: IoU per lesion type (microaneurysms, hemorrhages, hard exudates, soft exudates); attention consistency score

**Boundary Conditions:**
- IoU is an interpretability metric, not clinical localization — Grad-CAM activation does not constitute diagnostic delineation of lesion boundaries (NC-14).
- Results are bounded to EfficientNet-B4 architecture; generalization to other architectures (e.g., ResNet-50) is not asserted without additional experiments.

---

### SC-8.1
**Parent Claim:** PC-8
**Sub-Claim ID:** SC-8.1
**Formal Statement:** Component-level ablation produces weighted F1 measurements at each ablation level (resize only → FOV standardization → + green channel → + normalization → + CLAHE → + HSV contrast enhancement = full pipeline) on EyePACS, identifying a ranked contribution hierarchy among the five preprocessing components.

**Evidence Reference:**
- Dissertation Section: Experiment 2 (Component-Level Ablation)
- Dataset: EyePACS
- Metrics: Weighted F1-score at each ablation level; incremental F1 improvement per component addition

**Boundary Conditions:**
- The component hierarchy is bounded to the tested architectures (ResNet-50, EfficientNet-B3) and datasets (EyePACS) (NC-17).
- Component interactions may mean individual contributions are not strictly additive; the hierarchy reflects sequential addition ordering, not isolated effects.

---

### SC-9.1
**Parent Claim:** PC-9
**Sub-Claim ID:** SC-9.1
**Formal Statement:** Cross-camera performance is evaluated via F1-score and ROC-AUC per camera group (Canon, Topcon, Kowa, Zeiss) across RFMiD, DDR, ODIR-5K, IDRiD, and Messidor subsets, producing a cross-device performance matrix for models trained on EyePACS with the 5-component preprocessing pipeline.

**Evidence Reference:**
- Dissertation Section: Experiment 6 (Device Domain Shift Evaluation)
- Dataset: RFMiD (Topcon/Kowa), DDR (Canon/Topcon), ODIR-5K (Canon/Zeiss), IDRiD, Messidor — subsets grouped by camera model
- Metrics: F1-score, ROC-AUC per camera group; cross-device performance variance

**Boundary Conditions:**
- Device domain shift results do not constitute device certification or regulatory compliance (NC-16).
- Results are bounded to the specific camera models represented in the tested datasets (Invariants H-6).
- Camera-specific image characteristics beyond preprocessing scope (e.g., sensor noise profiles, optical characteristics) may remain unaddressed.

---

## IV. COUNTER-ARGUMENTS AND LIMITATIONS

---

### PC-1: Counter-Arguments and Limitations

**Counter-Argument CA-1.1:**
Claim: Preprocessing improvement may be confounded by simultaneous architectural change. In LC-SAPAKOVA-2025-01, preprocessing (pipeline activation) and architectural complexity increase (two-block → four-block CNN) are applied together in the enhanced condition. The isolated effect of preprocessing versus architectural complexity change is not independently measured.
Source: LC-SAPAKOVA-2025-01, §II.7 Assumption 3; dissertation §5.2 (ablation study required).
Condition of Failure: If ablation study (§5.2) demonstrates that architectural complexity alone accounts for performance gains, the preprocessing dominance claim weakens to conditional status.

**Counter-Argument CA-1.2:**
Claim: Test performance is evaluated on a non-public supplementary dataset that cannot be independently reproduced.
Source: LC-SAPAKOVA-2025-01, §II.6 Limitation 1; SB-2.2.
Condition of Failure: If results do not replicate on APTOS 2019 public partition alone, generalizability is structurally limited.

**Counter-Argument CA-1.3:**
Claim: Accuracy metric is subject to inflation under class imbalance (Class 0: 49.3%–73.5%); a classifier assigning all images to Class 0 could achieve ~49–73% accuracy without learning DR-relevant features.
Source: Invariants §V (EH-1); SB-2.1.
Condition of Failure: If weighted F1 and Cohen's Kappa do not satisfy EH-3 thresholds, accuracy-based claims do not constitute evidence of preprocessing dominance.

---

### PC-2: Counter-Arguments and Limitations

**Counter-Argument CA-2.1:**
Claim: The T/80 CLAHE formulation was derived on STARE (157 images, different disease taxonomy) and is not directly validated for APTOS 2019 five-class DR staging without independent parameter optimization.
Source: DGL-5; LC-AlTimemy-2021, §3.
Condition of Failure: If clip limit optimum on APTOS 2019 differs substantially from T/80 formulation, the source cannot be used as direct parameter justification.

**Counter-Argument CA-2.2:**
Claim: Sensitivity formula anomaly in LC-AlTimemy-2021 (Sen = TP/(TP+TN) vs. standard TP/(TP+FN)) may undermine the credibility of that source's 100% accuracy/sensitivity claims.
Source: LC-AlTimemy-2021, Eq. 3, p. 9; SIR-3.
Condition of Failure: If the 100% accuracy claim is methodologically flawed due to metric formula error, the source's empirical results cannot be cited as evidence of CLAHE effectiveness.

---

### PC-3: Counter-Arguments and Limitations

**Counter-Argument CA-3.1:**
Claim: LC-SAPAKOVA-2025 and LC-Yesmukhamedov-2025-SELF share identical experimental data (same training set 35,126; same test set 3,662; same APTOS 2019 + supplementary clinical data). They cannot serve as independent confirmatory sources for H-3. Independent replication within the dissertation's own experiments is required.
Source: SIR-5; Invariants §V (EH-4).
Condition of Failure: If dissertation experiments do not replicate the fine-tuning performance differential in §4.4.1, H-3 lacks independent validation.

**Counter-Argument CA-3.2:**
Claim: EfficientNetB0 results cannot be generalized to the class of efficient CNN architectures; alternative architectures (ResNet, VGG, DenseNet) were not evaluated in the referenced publications.
Source: SIR-7; LC-SAPAKOVA-2025, §II.6; SB-1.7.
Condition of Failure: Claim fails as a general statement; it holds only as architecture-specific and is so bounded.

**Counter-Argument CA-3.3:**
Claim: Observed overfitting in Method 1 (Frozen) — training F1 = 0.87 vs. test F1 = 0.62 — exceeds the 15 pp overfitting threshold defined in OD-4. This indicates the frozen strategy is inadequate for this task but does not independently establish that progressive fine-tuning fully resolves the generalization deficit.
Source: LC-SAPAKOVA-2025, p. 499; Invariants OD-4.
Condition of Failure: If fine-tuning (Method 2) also exhibits training-test gap exceeding 15 pp on any primary metric, overfitting concern extends to Method 2.

---

### PC-4: Counter-Arguments and Limitations

**Counter-Argument CA-4.1:**
Claim: The mathematical model lacks quantitative experimental validation against physical or clinical data. Temperature distribution results are qualitative only; no numerical thresholds, error margins, or calibration against measured tissue temperatures are reported.
Source: LC-Sapakova-2024-01, §II.5; §II.6; SIR-6.
Condition of Failure: This claim fails as an empirical or clinical contribution. It is bounded to its status as a theoretical/computational contribution.

**Counter-Argument CA-4.2:**
Claim: The model omits blood perfusion (Pennes bioheat term), despite its relevance to retinal tissue thermal dynamics, and uses static tissue optical properties despite coagulation-induced property changes during laser exposure.
Source: LC-Sapakova-2024-01, §II.7 Assumptions 1, 4.
Condition of Failure: Model predictions may deviate significantly from physical reality in vivo; the dissertation must restrict its use of this model to "theoretical/computational grounding" (SIR-6).

---

### PC-5: Counter-Arguments and Limitations

**Counter-Argument CA-5.1:**
Claim: The system architecture has not been prototype-implemented or field-tested. All stated benefits (diagnostic accuracy improvement, telemedicine reach, cost reduction) are design-level projections, not demonstrated results.
Source: SB-4.1; DGL-4; LC-2025-Yesmukhamedov-01, §II.7.
Condition of Failure: Any claim framing the architecture as a demonstrated system, as a clinically validated tool, or as an infrastructure with certified compliance fails per CFC-2.3, CFC-2.4, SB-4.2.

**Counter-Argument CA-5.2:**
Claim: The projected deployment outcomes for Kazakhstan (4+ million rural residents accessed; 20–30% late-stage DR complication reduction; 15–20% cost reduction) are third-party projections cited by LC-2025-Yesmukhamedov-01, not results of this dissertation. They cannot be attributed to dissertation findings.
Source: SIR-8; SB-1.6; CFC-2.3; LC-2025-Yesmukhamedov-01, p. 88.
Condition of Failure: Attribution of these figures to dissertation findings constitutes a forbidden claim type (CFC-2.3).

---

### PC-6: Counter-Arguments and Limitations

**Counter-Argument CA-6.1:**
Claim: Distribution shift between EyePACS and external datasets (Messidor, Messidor-2, IDRiD) — arising from differences in imaging equipment, patient demographics, grading protocols, and image quality — may degrade performance beyond the G ≥ 0.85 threshold.
Source: SB-2.3; Invariants H-4.
Condition of Failure: If G < 0.85 on any external dataset, the transferability claim for that dataset is not supported. If G < 0.85 on all external datasets, PC-6 fails.

**Counter-Argument CA-6.2:**
Claim: Messidor uses a different grading scale — binary referable/non-referable — requiring label harmonization. The harmonization procedure introduces methodological complexity and potential label mapping errors that may affect generalization ratio computation.
Source: Messidor dataset documentation; Invariants H-4 scope.
Condition of Failure: If label harmonization methodology is not transparently documented and justified, generalization ratio on Messidor is not interpretable.

---

### PC-7: Counter-Arguments and Limitations

**Counter-Argument CA-7.1:**
Claim: Grad-CAM is architecture-dependent — activation maps are computed from the final convolutional layer of the specific architecture. Results on EfficientNet-B4 may not generalize to ResNet-50 or other architectures with different feature hierarchies and receptive field sizes.
Source: Grad-CAM methodology constraints; Invariants H-5 scope.
Condition of Failure: If IoU patterns differ substantially across architectures, the explainability claim is bounded to EfficientNet-B4 only.

**Counter-Argument CA-7.2:**
Claim: IoU with lesion masks measures spatial overlap between activation regions and annotated lesion areas, not causal feature importance. High IoU indicates co-localization, not that the model uses lesion features causally for classification.
Source: NC-14; Grad-CAM interpretability limitations.
Condition of Failure: IoU evidence supports an interpretability claim only; it cannot establish that preprocessing causally directs model attention to lesion regions in a mechanistic sense.

---

### PC-8: Counter-Arguments and Limitations

**Counter-Argument CA-8.1:**
Claim: Component interactions may mean individual contributions are not additive — removing one component may affect others non-linearly. Sequential ablation measures the contribution of each component conditional on the presence of all preceding components, not its isolated effect.
Source: Experiment 2 methodology constraints; ablation design limitations.
Condition of Failure: If component ordering significantly affects the measured hierarchy (i.e., different ablation orderings produce different rankings), the identified hierarchy is ordering-dependent, not intrinsic.

---

### PC-9: Counter-Arguments and Limitations

**Counter-Argument CA-9.1:**
Claim: Camera-specific image characteristics beyond preprocessing scope — such as sensor noise profiles, optical characteristics, dynamic range, and color response — may remain unaddressed by the 5-component preprocessing pipeline. Performance variability across camera groups may reflect residual device-specific artifacts not corrected by preprocessing.
Source: Invariants H-6 scope; SB-1.8.
Condition of Failure: If performance variance across camera groups exceeds acceptable bounds despite preprocessing, the pipeline's device-domain robustness claim is weakened.

---

## V. CLAIM DEPENDENCY STRUCTURE

```
IT-1 (Main Thesis)
├── PC-1 [Empirical — Preprocessing Dominance]          ← No upstream dependency
│   ├── SC-1.1 [Accuracy and F1 improvement evidence]
│   ├── SC-1.2 [Convergence and loss dynamics]
│   ├── SC-1.3 [Processing time — secondary metric only]
│   └── SC-1.4 [Class imbalance — interpretive framing]
│
├── PC-2 [Empirical — CLAHE Threshold Sensitivity]      ← Depends on PC-1
│   ├── SC-2.1 [T/80 formulation — theoretical adaptation]
│   └── SC-2.2 [Sensitivity profile — experimental result]
│
├── PC-3 [Empirical — Two-Stage Fine-Tuning]            ← Depends on PC-1
│   ├── SC-3.1 [EfficientNetB0 Frozen vs. Fine-Tuned metrics]
│   └── SC-3.2 [ResNet50 comparison — additional architecture]
│
├── PC-4 [Theoretical — Laser-Tissue Model]             ← Independent (no empirical dependency)
│   └── SC-4.1 [Thermal-optical equations; simulation results]
│
├── PC-5 [System-level — DR Screening Architecture]     ← Depends on PC-1
│   ├── SC-5.1 [Architecture specification and UML diagrams]
│   └── SC-5.2 [Comparative analysis of existing systems]
│
├── PC-6 [Empirical — Cross-Database Transferability]   ← Depends on PC-1
│   └── SC-6.1 [Generalization ratio evidence on Messidor, Messidor-2, IDRiD]
│
├── PC-7 [Empirical — Explainability via Grad-CAM]      ← Depends on PC-1, PC-6
│   └── SC-7.1 [IoU quantitative evidence per lesion type on IDRiD]
│
├── PC-8 [Empirical — Preprocessing Component Hierarchy] ← Depends on PC-1
│   └── SC-8.1 [Component ablation F1 results at each level]
│
└── PC-9 [Empirical — Device Domain Shift Robustness]   ← Depends on PC-1, PC-6
    └── SC-9.1 [Cross-camera performance matrix per camera group]
```

**Dependency Rules:**
- PC-3 requires PC-1 to be validated: the two-stage fine-tuning protocol operates under the preprocessing regime established in PC-1. If PC-1 fails, PC-3 cannot be evaluated under the same conditions.
- PC-2 requires PC-1 to be validated: CLAHE is embedded in the pipeline of PC-1; parameter sensitivity testing presupposes the pipeline's demonstrated effectiveness.
- PC-5 requires PC-1 for its AI processing module justification. If PC-1 fails, the architecture's core preprocessing-CNN module lacks experimental grounding.
- PC-4 is independent of PC-1, PC-2, PC-3, PC-5. Its failure or success does not condition any other primary claim.
- PC-6 requires PC-1: cross-database transferability is only meaningful if the pipeline has been validated on the primary dataset (EyePACS).
- PC-7 requires PC-1 (pipeline validity) and PC-6 (cross-database generalization to IDRiD, which supplies the lesion masks for IoU computation).
- PC-8 requires PC-1: component-level ablation presupposes an established full pipeline whose components can be systematically removed.
- PC-9 requires PC-1 (pipeline validity) and PC-6 (cross-database generalization framework for evaluation on external datasets grouped by camera model).
- EH-4 (Sufficient Validation Criterion) requires PC-1 to be satisfied on EyePACS AND confirmed in direction of effect on at least one external dataset (Messidor-2 or IDRiD) AND replicated across both architectures in the factorial design (ResNet-50 and EfficientNet-B3). PC-3 contributes additional architecture replication evidence. PC-6 contributes the cross-database confirmation required by EH-4.

---

## VI. CLAIM STRENGTH CLASSIFICATION

---

### PC-1 — Preprocessing Dominance
**Strength: MODERATE**
**Justification:**
- Direct experimental evidence exists (LC-SAPAKOVA-2025-01): validation accuracy 71% → 86%; classification accuracy 88% → 91%; ROC-AUC = 0.9638; Weighted F1 = 0.91.
- Evidence satisfies EH-3 criteria direction (weighted F1 Δ ≥ 5 pp; ROC-AUC ≥ 0.9638) on the dataset tested.
- Strength is MODERATE rather than STRONG because: (a) preprocessing and architectural complexity change are confounded in the existing source (SC-1.1 boundary); (b) supplementary clinical dataset is non-public (SB-2.2); (c) ablation study isolating preprocessing from architectural change is required for Strong classification and is not yet documented in a separate independent source; (d) binary vs. five-class classification ambiguity exists in LC-SAPAKOVA-2025-01 reporting (SC-1.1 boundary).
- Promotion to STRONG requires: Experiment 1 ablation on EyePACS with 2×2 factorial design (ResNet-50 + EfficientNet-B3), satisfying EH-3 independently for both architectures, with 5-fold cross-validation and mixed-effects model.

---

### PC-2 — CLAHE Threshold Sensitivity
**Strength: CONDITIONAL**
**Justification:**
- The T/80 formulation is established in LC-AlTimemy-2021 on STARE; however, metric formula anomaly in that source (Sen = TP/(TP+TN)) weakens confidence in its 100% performance claims.
- CLAHE parameters (clip limit 2.0, grid 8×8) are documented in LC-SAPAKOVA-2025-01 as producing improved classification, but no explicit parameter sweep across clip limit values is documented in the available literature cards.
- Dissertation §4.3 is the primary evidence source for SC-2.2. Until those experimental results are produced and validated within the dissertation, claim strength is CONDITIONAL on experimental execution.
- Claim fails if no identifiable optimum is found within the tested range, per H-2 falsification requirement (Invariants VCR-3).

---

### PC-3 — Two-Stage Fine-Tuning
**Strength: MODERATE**
**Justification:**
- Direct empirical evidence exists in prior self-publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF): Method 2 Precision = 0.75, Recall = 0.74, F1 = 0.74 vs. Method 1 Precision = 0.65, Recall = 0.60, F1 = 0.62. Differential is substantial (+10 pp Precision, +14 pp Recall, +12 pp F1).
- Strength is MODERATE rather than STRONG because: (a) the two sources are not independent (identical experimental data; SIR-5); (b) independent replication within the dissertation's own experiments has not been documented in a separate literature card; (c) the claim is architecture-specific (EfficientNetB0 only; SIR-7); (d) supplementary clinical data non-reproducibility (SB-2.2).
- Promotion to STRONG requires: independent replication in dissertation §4.4 experiments on APTOS 2019 public partition, with explicit extension beyond prior self-publication results.

---

### PC-4 — Laser-Tissue Mathematical Model
**Strength: CONDITIONAL**
**Justification:**
- The mathematical equations are standard (Beer's law, heat conduction, Gaussian beam) applied to fundus tissue layers; they are not contested as formulations.
- The claim is bounded to theoretical/computational grounding status per SIR-6 and SB-1.5.
- CONDITIONAL: valid as a theoretical claim within its bounded scope (computational simulation; qualitative results). Fails if claimed as empirically or clinically validated (CFC-2.4; SIR-6).
- No quantitative validation data exists; this constraint is permanent under current evidence.

---

### PC-5 — System Architecture
**Strength: CONDITIONAL**
**Justification:**
- The architecture design is formally specified in LC-2025-Yesmukhamedov-01 with UML diagrams, component specifications, and comparative analysis. As a design claim, it is well-documented.
- CONDITIONAL: valid as a design/conceptual claim only. Fails if asserted as a deployed, prototype-validated, or clinically tested system (SB-4.1; DGL-4).
- Infrastructure prerequisites for Kazakhstan deployment (investment, algorithm adaptation, standards) constitute acknowledged unresolved preconditions (LC-2025-Yesmukhamedov-01, p. 90).

---

### PC-6 — Cross-Database Transferability
**Strength: CONDITIONAL**
**Justification:**
- No experimental results yet available; claim is pending Experiment 5 execution.
- CONDITIONAL: promotion to MODERATE requires G ≥ 0.85 on at least 2 of 3 external datasets (Messidor, Messidor-2, IDRiD) with documented label harmonization methodology for Messidor.
- Claim fails if G < 0.85 on all tested external datasets (Invariants VCR-3 applied to H-4).

---

### PC-7 — Explainability (Grad-CAM)
**Strength: CONDITIONAL**
**Justification:**
- No experimental results yet available; claim is pending Experiment 4 execution.
- CONDITIONAL: promotion to MODERATE requires IoU(preprocessing) > IoU(baseline) with statistical significance (e.g., paired test across IDRiD images) for at least 3 of 4 lesion types.
- Results are bounded to EfficientNet-B4 architecture; IoU is an interpretability metric, not clinical localization (NC-14).

---

### PC-8 — Preprocessing Component Hierarchy
**Strength: CONDITIONAL**
**Justification:**
- No experimental results yet available; claim is pending Experiment 2 execution.
- CONDITIONAL: promotion to MODERATE requires an identifiable contribution ranking with consistent ordering across cross-validation folds.
- The hierarchy is bounded to tested architectures and datasets (NC-17); non-additivity of component interactions (CA-8.1) may limit interpretability of the ranking.

---

### PC-9 — Device Domain Shift Robustness
**Strength: CONDITIONAL**
**Justification:**
- No experimental results yet available; claim is pending Experiment 6 execution.
- CONDITIONAL: promotion to MODERATE requires performance variance across camera groups below a defined threshold (to be specified in Experiment 6 protocol).
- Device domain shift results do not constitute device certification (NC-16); camera-specific characteristics beyond preprocessing scope may remain unaddressed (CA-9.1).

---

## VII. NON-CLAIMS (Explicitly Not Argued)

The following propositions are intentionally excluded from the dissertation's argumentation. These are not claims of the dissertation. They are listed here to enforce epistemic boundary compliance.

**NC-1.** The proposed preprocessing pipeline is effective for all fundus image datasets.
*(Forbidden per CFC-2.1; DGL-1)*

**NC-2.** The proposed pipeline outperforms existing commercial DR diagnostic systems (IDx-DR, EyeNuk, DeepMind, etc.) under identical evaluation conditions.
*(Forbidden per CFC-2.2: no controlled experiment against named systems under identical conditions is documented)*

**NC-3.** The system reduces late-stage DR complications by 20–30% in Kazakhstan, or reduces healthcare costs by 15–20%.
*(Forbidden per CFC-2.3; SIR-8; SB-1.6: these are third-party projections cited by LC-2025-Yesmukhamedov-01, p. 88)*

**NC-4.** The system achieves clinical-grade diagnostic accuracy.
*(Forbidden per CFC-2.4: no clinical validation trial is documented in any literature card)*

**NC-5.** The preprocessing pipeline achieves 100% accuracy on DR classification.
*(Forbidden per CFC-2.5; SB-1.2: the 100% accuracy in LC-AlTimemy-2021 is on a different dataset, different taxonomy, and potentially affected by metric formula anomaly)*

**NC-6.** EfficientNetB0 represents the globally optimal or generally superior architecture for DR classification.
*(Forbidden per SIR-7; SB-1.7: alternative architectures were not comparatively evaluated)*

**NC-7.** The laser-tissue interaction mathematical model (Chapter 2, §2.4) constitutes an experimentally or clinically validated model.
*(Forbidden per SB-1.5; SIR-6)*

**NC-8.** The system architecture (Chapter 6) has been prototype-implemented or field-tested in Kazakhstan healthcare settings.
*(Forbidden per SB-4.1; SB-4.3; DGL-4)*

**NC-9.** GDPR/HIPAA compliance has been certified for the proposed system.
*(Forbidden per SB-4.2: compliance framing is a design specification only)*

**NC-10.** CLAHE parameters optimized in this dissertation are portable to other fundus image datasets or imaging devices without independent validation.
*(Forbidden per DGL-5)*

**NC-11.** Results generalize to imaging modalities other than fundus photography (OCT, fluorescein angiography, etc.).
*(Forbidden per SB-1.4)*

**NC-12.** The proposed system performs equivalently across specific demographic subgroups (ethnic, age-stratified, comorbidity-defined populations).
*(Forbidden per DGL-3)*

**NC-13.** LC-SAPAKOVA-2025 and LC-Yesmukhamedov-2025-SELF constitute independent confirmatory evidence of any shared claim.
*(Forbidden per SIR-5: sources share identical experimental data)*

**NC-14.** Grad-CAM activation does not constitute clinical localization of pathology — it is an interpretability tool, not a diagnostic output. Grad-CAM overlays indicate regions of high gradient-weighted activation in the final convolutional layer and do not represent pixel-level diagnostic delineation of lesion boundaries.
*(Forbidden per SB-1.11; Invariants H-5 scope)*

**NC-15.** The dirty data pipeline (External Image Ingestion Protocol) is not validated for arbitrary clinical data sources — validation is bounded to specific Kazakh medical center data processed. Generalization of the ingestion protocol to other clinical data sources requires independent validation.
*(Forbidden per Invariants scope boundaries)*

**NC-16.** Device domain shift results do not constitute device certification or regulatory compliance — they are empirical observations of cross-device performance variability. No claim of device-agnostic deployment readiness is permissible based on Experiment 6 alone.
*(Forbidden per SB-1.8; Invariants H-6 scope)*

**NC-17.** The preprocessing component ablation does not identify a universally optimal preprocessing configuration — the component hierarchy is bounded to the tested architectures (ResNet-50, EfficientNet-B3) and datasets (EyePACS). Extension to other architectures or datasets requires independent experimental validation.
*(Forbidden per Invariants Experiment 2 scope)*

---

*End of Argument_Map*
*Document version: 2.1. Supersedes v1.0.*
*Document bound to: DISSERTATION_INVARIANTS.md v2.1*
*All claims traceable to: LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-AlTimemy-2021, LC-SAPAKOVA-2025-01, LC-2025-Yesmukhamedov-01, and Experiments 1–6 as specified in the v2.1 Dissertation Project.*
