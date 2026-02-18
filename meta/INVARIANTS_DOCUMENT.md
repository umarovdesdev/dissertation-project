# INVARIANTS DOCUMENT

## Epistemic Constraint System for PhD Dissertation

**Dissertation Domain:** Automated Diabetic Retinopathy Diagnosis via Integrated Image Preprocessing and Convolutional Neural Network Classification

**Source Literature Cards Governing This Document:**
- LC-SAPAKOVA-2025 (Conference paper, DS 2025)
- LC-Sapakova-2024-01 (KazUTB, laser-tissue modeling)
- LC-Yesmukhamedov-2025-SELF (KBTU, Herald)
- LC-2025-Yesmukhamedov-01 (NAN RK, system architecture)
- LC-AlTimemy-2021 (Scopus Q2, upgraded CLAHE + RESNET50)
- LC-SAPAKOVA-2025-01 (Scopus Q3, EEJT, preprocessing-CNN integration)

**Document Status:** Immutable constraint system. No section may be altered without version-controlled amendment (see Section VIII).

---

## I. CENTRAL THESIS (Immutable Formulation)

The integration of a specified image preprocessing pipeline — comprising resizing, pixel normalization to [0, 1], Contrast-Limited Adaptive Histogram Equalization (CLAHE, clip limit 2.0, grid size 8×8), and data augmentation (rotation, flipping, zoom, brightness variation) — with convolutional neural network architectures (baseline: 2-block CNN with 32–64 filters, 256×256 input; enhanced: 4-layer CNN with 32–256 filters, batch normalization, dropout 0.4, 512×512 input) yields statistically measurable improvement in five-class diabetic retinopathy classification performance on the APTOS 2019 dataset, as measured by validation accuracy, precision, recall, F1-score, and ROC-AUC, compared to an equivalent CNN architecture without the specified preprocessing pipeline.

**Controlled conditions:** Results are valid only for (a) the APTOS 2019 Blindness Detection dataset supplemented with labeled clinical images from local medical centers, (b) the specific CNN architectures described, (c) the specific preprocessing parameter values stated, and (d) training conducted under the hardware and software configurations documented in the experimental protocol.

**Scope limits:** This thesis does not claim superiority over all possible preprocessing-architecture combinations. It does not claim clinical deployment readiness. It does not claim generalization to datasets, imaging equipment, or populations not tested.

---

## II. CORE HYPOTHESIS (Operational Form)

### II.1 Primary Hypothesis (H₁)

**If** a preprocessing pipeline consisting of resizing (to 512×512 via cubic interpolation), normalization ([0, 1]), CLAHE (clip limit 2.0, grid 8×8), and augmentation (±15° rotation, ±10% zoom, horizontal/vertical flips, brightness variation) is applied to fundus images from the APTOS 2019 dataset prior to input into an enhanced CNN (4 convolutional layers, 32–256 filters, batch normalization, dropout 0.4, Adam optimizer lr=0.0001, categorical cross-entropy loss, early stopping),

**Then** classification performance on five-class DR staging (0–4) will exceed that of the same CNN architecture receiving unprocessed or minimally processed images,

**As measured by:** validation accuracy, macro-averaged precision, macro-averaged recall, macro-averaged F1-score, and ROC-AUC.

**Independent variable:** Presence vs. absence of the specified preprocessing pipeline.

**Dependent variables:** Validation accuracy, precision, recall, F1-score, ROC-AUC, training/validation loss convergence rate.

**Evaluation criterion for confirmation:** The preprocessed condition must exceed the non-preprocessed condition on at least three of the five primary metrics simultaneously, with accuracy improvement ≥ 3 percentage points.

### II.2 Secondary Hypothesis (H₂)

**If** a two-stage fine-tuning strategy (Stage 1: freeze base layers, train classification head; Stage 2: unfreeze upper layers, fine-tune with reduced learning rate) is applied to EfficientNetB0 pre-trained on ImageNet for DR classification on the same dataset,

**Then** test-set precision, recall, and F1-score will exceed those of the frozen-only strategy,

**As measured by:** test precision, test recall, test F1-score, macro average, weighted average.

