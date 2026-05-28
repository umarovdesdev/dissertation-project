# Literature Card: Pratt et al. (2016)

---

# 1. Bibliographic Metadata

- **Full citation (APA 7):** Pratt, H., Coenen, F., Broadbent, D. M., Harding, S. P., & Zheng, Y. (2016). Convolutional neural networks for diabetic retinopathy. *Procedia Computer Science, 90*, 200–205.
- **DOI:** 10.1016/j.procs.2016.07.014
- **Journal / Conference:** *Procedia Computer Science* — International Conference on Medical Imaging Understanding and Analysis 2016 (MIUA 2016), Loughborough, UK, 6–8 July 2016
- **Year:** 2016
- **Publication type:** Empirical (conference paper)
- **Research domain classification:** Deep learning for medical image classification; automated diabetic retinopathy grading; CNN-based multi-class fundus image analysis

---

# 2. Study Type Classification

- **CNN-based classification study** ✓
- **EyePACS benchmarking** ✓ (Kaggle DR dataset, which is the EyePACS-sourced competition dataset)

**Justification:** The study proposes and evaluates a custom CNN trained and validated exclusively on the Kaggle DR dataset (EyePACS-derived). No external dataset is used. The study performs internal validation only, with no cross-dataset evaluation. Classification is five-class (0–4 DR severity). No pre-trained backbone is employed; the architecture is trained from scratch with a two-phase curriculum strategy.

---

# 3. Research Problem

**Specific problem addressed:** Five-class severity grading of diabetic retinopathy from colour fundus images using a CNN trained end-to-end, without hand-crafted feature extraction.

**Problem dimensions:**

- **Architecture design:** Custom deep CNN construction adequate for fine-grained, five-class DR grading on a large, imbalanced dataset.
- **Class imbalance:** Severe skew toward the "No DR" class (classes 4 and 5 comprising fewer than 3% of images); addressed via dynamic class-weight rebalancing.
- **Preprocessing:** Colour normalisation to mitigate inter-patient variability in illumination and ethnicity-related pixel intensity differences.
- **Clinical deployment:** Authors frame the problem in terms of real-time clinical screening feasibility (0.04 seconds per image classification).
- **Generalization:** Not explicitly addressed; no cross-dataset or external validation is performed.

---

# 4. Datasets Used

| Attribute | Details |
|---|---|
| **Name** | Kaggle Diabetic Retinopathy Detection dataset |
| **Public / Private** | Public |
| **Total sample size** | >80,000 images |
| **Training set** | ~78,000 images (full training set); initial pre-training on 10,290 images |
| **Validation set** | 5,000 images (held-out) |
| **Test set** | [NOT REPORTED — validation set used as test set; no separate test set described] |
| **Class taxonomy** | 5-class: 0 = No DR, 1 = Mild DR, 2 = Moderate DR, 3 = Severe DR, 4 = Proliferative DR |
| **Class balance** | Severely imbalanced; classes 3 and 4 represent <3% of images combined |
| **External dataset used?** | No |
| **Cross-dataset testing performed?** | No |

---

# 5. Preprocessing Pipeline

| Step | Details |
|---|---|
| **Resizing** | All images resized to 512×512 pixels |
| **Cropping** | [NOT REPORTED] |
| **Normalization** | Colour normalisation implemented using OpenCV; rationale: to counteract inter-patient variability in ethnicity, age, and illumination |
| **CLAHE** | [NOT REPORTED] |
| **Color normalization** | Yes — OpenCV-based colour normalisation (specific parameters not reported) |
| **Augmentation** | Real-time data augmentation applied per epoch: random rotation (0–90°), random horizontal flip (yes/no), random vertical flip (yes/no), random horizontal shift, random vertical shift |
| **Image quality filtering** | Not performed as a preprocessing step; authors note post-hoc that >10% of dataset images are clinically ungradable by UK national standards — these were not removed |
| **Lesion enhancement methods** | [NOT REPORTED] |

