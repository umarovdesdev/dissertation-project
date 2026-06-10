# Appendix A — Source Code of the Preprocessing Pipeline

> Draft generated per `prompts/writing-session-system-prompt.md` v6.0.0 · Brief: `briefs/A-brief.md` · Binding reference: INVARIANTS.md v6.0.0 · Source: real on-disk tree `experiments/src/preprocessing/` (+ `experiments/src/`), catalogued in `experiments/CLAUDE.md`; lineage #19/#21/#23/#24 🔹SELF. **Code-catalogue appendix — cites no experimental result; every path and excerpt is reproduced from disk, none invented.**

---

## PART 1: SECTION TEXT

Section 4.1.3 committed the preprocessing pipeline and training code to version control and promised their reproduction here, so that the transformation applied to every image is recoverable as source rather than described only in prose. This appendix discharges that promise. Its inclusion is not incidental documentation: under the central thesis of this work — that the model is the composition of preprocessing and the convolutional network, with the eight-stage pipeline an integral model component rather than ancillary data preparation — the preprocessing source *is* part of the model specification. Reproducing it is what makes that thesis auditable rather than merely asserted.

The code is organized as a Python package under `experiments/src/`. The preprocessing stack lives in the canonical package `experiments/src/preprocessing/`, whose public interface is exported from `experiments/src/preprocessing/__init__.py` and whose orchestrator, `PreprocessingPipeline` in `experiments/src/preprocessing/pipeline.py`, chains the eight stages in the fixed order specified in Chapter 3. The remaining apparatus required to reproduce the experiments is distributed across sibling subpackages of `experiments/src/`: `data/` (dataset loaders, the patient-level stratified k-fold splitter, unified augmentation, and label harmonization), `models/` (the ResNet-50 and EfficientNet factories and the two-stage fine-tuning utility), `training/` (the training loop, focal loss with inverse-frequency weights, and checkpoint management), `evaluation/` (metrics, calibration, and statistical tests), `explainability/` (Grad-CAM, IoU/ALO, and overlay rendering), `experiments/` (the seven experiment drivers), and `utils/` (YAML configuration handling, the reproducibility seed utility, and image-quality metrics). The catalogue below is confined to the preprocessing package, which implements the model component that distinguishes this work; the wider tree is named here only so that the reproduction is locatable in full.

Table A.1 maps each pipeline stage of Chapter 3 to the module that implements it. Every path is given relative to the repository root and corresponds to a file present in the versioned source tree.

**Table A.1. Pipeline stage → implementing module (`experiments/src/preprocessing/`).**

| Stage | Description (Ch 3) | Implementing module |
|-------|--------------------|---------------------|
| 0 | Canonical flip (left→right eye orientation) | `canonical_flip.py`, `canonical_orientation.py` |
| 1 | OD–fovea rotation normalization | `od_fovea_detect.py`, `canonical_orientation.py` |
| 2 | FOV crop + isotropic resize to 512×512 (centered zero-padding) | `crop_resize.py` |
| 3 | FOV mask generation (binary → 4th channel) | `crop_resize.py` (mask returned with the resized image) |
| 4 | Flat-field correction (adaptive σ = 0.07·D, inside mask) | `flat_field.py` |
| 5 | Dual-constraint CLAHE (LAB L-channel; stochastic at train) | `upgraded_clahe.py`, `polar_clahe.py`, `clahe.py` |
| 6 | Augmentation (unified affine + brightness/contrast + PCA colour; train only) | `experiments/src/data/augmentation_unified.py` |
| 7 | Dataset-specific normalize → tensor (always last) | `imagenet_normalize.py` |
| — | Configuration surface (baseline vs full-pipeline presets) | `config.py` (`PreprocessingConfig`, `PIPELINE_PRESETS`) |
| — | Stage orchestration (fixed execution order) | `pipeline.py` (`PreprocessingPipeline`) |

Stage 5 is implemented by more than one module because the pipeline ships with a polar variant of the dual-constraint CLAHE as its current default (`polar_clahe.py`), alongside the rectilinear tile-based formulation (`upgraded_clahe.py`); both are present in the versioned source and are reproduced as catalogued. Stages 0–5 and 7 are applied identically at training and inference, except that the Stage 5 contrast enhancement is stochastic at training time; Stage 6 augmentation is applied only during training and is inserted before the Stage 7 normalization so that it operates on `uint8` images. The baseline configuration (Configs A and C) bypasses Stages 0–6 in favour of a simple stretch-resize to 512×512 followed by ImageNet normalization on three channels, selected through the configuration preset rather than by editing the pipeline; the full pipeline (Configs B and D) runs all eight stages and emits four channels (RGB plus the FOV mask).

To establish that this catalogue reproduces real source rather than a paraphrase of it, the Stage 4 flat-field module is reproduced verbatim from `experiments/src/preprocessing/flat_field.py`:

