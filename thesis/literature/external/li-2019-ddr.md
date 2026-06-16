Literature Card: DDR (OIA-DDR) Dataset Descriptor

> Source-access note: The full article (Information Sciences, Elsevier) was behind a paywall at
> card-writing time (publisher access returned 403). This card was compiled from the publicly
> indexed abstract, the official dataset repository (github.com/nkicsl/DDR-dataset), and a public
> dataset mirror. Quantitative dataset attributes (image/patient/hospital/camera counts) are taken
> from the publicly indexed abstract summary and dataset documentation; fields requiring the full
> article body are marked [NOT REPORTED]. Upgrade from the full PDF when available.

1. Bibliographic Metadata
Full citation (APA 7):
Li, T., Gao, Y., Wang, K., Guo, S., Liu, H., & Kang, H. (2019). Diagnostic assessment of deep learning algorithms for diabetic retinopathy screening. Information Sciences, 501, 511–522. https://doi.org/10.1016/j.ins.2019.06.011
DOI: 10.1016/j.ins.2019.06.011
Journal: Information Sciences (Elsevier)
Year: 2019
Publication type: Empirical study with an accompanying dataset release (introduces and benchmarks the DDR / OIA-DDR dataset across classification, lesion segmentation, and lesion detection)
Research domain classification: Biomedical imaging; ophthalmology; retinal image analysis; diabetic retinopathy screening; deep learning benchmarking

2. Study Type Classification
Primary classification: Dataset descriptor + benchmark study (DDR / OIA-DDR)
Secondary applicable classifications:

CNN-based classification study (evaluates deep learning algorithms for DR grading)
Benchmark study (provides ground truths for classification, lesion segmentation, and lesion detection)
EyePACS/Messidor-adjacent (a large-scale DR-grading dataset, used in this dissertation alongside them as a device-domain-shift source)

Justification: The article both releases a large-scale Chinese-population DR dataset (DDR) and evaluates state-of-the-art deep learning algorithms on it for three tasks. Its contribution to this dissertation is primarily as a dataset descriptor: the source for DDR's size, camera diversity, and DR taxonomy.

3. Research Problem
Specific problem addressed: Lack of a large-scale, high-quality, general-purpose Chinese-population DR dataset supporting multiple tasks (image-level grading, pixel-level lesion segmentation, and lesion detection) for developing and benchmarking deep learning screening algorithms.
Problem dimensions addressed:

Lesion detection: A subset of images carries pixel-level annotations for four DR lesion types.
Clinical deployment: Motivated by automated DR screening at scale.
Generalization / device domain shift (relevant here): Images aggregated from many hospitals and dozens of camera types, supporting cross-device study.
Architecture scaling: The paper evaluates several deep learning algorithms (specific architectures [NOT REPORTED] from retrieved material).
Preprocessing: [NOT REPORTED] from retrieved material.

4. Datasets Used
This article introduces and benchmarks the DDR dataset. The following describes DDR itself:
Dataset: DDR (also released as OIA-DDR)

Public / Private: Public (released by the authors; repository under MIT license; distributed via Baidu Drive / Google Drive)
Total sample size: 13,673 color fundus images (per publicly indexed abstract summary)
Patients: 9,598 (per publicly indexed abstract summary)
Sites / geography: 147 hospitals across 23 provinces in China (per publicly indexed abstract summary)
Acquisition period: 2016–2018 (per publicly indexed abstract summary)
Cameras: 42 types of fundus cameras (per publicly indexed abstract summary)
Class taxonomy (DR grading): Six classes — the five ICDR ordinal DR grades (0 No DR, 1 Mild NPDR, 2 Moderate NPDR, 3 Severe NPDR, 4 PDR) plus an additional ungradable / poor-quality class
Lesion-level annotation: A subset of images carries pixel-level lesion annotations for four lesion types (microaneurysms, hemorrhages, hard exudates, soft exudates). Number of lesion-annotated images: ~757 (per publicly indexed abstract summary; [VERIFY against full text])
Image resolution: average ≈ 3216 × 2136 pixels (per dataset mirror; [VERIFY])
Train/validation/test split: [NOT REPORTED — exact split sizes not confirmed from retrieved material]
External dataset used? The grading task is on DDR; external comparison [NOT REPORTED]
Cross-dataset testing performed? [NOT REPORTED]

