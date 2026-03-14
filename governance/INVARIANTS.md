# DISSERTATION INVARIANTS DOCUMENT
## Immutable Epistemic Structure for Doctoral Research

**Research Domain:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S.  
**Document Status:** Binding constraint system — supersedes informal claim formulations across all dissertation chapters.  
**Document Version:** 3.0. Supersedes v2.2. V3 changes: experiments consolidated from 7 to 4; H-3 (Two-Stage Fine-Tuning) dropped; old Exp 3 (robustness to synthetic degradation) dropped; old Exp 5+6 merged into new Exp 3 (Cross-Dataset Generalization and Device Domain Shift); "dynamic clip limit" → "optimized clip limit" throughout; EyePACS size corrected to ~35,126 labeled (Kaggle partition); APTOS 2019 robustness role removed; SC-1.3 removed from ARGUMENT_MAP; ALO formalized as primary metric in H-5.

---

## I. CENTRAL THESIS (Immutable Formulation)

**IT-1.** An integrated preprocessing-CNN pipeline — comprising FOV standardization, green channel imaging, pixel normalization, CLAHE enhancement (LAB color space, optimized clip limit), and HSV contrast enhancement — applied to fundus images sourced from EyePACS (primary training), IDRiD (clinical validation, lesion localization, and CLAHE parameter sweep), Messidor/Messidor-2 (external generalization), and RFMiD/DDR/ODIR-5K (device domain shift), produces statistically measurable improvement in five-class diabetic retinopathy classification performance relative to a baseline CNN trained without preprocessing, under constrained computational conditions defined by hardware limitations operative during experimental execution.

**Scope boundary embedded in IT-1:**
- The thesis is bounded to five-stage DR classification (DR 0–4 per standard clinical grading).
- The thesis does not extend to general retinal disease classification, to other ophthalmological imaging modalities, or to imaging contexts not representable by the dataset architecture specified above (EyePACS, IDRiD, Messidor/Messidor-2, RFMiD, DDR, ODIR-5K).
- "Improvement" is defined exclusively as measurable difference in primary metrics (see Section V) computed across matched experimental conditions.
- The V3 dataset architecture enables evaluation of cross-database transferability (Messidor/Messidor-2, IDRiD), CLAHE parameter optimization (IDRiD), explainability via Grad-CAM with lesion mask comparison (IDRiD), and device domain shift across camera hardware (RFMiD, DDR, ODIR-5K).
- [V3 NOTE: Robustness to synthetic image degradation (APTOS 2019) was tested in the old Experiment 3, which has been dropped from V3 scope. APTOS 2019 is no longer an active experimental dataset.]

---

## II. CORE HYPOTHESES (Operational Form)

### Central Unifying Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. Hypotheses H-1 through H-6 are decompositions of this central hypothesis, each testing a specific aspect of the overarching claim.

---

**H-1 (Primary — Preprocessing Dominance):**

*If* fundus images from EyePACS are processed through the 5-component preprocessing pipeline comprising FOV standardization, green channel imaging, normalization, CLAHE enhancement (LAB color space, optimized clip limit), and HSV contrast enhancement,  
*and* a CNN classifier (ResNet-50 or EfficientNet-B3, pre-trained on ImageNet, adapted via fine-tuning) is trained on the processed images under a 2×2 factorial design,  
*then* classification accuracy, F1-score, and ROC-AUC will exceed those of the same architecture trained on unprocessed images (resize only) of equivalent source distribution, independently for both ResNet-50 and EfficientNet-B3.

- **Independent variable:** Presence vs. absence of the preprocessing pipeline (resize only vs. resize + proposed preprocessing).
- **Dependent variables:** Accuracy, F1-score (macro and weighted), ROC-AUC, Cohen's Kappa (quadratic weights), precision, recall — computed on the held-out test partition.
- **Control conditions:** Same dataset, same data partition strategy (5-fold cross-validation with patient-level split), same computational hardware, same training epoch budget.
- **Factorial design:** Four configurations — (A) resize only + ResNet-50, (B) preprocessing + ResNet-50, (C) resize only + EfficientNet-B3, (D) preprocessing + EfficientNet-B3. Preprocessing Dominance validated if Performance(B) > Performance(A) and Performance(D) > Performance(C) with EH-3 criteria satisfied independently for both architectures.

