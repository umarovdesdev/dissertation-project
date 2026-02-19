# LITERATURE CARD

---

## I. SOURCE IDENTIFICATION

- **Unique ID:** `LC-AlTimemy-2021`
- **Full Bibliographic Citation:** Sapakova, S., Yesmukhamedov, N., & Sapakov, A. (2025). Development of an image quality enhancement approach for diabetic retinopathy diagnosis. *Eastern-European Journal of Enterprise Technologies*, 4(9(136)), 79–88. https://doi.org/10.15587/1729-4061.2025.335570
- **Type of Publication:** Journal article / Empirical study (primary: journal article, published in a Scopus Q3-indexed journal; the work is empirical in nature, involving experimental model training and evaluation).
- **Year:** 2025
- **Research Domain Classification:** Medical Image Processing > Retinal Disease Detection > CNN-based Automated Multi-class Classification with Image Preprocessing Enhancement

---

## II. GLOBAL SOURCE ANALYSIS

### 1. Central Thesis

The authors propose that a fully automated retinal disease identification system combining an upgraded Contrast-Limited Adaptive Histogram Equalization (CLAHE) filter with a fine-tuned pre-trained RESNET50 network can achieve high-accuracy multi-class retinal disease classification while reducing human interaction. The authors explicitly state: "a novel design of an automated retinal diseases detection model to identify a variety of eye illnesses has been proposed. The proposed model simplified the conventional model and introduced a series of pre-processing procedures that allow high accuracy rate in disease identification" (Section 1, p. 4). Their central contribution is the integration of an upgraded CLAHE filter (with a controllable global threshold value) into a transfer learning pipeline to achieve 100% classification accuracy, sensitivity, and specificity on a five-class retinal disease task.

### 2. Research Problem Addressed

The authors identify the following specific problems:

- Manual diagnosis of retinal diseases by ophthalmologists is "time-consuming, even for skillful ophthalmologists" (Section 1, p. 1), and "the global increment in the number of patients with eye problem might exacerbate the situation in delayed disease detection" (Section 1, p. 1).
- The diagnosis process is "prone to errors when huge dataset is involved" (Abstract, p. 1).
- Conventional CLAHE has a fixed clipping value that may cause "excessive contrast enhancement that may result in processed image with odd appearance and undesired artifacts" (Section 2.2.1, p. 5) and "a poor manifestation in vanishing regions, typically the tiny veins" (Section 2.2.1, p. 5).
- The majority of fundus image pixels are black pixels "which might experience excessive enhancement effect that could distort the image overall visibility" (Section 1, p. 2).
- Common CNN requires "substantial amount of training set which is less feasible in training labeled medical images due to its high demand from experts in annotations and limited samples of data" (Section 1, p. 3).

### 3. Methodology

**Theoretical framework:**

- CLAHE theory as established in prior work [21, 30], with the authors' modification adding a global threshold parameter.
- Transfer learning theory: reusing pre-trained neural networks from other domains (specifically ImageNet) and fine-tuning for medical image classification [12, 26, 27, 28].
- RESNET50 architecture as the base pre-trained network, previously trained on ImageNet [33].
- Evaluation metrics based on confusion matrix parameters (TP, TN, FP, FN) as defined in [35].

**Methods used:**

1. *Upgraded CLAHE filter:* Conventional CLAHE clipping limit defined as: CLIP LIMIT = ⌈L/T⌉ + β · (φ − ⌈L/T⌉) (Eq. 1), where T = global threshold, φ = pixels population in each block, β = clip factor, L = gray scale. The proposed upgraded CLAHE uses: CLIP LIMIT = T/80 (Eq. 2). The modification adds a controllable global threshold value to the fixed contrast point (Section 2.2.1, p. 5).
2. *Intensity normalization:* Conducted to "increase wider intensity distribution within a proper range" (Section 2.2.1, p. 5).
3. *Light ring correction:* Operated in "LAB" color space, replacing the distorted outer border region with original dark background, then converting back to RGB (Section 2.2.1, p. 5).
4. *Data augmentation:* Rotation of dataset images by 30 degrees for eleven times (30° to 330°), expanding dataset from 152 to 1800 images (Section 2.2.2, p. 6).
5. *Single CNN model:* 4 convolution layers, 3×3 kernel, stride 1, one pixel-padding, max-pooling 2×2 with stride 2, softmax activation producing 1×6 vector (normal/abnormal) then 1×2 vector for disease class pairs (Section 2.3, pp. 6–7). Used as a quality validator for enhanced images.
6. *Transfer learning with RESNET50:* Input size 224×224×3. Fine-tuned from ImageNet pre-training. New fully connected layer specified for five-class identification (Section 2.4, pp. 7–8). Training parameters: 100 epochs, learning rate 0.0003, elapsed time 262 min (Table 2, p. 11).

