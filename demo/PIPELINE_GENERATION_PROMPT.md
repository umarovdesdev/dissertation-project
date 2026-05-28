# Pipeline Image Generation Prompt (Pipeline — Corrected)

**Project:** PhD Dissertation — "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
**Candidate:** Yesmukhamedov N.S. (IITU)
**Output directory:** `E:\dissertation-project\demo\public\pipeline\`
**Generator script:** `E:\dissertation-project\demo\generate_pipeline_images.py`

---

## Critical Corrections (vs. original GENERATION_PROMPT.md)

The original generation prompt produced images with systematic errors. **All regenerated images MUST apply these corrections:**

### Error 1: Stage 1 Rotation Causes Artifacts

**Problem:** `stage1_od_fovea_rotation()` rotates the image to align the OD-fovea axis horizontally. This rotation:
- Introduces black triangular border artifacts in the corners
- Confuses the FOV circle detector in Stage 2 (irregular contour → wrong center/radius)
- Causes Stage 2 to aggressively crop, cutting off the fundus edge
- Makes the FOV mask (Stage 3) an irregular polygon instead of a smooth circle

**Fix:** For all **visualization images**, skip Stage 1 entirely. Pipeline flow for visualization: `Raw → Stage 0 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 7`. Stage 1 is a valid pipeline stage (still described in text/tables), but its visual effect is minimal on well-acquired images and it breaks the visual chain.

### Error 2: FOV Crop Does Not Inscribe Circle in Square

**Problem:** `stage2_fov_crop_isotropic_resize()` used `margin = int(r * 0.05)`, producing a non-square crop with the fundus circle smaller than the 512×512 frame. The circle was also potentially off-center if clipped at image edges.

**Fix:** Use `margin_pct=0` for all visualization images. The updated function now:
1. Always crops a perfect square centered on the detected FOV (side = 2×radius)
2. Zero-pads if the square extends beyond image bounds
3. Resizes the square to 512×512

Result: the fundus circle is **inscribed in the square** — touching all 4 edges. No wasted black space.

### Error 3: V4 Stage Numbering in Titles

**Problem:** Several images still have V4 pipeline numbering in their titles:
- `method_flat_field.png` → says "Stage 2" and "σ=45" (V4 fixed sigma)
- `method_fov_crop.png` → says "Stage 1"
- `method_clahe_comparison.png` → says "Stage 3"
- `method_augmentation.png` → says "Stage 5"
- `od_fovea_detection_steps.png` → says "Stage 0b"
- `method_canonical_flip.png` → says "Stage 0a"
- `methods_comparison_table.png` → says "V4 Pipeline"

**Fix:** All titles must use pipeline stage numbering (0–7). All references to "V4" must be "Pipeline".

### Error 4: Flat-Field Shows Fixed σ=45

**Problem:** `method_flat_field.png` title says "σ=45" — this was the V4 fixed value.

**Fix:** Must show "σ = 0.07·D" (adaptive sigma). The flat-field formula is: `I' = I − GaussianBlur(I, σ=0.07·D) + μ_FOV`, where D is the FOV diameter.

### Error 5: Baseline vs pipeline Images Show Same Processing

**Problem:** In `before_after_pipeline.png` and `baseline_vs_pipeline.png`, the side still has cropping/rotation artifacts, reducing the visual contrast with baseline.

**Fix:**
- **Baseline** = `baseline_processing()` → stretch-resize to 512×512 (fills entire square, no circle, no enhancement). This distorts the circular FOV into an ellipse.
- **Pipeline** = Stage 0 → Stage 2 (margin_pct=0) → Stage 4 → Stage 5. Circle inscribed in square, uniform illumination, enhanced contrast.

The visual distinction should be immediately obvious: baseline fills the square (distorted ellipse) vs pipeline preserves the circle (inscribed, with black corners).

---

## Source Images

**Hard requirement:** ALL pipeline images must be produced by processing real fundus images from the directory `E:\dissertation-project\demo\public\fundus-examples\dr04\`. No synthetic, generated, or placeholder images are allowed. Every file in `public/pipeline/` must be the result of running a real fundus image through the corresponding pipeline stages.

Source files:
- `E:\dissertation-project\demo\public\fundus-examples\dr04\right_eye.jpeg` — right eye (OD), Patient 43199, EyePACS, DR Grade 4 (Proliferative DR)
- `E:\dissertation-project\demo\public\fundus-examples\dr04\left_eye.jpeg` — left eye (OS), same patient

The right eye has the optic disc (bright circular region) on the LEFT side. The left eye has the optic disc on the RIGHT side.

**Loading:**
```python
SRC_DIR = r'E:\dissertation-project\demo\public\fundus-examples\dr04'
right_img = cv2.cvtColor(cv2.imread(os.path.join(SRC_DIR, 'right_eye.jpeg')), cv2.COLOR_BGR2RGB)
left_img  = cv2.cvtColor(cv2.imread(os.path.join(SRC_DIR, 'left_eye.jpeg')),  cv2.COLOR_BGR2RGB)
```

If the files are not found, the script must terminate with `FileNotFoundError` rather than substituting placeholders.

---

## Pipeline Processing Recipe (for visualization)

```python
from generate_pipeline_images import (
    load_image, stage0_canonical_flip,
    stage2_fov_crop_isotropic_resize, stage3_fov_mask,
    stage4_flatfield, stage5_clahe, stage7_normalize,
    baseline_processing
)

