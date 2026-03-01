
# 1. Bibliographic Metadata

**Full citation (APA 7)**
Senapati, A., Tripathy, H. K., Sharma, V., & Gandomi, A. H. (2024). Artificial intelligence for diabetic retinopathy detection: A systematic review. *Informatics in Medicine Unlocked, 45*, 101445. [https://doi.org/10.1016/j.imu.2024.101445](https://doi.org/10.1016/j.imu.2024.101445)

**DOI:** 10.1016/j.imu.2024.101445
**Journal:** *Informatics in Medicine Unlocked* (Elsevier)
**Year:** 2024
**Publication type:** Systematic literature review (with quantitative bibliometric analysis; PRISMA-based)
**Research domain classification:** Medical AI; Diabetic Retinopathy; ML/DL-based fundus image analysis; bibliometric review

---

# 2. Study Type Classification

Applicable classifications:

* **Systematic review** ✔
* **Meta-analysis (bibliometric citation analysis only; not pooled diagnostic metrics)** ✔

Not applicable:

* External validation study ✘
* Cross-dataset validation ✘
* EyePACS benchmarking ✘
* Messidor benchmarking ✘
* IDRiD lesion-level study ✘
* Vision Transformer application ✘
* CNN-based classification study ✘
* Clinical prospective validation ✘

**Justification:**
The article conducts a PRISMA-based systematic review (2016–2023) of ML/DL methods for DR detection. It does not train or validate a new model.

---

# 3. Research Problem

**Primary problem addressed:**
To systematically analyze state-of-the-art AI, ML, and DL methodologies for diabetic retinopathy detection and classification using fundus images, identify limitations, and outline research gaps.

**Problem dimensions explicitly discussed:**

* Generalization limitations
* Computational complexity
* Low early-stage detection accuracy
* Class imbalance
* Model interpretability
* Dataset diversity
* Lack of robust early-stage DR detection
* Need for scalable, cost-effective systems

**Not addressed experimentally:**
Architecture scaling experiments, deployment trials, prospective validation.

---

# 4. Datasets Used (Surveyed in Literature)

The paper does not train models. It reviews commonly used datasets.

| Dataset           | Public/Private | Sample Size            | Class Taxonomy | Train/Val/Test | External Dataset Used | Cross-dataset Testing |
| ----------------- | -------------- | ---------------------- | -------------- | -------------- | --------------------- | --------------------- |
| DDR               | Public         | 15,234 images          | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| STARE             | Public         | 415 images (715×590)   | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| MESSIDOR 2        | Public         | 1,310 images           | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| IDRiD             | Public         | 590 images (4193×2567) | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| Kaggle APTOS 2019 | Public         | 6,023 images           | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| MESSIDOR          | Public         | 1,600 images           | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| HRF               | Public         | 150 images (3425×2248) | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |
| Kaggle EyePACS    | Public         | 75,523 images          | [NOT REPORTED] | [NOT REPORTED] | No                    | No                    |

**Important:**
No cross-dataset validation analysis is performed in this paper.

---

# 5. Preprocessing Pipeline

The paper describes preprocessing conceptually (Figure 15–16).

Explicitly mentioned preprocessing steps:

* Resizing
* Cropping
* Normalization
* Data augmentation
* Noise reduction
* Image enhancement

Not reported:

* Exact resizing dimensions → **[NOT REPORTED]**
* CLAHE parameters → **[NOT REPORTED]**
* Color normalization protocol → **[NOT REPORTED]**
* Augmentation strategy details → **[NOT REPORTED]**
* Image quality filtering → **[NOT REPORTED]**
* Lesion enhancement method → **[NOT REPORTED]**

This is descriptive only (not implemented).

---

# 6. Model Architecture

No original architecture developed.

Architectures discussed in literature:

* CNN
* AlexNet
* VGG-16
* GoogLeNet
* ResNet
* EfficientNet
* Mask R–CNN
* Transfer learning
* Hybrid ML-DL models

Not reported (for this study):

* Input resolution → **[NOT REPORTED]**
* Loss function → **[NOT REPORTED]**
* Optimizer → **[NOT REPORTED]**
* Epochs → **[NOT REPORTED]**
* Hyperparameters → **[NOT REPORTED]**

---

# 7. Validation Design

Validation in this article:

* PRISMA-based article screening
* Inclusion/exclusion criteria
* Citation analysis
* Bibliometric quantitative analysis

Not performed:

* Internal model validation
* Cross-validation
* External validation
* Multi-center validation
* Prospective clinical validation

---

# 8. Performance Metrics

The paper describes standard metrics formulaically:

* Accuracy
* Sensitivity
* Specificity
* Precision
* Recall
* F1-score
* NPV
* AUC (discussed conceptually)

No pooled AUC or confidence intervals calculated.

No confusion matrices provided.

No statistical meta-analysis pooling.

---

# 9. Authors’ Claims

### Performance Claims

* Many existing DL models suffer from overfitting and computational complexity.
* Accuracy is often insufficient for early-stage DR detection.

### Generalization Claims

* Current models lack robustness across datasets.
* Need for scalable and generalizable frameworks.

### Clinical Applicability Claims

* Automated systems can reduce ophthalmologist workload.
* Early detection reduces risk of blindness.

### Superiority Claims

* No claim of new superior model.
* Claim of comprehensive review coverage.

---

# 10. Empirical Support Assessment

* No empirical model tested → generalization claims not directly validated.
* No pooled statistical meta-analysis performed.
* No confidence intervals reported.
* Dataset adequacy discussed descriptively only.
* Class imbalance acknowledged but not analyzed quantitatively.
* Statistical testing: Not performed.

Conclusion: Claims are narrative, not empirically validated in this study.

---

# 11. Internal Validity

Not applicable to experimental modeling.

Review validity considerations:

* PRISMA framework used.
* Inclusion criteria clearly defined.
* Timeframe: 2016–2023.

Potential limitations:

* Search strategy limited to specified keywords.
* No inter-rater agreement statistics reported.
* No risk-of-bias assessment tool described.

---

# 12. External Validity

* Cross-population transferability not empirically tested.
* Dataset portability discussed conceptually.
* Clinical feasibility discussed theoretically.
* Hardware constraints not analyzed.

---

# 13. Strengths

* PRISMA-based systematic methodology.
* Multi-database search (Scopus, WoS, PubMed, Google Scholar).
* Quantitative citation analysis.
* Thematic evolution analysis (2010–2023).
* Clear research question framework (RQ1–RQ5).
* Comprehensive dataset enumeration.

---

# 14. Limitations

### Explicit (stated by authors)

* Need for more robust early-stage detection systems.
* Existing methods suffer from overfitting and computational complexity.

### Implicit (methodological)

* No quantitative meta-analysis pooling.
* No bias assessment of included studies.
* No external validation benchmarking synthesis.
* No comparison between CNN vs ViT architectures.
* No cost-sensitive learning evaluation.

---

# 15. Relevance to Your Dissertation

### Preprocessing dominance hypothesis

Moderately relevant. Paper emphasizes preprocessing (enhancement, normalization, segmentation), supporting its importance.

### Cross-database validation

Weak. Cross-dataset validation not analyzed empirically.

### EyePACS/Messidor benchmarking

Descriptive only.

### Vision Transformer comparison

Not covered.

### Risk of contradiction

Low. The article supports need for robust preprocessing and generalization research.

---

# 16. Citation-Ready Statements

1. “Existing AI-based DR detection systems still suffer from computational complexity, class imbalance, and limited early-stage accuracy.” (p.1–2)

2. “PRISMA methodology was adopted for systematic identification and screening of relevant articles.” (p.6–7)

3. “The Kaggle EyePACS dataset includes 75,523 fundus images.” (p.13, Table 9)

4. “From 2022–2023, researchers explored transfer learning, Mask R–CNN, and advanced DL techniques.” (p.10, Table 6)

5. “Accuracy alone is insufficient; sensitivity, specificity, F1-score, and AUC are required for reliable evaluation.” (p.14)

---

# 17. Epistemic Classification

**Classification:** Methodological precedent / Foundational survey

**Justification:**
This article structures the landscape of DR AI research (2016–2023) but does not contribute new empirical validation or benchmarking.

---

# 18. Analytical Synthesis

This article carries moderate epistemic weight as a structured systematic survey of DR AI research. It does not provide empirical benchmarking or cross-dataset validation evidence, limiting its direct impact on model performance claims. However, it reinforces the need for robust early-stage detection, preprocessing enhancement, and improved generalization—elements aligned with your preprocessing-dominance thesis. It does not address Vision Transformers or transformer-era benchmarking explicitly, leaving that gap open for your contribution. It supports the argument that existing CNN-based methods remain computationally heavy and potentially overfitted. The absence of cross-dataset validation synthesis further strengthens the need for your dissertation’s benchmarking framework.

---

**End of Literature Card.**
