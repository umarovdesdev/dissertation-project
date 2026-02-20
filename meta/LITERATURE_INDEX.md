# LITERATURE INDEX
## External Source Corpus — Navigation Table

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Generated from:** Literature Cards in /LITERATURE/
**Total sources indexed:** 45

---

### Section Map Key

| Code | Dissertation Section |
|------|---------------------|
| §1.1.1 | Pathophysiology and Clinical Grading Systems |
| §1.1.2 | Screening Requirements in Resource-Limited Healthcare Settings |
| §1.2.1 | Sources of Image Degradation in Clinical Practice |
| §1.2.2 | Impact of Image Quality on Diagnostic Model Performance |
| §1.3.1 | CNN Architectures for Medical Imaging |
| §1.3.2 | Transfer Learning Strategies in Ophthalmic Diagnostics |
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
| §3.1   | Formalization of the Unified Preprocessing Pipeline |
| §3.2   | Design of Baseline and Enhanced CNN Architectures |
| §3.3   | Transfer Learning Methodology Using EfficientNetB0 and ResNet50 |
| §3.4   | Evaluation Framework and Performance Metrics |
| §4.1   | Datasets and Experimental Configuration |
| §4.2   | Experiment 1: Baseline vs Enhanced CNN |
| §4.3   | Experiment 2: CLAHE Threshold Optimization |
| §4.4   | Experiment 3: Transfer Learning Strategy Comparison |
| §5.1   | Cross-Database Generalization Testing |
| §5.2   | Statistical Validation of Preprocessing Dominance |
| §5.3   | Comparative Analysis with Existing DR Systems |
| §6.1   | System Requirements and Design Principles |
| §6.2   | Modular Architecture with PACS and EHR Integration |
| §6.3   | Clinical Workflow Integration |
| INTRO  | Introduction (contextual framing) |

---

### Source Index

