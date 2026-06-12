# 1. Bibliographic Metadata

**Full citation (APA 7)**
Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. *Proceedings of the IEEE International Conference on Computer Vision (ICCV)*, 618–626.

**DOI:** 10.1109/ICCV.2017.74

**Journal / Conference:** IEEE International Conference on Computer Vision (ICCV) 2017 (IEEE, publisher)

**Year:** 2017

**Publication type:** Empirical methodology paper (explainability technique development + human studies)

**Research domain classification:** Explainable AI (XAI), CNN interpretability, weakly-supervised localization, computer vision.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| CNN-based classification study | ✔ (instrumentally) | Method is applied to off-the-shelf classification CNNs (VGG-16, AlexNet, ResNet). |
| Explainability / visualization method | ✔ | Primary contribution: Grad-CAM and Guided Grad-CAM. |
| External / cross-dataset validation | ❌ | Not a generalization study. |
| EyePACS / Messidor / IDRiD benchmarking | ❌ | No retinal datasets used. |
| Vision Transformer application | ❌ | Pre-ViT; CNN-only. |
| Clinical prospective validation | ❌ | None. |
| Human-subjects evaluation | ✔ | Amazon Mechanical Turk studies for class-discrimination and trust. |

**Justification:** The paper proposes a gradient-based class-discriminative localization technique and evaluates it on ImageNet localization, PASCAL VOC class-discrimination/trust human studies, captioning, and VQA. It is a **methodology reference**, not a domain (DR) study.

---

# 3. Research Problem

**Specific problem addressed:** CNN-based models are accurate but opaque ("hard to interpret"); existing pixel-space gradient visualizations (Guided Backpropagation, Deconvolution) are not class-discriminative, and CAM requires architectural changes + retraining. The paper seeks a class-discriminative visual explanation applicable to *any* CNN-based architecture without retraining.

- Generalization? No (interpretability, not generalization).
- Preprocessing? No.
- Architecture scaling? No.
- Lesion detection? No (but the localization principle is later borrowed for lesion-overlap evaluation in the dissertation).
- Clinical deployment? No (XAI background only).
- **Explainability? Yes — core.**

---

# 4. Datasets Used

| Dataset | Public/Private | Role | Notes |
| --- | --- | --- | --- |
| ImageNet (ILSVRC-15) | Public | Weakly-supervised localization evaluation (val set) | Top-1 / top-5 localization & classification error. |
| PASCAL VOC 2007 | Public | Human studies (class-discrimination, trust) | VGG-16 and AlexNet finetuned on train; visualizations on val. |
| MS COCO (via neuraltalk2 captioning) | Public | Captioning visualization | Qualitative. |
| VQA dataset | Public | VQA model visualization | Qualitative. |

**External dataset used?** N/A (general vision benchmarks). **Cross-dataset testing?** No. **No retinal/DR data.**

---

# 5. Preprocessing Pipeline

[NOT REPORTED] — preprocessing is the standard pipeline of the off-the-shelf models used (e.g., VGG-16 Caffe Model Zoo). No CLAHE, color normalization, FOV masking, or lesion enhancement is relevant; the paper is not a preprocessing study.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Architectures visualized | VGG-16, AlexNet, ResNet (incl. ResNet-18 and 200-layer ResNet for VQA) |
| Method | Gradient-weighted Class Activation Mapping (Grad-CAM); Guided Grad-CAM = Grad-CAM ⊙ Guided Backpropagation |
| Pretraining source | ImageNet (off-the-shelf); VGG-16/AlexNet finetuned on PASCAL VOC 2007 for human studies |
| Mechanism | Gradients of target class score flow into the final convolutional layer → neuron-importance weights via global-average-pooled gradients → weighted sum of feature maps → ReLU → coarse class-discriminative heatmap |
| Architectural change required | None (generalizes CAM without GAP-layer surgery or retraining) |
| Cost | One forward + one partial backward pass per image (≈ order of magnitude cheaper than occlusion). |

---

# 7. Validation Design

- Internal-only quantitative evaluation on ILSVRC-15 val (localization) — no cross-dataset or external validation.
- Human-subjects studies on PASCAL VOC 2007 (43 AMT workers class-discrimination; 54 AMT workers trust).
- No k-fold cross-validation, no confidence intervals, no statistical significance tests reported for the localization table.

---

# 8. Performance Metrics

- **ILSVRC-15 weakly-supervised localization (VGG-16):** Grad-CAM achieves significantly lower top-1/top-5 localization error than c-MWP and Simonyan et al.; better top-1 localization error than CAM, while CAM's architectural change *increases* top-1 classification error by **2.98%** (Grad-CAM makes no classification-accuracy compromise). Exact numeric cells in Table 1 not transcribed here (reported as "lower is better"; bounding box from largest connected segment after binarizing the map at 15% of max intensity).
- **Class-discrimination human study (PASCAL VOC):** Guided Grad-CAM correctly identifies visualized category in **61.23%** of cases vs **44.44%** for Guided Backpropagation (a **16.79%** improvement); Grad-CAM raises Deconvolution from **53.33%** to **61.23%**.
- **Trust human study:** With Guided Backpropagation, VGG-16 receives average reliability score **1.00** vs AlexNet; with Guided Grad-CAM, **1.27** (closer to "clearly more reliable"). VGG-16 = 79.09 mAP vs AlexNet 69.20 mAP on PASCAL classification (only same-prediction instances used).
- **Dataset-bias case study (doctor vs nurse):** biased search-engine training data (78% male doctors, 93% female nurses) → 82% generalization; after debiasing → **90%**.

Statistical tests: [NOT REPORTED]. Confidence intervals: [NOT REPORTED].

---

# 9. Authors' Claims

