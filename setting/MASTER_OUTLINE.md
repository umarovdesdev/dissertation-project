# MASTER OUTLINE
## Doctoral Dissertation: Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Master Structural Outline — Chapter-by-Chapter Content Specification
**Binding References:** DISSERTATION_INVARIANTS.md v.1.0 | ARGUMENT_MAP.md | GLOSSARY_v1_0.md | TABLE_OF_CONTENT.pdf
**Source Corpus:** LC-CONF | LC-KBTU | LC-KazUTB | LC-NAN_RK | LC-SQOPUS_Q2 | LC-SQOPUS_Q3
**Governing Documents:** CENTRAL_THESIS.md | CORE_OBJECTIVE.md | HYPOTHESIS.md

---

## FRONT MATTER

### Normative References
- List of standards governing dissertation format, terminology, and citation practice.

### Definitions
- Source: GLOSSARY_v1_0.md, Part A (Structured Glossary Table).
- All operationally defined terms (OD-1 through OD-6 per INVARIANTS §III) must appear here with verbatim definitions.
- Terminological stabilization recommendations (GLOSSARY §6) must be applied: canonical fine-tuning terminology, disambiguation of "feature extraction," "generalization," and "preprocessing" per Priority 1 items.

### Designations and Abbreviations
- CNN, CLAHE, DR, ROC-AUC, APTOS, STARE, EHR, PACS, HIPAA, GDPR, UML.
- Standardize: "EHR" (not "EMR"); "ResNet50" (not "RESNET50"); "EfficientNetB0" consistently (GLOSSARY §6, items 5, 7).

---

## INTRODUCTION

### Relevance of the Research
- **Medical context:** Diabetic retinopathy as a leading cause of preventable blindness; global prevalence data (IDF Diabetes Atlas 2021, cited via LC-NAN_RK, p. 86–87).
- **Kazakhstan-specific framing:** ~1,200 ophthalmologists serving the entire population; >40% rural residents with limited access to specialized care (LC-NAN_RK, p. 74, 77, 86–87).
- **Technical gap:** Suboptimal performance of baseline CNNs under variable image quality; absence of unified preprocessing-classification frameworks optimized for resource-limited environments (LC-SQOPUS_Q3, p. 81).
- **Boundary:** Projected deployment benefits (20–30% late-stage DR reduction; 15–20% cost reduction) are third-party projections, not dissertation findings (INVARIANTS SB-1.6; ARGUMENT_MAP NC-3; SIR-8).

### Scientific Novelty
1. Integration of contrast-adaptive preprocessing (upgraded CLAHE with threshold control) into a CNN-based DR classification pipeline — as a unified framework, not isolated techniques (LC-SQOPUS_Q3, p. 81; LC-SQOPUS_Q2, §1).
2. Two-stage fine-tuning protocol for EfficientNetB0 tailored to fundus image variability (LC-CONF, p. 497; LC-KBTU, §II.1).
3. Mathematical modeling of laser-tissue interaction for retinal therapy with qualitative simulation (LC-KazUTB, §II.1) — bounded as theoretical contribution only (INVARIANTS SB-1.5; ARGUMENT_MAP PC-4).
4. Modular AI-driven system architecture for DR screening in resource-limited environments (LC-NAN_RK, §II.1) — bounded as design specification only (INVARIANTS SB-4.1; ARGUMENT_MAP PC-5).

### Research Goal
- Verbatim from CORE_OBJECTIVE.md: "To develop and experimentally validate an integrated fundus image enhancement and CNN-based classification framework for automated multi-stage diabetic retinopathy diagnosis, with specific emphasis on contrast-adaptive preprocessing (including upgraded CLAHE with threshold control) to improve microvascular feature visibility and classification robustness under variable image quality and constrained computational conditions."

### Research Objectives
1. Analyze the current state of automated DR diagnosis, fundus image quality variability, and deep learning approaches to retinal image classification (→ Chapter 1).
2. Formalize the mathematical foundations of image enhancement techniques and CNN-based classification, including CLAHE with controllable threshold parameters and transfer learning theory (→ Chapter 2).
3. Design a unified preprocessing pipeline (resizing → normalization → CLAHE → augmentation) and integrate it with baseline, enhanced, and transfer learning CNN architectures (→ Chapter 3).
4. Experimentally validate the preprocessing dominance hypothesis (H-1), CLAHE threshold sensitivity (H-2), and two-stage fine-tuning protocol (H-3) (→ Chapter 4).
5. Conduct reliability validation through cross-database generalization, ablation study, and comparative analysis with existing DR systems (→ Chapter 5).
6. Design a modular system architecture for automated DR screening deployable in resource-limited environments (→ Chapter 6).