**Data sources:**

- STARE (Structured Analysis of the Retina) web-database [29]. The database provides 400 raw fundoscopic images covering 13 diseases and normal cases (Section 2.1.1, p. 5). The study used 157 images (Abstract, p. 1) / 152 images (Section 1, p. 4) from five classes: BDR, CRVO, CNV, PDR, and Normal.
- Inclusion criterion: "Only the pictures that had strong agreement marks annotated by the ophthalmologists were obtained from the image store" (Section 2.1, p. 4).
- Exclusion criterion: "The fundus images with severe artifacts distortions were not included in this study" (Section 2.1, p. 4).

**Analytical approach:**

- Confusion matrix analysis (Fig. 8, p. 10).
- Sensitivity: Sen = TP / (TP + TN) (Eq. 3, p. 9) — *Note: this formula as printed in the source differs from the standard sensitivity formula TP/(TP+FN)*.
- Specificity: Spe = TN / (TN + FP) (Eq. 4, p. 9).
- Accuracy: ACC = (TP + TN) / (TP + FP + TN + FN) (Eq. 5, p. 9).
- Comparison with state-of-the-art: VGG19-based method [31] (Table 4, p. 11) and feature extraction methods [18] (Table 5, p. 12).

### 4. Conceptual Contributions

**Key concepts introduced:**

- *Upgraded CLAHE with global threshold T/80:* A modification to the conventional CLAHE filter replacing the fixed clipping value with a controllable threshold calculated as T/80, where T is the global threshold. This allows adaptive histogram improvement "according to the pre-defined global threshold value" (Section 2.2.1, p. 5).
- *Single CNN as image quality validator:* The proposed single CNN network was designed to "examine the quality of the enhanced fundus images before entering the following classification stage" (Section 2.3, p. 7), serving as a preprocessing quality meter.
- *Two-stage classification pipeline:* First stage uses single CNN for binary classification (normal/abnormal), second stage uses transferred RESNET50 for multi-class disease identification.

**Definitions provided by the author:**

- Conventional CLAHE clipping limit (Eq. 1): CLIP LIMIT = ⌈L/T⌉ + β · (φ − ⌈L/T⌉), where T = global threshold, φ = pixels population in each block, β = clip factor, L = gray scale (Section 2.2.1, p. 5).
- Upgraded CLAHE clipping limit (Eq. 2): CLIP LIMIT = T/80 (Section 2.2.1, p. 5).
- Sensitivity (Eq. 3): Sen = TP / (TP + TN) (p. 9).
- Specificity (Eq. 4): Spe = TN / (TN + FP) (p. 9).
- Accuracy (Eq. 5): ACC = (TP + TN) / (TP + FP + TN + FN) (p. 9).

### 5. Empirical Contributions

**Data:**

- Original dataset: 152/157 images from STARE, 5 classes (BDR, CRVO, CNV, PDR, Normal).
- After augmentation: 1800 images total (Section 3/Table 3, p. 11).
- Class balancing: Adjusted to smallest class size of 186 images per class (Section 3, p. 9).
- Training set: 186 images per class × 5 = 930 total; described as 650 images for training and 280 for validation (p. 8). Table 3 shows 186 training + 56 validation per class (p. 11).
- Split: 70% training, 30% test (p. 8).

**Findings:**

- Single CNN model (pairwise classification): 100% accuracy, 100% sensitivity, 100% specificity for all five binary classification pairs (Table 1, p. 9).
- Transferred RESNET50 (multi-class): 100% accuracy, 100% sensitivity, 100% specificity (Abstract, p. 1; Section 3, p. 9).
- Confusion matrix shows zero misclassified images across all five classes (Fig. 8, p. 10).
- Training parameters: 100 epochs, learning rate 0.0003, training time 262 min, validation frequency 65 iterations (Table 2, p. 11).
- Optimal CLAHE parameter: T/80 achieved best image enhancement effect according to validation accuracy test (Section 4.1, p. 10).

**Measurable results — comparison with state-of-the-art:**

Table 4 (p. 11) — Comparison with [31] (Karthikeyan et al.):

