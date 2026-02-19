# LITERATURE CARD

---

## I. SOURCE IDENTIFICATION

| Field | Value |
|---|---|
| **Unique ID** | `LC-Yesmukhamedov-2025-SELF` |
| **Full Bibliographic Citation** | Yesmukhamedov N.S., Sapakova S.Z., Kozhamkulova Zh.Zh., Daniyarova D.R., Armankyzy R. Methods for Preprocessing and Analysis of Fundus Images for Diabetic Retinopathy Detection. Herald of the Kazakh-British Technical University, No. 4(75), 2025. https://doi.org/10.55452/1998-6688-2025-22-4-119-130 |
| **Type of Publication** | Empirical study (primary); methodological paper (secondary) |
| **Year** | 2025 |
| **Research Domain Classification** | diabetic retinopathy diagnosis, image preprocessing, deep learning, convolutional neural networks, fundus imaging |

---

## I-A. SOURCE STATUS CLASSIFICATION

- **Source Ownership:** Co-authored Publication (Dissertation Candidate as Co-author)
- **SELF_PUBLICATION_FLAG:** YES
- **Corpus Coverage Tags:** [OWN_STUDY] [PREPROCESS_DOMINANT]

---

## II. GLOBAL SOURCE ANALYSIS

### II.1 Central Thesis

The source argues that the combination of image preprocessing methods (augmentation, normalization, contrast enhancement) with the EfficientNetB0 deep learning architecture constitutes an effective approach for automated diabetic retinopathy classification, and that fine-tuning (opening upper layers for additional adaptation) significantly outperforms a frozen-layers approach in terms of precision, recall, and generalization on test and validation data. The central proposition is that input data quality improvement through preprocessing, coupled with appropriate transfer learning adaptation strategy, yields clinically meaningful improvements in DR diagnostic performance.

### II.2 Research Problem Addressed

The source identifies that diabetic retinopathy is a common eye disease in patients with diabetes and one of the main causes of vision loss, and that early diagnosis allows prevention of vision loss (Introduction, paragraph 1). The specific research gap motivating the work is the need to study and compare methods for preprocessing and analyzing fundus images in order to improve the quality of image processing and classification for effective diabetic retinopathy diagnosis (Abstract). The study addresses the practical problem of class imbalance in DR datasets (class 0 comprising 73.5% of training data while severe stages represent only 2.5% and 2.0%), which complicates accurate classification of rare but clinically important cases (Dataset and its Characteristics section; Data Processing section, point 1).

### II.3 Methodology

- **Theoretical Framework:** The study operates within the framework of transfer learning using pre-trained convolutional neural network models, specifically EfficientNetB0. The conceptual approach follows the paradigm of adapting pre-trained models through two strategies: frozen base layers with final layer training, and fine-tuning through opening upper layers for additional adaptation (Results and Discussion section).

- **Methods Used:**
  - EfficientNetB0 architecture with transfer learning
  - Two training approaches: (1) freezing all base layers and training only final layers; (2) opening upper layers after initial training for fine-tuning
  - Data augmentation: rotation, scaling, shifting, brightness changes (Data Augmentation, section 8)
  - Image normalization and preprocessing (contrast enhancement, light effect stabilization, noise/artifact smoothing, color balance adjustment) (Dataset section, Figure 3 description)
  - Convolutional layers for feature extraction (section 2, formula 2)
  - Softmax function for 5-class classification (section 3, formula 3)
  - Cross-entropy loss function (CrossEntropyLoss) for minimizing prediction error (section 4, formula 4)
  - Adam optimizer with step learning rate scheduler (StepLR) (section 5, formula 5)
  - Early stopping to prevent overfitting (section 7)
  - Cross-validation with fixed number of folds (section 1)
  - Cohen's Kappa metric with quadratic weights (section 6, formulas 6–7)
  - Grid search and random search for hyperparameter selection (Results and Discussion)
  - Callbacks: ReduceLROnPlateau and EarlyStopping (Results and Discussion)