- Grad-CAM produces class-discriminative localizations for any CNN-based model without architectural change or retraining.
- It generalizes CAM to a broad family of CNNs (FC layers, structured outputs, multimodal inputs).
- Guided Grad-CAM yields high-resolution, class-discriminative explanations.
- Visualizations outperform prior methods on interpretability and faithfulness; correlate with occlusion maps.
- Explanations help humans establish trust and discern a stronger from a weaker classifier even under identical predictions.
- Grad-CAM can expose and help remove dataset bias.

---

# 10. Empirical Support Assessment

| Claim | Evidence | Support |
| --- | --- | --- |
| Class-discriminative without retraining | Fig. 1 cat/dog separation; ILSVRC loc table | Supported |
| Outperforms CAM on localization w/o accuracy loss | Table 1; CAM +2.98% top-1 cls error | Supported |
| Improves human class-discrimination | 61.23% vs 44.44% | Supported (n=43 workers) |
| Aids trust calibration | 1.27 vs 1.00 reliability score | Supported but small sample (n=54) |
| Reveals dataset bias | doctor/nurse 82%→90% | Supported (single case study) |

External validation: N/A. CIs: none. Class imbalance: N/A. Statistical testing: minimal. Human-study sample sizes are modest.

---

# 11. Internal Validity

- Localization evaluated internally on one val set; threshold (15% of max) and largest-segment bounding box are heuristic choices that affect the metric.
- Human studies have small worker counts and no inter-rater reliability statistics.
- Faithfulness argued via correlation with occlusion maps (qualitative/illustrative), not a formal metric with CIs.
- Method is deterministic given a model; no augmentation-inflation risk.

---

# 12. External Validity

- Architecture-agnostic by design (VGG/AlexNet/ResNet, captioning, VQA) — strong portability across CNN families.
- No evaluation on medical or retinal imagery; transfer to fundus-lesion localization is an extrapolation the dissertation must justify.
- Low compute cost → clinically feasible as an inference-time explainability tool.

---

# 13. Strengths

- General, retraining-free, architecture-agnostic.
- Combines coarse class-discrimination with high-resolution detail (Guided Grad-CAM).
- Quantitative localization + human-subject validation + faithfulness correlation.
- Computationally cheap (single partial backward pass).
- Demonstrated practical utility (failure analysis, bias detection).

---

# 14. Limitations

**Explicit (authors):** Discriminative ability of Grad-CAM degrades in shallower layers / across dimensionality changes; Guided Backpropagation component inherits its known limitations.

**Implicit (methodological):** Coarse spatial resolution at the final conv layer; heuristic thresholding; no medical-domain validation; human studies under-powered; no confidence intervals or significance testing; faithfulness shown by correlation, not proof.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| Preprocessing-dominance hypothesis | Peripheral | Not a preprocessing study. |
| Cross-database generalization | Peripheral | Not addressed. |
| EyePACS/Messidor/IDRiD benchmarking | Peripheral | No retinal data. |
| CNN vs ViT | Peripheral | Pre-ViT. |
| **Explainability (Grad-CAM ALO/IoU)** | **Core / foundational** | Canonical primary source for the Grad-CAM method underlying Exp 4 (§4.5) lesion-localization and §2.5.1–§2.5.2 formalization. |
| Clinical degradation | Peripheral | N/A. |

**Risk of contradiction:** None. This is a method the dissertation *uses*, not a competing empirical result. Must be cited as the foundational Grad-CAM reference; ALO/IoU lesion-overlap framing is the dissertation's own application, not claimed by Selvaraju et al.

---

# 16. Citation-Ready Statements

1. "Grad-CAM uses the gradients of any target concept … flowing into the final convolutional layer to produce a coarse localization map highlighting the important regions in the image for predicting the concept." (Abstract)
2. "Our approach … is applicable to a wide variety of CNN model-families … without architectural changes or re-training." (Abstract)
3. "Grad-CAM also achieves better top-1 localization error than CAM, which requires a change in the model architecture, necessitates re-training and thereby achieves worse classification errors (2.98% increase in top-1)." (§4.1)
4. "When viewing Guided Grad-CAM, human subjects can correctly identify the category being visualized in 61.23% of cases (compared to 44.44% for Guided Backpropagation)." (§5.1)
5. "Grad-CAM can help detect and remove biases in datasets, which is important not just for generalization, but also for fair and ethical outcomes." (§6.2)

---

# 17. Epistemic Classification

**Methodological precedent / Foundational (for explainability).**

**Justification:** Grad-CAM is one of the two or three canonical gradient-based CNN explanation techniques and is the operational explainability method for the dissertation's lesion-localization evaluation. Its epistemic weight is high *as a method*, but it carries no DR-domain empirical results.

---

# 18. Analytical Synthesis

This paper supplies the foundational method for the dissertation's explainability experiment (Exp 4, §4.5) and the theoretical formalization in §2.5.1–§2.5.2. Its epistemic contribution is methodological: a class-discriminative, retraining-free, architecture-agnostic visualization that the dissertation borrows to compute attention-lesion overlap (ALO) and IoU against IDRiD pixel-level annotations. It neither strengthens nor weakens the preprocessing-dominance argument, because it makes no claim about preprocessing or cross-dataset robustness. Its empirical evidence (ILSVRC localization, AMT human studies) is in the natural-image domain, so the dissertation must explicitly justify transferring Grad-CAM to fundus lesion localization rather than citing Selvaraju et al. as evidence of clinical validity. The method's low inference cost supports its feasibility within a clinical screening pipeline. Cite it strictly as the Grad-CAM primary source, alongside #57 (CAM) and #58 (Grad-CAM++) which complete the lineage.

End of Literature Card.
