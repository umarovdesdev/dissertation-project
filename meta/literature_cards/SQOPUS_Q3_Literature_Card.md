# LITERATURE CARD

---

## I. SOURCE IDENTIFICATION

- **Unique ID:** `SQOPUS_Q3`
- **Full Bibliographic Citation:** Sapakova, S., Yesmukhamedov, N., & Sapakov, A. (2025). Development of an image quality enhancement approach for diabetic retinopathy diagnosis. *Eastern-European Journal of Enterprise Technologies*, 4(9(136)), 79–88. https://doi.org/10.15587/1729-4061.2025.335570
- **Type of Publication:** Journal article / Empirical study (primary: journal article, published in a Scopus Q3-indexed journal; the work is empirical in nature, involving experimental model training and evaluation).
- **Year:** 2025
- **Research Domain Classification:** Computer Science > Medical Image Analysis > Diabetic Retinopathy > Preprocessing-CNN Integration

---

## II. GLOBAL SOURCE ANALYSIS

### II.1. Central Thesis

The central thesis, as explicitly stated by the authors, is formulated in the aim of the study: "The aim of the study is the development of an approach that combines advanced image enhancement techniques with convolutional neural networks (CNNs) for automated diabetic retinopathy diagnosis. The emphasis is on integrating methods that have not been previously combined, focusing on improving robustness and accuracy under variable image quality and limited computational resources." (p. 81)

A more concise formulation appears in the abstract: "The core problem addressed is the suboptimal performance of baseline CNNs in identifying DR stages from medical imagery." The thesis is that integrating advanced preprocessing techniques (resizing, normalization, CLAHE, data augmentation) with CNN architecture yields significantly improved classification performance compared to a baseline CNN without such preprocessing. (p. 79)

### II.2. Research Problem Addressed

The specific problem addressed is stated as follows: "the limited generalization ability of neural networks under variable image quality, the absence of a unified framework integrating image enhancement and classification in an optimized, resource-efficient manner, and the lack of standardized, annotated datasets for benchmarking." (p. 81)

The problem is framed as both **methodological** (absence of a unified preprocessing-classification framework) and **empirical** (demonstrating that preprocessing integration improves CNN accuracy under constrained conditions). The authors explicitly frame the issue as the "suboptimal performance of baseline CNNs in identifying DR stages from medical imagery" (p. 79), attributing this to the dependence of model accuracy on image quality: "In real clinical scenarios, retinal images often suffer from poor resolution, uneven illumination, and various types of noise. These factors significantly impair the generalizability of neural network models." (p. 79)

### II.3. Methodology

**Theoretical framework:** The theoretical framework is not formally named or cited as a unified theory. It is implicitly grounded in convolutional neural network theory (feature extraction via convolution and pooling, classification via fully connected layers) and image processing theory (contrast enhancement, spatial normalization). The authors reference the general CNN architecture (input → convolution → pooling → fully connected → output) as the structural basis (p. 83, Fig. 3).

**Methods used:**

- **Image preprocessing:**
  - Resizing: all images resized to 256 × 256 pixels for the baseline model and 512 × 512 pixels using cubic interpolation for the enhanced model (pp. 81, 83)
  - Normalization: pixel values normalized to [0, 1] range (p. 82)
  - CLAHE (Contrast Limited Adaptive Histogram Equalization): applied using OpenCV with clip limit of 2.0 and grid size of 8 × 8 (p. 83)
  - Data augmentation: horizontal and vertical flips, random rotations (±15°), zoom (±10%), and brightness variation (p. 83)
  - Image super-resolution: cubic interpolation via OpenCV to upscale images to 512 × 512 pixels (p. 83)

- **CNN architectures:**
  - *Baseline model:* Two convolutional blocks (32 filters, then 64 filters), both using 3 × 3 kernels and ReLU activation, followed by max-pooling (2 × 2); fully connected layer with 128 neurons (ReLU); output layer with single neuron and sigmoid activation for binary classification; optimized with Adam optimizer and binary cross-entropy loss; input size 256 × 256; batch size 32; 30 epochs (p. 83)
  - *Enhanced model:* Four convolutional layers with increasing filter sizes (32, 64, 128, 256), each with ReLU activation and max-pooling; batch normalization layers; dropout layers (rate = 0.4) after dense layers; two dense layers followed by softmax output layer (5-class); compiled with Adam optimizer (learning rate = 0.0001) and categorical cross-entropy loss; batch size 32; early stopping applied; convergence within 35–40 epochs (p. 83)