| Methods | Proposed method | Method in [31] |
|---------|----------------|----------------|
| Number of augmented images | 960 | 2484 |
| CNN Pre-trained | RESNET50 | VGG19 |
| Classification accuracy | 100% | 95.6% |
| Sensitivity | 100% | 40%–100% |
| Specificity | 100% | 99%–100% |
| Training-set / validation-set | 70% / 30% | 80% / 20% |
| Deep learning technique | Transfer learning | Transfer learning |
| Epochs | 100 | 50 |

Table 5 (p. 12) — Feature extraction comparison on STARE:

| Network | Accuracy |
|---------|----------|
| Resnet_101 [18] | 81.6% |
| DesNet_121 [18] | 85.5% |
| SetNet_101 [18] | 83.21% |
| WP_CNN_101 [18] | 90.84% |
| Proposed model | 96.7% |

### 6. Limitations Acknowledged by the Author

- "The proposed model had a drawback that its classification only covered five retina classes" (Section 5, p. 12).
- "Further investigation is required to evaluate the model in detecting more disease cases" (Section 5, p. 12).

### 7. Implicit Assumptions

- The rotation-based augmentation (30° increments) adequately represents real-world image variance for retinal fundus images. [Inferable from: Section 2.2.2, p. 6 — no justification provided for why rotation alone suffices as an augmentation strategy.]
- The STARE dataset, with 152–157 images from five classes, is representative enough to validate a generalizable retinal disease detection system. [Inferable from: Section 2.1, p. 4 — no discussion of dataset representativeness or demographic diversity.]
- The reported 100% accuracy on all metrics is indicative of genuine generalization rather than overfitting to a small, augmented dataset. [Inferable from: Section 3, p. 9 — despite acknowledging overfitting as "the main drawback of multi-class classification model" in Section 2.3, p. 7, no explicit overfitting analysis is provided for the final transferred model.]
- The upgraded CLAHE parameter T/80 is universally optimal for retinal fundus image enhancement. [Inferable from: Section 4.1, p. 10 — optimality was determined by validation accuracy on a single dataset.]

---

## III. EXTRACTION BLOCKS

---

```
[Extraction Block ID: EB-01]

Relevant to:
• Dissertation claim(s) supported or challenged: "The diagnostic effectiveness of CNN models 
  for automated DR classification depends more on the quality of input images than on 
  architectural complexity alone"; "Integration of preprocessing methods with CNN models as 
  a unified system significantly improves diagnostic accuracy."
• Concept(s) used: Upgraded CLAHE, modified clipping limit, global threshold T/80
• Research question addressed: Chapter 2 (Section 2.1.2 — mathematical foundations of 
  CLAHE) and Chapter 3 (Section 3.1.2 — modified CLAHE algorithm)

Function in dissertation:
• Methodological precedent / Conceptual clarification

Extracted Content (Strict Extraction Only):
• The conventional CLAHE clipping limit is defined as: CLIP LIMIT = ⌈L/T⌉ + β · (φ − ⌈L/T⌉) 
  (Eq. 1, p. 5), where T = global threshold, φ = pixels population in each block, β = clip 
  factor, L = gray scale.
• The proposed upgraded CLAHE replaces this with: CLIP LIMIT = T/80 (Eq. 2, p. 5).
• The modification overcomes the fixed clipping feature by "adding a global threshold value 
  to the fixed contrast point in the filter" (Section 2.2.1, p. 5).
• The histogram is "improved adaptively according to the pre-defined global threshold value" 
  (Section 2.2.1, p. 5).
• "The proposed model greatly improved the image distinctiveness, especially the tiny veins" 
  (Section 2.2.1, p. 5).
• The clipping parameter at T/80 was found to achieve the best image enhancement effect 
  according to the validation accuracy test (Section 4.1, p. 10).
• Image quality score comparison: conventional CLAHE = 33.2284; upgraded CLAHE T/80 = 
  34.3483 (Fig. 4, p. 6).

Strength of Relevance:
• Core
```

---