- **Data Sources:** A dataset containing fundus images divided into training and test sets. Training set: 35,126 images; test set: 3,662 images. Five-class labels corresponding to DR stages: 0 – no disease, 1 – early stage, 2 – moderate stage, 3 – severe stage, 4 – proliferative stage. Training set distribution: Class 0: 25,810 (73.5%), Class 1: 2,443 (7.0%), Class 2: 5,292 (15.1%), Class 3: 873 (2.5%), Class 4: 708 (2.0%). Test set distribution: Class 0: 1,805 (49.3%), Class 1: 370 (10.1%), Class 2: 999 (27.3%), Class 3: 193 (5.3%), Class 4: 295 (8.0%) (Dataset and its Characteristics section).

- **Analytical Approach:** Results evaluated using Precision, Recall, F1-Score, and Accuracy metrics. Cohen's Kappa metric with quadratic weights was used for inter-class agreement assessment. Cross-validation ensured model stability and reproducibility. Comparison between Method 1 (frozen layers) and Method 2 (fine-tuning) was performed across Train, Test, and Val subsets (Results and Discussion section; Figure 4; Figure 5).

### II.4 Conceptual Contributions

No novel conceptual contributions identified; the source operates within established terminology. The source applies existing concepts (transfer learning, fine-tuning, data augmentation, cross-validation, Cohen's Kappa) to the specific domain of DR classification using EfficientNetB0. The contribution is primarily methodological and empirical rather than conceptual.

### II.5 Empirical Contributions (if applicable)

- **Data:** Fundus images classified into five DR stages (0–4), with training set of 35,126 images and test set of 3,662 images exhibiting significant class imbalance.

- **Findings:**
  - Method 1 (frozen base layers): Precision for test set was 65%; accuracy of validation set was 63%; recall for test set was 60% (Abstract).
  - Method 2 (fine-tuning, opening upper layers): Precision for test set was 75%; accuracy of validation set reached 71%; recall for test set was 74% (Abstract).
  - Train-class Precision was 0.85, while Test and Val were 0.65 and 0.68 respectively, indicating potential overfitting (Results Analysis, point 1).
  - Overall Accuracy reached 80% (Results Analysis, point 2).
  - Average weighted Precision: 0.81; Recall: 0.85; F1-Score: 0.83 (Results Analysis, point 2).
  - Accuracy was 0.80 for both methods, but Macro Average and Weighted Average were significantly better for Method 2 (0.77 and 0.81 vs. 0.72 and 0.74) (Results Comparison, point 2).
  - The fine-tuning method reduced overfitting and increased overall model efficiency (Results Comparison).

- **Measurable Results:**

| Metric | Method 1 (Frozen) | Method 2 (Fine-tuning) |
|---|---|---|
| Precision (Test) | 65% | 75% |
| Accuracy (Validation) | 63% | 71% |
| Recall (Test) | 60% | 74% |
| Accuracy (Overall) | 0.80 | 0.80 |
| Precision (Train) | 0.85 | — |
| Precision (Test) | 0.65 | — |
| Precision (Val) | 0.68 | — |
| Macro Average (Method 1 / Method 2) | 0.72 | 0.77 |
| Weighted Average (Method 1 / Method 2) | 0.74 | 0.81 |
| Weighted Precision (summary) | 0.81 | — |
| Weighted Recall (summary) | 0.85 | — |
| Weighted F1-Score (summary) | 0.83 | — |

### II.6 Limitations Acknowledged by the Author

- Limited data volume was identified as a shortcoming (Conclusion, paragraph 2).
- Difficulties in interpreting model results were identified (Conclusion, paragraph 2).
- The author states that "additional data and interpretive improvements are needed to ensure overall model stability" (Conclusion, paragraph 1).
- Relatively low metrics on Test and Val classes indicate model overfitting, and "data balancing, hyperparameter optimization, and additional regularization methods are considered" to improve results (Results Analysis, point 3).

### II.7 Implicit Assumptions

- The source assumes that the EfficientNetB0 architecture pre-trained on ImageNet features transfers meaningfully to fundus image analysis, without explicitly discussing the domain gap between natural images and medical fundus images.
- The source assumes that the five-class DR staging system (0–4) used in the dataset labels reflects clinically validated ground truth, without discussing inter-rater reliability of the labeling process or the provenance of diagnostic labels.
- The source implicitly assumes that class imbalance can be sufficiently addressed through weighted loss functions and data augmentation, without testing alternative strategies such as oversampling (e.g., SMOTE) or undersampling.

---

## III. EXTRACTION BLOCKS

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-01]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C1 (Integration of preprocessing methods with CNN constitutes a unified system for automated DR diagnosis); C2 (Diagnostic effectiveness depends on input image quality apart from model architecture)
- **Concept(s) used:** Preprocessing-CNN integration; image augmentation; normalization; contrast enhancement
- **Research question addressed:** RQ1

