# LITERATURE CARD

---

## I. SOURCE IDENTIFICATION

| Field | Content |
|-------|---------|
| **Unique ID** | LC-SAPAKOVA-2025 |
| **Full Bibliographic Citation** | S. Sapakova, N. Yesmukhamedov, A. Sapakov, A. Yemberdiyeva, and Z. Kozhamkulova, "Methods for pre-processing and analysis of fund images for detection of diabetic retinopathy," *Procedia Computer Science*, vol. 272, pp. 496–501, 2025. doi: 10.1016/j.procs.2025.10.237 |
| **Type of Publication** | Conference paper (The 3rd International Workshop on Digital Society: in the Eve of the 6th Information Revolution — DS 2025, October 28–30, 2025, Istanbul, Türkiye) |
| **Year** | 2025 |
| **Research Domain Classification** | Medical Image Analysis → Diabetic Retinopathy Detection → CNN-based Classification → Image Preprocessing & Transfer Learning |

---

## II. GLOBAL SOURCE ANALYSIS

### II.1 Central Thesis

The source argues that a two-stage adaptation strategy for EfficientNetB0 — initially freezing base layers and training only the classification head, followed by unfreezing and fine-tuning the top layers — coupled with systematic image preprocessing (augmentation, normalization, contrast enhancement), significantly improves diagnostic performance for diabetic retinopathy classification on fundus images compared to a fully frozen transfer learning approach. [Thesis reconstructed from sections: Abstract, §3.3, §4 Conclusion]

### II.2 Research Problem Addressed

- **General problem domain:** Automated detection and classification of diabetic retinopathy from fundus images using deep learning.
- **Specific problem:** Improving image classification accuracy for early DR diagnosis by optimizing (a) fundus image preprocessing techniques and (b) transfer learning adaptation strategies for EfficientNetB0, particularly under conditions of severe class imbalance and limited data. [p. 496, Abstract; p. 497, Introduction]

### II.3 Methodology

- **Theoretical framework:** Transfer learning theory applied to medical image classification; convolutional neural network feature extraction; five-class ordinal classification of DR stages per standard clinical grading (0 — no disease, 1 — early, 2 — moderate, 3 — severe, 4 — proliferative). [p. 497]
- **Methods used:**
  - **Architecture:** EfficientNetB0 with transfer learning. Alternative architectures (ResNet, VGG, DenseNet) were explicitly excluded from this study; comparative analysis is deferred to future work. [p. 498]
  - **Training protocol — Two-stage strategy:**
    - *Method 1 (Freeze):* Freezing all base layers, training only the classification head with softmax output. [p. 497, 499]
    - *Method 2 (Unfreeze Top Layers):* After initial training, unfreezing upper layers and fine-tuning the full top portion of the network. [p. 497, 499]
  - **Preprocessing:** Image augmentation (rotation, scaling, shifting, brightness adjustment, skewing), contrast enhancement, illumination normalization, artifact and noise smoothing, color balance adjustment. [p. 497, 498]
  - **Optimizer:** Adam with StepLR learning rate scheduler; callbacks including ReduceLROnPlateau and EarlyStopping. [p. 497, 499]
  - **Loss function:** Cross-entropy loss; weighted loss functions applied to address class imbalance. [p. 497, 498]
  - **Evaluation metrics:** Precision, Recall, F1-score, Accuracy, Cohen's Kappa (squared weights), Macro Average, Weighted Average. [p. 497, 499]
- **Data sources:**
  - Primary dataset: APTOS 2019 Blindness Detection dataset (Kaggle). [p. 498]
  - Supplementary data: Additional anonymized fundus images from private medical centers, labeled by certified ophthalmologists. [p. 498]
  - Training set: 35,126 images; Test set: 3,662 images. Five-class distribution. [p. 498]
  - Training set class distribution: Class 0 — 25,810 (73.5%), Class 1 — 2,443 (7.0%), Class 2 — 5,292 (15.1%), Class 3 — 873 (2.5%), Class 4 — 708 (2.0%). [p. 498]
  - Test set class distribution: Class 0 — 1,805 (49.3%), Class 1 — 370 (10.1%), Class 2 — 999 (27.3%), Class 3 — 193 (5.3%), Class 4 — 295 (8.0%). [p. 498]
