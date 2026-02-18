# ARGUMENT MAP

## Dissertation: Integrated Preprocessing-CNN Pipeline for Automated Diabetic Retinopathy Diagnosis in Resource-Limited Environments

---

## I. MAIN THESIS NODE

**Thesis Formulation:**

Systematic improvement of input data quality through an integrated preprocessing pipeline (resizing, normalization, CLAHE, data augmentation) has a greater impact on CNN-based diabetic retinopathy diagnostic performance than increases in model architectural complexity alone, and the integration of this pipeline with convolutional neural networks within a modular system architecture constitutes a clinically applicable approach for automated five-class DR screening deployable in resource-limited healthcare environments.

**Thesis Components:**
- (T1) Preprocessing quality is the primary performance driver over architectural complexity.
- (T2) Integration of preprocessing with CNN as a unified pipeline yields improved diagnostic accuracy.
- (T3) The approach is deployable in resource-limited environments via modular system architecture.

---

## II. PRIMARY CLAIMS (Level 1)

---

### PC-1: Preprocessing Dominance

- **Formal Statement:** The diagnostic effectiveness of CNN models for automated DR classification depends more on the quality of input images (as improved by systematic preprocessing) than on architectural complexity alone.
- **Claim Type:** Empirical
- **Required Evidence Type:** Comparative experimental results showing accuracy gains from preprocessing exceeding gains from architectural changes; ablation study isolating preprocessing contribution.
- **Dependency:** None (foundational claim)

---

### PC-2: Unified Pipeline Integration

- **Formal Statement:** Integration of image enhancement methods (resizing, normalization, CLAHE, data augmentation) with CNN classification as a formalized, unified pipeline significantly improves diagnostic accuracy and generalization compared to CNN classification without such preprocessing.
- **Claim Type:** Methodological / Empirical
- **Required Evidence Type:** Quantitative comparison of baseline CNN (no preprocessing) vs. enhanced CNN (with preprocessing pipeline) on identical datasets using multi-metric evaluation.
- **Dependency:** Depends on PC-1 (preprocessing dominance must hold for pipeline integration to be justified as the primary design principle).

---

### PC-3: Modified CLAHE with Simplified Threshold Control

- **Formal Statement:** A modified CLAHE algorithm with controllable threshold parameters improves feature preservation (microaneurysms, small vessels) in fundus images under variable quality conditions, and this improvement translates to measurably better CNN classification performance on small and imbalanced datasets.
- **Claim Type:** Methodological / Empirical
- **Required Evidence Type:** Threshold sensitivity analysis; image quality metrics before/after CLAHE; per-class performance comparison with and without CLAHE on APTOS 2019 and STARE datasets.
- **Dependency:** Depends on PC-1 and PC-2 (CLAHE is a component within the preprocessing pipeline whose dominance and integration are asserted by PC-1 and PC-2).

---

### PC-4: Two-Stage Fine-Tuning Strategy

