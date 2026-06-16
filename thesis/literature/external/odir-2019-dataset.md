Literature Card: ODIR-5K Dataset Descriptor (online resource)

> Source-access note: ODIR-5K has NO peer-reviewed descriptor article (the LITERATURE_INDEX
> "TO BE IDENTIFIED" flag is resolved by this finding). It is the dataset of the 2019 Peking
> University International Competition on Ocular Disease Intelligent Recognition (ODIR-2019).
> This card is compiled from the official challenge site (odir2019.grand-challenge.org) and the
> public dataset mirror. It must therefore be cited as an ELECTRONIC RESOURCE, not as a journal
> article. Fields requiring documentation not published on the challenge site are marked
> [NOT REPORTED].

1. Bibliographic Metadata
Full citation (electronic resource, GOST 7.1-2003 style):
Peking University International Competition on Ocular Disease Intelligent Recognition (ODIR-2019) [Electronic resource]. – Grand Challenge, 2019. – URL: https://odir2019.grand-challenge.org/ (date of access: 16.06.2026).
Data collector: Shanggong Medical Technology Co., Ltd.
DOI: [NOT APPLICABLE — no DOI; challenge dataset]
Venue: ODIR-2019 challenge, Peking University (International Competition on Ocular Disease Intelligent Recognition)
Year: 2019
Publication type: Dataset / online resource (challenge dataset; not a peer-reviewed article, not a systematic review)
Research domain classification: Biomedical imaging; ophthalmology; multi-disease ocular classification; computer-aided diagnosis

2. Study Type Classification
Primary classification: Dataset descriptor (online resource; multi-disease ocular dataset)
Secondary applicable classifications:

Benchmark study (the reference dataset for the ODIR-2019 challenge)
Methodological precedent (patient-level, both-eyes multi-label annotation by trained readers)

Justification: ODIR-5K is a challenge dataset providing paired left/right-eye color fundus images with patient-level multi-label diagnoses. It is not an algorithm study; it is the data resource on which ODIR-2019 competitors built models.

3. Research Problem
Specific problem addressed: Provision of a "real-life" multi-disease ophthalmic dataset — paired both-eye fundus images with patient-level diagnostic labels and age — for developing automated multi-disease ocular recognition.
Problem dimensions addressed:

Generalization: Eight diagnostic categories across a 5,000-patient cohort from multiple Chinese centers.
Device domain shift (relevant here): images captured by "various cameras in the market" (Canon, Zeiss, Kowa), supporting cross-device study.
Clinical deployment: Targets real-world ophthalmic screening (patient-level, both-eye decisions).
Preprocessing: [NOT REPORTED] — none described on the challenge site.
Architecture scaling: [NOT APPLICABLE] — dataset resource, no model is its contribution.

4. Datasets Used
This is a dataset descriptor. The following describes ODIR-5K itself:
Dataset: ODIR-5K (Ocular Disease Intelligent Recognition)

Public / Private: Public (challenge dataset; download via the official challenge site)
Total sample size: 5,000 patients; color fundus photographs of both (left and right) eyes per patient, plus patient age. Total image count: [NOT REPORTED as a single figure on the challenge site] (≈2 images/patient implied)
Class taxonomy: Patient-level multi-label across 8 categories — Normal (N), Diabetes (D), Glaucoma (G), Cataract (C), Age-related Macular Degeneration (A), Hypertension (H), Pathological Myopia (M), Other diseases/abnormalities (O). One patient may carry one or multiple labels.
Train/validation/test split: The challenge provided training plus off-site/on-site test partitions; exact per-partition counts [NOT REPORTED] from retrieved material.
External dataset used? No (it is itself the dataset)
Cross-dataset testing performed? No

Image acquisition details:

Cameras: "various cameras in the market" — Canon, Zeiss, and Kowa fundus cameras
Collection: by Shanggong Medical Technology Co., Ltd. from different hospitals/medical centers in China
Field of view / resolution / format: [NOT REPORTED] on the challenge site
Acquisition period: [NOT REPORTED]

