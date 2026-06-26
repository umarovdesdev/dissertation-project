# MASTER OUTLINE
## Doctoral Dissertation: Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Master Structural Outline — Chapter-by-Chapter Content Specification
**Binding References:** INVARIANTS.md v6.0.0 | ARGUMENT_MAP.md v6.0.0 | HYPOTHESIS.md v6.0.0 | GLOSSARY_EN.md | TABLE_OF_CONTENTS_EN.md
**Source Corpus:** LC-CONF | LC-KBTU | LC-KazUTB | LC-NAN_RK | LC-SQOPUS_Q2 | LC-SQOPUS_Q3
**Governing Documents:** CENTRAL_THESIS.md | CORE_OBJECTIVE.md | HYPOTHESIS.md

---

## FRONT MATTER

### Normative References
- List of standards governing dissertation format, terminology, and citation practice.

### Definitions
- Source: GLOSSARY_EN.md, Part A (Structured Glossary Table).
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
1. Integration of an 8-stage preprocessing pipeline — comprising canonical flip (Stage 0), OD-fovea rotation normalization (Stage 1), FOV crop + isotropic resize + zero-padding (Stage 2), FOV mask generation (Stage 3), adaptive flat-field correction (Stage 4), upgraded CLAHE with dual-constraint clip limit in LAB color space (Stage 5), augmentation (Stage 6), and dataset-specific normalization (Stage 7) — into a CNN-based DR classification pipeline as a unified framework, not isolated techniques (LC-SQOPUS_Q3, p. 81; LC-SQOPUS_Q2, §1).
2. Two-stage fine-tuning protocol for EfficientNetB0 tailored to fundus image variability (LC-CONF, p. 497; LC-KBTU, §II.1) [V3: retained as training strategy; H-3 dropped].
3. Mathematical modeling of laser-tissue interaction for retinal therapy with qualitative simulation (LC-KazUTB, §II.1) — bounded as theoretical contribution only (INVARIANTS SB-1.5; ARGUMENT_MAP PC-4).
4. Modular AI-driven system architecture for DR screening in resource-limited environments (LC-NAN_RK, §II.1) — bounded as design specification only (INVARIANTS SB-4.1; ARGUMENT_MAP PC-5).
5. Cross-dataset transferability validation on APTOS 2019 without retraining, with generalization ratio metric (G = F1_APTOS / F1_EyePACS, target G ≥ 0.85) — demonstrating pipeline robustness beyond the training domain (ARGUMENT_MAP PC-6).
6. Grad-CAM explainability analysis with quantitative ALO (primary metric: Attention–Lesion Overlap, `ALO = area(GradCAM ∩ lesion) / area(lesion)`) and IoU (secondary metric) against IDRiD pixel-level lesion masks (microaneurysms, hemorrhages, hard exudates, soft exudates) — providing causal evidence that preprocessing redirects CNN attention to clinically relevant structures (ARGUMENT_MAP PC-7).
7. Component-level ablation of the 8-stage preprocessing pipeline (7 levels: baseline → +canonical flip → +OD-fovea rotation normalization → +isotropic resize + FOV mask → +adaptive flat-field correction → +dual-constraint CLAHE → full pipeline) identifying a ranked contribution hierarchy among the stages (ARGUMENT_MAP PC-8).
8. Device domain shift evaluation across 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss) on RFMiD, DDR, ODIR-5K — quantifying cross-device performance variability for deployment readiness assessment (ARGUMENT_MAP PC-9).

### Research Goal
- To develop and experimentally validate an integrated fundus image enhancement and CNN-based classification framework for automated multi-stage diabetic retinopathy diagnosis, with specific emphasis on contrast-adaptive preprocessing (including upgraded CLAHE with threshold control) to improve microvascular feature visibility and classification robustness under variable image quality and constrained computational conditions. The framework is further validated for generalization across multiple independent datasets (Messidor, Messidor-2, IDRiD), explainability via Grad-CAM attention analysis, and robustness under device domain shift across camera hardware (RFMiD, DDR, ODIR-5K).

### Research Objectives
1. Analyze the current state of automated DR diagnosis, fundus image quality variability, device-specific acquisition challenges, and deep learning approaches to retinal image classification (→ Chapter 1).
2. Formalize the mathematical foundations of image enhancement techniques, CNN-based classification, transfer learning theory, explainability methods (CAM, Grad-CAM), and image quality metrics (CNR, VVI, SSIM, Entropy) (→ Chapter 2).
3. Design the 8-stage preprocessing pipeline (canonical flip [Stage 0] → OD-fovea rotation normalization [Stage 1] → FOV crop + isotropic resize + zero-padding [Stage 2] → FOV mask generation [Stage 3] → adaptive flat-field correction [Stage 4] → upgraded CLAHE [Stage 5] → augmentation [Stage 6] → dataset-specific normalization [Stage 7]) and integrate it with ResNet-50, EfficientNet-B3, and EfficientNet-B4 architectures (→ Chapter 3).
4. Experimentally validate the integrated pipeline dominance hypothesis (H-1) via 2×2 factorial ablation on EyePACS (100%, ~35,126 images) with ResNet-50 and EfficientNet-B3, 4 configurations A–D, 5-fold CV (→ Chapter 4, Experiment 1).
5. Validate the preprocessing component contribution hierarchy via component-level ablation on EyePACS (→ Chapter 4, Experiment 2) and CLAHE threshold sensitivity (H-2) as a sub-analysis, plus flat-field σ sweep.
6. Validate cross-dataset transferability to APTOS 2019 without retraining, generalization ratio G ≥ 0.85 (H-4) (→ Chapter 4, Experiment 3).
7. Validate explainability via Grad-CAM on EfficientNet-B4 with ALO (primary) and IoU (secondary) against IDRiD lesion masks and Clinical qualitative Grad-CAM (H-5) (→ Chapter 4, Experiment 4).
8. Validate clinical degradation resistance (H-7) on IDRiD + Messidor-2 (→ Chapter 4, Experiment 5).
9. Validate device domain shift on RFMiD/DDR/ODIR-5K across camera hardware (H-6) (→ Chapter 4, Experiment 6).
10. Validate small data training on IDRiD → Clinical dataset, 5-fold CV (→ Chapter 4, Experiment 7).
8. Design a modular system architecture for automated DR screening deployable in resource-limited environments, informed by multi-dataset and multi-device experimental evidence (→ Chapter 6).