**Evaluation criterion:** Method 2 must exceed Method 1 on test precision, test recall, and test F1-score simultaneously.

**Empirical basis:** LC-SAPAKOVA-2025 reports Method 2 exceeded Method 1 by +10 pp (precision), +14 pp (recall), +12 pp (F1-score) on test data. LC-Yesmukhamedov-2025-SELF corroborates with identical metric differentials.

---

## III. OPERATIONAL DEFINITIONS

### III.1 Image Quality

The degree to which a fundus image satisfies the following measurable preprocessing conditions: (a) spatial resolution of 256×256 pixels (baseline) or 512×512 pixels (enhanced, via cubic interpolation); (b) pixel intensity values normalized to the [0, 1] range; (c) local contrast enhanced via CLAHE with clip limit 2.0 and grid size 8×8; (d) artifacts and noise smoothed; (e) color balance adjusted. Image quality is operationally defined as the completion of all specified pipeline stages. It is not a subjective assessment.

**Source basis:** LC-SAPAKOVA-2025-01 (pp. 81–83); LC-SAPAKOVA-2025 (p. 498); LC-AlTimemy-2021 (Section 2.2.1).

### III.2 Architectural Complexity

The number of trainable parameters, convolutional layers, and filter counts in a CNN model. Operationally:
- **Low complexity (baseline):** 2 convolutional blocks (32, 64 filters), 3×3 kernels, max-pooling, fully connected layer with 128 neurons, sigmoid output. Binary cross-entropy loss. Input: 256×256.
- **Moderate complexity (enhanced):** 4 convolutional layers (32, 64, 128, 256 filters), batch normalization, dropout (0.4), two dense layers, softmax 5-class output. Categorical cross-entropy loss. Input: 512×512.
- **Transfer learning complexity (EfficientNetB0):** Pre-trained on ImageNet. Two adaptation strategies: (a) frozen base layers with trainable classification head; (b) progressive fine-tuning of upper layers.

Architectural complexity is bounded by the three configurations above. No claims extend to architectures outside this set.

**Source basis:** LC-SAPAKOVA-2025-01 (p. 83); LC-SAPAKOVA-2025 (pp. 497–499); LC-Yesmukhamedov-2025-SELF (Results and Discussion section).

### III.3 Preprocessing Pipeline

An ordered, deterministic sequence of image transformations applied to raw fundus images before CNN input. The pipeline is defined as:
1. **Resizing:** To 256×256 (baseline) or 512×512 (enhanced) pixels via cubic interpolation.
2. **Normalization:** Pixel values mapped to [0, 1] range.
3. **CLAHE:** Contrast-Limited Adaptive Histogram Equalization, clip limit = 2.0, grid size = 8×8, applied via OpenCV.
4. **Augmentation:** Horizontal and vertical flips, random rotation (±15°), zoom (±10%), brightness variation.

The pipeline is operationally complete only when all four stages are applied in sequence. Partial application constitutes a different experimental condition.

**Source basis:** LC-SAPAKOVA-2025-01 (pp. 81–83); LC-AlTimemy-2021 (Section 2.2.1, Eq. 2); LC-SAPAKOVA-2025 (p. 498).

### III.4 Generalization

The ability of a trained model to maintain classification performance on data not seen during training. Operationally measured by:
- The difference between training-set and test-set F1-score (train-test F1 gap).
- Validation accuracy relative to training accuracy.
- Performance on held-out test partitions from the same dataset (APTOS 2019).

A model is considered to generalize within-dataset if the train-test F1 gap is ≤ 0.15. Cross-dataset generalization (e.g., STARE) is not claimed unless explicitly tested and reported.

**Source basis:** LC-SAPAKOVA-2025 (p. 499: train F1=0.87 vs. test F1=0.62 for Method 1; train F1=0.86 vs. test F1=0.74 for Method 2); LC-SAPAKOVA-2025-01 (p. 86: dataset-specific training limits generalization).

### III.5 Diagnostic Effectiveness

The aggregate classification performance of the preprocessing-CNN system as measured by the following metrics on the test or validation partition:
- **Primary:** F1-score (macro-averaged), ROC-AUC.
- **Secondary:** Precision (per-class and macro-averaged), Recall (per-class and macro-averaged), Accuracy, Cohen's Kappa (quadratic weights), Weighted Average.