---

**H-2 (Secondary — CLAHE Threshold Sensitivity):**

*If* the clip limit parameter of CLAHE is varied across controlled values on a small fundus image dataset,  
*then* classification performance of the downstream CNN will exhibit a parameter-dependent sensitivity profile, identifiable as a non-trivial sensitivity curve with at least one local optimum within the tested range.

- **Independent variable:** CLAHE clip limit value.
- **Dependent variables:** Per-class F1-score for DR stages with smallest lesion features (microaneurysms, small vessels — predominantly DR 1 and DR 2 classes).
- **Scope:** Bounded to the parameter range tested experimentally. No extrapolation to untested parameter values is permissible.

---

<!-- DROPPED V3: H-3 (Secondary — Two-Stage Fine-Tuning) -->

### DROPPED (V3): H-3 — Two-Stage Fine-Tuning

> **V3 Status:** DROPPED. H-3 is not tested in any V3 experiment. The two-stage fine-tuning protocol is retained as a training strategy but is not an independent hypothesis. Historical text preserved for audit trail.

**H-3 (Secondary — Two-Stage Fine-Tuning) [DROPPED V3]:**

*If* EfficientNetB0 (pre-trained on ImageNet) is adapted using a two-stage protocol — (1) frozen base layers with classification head training, followed by (2) progressive unfreezing of upper layers — under the same preprocessing regime,
*then* test-set precision, recall, F1-score, and Cohen's Kappa will exceed those obtained from the frozen-only strategy (Stage 1 alone).

- **Independent variable:** Frozen-only vs. progressive fine-tuning adaptation strategy.
- **Dependent variables:** Precision (Test), Recall (Test), F1-Score (Test), Macro Average, Weighted Average, Cohen's Kappa.
- **Empirical reference values:** Frozen method — Precision 0.65, Recall 0.60, F1 0.62; Fine-tuned method — Precision 0.75, Recall 0.74, F1 0.74 (LC-SAPAKOVA-2025 / LC-Yesmukhamedov-2025-SELF). These values constitute the published empirical baseline for this hypothesis and must be cited as prior self-publications.

<!-- END DROPPED V3: H-3 -->

---

**H-4 (Secondary — Cross-Database Transferability):**

*If* a CNN model trained on EyePACS with the full preprocessing pipeline is applied without retraining to Messidor-2 and IDRiD,  
*then* the generalization ratio G = F1_external / F1_EyePACS will satisfy G ≥ 0.85 on both external datasets.

- **Independent variable:** Dataset (EyePACS training vs. Messidor-2 / IDRiD external evaluation).
- **Dependent variables:** Accuracy, Weighted F1-score, ROC-AUC, generalization ratio G (per OD-4).
- **Scope:** No retraining is performed on external datasets. Results are bounded to the specific architectures and preprocessing configurations tested. The G ≥ 0.85 threshold is a pre-registered success criterion, not a guaranteed outcome.

---

**H-5 (Secondary — Explainability):**

*If* Grad-CAM activation maps are computed for a CNN (EfficientNet-B4) processing fundus images with vs. without preprocessing,
*then* the Attention–Lesion Overlap (ALO) between Grad-CAM activation regions and pixel-level lesion masks from the IDRiD dataset will satisfy ALO_preproc > ALO_baseline, demonstrating that preprocessing directs model attention toward clinically relevant structures. ALO is defined as ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask) and serves as the primary explainability metric. IoU is retained as a secondary metric: IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask), with IoU_preproc > IoU_baseline as the secondary condition.

- **Independent variable:** Presence vs. absence of the preprocessing pipeline.
- **Dependent variables:** ALO between Grad-CAM activations and IDRiD lesion masks, per lesion type (primary); IoU between Grad-CAM activations and IDRiD lesion masks, per lesion type (secondary).
- **Scope:** Bounded to IDRiD images with available pixel-level lesion annotations. Grad-CAM activation does not constitute clinical localization of pathology (see NC-14). Results are bounded to EfficientNet-B4 architecture.