### Object and Subject of Research
- **Object:** Fundus images of patients with diabetic retinopathy, sourced from APTOS 2019 and supplementary clinical corpora.
- **Subject:** The process of automated multi-stage DR classification through integrated preprocessing and CNN-based analysis.

### Research Hypothesis
- Verbatim from HYPOTHESIS.md, mapped to INVARIANTS §II:
  - **H-1 (Primary — Preprocessing Dominance):** See INVARIANTS §II, H-1. Independent variable: presence vs. absence of preprocessing pipeline. Dependent variables: Accuracy, F1-score, ROC-AUC, Cohen's Kappa. Empirical dominance criterion: EH-3 (weighted F1 Δ ≥ 5 pp; ROC-AUC Δ ≥ 0.02; no Cohen's Kappa degradation).
  - **H-2 (Secondary — CLAHE Threshold Sensitivity):** See INVARIANTS §II, H-2. Bounded to tested parameter range; no extrapolation permissible.
  - **H-3 (Secondary — Two-Stage Fine-Tuning):** See INVARIANTS §II, H-3. Empirical reference values from LC-CONF (Table 3) / LC-KBTU as prior self-publications (SIR-4).

### Methodological Basis
- Experimental comparison with controlled conditions (matched dataset, hardware, training budget).
- Multi-metric evaluation framework: weighted F1-score, ROC-AUC, Cohen's Kappa, Accuracy (INVARIANTS EH-1).
- Transfer learning theory; CNN feature extraction and classification; adaptive histogram equalization theory.
- Cross-validation and statistical reliability protocols (INVARIANTS EH-4).

### Provisions Submitted for Defense
1. The integrated preprocessing pipeline (resizing, normalization, modified CLAHE, augmentation) produces statistically measurable improvement in five-class DR classification (ARGUMENT_MAP PC-1).
2. CLAHE clip limit parameter exhibits a parameter-dependent sensitivity profile with identifiable local optimum (ARGUMENT_MAP PC-2).
3. Two-stage fine-tuning of EfficientNetB0 outperforms frozen-only strategy (ARGUMENT_MAP PC-3).
4. Coupled thermal-optical mathematical model provides theoretical grounding for laser-tissue interaction (ARGUMENT_MAP PC-4; theoretical claim only).
5. Modular system architecture specification for DR screening in resource-limited environments (ARGUMENT_MAP PC-5; design specification only).

### Theoretical Significance
- Mathematical formalization of modified CLAHE with simplified threshold control (T/80 formulation adapted from LC-SQOPUS_Q2).
- Theoretical framework for preprocessing-as-primary-driver of diagnostic performance (Preprocessing Dominance Hypothesis).
- Coupled thermal-optical model of fundus tissue response (LC-KazUTB; theoretical/computational only).

### Practical Significance
- Validated preprocessing-CNN pipeline applicable to APTOS 2019 and supplementary clinical datasets.
- System architecture design for integration with PACS, EHR, and telemedicine platforms in Kazakhstan (LC-NAN_RK; design specification, not deployed).
- Boundary: No clinical-grade accuracy claim; no prototype implementation (INVARIANTS SB-1.3, SB-4.1).

### Approbation of Research Results
- Conference presentations and publications (see Publications section).

### Publications
- LC-CONF: Sapakova et al. (2025), DS 2025 Conference, Procedia Computer Science.
- LC-KBTU: Yesmukhamedov et al. (2025), Herald of KBTU.
- LC-KazUTB: Sapakova et al. (2024), Herald of KazUTB.
- LC-NAN_RK: Yesmukhamedov et al. (2025), News of NAS RK.
- LC-SQOPUS_Q3: Sapakova, Yesmukhamedov, & Sapakov (2025), Eastern-European Journal of Enterprise Technologies.
- Self-citation transparency rule (SIR-4) applies to all self-authored publications.

---

## CHAPTER 1: PROBLEM DOMAIN ANALYSIS AND CURRENT STATE OF AUTOMATED DIABETIC RETINOPATHY DIAGNOSIS

**Chapter Function:** Establish the clinical, epidemiological, and technical context; identify the research gap; justify the research direction.

### 1.1 Medical and Epidemiological Context of Diabetic Retinopathy

#### 1.1.1 Pathophysiology and Clinical Grading Systems
- Five-stage clinical grading: DR 0 (no disease) through DR 4 (proliferative) per standard classification.
- Microvascular pathology: microaneurysms, hemorrhages, exudates, neovascularization.
- Source alignment: LC-CONF (p. 496–497); LC-KBTU (§II.2); LC-NAN_RK (p. 74–75).