right_img = load_image('right_eye.jpeg')
left_img  = load_image('left_eye.jpeg')

# pipeline (NO Stage 1 rotation)
s0   = stage0_canonical_flip(right_img, is_left_eye=False)
s2   = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)  # inscribed circle
mask = stage3_fov_mask(s2)
s4   = stage4_flatfield(s2)
s5   = stage5_clahe(s4)
s7_disp, _ = stage7_normalize(s5, mask)

# Left eye (for bilateral pair)
l_s0 = stage0_canonical_flip(left_img, is_left_eye=True)   # flipped
l_s2 = stage2_fov_crop_isotropic_resize(l_s0, margin_pct=0)
# ... etc.

# Baseline (for comparison images)
baseline = baseline_processing(right_img)  # stretch-resize 512×512
```

**Key rules:**
- NEVER call `stage1_od_fovea_rotation()` in visualization code
- ALWAYS pass `margin_pct=0` to `stage2_fov_crop_isotropic_resize()`
- Baseline uses `baseline_processing()` (stretch-resize), NOT pipeline stages

---

## Image Specifications (17 files)

### Group 1: Per-Stage Stepper Images (referenced by ModelPipeline.js STAGE_IMAGES)

#### 1. `method_canonical_flip.png`
- **Status:** EXISTS — needs title fix
- **Content:** 3-panel: Left eye raw (OD on left) → Left eye flipped (OD on right) → Right eye raw (OD already on right)
- **Title:** "Stage 0: Canonical Flip — cv2.flip(image, 1) for left eyes"
- **Annotations:** Panel subtitles: "Left Eye (OS) — Raw / OD on LEFT side", "Left Eye — After Flip / OD on RIGHT side ✓", "Right Eye (OD) — Raw / OD already RIGHT ✓"
- **Fix needed:** Title says "Stage 0a" → change to "Stage 0"

#### 2. `od_fovea_search_region.png`
- **Status:** EXISTS — needs title fix
- **Content:** Single image showing the OD detection, fovea search annular zone, and detected OD-fovea axis
- **Title:** "Stage 1: OD-Fovea Detection — Annular Search Region"
- **Fix needed:** Title says "Stage 0b" → change to "Stage 1". This image illustrates the Stage 1 algorithm but does NOT need to show a rotated output.

#### 3. `od_fovea_detection_steps.png`
- **Status:** EXISTS — needs title fix
- **Content:** 4-panel: Green channel → OD mask (97th percentile) → Fovea search (annular zone) → Result with OD-fovea axis line
- **Title:** "Stage 1: OD-Fovea Detection — Classical CV Approach"
- **Fix needed:** Title says "Stage 0b" → change to "Stage 1"

#### 4. `stage_2_isotropic_resize.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2-panel: (a) Pre-crop image with FOV boundary circle drawn (green dashed), (b) After isotropic resize to 512×512 with fundus circle inscribed in square
- **Title:** "Stage 2: FOV Crop + Isotropic Resize (512×512)"
- **Fix needed:** Current version shows cropped fundus from rotated image. Regenerate: skip Stage 1, use `margin_pct=0`. The right panel must show the fundus circle touching all 4 edges of the square.

#### 5. `stage_4_flatfield.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2-panel: Before flat-field (after Stage 2) → After flat-field
- **Title:** "Stage 4: Adaptive Flat-Field Correction (σ = 0.07·D)"
- **Fix needed:** Regenerate from corrected Stage 2 output (no rotation, inscribed circle). Current version has fundus not touching edges.

#### 6. `stage_5_clahe.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2-panel: Before CLAHE (after flat-field) → After CLAHE
- **Title:** "Stage 5: CLAHE (Dual-Constraint, LAB L-channel)"
- **Subtitle:** "clip_factor=2.0, threshold=0.01"
- **Fix needed:** Regenerate from corrected chain. Current version has fundus not touching edges.

#### 7. `stage_7_normalized.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2-panel: Normalized RGB (rescaled for display) | FOV Mask (Channel 4)
- **Title:** "Stage 7: Dataset-Specific Normalize → 4-Channel Tensor"
- **Fix needed:** Regenerate from corrected chain. Current FOV mask is an irregular polygon (rotation artifact) — should be a smooth circle inscribed in the square.

