LITERATURE CARD
PhD Dissertation Literature Review
1. Bibliographic Metadata
Full Citation (APA 7): Goh, J. H. L., Ang, E., Srinivasan, S., Lei, X., Loh, J., Quek, T. C., Xue, C., Xu, X., Liu, Y., Cheng, C.-Y., Rajapakse, J. C., & Tham, Y.-C. (2024). Comparative analysis of vision transformers and conventional convolutional neural networks in detecting referable diabetic retinopathy. Ophthalmology Science, 4(6), 100552.
DOI: https://doi.org/10.1016/j.xops.2024.100552
Journal: Ophthalmology Science
Year: 2024
Publication Type: Empirical (comparative model evaluation with external validation)
Research Domain: Medical AI; Deep learning for diabetic retinopathy detection; Vision Transformer vs. CNN comparison

2. Study Type Classification
•	CNN-based classification study
•	Vision Transformer application
•	External validation study
•	Cross-dataset validation
•	Messidor benchmarking
Justification: The study systematically compares 5 CNN and 4 ViT architectures for binary referable DR classification, trained on Kaggle and externally validated on SEED and Messidor-1 datasets.

3. Research Problem
The study addresses the underexplored comparative performance of Vision Transformers versus conventional CNNs for referable diabetic retinopathy detection. Prior studies comparing these architectures relied on small, imbalanced datasets and lacked external validation, limiting the reliability of conclusions regarding ViT superiority.
Related to: Architecture comparison, generalization (external validation), clinical deployment potential

4. Datasets Used
Field	Details
Dataset 1	Kaggle DR Detection (2015)
Public/Private	Public
Sample Size	41,614 good-quality images (from 88,702 original; 25,536 unique individuals)
Class Taxonomy	Binary: Referable DR (moderate, severe, proliferative) vs. Non-referable DR (normal, mild)
Train/Val/Test Split	39,531 / 1,038 / 1,045 (individual-level split, no overlap)
External Dataset?	No (internal training + test)

Field	Details
Dataset 2	SEED (Singapore Epidemiology of Eye Diseases)
Public/Private	Private (available on reasonable request)
Sample Size	5,455 images from 2,855 participants (993 Malay, 577 Chinese, 1,287 Indian)
Class Taxonomy	Binary: Referable vs. Non-referable (original 6-class reclassified)
Role	External test set
Camera	Canon CR-1 Mark-II nonmydriatic

Field	Details
Dataset 3	Messidor-1
Public/Private	Public
Sample Size	1,200 images
Class Taxonomy	Binary: Referable (grade 2-3) vs. Non-referable (grade 0-1)
Role	External test set
Camera	Topcon TRC NW6 nonmydriatic

Cross-dataset testing performed? Yes — models trained on Kaggle, tested on SEED and Messidor-1.

5. Preprocessing Pipeline
Automated image quality filtering: Yes — excluded poor-quality images from 88,702 to 41,614
Resizing: [NOT REPORTED]
Cropping: [NOT REPORTED]
Normalization: [NOT REPORTED]
CLAHE: [NOT REPORTED]
Color normalization: [NOT REPORTED]
Augmentation: Not performed on training data (authors criticize prior work for augmenting low-quality images)
Lesion enhancement: [NOT REPORTED]
Note: The study emphasizes quality filtering as a key preprocessing step but does not report standard image preprocessing parameters (resize, normalization, CLAHE, color space). This is a significant reporting gap.

6. Model Architecture
CNN Models
•	VGG-19
•	ResNet50
•	InceptionV3
•	DenseNet201
•	EfficientNetV2S
ViT Models
•	VAN_small (Visual Attention Network)
•	CrossViT_small
•	ViT_small
•	SWIN_tiny (Hierarchical Vision Transformer using Shifted Windows)

Pretraining: All models pretrained on ImageNet
Transfer learning protocol: Fine-tuning with ImageNet pretrained weights
Parameter scale: All models approximately 20 million parameters
Input resolution: [NOT REPORTED]
Loss function: [NOT REPORTED] (class weights assigned for imbalance)
Optimizer: [NOT REPORTED]
Epochs: Early stopping at 20 epochs when no further improvement
Checkpoint strategy: Saved model with highest AUC on internal validation set

7. Validation Design
•	Internal validation: Yes (Kaggle internal test set, n=1,045, individual-level split)
•	External validation: Yes (SEED, n=5,455; Messidor-1, n=1,200)
•	Cross-validation: No (single train/val/test split)
•	Prospective validation: No (retrospective study)
•	Multi-center validation: Partial — SEED is multi-ethnic (Malay, Chinese, Indian cohorts)
•	Subgroup analyses: Age (<60 vs. ≥60), gender, ethnicity (in supplementary)
•	Sensitivity analysis: 200 poor-quality images added back to test robustness