#### 1.1.2 Screening Requirements in Resource-Limited Healthcare Settings
- Global screening burden; WHO recommendations for early detection.
- Kazakhstan-specific: ophthalmologist-to-population ratio, rural access limitations (LC-NAN_RK, p. 77, 86–87).
- Boundary: Epidemiological statistics are contextual framing, not dissertation results (SIR-8; SB-1.6).

### 1.2 Fundus Image Acquisition and Quality Variability

#### 1.2.1 Sources of Image Degradation in Clinical Practice
- Illumination inconsistencies, motion artifacts, camera-specific noise, patient-related factors.
- Operational definition of image quality per INVARIANTS OD-1.

#### 1.2.2 Impact of Image Quality on Diagnostic Model Performance
- Baseline CNN performance degradation on unprocessed images as evidence of quality impact.
- Link to preprocessing motivation: "the limited generalization ability of neural networks under variable image quality" (LC-SQOPUS_Q3, p. 81).

### 1.3 Deep Learning Approaches to Retinal Image Classification

#### 1.3.1 Convolutional Neural Network Architectures for Medical Imaging
- General CNN architecture: input, convolutional/pooling layers, fully connected layers (GLOSSARY §1, CNN definition).
- Architectures relevant to DR: EfficientNet family, ResNet, VGG, DenseNet.
- Boundary: Dissertation evaluates EfficientNetB0 and ResNet50 only; no claim of architectural optimality (INVARIANTS SB-3.1; ARGUMENT_MAP NC-6).

#### 1.3.2 Transfer Learning Strategies in Ophthalmic Diagnostics
- ImageNet pre-training and domain transfer to medical imaging.
- Domain gap acknowledgment per INVARIANTS DGL-6.
- Frozen-layer vs. progressive fine-tuning as competing strategies.

### 1.4 Critical Analysis of Existing Automated DR Screening Systems
- Review of IDx-DR, EyeNuk, DeepMind retinal systems.
- Boundary: No superiority claim against named commercial systems (INVARIANTS CFC-2.2; ARGUMENT_MAP NC-2). Comparison is contextual benchmarking, not controlled evaluation.

### 1.5 Formulation of the Research Problem and Justification of Research Direction
- Synthesis of gaps identified in §1.1–1.4.
- Central gap: absence of a unified framework integrating image enhancement and CNN classification optimized for resource-limited conditions (LC-SQOPUS_Q3, p. 81).
- Justification for the specific research direction aligned with CORE_OBJECTIVE.md.

### Conclusions to Chapter 1
- Summarize the state of the art; identify specific gaps; state the research problem formally.

---

## CHAPTER 2: THEORETICAL FOUNDATIONS OF IMAGE PREPROCESSING AND DEEP LEARNING FOR FUNDUS IMAGE ANALYSIS

**Chapter Function:** Provide the mathematical and theoretical grounding for all methods used in Chapters 3–4.

### 2.1 Mathematical Foundations of Image Enhancement Techniques

#### 2.1.1 Histogram Equalization and Adaptive Contrast Enhancement
- Theory of histogram equalization as intensity redistribution.
- Transition from global to adaptive methods; motivation for CLAHE (GLOSSARY §1, Histogram Equalization, CLAHE).

#### 2.1.2 Formalization of CLAHE with Controllable Threshold Parameters
- Conventional CLAHE: CLIP LIMIT = ⌈L/T⌉ + β·(φ − ⌈L/T⌉) (Eq. 1, per LC-SQOPUS_Q2, §2.2.1).
- Upgraded CLAHE (T/80 formulation): CLIP LIMIT = T/80 (Eq. 2, per LC-SQOPUS_Q2, §2.2.1, p. 5).
- Boundary: T/80 formulation derived on STARE dataset; not directly transferable to APTOS 2019 without independent validation (INVARIANTS DGL-5; GLOSSARY §2, Upgraded CLAHE entry).
- Sensitivity formula anomaly in LC-SQOPUS_Q2: Sen = TP/(TP+TN) deviates from standard Sen = TP/(TP+FN) — must be noted per SIR-3.

#### 2.1.3 Spatial Filtering and Noise Reduction Methods
- Spatial filtering theory for noise reduction and feature enhancement in fundus images.
- Artifact and noise smoothing as preprocessing prerequisite (LC-CONF, p. 497).

### 2.2 Theoretical Framework of Convolutional Neural Networks

#### 2.2.1 Convolution, Pooling, and Feature Extraction Operations
- Convolution operation with learned kernels (3×3); max-pooling (2×2, stride 2).
- Hierarchical feature extraction from low-level edges to high-level pathological structures.
- Formal definitions per GLOSSARY §1.

