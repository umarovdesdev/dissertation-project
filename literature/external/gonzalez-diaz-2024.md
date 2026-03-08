# Literature Card: González-Díaz et al. (2024) — ViT for AMD Detection

---

## 1. Bibliographic Metadata

- **Full citation (APA 7):** González-Díaz, J. E., Reyes-Delgado, A. J., Sánchez-Cervantes, J. L., Mejia-Miranda, J., Alor-Hernández, G., & Rodríguez-Mazahua, L. (2024). Use of Vision Transformers in Ophthalmology for Early Detection of Age-Related Macular Degeneration (AMD): A Comparative Analysis. *Preprints.org*, 20241101740. https://doi.org/10.20944/preprints202411.1740.v1
- **DOI:** 10.20944/preprints202411.1740.v1
- **Journal / Conference:** Preprints.org (preprint server; **NOT peer-reviewed**)
- **Year:** 2024
- **Publication type:** Empirical comparative study (preprint)
- **Research domain classification:** Vision Transformer application for ophthalmic disease classification (AMD); comparative architecture benchmarking on fundus images

---

## 2. Study Type Classification

- **Vision Transformer application** — Evaluates five ViT architectures (Classic ViT, Swin Transformer, BEiT, Swin Transformer V2, SwiftFormer) for dry AMD grading.
- **CNN-based classification study** — While exclusively ViT-focused, the study positions itself within the broader ViT-vs-CNN literature and benchmarks ViT variants against each other.
- **Benchmark study (limited scope)** — Compares architectures on a single small private/curated dataset without external validation.

**Justification:** The study trains and evaluates five ViT models on a single curated dataset with a 4-class AMD grading scheme. No external datasets are used for validation. No cross-dataset testing is performed. This is an internal benchmarking study of ViT architectures, not an external validation or clinical validation study.

---

## 3. Research Problem

- **Specific problem addressed:** Comparative evaluation of five Vision Transformer architectures for detecting and grading dry AMD from fundus images, assessing both classification performance and computational efficiency.
- **Relevance to:**
  - **Architecture scaling:** Yes — compares lightweight (SwiftFormer, 50M params) versus heavyweight (ViT/BEiT, ~86–88M params) architectures.
  - **Generalization:** Claimed but weakly supported — no external dataset testing.
  - **Clinical deployment:** Partially — computational efficiency metrics (inference time, memory, energy) are reported, and future telemedicine platform is proposed.
  - **Preprocessing:** Minimally addressed; augmentation described, but no systematic preprocessing pipeline evaluation.
  - **Lesion detection:** Not applicable — image-level classification only, no lesion-level segmentation or detection.

---

## 4. Datasets Used

| Attribute | Details |
|---|---|
| **Name** | Curated dataset from Baidu Research open-access dataset and "ARMD curated dataset 2023" (Kaggle, Mujib) |
| **Public / Private** | Sources are public; final curated dataset appears study-specific |
| **Sample size** | 305 original fundus images → augmented to 911 total images |
| **Class taxonomy** | 4-class: No AMD, Mild, Moderate, Advanced |
| **Train/validation/test split** | 70/15/15 ratio; post-augmentation: 819 training, 46 validation, 46 test |
| **External dataset used?** | No |
| **Cross-dataset testing performed?** | No |

**Critical note:** The test set contains only **46 images** (~11–12 per class assuming balance). Per-class metrics are based on approximately 5 images per class in test and validation sets (the article references 5 images per class for "No AMD" and "Advanced" based on confusion matrix counts). This is an extremely small evaluation sample.

---

## 5. Preprocessing Pipeline

- **Resizing:** [NOT REPORTED explicitly; input resolution not stated beyond model defaults]
- **Cropping:** [NOT REPORTED]
- **Normalization:** [NOT REPORTED]
- **CLAHE:** [NOT REPORTED]
- **Color normalization:** [NOT REPORTED]
- **Augmentation:** Yes — random transformations including size changes, rotations between -5° and 5°, brightness and contrast modifications. Augmentations were kept subtle; exceeding 10 augmented versions per original image was found to introduce noise. Applied only to the training set.
- **Image quality filtering:** Medical experts reviewed and validated images for clinical relevance and accuracy.
- **Lesion enhancement methods:** [NOT REPORTED]