**Function in dissertation:**
- Empirical support
- Methodological precedent

**Extracted Content (Strict Extraction Only):**
- "For preprocessing, image augmentation methods (rotation, scaling, cropping, contrast enhancement) and normalization were introduced." (Abstract)
- Preprocessing stages include: clarity level enhancement, increasing image contrast; light effect stabilization, reducing lighting inequality; smoothing artifacts and noise; color balance change (Dataset and its Characteristics section, Figure 3 description).
- "These steps are necessary for preparing images used in computer vision tasks for diagnosing fundus diseases, such as diabetic retinopathy and glaucoma. Proper image processing significantly increases the accuracy and reliability of automated diagnostic systems." (Dataset and its Characteristics section, final paragraph)
- Data augmentation included rotation, scaling, and brightness changes to allow the model to "adapt to real-world conditions and better represent key features of diabetic retinopathy" (section 8, Data Augmentation).

**Strength of Relevance:** **Core**

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-02]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C2 (Diagnostic effectiveness depends on input image quality); C3 (Proposed approach improves classification and reduces overfitting)
- **Concept(s) used:** Transfer learning; fine-tuning; frozen layers vs. open layers
- **Research question addressed:** RQ1, RQ3

**Function in dissertation:**
- Empirical support
- Benchmark comparison

**Extracted Content (Strict Extraction Only):**
- Two approaches tested with EfficientNetB0: "the first method used freezing all layers and working only with final layers, while the second method opened upper layers after initial training and performed further model fine-tuning" (Results and Discussion section).
- Method 1: Precision (Test) = 65%, Accuracy (Val) = 63%, Recall (Test) = 60% (Abstract).
- Method 2: Precision (Test) = 75%, Accuracy (Val) = 71%, Recall (Test) = 74% (Abstract).
- "By Precision, Recall, and F1-Score metrics, the second method showed significantly higher results, especially on test and validation data. Method 2 increased model complexity by opening upper layers and ensured better adaptation to specific data" (Results Comparison, point 1).
- "The second method, i.e., opening upper layers and additional model fine-tuning, proved more effective. This method provided higher results on test and validation data, thereby reducing the overfitting problem and increasing the model's overall efficiency." (Results Comparison, final paragraph)

**Strength of Relevance:** **Core**

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-03]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C3 (Proposed approach reduces overfitting under limited resources)
- **Concept(s) used:** Overfitting; regularization; early stopping; callbacks
- **Research question addressed:** RQ2

**Function in dissertation:**
- Empirical support
- Methodological precedent

**Extracted Content (Strict Extraction Only):**
- "Metrics in the Train class are significantly higher compared to Test and Val classes, which may indicate data imbalance or lack of model generalization ability. For example, Precision for Train is 0.85, while for Test and Val it is 0.65 and 0.68 respectively." (Results Analysis, point 1)
- "Despite high accuracy on training data, relatively low metrics in Test and Val classes indicate model overfitting." (Results Analysis, point 3)
- "Early stopping was used to stop training if Cohen's Kappa metric on the validation set did not improve for k epochs, preventing overfitting" (section 7, Early Stopping).
- Callbacks ReduceLROnPlateau and EarlyStopping with Adam optimizer were used "to increase training efficiency" (Results and Discussion section).
- The Conclusion states: "callback functions (EarlyStopping, ReduceLROnPlateau) optimized the learning process and prevented overfitting."