### Group 2: Composite/Overview Images (referenced by ModelPipeline.js)

#### 8. `pipeline_stages_grid.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 3×3 grid showing right_eye.jpeg through all pipeline stages
- **Panels:** Raw Input, Stage 0: Canonical Flip, Stage 1: OD-Fovea Rotation, Stage 2: FOV Crop + Resize, Stage 3: FOV Mask, Stage 4: Flat-Field, Stage 5: CLAHE, Stage 6: Augmentation (train only), Stage 7: Normalize → 4ch
- **Title:** "Pipeline Stages — Patient 43199 (DR4, Proliferative DR)"
- **Stage badges:** Colored badges in bottom-left of each panel (Raw=gray, S0–S3=blue, S4–S5=teal, S6=amber, S7=purple)
- **Fix needed:** Regenerate with corrected processing chain. Stage 1 panel can show a mild rotation or the same image with a detected axis line overlay (since the rotation effect is minimal on this well-acquired image). Stage 2 onward: fundus must be inscribed in square. Stage 3 mask must be a smooth circle.
- **Special handling for Stage 1 panel:** Show the image WITH the OD-fovea axis drawn (green line from OD to fovea) to illustrate what Stage 1 detects, rather than showing a rotated image with artifacts.

#### 9. `bilateral_pair.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2×3 grid. Top row: Right eye (OD) raw → Cropped 512×512 → Full Pipeline. Bottom row: Left eye (OS) raw → Flipped + Cropped → Full Pipeline.
- **Title:** "Bilateral Pair — Canonical Flip + Full Pipeline / Patient 43199 (DR4)"
- **Row labels:** "OD" (left margin, top row), "OS" (left margin, bottom row)
- **Key visual:** After canonical flip + crop, both eyes should look like right eyes (OD on same side). Fundus circles inscribed in squares.
- **Fix needed:** Remove Stage 1 rotation, use `margin_pct=0`.

#### 10. `before_after_pipeline.png`
- **Status:** EXISTS — needs regeneration
- **Content:** Side-by-side: Baseline (3ch) vs Full Pipeline (4ch)
- **Left panel:** Baseline — stretch-resize to 512×512 (fills entire square, distorted elliptical FOV). Badge: "3ch RGB" (gray).
- **Right panel:** Pipeline — isotropic resize with flat-field + CLAHE (circular FOV inscribed in square, black corners). Badge: "4ch RGBM" (teal).
- **Title:** "Baseline Processing vs Full Pipeline"
- **Caption:** "isotropic resize preserves circular FOV geometry; flat-field corrects illumination; CLAHE enhances vessel contrast"
- **Fix needed:** Regenerate with corrected pipeline processing. The visual contrast between baseline (distorted, filling square) and pipeline (circle inscribed, enhanced) must be immediately obvious.

#### 11. `baseline_vs_pipeline.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2×2 grid comparison
- **Top-left:** Baseline stretch-resize (distorts geometry)
- **Top-right:** isotropic resize (preserves circular FOV)
- **Bottom-left:** Baseline (no enhancement, original illumination)
- **Bottom-right:** Pipeline flat-field + CLAHE (uniform illumination, enhanced contrast)
- **Title:** "Baseline Stretch-Resize vs pipeline Isotropic Resize"
- **Fix needed:** Same corrections as above.

### Group 3: Method Detail Images (referenced by ModelMethods.js)

#### 12. `method_fov_crop.png`
- **Status:** EXISTS — needs title fix + regeneration
- **Content:** 3-panel: FOV detection (green boundary) → After crop + resize → Example of black borders wasting CNN capacity
- **Title:** "Stage 2: FOV Crop + Resize — Removing Device-Specific Borders"
- **Fix needed:** Title says "Stage 1" → change to "Stage 2". Regenerate with inscribed circle.

#### 13. `method_flat_field.png`
- **Status:** EXISTS — needs title fix + regeneration
- **Content:** 3-panel: Before flat-field (illumination gradient visible) → Illumination estimate (GaussianBlur) → After flat-field (uniform illumination)
- **Title:** "Stage 4: Flat-Field Correction — corrected = image − blur(σ=0.07·D) + μ_FOV"
- **Fix needed:** Title says "Stage 2" and "σ=45" → change to "Stage 4" and "σ=0.07·D". Regenerate with corrected processing. The middle panel (illumination estimate) should show the Gaussian-blurred image that gets subtracted.

#### 14. `method_clahe_comparison.png`
- **Status:** EXISTS — needs title fix + regeneration
- **Content:** 3-panel: Input (after flat-field) → Standard CLAHE (cv2.createCLAHE clip=2.0) → Upgraded CLAHE (dual-constraint)
- **Title:** "Stage 5: Standard CLAHE vs. Upgraded CLAHE (Dual-Constraint)"
- **Fix needed:** Title says "Stage 3" → change to "Stage 5". Regenerate with corrected input (inscribed circle).