#### 2.2.2 Loss Functions and Optimization for Imbalanced Medical Datasets
- Binary cross-entropy (baseline, sigmoid output) vs. categorical cross-entropy (enhanced, softmax 5-class).
- Weighted loss function formulation for ordinal class structure and severe class imbalance.
- Adam optimizer; StepLR and ReduceLROnPlateau schedulers; EarlyStopping (LC-CONF, p. 497, 499–500).

#### 2.2.3 Regularization Techniques: Dropout, Batch Normalization, and Data Augmentation
- Dropout (rate 0.4) after dense layers; batch normalization within convolutional blocks.
- Data augmentation as both regularization and class imbalance mitigation: horizontal/vertical flips, rotation ±15°, zoom ±10°, brightness variation (INVARIANTS OD-3; LC-SQOPUS_Q3, p. 82–83).

### 2.3 Transfer Learning Theory and Domain Adaptation

#### 2.3.1 Feature Transferability Across Visual Domains
- Theoretical premise: features learned on ImageNet retain partial utility for fundus image classification.
- Explicit caveat: transferability "is not theoretically guaranteed and is evaluated empirically within the dissertation's experimental framework only" (INVARIANTS DGL-6).

#### 2.3.2 Frozen-Layer versus Progressive Fine-Tuning Strategies
- Frozen-layer strategy: all base layers frozen; only classification head trained (Method 1).
- Progressive fine-tuning: after initial training, upper layers unfrozen and fine-tuned (Method 2).
- Canonical terminology per GLOSSARY §6 Priority 1, item 1.

### 2.4 Mathematical Modeling of Laser-Tissue Interaction in Retinal Therapy

#### 2.4.1 Coupled Thermal-Optical Model of Fundus Tissue Response
- Beer's law for radiation attenuation: I(r,z) = I₀(r)e^(−∫₀ᶻ β(r,ξ)dξ).
- Gaussian beam intensity profile: I₀(r) = (P/πa²)e^(−(r/a)²).
- General heat conduction equation: Coσ(x,y,z,T)∂T/∂t = div(k(x,y,z,T)·grad(T)).
- Finite difference method (explicit scheme) for numerical solution.
- Source: LC-KazUTB, §II.3 (Equations 1–8).
- Findings: Surface layers (cornea) exhibit faster temperature rise; deep layers (choroid, retina) stabilize after continued exposure (ARGUMENT_MAP SC-4.1).

#### 2.4.2 Implications for Diagnostic Image Feature Interpretation
- Qualitative support for understanding thermal effects on retinal features visible in fundus images.
- **Critical boundary:** No quantitative clinical validation; computational simulation only (INVARIANTS SB-1.5; SIR-6). Model omits blood perfusion term; tissue properties treated as static (LC-KazUTB, §II.7). The claim that simulation "confirms effectiveness of laser therapy" is the source's claim, not the dissertation's validated finding (SIR-6; CFC-2.4).

### Conclusions to Chapter 2
- Summarize theoretical apparatus; distinguish between experimentally grounded components (§2.1–2.3) and theoretical/computational components (§2.4).

---

## CHAPTER 3: METHODOLOGY OF INTEGRATED PREPROCESSING-CNN PIPELINE DESIGN

**Chapter Function:** Specify all methodological decisions; make the experimental framework fully reproducible.

### 3.1 Formalization of the Unified Preprocessing Pipeline

#### 3.1.1 Pipeline Stage Specification: Resizing, Normalization, Enhancement, Augmentation
- Formal pipeline definition per INVARIANTS OD-3: (1) Resizing to 512×512 (or 256×256 for baseline), (2) Pixel normalization x/255.0 → [0, 1], (3) CLAHE (clip limit 2.0, grid 8×8), (4) Augmentation.
- "Active" vs. "absent" pipeline definitions (OD-3): active = all four stages in order; absent = no transformations beyond dimensional resizing.

#### 3.1.2 Modified CLAHE Algorithm with Simplified Threshold Control
- Adaptation of T/80 formulation (LC-SQOPUS_Q2) to APTOS 2019 image distribution.
- Independent validation within dissertation's framework required per DGL-5.
- Implementation via OpenCV (LC-SQOPUS_Q3, p. 82–83).

#### 3.1.3 Augmentation Strategy for Class Imbalance Mitigation
- Specific operations: horizontal/vertical flips, rotation ±15°, zoom ±10%, brightness variation.
- Dual function: regularization (§2.2.3) and class imbalance mitigation.
- Class distribution documented: Class 0 = 73.5% training / 49.3% test; Classes 3+4 = 4.5% training / 13.3% test (LC-CONF, p. 498; ARGUMENT_MAP SC-1.4).

### 3.2 Design of Baseline and Enhanced CNN Architectures