### Object and Subject of Research
- **Object:** Fundus images of patients with diabetic retinopathy, sourced from EyePACS (primary training), APTOS 2019 (cross-dataset transferability), IDRiD (explainability + CLAHE sweep), Messidor-2 (clinical degradation), DDR/ODIR-5K/RFMiD (device domain shift), and Clinical dataset (small data, Exp 7).
- **Subject:** The process of automated multi-stage DR classification through integrated preprocessing and CNN-based analysis.

### Research Hypothesis
- Verbatim from HYPOTHESIS.md, mapped to INVARIANTS §II:
  - **H-1 (Primary — Integrated Pipeline Dominance):** See INVARIANTS §II, H-1. The independent variable is the composite *(preprocessing × pretraining source)* pair (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL). Dependent variables: Accuracy, F1-score, ROC-AUC, Cohen's Kappa. Tested on ResNet-50 and EfficientNet-B3 on EyePACS 100% (4 configs A–D, 5-fold CV). Empirical dominance criterion: EH-3 (weighted F1 Δ ≥ 5 pp; ROC-AUC Δ ≥ 0.02; no Cohen's Kappa degradation). Attribution of the observed effect to preprocessing alone, pretraining alone, or their interaction is **forbidden** under CFC-2.8; permissible claims are restricted to the integrated pipeline as a whole.
  - **H-2 (Secondary — Component Ablation + CLAHE/σ Sweeps):** See INVARIANTS §II, H-2. Bounded to tested parameter range on EyePACS/IDRiD; no extrapolation permissible.
  - **H-3 [DROPPED V3]:** H-3 is not tested. Empirical reference from LC-CONF / LC-KBTU cited as prior self-publications only (SIR-4).
  - **H-4 (Cross-Dataset Transferability — APTOS 2019):** Models trained on EyePACS with pipeline generalize to APTOS 2019 without retraining, achieving generalization ratio G ≥ 0.85 (G = F1_APTOS / F1_EyePACS).
  - **H-5 (Explainability):** Preprocessing shifts CNN attention toward clinically relevant lesion regions: ALO between Grad-CAM activation maps and IDRiD lesion masks is higher for preprocessed models than baseline (ALO_preproc > ALO_baseline) — ALO is the PRIMARY metric. IoU_preproc > IoU_baseline is the secondary condition.
  - **H-6 (Device Domain Shift):** Preprocessed models maintain classification performance across images from different fundus camera domains (Canon, Topcon, Kowa, Zeiss), as evaluated on DDR, ODIR-5K, RFMiD.
  - **H-7 (Clinical Degradation Resistance):** preprocessing reduces cross-dataset performance drop compared to baseline, evaluated on IDRiD + Messidor-2.

### Methodological Basis
- Experimental comparison with controlled conditions (matched dataset, hardware, training budget).
- Multi-metric evaluation framework: weighted F1-score, ROC-AUC, Cohen's Kappa, Accuracy (INVARIANTS EH-1).
- Transfer learning theory; CNN feature extraction and classification; adaptive histogram equalization theory.
- 5-fold cross-validation with patient-level split; mixed-effects model for cross-fold analysis.
- Bonferroni/Holm correction for multiple comparisons.
- Grad-CAM explainability analysis with quantitative ALO (primary) and IoU (secondary) against lesion masks.
- Calibration metrics: Expected Calibration Error (ECE), Brier Score.
- Image quality metrics: Contrast-to-Noise Ratio (CNR), Vessel Visibility Index (VVI), Structural Similarity Index (SSIM), Image Entropy.
- Cross-validation and statistical reliability protocols (INVARIANTS EH-4).