```
[Extraction Block ID: EB-02]

Relevant to:
• Dissertation claim(s) supported or challenged: "The proposed approach achieves high 
  diagnostic results under limited computational resources without requiring complex 
  architectures."
• Concept(s) used: Transfer learning, fine-tuned RESNET50, ImageNet pre-training
• Research question addressed: Chapter 2 (Section 2.3 — transfer learning theory) and 
  Chapter 3 (Section 3.3 — transfer learning methodology using ResNet50)

Function in dissertation:
• Methodological precedent / Empirical support

Extracted Content (Strict Extraction Only):
• RESNET50 "was proven to have better feature extractions that allowed higher accurate 
  prediction rate as compared to the other CNN networks, which recorded an accuracy score 
  of 67%" (Section 2.4, p. 7).
• RESNET50 "consists of several dimensional of convolutional filters which could minimize 
  the training periods and avoid the over-fitting issue" (Section 2.4, p. 7).
• The network was previously trained with the "Image-Net" database [33] (Section 2.4, p. 7).
• Input image size: 224 × 224 × 3 (width, height, channel) (Section 2.4, p. 7).
• Transfer learning was applied "for fused feature extraction with the features from the 
  untrained dataset" (Section 2.4, p. 7).
• The technique "potentially assisted the architecture in learning the common features from 
  the raw images without additional training for common data, which indeed minimized the 
  required training time" (Section 2.4, pp. 7–8).
• New fully connected layer specified for five-class identification (Section 2.4, p. 8).
• The transfer learning method "took shorter training process instead of training the model 
  from scratch with one thousand classes" (Section 4.2, p. 10).

Strength of Relevance:
• Core
```

---

```
[Extraction Block ID: EB-03]

Relevant to:
• Dissertation claim(s) supported or challenged: "Integration of preprocessing methods 
  (resize, normalization, augmentation, CLAHE) with CNN models as a unified system 
  significantly improves diagnostic accuracy."
• Concept(s) used: Data augmentation, rotation-based augmentation
• Research question addressed: Chapter 3 (Section 3.1.3 — augmentation methodology)

Function in dissertation:
• Methodological precedent

Extracted Content (Strict Extraction Only):
• "Accuracy of classification of a trained network depends strongly on the training dataset 
  size which consists of adequate variants" (Section 2.2.2, p. 6).
• "Due to limitation of training data, the augmentation methods are often applied to feed the 
  network" (Section 2.2.2, p. 6).
• Augmentation applied: "rotation of the dataset images by 30 degrees for eleven times 
  (ranges from 30° to 330°)" (Section 2.2.2, p. 6).
• Purpose: "to feed the CNN network with images of different views and thus forming a 
  trained network that enabled recognition of the region of interest from different orientations" 
  (Section 2.2.2, p. 6).
• Dataset expanded from 152 images to 1800 images after augmentation (Fig. 6, p. 7).
• After class balancing: 186 training + 56 validation images per class (Table 3, p. 11).

Strength of Relevance:
• Supporting
```

---

```
[Extraction Block ID: EB-04]

Relevant to:
• Dissertation claim(s) supported or challenged: "The proposed approach achieves high 
  diagnostic results under limited computational resources without requiring complex 
  architectures."
• Concept(s) used: STARE dataset, small dataset handling, class balancing
• Research question addressed: Chapter 4 (Section 4.1.1 — dataset selection and handling)

Function in dissertation:
• Methodological precedent / Empirical support

Extracted Content (Strict Extraction Only):
• Dataset: STARE (Structured Analysis of the Retina) web-database [29], providing 400 raw 
  fundoscopic images covering 13 diseases and normal cases (Section 2.1.1, p. 5).
• Study used 157 images (Abstract) / 152 images (Section 1, p. 4) from five classes: BDR, 
  CRVO, CNV, PDR, and Normal.
• Inclusion: "Only the pictures that had strong agreement marks annotated by the 
  ophthalmologists were obtained" (Section 2.1, p. 4).
• Exclusion: "The fundus images with severe artifacts distortions were not included" 
  (Section 2.1, p. 4).
• Class balancing: Groups adjusted "according to the smallest enumerate image classes of 
  fundus images, which was 186 images" (Section 3, p. 9).
• Training: 650 images; Validation: 280 images (p. 8). Table 3 confirms 186 training + 56 
  validation per class across 5 classes (p. 11).
• "Common CNN requires substantial amount of training set which is less feasible in training 
  labeled medical images" — motivation for transfer learning on small datasets (Section 1, 
  p. 3).

Strength of Relevance:
• Supporting
```

---