---

**H-6 (Secondary — Device Robustness):**

*If* a CNN model trained on EyePACS with the full preprocessing pipeline is evaluated on fundus images from datasets captured by different camera hardware (RFMiD: Topcon/Kowa; DDR: Canon/Topcon; ODIR-5K: Canon/Zeiss),  
*then* classification performance will be maintained across camera domains, with cross-device performance variance remaining within acceptable bounds relative to in-domain performance. Preprocessing standardizes retinal image appearance and reduces distribution differences between camera devices, leading to improved cross-device generalization.

- **Independent variable:** Camera/device domain (grouped by camera model across RFMiD, DDR, ODIR-5K).
- **Dependent variables:** Accuracy, F1-score, ROC-AUC per camera group.
- **Scope:** Results are bounded to the specific camera models represented in the tested datasets. Device domain shift results do not constitute device certification or regulatory compliance (see NC-16).

---

## III. OPERATIONAL DEFINITIONS

**OD-1: Image Quality**  
Image quality is operationally defined as the measurable capacity of a fundus image to support automated detection of microvascular features relevant to DR staging. Image quality is assessed through downstream classification performance metrics (accuracy, F1-score, ROC-AUC) computed on the same classifier architecture under identical training conditions with varying preprocessing states (absent vs. applied). No standalone subjective image quality score is used as the primary quality measure. An image quality condition is considered degraded if baseline CNN accuracy on unprocessed images falls below the enhanced CNN accuracy by a statistically interpretable margin under matched conditions.

**OD-2: Architectural Complexity**  
Architectural complexity is operationally defined by the number of convolutional layers, total trainable parameter count, filter size range, and presence or absence of regularization components (batch normalization, dropout). The baseline architecture (two convolutional blocks, 32–64 filters, no batch normalization, no dropout, sigmoid output) constitutes the low-complexity reference. The enhanced architecture (four convolutional blocks, 32–256 filters, batch normalization, dropout rate 0.4, softmax 5-class output) constitutes the high-complexity reference. Architectures outside these bounds are not evaluated within this dissertation.

**OD-3: Preprocessing Pipeline**
The preprocessing pipeline is the ordered sequence of image transformation operations applied prior to CNN input, comprising five components: (1) FOV standardization — fundus circle detection (Hough transform), black border removal, image centering, resize to 512×512; (2) Green channel imaging — extraction of the green channel from RGB (highest vessel-to-background contrast in retinal images); (3) Normalization — pixel intensity normalization to [0, 1] range; (4) CLAHE enhancement — applied in LAB color space (L-channel) with optimized clip limit (selected via parameter sweep, Experiment 2; replaces the fixed clip limit 2.0 of v1.0); (5) HSV contrast enhancement — additional contrast adjustment in HSV color space. A preprocessing pipeline is considered active when all five components are applied in the specified order. A pipeline is considered absent when images are passed to the CNN with resize only (FOV standardization without subsequent pipeline components). Data augmentation operations (horizontal flip, vertical flip, rotation, zoom, brightness variation) are applied during training as a separate data augmentation layer and are not a preprocessing component — this separation enables clean ablation in component-level experiments.

**OD-4: Generalization**  
Generalization is operationally defined as the difference between training-set performance and held-out test-set performance on the same evaluation metric. Overfitting is the condition wherein training precision exceeds test precision by more than 15 percentage points on any primary metric. Cross-database generalization is defined as the ratio of test-set F1-score on a secondary dataset (e.g., Messidor-2, IDRiD) to test-set F1-score on the primary dataset (EyePACS) under the same trained model, without retraining: G = F1_external / F1_EyePACS.

**OD-5: Diagnostic Effectiveness**  
Diagnostic effectiveness is operationally defined as the joint performance profile on four primary metrics — Accuracy, weighted F1-score, ROC-AUC, and Cohen's Kappa (quadratic weights) — computed on the held-out test partition. A preprocessing-CNN configuration is considered diagnostically effective when: Accuracy ≥ 0.80, weighted F1-score ≥ 0.80, ROC-AUC ≥ 0.90, and Cohen's Kappa ≥ 0.70, on the held-out EyePACS test partition (V3 primary dataset). [V3 NOTE: Re-anchored from APTOS 2019 (v1.0) to EyePACS. Threshold values retained from prior self-publications as reference baselines.] These threshold values are derived from the published empirical results in LC-SAPAKOVA-2025-01 (weighted F1 = 0.91, ROC-AUC = 0.9638) and LC-Yesmukhamedov-2025-SELF (Weighted Average = 0.81, Accuracy = 0.80).