- **Analytical approach:** Comparison of Method 1 (Freeze) vs. Method 2 (Unfreeze Top Layers) across Train, Val, and Test splits using Precision, Recall, F1-Score, Accuracy, Macro Average, and Weighted Average. Cross-validation with fixed folds for robustness confirmation. [p. 497, 499]

### II.4 Conceptual Contributions

- The source introduces the concept of a "two-stage adaptation of EfficientNetB0 tailored to fundus image variability" as a methodological approach to DR detection, framing it as a novelty relative to existing DR literature. [p. 497]
- The source frames preprocessing not as isolated techniques but as a combined pipeline whose aggregate effect improves model robustness. [p. 498]
- *Uses standard definitions of diabetic retinopathy stages (0–4), EfficientNetB0 architecture, transfer learning, and data augmentation without modification.*

### II.5 Empirical Contributions

- **Data:** APTOS 2019 + supplementary clinical images; 35,126 training, 3,662 test images; 5-class DR classification; severely imbalanced (Class 0: 73.5% in training). [p. 498]
- **Findings — Method 1 (Freeze):** Precision (Test) = 0.65, Recall (Test) = 0.60, F1-Score (Test) = 0.62, Accuracy = 0.80, Macro Avg = 0.72, Weighted Avg = 0.74. [p. 499, Table 3]
- **Findings — Method 2 (Unfreeze Top Layers):** Precision (Test) = 0.75, Recall (Test) = 0.74, F1-Score (Test) = 0.74, Accuracy = 0.80, Macro Avg = 0.77, Weighted Avg = 0.81. [p. 499, Table 3]
- **Measurable results:** Fine-tuning (Method 2) improved test Precision by +10 pp, Recall by +14 pp, F1-Score by +12 pp over Method 1, while accuracy remained constant at 0.80. Macro Average improved from 0.72 to 0.77; Weighted Average from 0.74 to 0.81. [p. 499, Table 3]
- **Training metrics (Method 1):** Precision = 0.85, Recall = 0.90, F1-Score = 0.87. Evidence of overfitting: training F1 = 0.87 vs. test F1 = 0.62. [p. 499, Tables 1–2]

### II.6 Limitations Acknowledged by the Author

- Limited amount of data acknowledged as a shortcoming. [p. 500, Conclusion]
- Difficulties in interpretation of model results. [p. 500, Conclusion]
- Alternative architectures (ResNet, VGG, DenseNet) were not evaluated; comparative analysis deferred to future work. [p. 498]
- Additional data and explanatory improvements are needed to ensure overall model stability. [p. 500, Conclusion]

### II.7 Implicit Assumptions

> **Assumption:** EfficientNetB0 is a sufficiently representative architecture for evaluating the impact of transfer learning strategies on DR classification, and conclusions drawn from it generalize to the broader class of efficient CNN architectures.
> **Textual basis:** The authors chose to evaluate only EfficientNetB0 and state that "alternative architectures (ResNet, VGG, DenseNet) were not evaluated at this stage," yet frame their two-stage fine-tuning conclusion as a general methodological finding. [p. 498]

> **Assumption:** The supplementary anonymized fundus images from private medical centers are comparable in quality and labeling consistency to the APTOS 2019 dataset.
> **Textual basis:** The authors state these images "were labeled by certified ophthalmologists, in accordance with data protection and ethical standards" but do not report inter-annotator agreement or quality validation procedures for the supplementary data. [p. 498]

> **Assumption:** Overall accuracy is a secondary metric compared to Precision, Recall, and F1-Score for evaluating DR classification performance under class imbalance.
> **Textual basis:** Despite both methods achieving identical accuracy (0.80), the authors conclude Method 2 is "significantly better" based exclusively on improvements in Precision, Recall, F1-Score, and averaged metrics. [p. 499–500]

---