5. Preprocessing Pipeline
The preprocessing applied before benchmarking is [NOT REPORTED] from retrieved material (full article not accessed).
Resizing [NOT REPORTED]
Cropping [NOT REPORTED]
Normalization [NOT REPORTED]
CLAHE [NOT REPORTED]
Color normalization [NOT REPORTED]
Augmentation [NOT REPORTED]
Image quality filtering Partially reported: the six-class taxonomy includes an explicit ungradable/poor-quality class, indicating image-quality stratification is built into the labels.
Lesion enhancement methods [NOT REPORTED]

6. Model Architecture
The article evaluates deep learning algorithms for classification, segmentation, and detection, but the specific architectures, pretraining, and hyperparameters are [NOT REPORTED] from retrieved material.
Architecture type: [NOT REPORTED]
Pretraining source: [NOT REPORTED]
Transfer learning protocol: [NOT REPORTED]
Input resolution: [NOT REPORTED]
Loss function: [NOT REPORTED]
Optimizer: [NOT REPORTED]
Epochs: [NOT REPORTED]
Hyperparameters: [NOT REPORTED]

7. Validation Design
The benchmark evaluates deep learning algorithms on DDR's three tasks; the exact validation design (internal split, cross-validation, external validation) is [NOT REPORTED] from retrieved material. The dataset is grader-labeled (seven graders, per publicly indexed abstract summary; [VERIFY]) according to image quality and DR level.

8. Performance Metrics
Specific performance metrics (AUC, sensitivity, specificity, accuracy, F1, Kappa, segmentation IoU/Dice, detection mAP) are [NOT REPORTED] from retrieved material. The paper evaluates "state-of-the-art deep learning algorithms" across classification, semantic segmentation, and object detection; numeric values require the full text.

9. Authors' Claims
Performance claims: [NOT REPORTED] in detail from retrieved material; the paper reports a diagnostic assessment of deep learning algorithms across three tasks.
Generalization claims: DDR is presented as a large-scale, general-purpose, high-quality dataset suitable for classification, lesion segmentation, and lesion detection.
Clinical applicability claims: Aimed at automated DR screening.
Superiority claims: [NOT REPORTED] from retrieved material.

10. Empirical Support Assessment
Does data support generalization claims? The scale (13,673 images, 9,598 patients, 147 hospitals, 42 cameras) supports the "large-scale, general-purpose" characterization and is genuinely strong for cross-device/cross-site study.
Is external validation robust? [NOT REPORTED] from retrieved material.
Are confidence intervals reported? [NOT REPORTED].
Is dataset size adequate? Yes for DR grading — 13,673 images is among the larger public DR datasets; the ~757-image lesion-annotation subset is modest for segmentation, consistent with the field.
Is class imbalance addressed? [NOT REPORTED]; an explicit ungradable class is present.
Is statistical testing adequate? [NOT REPORTED].

11. Internal Validity
Model-level validity (overfitting/leakage/augmentation inflation) cannot be assessed from retrieved material. Dataset-level considerations:

Multi-site, multi-device aggregation (147 hospitals, 42 cameras) reduces single-center confound relative to single-site datasets — a strength for ecological validity, and the basis of its use as a device-domain-shift source here.
Grading reliability: labeled by multiple graders by quality and DR level; inter-grader agreement statistics [NOT REPORTED from retrieved material].
This card's secondary-source provenance limits internal-validity assessment until the full PDF is consulted.

12. External Validity
Cross-population transferability: DDR is a Chinese-population dataset aggregated across 23 provinces — broad within China; transfer to other populations is the subject of cross-dataset study (relevant to H-4/H-6), not claimed by this card.
Dataset portability: High — publicly released under MIT license with a maintained repository (nkicsl/DDR-dataset).
Clinical feasibility: Multi-hospital, multi-camera acquisition reflects realistic, heterogeneous screening conditions.
Hardware constraints: 42 fundus camera types span the dataset; no computational hardware requirement stated for reuse.

13. Strengths

Scale: 13,673 images from 9,598 patients — among the larger public DR datasets.
Multi-site, multi-device breadth: 147 hospitals, 23 provinces, 42 camera types — strong device/site diversity, directly relevant to device domain shift (H-6).
Multi-task ground truth: supports image-level grading, pixel-level lesion segmentation, and lesion detection in one resource.
Explicit ungradable class: image-quality is modeled as a label, supporting realistic screening evaluation.
Open release: MIT-licensed, maintained repository.

