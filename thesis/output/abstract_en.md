# ABSTRACT

**of the dissertation work by Yesmukhamedov Nurmaganbet Seitkaliuly titled "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification", submitted for the degree of Doctor of Philosophy (PhD) in the educational programme 8D061 — Information and Communication Technologies**

---

## Relevance of the research topic

Diabetic retinopathy (DR) is one of the leading causes of preventable blindness among the working-age population worldwide. Because the early stages of DR are clinically asymptomatic, timely detection depends on regular screening of fundus images, yet the number of ophthalmologists is insufficient to manually examine the rapidly growing population of diabetic patients — a shortage that is especially acute in resource-limited and rural healthcare settings, including the regions of Kazakhstan. Automated diagnosis based on convolutional neural networks (CNNs) is therefore a practically significant direction of research.

The dominant tradition in automated DR diagnosis — here designated paradigm **P1**, the end-to-end CNN paradigm — treats image preprocessing as ancillary data preparation that does not require methodological discussion, on the assumption that a sufficiently deep network learns the relevant invariances directly from raw or minimally normalised pixels. In practice, however, fundus images acquired by different cameras, under different illumination conditions, and with different noise levels exhibit substantial domain variability. This variability manifests as distribution shift in the input feature space and degrades the generalisation of CNN models trained on one domain when they are applied to another. The methodological gap motivating this dissertation is the absence of a formalised, experimentally controlled treatment of preprocessing as an integral component of the diagnostic model.

This work advances an alternative paradigm — **P2**, the integrated preprocessing-CNN paradigm — in which preprocessing is an integral component of the model itself, because it defines the feature space available to the network and therefore co-determines what the network can learn. The relevance of the topic follows from the need to reduce inter-device and inter-acquisition domain variability while preserving diagnostically relevant retinal features, and to do so under the computational constraints characteristic of real screening environments.

## Aim of the research

To develop and experimentally validate an integrated fundus image enhancement and CNN-based classification framework for automated multi-stage diabetic retinopathy diagnosis, in which an 8-stage preprocessing pipeline (V5) is treated as an integral component of the model, producing a statistically measurable and reproducible improvement in five-class DR diagnostic performance relative to an equivalent architecture trained without the pipeline, under constrained computational conditions.

## Objectives of the research

1. To analyse the medical, epidemiological, and technical context of automated DR diagnosis, the sources of fundus image quality variability, and the current state of CNN-based screening systems, and to formulate the research problem (Chapter 1).
2. To establish the theoretical foundations of image enhancement (histogram equalisation, dual-constraint CLAHE, spatial filtering), of convolutional neural networks (convolution, pooling, loss functions for imbalanced data, regularisation), of transfer and self-supervised representation learning, and of explainability methods (Grad-CAM, ALO, IoU) (Chapter 2).
3. To design and formalise the integrated preprocessing-CNN methodology — the 8-stage V5 pipeline, the CNN architectures (ResNet-50, EfficientNet-B3), the pretraining strategy, and the multi-metric evaluation framework (Chapter 3).
4. To experimentally validate the integrated pipeline through seven experiments: integrated-pipeline dominance (Experiment 1), component ablation and parameter sweeps (Experiment 2), cross-dataset transferability (Experiment 3), Grad-CAM explainability (Experiment 4), clinical degradation resistance (Experiment 5), device domain shift (Experiment 6), and small-data training (Experiment 7) (Chapter 4).
5. To validate the reliability of the results through statistical analysis and comparative benchmarking, and to state the limitations and boundary conditions of the approach (Chapter 5).
6. To design an architecture for an automated DR screening system suitable for resource-limited environments, with telemedicine and eHealth integration applicable to Kazakhstan healthcare infrastructure (Chapter 6).

## Object of the research

The process of automated diagnosis of diabetic retinopathy from colour fundus images using convolutional neural networks.

## Subject of the research

Methods and models for integrating fundus image preprocessing (enhancement) with CNN classification, and the effect of the integrated preprocessing-CNN pipeline on the diagnostic performance, transferability, interpretability, and device robustness of five-class DR classification.

## Methodology and methods of the research

