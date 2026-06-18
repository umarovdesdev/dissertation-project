# DEFINITIONS

**Architectural complexity** — the capacity of a CNN as defined by the number of convolutional layers, total trainable-parameter count, filter-size range, and the presence or absence of regularization components (batch normalization, dropout).

**Baseline (baseline arm)** — the reference configuration of Experiment 1: stretch-resize to 512×512 followed by ImageNet normalization, producing a 3-channel tensor with no field-of-view mask and no preprocessing stages; the backbone is initialized from ImageNet.

**CLAHE (Contrast-Limited Adaptive Histogram Equalization)** — an adaptive contrast-enhancement method operating on local image tiles with a clip limit that bounds contrast amplification; applied in the pipeline to the LAB L-channel under a dual-constraint clip limit (Stage 5).

**Composite independent variable** — the combined manipulated factor of Experiment 1 (H-1), in which the full-pipeline arm differs from baseline jointly along the preprocessing axis (eight-stage pipeline vs. stretch-resize + ImageNet normalize) and the pretraining axis (ophthalmology-specific self-supervised pretraining vs. ImageNet).

**Convolutional Neural Network (CNN)** — a neural architecture comprising convolutional and pooling layers for feature extraction and fully connected layers for classification; the classification backbone operating on preprocessed fundus images for five-class DR staging.

**Cross-validation** — a validation strategy using 5-fold patient-level stratified splitting; for each fold, four folds serve as training data and one as test data, with no patient's images appearing in both partitions; metrics are reported as mean ± standard deviation across folds.

**Data augmentation** — image transformations (flips, rotations, zoom, brightness/contrast, PCA colour) applied to the training data to increase variability and improve generalization; the train-only Stage 6 of the pipeline.

**Dataset-specific normalization** — channel-wise normalization (Stage 7) using mean and standard deviation computed from the training split of the primary dataset rather than ImageNet statistics; the normalization of the full pipeline.

**Diabetic retinopathy (DR)** — a microvascular complication of diabetes mellitus and a leading cause of preventable vision loss, graded in five severity stages (0 — none, 1 — mild, 2 — moderate, 3 — severe, 4 — proliferative).

**Diagnostic effectiveness** — the joint performance profile on four primary metrics (accuracy, weighted F1-score, ROC-AUC, and Cohen's Kappa with quadratic weights) computed on the held-out test partition.

**Domain shift** — the distributional difference between training data and target deployment data arising from differences in imaging equipment, patient populations, or acquisition protocols.

**Field-of-view (FOV) mask** — a binary spatial mask (1.0 = real fundus data, 0.0 = zero-padding) generated at Stage 3 and appended as the 4th input channel, allowing the CNN to distinguish genuine retinal pixels from padded background.

**Flat-field correction (adaptive)** — Gaussian-blur subtraction with adaptive σ = 0.07·D (D = FOV diameter), applied inside the FOV mask to normalize uneven illumination while preserving local contrast; Stage 4 of the pipeline.

**Fundus image** — a retinal photograph acquired by fundoscopy; the exclusive imaging modality of the dissertation and the input to the preprocessing pipeline and the CNN classifier.

**Generalization (cross-database)** — the ratio of test-set F1-score on a secondary dataset to test-set F1-score on the primary dataset under the same trained model without retraining; the generalization ratio G = F1_external / F1_EyePACS.

**Grad-CAM (Gradient-weighted Class Activation Mapping)** — an explainability method producing class-discriminative localization maps from a gradient-weighted combination of final convolutional feature maps; an interpretability tool, not a clinical localization of pathology.

**Image quality** — the measurable capacity of a fundus image to support automated detection of microvascular features relevant to DR staging, assessed through downstream classification performance rather than a subjective visual score.

**Integrated pipeline dominance (H-1)** — the primary hypothesis that the integrated full-pipeline configuration outperforms the baseline as a unitary system, validated when the empirical dominance criterion (≥ 5 pp weighted-F1 gain, ≥ 0.02 ROC-AUC gain, no Cohen's Kappa degradation) is satisfied.

**Ophthalmology-specific self-supervised pretraining** — self-supervised pretraining of the CNN backbone on an unlabeled retinal fundus corpus (no DR labels), used as the full-pipeline-arm initialization; learns fundus-domain representations directly on the 4-channel pipeline tensor.

**Physician-in-the-loop** — a design paradigm in which the clinician acts not merely as a consumer of AI outputs but as a tuner and auditor who interprets results and adjusts the system; the proposed system is a decision-support tool within this paradigm.

**Preprocessing pipeline** — the canonical ordered eight-stage sequence (Stages 0–7) applied to fundus images prior to CNN input; the full pipeline applies all eight stages, producing a 4-channel tensor (RGB + FOV mask).

**Resource-limited environment** — a deployment context characterized by at least two of: absence of GPU acceleration; available RAM below 16 GB; batch-processing-time constraints; network connectivity precluding continuous cloud-API reliance.

**Transfer learning** — the reuse and adaptation of pretrained network weights to the fundus-image domain; under H-1 the initialization source is slaved to the arm (ImageNet for baseline, ophthalmology-specific SSL for the full pipeline).

**Weighted loss function** — a cross-entropy loss with class-specific weights addressing class imbalance and exploiting the ordinal structure of the five-class DR grading.