### Provisions Submitted for Defense
0. **Paradigmatic framing (methodological, non-empirical):** The integrated preprocessing-CNN paradigm (P2) is positioned as conceptually more productive than the end-to-end CNN paradigm (P1) for five-class DR classification across heterogeneous fundus conditions — argued discursively in §1.4–§1.5, feeds the central thesis IT-1 (ARGUMENT_MAP PC-0; codes P1/P2, SIR-9, CFC-2.9, SB-1.12). [Spec stub — full PC-0 prose belongs to the §1.4/§1.5 writing loop.]
1. The integrated 8-stage preprocessing pipeline (canonical flip, OD-fovea rotation normalization, FOV crop + isotropic resize + zero-padding, FOV mask generation, adaptive flat-field correction, upgraded CLAHE, augmentation, dataset-specific normalization) produces statistically measurable improvement in five-class DR classification independently for both ResNet-50 and EfficientNet-B3 on EyePACS 100% (ARGUMENT_MAP PC-1).
2. CLAHE clip limit parameter exhibits a parameter-dependent sensitivity profile with identifiable local optimum on IDRiD (ARGUMENT_MAP PC-2).
3. Two-stage fine-tuning of EfficientNetB0 outperforms frozen-only strategy (ARGUMENT_MAP PC-3) [V3 DEMOTED: PC-3 is no longer a primary provision; cited as prior work only].
4. Coupled thermal-optical mathematical model provides theoretical grounding for laser-tissue interaction (ARGUMENT_MAP PC-4; theoretical claim only).
5. Modular system architecture specification for DR screening in resource-limited environments (ARGUMENT_MAP PC-5; design specification only).
6. Models trained on EyePACS with the 8-stage preprocessing pipeline generalize to APTOS 2019 without retraining, achieving generalization ratio G ≥ 0.85 (G = F1_APTOS / F1_EyePACS) (ARGUMENT_MAP PC-6).
7. Grad-CAM analysis demonstrates that preprocessing redirects CNN attention toward clinically relevant lesion regions: ALO_preproc > ALO_baseline on IDRiD lesion masks (ALO is the PRIMARY metric; IoU_preproc > IoU_baseline is secondary) (ARGUMENT_MAP PC-7).
8. Component-level ablation (Levels 0–6) identifies a ranked contribution hierarchy among the pipeline stages, measured by incremental weighted F1 improvement on EyePACS (ARGUMENT_MAP PC-8).
9. Preprocessed models maintain classification performance across images from different fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss), as evaluated on RFMiD, DDR, ODIR-5K (ARGUMENT_MAP PC-9).

### Theoretical Significance
- Mathematical formalization of modified CLAHE with simplified threshold control (T/80 formulation adapted from LC-SQOPUS_Q2).
- Theoretical framework for the integrated preprocessing-CNN paradigm as a driver of diagnostic performance (Integrated Pipeline Dominance hypothesis, H-1; composite preprocessing × pretraining IV per CFC-2.8).
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
- Motivation for device domain shift evaluation (Experiment 6) and preprocessing pipeline normalization across camera domains.

### 1.3 Deep Learning Approaches to Retinal Image Classification

#### 1.3.1 Convolutional Neural Network Architectures for Medical Imaging
- General CNN architecture: input, convolutional/pooling layers, fully connected layers (GLOSSARY §1, CNN definition).
- Architectures relevant to DR: EfficientNet family, ResNet, VGG, DenseNet.
- Boundary: Dissertation evaluates ResNet-50, EfficientNet-B3, and EfficientNet-B4; no claim of architectural optimality (INVARIANTS SB-3.1; ARGUMENT_MAP NC-6).

#### 1.3.2 Transfer Learning and Self-Supervised Pretraining in Ophthalmic Diagnostics
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

#### 2.1.2 Formalization of CLAHE with Dual-Constraint Clip Limit
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

#### 2.3.3 In-Domain Self-Supervised Pretraining for Retinal Imaging
- Ophthalmology-specific self-supervised pretraining (DINO / BYOL / SimCLR / MoCo family, selected empirically) on an unlabeled retinal fundus corpus without DR labels, producing retina-aware initialization weights for the CNN backbone (HYPOTHESIS H-1 v6.0.0; INVARIANTS Section X).
- In-domain (retinal) initialization vs. natural-image (ImageNet) initialization: expected sample-efficiency and clinical-generalization benefit; transferability is not theoretically guaranteed and is evaluated empirically (DGL-6).
- Composite-IV note: the integrated arm of H-1 combines this SSL initialization with preprocessing; per CFC-2.8 it is reported only as part of the integrated configuration, never as an independently attributable factor.
- Literature: #73 (THIN — DINO/BYOL/SimCLR/MoCo-on-fundus primary sources to be acquired).

### 2.4 Mathematical Modeling of Laser-Tissue Interaction in Retinal Therapy