| # | Source | Type | Key Result | Dataset | Maps to |
|---|--------|------|------------|---------|---------|
| 01 | Pratt et al. (2016) | CNN classification | 75% acc, 30% sens, 95% spec, 5-class DR, Kaggle | EyePACS/Kaggle | §1.3.1, §2.2.2, §2.2.3, INTRO |
| 02 | Saxena et al. (2020) | Cross-dataset validation | AUC 0.958 Messidor-1, 0.92 Messidor-2, binary DR, InceptionResNetV2 | EyePACS/Kaggle, Messidor-1, Messidor-2 | §1.3.2, §1.4, §3.1, §5.1, §5.3 |
| 03 | Sánchez-Gutiérrez et al. (2022) | Clinical validation | AUC 0.988, 90.5% sens, 97.1% spec, 96% workload reduction, RetCAD | Private (Ramon y Cajal) | §1.4, §6.3 |
| 04 | Arrieta et al. (2022) | CNN classification | AUC 0.94 EyePACS, 0.89 Messidor-2, semi-supervised with 2% labels | EyePACS/Kaggle, Messidor-2 | §1.3.1, §2.3.1, §5.1 |
| 05 | Rakhlin (2017) | Cross-dataset validation | AUC 0.967 Messidor-2, 0.923 Kaggle, modified VGGNet | EyePACS/Kaggle, Messidor-2 | §1.2.2, §1.3.1, §5.1, §5.3 |
| 06 | Porwal et al. (2018) | Dataset descriptor | IDRiD: 516 images, 81 pixel-annotated, Indian population, 5-class DR | IDRiD | §1.1.2, §4.1, INTRO |
| 07 | Baget-Bernaldiz et al. (2021) | External validation | AUC 0.988 RDR own pop., 0.968 Messidor, 4-class ICDR | Private (Spanish), Messidor-1, EyePACS/Kaggle | §1.4, §5.1, §5.3 |
| 08 | Wan et al. (2021) | Segmentation | SE 92.77% exudates (e_ophtha_EX), AUPR 0.78 hard exudates (IDRiD) | IDRiD, e_ophtha_EX, Private | §1.3.1, §2.2.1 |
| 09 | Xu et al. (2024) | Ensemble / Hybrid | Acc 0.97, AUC 0.97, EfficientNet+Swin Transformer V2 hybrid, 5-class | APTOS 2019 | §1.3.1, §1.3.2, §3.2 |
| 10 | Porwal et al. (2018) | Dataset descriptor | IDRiD: 516 images, pixel-level lesion masks + DR/DME grading, Indian pop. | IDRiD | §1.1.2, §4.1, INTRO |
| 11 | Ting et al. (2017) | External validation | AUC 0.936 referable DR, validated on 10 multiethnic datasets (AUC 0.889–0.983) | SIDRP (private), 10 external cohorts | §1.4, §5.1, §5.3, §6.3 |
| 12 | Gulshan et al. (2016) | CNN classification | AUC 0.991 EyePACS-1, 0.990 Messidor-2, Inception-v3 ensemble | EyePACS (private), Messidor-2 | §1.3.1, §1.3.2, §1.4, §5.1, §5.3, INTRO |
| 13 | Ting et al. (2017) | External validation | AUC 0.936 rDR, 100% sens vtDR, 10 multiethnic external datasets | SIDRP (private), 10 external cohorts | §1.4, §5.1, §5.3, §6.3 |
| 14 | Wewetzer et al. (2021) | Meta-analysis | Pooled sens 87%, spec 90%, SROC AUC 0.9543, 10 DL screening studies in PC | Multiple (pooled) | §1.4, §5.3, §6.3, INTRO |
| 15 | Liu et al. (2022) | Benchmark study | κw 0.9303 DR grading, 0.70 image quality accuracy, EfficientNet dominant | DeepDRiD | §1.2.2, §1.3.1, §3.1, §4.1 |
| 16 | Goh et al. (2024) | CNN classification | SWIN AUC 95.7% Kaggle, 97.3% SEED, 96.3% Messidor-1, ViT > CNN | EyePACS/Kaggle, SEED, Messidor-1 | §1.3.1, §5.1, §5.2, §5.3 |
| 17 | Voets et al. (2019) | Cross-dataset validation | AUC 0.951 EyePACS, 0.853 Messidor-2 (reproduction of Gulshan 2016) | EyePACS/Kaggle, Messidor-2 | §1.2.2, §1.5, §5.1, §5.2 |
| 18 | González-Díaz et al. (2024) | ViT comparison | ViT acc 83.69%, BEiT F1 86.36%, 4-class AMD, 305 images | Private (curated AMD) | §1.3.1 |
| **19** | **Sapakova et al. (2025)** 🔹SELF | **Transfer learning** | **F1 0.74 fine-tuned vs 0.62 frozen, EfficientNetB0, 5-class DR** | **APTOS 2019, Private clinical** | **§2.3.2, §3.3, §4.4, §4.1, §2.2.2, §2.2.3, §3.1** |
| **20** | **Sapakova et al. (2024)** 🔹SELF | **Mathematical modeling** | **Thermal model of laser-fundus interaction, FDM simulation, qualitative** | **None (simulation)** | **§2.4.1** |
| **21** | **Yesmukhamedov et al. (2025a)** 🔹SELF | **Transfer learning** | **Precision 75% fine-tuned vs 65% frozen, EfficientNetB0, 5-class DR** | **APTOS 2019, Private clinical** | **§2.3.2, §3.3, §4.4, §3.1, §3.4, §2.2.2, §2.2.3** |
| **22** | **Yesmukhamedov et al. (2025b)** 🔹SELF | **System architecture** | **Modular AI diagnostic architecture for Kazakhstan, physician-in-the-loop** | **None (design study)** | **§6.1, §6.2, §6.3, §1.4, §1.1.2** |
| **23** | **Sapakova, Yesmukhamedov & Sapakov (2025a)** 🔹SELF | **CLAHE / Enhancement** | **100% acc/sens/spec, upgraded CLAHE T/80 + ResNet50, 5-class retinal** | **STARE** | **§2.1.2, §3.1, §3.3, §4.3, §5.3, §2.1.1** |
| **24** | **Sapakova, Yesmukhamedov & Sapakov (2025b)** 🔹SELF | **Preprocessing study** | **Val acc 71%→86% with preprocessing, ROC-AUC 0.9638, 4-layer CNN** | **APTOS 2019, Private clinical** | **§3.1, §3.2, §4.2, §4.1, §2.1.2, §5.2, §1.2.2** |
| 25 | Wikipedia — Adaptive Histogram Equalization | Background reference | Algorithmic description of AHE/CLAHE; clip limit 3–4, 8×8 tile grid | None | §2.1.1, §2.1.2 |
| 26 | Shaout & Han (2025) | Preprocessing study | FCE+CLAHE 59% preference, 88% combined; fuzzy logic + CLAHE blending | DRIVE | §2.1.1, §3.1 |
| 27 | Hayati et al. (2023) | CLAHE / Enhancement | CLAHE improved 3/4 CNNs; EfficientNetB4 97.83% acc; ResNet34 −12.02% | APTOS 2019 | §2.1.1, §2.1.2, §3.1, §4.3, §5.2 |
| 28 | Brancati et al. (2025) | Peripheral (FHIR / breast ML) | MLP 97.67% acc breast lesion, 3 hand-crafted features, BUSI | BUSI | Peripheral |
| 29 | Tabari et al. (2024) | Review / Survey (FHIR) | 27 studies reviewed; FHIR pipeline-based (21) vs non-linear (6) models | None (scoping review) | Peripheral |
| 30 | Chakka (2023) | Preprocessing study | Rescaling best of 4 techniques for OCT; ResNet-50; no numerical metrics | Kaggle OCT (4,480 images) | §2.1.1 |
| 31 | Kesharwani et al. (2021) | Review / Survey (clinical) | Narrative DR review; 95% vision loss preventable if treated early | None (narrative review) | §1.1.1 |
| 32 | Kusuhara et al. (2018) | Review / Survey (clinical) | DR prevalence 34.6%; pericyte dropout → BRB breakdown; VEGF/Ang2 pathways | None (narrative review) | §1.1.1 |
| 33 | Gettinger et al. (2025) | Review (pathophysiology / experimental models) | No single model reproduces full human DR phenotype; STZ limited to early-stage | None (narrative review) | §1.1.1, INTRO |
| 34 | Morya et al. (2024) | Review (pathophysiology / treatment) | DR present in 1/3 of diabetic patients; 35–55% screening compliance; Remidio 98% sens | None (narrative review) | §1.1.1, §1.1.2, §6.3 |
| 35 | Wang & Lo (2018) | Review (pathophysiology / treatment) | Neurodegeneration may precede microvasculopathy; anti-VEGF first-line for DME/PDR | None (narrative review) | §1.1.1, INTRO |
| 36 | Nandal (2024) | Empirical (AI-driven HL7/FHIR interoperability) | 93% semantic mapping precision; F1=0.89 NLP extraction; 97% interoperability | MIMIC-III, Synthetic HL7 | §6.2 |
| 37 | Geetha & Hema (2026) | ViT hybrid (DR + glaucoma) | 98.4% acc; ViT + BFF + HGS optimizer; no external validation | Open-source (unnamed) | §1.3.1 |
| 38 | Khosravi et al. (2025) | External validation (retinal hemorrhage) | FastViT AUC 0.9811, ResNet18 AUC 0.9626; 2661-image external dataset | RFMiD, DeepEyeNet, BRSET, Private (multi-country) | §1.3.1, §5.1 |
| 39 | Senapati et al. (2024) | Systematic review (DR AI) | PRISMA-based; 2016–2023; EyePACS 75,523 images; identifies overfitting + class imbalance gaps | Multiple (surveyed) | §1.4, §1.5, §2.2.2 |
| 40 | Araf et al. (2024) | Systematic review (cost-sensitive learning) | 173 papers reviewed; CSL preserves distribution; only 2 validation studies identified | Multiple (surveyed) | §2.2.2, §3.4 |
| 41 | Sharma et al. (2025) | ViT-CapsNet hybrid (DR) | 94% acc on EyePACS (30,262 images); AUC 0.44–0.56 per class; no external validation | EyePACS/Kaggle | §1.3.1, §4.1 |
| 42 | Arora et al. (2024) | CNN classification (DR) | EfficientNetB0 avg acc 0.8653; max training acc 97.11%; undersampled to 3,704 images | Kaggle DR Resized (35,108 images) | §1.3.1, §2.2.2 |
| 43 | Ryu et al. (2021) | CNN classification + external validation (OCTA) | AUC 0.960–0.976 internal; AUC 0.938–0.962 external; ResNet101 on OCTA | Private (single-center) | §1.3.1, §1.4 |
| 44 | Zhang et al. (2022) | Multicentre external validation (DR screening) | AUROC 0.9931 referable DR (image); 0.9848 (patient); Cohen's κ 0.86–0.93 vs experts | Private (83,465 images, 4 centres) | §1.4, §5.1, §5.3, §6.3 |
| 45 | Ruamviboonsuk et al. (2022) | Prospective clinical validation (DR screening) | Acc 94.7%, sens 91.4% VTDR; outperformed specialists (p=0.024); 9 Thai sites | Private (7,651 patients, prospective) | §1.4, §5.3, §6.3 |

