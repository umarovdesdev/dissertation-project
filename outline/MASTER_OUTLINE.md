# MASTER OUTLINE
## Doctoral Dissertation: Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Master Structural Outline — Chapter-by-Chapter Content Specification
**Binding References:** DISSERTATION_INVARIANTS.md v4.0 | ARGUMENT_MAP.md v4.0 | GLOSSARY_EN.md | TABLE_OF_CONTENTS_EN.md
**Source Corpus:** LC-CONF | LC-KBTU | LC-KazUTB | LC-NAN_RK | LC-SQOPUS_Q2 | LC-SQOPUS_Q3
**Governing Documents:** CENTRAL_THESIS.md | CORE_OBJECTIVE.md | HYPOTHESIS.md

---

## FRONT MATTER

### Normative References
- List of standards governing dissertation format, terminology, and citation practice.

### Definitions
- Source: GLOSSARY_v2_1.md, Part A (Structured Glossary Table).
- All operationally defined terms (OD-1 through OD-6 per INVARIANTS §III) must appear here with verbatim definitions.
- Terminological stabilization recommendations (GLOSSARY §6) must be applied: canonical fine-tuning terminology, disambiguation of "feature extraction," "generalization," and "preprocessing" per Priority 1 items.

### Designations and Abbreviations
- CNN, CLAHE, DR, ROC-AUC, APTOS, EyePACS, IDRiD, Messidor, Messidor-2, RFMiD, DDR, ODIR-5K, EHR, PACS, HIPAA, GDPR, UML, Grad-CAM, IoU, ECE, SSIM, CNR, VVI, FOV, HSV, LAB.
- Standardize: "EHR" (not "EMR"); "ResNet-50" (not "RESNET50"); "EfficientNet-B3" consistently (GLOSSARY §6, items 5, 7).

---

## INTRODUCTION

### Relevance of the Research
- **Medical context:** Diabetic retinopathy as a leading cause of preventable blindness; global prevalence data (IDF Diabetes Atlas 2021, cited via LC-NAN_RK, p. 86–87).
- **Kazakhstan-specific framing:** ~1,200 ophthalmologists serving the entire population; >40% rural residents with limited access to specialized care (LC-NAN_RK, p. 74, 77, 86–87).
- **Technical gap:** Suboptimal performance of baseline CNNs under variable image quality; absence of unified preprocessing-classification frameworks optimized for resource-limited environments (LC-SQOPUS_Q3, p. 81).
- **Boundary:** Projected deployment benefits (20–30% late-stage DR reduction; 15–20% cost reduction) are third-party projections, not dissertation findings (INVARIANTS SB-1.6; ARGUMENT_MAP NC-3; SIR-8).

### Scientific Novelty
1. Integration of a 6-stage V4 preprocessing pipeline — comprising canonical orientation (Stage 0: Stage 0a canonical flip + Stage 0b OD-fovea rotation normalization), FOV crop+resize (Stage 1), flat-field illumination correction (Stage 2), upgraded CLAHE with dual-constraint clip limit in LAB color space (Stage 3), ImageNet normalization (Stage 4), and integrated augmentation (Stage 5) — into a CNN-based DR classification pipeline as a unified framework, not isolated techniques (LC-SQOPUS_Q3, p. 81; LC-SQOPUS_Q2, §1).
2. Two-stage fine-tuning protocol for EfficientNetB0 tailored to fundus image variability (LC-CONF, p. 497; LC-KBTU, §II.1) [V3: retained as training strategy; H-3 dropped].
3. Mathematical modeling of laser-tissue interaction for retinal therapy with qualitative simulation (LC-KazUTB, §II.1) — bounded as theoretical contribution only (INVARIANTS SB-1.5; ARGUMENT_MAP PC-4).
4. Modular AI-driven system architecture for DR screening in resource-limited environments (LC-NAN_RK, §II.1) — bounded as design specification only (INVARIANTS SB-4.1; ARGUMENT_MAP PC-5).
5. Cross-database transferability validation across 3+ independent datasets (Messidor, Messidor-2, IDRiD) with generalization ratio metric (G = F1_external / F1_EyePACS) — demonstrating pipeline robustness beyond the training domain (ARGUMENT_MAP PC-6).
6. Grad-CAM explainability analysis with quantitative ALO (primary metric: Attention–Lesion Overlap, `ALO = area(GradCAM ∩ lesion) / area(lesion)`) and IoU (secondary metric) against IDRiD pixel-level lesion masks (microaneurysms, hemorrhages, hard exudates, soft exudates) — providing causal evidence that preprocessing redirects CNN attention to clinically relevant structures (ARGUMENT_MAP PC-7).
7. 6-stage V4 preprocessing pipeline (canonical orientation [Stage 0a: canonical flip; Stage 0b: OD-fovea rotation normalization], FOV crop+resize, flat-field correction, upgraded CLAHE, ImageNet normalization, integrated augmentation) with component-level ablation identifying ranked contribution hierarchy (ARGUMENT_MAP PC-8).
8. Device domain shift evaluation across 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss) on RFMiD, DDR, ODIR-5K — quantifying cross-device performance variability for deployment readiness assessment (ARGUMENT_MAP PC-9).

### Research Goal
- To develop and experimentally validate an integrated fundus image enhancement and CNN-based classification framework for automated multi-stage diabetic retinopathy diagnosis, with specific emphasis on contrast-adaptive preprocessing (including upgraded CLAHE with threshold control) to improve microvascular feature visibility and classification robustness under variable image quality and constrained computational conditions. The framework is further validated for generalization across multiple independent datasets (Messidor, Messidor-2, IDRiD), explainability via Grad-CAM attention analysis, and robustness under device domain shift across camera hardware (RFMiD, DDR, ODIR-5K).