Diagnostic effectiveness is not equivalent to clinical diagnostic validity. It denotes computational classification performance on labeled benchmark data only.

**Source basis:** LC-SAPAKOVA-2025-01 (p. 83–84); LC-SAPAKOVA-2025 (p. 499, Table 3); LC-Yesmukhamedov-2025-SELF (formulas 6–7); LC-AlTimemy-2021 (Eqs. 3–5).

### III.6 Resource-Limited Environment

A deployment context characterized by one or more of the following operational constraints:
- Hardware overheating limiting training epoch count (LC-SAPAKOVA-2025-01, p. 86).
- Limited availability of GPU resources, restricting model complexity and image resolution (LC-SAPAKOVA-2025-01, p. 81).
- Geographic remoteness from specialized ophthalmological care (LC-2025-Yesmukhamedov-01, pp. 86–87: ~1,200 ophthalmologists for Kazakhstan; ~70% rural residents with limited eye care access).
- Reliance on portable diagnostic devices (e.g., Fundus on Phone, ~$5,000) rather than clinical-grade imaging equipment (LC-2025-Yesmukhamedov-01, p. 87).

This definition is descriptive of target deployment conditions. It does not constitute a claim that the proposed system has been validated in such environments.

**Source basis:** LC-2025-Yesmukhamedov-01 (pp. 86–88); LC-SAPAKOVA-2025-01 (pp. 81, 86–87).

---

## IV. SCOPE BOUNDARIES

### IV.1 What Is NOT Claimed

1. The dissertation does not claim that the proposed preprocessing pipeline is optimal among all possible preprocessing configurations.
2. The dissertation does not claim that the CNN architectures tested (baseline 2-block, enhanced 4-layer, EfficientNetB0) represent the full space of viable architectures for DR classification. Alternative architectures (ResNet variants beyond ResNet50, VGG, DenseNet, Vision Transformers) were not evaluated. (LC-SAPAKOVA-2025, p. 498)
3. The dissertation does not claim clinical deployment readiness. No clinical trial, regulatory approval, or real-world clinical validation has been performed.
4. The dissertation does not claim that the 100% accuracy reported in LC-AlTimemy-2021 on the STARE dataset (157 images, 5 disease types) is transferable to the APTOS 2019 five-class DR severity grading task.
5. The dissertation does not claim that preprocessing impact can be isolated from architectural adaptation when both are changed simultaneously. (LC-SAPAKOVA-2025, Section IV: "the source does not isolate preprocessing impact from architectural adaptation.")
6. The dissertation does not claim interpretability or explainability of the CNN classification decisions. Grad-CAM, SHAP, and equivalent methods are identified as future work. (LC-SAPAKOVA-2025-01, p. 86)
7. The dissertation does not claim that the supplementary clinical dataset from local medical centers is distributionally equivalent to APTOS 2019. No inter-annotator agreement or distributional similarity analysis has been reported. (LC-SAPAKOVA-2025, p. 498; LC-SAPAKOVA-2025-01, p. 81)
8. The dissertation does not claim that the proposed system architecture (LC-2025-Yesmukhamedov-01) has been implemented as a functional prototype or tested in a clinical information system.

### IV.2 Dataset Limitations

1. **Primary dataset:** APTOS 2019 Blindness Detection (Kaggle). 3,662 labeled images (training partition); 1,928 unlabeled test images. Five DR severity classes (0–4).
2. **Class imbalance:** Training set: Class 0 = 73.5%, Class 1 = 7.0%, Class 2 = 15.1%, Class 3 = 2.5%, Class 4 = 2.0%. Severe and proliferative stages are severely underrepresented.
3. **Supplementary data:** Anonymized fundus images from private medical centers, labeled by certified ophthalmologists. Not publicly available. No inter-annotator reliability reported.
4. **STARE dataset** (referenced via LC-AlTimemy-2021): 157 images, 5 disease types (BDR, CRVO, CNV, PDR, Normal). Fundamentally different classification task from APTOS 2019 DR severity grading. Not directly comparable.
5. **No multi-center external validation dataset** has been employed. All reported metrics are within-dataset evaluations.

