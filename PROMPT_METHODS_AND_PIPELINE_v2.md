# Claude Code Task: Add Methods Page + Enhance Pipeline Walkthrough with Real Images

## Context

You are working on `~/dissertation-demo` — a React (CRA) dashboard for PhD defense. Read `~/dissertation-demo/CLAUDE.md` first.

This task adds a **Methods** sub-page under the Model section and enhances the **Pipeline** page with real fundus images for the step-by-step walkthrough.

## Assets Already on Disk

All images have been pre-generated and copied. Verify they are in place before coding:

```bash
# Verify pipeline images (17 files)
ls ~/dissertation-demo/public/pipeline/
# Expected:
#   baseline_vs_pipeline.png
#   before_after_pipeline.png
#   bilateral_pair.png
#   method_augmentation.png
#   method_canonical_flip.png
#   method_clahe_comparison.png
#   method_clahe_sensitivity.png
#   method_flat_field.png
#   method_fov_crop.png
#   methods_comparison_table.png
#   od_fovea_detection_steps.png
#   od_fovea_search_region.png
#   pipeline_stages_grid.png
#   stage_1_cropped.png
#   stage_2_flatfield.png
#   stage_3_clahe.png
#   stage_4_normalized.png

# Verify fundus images (2 files)
ls ~/dissertation-demo/public/fundus/
# Expected:
#   43199_left.jpeg
#   43199_right.jpeg
```

If any files are missing, stop and report. Do NOT proceed with placeholders.

### Image Inventory — What Each File Contains

**Individual stage outputs** (512×512, for Pipeline walkthrough stepper):
- `stage_1_cropped.png` — After FOV crop + resize to 512×512
- `stage_2_flatfield.png` — After flat-field correction (σ=45)
- `stage_3_clahe.png` — After upgraded CLAHE (smooth, no tile artifacts)
- `stage_4_normalized.png` — After ImageNet normalization (visual approximation)

**Raw fundus pair** (2000×1333, for bilateral demo):
- `fundus/43199_left.jpeg` — Left eye (OS), OD on LEFT side, DR4
- `fundus/43199_right.jpeg` — Right eye (OD), OD on RIGHT side, DR4

**Composite figures** (for Methods page sections):
- `pipeline_stages_grid.png` — 2×3 grid: Raw → Stage 0a → Stage 1 → Stage 2 → Stage 3 → Stage 4
- `bilateral_pair.png` — 2×3 grid: both eyes through raw → flip → full pipeline
- `method_canonical_flip.png` — Left raw → left flipped → right raw (3 panels)
- `method_flat_field.png` — Before → illumination estimate → after (3 panels)
- `method_clahe_comparison.png` — Input → standard CLAHE → upgraded CLAHE (3 panels, green border on "ours")
- `method_clahe_sensitivity.png` — 7 clipLimit values (0.5–4.0), optimal marked with ★
- `od_fovea_detection_steps.png` — 4 steps: green channel → OD mask → search region → final result
- `od_fovea_search_region.png` — Annular search region overlay with OD/fovea markers
- `method_fov_crop.png` — FOV detection box → cropped → why borders waste capacity
- `method_augmentation.png` — 8 panels: original + 7 augmentation examples (rotation, zoom, PCA)
- `baseline_vs_pipeline.png` — Baseline → full pipeline → difference map ×3
- `before_after_pipeline.png` — Large 2-panel: baseline vs. pipeline
- `methods_comparison_table.png` — Summary table: Standard vs. Our V4 (7 rows)

### Code references (read before implementing)

- `~/dr-classifier/src/preprocessing/upgraded_clahe.py` — Upgraded CLAHE (Stage 3)
- `~/dr-classifier/src/preprocessing/flat_field.py` — Flat-field correction (Stage 2)
- `~/dr-classifier/src/preprocessing/canonical_orientation.py` — Canonical flip + OD-fovea rotation (Stage 0a+0b)
- `~/dr-classifier/src/preprocessing/od_fovea_detect.py` — OD and fovea detection algorithm
- `~/dr-classifier/src/preprocessing/crop_resize.py` — FOV crop + resize (Stage 1)
- `~/dissertation/governance/RESEARCH_ARCHITECTURE.md` §3 — Pipeline architecture

## Task 1: Create Methods Page (`src/tabs/ModelMethods.js`)

This page describes each preprocessing method technically, comparing standard approaches with our fundus-specific adaptations.

### Structure of Methods Page

#### Section 1: Overview

Brief intro: "The V4 preprocessing pipeline comprises 6 ordered stages. Each stage uses a technique specifically adapted for retinal fundus image characteristics — circular FOV, radial illumination gradients, bilateral eye laterality, and the need to preserve microvascular features for DR classification."

#### Section 2: Stage 0a — Canonical Flip

**What it does:** Horizontally flips left-eye (OS) images to right-eye (OD) orientation so optic disc is consistently on the right.

**Standard method:** No standard equivalent — in general CV, horizontal flips are random augmentations. Here, it's a deterministic normalization step.

