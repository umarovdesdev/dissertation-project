# LITERATURE INDEX
## External Source Corpus — Navigation Table

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Generated from:** Literature Cards in /literature/
**Total sources indexed:** 120 active (numbered 01–121; #13 retired as duplicate of #11)
**Version:** 6.1.0 — extends v6.0.0 with the #83–#121 expansion (39 new sources): the FGADR benchmark plus ophthalmology-specific SSL/foundation models, fundus image-degradation & quality, foundational loss/optimisation/regularisation/augmentation methods, architecture-lineage references, transfer-learning & medical-DL surveys, and externally-validated DR/ophthalmology clinical studies. Resolves the §1.2.1 gap and the §2.3.3 / §3.3.2 SSL gaps; fills the missing card files for #46 (Grad-CAM), #47 (EyePACS) and #48 (Messidor).

> **v6.0.0 amendment (navigation sync).** The Section Map Key, Source Index "Maps to" column, and
> Coverage Matrix are re-aligned to the current chapter structure: all seven experiments now live in
> **Chapter 4** (§4.2–§4.8) and Chapter 5 is "Reliability Validation and Comparative Analysis"
> (§5.1 Explainability Results, §5.2 Statistical Validation, §5.3 Comparative Analysis, §5.4 Limitations).
> Section-code remap applied throughout this index: **old §5.1→§4.4, §5.2→§5.1, §5.3→§4.7, §5.4→§5.2,
> §5.5→§5.3, §5.6→§5.4**; the dropped "Robustness to Image Degradation" experiment (old §4.4) is removed.
> Two sections were added per v6.0.0 (ophthalmology-specific self-supervised pretraining): **§2.3.3**
> (theory) and **§3.3.2** (methodology). H-1 is now "Integrated Pipeline Dominance" (composite
> *preprocessing × pretraining* IV); CLAHE is named "dual-constraint clip limit".

---

### Section Map Key

| Code | Dissertation Section |
|------|---------------------|
| §1.1.1 | Pathophysiology and Clinical Grading Systems |
| §1.1.2 | Screening Requirements in Resource-Limited Healthcare Settings |
| §1.2.1 | Sources of Image Degradation in Clinical Practice |
| §1.2.2 | Impact of Image Quality on Diagnostic Model Performance |
| §1.2.3 | Device-Specific Variability in Fundus Imaging |
| §1.3.1 | CNN Architectures for Medical Imaging |
| §1.3.2 | Transfer Learning and Self-Supervised Pretraining in Ophthalmic Diagnostics |
| §1.3.3 | Explainability Methods in Medical Image Classification |
| §1.4   | Critical Analysis of Existing Automated DR Screening Systems |
| §1.5   | Formulation of the Research Problem |
| §2.1.1 | Histogram Equalization and Adaptive Contrast Enhancement |
| §2.1.2 | Formalization of CLAHE with Dual-Constraint Clip Limit |
| §2.1.3 | Spatial Filtering and Noise Reduction Methods |
| §2.2.1 | Convolution, Pooling, and Feature Extraction Operations |
| §2.2.2 | Loss Functions and Optimization for Imbalanced Medical Datasets |
| §2.2.3 | Regularization Techniques: Dropout, Batch Normalization, Data Augmentation |
| §2.3.1 | Feature Transferability Across Visual Domains |
| §2.3.2 | Frozen-Layer versus Progressive Fine-Tuning Strategies |
| §2.3.3 | In-Domain Self-Supervised Pretraining for Retinal Imaging (NEW v6.0.0) |
| §2.4.1 | Coupled Thermal-Optical Model of Fundus Tissue Response |
| §2.5   | Explainability in Deep Learning for Medical Imaging |
| §2.5.1 | CAM / Grad-CAM Theory and Formalization |
| §2.5.2 | Attention Map Interpretation |
| §2.5.3 | ALO and IoU as Quantitative Explainability Metrics |
| §2.6   | Image Quality Metrics for Preprocessing Evaluation: CNR, VVI, Entropy, SSIM |
| §3.1   | Formalization of the Unified Preprocessing Pipeline (8-stage) |
| §3.1.4 | External Image Ingestion Protocol (methodological contribution) |
| §3.2   | Design of ResNet-50 / EfficientNet-B3 Architectures |
| §3.3   | Transfer Learning and Pretraining Methodology |
| §3.3.2 | Ophthalmology-Specific Self-Supervised Pretraining of the CNN Backbone (NEW v6.0.0) |
| §3.4   | Evaluation Framework and Performance Metrics (clinical, calibration, image quality) |
| §4.1   | Datasets and Experimental Configuration (EyePACS, APTOS 2019, IDRiD, Messidor-2, RFMiD, DDR, ODIR-5K, Clinical) |
| §4.2   | Experiment 1: Integrated Pipeline Dominance (H-1) |
| §4.3   | Experiment 2: Stage Ablation + CLAHE/σ Sweeps (H-2) |
| §4.4   | Experiment 3: Cross-Dataset Transferability on APTOS 2019 (H-4) |
| §4.5   | Experiment 4: Grad-CAM Explainability on IDRiD + Clinical (H-5) |
| §4.6   | Experiment 5: Clinical Degradation Resistance on IDRiD + Messidor-2 (H-7) |
| §4.7   | Experiment 6: Device Domain Shift on DDR + ODIR-5K + RFMiD (H-6) |
| §4.8   | Experiment 7: Small Data Training (IDRiD → Clinical) |
| §5.1   | Explainability Results |
| §5.2   | Statistical Validation |
| §5.3   | Comparative Analysis with Published Systems |
| §5.4   | Limitations and Boundary Conditions |
| §6.1   | System Requirements and Design Principles |
| §6.2   | AI Processing Module / PACS and EHR Integration |
| §6.3   | Clinical Workflow Integration |
| §6.4   | Data Security and Regulatory Compliance |
| INTRO  | Introduction (contextual framing) |

---

### Source Index

The **Paradigm** column was added in governance v5.3 to support the paradigmatic framing (P1 / P2 / N/A) per INVARIANTS SIR-9. See the *Notes* section below for the full classification rule.

| # | Source | Type | Key Result | Dataset | Paradigm | Maps to |
|---|--------|------|------------|---------|----------|---------|
| 01 | Pratt et al. (2016) | CNN classification | 75% acc, 30% sens, 95% spec, 5-class DR, Kaggle | EyePACS/Kaggle | P1 | §1.3.1, §2.2.2, §2.2.3, INTRO |
| 02 | Saxena et al. (2020) | Cross-dataset validation | AUC 0.958 Messidor-1, 0.92 Messidor-2, binary DR, InceptionResNetV2 | EyePACS/Kaggle, Messidor-1, Messidor-2 | P1 | §1.3.2, §1.4, §3.1, §4.4, §4.7, §5.3 |
| 03 | Sánchez-Gutiérrez et al. (2022) | Clinical validation | AUC 0.988, 90.5% sens, 97.1% spec, 96% workload reduction, RetCAD | Private (Ramon y Cajal) | P1 | §1.4, §6.3 |
| 04 | Arrieta et al. (2022) | CNN classification | AUC 0.94 EyePACS, 0.89 Messidor-2, semi-supervised with 2% labels | EyePACS/Kaggle, Messidor-2 | P1 | §1.3.1, §2.3.1, §4.4 |
| 05 | Rakhlin (2017) | Cross-dataset validation | AUC 0.967 Messidor-2, 0.923 Kaggle, modified VGGNet | EyePACS/Kaggle, Messidor-2 | P1 | §1.2.2, §1.3.1, §4.4, §5.3 |
| 06 | Porwal et al. (2018) | Dataset descriptor | IDRiD: 516 images, 81 pixel-annotated, Indian population, 5-class DR | IDRiD | N/A | §1.1.2, §4.1, §4.5, §5.1, INTRO |
| 07 | Baget-Bernaldiz et al. (2021) | External validation | AUC 0.988 RDR own pop., 0.968 Messidor, 4-class ICDR | Private (Spanish), Messidor-1, EyePACS/Kaggle | P1 | §1.4, §4.4, §5.3 |
| 08 | Wan et al. (2021) | Segmentation | SE 92.77% exudates (e_ophtha_EX), AUPR 0.78 hard exudates (IDRiD) | IDRiD, e_ophtha_EX, Private | P1 | §1.3.1, §2.2.1 |
| 09 | Xu et al. (2024) | Ensemble / Hybrid | Acc 0.97, AUC 0.97, EfficientNet+Swin Transformer V2 hybrid, 5-class | APTOS 2019 | P1 | §1.3.1, §1.3.2, §3.2 |
| 10 | Porwal et al. (2018) | Dataset descriptor | IDRiD: 516 images, pixel-level lesion masks + DR/DME grading, Indian pop. | IDRiD | N/A | §1.1.2, §4.1, §4.5, §5.1, INTRO |
| 11 | Ting et al. (2017) | External validation | AUC 0.936 referable DR, validated on 10 multiethnic datasets (AUC 0.889–0.983) | SIDRP (private), 10 external cohorts | P1 | §1.4, §4.4, §5.3, §6.3 |
| 12 | Gulshan et al. (2016) | CNN classification | AUC 0.991 EyePACS-1, 0.990 Messidor-2, Inception-v3 ensemble | EyePACS (private), Messidor-2 | P1 (canonical representative) | §1.3.1, §1.3.2, §1.4, §4.4, §5.3, INTRO |
| 14 | Wewetzer et al. (2021) | Meta-analysis | Pooled sens 87%, spec 90%, SROC AUC 0.9543, 10 DL screening studies in PC | Multiple (pooled) | N/A | §1.4, §5.3, §6.3, INTRO |
| 15 | Liu et al. (2022) | Benchmark study | κw 0.9303 DR grading, 0.70 image quality accuracy, EfficientNet dominant | DeepDRiD | P1 | §1.2.2, §1.3.1, §3.1, §4.1 |
| 16 | Goh et al. (2024) | CNN classification | SWIN AUC 95.7% Kaggle, 97.3% SEED, 96.3% Messidor-1, ViT > CNN | EyePACS/Kaggle, SEED, Messidor-1 | P1 | §1.3.1, §4.4, §5.2, §5.3 |
| 17 | Voets et al. (2019) | Cross-dataset validation | AUC 0.951 EyePACS, 0.853 Messidor-2 (reproduction of Gulshan 2016) | EyePACS/Kaggle, Messidor-2 | P1 | §1.2.2, §1.5, §4.4, §5.2 |
| 18 | González-Díaz et al. (2024) | ViT comparison | ViT acc 83.69%, BEiT F1 86.36%, 4-class AMD, 305 images | Private (curated AMD) | P1 | §1.3.1 |
| **19** | **Sapakova et al. (2025)** 🔹SELF | **Transfer learning** | **F1 0.74 fine-tuned vs 0.62 frozen, EfficientNetB0, 5-class DR** | **APTOS 2019, Private clinical** | **P1 (prior self-work)** | **§2.3.2, §3.3, §4.2, §4.1, §2.2.2, §2.2.3, §3.1** |
| **20** | **Sapakova et al. (2024)** 🔹SELF | **Mathematical modeling** | **Thermal model of laser-fundus interaction, FDM simulation, qualitative** | **None (simulation)** | **N/A** | **§2.4.1** |
| **21** | **Yesmukhamedov et al. (2025a)** 🔹SELF | **Transfer learning** | **Precision 75% fine-tuned vs 65% frozen, EfficientNetB0, 5-class DR** | **APTOS 2019, Private clinical** | **P1 (prior self-work)** | **§2.3.2, §3.3, §4.2, §3.1, §3.4, §2.2.2, §2.2.3** |
| **22** | **Yesmukhamedov et al. (2025b)** 🔹SELF | **System architecture** | **Modular AI diagnostic architecture for Kazakhstan, physician-in-the-loop** | **None (design study)** | **N/A** | **§6.1, §6.2, §6.3, §1.4, §1.1.2** |
| **23** | **Sapakova, Yesmukhamedov & Sapakov (2025a)** 🔹SELF | **CLAHE / Enhancement** | **100% acc/sens/spec, upgraded CLAHE T/80 + ResNet50, 5-class retinal** | **STARE** | **P2-tending (prior self-work toward the integrated pipeline)** | **§2.1.2, §3.1, §3.3, §4.3, §5.3, §2.1.1** |
| **24** | **Sapakova, Yesmukhamedov & Sapakov (2025b)** 🔹SELF | **Preprocessing study** | **Val acc 71%→86% with preprocessing, ROC-AUC 0.9638, 4-layer CNN** | **APTOS 2019, Private clinical** | **P2-tending (prior self-work toward the integrated pipeline)** | **§3.1, §3.2, §4.2, §4.1, §2.1.2, §5.2, §1.2.2** |
| 25 | Wikipedia — Adaptive Histogram Equalization | Background reference | Algorithmic description of AHE/CLAHE; clip limit 3–4, 8×8 tile grid | N/A | §2.1.1, §2.1.2 |
| 26 | Shaout & Han (2025) | Preprocessing study | FCE+CLAHE 59% preference, 88% combined; fuzzy logic + CLAHE blending | DRIVE | N/A (preprocessing method, no CNN comparison) | §2.1.1, §3.1 |
| 27 | Hayati et al. (2023) | CLAHE / Enhancement | CLAHE improved 3/4 CNNs; EfficientNetB4 97.83% acc; ResNet34 −12.02% | APTOS 2019 | P1 (preprocessing varied but treated as exogenous factor) | §2.1.1, §2.1.2, §3.1, §4.3, §5.2 |
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
| 38 | Khosravi et al. (2025) | External validation (retinal hemorrhage) | FastViT AUC 0.9811, ResNet18 AUC 0.9626; 2661-image external dataset | RFMiD, DeepEyeNet, BRSET, Private (multi-country) | P1 | §1.3.1, §4.4, §4.7 |
| 39 | Senapati et al. (2024) | Systematic review (DR AI) | PRISMA-based; 2016–2023; EyePACS 75,523 images; identifies overfitting + class imbalance gaps | Multiple (surveyed) | N/A (survey) | §1.4, §1.5, §2.2.2 |
| 40 | Araf et al. (2024) | Systematic review (cost-sensitive learning) | 173 papers reviewed; CSL preserves distribution; only 2 validation studies identified | Multiple (surveyed) | N/A (survey) | §2.2.2, §3.4 |
| 41 | Sharma et al. (2025) | ViT-CapsNet hybrid (DR) | 94% acc on EyePACS (30,262 images); AUC 0.44–0.56 per class; no external validation | EyePACS/Kaggle | P1 | §1.3.1, §4.1 |
| 42 | Arora et al. (2024) | CNN classification (DR) | EfficientNetB0 avg acc 0.8653; max training acc 97.11%; undersampled to 3,704 images | Kaggle DR Resized (35,108 images) | P1 | §1.3.1, §2.2.2 |
| 43 | Ryu et al. (2021) | CNN classification + external validation (OCTA) | AUC 0.960–0.976 internal; AUC 0.938–0.962 external; ResNet101 on OCTA | Private (single-center) | P1 | §1.3.1, §1.4 |
| 44 | Zhang et al. (2022) | Multicentre external validation (DR screening) | AUROC 0.9931 referable DR (image); 0.9848 (patient); Cohen's κ 0.86–0.93 vs experts | Private (83,465 images, 4 centres) | P1 | §1.4, §4.4, §5.3, §6.3 |
| 45 | Ruamviboonsuk et al. (2022) | Prospective clinical validation (DR screening) | Acc 94.7%, sens 91.4% VTDR; outperformed specialists (p=0.024); 9 Thai sites | Private (7,651 patients, prospective) | P1 | §1.4, §5.3, §6.3 |
| 46 ✅ | Selvaraju et al. (2017) "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization" (ICCV 2017) — **card written** `selvaraju-2017-grad-cam.md` | Explainability method | Grad-CAM gradient-weighted class activation mapping; ILSVRC-15 weakly-supervised localization; AMT class-discrimination 61.23% vs 44.44% | ImageNet / VOC | N/A (methodology reference) | §1.3.3, §2.5.1, §2.5.2, §4.5, §5.1 |
| 47 ✅ | Cuadros & Bresnick (2009) "EyePACS: An Adaptable Telemedicine System for Diabetic Retinopathy Screening" (J Diabetes Sci Technol 3(3):509–516) — **card written** `cuadros-2009-eyepacs.md` | Dataset/system descriptor | EyePACS telemedicine system; Canon CR-DGi/CR-1 nonmydriatic cameras, ETDRS-based 5-level grading; >34,100 DRS encounters. (The ~35,126-image labeled partition is a Kaggle-competition attribute.) | EyePACS/Kaggle | N/A | §4.1, §1.2.3, §6.3, INTRO |
| 48 ✅ | Decencière et al. (2014) "Feedback on a Publicly Distributed Image Database: The Messidor Database" (Image Anal Stereol 33(3):231–234) — **card written** `decenciere-2014-messidor.md` | Dataset descriptor | Messidor: 1,200 fundus images, Topcon TRC NW6, 45° FOV (distinct from Messidor-2 = 1,748) | Messidor / Messidor-2 | N/A | §4.1, §4.4, §4.6, INTRO |
| 49 ✅ | Pachade et al. (2021) "Retinal Fundus Multi-Disease Image Dataset (RFMiD)" (Data 6(2):14, DOI 10.3390/data6020014) — **card written** `pachade-2021-rfmid.md` | Dataset descriptor | 3,200 images, 46 conditions, 1920/640/640 split; three cameras: TOPCON 3D OCT-2000, Kowa VX-10α, TOPCON TRC-NW300 | RFMiD | N/A | §4.1, §1.2.3, §4.7 |
| 50 ✅ | Li et al. (2019) "Diagnostic Assessment of Deep Learning Algorithms for Diabetic Retinopathy Screening" (Information Sciences 501:511–522, DOI 10.1016/j.ins.2019.06.011) — DDR/OIA-DDR — **card written** `li-2019-ddr.md` | Dataset descriptor + benchmark | 13,673 images, 9,598 patients, 147 hospitals/23 provinces, 42 camera types; six classes (ICDR 0–4 + ungradable) | DDR | N/A | §4.1, §1.2.3, §4.7 |
| 51 ✅ | ODIR-2019 (Peking University Int'l Competition on Ocular Disease Intelligent Recognition) — **online resource**, no peer-reviewed descriptor (TO-BE-IDENTIFIED resolved) — **card written** `odir-2019-dataset.md` | Dataset descriptor (electronic resource) | 5,000 patients, both eyes, 8 labels; Canon/Zeiss/Kowa cameras; collected by Shanggong Medical Technology | ODIR-5K | N/A | §4.1, §1.2.3, §4.7 |
| 52 ✅ | Guo et al. (2017) "On Calibration of Modern Neural Networks" (ICML, PMLR 70:1321–1330) — **card written** `guo-2017-calibration.md` | Calibration methodology | ECE / reliability diagrams / temperature scaling; depth-width-weight-decay-BatchNorm drive miscalibration | ImageNet / CIFAR | N/A (methodology reference) | §2.6, §3.4, §5.2 |
| 53 ✅ | Wang et al. (2004) "Image Quality Assessment: From Error Visibility to Structural Similarity" (IEEE TIP 13(4):600–612) — **card written** `wang-2004-ssim.md` | Image quality metric | SSIM (luminance×contrast×structure), mean SSIM; structure-loss > pointwise error vs MSE/PSNR | Various (image quality benchmarks) | N/A (methodology reference) | §2.6, §3.1 |
| 54 🆕 | Pizer et al. (1987) "Adaptive Histogram Equalization and Its Variations" | Image enhancement method | Introduces **clipped AHE (CLAHE precursor)**; histogram clipping limits noise over-enhancement; qualitative medical-image eval | Medical images (CT/MRI/angiography, qualitative) | N/A (methodology reference) | §2.1.1, §2.1.2 |
| 55 🆕 | Tomasi & Manduchi (1998) "Bilateral Filtering for Gray and Color Images" | Image filtering method | Bilateral filter: edge-preserving smoothing via joint geometric + photometric weighting; qualitative | None (illustrative images) | N/A (methodology reference) | §2.1.3 |
| 56 🆕 | Buades et al. (2011) "Non-Local Means Denoising" | Image denoising method | Non-Local Means: averages non-local similar patches; patchwise PSNR gain; qualitative | None (illustrative images) | N/A (methodology reference) | §2.1.3 |
| 57 🆕 | Zhou et al. (2016) "Learning Deep Features for Discriminative Localization" (CAM) | Explainability method | **Class Activation Mapping (CAM)** via global average pooling; weakly-supervised localization (37.1% top-5 loc error, ILSVRC) | ILSVRC / various | N/A (methodology reference) | §1.3.3, §2.5.1, §2.5.2 |
| 58 🆕 | Chattopadhyay et al. (2018) "Grad-CAM++" | Explainability method | Grad-CAM++ improves localization & multi-instance handling over Grad-CAM (avg-drop 36.8% vs 46.6%, ImageNet) | ImageNet, VOC, CIFAR-10 | N/A (methodology reference) | §1.3.3, §2.5.1, §2.5.2, §4.5 |
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
| 73 🆕 | Cheplygina et al. (2018) "Not-so-supervised: A Survey of SSL, MIL and Transfer Learning in Medical Image Analysis" | Review / Survey (medical ML) | Survey of semi-supervised, multi-instance, and transfer learning under limited labels in medical imaging | None (survey) | N/A (survey) | §1.3.2, §2.3.1, §2.3.2, §2.3.3, §3.3.2 |
| 74 🆕 | Zhou et al. (2022) "Domain Generalization: A Survey" | Review / Survey (DG) | Taxonomy of domain-generalization methods; OOD performance degradation under domain shift | None (survey) | N/A (survey) | §1.2.3, §4.7 |
| 75 🆕 | Wang & Deng (2018) "Deep Visual Domain Adaptation: A Survey" | Review / Survey (DA) | Deep domain-adaptation taxonomy (discrepancy / adversarial / reconstruction based) | None (survey) | N/A (survey) | §1.2.3, §4.7 |
| 76 🆕 | Ganin et al. (2016) "Domain-Adversarial Training of Neural Networks" (DANN) | Domain adaptation method | **DANN** + gradient reversal layer; domain-invariant features; e.g. MNIST→MNIST-M 0.767 | MNIST/SVHN/GTSRB/Office, etc. | N/A (methodology reference) | §4.7, §2.3.2 |
| 77 🆕 | Abràmoff et al. (2018) "Pivotal Trial of an Autonomous AI System for DR Detection in Primary Care" (IDx-DR) | Prospective clinical validation | Autonomous IDx-DR; sens 87.2%, spec 90.7%, imageability 96.1%; 900 patients, 10 primary-care sites; FDA pivotal | Private (prospective, 900 pts) | P1 | §1.4, §6.3, INTRO |
| 78 🆕 | Fu et al. (2020) "Evaluation of Retinal Image Quality Assessment Networks in Different Color-spaces" (EyeQ) | Dataset descriptor + RIQA | **EyeQ** (28,792 EyePACS images, 3-level quality grading); MCF-Net 0.9175 acc; image quality affects DR detection | EyeQ (re-annotated from EyePACS) | P1 | §1.2.2, §4.7, §3.1 |
| 79 🆕 | Chin & Shih (2021) "Concisely Indexed Multi-keyword Rank Search on Encrypted Cloud Documents" | Peripheral (encrypted search) | PCA-condensed index for encrypted multi-keyword cloud search; <1/10 storage vs MRSE | BBC text corpus | N/A | Peripheral |
| 80 🆕 | Koch (2019) "Universal Bounds and Monotonicity Properties of Ratios of Hermite and Parabolic Cylinder Functions" | Peripheral (mathematics) | Monotonicity & optimal bounds of Hermite/parabolic-cylinder function ratios; Turán-type inequalities | None (theoretical) | N/A | Peripheral |
| 81 🆕 | Hungerford (1999) "Comments on Proton Emission after Muon Capture" | Peripheral (nuclear physics) | Charged-particle emission after atomic muon capture (~15% in light nuclei); MECO background estimate | None (physics) | N/A | Peripheral |
| 82 🆕 | Ostahie et al. (2015) "Electrical Manipulation of the Edge States in Graphene…" | Peripheral (condensed-matter physics) | Electrically-induced "shortcut edge states" in graphene; unconventional quantum-Hall plateaus | None (simulation) | N/A | Peripheral |
| 83 🆕 | Zhou et al. (2020) "A Benchmark for Studying Diabetic Retinopathy: Segmentation, Grading, and Transferability" (FGADR) | Dataset descriptor + benchmark | FGADR: 2,842 images (1,842 pixel-level lesion + 1,000 grade); joint grading; FGADR→ODIR-5K transfer | FGADR, ODIR-5K | P1 | §1.3.1, §1.3.2, §4.5, §4.1 |
| 84 🆕 | Zhou et al. (2023) "A foundation model for generalizable disease detection from retinal images" (RETFound) | Ophthalmology SSL foundation model | MAE/ViT pretrained on 1.6M retinal images; outperforms SimCLR/SwAV/DINO/MoCo-v3; label-efficient multi-disease | Multi-cohort retinal | P1 | §2.3.3, §3.3.2, §4.4, §1.3.2 |
| 85 🆕 | Azizi et al. (2021) "Big Self-Supervised Models Advance Medical Image Classification" (MICLe) | Medical SSL | In-domain SSL + multi-instance contrastive; +6.7% derm top-1, +1.1% CXR mAUC | Dermatology, Chest X-ray | N/A (method) | §2.3.3, §3.3.2 |
| 86 🆕 | Chen et al. (2020) "A Simple Framework for Contrastive Learning…" (SimCLR) | SSL method | Contrastive (NT-Xent); ImageNet linear 76.5% top-1 | ImageNet | N/A (method) | §2.3.3, §3.3.2 |
| 87 🆕 | He et al. (2020) "Momentum Contrast…" (MoCo) | SSL method | Momentum encoder + queue; SSL ≥ supervised on transfer tasks | ImageNet, COCO/VOC | N/A (method) | §2.3.3, §3.3.2 |
| 88 🆕 | Grill et al. (2020) "Bootstrap Your Own Latent" (BYOL) | SSL method | Negative-free SSL; ImageNet linear 74.3% top-1 | ImageNet | N/A (method) | §2.3.3, §3.3.2 |
| 89 🆕 | Caron et al. (2021) "Emerging Properties in Self-Supervised Vision Transformers" (DINO) | SSL method (ViT) | Self-distillation; emergent attention segmentation; ViT-B/8 linear 80.1% | ImageNet | N/A (method) | §2.3.3, §3.3.2, §2.5 |
| 90 🆕 | He et al. (2022) "Masked Autoencoders Are Scalable Vision Learners" (MAE) | SSL method | 75% masking; ViT-H ImageNet-1K fine-tune 87.8%; **basis of RETFound pretraining** | ImageNet | N/A (method) | §3.3.2, §2.3.3 |
| 91 🆕 | Chen & He (2021) "Exploring Simple Siamese Representation Learning" (SimSiam) | SSL method | Negative-free; stop-gradient prevents collapse | ImageNet | N/A (method) | §2.3.3, §3.3.2 |
| 92 🆕 | Shurrab & Duwairi (2022) "Self-supervised learning … in medical imaging: a survey" | Review / Survey (medical SSL) | Taxonomy: predictive/contrastive/generative SSL in medical imaging | None (survey) | N/A (survey) | §2.3.3, §3.3.2 |
| 93 🆕 | Shen et al. (2020) "Modeling and Enhancing Low-Quality Retinal Fundus Images" (cofe-Net) | Preprocessing / enhancement | Degradation model (illumination/blur/artifacts) + cofe-Net (LQA+RSA); improves downstream segmentation/detection | Fundus (synthetic + real) | P1 | §1.2.1, §3.1, §2.6, §4.7 |
| 94 🆕 | Zago et al. (2018) "Retinal image quality assessment using deep learning" | RIQA / image quality | Inception-v3 transfer; DRIMDB AUC 99.98%, ELSA-Brasil 98.56% (inter-DB) | DRIMDB, ELSA-Brasil | P1 | §2.6, §1.2.2, §4.7 |
| 95 🆕 | Zuiderveld (1994) "Contrast Limited Adaptive Histogram Equalization" (Graphics Gems IV) | Image enhancement method | Canonical CLAHE algorithm (clip limit + tile interpolation); citable replacement for #25 | Medical images (illustrative) | N/A (method) | §2.1.1, §2.1.2 |
| 96 🆕 | Lin et al. (2017) "Focal Loss for Dense Object Detection" (RetinaNet) | Loss function | **Focal Loss (γ=2)** — the dissertation's training loss; COCO AP 39.1 | COCO | N/A (method) | §2.2.2, §3.4 |
| 97 🆕 | Cui et al. (2019) "Class-Balanced Loss Based on Effective Number of Samples" | Loss function | Effective-number re-weighting (1−β^n)/(1−β); long-tailed gains | Long-tailed CIFAR/iNat/ImageNet-LT | N/A (method) | §2.2.2 |
| 98 🆕 | Buda et al. (2018) "A systematic study of the class imbalance problem in CNNs" | Imbalance study | Oversampling best; no CNN overfitting penalty; thresholding helps | MNIST/CIFAR/ImageNet | N/A (method) | §2.2.2, §2.2.3, §3.4 |
| 99 🆕 | Kingma & Ba (2015) "Adam: A Method for Stochastic Optimization" | Optimizer | Adaptive moment estimation; defaults β1=0.9, β2=0.999 | MNIST/CIFAR/IMDB | N/A (method) | §2.2.2, §3.2 |
| 100 🆕 | Ioffe & Szegedy (2015) "Batch Normalization…" | Normalization | Per-batch normalization; ~14× fewer steps; intrinsic to ResNet-50 | ImageNet | N/A (method) | §2.2.3, §3.2 |
| 101 🆕 | Srivastava et al. (2014) "Dropout…" | Regularization | Random unit dropping ≈ ensemble averaging; reduces overfitting | MNIST/CIFAR/ImageNet/TIMIT | N/A (method) | §2.2.3 |
| 102 🆕 | Zhang et al. (2018) "mixup: Beyond Empirical Risk Minimization" | Augmentation | Convex input/label mixing; robustness + calibration gains | ImageNet/CIFAR | N/A (method) | §2.2.3 |
| 103 🆕 | Shorten & Khoshgoftaar (2019) "A survey on Image Data Augmentation for Deep Learning" | Review / Survey | Augmentation taxonomy (geometric/color/mixing/erasing/GAN) | None (survey) | N/A (survey) | §2.2.3 |
| 104 🆕 | Cubuk et al. (2020) "RandAugment…" | Augmentation policy | 2-parameter search-free augmentation; matches AutoAugment | ImageNet/CIFAR/COCO | N/A (method) | §2.2.3 |
| 105 🆕 | Simonyan & Zisserman (2015) "Very Deep Convolutional Networks" (VGG) | CNN architecture | Depth via 3×3 filters; ILSVRC-14 top-5 6.8%; basis of cited DR baselines | ImageNet | N/A (architecture) | §1.3.1 |
| 106 🆕 | Szegedy et al. (2015) "Going Deeper with Convolutions" (GoogLeNet/Inception-v1) | CNN architecture | Inception module + 1×1 bottlenecks; ILSVRC-14 top-5 6.67% | ImageNet | N/A (architecture) | §1.3.1 |
| 107 🆕 | Szegedy et al. (2016) "Rethinking the Inception Architecture" (Inception-v3) | CNN architecture | Factorized conv + label smoothing; **backbone of Gulshan 2016 (#12)** & Esteva 2017 (#121); top-5 3.5% | ImageNet | N/A (architecture) | §1.3.1, §3.2 |
| 108 🆕 | Liu et al. (2021) "Swin Transformer…" | ViT architecture | Hierarchical shifted-window attention; ImageNet 87.3%, COCO 58.7 AP, ADE20K 53.5 mIoU | ImageNet/COCO/ADE20K | N/A (architecture) | §1.3.1 |
| 109 🆕 | Pan & Yang (2010) "A Survey on Transfer Learning" | Review / Survey | Canonical transfer-learning taxonomy (domain/task; what-to-transfer; negative transfer) | None (survey) | N/A (survey) | §2.3.1, §2.3.2 |
| 110 🆕 | Litjens et al. (2017) "A survey on deep learning in medical image analysis" | Review / Survey | >300 works; CNN dominance; data-scarcity/imbalance/interpretability challenges | None (survey) | N/A (survey) | §1.3.1, §1.3.2 |
| 111 🆕 | Quellec et al. (2017) "Deep image mining for diabetic retinopathy screening" | CNN + explainability | Referable-DR Az 0.954 (Kaggle), 0.949 (e-ophtha); weakly-supervised lesion heatmaps (DiaretDB1) | Kaggle/EyePACS, e-ophtha, DiaretDB1 | P1 | §1.3.1, §1.3.3, §4.5, §4.4 |
| 112 🆕 | Gargeya & Leng (2017) "Automated Identification of DR Using Deep Learning" | CNN + external validation | AUC 0.97 (5-fold), 94% sens/98% spec; Messidor-2 0.94, e-ophtha 0.95 | Local (EyePACS), Messidor-2, e-ophtha | P1 | §1.3.1, §1.4, §4.4 |
| 113 🆕 | Krause et al. (2018) "Grader Variability and the Importance of Reference Standards…" | Evaluation methodology | Adjudication reference standard; mild+ DR sens 0.970, spec 0.917, AUC 0.986 | Private (DR screening) | P1 | §1.5, §3.4, §5.3 |
| 114 🆕 | Son et al. (2020) "…Screening Multiple Abnormal Findings in Retinal Fundus Images" | CNN + external validation | 12 findings; AUROC 96.2–99.9% in-house, 94.7–98.0% external | Private + external | P1 | §1.3.1, §4.7, §4.4 |
| 115 🆕 | Bellemo et al. (2019) "AI … to screen for … DR in Africa" | Clinical validation (cross-population) | Referable DR AUC 0.973 (CI 0.969–0.978), sens 92.25%, spec 89.04%; Zambia | Private (Zambia, 4,504 imgs) | P1 | §1.4, §4.4, §6.3 |
| 116 🆕 | Dai et al. (2021) "A deep learning system for detecting DR across the disease spectrum" (DeepDR) | Multi-task DR system | Quality+lesion+grading; 466,247 imgs; lesion AUC 0.901–0.967; 3 external sets | Private (China) + 3 external | P1 | §1.3.1, §1.2.2, §4.5, §4.4 |
| 117 🆕 | De Fauw et al. (2018) "Clinically applicable deep learning … in retinal disease" | Clinical validation (device-independent) | Segmentation→classification; device-independent referral; n=997 test (OCT) | Private (Moorfields OCT) | P1 | §1.4, §4.7, §6.3, INTRO |
| 118 🆕 | Ting et al. (2019) "Deep learning in ophthalmology: technical and clinical considerations" | Review / Survey | DL-in-ophthalmology technical + clinical-translation review | None (survey) | N/A (survey) | §1.3.1, §1.4, §6.3 |
| 119 🆕 | Beede et al. (2020) "A Human-Centered Evaluation of a DL System … for DR" | Socio-technical field study | 11 Thai clinics; socio-environmental factors + quality gating affect deployment | Field study (Thailand) | N/A | §6.1, §6.3, §1.2.2 |
| 120 🆕 | Burlina et al. (2017) "Automated Grading of AMD … Deep CNNs" | CNN classification (AMD) | AREDS color-fundus CNN grading via transfer learning (AMD, peripheral) | AREDS | P1 | §1.3.1 |
| 121 🆕 | Esteva et al. (2017) "Dermatologist-level classification of skin cancer…" | CNN classification (landmark) | Inception-v3 transfer; 129,450 images; dermatologist-level; **P1 end-to-end paradigm foil** | Clinical dermatology | P1 | §1.3.1, §2.3.1, INTRO |

---

### Coverage Matrix

| Dissertation Section | Sources Covering It |
|---------------------|---------------------|
| §1.1.1 | #31, #32, **#33, #34, #35** |
| §1.1.2 | #06, #10, **#22**, #34 |
| §1.2.1 | #93 ✅ RESOLVED (cofe-Net degradation model: illumination/blur/artifacts) |
| §1.2.2 | #05, #15, #17, **#24**, #78, #94, #116, #119 |
| §1.2.3 | #47, #49, #50, #51, #74, #75 |
| §1.3.1 | #01, #04, #05, #08, #09, #12, #15, #16, #18, #37, #38, #41, #42, #43, #65, #66, #67, #68, #69, #70, #83, #105, #106, #107, #108, #110, #111, #112, #114, #116, #120, #121 |
| §1.3.2 | #02, #09, #12, #73, #84, #110 |
| §1.3.3 | #46, #57, #58, #59, #60, #61, #62 |
| §1.4 | #02, #03, #07, #11, #12, #14, **#22**, #39, #43, #44, #45, #77, #112, #113, #115, #117, #118 |
| §1.5 | #17, #39, #113 |
| §2.1.1 | #25, #26, #27, #30, **#23**, #54, #95 |
| §2.1.2 | #25, #27, **#23, #24**, #54, #95 |
| §2.1.3 | #55, #56 |
| §2.2.1 | #08, #65, #66, #67 |
| §2.2.2 | #01, **#19, #21**, #39, #40, #42, #96, #97, #98, #99 |
| §2.2.3 | #01, **#19, #21**, #65, #98, #100, #101, #102, #103, #104 |
| §2.3.1 | #04, #71, #72, #73, #109, #121 |
| §2.3.2 | **#19, #21**, #71, #72, #76, #109 |
| §2.3.3 (NEW) | ✅ RESOLVED — #84 (RETFound, in-domain retinal SSL), #85 (MICLe), #86 (SimCLR), #87 (MoCo), #88 (BYOL), #89 (DINO), #90 (MAE), #91 (SimSiam), #92 (medical-SSL survey), #73 (general survey). **Well-covered.** |
| §2.4.1 | **#20** ⚡ THIN |
| §2.5.1 | #46, #57, #58 |
| §2.5.2 | #46, #57, #58 |
| §2.5.3 | #63, #64 |
| §2.6 | #52, #53, #93, #94 |
| §3.1 | #02, #15, #26, #27, #53, **#19, #21, #23, #24**, #78 |
| §3.1.4 | ⚠️ GAP — no external literature; methodological contribution by candidate |
| §3.2 | #09, **#24**, #66, #68, #69, #70, #99, #100, #107, #108 |
| §3.3 | **#19, #21, #23**, #71, #72, #109 |
| §3.3.2 (NEW) | ✅ RESOLVED — #84 (RETFound), #90 (MAE — pretraining basis), #85 (MICLe), #86–#89, #91 (SSL methods), #92 (survey). Ophthalmology-specific SSL now well-grounded. **[v6.2.0] #88 (BYOL, Grill et al. 2020) is the selected *primary* protocol** for the integrated-arm SSL initialization (MoCo #87 / SimSiam #91 / DINO #89 retained as alternatives); cited accordingly in §3.3.2. |
| §3.4 | **#21**, #40, #52, #64, #96, #98, #113 |
| §4.1 | #06, #10, #15, #47, #48, #49, #50, #51, **#19, #21, #24**, #41, #83 |
| §4.2 (Exp 1, H-1) | **#19, #21, #24** ⚡ THIN (self-only) |
| §4.3 (Exp 2, H-2) | #27, **#23** |
| §4.4 (Exp 3 — Cross-Dataset Transferability, H-4) | #02, #04, #05, #07, #11, #12, #16, #17, #38, #44, #48, #84, #111, #112, #115, #116 |
| §4.5 (Exp 4 — Explainability, H-5) | #06, #10, #46, #57, #58, #83, #111, #116 |
| §4.6 (Exp 5 — Clinical Degradation, H-7) | #06, #10, #17, #44, #48, #78 |
| §4.7 (Exp 6 — Device Domain Shift, H-6) | #38, #49, #50, #51, #74, #75, #76, #78, #93, #94, #114, #117 |
| §4.8 (Exp 7 — Small Data Training) | #06, #10 ⚡ THIN |
| §5.1 (Explainability Results) | #06, #10, #16, #17, #27, #46, **#24**, #57, #58 |
| §5.2 (Statistical Validation) | #16, #17, #27, #52, **#24** |
| §5.3 (Comparative Analysis) | #02, #05, #07, #11, #12, #14, #16, **#23**, #44, #45 |
| §5.4 (Limitations) | — (populated by candidate's own experimental limitations) |
| §6.1 | **#22**, #119 |
| §6.2 | **#22**, #36 |
| §6.3 | #03, #11, #14, **#22**, #34, #44, #45, #115, #117, #118, #119 |
| §6.4 | — (regulatory framing; candidate's design specification) |
| INTRO | #01, #06, #10, #12, #14, #33, #35, #47, #48, #117, #121 |

---

### Gaps Identified

**⚠️ GAP (0 external sources) — remaining after the v6.1.0 expansion:**
- §3.1.4 — External Image Ingestion Protocol (methodological contribution by candidate; no external literature expected — by design)

**✅ GAPS RESOLVED in the v6.1.0 expansion (#83–#121):**
- §1.2.1 — Sources of Image Degradation in Clinical Practice — RESOLVED by **#93** (Shen et al. cofe-Net: explicit degradation model of uneven illumination, blur, artifacts).
- §3.3.2 — Ophthalmology-Specific Self-Supervised Pretraining — RESOLVED by **#84 (RETFound)** + **#90 (MAE, the pretraining basis)** + **#85 (MICLe)** + the SSL method corpus **#86–#89, #91** + survey **#92**.
- §2.3.3 — In-Domain Self-Supervised Pretraining for Retinal Imaging — RESOLVED by the same #84–#92 corpus (was ⚡ THIN on #73 only).

**✅ GAPS RESOLVED previously (#54–#82):**
- §2.1.3 — Spatial Filtering and Noise Reduction Methods — RESOLVED by #55 (bilateral filtering) and #56 (non-local means).
- §2.5.3 — ALO and IoU as Quantitative Explainability Metrics — RESOLVED by #63 (Generalized IoU metric/loss) and #64 (PASCAL VOC IoU > 0.5 criterion).

**⚡ THIN (1 source or thin coverage) — after v6.1.0:**
- §2.4.1 — Coupled Thermal-Optical Model of Fundus Tissue Response (#20 🔹SELF only) — still THIN.
- §4.2 — Experiment 1: Integrated Pipeline Dominance (#19, #21, #24 🔹SELF only; the SSL corpus #84–#92 now supports the *pretraining* arm of the composite H-1 IV, but the integrated-pipeline self-comparison remains self-only).
- §4.8 — Experiment 7: Small Data Training (#06, #10 dataset descriptors; #84 RETFound label-efficiency is supportive context) — still THIN.

**⬆️ THIN STATUS UPGRADED in the v6.1.0 expansion:**
- §2.3.3 / §3.3.2 → **well-covered** by #84–#92 (see Gaps Resolved above).
- §2.6 — Image Quality Metrics → adds #93 (cofe-Net) and #94 (Zago RIQA, fundus-specific) to #52, #53.
- §6.1 — System Requirements → adds #119 (Beede et al. socio-technical deployment) to #22.
- §2.2.2 / §2.2.3 — Loss & Regularization → adds the canonical method primaries #96 (Focal Loss, the dissertation's loss), #97, #98, #99, #100, #101, #102, #103, #104.

**⬆️ THIN STATUS UPGRADED in the #54–#82 expansion (retained):**
- §1.3.3 — Explainability Methods → #46, #57, #58, #59, #60, #61, #62. **Well-covered.**
- §2.2.1 — Convolution, Pooling, and Feature Extraction → #08, #65, #66, #67 (AlexNet/ResNet/DenseNet foundations).
- §2.3.1 — Feature Transferability Across Visual Domains → #04, #71, #72, #73.
- §2.5.1 — CAM / Grad-CAM Theory → #46, #57 (CAM), #58 (Grad-CAM++).
- §2.5.2 — Attention Map Interpretation → #46, #57, #58.
- §4.7 — Experiment 6: Device Domain Shift (was dataset-descriptors only) → adds #74, #75, #76 (DG/DA literature) + #78 (image-quality).

---

### Notes

**Paradigm column (v5.3) — classification rule.**
Per INVARIANTS SIR-9, every CNN-based or ViT-based DR/retinal-image classification source has been tagged as **P1** (end-to-end CNN paradigm; preprocessing as auxiliary step), **P2-tending** (preprocessing explicitly formalised as model component), or **N/A** (methodology reference, dataset descriptor, clinical/pathophysiology review, mathematical model, system architecture, or survey). Tag rationale:
- **P1** — backbone-centric study in which preprocessing is either unreported, reported as a fixed exogenous step, or varied but treated as a tuning input rather than as a formalised model component. The dominant class in the literature corpus.
- **P1 (canonical representative)** — reserved for Gulshan et al. (2016) per SB-1.12 / SIR-9; see gulshan-2016.md §15 Paradigmatic Role for the methodological-practice grounds.
- **P2-tending (prior self-work toward the integrated pipeline)** — the candidate's prior preprocessing studies (#23, #24) that move toward the formalisation but predate the integrated-preprocessing-CNN paradigm as formally defined in this dissertation. Per CFC-2.7 they must be cited as prior own work and as evolutionary precursors of the pipeline, not as full P2 instantiations.
- **N/A** — the source does not have a paradigmatic position in the P1/P2 dichotomy: dataset descriptors, methodology references (Grad-CAM, SSIM, calibration), pathophysiology reviews, mathematical models, system architectures, surveys.

Per CFC-2.9 and SIR-1, no source has been attributed an explicit "preprocessing is unimportant" claim. P1 tagging is a claim about *observable methodological practice*, not about authorial intent. Per CFC-2.2, no Paradigm tag licenses a head-to-head numerical comparison with the source. Per SB-1.12, the Paradigm column does not redefine the dissertation's operational experimental baseline (configs A/C, OD-3).

**v6.0.0 navigation-sync note (READ FIRST for cross-references).**
This index was re-aligned to the corrected chapter structure. The seven experiments are now all in Chapter 4; Chapter 5 is validation/analysis. Where older notes below cite section numbers, translate per this remap: **old §5.1 (cross-database generalization / Exp 5) → §4.4** (Cross-Dataset Transferability, Exp 3) and **§4.6** (Clinical Degradation, Exp 5); **old §5.2 → §5.1** (Explainability Results); **old §5.3 (device domain shift, Exp 6) → §4.7**; **old §5.4 → §5.2** (Statistical Validation); **old §5.5 → §5.3** (Comparative Analysis); **old §5.6 → §5.4** (Limitations). The old "Robustness to Image Degradation" experiment (old §4.4) is dropped. H-1 is now **"Integrated Pipeline Dominance"** (composite *preprocessing × pretraining-source* IV: ImageNet baseline vs. ophthalmology-specific SSL); CLAHE is named **"dual-constraint clip limit"**; §2.3.3 and §3.3.2 are new SSL sections per the v6.0.0 amendment.

**Existing notes (retained):**

1. Sources #06 and #10 are **duplicate entries** for the same article (Porwal et al., 2018 — IDRiD dataset descriptor). Consider consolidating to a single entry.
2. ~~Sources #11 and #13 duplicate~~ — RESOLVED: duplicate card removed; Source #11 (ting-2017.md) is the canonical entry. #13 is retired and is not used anywhere in this index.
3. Source #18 (González-Díaz et al., 2024) addresses **AMD, not diabetic retinopathy**. Its relevance is peripheral (ViT architecture comparison only).

**Self-publication notes (retained):**

4. Sources #19–#24 are all **co-authored by the dissertation candidate** (🔹SELF flag). All carry **high self-plagiarism risk** — content must be explicitly self-cited and substantially reformulated in the dissertation.
5. Sources #23 and #24 are **duplicate entries for the same article** (Sapakova, Yesmukhamedov & Sapakov, 2025 — *Eastern-European Journal of Enterprise Technologies*, DOI: 10.15587/1729-4061.2025.335570). Two literature cards were prepared from different analytical perspectives. Consider consolidating to a single entry.
6. Sources #19 (CONF, Procedia CS 2025) and #21 (KBTU, Herald KBTU 2025) report **overlapping experiments** — both evaluate EfficientNetB0 frozen vs. fine-tuned on APTOS 2019 with nearly identical metrics. The dissertation should treat these as a single experimental thread with unified citation.
7. §6.2 (AI Processing Module / PACS and EHR Integration) accommodates the system architecture content from #22.

**Previous sources notes (#25–#32, retained):**

8. Source #25 (Wikipedia — AHE/CLAHE) is **NOT citable** in a doctoral dissertation. It serves only as a conceptual primer. Original sources (Pizer et al., 1987 = #54; Zuiderveld, 1994) should be cited instead. Classified as **Background reference**.
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
18. Source #38 (Khosravi et al., 2025) is the **strongest new external validation study** — multi-country (USA, South Korea, Brazil), multi-source (public + private), 2661 external images, FastViT vs ResNet18. **Not DR-focused** (retinal hemorrhage classification) but demonstrates cross-dataset ViT > CNN advantage. Directly supports §4.4 (cross-dataset transferability) arguments. Caution: severe class imbalance (2346 medical vs 315 trauma) and no CI/statistical tests.
19. Source #39 (Senapati et al., 2024) is a **PRISMA-based systematic review** of DR AI (2016–2023). Provides bibliometric landscape and identifies overfitting, class imbalance, and early-stage detection as key gaps. **Resolves ⚡ THIN status of §1.5** (was covered only by #17). No empirical benchmarking or ViT coverage. Moderate epistemic weight as field-mapping survey.
20. Source #40 (Araf et al., 2024) is the **first systematic review dedicated to cost-sensitive learning in medical data** (173 papers, 2010–2022). Reveals that only 2 of 173 studies were validation research. Strengthens §2.2.2 (loss functions for imbalanced data) and partially addresses §3.4 (evaluation frameworks). No architecture-level or DR-specific benchmarking.
21. Source #41 (Sharma et al., 2025) proposes ViT-CapsNet on EyePACS (30,262 images). **Critical inconsistency**: reported AUC values per class (0.44–0.56) are fundamentally incompatible with claimed 94% accuracy. No external validation, no hyperparameter transparency, no statistical testing. **Cite with extreme caution** — epistemic weight is low due to internal metric inconsistency.
22. Source #42 (Arora et al., 2024) applies EfficientNetB0 to Kaggle DR with undersampling (35,108 → 3,704 images). Internal accuracy 0.8653; max training accuracy 97.11% suggests **significant overfitting** (11-point gap). No AUC, no class-wise metrics, no external validation. CI bounds reported as identical values (likely artifact). Limited epistemic weight.
23. Source #43 (Ryu et al., 2021) is an **OCTA-based DR classification study** with external validation — ResNet101 on OCTA scans, AUC 0.960–0.976 internal, 0.938–0.962 external. **Not fundus-based**, but demonstrates temporal external validation methodology and CNN > handcrafted feature advantage. Useful as modality-shift reference for §1.3.1 and §1.4.
24. Source #44 (Zhang et al., 2022) is a **high-quality multicentre external validation study** published in BMJ Open. Ensemble CNN (Inception-V3/Xception/Inception-ResNet-V2) on 83,465 images from 4 centres. AUROC 0.9931 referable DR, Cohen's κ 0.86–0.93 vs experts. **Strongest new evidence for §4.4 (transferability) and §5.3 (comparative analysis)**. Limitation: China-only, no public dataset benchmarking, preprocessing not reported.
25. Source #45 (Ruamviboonsuk et al., 2022) is the **highest-impact new source** — prospective clinical validation of DL screening in Thailand's national programme, published in *The Lancet Digital Health*. Sens 91.4% VTDR, outperformed specialists (p=0.024), 9 sites, 7,651 patients. **Gold standard for §6.3 clinical deployment evidence**. Limitation: no architecture transparency, no preprocessing details, single-country.

**Impact of new sources on coverage gaps:**

26. §1.1.1 (Pathophysiology) upgraded from **2 sources to 5 sources** (#31, #32, #33, #34, #35). **Well-covered**.
27. §1.1.2 (Screening Requirements) upgraded from **3 to 4 sources** (added #34 via screening compliance data).
28. §1.4 (Critical Analysis of DR Systems) upgraded from **8 to 12 sources** (added #39, #43, #44, #45). **Very well-covered**.
29. §1.5 (Formulation of Research Problem) upgraded from **⚡ THIN (1 source) to 2 sources** (#17, #39). No longer critically thin.
30. §2.2.2 (Loss Functions / Imbalanced Data) upgraded from **3 to 6 sources** (added #39, #40, #42).
31. §3.4 (Evaluation Framework) upgraded from **⚡ THIN (1 🔹SELF) to 2 sources** (added #40). Now has external support.
32. §4.4 (Cross-Dataset Transferability, Exp 3) carries the external-validation corpus formerly indexed under old §5.1 — #02, #04, #05, #07, #11, #12, #16, #17, #38, #44, #48. **Well-covered.**
33. §5.3 (Comparative Analysis) upgraded from **9 to 11 sources** (added #44, #45 to the prior comparative-analysis corpus).
34. §6.2 (PACS/EHR Integration) upgraded from **⚡ THIN (1 🔹SELF) to 2 sources** (added #36). Now has external support.
35. §6.3 (Clinical Workflow) upgraded from **5 to 7 sources** (added #34, #44, #45). **Very well-covered**.
36. **Remaining true gaps**: §1.2.1, §3.1.4 (by design), and the new §3.3.2 (SSL). §2.1.3 was resolved by #55/#56.
37. **⚠️ Self-only coverage warning:** Sections §2.4.1, §4.2, §6.1 remain covered **only by self-publications**. External supporting literature is strongly recommended for examiner robustness.
38. **⚠️ Metric inconsistency flag**: Source #41 (Sharma et al., 2025) reports class-level AUC values (0.44–0.56) incompatible with 94% accuracy. Do NOT cite AUC values without explicit disclaimers.

**Notes on the explainability / device-shift expansion (#46–#82):**

39. Sources #46–#53 support the expanded experimental design (explainability, device domain shift, calibration, image-quality metrics). Sources #46 (Selvaraju, Grad-CAM), #47 (EyePACS descriptor), #48 (Messidor descriptor), #52 (Guo, calibration), and #53 (Wang, SSIM) are canonical references. Sources #49 (RFMiD, Pachade et al. 2021) and #50 (DDR, Li et al. 2019) are dataset descriptors with identifiable papers — **cards now written**. Source #51 (ODIR-5K) is **resolved**: it has no peer-reviewed descriptor and is cited as the ODIR-2019 challenge **electronic resource** — **card now written**.
40. §2.5 (Explainability in Deep Learning for Medical Imaging) requires Grad-CAM formalization. Source #46 (Selvaraju et al., 2017) is the foundational reference; #57 (CAM) and #58 (Grad-CAM++) complete the lineage.
41. §1.2.3 (Device-Specific Variability in Fundus Imaging) and §4.7 (Experiment 6: Device Domain Shift). Sources #49, #50, #51 provide dataset descriptors with camera model information; #74, #75, #76 supply the domain-shift theory.
42. **Section numbering authority.** The Section Map Key above is authoritative and reflects the corrected TABLE_OF_CONTENTS (EN/KZ) under INVARIANTS v6.0.0. Historical "Maps to" entries in individual literature cards still using the v2.1/v3.0 numbering must be remapped per the v6.0.0 navigation-sync note during the next literature-card pass.

**New sources notes (#54–#82) — foundational method, architecture, explainability, and domain-shift corpus:**

43. Sources #54–#82 are **foundational / methodological references** grounding the dissertation's preprocessing, architecture, transfer-learning, explainability, and domain-shift chapters in their canonical primary literature. Most are **N/A** under the Paradigm rule (architecture papers, methodology references, surveys, dataset/benchmark descriptors) because they are not CNN/ViT-based **DR/retinal** classification studies. Only #77 (Abràmoff — autonomous DR detection) and #78 (Fu — EyeQ retinal image-quality classification) are retinal-image CNN studies and are tagged **P1**.
44. **CLAHE provenance resolved.** Source #54 (Pizer et al., 1987) introduces *clipped* adaptive histogram equalization — the methodological origin of CLAHE. It is the **citable primary source** that replaces the non-citable Wikipedia entry (#25) flagged in note 8. The dissertation should cite #54 (and Zuiderveld, 1994, if acquired) for CLAHE rather than #25 in §2.1.1–§2.1.2.
45. **§2.1.3 GAP resolved.** Sources #55 (Tomasi & Manduchi — bilateral filtering) and #56 (Buades et al. — non-local means) supply the previously-missing spatial-filtering / noise-reduction literature. Both are method papers with qualitative (not benchmark) evaluation; cite as algorithmic foundations, not as evidence of DR classification gains.
46. **Explainability corpus.** Source #57 (Zhou et al., 2016 — CAM) and #58 (Chattopadhyay et al., 2018 — Grad-CAM++); together with #46 (Selvaraju — Grad-CAM) they ground §2.5.1–§2.5.2 and Exp 4 (§4.5). Sources #59 (Tjoa & Guan), #60 (Samek et al. — LRP), #61 (Lundberg & Lee — SHAP), and #62 (Ribeiro et al. — LIME) broaden §1.3.3/§2.5. **Caution:** #61 (SHAP) and #62 (LIME) are feature-attribution methods not used as the dissertation's primary lesion-localization tool — cite as XAI background, not as the operational explainability metric.
47. **§2.5.3 grounding.** Source #63 (Rezatofighi et al. — Generalized IoU) and #64 (Everingham et al. — PASCAL VOC, defining AP and the IoU > 0.5 criterion) provide the formal IoU grounding for the ALO/IoU overlap evaluation in Exp 4 (§4.5). Both are object-detection references; the dissertation must frame IoU as an *overlap metric borrowed for lesion-localization evaluation*, not as a detection benchmark.
48. **CNN backbone provenance.** Sources #65 (AlexNet), #66 (ResNet), #67 (DenseNet), #68 (EfficientNet), #69 (EfficientNetV2) and #70 (ViT) are the canonical architecture papers. **#66 (ResNet-50)** and **#68 (EfficientNet-B3)** are the dissertation's two operational backbones (Exp 1, configs A–D) and should be cited at first mention in §3.2. #70 (ViT) and #69 (EfficientNetV2) support the CNN-vs-ViT discussion (§1.3.1).
49. **Transfer-learning / SSL theory.** Sources #71 (Yosinski et al.), #72 (Kornblith et al.), and #73 (Cheplygina et al. — SSL/MIL/TL medical survey) ground §2.3.1–§2.3.2. **#73 additionally anchors the new §2.3.3 / §3.3.2 (in-domain self-supervised pretraining)** per the v6.0.0 amendment, but is a general survey — dedicated DINO/BYOL/SimCLR/MoCo and ophthalmology-SSL primary sources still need to be acquired (see §3.3.2 GAP).
50. **Domain-shift literature.** Sources #74 (Zhou et al. — DG survey), #75 (Wang & Deng — DA survey), and #76 (Ganin et al. — DANN) supply the conceptual and methodological grounding for §1.2.3 and Exp 6 (§4.7 device domain shift), previously covered by dataset descriptors only. These are general-purpose (non-retinal) references; cite for problem framing, not as retinal-domain-shift evidence.
51. Source #77 (Abràmoff et al., 2018 — IDx-DR pivotal trial) is a **high-impact prospective clinical-validation precedent** (FDA-authorized autonomous DR system). Strongest new support for §1.4 and §6.3 clinical-deployment arguments. **Limitation:** no preprocessing ablation and no public-benchmark comparison — must not be cited as evidence for the integrated-pipeline-dominance hypothesis.
52. Source #78 (Fu et al., 2020 — EyeQ) re-annotates **28,792 EyePACS images** into a 3-level retinal image-quality dataset and shows downstream DR-detection performance degrades with image quality. Supports §1.2.2 (image quality → performance) and §4.7 (multi-camera EyePACS acquisition). EyePACS-derived single-source; no external validation.
53. **Off-topic / domain-mismatch cards (#79–#82).** Sources #79 (encrypted cloud search), #80 (Hermite-function mathematics), #81 (muon-capture nuclear physics), and #82 (graphene quantum-Hall physics) are **outside the medical-imaging / DR domain** and carry negligible relevance. They are indexed for completeness and registered in the Peripheral Sources Registry below. They should **not** appear in the dissertation literature review.
54. **Alternate / supplementary cards for already-indexed sources (no new number assigned).** Two newly-supplied cards are second analytical cards for sources already in this index and do **not** receive new source numbers:
    - `gulshan-2016-supplementary-validation.md` → maps to **#12** (Gulshan et al., 2016). Analyses the JAMA supplementary appendix (scale-normalisation to 299 px, FOV-mask exclusion) and reinforces #12's §1.2.2/§3.1 preprocessing detail; cite under #12.
    - `voets-2019-reproduction-study.md` → maps to **#17** (Voets et al., 2019). Details the public-data reproduction (EyePACS AUC 0.951, Messidor-2 0.853) and reproducibility recommendations; cite under #17.
    Both files are in `external/` for archival completeness but are consolidated to their canonical entries (analogous to the #06/#10 and #23/#24 duplicate-card handling).

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
| 46 🆕 | Selvaraju et al. (2017) | Foundational (explainability) | Core methodology: Grad-CAM formalization for §2.5 and Exp 4 (§4.5) |
| 47 🆕 | EyePACS descriptor | Dataset descriptor | Infrastructure: primary training dataset characterization |
| 48 🆕 | Messidor / Messidor-2 descriptor | Dataset descriptor | Infrastructure: external generalization dataset characterization |
| 49 ✅ | Pachade et al. (2021) — RFMiD | Dataset descriptor | Infrastructure: device domain shift dataset (TOPCON 3D OCT-2000 / Kowa VX-10α / TOPCON TRC-NW300) |
| 50 ✅ | Li et al. (2019) — DDR | Dataset descriptor | Infrastructure: device domain shift dataset (42 camera types) |
| 51 ✅ | ODIR-2019 / ODIR-5K (electronic resource) | Dataset descriptor | Infrastructure: device domain shift dataset (Canon/Zeiss/Kowa) |
| 52 ✅ | Guo et al. (2017) — `guo-2017-calibration.md` | Foundational (calibration) | Methodology: ECE / temperature scaling for §3.4, §5.2 |
| 53 ✅ | Wang et al. (2004) — `wang-2004-ssim.md` | Foundational (image quality) | Methodology: SSIM metric definition for §2.6, §3.1 |

### Epistemic Tier Summary (New Sources #54–#82)

| # | Source | Epistemic Tier | Dissertation Role |
|---|--------|----------------|-------------------|
| 54 🆕 | Pizer et al. (1987) | Foundational (preprocessing) | Methodology: CLAHE precursor; citable replacement for #25 in §2.1.1–§2.1.2 |
| 55 🆕 | Tomasi & Manduchi (1998) | Foundational (preprocessing) | Methodology: bilateral filtering for §2.1.3 |
| 56 🆕 | Buades et al. (2011) | Foundational (preprocessing) | Methodology: non-local means denoising for §2.1.3 |
| 57 🆕 | Zhou et al. (2016) | Foundational (explainability) | Methodology: CAM origin for §2.5.1–§2.5.2 |
| 58 🆕 | Chattopadhyay et al. (2018) | Foundational (explainability) | Methodology: Grad-CAM++ for §2.5.1–§2.5.2, Exp 4 (§4.5) |
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
| 73 🆕 | Cheplygina et al. (2018) | Survey (medical ML) | Framing: SSL/MIL/TL under limited labels for §2.3.1–§2.3.2; anchors new §2.3.3 / §3.3.2 |
| 74 🆕 | Zhou et al. (2022) | Foundational survey (DG) | Framing: domain-generalization grounding for §1.2.3, §4.7 |
| 75 🆕 | Wang & Deng (2018) | Foundational survey (DA) | Framing: domain-adaptation taxonomy for §1.2.3, §4.7 |
| 76 🆕 | Ganin et al. (2016) | Foundational (domain adaptation) | Methodology: DANN/gradient reversal for §4.7, §2.3.2 |
| 77 🆕 | Abràmoff et al. (2018) | High-impact clinical validation | Core evidence: autonomous DR pivotal trial for §1.4, §6.3 |
| 78 🆕 | Fu et al. (2020) | Dataset descriptor + RIQA | Evidence: image-quality↔DR performance (EyeQ) for §1.2.2, §4.7 |
| 79 🆕 | Chin & Shih (2021) | Peripheral (off-domain) | Excluded: encrypted-search; no DR relevance |
| 80 🆕 | Koch (2019) | Peripheral (off-domain) | Excluded: special-functions mathematics; no DR relevance |
| 81 🆕 | Hungerford (1999) | Peripheral (off-domain) | Excluded: nuclear physics; no DR relevance |
| 82 🆕 | Ostahie et al. (2015) | Peripheral (off-domain) | Excluded: condensed-matter physics; no DR relevance |

### Epistemic Tier Summary (New Sources #83–#121 — v6.1.0 expansion)

| # | Source | Epistemic Tier | Dissertation Role |
|---|--------|----------------|-------------------|
| 83 🆕 | Zhou et al. (2020) — FGADR | Benchmark / dataset descriptor | Comparator: pixel-level lesion benchmark; interpretable-grading framing (not a dissertation dataset) |
| 84 🆕 | Zhou et al. (2023) — RETFound | High-impact / foundational (ophthalmology SSL) | Core: in-domain SSL evidence; anchors §2.3.3/§3.3.2 + composite H-1 pretraining arm |
| 85 🆕 | Azizi et al. (2021) — MICLe | Methodological precedent (medical SSL) | Support: in-domain SSL > ImageNet transfer (derm/CXR) |
| 86 🆕 | Chen et al. (2020) — SimCLR | Foundational (contrastive SSL) | Background: SSL design space |
| 87 🆕 | He et al. (2020) — MoCo | Foundational (contrastive SSL) | Background: SSL design space |
| 88 🆕 | Grill et al. (2020) — BYOL | Foundational (non-contrastive SSL) | Background: SSL design space |
| 89 🆕 | Caron et al. (2021) — DINO | Foundational (SSL for ViT) | Background: SSL + emergent attention |
| 90 🆕 | He et al. (2022) — MAE | Foundational (masked image modeling) | Core method: pretraining basis of RETFound |
| 91 🆕 | Chen & He (2021) — SimSiam | Foundational (SSL analysis) | Background: collapse-avoidance mechanism |
| 92 🆕 | Shurrab & Duwairi (2022) | Survey (medical SSL) | Framing: medical-SSL landscape for §2.3.3/§3.3.2 |
| 93 🆕 | Shen et al. (2020) — cofe-Net | High-impact empirical (preprocessing) | Core: resolves §1.2.1 degradation-sources gap; preprocessing-as-component support |
| 94 🆕 | Zago et al. (2018) — RIQA | Empirical (image quality) | Support: fundus RIQA for §2.6/§1.2.2 |
| 95 🆕 | Zuiderveld (1994) — CLAHE | Foundational (preprocessing) | Core method: canonical CLAHE source for §2.1.1–§2.1.2 (replaces #25) |
| 96 🆕 | Lin et al. (2017) — Focal Loss | Foundational (loss) | Core method: the dissertation's training loss (γ=2) |
| 97 🆕 | Cui et al. (2019) — Class-Balanced Loss | Methodological precedent (loss) | Support: imbalanced-data re-weighting |
| 98 🆕 | Buda et al. (2018) — imbalance study | Methodological precedent | Support: imbalance-handling guidance |
| 99 🆕 | Kingma & Ba (2015) — Adam | Foundational (optimizer) | Method: training optimizer reference |
| 100 🆕 | Ioffe & Szegedy (2015) — BatchNorm | Foundational (normalization) | Method: intrinsic to ResNet-50; small-batch caveat |
| 101 🆕 | Srivastava et al. (2014) — Dropout | Foundational (regularization) | Method: regularization reference |
| 102 🆕 | Zhang et al. (2018) — mixup | Methodological precedent (augmentation) | Support: augmentation-as-regularization |
| 103 🆕 | Shorten & Khoshgoftaar (2019) | Survey (augmentation) | Framing: augmentation taxonomy for §2.2.3 |
| 104 🆕 | Cubuk et al. (2020) — RandAugment | Methodological precedent (augmentation) | Support: practical augmentation policy |
| 105 🆕 | Simonyan & Zisserman (2015) — VGG | Foundational (architecture) | Background: CNN-depth lineage; cited DR baselines |
| 106 🆕 | Szegedy et al. (2015) — GoogLeNet | Foundational (architecture) | Background: Inception lineage |
| 107 🆕 | Szegedy et al. (2016) — Inception-v3 | Foundational (architecture) | Background: backbone of Gulshan (#12) + Esteva (#121); label smoothing |
| 108 🆕 | Liu et al. (2021) — Swin Transformer | Foundational (ViT) | Comparator: CNN-vs-ViT discussion; cited DR/ViT hybrids |
| 109 🆕 | Pan & Yang (2010) | Survey (transfer learning) | Framing: transfer-learning taxonomy for §2.3 |
| 110 🆕 | Litjens et al. (2017) | Survey (medical DL) | Framing: medical-DL field landscape for §1.3 |
| 111 🆕 | Quellec et al. (2017) | High-impact empirical (DR explainability) | Evidence: weakly-supervised lesion heatmaps (Exp 4 precedent) + cross-dataset |
| 112 🆕 | Gargeya & Leng (2017) | High-impact empirical (DR screening) | Evidence: external validation (Messidor-2/e-ophtha) |
| 113 🆕 | Krause et al. (2018) | High-impact methodological precedent | Evidence: reference-standard / label-quality for §3.4 |
| 114 🆕 | Son et al. (2020) | High-impact empirical (multi-finding) | Evidence: in-house→external degradation for §4.7 |
| 115 🆕 | Bellemo et al. (2019) | High-impact clinical validation | Core evidence: cross-population transfer (Zambia) for §4.4/§6.3 |
| 116 🆕 | Dai et al. (2021) — DeepDR | High-impact empirical (multi-task DR) | Evidence: integrated quality+lesion+grading; external validation |
| 117 🆕 | De Fauw et al. (2018) | High-impact clinical validation | Core evidence: device-independent representation (preprocessing-as-component) |
| 118 🆕 | Ting et al. (2019) | Survey (ophthalmology DL) | Framing: technical + clinical-translation review |
| 119 🆕 | Beede et al. (2020) | High-impact socio-technical study | Evidence: clinical-deployment human factors for §6.1/§6.3 |
| 120 🆕 | Burlina et al. (2017) | Empirical (AMD CNN) | Comparator: color-fundus CNN-grading + transfer learning (AMD, peripheral) |
| 121 🆕 | Esteva et al. (2017) | Foundational / high-impact precedent | Background: medical transfer-learning landmark; **P1 end-to-end paradigm foil** to the integrated pipeline |

> **✅ Dataset-descriptor cards completed (2026-06-16):** #49 (Pachade — RFMiD `pachade-2021-rfmid.md`), #50 (Li — DDR `li-2019-ddr.md`), and #51 (ODIR-2019 / ODIR-5K `odir-2019-dataset.md`) now have card files. #51's "TO BE IDENTIFIED" flag is **resolved**: ODIR-5K has no peer-reviewed descriptor and is carded/cited as the ODIR-2019 challenge **electronic resource**. Cards were compiled from open-access records (RFMiD abstract + dataset docs; DDR abstract + official repository, full Elsevier text pending; ODIR challenge site) — each carries a Source-access note and `[NOT REPORTED]`/`[VERIFY]` flags where the full text was not accessed. Upgrade #50 from the full PDF when available.