### Research Objectives
1. Analyze the current state of automated DR diagnosis, fundus image quality variability, device-specific acquisition challenges, and deep learning approaches to retinal image classification (→ Chapter 1).
2. Formalize the mathematical foundations of image enhancement techniques, CNN-based classification, transfer learning theory, explainability methods (CAM, Grad-CAM), and image quality metrics (CNR, VVI, SSIM, Entropy) (→ Chapter 2).
3. Design the 6-stage V4 preprocessing pipeline (canonical orientation [Stage 0a: canonical flip; Stage 0b: OD-fovea rotation normalization] → FOV crop+resize (PIL-based, Stage 1) → flat-field correction (σ=45, Stage 2) → upgraded CLAHE (dual-constraint clip limit, LAB L-channel, stochastic, Stage 3) → ImageNet normalization (Stage 4) → integrated augmentation (Stage 5)) and integrate it with ResNet-50, EfficientNet-B3, and EfficientNet-B4 architectures (→ Chapter 3).
4. Experimentally validate the preprocessing dominance hypothesis (H-1) via factorial ablation on EyePACS with ResNet-50 and EfficientNet-B3, 6 configurations A–F (→ Chapter 4, Experiment 1).
5. Validate the preprocessing component contribution hierarchy via component-level ablation on EyePACS (→ Chapter 4, Experiment 2) and CLAHE threshold sensitivity (H-2) as a sub-analysis.
6. [V3: Old Objective 6 dropped — Experiment 3 (robustness to synthetic image degradation on APTOS 2019) is no longer active in V3.] Validate explainability via Grad-CAM on EfficientNet-B4 with ALO (primary) and IoU (secondary) against IDRiD lesion masks (→ Chapter 4, V3 Experiment 4).
7. Validate cross-database generalization on Messidor/Messidor-2/IDRiD and device domain shift on RFMiD/DDR/ODIR-5K across camera hardware (→ Chapter 5, V3 Experiment 3: Cross-Dataset Generalization and Device Domain Shift — merged from old Exp 5+6).
8. Design a modular system architecture for automated DR screening deployable in resource-limited environments, informed by multi-dataset and multi-device experimental evidence (→ Chapter 6).

### Object and Subject of Research
- **Object:** Fundus images of patients with diabetic retinopathy, sourced from EyePACS (primary training), IDRiD (clinical validation, lesion localization, and CLAHE parameter sweep), Messidor/Messidor-2 (external generalization), and RFMiD/DDR/ODIR-5K (device domain shift evaluation). [V3: APTOS 2019 no longer an active experimental dataset.]
- **Subject:** The process of automated multi-stage DR classification through integrated preprocessing and CNN-based analysis.

### Research Hypothesis
- Verbatim from HYPOTHESIS.md, mapped to INVARIANTS §II:
  - **H-1 (Primary — Preprocessing Dominance):** See INVARIANTS §II, H-1. Independent variable: presence vs. absence of 6-stage V4 preprocessing pipeline. Dependent variables: Accuracy, F1-score, ROC-AUC, Cohen's Kappa. Tested on ResNet-50 and EfficientNet-B3 on EyePACS (6 configs A–F). Empirical dominance criterion: EH-3 (weighted F1 Δ ≥ 5 pp; ROC-AUC Δ ≥ 0.02; no Cohen's Kappa degradation).
  - **H-2 (Secondary — CLAHE Threshold Sensitivity):** See INVARIANTS §II, H-2. Bounded to tested parameter range on IDRiD; no extrapolation permissible.
  - **H-3 (Secondary — Two-Stage Fine-Tuning) [DROPPED V3]:** See INVARIANTS §II, H-3. H-3 is not tested in V3. Empirical reference from LC-CONF (Table 3) / LC-KBTU cited as prior self-publications only (SIR-4).
  - **H-4 (Cross-Database Transferability):** Models trained on EyePACS with the 6-stage V4 preprocessing pipeline generalize to Messidor, Messidor-2, and IDRiD without retraining, achieving generalization ratio G ≥ 0.85 per OD-4 (G = F1_external / F1_EyePACS).
  - **H-5 (Explainability):** Preprocessing shifts CNN attention toward clinically relevant lesion regions: ALO between Grad-CAM activation maps and IDRiD lesion masks is higher for preprocessed models than baseline (ALO_preproc > ALO_baseline) — ALO is the PRIMARY metric. IoU_preproc > IoU_baseline is the secondary condition.
  - **H-6 (Device Robustness):** Preprocessed models maintain classification performance across images from different fundus camera domains (Canon, Topcon, Kowa, Zeiss), as evaluated on RFMiD, DDR, ODIR-5K.

### Methodological Basis
- Experimental comparison with controlled conditions (matched dataset, hardware, training budget).
- Multi-metric evaluation framework: weighted F1-score, ROC-AUC, Cohen's Kappa, Accuracy (INVARIANTS EH-1).
- Transfer learning theory; CNN feature extraction and classification; adaptive histogram equalization theory.
- 3-fold cross-validation with patient-level split (replacing 80/10/10); mixed-effects model for cross-fold analysis.
- Bonferroni/Holm correction for multiple comparisons.
- Grad-CAM explainability analysis with quantitative ALO (primary) and IoU (secondary) against lesion masks.
- Calibration metrics: Expected Calibration Error (ECE), Brier Score.
- Image quality metrics: Contrast-to-Noise Ratio (CNR), Vessel Visibility Index (VVI), Structural Similarity Index (SSIM), Image Entropy.
- Cross-validation and statistical reliability protocols (INVARIANTS EH-4).

### Provisions Submitted for Defense
1. The integrated 6-stage V4 preprocessing pipeline (canonical orientation [Stage 0a: canonical flip; Stage 0b: OD-fovea rotation normalization], FOV crop+resize, flat-field correction, upgraded CLAHE, ImageNet normalization, integrated augmentation) produces statistically measurable improvement in five-class DR classification independently for both ResNet-50 and EfficientNet-B3 on EyePACS (ARGUMENT_MAP PC-1).
2. CLAHE clip limit parameter exhibits a parameter-dependent sensitivity profile with identifiable local optimum on IDRiD (ARGUMENT_MAP PC-2).
3. Two-stage fine-tuning of EfficientNetB0 outperforms frozen-only strategy (ARGUMENT_MAP PC-3) [V3 DEMOTED: PC-3 is no longer a primary provision; cited as prior work only].
4. Coupled thermal-optical mathematical model provides theoretical grounding for laser-tissue interaction (ARGUMENT_MAP PC-4; theoretical claim only).
5. Modular system architecture specification for DR screening in resource-limited environments (ARGUMENT_MAP PC-5; design specification only).
6. Models trained on EyePACS with the 6-stage V4 preprocessing pipeline generalize to Messidor, Messidor-2, and IDRiD without retraining, achieving generalization ratio G ≥ 0.85 (ARGUMENT_MAP PC-6).
7. Grad-CAM analysis demonstrates that preprocessing redirects CNN attention toward clinically relevant lesion regions: ALO_preproc > ALO_baseline on IDRiD lesion masks (ALO is the PRIMARY metric; IoU_preproc > IoU_baseline is secondary) (ARGUMENT_MAP PC-7).
8. Component-level ablation (V4 Levels 0–4) identifies a ranked contribution hierarchy among the 6 V4 pipeline stages, measured by incremental weighted F1 improvement on EyePACS (ARGUMENT_MAP PC-8).
9. Preprocessed models maintain classification performance across images from different fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss), as evaluated on RFMiD, DDR, ODIR-5K (ARGUMENT_MAP PC-9).