### IV.3 Architectural Limitations

1. Only three CNN configurations were experimentally evaluated: baseline 2-block CNN, enhanced 4-layer CNN, and EfficientNetB0 with transfer learning.
2. ResNet50 is referenced via LC-AlTimemy-2021 as a methodological precedent but with a different dataset (STARE) and classification task (disease type, not severity grading).
3. No ensemble methods, attention mechanisms, or transformer-based architectures were tested.
4. Hyperparameter selection was performed via grid search and random search (LC-Yesmukhamedov-2025-SELF); no Bayesian optimization or neural architecture search was employed.

### IV.4 Deployment Limitations

1. The system architecture (LC-2025-Yesmukhamedov-01) is a conceptual design documented via UML diagrams. No functional prototype exists.
2. No real-time inference benchmarks on edge devices or mobile platforms have been reported.
3. Telemedicine and portable device deployment projections (LC-2025-Yesmukhamedov-01, pp. 87–88) are based on external benchmarks and Kazakhstan-specific statistics, not on experiments conducted within this dissertation.
4. GDPR/HIPAA compliance is stated as a design requirement but has not been validated through compliance testing or certification.

---

## V. EVIDENCE HIERARCHY

### V.1 Primary Evaluation Metrics

| Metric | Definition | Priority |
|--------|-----------|----------|
| F1-Score (macro-averaged) | Harmonic mean of precision and recall, averaged across all five DR classes equally | Highest |
| ROC-AUC | Area under the Receiver Operating Characteristic curve | Highest |

### V.2 Secondary Evaluation Metrics

| Metric | Definition | Priority |
|--------|-----------|----------|
| Precision (per-class and macro) | TP / (TP + FP) | Secondary |
| Recall (per-class and macro) | TP / (TP + FN) | Secondary |
| Accuracy | (TP + TN) / (TP + FP + TN + FN) | Secondary |
| Cohen's Kappa (quadratic weights) | κ = 1 − (Σ w_{i,j}·O_{i,j}) / (Σ w_{i,j}·E_{i,j}), w_{i,j} = (i−j)²/(C−1)² | Secondary |
| Weighted Average (precision, recall, F1) | Class-size-weighted averages | Secondary |
| Training-validation loss convergence rate | Epochs to convergence; final loss values | Diagnostic |

### V.3 Empirical Dominance Criterion

A model configuration A is said to exhibit empirical dominance over configuration B if and only if:
1. A exceeds B on both primary metrics (F1-macro and ROC-AUC), AND
2. A exceeds B on at least two of the three secondary metrics (precision-macro, recall-macro, accuracy).

If A exceeds B on primary metrics but not secondary metrics, the result is reported as partial dominance with explicit qualification.

Identical accuracy with divergent F1/precision/recall (as observed in LC-SAPAKOVA-2025: both methods achieved accuracy = 0.80 but differed on F1 by +12 pp) does not constitute equivalence. Accuracy alone is insufficient for dominance claims under class imbalance.

### V.4 Sufficient Validation Criterion

A claim is considered sufficiently validated when:
1. Results are reported on a held-out test partition not used during training or hyperparameter selection.
2. Cross-validation with fixed folds has been performed to confirm stability.
3. Per-class metrics are reported alongside aggregated metrics to expose class-specific weaknesses.
4. The train-test performance gap is explicitly documented and analyzed.

A claim is NOT sufficiently validated if it relies only on training-set metrics, or if it is tested only on a dataset with fewer than 500 images, or if cross-validation has not been performed.

---

## VI. CLAIM FORMULATION CONSTRAINTS

### VI.1 Permissible Claim Types

| Claim Type | Template | Example |
|-----------|----------|---------|
| Comparative performance | "Configuration A achieved [metric] = [value] on [dataset partition], compared to [metric] = [value] for Configuration B." | "The enhanced model achieved validation accuracy of 91% compared to 88% for the baseline." |
| Conditional improvement | "Under [specified conditions], the proposed pipeline improved [metric] by [magnitude]." | "Under the specified preprocessing pipeline, validation accuracy improved from 71% to 86%." |
| Bounded applicability | "The proposed approach demonstrated [outcome] on [specific dataset] under [specific conditions]." | "The approach demonstrated F1=0.91 on APTOS 2019 binary classification with CLAHE preprocessing." |
| Acknowledged limitation | "The proposed approach has not been validated for [condition/dataset/scenario]." | "The model has not been validated on multi-center external datasets." |
| Methodological contribution | "The dissertation formalizes/specifies/evaluates [method] as applied to [domain]." | "The dissertation specifies a four-stage preprocessing pipeline for fundus image DR classification." |