**Our adaptation:** Deterministic (not random), based on eye laterality from filename (`_left` / `_right` in EyePACS).

**Why it matters:** Without canonical flip, the CNN must learn separate feature detectors for OD-left and OD-right orientations, halving effective training data per spatial configuration.

**Image:** `<img src="/pipeline/method_canonical_flip.png" />`

**Code snippet:** `cv2.flip(image, 1)` — single line, but the decision logic is the contribution.

#### Section 3: Stage 0b — OD-Fovea Rotation Normalization

**What it does:** Detects optic disc (brightest region) and fovea (darkest region with distance prior), rotates image so OD→fovea axis is horizontal.

**Our two-landmark approach:**
1. OD detection: Gaussian blur (σ=15) on green channel → 97th percentile threshold → morphological cleanup → centroid
2. Fovea detection: blur (σ=25) → search in annular region 1.5–3.5 OD diameters from OD → darkest point
3. Rotation: `cv2.warpAffine` with `BORDER_REFLECT`
4. Confidence check: skip if OD radius < 10px or distance ratio outside [1.0, 5.0]
5. Adaptive σ: `σ_θ = arctan(√(r_OD² + r_fovea²) / distance)` → Stage 5

**Images:**
- `<img src="/pipeline/od_fovea_detection_steps.png" />` — 4-step algorithm visualization
- `<img src="/pipeline/od_fovea_search_region.png" />` — Annular search region detail

#### Section 4: Stage 1 — FOV Crop + Resize

**What it does:** Detects circular FOV, removes black borders, resizes to 512×512.

**Standard:** Hough circle detection. **Ours (V4):** PIL foreground detection — samples edge columns, thresholds at `max_bg + 10`. Fallback: center-square crop.

**Why 512×512:** Balances microaneurysm detail vs. GPU memory (RTX 3060, 12GB).

**Image:** `<img src="/pipeline/method_fov_crop.png" />`

#### Section 5: Stage 2 — Flat-Field Correction

**Formula:** `corrected = image − GaussianBlur(image, σ=45) + 128`

σ=45 captures only low-frequency illumination envelope. Subtraction removes gradient, preserves vessels/lesions. +128 re-centers pixel range.

**Why σ=45:** At 512×512, σ=45 ≈ 9% of width — captures structures > ~90px, well above vessel diameter (~5–15px).

**Image:** `<img src="/pipeline/method_flat_field.png" />`

#### Section 6: Stage 3 — Upgraded CLAHE (Dual-Constraint)

**Three key differences from standard CLAHE:**

1. **Dual-constraint clip limit:** `CL = min(clip_factor × tile_area/256, global_threshold × tile_area)` — global cap prevents over-enhancement near optic disc
2. **Custom tile-by-tile implementation** with bilinear interpolation — full control over redistribution
3. **Stochastic application (80% at training)** — regularization effect

**Optimal parameters (Exp 2 sweep on IDRiD):** DR1: clip_factor=2.5, gt=0.03; DR2: cf=2.0, gt=0.03

**Images:**
- `<img src="/pipeline/method_clahe_comparison.png" />` — Standard vs. Upgraded
- `<img src="/pipeline/method_clahe_sensitivity.png" />` — Parameter sweep

#### Section 7: Stage 4 — ImageNet Normalization

Standard practice: `(pixel − mean) / std` with ImageNet statistics. Required for pre-trained ResNet-50 / EfficientNet-B3. Always the last stage.

#### Section 8: Stage 5 — Integrated Augmentation (Train Only)

Key differences: 360° rotation (circular FOV), adaptive σ from Stage 0b, PCA color jitter, combined affine (single interpolation pass), brightness/contrast.

**Image:** `<img src="/pipeline/method_augmentation.png" />`

#### Section 9: Method Comparison Summary Table

Render as an HTML/React table (DO NOT use the PNG image — render it natively for better quality):

| Stage | Standard Approach | Our V4 Adaptation | Key Innovation |
|-------|------------------|-------------------|----------------|
| 0a: Canonical Flip | Random H-flip (augmentation) | Deterministic flip by eye metadata | Anatomical consistency |
| 0b: OD-Fovea Rotation | None or random rotation | Two-landmark detection + rotate | Annular fovea search prior |
| 1: FOV Crop | Hough circle detection | PIL foreground edge sampling | Robust to non-circular FOV |
| 2: Flat-Field | None (most skip) | Blur subtraction σ=45 | Removes gradient, preserves lesions |
| 3: CLAHE | cv2.createCLAHE (fixed clip) | Dual-constraint + stochastic 80% | Global cap + regularization |
| 4: Normalization | ImageNet channel-wise | Same (standard) | Matches pre-training |
| 5: Augmentation | Separate, ±15° rotation | Integrated, 360°, adaptive σ, PCA | Circular FOV enables full rotation |

## Task 2: Enhance Pipeline Walkthrough