### Theoretical Significance
- Mathematical formalization of modified CLAHE with simplified threshold control (T/80 formulation adapted from LC-SQOPUS_Q2).
- Theoretical framework for preprocessing-as-primary-driver of diagnostic performance (Preprocessing Dominance Hypothesis).
- Coupled thermal-optical model of fundus tissue response (LC-KazUTB; theoretical/computational only).

### Practical Significance
- Multi-dataset validated preprocessing-CNN pipeline applicable to EyePACS (primary), Messidor/Messidor-2 (generalization), and IDRiD (clinical validation), with device domain shift evidence from RFMiD/DDR/ODIR-5K supporting real-world deployment variability assessment.
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

#### 1.2.3 Device-Specific Variability in Fundus Imaging
- Camera-dependent image characteristics across major manufacturers: Canon, Topcon, Kowa, Zeiss.
- Variations in field of view, illumination profile, color rendering, resolution, and compression artifacts across camera models.
- Device-specific variability as a clinical deployment challenge: models trained on one camera type may not generalize to images from other devices.
- Motivation for device domain shift evaluation (V3 Experiment 3) and preprocessing pipeline normalization across camera domains.

### 1.3 Deep Learning Approaches to Retinal Image Classification

#### 1.3.1 Convolutional Neural Network Architectures for Medical Imaging
- General CNN architecture: input, convolutional/pooling layers, fully connected layers (GLOSSARY §1, CNN definition).
- Architectures relevant to DR: EfficientNet family, ResNet, VGG, DenseNet.
- Boundary: Dissertation evaluates ResNet-50, EfficientNet-B3, and EfficientNet-B4; no claim of architectural optimality (INVARIANTS SB-3.1; ARGUMENT_MAP NC-6).

#### 1.3.2 Transfer Learning Strategies in Ophthalmic Diagnostics
- ImageNet pre-training and domain transfer to medical imaging.
- Domain gap acknowledgment per INVARIANTS DGL-6.
- Frozen-layer vs. progressive fine-tuning as competing strategies.

#### 1.3.3 Explainability Methods in Medical Image Classification
- Grad-CAM (Gradient-weighted Class Activation Mapping) as an emerging requirement for clinical trust and regulatory acceptance.
- Attention visualization techniques: CAM, Grad-CAM, and their application to ophthalmic imaging.
- Explainability as a prerequisite for deploying AI-based diagnostic tools in clinical settings — understanding what the model "sees" in fundus images.
- Boundary: Explainability methods provide interpretability, not clinical localization (ARGUMENT_MAP NC-14).

### 1.4 Critical Analysis of Existing Automated DR Screening Systems
- Review of IDx-DR, EyeNuk, DeepMind retinal systems.
- Boundary: No superiority claim against named commercial systems (INVARIANTS CFC-2.2; ARGUMENT_MAP NC-2). Comparison is contextual benchmarking, not controlled evaluation.
- Coverage of multi-device benchmark datasets: RFMiD (Topcon, Kowa cameras; multi-disease including DR subset), DDR (Canon, Topcon; 5-class DR grading), ODIR-5K (Canon, Zeiss; multi-disease including DR subset) — as resources for evaluating device domain shift in DR classification systems.

### 1.5 Formulation of the Research Problem and Justification of Research Direction
- Synthesis of gaps identified in §1.1–1.4.
- Central gap: absence of a unified framework integrating image enhancement and CNN classification optimized for resource-limited conditions (LC-SQOPUS_Q3, p. 81).
- Additional gaps: lack of cross-database transferability evidence, absence of explainability validation, and untested device domain shift robustness.
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
- V4 update: CLAHE now applied with dual-constraint clip limit (clip_factor × tile_area/256, capped by global_threshold × tile_area) and stochastic train-time application (80% probability), replacing fixed clip limit 2.0 from v1.0.
- Boundary: T/80 formulation derived on STARE dataset; not directly transferable to EyePACS without independent validation (INVARIANTS DGL-5; GLOSSARY §2, Upgraded CLAHE entry).
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

### 2.5 Explainability in Deep Learning for Medical Imaging

#### 2.5.1 Class Activation Mapping (CAM) and Grad-CAM Mathematical Formulation
- CAM: weighted sum of feature maps from final convolutional layer using global average pooling weights.
- Grad-CAM: generalization of CAM using gradient information — gradient of target class score with respect to feature maps, followed by global average pooling and ReLU activation.
- Mathematical formulation: L^c_Grad-CAM = ReLU(Σ_k α^c_k · A^k), where α^c_k = (1/Z) Σ_i Σ_j (∂y^c / ∂A^k_ij).
- Advantages of Grad-CAM: architecture-agnostic (no modification to network required), applicable to any convolutional layer.

#### 2.5.2 Interpretation of Attention Maps in Ophthalmic Context
- Grad-CAM activation regions in fundus images: correspondence to microaneurysms, hemorrhages, exudates, and neovascularization.
- Clinical relevance: whether model attention aligns with ophthalmologist-identified lesion regions.
- Distinction between interpretability and diagnostic localization — Grad-CAM provides attention visualization, not pixel-level segmentation (ARGUMENT_MAP NC-14).

#### 2.5.3 ALO and IoU as Quantitative Explainability Metrics
- **ALO (primary metric):** Attention–Lesion Overlap — `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)`. Asymmetric metric measuring what fraction of the lesion is covered by model attention. Answers the clinical question "Does the model attend to the lesion?"
- **IoU (secondary metric):** Intersection-over-Union — `IoU = |A ∩ B| / |A ∪ B|`, where A = binarized Grad-CAM activation region, B = lesion mask. Symmetric metric measuring spatial precision of attention overlap.
- Application to IDRiD pixel-level annotations: microaneurysms, hemorrhages, hard exudates, soft exudates.
- ALO is primary because lesion coverage is the clinically relevant property; IoU provides complementary spatial precision evidence.