14. Limitations
Explicit (stated by authors): [NOT REPORTED from retrieved material.]
Implicit (methodological):

Single-country sourcing: Chinese-population only; cross-population generalization undemonstrated by the dataset alone.
Small lesion-annotation subset: ~757 lesion-annotated images relative to 13,673 total limits segmentation-benchmark statistical power.
Card provenance gap: preprocessing, architectures, splits, and metrics are [NOT REPORTED] here because the full article was not accessed; to be filled from the PDF.
Device heterogeneity confound: 42 camera types is a strength for domain-shift study but a label-independent appearance confound for single-distribution modeling.

15. Relevance to My Dissertation
Relevance to preprocessing dominance hypothesis:
Moderate. DDR provides large-scale raw DR images with a standard ordinal taxonomy; downstream preprocessing is fully the researcher's choice, allowing preprocessing effects to be isolated. It is not the primary preprocessing-dominance dataset (EyePACS is) but supports cross-dataset robustness arguments.
Relevance to cross-database / device domain shift:
High. DDR is one of the three device-domain-shift datasets (with RFMiD and ODIR-5K) for Experiment 6 (H-6, §4.7); its 42-camera, 147-hospital breadth is the salient property. Used in this dissertation for DR labels / camera-attribute context.
Relevance to EyePACS/Messidor benchmarking:
Moderate-to-high. Shares the ICDR 0–4 grading scale, enabling compatible cross-dataset DR-grading comparison; complements EyePACS (US) and Messidor (French) with a large Chinese-population set.
Relevance to Vision Transformer comparison:
Indirect. Used by later architecture studies as a benchmark; this article predates the ViT wave in DR.
Risk of contradiction:
Low. As a dataset/benchmark source it does not make claims that would contradict the dissertation; its own algorithm metrics (once read from the full text) are third-party benchmark context, not dissertation results.

16. Citation-Ready Statements

The DDR dataset comprises 13,673 color fundus images from 9,598 patients, collected from 147 hospitals across 23 provinces in China between 2016 and 2018 using 42 types of fundus cameras (Li et al., 2019; per publicly indexed abstract — [VERIFY page from full text]).
DDR images are graded into six classes by image quality and DR level, comprising the five ICDR ordinal DR grades plus an ungradable/poor-quality class (Li et al., 2019; dataset documentation — [VERIFY]).
A subset of DDR images carries pixel-level annotations for four DR lesion types (microaneurysms, hemorrhages, hard exudates, soft exudates) (Li et al., 2019; dataset documentation).
DDR supports three tasks — image classification, semantic (lesion) segmentation, and lesion (object) detection — and is released as a general-purpose DR dataset (Li et al., 2019; dataset repository).

17. Epistemic Classification
Primary classification: Benchmark study / Dataset descriptor
Secondary classification: High-impact empirical evidence (large multi-site DR benchmark)
Justification: DDR is a large, multi-site, multi-device public DR dataset that has become a community benchmark. In this dissertation its epistemic role is instrumental and device-shift-related: it is a DR-label and camera-attribute source for Experiment 6, cited when device domain shift and cross-dataset robustness are discussed, rather than as direct evidence for or against the dissertation's own algorithmic claims.

18. Analytical Synthesis
DDR carries substantial benchmark epistemic weight as one of the larger, more device-diverse public DR datasets, aggregated across 147 hospitals, 23 provinces, and 42 camera types in China. For this dissertation its contribution is instrumental: it supplies DR labels and camera-attribute/device-heterogeneity context for the device-domain-shift experiment (H-6, §4.7), where the multi-camera, multi-site breadth is the decisive property. Sharing the ICDR 0–4 grading scale, it enables compatible cross-dataset DR-grading comparison alongside EyePACS and Messidor-2. It neither directly strengthens nor weakens the preprocessing-dominance argument, since the dissertation does not adopt its algorithmic results as findings; by providing large-scale raw multi-device images, however, it offers a clean setting for cross-device generalization study. The single-country sourcing and the modest lesion-annotation subset are structural limitations to acknowledge, and this card's reliance on the abstract plus dataset documentation (the full Elsevier article was not accessed) should be resolved by re-deriving the preprocessing, architecture, split, and metric fields from the PDF when available.