The research methodology combines image-processing theory, deep-learning theory, and an experimentally controlled validation framework. The methods used include: classical computer-vision detection (optic disc and fovea localisation for rotation normalisation), adaptive flat-field illumination correction, dual-constraint Contrast-Limited Adaptive Histogram Equalisation (CLAHE) in the LAB colour space, CNN classification with ResNet-50 and EfficientNet-B3 backbones, transfer learning from ImageNet, ophthalmology-specific self-supervised pretraining (DINO / BYOL / SimCLR / MoCo family) on an unlabelled retinal fundus corpus, Focal Loss for class imbalance, Grad-CAM explainability analysis, and a statistical validation framework based on 5-fold patient-level stratified cross-validation, McNemar and DeLong tests, mixed-effects modelling, bootstrap confidence intervals, and Bonferroni/Holm correction for multiple comparisons.

## Scientific novelty

1. An 8-stage integrated V5 fundus preprocessing pipeline is formalised as a binding component of the diagnostic model (operationalisation of paradigm P2), comprising canonical flip, OD-fovea rotation normalisation, FOV crop with isotropic resize and centred zero-padding, FOV mask generation as a 4th input channel, adaptive flat-field correction (σ = 0.07 × FOV diameter), dual-constraint stochastic CLAHE on the LAB L-channel, augmentation, and dataset-specific channel-wise normalisation.
2. The hypothesis of integrated-pipeline dominance is formalised and tested under a controlled 2×2 factorial design (configurations A–D) over two established architectures (ResNet-50, EfficientNet-B3), with a pre-registered dominance criterion (Δ weighted F1 ≥ 5 pp, Δ ROC-AUC ≥ 0.02, no Cohen's Kappa degradation).
3. A dual-constraint stochastic CLAHE variant is adapted and validated within the five-class DR context (LAB L-channel; clip limit CL = min(clip_factor × tile_area / 256, global_threshold × tile_area); 80% train-time probability).
4. An adaptive flat-field illumination correction is introduced whose Gaussian σ scales with the per-image FOV diameter rather than using a fixed global value, applied only inside the FOV mask.
5. An explicit binary FOV mask is introduced as a dedicated pipeline stage and appended as the 4th input channel, informing the CNN of valid pixel regions and preventing padding artefacts from being learned as features.
6. Attention–Lesion Overlap (ALO) is introduced as a primary, asymmetric explainability metric that directly measures the fraction of a lesion covered by model attention, complemented by Intersection-over-Union (IoU) as a secondary metric, evaluated against IDRiD pixel-level lesion masks.
7. The integrated pipeline is validated across a multi-dataset, multi-device architecture (EyePACS, APTOS 2019, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD, and a Kazakh clinical dataset), including cross-dataset transfer, clinical degradation resistance, and device domain shift across four camera manufacturers (Canon, Topcon, Kowa, Zeiss).

## Statements submitted for defense

1. Preprocessing is an integral component of the diagnostic model, not ancillary data preparation: the integrated configuration (8-stage V5 pipeline + in-domain pretraining) achieves statistically significant dominance in five-class DR classification over an equivalent baseline configuration (stretch-resize + ImageNet normalisation), satisfying the pre-registered dominance criterion for both ResNet-50 and EfficientNet-B3 (H-1).
2. The contribution of individual pipeline stages can be quantified by component ablation, and the dual-constraint CLAHE clip-limit and the flat-field σ exhibit identifiable sensitivity profiles with a local optimum within the tested range (H-2).
3. A model trained on EyePACS with the V5 pipeline transfers to APTOS 2019 without retraining, achieving a generalisation ratio G = F1_APTOS / F1_EyePACS ≥ 0.85 (H-4).
4. The V5 pipeline redirects CNN attention toward clinically relevant lesion regions, demonstrated quantitatively by higher ALO (primary) and IoU (secondary) against IDRiD lesion masks and qualitatively by Grad-CAM overlays on a Kazakh clinical dataset (H-5).
5. The V5 pipeline reduces cross-dataset performance degradation Δ = F1_EyePACS_val − F1_external on IDRiD and Messidor-2 relative to the baseline (H-7).
6. The V5 pipeline maintains classification performance across images from different fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss) within acceptable bounds relative to in-domain performance (H-6).

## Main results of the research