## III. EXTRACTION BLOCKS

---

### Extraction Block EB-01: Two-Stage Fine-Tuning Strategy for EfficientNetB0

**Relevant to:**

- **Dissertation claim(s) supported or challenged:** Two-Stage Fine-Tuning (Claim 4); Preprocessing Dominance Thesis (Claim 1, indirectly)
- **Dissertation outline section(s):** §3.3.2 Two-Stage Fine-Tuning Protocol Design; §4.4.1 EfficientNetB0: Frozen versus Progressive Fine-Tuning
- **Concept(s) used:** Transfer learning, progressive fine-tuning, frozen-layer strategy, EfficientNetB0
- **Research question addressed:** Determining the most effective transfer learning adaptation strategy for five-class DR classification

**Function in dissertation:**

- [x] Empirical support — provides data or results that corroborate dissertation findings
- [x] Methodological precedent — establishes or validates a method the dissertation adopts or adapts

**Extracted Content (Strict Extraction Only):**

- Two training strategies were tested: (1) freezing base layers and training only the classification head, and (2) fine-tuning by unfreezing the top layers after initial training. [p. 496, Abstract]
- Method 2 (Unfreeze Top Layers) achieved: Precision (Test) = 0.75, Recall (Test) = 0.74, F1-Score (Test) = 0.74, compared to Method 1: Precision = 0.65, Recall = 0.60, F1-Score = 0.62. [p. 499, Table 3]
- Both methods achieved identical overall accuracy of 0.80. [p. 499, Table 3]
- Macro Average improved from 0.72 (Method 1) to 0.77 (Method 2); Weighted Average from 0.74 to 0.81. [p. 499, Table 3]
- The authors conclude that "unfreezing and fine-tuning the top layers leads to more balanced and robust generalization on unseen data, whereas fully freezing the layers limits the model's ability to generalize." [p. 499]
- The improvements are attributed to "the model's enhanced ability to generalize after fine-tuning, reducing overfitting and capturing more complex features." [p. 496, Abstract]

**Strength of Relevance:** **Core** — This is the central experimental finding of the source and directly maps to the dissertation's Claim 4 (Two-Stage Fine-Tuning). The exact metrics reported here are referenced in the dissertation's key experimental results.

---

### Extraction Block EB-02: Image Preprocessing Pipeline for Fundus Analysis

**Relevant to:**

- **Dissertation claim(s) supported or challenged:** Preprocessing Dominance Thesis (Claim 1); Unified Pipeline Approach (Claim 2)
- **Dissertation outline section(s):** §3.1.1 Pipeline Stage Specification: Resizing, Normalization, Enhancement, Augmentation; §3.1.3 Augmentation Strategy for Class Imbalance Mitigation
- **Concept(s) used:** Image augmentation, contrast enhancement, illumination normalization, noise reduction, preprocessing pipeline
- **Research question addressed:** Developing and evaluating preprocessing methods that improve CNN diagnostic performance on fundus images

**Function in dissertation:**

- [x] Methodological precedent — establishes or validates a method the dissertation adopts or adapts
- [x] Empirical support — provides data or results that corroborate dissertation findings

**Extracted Content (Strict Extraction Only):**

- Preprocessing steps include image augmentation (rotation, scaling, cropping, contrast enhancement) and normalization to increase model robustness. [p. 496, Abstract]
- Preprocessing consists of: contrast enhancement, illumination normalization, artifact and noise smoothing, and color balance adjustment. [p. 498]
- Augmentation techniques applied: rotation, scaling, shifting, brightness adjustment, skewing — applied to address dataset imbalance and improve variability and generalization. [p. 498]
- The authors state: "Proper image processing significantly increases the accuracy and reliability of automated diagnostic systems, allowing for clear and informative data." [p. 498]
- Image augmentation and preprocessing methods "have a positive effect on improving the efficiency of the model." [p. 500, Conclusion]

**Strength of Relevance:** **Core** — Directly supports the dissertation's Preprocessing Dominance Thesis by providing empirical evidence and methodological description of a preprocessing pipeline for DR fundus image classification.