```
[Extraction Block ID: EB-05]

Relevant to:
• Dissertation claim(s) supported or challenged: "The proposed approach achieves high 
  diagnostic results under limited computational resources without requiring complex 
  architectures"; "The proposed method forms a reproducible pipeline for automated 
  diagnosis of diabetic retinopathy."
• Concept(s) used: Classification accuracy, sensitivity, specificity, confusion matrix
• Research question addressed: Chapter 4 (experimental results) and Chapter 5 (validation 
  and comparative analysis)

Function in dissertation:
• Empirical support

Extracted Content (Strict Extraction Only):
• Single CNN pairwise classification results (Table 1, p. 9):
  - BC1: CNV_hist vs BDR — 100% accuracy, 100% sensitivity, 100% specificity
  - BC2: PDR vs BRV — 100% accuracy, 100% sensitivity, 100% specificity
  - BC3: CRVO vs Normal — 100% accuracy, 100% sensitivity, 100% specificity
  - BC4: CNV_hist vs Normal — 100% accuracy, 100% sensitivity, 100% specificity
  - BC5: BDR vs PDR — 100% accuracy, 100% sensitivity, 100% specificity
• Transferred RESNET50 multi-class results: "zero misclassified images, recorded the 
  sensitivity of 100.0% and specificity of 100.0%. As result, the classification model yielded 
  an accuracy rate of 100 percent" (Section 3, p. 9).
• Confusion matrix (Fig. 8, p. 10): Each class at 20.0% (equal distribution), 0.0% 
  misclassification across all class pairs.
• Training parameters: 100 epochs, learning rate 0.0003, training time 262 min, validation 
  frequency 65 iterations (Table 2, p. 11).
• Hardware: Windows OS, Intel Core i9-10900X @ 3.70GHz CPU, 128 Gb RAM, AMD Radeon 
  RX 5700 Graphics with 8 Gb RAM (Section 2.1, p. 4).

Strength of Relevance:
• Core
```

---

```
[Extraction Block ID: EB-06]

Relevant to:
• Dissertation claim(s) supported or challenged: "The proposed approach achieves high 
  diagnostic results under limited computational resources without requiring complex 
  architectures."
• Concept(s) used: Benchmarking, comparative analysis, VGG19, feature extraction methods
• Research question addressed: Chapter 5 (Section 5.3 — benchmarking against existing 
  methods)

Function in dissertation:
• Empirical support / Critical counterpoint

Extracted Content (Strict Extraction Only):
• Comparison with [31] (Karthikeyan et al., VGG19-STARE): The proposed method achieved 
  100% classification accuracy vs. 95.6%; 100% sensitivity vs. 40%–100%; 100% specificity 
  vs. 99%–100%. Proposed method used fewer augmented images (960 vs. 2484) and more 
  epochs (100 vs. 50) (Table 4, p. 11).
• "The automated detection model using (VGG19) network and (STARE) database proposed in 
  previous study had achieved 95.63% in classification accuracy, 92.99% in validation 
  accuracy and sensitivity ranged from 40 to 100%" (Section 4.2, pp. 10–11).
• "The proposed framework showed superiority in terms of its classification accuracy even 
  though the input training dataset was smaller" (Section 4.2, p. 11).
• Feature extraction comparison on STARE (Table 5, p. 12): Resnet_101 = 81.6%, DesNet_121 
  = 85.5%, SetNet_101 = 83.21%, WP_CNN_101 = 90.84%, Proposed model = 96.7%.

Strength of Relevance:
• Supporting
```

---

```
[Extraction Block ID: EB-07]

Relevant to:
• Dissertation claim(s) supported or challenged: Core hypothesis — "Systematic improvement 
  of input data quality through an integrated preprocessing pipeline has a greater impact on 
  CNN-based DR diagnostic performance than increases in model architectural complexity."
• Concept(s) used: Image preprocessing impact on CNN performance, single CNN as quality 
  validator, preprocessing dominance
• Research question addressed: Core dissertation hypothesis (preprocessing dominance)

Function in dissertation:
• Theoretical grounding / Empirical support

Extracted Content (Strict Extraction Only):
• "The proposed single CNN network aimed to examine the quality of the enhanced fundus 
  images before entering the following classification stage" (Section 2.3, p. 7).
• The single CNN was "used as a meter to evaluate the upgraded CLAHE-enhanced images" 
  (Section 4.1, p. 10).
• "The clipping parameter at T/80 was found to achieve the best image enhancement effect 
  according to the validation accuracy test" (Section 4.1, p. 10) — indicating preprocessing 
  quality was validated via downstream CNN accuracy.
• The proposed model "introduced a series of pre-processing procedures that allow high 
  accuracy rate in disease identification" (Section 1, p. 4).
• "A series of pre-processing techniques were used to reduce the overfitting to achieve a 
  higher accuracy rate. The presented preprocessing approach managed to boost the retina 
  picture aspect" (Section 1, p. 4).
• "The suggested model can contribute better feature detection than classification accuracy" 
  (Section 1, p. 4).
• "The accuracy of MA recognition is closely related to the image quality" [25] — cited by 
  authors as motivation (Section 1, p. 2).

Strength of Relevance:
• Core
```

---

