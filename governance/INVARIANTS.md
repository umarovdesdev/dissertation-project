# DISSERTATION INVARIANTS DOCUMENT
## Immutable Epistemic Structure for Doctoral Research

**Research Domain:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S.  
**Document Status:** Binding constraint system — supersedes informal claim formulations across all dissertation chapters.

---

## I. CENTRAL THESIS (Immutable Formulation)

**IT-1.** An integrated preprocessing-CNN pipeline — comprising resizing, pixel normalization to [0, 1], modified CLAHE with controllable threshold parameter (clip limit ≥ 2.0, tile grid ≥ 8×8), and data augmentation — applied to fundus images sourced from APTOS 2019 and supplementary clinical corpora, produces statistically measurable improvement in five-class diabetic retinopathy classification performance relative to a baseline CNN trained without preprocessing, under constrained computational conditions defined by hardware limitations operative during experimental execution.

**Scope boundary embedded in IT-1:**
- The thesis is bounded to five-stage DR classification (DR 0–4 per standard clinical grading).
- The thesis does not extend to general retinal disease classification, to other ophthalmological imaging modalities, or to imaging contexts not representable by the APTOS 2019 and STARE datasets.
- "Improvement" is defined exclusively as measurable difference in primary metrics (see Section V) computed across matched experimental conditions.

---

## II. CORE HYPOTHESIS (Operational Form)

**H-1 (Primary — Preprocessing Dominance):**

*If* fundus images from APTOS 2019 (n = 3,662 labeled samples, five DR classes) are processed through a unified preprocessing pipeline comprising resizing (256×256 or 512×512 pixels), normalization, CLAHE (clip limit 2.0, grid 8×8), and augmentation (horizontal/vertical flip, rotation ±15°, zoom ±10%, brightness variation),  
*and* a CNN classifier (multi-block architecture with batch normalization, dropout rate 0.4, categorical cross-entropy loss, Adam optimizer, learning rate 0.0001) is trained on the processed images,  
*then* classification accuracy, F1-score, and ROC-AUC will exceed those of a baseline CNN (two convolutional blocks, 32–64 filters, sigmoid output, binary cross-entropy, input 256×256) trained on unprocessed images of equivalent source distribution.

- **Independent variable:** Presence vs. absence of the unified preprocessing pipeline.
- **Dependent variables:** Accuracy, F1-score (macro and weighted), ROC-AUC, Cohen's Kappa (quadratic weights), precision, recall — computed on the held-out test partition.
- **Control conditions:** Same dataset, same data partition strategy, same computational hardware, same training epoch budget.

---

**H-2 (Secondary — CLAHE Threshold Sensitivity):**

*If* the clip limit parameter of CLAHE is varied across controlled values on a small fundus image dataset,  
*then* classification performance of the downstream CNN will exhibit a parameter-dependent sensitivity profile, identifiable as a non-trivial sensitivity curve with at least one local optimum within the tested range.

- **Independent variable:** CLAHE clip limit value.
- **Dependent variables:** Per-class F1-score for DR stages with smallest lesion features (microaneurysms, small vessels — predominantly DR 1 and DR 2 classes).
- **Scope:** Bounded to the parameter range tested experimentally. No extrapolation to untested parameter values is permissible.

---

**H-3 (Secondary — Two-Stage Fine-Tuning):**

*If* EfficientNetB0 (pre-trained on ImageNet) is adapted using a two-stage protocol — (1) frozen base layers with classification head training, followed by (2) progressive unfreezing of upper layers — under the same preprocessing regime,  
*then* test-set precision, recall, F1-score, and Cohen's Kappa will exceed those obtained from the frozen-only strategy (Stage 1 alone).

- **Independent variable:** Frozen-only vs. progressive fine-tuning adaptation strategy.
- **Dependent variables:** Precision (Test), Recall (Test), F1-Score (Test), Macro Average, Weighted Average, Cohen's Kappa.
- **Empirical reference values:** Frozen method — Precision 0.65, Recall 0.60, F1 0.62; Fine-tuned method — Precision 0.75, Recall 0.74, F1 0.74 (LC-SAPAKOVA-2025 / LC-Yesmukhamedov-2025-SELF). These values constitute the published empirical baseline for this hypothesis and must be cited as prior self-publications.

---