---

### Coverage Matrix

| Dissertation Section | Sources Covering It |
|---------------------|---------------------|
| §1.1.1 | #31, #32, **#33, #34, #35** |
| §1.1.2 | #06, #10, **#22**, #34 |
| §1.2.1 | ⚠️ GAP |
| §1.2.2 | #05, #15, #17, **#24** |
| §1.3.1 | #01, #04, #05, #08, #09, #12, #15, #16, #18, #37, #38, #41, #42, #43 |
| §1.3.2 | #02, #09, #12 |
| §1.4 | #02, #03, #07, #11, #12, #13, #14, **#22**, #39, #43, #44, #45 |
| §1.5 | #17, #39 |
| §2.1.1 | #25, #26, #27, #30, **#23** |
| §2.1.2 | #25, #27, **#23, #24** |
| §2.1.3 | ⚠️ GAP |
| §2.2.1 | #08 ⚡ THIN |
| §2.2.2 | #01, **#19, #21**, #39, #40, #42 |
| §2.2.3 | #01, **#19, #21** |
| §2.3.1 | #04 ⚡ THIN |
| §2.3.2 | **#19, #21** |
| §2.4.1 | **#20** ⚡ THIN |
| §3.1 | #02, #15, #26, #27, **#19, #21, #23, #24** |
| §3.2 | #09, **#24** |
| §3.3 | **#19, #21, #23** |
| §3.4 | **#21**, #40 |
| §4.1 | #06, #10, #15, **#19, #21, #24**, #41 |
| §4.2 | **#24** ⚡ THIN |
| §4.3 | #27, **#23** |
| §4.4 | **#19, #21** |
| §5.1 | #02, #04, #05, #07, #11, #12, #13, #16, #17, #38, #44 |
| §5.2 | #16, #17, #27, **#24** |
| §5.3 | #02, #05, #07, #11, #12, #13, #14, #16, **#23**, #44, #45 |
| §6.1 | **#22** ⚡ THIN |
| §6.2 | **#22**, #36 |
| §6.3 | #03, #11, #13, #14, **#22**, #34, #44, #45 |
| INTRO | #01, #06, #10, #12, #14, #33, #35 |