### 2.6 Image Quality Metrics for Preprocessing Evaluation

- Theoretical basis for quantifying preprocessing effectiveness independently of downstream classification.
- **Contrast-to-Noise Ratio (CNR):** Signal quality of vessel structures versus background — measures ability to distinguish retinal vasculature from surrounding tissue.
- **Vessel Visibility Index (VVI):** Detectability of retinal vasculature — quantifies enhancement of vessel structures after preprocessing.
- **Image Entropy:** Information content of the image — measures the increase in informational richness after contrast enhancement.
- **Structural Similarity Index (SSIM):** Preservation of structural information relative to original image — confirms that preprocessing does not introduce destructive artifacts.
- These metrics provide the theoretical grounding for the image quality analysis in Experiment 2 (§4.3) pipeline evaluation.

### Conclusions to Chapter 2
- Summarize theoretical apparatus; distinguish between experimentally grounded components (§2.1–2.3, §2.5–2.6) and theoretical/computational components (§2.4).

---

## CHAPTER 3: METHODOLOGY OF INTEGRATED PREPROCESSING-CNN PIPELINE DESIGN

**Chapter Function:** Specify all methodological decisions; make the experimental framework fully reproducible.

### 3.1 Formalization of the Unified Preprocessing Pipeline

#### 3.1.1 Pipeline Component Specification: 6-Stage V4 System

- V4 pipeline definition (replaces V3 5-component pipeline per INVARIANTS OD-3 v4.0):
  - **(Stage 0) Canonical Orientation** (toggleable): Two-sub-stage orientation normalization. NEW in V4.
    - **(Stage 0a) Canonical Flip:** Left→right eye horizontal flip to canonical right-eye orientation.
    - **(Stage 0b) OD-Fovea Rotation Normalization:** Classical CV detection of OD (brightest) and fovea (darkest with distance prior); rotates image so OD→fovea axis is horizontal; fallback to identity when detection confidence is low. Augmentation rotation_sigma (Stage 5) is adaptive from detection uncertainty; fallback σ=13.0°.
  - **(Stage 1) PIL-based FOV Crop and Resize:** Foreground detection, border removal, resize to 512×512 (always on). Replaces V3 Hough circle detection.
  - **(Stage 2) Flat-Field Correction:** Gaussian blur subtraction — `corrected = image − GaussianBlur(image, σ=45) + 128` (toggleable). NEW in V4.
  - **(Stage 3) Upgraded CLAHE:** Dual-constraint clip limit (`CL_tile = min(clip_factor × tile_area/256, global_threshold × tile_area)`) on LAB L-channel; stochastic at train time (80% probability) (toggleable). UPGRADED from V3 dynamic clip limit.
  - **(Stage 4) ImageNet Normalization:** `(x − mean)/std → tensor`; mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]; always on, always last. Replaces V3 pixel normalization [0,1].
  - **(Stage 5) Integrated Augmentation:** Unified affine (rotation_sigma adaptive from Stage 0b OD/fovea uncertainty or fallback 13.0°, clipped ±40°) + brightness/contrast + PCA color jitter; train only, inserted before Stage 4. NEW in V4 (was separate layer in V3).
- "Active" pipeline definition (full V4): all toggleable stages (0, 2, 3, 5) applied in order. "Absent" (V4 baseline): crop + resize + ImageNet normalize only (Stages 1 + 4).
- Augmentation (Stage 5) is integrated into the V4 pipeline at train time; differs from V3 where augmentation was a separate layer.

*[V3 Historical pipeline: (1) FOV Standardization (Hough), (2) CLAHE (dynamic clip limit), (3) HSV contrast enhancement, (4) Green channel imaging, (5) Pixel normalization [0,1]. Used for Exp 2 ablation historical comparison only. Green channel and HSV are NOT V4 components.]*

#### 3.1.2 Upgraded CLAHE Algorithm with Dual-Constraint Clip Limit
- Adaptation of T/80 formulation (LC-SQOPUS_Q2) — now applied in LAB color space with dual-constraint clip limit.
- Independent validation within dissertation's framework required per DGL-5.
- Implementation via OpenCV (LC-SQOPUS_Q3, p. 82–83).

#### 3.1.3 Augmentation Strategy for Class Imbalance Mitigation
- Specific operations: horizontal/vertical flips, rotation ±15°, zoom ±10%, brightness variation.
- Dual function: regularization (§2.2.3) and class imbalance mitigation.
- Class distribution documented: Class 0 = 73.5% training / 49.3% test; Classes 3+4 = 4.5% training / 13.3% test (LC-CONF, p. 498; ARGUMENT_MAP SC-1.4).

#### 3.1.4 External Image Ingestion Protocol
- Methodological contribution for integrating clinical data from Kazakh medical centers.
- Five-stage protocol: (1) Quality Gate — automated quality assessment and rejection of unusable images, (2) Geometric Standardization — alignment to standard FOV and resolution, (3) Preprocessing Pipeline — application of the 6-stage V4 system, (4) Label Harmonization — mapping institutional labels to standard 5-class DR taxonomy, (5) Distribution Analysis — statistical comparison of ingested data with training distribution.
- Boundary: The ingestion protocol is validated only for specific Kazakh medical center data; generalization to other clinical data sources requires independent validation (ARGUMENT_MAP NC-15).

### 3.2 Design of CNN Architectures for DR Classification

#### 3.2.1 ResNet-50 and EfficientNet-B3 as Primary Experimental Architectures
- **ResNet-50:** 50-layer residual network pre-trained on ImageNet; classification head replaced with 5-class softmax. Serves as Architecture A in the V4 factorial ablation (Experiment 1, configs A, B, E).
- **EfficientNet-B3:** Compound-scaled architecture pre-trained on ImageNet; classification head replaced with 5-class softmax. Serves as Architecture B in the V4 factorial ablation (Experiment 1, configs C, D, F).
- Rationale for selection: two established pretrained backbone families (ResNet, EfficientNet) provide stronger replication test across architecture families than custom shallow CNNs.
- Domain gap acknowledgment (DGL-6).