**Assessment:** The preprocessing pipeline is severely underspecified. No details on resizing, normalization, or standard ophthalmological preprocessing (e.g., CLAHE, green channel extraction) are provided. This is a significant methodological gap.

---

## 6. Model Architecture

| Attribute | ViT | Swin Transformer | BEiT | Swin Transformer V2 | SwiftFormer |
|---|---|---|---|---|---|
| **Architecture type** | Vision Transformer | Shifted Window Transformer | Bidirectional Encoder ViT | Swin V2 | Efficient Additive Attention ViT |
| **Parameters** | 86.39M | 27.52M | 85.76M | 27.58M | 23.14M |
| **FLOPs** | 17.58 GFLOPs | 4.51 GFLOPs | 17.58 GFLOPs | 5.96 GFLOPs | 0.61 GFLOPs |
| **Pretraining source** | Supervised (ImageNet implied) | Supervised (ImageNet implied) | Auto-supervised | Supervised (ImageNet implied) | Efficient attention |
| **Input resolution** | [NOT REPORTED explicitly] | [NOT REPORTED explicitly] | [NOT REPORTED explicitly] | [NOT REPORTED explicitly] | [NOT REPORTED explicitly] |

**Training hyperparameters (all models):**

- **Optimizer:** Adam (betas=0.9, 0.999; epsilon=1e-08)
- **Epochs:** 80
- **Batch size:** Train=32, Eval=32, Gradient Accumulation Steps=4, Total Train Batch Size=128
- **Seed:** 42
- **LR Scheduler:** Linear
- **Learning rates:** ViT & Swin T: 5.5e-05; BEiT & Swin T V2: 4e-05; SwiftFormer: 3e-4
- **Warmup ratio:** ViT & Swin T: 0.05; BEiT & Swin T V2: 0.01; SwiftFormer: 0.15
- **Loss function:** [NOT REPORTED]

---

## 7. Validation Design

- **Internal validation only?** Yes
- **Cross-validation?** No
- **External validation?** No
- **Prospective validation?** No
- **Multi-center validation?** No

**Assessment:** The study uses a single train/validation/test split (70/15/15) from one curated dataset. No k-fold cross-validation, no external dataset testing. The validation set (46 images) was used for hyperparameter tuning; the test set (46 images) was used for final evaluation. This is the weakest possible validation design for a classification study.

---

## 8. Performance Metrics

### Overall Accuracy (Table 4)

| Model | Validation | Testing | Average |
|---|---|---|---|
| ViT | 0.8695 | 0.8043 | 0.8369 |
| Swin Transformer | 0.7826 | 0.7391 | 0.76085 |
| BEiT | 0.8478 | 0.8043 | 0.82605 |
| Swin Transformer V2 | 0.7608 | 0.7826 | 0.7717 |
| SwiftFormer | 0.8478 | 0.7826 | 0.8152 |

### AUC-ROC (Micro-average, OvR strategy)

| Model | Validation | Testing |
|---|---|---|
| ViT | 0.96 | 0.93 |
| Swin Transformer | 0.93 | 0.91 |
| BEiT | 0.92 | 0.94 |
| Swin Transformer V2 | 0.90 | 0.90 |
| SwiftFormer | 0.92 | 0.91 |

### Class-level AUC (from ROC curve figures)

| Model | Class | Validation AUC | Testing AUC |
|---|---|---|---|
| ViT | Advanced | 0.99 | 0.93 |
| ViT | Mild | 0.96 | 0.91 |
| ViT | Moderate | 0.95 | 0.95 |
| ViT | No AMD | 0.85 | 0.91 |
| BEiT | Advanced | 1.00 | 0.95 |
| BEiT | Mild | 0.91 | 0.92 |
| BEiT | Moderate | 0.92 | 0.96 |
| BEiT | No AMD | 0.81 | 0.82 |
| Swin T V2 | Advanced | 0.96 | 0.86 |
| SwiftFormer | Advanced | 0.98 | 0.97 |
| SwiftFormer | Moderate | 0.97 | 0.87 |

### F1-Score by class (Average of Validation and Testing — from Table 7)