8. Performance Metrics
AUC Performance
Model	Kaggle (Internal)	SEED (External)	Messidor-1 (External)
VGG-19	86.1%	94.0%	86.5%
ResNet50	89.4%	92.4%	89.7%
DenseNet201	88.7%	92.9%	87.8%
InceptionV3	88.3%	91.7%	89.7%
EfficientNetV2S	89.2%	94.1%	87.9%
VAN_small	90.7%	95.2%	90.1%
CrossViT_small	93.8%	94.5%	90.5%
ViT_small	94.5%	95.5%	91.4%
SWIN_tiny	95.7%	97.3%	96.3%

Sensitivity at 80% Specificity
Model	Kaggle	SEED	Messidor-1
VGG-19	76.3%	89.4%	77.4%
ResNet50	83.8%	89.2%	82.0%
DenseNet201	82.5%	89.2%	80.4%
InceptionV3	81.3%	87.2%	79.0%
EfficientNetV2S	83.1%	91.7%	81.8%
VAN_small	83.8%	91.4%	83.6%
CrossViT_small	90.0%	92.3%	82.0%
ViT_small	91.9%	93.9%	84.2%
SWIN_tiny	94.4%	96.9%	94.8%

Maximum F1 Scores (SWIN_tiny)
•	Kaggle internal: F1max = 0.80 (Recall 83.1%, Precision 76.4%)
•	SEED external: F1max = 0.79 (Recall 79.5%, Precision 78.2%)
•	Messidor-1 external: F1max = 0.90 (Recall 87.8%, Precision 91.5%)

Statistical tests: DeLong test for AUC comparison (with Bonferroni correction); McNemar test for sensitivity comparison at fixed 80% specificity.
Confidence intervals: [NOT REPORTED]
Cohen’s Kappa: [NOT REPORTED]

9. Authors’ Claims
Performance Claims
•	SWIN transformer achieved the highest AUC across all test sets (95.7%, 97.3%, 96.3%)
•	SWIN significantly outperformed all 5 CNN models (all P < 0.001 on internal test)
•	At 80% specificity, SWIN achieved highest sensitivity (94.4% internal; 96.9% SEED; 94.8% Messidor-1)
Generalization Claims
•	Superior performance was consistent across internal and both external test sets
•	Findings held across subgroups of age, gender, and ethnicity
Clinical Applicability Claims
•	ViTs can improve and optimize retinal photo-based deep learning for referable DR detection
•	Findings offer insights for development of AI-powered screening tools
Superiority Claims
•	ViTs provide superior performance over CNNs in detecting referable DR
•	SWIN specifically outperformed all CNN and most ViT models

10. Empirical Support Assessment
Does data support generalization claims? Partially. External validation on two datasets (SEED, Messidor-1) with different populations and cameras strengthens generalization evidence. However, all models were trained on a single dataset (Kaggle), limiting diversity of training distribution.
Is external validation robust? Yes. Two independent external datasets from different populations (multi-ethnic Singaporean cohort and European dataset), captured with different cameras.
Are confidence intervals reported? No. AUC values are reported without confidence intervals, which weakens the precision of performance claims.
Is dataset size adequate? Moderately. Training set (39,531) is substantial. Internal test set (1,045) is adequate. SEED external set (5,455) is large. Messidor-1 (1,200) is moderate.
Is class imbalance addressed? Yes. Class weights were applied during training. Consistent DR ratios were maintained across train/val/test splits.
Is statistical testing adequate? Yes. DeLong test with Bonferroni correction for AUC; McNemar test for sensitivity comparisons. Multiple comparison correction is appropriate.

11. Internal Validity
Overfitting risk: Low-moderate. Individual-level split prevents data leakage; early stopping at 20 epochs; model checkpointing on validation AUC. However, no cross-validation was performed.
Dataset leakage risk: Low. Individual-level splitting explicitly prevents image-level leakage between train and test sets.
Confounders: Single training dataset may introduce dataset-specific biases. Camera variability in Kaggle is uncontrolled.
Augmentation inflation risk: Not applicable — no data augmentation was performed (a deliberate choice).
Metric reliability: Moderate. AUC and sensitivity at fixed specificity are appropriate metrics. Absence of confidence intervals reduces reliability assessment.

12. External Validity
Cross-population transferability: Demonstrated across multi-ethnic Singaporean population (Malay, Chinese, Indian) and European Messidor-1 dataset.
Dataset portability: Strong. Models trained on Kaggle (various cameras) and tested on Canon CR-1 (SEED) and Topcon TRC NW6 (Messidor-1) without retraining.
Clinical feasibility: Authors acknowledge lack of prospective clinical trial evidence as a barrier. No real-world deployment assessment.
Hardware constraints: [NOT REPORTED]

13. Strengths
•	Systematic comparison of 9 models (5 CNN + 4 ViT) under standardized conditions
•	All models constrained to approximately 20M parameters for fair comparison
•	All models pretrained on ImageNet with identical protocol
•	Individual-level data splitting to prevent leakage
•	External validation on two independent datasets with different demographics and camera systems
•	Automated image quality filtering (reduced 88,702 to 41,614 images)
•	Appropriate statistical testing with multiple comparison correction (DeLong + Bonferroni)
•	Subgroup analyses by age, gender, and ethnicity
•	Post-hoc sensitivity analysis with poor-quality images
•	Code availability on GitHub