---

### Extraction Block EB-03: Class Imbalance in DR Datasets and Mitigation Strategies

**Relevant to:**

- **Dissertation claim(s) supported or challenged:** Preprocessing Dominance Thesis (Claim 1); Resource Stability (Claim 3)
- **Dissertation outline section(s):** §4.1.2 Class Distribution Analysis and Data Partitioning Strategy; §3.3.3 Weighted Loss Function Formulation for Ordinal Class Structure; §2.2.2 Loss Functions and Optimization for Imbalanced Medical Datasets
- **Concept(s) used:** Class imbalance, weighted loss functions, data augmentation for balancing, ordinal classification
- **Research question addressed:** Addressing severe class imbalance in DR classification datasets to improve model generalization

**Function in dissertation:**

- [x] Empirical support — provides data or results that corroborate dissertation findings
- [x] Methodological precedent — establishes or validates a method the dissertation adopts or adapts

**Extracted Content (Strict Extraction Only):**

- Training set was highly imbalanced: Class 0 comprised 73.5%, while Classes 3 and 4 accounted for only 2.5% and 2.0% respectively. [p. 498]
- To address imbalance, weighted loss functions and augmentation were applied. [p. 498]
- The model showed evidence of overfitting: training F1 = 0.87 vs. test F1 = 0.62 (Method 1), attributed in part to "class imbalance and limited representation of severe cases." [p. 499]
- The authors note: "Enhancing robustness may require regularization, hyperparameter tuning, and class balancing." [p. 499]

**Strength of Relevance:** **Supporting** — Provides empirical documentation of the class imbalance problem and mitigation approaches relevant to the dissertation's experimental design, but the specific weighted loss formulation is not detailed.

---

### Extraction Block EB-04: Overfitting Diagnosis and Regularization Techniques

**Relevant to:**

- **Dissertation claim(s) supported or challenged:** Two-Stage Fine-Tuning (Claim 4); Preprocessing Dominance Thesis (Claim 1)
- **Dissertation outline section(s):** §2.2.3 Regularization Techniques: Dropout, Batch Normalization, and Data Augmentation; §4.4.1 EfficientNetB0: Frozen vs. Progressive Fine-Tuning
- **Concept(s) used:** Overfitting, regularization, EarlyStopping, ReduceLROnPlateau, generalization
- **Research question addressed:** Reducing overfitting in DR classification models under data-constrained conditions

**Function in dissertation:**

- [x] Empirical support — provides data or results that corroborate dissertation findings
- [x] Theoretical grounding — provides foundational theory the dissertation builds upon

**Extracted Content (Strict Extraction Only):**

- Training set F1 = 0.87 vs. test set F1 = 0.62, indicating overfitting "likely caused by class imbalance and limited representation of severe cases." [p. 499]
- Adam optimizer with ReduceLROnPlateau and EarlyStopping callbacks was employed to reduce overfitting. [p. 499]
- Fine-tuning (Method 2) reduced the train-test F1 gap: training F1 = 0.86 with test F1 = 0.74, compared to Method 1's training F1 = 0.87 with test F1 = 0.62. [p. 499, Table 3]
- The callback functions "help to optimize the learning process and prevent the model from overfitting." [p. 500, Conclusion]
- Cross-validation with fixed folds was used to confirm robustness. [p. 497]

**Strength of Relevance:** **Supporting** — Provides evidence that the two-stage fine-tuning approach reduces overfitting, supporting the dissertation's argument for this strategy. The specific regularization techniques documented serve as methodological precedent.

---

### Extraction Block EB-05: EfficientNetB0 Architecture Selection Rationale

**Relevant to:**

- **Dissertation claim(s) supported or challenged:** Resource Stability (Claim 3)
- **Dissertation outline section(s):** §3.2 Design of Baseline and Enhanced CNN Architectures; §3.3.1 Architecture Adaptation for Five-Class DR Classification
- **Concept(s) used:** EfficientNetB0, computational efficiency, accuracy-to-computation ratio, resource-limited deployment
- **Research question addressed:** Selecting a computationally efficient CNN architecture suitable for DR classification under resource constraints

