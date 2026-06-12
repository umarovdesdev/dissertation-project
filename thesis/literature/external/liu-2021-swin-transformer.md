# 1. Bibliographic Metadata

**Full citation (APA 7)**
Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., & Guo, B. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 10012–10022. (arXiv:2103.14030)

**DOI:** 10.1109/ICCV48922.2021.00986

**Conference:** ICCV 2021 (IEEE) — Marr Prize (best paper)

**Year:** 2021

**Publication type:** Architecture reference (Swin Transformer)

**Research domain classification:** Vision Transformers, hierarchical backbones.

---

# 2. Study Type Classification

| Category | Mark | Justification |
| --- | --- | --- |
| Architecture reference (ViT) | ✔ | Hierarchical ViT with shifted-window attention. |
| Empirical study | ◐ | ImageNet/COCO/ADE20K. |
| Retinal/DR | ❌ | General; Swin used by cited DR/ViT works (e.g., Goh #16, Xu #09). |

**Justification:** Canonical hierarchical-ViT reference for the CNN-vs-ViT discussion (§1.3.1).

---

# 3. Research Problem

Make transformers a general vision backbone via hierarchical feature maps and linear-complexity shifted-window self-attention. Addresses **architecture design (ViT)**.

---

# 4. Datasets Used

ImageNet-1K/22K (classification), COCO (detection), ADE20K (segmentation).

---

# 5. Preprocessing Pipeline

Standard ViT patchify + windowed attention.

---

# 6. Model Architecture

| Item | Description |
| --- | --- |
| Mechanism | Shifted-window multi-head self-attention; hierarchical stages |
| Complexity | Linear in image size |

---

# 7. Validation Design

Classification/detection/segmentation benchmarks.

---

# 8. Performance Metrics

ImageNet-1K top-1 **87.3%** (Swin-L, 22K-pretrained); COCO **58.7** box AP; ADE20K **53.5** mIoU — SOTA at publication. (Headline.)

---

# 9. Authors' Claims

Swin is a general-purpose vision backbone surpassing prior ViTs/CNNs across classification, detection, segmentation.

---

# 10. Empirical Support Assessment

Multi-task SOTA evidence strong. Robust architecture reference.

---

# 11. Internal Validity

Controlled; large-scale pretraining dependency.

---

# 12. External Validity

Widely transferred, including medical imaging and DR hybrids.

---

# 13. Strengths

Hierarchical, efficient, multi-task SOTA.

---

# 14. Limitations

**Implicit:** Data/compute-hungry; non-medical evaluation here.

---

# 15. Relevance to My Dissertation

| Axis | Relevance | Notes |
| --- | --- | --- |
| **CNN vs ViT (§1.3.1)** | **Supporting (foundational)** | Backbone behind cited ViT/hybrid DR studies (Goh #16, Xu #09); contextualizes the CNN-vs-transformer discussion. |
| Preprocessing-dominance | Peripheral | N/A. |

**Risk of contradiction:** Low — the dissertation uses CNN backbones; Swin frames the transformer alternative without competing on the preprocessing claim.

---

# 16. Citation-Ready Statements

1. "Swin Transformer … computed with shifted windows … brings greater efficiency by limiting self-attention computation to non-overlapping local windows while also allowing for cross-window connection." (Abstract)
2. It achieves 87.3% top-1 on ImageNet-1K and SOTA on COCO and ADE20K. (Abstract)

---

# 17. Epistemic Classification

**Foundational / architecture reference (ViT).**

---

# 18. Analytical Synthesis

Swin Transformer is the hierarchical-ViT backbone underlying several cited DR/ViT studies (Goh #16, Xu #09) and is the key reference for the dissertation's CNN-versus-transformer discussion in §1.3.1. It demonstrates that windowed-attention transformers can serve as general vision backbones with strong multi-task performance, framing the architectural alternative to the dissertation's chosen CNN backbones. It is non-medical, preprocessing-agnostic, and neutral to preprocessing-dominance; cite to situate the transformer trend without implying a head-to-head DR comparison.

End of Literature Card.