| Model | No AMD | Mild | Moderate | Advanced |
|---|---|---|---|---|
| ViT | 0.7083 | 0.8547 | 0.8500 | 0.8194 |
| Swin Transformer | 0.5357 | 0.8222 | 0.7813 | 0.5357 |
| BEiT | 0.5857 | 0.8534 | 0.8411 | 0.8636 |
| Swin Transformer V2 | 0.4857 | 0.8050 | 0.8286 | 0.6857 |
| SwiftFormer | 0.5714 | 0.8494 | 0.8333 | 0.7917 |

### Computational Efficiency (Table 9)

| Model | Training Time (min) | Inference Time (ms/img) | Memory (GB) | Parameters (M) | FLOPs (GFLOPs) | Energy (W) |
|---|---|---|---|---|---|---|
| ViT | 17.38 | 14.31 | 7.53 | 86.39 | 17.58 | 175.82 |
| Swin Transformer | 9.92 | 23.23 | 5.52 | 27.52 | 4.51 | 169.78 |
| BEiT | 17.55 | 14.62 | 7.70 | 85.76 | 17.58 | 177.56 |
| Swin Transformer V2 | 13.45 | 37.14 | 7.37 | 27.58 | 5.96 | 174.04 |
| SwiftFormer | 4.60 | 14.19 | 3.86 | 23.14 | 0.61 | 131.46 |

- **Sensitivity/Specificity (overall):** [NOT REPORTED as aggregate; only class-level recall provided]
- **Cohen's Kappa:** [NOT REPORTED]
- **Confidence intervals:** [NOT REPORTED]
- **Statistical tests:** [NOT REPORTED]

---

## 9. Authors' Claims

1. **Performance claims:** Classic ViT and BEiT achieved the best overall performance, with accuracy of 83.69% and 82.60% and F1-scores of 85.47% and 86.36%, respectively.
2. **Computational efficiency claims:** SwiftFormer excelled in computational efficiency with inference time of 14.19 ms/img, memory consumption of 3.86 GB, and energy efficiency of 131.46 W.
3. **Generalization claims:** The study claims to evaluate "generalization capabilities" of ViT models for AMD detection; Classic ViT is described as demonstrating "consistency and reliability in controlled and real-world environments."
4. **Clinical applicability claims:** The study claims to provide "evidence-based guidance for selecting ViT models for early detection of AMD, streamlining clinical diagnosis, and improving patient outcomes."
5. **Superiority claims:** The study claims ViT architectures have "significant potential" for AMD detection and that combining different models "may be an effective strategy for improving diagnostic accuracy in clinical practice."

---

## 10. Empirical Support Assessment

- **Does data support generalization claims?** **No.** No external validation, no cross-dataset testing, no cross-population evaluation. All evaluation is on a single split from one curated dataset. The term "generalization" is used loosely to describe validation-to-test consistency, which is not generalization in the standard machine learning sense.
- **Is external validation robust?** **Not applicable** — no external validation was performed.
- **Are confidence intervals reported?** **No.** No confidence intervals, no standard deviations, no bootstrapping.
- **Is dataset size adequate?** **No.** The original dataset of 305 images is extremely small. The test set of 46 images (~5 per class for minority classes) makes per-class metrics highly unstable. A single misclassification changes recall by 20% in a 5-sample class.
- **Is class imbalance addressed?** **Partially.** The authors mention balanced representation but do not report exact class distributions. Based on confusion matrices, the "No AMD" and "Advanced" classes appear to have approximately 5 images each in the test set, while "Mild" and "Moderate" have approximately 21 and 15 respectively.
- **Is statistical testing adequate?** **No.** No statistical tests are reported. No significance testing between models. No paired comparisons. Performance differences between models may be entirely within noise given the tiny test set.

---

## 11. Internal Validity

- **Overfitting risk:** **HIGH.** Training on 819 images (many augmented from 214 originals) with models containing 23–88 million parameters creates severe overfitting risk. The validation set of 46 images provides minimal overfitting detection capacity.
- **Dataset leakage risk:** **MODERATE.** The augmentation was applied before splitting (the text states augmentation was applied to the training set of 214 images, expanding it to 819, with 46 validation and 46 test). If augmented versions of the same original image appear in both training and validation/test sets, this constitutes data leakage. The description is ambiguous — the text states the 70-15-15 split was done first, then augmentation was applied to the training set. If this sequence was followed correctly, leakage risk is lower.
- **Confounders:** Dataset sourced from two different databases (Baidu Research and Kaggle ARMD dataset); no discussion of domain differences, image quality variation, or acquisition protocol differences between sources.
- **Augmentation inflation risk:** **HIGH.** Augmenting 214 images to 819 (approximately 3.8× increase) with subtle transformations means the model sees highly correlated training samples. This inflates apparent training data diversity without genuine sample independence.
- **Metric reliability:** **LOW.** With ~5 test samples per minority class, all per-class metrics have extremely high variance. A single misclassification shifts recall/precision by 20%.
- **Formula correctness:** The provided formulas for precision, recall, F1-score, and accuracy are standard and correct.