**OD-6: Resource-Limited Environment**  
A resource-limited environment is defined as a deployment context characterized by at least two of the following conditions: (a) the absence of GPU acceleration for inference; (b) available RAM below 16 GB; (c) batch processing time constraints requiring inference completion within real-time or near-real-time clinical workflow; (d) network connectivity limitations precluding continuous cloud API reliance. The hardware conditions under which experiments were conducted operationalize this definition. Deployment in Kazakhstan's rural healthcare context (approximately 40% rural population, approximately 1,200 ophthalmologists nationally, per LC-2025-Yesmukhamedov-01, p. 77) provides the clinical framing but does not independently validate the computational definition.

---

## IV. SCOPE BOUNDARIES

**SB-1: What Is NOT Claimed**

- SB-1.1 The dissertation does not claim that the preprocessing pipeline achieves performance improvements on retinal imaging datasets other than those specified in the V3 dataset architecture (EyePACS, IDRiD, Messidor/Messidor-2, RFMiD, DDR, ODIR-5K), unless additional cross-database generalization experiments are explicitly conducted and reported. [V3: APTOS 2019 removed from active dataset architecture.]
- SB-1.2 The dissertation does not claim that 100% classification accuracy, sensitivity, or specificity is achievable on any dataset in the v2.1 architecture. Values reported for the STARE-based CLAHE study (LC-AlTimemy-2021) achieving 100% accuracy on 157/152 images are not transferable to the dissertation's experimental context.
- SB-1.3 The dissertation does not claim that the proposed system is a standalone diagnostic device or replaces ophthalmologist assessment. The system is a decision-support tool within a physician-in-the-loop paradigm.
- SB-1.4 The dissertation does not claim generalization of results to imaging modalities other than fundus photography (e.g., OCT, fluorescein angiography).
- SB-1.5 The dissertation does not claim that the laser-tissue interaction mathematical model (Chapter 2, Section 2.4) constitutes an experimentally validated clinical model. The model in LC-Sapakova-2024-01 provides qualitative simulation results without quantitative validation against experimental or clinical data.
- SB-1.6 The dissertation does not claim that projected deployment outcomes for Kazakhstan (20–30% reduction in late-stage DR complications; 15–20% cost reduction, per LC-2025-Yesmukhamedov-01, p. 88) are demonstrated results of this research. These are externally projected figures cited for contextual framing only.
- SB-1.7 The dissertation does not claim that any single architecture (ResNet-50, EfficientNet-B3, EfficientNet-B4, or EfficientNetB0) represents the globally optimal architecture for DR classification. The dissertation evaluates specific architectures within the experimental design; no comparative claim across the full architecture space is permissible without additional experiments.
- SB-1.8 The dissertation does not claim that device domain shift results (V3 Experiment 3) constitute device certification, regulatory approval, or compliance with medical device standards. Results are empirical observations of cross-device performance variability.
- SB-1.9 [V3: Experiment 3 (robustness to synthetic image degradation) has been dropped from V3 scope. This scope boundary is retained for historical reference: the dissertation does not claim that synthetic image degradation results are equivalent to robustness under real-world clinical imaging variability. As old Experiment 3 is no longer active, no synthetic degradation claims are made in V3.]
- SB-1.10 The dissertation does not claim that calibration metrics (ECE, Brier Score) establish clinical reliability of predicted probabilities. Calibration is reported as an empirical diagnostic property of the model, not as a guarantee of clinical decision-making reliability.
- SB-1.11 The dissertation does not claim that Grad-CAM explainability analysis constitutes clinical validation of the model's diagnostic reasoning. Grad-CAM provides post-hoc interpretability, not a mechanistic explanation of model decision processes (see NC-14).