#### 2.4.1 Coupled Thermal-Optical Model of Fundus Tissue Response
- Beer's law for radiation attenuation: I(r,z) = I₀(r)e^(−∫₀ᶻ β(r,ξ)dξ).
- Gaussian beam intensity profile: I₀(r) = (P/πa²)e^(−(r/a)²).
- General heat conduction equation: Coσ(x,y,z,T)∂T/∂t = div(k(x,y,z,T)·grad(T)).
- Finite difference method (explicit scheme) for numerical solution.
- Source: LC-KazUTB, §II.3 (Equations 1–8).
- Findings: Surface layers (cornea) exhibit faster temperature rise; deep layers (choroid, retina) stabilize after continued exposure (ARGUMENT_MAP SC-4.1).
- **Implications for diagnostic image feature interpretation (consolidated — formerly §2.4.2; folded into this subsection's closing, see drafts/2.4.1-draft.md):** Qualitative support for understanding thermal effects on retinal features visible in fundus images; framed as epistemically independent of the diagnostic preprocessing–CNN system (reflected in §0.9 theoretical significance, PC-4).
- **Critical boundary:** No quantitative clinical validation; computational simulation only (INVARIANTS SB-1.5; SIR-6). Model omits blood perfusion term; tissue properties treated as static (LC-KazUTB, §II.7). The claim that simulation "confirms effectiveness of laser therapy" is the source's claim, not the dissertation's validated finding (SIR-6; CFC-2.4).

> **Structure note (2026-06-16):** §2.4 is a single consolidated subsection (§2.4.1). The
> originally planned §2.4.2 was folded into §2.4.1's closing during drafting; TOC_EN/TOC_KZ and
> this outline were synced to match the as-written structure. §2.5 is not renumbered.

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

#### 3.1.1 Pipeline Stage Specification: 8-Stage System

- pipeline definition (8 stages, all always-on except Stage 6 train-only):
  - **(Stage 0) Canonical Flip** (always on): Left→right eye horizontal flip to canonical right-eye orientation.
  - **(Stage 1) OD-Fovea Rotation Normalization** (always on): Classical CV detection of OD (brightest) and fovea (darkest); rotates image so OD→fovea axis is horizontal.
  - **(Stage 2) FOV Crop + Isotropic Resize + Zero-Padding** (always on): Detect FOV circle radius R, crop, scale isotropically to 512×512, zero-pad to preserve geometry. Preserves fundus circle shape (contrast with baseline stretch-resize).
  - **(Stage 3) FOV Mask Generation** (always on): Binary mask (1.0 = fundus, 0.0 = zero-padding) appended as 4th input channel.
  - **(Stage 4) Adaptive Flat-Field Correction** (always on): `corrected = image − GaussianBlur(image, σ=0.07·D) + mean`. Adaptive σ proportional to FOV diameter D.
  - **(Stage 5) Upgraded CLAHE** (always on): Dual-constraint clip limit (`CL_tile = min(clip_factor × tile_area/256, global_threshold × tile_area)`) on LAB L-channel; stochastic at train time (p=0.8).
  - **(Stage 6) Augmentation** (train only): Unified affine + ColorJitter (brightness/contrast/saturation/hue) + Gaussian noise + JPEG compression.
  - **(Stage 7) Dataset-Specific Normalization** (always on, always last): `(x − μ_dataset)/σ_dataset → tensor`; mean/std computed from training set per dataset.
- Baseline (Exp 1 A/C): stretch-resize 512×512 + ImageNet normalize (3 channels).
- Full pipeline (Exp 1 B/D): all 8 stages (4 channels: RGB + FOV mask).

#### 3.1.2 Upgraded CLAHE Algorithm with Dual-Constraint Clip Limit
- Adaptation of T/80 formulation (LC-SQOPUS_Q2) — now applied in LAB color space with dual-constraint clip limit.
- Independent validation within dissertation's framework required per DGL-5.
- Implementation via OpenCV (LC-SQOPUS_Q3, p. 82–83).

#### 3.1.3 Augmentation Strategy for Class Imbalance Mitigation
- Final on-the-fly augmentation pipeline (train only), applied in order: (1) unified affine (rotation, zoom, anisotropic stretch, shear); (2) ColorJitter — brightness/contrast/saturation (each factor ∈ [0.9, 1.1]) and hue (shift ∈ [−0.02, 0.02]), each component p = 0.5; (3) Gaussian noise (σ ∈ [2, 6], p = 0.15); (4) JPEG compression (quality ∈ [70, 100], p = 0.20). The Gaussian-noise and JPEG-compression terms simulate variability in image-acquisition conditions.
- Dual function: regularization (§2.2.3) and class imbalance mitigation.
- Class distribution documented: Class 0 = 73.5% training / 49.3% test; Classes 3+4 = 4.5% training / 13.3% test (LC-CONF, p. 498; ARGUMENT_MAP SC-1.4).

#### 3.1.4 External Image Ingestion Protocol
- Methodological contribution for integrating clinical data from Kazakh medical centers.
- Five-stage protocol: (1) Quality Gate — automated quality assessment and rejection of unusable images, (2) Geometric Standardization — alignment to standard FOV and resolution, (3) Preprocessing Pipeline — application of the 8-stage system, (4) Label Harmonization — mapping institutional labels to standard 5-class DR taxonomy, (5) Distribution Analysis — statistical comparison of ingested data with training distribution.
- Boundary: The ingestion protocol is validated only for specific Kazakh medical center data; generalization to other clinical data sources requires independent validation (ARGUMENT_MAP NC-15).

### 3.2 Design of CNN Architectures for DR Classification

#### 3.2.1 ResNet-50 and EfficientNet-B3 as Primary Experimental Architectures
- **ResNet-50:** 50-layer residual network pre-trained on ImageNet; classification head replaced with 5-class softmax. Serves as Architecture A in the factorial ablation (Experiment 1, configs A, B).
- **EfficientNet-B3:** Compound-scaled architecture pre-trained on ImageNet; classification head replaced with 5-class softmax. Serves as Architecture B in the factorial ablation (Experiment 1, configs C, D).
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

#### 3.3.2 Ophthalmology-Specific Self-Supervised Pretraining of the CNN Backbone
- integrated-arm initialization: the CNN backbone (ResNet-50 or EfficientNet-B3) is initialized from ophthalmology-specific self-supervised pretraining (DINO / BYOL / SimCLR / MoCo family, selected empirically) on an unlabeled retinal fundus corpus without DR labels; the baseline arm uses ImageNet weights (HYPOTHESIS H-1 v6.0.0; INVARIANTS Section X).
- SSL pretraining is performed on the 4-channel input (AOQ-2 resolved v6.0.0); both backbones are used in both arms, preserving the 2×2 (preprocessing × architecture) factorial symmetry.
- Composite-IV boundary: per CFC-2.8, the SSL initialization is reported as part of the integrated configuration and is not independently attributable.
- Literature: #73 (GAP — ophthalmology-SSL primary sources to be acquired).

#### 3.3.3 Two-Stage Fine-Tuning Protocol Design
- Stage 1 (Frozen-layer strategy): Freeze all base layers; train classification head only.
- Stage 2 (Progressive fine-tuning): Unfreeze upper layers; fine-tune with reduced learning rate.
- Optimizer: Adam with StepLR scheduler; callbacks: ReduceLROnPlateau, EarlyStopping (LC-CONF, p. 497, 499–500).

#### 3.3.4 Weighted Loss Function Formulation for Ordinal Class Structure
- Categorical cross-entropy with class weights inversely proportional to class frequency.
- Addresses severe imbalance (Class 0: 73.5% vs. Class 4: 2.0% in training).

### 3.4 Evaluation Framework and Performance Metrics

#### 3.4.1 Multi-Metric Assessment Framework
- **Primary metrics (EH-1):** weighted F1-score > ROC-AUC > Cohen's Kappa (quadratic weights) > Accuracy.
- **Secondary metrics (EH-2):** per-class precision/recall, macro averages, training-set metrics (overfitting diagnosis only).
- **Clinical screening metrics:** Sensitivity, Specificity, PPV, NPV for referable DR (grade ≥ 2) — applied in Experiments 3 and 5.
- **Calibration metrics:** Expected Calibration Error (ECE), Brier Score — applied in Experiment 1.
- **Image quality metrics:** Contrast-to-Noise Ratio (CNR), Vessel Visibility Index (VVI), Image Entropy, Structural Similarity Index (SSIM) — applied in Experiment 2 pipeline analysis.
- **Explainability metrics:** Grad-CAM ALO (primary) and IoU (secondary) with IDRiD lesion masks (per lesion type), attention consistency score across datasets — applied in Experiment 4.
- **Generalization metric:** G = F1_external / F1_EyePACS per OD-4 — applied in Experiment 3.
- Diagnostic effectiveness thresholds per INVARIANTS OD-5: Accuracy ≥ 0.80, weighted F1 ≥ 0.80, ROC-AUC ≥ 0.90, Cohen's Kappa ≥ 0.70.

#### 3.4.2 Cross-Validation and Statistical Reliability Protocols
- **5-fold cross-validation with patient-level split:** All experiments use 5-fold CV with patient-level split to prevent data leakage. For each fold, 4 folds serve as training and 1 fold as test. All metrics reported as mean ± standard deviation across 5 folds.
- **Mixed-effects model:** Cross-fold analysis accounting for fold as random effect (Experiment 1).
- **Bonferroni/Holm correction:** Multiple comparison correction across configurations (Experiments 1, 2).
- **McNemar test:** Paired classification comparison (Experiment 1).
- **DeLong test:** ROC-AUC comparison (Experiments 1, 3, 5, 6).
- **Bootstrap 95% CI:** ≥ 1000 iterations on all primary metrics (all experiments).
- Empirical dominance criterion (EH-3): weighted F1 Δ ≥ 5 pp AND ROC-AUC Δ ≥ 0.02 AND no Cohen's Kappa degradation.
- Sufficient validation criterion (EH-4): EH-3 on EyePACS + direction confirmed on secondary datasets + replication across ≥ 2 architectures.

### Conclusions to Chapter 3
- Summarize the complete methodological specification; confirm reproducibility conditions.

---

## CHAPTER 4: EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

**Chapter Function:** Execute Experiments 1–7; report results for H-1, H-2, H-4, H-5, H-6, H-7 with full boundary conditions.

### 4.1 Datasets and Experimental Configuration

#### 4.1.1 Dataset Architecture
- **EyePACS (Primary Training):** ~35,126 labeled images (100%), five-class DR staging (DR 0–4), Canon CR-1 camera. Primary dataset for Experiments 1, 2, 3, 4, 5, 6. Public dataset.
- **APTOS 2019 (Cross-Dataset Transferability):** ~3,662 labeled samples. Five-class DR staging. Mixed camera models. External test dataset for Experiment 3 (zero-shot transfer from EyePACS, G ≥ 0.85).
- **IDRiD (Explainability + CLAHE Sweep + Small Data):** Five-class DR staging with pixel-level lesion annotations. Kowa camera. Datasets for Experiments 2 (CLAHE sweep), 4 (explainability), 5 (clinical degradation), 7 (small data training). Public dataset.
- **Messidor-2 (Clinical Degradation):** Topcon camera. Dataset for Experiment 5 (clinical degradation resistance H-7). Public dataset.
- **RFMiD (Device Domain Shift):** Topcon, Kowa cameras. Multi-disease including DR subset. Dataset for Experiment 6.
- **DDR (Device Domain Shift):** Canon, Topcon cameras. Five-class DR grading. Dataset for Experiment 6.
- **ODIR-5K (Device Domain Shift):** Canon, Zeiss cameras. Multi-disease including DR subset. Dataset for Experiment 6.
- **Clinical Dataset (Small Data):** Images from Kazakh medical centers. Dataset for Experiment 7. Camera model TBD.

#### 4.1.2 Class Distribution Analysis and Data Partitioning Strategy
- EyePACS class distribution (~35,126 labeled images, 100%) and 5-fold cross-validation with patient-level stratified split.
- Class imbalance as primary confounding factor necessitating weighted F1 and Cohen's Kappa (ARGUMENT_MAP SC-1.4).
- Label harmonization methodology for datasets with non-standard taxonomies (Messidor-2, RFMiD, ODIR-5K).

#### 4.1.3 Hardware Specification and Reproducibility Protocol
- Document specific hardware configuration (DGL-2).
- Fixed random seeds, versioned code repository, and environment specification for full reproducibility.
<!-- SC-1.3 REMOVED V3: Processing time differential claim deleted as implausible. Do not restore. -->

### 4.2 Experiment 1: Integrated Pipeline Dominance on EyePACS
- **Tests:** H-1 (Integrated Pipeline Dominance)
- **Evidence target:** ARGUMENT_MAP PC-1

#### 4.2.1 Factorial Design (4 Configurations A–D)
- A 2×2 factorial experimental design to isolate the independent effects of preprocessing vs. architecture:
  - Factor A: Preprocessing (baseline 3ch stretch-resize + ImageNet normalize vs. full 8-stage pipeline 4ch)
  - Factor B: Architecture (ResNet-50 vs. EfficientNet-B3)
- Four controlled experimental configurations:
  - **Config A:** baseline (3ch) + ResNet-50
  - **Config B:** full pipeline (4ch) + ResNet-50
  - **Config C:** baseline (3ch) + EfficientNet-B3
  - **Config D:** full pipeline (4ch) + EfficientNet-B3
- All experiments conducted under matched dataset partitions (5-fold CV with patient-level split), hardware configuration, optimizer settings, and training budgets.
- Statistical analysis: Mixed-effects model across folds; McNemar test for paired comparison; DeLong test for ROC-AUC comparison; Bootstrap 95% CI.
- Integrated Pipeline Dominance (H-1) is considered supported only if the integrated arm outperforms the baseline arm satisfying EH-3 criteria independently for both ResNet-50 (B > A) and EfficientNet-B3 (D > C) (attribution to preprocessing alone is forbidden, CFC-2.8).

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

#### 4.3.1 Ablation Design (Levels 0–6)
- Sequential addition of pipeline stages to isolate individual contributions:
  - Level 0: Baseline (3ch stretch-resize + ImageNet normalize)
  - Level 1: + Canonical flip (Stage 0)
  - Level 2: + OD-fovea rotation normalization (Stage 1)
  - Level 3: + Isotropic resize + FOV mask (Stages 2+3+7, 4ch)
  - Level 4: + Adaptive flat-field correction (Stage 4)
  - Level 5: + Upgraded CLAHE (Stage 5)
  - Level 6: Full pipeline (all stages incl. augmentation Stage 6)
- Also: CLAHE parameter sweep (clip_factor × global_threshold grid on IDRiD) and flat-field σ sweep.
- Weighted F1 and image quality metrics (CNR, VVI, Entropy, SSIM) at each level.

#### 4.3.2 CLAHE Threshold Sensitivity Analysis (H-2 Sub-Analysis)
- Clip limit parameter sweep across controlled values on IDRiD.
- Document sensitivity curve; identify local optimum within tested range.
- No extrapolation to untested values (INVARIANTS H-2; CFC-1.2).
- If no identifiable optimum found → H-2 falsification per VCR-3.

#### 4.3.3 Impact on Feature Preservation in Microaneurysms and Small Vessels
- Per-class F1-score analysis for DR 1 and DR 2 (microaneurysm and small vessel features).
- Independent validation of CLAHE parameters within dissertation framework (DGL-5).
- Sensitivity formula anomaly note if citing LC-SQOPUS_Q2 figures (SIR-3).

### 4.4 Experiment 3: Cross-Dataset Transferability on APTOS 2019 (H-4)
- **Tests:** H-4 (Cross-Dataset Transferability)
- **Evidence target:** ARGUMENT_MAP PC-6

#### 4.4.1 Zero-Shot Transfer to APTOS 2019
- Models trained on EyePACS with full pipeline applied directly to APTOS 2019 without retraining.
- Generalization ratio G = F1_APTOS / F1_EyePACS per OD-4. Target: G ≥ 0.85.

#### 4.4.2 Baseline vs Pipeline Comparison
- Compare G for baseline (3ch) vs pipeline (4ch) to show preprocessing improves cross-dataset generalization.

### 4.5 Experiment 4: Grad-CAM Explainability on IDRiD + Clinical (H-5)
- **Tests:** H-5 (Explainability — preprocessing shifts CNN attention toward lesion regions)
- **Evidence target:** ARGUMENT_MAP PC-7

#### 4.5.1 Grad-CAM Generation Protocol
- Model: EfficientNet-B4 pre-trained on ImageNet, fine-tuned on EyePACS with pipeline.
- IDRiD: 10 images per DR class (50 total). Clinical: qualitative Grad-CAM overlays.
- Two conditions: baseline (3ch) vs pipeline (4ch).

#### 4.5.2 Quantitative ALO and IoU with IDRiD Lesion Masks
- **ALO (primary):** `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)`. Hypothesis: ALO(integrated) > ALO(baseline).
- **IoU (secondary):** `IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)`. Hypothesis: IoU(integrated) > IoU(baseline).
- Per lesion type: microaneurysms, hemorrhages, hard exudates, soft exudates.
- Boundary: Grad-CAM activation is interpretability, not diagnostic localization (ARGUMENT_MAP NC-14).

#### 4.5.3 Attention Consistency Across Datasets
- Cosine similarity of Grad-CAM distributions across dataset pairs.

### 4.6 Experiment 5: Clinical Degradation Resistance (H-7)
- **Tests:** H-7 (preprocessing reduces cross-dataset performance drop)
- **Datasets:** EyePACS → IDRiD + Messidor-2
- pipeline should narrow cross-dataset performance gap compared to baseline.

### 4.7 Experiment 6: Device Domain Shift (H-6)
- **Tests:** H-6 (Device Robustness)
- **Datasets:** EyePACS → DDR + ODIR-5K + RFMiD
- Cross-device F1 variance reduction: preprocessed models maintain performance across Canon, Topcon, Kowa, Zeiss.
- Boundary: Results do not constitute device certification (ARGUMENT_MAP NC-16).

### 4.8 Experiment 7: Small Data Training (IDRiD → Clinical)
- **Datasets:** IDRiD (5-fold CV training) → Clinical dataset evaluation
- Small data training with pipeline; qualitative Grad-CAM on Clinical images.

### Conclusions to Chapter 4
- State H-1, H-2, H-4, H-5, H-6, H-7 outcomes explicitly.
- Report falsifying observations if any hypothesis direction not confirmed (VCR-3).
- Acknowledge confounds and boundary conditions.

---

## CHAPTER 5: RELIABILITY VALIDATION AND COMPARATIVE ANALYSIS

**Chapter Function:** Strengthen claim robustness through cross-database generalization, device domain shift evaluation, and benchmarking.

<!-- v6.0.0: all seven experiments live in Chapter 4 (§4.2–§4.8); Chapter 5 is Reliability Validation and Comparative Analysis. -->

### 5.1 Explainability Results
- Presentation of Grad-CAM comparison results from Experiment 4 (§4.5).
- Grad-CAM overlays for representative images from each DR class (0–4) — with vs. without preprocessing.
- ALO scores (primary) and IoU scores (secondary) between Grad-CAM activations and IDRiD pixel-level lesion masks per lesion type.
- Attention consistency maps across datasets — whether the model attends to similar features on EyePACS, Messidor, and IDRiD images.

### 5.2 Statistical Validation

#### 5.2.1 Bootstrap Confidence Intervals and Mixed-Effects Model
- Bootstrap 95% CI (≥ 1000 iterations) on all primary metrics across all experiments.
- Mixed-effects model for cross-fold analysis in Experiment 1 (fold as random effect).
- McNemar test for paired classification comparison (Experiment 1: B vs A, D vs C).
- DeLong test for ROC-AUC comparison (Experiments 1, 3, 5, and 6).
- Bonferroni/Holm correction for multiple comparisons (Experiments 1, 2).

#### 5.2.2 Final Claim Strength Classifications
- Final claim strength classifications for PC-1 through PC-10 based on accumulated experimental evidence.
- Classification levels: STRONG, MODERATE, CONDITIONAL, per ARGUMENT_MAP §VI methodology.
- Conditions for strength promotion documented for each claim.

### 5.3 Comparative Analysis with Published Systems

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
- Non-claims enumeration (ARGUMENT_MAP §VII, NC-1 through NC-17):
  - NC-14: Grad-CAM activation does not constitute clinical localization — interpretability tool only.
  - NC-15: External Image Ingestion Protocol validated only for specific Kazakh medical center data.
  - NC-16: Device domain shift results do not constitute device certification or regulatory compliance.
  - NC-17: Preprocessing component hierarchy bounded to tested architectures and datasets.

### Conclusions to Chapter 5
- State final claim strength classifications for PC-1 through PC-10.
- Summarize hypothesis outcomes for H-1, H-2, H-4, H-5, H-6, H-7: confirmed, partially confirmed, or falsified (per VCR-3).
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
- Configurable pipeline parameters based on the validated 8-stage preprocessing pipeline (§3.1): canonical flip (Stage 0), OD-fovea rotation normalization (Stage 1), FOV crop + isotropic resize (Stage 2), FOV mask generation (Stage 3), adaptive flat-field correction (σ = 0.07 × FOV diameter, Stage 4), dual-constraint CLAHE on the LAB L-channel (Stage 5), integrated augmentation (Stage 6), and dataset-specific normalization (Stage 7).
- Link to PC-1: the preprocessing-CNN pipeline validated experimentally constitutes the AI processing module core.

#### 6.2.2 Inference Module with Model Selection Logic
- Model selection between ResNet-50, EfficientNet-B3, and EfficientNet-B4 based on computational resource availability and deployment context.
- Note: Device domain shift results from Experiment 6 (§4.7) inform deployment variability considerations — performance variance across camera groups should be factored into model selection and deployment strategy for environments with heterogeneous camera hardware.

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
- Summarize hypothesis outcomes: H-1, H-2, H-4, H-5, H-6, H-7 — confirmed, partially confirmed, or falsified (per VCR-3). [H-3 DROPPED — not tested]
- Enumerate primary contributions (provisions submitted for defense) with final claim strength classifications for PC-1 through PC-10.
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
- Complete implementation code for the 8-stage preprocessing pipeline.

### Appendix B — Supplementary Experimental Results and Confusion Matrices
- Per-class confusion matrices for all experiments (Chapters 4–5).
- Training/validation loss and accuracy curves.

### Appendix C — System Architecture UML Diagrams
- Component, sequence, class, activity, and ER diagrams (Chapter 6).

### Appendix D — Certificates of Implementation and Approbation Acts
- Conference participation certificates; publication confirmations.

### Appendix E — Grad-CAM Visualization Gallery
- Representative Grad-CAM overlay images per DR class (0–4), with and without preprocessing.
- Visual comparison of attention maps between baseline (stretch-resize + ImageNet normalize) and full 8-stage preprocessing pipeline.
- Selected examples from EyePACS, Messidor, and IDRiD to demonstrate attention consistency across datasets.

### Appendix F — Device Domain Shift Supplementary Tables
- Per-camera performance matrices: Accuracy, F1-score, ROC-AUC for each camera group (Canon, Topcon, Kowa, Zeiss).
- Cross-dataset × cross-camera performance heatmaps.
- Supplementary statistical tables for Experiments 5 and 6.

---

## TRACEABILITY MATRIX

| Outline Section | Experiment | Hypothesis Tested | Primary Claim | Sub-Claims | Literature Cards | Invariant Constraints |
|---|---|---|---|---|---|---|
| §1.4–§1.5 | — | — | PC-0 (paradigmatic framing) | — | LITERATURE_INDEX Paradigm column; #12 (Gulshan, canonical P1) | SIR-9, CFC-2.9, SB-1.12 |
| §4.2 | Exp 1 | H-1 | PC-1 | SC-1.1, SC-1.2, SC-1.4 ~~SC-1.3~~ (removed) | LC-SQOPUS_Q3, LC-CONF | EH-3, EH-4, CFC-2.8, OD-1, OD-3 |
| §4.3 | Exp 2 | H-2 (+ component ablation) | PC-8 / PC-2 | SC-2.1, SC-2.2 | LC-SQOPUS_Q2, LC-SQOPUS_Q3 | DGL-5, CFC-1.2, SIR-3 |
| §4.4 | Exp 3 | H-4 | PC-6 | — | — | OD-4, DGL-1 |
| §4.5 | Exp 4 | H-5 | PC-7 | — | — | NC-14 |
| §4.6 | Exp 5 | H-7 | PC-10 | — | — | OD-4, DGL-1 |
| §4.7 | Exp 6 | H-6 | PC-9 | — | — | DGL-1, NC-16 |
| §4.8 | Exp 7 | — | — | — | — | DGL-1 |
| §2.4 | — | — | PC-4 | SC-4.1 | LC-KazUTB | SB-1.5, SIR-6, CFC-2.4 |
| §6.1–6.4 | — | — | PC-5 | SC-5.1 | LC-NAN_RK | SB-4.1, SB-4.2, SB-4.3, DGL-4 |

*Historical note (v6.0.0): H-3 is dropped (not tested); PC-3 (two-stage fine-tuning) is demoted to a prior-work citation only; the old §4.4 "Robustness to Image Degradation" experiment is removed.*

---

*End of MASTER_OUTLINE.md*
*Binding references: INVARIANTS.md v6.0.0 | ARGUMENT_MAP.md v6.0.0 | HYPOTHESIS.md v6.0.0 | CENTRAL_THESIS.md v6.0.0 | CONTRIBUTIONS.md v6.0.0 | RESEARCH_ARCHITECTURE.md v6.0.0 | GLOSSARY_EN.md*
*Document Version: 6.0.0 — v6.0.0 sync: 8-stage pipeline (canonical flip → OD-fovea rotation normalization → FOV crop + isotropic resize → FOV mask → adaptive flat-field correction σ=0.07·D → dual-constraint CLAHE → augmentation → dataset-specific normalization); Experiment 1 = 2×2 factorial, 4 configs A–D (ResNet-50 A/B, EfficientNet-B3 C/D), 5-fold CV; H-1 = Integrated Pipeline Dominance (composite preprocessing × pretraining IV, baseline⟹ImageNet vs integrated⟹ophthalmology-SSL, CFC-2.8); all seven experiments in Chapter 4 (§4.2–§4.8), Chapter 5 = Reliability Validation (§5.1 Explainability, §5.2 Statistical, §5.3 Comparative, §5.4 Limitations); added §2.3.3 and §3.3.2 SSL sections; PC-0 paradigmatic framing + PC-10 clinical degradation; H-3 dropped, ALO primary / IoU secondary.*
*All structural decisions traceable to the governing source corpus.*