#### 3.2.2 Historical v1.0 Architectures (Reference Only)
- **Shallow Baseline CNN (v1.0):** 2 convolutional blocks, 32–64 filters, sigmoid output, binary cross-entropy, input 256×256. No batch normalization, no dropout. Operational definition of low-complexity reference per INVARIANTS OD-2.
- **Enhanced Multi-Block CNN (v1.0):** 4 convolutional blocks, 32–256 filters, batch normalization, dropout 0.4, softmax 5-class output, categorical cross-entropy, Adam lr=0.0001. Operational definition of high-complexity reference per INVARIANTS OD-2.
- These architectures are retained as historical v1.0 references and are not used in v2.1 experiments. They document the prior experimental context from self-publications (LC-SQOPUS_Q3, LC-CONF).

### 3.3 Transfer Learning Methodology

#### 3.3.1 Architecture Adaptation for Five-Class DR Classification
- EfficientNetB0 pre-trained on ImageNet; classification head replaced with 5-class softmax — used for two-stage fine-tuning training strategy (H-3 dropped in V3; retained as training method only).
- EfficientNet-B4 for explainability analysis (Experiment 4) — selected for higher-resolution feature maps suitable for Grad-CAM visualization.
- ResNet-50 as primary architecture for replication requirement (INVARIANTS EH-4).
- Domain gap acknowledgment (DGL-6).
- Note: Replication is now conducted on EyePACS (primary dataset), in addition to prior APTOS 2019 self-publication results.

#### 3.3.2 Two-Stage Fine-Tuning Protocol Design
- Stage 1 (Frozen-layer strategy): Freeze all base layers; train classification head only.
- Stage 2 (Progressive fine-tuning): Unfreeze upper layers; fine-tune with reduced learning rate.
- Optimizer: Adam with StepLR scheduler; callbacks: ReduceLROnPlateau, EarlyStopping (LC-CONF, p. 497, 499–500).

#### 3.3.3 Weighted Loss Function Formulation for Ordinal Class Structure
- Categorical cross-entropy with class weights inversely proportional to class frequency.
- Addresses severe imbalance (Class 0: 73.5% vs. Class 4: 2.0% in training).

### 3.4 Evaluation Framework and Performance Metrics

#### 3.4.1 Multi-Metric Assessment Framework
- **Primary metrics (EH-1):** weighted F1-score > ROC-AUC > Cohen's Kappa (quadratic weights) > Accuracy.
- **Secondary metrics (EH-2):** per-class precision/recall, macro averages, training-set metrics (overfitting diagnosis only).
- **Clinical screening metrics:** Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2) — applied in V3 Experiment 3.
- **Calibration metrics:** Expected Calibration Error (ECE), Brier Score — applied in V4 Experiments 1 and 5.
- **Image quality metrics:** Contrast-to-Noise Ratio (CNR), Vessel Visibility Index (VVI), Image Entropy, Structural Similarity Index (SSIM) — applied in V4 Experiment 2 pipeline analysis.
- **Explainability metrics:** Grad-CAM ALO (primary) and IoU (secondary) with IDRiD lesion masks (per lesion type), attention consistency score across datasets — applied in V4 Experiment 4.
- **Generalization metric:** G = F1_external / F1_EyePACS per OD-4 — applied in V4 Experiment 5.
- Diagnostic effectiveness thresholds per INVARIANTS OD-5: Accuracy ≥ 0.80, weighted F1 ≥ 0.80, ROC-AUC ≥ 0.90, Cohen's Kappa ≥ 0.70.

#### 3.4.2 Cross-Validation and Statistical Reliability Protocols
- **3-fold cross-validation with patient-level split:** All experiments use 3-fold CV with patient-level split to prevent data leakage. For each fold, 2 folds serve as training and 1 fold as test. All metrics reported as mean ± standard deviation across 3 folds.
- **Mixed-effects model:** Cross-fold analysis accounting for fold as random effect (Experiment 1).
- **Bonferroni/Holm correction:** Multiple comparison correction across configurations (V4 Experiments 1, 2).
- **McNemar test:** Paired classification comparison (V4 Experiment 1).
- **DeLong test:** ROC-AUC comparison (V4 Experiments 1, 5, and 6).
- **Bootstrap 95% CI:** ≥ 1000 iterations on all primary metrics (all experiments).
- Empirical dominance criterion (EH-3): weighted F1 Δ ≥ 5 pp AND ROC-AUC Δ ≥ 0.02 AND no Cohen's Kappa degradation.
- Sufficient validation criterion (EH-4): EH-3 on EyePACS + direction confirmed on secondary datasets + replication across ≥ 2 architectures.

### Conclusions to Chapter 3
- Summarize the complete methodological specification; confirm reproducibility conditions.

---

## CHAPTER 4: EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

**Chapter Function:** Execute Experiments 1–4; report results for H-1, H-2, H-5 with full boundary conditions.

### 4.1 Datasets and Experimental Configuration

#### 4.1.1 Dataset Architecture V4
- **EyePACS (Primary Training):** ~35,126 labeled images (Kaggle labeled partition), five-class DR staging (DR 0–4), Canon CR-1 camera. Primary dataset for V4 Experiments 1 and 2. Public dataset.
- **APTOS 2019 [NOT ACTIVE]:** 3,662 labeled samples. Old Experiment 3 (robustness under image degradation) is DROPPED. APTOS 2019 is not an active experimental dataset.
- **IDRiD (Clinical Validation + CLAHE Sweep):** Five-class DR staging with pixel-level lesion annotations (microaneurysms, hemorrhages, hard exudates, soft exudates). Kowa camera. Dataset for V4 Experiments 2 (CLAHE sweep), 4 (explainability), and 5 (generalization). Public dataset.
- **Messidor / Messidor-2 (External Generalization):** Topcon camera. Datasets for V4 Experiment 5 (cross-dataset generalization). Public datasets.
- **RFMiD (Device Domain Shift):** Topcon, Kowa cameras. Multi-disease including DR subset. Dataset for V4 Experiment 6.
- **DDR (Device Domain Shift):** Canon, Topcon cameras. Five-class DR grading. Dataset for V4 Experiment 6.
- **ODIR-5K (Device Domain Shift):** Canon, Zeiss cameras. Multi-disease including DR subset. Dataset for V4 Experiment 6.
- Supplementary clinical images from Kazakh medical centers: not publicly available; future work only (VCR-4; NC-15).