1. A critical analysis of the medical, epidemiological, and technical context of automated DR diagnosis and of fundus image quality variability was carried out; the limitations of the end-to-end paradigm (P1) were identified and the research problem was formulated.
2. An 8-stage integrated V5 preprocessing pipeline was designed and formalised as an integral component of the diagnostic model (paradigm P2), comprising canonical flip, OD-fovea rotation normalisation, FOV crop with isotropic resize and centred zero-padding, FOV mask generation as a 4th input channel, adaptive flat-field correction, dual-constraint stochastic CLAHE, augmentation, and dataset-specific normalisation.
3. The dominance of the integrated configuration over the baseline was established under a controlled 2×2 factorial design (configurations A–D) on EyePACS for both ResNet-50 and EfficientNet-B3, evaluated against the pre-registered dominance criterion (Experiment 1).
4. The contribution of the individual pipeline stages was quantified through a 7-level component ablation, and the dual-constraint CLAHE clip-limit and the flat-field σ were characterised by parameter sweeps supported by image-quality metrics (CNR, VVI, entropy, SSIM) (Experiment 2).
5. The cross-dataset transferability of the pipeline was evaluated on APTOS 2019 without retraining against the pre-registered generalisation ratio G ≥ 0.85 (Experiment 3).
6. Grad-CAM explainability analysis, using the proposed Attention–Lesion Overlap (ALO, primary) and IoU (secondary) against IDRiD pixel-level lesion masks and qualitative overlays on a Kazakh clinical dataset, characterised the alignment of model attention with clinically relevant lesion structures (Experiment 4).
7. The clinical degradation resistance of the pipeline (IDRiD, Messidor-2; Experiment 5), its device robustness across four camera manufacturers (DDR, ODIR-5K, RFMiD; Experiment 6), and its trainability on small clinical data (Experiment 7) were evaluated.
8. A modular architecture for an automated DR screening system suitable for resource-limited environments, with telemedicine and eHealth integration applicable to Kazakhstan healthcare infrastructure, was designed.

## Theoretical significance

The work contributes a conceptual reframing of preprocessing as an integral model component that co-determines the feature space available to the CNN (paradigm P2), and places this reframing under direct empirical test against the end-to-end paradigm (P1). It provides a formal specification of the 8-stage pipeline, a mathematical formalisation of the dual-constraint CLAHE clip limit, the adaptive flat-field correction, and the ALO explainability metric, together with a rigorous statistical framework for validating preprocessing effects under class imbalance.

## Practical significance

The integrated pipeline constitutes a transferable, interpretable, and device-robust preprocessing regime for automated DR diagnosis under constrained computational conditions. A modular automated DR screening system architecture is proposed, with preprocessing-engine, inference, telemedicine, and physician-in-the-loop decision-support modules, integrable with PACS/EHR systems and the national eHealth platform, and applicable to DR screening in rural and underserved regions of Kazakhstan. *(Implementation acts and approbation certificates: see appendices.)*

## Reliability of the results