#### 3.2.1 Shallow Baseline CNN for Preprocessing Quality Validation
- Architecture: 2 convolutional blocks, 32–64 filters, sigmoid output, binary cross-entropy, input 256×256.
- No batch normalization, no dropout.
- Operational definition of low-complexity reference per INVARIANTS OD-2.

#### 3.2.2 Enhanced Multi-Block CNN with Regularization Layers
- Architecture: 4 convolutional blocks, 32–256 filters, batch normalization, dropout 0.4, softmax 5-class output, categorical cross-entropy, Adam lr=0.0001.
- Operational definition of high-complexity reference per INVARIANTS OD-2.
- Boundary: Architectural change and preprocessing are applied simultaneously in the primary comparison; ablation study (§5.2) required to isolate preprocessing contribution (ARGUMENT_MAP PC-1, strength justification).

### 3.3 Transfer Learning Methodology Using EfficientNetB0 and ResNet50

#### 3.3.1 Architecture Adaptation for Five-Class DR Classification
- EfficientNetB0 pre-trained on ImageNet; classification head replaced with 5-class softmax.
- ResNet50 as secondary architecture for replication requirement (INVARIANTS EH-4).
- Domain gap acknowledgment (DGL-6).

#### 3.3.2 Two-Stage Fine-Tuning Protocol Design
- Stage 1 (Frozen-layer strategy): Freeze all base layers; train classification head only.
- Stage 2 (Progressive fine-tuning): Unfreeze upper layers; fine-tune with reduced learning rate.
- Optimizer: Adam with StepLR scheduler; callbacks: ReduceLROnPlateau, EarlyStopping (LC-CONF, p. 497, 499–500).

#### 3.3.3 Weighted Loss Function Formulation for Ordinal Class Structure
- Categorical cross-entropy with class weights inversely proportional to class frequency.
- Addresses severe imbalance (Class 0: 73.5% vs. Class 4: 2.0% in training).

### 3.4 Evaluation Framework and Performance Metrics

#### 3.4.1 Multi-Metric Assessment: Accuracy, F1-Score, ROC-AUC, Cohen's Kappa
- Primary metrics (EH-1): weighted F1-score > ROC-AUC > Cohen's Kappa (quadratic weights) > Accuracy.
- Secondary metrics (EH-2): per-class precision/recall, macro averages, training-set metrics (overfitting diagnosis only).
- Diagnostic effectiveness thresholds per INVARIANTS OD-5: Accuracy ≥ 0.80, weighted F1 ≥ 0.80, ROC-AUC ≥ 0.90, Cohen's Kappa ≥ 0.70.

#### 3.4.2 Cross-Validation and Statistical Reliability Protocols
- Empirical dominance criterion (EH-3): weighted F1 Δ ≥ 5 pp AND ROC-AUC Δ ≥ 0.02 AND no Cohen's Kappa degradation.
- Sufficient validation criterion (EH-4): EH-3 on APTOS 2019 + direction confirmed on secondary dataset + replication across ≥ 2 architectures.
- Data partition: 80/10/10 split (training/validation/test).

### Conclusions to Chapter 3
- Summarize the complete methodological specification; confirm reproducibility conditions.

---

## CHAPTER 4: EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

**Chapter Function:** Execute experiments H-1, H-2, H-3; report results with full boundary conditions.

### 4.1 Datasets and Experimental Configuration

#### 4.1.1 APTOS 2019, STARE, and Supplementary Clinical Image Corpora
- APTOS 2019: 3,662 labeled samples, five-class DR staging (public dataset).
- APTOS 2019 + supplementary clinical data: training 35,126; test 3,662 (LC-CONF, p. 498).
- STARE: 157 images, five-class taxonomy (BDR, CRVO, CNV, PDR, Normal) — taxonomically non-equivalent to DR 0–4 (INVARIANTS SB-2.3; DGL-1).
- Supplementary clinical images: not publicly available; reproducibility structurally limited (SB-2.2).

#### 4.1.2 Class Distribution Analysis and Data Partitioning Strategy
- Training distribution: Class 0 = 25,810 (73.5%), Class 1 = 2,443 (7.0%), Class 2 = 5,292 (15.1%), Class 3 = 873 (2.5%), Class 4 = 708 (2.0%) (LC-CONF, p. 498).
- Test distribution: Class 0 = 1,805 (49.3%), Class 1 = 370 (10.1%), Class 2 = 999 (27.3%), Class 3 = 193 (5.3%), Class 4 = 295 (8.0%) (LC-CONF, p. 498).
- Class imbalance as primary confounding factor necessitating weighted F1 and Cohen's Kappa (ARGUMENT_MAP SC-1.4).

