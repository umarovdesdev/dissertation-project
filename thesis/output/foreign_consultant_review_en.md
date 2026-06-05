# REVIEW

**of the foreign scientific consultant on the dissertation of Yesmukhamedov Nurmaganbet Seitkaliuly**

on the topic *"Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"*, submitted for the degree of Doctor of Philosophy (PhD)

**Educational programme:** 8D061 — Information and Communication Technologies

---

## 1. General overview

Diabetic retinopathy (DR) remains one of the leading causes of preventable blindness among the working-age population worldwide, and its early stages are clinically asymptomatic. Reliable, large-scale screening of colour fundus images is therefore essential, yet the global shortage of ophthalmologists — particularly acute in resource-limited and rural healthcare settings — makes automated, computationally efficient diagnostic tools a pressing socio-economic need. The dissertation of Yesmukhamedov Nurmaganbet Seitkaliuly addresses precisely this problem, and does so from a methodologically well-motivated standpoint.

The work is timely and relevant not only because of its clinical motivation, but also because of the scientific stance it adopts. The dominant tradition in automated DR diagnosis treats image preprocessing as ancillary data preparation, assuming that a sufficiently deep convolutional neural network (CNN) learns the necessary invariances directly from raw or minimally normalised pixels. The candidate convincingly demonstrates the limitation of this assumption: fundus images acquired by different cameras, under different illumination conditions, and with different noise levels exhibit substantial domain variability that degrades the generalisation of CNN models. The justification for the proposed approach — treating preprocessing as an integral component of the diagnostic model that defines the feature space available to the network — is clearly articulated and scientifically sound.

## 2. Scientific novelty and methodological contribution

The principal scientific contribution of the dissertation is the conceptual and operational reframing of preprocessing as an integral model component, and the placement of this reframing under direct, controlled experimental test. The key methodological results are:

- An **8-stage integrated preprocessing pipeline (V5)** formalised as a binding part of the model specification, comprising canonical flip, OD-fovea rotation normalisation, FOV crop with isotropic resize and centred zero-padding, FOV mask generation as a 4th input channel, adaptive flat-field illumination correction (σ = 0.07 × FOV diameter), dual-constraint stochastic CLAHE on the LAB L-channel, augmentation, and dataset-specific channel-wise normalisation.
- A **dual-constraint stochastic CLAHE** variant adapted to the five-class DR context, with clip limit CL = min(clip_factor × tile_area / 256, global_threshold × tile_area) applied with 80% probability at training time and deterministically at inference.
- An **adaptive flat-field correction** whose Gaussian σ scales with the per-image field-of-view diameter rather than a fixed global value, applied only within the FOV mask.
- An explicit **binary FOV mask** introduced as a dedicated pipeline stage and appended as the 4th input channel, informing the CNN of valid pixel regions.
- A new explainability metric, **Attention–Lesion Overlap (ALO)**, an asymmetric measure of the fraction of a lesion covered by model attention, complemented by Intersection-over-Union (IoU).

These contributions differ from existing approaches in that the preprocessing pipeline is not an undocumented preliminary step but a formalised, parameterised, and experimentally validated component of the model, evaluated under a controlled 2×2 factorial design across two established architecture families (ResNet-50 and EfficientNet-B3) with a pre-registered dominance criterion.

## 3. Experimental evaluation and results

The experimental design is rigorous and comprehensive. The work draws on eight datasets organised into functional tiers: EyePACS (~35,126 images) for primary training and ablation; APTOS 2019 (~3,662) for cross-dataset transfer; IDRiD (516 images, 81 with pixel-level lesion masks) for clinical validation and explainability; Messidor-2 (~1,748) for clinical degradation; DDR (~13,673), ODIR-5K (~5,000), and RFMiD (~3,200) for device domain shift across four camera manufacturers (Canon, Topcon, Kowa, Zeiss); and a Kazakh clinical dataset for qualitative validation.

The evaluation is multi-metric (weighted F1, ROC-AUC, Cohen's Kappa with quadratic weights, accuracy), with all primary metrics reported as mean ± standard deviation under 5-fold patient-level stratified cross-validation with strict leakage control. Statistical reliability is ensured through McNemar and DeLong tests, mixed-effects modelling across folds, bootstrap confidence intervals (≥ 1000 resamples), and Bonferroni/Holm correction for multiple comparisons. The integrated configuration is benchmarked against an equivalent baseline (stretch-resize + ImageNet normalisation), and the pipeline's robustness is assessed through cross-dataset transfer (pre-registered generalisation ratio G ≥ 0.85), clinical degradation resistance, and cross-device evaluation. Image quality is independently quantified with CNR, VVI, entropy, and SSIM. This methodology meets international standards for experimental validation in medical image analysis.

## 4. Practical significance

The practical significance of the work is substantial. The integrated pipeline constitutes a transferable, interpretable, and device-robust preprocessing regime designed explicitly for constrained computational conditions, making it suitable for real-world deployment where high-end hardware is unavailable. The candidate further proposes a modular automated DR screening system architecture — comprising a configurable preprocessing engine, an inference module, telemedicine support, and a physician-in-the-loop decision-support interface — that integrates with PACS/EHR systems and national eHealth platforms. The approach is scalable and cost-effective, and is directly applicable to DR screening in rural and underserved regions, including the healthcare infrastructure of Kazakhstan. The explicit treatment of data security and regulatory compliance (GDPR/HIPAA-aligned) further strengthens its implementation potential.

## 5. Conclusion

The dissertation of Yesmukhamedov Nurmaganbet Seitkaliuly makes a significant, original, and scientifically substantiated contribution to the field of automated diabetic retinopathy diagnosis. The work is methodologically rigorous, experimentally thorough, and clearly delimited in its claims — the candidate explicitly states the boundaries of the work and refrains from overstated assertions. The dissertation meets the academic and methodological requirements for doctoral research and conforms to international standards for the award of a PhD degree. In my assessment, the author, Yesmukhamedov Nurmaganbet Seitkaliuly, fully deserves the degree of Doctor of Philosophy (PhD) under educational programme 8D061 — Information and Communication Technologies.

---

## Reviewer information

Name: Prof. Dr. Syed Abdul Rahman Al-Haddad

Academic title: Professor

Place of work: Department of Computer and Communication Systems Engineering, Faculty of Engineering, Universiti Putra Malaysia, 43400 UPM Serdang, Selangor

Country: Malaysia

Signature: /signature/   Date: "__" ____________ 20__

Stamp: / Professor, Department of Computer and Communication Systems Engineering, Faculty of Engineering, Universiti Putra Malaysia /
