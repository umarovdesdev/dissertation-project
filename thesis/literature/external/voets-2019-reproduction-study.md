# 1. Bibliographic Metadata

**Full citation (APA 7)**
Voets, M., Møllersen, K., & Bongo, L. A. (2019). *Reproduction study using public data of: Development and validation of a deep learning algorithm for detection of diabetic retinopathy in retinal fundus photographs*. PLOS ONE, 14(6), e0217541. [https://doi.org/10.1371/journal.pone.0217541](https://doi.org/10.1371/journal.pone.0217541). 

**DOI**
10.1371/journal.pone.0217541. 

**Journal (+ publisher)**
PLOS ONE (PLOS). 

**Year**
2019. 

**Publication type**
Empirical reproduction study / reproducibility study. 

**Research domain classification**
Medical AI; diabetic retinopathy detection; deep learning; reproducibility and validation of CNN-based image classification. 

---

# 2. Study Type Classification

| Category                        | Status | Justification                                                                                                                   |
| ------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- |
| CNN-based classification study  | ✔      | Re-implemented and trained a deep learning algorithm for referable diabetic retinopathy detection using InceptionV3. (Methods)  |
| External validation study       | ✔      | Evaluated performance on independent EyePACS test data and Messidor-2. (Results)                                                |
| Cross-dataset validation        | ✔      | Trained on Kaggle EyePACS and evaluated on Messidor-2.                                                                          |
| EyePACS benchmarking            | ✔      | EyePACS test set used for evaluation.                                                                                           |
| Messidor benchmarking           | ✔      | Messidor-2 test set used for evaluation.                                                                                        |
| IDRiD lesion-level study        | ❌      | IDRiD is not used.                                                                                                              |
| Vision Transformer application  | ❌      | Only InceptionV3 is reported.                                                                                                   |
| Clinical prospective validation | ❌      | No prospective clinical deployment or prospective patient enrollment reported.                                                  |

---

# 3. Research Problem

**Specific problem addressed**

To determine whether the results reported by Gulshan et al. (JAMA 2016) for automated referable diabetic retinopathy detection can be reproduced using publicly available datasets and a re-implementation of the original method. (Introduction, Conclusion)  

**Problem categories**

* Generalization ✔
* Clinical applicability ✔
* Preprocessing ✔
* Reproducibility / replication ✔
* Dataset quality and labeling quality ✔

**Not explicitly focused on**

* Lesion segmentation
* Explainability
* Attention maps
* Grad-CAM
* Vision Transformers
* Architecture scaling studies
* Device-specific adaptation methods
* Domain adaptation methods
* Multi-class DR grading optimization

All are [NOT REPORTED] as study objectives.

---

# 4. Datasets Used

| Dataset        | Public/Private | Sample Size                                              | Task                | Train/Val/Test                                 | External Dataset | Cross-Dataset Testing |
| -------------- | -------------- | -------------------------------------------------------- | ------------------- | ---------------------------------------------- | ---------------- | --------------------- |
| Kaggle EyePACS | Public         | 88,702 images total; 57,146 train+validation; 8,790 test | Binary referable DR | 80/20 split within 57,146; separate 8,790 test | No               | Source dataset        |
| Messidor-2     | Public         | 1,748 images                                             | Binary referable DR | Test only                                      | Yes              | Yes                   |

Source: Data Sets section. 

**Class taxonomy**

* Referable diabetic retinopathy (moderate-or-worse DR). 
* Binary classification output. 

**Class balancing**

Authors state that the EyePACS subset size was chosen to maintain the same binary rDR balance as the original study. 

**External dataset used**

Yes — Messidor-2. 

---

# 5. Preprocessing Pipeline

| Component                            | Reported Information                                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Resizing/resolution                  | Images resized so each image had height and width of 299 pixels with fundus centered.                  |
| Normalization                        | Images normalized to [-1,1].                                                                           |
| Data augmentation                    | Same augmentation settings as reported later by Krause et al. (2017). Specific operations not listed.  |
| CLAHE                                | [NOT REPORTED]                                                                                         |
| Color normalization                  | [NOT REPORTED]                                                                                         |
| Illumination / flat-field correction | [NOT REPORTED]                                                                                         |
| FOV crop                             | Fundus center and radius detected; image centered and resized.                                         |
| FOV mask                             | [NOT REPORTED]                                                                                         |
| Image quality filtering              | Images graded for gradability; experiments conducted with gradable-only training.                      |
| Lesion enhancement                   | [NOT REPORTED]                                                                                         |

---

# 6. Model Architecture

| Item                       | Description                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------ |
| Architecture               | InceptionV3.                                                                                     |
| Pretraining source         | ImageNet.                                                                                        |
| Transfer learning protocol | Pre-initialized using ImageNet-trained weights.                                                  |
| Input resolution           | 299×299.                                                                                         |
| Final layer                | [NOT REPORTED]                                                                                   |
| Parameter count            | [NOT REPORTED]                                                                                   |
| Loss function              | [NOT REPORTED]                                                                                   |
| Optimizer                  | RMSProp.                                                                                         |
| Learning rate              | 0.001.                                                                                           |
| Learning-rate scheduler    | Learning rate adjusted during validation in original work; implementation details not reported.  |
| Weight decay               | 4 × 10⁻⁵.                                                                                        |
| Batch normalization        | Applied after each convolutional layer.                                                          |
| Batch size                 | [NOT REPORTED]                                                                                   |
| Epochs                     | [NOT REPORTED]                                                                                   |
| Early stopping             | Yes; validation AUC with patience=10 epochs.                                                     |
| Ensemble                   | Yes; 10-network ensemble.                                                                        |

---

# 7. Validation Design

**Validation design**

* Internal train/validation split (80/20). 
* Independent EyePACS test set. 
* External validation on Messidor-2. 

**Confidence intervals reported?**

Yes. AUC confidence intervals reported. 

**Statistical tests reported?**

No formal hypothesis testing reported. [NOT REPORTED]

**Overfitting addressed?**

Yes.

* Early stopping based on validation AUC. 
* Patience parameter. 
* Ensemble learning. 

---

# 8. Performance Metrics

## Kaggle EyePACS Test Set

| Metric                                       | Value                      |
| -------------------------------------------- | -------------------------- |
| AUC                                          | 0.951 (95% CI 0.947–0.956) |
| High-sensitivity operating point sensitivity | 90.6%                      |
| High-sensitivity operating point specificity | 84.7%                      |
| High-specificity operating point sensitivity | 83.6%                      |
| High-specificity operating point specificity | 92.0%                      |

(Table 1; Results) 

## Messidor-2

| Metric                                       | Value                      |
| -------------------------------------------- | -------------------------- |
| AUC                                          | 0.853 (95% CI 0.835–0.871) |
| High-sensitivity operating point sensitivity | 81.8%                      |
| High-sensitivity operating point specificity | 71.2%                      |
| High-specificity operating point sensitivity | 68.7%                      |
| High-specificity operating point specificity | 88.5%                      |

(Table 1; Results) 

## Metrics Not Reported

* Accuracy
* F1-score
* Precision
* Recall beyond operating points
* Cohen's Kappa
* Quadratic Weighted Kappa (QWK)
* Calibration metrics
* Brier score results
* Confusion matrix counts

---

# 9. Authors' Claims

* The JAMA 2016 study could not be successfully reproduced using publicly available data. 
* Differences may stem from dataset quality, grading procedures, and availability of multiple expert grades. 
* Reproducing deep-learning medical imaging studies is challenging when data and code are unavailable. 
* Reporting of preprocessing details and hyperparameters is critical for reproducibility. 
* Their findings do not invalidate the broader conclusion that deep learning can detect diabetic retinopathy. 

---

# 10. Empirical Support Assessment

| Claim                                                | Empirical Support                                                                                      |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Original results could not be reproduced             | Strongly supported by reported AUC differences on both EyePACS and Messidor-2.                         |
| Public-data reproduction performs worse              | Supported by direct comparison with original reported metrics.                                         |
| Multiple expert grades may explain discrepancy       | Plausible but not directly tested in this study.                                                       |
| Data quality contributes to performance differences  | Plausible; not experimentally isolated.                                                                |
| Reproducibility requires hyperparameter transparency | Supported by authors' experience retraining after hyperparameter release, but not formally quantified. |

**External validation robustness:** Moderate.

**Confidence intervals:** Present.

**Class imbalance handling:** Limited reporting.

**Statistical testing:** Not reported.

**Generalization verdict:** The study provides evidence of reduced cross-dataset performance and reproduction difficulty, but does not experimentally isolate causes of performance degradation.

---

# 11. Internal Validity

* Early stopping used to mitigate overfitting. 
* Ensemble averaging used. 
* Potential label-quality limitations due to single-grade labels acknowledged. 
* Potential preprocessing–architecture confounding exists because preprocessing and hyperparameter settings changed together relative to original study.
* Data-leakage issues are not discussed. [NOT REPORTED]
* Class balancing methodology is only partially described. 

---

# 12. External Validity

* Training data originate primarily from one public EyePACS source. 
* External evaluation performed on Messidor-2. 
* Authors explicitly discuss possible overfitting to camera and patient characteristics. 
* No prospective clinical deployment.
* Hardware dependency not reported.

---

# 13. Strengths

* Publicly reproducible study design. 
* External validation on Messidor-2. 
* Confidence intervals reported for AUC. 
* Uses same base architecture (InceptionV3) as original benchmark. 
* Explicit discussion of reproducibility limitations. 

---

# 14. Limitations

### Explicit (authors state)

* Different datasets from original study. 
* Only one DR grade per image. 
* No macular edema labels. 
* Messidor-2 grades were per-patient rather than per-image. 
* Potential overfitting to EyePACS source characteristics. 

### Implicit (observed)

* No statistical significance testing.
* No calibration analysis.
* No explainability assessment.
* No lesion-level validation.
* No systematic ablation of preprocessing choices.
* No comparison with alternative architectures.

---

# 15. Relevance to My Dissertation

| Dissertation Axis                                 | Relevance  | Notes                                                                                                                                     |
| ------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Preprocessing-dominance hypothesis                | Supporting | Shows preprocessing description is critical for reproducibility, but does not quantify preprocessing contribution.                        |
| Cross-database generalization                     | Core       | Direct EyePACS→Messidor-2 evaluation and discussion of dataset shift.                                                                     |
| CNN vs ViT comparison                             | Peripheral | No ViT models.                                                                                                                            |
| EyePACS benchmarking                              | Core       | Major dataset used.                                                                                                                       |
| Messidor benchmarking                             | Core       | External benchmark used.                                                                                                                  |
| IDRiD benchmarking                                | Peripheral | Not included.                                                                                                                             |
| APTOS benchmarking                                | Peripheral | Not included.                                                                                                                             |
| Explainability (Grad-CAM IoU/ALO)                 | Peripheral | Not addressed.                                                                                                                            |
| Device domain shift / clinical degradation        | Supporting | Authors discuss camera and patient characteristic shifts affecting AUC.                                                                   |
| Risk of contradicting preprocessing-driven thesis | Low        | Study emphasizes data quality, grading quality, preprocessing transparency, and dataset differences rather than architecture superiority. |

---

# 16. Citation-Ready Statements

1. “We were not able to reproduce the original study’s results with publicly available data.” (Abstract, p.1) 

2. “Our algorithm’s AUC for detecting rDR for our EyePACS and Messidor-2 test sets were 0.951 and 0.853, respectively.” (Introduction, p.2) 

3. “The main challenge in this reproduction study was to find optimal hyper-parameters for our data.” (Discussion: Hyper-parameters, p.8) 

4. “Training on our single Kaggle EyePACS data set may result in overfitting to the cameras and patient characteristics in that data set.” (Discussion, p.8) 

5. “We therefore recommend the following improvements to the reporting of deep learning methods: (i) use public data or provide detailed data description, (ii) publish source code or all details regarding the pre-processing of the data, and (iii) all hyper-parameters.” (Conclusion, p.9) 

---

# 17. Epistemic Classification

**High-impact benchmark**

**Justification:**
The study directly evaluates reproducibility of one of the most influential diabetic retinopathy deep-learning benchmarks (Gulshan et al., 2016), performs external validation on Messidor-2, reports quantitative performance gaps, and discusses methodological factors affecting reproducibility and generalization. Its primary contribution is benchmarking reproducibility rather than proposing a new architecture.  

---

# 18. Analytical Synthesis

This study is highly relevant to dissertation arguments concerning cross-database generalization and the importance of preprocessing and data standardization. The authors reproduced a landmark DR detection system using public data and obtained substantially lower performance than originally reported, particularly on Messidor-2 external validation. The work does not demonstrate that preprocessing alone determines performance; however, it repeatedly highlights that preprocessing details, hyperparameters, grading protocols, and dataset characteristics materially affect reproducibility. The discussion of camera-specific and patient-specific overfitting directly supports concerns regarding domain shift and external validity. Because the study uses a single CNN family (InceptionV3), it does not inform CNN-versus-ViT comparisons or explainability analyses. Its epistemic value lies primarily in showing that benchmark performance may degrade considerably when datasets, grading procedures, and preprocessing pipelines differ. For a dissertation emphasizing robust preprocessing as a component of the model itself, this paper provides supporting evidence that data preparation and standardization cannot be treated as incidental implementation details. 

End of Literature Card.