**Strength of Relevance:** **Core**

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-04]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C4 (Standardized approaches for systematic integration of preprocessing and CNN are limited)
- **Concept(s) used:** Class imbalance; dataset characteristics; weighted loss functions
- **Research question addressed:** RQ2

**Function in dissertation:**
- Literature gap evidence
- Empirical support

**Extracted Content (Strict Extraction Only):**
- Training set class distribution: Class 0: 25,810 (73.5%), Class 1: 2,443 (7.0%), Class 2: 5,292 (15.1%), Class 3: 873 (2.5%), Class 4: 708 (2.0%) (Dataset and its Characteristics section).
- "In the training set, class 0 (no retinopathy) is dominant, comprising 73.5% of total data, while severe stages (classes 3 and 4) are significantly less, showing 2.5% and 2.0% respectively." (Data Processing, point 1)
- "Weighted loss functions and data augmentation methods were used to account for class imbalance." (Data Processing, point 1)
- "These features demonstrated the need for methods that effectively combat class imbalance and improve classification accuracy of rare but clinically important cases." (Data Processing, final sentence)
- The cross-entropy loss function was employed specifically because "the DR classification problem involves imbalanced classes" and it "allows the model to accurately identify rare but important classes (e.g., class 4, severe DR stage)" (section 4, pages 3–4).

**Strength of Relevance:** **Supporting**

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-05]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C1 (Unified system for automated DR diagnosis); C5 (Reproducible pipeline applicable in screening environments)
- **Concept(s) used:** EfficientNetB0; transfer learning; softmax classification; cross-validation
- **Research question addressed:** RQ2

**Function in dissertation:**
- Methodological precedent

**Extracted Content (Strict Extraction Only):**
- "The study used the EfficientNetB0 neural network for image classification. This method uses the Transfer Learning approach based on pre-trained models." (Results and Discussion, paragraph 1)
- "Hyperparameters of the EfficientNetB0 model were selected experimentally in advance. Learning rate, batch size, optimizer type, and regularization parameters were evaluated in several experimental configurations. The most efficient combination was selected through grid search and random search methods." (Results and Discussion)
- "Cross-validation results ensured model stability and reproducibility, allowing evaluation of research results on other datasets." (Results and Discussion)
- "Multiclass image classification was performed through softmax activation in the final layer." (Results and Discussion)
- The softmax function transforms model outputs into probabilities across five DR classes, "from 'no retinopathy' (class 0) to 'severe stage' (class 4)" (section 3, formula 3).

**Strength of Relevance:** **Core**

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-06]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C1; C2
- **Concept(s) used:** Deep learning for DR diagnosis; CNN; image processing; literature context
- **Research question addressed:** RQ1, RQ3

**Function in dissertation:**
- Theoretical grounding
- Literature gap evidence

**Extracted Content (Strict Extraction Only):**
- The literature review discusses use of image processing methods for deep learning models aimed at DR diagnosis, including "image enhancement, segmentation for separating blood vessels and lesions, and feature extraction such as structure and color" (Introduction, paragraph 2, discussing references [1–3]).
- Reference [4] demonstrates "the importance of early DR detection to prevent vision deterioration" and focuses on "the effectiveness of various image preprocessing methods such as Sobel, Winer, Gauss, and non-local mean filters, which improve image quality by reducing noise and increasing clarity for accurate analysis" (Introduction, paragraph on [4]).
- "The combination of preprocessing and CNN prediction methods increases image quality and prediction accuracy" (Introduction, discussing references [6–7]).
- "Integration of image preprocessing methods and deep learning models significantly improves diabetic retinopathy prediction and diagnosis accuracy" (Introduction, final sentence of literature review).

**Strength of Relevance:** **Supporting**

---

**[Extraction Block ID: EB-LC-Yesmukhamedov-2025-SELF-07]**