## III. OPERATIONAL DEFINITIONS

**OD-1: Image Quality**  
Image quality is operationally defined as the measurable capacity of a fundus image to support automated detection of microvascular features relevant to DR staging. Image quality is assessed through downstream classification performance metrics (accuracy, F1-score, ROC-AUC) computed on the same classifier architecture under identical training conditions with varying preprocessing states (absent vs. applied). No standalone subjective image quality score is used as the primary quality measure. An image quality condition is considered degraded if baseline CNN accuracy on unprocessed images falls below the enhanced CNN accuracy by a statistically interpretable margin under matched conditions.

**OD-2: Architectural Complexity**  
Architectural complexity is operationally defined by the number of convolutional layers, total trainable parameter count, filter size range, and presence or absence of regularization components (batch normalization, dropout). The baseline architecture (two convolutional blocks, 32–64 filters, no batch normalization, no dropout, sigmoid output) constitutes the low-complexity reference. The enhanced architecture (four convolutional blocks, 32–256 filters, batch normalization, dropout rate 0.4, softmax 5-class output) constitutes the high-complexity reference. Architectures outside these bounds are not evaluated within this dissertation.

**OD-3: Preprocessing Pipeline**  
The preprocessing pipeline is the ordered sequence of image transformation operations applied prior to CNN input: (1) resizing to target resolution (256×256 or 512×512 pixels), (2) pixel value normalization to [0, 1], (3) CLAHE with specified clip limit and tile grid parameters, (4) data augmentation operations (horizontal flip, vertical flip, rotation ±15°, zoom ±10%, brightness variation). A preprocessing pipeline is considered active when all four stages are applied in the specified order. A pipeline is considered absent when images are passed to the CNN without any of these transformations beyond basic resizing required for input dimension matching.

**OD-4: Generalization**  
Generalization is operationally defined as the difference between training-set performance and held-out test-set performance on the same evaluation metric. Overfitting is the condition wherein training precision exceeds test precision by more than 15 percentage points on any primary metric. Cross-database generalization is defined as the ratio of test-set F1-score on a secondary dataset (e.g., STARE) to test-set F1-score on the primary dataset (APTOS 2019) under the same trained model, without retraining.

**OD-5: Diagnostic Effectiveness**  
Diagnostic effectiveness is operationally defined as the joint performance profile on four primary metrics — Accuracy, weighted F1-score, ROC-AUC, and Cohen's Kappa (quadratic weights) — computed on the held-out test partition. A preprocessing-CNN configuration is considered diagnostically effective when: Accuracy ≥ 0.80, weighted F1-score ≥ 0.80, ROC-AUC ≥ 0.90, and Cohen's Kappa ≥ 0.70, on the APTOS 2019 test partition. These threshold values are derived from the published empirical results in LC-SAPAKOVA-2025-01 (weighted F1 = 0.91, ROC-AUC = 0.9638) and LC-Yesmukhamedov-2025-SELF (Weighted Average = 0.81, Accuracy = 0.80).

**OD-6: Resource-Limited Environment**  
A resource-limited environment is defined as a deployment context characterized by at least two of the following conditions: (a) the absence of GPU acceleration for inference; (b) available RAM below 16 GB; (c) batch processing time constraints requiring inference completion within real-time or near-real-time clinical workflow; (d) network connectivity limitations precluding continuous cloud API reliance. The hardware conditions under which experiments were conducted operationalize this definition. Deployment in Kazakhstan's rural healthcare context (approximately 40% rural population, approximately 1,200 ophthalmologists nationally, per LC-2025-Yesmukhamedov-01, p. 77) provides the clinical framing but does not independently validate the computational definition.

---

## IV. SCOPE BOUNDARIES

**SB-1: What Is NOT Claimed**