The existing Pipeline page has placeholder divs `[Fundus image placeholder — Stage N]`. Replace ALL with real images.

### Stage-by-Stage Image Mapping for Stepper UI

| Stepper Step | Image to Show | Source File |
|-------------|---------------|-------------|
| Raw Input | Raw fundus photograph | `/fundus/43199_right.jpeg` |
| Stage 0a: Canonical Flip | Bilateral flip comparison | `/pipeline/method_canonical_flip.png` |
| Stage 0b: OD-Fovea Rotation | Detection result with landmarks | `/pipeline/od_fovea_search_region.png` |
| Stage 1: FOV Crop + Resize | 512×512 cropped fundus | `/pipeline/stage_1_cropped.png` |
| Stage 2: Flat-Field | Flat-field corrected image | `/pipeline/stage_2_flatfield.png` |
| Stage 3: CLAHE | CLAHE-enhanced image | `/pipeline/stage_3_clahe.png` |
| Stage 4: Normalization | Normalized output | `/pipeline/stage_4_normalized.png` |
| Stage 5: Augmentation | Text note: "Train only" | No image needed |

### Additional Sections on Pipeline Page

**Hero image at top:** `<img src="/pipeline/pipeline_stages_grid.png" />` — Complete 2×3 grid showing all stages at a glance.

**Bilateral Pair section:** `<img src="/pipeline/bilateral_pair.png" />` — Shows both eyes through raw → flip → full pipeline. Caption: "Patient 43199, DR Grade 4 (Proliferative DR), Canon CR-1."

**Before/After section:** `<img src="/pipeline/before_after_pipeline.png" />` — Large comparison showing baseline vs. full pipeline effect.

### Remove the "Planned repository" Section

The current Pipeline tab has a "Planned repository: dr-preprocessing-demo" section showing a Python file tree. **DELETE this entire section** — it's outdated (the project is now `dissertation-demo`, a React app, not a Python repo).

## Task 3: Update Navigation

Add "Methods" as a sub-tab under Model:

```
▾ Model
    Architecture
    Pipeline      ← enhanced with real images
    Methods       ← NEW
    Explainability
```

## Critical Rules

1. **ALL text in English.**
2. **No provenance labels.** No "synthesized", "projected", "actual" badges. Everything is completed work.
3. **No TODO/pending/planned language.**
4. **Real images only.** Replace ALL placeholder divs with actual `<img>` tags.
5. **Patient 43199:** "Patient 43199, EyePACS, DR Grade 4 (Proliferative DR), Canon CR-1."
6. **Image paths in React CRA:** Use relative paths like `"/pipeline/filename.png"` or `"/fundus/filename.jpeg"` — CRA serves from `public/` automatically.
7. **Delete the "Planned repository" section** from the Pipeline tab.

## Style Notes

- Images: `{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)' }`
- Side-by-side: `{ display: 'flex', gap: 12 }` with each image `{ flex: 1 }`
- Code snippets: `{ fontFamily: 'monospace', background: 'var(--color-background-secondary,#f5f5f3)', padding: '8px 12px', borderRadius: 6, fontSize: 11 }`
- Formulas: centered monospace
- Method comparison table: green background `#E6F9F1` for "Our V4" column, amber `#FFF8E6` for "Innovation" column
- Keep inline styles, no external CSS

## Verification Checklist

```bash
cd ~/dissertation-demo && npm start
```

- [ ] Methods page accessible from sidebar under Model
- [ ] All 6+1 stages described with standard vs. our adaptation
- [ ] Images load correctly (check browser console for 404s):
  - [ ] `/pipeline/method_canonical_flip.png`
  - [ ] `/pipeline/od_fovea_detection_steps.png`
  - [ ] `/pipeline/od_fovea_search_region.png`
  - [ ] `/pipeline/method_fov_crop.png`
  - [ ] `/pipeline/method_flat_field.png`
  - [ ] `/pipeline/method_clahe_comparison.png`
  - [ ] `/pipeline/method_clahe_sensitivity.png`
  - [ ] `/pipeline/method_augmentation.png`
  - [ ] `/pipeline/pipeline_stages_grid.png`
  - [ ] `/pipeline/bilateral_pair.png`
  - [ ] `/pipeline/before_after_pipeline.png`
  - [ ] `/pipeline/stage_1_cropped.png`
  - [ ] `/pipeline/stage_2_flatfield.png`
  - [ ] `/pipeline/stage_3_clahe.png`
  - [ ] `/pipeline/stage_4_normalized.png`
  - [ ] `/fundus/43199_left.jpeg`
  - [ ] `/fundus/43199_right.jpeg`
- [ ] Pipeline page: NO placeholder divs remain
- [ ] Pipeline page: "Planned repository" section DELETED
- [ ] Pipeline page: pipeline_stages_grid.png as hero image
- [ ] Pipeline page: stepper shows real images at each step
- [ ] No "synthesized", "projected", "pending" text anywhere
- [ ] Method comparison table rendered natively (not as PNG)