**SB-2: Dataset Limitations**

- SB-2.1 The primary training dataset (EyePACS) contains approximately 35,126 labeled images (Kaggle labeled partition) with 5-class DR grading, providing statistical power for the factorial ablation design. Class imbalance characteristics must be documented and all performance claims interpreted in the context of distributional asymmetry.
- SB-2.2 Supplementary clinical images from private medical centers (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-SAPAKOVA-2025-01) are not publicly available due to privacy agreements. Reproducibility of results dependent on supplementary data is structurally limited.
- SB-2.3 Cross-database comparisons between EyePACS and external datasets (Messidor/Messidor-2, IDRiD, RFMiD, DDR, ODIR-5K) must explicitly acknowledge differences in imaging equipment, patient demographics, grading protocols, and disease taxonomy where applicable. RFMiD and ODIR-5K use multi-disease taxonomies with DR subsets; taxonomic mapping must be documented.

**SB-3: Architectural Limitations**

- SB-3.1 The dissertation evaluates two primary architectures in the factorial ablation (ResNet-50, EfficientNet-B3), one architecture for explainability analysis (EfficientNet-B4), and documents prior results on EfficientNetB0 from self-publications. No claim of architectural optimality or exhaustive search over the architecture space is permissible.
- SB-3.2 Results obtained under the specific hyperparameter configurations documented in the methodology do not generalize to architecturally equivalent configurations with different hyperparameters.

**SB-4: Deployment Limitations**

- SB-4.1 The system architecture described in Chapter 6 is a conceptual and design contribution (LC-2025-Yesmukhamedov-01). No prototype implementation or clinical deployment testing results are available as of the literature card record date.
- SB-4.2 GDPR/HIPAA compliance framing is a design specification, not a certified compliance status.
- SB-4.3 Applicability claims to Kazakhstan healthcare infrastructure are bounded by the absence of field testing in Kazakhstan clinical settings.

---

## V. EVIDENCE HIERARCHY

**EH-1: Primary Evaluation Metrics**

In descending order of evidentiary weight for evaluating diagnostic effectiveness:
1. Weighted F1-score (accounts for class imbalance; directly interpretable under skewed distribution)
2. ROC-AUC (threshold-independent performance measure)
3. Cohen's Kappa with quadratic weights (penalizes clinically significant ordinal misclassification)
4. Accuracy (reported but subject to inflation under class imbalance; not sufficient alone)

**EH-2: Secondary Metrics**

The following metrics are reported as supplementary and cannot independently establish or refute the primary hypotheses:
- Per-class Precision and Recall (informative but unstable under severe class imbalance for minority classes)
- Macro Average Precision/Recall/F1-score (reported alongside weighted average)
- Training-set metrics (used only for overfitting diagnosis, not for hypothesis evaluation)
- Clinical screening metrics: Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2) — reported for Experiment 3 (V3: Cross-Dataset Generalization and Device Domain Shift)
- Calibration metrics: Expected Calibration Error (ECE) and Brier Score — reported for Experiments 1 and 3 (V3)
- Image quality metrics: Contrast-to-Noise Ratio (CNR), Vessel Visibility Index, Entropy, SSIM — reported for pipeline analysis in Experiment 2
- Explainability metrics: Grad-CAM ALO (primary) and IoU (secondary) with lesion masks, attention consistency score — reported for Experiment 4 (V3)
- Generalization ratio: G = F1_external / F1_EyePACS per OD-4 — reported for Experiment 3 (V3)

**EH-3: Empirical Dominance Criterion**

A preprocessing condition is considered empirically dominant over a no-preprocessing baseline if and only if:
- Weighted F1-score improvement ≥ 5 percentage points on the test partition, AND
- ROC-AUC improvement ≥ 0.02 on the test partition, AND
- No degradation in Cohen's Kappa relative to baseline.

All three conditions must hold simultaneously. Improvement on a subset of metrics without satisfying all three does not constitute empirical dominance under this document.

**EH-4: Sufficient Validation Criterion**