**Relevant to:**
- **Dissertation claim(s) supported or challenged:** C3 (Improves classification and reduces overfitting); C5 (Applicable pipeline)
- **Concept(s) used:** Cohen's Kappa; quadratic weights; clinical significance of classification errors
- **Research question addressed:** RQ2

**Function in dissertation:**
- Methodological precedent
- Conceptual clarification

**Extracted Content (Strict Extraction Only):**
- Cohen's Kappa metric with quadratic weights was used: κ = 1 − (Σ_{i,j} w_{i,j} · O_{i,j}) / (Σ_{i,j} w_{i,j} · E_{i,j}), with quadratic weights w_{i,j} = (i−j)² / (C−1)² (section 6, formulas 6–7).
- "Quadratic weights ensured that errors between adjacent classes (e.g., 2 and 3) are penalized less than errors between distant classes (e.g., 0 and 4). This has clinical significance, as errors in transitions between mild stages are less critical than missing severe cases." (section 6)
- The Adam optimizer provided "adaptive gradient control that contributed to fast and stable convergence," which is "extremely important when analyzing complex fundus images where gradients may be sparse due to data heterogeneity (e.g., small lesions like microaneurysms are rare)" (section 5).

**Strength of Relevance:** **Supporting**

---

## IV. RELATIONAL POSITIONING

- **Supports which dissertation claims:**
  - **C1:** The source demonstrates a working integration of preprocessing methods (augmentation, normalization, contrast enhancement) with the EfficientNetB0 CNN architecture for automated five-class DR classification, directly instantiating the unified system concept.
  - **C2:** The source provides empirical evidence that preprocessing methods (augmentation, normalization) improve model performance, with fine-tuning yielding 10 percentage point improvements in precision and 14 percentage point improvements in recall over the frozen-layer baseline.
  - **C3:** The source documents overfitting in Method 1 and demonstrates that fine-tuning combined with early stopping and callbacks reduces overfitting while improving classification performance.
  - **C5:** Cross-validation results and the use of EfficientNetB0 (a computationally efficient architecture) support the applicability of the approach in resource-aware screening contexts.

- **Contradicts which claims (if any):**
  - Partial tension with **C3** regarding overfitting reduction: even Method 2 shows an Accuracy of 0.80 for both methods (no improvement), and the source acknowledges remaining overfitting concerns requiring additional data and regularization. The source does not fully demonstrate that overfitting is resolved, only reduced.

- **Extends which conceptual axis:**
  - Extends the **preprocessing-as-performance-driver axis** by empirically comparing two transfer learning adaptation strategies (frozen vs. fine-tuned) under the same preprocessing regime.
  - Extends the **transfer learning methodology axis** by applying EfficientNetB0 specifically to DR classification and comparing layer-freezing strategies.

- **Overlaps with which other sources (if known):**
  - Overlaps thematically with references [1–3] (image processing for DR deep learning models), [4] (preprocessing filter methods for DR), and [6–7] (combination of preprocessing and CNN methods) as cited in the source's own literature review.
  - Overlaps with reference [2] (Demin et al., 2023) on the topic of neural networks for analyzing fundus images in the context of laser coagulation treatment for DR, which is directly relevant to the dissertation's focus on laser coagulation support systems.

---

## V. REUSABILITY CONTROL

- **What can be reused in dissertation drafting:**
  - The comparative results between frozen-layer and fine-tuning approaches (specific Precision, Recall, Accuracy values) can be directly cited as the dissertant's own published empirical findings.
  - The mathematical formulations of convolution (formula 2), softmax (formula 3), cross-entropy loss (formula 4), Adam optimizer (formula 5), and Cohen's Kappa (formulas 6–7) can be referenced as methodological descriptions from prior published work.
  - The dataset characteristics and class distributions can be referenced as foundational data descriptions.
  - The literature review content (Introduction) can be cited for positioning within the broader DR diagnosis research landscape.