#### 15. `method_clahe_sensitivity.png`
- **Status:** EXISTS — needs regeneration
- **Content:** 2×4 grid showing CLAHE output at different clipLimit values (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0). Highlight optimal range (2.0–3.0). Note that clip≥4 over-enhances.
- **Title:** "H-2: CLAHE Parameter Sensitivity — clipLimit Sweep"
- **Fix needed:** Regenerate with corrected input images (inscribed circle, no rotation artifacts).

#### 16. `method_augmentation.png`
- **Status:** EXISTS — needs title fix + regeneration
- **Content:** 2×4 grid showing augmentation examples: Original, Rotation +25°, Rotation −15°, Rotation +180°, Zoom 1.1×, Brightness +10%, PCA Color Jitter, Combined
- **Title:** "Stage 6: Augmentation Examples (Train Only) — 360° rotation valid for circular FOV"
- **Fix needed:** Title says "Stage 5" → change to "Stage 6". Regenerate with corrected input (inscribed circle).

#### 17. `methods_comparison_table.png`
- **Status:** EXISTS — needs regeneration
- **Content:** Comparison table: Standard approach vs pipeline fundus-specific adaptations for each pipeline stage
- **Title:** "Pipeline — Standard vs. Fundus-Specific Adaptations"
- **Fix needed:** Title says "V4 Pipeline" → change to "Pipeline". Update table content:
  - Stage numbering: 0–7 (not 0a, 0b, 1, 2, 3, 4, 5)
  - Flat-field row: "σ=0.07·D (adaptive)" not "σ=45"
  - Add Stage 3 (FOV Mask) if missing
  - Columns: Stage | Standard | Our | Innovation

---

## Visual Style Guidelines

- **Resolution:** 200 DPI
- **Background:** White for composite figures, black for individual fundus panels
- **Font:** Sans-serif (DejaVu Sans). Title 14pt bold, subtitles 11pt, annotations 9–10pt
- **Colors:** Match dashboard palette: blue=#378ADD, teal=#1D9E75, coral=#D85A30, gray=#888780
- **Fundus display:** `ax.imshow(img); ax.axis('off')` — no axes, no ticks
- **FOV circle annotations:** Green dashed line (#1D9E75), linewidth=2

---

## Regeneration Priority

**Must regenerate (breaking errors):**
1. `pipeline_stages_grid.png` — rotation artifacts, FOV not inscribed, Stage 3 mask irregular
2. `stage_2_isotropic_resize.png` — FOV cropped, not inscribed
3. `stage_4_flatfield.png` — input from broken Stage 2
4. `stage_5_clahe.png` — input from broken chain
5. `stage_7_normalized.png` — irregular polygon mask instead of circle
6. `bilateral_pair.png` — rotation + cropping
7. `before_after_pipeline.png` — pipeline side has artifacts
8. `baseline_vs_pipeline.png` — pipeline side has artifacts

**Must fix titles (updated numbering):**
9. `method_canonical_flip.png` — "Stage 0a" → "Stage 0"
10. `od_fovea_detection_steps.png` — "Stage 0b" → "Stage 1"
11. `method_fov_crop.png` — "Stage 1" → "Stage 2"
12. `method_flat_field.png` — "Stage 2" → "Stage 4", σ=45 → σ=0.07·D
13. `method_clahe_comparison.png` — "Stage 3" → "Stage 5"
14. `method_augmentation.png` — "Stage 5" → "Stage 6"
15. `methods_comparison_table.png` — "V4" → "Pipeline"

**OK as-is (only if titles fixed):**
16. `od_fovea_search_region.png` — small image, illustrates concept
17. `method_clahe_sensitivity.png` — title OK, but fundus images should ideally be regenerated

---

## Verification Checklist

After regeneration, verify:

- [ ] Every fundus image from Stage 2 onward has the circle **inscribed in the 512×512 square** (touching all 4 edges)
- [ ] No image shows rotation artifacts (black triangular corners from Stage 1)
- [ ] FOV mask (Stage 3 / stage_7_normalized.png right panel) is a **smooth circle**, not an irregular polygon
- [ ] All titles use pipeline stage numbering (0–7)
- [ ] No title contains "V4"
- [ ] Flat-field references say "σ = 0.07·D" (not "σ=45")
- [ ] Baseline images use stretch-resize (fills entire square, no circle)
- [ ] Pipeline images use isotropic resize (circle inscribed, black corners)
- [ ] `bilateral_pair.png` — after canonical flip, both rows look like right eyes
- [ ] `pipeline_stages_grid.png` — Stage 1 panel shows axis detection overlay (not a rotated image with artifacts)
- [ ] `methods_comparison_table.png` — says "Pipeline" with correct stage numbers