The preprocessing dominance hypothesis (H-1) is considered sufficiently validated if:
- The empirical dominance criterion (EH-3) is satisfied on the EyePACS test partition, AND
- The same direction of effect (preprocessing ≻ no-preprocessing on primary metrics) is confirmed on at least one external dataset (Messidor-2 or IDRiD), AND
- Results are replicated across both architectures in the factorial design (ResNet-50 and EfficientNet-B3).

[V3 NOTE: H-3 (two-stage fine-tuning) has been DROPPED. EH-4 sufficient validation criterion no longer includes H-3. The two-stage fine-tuning protocol is used as a training strategy; its empirical baseline from prior self-publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF) is cited in context but not evaluated as a hypothesis.]

---

## VI. CLAIM FORMULATION CONSTRAINTS

**CFC-1: Permissible Claim Types**

- CFC-1.1 *Comparative claims bounded to tested configurations:* "Under conditions [X], configuration [A] outperformed configuration [B] on metric [M] by [δ]."
- CFC-1.2 *Parameter sensitivity claims bounded to tested ranges:* "Within the CLAHE clip limit range [a, b], classification performance on [metric] exhibited a sensitivity profile with optimum at [value]."
- CFC-1.3 *Architectural precedent claims with explicit limitation:* "The two-stage fine-tuning protocol demonstrated by [LC-SAPAKOVA-2025] achieved [metric values] on [dataset]; this dissertation extends this finding by [specific methodological extension]."
- CFC-1.4 *Conceptual contribution claims:* "The modified CLAHE formulation with simplified threshold control (CLIP LIMIT = T/80, per LC-AlTimemy-2021) was adapted and validated within the dissertation's preprocessing pipeline."
- CFC-1.5 *Design claims for the system architecture:* "The proposed system architecture specifies [component] intended to support [function]; empirical validation of the deployed system is reserved for future work."

**CFC-2: Forbidden Claim Types**

- CFC-2.1 Universal generalization claims: "The proposed method is effective for all fundus image datasets." — Forbidden: no cross-database exhaustive testing documented.
- CFC-2.2 Superiority claims without direct comparison: "The proposed pipeline outperforms existing DR diagnostic systems." — Forbidden unless accompanied by a direct controlled experiment against named systems under identical evaluation conditions.
- CFC-2.3 Deployment outcome claims stated as results: "The system reduces late-stage DR complications by 20–30% in Kazakhstan." — Forbidden: this figure is a third-party projection cited in LC-2025-Yesmukhamedov-01, p. 88; it is not a result of this dissertation's experiments.
- CFC-2.4 Validated clinical claims: "The system achieves clinical-grade diagnostic accuracy." — Forbidden: no clinical validation trial is documented in any literature card.
- CFC-2.5 Perfect performance generalizations: "The preprocessing pipeline achieves 100% accuracy on DR classification." — Forbidden: 100% accuracy reported in LC-AlTimemy-2021 is on a different dataset, classification task, and cannot be transferred to the dissertation's experimental framework.
- CFC-2.6 Amplified source claims: Any claim that attributes to a cited source a conclusion stronger than explicitly stated in that source. — Forbidden per Section VII rules.
- CFC-2.7 Retroactive re-characterization of prior self-publications: Prior publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-2025-Yesmukhamedov-01) must be cited as-is and may not be retroactively characterized as having claimed, proven, or demonstrated conclusions beyond what their texts state.

**CFC-3: Non-Claims**

- NC-1 through NC-13: Retained from v1.0 (as specified in prior Argument Map and claim structure documents).
- NC-14: Grad-CAM activation does not constitute clinical localization of pathology — it is an interpretability tool, not a diagnostic output. Grad-CAM overlays indicate regions of high gradient-weighted activation in the final convolutional layer and do not represent pixel-level diagnostic delineation of lesion boundaries.
- NC-15: The dirty data pipeline (External Image Ingestion Protocol) is not validated for arbitrary clinical data sources — validation is bounded to specific Kazakh medical center data. Generalization of the ingestion protocol to other clinical data sources requires independent validation.
- NC-16: Device domain shift results do not constitute device certification or regulatory compliance — they are empirical observations of cross-device performance variability. No claim of device-agnostic deployment readiness is permissible based on V3 Experiment 3 alone.
- NC-17: The preprocessing component ablation does not identify a universally optimal preprocessing configuration — the component hierarchy is bounded to the tested architectures (ResNet-50, EfficientNet-B3) and datasets (EyePACS). Extension to other architectures or datasets requires independent experimental validation.