Reliability is ensured by: the use of large-scale and multiple public datasets (~35,126 EyePACS training images and seven additional datasets); 5-fold patient-level stratified cross-validation with strict leakage control; reporting of all primary metrics as mean ± standard deviation; a multi-metric assessment (weighted F1, ROC-AUC, Cohen's Kappa with quadratic weights, accuracy); statistical hypothesis testing (McNemar, DeLong), mixed-effects modelling across folds, bootstrap confidence intervals (≥ 1000 resamples), and Bonferroni/Holm correction; pre-registered success criteria; and comparison with published systems (IDx-DR, Eyenuk, DeepMind).

## Empirical (experimental) basis

Eight datasets organised into functional tiers: EyePACS (~35,126 images, primary training and ablation, Canon CR-1); APTOS 2019 (~3,662, cross-dataset transfer); IDRiD (516 images, 81 with pixel-level lesion masks, clinical validation and explainability, Kowa); Messidor-2 (~1,748, clinical degradation, Topcon); DDR (~13,673, device shift, Canon/Topcon); ODIR-5K (~5,000, device shift, Canon/Zeiss); RFMiD (~3,200, device shift, Topcon/Kowa); and a Kazakh clinical dataset (60 images, 30 patients × 2 eyes, balanced, qualitative validation). Image quality is evaluated with CNR, VVI, entropy, and SSIM.

## Approbation of the results and connection with scientific programmes

The results of the research were reported and discussed at international scientific forums, including the 3rd International Workshop on Digital Society (DS 2025, Istanbul, Türkiye, 28–30 October 2025), and published in international peer-reviewed journals. The research direction corresponds to the priorities of the digitalisation of healthcare and the development of artificial-intelligence technologies of the Republic of Kazakhstan (in accordance with subpara. 2, para. 3, art. 20 of the Law of the Republic of Kazakhstan "On Science").

## Publications

The main results of the dissertation are published in 5 scientific works, including: articles in journals indexed by Scopus / Web of Science — 1 (*Eastern-European Journal of Enterprise Technologies*, Q3); a paper in international conference proceedings indexed by Scopus — 1 (*Procedia Computer Science*, DS 2025); and articles in journals recommended by the Committee for Quality Assurance in Science and Higher Education (KKSON) of the Republic of Kazakhstan — 3 (*News of the NAS RK, Physico-Mathematical Series*; *Herald of the Kazakh-British Technical University*; *Herald of KazUTB*). See the List of published works below.

## Structure and length of the dissertation

The dissertation consists of an introduction, six chapters, a conclusion, a list of references used, and appendices. The work is supplemented with tables, figures, and the source code of the preprocessing pipeline.

---

# MAIN CONTENT OF THE WORK

**The introduction** substantiates the relevance of the topic, formulates the aim, objectives, object and subject of the research, the central hypothesis, the scientific novelty, the statements submitted for defense, the methodological basis, the theoretical and practical significance, the reliability of the results, the empirical basis, the approbation, the connection with scientific programmes, and the publications, and describes the structure and length of the dissertation.

**Chapter 1 — "Problem Domain Analysis and Current State of Automated Diabetic Retinopathy Diagnosis"** examines the medical and epidemiological context of DR and its clinical grading, the screening requirements of resource-limited settings, the sources of fundus image quality degradation and device-specific variability, deep-learning approaches to retinal image classification (CNN architectures, transfer and self-supervised pretraining, explainability), and provides a critical analysis of existing automated DR screening systems, concluding with the formulation of the research problem and the justification of the research direction.

**Chapter 2 — "Theoretical Foundations of Image Preprocessing and Deep Learning for Fundus Image Analysis"** establishes the mathematical foundations of image enhancement (histogram equalisation, dual-constraint CLAHE, spatial filtering), the theoretical framework of CNNs (convolution, pooling, loss functions for imbalanced data, regularisation), transfer and in-domain self-supervised representation learning, the mathematical modelling of laser-tissue interaction in retinal therapy, explainability (CAM, Grad-CAM, ALO, IoU), and image quality metrics for preprocessing evaluation.

**Chapter 3 — "Methodology of Integrated Preprocessing-CNN Pipeline Design"** formalises the unified 8-stage V5 preprocessing pipeline and the modified dual-constraint CLAHE algorithm, the augmentation strategy, and the external image ingestion protocol; specifies the CNN architectures (ResNet-50 and EfficientNet-B3); details the transfer-learning and ophthalmology-specific self-supervised pretraining methodology, the architecture adaptation for five-class classification, and the weighted (Focal) loss formulation; and defines the multi-metric evaluation and statistical reliability framework.

**Chapter 4 — "Experimental Research — Preprocessing Impact on CNN Diagnostic Performance"** presents the tiered dataset architecture and the seven experiments: Experiment 1 (integrated-pipeline dominance via a restored 2×2 factorial, configs A–D), Experiment 2 (V5 stage ablation across 7 levels, CLAHE threshold and flat-field σ sweeps with image-quality metrics), Experiment 3 (zero-shot cross-dataset transfer to APTOS 2019), Experiment 4 (Grad-CAM explainability with quantitative ALO/IoU on IDRiD and qualitative overlays on the Clinical dataset), Experiment 5 (clinical degradation resistance on IDRiD and Messidor-2), Experiment 6 (device domain shift on DDR, ODIR-5K, RFMiD), and Experiment 7 (small-data training on IDRiD with the Clinical dataset held out).

**Chapter 5 — "Reliability Validation and Comparative Analysis"** consolidates the explainability results, the statistical validation (bootstrap confidence intervals and mixed-effects modelling, final claim-strength classifications), the comparative analysis against published systems (IDx-DR, Eyenuk, DeepMind) and the performance-complexity trade-off, and states the limitations and boundary conditions of the proposed approach.

**Chapter 6 — "Architecture of an Automated DR Screening System for Resource-Limited Environments"** specifies the functional and non-functional requirements, the modular architecture with PACS and EHR integration, the AI processing module (configurable preprocessing engine and inference module), clinical workflow integration (telemedicine, portable-device and national eHealth-platform support, physician-in-the-loop decision support), and the data security and regulatory-compliance framework (GDPR/HIPAA-aligned), with its applicability to Kazakhstan healthcare infrastructure.

---

# CONCLUSION

1. Preprocessing was formalised as an integral component of the diagnostic model (paradigm P2) through an 8-stage V5 pipeline, and the hypothesis of integrated-pipeline dominance was placed under controlled experimental contrast against the baseline (paradigm P1) on EyePACS, providing an empirical comparison of the two paradigms under otherwise matched conditions.
2. A component-ablation analysis quantified the contribution of the individual pipeline stages, and the dual-constraint CLAHE and adaptive flat-field correction were characterised by parameter sweeps with identifiable optima, supported by image-quality metrics (CNR, VVI, entropy, SSIM).
3. The cross-dataset transferability of the integrated pipeline was evaluated on APTOS 2019 against the pre-registered generalisation criterion G ≥ 0.85.
4. Grad-CAM explainability analysis, using the proposed ALO metric (primary) and IoU (secondary) against IDRiD pixel-level lesion masks and qualitative overlays on a Kazakh clinical dataset, characterised the alignment of model attention with clinically relevant lesion structures.
5. The clinical degradation resistance of the pipeline was evaluated on IDRiD and Messidor-2, and its device robustness across four camera manufacturers was evaluated on DDR, ODIR-5K, and RFMiD.
6. An architecture for an automated DR screening system for resource-limited environments was designed, with telemedicine and eHealth integration applicable to the healthcare infrastructure of the Republic of Kazakhstan.

The dissertation thus delivers a transferable, interpretable, and device-robust integrated preprocessing-CNN regime for automated diabetic retinopathy diagnosis under constrained computational conditions. The work does not claim global state-of-the-art, clinical device certification, replacement of the ophthalmologist, or cross-modality transfer; these boundaries are stated explicitly.

---

# LIST OF PUBLISHED WORKS ON THE DISSERTATION TOPIC

**Articles in journals indexed by Scopus / Web of Science:**

1. Sapakova S., Yesmukhamedov N., Sapakov A. Development of an image quality enhancement approach for diabetic retinopathy diagnosis // Eastern-European Journal of Enterprise Technologies. — 2025. — Vol. 4, No. 9(136). — P. 79–88. (Scopus, Q3). https://doi.org/10.15587/1729-4061.2025.335570

**Papers in international conference proceedings indexed by Scopus:**

2. Sapakova S., Yesmukhamedov N., Sapakov A., Yemberdiyeva A., Kozhamkulova Z. Methods for pre-processing and analysis of fundus images for detection of diabetic retinopathy // Procedia Computer Science. — 2025. — Vol. 272. — P. 496–501. (The 3rd International Workshop on Digital Society — DS 2025, Istanbul, Türkiye). https://doi.org/10.1016/j.procs.2025.10.237

**Articles in journals recommended by the KKSON of the Republic of Kazakhstan:**

3. Yesmukhamedov N.S., Sapakova S., Al-Haddad S.A.R., Daniyarova D. Development of an information system architecture for healthcare institutions using artificial intelligence // News of the National Academy of Sciences of the Republic of Kazakhstan, Physico-Mathematical Series. — 2025. — Vol. 2(354). — P. 74–91. https://doi.org/10.32014/2025.2518-1726.345

4. Yesmukhamedov N.S., Sapakova S.Z., Kozhamkulova Zh.Zh., Daniyarova D.R., Armankyzy R. Methods for preprocessing and analysis of fundus images for diabetic retinopathy detection // Herald of the Kazakh-British Technical University. — 2025. — No. 4(75). — Vol. 22. — P. 119–130. https://doi.org/10.55452/1998-6688-2025-22-4-119-130

5. Sapakova S.Z., Daniyarova D.R., Yesmukhamedov N.S., Armankyzy R., Yemberdiyeva A.B., Kaldybaeva A.S. Mathematical modeling of laser exposure on fundus tissues in the treatment of diabetic retinopathy // Herald of KazUTB. — 2024. — Vol. 2, No. 27-740. https://doi.org/10.58805/kazutb.v.2.27-740
