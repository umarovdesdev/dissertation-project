# LITERATURE INDEX
## External Source Corpus — Navigation Table

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Generated from:** Literature Cards in /LITERATURE/
**Total sources indexed:** 18

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

---

### Coverage Matrix

| Dissertation Section | Sources Covering It |
|---------------------|---------------------|
| §1.1.1 | ⚠️ GAP |
| §1.1.2 | #06, #10 |
| §1.2.1 | ⚠️ GAP |
| §1.2.2 | #05, #15, #17 |
| §1.3.1 | #01, #04, #05, #08, #09, #12, #15, #16, #18 |
| §1.3.2 | #02, #09, #12 |
| §1.4 | #02, #03, #07, #11, #12, #13, #14 |
| §1.5 | #17 ⚡ THIN |
| §2.1.1 | ⚠️ GAP |
| §2.1.2 | ⚠️ GAP |
| §2.1.3 | ⚠️ GAP |
| §2.2.1 | #08 ⚡ THIN |
| §2.2.2 | #01 ⚡ THIN |
| §2.2.3 | #01 ⚡ THIN |
| §2.3.1 | #04 ⚡ THIN |
| §2.3.2 | ⚠️ GAP |
| §2.4.1 | ⚠️ GAP |
| §3.1 | #02, #15 |
| §3.2 | #09 ⚡ THIN |
| §3.3 | ⚠️ GAP |
| §3.4 | ⚠️ GAP |
| §4.1 | #06, #10, #15 |
| §4.2 | ⚠️ GAP |
| §4.3 | ⚠️ GAP |
| §4.4 | ⚠️ GAP |
| §5.1 | #02, #04, #05, #07, #11, #12, #13, #16, #17 |
| §5.2 | #16, #17 |
| §5.3 | #02, #05, #07, #11, #12, #13, #14, #16 |
| §6.1 | ⚠️ GAP |
| §6.3 | #03, #11, #13, #14 |
| INTRO | #01, #06, #10, #12, #14 |

---

### Gaps Identified

**⚠️ GAP (0 sources):**
- §1.1.1 — Pathophysiology and Clinical Grading Systems
- §1.2.1 — Sources of Image Degradation in Clinical Practice
- §2.1.1 — Histogram Equalization and Adaptive Contrast Enhancement
- §2.1.2 — Formalization of CLAHE with Controllable Threshold Parameters
- §2.1.3 — Spatial Filtering and Noise Reduction Methods
- §2.3.2 — Frozen-Layer versus Progressive Fine-Tuning Strategies
- §2.4.1 — Coupled Thermal-Optical Model of Fundus Tissue Response
- §3.3 — Transfer Learning Methodology Using EfficientNetB0 and ResNet50
- §3.4 — Evaluation Framework and Performance Metrics
- §4.2 — Experiment 1: Baseline vs Enhanced CNN
- §4.3 — Experiment 2: CLAHE Threshold Optimization
- §4.4 — Experiment 3: Transfer Learning Strategy Comparison
- §6.1 — System Requirements and Design Principles

**⚡ THIN (1 source):**
- §1.5 — Formulation of Research Problem (#17)
- §2.2.1 — Convolution, Pooling, and Feature Extraction Operations (#08)
- §2.2.2 — Loss Functions and Optimization for Imbalanced Medical Datasets (#01)
- §2.2.3 — Regularization Techniques: Dropout, Batch Normalization, Data Augmentation (#01)
- §2.3.1 — Feature Transferability Across Visual Domains (#04)
- §3.2 — Design of Baseline and Enhanced CNN Architectures (#09)

---

### Notes

1. Sources #06 and #10 are **duplicate entries** for the same article (Porwal et al., 2018 — IDRiD dataset descriptor). Both literature cards contain identical content. Consider consolidating to a single entry.
2. Sources #11 and #13 are **duplicate entries** for the same article (Ting et al., 2017 — JAMA multiethnic DLS validation). Both literature cards contain the same study with minor formatting differences. Consider consolidating to a single entry.
3. Source #18 (González-Díaz et al., 2024) addresses **AMD, not diabetic retinopathy**. Its relevance to the dissertation is peripheral (ViT architecture comparison only).
4. Sections §2.x (mathematical foundations), §3.x (methodology), and §4.x (experiments) have the most severe coverage gaps, which is expected since these sections describe the candidate's own contributions rather than prior literature. However, §2.1.1–§2.1.3 (preprocessing theory) and §2.3.2 (fine-tuning strategies) would benefit from additional literature support.
5. Section §5.1 (Cross-Database Generalization Testing) has the strongest coverage with 9 sources.