### VI.2 Forbidden Claim Types

| Forbidden Type | Reason | Violation Example |
|---------------|--------|-------------------|
| Universal superiority | No exhaustive architecture comparison performed | "The proposed method outperforms all existing DR classification approaches." |
| Clinical validity | No clinical trial or regulatory validation conducted | "The system is ready for clinical deployment." |
| Unqualified generalization | Only within-dataset evaluation performed | "The model generalizes to real-world clinical imaging." |
| Causal attribution without isolation | Preprocessing and architecture changes were not independently varied in all experiments | "Preprocessing alone caused the accuracy improvement." |
| Performance extrapolation from different tasks | STARE (disease types) ≠ APTOS (severity grades) | "The 100% accuracy on STARE validates the approach for DR severity classification." |
| Claims of novelty without prior art review | Limited architecture comparison | "This is the first study to combine CLAHE with CNN for DR classification." |
| Projections stated as results | LC-2025-Yesmukhamedov-01 projections are not experimental results | "The system will reduce late-stage DR complications by 20–30%." |

---

## VII. SOURCE INTERPRETATION RULES

### VII.1 Anti-Amplification Rule

No source may be cited as providing stronger evidence than the source itself claims. Specifically:
1. If a source reports results on a dataset of N < 200 images (e.g., LC-AlTimemy-2021, STARE, 157 images), its findings must be qualified with the dataset size limitation.
2. If a source reports 100% accuracy on all metrics, the dissertation must note the small dataset size and potential overfitting risk when citing this result. The dissertation must not present such results as evidence of generalizable performance.
3. If a source reports projections or external benchmarks (e.g., LC-2025-Yesmukhamedov-01, pp. 87–88), these must be labeled as projections, not as results of the dissertation's own experiments.
4. If a source's conclusion overstates its empirical support (e.g., "results confirm the effectiveness" without quantitative validation, as in LC-Sapakova-2024-01, p. 7), the dissertation must cite only the specific evidence provided, not the conclusion.

### VII.2 Self-Citation Constraint

Four of six literature cards flag HIGH self-plagiarism risk (LC-SAPAKOVA-2025, LC-Sapakova-2024-01, LC-Yesmukhamedov-2025-SELF, LC-2025-Yesmukhamedov-01, LC-SAPAKOVA-2025-01). For all self-authored sources:
1. Every reuse of content must be explicitly attributed as prior own work.
2. No verbatim text may be reused without quotation marks and citation.
3. All methodological descriptions must be substantially expanded beyond the published versions.
4. All figures must be regenerated, not reproduced.
5. The dissertation must clearly state the relationship between each prior publication and the dissertation research.

### VII.3 Cross-Source Consistency Rule

When two or more sources report on the same experimental configuration (as LC-SAPAKOVA-2025 and LC-Yesmukhamedov-2025-SELF report identical metrics for EfficientNetB0 Methods 1 and 2):
1. The dissertation must identify and acknowledge the overlapping publication of results.
2. Metrics must be cited from one primary source, with cross-reference to the corroborating source.
3. Discrepancies between sources (e.g., LC-SAPAKOVA-2025-01 reports both precision 0.90/0.93 on p. 84 and precision 0.82 on p. 87) must be documented and resolved before citation.

### VII.4 Formula Verification Rule

If a source contains an apparent error in a standard formula (e.g., LC-AlTimemy-2021, Eq. 3: Sensitivity = TP/(TP+TN) instead of the standard TP/(TP+FN)), the dissertation must:
1. Use the standard, correct formulation.
2. Note the discrepancy when citing the source's evaluation methodology.
3. Not propagate the error.

### VII.5 Task Comparability Rule