---

## 12. External Validity

- **Cross-population transferability:** **Cannot be assessed.** No external validation. Dataset sources (Baidu Research — likely Chinese population; Kaggle ARMD dataset — population unknown) do not represent global clinical diversity.
- **Dataset portability:** **Not demonstrated.** No cross-dataset testing.
- **Clinical feasibility:** Computational efficiency metrics are provided (inference time 14–37 ms/img), which is relevant for deployment. However, accuracy levels (74–84%) on a 4-class problem with a tiny test set do not meet clinical deployment thresholds.
- **Hardware constraints:** Training performed on AMD Ryzen 5 3500X CPU, NVIDIA RTX 3070 GPU (8 GB), 16 GB DDR4 RAM. SwiftFormer requires only 3.86 GB memory, suggesting mobile/edge deployment potential.

---

## 13. Strengths

1. **Comprehensive ViT comparison:** Evaluates five distinct ViT architectures (Classic ViT, Swin Transformer, BEiT, Swin Transformer V2, SwiftFormer) in a controlled comparative framework on the same dataset.
2. **Computational efficiency reporting:** Provides detailed computational metrics (training time, inference time, memory consumption, parameters, FLOPs, energy efficiency) alongside classification performance — a dimension often omitted in medical imaging studies.
3. **Multi-class grading:** Addresses 4-stage AMD grading (No AMD, Mild, Moderate, Advanced) rather than binary classification, which is more clinically relevant.
4. **Per-class analysis:** Reports precision, recall, and F1-score for each individual class and for both validation and test sets, enabling granular performance assessment.
5. **ROC analysis with OvR strategy:** Provides per-class AUC-ROC using One-vs-Rest binarization with micro-averaging.

---

## 14. Limitations

### Explicit (stated by authors)
- Small sample size and class imbalance acknowledged as contributing to margin of error.
- Models face challenges in classifying the "No AMD" class accurately.
- Further optimization needed to improve specificity without compromising sensitivity.
- Need for larger, more diverse datasets to overcome limitations.

### Implicit (methodological)
1. **Critically small dataset:** 305 original images, 46-image test set (~5 per minority class) — below any reasonable minimum for reliable deep learning evaluation.
2. **No external validation:** All evaluation is on a single internal split; no cross-dataset testing.
3. **No confidence intervals or statistical tests:** Performance differences between models cannot be assessed for significance.
4. **No cross-validation:** Single train/val/test split with no k-fold or repeated holdout.
5. **Preprocessing pipeline unspecified:** No information on resizing, normalization, or standard ophthalmological preprocessing.
6. **Input resolution not reported:** Critical parameter for ViT architectures is missing.
7. **Loss function not reported.**
8. **Not peer-reviewed:** Published as a preprint on Preprints.org.
9. **Augmentation details insufficient:** Exact augmentation ratios per class not reported; risk of inflated training diversity.
10. **No comparison with CNN baselines:** Despite extensive related work discussing ViT-vs-CNN, no CNN baseline is included in the actual experiments.
11. **Transfer learning protocol underspecified:** Pretraining sources are listed generically (Table 2 mentions "supervised pretraining" and "auto-supervised pretraining") but exact pretrained checkpoint identifiers and fine-tuning protocols are not detailed.
12. **AMD focus is dry AMD only:** Wet AMD is excluded without justification for scope limitation.
13. **Averaged validation/testing metrics reported as primary results** — averaging validation and test performance conflates model selection and evaluation.

---

## 15. Relevance to My Dissertation