```
[Extraction Block ID: EB-08]

Relevant to:
• Dissertation claim(s) supported or challenged: "The proposed method forms a reproducible 
  pipeline for automated diagnosis of diabetic retinopathy."
• Concept(s) used: Automated detection pipeline, system architecture, clinical integration
• Research question addressed: Chapter 6 (Architecture of an Automated DR Screening 
  System)

Function in dissertation:
• Methodological precedent

Extracted Content (Strict Extraction Only):
• The proposed framework is described as "a fully automatic multi-class retina diseases 
  prediction system to assist ophthalmologists in making speedy and accurate investigation" 
  (Abstract, p. 1).
• "A fully automated model of identification of retinal disease is proposed to reduce human 
  interaction while retaining its high accuracy classification results" (Abstract, p. 1).
• "The automated framework reduced the human attention level thus resulting in a huge 
  improvement in its efficiency" (Section 1, p. 4).
• Pipeline stages (Fig. 2, p. 3; Fig. 3, p. 4; Fig. 6, p. 7): (1) Dataset download → 
  (2) Labeling/folding images → (3) Image preprocessing with upgraded CLAHE → 
  (4) Augmentation (152→1800) → (5) Class balancing → (6) Training/validation split → 
  (7) Deep transfer learning with RESNET50 → (8) Multi-class disease classification output.
• "The proposed model was completely independent of the abrupt feature changes thus it could 
  be applied by ophthalmologists in retinal illness prediction" (Section 5, p. 12).
• "The superior performance offered by the proposed model could possibly be added into the 
  screening medical devices in viewing retina, such as electrocardiograph, ultrasonic imaging 
  system or other medical detection devices" (Section 5, p. 12).

Strength of Relevance:
• Supporting
```

---

```
[Extraction Block ID: EB-09]

Relevant to:
• Dissertation claim(s) supported or challenged: "Integration of preprocessing methods 
  (resize, normalization, augmentation, CLAHE) with CNN models as a unified system 
  significantly improves diagnostic accuracy."
• Concept(s) used: Intensity normalization, LAB color space correction, preprocessing 
  pipeline integration
• Research question addressed: Chapter 3 (Section 3.1 — unified preprocessing pipeline)

Function in dissertation:
• Methodological precedent

Extracted Content (Strict Extraction Only):
• "We conducted normalization to increase wider intensity distribution within a proper range 
  and allow more valuable features to be input into the CNN model" (Section 2.2.1, p. 5).
• Light ring distortion at image outer border was corrected "by replacing the region (light 
  ring) with original dark background" (Section 2.2.1, p. 5).
• "The corrective process could be operated in 'LAB' color space, and eventually changed the 
  color space back to RGB color space" (Section 2.2.1, p. 5).
• Preprocessing steps described as a series: image enhancement with upgraded CLAHE → 
  normalization → distortion correction → augmentation (Sections 2.2.1–2.2.2, pp. 5–6).

Strength of Relevance:
• Supporting
```

---

```
[Extraction Block ID: EB-10]

Relevant to:
• Dissertation claim(s) supported or challenged: "The diagnostic effectiveness of CNN models 
  for automated DR classification depends more on the quality of input images than on 
  architectural complexity alone."
• Concept(s) used: Overfitting in multi-class classification, small dataset challenges
• Research question addressed: Chapter 4 and Chapter 5 — overfitting analysis

Function in dissertation:
• Conceptual clarification / Critical counterpoint

Extracted Content (Strict Extraction Only):
• "In most cases, the main drawback of multi-class classification model is overfitting" 
  (Section 2.3, p. 7).
• Transfer learning concept was used to overcome the long processing time of fully connected 
  layers "instead of trained a CNN model from scratch" (Section 2.4, p. 8).
• X. Li et al. [27] suggested transfer learning to "minimize the overfitting problem that might 
  be invoked in training small dataset" (Section 1, p. 3).
• "A series of pre-processing techniques were used to reduce the overfitting to achieve a 
  higher accuracy rate" (Section 1, p. 4).
• Despite achieving 100% across all metrics on a small augmented dataset, no explicit 
  overfitting analysis (e.g., learning curves showing gap between training and validation) is 
  presented beyond the confusion matrix in Fig. 8 (p. 10).

Strength of Relevance:
• Supporting
```

---

## IV. RELATIONAL POSITIONING

**Supports which dissertation claims:**

1. *"The diagnostic effectiveness of CNN models for automated DR classification depends more on the quality of input images than on architectural complexity alone."* — Strongly supported. The source explicitly uses a single CNN as a quality validator for preprocessing output (Section 2.3, p. 7) and attributes classification success to the upgraded CLAHE preprocessing step. The statement "the suggested model can contribute better feature detection than classification accuracy" (p. 4) directly aligns with the preprocessing dominance hypothesis.

