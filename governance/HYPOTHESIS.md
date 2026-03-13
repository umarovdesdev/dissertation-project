## Central Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. The hypotheses H-1 through H-6 below are decompositions of this central hypothesis, each testing a specific aspect of the overarching claim.

---

**H-1 (Preprocessing Dominance).** If fundus images from EyePACS are processed through the 5-component preprocessing pipeline — comprising FOV standardization, green channel imaging, normalization, CLAHE enhancement (LAB color space, optimized clip limit), and HSV contrast enhancement — and a CNN classifier (ResNet-50 or EfficientNet-B3, pre-trained on ImageNet, adapted via fine-tuning) is trained on the processed images under a 2×2 factorial design, then classification performance measured by accuracy, precision, recall, F1-score (macro and weighted), ROC-AUC, and Cohen's Kappa (quadratic weights) will be statistically significantly higher than that of the same architecture trained on unprocessed images (resize only) of equivalent source distribution, independently for both ResNet-50 and EfficientNet-B3, satisfying the dominance criterion of weighted F1 Δ ≥ 5 pp, ROC-AUC Δ ≥ 0.02, and no Kappa degradation.

**H-2 (CLAHE Threshold Sensitivity).** If the CLAHE clip limit parameter is varied across controlled values on IDRiD, then per-class F1-score for DR 1 and DR 2 will exhibit a parameter-dependent sensitivity profile with at least one local optimum within the tested range.

### DROPPED (V3)

**H-3 (Two-Stage Fine-Tuning) — DROPPED IN V3.** If EfficientNetB0 (pre-trained on ImageNet) is adapted using a two-stage protocol — frozen base layers with classification head training, followed by progressive unfreezing of upper layers — under the same preprocessing regime, then test-set precision, recall, F1-score, and Cohen's Kappa will exceed those obtained from the frozen-only strategy (Stage 1 alone).

> **V3 Note:** H-3 is not tested in any V3 experiment. The two-stage fine-tuning protocol is retained as a training strategy but is not an independent hypothesis. Historical text preserved for audit trail.

### (End of dropped section)

**H-4 (Cross-Database Transferability).** If models trained on EyePACS with the 5-component preprocessing pipeline are evaluated on Messidor-2 and IDRiD without retraining, then the generalization ratio G = F1_external / F1_EyePACS will be ≥ 0.85 on both external datasets.

**H-5 (Explainability).** If Grad-CAM analysis is applied to a CNN (EfficientNet-B4) processing fundus images with and without preprocessing, then the Attention–Lesion Overlap (ALO) between Grad-CAM activation regions and IDRiD pixel-level lesion masks will be significantly higher for preprocessed models (ALO_preproc > ALO_baseline), demonstrating that preprocessing directs model attention toward clinically relevant structures (microaneurysms, hemorrhages, hard exudates, soft exudates). ALO is defined as `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)` and serves as the **primary** explainability metric, measuring what fraction of the lesion is covered by model attention (clinically relevant — lesion coverage). Intersection-over-Union (IoU) is retained as a **secondary** metric measuring symmetric spatial precision: `IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)`. Rationale: ALO directly answers the clinical question "Does the model attend to the lesion?" while IoU measures spatial precision. Both are informative; ALO is primary because lesion coverage is the clinically relevant property.

**H-6 (Device Robustness).** If preprocessed models trained on EyePACS (Canon CR-1) are evaluated on images from different fundus cameras (Topcon, Kowa via RFMiD; Canon, Topcon via DDR; Canon, Zeiss via ODIR-5K), then classification performance will be maintained across camera domains, with cross-device performance variance remaining within acceptable bounds relative to in-domain performance. Preprocessing standardizes retinal image appearance and reduces distribution differences between camera devices, leading to improved cross-device generalization.

---

## Argument Structure

The hypotheses above are linked by the following causal argument:

**Premise 1 (Domain Variability):** Fundus images acquired by different devices, under different illumination conditions, and with different noise levels exhibit substantial domain variability that degrades CNN classification performance.

**Premise 2 (Distribution Shift Degrades CNN):** This domain variability manifests as distribution shift in the input feature space, causing CNN models trained on one domain to generalize poorly to others.

**Premise 3 (Preprocessing Normalizes):** The proposed 5-component preprocessing pipeline standardizes retinal image appearance — normalizing illumination, enhancing contrast, extracting the most informative channel, and reducing device-specific artifacts — thereby reducing inter-domain distribution shift while preserving diagnostically relevant retinal features.

**Conclusion:** Application of the preprocessing pipeline prior to CNN classification improves diagnostic performance (H-1), is robust to parameter variation (H-2), transfers across datasets (H-4), directs attention to clinically relevant lesions (H-5), and generalizes across imaging devices (H-6). [Note V3: H-3 (two-stage fine-tuning) removed from causal chain — the fine-tuning protocol is used as a training strategy but is not an independently tested hypothesis.]