- **Formal Statement:** A two-stage transfer learning adaptation strategy — initially freezing base layers and training only the classification head, followed by unfreezing and fine-tuning upper layers — yields superior classification performance (Precision, Recall, F1-Score, Cohen's Kappa) compared to a fully frozen strategy, for both EfficientNetB0 and ResNet50 architectures on five-class DR classification tasks.
- **Claim Type:** Empirical
- **Required Evidence Type:** Quantitative comparison of frozen vs. progressive fine-tuning strategies across multiple metrics and architectures; per-class performance analysis under class imbalance; overfitting analysis (train-test performance gap).
- **Dependency:** Depends on PC-2 (fine-tuning is evaluated within the context of the unified pipeline; preprocessing is held constant across fine-tuning comparisons).

---

### PC-5: Resource-Efficient Deployment

- **Formal Statement:** The proposed preprocessing-CNN pipeline achieves clinically meaningful diagnostic performance under limited computational resources without requiring complex or resource-intensive architectures, making it suitable for deployment in resource-limited healthcare environments.
- **Claim Type:** Empirical / System-level
- **Required Evidence Type:** Performance metrics achieved under documented hardware constraints; comparison of performance-to-complexity ratios across architectures; processing time measurements.
- **Dependency:** Depends on PC-1, PC-2, PC-4 (resource efficiency is meaningful only if the pipeline and fine-tuning strategy are validated as effective).

---

### PC-6: Laser-Tissue Interaction Modeling

- **Formal Statement:** Mathematical modeling of laser-tissue thermal interaction (coupled thermal-optical model) in fundus tissue provides a theoretical framework for understanding diagnostic image feature characteristics resulting from prior laser coagulation treatment, and supports optimization of laser parameters for DR therapy.
- **Claim Type:** Theoretical
- **Required Evidence Type:** Mathematical formulation (heat conduction equation, Beer-Lambert law, Gaussian beam model); numerical simulation results showing differential temperature distribution across tissue layers.
- **Dependency:** Independent of PC-1 through PC-5 (parallel theoretical component); conditionally linked to PC-2 via image feature interpretation.

---

### PC-7: System Architecture for Clinical Integration

- **Formal Statement:** A modular, scalable AI-driven information system architecture — integrating PACS, EHR, cloud services, AI processing modules, telemedicine capabilities, and physician-in-the-loop decision support — provides an implementable framework for deploying the proposed DR screening pipeline in Kazakhstan's healthcare infrastructure.
- **Claim Type:** System-level
- **Required Evidence Type:** Architectural specification (UML diagrams, component specifications, ER model); comparative analysis with existing AI systems (IDx-DR, Eyenuk, DeepMind); functional and non-functional requirements specification; regulatory compliance framework (GDPR/HIPAA).
- **Dependency:** Depends on PC-2 and PC-5 (the AI processing module implements the validated preprocessing-CNN pipeline under resource constraints).

---

## III. SUB-CLAIMS (Level 2)

---

### SC-1.1: Preprocessing raises baseline CNN accuracy

- **Formal Statement:** Application of the preprocessing pipeline (resize, normalization, CLAHE, augmentation) to fundus images improves baseline CNN validation accuracy from 71% to 86%.
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-01
  - Dissertation Section: §4.2 (Experiment 1)
  - Dataset: APTOS 2019 + supplementary clinical images
  - Metric: Validation accuracy (71% → 86%)
- **Boundary Conditions:** Measured on a specific dataset composition; improvement magnitude may vary with dataset characteristics and image acquisition conditions.

---

### SC-1.2: Enhanced model with preprocessing outperforms baseline without preprocessing

- **Formal Statement:** The enhanced CNN (4 convolutional layers, 32–256 filters, batch normalization, dropout, 512×512 input with preprocessing) achieves 91% validation accuracy vs. 88% for the baseline model (2 convolutional blocks, 256×256 input, no CLAHE).
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-01, EB-LC-SAPAKOVA-2025-01-03
  - Dissertation Section: §4.2.2
  - Dataset: APTOS 2019 + supplementary clinical data (25,000 labeled retinal images)
  - Metrics: Validation accuracy (91% vs. 88%); ROC-AUC = 0.9638; F1-score (0.91 vs. 0.87–0.89)
- **Boundary Conditions:** Enhanced model uses both preprocessing and increased architectural complexity; the contribution of preprocessing vs. architecture is not fully isolated in this comparison alone (requires ablation study SC-1.3).

---

### SC-1.3: Ablation study confirms preprocessing as primary performance driver

- **Formal Statement:** Ablation study demonstrates that removal of preprocessing components degrades classification performance more than reduction of architectural complexity.
- **Evidence Reference:**
  - Dissertation Section: §5.2.1 (Ablation Study: Preprocessing Components versus Architectural Complexity), §5.2.2 (Quantitative Evidence for Image Quality as Primary Performance Driver)
  - Dataset: APTOS 2019
  - Metrics: Accuracy, F1-Score, ROC-AUC with and without individual preprocessing stages
- **Boundary Conditions:** Ablation results are bounded by the specific architectures tested (baseline CNN, enhanced CNN, EfficientNetB0, ResNet50) and the specific datasets used.

---

### SC-2.1: Pipeline stage specification

- **Formal Statement:** The unified preprocessing pipeline consists of four formalized stages: (1) resizing (256×256 or 512×512 via cubic interpolation), (2) normalization (pixel values to [0,1]), (3) CLAHE enhancement (clip limit 2.0, grid size 8×8), (4) data augmentation (horizontal/vertical flips, ±15° rotation, ±10% zoom, brightness variation).
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-02
  - Literature Card: LC-SAPAKOVA-2025 (CONF), EB-02
  - Dissertation Section: §3.1.1
- **Boundary Conditions:** Parameter values (clip limit, grid size, augmentation ranges) are optimized for APTOS 2019 image characteristics; transferability to other fundus image corpora requires validation.

---

### SC-2.2: Preprocessing improves classification with and without CLAHE

- **Formal Statement:** CNN classification accuracy with the CV2/CLAHE preprocessing pipeline reaches 91% (precision 0.90/0.93, recall 0.93/0.90, F1-score 0.91) compared to 88% without preprocessing (precision 0.91/0.85, recall 0.83/0.92, F1-score 0.87/0.89).
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-04
  - Dissertation Section: §4.2.2
  - Dataset: APTOS 2019 + supplementary data
  - Metrics: Accuracy, Precision, Recall, F1-score per class; Confusion matrices
- **Boundary Conditions:** Comparison performed using binary classification (classes 0 and 1); relationship to full five-class performance requires separate evaluation.

---

### SC-3.1: Modified CLAHE threshold sensitivity

- **Formal Statement:** The CLAHE threshold parameter affects classification performance in a measurable and non-trivial manner, with optimal threshold values improving feature visibility (particularly for microaneurysms and small vessels) on small datasets.
- **Evidence Reference:**
  - Literature Card: LC-AlTimemy-2021, EB-01 (upgraded CLAHE with T/80 formulation; image quality score: conventional CLAHE = 33.2284 vs. upgraded CLAHE T/80 = 34.3483)
  - Dissertation Section: §4.3 (Experiment 2: Modified CLAHE Threshold Optimization on Small Datasets), §4.3.1, §4.3.2
  - Dataset: APTOS 2019, STARE
  - Metrics: Image quality scores; downstream classification accuracy by threshold value
- **Boundary Conditions:** The T/80 optimality was determined on STARE (157 images, 5 disease types); generalizability to APTOS 2019 (3,662 images, 5 DR severity grades) requires independent validation. The classification task differs (multi-disease vs. DR severity grading).

---

### SC-3.2: CLAHE preserves diagnostically relevant features

- **Formal Statement:** CLAHE with appropriate threshold control improves local contrast in darker fundus regions, enhancing visibility of pathological features without introducing artifacts, particularly improving visibility of tiny veins.
- **Evidence Reference:**
  - Literature Card: LC-AlTimemy-2021, EB-01 ("improved the image distinctiveness, especially the tiny veins")
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-02 ("improves local contrast, especially in darker regions of the fundus, enhancing the visibility of pathological features without introducing artifacts")
  - Dissertation Section: §4.3.2
- **Boundary Conditions:** Feature preservation claims are qualitative in both sources; no formal pathological feature detection metric (e.g., microaneurysm detection rate) is reported.

---

### SC-4.1: EfficientNetB0 frozen vs. progressive fine-tuning

- **Formal Statement:** For EfficientNetB0 on five-class DR classification, progressive fine-tuning (Method 2) achieves Test Precision = 0.75, Recall = 0.74, F1-Score = 0.74, Macro Average = 0.77, Weighted Average = 0.81, compared to frozen strategy (Method 1): Precision = 0.65, Recall = 0.60, F1-Score = 0.62, Macro Average = 0.72, Weighted Average = 0.74.
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025 (CONF), EB-01
  - Literature Card: LC-Yesmukhamedov-2025-SELF, EB-LC-Yesmukhamedov-2025-SELF-02
  - Dissertation Section: §4.4.1
  - Dataset: APTOS 2019 + supplementary (35,126 training, 3,662 test images)
  - Metrics: Precision, Recall, F1-Score, Macro Average, Weighted Average (all from Table 3 of CONF source)
- **Boundary Conditions:** Overall accuracy remained constant at 0.80 for both methods; improvement is visible only in class-sensitive metrics. Evidence of remaining overfitting: training F1 = 0.86 (Method 2) vs. test F1 = 0.74.

---

### SC-4.2: Fine-tuning reduces overfitting

- **Formal Statement:** Progressive fine-tuning reduces the train-test F1 gap compared to the frozen strategy: Method 2 training F1 = 0.86, test F1 = 0.74 (gap = 0.12) vs. Method 1 training F1 = 0.87, test F1 = 0.62 (gap = 0.25).
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025 (CONF), EB-04
  - Literature Card: LC-Yesmukhamedov-2025-SELF, EB-LC-Yesmukhamedov-2025-SELF-03
  - Dissertation Section: §4.4.1
  - Metrics: Train F1 vs. Test F1 gap
- **Boundary Conditions:** Overfitting is reduced but not eliminated. Source acknowledges "additional data and interpretive improvements are needed to ensure overall model stability."

---

### SC-4.3: ResNet50 transfer learning performance

- **Formal Statement:** ResNet50 with transfer learning achieves high classification accuracy on retinal disease classification tasks, with fine-tuned ResNet50 outperforming feature-extraction-only approaches.
- **Evidence Reference:**
  - Literature Card: LC-AlTimemy-2021, EB-02 (RESNET50 achieved 100% accuracy on STARE with upgraded CLAHE preprocessing)
  - Dissertation Section: §4.4.2
  - Dataset: STARE (157 images, augmented to 960); dissertation uses APTOS 2019
  - Metrics: Accuracy, Sensitivity, Specificity
- **Boundary Conditions:** 100% accuracy on STARE raises overfitting concerns due to small, augmented dataset. Performance on STARE (5 disease types) is not directly comparable to APTOS 2019 (5 DR severity grades). The sensitivity formula in the source (Eq. 3: TP/(TP+TN)) contains an apparent error vs. standard TP/(TP+FN).

---

### SC-5.1: EfficientNetB0 computational efficiency

- **Formal Statement:** EfficientNetB0 provides a high accuracy-to-computation ratio, making it suitable for resource-limited deployment.
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025 (CONF), EB-05 ("high accuracy-to-computation ratio, providing an optimal balance between performance and computational efficiency")
  - Dissertation Section: §3.3.1
- **Boundary Conditions:** No explicit computational cost comparison across architectures is provided in the sources reviewed. The efficiency claim is based on architectural properties, not measured FLOPs or inference time comparison.

---

### SC-5.2: Performance achieved under hardware constraints

- **Formal Statement:** The enhanced CNN model achieves improved classification results (91% validation accuracy) even under documented hardware constraints (overheating limiting epoch count).
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-05
  - Dissertation Section: §4.1.3, §5.4
  - Metric: Validation accuracy achieved within 35–40 epochs before hardware-imposed termination
- **Boundary Conditions:** Hardware constraints are documented as a limitation, not a controlled experimental variable. The source acknowledges "further gains are possible with extended computational resources."

---

### SC-5.3: Processing time comparison

- **Formal Statement:** Preprocessing with CV2/CLAHE achieves faster per-step processing time (1s 108ms/step) compared to without preprocessing (8s 986ms/step).
- **Evidence Reference:**
  - Literature Card: LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-04
  - Dissertation Section: §4.2, §5.2
  - Metric: Processing time per step
- **Boundary Conditions:** Processing time difference may be attributed to input resolution differences (512×512 with preprocessing vs. 256×256 baseline); the metric conflates preprocessing pipeline efficiency with model inference time.

---

### SC-6.1: Thermal model mathematical formulation

- **Formal Statement:** The coupled thermal-optical model for laser-tissue interaction in fundus tissue is described by: Beer's law for laser attenuation (I(r,z) = I₀(r)e^(−∫β(r,ξ)dξ)), energy balance equation (ΔV·Co·ΔT = W·Δt), Gaussian beam profile (I₀(r) = (P/πa²)e^(−(r/a)²)), and heat conduction equation (Coσ∂T/∂t = div(k·grad(T))).
- **Evidence Reference:**
  - Literature Card: LC-Sapakova-2024-01, EB-01 (Equations 1–8)
  - Dissertation Section: §2.4.1
- **Boundary Conditions:** Model assumes static tissue optical/thermal properties; no blood perfusion term; homogeneous properties within each layer; no experimental validation against clinical data.

---

### SC-6.2: Differential temperature distribution across tissue layers

- **Formal Statement:** Numerical simulation demonstrates that surface tissue layers (cornea) absorb laser energy faster than deeper layers (choroid, retina), with temperature stabilizing in deep layers after initial exposure.
- **Evidence Reference:**
  - Literature Card: LC-Sapakova-2024-01, EB-02 (Figures 2–5)
  - Dissertation Section: §2.4.2
- **Boundary Conditions:** Results are qualitative only; no specific numerical temperature values reported. Simulation uses assumed parameters without specified sources.

---

### SC-7.1: Modular system architecture specification

- **Formal Statement:** The proposed system architecture comprises modular components: Image Capture, Image Processing, Recognition Model, Diagnosis, Reporting, User Interface, Data Storage, Error Handling, and Security, with PACS and EHR integration via FHIR/HL7 standards.
- **Evidence Reference:**
  - Literature Card: LC-2025-Yesmukhamedov-01, EB-02 (Tables 2–3, Fig. 1)
  - Dissertation Section: §6.1, §6.2
- **Boundary Conditions:** No prototype implementation or testing reported. Architecture is conceptual/specified but not empirically validated.

---

### SC-7.2: Comparative positioning against existing systems

- **Formal Statement:** Existing AI-based DR screening systems (IDx-DR, Eyenuk, DeepMind, Orbis Cybersight AI, etc.) have identified limitations including: restriction to single diseases, requirement for advanced imaging equipment, limited adoption in non-English-speaking regions, and dependency on internet connectivity.
- **Evidence Reference:**
  - Literature Card: LC-2025-Yesmukhamedov-01, EB-01 (Table 1)
  - Dissertation Section: §1.4, §5.3.1
- **Boundary Conditions:** Comparative analysis is qualitative; no direct quantitative benchmarking of the proposed system against these systems using identical datasets.

---

### SC-7.3: Kazakhstan deployment context

- **Formal Statement:** Kazakhstan's healthcare infrastructure context — approximately 1,200 ophthalmologists, ~40% rural population, ~70% of rural residents with limited eye care access, ~8% adult diabetes prevalence — justifies the need for resource-efficient automated DR screening.
- **Evidence Reference:**
  - Literature Card: LC-2025-Yesmukhamedov-01, EB-03
  - Dissertation Section: §1.1.2, §6.3.1, §6.4.2
- **Boundary Conditions:** Statistics are derived from external sources (IDF Diabetes Atlas 2021) and are projections. Actual deployment feasibility depends on infrastructure investment, regulatory approval, and clinician training not addressed experimentally.

---

### SC-7.4: Physician-in-the-loop decision support

- **Formal Statement:** The proposed system operates within a physician-in-the-loop paradigm, incorporating a Doctor-AI Feedback Loop where clinicians can request clarification or corrections from the AI model.
- **Evidence Reference:**
  - Literature Card: LC-2025-Yesmukhamedov-01, EB-05
  - Dissertation Section: §6.3.2
- **Boundary Conditions:** Conceptual framework only; no user studies, clinical trials, or interface prototyping reported.

---

### SC-7.5: Data security and regulatory compliance

- **Formal Statement:** The proposed system architecture includes security components (encryption, authentication, security gateway) aligned with GDPR and HIPAA requirements.
- **Evidence Reference:**
  - Literature Card: LC-2025-Yesmukhamedov-01, EB-04
  - Dissertation Section: §6.4.1
- **Boundary Conditions:** Compliance is stated as a design requirement, not demonstrated through audit, certification, or penetration testing.

---

## IV. COUNTER-ARGUMENTS AND LIMITATIONS

---

### For PC-1 (Preprocessing Dominance):

- **Counter-argument:** Preprocessing and architectural changes are not fully isolated in the primary experiments. The enhanced model uses both preprocessing and increased architectural complexity (4 conv layers, batch normalization, dropout, larger input resolution) simultaneously.
  - **Source:** LC-SAPAKOVA-2025-01, §II.7, Assumption 3; SC-1.2 boundary conditions.
  - **Conditions under which claim fails:** If the ablation study (§5.2.1) shows that architectural improvements contribute equally or more than preprocessing to performance gains.

- **Counter-argument:** The preprocessing pipeline's impact has not been independently validated across diverse clinical imaging conditions (different cameras, lighting, patient demographics).
  - **Source:** LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-06 ("The model was trained primarily on high-quality images... does not fully capture the variability of retinal images in real clinical practice").
  - **Conditions under which claim fails:** If cross-database generalization testing (§5.1) reveals that preprocessing gains do not transfer to heterogeneous image sources.

---

### For PC-2 (Unified Pipeline Integration):

- **Counter-argument:** The source reporting the most comprehensive pipeline evaluation (LC-SAPAKOVA-2025-01) shows an internal metric inconsistency: conclusion reports precision 0.82, recall 0.85, F1-score 0.83, while main results report higher values (precision 0.90/0.93, recall 0.93/0.90, F1-score 0.91).
  - **Source:** LC-SAPAKOVA-2025-01, §IV Relational Positioning.
  - **Conditions under which claim fails:** If the lower values represent the multiclass evaluation and the higher values are binary-only, the pipeline's effectiveness for five-class DR grading is weaker than initially reported.

- **Counter-argument:** The pipeline lacks standardized external benchmarking. No direct comparison is made on identical datasets and identical metrics against published systems (IDx-DR sensitivity 96%, specificity 93%).
  - **Source:** LC-2025-Yesmukhamedov-01, EB-03 (external benchmarks cited but not replicated).

---

### For PC-3 (Modified CLAHE):

- **Counter-argument:** The CLAHE threshold optimality (T/80) was established on a different dataset (STARE, 157 images, 5 disease types) and a different classification task than the dissertation's primary evaluation (APTOS 2019, 3,662 images, 5 DR severity grades).
  - **Source:** LC-AlTimemy-2021, §II.7, Assumption 4.
  - **Conditions under which claim fails:** If CLAHE parameter sensitivity analysis on APTOS 2019 (§4.3.1) yields a different optimal threshold, undermining the claim of a generalizable modified CLAHE approach.

- **Counter-argument:** Feature preservation claims (microaneurysms, small vessels) are qualitative in all sources reviewed; no quantitative pathological feature detection metric is provided.
  - **Source:** LC-AlTimemy-2021, EB-01; LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-02.

---

### For PC-4 (Two-Stage Fine-Tuning):

- **Counter-argument:** Overall accuracy (0.80) remained identical for both frozen and fine-tuned strategies; the improvement is visible only in class-sensitive metrics (Precision, Recall, F1-Score).
  - **Source:** LC-SAPAKOVA-2025 (CONF), EB-01.
  - **Conditions under which claim fails:** If accuracy is adopted as the primary metric (which the sources argue against due to class imbalance), the fine-tuning strategy shows no improvement.

- **Counter-argument:** Only EfficientNetB0 was evaluated for two-stage fine-tuning in the published self-authored sources; alternative architectures (ResNet, VGG, DenseNet) were explicitly deferred to future work.
  - **Source:** LC-SAPAKOVA-2025 (CONF), §II.6; LC-Yesmukhamedov-2025-SELF, §II.7.
  - **Conditions under which claim fails:** If ResNet50 fine-tuning results (§4.4.2) do not replicate the same pattern of improvement.

---

### For PC-5 (Resource-Efficient Deployment):

- **Counter-argument:** Hardware constraints are documented as a limitation encountered during research, not as a controlled experimental variable simulating real deployment conditions.
  - **Source:** LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-05 ("Hardware constraints prevented longer training durations. Due to overheating during extended training, the number of epochs was limited").
  - **Conditions under which claim fails:** If performance is substantially lower when genuinely deployed on target hardware (portable devices, edge devices) in clinical settings.

- **Counter-argument:** No formal deployment testing on actual resource-limited clinical hardware (portable retinal cameras, mobile devices, edge computing) is reported.
  - **Source:** LC-SAPAKOVA-2025-01, EB-LC-SAPAKOVA-2025-01-05 ("Deployment challenges such as real-time inference on edge devices or in mobile applications should be addressed").

---

### For PC-6 (Laser-Tissue Interaction Modeling):

- **Counter-argument:** The thermal model has no experimental validation against clinical or laboratory data. All results are computational simulations with assumed parameter values.
  - **Source:** LC-Sapakova-2024-01, §II.5, §II.6 ("further research and experiments are required").
  - **Conditions under which claim fails:** If model predictions diverge significantly from clinical observations of laser coagulation effects on retinal tissue.

- **Counter-argument:** The model omits blood perfusion (Pennes bioheat equation term), assumes static tissue properties, and uses homogeneous layer approximation despite acknowledging tissue inhomogeneity.
  - **Source:** LC-Sapakova-2024-01, §II.7, Assumptions 1–4.

---

### For PC-7 (System Architecture):

- **Counter-argument:** The system architecture is entirely conceptual; no prototype implementation, user testing, or operational validation is reported.
  - **Source:** LC-2025-Yesmukhamedov-01, §II.5, §II.7.
  - **Conditions under which claim fails:** If implementation reveals unforeseen integration challenges, performance bottlenecks, or incompatibility with Kazakhstan's existing healthcare IT infrastructure.

- **Counter-argument:** Published performance metrics of referenced AI systems (IDx-DR sensitivity 96%, specificity 93%) may not be transferable to the Kazakhstan context due to dataset differences, population-specific variation, and regulatory requirements.
  - **Source:** LC-2025-Yesmukhamedov-01, §II.7, Assumption 3.

---

## V. CLAIM DEPENDENCY STRUCTURE

```
PC-1 (Preprocessing Dominance)
  ├── PC-2 (Unified Pipeline) depends on PC-1
  │     ├── PC-3 (Modified CLAHE) depends on PC-1, PC-2
  │     └── PC-4 (Two-Stage Fine-Tuning) depends on PC-2
  │           └── PC-5 (Resource-Efficient Deployment) depends on PC-1, PC-2, PC-4
  │                 └── PC-7 (System Architecture) depends on PC-2, PC-5
  └── (provides theoretical grounding for all downstream claims)

PC-6 (Laser-Tissue Modeling) — Independent
  └── Conditionally linked to PC-2 via §2.4.2 (image feature interpretation)
```

**Formal Dependencies:**

1. PC-2 depends on PC-1: The unified pipeline design is justified by the claim that preprocessing is the primary performance driver.
2. PC-3 depends on PC-1 and PC-2: Modified CLAHE is a component within the pipeline whose overall dominance (PC-1) and integration (PC-2) must hold.
3. PC-4 depends on PC-2: Fine-tuning strategy is evaluated within the pipeline context; preprocessing is held constant.
4. PC-5 depends on PC-1, PC-2, PC-4: Resource efficiency is meaningful only if the pipeline and strategies it implements are validated.
5. PC-7 depends on PC-2 and PC-5: System architecture implements the validated pipeline under resource constraints.
6. PC-6 is independent but conditionally linked to PC-2 via diagnostic image feature interpretation (§2.4.2).

---

## VI. CLAIM STRENGTH CLASSIFICATION

---

### PC-1: Preprocessing Dominance — **Moderate**

- **Justification:** Direct empirical evidence shows accuracy improvement from preprocessing (71% → 86%, 88% → 91%); however, preprocessing and architectural changes are not fully isolated in primary experiments. Claim strength depends on ablation study (§5.2.1) not yet available from external published sources. Two independent self-authored publications (LC-SAPAKOVA-2025-01, LC-SAPAKOVA-2025 CONF) provide supporting data.

---

### PC-2: Unified Pipeline Integration — **Strong**

- **Justification:** Multiple published sources (LC-SAPAKOVA-2025-01, LC-SAPAKOVA-2025 CONF, LC-Yesmukhamedov-2025-SELF) provide convergent evidence that the pipeline improves performance. External source (LC-AlTimemy-2021) independently demonstrates that CLAHE + transfer learning pipeline achieves high accuracy. Pipeline specification is documented with exact parameters. ROC-AUC = 0.9638 provides robust single-metric validation.

---

### PC-3: Modified CLAHE — **Conditional**

- **Justification:** CLAHE threshold optimization evidence comes primarily from an external source (LC-AlTimemy-2021) using a different dataset (STARE) and different classification task (multi-disease vs. DR severity). Dissertation-specific threshold sensitivity analysis (§4.3) is required but not yet published. Feature preservation claims are qualitative.

---

### PC-4: Two-Stage Fine-Tuning — **Strong**

- **Justification:** Direct empirical validation with quantified improvements (+10 pp Precision, +14 pp Recall, +12 pp F1-Score) from two self-authored publications (LC-SAPAKOVA-2025 CONF, LC-Yesmukhamedov-2025-SELF) with consistent results. Overfitting reduction is quantified (train-test F1 gap reduced from 0.25 to 0.12). Limited to EfficientNetB0 in published sources; ResNet50 comparison (§4.4.2) is pending.

---

### PC-5: Resource-Efficient Deployment — **Conditional**

- **Justification:** Performance under hardware constraints is documented but as an incidental limitation, not a controlled experiment. No formal deployment testing on target hardware. Processing time comparison exists but may be confounded by resolution differences. EfficientNetB0 efficiency rationale is architectural, not empirically benchmarked in the sources.

---

### PC-6: Laser-Tissue Interaction Modeling — **Conditional**

- **Justification:** Mathematical formulation is complete and published (LC-Sapakova-2024-01). Simulation results are qualitative only (no numerical temperature values). No experimental validation against clinical data. Model omits key physical factors (blood perfusion, dynamic tissue properties).

---

### PC-7: System Architecture — **Conditional**

- **Justification:** Architecture is specified in detail (UML diagrams, ER model, component tables, DMP taxonomy) in a published source (LC-2025-Yesmukhamedov-01). Comparative analysis with existing systems is provided. However, no prototype implementation, no empirical validation, no user testing, and no deployment in actual clinical settings are reported. Kazakhstan-specific statistics support the deployment rationale but are projections.

---

## VII. NON-CLAIMS (Explicitly Not Argued)

1. The dissertation does not claim that the proposed system has been clinically validated in a real healthcare setting or received regulatory approval.

2. The dissertation does not claim superiority over all existing commercial DR screening systems (IDx-DR, Eyenuk, DeepMind) on identical benchmarks.

3. The dissertation does not claim that EfficientNetB0 or ResNet50 is the optimal architecture for DR classification in absolute terms; it evaluates these as representative architectures within the pipeline framework.

4. The dissertation does not claim that the modified CLAHE threshold parameter (T/80 or clip limit 2.0) is universally optimal across all fundus image datasets.

5. The dissertation does not claim that the laser-tissue thermal model has been experimentally validated against clinical or laboratory measurements.

6. The dissertation does not claim that the proposed system architecture has been implemented as a functioning prototype.

7. The dissertation does not claim resolution of the class imbalance problem; it documents mitigation strategies (weighted loss, augmentation) and acknowledges remaining limitations.

8. The dissertation does not claim that model interpretability has been addressed (Grad-CAM, SHAP, or equivalent explainability tools are identified as future work).

9. The dissertation does not claim generalizability to non-APTOS, non-STARE fundus image populations without additional cross-database validation.

10. The dissertation does not argue that the five-class APTOS classification scheme is clinically superior to alternative DR grading systems (e.g., ETDRS).

---

*Argument Map constructed from: 6 Literature Cards (LC-SAPAKOVA-2025, LC-Sapakova-2024-01, LC-Yesmukhamedov-2025-SELF, LC-2025-Yesmukhamedov-01, LC-AlTimemy-2021, LC-SAPAKOVA-2025-01) and approved Table of Contents.*