**Function in dissertation:**

- [x] Theoretical grounding — provides foundational theory the dissertation builds upon
- [x] Methodological precedent — establishes or validates a method the dissertation adopts or adapts

**Extracted Content (Strict Extraction Only):**

- EfficientNetB0 was selected for its "high accuracy-to-computation ratio, providing an optimal balance between performance and computational efficiency." [p. 498]
- This is characterized as "particularly important when working with large medical datasets, where training speed and resource efficiency are critical." [p. 497–498]
- Alternative architectures (ResNet, VGG, DenseNet) were not evaluated at this stage, with "comparative analysis of different architectures planned for future work." [p. 498]
- The proposed method "demonstrates high potential for implementation in automated diagnostic systems for early detection of retinal diseases and can be applied in clinical decision-support tools under limited data conditions." [p. 496, Abstract]

**Strength of Relevance:** **Supporting** — Provides justification for EfficientNetB0 selection that aligns with the dissertation's Resource Stability claim, but the absence of comparative architecture evaluation limits the strength of the efficiency argument.

---

### Extraction Block EB-06: Dataset Composition and Experimental Configuration

**Relevant to:**

- **Dissertation claim(s) supported or challenged:** Clinical Applicability (Claim 5)
- **Dissertation outline section(s):** §4.1.1 APTOS 2019, STARE, and Supplementary Clinical Image Corpora; §4.1.2 Class Distribution Analysis and Data Partitioning Strategy
- **Concept(s) used:** APTOS 2019 dataset, supplementary clinical data, five-class DR classification, data partitioning
- **Research question addressed:** Establishing a robust and representative dataset for DR classification experiments

**Function in dissertation:**

- [x] Methodological precedent — establishes or validates a method the dissertation adopts or adapts

**Extracted Content (Strict Extraction Only):**

- Primary dataset: APTOS 2019 Blindness Detection dataset from Kaggle. [p. 498]
- Supplementary data: "additional anonymized fundus images were incorporated from private medical centers," labeled by certified ophthalmologists "in accordance with data protection and ethical standards." [p. 498]
- Total training set: 35,126 images; test set: 3,662 images. [p. 498]
- Five diagnostic categories: 0 — no disease, 1 — early stage, 2 — moderate stage, 3 — severe stage, 4 — proliferative stage. [p. 498]
- Test set designed to simulate "real-world conditions with predominantly healthy cases." [p. 498]

**Strength of Relevance:** **Core** — The dissertation uses the same primary dataset (APTOS 2019) and supplementary clinical data; this source documents the exact experimental configuration.

---

## IV. RELATIONAL POSITIONING

| Relation | Specification |
|----------|--------------|
| **Supports which dissertation claims** | **Two-Stage Fine-Tuning (Claim 4):** Directly provides the empirical comparison of frozen vs. unfrozen fine-tuning strategies with quantified performance improvements. **Preprocessing Dominance Thesis (Claim 1):** Supports the argument that preprocessing (augmentation, normalization, contrast enhancement) improves model robustness. **Resource Stability (Claim 3):** EfficientNetB0 selection rationale aligns with resource-efficient deployment argument. **Clinical Applicability (Claim 5):** Explicit statement that the method is applicable to "clinical decision-support tools under limited data conditions." |
| **Contradicts which claims (if any)** | No direct contradictions identified. However, the source does not isolate preprocessing impact from architectural adaptation — the Preprocessing Dominance Thesis is supported but not independently tested (preprocessing and fine-tuning strategy are changed simultaneously). |
| **Extends which conceptual axis** | Extends the transfer learning methodology axis by providing a concrete two-stage protocol specifically tailored to fundus image variability in DR classification. Also extends the preprocessing pipeline axis by documenting the specific augmentation and enhancement steps applied to the APTOS 2019 dataset. |
| **Overlaps with which other sources** | Expected overlap with: Sarki et al. (2021) [Ref. 5] on image preprocessing for DR; Balaji et al. (2024) [Ref. 4/12] on deep learning with preprocessing for DR; Sapakova et al. (2024) [Ref. 8] as a prior publication by overlapping authors. Cross-source overlap assessment requires full bibliography review for complete mapping. |