- **What must be reformulated:**
  - The Abstract and Conclusion sections contain high-level claims and summary statements that overlap closely with likely dissertation chapter summaries; these must be carefully reformulated to avoid redundancy.
  - The preprocessing pipeline description (Dataset section, Figure 3 commentary) will require expansion and differentiation in the dissertation to reflect the dissertation's more comprehensive preprocessing approach (including CLAHE, which is not mentioned in this source).
  - The Results and Discussion framing must be distinguished from the dissertation's experimental framework (the dissertation uses a different baseline architecture with 4 conv layers, 32–256 filters, and a different image resolution of 256×256 vs. 512×512).

- **Risk of self-plagiarism:**
  - **HIGH RISK — Source is authored by the dissertant (Yesmukhamedov N.S. is first author).** All reused content must be explicitly cited as prior own work. Direct textual reuse must be disclosed and minimized. Conceptual and methodological reuse must be framed as building upon prior published results. The dissertation should clearly delineate how the dissertation's experimental setup (4 conv layers, CLAHE, 256×256 vs. 512×512 resolution, APTOS 2019 dataset with 3,662 images) differs from and extends the results reported in this source (EfficientNetB0, 35,126 training images, no explicit CLAHE mention).

---

## VI. TERMINOLOGY INDEX

| Term | Definition/Usage in Source | Corresponding Dissertation Usage | Stability Note |
|---|---|---|---|
| **Diabetic retinopathy (DR)** | "A common eye disease in patients with diabetes and one of the main causes of vision loss" (Introduction, paragraph 1); classified into 5 stages (0–4) | Same definition and 5-class staging system (DR 0–4) | Aligned |
| **EfficientNetB0** | Pre-trained CNN architecture used via transfer learning with two adaptation strategies (frozen layers and fine-tuning) | Not used in the dissertation's own experiments (dissertation uses custom 4-layer CNN); referenced as prior work | **Discrepancy:** Dissertation uses custom CNN, not EfficientNetB0. Must be positioned as a different architectural choice in the dissertant's prior work. |
| **Data augmentation** | "Rotation, scaling, shifting, brightness changes" used "to improve model generalization and increase their volume and variability" (Materials and Methods) | Same concept: rotation, scaling, augmentation; dissertation also includes CLAHE | Partially aligned; dissertation extends augmentation to include CLAHE |
| **Transfer learning** | "Transfer Learning approach based on pre-trained models" with frozen base layers and fine-tuning (Results and Discussion) | Referenced in the dissertation as a known approach; dissertation's own model is trained from scratch | Aligned in concept; differs in application |
| **Fine-tuning** | "Opening upper layers after initial training" for additional model adaptation (Results and Discussion) | Same conceptual usage | Aligned |
| **Cross-entropy loss (CrossEntropyLoss)** | Loss function used "to minimize the discrepancy between true class labels and predicted probabilities" for imbalanced multi-class classification (section 4, formula 4) | Same loss function used in the dissertation's CNN training pipeline | Aligned |
| **Cohen's Kappa** | Metric with "quadratic weights" used to assess agreement between predictions and ground truth, where "errors between adjacent classes are penalized less than errors between distant classes" (section 6) | Used in the dissertation as an evaluation metric | Aligned |
| **Early stopping** | "Stop training if Cohen's Kappa metric on the validation set did not improve for k epochs, preventing overfitting" (section 7) | Dissertation uses EarlyStopping callback with same purpose | Aligned |
| **Softmax** | Function transforming model outputs into "probabilities of belonging to each class" for 5-class DR classification (section 3, formula 3) | Dissertation uses "Softmax 5-class" in final layer | Aligned |
| **Class imbalance** | Training set dominated by Class 0 (73.5%); severe stages represent 2.5% and 2.0%; addressed through weighted loss functions and augmentation (Data Processing section) | Same problem acknowledged in the dissertation; addressed through augmentation and preprocessing | Aligned |
| **Fundus images** | Retinal photographs used for DR diagnosis, requiring preprocessing (contrast enhancement, noise removal, normalization) for automated analysis | Same usage throughout the dissertation | Aligned |