#### 4.1.3 Hardware Constraints and Computational Resource Limitations
- Document specific hardware configuration (DGL-2).
- Hardware overheating constraints on epoch count noted (LC-SQOPUS_Q3, p. 86).
- Processing time differential: 1s 108ms/step with preprocessing vs. 8s 986ms/step without (ARGUMENT_MAP SC-1.3).

### 4.2 Experiment 1: Baseline CNN without Preprocessing versus Enhanced CNN
- **Tests:** H-1 (Preprocessing Dominance)
- **Evidence target:** ARGUMENT_MAP PC-1, SC-1.1, SC-1.2

#### 4.2.1 Training Dynamics and Convergence Analysis
- Enhanced CNN: 94.5% training accuracy, 91.3% validation accuracy, convergence within 35–40 epochs, validation loss stabilizing at 0.18–0.20 (LC-SQOPUS_Q3, p. 86).
- Baseline CNN: validation loss stabilizing at 0.27–0.30 (ARGUMENT_MAP SC-1.2).
- Epoch-level analysis: Epoch 9 val_acc 93.41%, val_loss 0.1833 vs. baseline val_acc 91.71%, val_loss 0.2288 (LC-SQOPUS_Q3, p. 86, Table 2).

#### 4.2.2 Quantitative Comparison of Diagnostic Metrics
- Validation accuracy: 71% (no preprocessing) → 86% (with preprocessing) (ARGUMENT_MAP SC-1.1).
- Classification accuracy: 88% → 91% (ARGUMENT_MAP SC-1.1).
- Weighted F1 = 0.91; ROC-AUC = 0.9638 (LC-SQOPUS_Q3, p. 84).
- Evaluate against EH-3 criteria: weighted F1 Δ ≥ 5 pp ✓; ROC-AUC ≥ 0.9638 ✓; Cohen's Kappa — report.
- **Boundary:** Preprocessing and architectural complexity change are confounded; ablation study required (§5.2) for isolation. Binary vs. five-class classification reporting ambiguity must be resolved (LC-SQOPUS_Q3, §II.7 Assumption 3).

### 4.3 Experiment 2: Modified CLAHE Threshold Optimization on Small Datasets
- **Tests:** H-2 (CLAHE Threshold Sensitivity)
- **Evidence target:** ARGUMENT_MAP PC-2, SC-2.1, SC-2.2

#### 4.3.1 Threshold Parameter Sensitivity Analysis
- Clip limit parameter sweep across controlled values.
- Document sensitivity curve; identify local optimum within tested range.
- No extrapolation to untested values (INVARIANTS H-2; CFC-1.2).
- If no identifiable optimum found → H-2 falsification per VCR-3.

#### 4.3.2 Impact on Feature Preservation in Microaneurysms and Small Vessels
- Per-class F1-score analysis for DR 1 and DR 2 (microaneurysm and small vessel features).
- Independent validation of CLAHE parameters within dissertation framework (DGL-5).
- Sensitivity formula anomaly note if citing LC-SQOPUS_Q2 figures (SIR-3).

### 4.4 Experiment 3: Transfer Learning Strategy Comparison
- **Tests:** H-3 (Two-Stage Fine-Tuning)
- **Evidence target:** ARGUMENT_MAP PC-3, SC-3.1, SC-3.2

#### 4.4.1 EfficientNetB0: Frozen versus Progressive Fine-Tuning
- Published baseline (prior self-publications, cited per SIR-4):
  - Method 1 (Frozen): Precision = 0.65, Recall = 0.60, F1 = 0.62, Accuracy = 0.80, Macro Avg = 0.72, Weighted Avg = 0.74.
  - Method 2 (Progressive fine-tuning): Precision = 0.75, Recall = 0.74, F1 = 0.74, Accuracy = 0.80, Macro Avg = 0.77, Weighted Avg = 0.81.
- Differential: +10 pp Precision, +14 pp Recall, +12 pp F1 (LC-CONF, p. 499, Table 3).
- Dissertation must replicate and extend these results, not simply reproduce (ARGUMENT_MAP SC-3.1 boundary).
- LC-CONF and LC-KBTU share identical experimental data → cannot be cited as independent confirmation (SIR-5).
- Method 1 overfitting documented: training F1 = 0.87 vs. test F1 = 0.62.

#### 4.4.2 ResNet50: Feature Extraction versus End-to-End Fine-Tuning
- ResNet50 as secondary architecture for EH-4 replication requirement.
- Methodological precedent from LC-SQOPUS_Q2 (ResNet50 on STARE; 100 epochs, lr=0.0003).
- Boundary: LC-SQOPUS_Q2 results on STARE with different taxonomy; not directly comparable (SB-2.3; ARGUMENT_MAP SC-3.2 boundary).