#### 4.1.2 Class Distribution Analysis and Data Partitioning Strategy
- EyePACS class distribution (~35,126 labeled images, 40% subset, ~14,050 used for experiments) and 3-fold cross-validation with patient-level stratified split.
- Class imbalance as primary confounding factor necessitating weighted F1 and Cohen's Kappa (ARGUMENT_MAP SC-1.4).
- Label harmonization methodology for datasets with non-standard taxonomies (Messidor, RFMiD, ODIR-5K).

#### 4.1.3 Hardware Specification and Reproducibility Protocol
- Document specific hardware configuration (DGL-2).
- Fixed random seeds, versioned code repository, and environment specification for full reproducibility.
<!-- SC-1.3 REMOVED V3: Processing time differential claim deleted as implausible. Do not restore. -->

### 4.2 Experiment 1: Causal Improvement — Preprocessing vs. Architecture on EyePACS
- **Tests:** H-1 (Preprocessing Dominance)
- **Evidence target:** ARGUMENT_MAP PC-1

#### 4.2.1 Factorial Design (6 Configurations A–F)
- A factorial experimental design is implemented to isolate the independent effects of preprocessing vs. architecture, with optional binocular blending extension:
  - Factor A: Preprocessing (baseline crop+resize+ImageNet normalize vs. full V4 6-stage pipeline)
  - Factor B: Architecture (ResNet-50 vs. EfficientNet-B3)
  - Optional extension: per-patient binocular blending (configs E, F)
- Six controlled experimental configurations:
  - **Config A:** baseline (crop+resize+ImageNet normalize) + ResNet-50
  - **Config B:** full V4 pipeline + ResNet-50
  - **Config C:** baseline (crop+resize+ImageNet normalize) + EfficientNet-B3
  - **Config D:** full V4 pipeline + EfficientNet-B3
  - **Config E:** full V4 pipeline + ResNet-50 + per-patient binocular blending (optional)
  - **Config F:** full V4 pipeline + EfficientNet-B3 + per-patient binocular blending (optional)

*[V3 Historical: 4 configs A–D; baseline was "resize only"; pipeline was 5-component V3]*
- All experiments conducted under matched dataset partitions (3-fold CV with patient-level split), hardware configuration, optimizer settings, and training budgets.
- Statistical analysis: Mixed-effects model across folds; McNemar test for paired comparison; DeLong test for ROC-AUC comparison; Bootstrap 95% CI.
- The preprocessing dominance hypothesis (H-1) is considered supported only if the main effect of preprocessing satisfies EH-3 criteria independently for both ResNet-50 (B > A) and EfficientNet-B3 (D > C).

#### 4.2.2 Training Dynamics and Convergence Analysis
- Training/validation loss and accuracy curves for all four configurations (A–D).
- Convergence analysis across architectures with and without preprocessing.
- Calibration analysis: ECE and Brier Score for each configuration.

#### 4.2.3 Quantitative Comparison of Diagnostic Metrics
- Primary metrics: weighted F1-score, ROC-AUC, Cohen's Kappa, Accuracy across all four configurations.
- Evaluate against EH-3 criteria independently for both architectures.
- Per-class performance analysis under severe class imbalance.
- **Boundary:** This replaces the v1.0 confounded comparison (2-block CNN without preprocessing vs. 4-block CNN with preprocessing) with a proper factorial design on established architectures.

### 4.3 Experiment 2: Preprocessing Component Ablation on EyePACS
- **Tests:** Preprocessing component contribution hierarchy; H-2 (CLAHE Threshold Sensitivity) as sub-analysis
- **Evidence target:** ARGUMENT_MAP PC-8 (component hierarchy); ARGUMENT_MAP PC-2 (CLAHE sensitivity)

#### 4.3.1 V4 Ablation Design (Levels 0–4)
- Sequential addition of V4 pipeline stages to isolate individual contributions:
  - Level 0: V4 baseline (crop+resize+ImageNet normalize, Stages 1+4) — no toggleable stages
  - Level 1a: baseline + canonical flip only (Stages 0a+1+4)
  - Level 1b: baseline + canonical orientation (Stage 0a + Stage 0b OD-fovea rotation, Stages 0a+0b+1+4)
  - Level 2: baseline + flat-field correction (Stages 1+2+4)
  - Level 3: baseline + upgraded CLAHE (Stages 1+3+4)
  - Level 4: full V4 pipeline (all stages: 0a+0b+1+2+3+4+5)
- Weighted F1 measured at each ablation level on EyePACS.
- Image quality metrics (CNR, VVI, Entropy, SSIM) calculated before and after each pipeline stage to quantify preprocessing effect independently of downstream classification.

#### 4.3.2 CLAHE Threshold Sensitivity Analysis (H-2 Sub-Analysis)
- Clip limit parameter sweep across controlled values on IDRiD.
- Document sensitivity curve; identify local optimum within tested range.
- No extrapolation to untested values (INVARIANTS H-2; CFC-1.2).
- If no identifiable optimum found → H-2 falsification per VCR-3.

#### 4.3.3 Impact on Feature Preservation in Microaneurysms and Small Vessels
- Per-class F1-score analysis for DR 1 and DR 2 (microaneurysm and small vessel features).
- Independent validation of CLAHE parameters within dissertation framework (DGL-5).
- Sensitivity formula anomaly note if citing LC-SQOPUS_Q2 figures (SIR-3).

### 4.4 Experiment 3: Cross-Dataset Generalization and Device Domain Shift
- **Tests:** H-4 (Cross-Database Transferability) and H-6 (Device Robustness)
- **Evidence target:** ARGUMENT_MAP PC-6 (generalization), PC-9 (device robustness)

<!-- V3: Merged from old Experiments 5 + 6. Old Experiment 3 (APTOS robustness) DROPPED. -->

#### 4.4.1 Cross-Database Transferability Without Retraining
- Models trained on EyePACS (ResNet-50, EfficientNet-B3) with 6-stage V4 preprocessing applied directly to Messidor, Messidor-2, and IDRiD without retraining.
- Generalization ratio G = F1_external / F1_EyePACS per OD-4. Target: G ≥ 0.85 on at least 2 of 3 external datasets.
- Label harmonization methodology for Messidor (referable/non-referable mapping to 5-class taxonomy).
- Boundary: No controlled experiment against named systems under identical conditions; contextual benchmarking only (CFC-2.2; ARGUMENT_MAP NC-2).