- SB-1.1 The dissertation does not claim that the preprocessing pipeline achieves performance improvements on retinal imaging datasets other than APTOS 2019 and STARE, unless cross-database generalization experiments (Section 5.1) are explicitly conducted and reported.
- SB-1.2 The dissertation does not claim that 100% classification accuracy, sensitivity, or specificity is achievable on APTOS 2019. Values reported for the STARE-based CLAHE study (LC-AlTimemy-2021) achieving 100% accuracy on 157/152 images are not transferable to the dissertation's experimental context.
- SB-1.3 The dissertation does not claim that the proposed system is a standalone diagnostic device or replaces ophthalmologist assessment. The system is a decision-support tool within a physician-in-the-loop paradigm.
- SB-1.4 The dissertation does not claim generalization of results to imaging modalities other than fundus photography (e.g., OCT, fluorescein angiography).
- SB-1.5 The dissertation does not claim that the laser-tissue interaction mathematical model (Chapter 2, Section 2.4) constitutes an experimentally validated clinical model. The model in LC-Sapakova-2024-01 provides qualitative simulation results without quantitative validation against experimental or clinical data.
- SB-1.6 The dissertation does not claim that projected deployment outcomes for Kazakhstan (20–30% reduction in late-stage DR complications; 15–20% cost reduction, per LC-2025-Yesmukhamedov-01, p. 88) are demonstrated results of this research. These are externally projected figures cited for contextual framing only.
- SB-1.7 The dissertation does not claim that EfficientNetB0 represents the globally optimal architecture for DR classification. Alternative architectures (ResNet, VGG, DenseNet) were not evaluated in the referenced conference publications; no comparative claim across architecture families is permissible without additional experiments.

**SB-2: Dataset Limitations**

- SB-2.1 The primary dataset (APTOS 2019) contains 3,662 labeled training images with severe class imbalance: Class 0 constitutes 49.3%–73.5% of images (test/train respectively); Classes 3 and 4 together constitute 13.3% of test images and 4.5% of training images. All performance claims must be interpreted in the context of this distributional asymmetry.
- SB-2.2 Supplementary clinical images from private medical centers (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-SAPAKOVA-2025-01) are not publicly available due to privacy agreements. Reproducibility of results dependent on supplementary data is structurally limited.
- SB-2.3 The STARE dataset used in Section 5.1 contains 157 images across a different five-class disease taxonomy (BDR, CRVO, CNV, PDR, Normal), which does not correspond to the dissertation's five-class DR severity grading (DR 0–4). Cross-dataset comparisons must explicitly acknowledge this taxonomic non-equivalence.

**SB-3: Architectural Limitations**

- SB-3.1 The dissertation evaluates two CNN configurations (baseline: two-block; enhanced: four-block) and two transfer learning architectures (EfficientNetB0, ResNet50). No claim of architectural optimality or exhaustive search over the architecture space is permissible.
- SB-3.2 Results obtained under the specific hyperparameter configurations documented in the methodology (Adam optimizer, learning rate 0.0001, batch size 32, dropout 0.4, early stopping) do not generalize to architecturally equivalent configurations with different hyperparameters.

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

**EH-3: Empirical Dominance Criterion**

A preprocessing condition is considered empirically dominant over a no-preprocessing baseline if and only if:
- Weighted F1-score improvement ≥ 5 percentage points on the test partition, AND
- ROC-AUC improvement ≥ 0.02 on the test partition, AND
- No degradation in Cohen's Kappa relative to baseline.

All three conditions must hold simultaneously. Improvement on a subset of metrics without satisfying all three does not constitute empirical dominance under this document.

**EH-4: Sufficient Validation Criterion**

The preprocessing dominance hypothesis (H-1) is considered sufficiently validated if:
- The empirical dominance criterion (EH-3) is satisfied on the APTOS 2019 test partition, AND
- The same direction of effect (preprocessing ≻ no-preprocessing on primary metrics) is confirmed on at least one secondary dataset (STARE or equivalent), AND
- Results are replicated across at least two architectures (e.g., custom CNN and EfficientNetB0).

Sufficient validation of H-3 (two-stage fine-tuning) requires replication of the performance differential documented in prior self-publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF) within the dissertation's experimental configuration, with explicit acknowledgment that the prior publications constitute the foundational empirical record for this hypothesis.

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
- CFC-2.5 Perfect performance generalizations: "The preprocessing pipeline achieves 100% accuracy on DR classification." — Forbidden: 100% accuracy reported in LC-AlTimemy-2021 is on a different dataset, classification task, and cannot be transferred to the dissertation's APTOS 2019 framework.
- CFC-2.6 Amplified source claims: Any claim that attributes to a cited source a conclusion stronger than explicitly stated in that source. — Forbidden per Section VII rules.
- CFC-2.7 Retroactive re-characterization of prior self-publications: Prior publications (LC-SAPAKOVA-2025, LC-Yesmukhamedov-2025-SELF, LC-Sapakova-2024-01, LC-2025-Yesmukhamedov-01) must be cited as-is and may not be retroactively characterized as having claimed, proven, or demonstrated conclusions beyond what their texts state.

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

