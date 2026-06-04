# LITERATURE INDEX
## External Source Corpus — Navigation Table

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Generated from:** Literature Cards in /LITERATURE/
**Total sources indexed:** 82
**Version:** Updated to v3.0 — aligned with INVARIANTS v3.0 and MASTER_OUTLINE v3.0 (source corpus expanded with method/architecture/explainability/domain-adaptation foundations, #54–#82)

---

### Section Map Key

| Code | Dissertation Section |
|------|---------------------|
| §1.1.1 | Pathophysiology and Clinical Grading Systems |
| §1.1.2 | Screening Requirements in Resource-Limited Healthcare Settings |
| §1.2.1 | Sources of Image Degradation in Clinical Practice |
| §1.2.2 | Impact of Image Quality on Diagnostic Model Performance |
| §1.2.3 | Device-Specific Variability in Fundus Imaging (NEW v2.1) |
| §1.3.1 | CNN Architectures for Medical Imaging |
| §1.3.2 | Transfer Learning Strategies in Ophthalmic Diagnostics |
| §1.3.3 | Explainability Methods in Medical Image Classification (NEW v2.1) |
| §1.4   | Critical Analysis of Existing Automated DR Screening Systems |
| §1.5   | Formulation of Research Problem |
| §2.1.1 | Histogram Equalization and Adaptive Contrast Enhancement |
| §2.1.2 | Formalization of CLAHE with Controllable Threshold Parameters |
| §2.1.3 | Spatial Filtering and Noise Reduction Methods |
| §2.2.1 | Convolution, Pooling, and Feature Extraction Operations |
| §2.2.2 | Loss Functions and Optimization for Imbalanced Medical Datasets |
| §2.2.3 | Regularization Techniques: Dropout, Batch Normalization, Data Augmentation |
| §2.3.1 | Feature Transferability Across Visual Domains |
| §2.3.2 | Frozen-Layer versus Progressive Fine-Tuning Strategies |
| §2.4.1 | Coupled Thermal-Optical Model of Fundus Tissue Response |
| §2.5   | Explainability in Deep Learning for Medical Imaging (NEW v2.1) |
| §2.5.1 | CAM / Grad-CAM Theory and Formalization (NEW v2.1) |
| §2.5.2 | Attention Map Interpretation (NEW v2.1) |
| §2.5.3 | IoU as Metric for Explainability Evaluation (NEW v2.1) |
| §2.6   | Image Quality Metrics for Preprocessing Evaluation (NEW v2.1): CNR, VVI, Entropy, SSIM |
| §3.1   | Formalization of the Unified Preprocessing Pipeline (5-component pipeline, v2.1) |
| §3.1.4 | External Image Ingestion Protocol (NEW v2.1 — methodological contribution) |
| §3.2   | Design of ResNet-50 / EfficientNet-B3 Architectures (v2.1 — replaces Baseline/Enhanced CNN) |
| §3.3   | Transfer Learning Methodology Using EfficientNetB0 and ResNet50 |
| §3.4   | Evaluation Framework and Performance Metrics (expanded v2.1: clinical, calibration, image quality) |
| §4.1   | Datasets and Experimental Configuration (EyePACS, APTOS 2019, IDRiD, Messidor, RFMiD, DDR, ODIR-5K) |
| §4.2   | Experiment 1: Causal Improvement (Preprocessing vs Architecture) (v2.1) |
| §4.3   | Experiment 2: Preprocessing Component Ablation (NEW v2.1) |
| §4.4   | Experiment 3: Robustness to Image Degradation (NEW v2.1) |
| §4.5   | Experiment 4: Explainability Analysis (NEW v2.1) |
| §5.1   | Experiment 5: Clinical Generalization (v2.1) |
| §5.2   | Explainability Results (v2.1) |
| §5.3   | Experiment 6: Device Domain Shift (NEW v2.1) |
| §5.4   | Statistical Validation (v2.1) |
| §5.5   | Comparative Analysis with Published Systems (v2.1) |
| §5.6   | Limitations and Boundary Conditions (v2.1) |
| §6.1   | System Requirements and Design Principles |
| §6.2   | Modular Architecture with PACS and EHR Integration |
| §6.3   | Clinical Workflow Integration |
| INTRO  | Introduction (contextual framing) |

---

### Source Index

The **Paradigm** column was added in governance v5.3 to support the paradigmatic framing (P1 / P2 / N/A) per INVARIANTS v5.3 SIR-9. See the *Notes* section below for the full classification rule.

| # | Source | Type | Key Result | Dataset | Paradigm | Maps to |
|---|--------|------|------------|---------|----------|---------|
| 01 | Pratt et al. (2016) | CNN classification | 75% acc, 30% sens, 95% spec, 5-class DR, Kaggle | EyePACS/Kaggle | P1 | §1.3.1, §2.2.2, §2.2.3, INTRO |
| 02 | Saxena et al. (2020) | Cross-dataset validation | AUC 0.958 Messidor-1, 0.92 Messidor-2, binary DR, InceptionResNetV2 | EyePACS/Kaggle, Messidor-1, Messidor-2 | P1 | §1.3.2, §1.4, §3.1, §5.1, §5.3, §5.5 |
| 03 | Sánchez-Gutiérrez et al. (2022) | Clinical validation | AUC 0.988, 90.5% sens, 97.1% spec, 96% workload reduction, RetCAD | Private (Ramon y Cajal) | P1 | §1.4, §6.3 |
| 04 | Arrieta et al. (2022) | CNN classification | AUC 0.94 EyePACS, 0.89 Messidor-2, semi-supervised with 2% labels | EyePACS/Kaggle, Messidor-2 | P1 | §1.3.1, §2.3.1, §5.1 |
| 05 | Rakhlin (2017) | Cross-dataset validation | AUC 0.967 Messidor-2, 0.923 Kaggle, modified VGGNet | EyePACS/Kaggle, Messidor-2 | P1 | §1.2.2, §1.3.1, §5.1, §5.5 |
| 06 | Porwal et al. (2018) | Dataset descriptor | IDRiD: 516 images, 81 pixel-annotated, Indian population, 5-class DR | IDRiD | N/A | §1.1.2, §4.1, §4.5, §5.2, INTRO |
| 07 | Baget-Bernaldiz et al. (2021) | External validation | AUC 0.988 RDR own pop., 0.968 Messidor, 4-class ICDR | Private (Spanish), Messidor-1, EyePACS/Kaggle | P1 | §1.4, §5.1, §5.5 |
| 08 | Wan et al. (2021) | Segmentation | SE 92.77% exudates (e_ophtha_EX), AUPR 0.78 hard exudates (IDRiD) | IDRiD, e_ophtha_EX, Private | P1 | §1.3.1, §2.2.1 |
| 09 | Xu et al. (2024) | Ensemble / Hybrid | Acc 0.97, AUC 0.97, EfficientNet+Swin Transformer V2 hybrid, 5-class | APTOS 2019 | P1 | §1.3.1, §1.3.2, §3.2 |
| 10 | Porwal et al. (2018) | Dataset descriptor | IDRiD: 516 images, pixel-level lesion masks + DR/DME grading, Indian pop. | IDRiD | N/A | §1.1.2, §4.1, §4.5, §5.2, INTRO |
| 11 | Ting et al. (2017) | External validation | AUC 0.936 referable DR, validated on 10 multiethnic datasets (AUC 0.889–0.983) | SIDRP (private), 10 external cohorts | P1 | §1.4, §5.1, §5.5, §6.3 |
| 12 | Gulshan et al. (2016) | CNN classification | AUC 0.991 EyePACS-1, 0.990 Messidor-2, Inception-v3 ensemble | EyePACS (private), Messidor-2 | P1 (canonical representative) | §1.3.1, §1.3.2, §1.4, §5.1, §5.5, INTRO |
| 14 | Wewetzer et al. (2021) | Meta-analysis | Pooled sens 87%, spec 90%, SROC AUC 0.9543, 10 DL screening studies in PC | Multiple (pooled) | N/A | §1.4, §5.5, §6.3, INTRO |
| 15 | Liu et al. (2022) | Benchmark study | κw 0.9303 DR grading, 0.70 image quality accuracy, EfficientNet dominant | DeepDRiD | P1 | §1.2.2, §1.3.1, §3.1, §4.1 |
| 16 | Goh et al. (2024) | CNN classification | SWIN AUC 95.7% Kaggle, 97.3% SEED, 96.3% Messidor-1, ViT > CNN | EyePACS/Kaggle, SEED, Messidor-1 | P1 | §1.3.1, §5.1, §5.4, §5.5 |
| 17 | Voets et al. (2019) | Cross-dataset validation | AUC 0.951 EyePACS, 0.853 Messidor-2 (reproduction of Gulshan 2016) | EyePACS/Kaggle, Messidor-2 | P1 | §1.2.2, §1.5, §5.1, §5.4 |
| 18 | González-Díaz et al. (2024) | ViT comparison | ViT acc 83.69%, BEiT F1 86.36%, 4-class AMD, 305 images | Private (curated AMD) | P1 | §1.3.1 |
| **19** | **Sapakova et al. (2025)** 🔹SELF | **Transfer learning** | **F1 0.74 fine-tuned vs 0.62 frozen, EfficientNetB0, 5-class DR** | **APTOS 2019, Private clinical** | **P1 (prior self-work)** | **§2.3.2, §3.3, §4.2, §4.1, §2.2.2, §2.2.3, §3.1** |
| **20** | **Sapakova et al. (2024)** 🔹SELF | **Mathematical modeling** | **Thermal model of laser-fundus interaction, FDM simulation, qualitative** | **None (simulation)** | **N/A** | **§2.4.1** |
| **21** | **Yesmukhamedov et al. (2025a)** 🔹SELF | **Transfer learning** | **Precision 75% fine-tuned vs 65% frozen, EfficientNetB0, 5-class DR** | **APTOS 2019, Private clinical** | **P1 (prior self-work)** | **§2.3.2, §3.3, §4.2, §3.1, §3.4, §2.2.2, §2.2.3** |
| **22** | **Yesmukhamedov et al. (2025b)** 🔹SELF | **System architecture** | **Modular AI diagnostic architecture for Kazakhstan, physician-in-the-loop** | **None (design study)** | **N/A** | **§6.1, §6.2, §6.3, §1.4, §1.1.2** |
| **23** | **Sapakova, Yesmukhamedov & Sapakov (2025a)** 🔹SELF | **CLAHE / Enhancement** | **100% acc/sens/spec, upgraded CLAHE T/80 + ResNet50, 5-class retinal** | **STARE** | **P2-tending (prior self-work toward V5)** | **§2.1.2, §3.1, §3.3, §4.3, §5.5, §2.1.1** |
| **24** | **Sapakova, Yesmukhamedov & Sapakov (2025b)** 🔹SELF | **Preprocessing study** | **Val acc 71%→86% with preprocessing, ROC-AUC 0.9638, 4-layer CNN** | **APTOS 2019, Private clinical** | **P2-tending (prior self-work toward V5)** | **§3.1, §3.2, §4.2, §4.1, §2.1.2, §5.4, §1.2.2** |
| 25 | Wikipedia — Adaptive Histogram Equalization | Background reference | Algorithmic description of AHE/CLAHE; clip limit 3–4, 8×8 tile grid | N/A | §2.1.1, §2.1.2 |
| 26 | Shaout & Han (2025) | Preprocessing study | FCE+CLAHE 59% preference, 88% combined; fuzzy logic + CLAHE blending | DRIVE | N/A (preprocessing method, no CNN comparison) | §2.1.1, §3.1 |
| 27 | Hayati et al. (2023) | CLAHE / Enhancement | CLAHE improved 3/4 CNNs; EfficientNetB4 97.83% acc; ResNet34 −12.02% | APTOS 2019 | P1 (preprocessing varied but treated as exogenous factor) | §2.1.1, §2.1.2, §3.1, §4.3, §5.4 |
| 28 | Brancati et al. (2025) | Peripheral (FHIR / breast ML) | MLP 97.67% acc breast lesion, 3 hand-crafted features, BUSI | BUSI | N/A | Peripheral |
| 29 | Tabari et al. (2024) | Review / Survey (FHIR) | 27 studies reviewed; FHIR pipeline-based (21) vs non-linear (6) models | None (scoping review) | N/A | Peripheral |
| 30 | Chakka (2023) | Preprocessing study | Rescaling best of 4 techniques for OCT; ResNet-50; no numerical metrics | Kaggle OCT (4,480 images) | P1 | §2.1.1 |
| 31 | Kesharwani et al. (2021) | Review / Survey (clinical) | Narrative DR review; 95% vision loss preventable if treated early | None (narrative review) | N/A | §1.1.1 |
| 32 | Kusuhara et al. (2018) | Review / Survey (clinical) | DR prevalence 34.6%; pericyte dropout → BRB breakdown; VEGF/Ang2 pathways | None (narrative review) | N/A | §1.1.1 |
| 33 | Gettinger et al. (2025) | Review (pathophysiology / experimental models) | No single model reproduces full human DR phenotype; STZ limited to early-stage | None (narrative review) | N/A | §1.1.1, INTRO |
| 34 | Morya et al. (2024) | Review (pathophysiology / treatment) | DR present in 1/3 of diabetic patients; 35–55% screening compliance; Remidio 98% sens | None (narrative review) | N/A | §1.1.1, §1.1.2, §6.3 |
| 35 | Wang & Lo (2018) | Review (pathophysiology / treatment) | Neurodegeneration may precede microvasculopathy; anti-VEGF first-line for DME/PDR | None (narrative review) | N/A | §1.1.1, INTRO |
| 36 | Nandal (2024) | Empirical (AI-driven HL7/FHIR interoperability) | 93% semantic mapping precision; F1=0.89 NLP extraction; 97% interoperability | MIMIC-III, Synthetic HL7 | N/A | §6.2 |
| 37 | Geetha & Hema (2026) | ViT hybrid (DR + glaucoma) | 98.4% acc; ViT + BFF + HGS optimizer; no external validation | Open-source (unnamed) | P1 | §1.3.1 |
| 38 | Khosravi et al. (2025) | External validation (retinal hemorrhage) | FastViT AUC 0.9811, ResNet18 AUC 0.9626; 2661-image external dataset | RFMiD, DeepEyeNet, BRSET, Private (multi-country) | P1 | §1.3.1, §5.1, §5.3 |
| 39 | Senapati et al. (2024) | Systematic review (DR AI) | PRISMA-based; 2016–2023; EyePACS 75,523 images; identifies overfitting + class imbalance gaps | Multiple (surveyed) | N/A (survey) | §1.4, §1.5, §2.2.2 |
| 40 | Araf et al. (2024) | Systematic review (cost-sensitive learning) | 173 papers reviewed; CSL preserves distribution; only 2 validation studies identified | Multiple (surveyed) | N/A (survey) | §2.2.2, §3.4 |
| 41 | Sharma et al. (2025) | ViT-CapsNet hybrid (DR) | 94% acc on EyePACS (30,262 images); AUC 0.44–0.56 per class; no external validation | EyePACS/Kaggle | P1 | §1.3.1, §4.1 |
| 42 | Arora et al. (2024) | CNN classification (DR) | EfficientNetB0 avg acc 0.8653; max training acc 97.11%; undersampled to 3,704 images | Kaggle DR Resized (35,108 images) | P1 | §1.3.1, §2.2.2 |
| 43 | Ryu et al. (2021) | CNN classification + external validation (OCTA) | AUC 0.960–0.976 internal; AUC 0.938–0.962 external; ResNet101 on OCTA | Private (single-center) | P1 | §1.3.1, §1.4 |
| 44 | Zhang et al. (2022) | Multicentre external validation (DR screening) | AUROC 0.9931 referable DR (image); 0.9848 (patient); Cohen's κ 0.86–0.93 vs experts | Private (83,465 images, 4 centres) | P1 | §1.4, §5.1, §5.5, §6.3 |
| 45 | Ruamviboonsuk et al. (2022) | Prospective clinical validation (DR screening) | Acc 94.7%, sens 91.4% VTDR; outperformed specialists (p=0.024); 9 Thai sites | Private (7,651 patients, prospective) | P1 | §1.4, §5.5, §6.3 |
| 46 🆕 | Selvaraju et al. (2017) "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization" | Explainability method | Grad-CAM visualization of CNN decisions; gradient-weighted class activation mapping | ImageNet / various | N/A (methodology reference) | §2.5.1, §2.5.2, §1.3.3, §4.5, §5.2 |
| 47 🆕 | Cuadros & Bresnick (2009) "EyePACS: An Adaptable Telemedicine System for Diabetic Retinopathy Screening" — OR — Kaggle Diabetic Retinopathy Detection competition descriptor | Dataset descriptor | ~35,126 labeled fundus images (Kaggle labeled partition), 5-class DR grading (0–4), Canon CR-1 camera | EyePACS/Kaggle | N/A | §4.1, §1.2.3, INTRO |
| 48 🆕 | Decencière et al. (2014) "Feedback on a Publicly Distributed Image Database: The Messidor Database" — OR — Messidor-2 dataset descriptor | Dataset descriptor | 1,748 images (Messidor-2), Topcon TRC NW6 camera, referable/non-referable + DR grade | Messidor / Messidor-2 | N/A | §4.1, §5.1, INTRO |
| 49 🆕 | Pachade et al. (2021) "Retinal Fundus Multi-Disease Image Dataset (RFMiD)" | Dataset descriptor | 3,200 images, multi-disease retinal dataset, Topcon TRC-NW300 and Kowa cameras | RFMiD | N/A | §4.1, §1.2.3, §5.3 |
| 50 🆕 | Li et al. (2019) "Diagnostic Assessment of Deep Learning Algorithms for Diabetic Retinopathy Screening" — OR — DDR dataset descriptor | Dataset descriptor | DR grading dataset, Canon and Topcon fundus cameras | DDR | N/A | §4.1, §1.2.3, §5.3 |
| 51 🆕 | TO BE IDENTIFIED — ODIR-5K challenge dataset descriptor (Peking University) | Dataset descriptor | Multi-disease ocular dataset, Canon and Zeiss fundus cameras, ~5,000 patients | ODIR-5K | N/A | §4.1, §1.2.3, §5.3 |
| 52 🆕 | Guo et al. (2017) "On Calibration of Modern Neural Networks" | Calibration methodology | ECE metric definition, calibration analysis of modern deep networks, Brier Score | ImageNet / CIFAR | N/A (methodology reference) | §2.6, §3.4, §5.4 |
| 53 🆕 | Wang et al. (2004) "Image Quality Assessment: From Error Visibility to Structural Similarity" | Image quality metric | SSIM definition, structural similarity index for image quality evaluation | Various (image quality benchmarks) | N/A (methodology reference) | §2.6, §3.1 |
| 54 🆕 | Pizer et al. (1987) "Adaptive Histogram Equalization and Its Variations" | Image enhancement method | Introduces **clipped AHE (CLAHE precursor)**; histogram clipping limits noise over-enhancement; qualitative medical-image eval | Medical images (CT/MRI/angiography, qualitative) | N/A (methodology reference) | §2.1.1, §2.1.2 |
| 55 🆕 | Tomasi & Manduchi (1998) "Bilateral Filtering for Gray and Color Images" | Image filtering method | Bilateral filter: edge-preserving smoothing via joint geometric + photometric weighting; qualitative | None (illustrative images) | N/A (methodology reference) | §2.1.3 |
| 56 🆕 | Buades et al. (2011) "Non-Local Means Denoising" | Image denoising method | Non-Local Means: averages non-local similar patches; patchwise PSNR gain; qualitative | None (illustrative images) | N/A (methodology reference) | §2.1.3 |
| 57 🆕 | Zhou et al. (2016) "Learning Deep Features for Discriminative Localization" (CAM) | Explainability method | **Class Activation Mapping (CAM)** via global average pooling; weakly-supervised localization (37.1% top-5 loc error, ILSVRC) | ILSVRC / various | N/A (methodology reference) | §2.5.1, §2.5.2, §1.3.3 |
| 58 🆕 | Chattopadhyay et al. (2018) "Grad-CAM++" | Explainability method | Grad-CAM++ improves localization & multi-instance handling over Grad-CAM (avg-drop 36.8% vs 46.6%, ImageNet) | ImageNet, VOC, CIFAR-10 | N/A (methodology reference) | §2.5.1, §2.5.2, §1.3.3, §4.5 |
| 59 🆕 | Tjoa & Guan (2020) "A Survey on Explainable AI (XAI): towards Medical XAI" | Review / Survey (XAI) | Taxonomy of XAI methods toward medical XAI; perceptive vs mathematical-structure interpretability | None (survey) | N/A (survey) | §1.3.3, §2.5 |
| 60 🆕 | Samek et al. (2017) "Explainable AI: Understanding, Visualizing and Interpreting Deep Learning Models" | Methodology / Review (XAI) | XAI framework; LRP > sensitivity analysis; perturbation-based explanation evaluation | ImageNet, 20 Newsgroups, HMDB51 | N/A (methodology reference) | §1.3.3, §2.5 |
| 61 🆕 | Lundberg & Lee (2017) "A Unified Approach to Interpreting Model Predictions" (SHAP) | Explainability method | **SHAP**: unique additive feature attribution (local accuracy/missingness/consistency); Kernel & Deep SHAP | MNIST, synthetic, human study | N/A (methodology reference) | §2.5, §1.3.3 |
| 62 🆕 | Ribeiro et al. (2016) "Why Should I Trust You?: Explaining the Predictions of Any Classifier" (LIME) | Explainability method | **LIME**: model-agnostic local surrogate explanations; >90% feature recall; SP-LIME for global view | Text + image (Inception) | N/A (methodology reference) | §2.5, §1.3.3 |
| 63 🆕 | Rezatofighi et al. (2019) "Generalized Intersection over Union" (GIoU) | Metric / Loss (IoU) | **Generalized IoU** metric & loss; non-zero gradient for non-overlapping boxes; improves detector localization | PASCAL VOC, MS COCO | N/A (methodology reference) | §2.5.3 |
| 64 🆕 | Everingham et al. (2010) "The PASCAL Visual Object Classes (VOC) Challenge" | Dataset descriptor / Benchmark | Defines **Average Precision** and **IoU > 0.5** detection criterion; 9,963 images, 20 classes | PASCAL VOC | N/A | §2.5.3, §3.4 |
| 65 🆕 | Krizhevsky et al. (2012) "ImageNet Classification with Deep CNNs" (AlexNet) | CNN architecture | **AlexNet**; 8-layer CNN, ReLU + dropout + PCA color augmentation; ImageNet top-5 err 15.3% | ImageNet / ILSVRC | N/A (architecture reference) | §1.3.1, §2.2.1, §2.2.3 |
| 66 🆕 | He et al. (2016) "Deep Residual Learning for Image Recognition" (ResNet) | CNN architecture | **ResNet** residual learning; ResNet-50/101/152 (ResNet-50 = dissertation backbone); ImageNet top-5 err 3.57% (ensemble) | ImageNet, CIFAR-10 | N/A (architecture reference) | §1.3.1, §2.2.1, §3.2 |
| 67 🆕 | Huang et al. (2017) "Densely Connected Convolutional Networks" (DenseNet) | CNN architecture | **DenseNet** dense connectivity; feature reuse + parameter efficiency; competitive ImageNet/CIFAR | ImageNet, CIFAR, SVHN | N/A (architecture reference) | §1.3.1, §2.2.1 |
| 68 🆕 | Tan & Le (2019) "EfficientNet: Rethinking Model Scaling for CNNs" | CNN architecture | **EfficientNet** compound scaling (B0–B7); B7 84.4% top-1; **EfficientNet-B3 = dissertation backbone** | ImageNet + 8 transfer datasets | N/A (architecture reference) | §1.3.1, §3.2 |
| 69 🆕 | Tan & Le (2021) "EfficientNetV2: Smaller Models and Faster Training" | CNN architecture | EfficientNetV2; training-aware NAS + progressive learning; faster training; surpasses ViT-L/16(21k) | ImageNet, ImageNet21k + transfer | N/A (architecture reference) | §1.3.1, §3.2 |
| 70 🆕 | Dosovitskiy et al. (2021) "An Image is Worth 16×16 Words" (ViT) | ViT architecture | **Vision Transformer**; pure transformer on image patches; ViT-H/14 88.55% ImageNet; "large-scale training trumps inductive bias" | ImageNet/21k, JFT-300M | N/A (architecture reference) | §1.3.1 |
| 71 🆕 | Yosinski et al. (2014) "How Transferable Are Features in Deep Neural Networks?" | Transfer learning | Layer-wise feature transferability; lower layers general, higher task-specific; fine-tuning > training from scratch | ImageNet (A/B splits) | N/A (methodology reference) | §2.3.1, §2.3.2 |
| 72 🆕 | Kornblith et al. (2019) "Do Better ImageNet Models Transfer Better?" | Transfer learning | ImageNet accuracy predicts transfer (r = 0.99 fixed features, 0.96 fine-tuning) across 12 datasets | 12 transfer datasets | N/A (methodology reference) | §2.3.1, §2.3.2 |
| 73 🆕 | Cheplygina et al. (2018) "Not-so-supervised: A Survey of SSL, MIL and Transfer Learning in Medical Image Analysis" | Review / Survey (medical ML) | Survey of semi-supervised, multi-instance, and transfer learning under limited labels in medical imaging | None (survey) | N/A (survey) | §2.3.1, §2.3.2 |
| 74 🆕 | Zhou et al. (2022) "Domain Generalization: A Survey" | Review / Survey (DG) | Taxonomy of domain-generalization methods; OOD performance degradation under domain shift | None (survey) | N/A (survey) | §1.2.3, §5.3 |
| 75 🆕 | Wang & Deng (2018) "Deep Visual Domain Adaptation: A Survey" | Review / Survey (DA) | Deep domain-adaptation taxonomy (discrepancy / adversarial / reconstruction based) | None (survey) | N/A (survey) | §1.2.3, §5.3 |
| 76 🆕 | Ganin et al. (2016) "Domain-Adversarial Training of Neural Networks" (DANN) | Domain adaptation method | **DANN** + gradient reversal layer; domain-invariant features; e.g. MNIST→MNIST-M 0.767 | MNIST/SVHN/GTSRB/Office, etc. | N/A (methodology reference) | §5.3, §2.3.2 |
| 77 🆕 | Abràmoff et al. (2018) "Pivotal Trial of an Autonomous AI System for DR Detection in Primary Care" (IDx-DR) | Prospective clinical validation | Autonomous IDx-DR; sens 87.2%, spec 90.7%, imageability 96.1%; 900 patients, 10 primary-care sites; FDA pivotal | Private (prospective, 900 pts) | P1 | §1.4, §6.3, INTRO |
| 78 🆕 | Fu et al. (2020) "Evaluation of Retinal Image Quality Assessment Networks in Different Color-spaces" (EyeQ) | Dataset descriptor + RIQA | **EyeQ** (28,792 EyePACS images, 3-level quality grading); MCF-Net 0.9175 acc; image quality affects DR detection | EyeQ (re-annotated from EyePACS) | P1 | §1.2.2, §5.3, §3.1 |
| 79 🆕 | Chin & Shih (2021) "Concisely Indexed Multi-keyword Rank Search on Encrypted Cloud Documents" | Peripheral (encrypted search) | PCA-condensed index for encrypted multi-keyword cloud search; <1/10 storage vs MRSE | BBC text corpus | N/A | Peripheral |
| 80 🆕 | Koch (2019) "Universal Bounds and Monotonicity Properties of Ratios of Hermite and Parabolic Cylinder Functions" | Peripheral (mathematics) | Monotonicity & optimal bounds of Hermite/parabolic-cylinder function ratios; Turán-type inequalities | None (theoretical) | N/A | Peripheral |
| 81 🆕 | Hungerford (1999) "Comments on Proton Emission after Muon Capture" | Peripheral (nuclear physics) | Charged-particle emission after atomic muon capture (~15% in light nuclei); MECO background estimate | None (physics) | N/A | Peripheral |
| 82 🆕 | Ostahie et al. (2015) "Electrical Manipulation of the Edge States in Graphene…" | Peripheral (condensed-matter physics) | Electrically-induced "shortcut edge states" in graphene; unconventional quantum-Hall plateaus | None (simulation) | N/A | Peripheral |

---

### Coverage Matrix

| Dissertation Section | Sources Covering It |
|---------------------|---------------------|
| §1.1.1 | #31, #32, **#33, #34, #35** |
| §1.1.2 | #06, #10, **#22**, #34 |
| §1.2.1 | ⚠️ GAP |
| §1.2.2 | #05, #15, #17, **#24**, #78 |
| §1.2.3 (NEW) | #47, #49, #50, #51, #74, #75 |
| §1.3.1 | #01, #04, #05, #08, #09, #12, #15, #16, #18, #37, #38, #41, #42, #43, #65, #66, #67, #68, #69, #70 |
| §1.3.2 | #02, #09, #12 |
| §1.3.3 (NEW) | #46, #57, #58, #59, #60, #61, #62 |
| §1.4 | #02, #03, #07, #11, #12, #13, #14, **#22**, #39, #43, #44, #45, #77 |
| §1.5 | #17, #39 |
| §2.1.1 | #25, #26, #27, #30, **#23**, #54 |
| §2.1.2 | #25, #27, **#23, #24**, #54 |
| §2.1.3 | #55, #56 |
| §2.2.1 | #08, #65, #66, #67 |
| §2.2.2 | #01, **#19, #21**, #39, #40, #42 |
| §2.2.3 | #01, **#19, #21**, #65 |
| §2.3.1 | #04, #71, #72, #73 |
| §2.3.2 | **#19, #21**, #71, #72, #76 |
| §2.4.1 | **#20** ⚡ THIN |
| §2.5.1 (NEW) | #46, #57, #58 |
| §2.5.2 (NEW) | #46, #57, #58 |
| §2.5.3 (NEW) | #63, #64 |
| §2.6 (NEW) | #52, #53 ⚡ THIN |
| §3.1 | #02, #15, #26, #27, #53, **#19, #21, #23, #24**, #78 |
| §3.1.4 (NEW) | ⚠️ GAP — no external literature; methodological contribution by candidate |
| §3.2 | #09, **#24**, #66, #68, #69, #70 |
| §3.3 | **#19, #21, #23**, #71, #72 |
| §3.4 | **#21**, #40, #52, #64 |
| §4.1 | #06, #10, #15, #47, #48, #49, #50, #51, **#19, #21, #24**, #41 |
| §4.2 | **#19, #21, #24** ⚡ THIN (self-only) |
| §4.3 | #27, **#23** |
| §4.4 | ⚠️ GAP — no external literature on robustness-to-degradation experiments (NEW v2.1 experiment) |
| §4.5 (NEW) | #06, #10, #46, #57, #58 |
| §5.1 (NEW — Exp 5) | #02, #04, #05, #07, #11, #12, #13, #16, #17, #38, #44, #48 |
| §5.2 (NEW — Explainability results) | #06, #10, #16, #17, #27, #46, **#24**, #57, #58 |
| §5.3 (NEW — Exp 6 Device Domain Shift) | #38, #49, #50, #51, #74, #75, #76, #78 |
| §5.4 (NEW — Statistical Validation) | #16, #17, #27, #52, **#24** |
| §5.5 | #02, #05, #07, #11, #12, #13, #14, #16, **#23**, #44, #45 |
| §5.6 (NEW) | — (populated by candidate's own experimental limitations) |
| §6.1 | **#22** ⚡ THIN |
| §6.2 | **#22**, #36 |
| §6.3 | #03, #11, #13, #14, **#22**, #34, #44, #45 |
| INTRO | #01, #06, #10, #12, #14, #33, #35, #47, #48 |

---

### Gaps Identified

**⚠️ GAP (0 sources):**
- §1.2.1 — Sources of Image Degradation in Clinical Practice
- §3.1.4 — External Image Ingestion Protocol (NEW v2.1 — methodological contribution by candidate; no external literature expected)
- §4.4 — Experiment 3: Robustness to Image Degradation (NEW v2.1 — no external literature on controlled degradation experiments for DR preprocessing)

**✅ GAPS RESOLVED in this update (#54–#82):**
- §2.1.3 — Spatial Filtering and Noise Reduction Methods — RESOLVED by #55 (bilateral filtering) and #56 (non-local means).
- §2.5.3 — IoU as Metric for Explainability Evaluation — RESOLVED by #63 (Generalized IoU metric/loss) and #64 (PASCAL VOC IoU > 0.5 criterion).

**⚡ THIN (1 source or thin coverage):**
- §2.4.1 — Coupled Thermal-Optical Model of Fundus Tissue Response (#20 🔹SELF only)
- §2.6 — Image Quality Metrics for Preprocessing Evaluation (#52, #53 — two sources but both are general references, not DR-specific applications)
- §4.2 — Experiment 1: Causal Improvement (#19, #21, #24 🔹SELF only)
- §6.1 — System Requirements and Design Principles (#22 🔹SELF only)

**⬆️ THIN STATUS UPGRADED in this update (#54–#82):**
- §1.3.3 — Explainability Methods (was #46 only) → now #46, #57, #58, #59, #60, #61, #62. **Well-covered.**
- §2.2.1 — Convolution, Pooling, and Feature Extraction (was #08 only) → now #08, #65, #66, #67 (AlexNet/ResNet/DenseNet foundations).
- §2.3.1 — Feature Transferability Across Visual Domains (was #04 only) → now #04, #71, #72, #73.
- §2.5.1 — CAM / Grad-CAM Theory (was #46 only) → now #46, #57 (CAM), #58 (Grad-CAM++).
- §2.5.2 — Attention Map Interpretation (was #46 only) → now #46, #57, #58.
- §5.3 — Experiment 6: Device Domain Shift (was #38, #49, #50, #51 dataset-descriptors only) → now adds #74, #75, #76 (DG/DA literature) + #78 (image-quality), supplying the previously-missing literature on distribution shift.

---

### Notes

**Paradigm column (v5.3) — classification rule.**
Per INVARIANTS v5.3 SIR-9, every CNN-based or ViT-based DR/retinal-image classification source has been tagged as **P1** (end-to-end CNN paradigm; preprocessing as auxiliary step), **P2-tending** (preprocessing explicitly formalised as model component), or **N/A** (methodology reference, dataset descriptor, clinical/pathophysiology review, mathematical model, system architecture, or survey). Tag rationale:
- **P1** — backbone-centric study in which preprocessing is either unreported, reported as a fixed exogenous step, or varied but treated as a tuning input rather than as a formalised model component. The dominant class in the literature corpus.
- **P1 (canonical representative)** — reserved for Gulshan et al. (2016) per SB-1.12 / SIR-9; see gulshan-2016.md §15 Paradigmatic Role for the methodological-practice grounds.
- **P2-tending (prior self-work toward V5)** — the candidate's prior preprocessing studies (#23, #24) that move toward the V5 formalisation but predate the integrated-preprocessing-CNN paradigm as formally defined in this dissertation. Per CFC-2.7 they must be cited as prior own work and as evolutionary precursors of the V5 pipeline, not as full P2 instantiations.
- **N/A** — the source does not have a paradigmatic position in the P1/P2 dichotomy: dataset descriptors, methodology references (Grad-CAM, SSIM, calibration), pathophysiology reviews, mathematical models, system architectures, surveys.

Per CFC-2.9 and SIR-1, no source has been attributed an explicit "preprocessing is unimportant" claim. P1 tagging is a claim about *observable methodological practice*, not about authorial intent. Per CFC-2.2, no Paradigm tag licenses a head-to-head numerical comparison with the source. Per SB-1.12, the Paradigm column does not redefine the dissertation's operational experimental baseline (configs A/C, OD-3).

**Existing notes (retained):**

1. Sources #06 and #10 are **duplicate entries** for the same article (Porwal et al., 2018 — IDRiD dataset descriptor). Consider consolidating to a single entry.
2. ~~Sources #11 and #13 duplicate~~ — RESOLVED: duplicate card removed; Source #11 (ting-2017.md) is the canonical entry.
3. Source #18 (González-Díaz et al., 2024) addresses **AMD, not diabetic retinopathy**. Its relevance is peripheral (ViT architecture comparison only).

**Self-publication notes (retained):**

4. Sources #19–#24 are all **co-authored by the dissertation candidate** (🔹SELF flag). All carry **high self-plagiarism risk** — content must be explicitly self-cited and substantially reformulated in the dissertation.
5. Sources #23 and #24 are **duplicate entries for the same article** (Sapakova, Yesmukhamedov & Sapakov, 2025 — *Eastern-European Journal of Enterprise Technologies*, DOI: 10.15587/1729-4061.2025.335570). Two literature cards were prepared from different analytical perspectives. Consider consolidating to a single entry.
6. Sources #19 (CONF, Procedia CS 2025) and #21 (KBTU, Herald KBTU 2025) report **overlapping experiments** — both evaluate EfficientNetB0 frozen vs. fine-tuned on APTOS 2019 with nearly identical metrics. The dissertation should treat these as a single experimental thread with unified citation.
7. §6.2 (Modular Architecture with PACS and EHR Integration) was **added to the Section Map Key** to accommodate the system architecture content from #22.

**Previous sources notes (#25–#32, retained):**

8. Source #25 (Wikipedia — AHE/CLAHE) is **NOT citable** in a doctoral dissertation. It serves only as a conceptual primer. Original sources (Pizer et al., 1987; Zuiderveld, 1994) should be cited instead. Classified as **Background reference**.
9. Source #26 (Shaout & Han, 2025) is an **arXiv preprint** evaluated by 10-person subjective survey only. Low epistemic weight. Provides reproducible fuzzy+CLAHE pipeline with explicit CLAHE parameters (clipLimit=2.0, tileGridSize=8×8).
10. Source #27 (Hayati et al., 2023) is the **most directly relevant new external source** — it empirically evaluates CLAHE's impact on 4 CNN architectures for binary DR classification on APTOS 2019. Key nuance: CLAHE degraded ResNet34 by −12.02%, complicating universal preprocessing-dominance claims. Published in Procedia Computer Science (conference proceedings); limited-scope study with accuracy-only metrics.
11. Sources #28 (Brancati et al., 2025) and #29 (Tabari et al., 2024) are **domain mismatches** — FHIR/health informatics papers with no relevance to DR deep learning. Classified as **Peripheral**. Should not be included in the dissertation literature review unless clinical deployment infrastructure is discussed.
12. Source #30 (Chakka, 2023) is published in a **high school journal** with minimal peer review. No numerical metrics reported. Extremely low epistemic weight. Classified as **Limited-scope**.
13. Sources #31 (Kesharwani et al., 2021) and #32 (Kusuhara et al., 2018) **resolve the §1.1.1 GAP** (Pathophysiology and Clinical Grading Systems). However, #31 has significant citation errors and was published in a journal flagged for questionable editorial practices — cite with caution. #32 (Kusuhara et al., 2018, *Diabetes & Metabolism Journal*) is the **higher-quality source** for DR pathophysiology.

**New sources notes (#33–#45):**

14. Sources #33 (Gettinger et al., 2025), #34 (Morya et al., 2024), and #35 (Wang & Lo, 2018) are **pathophysiology/treatment narrative reviews** that collectively **strengthen §1.1.1 coverage** from 2 to 5 sources. All three reinforce neurodegeneration-preceding-microvasculopathy claims. None carry AI benchmarking value. #35 (Wang & Lo) provides the strongest clinical trial linkage (DRCR.net Protocol I).
15. Source #34 (Morya et al., 2024) additionally provides **screening compliance data** (35–55%) and **AI screening mentions** (IDxDR, Remidio Medios) — useful for §1.1.2 and §6.3 framing, though AI discussion is high-level and non-architectural.
16. Source #36 (Nandal, 2024) is an **HL7/FHIR interoperability prototype** study. **Peripheral to core DR imaging research**, but directly relevant to §6.2 (PACS/EHR integration). Resolves previous ⚡ THIN status of §6.2 (was covered only by #22 🔹SELF). However: no DOI reported, published in a non-core journal, moderate epistemic weight.
17. Source #37 (Geetha & Hema, 2026) presents a ViT-BFF-HGS hybrid for joint DR/glaucoma detection. **Architecturally novel** but critically flawed: no dataset names disclosed, no external validation, no AUC/CI/statistical testing. High internal accuracy claim (98.4%) unsupported by standard validation. **Use only as transformer-era architectural reference**, not as evidence of generalization.
18. Source #38 (Khosravi et al., 2025) is the **strongest new external validation study** — multi-country (USA, South Korea, Brazil), multi-source (public + private), 2661 external images, FastViT vs ResNet18. **Not DR-focused** (retinal hemorrhage classification) but demonstrates cross-dataset ViT > CNN advantage. Directly supports §5.1 arguments. Caution: severe class imbalance (2346 medical vs 315 trauma) and no CI/statistical tests.
19. Source #39 (Senapati et al., 2024) is a **PRISMA-based systematic review** of DR AI (2016–2023). Provides bibliometric landscape and identifies overfitting, class imbalance, and early-stage detection as key gaps. **Resolves ⚡ THIN status of §1.5** (was covered only by #17). No empirical benchmarking or ViT coverage. Moderate epistemic weight as field-mapping survey.
20. Source #40 (Araf et al., 2024) is the **first systematic review dedicated to cost-sensitive learning in medical data** (173 papers, 2010–2022). Reveals that only 2 of 173 studies were validation research. Strengthens §2.2.2 (loss functions for imbalanced data) and partially addresses §3.4 (evaluation frameworks). No architecture-level or DR-specific benchmarking.
21. Source #41 (Sharma et al., 2025) proposes ViT-CapsNet on EyePACS (30,262 images). **Critical inconsistency**: reported AUC values per class (0.44–0.56) are fundamentally incompatible with claimed 94% accuracy. No external validation, no hyperparameter transparency, no statistical testing. **Cite with extreme caution** — epistemic weight is low due to internal metric inconsistency.
22. Source #42 (Arora et al., 2024) applies EfficientNetB0 to Kaggle DR with undersampling (35,108 → 3,704 images). Internal accuracy 0.8653; max training accuracy 97.11% suggests **significant overfitting** (11-point gap). No AUC, no class-wise metrics, no external validation. CI bounds reported as identical values (likely artifact). Limited epistemic weight.
23. Source #43 (Ryu et al., 2021) is an **OCTA-based DR classification study** with external validation — ResNet101 on OCTA scans, AUC 0.960–0.976 internal, 0.938–0.962 external. **Not fundus-based**, but demonstrates temporal external validation methodology and CNN > handcrafted feature advantage. Useful as modality-shift reference for §1.3.1 and §1.4.
24. Source #44 (Zhang et al., 2022) is a **high-quality multicentre external validation study** published in BMJ Open. Ensemble CNN (Inception-V3/Xception/Inception-ResNet-V2) on 83,465 images from 4 centres. AUROC 0.9931 referable DR, Cohen's κ 0.86–0.93 vs experts. **Strongest new evidence for §5.1 and §5.5**. Limitation: China-only, no public dataset benchmarking, preprocessing not reported.
25. Source #45 (Ruamviboonsuk et al., 2022) is the **highest-impact new source** — prospective clinical validation of DL screening in Thailand's national programme, published in *The Lancet Digital Health*. Sens 91.4% VTDR, outperformed specialists (p=0.024), 9 sites, 7,651 patients. **Gold standard for §6.3 clinical deployment evidence**. Limitation: no architecture transparency, no preprocessing details, single-country.

**Impact of new sources on coverage gaps:**

26. §1.1.1 (Pathophysiology) upgraded from **2 sources to 5 sources** (#31, #32, #33, #34, #35). **Well-covered**.
27. §1.1.2 (Screening Requirements) upgraded from **3 to 4 sources** (added #34 via screening compliance data).
28. §1.4 (Critical Analysis of DR Systems) upgraded from **8 to 12 sources** (added #39, #43, #44, #45). **Very well-covered**.
29. §1.5 (Formulation of Research Problem) upgraded from **⚡ THIN (1 source) to 2 sources** (#17, #39). No longer critically thin.
30. §2.2.2 (Loss Functions / Imbalanced Data) upgraded from **3 to 6 sources** (added #39, #40, #42).
31. §3.4 (Evaluation Framework) upgraded from **⚡ THIN (1 🔹SELF) to 2 sources** (added #40). Now has external support.
32. §5.1 (Cross-Database Generalization) upgraded from **9 to 11 sources** (added #38, #44).
33. §5.5 (Comparative Analysis) carries forward v1.0 §5.3 coverage — upgraded from **9 to 11 sources** (added #44, #45).
34. §6.2 (PACS/EHR Integration) upgraded from **⚡ THIN (1 🔹SELF) to 2 sources** (added #36). Now has external support.
35. §6.3 (Clinical Workflow) upgraded from **5 to 7 sources** (added #34, #44, #45). **Very well-covered**.
36. **Remaining true gaps reduced to 2 (v1.0)**: §1.2.1, §2.1.3. These still require **additional literature acquisition**.
37. **⚠️ Self-only coverage warning (reduced):** Sections §2.4.1, §4.2, §6.1 remain covered **only by self-publications**. External supporting literature is strongly recommended for examiner robustness.
38. **⚠️ Metric inconsistency flag**: Source #41 (Sharma et al., 2025) reports class-level AUC values (0.44–0.56) incompatible with 94% accuracy. Do NOT cite AUC values without explicit disclaimers.

**New notes for v2.1 (#39–#42):**

39. Sources #46–#53 are **new entries added for v2.1** to support expanded experimental design (6 experiments, explainability, device domain shift, calibration metrics). Literature cards must be created for each. Sources #46 (Selvaraju, Grad-CAM), #47 (EyePACS descriptor), #48 (Messidor descriptor), #52 (Guo, calibration), and #53 (Wang, SSIM) are canonical references with well-known citations. Sources #49 (RFMiD), #50 (DDR) are dataset descriptors with likely identifiable papers. Source #51 (ODIR-5K) is marked "TO BE IDENTIFIED" pending confirmation of the authoritative descriptor.
40. §2.5 (Explainability in Deep Learning for Medical Imaging) is a **new theoretical section** requiring Grad-CAM formalization. Source #46 (Selvaraju et al., 2017) is the foundational reference; additional explainability sources (e.g., Zhou et al. 2016 for CAM, Chattopadhyay et al. 2018 for Grad-CAM++) may be needed to bring §2.5.1–§2.5.3 above ⚡ THIN status.
41. §1.2.3 (Device-Specific Variability in Fundus Imaging) and §5.3 (Experiment 6: Device Domain Shift) are **new sections in v2.1**. Sources #49, #50, #51 provide dataset descriptors with camera model information; additional literature on camera-induced distribution shift in retinal imaging is recommended to strengthen the theoretical grounding and avoid dataset-descriptor-only coverage.
42. The v2.1 Section Map Key **replaces v1.0 section numbers**. Existing "Maps to" entries in the Source Index have been updated to v2.1 numbering where applicable. Key remapping: v1.0 §5.3 (Comparative Analysis) → v2.1 §5.5; v1.0 §5.2 (Statistical Validation of Preprocessing Dominance) → v2.1 §5.4; v1.0 §5.1 (Cross-Database Generalization Testing) → v2.1 §5.1 (Experiment 5). Existing "Maps to" entries in individual literature cards should be verified and remapped during literature card updates.

**New sources notes (#54–#82) — foundational method, architecture, explainability, and domain-shift corpus:**

43. Sources #54–#82 are **foundational / methodological references** added to ground the dissertation's preprocessing, architecture, transfer-learning, explainability, and domain-shift chapters in their canonical primary literature. Most are **N/A** under the Paradigm rule (architecture papers, methodology references, surveys, dataset/benchmark descriptors) because they are not CNN/ViT-based **DR/retinal** classification studies. Only #77 (Abràmoff — autonomous DR detection) and #78 (Fu — EyeQ retinal image-quality classification) are retinal-image CNN studies and are tagged **P1**.
44. **CLAHE provenance resolved.** Source #54 (Pizer et al., 1987) introduces *clipped* adaptive histogram equalization — the methodological origin of CLAHE. It is the **citable primary source** that replaces the non-citable Wikipedia entry (#25) flagged in note 8. The dissertation should cite #54 (and Zuiderveld, 1994, if acquired) for CLAHE rather than #25 in §2.1.1–§2.1.2.
45. **§2.1.3 GAP resolved.** Sources #55 (Tomasi & Manduchi — bilateral filtering) and #56 (Buades et al. — non-local means) supply the previously-missing spatial-filtering / noise-reduction literature. Both are method papers with qualitative (not benchmark) evaluation; cite as algorithmic foundations, not as evidence of DR classification gains.
46. **Explainability corpus expanded.** Source #57 (Zhou et al., 2016 — CAM) and #58 (Chattopadhyay et al., 2018 — Grad-CAM++) are the CAM/Grad-CAM lineage explicitly recommended in note 40; together with the existing #46 (Selvaraju — Grad-CAM) they ground §2.5.1–§2.5.2 and Exp 4. Sources #59 (Tjoa & Guan — medical XAI survey), #60 (Samek et al. — LRP), #61 (Lundberg & Lee — SHAP), and #62 (Ribeiro et al. — LIME) broaden §1.3.3/§2.5 to the wider XAI landscape. **Caution:** #61 (SHAP) and #62 (LIME) are feature-attribution methods not used as the dissertation's primary lesion-localization tool — cite as XAI background, not as the operational explainability metric.
47. **§2.5.3 GAP resolved.** Source #63 (Rezatofighi et al. — Generalized IoU) and #64 (Everingham et al. — PASCAL VOC, which defines AP and the IoU > 0.5 detection criterion) provide the formal IoU grounding for explainability-overlap evaluation (ALO/IoU in Exp 4). Both are object-detection references; the dissertation must frame IoU as an *overlap metric borrowed for lesion-localization evaluation*, not as a detection benchmark (consistent with SB/CFC constraints).
48. **CNN backbone provenance.** Sources #65 (AlexNet), #66 (ResNet), #67 (DenseNet), #68 (EfficientNet), #69 (EfficientNetV2) and #70 (ViT) are the canonical architecture papers. **#66 (ResNet-50)** and **#68 (EfficientNet-B3)** are the dissertation's two operational backbones (Exp 1, configs A–D) and should be cited at first mention in §3.2. #70 (ViT) and #69 (EfficientNetV2) support the CNN-vs-ViT discussion (§1.3.1); note that #70 argues "scale > inductive bias," a position **tangential to but not contradicting** the preprocessing-as-model-component thesis — cite with the framing already used for #16/#70-class ViT sources.
49. **Transfer-learning theory.** Sources #71 (Yosinski et al. — layer transferability), #72 (Kornblith et al. — ImageNet-accuracy↔transfer correlation), and #73 (Cheplygina et al. — SSL/MIL/TL medical survey) ground §2.3.1–§2.3.2 (frozen vs fine-tuned), complementing the candidate's own #19/#21 frozen-vs-fine-tuned experiments.
50. **Domain-shift literature.** Sources #74 (Zhou et al. — DG survey), #75 (Wang & Deng — DA survey), and #76 (Ganin et al. — DANN) supply the conceptual and methodological grounding for §1.2.3 and Exp 6 (§5.3 device domain shift), which was previously covered by dataset descriptors only. These are general-purpose (non-retinal) references; cite for problem framing, not as retinal-domain-shift evidence.
51. Source #77 (Abràmoff et al., 2018 — IDx-DR pivotal trial) is a **high-impact prospective clinical-validation precedent** (FDA-authorized autonomous DR system, multi-site, masked reference standard). Strongest new support for §1.4 and §6.3 clinical-deployment arguments. **Limitation:** no preprocessing ablation and no public-benchmark comparison — it does not isolate preprocessing effects and must not be cited as evidence for the preprocessing-dominance hypothesis.
52. Source #78 (Fu et al., 2020 — EyeQ) re-annotates **28,792 EyePACS images** into a 3-level retinal image-quality dataset and shows downstream DR-detection performance degrades with image quality. Supports §1.2.2 (image quality → performance) and §5.3 (multi-camera EyePACS acquisition). EyePACS-derived single-source; no external validation.
53. **Off-topic / domain-mismatch cards (#79–#82).** Sources #79 (encrypted cloud search), #80 (Hermite-function mathematics), #81 (muon-capture nuclear physics), and #82 (graphene quantum-Hall physics) are **outside the medical-imaging / DR domain** and carry negligible relevance to the dissertation. They are indexed for completeness and registered in the Peripheral Sources Registry below, following the convention established for #28/#29. They should **not** appear in the dissertation literature review.
54. **Alternate / supplementary cards for already-indexed sources (no new number assigned).** Two of the newly-supplied cards are second analytical cards for sources already in this index and therefore do **not** receive new source numbers (per the avoid-duplicates rule):
    - `gulshan-2016-supplementary-validation.md` → maps to **#12** (Gulshan et al., 2016). This card analyses the JAMA supplementary appendix (scale-normalisation to 299 px, FOV-mask exclusion) and reinforces #12's §1.2.2/§3.1 preprocessing detail; cite under #12.
    - `voets-2019-reproduction-study.md` → maps to **#17** (Voets et al., 2019). This card details the public-data reproduction (EyePACS AUC 0.951, Messidor-2 0.853) and reproducibility recommendations; cite under #17.
    Both files were copied into `external/` for archival completeness but are consolidated to their canonical entries (analogous to the #06/#10 and #23/#24 duplicate-card handling).

---

### Self-Publication Registry

| # | Short Label | Venue | Year | DOI | Overlap with Other Self-Pubs |
|---|-------------|-------|------|-----|------------------------------|
| 19 | CONF | Procedia Computer Science (DS 2025) | 2025 | 10.1016/j.procs.2025.10.237 | Overlaps #21 (same experiment) |
| 20 | KazUTB | Vestnik KazUTB | 2024 | 10.58805/kazutb.v.2.27-740 | Unique (laser-tissue modeling) |
| 21 | KBTU | Herald of KBTU | 2025 | 10.55452/1998-6688-2025-22-4-119-130 | Overlaps #19 (same experiment) |
| 22 | NAN_RK | News of NAS RK, Phys.-Math. Series | 2025 | 10.32014/2025.2518-1726.345 | Unique (system architecture) |
| 23 | SQOPUS_Q2 | Eastern-European J. Enterprise Tech. | 2025 | 10.15587/1729-4061.2025.335570 | **Duplicate of #24** (same article) |
| 24 | SQOPUS_Q3 | Eastern-European J. Enterprise Tech. | 2025 | 10.15587/1729-4061.2025.335570 | **Duplicate of #23** (same article) |

---

### Peripheral Sources Registry

| # | Source | Domain | Reason for Peripheral Classification |
|---|--------|--------|--------------------------------------|
| 25 | Wikipedia — AHE | Image processing (encyclopedic) | Not peer-reviewed; not citable in dissertation |
| 28 | Brancati et al. (2025) | FHIR / breast cancer ML | Domain mismatch; no DR or retinal imaging content |
| 29 | Tabari et al. (2024) | FHIR scoping review | Domain mismatch; no imaging or AI classification content |
| 30 | Chakka (2023) | OCT preprocessing | High school journal; no numerical metrics; low rigor |
| 31 | Kesharwani et al. (2021) | DR pathophysiology | Multiple citation errors; questionable journal; use #32 instead |
| 36 | Nandal (2024) | HL7/FHIR interoperability | Peripheral to DR imaging; relevant only to §6.2 infrastructure |
| 79 | Chin & Shih (2021) | Encrypted cloud document search | Domain mismatch; PCA index compression for searchable encryption; no imaging/DR content |
| 80 | Koch (2019) | Mathematics (special functions) | Off-topic; Hermite/parabolic-cylinder function inequalities; no ML or imaging content |
| 81 | Hungerford (1999) | Nuclear physics (muon capture) | Off-topic; charged-particle emission spectra; no ML or imaging content |
| 82 | Ostahie et al. (2015) | Condensed-matter physics (graphene) | Off-topic; quantum-Hall edge states; no ML or imaging content |

---

### Epistemic Tier Summary (New Sources #33–#45)

| # | Source | Epistemic Tier | Dissertation Role |
|---|--------|----------------|-------------------|
| 33 | Gettinger et al. (2025) | Methodological precedent | Background: DR pathophysiology + experimental models |
| 34 | Morya et al. (2024) | Peripheral / Background | Background: clinical context + screening compliance |
| 35 | Wang & Lo (2018) | Foundational (clinical) | Background: pathophysiology + treatment paradigm |
| 36 | Nandal (2024) | Limited-scope prototype | Infrastructure: FHIR/EHR integration reference |
| 37 | Geetha & Hema (2026) | Transformer-era (limited) | Comparator: ViT architectural reference only |
| 38 | Khosravi et al. (2025) | Clinical validation precedent | Evidence: cross-dataset external validation + ViT > CNN |
| 39 | Senapati et al. (2024) | Methodological precedent / Survey | Framing: field landscape + gap identification |
| 40 | Araf et al. (2024) | Foundational review | Methodology: CSL taxonomy + validation gap evidence |
| 41 | Sharma et al. (2025) | Limited-scope (⚠️ metric issues) | Comparator: ViT-CapsNet baseline with caveats |
| 42 | Arora et al. (2024) | Limited-scope | Comparator: EfficientNetB0 baseline |
| 43 | Ryu et al. (2021) | Clinical validation precedent | Evidence: OCTA-based CNN + external validation methodology |
| 44 | Zhang et al. (2022) | High-impact empirical evidence | Core evidence: multicentre CNN validation + expert comparison |
| 45 | Ruamviboonsuk et al. (2022) | High-impact clinical validation | Core evidence: prospective LMIC deployment gold standard |

### Epistemic Tier Summary (New Sources #46–#53)

| # | Source | Epistemic Tier | Dissertation Role |
|---|--------|----------------|-------------------|
| 46 🆕 | Selvaraju et al. (2017) | Foundational (explainability) | Core methodology: Grad-CAM formalization for §2.5 and Exp 4 |
| 47 🆕 | EyePACS descriptor | Dataset descriptor | Infrastructure: primary training dataset characterization |
| 48 🆕 | Messidor / Messidor-2 descriptor | Dataset descriptor | Infrastructure: external generalization dataset characterization |
| 49 🆕 | Pachade et al. (2021) — RFMiD | Dataset descriptor | Infrastructure: device domain shift dataset (Topcon/Kowa) |
| 50 🆕 | Li et al. (2019) — DDR | Dataset descriptor | Infrastructure: device domain shift dataset (Canon/Topcon) |
| 51 🆕 | ODIR-5K descriptor (TO BE IDENTIFIED) | Dataset descriptor | Infrastructure: device domain shift dataset (Canon/Zeiss) |
| 52 🆕 | Guo et al. (2017) | Foundational (calibration) | Methodology: ECE/Brier Score metric definitions for §3.4, §5.4 |
| 53 🆕 | Wang et al. (2004) | Foundational (image quality) | Methodology: SSIM metric definition for §2.6, §3.1 |

### Epistemic Tier Summary (New Sources #54–#82)

| # | Source | Epistemic Tier | Dissertation Role |
|---|--------|----------------|-------------------|
| 54 🆕 | Pizer et al. (1987) | Foundational (preprocessing) | Methodology: CLAHE precursor; citable replacement for #25 in §2.1.1–§2.1.2 |
| 55 🆕 | Tomasi & Manduchi (1998) | Foundational (preprocessing) | Methodology: bilateral filtering for §2.1.3 |
| 56 🆕 | Buades et al. (2011) | Foundational (preprocessing) | Methodology: non-local means denoising for §2.1.3 |
| 57 🆕 | Zhou et al. (2016) | Foundational (explainability) | Methodology: CAM origin for §2.5.1–§2.5.2 |
| 58 🆕 | Chattopadhyay et al. (2018) | Foundational (explainability) | Methodology: Grad-CAM++ for §2.5.1–§2.5.2, Exp 4 |
| 59 🆕 | Tjoa & Guan (2020) | Survey (medical XAI) | Framing: XAI landscape for §1.3.3, §2.5 |
| 60 🆕 | Samek et al. (2017) | Foundational (XAI) | Methodology: LRP / perturbation evaluation for §1.3.3, §2.5 |
| 61 🆕 | Lundberg & Lee (2017) | Foundational (XAI) | Methodology: SHAP attribution background for §2.5 |
| 62 🆕 | Ribeiro et al. (2016) | Foundational (XAI) | Methodology: LIME attribution background for §2.5 |
| 63 🆕 | Rezatofighi et al. (2019) | Foundational (metric) | Methodology: Generalized IoU for explainability-overlap (§2.5.3) |
| 64 🆕 | Everingham et al. (2010) | High-impact benchmark | Methodology: AP / IoU>0.5 definition for §2.5.3, §3.4 |
| 65 🆕 | Krizhevsky et al. (2012) | Foundational (architecture) | Background: AlexNet CNN foundations for §1.3.1, §2.2.1 |
| 66 🆕 | He et al. (2016) | Foundational (architecture) | Backbone: ResNet-50 (operational backbone) for §1.3.1, §3.2 |
| 67 🆕 | Huang et al. (2017) | Foundational (architecture) | Background: DenseNet for §1.3.1 |
| 68 🆕 | Tan & Le (2019) | High-impact benchmark | Backbone: EfficientNet-B3 (operational backbone) for §1.3.1, §3.2 |
| 69 🆕 | Tan & Le (2021) | Architecture refinement | Comparator: EfficientNetV2 for §1.3.1, §3.2 |
| 70 🆕 | Dosovitskiy et al. (2021) | Transformer-era benchmark | Comparator: ViT for CNN-vs-ViT discussion (§1.3.1) |
| 71 🆕 | Yosinski et al. (2014) | Foundational (transfer learning) | Methodology: layer transferability for §2.3.1–§2.3.2 |
| 72 🆕 | Kornblith et al. (2019) | High-impact benchmark | Methodology: ImageNet↔transfer correlation for §2.3.1–§2.3.2 |
| 73 🆕 | Cheplygina et al. (2018) | Survey (medical ML) | Framing: SSL/MIL/TL under limited labels for §2.3.1–§2.3.2 |
| 74 🆕 | Zhou et al. (2022) | Foundational survey (DG) | Framing: domain-generalization grounding for §1.2.3, §5.3 |
| 75 🆕 | Wang & Deng (2018) | Foundational survey (DA) | Framing: domain-adaptation taxonomy for §1.2.3, §5.3 |
| 76 🆕 | Ganin et al. (2016) | Foundational (domain adaptation) | Methodology: DANN/gradient reversal for §5.3, §2.3.2 |
| 77 🆕 | Abràmoff et al. (2018) | High-impact clinical validation | Core evidence: autonomous DR pivotal trial for §1.4, §6.3 |
| 78 🆕 | Fu et al. (2020) | Dataset descriptor + RIQA | Evidence: image-quality↔DR performance (EyeQ) for §1.2.2, §5.3 |
| 79 🆕 | Chin & Shih (2021) | Peripheral (off-domain) | Excluded: encrypted-search; no DR relevance |
| 80 🆕 | Koch (2019) | Peripheral (off-domain) | Excluded: special-functions mathematics; no DR relevance |
| 81 🆕 | Hungerford (1999) | Peripheral (off-domain) | Excluded: nuclear physics; no DR relevance |
| 82 🆕 | Ostahie et al. (2015) | Peripheral (off-domain) | Excluded: condensed-matter physics; no DR relevance |