---

## VII. SOURCE INTERPRETATION RULES

**SIR-1: Non-Amplification Rule**  
A cited source may only be attributed conclusions that are explicitly stated within the cited text. Implications, logical consequences, or extensions of a source's conclusions are attributed to the dissertation's own analysis, not to the source. The source is cited for what it states; the dissertation is credited for what it infers.

**SIR-2: Limitation Inheritance Rule**  
When a source's result is cited as supporting a dissertation claim, the limitations acknowledged in that source's literature card (Section II.6) are co-inherited by the claim unless the dissertation provides evidence that specifically addresses those limitations. The limitation must be noted at first citation of the relevant result.

**SIR-3: Metric Consistency Rule**  
When citing performance metrics from a source, the evaluation context (dataset, partition, class taxonomy, metric formula) must be replicated or the difference must be explicitly stated. The sensitivity formula anomaly in LC-AlTimemy-2021 (Eq. 3: Sen = TP/(TP+TN), deviating from standard Sen = TP/(TP+FN)) must be noted if that source's sensitivity figure is cited.

**SIR-4: Self-Citation Transparency Rule**  
All self-authored prior publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-2025-Yesmukhamedov-01) must be explicitly identified as prior own work at point of citation. Results from these sources cited in the dissertation must be framed as "previously published results" and must be accompanied by a statement of how the dissertation's treatment extends, validates, or formalizes those results.

**SIR-5: No Cross-Source Aggregation Without Independence Confirmation**  
Sources that share overlapping datasets, authors, or experimental configurations (notably LC-SAPAKOVA-2025 and LC-Yesmukhamedov-2025-SELF, which use identical experimental data) may not be cited as independent confirmatory evidence of the same claim. Independent confirmation requires methodologically distinct experiments on distinct data partitions or datasets.

**SIR-6: Modeling Study Non-Extrapolation Rule**  
LC-Sapakova-2024-01 presents computational simulation results without quantitative clinical validation. Results from this source may be cited as theoretical/computational grounding only. They may not be cited as empirical validation of physical or clinical outcomes. The statement that simulation results "confirm the effectiveness of laser therapy" (LC-Sapakova-2024-01, Results, p. 7) is a claim of the source and must be cited as such, not absorbed into the dissertation's own validated claims.

**SIR-7: Architecture Generalization Prohibition**  
Results obtained with EfficientNetB0 (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF) may not be generalized to the class of efficient CNN architectures without explicit comparative experiments. The source's own limitation (LC-SAPAKOVA-2025, Section II.6) that "alternative architectures were not evaluated at this stage" is binding.

**SIR-8: Projected Outcome Non-Attribution Rule**  
Projected outcomes for Kazakhstan deployment cited in LC-2025-Yesmukhamedov-01 (p. 88: 4+ million rural residents accessed; 20–30% late-stage DR reduction; 15–20% cost reduction) are third-party projections cited by the authors. They may not be attributed to the dissertation's own findings or used to substantiate claims about demonstrated system impact.

---

## VIII. THESIS VERSION CONTROL RULE

**VCR-1:** The Central Thesis (Section I) and Core Hypotheses (Section II) are immutable post-ratification of this document. Modifications to the thesis or hypotheses require the creation of a new versioned Invariants document; they do not propagate retroactively to literature cards. Note (v3.0): H-3 (Two-Stage Fine-Tuning) has been DROPPED from V3. The dropping of H-3 constitutes a scope reduction, not a falsification — H-3 is simply no longer tested as an independent hypothesis. The two-stage fine-tuning protocol remains in use as a training strategy. ALO is confirmed as the PRIMARY explainability metric in H-5; IoU is secondary.

**VCR-2:** Literature cards record the state of source interpretation at the time of extraction. If new sources are added to the dissertation, new literature cards must be created and appended to the literature card corpus. Existing literature cards are not modified to accommodate new sources.