**VCR-1:** The Central Thesis (Section I) and Core Hypotheses (Section II) are immutable post-ratification of this document. Modifications to the thesis or hypotheses require the creation of a new versioned Invariants document; they do not propagate retroactively to literature cards.

**VCR-2:** Literature cards record the state of source interpretation at the time of extraction. If new sources are added to the dissertation, new literature cards must be created and appended to the literature card corpus. Existing literature cards are not modified to accommodate new sources.

**VCR-3:** If experimental results contradict the direction of effect specified in H-1, H-2, or H-3, the hypothesis is not silently modified. The result is reported as a falsifying observation, and the dissertation text must explicitly account for the discrepancy between the null finding and the hypothesis as stated.

**VCR-4:** The scope boundaries defined in Section IV are fixed for the dissertation's primary experimental claims. If additional experiments are conducted beyond the scope defined here, those experiments constitute extended contributions and must be explicitly labeled as extensions, not revisions of the core thesis.

**VCR-5:** Terminology defined in Section III must remain stable across all dissertation chapters. Terminological drift — the use of operationally defined terms with different referents in different sections — constitutes a constraint violation.

---

## IX. DEPLOYMENT AND GENERALIZATION LIMITATIONS

**DGL-1: Dataset-Bound Generalization**  
All performance claims are bounded to the APTOS 2019 dataset (3,662 labeled samples, five-class DR staging) and, where cross-database experiments are conducted, to the STARE dataset (157 images, five-class disease taxonomy, taxonomically non-equivalent to APTOS DR 0–4). Extension to other fundus image datasets, other imaging devices, or other clinical populations requires independent experimental validation not currently available.

**DGL-2: Hardware-Specific Reproducibility**  
Experimental results are obtained under hardware constraints as documented in Section 4.1.3 of the dissertation. Claims about computational efficiency or real-time inference capability are bounded to the specific hardware configuration used. They do not generalize to substantially different hardware contexts (e.g., mobile inference on ARM processors, or server-class GPU clusters) without re-evaluation.

**DGL-3: Clinical Population Non-Extrapolation**  
The APTOS 2019 dataset and supplementary clinical images from private medical centers do not constitute a demographically characterized clinical population sample. No claims regarding system performance on specific ethnic, age-stratified, or comorbidity-defined patient groups are permissible.

**DGL-4: System Architecture Deployment Constraints**  
The system architecture described in Chapter 6 (LC-2025-Yesmukhamedov-01) has not been prototype-implemented or field-tested. All deployment-oriented statements (PACS integration, EHR interoperability, GDPR/HIPAA compliance, telemedicine support) are design specifications. Their operational realization in Kazakhstan's healthcare infrastructure is subject to infrastructure prerequisites acknowledged in the source (LC-2025-Yesmukhamedov-01, p. 90): investments in diagnostic equipment, adaptation of algorithms to local data, national standards development, and specialist training.

**DGL-5: CLAHE Parameter Portability**  
CLAHE parameters validated in the dissertation context (clip limit 2.0, grid size 8×8, per LC-SAPAKOVA-2025-01) were optimized for the APTOS 2019 image distribution and the specified CNN architectures. The T/80 threshold formulation from LC-AlTimemy-2021 was derived on the STARE dataset with different image characteristics. No parameter-level equivalence between these configurations is asserted. If the dissertation adopts modified CLAHE parameters, those parameters must be independently validated within the dissertation's experimental framework.

**DGL-6: Transfer Learning Domain Gap**  
EfficientNetB0 and ResNet50 weights were pre-trained on ImageNet (natural images). Transfer of these weights to fundus image classification represents a domain shift. The degree to which ImageNet features transfer to retinal microvascular feature representations is not theoretically guaranteed and is evaluated empirically within the dissertation's experimental framework only. Claims about feature transferability are bounded to the architectures, fine-tuning protocols, and datasets documented in the literature cards.

---

*Document version: 1.0. Binding upon ratification. All subsequent dissertation drafts are subject to constraint verification against this document.*
