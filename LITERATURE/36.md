# 1. Bibliographic Metadata

**Full citation (APA 7)**
Arora, L., Singh, S. K., Kumar, S., Gupta, H., Alhalabi, W., Arya, V., Bansal, S., Chui, K. T., & Gupta, B. B. (2024). *Ensemble deep learning and EfficientNet for accurate diagnosis of diabetic retinopathy*. Scientific Reports, 14, 30554. [https://doi.org/10.1038/s41598-024-81132-4](https://doi.org/10.1038/s41598-024-81132-4)

**DOI:** [https://doi.org/10.1038/s41598-024-81132-4](https://doi.org/10.1038/s41598-024-81132-4)

**Journal:** Scientific Reports (Nature Portfolio)

**Year:** 2024

**Publication type:** Empirical study

**Research domain classification:** CNN-based diabetic retinopathy severity classification (fundus imaging)

---

# 2. Study Type Classification

* CNN-based classification study ✅
* External validation study ❌
* Cross-dataset validation ❌
* EyePACS benchmarking ❌
* Messidor benchmarking ❌
* IDRiD lesion-level study ❌
* Vision Transformer application ❌ (ViTs mentioned only in future work)
* Clinical prospective validation ❌

**Justification:**
Single-dataset, retrospective CNN-based five-class DR severity classification using Kaggle fundus images.

---

# 3. Research Problem

**Problem addressed:**
Improve diabetic retinopathy severity classification accuracy using EfficientNetB0 with compound scaling and CNN layering techniques.

**Related to:**

* Architecture scaling ✅
* Class imbalance handling ✅
* Computational efficiency vs. accuracy trade-off ✅
* Clinical deployment (discussion-level)

Not focused on:

* Lesion segmentation
* Cross-dataset generalization

---

# 4. Datasets Used

### Dataset: “Diabetic Retinopathy Resized Dataset” (Kaggle)

* Public dataset
* Total images: **35,108**
* Class taxonomy: **5-class ICDRDSS-based severity grading**

  * No DR: 25,802
  * Mild DR: 5,288
  * Moderate DR: 2,438
  * Severe DR: 708
  * Proliferative DR: 872

### Class balancing

* Undersampling performed using RandomUnderSampler
* Balanced dataset size: **3,704 images**
* Train: 2,963
* Validation: 741
* Test set: **[NOT REPORTED as independent hold-out set]**

### External dataset used?

No

### Cross-dataset testing?

No

---

# 5. Preprocessing Pipeline

* Resizing: **224×224 pixels**
* Normalization: pixel values scaled to [0,1]
* Data augmentation:

  * Random horizontal flips
  * Random rotations up to 0.1 radians
  * Random zoom up to 10%
* CLAHE: **[NOT REPORTED]**
* Color normalization: **[NOT REPORTED]**
* Image quality filtering: **[NOT REPORTED]**
* Lesion enhancement methods: **None reported**

---

# 6. Model Architecture

* Architecture: EfficientNetB0 (CNN)
* Pretraining: ImageNet
* Transfer learning: include_top=False; added custom dense layer
* Input resolution: 224×224×3
* Final layer: Dense(5) with softmax
* Total parameters: 4,049,571

  * Trainable: 4,007,548
* Loss: Sparse Categorical Cross-Entropy
* Optimizer: Adam
* Learning rate: 0.001
* Scheduler: LR reduced by 0.5 every 3 epochs
* Batch size: 32
* Epochs: 40

---

# 7. Validation Design

* Internal validation only
* No cross-validation
* No external validation
* No multi-center validation
* No prospective validation

Dataset split after undersampling: training and validation only.

---

# 8. Performance Metrics

Reported metrics:

### Average (with augmentation)

* Accuracy: **0.8653**
* Loss: **0.5663**
* 95% CI (accuracy): (0.8677, 0.8677)
* 95% CI (loss): (0.5529, 0.5529)

### Maximum training accuracy:

* 97.11% (with augmentation)
* 96.87% (without augmentation)

### Comparison (Luo et al.)

* Luo accuracy: 83.6%
* EfficientNet processing time: 1190 seconds
* Luo model processing time: 4778 seconds

### Not reported:

* AUC
* Sensitivity
* Specificity
* F1-score
* Cohen’s Kappa
* Confusion matrix
* Statistical hypothesis tests

---

# 9. Authors’ Claims

* EfficientNetB0 achieves high classification accuracy.
* Data augmentation improves generalization.
* Model is computationally efficient.
* Suitable for resource-limited environments.
* Outperforms Luo et al.’s CNN in accuracy and efficiency.

---

# 10. Empirical Support Assessment

* Generalization claims unsupported (no external validation).
* No cross-dataset testing.
* Confidence intervals reported but identical bounds suggest reporting artifact.
* Severe class imbalance addressed via undersampling.
* No AUC or class-wise metrics provided.
* No statistical significance testing reported.

Conclusion: Claims of robustness and generalization are weakly supported.

---

# 11. Internal Validity

* Overfitting risk: High (training accuracy ~97% vs. validation ~86%)
* Dataset leakage risk: Not explicitly addressed
* Undersampling reduces sample diversity
* Augmentation inflation risk present
* Metric reliability limited (accuracy only)
* CI reporting questionable (identical bounds)

---

# 12. External Validity

* No cross-population validation
* Single Kaggle dataset only
* Real-world imbalanced performance untested
* Hardware efficiency favorable (shorter runtime)

Clinical feasibility: Theoretical only.

---

# 13. Strengths

* Clear architectural specification
* Transparent hyperparameter reporting
* Explicit imbalance handling
* Computational cost comparison
* Pretrained backbone with transfer learning

---

# 14. Limitations

### Explicit (authors state):

* Dataset demographic bias
* Artificial balancing may distort real-world performance
* No testing on naturally imbalanced data

### Implicit:

* No external validation
* No AUC
* No class-wise sensitivity
* No lesion-level interpretability
* No statistical tests

---

# 15. Relevance to My Dissertation

* Weak relevance to preprocessing-dominance hypothesis (minimal preprocessing used)
* No cross-database validation → does not support generalization claims
* No EyePACS/Messidor benchmarking
* No Vision Transformer comparison
* Low risk of contradicting preprocessing-driven generalization thesis

---

# 16. Citation-Ready Statements

1. “EfficientNetB0 achieved an average accuracy of 0.8653 with data augmentation applied.” (p. 14)
2. “The model achieved a maximum accuracy of 97.11% after 40 epochs.” (p. 12)
3. “The dataset consisted of 35,108 retinal images classified into five severity categories.” (p. 11)
4. “Undersampling reduced the dataset to 3,704 balanced images.” (p. 11)
5. “EfficientNetB0 required 1190 seconds compared to 4778 seconds for Luo’s model.” (p. 12)

---

# 17. Epistemic Classification

**Classification:** Limited-scope study

**Justification:**
Single-dataset internal validation study without cross-dataset benchmarking or external validation. Moderate empirical weight.

---

# 18. Analytical Synthesis

This article represents a conventional transfer-learning application of EfficientNetB0 to five-class DR severity grading using a single Kaggle dataset. Its methodological scope is limited to internal validation following undersampling-based balancing. While it demonstrates reasonable internal performance (0.8653 accuracy), it does not establish cross-dataset robustness or real-world generalization. The absence of AUC, sensitivity, and class-wise metrics limits clinical interpretability. For a dissertation emphasizing preprocessing dominance and international benchmarking, this study provides limited epistemic weight. It neither strengthens nor refutes preprocessing-driven generalization hypotheses, as preprocessing methods are minimal and no cross-database testing is performed.

---

End of Literature Card.