2. *"Integration of preprocessing methods with CNN models as a unified system significantly improves diagnostic accuracy."* — Supported. The source presents a unified pipeline (upgraded CLAHE → normalization → augmentation → transfer learning RESNET50) and achieves 100% classification performance.

3. *"The proposed approach achieves high diagnostic results under limited computational resources without requiring complex architectures."* — Supported. The source achieves 100% accuracy using transfer learning on a small dataset (152 original images) with fewer augmented images (960) than the comparator study [31] (2484).

4. *"The proposed method forms a reproducible pipeline for automated diagnosis of diabetic retinopathy."* — Partially supported. The source presents a clear pipeline architecture (Figs. 2, 3, 6) with defined parameters. However, the source addresses general retinal diseases (BDR, CRVO, CNV, PDR), not specifically diabetic retinopathy grading as in the dissertation's APTOS 2019 framework.

**Contradicts which claims (if any):**

- The source reports 100% accuracy/sensitivity/specificity on a very small dataset (157 images from STARE, augmented to 960 balanced images). The dissertation uses APTOS 2019 (3662 images, 5 DR severity classes) and reports more realistic metrics (86% accuracy, F1 ≈ 0.91). The perfect scores raise questions about generalizability and may reflect overfitting to a small, homogeneous dataset rather than genuine model superiority. This difference limits direct comparability of performance claims.
- The source's sensitivity formula (Eq. 3: Sen = TP/(TP+TN), p. 9) appears to differ from the standard formula (TP/(TP+FN)), which may indicate an error in the published text. The dissertation should note this discrepancy when citing evaluation methodology.
- The source uses a different classification task (5 disease types) versus the dissertation (5 DR severity grades 0–4), which are fundamentally different clinical problems.

**Extends which conceptual axis:**

- *CLAHE modification theory:* The source extends CLAHE theory by introducing a controllable threshold parameter (T/80), providing a mathematical formulation (Eq. 2) that the dissertation can reference when discussing its own CLAHE parameterization approach.
- *Transfer learning for small medical datasets:* The source demonstrates transfer learning with RESNET50 on a very small dataset, providing precedent for the dissertation's use of transfer learning with EfficientNetB0 and ResNet50 on APTOS 2019.
- *Preprocessing as quality assurance:* The concept of using a simple CNN to validate preprocessing quality before the main classification stage is a novel methodological contribution relevant to the dissertation's preprocessing dominance hypothesis.

**Overlaps with which other sources (if known):**

- [31] Karthikeyan et al. (2019): VGG19 + STARE dataset study, achieving 95.6% classification accuracy — directly compared in Table 4.
- [18] Hong et al. (2018): Deep CNN for AMD detection using feature extraction on STARE — compared in Table 5.
- [27] X. Li et al. (2017): Transfer learning with Alex-Net, VGG variants for diabetic retinopathy — cited as methodological precedent.
- [26] De et al.: Transfer learning with VGG16 for OCTA classification — cited as related work.
- [33] Hagos & Kant (2019): Transfer learning for diabetic retinopathy detection from small datasets.

---

## V. REUSABILITY CONTROL

**What can be reused in dissertation drafting:**

- The mathematical formulation of conventional CLAHE (Eq. 1) and upgraded CLAHE (Eq. 2) can be cited as prior art in Chapter 2 (Section 2.1.2) when establishing the theoretical foundations of CLAHE modification.
- The performance comparison data (Tables 4 and 5) can be referenced in Chapter 5 (Section 5.3) when benchmarking against existing methods on the STARE dataset.
- The concept of using a single CNN as a preprocessing quality validator can be referenced as methodological precedent in Chapter 3.
- The augmentation strategy (rotation-based) can be cited in Chapter 3 (Section 3.1.3) as a comparison point to the dissertation's augmentation approach.
- The pipeline architecture description (Figs. 2, 3, 6) can be referenced in Chapter 6 as a precedent for automated DR screening system design.

**What must be reformulated:**