5. Preprocessing Pipeline
No preprocessing pipeline is described on the challenge site; images are provided for downstream researchers.
Resizing [NOT REPORTED]
Cropping [NOT REPORTED]
Normalization [NOT REPORTED]
CLAHE [NOT REPORTED]
Color normalization [NOT REPORTED]
Augmentation [NOT REPORTED]
Image quality filtering [NOT REPORTED]
Lesion enhancement methods [NOT REPORTED]

6. Model Architecture
Not applicable. The dataset resource does not present, train, or evaluate a model as its contribution.
Architecture type: [NOT APPLICABLE]
Pretraining source: [NOT APPLICABLE]
Transfer learning protocol: [NOT APPLICABLE]
Input resolution: [NOT APPLICABLE]
Loss function: [NOT APPLICABLE]
Optimizer: [NOT APPLICABLE]
Epochs: [NOT APPLICABLE]
Hyperparameters: [NOT APPLICABLE]

7. Validation Design
Not applicable in the algorithmic sense. Annotation/label methodology: "Annotations are labeled by trained human readers with quality control management," classifying each patient into the eight labels based on both-eye images and patient age. No algorithmic internal/cross/external/prospective validation is part of the dataset resource.

8. Performance Metrics
Not applicable. No model is evaluated as the dataset's contribution; no AUC/sensitivity/specificity/accuracy/F1/Kappa/confusion matrix is reported by the resource itself.

9. Authors' Claims
Performance claims: None (no model).
Generalization claims: The dataset is presented as a "real-life" set of patient information collected across different hospitals/medical centers in China with cameras varying across the market.
Clinical applicability claims: Targets patient-level multi-disease ocular screening from both-eye images plus age.
Superiority claims: None.

10. Empirical Support Assessment
Does data support generalization claims? The multi-center, multi-camera, 8-disease, both-eye design supports the "real-life" framing; per-class counts and exact image totals [NOT REPORTED].
Is external validation robust? Not applicable — dataset resource.
Are confidence intervals reported? No (no metrics).
Is dataset size adequate? 5,000 patients (≈10,000 images) is a moderate-to-large multi-disease cohort; per-disease counts for rarer categories are presumably imbalanced ([NOT REPORTED]).
Is class imbalance addressed? [NOT REPORTED]; multi-label real-world distribution implies imbalance.
Is statistical testing adequate? Not applicable.

11. Internal Validity
No model is part of the resource, so model-level validity does not apply. Annotation-level considerations:

Annotation reliability: labels assigned by trained human readers under quality-control management; inter-reader agreement statistics [NOT REPORTED].
Patient-level multi-label structure: labels are per patient (both eyes + age), not per image — important for any image-level use, which must map patient labels to eyes carefully.
Multi-device confound: multiple camera brands introduce appearance variation by design.
Provenance: this card rests on the challenge site and a public mirror; no peer-reviewed methodology document exists to audit.

12. External Validity
Cross-population transferability: Chinese multi-center cohort; transfer to other populations is undemonstrated by the resource itself.
Dataset portability: High — publicly downloadable from the challenge site; widely mirrored (e.g., Kaggle).
Clinical feasibility: Patient-level, both-eye, multi-camera design reflects realistic ophthalmic screening practice.
Hardware constraints: Canon, Zeiss, Kowa fundus cameras span the dataset; no computational requirement stated.

13. Strengths

Patient-level, both-eye design: paired left/right images plus age, closer to real clinical decision-making than single-image datasets.
Multi-disease breadth: eight categories including diabetes, glaucoma, cataract, AMD, hypertension, and pathological myopia.
Multi-device, multi-center acquisition: Canon/Zeiss/Kowa across multiple Chinese centers — relevant to device domain shift (H-6).
Public challenge benchmark: ODIR-2019 competition provides an independent community-use context.

14. Limitations
Explicit (stated by authors): [NOT REPORTED — no peer-reviewed descriptor.]
Implicit (methodological):