- **Implementation:** Both models built using Keras with TensorFlow backend; CLAHE applied using OpenCV (p. 83)

**Data sources:**

- APTOS 2019 Blindness Detection dataset: 3,662 labeled training samples and 1,928 unlabeled test samples; five DR stages (0 = no DR, 1 = mild, 2 = moderate, 3 = severe, 4 = proliferative DR) (p. 81)
- Supplementary retinal images from local medical centers, manually labeled by certified ophthalmologists; not publicly available due to privacy agreements (pp. 81, 83)
- The enhanced model was trained on a dataset of 25,000 labeled retinal images, split 80% training / 10% validation / 10% testing (p. 83)
- The authors note the dataset is "not publicly available due to ethical considerations" (p. 79) and "privacy agreements" (p. 83)

**Analytical approach:**

- Metrics: accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix analysis (p. 83)
- Comparison between baseline and enhanced models across training/validation accuracy and loss over 10 epochs (Table 2, p. 86)
- ROC curve analysis with AUC computation (Fig. 8, p. 85)
- Classification reports with per-class precision, recall, and F1-score (Figs. 4–5, p. 84)

### II.4. Conceptual Contributions

The source does not introduce new technical terms or formal theoretical frameworks. It uses established concepts (CLAHE, CNN, data augmentation, ROC-AUC, etc.) without modification.

The principal conceptual contribution is the articulation of a *synergy between preprocessing and CNN architecture*: "A distinctive feature of the results lies in the synergy between preprocessing and CNN architecture, which enabled significantly improved classification performance even under hardware constraints." (p. 79) This "synergy" is not formally defined but is used to describe the combined effect of the preprocessing pipeline and CNN classification as exceeding the sum of their individual contributions.

The authors also frame the concept of a *modular pipeline*: "A promising approach to address current limitations in automated DR diagnosis is the development of modular pipelines that combine lightweight image enhancement with transfer learning using pre-trained CNNs." (p. 81) However, transfer learning is not implemented in this study; it is referenced as a future direction.

### II.5. Empirical Contributions

**Data generated/analyzed:**

- The authors trained and evaluated two CNN models on retinal fundus image datasets as described above.

**Principal quantitative findings:**

- Image enhancement techniques (resizing and augmentation) improved validation accuracy from 71% to 86% (p. 83)
- Enhanced model achieved 94.5% training accuracy and 91.3% validation accuracy, converging within 35–40 epochs (p. 84)
- With preprocessing (CV2/CLAHE), accuracy reached 91% (precision 0.90/0.93, recall 0.93/0.90, F1-score 0.91/0.91 for classes 0 and 1 respectively) vs. 88% without preprocessing (precision 0.91/0.85, recall 0.83/0.92, F1-scores 0.87/0.89) (p. 84)
- ROC-AUC = 0.9638 (p. 84)
- Enhanced model by Epoch 9: validation accuracy 93.41%, validation loss 0.1833 vs. original model validation accuracy 91.71%, validation loss 0.2288 (Table 2, p. 86)
- Original model loss started at ~0.67 and stabilized around 0.27–0.30; enhanced model loss started at ~0.23 and stabilized around 0.18–0.20 (p. 84)
- Processing time: 1s 108ms/step (with preprocessing) vs. 8s 986ms/step (without preprocessing) (p. 84)
- Conclusion reports: precision (0.82), recall (0.85), F1-score (0.83); validation loss reduced from 0.89 to 0.45 (p. 87)

**Comparisons made:**

- Baseline CNN (no preprocessing, 256 × 256) vs. Enhanced CNN (preprocessing pipeline, 512 × 512): the enhanced model consistently outperformed across all epochs (Table 2, p. 86)
- With vs. without CV2 preprocessing (Figs. 4–5, p. 84)

### II.6. Limitations Acknowledged by the Author