#### 4.4.3 Per-Class Performance Analysis under Severe Class Imbalance
- Per-class precision, recall, F1 for all five DR stages.
- Focus on minority classes (DR 3, DR 4): instability under severe imbalance (EH-2).
- Cohen's Kappa (quadratic weights) for ordinal misclassification assessment.

### Conclusions to Chapter 4
- State H-1, H-2, H-3 outcomes explicitly.
- Report falsifying observations if any hypothesis direction not confirmed (VCR-3).
- Acknowledge confounds and boundary conditions.

---

## CHAPTER 5: RELIABILITY VALIDATION AND COMPARATIVE ANALYSIS

**Chapter Function:** Strengthen claim robustness through generalization testing, ablation, and benchmarking.

### 5.1 Cross-Database Generalization Testing

#### 5.1.1 Model Transferability Across Heterogeneous Image Sources
- Cross-database generalization metric: ratio of test-set F1-score on STARE to F1-score on APTOS 2019 under same trained model, without retraining (INVARIANTS OD-4).
- Taxonomic non-equivalence between STARE and APTOS 2019 must be explicitly acknowledged (SB-2.3).

#### 5.1.2 Stability Assessment under Varying Image Quality Conditions
- Test preprocessing pipeline effectiveness under different image quality profiles.
- Link to OD-1 (operational definition of image quality).

### 5.2 Statistical Validation of Preprocessing Dominance Hypothesis

#### 5.2.1 Ablation Study: Preprocessing Components versus Architectural Complexity
- **Critical experiment:** Isolate preprocessing contribution from architectural complexity change.
- Required for promoting PC-1 claim strength from MODERATE to STRONG (ARGUMENT_MAP §VI, PC-1).
- Design: Same enhanced architecture with vs. without preprocessing; same baseline architecture with vs. without preprocessing.
- Must satisfy EH-3 across both custom CNN and EfficientNetB0 on publicly reproducible APTOS 2019 partition.

#### 5.2.2 Quantitative Evidence for Image Quality as Primary Performance Driver
- Formal evaluation of preprocessing dominance per EH-3.
- Direction of effect confirmation on secondary dataset per EH-4.

### 5.3 Comparative Analysis with Existing DR Diagnostic Systems

#### 5.3.1 Benchmarking Against Published Results: IDx-DR, EyeNuk, DeepMind
- Literature-based comparison using published metrics.
- **Critical boundary:** No controlled experiment against named systems under identical conditions. This is contextual benchmarking, not a superiority claim (CFC-2.2; ARGUMENT_MAP NC-2).

#### 5.3.2 Performance-Complexity Trade-Off Analysis
- Resource efficiency: EfficientNetB0 "high accuracy-to-computation ratio" (LC-CONF, p. 498).
- Computational cost comparison between architectures tested.
- Boundary: Claims about computational efficiency are hardware-specific (DGL-2).

### 5.4 Limitations and Boundary Conditions of the Proposed Approach
- Comprehensive enumeration of all INVARIANTS scope boundaries (SB-1 through SB-4).
- Dataset-bound generalization (DGL-1); hardware-specific reproducibility (DGL-2); clinical population non-extrapolation (DGL-3).
- CLAHE parameter portability limitation (DGL-5); transfer learning domain gap (DGL-6).
- Non-claims enumeration (ARGUMENT_MAP §VII, NC-1 through NC-13).

### Conclusions to Chapter 5
- State final claim strength classifications for PC-1 through PC-5.
- Identify remaining open questions.

---

## CHAPTER 6: ARCHITECTURE OF AN AUTOMATED DR SCREENING SYSTEM FOR RESOURCE-LIMITED ENVIRONMENTS

**Chapter Function:** Translate validated experimental results into a system design specification.
**Epistemic status of entire chapter:** Design specification only. No prototype implementation or field testing (INVARIANTS SB-4.1; ARGUMENT_MAP PC-5).

### 6.1 System Requirements and Design Principles

#### 6.1.1 Functional and Non-Functional Requirements Specification
- Functional: Image capture, preprocessing, inference, reporting, physician feedback loop.
- Non-functional: Response time, scalability, data security, interoperability.
- Resource-limited environment definition per INVARIANTS OD-6.

#### 6.1.2 Modular Architecture with PACS and EHR Integration
- Component specification: Image Capture, Image Processing, Recognition Model, Diagnosis, Reporting, User Interface, Data Storage, Error Handling, Doctor-AI Feedback Loop (LC-NAN_RK, §II.4).
- UML diagrams: component, sequence, class, activity, ER (ARGUMENT_MAP SC-5.1).

### 6.2 AI Processing Module Design

#### 6.2.1 Preprocessing Engine with Configurable Pipeline Parameters
- Configurable pipeline parameters based on validated preprocessing pipeline (§3.1).
- Link to PC-1: the preprocessing-CNN pipeline validated experimentally constitutes the AI processing module core.