#### 4.4.2 Device Domain Shift — Cross-Camera Evaluation
- Dataset subsets grouped by camera model:
  - Canon (EyePACS, DDR subset, ODIR-5K subset)
  - Topcon (Messidor, RFMiD subset, DDR subset)
  - Kowa (IDRiD, RFMiD subset)
  - Zeiss (ODIR-5K subset)
- Performance comparison across camera domains: Accuracy, F1-score, ROC-AUC per camera group.
- Boundary: Device domain shift results do not constitute device certification or regulatory compliance (ARGUMENT_MAP NC-16).

#### 4.4.3 Generalization Ratio and Cross-Device Performance Matrix
- Generalization ratio G per external dataset.
- Cross-device performance matrix: per-camera-group metrics.
- Published benchmarks for comparison: Gulshan 2016 (AUC 0.990 Messidor-2), Rakhlin 2017 (AUC 0.967 Messidor-2), Saxena 2020 (AUC 0.92 Messidor-2), Ting 2017 (AUC 0.936 referable DR across 10 datasets).
- Clinical screening metrics: Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2).

### 4.5 Experiment 4: Explainability Analysis via Grad-CAM
- **Tests:** H-5 (Explainability — preprocessing shifts CNN attention toward lesion regions)
- **Evidence target:** ARGUMENT_MAP PC-7

#### 4.5.1 Grad-CAM Generation Protocol
- Model: EfficientNet-B4 pre-trained on ImageNet, fine-tuned on EyePACS.
- Sampling: 10 randomly selected images per DR class (50 total).
- Two pipelines compared: (1) Baseline — crop+resize+ImageNet normalize (Stages 1+4); (2) Proposed — full V4 6-stage preprocessing.
- Grad-CAM activation maps generated from the final convolutional layer for the predicted class.

#### 4.5.2 Quantitative ALO and IoU with IDRiD Lesion Masks
- **ALO (primary):** `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)` — measures what fraction of the lesion is covered by model attention. Hypothesis: ALO(preprocessing) > ALO(baseline).
- **IoU (secondary):** `IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)` — symmetric spatial precision. Hypothesis: IoU(preprocessing) > IoU(baseline).
- Both metrics computed per lesion type: microaneurysms, hemorrhages, hard exudates, soft exudates.
- Statistical test: paired test across IDRiD images; significance required for at least 3 of 4 lesion types.
- Boundary: Grad-CAM activation does not constitute clinical localization of pathology — it is an interpretability tool, not a diagnostic output (ARGUMENT_MAP NC-14).

#### 4.5.3 Attention Consistency Across Datasets
- Whether the model attends to similar features on EyePACS, Messidor, and IDRiD images.
- Attention consistency score as a measure of model stability across data distributions.

### Conclusions to Chapter 4
- State H-1, H-2, H-5 outcomes explicitly.
- Report falsifying observations if any hypothesis direction not confirmed (VCR-3).
- Summarize V4 Experiments 1, 2, 4 outcomes: preprocessing dominance (H-1), component hierarchy (PC-8), CLAHE sensitivity (H-2), and explainability (H-5). [Generalization (H-4) and device shift (H-6) covered by V4 Experiments 5 and 6 — Chapter 5.]
- Acknowledge confounds and boundary conditions.

---

## CHAPTER 5: RELIABILITY VALIDATION AND COMPARATIVE ANALYSIS

**Chapter Function:** Strengthen claim robustness through cross-database generalization, device domain shift evaluation, and benchmarking.

<!-- V3: Old Experiments 5 and 6 merged into V3 Experiment 3 (now in §4.4). Chapter 5 is restructured as validation and analysis. -->

### 5.1 Explainability Results
- Presentation of Grad-CAM comparison results from V4 Experiment 4 (§4.5).
- Grad-CAM overlays for representative images from each DR class (0–4) — with vs. without preprocessing.
- ALO scores (primary) and IoU scores (secondary) between Grad-CAM activations and IDRiD pixel-level lesion masks per lesion type.
- Attention consistency maps across datasets — whether the model attends to similar features on EyePACS, Messidor, and IDRiD images.

### 5.4 Statistical Validation

#### 5.4.1 Bootstrap Confidence Intervals and Mixed-Effects Model
- Bootstrap 95% CI (≥ 1000 iterations) on all primary metrics across all experiments.
- Mixed-effects model for cross-fold analysis in V4 Experiment 1 (fold as random effect).
- McNemar test for paired classification comparison (V4 Experiment 1: B vs A, D vs C).
- DeLong test for ROC-AUC comparison (V4 Experiments 1, 5, and 6).
- Bonferroni/Holm correction for multiple comparisons (V4 Experiments 1, 2).

#### 5.4.2 Final Claim Strength Classifications
- Final claim strength classifications for PC-1 through PC-9 based on accumulated experimental evidence.
- Classification levels: STRONG, MODERATE, CONDITIONAL, per ARGUMENT_MAP §VI methodology.
- Conditions for strength promotion documented for each claim.

### 5.5 Comparative Analysis with Published Systems

#### 5.5.1 Benchmarking Against Published Results: IDx-DR, EyeNuk, DeepMind
- Literature-based comparison using published metrics.
- **Critical boundary:** No controlled experiment against named systems under identical conditions. This is contextual benchmarking, not a superiority claim (CFC-2.2; ARGUMENT_MAP NC-2).

#### 5.5.2 Performance-Complexity Trade-Off Analysis
- Resource efficiency: EfficientNetB0 "high accuracy-to-computation ratio" (LC-CONF, p. 498).
- Computational cost comparison between architectures tested.
- Boundary: Claims about computational efficiency are hardware-specific (DGL-2).

### 5.6 Limitations and Boundary Conditions of the Proposed Approach
- Comprehensive enumeration of all INVARIANTS scope boundaries (SB-1 through SB-4).
- Dataset-bound generalization (DGL-1); hardware-specific reproducibility (DGL-2); clinical population non-extrapolation (DGL-3).
- CLAHE parameter portability limitation (DGL-5); transfer learning domain gap (DGL-6).
- Non-claims enumeration (ARGUMENT_MAP §VII, NC-1 through NC-17):
  - NC-14: Grad-CAM activation does not constitute clinical localization — interpretability tool only.
  - NC-15: External Image Ingestion Protocol validated only for specific Kazakh medical center data.
  - NC-16: Device domain shift results do not constitute device certification or regulatory compliance.
  - NC-17: Preprocessing component hierarchy bounded to tested architectures and datasets.