1. "Dataset-specific training limits the model's generalization. The model was trained and validated on a specific dataset, which may not fully represent the diversity of retinal images encountered in practice." (p. 86)
2. "Hardware constraints prevented longer training durations. Due to overheating during extended training, the number of epochs was limited, potentially restricting the full learning potential of the model." (p. 86)
3. "Controlled imaging conditions in the dataset may differ from varied real-world scenarios, impacting model adaptability to noise, occlusions, or varying illumination levels." (p. 86)
4. "The model's interpretability could be further improved through explainability tools like Grad-CAM or SHAP to enhance clinical trust." (p. 86)
5. "The system currently functions as a black box without incorporating contextual patient data (e.g., medical history), which might limit diagnostic richness." (pp. 86–87)
6. "The model was trained primarily on high-quality images from a private dataset and APTOS 2019, which does not fully capture the variability of retinal images in real clinical practice." (p. 86)

### II.7. Implicit Assumptions

1. **The APTOS 2019 classification scheme (5-class) is clinically valid and sufficient for DR staging.** Textual basis: The authors adopt the APTOS labeling without discussing its clinical validity or comparing it to alternative grading systems (e.g., ETDRS). The five-stage scheme is used as ground truth throughout (p. 81).

2. **Cubic interpolation for upscaling does not introduce diagnostically relevant artifacts.** Textual basis: The authors state cubic interpolation was "chosen for its ability to preserve spatial details" (p. 83) but present no evidence or analysis to verify that upscaling from original resolution to 512 × 512 does not introduce misleading features.

3. **Binary classification performance (with/without preprocessing comparison in Figs. 4–5) is representative of the model's multiclass capability.** Textual basis: The confusion matrix and classification report in Figs. 4–5 show binary classification (classes 0 and 1, p. 84), while the enhanced model is described as a 5-class softmax classifier (p. 83). The relationship between the binary and multiclass evaluations is not explicitly addressed.

4. **The supplementary clinical dataset from local medical centers is compatible with APTOS in terms of image characteristics.** Textual basis: The authors state images were "manually labeled by certified ophthalmologists to ensure consistency with the APTOS classification scheme" (p. 81), but no analysis of distributional similarity between the two sources is provided.

---

## III. EXTRACTION BLOCKS

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-01

**RELEVANT TO:**
- **Dissertation claim(s) supported:** "The effectiveness of CNN models in DR diagnosis depends primarily on the quality of input images, not solely on architectural complexity."
- **Concept(s) used:** Image preprocessing pipeline (resizing, normalization, CLAHE, augmentation); preprocessing-CNN synergy
- **Dissertation section(s):** Chapter 1 (critical analysis of existing DR systems); Chapter 3 (formalization of the unified preprocessing pipeline); Chapter 4 (experiments comparing baseline vs. enhanced CNN)
- **Research question addressed:** Does integrating advanced preprocessing with CNN classification improve diagnostic accuracy?