---

# 6. Model Architecture

| Attribute | Details |
|---|---|
| **Architecture type** | Custom deep CNN (no named backbone) |
| **Layers** | 10 convolutional layers: 2× (32 filters, 3×3), 2× (64 filters, 3×3), 2× (128 filters, 3×3), 2× (256 filters, 3×3), 2× (512 filters, 3×3); followed by 2× fully connected layers (1024 nodes each); output: fully connected 5-node softmax layer |
| **Pooling** | MaxPooling with 3×3 kernel, 2×2 stride |
| **Batch normalisation** | Applied after each convolutional layer initially; reduced to one per block as feature maps increase |
| **Dropout** | 0.5 after final convolutional block and after first fully connected layer |
| **Activation** | Leaky ReLU (α = 0.01) |
| **Regularisation** | L2 regularisation on weights and biases in convolutional layers |
| **Weight initialisation** | Gaussian initialisation |
| **Loss function** | Categorical cross-entropy |
| **Optimizer** | Stochastic gradient descent (SGD) with Nesterov momentum |
| **Learning rate schedule** | 0.0001 for first 5 epochs (stabilisation); 0.0003 for 120 epochs on initial 10,290 images; low rate on full 78,000-image set; reduced by factor of 10 upon loss/accuracy saturation |
| **Epochs** | 120 (initial 10,290 images) + 20 (full training set) |
| **Pretraining source** | None (trained from scratch; no ImageNet or transfer learning reported) |
| **Transfer learning protocol** | [NOT REPORTED — not used] |
| **Input resolution** | 512×512 pixels |
| **Hardware** | NVIDIA K40c GPU (2880 CUDA cores, cuDNN library) |
| **Software** | Keras + Theano backend |
| **Training time** | ~350 hours for initial 120-epoch phase |
| **Class-weight strategy** | Dynamic per-batch class weights updated relative to proportion of "No DR" images in each batch |

---

# 7. Validation Design

- **Internal validation only:** Yes — 5,000 images held out from the Kaggle dataset
- **Cross-validation:** No
- **External validation:** No
- **Prospective validation:** No
- **Multi-center validation:** No

The validation set is drawn from the same Kaggle dataset as the training set. No information is provided on how the 5,000 validation images were sampled (random, stratified, etc.), nor whether the class distribution in the validation set mirrors the training distribution. This constitutes a **single-dataset, single-split, internal validation design** — the weakest form of validation in the evidence hierarchy.

---

# 8. Performance Metrics

**As reported in Section 4 (Results) and confirmed against the confusion matrix (Fig. 4):**

| Metric | Value |
|---|---|
| **Sensitivity** | 30% |
| **Specificity** | 95% |
| **Accuracy** | 75% |
| **AUC** | [NOT REPORTED] |
| **F1 score** | [NOT REPORTED] |
| **Cohen's Kappa** | [NOT REPORTED] |
| **Confidence intervals** | [NOT REPORTED] |
| **Per-class breakdown** | Available via confusion matrix (Fig. 4) but not numerically tabulated in text |
| **Statistical tests** | [NOT REPORTED] |