**VCR-3:** If experimental results contradict the direction of effect specified in H-1, H-2, H-4, H-5, or H-6, the hypothesis is not silently modified. The result is reported as a falsifying observation, and the dissertation text must explicitly account for the discrepancy between the null finding and the hypothesis as stated. [V3: H-3 removed from this list — H-3 is DROPPED and no longer tested.]

**VCR-4:** The scope boundaries defined in Section IV are fixed for the dissertation's primary experimental claims. If additional experiments are conducted beyond the scope defined here, those experiments constitute extended contributions and must be explicitly labeled as extensions, not revisions of the core thesis.

**VCR-5:** Terminology defined in Section III must remain stable across all dissertation chapters. Terminological drift — the use of operationally defined terms with different referents in different sections — constitutes a constraint violation.

---

## IX. DEPLOYMENT AND GENERALIZATION LIMITATIONS

**DGL-1: Dataset-Bound Generalization**
All performance claims are bounded to the V3 dataset architecture: EyePACS (~35,126 labeled images, Kaggle labeled partition, five-class DR staging, primary training), IDRiD (clinical validation, lesion localization with pixel-level annotations, and CLAHE parameter sweep), Messidor/Messidor-2 (external generalization), and RFMiD/DDR/ODIR-5K (device domain shift evaluation across Topcon, Kowa, Canon, and Zeiss camera hardware). [V3: APTOS 2019 is no longer an active experimental dataset — old Experiment 3 (robustness to synthetic degradation) was dropped.] Extension to other fundus image datasets, other imaging devices not represented in the tested corpora, or other clinical populations requires independent experimental validation not currently available.

**DGL-2: Hardware-Specific Reproducibility**  
Experimental results are obtained under hardware constraints as documented in Section 4.1.3 of the dissertation. Claims about computational efficiency or real-time inference capability are bounded to the specific hardware configuration used. They do not generalize to substantially different hardware contexts (e.g., mobile inference on ARM processors, or server-class GPU clusters) without re-evaluation.

**DGL-3: Clinical Population Non-Extrapolation**  
The datasets in the v2.1 architecture and supplementary clinical images from private medical centers do not constitute a demographically characterized clinical population sample. No claims regarding system performance on specific ethnic, age-stratified, or comorbidity-defined patient groups are permissible.

**DGL-4: System Architecture Deployment Constraints**  
The system architecture described in Chapter 6 (LC-2025-Yesmukhamedov-01) has not been prototype-implemented or field-tested. All deployment-oriented statements (PACS integration, EHR interoperability, GDPR/HIPAA compliance, telemedicine support) are design specifications. Their operational realization in Kazakhstan's healthcare infrastructure is subject to infrastructure prerequisites acknowledged in the source (LC-2025-Yesmukhamedov-01, p. 90): investments in diagnostic equipment, adaptation of algorithms to local data, national standards development, and specialist training.

**DGL-5: CLAHE Parameter Portability**
CLAHE parameters validated in the dissertation context (optimized clip limit in LAB color space per V3 pipeline, selected via parameter sweep in Experiment 2; and clip limit 2.0 / grid size 8×8 per prior self-publications LC-SAPAKOVA-2025-01) were optimized for specific image distributions and CNN architectures. The T/80 threshold formulation from LC-AlTimemy-2021 was derived on the STARE dataset with different image characteristics. No parameter-level equivalence between these configurations is asserted. If the dissertation adopts modified CLAHE parameters, those parameters must be independently validated within the dissertation's experimental framework.

**DGL-6: Transfer Learning Domain Gap**  
EfficientNetB0, EfficientNet-B3, EfficientNet-B4, and ResNet-50 weights were pre-trained on ImageNet (natural images). Transfer of these weights to fundus image classification represents a domain shift. The degree to which ImageNet features transfer to retinal microvascular feature representations is not theoretically guaranteed and is evaluated empirically within the dissertation's experimental framework only. Claims about feature transferability are bounded to the architectures, fine-tuning protocols, and datasets documented in the literature cards and v2.1 experimental protocol.

---

*Document version: 3.0. Supersedes v2.2. Binding upon ratification. All subsequent dissertation drafts are subject to constraint verification against this document.*