---

### Gaps Identified

**⚠️ GAP (0 sources):**
- §1.2.1 — Sources of Image Degradation in Clinical Practice
- §2.1.3 — Spatial Filtering and Noise Reduction Methods

**⚡ THIN (1 source):**
- §2.2.1 — Convolution, Pooling, and Feature Extraction Operations (#08)
- §2.3.1 — Feature Transferability Across Visual Domains (#04)
- §2.4.1 — Coupled Thermal-Optical Model of Fundus Tissue Response (#20 🔹SELF only)
- §4.2 — Experiment 1: Baseline vs Enhanced CNN (#24 🔹SELF only)
- §6.1 — System Requirements and Design Principles (#22 🔹SELF only)

---

### Notes

**Existing notes (retained):**

1. Sources #06 and #10 are **duplicate entries** for the same article (Porwal et al., 2018 — IDRiD dataset descriptor). Consider consolidating to a single entry.
2. Sources #11 and #13 are **duplicate entries** for the same article (Ting et al., 2017 — JAMA multiethnic DLS validation). Consider consolidating to a single entry.
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
24. Source #44 (Zhang et al., 2022) is a **high-quality multicentre external validation study** published in BMJ Open. Ensemble CNN (Inception-V3/Xception/Inception-ResNet-V2) on 83,465 images from 4 centres. AUROC 0.9931 referable DR, Cohen's κ 0.86–0.93 vs experts. **Strongest new evidence for §5.1 and §5.3**. Limitation: China-only, no public dataset benchmarking, preprocessing not reported.
25. Source #45 (Ruamviboonsuk et al., 2022) is the **highest-impact new source** — prospective clinical validation of DL screening in Thailand's national programme, published in *The Lancet Digital Health*. Sens 91.4% VTDR, outperformed specialists (p=0.024), 9 sites, 7,651 patients. **Gold standard for §6.3 clinical deployment evidence**. Limitation: no architecture transparency, no preprocessing details, single-country.

**Impact of new sources on coverage gaps:**

26. §1.1.1 (Pathophysiology) upgraded from **2 sources to 5 sources** (#31, #32, #33, #34, #35). **Well-covered**.
27. §1.1.2 (Screening Requirements) upgraded from **3 to 4 sources** (added #34 via screening compliance data).
28. §1.4 (Critical Analysis of DR Systems) upgraded from **8 to 12 sources** (added #39, #43, #44, #45). **Very well-covered**.
29. §1.5 (Formulation of Research Problem) upgraded from **⚡ THIN (1 source) to 2 sources** (#17, #39). No longer critically thin.
30. §2.2.2 (Loss Functions / Imbalanced Data) upgraded from **3 to 6 sources** (added #39, #40, #42).
31. §3.4 (Evaluation Framework) upgraded from **⚡ THIN (1 🔹SELF) to 2 sources** (added #40). Now has external support.
32. §5.1 (Cross-Database Generalization) upgraded from **9 to 11 sources** (added #38, #44).
33. §5.3 (Comparative Analysis) upgraded from **9 to 11 sources** (added #44, #45).
34. §6.2 (PACS/EHR Integration) upgraded from **⚡ THIN (1 🔹SELF) to 2 sources** (added #36). Now has external support.
35. §6.3 (Clinical Workflow) upgraded from **5 to 7 sources** (added #34, #44, #45). **Very well-covered**.
36. **Remaining true gaps reduced to 2**: §1.2.1, §2.1.3. These still require **additional literature acquisition**.
37. **⚠️ Self-only coverage warning (reduced):** Sections §2.4.1, §4.2, §6.1 remain covered **only by self-publications**. External supporting literature is strongly recommended for examiner robustness.
38. **⚠️ Metric inconsistency flag**: Source #41 (Sharma et al., 2025) reports class-level AUC values (0.44–0.56) incompatible with 94% accuracy. Do NOT cite AUC values without explicit disclaimers.

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