**Critical note on metric definitions (authors' own, p. 204):**
- Sensitivity = patients correctly identified as having DR / true total with DR
- Specificity = patients correctly identified as not having DR / true total not having DR
- Accuracy = patients with a correct classification (across all five classes)

**Important discrepancy:** The abstract states "sensitivity of 95% and an accuracy of 75%," while the Results section (p. 204) corrects this to **95% specificity** and **30% sensitivity**. The abstract contains a labelling error. This is methodologically significant and must be noted in any citation.

---

# 9. Authors' Claims

**Performance claims:**
- The CNN achieves 95% specificity, 75% accuracy, and 30% sensitivity on 5,000 validation images (p. 204).
- An image can be classified in 0.04 seconds, enabling real-time clinical feedback (p. 203).
- The network "accurately classifies the majority of proliferative cases and cases with no DR" (p. 204).

**Generalization claims:**
- Results are described as "impressive" and "promising" for a "high-level classification task" on a large, general dataset (abstract, p. 200).
- Authors claim that comparable results are produced "without any feature-specific detection" (p. 205).

**Clinical applicability claims:**
- The CNN could classify thousands of images per minute, enabling real-time screening integration (p. 204–205).
- The trained network could make "instant response to a patient possible" (p. 204).

**Superiority claims:**
- Claimed to be "the first paper discussing the five class classification of DR using a CNN approach" (p. 201).
- Previous SVM-based five-class methods required manual feature extraction and were validated only on ~100 images; the CNN is stated to be more real-time applicable (p. 202).

---

# 10. Empirical Support Assessment

**Does data support generalization claims?**
No. Validation is performed exclusively on a held-out split of the same Kaggle dataset used for training. No cross-dataset or external population testing is conducted. Generalization claims are therefore unsupported empirically.

**Is external validation robust?**
Not applicable — no external validation is performed.

**Are confidence intervals reported?**
No. No confidence intervals are provided for any metric.

**Is dataset size adequate?**
The training set (~78,000 images) is large by 2016 standards. However, classes 3 and 4 (Severe and Proliferative DR) together represent fewer than 3% of images (~2,340 images), raising concerns about the adequacy of rare-class representation.

**Is class imbalance addressed?**
Partially. Dynamic per-batch class-weight rebalancing is implemented. No post-hoc evaluation of per-class performance (beyond the confusion matrix figure) is reported numerically.

**Is statistical testing adequate?**
No. No statistical tests, no confidence intervals, no bootstrapping, and no comparison significance tests are reported.

---

# 11. Internal Validity

**Overfitting risk:** Moderate-to-high. Two-phase curriculum training with 120 + 20 epochs on overlapping data, without reported cross-validation. Dynamic class weights and dropout mitigate but do not eliminate risk. The 350-hour training duration on only 10,290 images for 120 epochs raises the possibility of overfitting to the pre-training subset.

**Dataset leakage risk:** [NOT REPORTABLE — insufficient methodological detail]. The separation protocol between the 10,290-image pre-training set and the full 78,000-image training set is not clarified. It is unclear whether the 10,290 images are a subset of the 78,000 or an independent set.

**Confounders:** The authors explicitly acknowledge that >10% of images are clinically ungradable by UK national standards, yet these images were included in both training and validation with erroneous labels. This constitutes a significant label noise confounder.

**Augmentation inflation risk:** Real-time augmentation is applied per epoch. Since the augmented images are generated on-the-fly and not held fixed, the risk of augmentation-driven artificial metric inflation is lower than static augmentation, but the degree of distributional diversity achieved is not quantified.

**Metric reliability:** The abstract-body discrepancy in sensitivity vs. specificity labelling (95% attributed to sensitivity in abstract, but identified as specificity in results) undermines confidence in the precision of metric reporting.

**Formula correctness:** The authors define sensitivity and specificity in binary terms applied to a five-class problem. This collapses the multi-class problem into a binary DR/no-DR distinction for reporting purposes, potentially obscuring inter-class confusion which is the core clinical challenge.

---

# 12. External Validity

**Cross-population transferability:** Not demonstrated. The Kaggle dataset includes patients of varying ethnicities and age groups, which provides some demographic breadth, but no population-specific performance disaggregation is reported.

**Dataset portability:** Not tested. The model is not evaluated on any external dataset (e.g., Messidor, IDRiD, local clinical data).

**Clinical feasibility:** Authors cite 0.04 seconds per image classification and the ability to process thousands of images per minute as evidence of clinical deployability. However, no integration testing, clinician comparison study, or regulatory feasibility assessment is reported.

**Hardware constraints:** NVIDIA K40c GPU required for training; inference hardware requirements not specified. The 350-hour training time is a practical constraint.

---

# 13. Strengths

1. **Scale of training data:** ~78,000 fundus images — substantially larger than all prior five-class DR classification studies cited (which used 89–200 images).
2. **End-to-end learning:** No hand-crafted feature extraction required, reducing domain-specific engineering dependency.
3. **Dynamic class-weight rebalancing:** Per-batch weight adjustment is a methodologically sound approach to severe class imbalance, superior to static oversampling.
4. **Real-time augmentation:** On-the-fly augmentation avoids static dataset inflation and improves generalisation to image variability.
5. **Multi-layer regularisation stack:** Combination of dropout (0.5), L2 regularisation, leaky ReLU, and batch normalisation represents a principled effort to control overfitting.
6. **Historical priority claim:** Presented as the first CNN-based five-class DR grading study, establishing a methodological precedent.

---

# 14. Limitations

**Explicit (stated by authors):**
- Low sensitivity (30%) attributed to difficulty distinguishing mild, moderate, and severe DR classes (p. 205).
- >10% of dataset images are clinically ungradable by UK national standards, yet were included with potentially incorrect labels, possibly "severely hindering" results (p. 205).
- Network trained on only one image per eye (p. 204).
- Plans for a cleaner clinical dataset noted as future work, implicitly acknowledging current dataset quality limitations (p. 205).

**Implicit (methodological):**
- No external or cross-dataset validation; generalization is entirely undemonstrated.
- No AUC, F1, or Cohen's Kappa reported — metrics standard in clinical AI evaluation are absent.
- No confidence intervals or statistical testing on any reported metric.
- Abstract-body metric labelling error (sensitivity/specificity transposition) undermines reporting credibility.
- The binary framing of sensitivity/specificity for a five-class problem masks clinically critical inter-class confusion.
- No ablation study to isolate contributions of preprocessing, augmentation, or architecture depth.
- The 10,290-image pre-training set and 78,000-image full training set relationship is not clearly defined.
- No comparison against a held-out test set distinct from the validation set.
- No clinician benchmark or human-level performance comparison provided.

---

# 15. Relevance to My Dissertation

**Position in paradigm space (v5.3):** P1 (end-to-end CNN; preprocessing as auxiliary step). Grounds (per SIR-9): the paper applies colour normalisation as a fixed preprocessing step but conducts no controlled comparison against the no-preprocessing condition and does not formalise preprocessing as a contributing component of the model. Per CFC-2.9 / SIR-1, no theoretical "preprocessing is unimportant" claim is attributed to the authors.

**Relevance to preprocessing dominance hypothesis:**
Moderate. The paper implements colour normalisation as the primary preprocessing step and explicitly attributes inter-patient image variability to ethnicity, age, and illumination differences. However, no ablation comparing performance with vs. without preprocessing is conducted, making it impossible to isolate the contribution of preprocessing to the reported metrics. This paper cannot be cited as evidence for or against preprocessing dominance; it documents its use without quantifying its effect.

**Relevance to cross-database validation:**
High relevance as a negative case. This paper performs no cross-database validation whatsoever, making it a clear example of the internal-validation-only limitation that motivates cross-dataset robustness research.

**Relevance to EyePACS/Messidor benchmarking:**
Relevant to EyePACS (Kaggle dataset) benchmarking specifically. No Messidor evaluation. Provides a 2016 baseline for five-class EyePACS performance (75% accuracy, 95% specificity, 30% sensitivity) against which later models can be compared.

**Relevance to Vision Transformer comparison:**
Low direct relevance. This is a pre-Transformer, from-scratch CNN study. Useful as a historical baseline establishing what CNN architectures achieved without transfer learning or attention mechanisms in 2016.

**Risk of contradiction:**
Low. This paper makes modest, explicitly qualified performance claims. Its limitations are largely acknowledged by the authors. No inflated generalization or superiority claims are made that would directly contradict dissertation arguments about the necessity of cross-dataset validation or preprocessing rigour.

---

# 16. Citation-Ready Statements

1. "As far as we are aware, this is the first paper discussing the five class classification of DR using a CNN approach" (Pratt et al., 2016, p. 201) — establishing historical CNN precedent for five-class grading.

2. "The final trained network achieved, 95% specificity, 75% accuracy and 30% sensitivity" on 5,000 validation images drawn from the Kaggle DR dataset (Pratt et al., 2016, p. 204) — providing a 2016 CNN baseline for five-class EyePACS performance.

3. "Less than three percent of images came from the 4th and 5th class, meaning changes had to be made in our network to ensure it could still learn the features of these images" (Pratt et al., 2016, p. 201) — documenting the class imbalance problem characteristic of large-scale DR datasets.

4. "By national UK standards around over 10% of the images in our dataset are deemed ungradable. These images were defined a class on the basis of having at least a certain level of DR. This could have severely hindered our results" (Pratt et al., 2016, p. 205) — acknowledging the label noise problem inherent to competition-sourced DR datasets.

5. "The dataset contained images from patients of varying ethnicity, age groups and extremely varied levels of lighting in the fundus photography. This affects the pixel intensity values within the images and creates unnecessary variation unrelated to classification levels. To counteract this, colour normalisation was implemented" (Pratt et al., 2016, p. 203) — providing explicit rationale for preprocessing as a necessary step to mitigate non-pathological image variability.

6. "Each of the previous five class methods required feature extraction from the images before being input to an SVM classifier and have only been validated on small test sets of approximately 100 images. These methods are less real-time applicable than a CNN" (Pratt et al., 2016, p. 202) — contextualising CNN advantage over SVM-based methods in scalability and automation.

---

# 17. Epistemic Classification

**Classification: Methodological Precedent / Limited-Scope Study**

**Justification:** The paper holds genuine historical significance as the first reported CNN-based five-class DR grading study on a large-scale dataset, establishing an architectural and methodological template that subsequent work built upon. However, its epistemic weight as evidence is substantially limited by the absence of external validation, missing standard metrics (AUC, Kappa, F1), no confidence intervals, significant label noise acknowledged by the authors, and a reporting error in the abstract. It functions as a methodological precedent rather than as high-impact empirical evidence. It is not a benchmark study in the formal sense (no standardised evaluation protocol is followed), nor a clinical validation precedent (no clinician comparison or prospective evaluation). It is better characterised as a proof-of-concept study with historical significance in the CNN-for-DR literature.

---

# 18. Analytical Synthesis

Pratt et al. (2016) occupies a specific and bounded role in the diabetic retinopathy deep learning literature: it is the historically significant first demonstration that a CNN can be applied to five-class DR grading at scale, but it does not constitute strong empirical evidence by contemporary methodological standards. The paper's epistemic weight is primarily historical — it establishes the feasibility of the task and the viability of end-to-end CNN learning without hand-crafted features — rather than evidentiary, given the absence of AUC, Cohen's Kappa, confidence intervals, and any form of external validation. For dissertation purposes, it is most appropriately cited as the origin point of CNN-based five-class DR grading and as a demonstration of the class imbalance challenge inherent to large-scale DR datasets, not as evidence of model performance or generalisation. The paper neither strengthens nor weakens a preprocessing-dominance hypothesis, as no ablation of the colour normalisation step is performed; it documents preprocessing use without quantifying its contribution. The complete absence of cross-dataset validation makes this study a canonical illustration of the internal-validation-only limitation that motivates cross-database robustness research, and it can be strategically cited as such in a dissertation arguing for the necessity of multi-dataset evaluation. The sensitivity/specificity labelling error in the abstract must be flagged if this paper is cited on performance grounds, as it has propagated into secondary literature.