No peer-reviewed descriptor: bibliographic and methodological detail rests on the challenge site and mirrors, not a citable article; reproducibility documentation is thinner than for journal-published datasets.
Patient-level labels: mapping patient-level multi-labels to individual eye images is non-trivial and a source of label noise for image-level tasks.
Undisclosed split/format/resolution: exact image counts, partitions, format, and resolution are [NOT REPORTED] on the site.
Single-country sourcing: Chinese centers only.
Multi-camera confound: appearance variation across brands.

15. Relevance to My Dissertation
Relevance to preprocessing dominance hypothesis:
Low. ODIR-5K is a multi-disease (not DR-grading) dataset; not a primary preprocessing-dominance vehicle.
Relevance to cross-database / device domain shift:
High. ODIR-5K is one of the three device-domain-shift datasets (with RFMiD and DDR) for Experiment 6 (H-6, §4.7); its multi-camera (Canon/Zeiss/Kowa), multi-center acquisition is the salient property. Used in this dissertation for DR-relevant labels (the Diabetes/"D" category) and camera-attribute context only; its 8-disease multi-label taxonomy is outside the DR 0–4 scope (SB).
Relevance to EyePACS/Messidor benchmarking:
Low. Different task (multi-disease patient-level vs DR grading); complementary, not a substitute benchmark.
Relevance to Vision Transformer comparison:
Indirect. Used by later architecture studies; the resource itself is dataset-only.
Risk of contradiction:
Low. As a dataset resource it makes no algorithmic claim that could contradict the dissertation; scope must be respected (DR-relevant / camera-attribute use only, SB).

16. Citation-Ready Statements

ODIR-5K consists of records from 5,000 patients, including age, color fundus photographs of both eyes, and diagnostic keywords, collected by Shanggong Medical Technology Co., Ltd. from different hospitals/medical centers in China (ODIR-2019 challenge site).
"Annotations are labeled by trained human readers with quality control management," classifying each patient into eight labels based on both-eye images and patient age (ODIR-2019 challenge site).
ODIR-5K provides eight categories — Normal, Diabetes, Glaucoma, Cataract, Age-related Macular Degeneration, Hypertension, Pathological Myopia, and Other — and is multi-label (one patient may carry one or multiple labels) (ODIR-2019 challenge site).
The fundus images "are captured by various cameras in the market" — Canon, Zeiss, and Kowa (ODIR-2019 challenge site).

17. Epistemic Classification
Primary classification: Benchmark study / Dataset descriptor (online resource)
Secondary classification: Methodological precedent (patient-level both-eye multi-label annotation)
Justification: ODIR-5K is the reference dataset of the ODIR-2019 challenge and a widely used multi-disease ocular benchmark. In this dissertation its epistemic role is instrumental and device-shift-related: it is a DR-relevant-label and camera-attribute source for Experiment 6, cited as an electronic resource when device domain shift is discussed, not as evidence for or against DR-grading algorithmic claims.

18. Analytical Synthesis
ODIR-5K carries benchmark epistemic weight as the ODIR-2019 challenge dataset and a widely mirrored multi-disease ocular resource, distinguished by its patient-level, both-eye design and its multi-camera (Canon/Zeiss/Kowa), multi-center acquisition. For this dissertation its role is instrumental and scope-bounded: it supplies DR-relevant labels (the Diabetes category) and camera-attribute/device-heterogeneity context for the device-domain-shift experiment (H-6, §4.7), and it is cited only at the DR-relevant / camera-attribute level because its eight-disease, patient-level multi-label taxonomy lies outside the DR 0–4 target (SB). It neither strengthens nor weakens the preprocessing-dominance argument, since the dissertation adopts none of its results as findings. The decisive practical facts are that ODIR-5K has no peer-reviewed descriptor — so it must be cited as an electronic resource (resolving the prior "TO BE IDENTIFIED" flag) — and that its patient-level labels require careful mapping to individual eye images for any image-level use.
