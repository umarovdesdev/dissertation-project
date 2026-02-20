# LITERATURE INDEX
## External Source Corpus — Navigation Table

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Generated from:** Literature Cards in /LITERATURE/
**Total sources indexed:** 24

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

---

### Coverage Matrix

| Dissertation Section | Sources Covering It |
|---------------------|---------------------|
| §1.1.1 | ⚠️ GAP |
| §1.1.2 | #06, #10, **#22** |
| §1.2.1 | ⚠️ GAP |
| §1.2.2 | #05, #15, #17, **#24** |
| §1.3.1 | #01, #04, #05, #08, #09, #12, #15, #16, #18 |
| §1.3.2 | #02, #09, #12 |
| §1.4 | #02, #03, #07, #11, #12, #13, #14, **#22** |
| §1.5 | #17 ⚡ THIN |
| §2.1.1 | **#23** ⚡ THIN |
| §2.1.2 | **#23, #24** |
| §2.1.3 | ⚠️ GAP |
| §2.2.1 | #08 ⚡ THIN |
| §2.2.2 | #01, **#19, #21** |
| §2.2.3 | #01, **#19, #21** |
| §2.3.1 | #04 ⚡ THIN |
| §2.3.2 | **#19, #21** |
| §2.4.1 | **#20** ⚡ THIN |
| §3.1 | #02, #15, **#19, #21, #23, #24** |
| §3.2 | #09, **#24** |
| §3.3 | **#19, #21, #23** |
| §3.4 | **#21** ⚡ THIN |
| §4.1 | #06, #10, #15, **#19, #21, #24** |
| §4.2 | **#24** ⚡ THIN |
| §4.3 | **#23** ⚡ THIN |
| §4.4 | **#19, #21** |
| §5.1 | #02, #04, #05, #07, #11, #12, #13, #16, #17 |
| §5.2 | #16, #17, **#24** |
| §5.3 | #02, #05, #07, #11, #12, #13, #14, #16, **#23** |
| §6.1 | **#22** ⚡ THIN |
| §6.2 | **#22** ⚡ THIN |
| §6.3 | #03, #11, #13, #14, **#22** |
| INTRO | #01, #06, #10, #12, #14 |

---

### Gaps Identified

**⚠️ GAP (0 sources):**
- §1.1.1 — Pathophysiology and Clinical Grading Systems
- §1.2.1 — Sources of Image Degradation in Clinical Practice
- §2.1.3 — Spatial Filtering and Noise Reduction Methods

**⚡ THIN (1 source):**
- §1.5 — Formulation of Research Problem (#17)
- §2.1.1 — Histogram Equalization and Adaptive Contrast Enhancement (#23 🔹SELF only)
- §2.2.1 — Convolution, Pooling, and Feature Extraction Operations (#08)
- §2.3.1 — Feature Transferability Across Visual Domains (#04)
- §2.4.1 — Coupled Thermal-Optical Model of Fundus Tissue Response (#20 🔹SELF only)
- §3.4 — Evaluation Framework and Performance Metrics (#21 🔹SELF only)
- §4.2 — Experiment 1: Baseline vs Enhanced CNN (#24 🔹SELF only)
- §4.3 — Experiment 2: CLAHE Threshold Optimization (#23 🔹SELF only)
- §6.1 — System Requirements and Design Principles (#22 🔹SELF only)
- §6.2 — Modular Architecture with PACS and EHR Integration (#22 🔹SELF only)

---

### Notes

**Existing notes (retained):**

1. Sources #06 and #10 are **duplicate entries** for the same article (Porwal et al., 2018 — IDRiD dataset descriptor). Consider consolidating to a single entry.
2. Sources #11 and #13 are **duplicate entries** for the same article (Ting et al., 2017 — JAMA multiethnic DLS validation). Consider consolidating to a single entry.
3. Source #18 (González-Díaz et al., 2024) addresses **AMD, not diabetic retinopathy**. Its relevance is peripheral (ViT architecture comparison only).

**New notes (self-publications):**

4. Sources #19–#24 are all **co-authored by the dissertation candidate** (🔹SELF flag). All carry **high self-plagiarism risk** — content must be explicitly self-cited and substantially reformulated in the dissertation.
5. Sources #23 and #24 are **duplicate entries for the same article** (Sapakova, Yesmukhamedov & Sapakov, 2025 — *Eastern-European Journal of Enterprise Technologies*, DOI: 10.15587/1729-4061.2025.335570). Two literature cards were prepared from different analytical perspectives (Q2 card focused on upgraded CLAHE + ResNet50; Q3 card focused on baseline vs. enhanced CNN pipeline). Consider consolidating to a single entry.
6. Sources #19 (CONF, Procedia CS 2025) and #21 (KBTU, Herald KBTU 2025) report **overlapping experiments** — both evaluate EfficientNetB0 frozen vs. fine-tuned on APTOS 2019 with nearly identical metrics. #19 is a conference paper; #21 is a journal version with expanded methodology. The dissertation should treat these as a single experimental thread with unified citation.
7. §6.2 (Modular Architecture with PACS and EHR Integration) was **added to the Section Map Key** to accommodate the system architecture content from #22 (NAN RK paper), which specifies DMP taxonomy, ER models, and FHIR/HL7 interoperability not previously covered.

**Impact of self-publications on coverage gaps:**

8. The 6 self-publications **resolved 10 previously critical gaps**: §2.3.2 (fine-tuning strategies), §2.4.1 (thermal-optical model), §3.1 (preprocessing pipeline — now 6 sources), §3.3 (transfer learning methodology), §4.1 (datasets), §4.2 (baseline vs enhanced), §4.3 (CLAHE optimization), §4.4 (TL strategy comparison), §6.1 (system requirements), §6.2 (new section).
9. **Remaining true gaps** reduced to 3: §1.1.1, §1.2.1, §2.1.3. These require **external (non-self) literature acquisition**.
10. **⚠️ Self-only coverage warning:** Sections §2.1.1, §2.4.1, §3.4, §4.2, §4.3, §6.1, §6.2 are now covered **only by self-publications**. These sections are vulnerable to examiner scrutiny — external supporting literature is strongly recommended.

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