14. Limitations
Explicit (Stated by Authors)
•	Parameter scale constrained to ~20M, preventing exploration of optimal scale per architecture
•	Kaggle dataset is open-source with potential mislabeling
•	Single training dataset introduces potential confounders and biases limiting generalizability
•	Lack of prospective clinical trial validation
Implicit (Methodological)
•	No reporting of preprocessing pipeline details (resizing, normalization, CLAHE) — critical omission for reproducibility
•	No confidence intervals for AUC or sensitivity values
•	No cross-validation; single train/val/test split
•	Input resolution not reported
•	Loss function and optimizer not reported
•	No explainability analysis (e.g., Grad-CAM, attention maps)
•	No comparison with ensemble approaches
•	F1max thresholds differ per model, complicating direct comparison beyond AUC

15. Relevance to Dissertation
Preprocessing dominance hypothesis: Highly relevant. The study’s failure to report preprocessing details paradoxically supports the argument that preprocessing is often underspecified in DR deep learning studies. The quality filtering step (reducing dataset by >50%) is itself a major preprocessing intervention whose impact is uncontrolled.
Cross-database validation: Directly relevant. Provides strong evidence of cross-dataset generalization for SWIN transformer, with consistent superiority across Kaggle, SEED, and Messidor-1.
EyePACS/Messidor benchmarking: Partially relevant. Uses Kaggle (EyePACS-derived) for training and Messidor-1 for external testing. Provides benchmark AUC values for both.
Vision Transformer comparison: Core relevance. This is one of the first studies to comprehensively compare ViTs vs. CNNs for referable DR with external validation. SWIN_tiny’s superiority is a key finding for the ViT discourse.
Risk of contradiction: Low. The study supports ViT superiority but does not directly test preprocessing effects, so it neither contradicts nor confirms preprocessing dominance. The uncontrolled preprocessing pipeline is a gap that can be cited as evidence of the field’s underattention to preprocessing.

16. Citation-Ready Statements
•	Goh et al. (2024) demonstrated that the SWIN transformer achieved AUC of 95.7% on Kaggle internal test, 97.3% on SEED, and 96.3% on Messidor-1, significantly outperforming all five CNN models (all P < 0.001) (p. 3).
•	At fixed 80% specificity, SWIN transformer achieved sensitivity of 94.4% on internal test, compared with CNN sensitivity ranging from 76.3% to 83.8% (p. 5).
•	The authors noted that prior ViT-CNN comparative studies “often rely on relatively small and imbalanced datasets” and lacked external validation (p. 2).
•	Despite comparing 9 architectures, the study did not report fundamental preprocessing parameters including image resizing, normalization, or color space transformations, illustrating the field’s pervasive underspecification of preprocessing pipelines.
•	External validation across multi-ethnic Singaporean cohorts (Malay, Chinese, Indian) and the European Messidor-1 dataset demonstrated consistent ViT superiority, supporting cross-population generalization (pp. 3, 5).
•	All models were constrained to approximately 20 million parameters and pretrained on ImageNet, providing a controlled architectural comparison (p. 3).
•	The study’s automated quality filtering reduced the Kaggle dataset from 88,702 to 41,614 images, representing a >50% exclusion rate that itself constitutes a significant preprocessing intervention (p. 2).

17. Epistemic Classification
Classification: High-impact empirical evidence; Transformer-era study
Justification: This study provides the most methodologically rigorous comparison to date of ViTs versus CNNs for referable DR, with external validation on two independent datasets. It establishes SWIN transformer as a benchmark architecture for referable DR detection. The external validation design and statistical rigor elevate it above prior small-scale ViT-CNN comparisons. However, it does not qualify as clinical validation (no prospective design) or as a methodological precedent for preprocessing (unreported pipeline).

18. Analytical Synthesis
This study carries substantial epistemic weight as one of the first externally validated comparisons of Vision Transformers and CNNs for referable DR detection. The SWIN transformer’s consistent superiority across three test sets, with rigorous statistical testing, provides strong evidence for the ViT paradigm in ophthalmic AI. For dissertation positioning, this paper serves as a primary reference for establishing that ViTs outperform CNNs under controlled conditions, while simultaneously exemplifying the field’s neglect of preprocessing documentation. The >50% quality-based exclusion rate from Kaggle is itself an uncontrolled preprocessing variable that may substantially influence reported performance, directly supporting the preprocessing-dominance argument. The study does not demonstrate cross-dataset robustness in the strongest sense, as all models were trained on a single source dataset; true robustness would require multi-source training or domain adaptation. The absence of preprocessing details (no reported resizing, normalization, or CLAHE parameters) means the observed ViT superiority cannot be disentangled from potential preprocessing effects, which is precisely the gap the dissertation aims to address.

— End of Literature Card —