```python
"""
Stage 4: Flat-Field Correction.

Reduces uneven illumination by subtracting a heavily blurred version of the
image and re-centering at 128:

    corrected = image − GaussianBlur(image, σ) + 128

A large σ captures only the low-frequency illumination gradient, so the
subtraction removes broad brightness variation while preserving local vessel
and lesion detail.

σ is computed adaptively as σ = 0.07 × FOV_diameter.  Correction
is applied only inside the FOV mask (padding pixels are left at zero).

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import cv2
import numpy as np


def apply_flat_field(
    image: np.ndarray,
    sigma: float = 45.0,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    Apply flat-field correction to reduce uneven illumination.

    Algorithm::

        blur      = GaussianBlur(image, σ)
        corrected = image − blur + 128

    When *mask* is provided, correction is applied only inside the mask
    (``mask > 0``). Padding areas (``mask == 0``) are left at zero.

    Kernel size is derived automatically from *sigma* (passed as ``(0, 0)``
    to :func:`cv2.GaussianBlur`).

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        sigma: Gaussian blur σ controlling the spatial scale of the
            illumination estimate.
        mask: Optional binary mask of shape ``(H, W)`` (float32 or uint8).
            When provided, only pixels where ``mask > 0`` are corrected;
            padding regions remain zero.

    Returns:
        Corrected RGB uint8 NumPy array of shape ``(H, W, 3)``.
    """
    blur = cv2.GaussianBlur(image, (0, 0), sigma)
    corrected = image.astype(np.float32) - blur.astype(np.float32) + 128.0
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)
    if mask is not None:
        mask_3ch = np.expand_dims(mask > 0, axis=-1).astype(np.uint8)
        corrected = corrected * mask_3ch  # zero out padding
    return corrected
```

The remaining modules follow the same conventions established for the codebase — type-hinted signatures, `Args`/`Returns` docstrings, paths resolved from configuration rather than hardcoded, and `pathlib.Path` throughout — and are reproduced in full in the assembled document from the same package. The pipeline lineage descends from the candidate's prior published work on upgraded CLAHE and preprocessing–classification integration (`yesmukhamedov-scopus-q2.md`/`yesmukhamedov-scopus-q3.md`, `yesmukhamedov-kbtu.md`, and the conference paper, 🔹prior own work; SIR-4); the source reproduced here formalizes and consolidates that line into the single versioned eight-stage system specified in Chapter 3. Consistent with the hardware-specific reproducibility bound stated in §4.1.3, the source is reproducible on equivalent hardware, but the computational-efficiency characteristics it exhibits remain specific to the documented setup (DGL-2); no claim of performance, accuracy, or deployment readiness is made by reproducing it. With the source catalogued and a representative module shown to be the real, on-disk implementation, the reproducibility loop opened in §4.1.3 is closed: the fixed configuration (Table 4.2), the documented hardware, and this versioned code together render the experimental pipeline recoverable.

---

## PART 3: COMPLIANCE CHECKLIST

**APP-A ✅ AVAILABLE (real on-disk source referenced by path)** — ✅ Satisfied. Stage→module map (Table A.1) and the verbatim `flat_field.py` excerpt both correspond to files verified present in `experiments/src/preprocessing/`; the wider `src/` tree is catalogued from `experiments/CLAUDE.md`.

**No-invention rule (every path/file real; excerpts verbatim)** — ✅ Satisfied. Every module named (`canonical_flip.py`, `canonical_orientation.py`, `od_fovea_detect.py`, `crop_resize.py`, `flat_field.py`, `upgraded_clahe.py`, `polar_clahe.py`, `clahe.py`, `imagenet_normalize.py`, `config.py`, `pipeline.py`, and `data/augmentation_unified.py`) exists on disk; the reproduced block is byte-for-byte from `flat_field.py`. No code was fabricated.

**CENTRAL_THESIS (preprocessing = integral model component)** — ✅ Satisfied. *"the preprocessing source is part of the model specification. Reproducing it is what makes that thesis auditable rather than merely asserted."* (opening ¶).

**Reproducibility loop closed (back-reference to §4.1.3)** — ✅ Satisfied. *"the fixed configuration (Table 4.2), the documented hardware, and this versioned code together render the experimental pipeline recoverable."* (final ¶).

**SIR-4 (#19/#21/#23/#24 prior own work, lineage identified, not re-claimed)** — ✅ Satisfied. *"The pipeline lineage descends from the candidate's prior published work … (🔹prior own work; SIR-4); the source reproduced here formalizes and consolidates that line."* (final ¶).

**SIR-1 (no amplification — code listed as it is)** — ✅ Satisfied. The appendix asserts only file existence, stage mapping, and the verbatim excerpt; no capability beyond what the code implements is described.

**DGL-2 (efficiency hardware-bound) carried** — ✅ Satisfied. *"the computational-efficiency characteristics it exhibits remain specific to the documented setup (DGL-2)."* (final ¶).

**CFC-2.2 (no superiority)** — ✅ Satisfied (absent). No comparison or ranking; code catalogue only.

**CFC-2.4 (no clinical-grade / real-time / deployment claim)** — ✅ Satisfied (absent). *"no claim of performance, accuracy, or deployment readiness is made by reproducing it."* (final ¶).

**CFC-2.5 (no perfect/performance figure)** — ✅ Satisfied (absent). No metric cited anywhere.

**No experimental result cited (supporting-artifact register)** — ✅ Satisfied. Only file paths, stage mappings, and reproduced source appear; no Exp 1–7 outcome.

**Paradigm positioning (CFC-2.9 / SIR-9)** — ⚪ Not applicable. No Gulshan/P1 source cited.

---

### Word count

PART 1 framing prose: ~840 words (within the 700–1,000 target). The reproduced code block is not counted toward prose word count.

### Deferred-asset log

None. APP-A ✅ AVAILABLE; all referenced source verified on disk. In Phase 3 (§11.2) the remaining modules are reproduced in full from the same package into the assembled document.