#### 6.2.2 Inference Module with Model Selection Logic
- Model selection between baseline CNN, enhanced CNN, EfficientNetB0, ResNet50 based on computational resource availability.

### 6.3 Clinical Workflow Integration

#### 6.3.1 Telemedicine and Portable Device Support for Rural Deployment

##### 6.3.1.1 Deployment in distributed telemedicine systems
- Design specifications for remote diagnostic support.

##### 6.3.1.2 Integration with national eHealth platforms
- Kazakhstan eHealth infrastructure context (LC-NAN_RK, p. 86–87).
- Infrastructure prerequisites: investments in diagnostic equipment, algorithm adaptation to local data, national standards development, specialist training (LC-NAN_RK, p. 90).

##### 6.3.1.3 Real-time remote DR screening in low-resource regions
- Design feasibility; not demonstrated capability (SB-4.1).

#### 6.3.2 Physician-in-the-Loop Decision Support Interface
- System is decision-support, not standalone diagnostic (INVARIANTS SB-1.3).
- Physician retains central role in decision-making (LC-NAN_RK, §II.1).

### 6.4 Data Security and Regulatory Compliance Framework

#### 6.4.1 GDPR/HIPAA-Aligned Data Management Protocols
- Design specification for compliance; not certified compliance status (SB-4.2; ARGUMENT_MAP NC-9).

#### 6.4.2 Applicability to Kazakhstan Healthcare Infrastructure
- Contextual analysis of Kazakhstan-specific regulatory requirements.
- Boundary: No field testing in Kazakhstan clinical settings (SB-4.3).

### Conclusions to Chapter 6
- Summarize architecture design; explicitly state design-only epistemic status.

---

## CONCLUSION

- Restate Central Thesis (INVARIANTS IT-1) and evaluate against experimental evidence.
- Summarize hypothesis outcomes: H-1, H-2, H-3 — confirmed, partially confirmed, or falsified (per VCR-3).
- Enumerate primary contributions (provisions submitted for defense) with final claim strength classifications.
- Restate scope boundaries and non-claims.
- Identify directions for future work: prototype implementation, clinical validation trial, architecture comparison, demographic subgroup evaluation, CLAHE parameter portability testing.

---

## REFERENCES

- All sources cited per self-citation transparency rule (SIR-4).
- LC-CONF and LC-KBTU identified as non-independent sources sharing identical experimental data (SIR-5).
- Sensitivity formula anomaly in LC-SQOPUS_Q2 noted per SIR-3.

---

## APPENDICES

### Appendix A — Source Code of the Preprocessing Pipeline
- Complete implementation code for the four-stage preprocessing pipeline.

### Appendix B — Supplementary Experimental Results and Confusion Matrices
- Per-class confusion matrices for all experiments (Chapters 4–5).
- Training/validation loss and accuracy curves.

### Appendix C — System Architecture UML Diagrams
- Component, sequence, class, activity, and ER diagrams (Chapter 6).

### Appendix D — Certificates of Implementation and Approbation Acts
- Conference participation certificates; publication confirmations.

---

## TRACEABILITY MATRIX

| Outline Section | Hypothesis Tested | Primary Claim | Sub-Claims | Literature Cards | Invariant Constraints |
|---|---|---|---|---|---|
| §4.2 | H-1 | PC-1 | SC-1.1, SC-1.2, SC-1.3, SC-1.4 | LC-SQOPUS_Q3, LC-CONF | EH-3, EH-4, OD-1, OD-3 |
| §4.3 | H-2 | PC-2 | SC-2.1, SC-2.2 | LC-SQOPUS_Q2, LC-SQOPUS_Q3 | DGL-5, CFC-1.2, SIR-3 |
| §4.4 | H-3 | PC-3 | SC-3.1, SC-3.2 | LC-CONF, LC-KBTU, LC-SQOPUS_Q2 | SIR-4, SIR-5, SIR-7 |
| §2.4 | — | PC-4 | SC-4.1 | LC-KazUTB | SB-1.5, SIR-6, CFC-2.4 |
| §6.1–6.4 | — | PC-5 | SC-5.1 | LC-NAN_RK | SB-4.1, SB-4.2, SB-4.3, DGL-4 |
| §5.2 | H-1 (ablation) | PC-1 (strength promotion) | — | LC-SQOPUS_Q3 | EH-3, EH-4 |

---

*End of MASTER_OUTLINE.md*
*Binding references: DISSERTATION_INVARIANTS.md v.1.0 | ARGUMENT_MAP.md | GLOSSARY_v1_0.md*
*All structural decisions traceable to the governing source corpus.*