- **Relevance to preprocessing dominance hypothesis:** **LOW.** The study does not systematically evaluate preprocessing impact. Preprocessing is underspecified. Cannot be used to support or refute preprocessing dominance arguments.
- **Relevance to cross-database validation:** **LOW.** No cross-database testing is performed. The study is explicitly single-dataset internal evaluation only.
- **Relevance to EyePACS/Messidor benchmarking:** **NONE.** Study addresses AMD (not diabetic retinopathy) and does not use EyePACS, Messidor, or any standard DR benchmarking datasets.
- **Relevance to Vision Transformer comparison:** **MODERATE.** The study provides a useful catalog of ViT architectures applied to ophthalmic fundus image classification, with computational efficiency data. However, the weak validation design limits the evidential weight of the performance comparisons.
- **Risk of contradiction:** **LOW.** The study's findings are too weakly supported to contradict robust evidence. Its modest accuracy values (74–84%) on a tiny dataset do not challenge well-validated CNN or ViT results on standard benchmarks.

---

## 16. Citation-Ready Statements

1. González-Díaz et al. (2024) compared five Vision Transformer architectures for dry AMD detection from fundus images, reporting that Classic ViT achieved the highest average accuracy (83.69%) while BEiT achieved the highest F1-score (86.36%) on a 4-class grading task (p. 2, Tables 4 and 7).

2. Among the five ViT architectures evaluated, SwiftFormer demonstrated the highest computational efficiency with an inference time of 14.19 ms/img, memory consumption of 3.86 GB, and 0.61 GFLOPs, compared to 14.31 ms/img, 7.53 GB, and 17.58 GFLOPs for Classic ViT (González-Díaz et al., 2024, Table 9).

3. All five ViT models achieved micro-average AUC-ROC values exceeding 0.90 on both validation and test sets for 4-class AMD grading, with Classic ViT achieving the highest test AUC of 0.93 (González-Díaz et al., 2024, Section 5.5).

4. González-Díaz et al. (2024) reported that all evaluated ViT architectures showed notably poor performance on the "No AMD" class, with F1-scores ranging from 0.4857 (Swin Transformer V2) to 0.7083 (Classic ViT), suggesting challenges in distinguishing normal fundus images from early-stage AMD (Table 7).

5. The study was limited by a dataset of only 305 original fundus images augmented to 911, with a test set of 46 images, and no external validation or statistical significance testing was performed (González-Díaz et al., 2024, Section 4.1).

---

## 17. Epistemic Classification

**Classification: Limited-scope study**

**Justification:** This is a non-peer-reviewed preprint evaluating ViT architectures on an extremely small dataset (305 images, 46-image test set) without external validation, confidence intervals, statistical testing, or cross-dataset evaluation. While the computational efficiency analysis provides useful descriptive data, the classification performance results carry minimal evidential weight due to the critically small sample size and absence of standard validation practices. The study cannot serve as a benchmark, foundational reference, or high-impact evidence. It may be cited peripherally as an example of ViT architecture comparison in ophthalmic imaging, with explicit caveats about its methodological limitations.

---

## 18. Analytical Synthesis

This preprint by González-Díaz et al. (2024) carries minimal epistemic weight for dissertation positioning due to its non-peer-reviewed status, critically small dataset (305 original images), and absence of external validation or statistical rigor. The study's primary value lies in its systematic comparison of five distinct ViT architectures with computational efficiency metrics, which provides a useful descriptive catalog of ViT variants in the ophthalmic imaging space. However, the performance results (74–84% accuracy on 46-image test sets) cannot be considered reliable evidence for any architecture's superiority. The study does not address preprocessing in any systematic way, making it irrelevant to the preprocessing-dominance hypothesis. It provides no cross-dataset evidence and therefore cannot contribute to arguments about generalization or dataset portability. For the dissertation, this paper may be cited only as a peripheral reference illustrating the growing interest in applying ViT architectures to ophthalmic disease detection, with explicit notation that it addresses AMD rather than diabetic retinopathy and suffers from fundamental validation deficiencies. The computational efficiency comparison (particularly SwiftFormer's 0.61 GFLOPs vs. ViT/BEiT's 17.58 GFLOPs) may be tangentially relevant if the dissertation discusses deployment considerations for transformer-based models.

---

*Literature Card generated: February 2026*
*Disease focus: Age-Related Macular Degeneration (not Diabetic Retinopathy)*
*Status: NOT PEER-REVIEWED preprint*