- The CLAHE parameterization differs: the source uses T/80 while the dissertation must define and justify its own CLAHE parameters. Direct adoption of T/80 is not appropriate without independent validation on APTOS 2019.
- The dataset differs fundamentally: STARE (157 images, 5 disease types) vs. APTOS 2019 (3662 images, 5 DR severity grades). Performance metrics are not directly comparable.
- The CNN architecture differs: the source uses RESNET50 (224×224×3 input) while the dissertation uses both baseline CNN and EfficientNetB0/ResNet50 (256×256 and 512×512 inputs).
- The classification task differs: multi-disease classification (BDR, CRVO, CNV, PDR, Normal) vs. DR severity grading (DR 0–4).
- The sensitivity formula (Eq. 3) as printed in the source contains an apparent error (TP/(TP+TN) instead of TP/(TP+FN)). The dissertation should use the standard formulation and note this discrepancy if citing the source's evaluation framework.

**Risk of self-plagiarism:** N/A — the source is not authored or co-authored by the dissertation candidate (Yesmukhamedov Nurmaganbet).

---

## VI. TERMINOLOGY INDEX

| Term | Definition/Usage in Source | Consistency Note |
|------|---------------------------|-----------------|
| Upgraded CLAHE / Modified CLAHE | CLAHE with controllable global threshold, CLIP LIMIT = T/80 (Eq. 2, p. 5), replacing the conventional fixed clipping value | Dissertation uses "modified CLAHE" — ensure consistent terminology; the source uses "upgraded CLAHE" throughout |
| Transfer learning / Deep transfer learning | Reusing pre-trained neural networks from other applications with fine-tuning for new tasks; used interchangeably in source (Sections 1, 2.4) | Source uses both "transfer learning" and "deep transfer learning"; dissertation should define precisely and use consistently |
| RESNET50 / ResNet50 | Residual Network "50", pre-trained on ImageNet, 224×224×3 input, used for multi-class classification (Section 2.4, p. 7) | Source capitalizes as "RESNET50"; dissertation should use standard notation "ResNet50" consistently |
| STARE dataset | Structured Analysis of the Retina web-database; 400 raw fundoscopic images, 13 diseases + normal (Section 2.1.1, p. 5) | Dissertation uses APTOS 2019 as primary dataset; STARE referenced for comparison only |
| Fundus image | Retinal fundoscopic image captured via color stereographic photography or related technology (Sections 1, 2.1) | Consistent with dissertation usage |
| Sensitivity | Sen = TP / (TP + TN) (Eq. 3, p. 9) — *Note: this formula differs from standard TP/(TP+FN)* | Flag discrepancy; dissertation should use standard formula and note source's deviation |
| Specificity | Spe = TN / (TN + FP) (Eq. 4, p. 9) | Consistent with standard definition |
| Accuracy | ACC = (TP + TN) / (TP + FP + TN + FN) (Eq. 5, p. 9) | Consistent with standard definition |
| Clipping limit | Predefined value in CLAHE to avoid excessive contrast enhancement; conventional: ⌈L/T⌉ + β·(φ − ⌈L/T⌉); proposed: T/80 (Eqs. 1–2, p. 5) | Dissertation should define its own clipping limit formulation clearly when contrasting with this source |
| Global threshold (T) | The controllable threshold parameter in upgraded CLAHE, dividing by 80 to determine clip limit (Eq. 2, p. 5) | Source-specific parameter; dissertation must define its own threshold parameters independently |
| Data augmentation | Rotation of images by 30° × 11 times (30°–330°) to expand training data (Section 2.2.2, p. 6) | Dissertation uses resize, normalization, augmentation, CLAHE — broader augmentation suite; note source's rotation-only approach |
| Overfitting | "The main drawback of multi-class classification model" (Section 2.3, p. 7); addressed via transfer learning and preprocessing | Consistent with dissertation's concern; note source does not provide explicit overfitting analysis |
| Fully connected layer / Dense layer | Final classification layer; compacts features to one-dimensional matrix; softmax activation for probability distribution (Section 2.3, pp. 6–7) | Consistent usage |
| Softmax activation | Converts fully-connected layer output "into probability distributions" for classification decisions (Section 2.3, p. 7) | Consistent with dissertation usage |
| Background Diabetic Retinopathy (BDR) | One of five disease classes in STARE classification; retinal condition with background-level diabetic changes | Different classification system from dissertation's DR 0–4 grading |
| Central Retina Vein Occlusion (CRVO) | One of five disease classes; vascular occlusion condition of the central retinal vein | Not directly present in dissertation's DR severity classification |
| Choroidal Neovascularization (CNV) | One of five disease classes; abnormal blood vessel growth beneath the retina | Not directly present in dissertation's DR severity classification |
| Proliferative Diabetic Retinopathy (PDR) | One of five disease classes; advanced stage of diabetic retinopathy with neovascularization | Maps conceptually to higher DR grades (DR 3–4) in dissertation's APTOS classification |