---

## V. REUSABILITY CONTROL

| Category | Assessment |
|----------|-----------|
| **What can be reused in dissertation drafting** | Specific quantitative results from Table 3 (Method 1 vs. Method 2 metrics) can be cited directly. Dataset composition details (sizes, class distributions) are directly reusable. The two-stage fine-tuning protocol description provides a citable methodological reference. EfficientNetB0 selection rationale is directly quotable. |
| **What must be reformulated** | The preprocessing pipeline description must be substantially expanded and reformulated in the dissertation context, as the source provides only a high-level enumeration. Conclusion statements about effectiveness must be reframed within the dissertation's broader argumentative structure (six-chapter framework vs. the source's conference paper scope). The overfitting analysis must be contextualized within the dissertation's more comprehensive regularization discussion. |
| **Risk of self-plagiarism** | **SELF-CITATION: This source is authored/co-authored by the doctoral candidate (Nurmaganbet Yesmukhamedov is the second author; Saya Sapakova, Askar Sapakov, Aknur Yemberdiyeva, and Zhadra Kozhamkulova are known co-authors).** All reused content must be explicitly attributed and substantially reformulated to avoid self-plagiarism. Overlapping experimental data (APTOS 2019 + supplementary clinical data, identical metric values), methodology descriptions (two-stage EfficientNetB0 fine-tuning protocol), and results sections (Table 3 metrics) require particularly careful reformulation. The dissertation must clearly indicate when citing its own prior conference publication and ensure that all descriptions, analyses, and interpretations are substantially expanded and independently articulated. |

---

## VI. TERMINOLOGY INDEX

| Term | Definition/Usage in Source | Stability Note |
|------|--------------------------|----------------|
| Diabetic retinopathy (DR) | "A widespread eye disease in diabetic patients" classified into five stages (0–4). [p. 496] | Align with standard clinical grading; consistent across dissertation. |
| EfficientNetB0 | Neural network architecture selected for "high accuracy-to-computation ratio." [p. 498] | Use consistently; distinguish from broader EfficientNet family when referencing specific variants. |
| Freeze (Method 1) | Training strategy: freezing base layers, training only the classification head. [p. 496, 499] | Dissertation should use "frozen-layer strategy" or equivalent consistently. |
| Unfreeze Top Layers (Method 2) | Training strategy: unfreezing upper layers after initial training for fine-tuning. [p. 496, 499] | Dissertation uses "progressive fine-tuning" or "two-stage fine-tuning" — ensure terminological alignment. |
| Fundus image | Retinal image used for DR diagnosis. [p. 496] | Note: source title uses "fund images" (apparent typographic error); dissertation should use "fundus images" consistently. |
| Data augmentation | Rotation, scaling, shifting, brightness adjustment, skewing applied to training images. [p. 497, 498] | Consistent with standard usage; enumerate specific techniques when referencing this source. |
| Transfer learning | Using pre-trained EfficientNetB0 weights adapted to DR classification. [p. 498–499] | Standard usage; no source-specific redefinition. |
| Weighted loss function | Cross-entropy loss with class weights to address imbalance. [p. 497, 498] | Source does not specify exact weight formulation; dissertation must define precisely if adopting. |
| Cohen's Kappa | Evaluation metric with squared weights for class imbalance assessment. [p. 497] | Ensure "squared weights" specification is maintained when citing this source's use of the metric. |
| APTOS 2019 | Primary dataset: APTOS 2019 Blindness Detection dataset from Kaggle. [p. 498] | Full name should be used on first reference; abbreviation thereafter. |
| EarlyStopping | Callback function to halt training when validation performance stops improving. [p. 497, 500] | Standard usage; consistent across dissertation. |
| ReduceLROnPlateau | Callback function reducing learning rate when metric plateaus. [p. 499, 500] | Standard usage; consistent across dissertation. |