**FUNCTION IN DISSERTATION:**
- [x] **Empirical support** — Provides direct experimental evidence (from the dissertation author's own published work) that preprocessing raises validation accuracy from 71% to 86% and from 88% to 91%.
- [x] **Methodological precedent** — Establishes the specific preprocessing pipeline (resize, normalize, CLAHE, augment) as a validated approach for the dissertation's methodology chapter.

**EXTRACTED CONTENT:**
- "Image enhancement techniques (resizing and augmentation) improved validation accuracy from 71% to 86%, highlighting the importance of proper preprocessing." (p. 83)
- "The enhanced model outperformed the original, achieving a validation accuracy of 91% compared to 88% for the baseline, and demonstrating reduced loss during both training and validation." (p. 79)
- "This improvement is attributed to the optimized input image quality and increased variability in the training set, which enhanced the model's ability to generalize and avoid overfitting." (p. 79)
- "A distinctive feature of the results lies in the synergy between preprocessing and CNN architecture, which enabled significantly improved classification performance even under hardware constraints." (p. 79)

**STRENGTH OF RELEVANCE:** **Core** — This block provides the central empirical evidence for the dissertation's primary claim that preprocessing quality determines CNN diagnostic performance.

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-02

**RELEVANT TO:**
- **Dissertation claim(s) supported:** "A unified preprocessing pipeline (resize, normalization, CLAHE, augmentation) integrated with CNN classification significantly improves diagnostic accuracy and generalization under variable image quality and limited computational resources."
- **Concept(s) used:** CLAHE parameters, image resizing via cubic interpolation, data augmentation techniques, pixel normalization
- **Dissertation section(s):** Chapter 2 (mathematical foundations of CLAHE, spatial filtering); Chapter 3 (modified CLAHE algorithm, formalization of unified preprocessing pipeline)
- **Research question addressed:** What specific preprocessing techniques, and with what parameters, are most effective?

**FUNCTION IN DISSERTATION:**
- [x] **Methodological precedent** — Specifies exact CLAHE parameters (clip limit 2.0, grid size 8 × 8), augmentation techniques, and normalization range used in the published pipeline.
- [x] **Empirical support** — Demonstrates quantitative impact of each preprocessing stage on model convergence and accuracy.

**EXTRACTED CONTENT:**
- "CLAHE was applied using OpenCV with a clip limit of 2.0 and a grid size of 8 × 8." (p. 83)
- "For image super-resolution, cubic interpolation via OpenCV was used to upscale images to 512 × 512 pixels before input to the enhanced CNN model." (p. 83)
- "All images were resized to 256 × 256 pixels and normalized to the range [0, 1]." (pp. 81–82)
- "Techniques included horizontal and vertical flips, random rotations (±15°), zoom (±10%), and brightness variation." (p. 83)
- "CLAHE improves local contrast, especially in darker regions of the fundus, enhancing the visibility of pathological features without introducing artifacts." (p. 83)
- The enhanced model's loss "begins lower (~0.23) and converges much earlier, stabilizing around 0.18–0.20" compared to the original model whose loss "starts high (~0.67) and decreases gradually but stabilizes around 0.27–0.30." (p. 84)

**STRENGTH OF RELEVANCE:** **Core** — This block documents the exact technical parameters of the preprocessing pipeline that the dissertation proposes as its methodological contribution.

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-03

**RELEVANT TO:**
- **Dissertation claim(s) supported:** "A unified preprocessing pipeline... integrated with CNN classification significantly improves diagnostic accuracy and generalization."
- **Concept(s) used:** CNN architecture design (convolutional layers, batch normalization, dropout, softmax classification); Adam optimizer; categorical cross-entropy
- **Dissertation section(s):** Chapter 3 (baseline and enhanced CNN architectures); Chapter 4 (experimental results)
- **Research question addressed:** What CNN architecture, combined with preprocessing, achieves optimal DR classification?

**FUNCTION IN DISSERTATION:**
- [x] **Methodological precedent** — Documents the full architecture of both baseline and enhanced CNN models used in the dissertation's experimental framework.
- [x] **Empirical support** — Reports training/validation accuracy and loss trajectories demonstrating the enhanced model's superiority.

**EXTRACTED CONTENT:**
- Baseline model: "two convolutional blocks: the first with 32 filters and the second with 64 filters, both using 3 × 3 kernels and ReLU activation, followed by max-pooling layers with 2 × 2 pooling windows. A fully connected layer with 128 neurons and ReLU activation preceded the output layer, which contained a single neuron with a sigmoid activation function, enabling binary classification." (p. 83)
- Enhanced model: "four convolutional layers with increasing filter sizes (32, 64, 128, 256), each followed by ReLU activation and max-pooling for spatial downsampling. Batch normalization layers were included to stabilize training, while dropout layers (rate = 0.4) after the dense layers reduced overfitting." Compiled with "Adam optimizer (learning rate = 0.0001)" and "categorical cross-entropy loss." (p. 83)
- "Training was performed on a dataset of 25,000 labeled retinal images, split into 80% training, 10% validation, and 10% testing." (p. 83)
- The enhanced model achieved "94.5% training accuracy and 91.3% validation accuracy" converging within "35–40 epochs." (p. 84)
- Table 2 (p. 86): By Epoch 9, the enhanced model reached validation accuracy of 93.41% and validation loss of 0.1833, compared to the original model's 91.71% and 0.2288 respectively.

**STRENGTH OF RELEVANCE:** **Core** — Provides the complete architectural specification and training results of the CNN models central to the dissertation.

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-04

**RELEVANT TO:**
- **Dissertation claim(s) supported:** Improved diagnostic performance validated through comprehensive metrics.
- **Concept(s) used:** ROC-AUC, precision, recall, F1-score, confusion matrix
- **Dissertation section(s):** Chapter 3 (evaluation framework); Chapter 4 (experimental results); Chapter 5 (reliability validation)
- **Research question addressed:** How is the diagnostic performance of the integrated system evaluated and validated?

**FUNCTION IN DISSERTATION:**
- [x] **Empirical support** — Provides the full set of evaluation metrics (ROC-AUC, precision, recall, F1-score, confusion matrix) that validate the proposed system.

**EXTRACTED CONTENT:**
- "The ROC curve highlights the model's excellent performance in distinguishing between positive and negative classes, with an AUC value of 0.9638." (p. 84)
- With preprocessing: "accuracy of 91%, with precision of 0.90, recall of 0.93, and an F1-score of 0.91 for class 0 (diabetic retinopathy present) and precision of 0.93, recall of 0.90, and an F1-score of 0.91 for class 1 (diabetic retinopathy absent)." (p. 84)
- Without preprocessing: "lower accuracy of 88%, and precision values of 0.91 for class 0 and 0.85 for class 1. The recall for class 0 is 0.83, while for class 1, it is 0.92, leading to F1-scores of 0.87 and 0.89, respectively." (p. 84)
- Confusion matrix with preprocessing: [[105, 8], [12, 106]] on 231 images (Fig. 4, p. 84)
- Confusion matrix without preprocessing: [[94, 19], [9, 109]] on 231 images (Fig. 5, p. 84)
- Conclusion reports: "precision (0.82), recall (0.85), and F1-score (0.83)" (p. 87)

**STRENGTH OF RELEVANCE:** **Core** — These metrics are the evidentiary basis for claiming the system's diagnostic reliability and will be directly referenced in the dissertation's evaluation chapters.

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-05

**RELEVANT TO:**
- **Dissertation claim(s) supported:** "The proposed approach offers a reproducible, resource-efficient pipeline suitable for deployment in resource-limited healthcare environments."
- **Concept(s) used:** Hardware constraints, computational resource limitations, clinical deployment feasibility
- **Dissertation section(s):** Chapter 6 (architecture for resource-limited environments); Chapter 5 (limitations)
- **Research question addressed:** Can the proposed system be practically deployed in resource-constrained settings?

**FUNCTION IN DISSERTATION:**
- [x] **Empirical support** — Documents the practical constraint of hardware overheating and limited epochs, which is directly relevant to resource-limited deployment arguments.
- [x] **Conceptual clarification** — Establishes that the enhanced model achieves improved results "even under hardware constraints" (p. 79), supporting the dissertation's resource-efficiency claims.

**EXTRACTED CONTENT:**
- "A distinctive feature of the results lies in the synergy between preprocessing and CNN architecture, which enabled significantly improved classification performance even under hardware constraints." (p. 79)
- "These limitations suggest that further gains are possible with extended computational resources and access to larger datasets." (p. 79)
- "Hardware constraints prevented longer training durations. Due to overheating during extended training, the number of epochs was limited, potentially restricting the full learning potential of the model." (p. 86)
- "Computational constraints are simulated by limiting the model complexity and image resolution to reflect resource-limited clinical environments." (p. 81)
- "Deployment challenges such as real-time inference on edge devices or in mobile applications should be addressed, especially for screening in rural or resource-constrained areas." (p. 87)

**STRENGTH OF RELEVANCE:** **Supporting** — Provides empirical context and acknowledged constraints for the dissertation's Chapter 6 claims about resource-limited deployment, though deployment itself is not experimentally validated in this source.

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-06

**RELEVANT TO:**
- **Dissertation claim(s) challenged or contextualized:** The source identifies gaps in the literature that remain partially unresolved by the source itself.
- **Concept(s) used:** Generalization, external validation, multi-center data, domain adaptation
- **Dissertation section(s):** Chapter 1 (critical analysis of existing systems); Chapter 5 (limitations, cross-database generalization)
- **Research question addressed:** What are the current limitations of automated DR diagnosis systems, and what remains unresolved?

**FUNCTION IN DISSERTATION:**
- [x] **Critical counterpoint** — The source's own acknowledged limitations (dataset specificity, lack of external validation, imaging variability) serve as critical counterpoints that the dissertation must address or inherit transparently.

**EXTRACTED CONTENT:**
- "The model was trained primarily on high-quality images from a private dataset and APTOS 2019, which does not fully capture the variability of retinal images in real clinical practice." (p. 86)
- "In real-world conditions, images may be acquired using different equipment, under variable lighting, with artifacts (glare, shadows, partial occlusion by eyelids or eyelashes), patient movement, low resolution, or digital noise, which may reduce the model's accuracy and limit its generalization ability." (p. 86)
- "To improve robustness and reliability, it is necessary to expand the training set with multi-center data, implement domain adaptation methods, use model ensembles, and test and integrate additional architectures (e.g., ResNet, EfficientNet)." (p. 86)
- "The model's interpretability could be further improved through explainability tools like Grad-CAM or SHAP to enhance clinical trust." (p. 86)

**STRENGTH OF RELEVANCE:** **Core** — These limitations define the research frontier the dissertation must navigate, and since this is a self-publication, the dissertation must demonstrate advancement beyond these acknowledged gaps.

---

### Extraction Block EB-LC-SAPAKOVA-2025-01-07

**RELEVANT TO:**
- **Dissertation claim(s) supported:** Literature gap identification supporting the need for integrated preprocessing-CNN research.
- **Concept(s) used:** Literature synthesis, research gaps in DR preprocessing and deep learning
- **Dissertation section(s):** Chapter 1 (critical analysis of existing systems, literature review)
- **Research question addressed:** What is the current state of research on preprocessing-CNN integration for DR diagnosis?

**FUNCTION IN DISSERTATION:**
- [x] **Theoretical grounding** — The literature review (pp. 79–81) systematically identifies gaps in 20 prior studies, providing the justification structure for the dissertation's problem statement.

**EXTRACTED CONTENT:**
- On [1]: "important aspects such as transparent description of preprocessing and training, dataset details, external validation, and comparison with advanced architectures remain unexplored." (pp. 79–80)
- On [5]: "CLAHE proving most effective under poor lighting. However, the work does not address how these enhancements influence downstream classification accuracy." (p. 80)
- On [7]: "the effect of such enhancement on classification accuracy remains untested, limiting its clinical value." (p. 80)
- On [14]: "CLAHE was combined with GANs to increase classification accuracy from 95.4% to 98%." However, "these studies lack a systematic evaluation against alternative preprocessing methods and fail to address real-time applicability." (p. 80)
- On [17]: "CNN optimization without explicit preprocessing, achieving 91% accuracy. Yet, the absence of enhancement makes it difficult to assess robustness in poor-quality images." (p. 80)
- Summary of gaps: "the limited generalization ability of neural networks under variable image quality, the absence of a unified framework integrating image enhancement and classification in an optimized, resource-efficient manner, and the lack of standardized, annotated datasets for benchmarking." (p. 81)

**STRENGTH OF RELEVANCE:** **Supporting** — Provides the literature analysis backdrop that justifies the dissertation's research direction, but the dissertation's own literature review should be broader and more current.

---

## IV. RELATIONAL POSITIONING

- **Supports which dissertation claims:**
  1. *Preprocessing quality determines CNN diagnostic performance:* Directly supported by the 71% → 86% accuracy improvement from preprocessing alone (p. 83) and the 88% → 91% improvement of the enhanced over baseline model (p. 79).
  2. *A unified preprocessing pipeline integrated with CNN improves accuracy and generalization:* Supported by the complete pipeline specification and comparative evaluation across epochs (Table 2, p. 86) and ROC-AUC of 0.9638 (p. 84).
  3. *The approach is suitable for resource-limited environments:* Partially supported by the demonstration that improved results were achieved "even under hardware constraints" (p. 79), though no formal deployment testing is reported.

- **Contradicts which claims:** No direct contradictions identified. However, the source's conclusion section reports precision (0.82), recall (0.85), and F1-score (0.83) (p. 87), which are lower than the values reported in the main results section (precision 0.90/0.93, recall 0.93/0.90, F1-score 0.91) (p. 84). This internal inconsistency within the source does not contradict the dissertation claims but requires careful handling when citing specific metric values.

- **Extends which conceptual axis:** Extends the methodological axis of preprocessing-CNN integration for medical image classification by providing a complete, specified, and evaluated pipeline with documented CLAHE parameters, augmentation strategies, and CNN architectural details.

- **Overlaps with which other sources:** Based on the source's own reference list, significant methodological overlap exists with:
  - [14] Deshpande (2023): CLAHE combined with GANs for DR classification
  - [17] Bhoopal et al. (2024): ResNet50 with CLAHE-GAN for DR detection
  - [18] Banupriya & Kalaivani (2022): hybrid image filters and enhanced CLAHE
  - [20] Mahender et al. (2023): optimized CNN achieving 91% accuracy without preprocessing
  - [5] Mohd Sharif et al. (2024): contrast enhancement and optimization for DR fundus images

---

## V. REUSABILITY CONTROL

### What can be reused in dissertation drafting:

- **Quantitative results:** All numerical performance values (accuracy, precision, recall, F1-score, ROC-AUC, loss values) from Table 2 (p. 86), Figs. 4–5 (p. 84), and Fig. 8 (p. 85) can be directly cited with proper attribution.
- **Technical specifications:** CLAHE parameters (clip limit 2.0, grid size 8 × 8), augmentation parameters (±15° rotation, ±10% zoom), optimizer settings (Adam, lr = 0.0001), and CNN layer specifications can be referenced as the published basis for the dissertation's methodology.
- **Literature gap analysis:** The structured review of 20 prior works (pp. 79–81) can be cited as a published foundation, though the dissertation must extend this review.
- **Confusion matrices and classification reports:** The specific values from Figs. 4–5 can be cited.
- **Training/validation curves:** The epoch-by-epoch comparison data in Table 2 can be referenced.

### What must be reformulated:

- **Methodology descriptions:** The detailed descriptions of the preprocessing pipeline and CNN architecture (pp. 81–83) overlap substantially with what the dissertation will present in Chapters 3–4. These must be significantly restructured and expanded in the dissertation, not reproduced.
- **Literature review content:** The gap analysis in Section 2 (pp. 79–81) must be substantially expanded, updated, and reformulated for the dissertation's Chapter 1, not copied.
- **Discussion and interpretation:** The discussion section (pp. 86–87) presents interpretations that the dissertation must rewrite in the broader context of the full doctoral work.
- **Abstract and introduction framing:** The problem statement and aim formulations must be rewritten for the dissertation context.

### Risk of self-plagiarism:

**⚠️ HIGH PRIORITY — Self-publication flag.** The dissertation author (Yesmukhamedov N.) is a co-author of this publication. The following considerations apply:

1. **Overlapping sections:**
   - The preprocessing pipeline description (pp. 81–83) overlaps with dissertation Chapter 3 (methodology).
   - The CNN architecture specification (p. 83) overlaps with dissertation Chapters 3–4.
   - The experimental results and evaluation (pp. 83–86, Table 2) overlap with dissertation Chapter 4.
   - The literature review (pp. 79–81) overlaps with dissertation Chapter 1.

2. **Required textual and structural modifications:**
   - All methodological descriptions must be substantially expanded in the dissertation with additional mathematical formalization, implementation details, and justification not present in the article.
   - Results must be presented in the dissertation with extended analysis, additional experiments (e.g., ablation studies, cross-database validation on STARE), and comparisons with additional architectures (EfficientNetB0, ResNet50) that go beyond the article's scope.
   - The literature review must be comprehensively expanded with more sources and deeper analysis.
   - Discussion must be reframed within the full six-chapter dissertation structure.

3. **Recommended citation approach:**
   - In the dissertation, cite the publication transparently, e.g.: "As previously reported by the author in [Sapakova, Yesmukhamedov & Sapakov, 2025], the enhanced model achieved a validation accuracy of 91%..."
   - When describing the methodology, reference the publication as the preliminary study: "The preprocessing pipeline was initially proposed and validated in our earlier work [citation]; in this dissertation, we extend and formalize this approach by..."
   - Use explicit language marking the relationship: "Building upon the findings of our published study [citation], this dissertation..."

4. **Publisher/license implications:**
   - The article is published under **Creative Commons CC BY license** (noted on p. 79: "This is an open access article under the Creative Commons CC BY license"). This permits reuse, adaptation, and redistribution provided appropriate credit is given. However, CC BY licensing does not exempt the author from institutional anti-plagiarism requirements. The dissertation must demonstrate sufficient intellectual transformation beyond the article.

---

## VI. TERMINOLOGY INDEX

| Term | Definition or Usage in Source | Page Reference | Must Remain Stable? | Notes |
|------|------------------------------|----------------|---------------------|-------|
| Diabetic retinopathy (DR) | "one of the most severe complications of diabetes mellitus and is the leading cause of preventable vision loss among working-age adults worldwide" | p. 79 | Yes | Core domain term |
| Fundus images | Retinal images used as input for DR diagnosis; acquired via fundoscopy | p. 79 | Yes | Used interchangeably with "retinal images" |
| CLAHE (Contrast Limited Adaptive Histogram Equalization) | Applied with clip limit of 2.0 and grid size of 8 × 8; "improves local contrast, especially in darker regions of the fundus, enhancing the visibility of pathological features without introducing artifacts" | pp. 82–83 | Yes | Parameters must remain consistent across dissertation |
| CNN (Convolutional Neural Network) | Architecture consisting of "input, convolutional and pooling layers for feature extraction, and fully connected layers for classification" | p. 83 | Yes | General architecture term |
| Data augmentation | "horizontal and vertical flips, random rotations (±15°), zoom (±10%), and brightness variation" | p. 83 | Yes | Specific parameter values must be consistent |
| Image normalization | Pixel values normalized to [0, 1] range | pp. 81–82 | Yes | Standard preprocessing step |
| Cubic interpolation | Method used for image super-resolution/upscaling to 512 × 512 | p. 83 | Yes | Specific to the enhanced model pipeline |
| Batch normalization | Layers "included to stabilize training" in the enhanced model | p. 83 | Yes | Standard CNN regularization term |
| Dropout | Rate = 0.4; applied "after the dense layers" to reduce overfitting | p. 83 | Yes | Parameter must be consistent |
| Adam optimizer | Used with learning rate = 0.0001 for the enhanced model | p. 83 | Yes | Hyperparameter must be consistent |
| Categorical cross-entropy | Loss function for the 5-class enhanced model | p. 83 | Yes | Distinct from binary cross-entropy used in baseline |
| Binary cross-entropy | Loss function for the baseline model | p. 83 | Yes | Baseline-specific |
| ROC-AUC | Receiver Operating Characteristic – Area Under Curve; reported value = 0.9638 | p. 84 | Yes | Key evaluation metric |
| F1-score | Harmonic mean of precision and recall; reported as 0.91 (enhanced) vs. 0.87–0.89 (baseline) | p. 84 | Yes | Key evaluation metric |
| Precision | Reported as 0.90/0.93 (enhanced, classes 0/1) | p. 84 | Yes | Key evaluation metric |
| Recall | Reported as 0.93/0.90 (enhanced, classes 0/1) | p. 84 | Yes | Key evaluation metric |
| APTOS 2019 | Blindness Detection dataset; 3,662 labeled training samples; 5 DR classes | p. 81 | Yes | Primary dataset identifier |
| EyePACS | Referenced as a similar dataset format; not directly used | p. 79 | Yes | Mentioned for comparability |
| Softmax | Output activation function for 5-class classification | p. 83 | Yes | Enhanced model output layer |
| Sigmoid | Output activation function for binary classification | p. 83 | Yes | Baseline model output layer |
| ReLU | Activation function used in convolutional and dense layers | p. 83 | Yes | Standard activation term |
| Max-pooling | Spatial downsampling with 2 × 2 pooling windows | p. 83 | Yes | Architecture component |
| Early stopping | Training termination strategy applied to the enhanced model | p. 83 | Yes | Regularization technique |
| Confusion matrix | Evaluation tool; reported for both models (Figs. 4–5) | p. 84 | Yes | Standard evaluation term |
| Keras | Deep learning library used for model implementation | p. 83 | Yes | Implementation dependency |
| TensorFlow | Backend framework for Keras | p. 83 | Yes | Implementation dependency |
| OpenCV (cv2) | Library used for CLAHE and image resizing | pp. 83–84 | Yes | Implementation dependency |

---

*Literature Card generated for: Sapakova, S., Yesmukhamedov, N., & Sapakov, A. (2025). Unique ID: LC-SAPAKOVA-2025-01. Self-publication flag: ACTIVE.*