Results from different classification tasks are not directly comparable. Specifically:
- STARE 5-disease-type classification (BDR, CRVO, CNV, PDR, Normal) ≠ APTOS 2019 5-severity-grade classification (DR 0–4).
- Binary classification metrics (classes 0/1 in LC-SAPAKOVA-2025-01, Figs. 4–5) ≠ five-class classification metrics from the same source's enhanced model specification.
- Cross-task comparisons may be presented only with explicit qualification of the task differences.

---

## VIII. THESIS VERSION CONTROL RULE

### VIII.1 Immutability of Literature Cards

Literature cards, once finalized, are immutable records of source extraction. If the thesis evolves (e.g., through addition of new experiments, modification of preprocessing parameters, or inclusion of additional architectures), the following rules apply:

1. **No retroactive alteration of literature cards.** Extraction blocks, relational positioning, and reusability assessments in existing cards must not be modified to fit revised thesis claims.
2. **New evidence requires new cards.** Any new source cited in the dissertation requires a new literature card following the same structured format.
3. **Thesis amendments require a version log.** Any change to Sections I (Central Thesis) or II (Core Hypothesis) of this Invariants Document must be recorded in a version log with: (a) date of amendment, (b) prior formulation, (c) revised formulation, (d) justification referencing specific new evidence, (e) list of literature cards affected.

### VIII.2 Claim-Evidence Traceability

Every claim in the dissertation must be traceable to:
1. At least one extraction block in a literature card (for claims supported by prior work), OR
2. The dissertation's own experimental results as documented in the experimental protocol (for novel empirical claims).

Claims that cannot be traced to either source are inadmissible.

---

## IX. DEPLOYMENT AND GENERALIZATION LIMITATIONS

### IX.1 Forbidden Extrapolations

1. **No extrapolation to untested datasets.** Classification performance reported on APTOS 2019 may not be stated or implied to hold for EyePACS, Messidor, IDRiD, or any other DR dataset unless explicitly tested.
2. **No extrapolation to untested imaging equipment.** The dataset-specific imaging characteristics (resolution, field of view, camera type) are not documented in the literature cards. Performance on images from portable devices (e.g., Fundus on Phone) is unknown and may not be assumed.
3. **No extrapolation to untested populations.** The APTOS 2019 dataset demographics are not specified. Performance on populations with different retinal pigmentation, age distributions, or diabetes prevalence profiles is unknown.
4. **No extrapolation from architecture to architecture.** Results obtained with the enhanced 4-layer CNN may not be attributed to EfficientNetB0 or ResNet50, and vice versa, unless the same experiment is conducted on each architecture.
5. **No extrapolation from simulation to clinical practice.** Laser-tissue interaction modeling results (LC-Sapakova-2024-01) are computational simulations without experimental validation. They may not be cited as evidence of clinical therapeutic efficacy.

### IX.2 Permitted Generalization Statements

1. "The results suggest that preprocessing improves CNN classification on the tested dataset" — permitted, as conditional and bounded.
2. "Further validation on external datasets is required to assess generalizability" — permitted and required.
3. "The system architecture is designed to be modular and scalable" — permitted only as a design attribute, not as a validated operational characteristic.
4. "The approach was demonstrated under hardware constraints consistent with resource-limited settings" — permitted only with explicit acknowledgment that this refers to training hardware limitations, not deployment testing.

### IX.3 Mandatory Qualification Statements

The dissertation must include the following qualifications in its discussion and conclusion chapters:

1. All reported metrics are dataset-specific and do not constitute evidence of generalization beyond the tested data partitions.
2. The class imbalance in the training data (Class 0: 73.5%; Classes 3–4: < 5% combined) limits the reliability of per-class metrics for severe and proliferative DR stages.
3. The supplementary clinical dataset has not been independently validated for labeling consistency or distributional compatibility with APTOS 2019.
4. The system architecture (Chapter 6) is a conceptual design without prototype implementation or empirical validation.
5. Hardware constraints during training (overheating, limited epochs) may have prevented the models from reaching full convergence potential.

---

*End of Invariants Document.*

*This document governs the epistemic structure of the dissertation. All literature review sections, experimental interpretations, discussion claims, and conclusion statements must conform to the constraints defined herein.*