### Conclusions to Chapter 5
- State final claim strength classifications for PC-1 through PC-9.
- Summarize hypothesis outcomes for H-1 through H-6: confirmed, partially confirmed, or falsified (per VCR-3).
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
- Configurable pipeline parameters based on the validated 6-stage V4 preprocessing pipeline (§3.1): canonical orientation (Stage 0a: canonical flip; Stage 0b: OD-fovea rotation normalization), FOV crop+resize (PIL-based), flat-field correction (σ=45), upgraded CLAHE (dual-constraint clip limit, LAB L-channel), ImageNet normalization, integrated augmentation.
- Link to PC-1: the preprocessing-CNN pipeline validated experimentally constitutes the AI processing module core.

#### 6.2.2 Inference Module with Model Selection Logic
- Model selection between ResNet-50, EfficientNet-B3, and EfficientNet-B4 based on computational resource availability and deployment context.
- Note: Device domain shift results from V4 Experiment 6 (§4.4) inform deployment variability considerations — performance variance across camera groups should be factored into model selection and deployment strategy for environments with heterogeneous camera hardware.

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
- Summarize hypothesis outcomes: H-1, H-2, H-4, H-5, H-6 — confirmed, partially confirmed, or falsified (per VCR-3). [V3 NOTE: H-3 DROPPED — not tested in V3]
- Enumerate primary contributions (provisions submitted for defense) with final claim strength classifications for PC-1 through PC-9.
- Restate scope boundaries and non-claims (NC-1 through NC-17).
- Identify directions for future work: prototype implementation, clinical validation trial, architecture comparison, demographic subgroup evaluation, CLAHE parameter portability testing, extended device domain shift evaluation, prospective explainability validation.

---

## REFERENCES

- All sources cited per self-citation transparency rule (SIR-4).
- LC-CONF and LC-KBTU identified as non-independent sources sharing identical experimental data (SIR-5).
- Sensitivity formula anomaly in LC-SQOPUS_Q2 noted per SIR-3.

---

## APPENDICES

### Appendix A — Source Code of the Preprocessing Pipeline
- Complete implementation code for the 6-stage V4 preprocessing pipeline.

### Appendix B — Supplementary Experimental Results and Confusion Matrices
- Per-class confusion matrices for all experiments (Chapters 4–5).
- Training/validation loss and accuracy curves.

### Appendix C — System Architecture UML Diagrams
- Component, sequence, class, activity, and ER diagrams (Chapter 6).

### Appendix D — Certificates of Implementation and Approbation Acts
- Conference participation certificates; publication confirmations.

### Appendix E — Grad-CAM Visualization Gallery
- Representative Grad-CAM overlay images per DR class (0–4), with and without preprocessing.
- Visual comparison of attention maps between baseline (crop+resize+ImageNet normalize) and full V4 6-stage preprocessing pipeline.
- Selected examples from EyePACS, Messidor, and IDRiD to demonstrate attention consistency across datasets.

### Appendix F — Device Domain Shift Supplementary Tables
- Per-camera performance matrices: Accuracy, F1-score, ROC-AUC for each camera group (Canon, Topcon, Kowa, Zeiss).
- Cross-dataset × cross-camera performance heatmaps.
- Supplementary statistical tables for V4 Experiments 5 and 6.

---

## TRACEABILITY MATRIX

| Outline Section | Experiment | Hypothesis Tested | Primary Claim | Sub-Claims | Literature Cards | Invariant Constraints |
|---|---|---|---|---|---|---|
| §4.2 | V4 Exp 1 | H-1 | PC-1 | SC-1.1, SC-1.2, SC-1.4 ~~SC-1.3~~ (removed) | LC-SQOPUS_Q3, LC-CONF | EH-3, EH-4, OD-1, OD-3 |
| §4.3 | V4 Exp 2 | H-2 (sub-analysis) | PC-8 / PC-2 | SC-2.1, SC-2.2 | LC-SQOPUS_Q2, LC-SQOPUS_Q3 | DGL-5, CFC-1.2, SIR-3 |
| §4.4 | ~~Exp 3~~ [DROPPED — robustness] | — | ~~PC-1 (robustness evidence)~~ | — | — | OD-1 |
| §4.5 | V4 Exp 4 | H-5 | PC-7 | — | — | NC-14 |
| §4.4 (gen.) | V4 Exp 5 | H-4 | PC-6 | — | — | OD-4, DGL-1 |
| §4.4 (dev.) | V4 Exp 6 | H-6 | PC-9 | — | — | DGL-1, NC-16 |
| §4.4 (v1.0 ref) [DROPPED] | — | ~~H-3~~ DROPPED | ~~PC-3~~ DEMOTED | SC-3.1, SC-3.2 | LC-CONF, LC-KBTU, LC-SQOPUS_Q2 | SIR-4, SIR-5, SIR-7 |
| §2.4 | — | — | PC-4 | SC-4.1 | LC-KazUTB | SB-1.5, SIR-6, CFC-2.4 |
| §6.1–6.4 | — | — | PC-5 | SC-5.1 | LC-NAN_RK | SB-4.1, SB-4.2, SB-4.3, DGL-4 |

---

*End of MASTER_OUTLINE.md*
*Binding references: DISSERTATION_INVARIANTS.md v4.0 | ARGUMENT_MAP.md v4.0 | GLOSSARY_v4.0*
*Document Version: 4.1 — V4 sync: V4 6-stage pipeline (canonical orientation [Stage 0a: canonical flip; Stage 0b: OD-fovea rotation normalization], flat-field correction, dual-constraint CLAHE, ImageNet normalization, integrated augmentation); Exp 1 expanded to 6 configs A–F; V3 merged Exp 3 split back into V4 Exp 5 (generalization) and V4 Exp 6 (device shift); 5-fold CV → 3-fold; ALO primary metric; IoU secondary. Updated 2026-03-26: Stage 0 expanded to 0a+0b; EyePACS 40% subset notation added.*
*All structural decisions traceable to the governing source corpus.*
