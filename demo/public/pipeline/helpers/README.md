# Pipeline Helpers — Reproduction Guide

Scripts to reproduce all preprocessing demo images from scratch.

## Prerequisites

- Python 3.x with OpenCV, NumPy, Pillow (`pip install opencv-python numpy Pillow`)
- Raw fundus images in `pipeline/drNN/input/left.png, right.png`
- For stage 1: user must manually mark OD and Fovea on images (see step 2)

## File Overview

```
helpers/
├── README.md                 ← this file
├── coords.json               ← detected OD/Fovea/Image/Midpoint coordinates + angles
├── s0_canonical_flip.py      ← Stage 0: horizontal flip for left eye
├── s1_detect_markers.py      ← Stage 1 step 1: detect Paint markers → coords.json
├── s1_draw_centers.py        ← Stage 1 step 2: draw 4 annotated centers on images
├── s1_rotate.py              ← Stage 1 step 3: rotate around 4 centers
├── s2_crop_resize.py         ← Stage 2: FOV crop + isotropic resize 512x512
├── s3_fov_mask.py            ← Stage 3: binary FOV mask from clean pre-rotation source
├── s4_flatfield.py           ← Stage 4: adaptive flat-field correction (σ=0.07·D)
├── s5_polar_adaptive.py      ← Stage 5: fovea-centered non-uniform polar CLAHE
├── s5_all_grades.py          ← Stage 5: all 3 CLAHE variants (upgraded + cv2 + polar)
├── s6_augmentation.py        ← Stage 6: augmentation demo (min/max per type + distributions)
└── s6_rotation_vis.py        ← Stage 6: adaptive rotation uncertainty visualization
```

---

## Full Reproduction Workflow

### Stage 0: Canonical Flip

```bash
python helpers/s0_canonical_flip.py
```

- Input: `pipeline/drNN/input/left.png, right.png`
- Output: `pipeline/drNN/preprocessing/stage_0_canonical_flip/left.png, right.png`
- Left eye flipped horizontally → OD on right. Right eye copied unchanged.

### Stage 1: OD-Fovea Rotation (4 steps)

#### Step 1 — Manual annotation

Copy `stage_0_canonical_flip/*.png` into `stage_1_od_fovea_rotation/*.png`.
Open each image in Paint and place two dots:

- **Black dot** (RGB 0,0,0) → center of Optic Disc (OD)
- **Purple/lilac dot** (~RGB 180,130,255) → center of Fovea

Dot size: ~5-10px radius.

#### Step 2 — Detect markers

```bash
python helpers/s1_detect_markers.py
```

Detects Paint dots via HSV filtering, computes image center + midpoint, saves to `coords.json`.

#### Step 3 — Draw annotated centers

```bash
python helpers/s1_draw_centers.py
```

Overwrites `stage_1/{side}.png` with 4 colored markers + axis line.

#### Step 4 — Rotate

```bash
python helpers/s1_rotate.py
```

Rotates clean stage_0 images around 4 centers → `stage_1/{od,fovea,midpoint,image}/{side}.png`.

### Stage 2: FOV Crop + Resize

```bash
python helpers/s2_crop_resize.py
```

- Input: `stage_1_od_fovea_rotation/image/{side}.png` (image-center rotation chosen)
- Output: `stage_2_fov_crop_resize/{side}.png` (512x512)
- Full pipeline: FOV crop + isotropic resize + zero-padding

### Stage 3: FOV Mask

```bash
python helpers/s3_fov_mask.py
```

- Input: `stage_0_canonical_flip/{side}.png` + `coords.json`
- Output: `stage_3_fov_mask/{side}.png` (512x512, binary)
- Mask generated from clean pre-rotation image, then rotated + cropped + resized identically to RGB

### Stage 4: Flat-Field Correction

```bash
python helpers/s4_flatfield.py
```

- Input: `stage_2_fov_crop_resize/{side}.png` (RGB) + `stage_3_fov_mask/{side}.png`
- Output: `stage_4_flatfield/{side}.png` (512x512)
- Formula: `corrected = image - GaussianBlur(image, σ) + 128`
- Adaptive σ = 0.07 × FOV_diameter (estimated from mask area)
- Mask zeros out padding and BORDER_REFLECT artifacts

### Stage 5: CLAHE (3 variants + adaptive polar substeps)

```bash
python helpers/s5_polar_adaptive.py
```

Stage 5 produces three CLAHE variants and six substep visualizations:

#### Variants (all in `stage_5_clahe/`)

| Folder | Method | Notes |
|--------|--------|-------|
| `stage_5_clahe/{side}.png` | upgraded_clahe (8×8 rect) | Dual-constraint, no interpolation → **visible grid** |
| `stage_5_clahe/cv2/{side}.png` | cv2.createCLAHE | Standard CLAHE with bilinear interpolation → smooth |
| `stage_5_clahe/polar/{side}.png` | Adaptive Polar CLAHE | **Novel**: vessel-density grid + dual-constraint + polar bilinear interpolation |

#### Polar CLAHE substeps (all in `stage_5_clahe/polar/`)

```
polar/
├── 1_vessel_detection/    Frangi multi-scale Hessian response (gamma=0.3 for visibility)
├── 2_vessel_density/      Smoothed density heatmap (JET colormap)
├── 3_polar_grid_adaptive/ Non-uniform polar grid overlaid on fundus
├── 4_density_grid_adaptive/ Density heatmap + grid overlay combined
├── 5_clahe_no_interpolation/ Dual-constraint CLAHE per sector, NO blending (shows seams)
├── left.png               Final result WITH polar bilinear interpolation
└── right.png
```

**Pipeline within polar CLAHE:**
1. **Vessel detection** — Frangi filter (multi-scale Hessian, σ = 1.0, 1.5, 2.0, 3.0)
2. **Vessel density map** — Gaussian-smoothed (σ=20) vessel response per region
3. **Adaptive polar grid** — fovea-centered (from coords.json, transformed to 512×512), log-spaced radial rings, **non-uniform angular sectors** (72 fine bins → adaptive merge based on vessel density)
4. **Per-sector dual-constraint CLAHE** — LUT computed with `clip = min(clip_factor × area/256, global_threshold × area)`
5. **Polar bilinear interpolation** — each pixel blends 4 neighboring sector LUTs (2 radial × 2 angular) → seamless result

**Parameters:**
- Nr = 8 radial rings (log-spaced: `r = (i/Nr)^1.5 × r_max`)
- N_fine = 72 angular bins per ring for density analysis
- MIN_SECTOR_BINS = 2, MAX_SECTOR_BINS = 6 (sector width bounds in fine bins)
- **MIN_SECTOR_AREA_FRAC = 0.01** — every tile (ring × angular sector) must cover ≥ 1% of FOV pixels (mask-based, per image). Inner rings whose total annular area is < 1% are kept as a single 360° sector. After greedy splitting, `merge_small_sectors()` post-processes any sub-threshold tile by merging it with the smaller-area neighbor.
- Merge threshold = median of non-zero smoothed density → high-density regions get narrower sectors
- clip_factor = 2.0, global_threshold = 0.01
- Center = fovea (from coords.json, transformed through rotation → crop → resize to 512×512)
- FOV reference: actual `mask.sum()` per image (~189-205k px), not 512² canvas. 1% threshold ≈ 1,890-2,059 px per tile — gives ~8 samples/256-bin LUT, the working minimum for stable CLAHE.

### Stage 6: Augmentation (train-time only)

```bash
python helpers/s6_augmentation.py
```

Stage 6 is applied on-the-fly during training (not saved to disk). For demo purposes, we generate **min/max extremes** of each augmentation type in isolation, plus distribution plots and parameter documentation.

**Input:** `stage_5_clahe/polar/{side}.png` (after polar CLAHE)

**Flip excluded** — canonical flip (Stage 0) already normalizes eye orientation.

#### Augmentation types (all in `stage_6_augmentation/`)

| Folder | Method | Min/Max shown | Probability |
|--------|--------|---------------|-------------|
| `1_rotation/` | Truncated Gaussian | ±40° (clip boundary) | 100% |
| `2_scale/` | Log-uniform zoom | 0.9× / 1.1× | 100% |
| `3_shear/` | Uniform shear | ±2° | 30% |
| `4_pca_color_jitter/` | PCA color noise | ±1σ (all components) | 50% |
| `5_brightness_contrast/` | Linear α×pixel+β | α=0.9/1.1, β=±10 | 50% |

#### Files per augmentation type

```
{type}/
├── left_min.png       Left eye, minimum augmentation value
├── left_max.png       Left eye, maximum augmentation value
├── right_min.png      Right eye, minimum augmentation value
├── right_max.png      Right eye, maximum augmentation value
├── distribution.png   Probability density plot
└── params.md          Configuration details from experiments/
```

**Key novelty — adaptive rotation σ:** rotation sigma is derived from OD-fovea detection uncertainty per image, not a fixed value. Fallback σ = 13° when detection fails.

**Parameters from:** `experiments/configs/default.yaml` (lines 54–70), `experiments/src/data/augmentation_unified.py`

#### Adaptive rotation visualization

```bash
python helpers/s6_rotation_vis.py              # all grades
python helpers/s6_rotation_vis.py dr03          # single grade
```

Generates iso-intensity contour rings around OD and Fovea to visualize detection uncertainty, plus angular fan variants showing how positional uncertainty translates to rotation σ.

**Approach:**
1. Green channel of `stage_2` image (best fundus landmark contrast)
2. Gaussian blur → threshold at multiple intensity levels → binary mask pre-blur (5×5, σ=1.5)
3. Contour extraction → resample to 120 uniform points → circular moving average (window=11)
4. Fallback chain when contrast < 5: green channel → grayscale → LAB L-channel → organic pseudo-ellipses

**Coordinate transform:** OpenCV `getRotationMatrix2D` convention `[cos sin; -sin cos]` applied to coords.json landmarks → stage_1 crop → stage_2 resize to 512×512.

**Files per grade in `1_rotation/`:**

```
1_rotation/
├── {side}_contours.png      Smoothed iso-intensity rings only
├── {side}_variant_A.png        Rings + tangent band fan (axis uncertainty)
├── {side}_variant_B.png        Rings + angular cone fan from midpoint
└── distribution_adaptive.png   Adaptive σ vs fallback σ=13° comparison
```

**Parameters:**
- OD: 5 contour levels, blur σ=10, search radius = 2.5 × r_od
- Fovea: 4 contour levels, blur σ=5, search radius = 3 × r_fovea
- r_od = OD-Fovea distance / 7, r_fovea = r_od × 0.5
- σ_θ = min(arctan(√(r_od² + r_fovea²) / distance), 15°)
- Fallback Fovea radii: [0.7, 1.2, 1.8, 2.3] × r_fovea, elongation=1.1
- Fan variant A: 9 tangent lines connecting Fovea to OD uncertainty spans
- Fan variant B: 9 lines from midpoint, ±2.5σ_θ angular spread

---

## Key Decisions

### D1. Stage 2 includes resize to 512x512

Initially considered crop-only (preserving original pixels) for demo. Changed to full pipeline with isotropic resize to 512x512 — all subsequent stages (flat-field, CLAHE, etc.) operate on 512x512.

### D2. Rotation center: image center chosen for stage_2+

All 4 rotation variants (od/fovea/midpoint/image) are generated for visual comparison, but `image/` is used as input for stage_2 onward. Rotating around image center keeps the fundus centered on the canvas, simplifying crop.

### D3. FOV mask from pre-rotation source (avoids BORDER_REFLECT artifacts)

Problem: `cv2.warpAffine(borderMode=BORDER_REFLECT)` fills rotation corners with mirrored fundus pixels. These appear as bright "ears" in corners, and a naive threshold mask includes them as fundus.

Solution: generate the binary mask from the clean stage_0 image (no rotation artifacts), then apply the same rotation with `BORDER_CONSTANT=0`. The mask exactly follows real fundus boundaries without "ears".

Small edge artifacts from the original camera frame are preserved — they are real, not rotation artifacts.

### D4. FOV detection for square images

The pipeline's `detect_fov_bbox()` only works for landscape images (w > 1.2h). Our demo images are square (already cropped from original landscape). Fallback: grayscale threshold (V > 15) + morphological cleanup to detect the fundus circle on black background.

### D5. Stage 5 CLAHE: three variants compared

Problem: our `upgraded_clahe.py` (dual clip constraint, 8×8 rectangular tiles) produces visible grid squares because it lacks bilinear interpolation between tiles.

Approaches tried:
1. **upgraded_clahe** — dual-constraint but no interpolation → grid artifacts
2. **cv2.createCLAHE** — built-in interpolation, smooth result, but only single clipLimit
3. **Adaptive Polar CLAHE** (novel) — combines: vessel-density-driven non-uniform polar tiling + dual-constraint clipping + polar bilinear interpolation

Decision: all three variants saved for comparison. Polar CLAHE is the novel contribution:
- Fovea-centered (coords.json → rotation → crop → resize transform)
- Polar grid matches radial fundus geometry (no wasted corner tiles)
- Log-spaced rings (finer at fovea, coarser at periphery)
- **Non-uniform angular sectors**: 72 fine bins analyzed per ring, merged adaptively where vessel density is low, split where high
- Dual-constraint preserved from upgraded_clahe
- Vectorized polar bilinear interpolation eliminates seams

Example sectors per ring (with 1% FOV-area constraint): dr00/left `[1, 1, 3, 7, 12, 15, 18, 17]`, dr03/left `[1, 2, 5, 10, 15, 16, 9, 6]`, dr04/left `[1, 1, 4, 8, 12, 14, 17, 11]`. Innermost ring (ring 0) is always single-sector — its annular area (~440-660 px) is below the 1% threshold for all test images.

Design document: `experiments/docs/polar_clahe_design.md`

### D6. BORDER_REFLECT for RGB rotation

RGB rotation uses `BORDER_REFLECT` (not `BORDER_CONSTANT=0`) to avoid black triangles in corners. The reflected pixels are visible but:
- Stage 2 crop removes most of them
- Stage 3 mask excludes them from the model's 4th channel
- Remaining visible artifacts in corners are cosmetic only

---

## Coordinates (coords.json)

| Grade | Side  | OD (x,y)    | Fovea (x,y)  | Angle    | Size      |
|-------|-------|-------------|---------------|----------|-----------|
| dr00  | left  | 1073, 587   | 631, 633      | -5.94°   | 1280x1280 |
| dr00  | right | 1053, 629   | 648, 638      | -1.27°   | 1280x1280 |
| dr01  | left  | 1055, 739   | 558, 767      | -3.22°   | 1455x1455 |
| dr01  | right | 1023, 635   | 540, 764      | -14.95°  | 1455x1455 |
| dr02  | left  | 1715, 1112  | 878, 1124     | -0.82°   | 2313x2313 |
| dr02  | right | 1715, 1044  | 892, 1102     | -4.03°   | 2312x2312 |
| dr03  | left  | 1027, 665   | 509, 740      | -8.24°   | 1381x1381 |
| dr03  | right | 1156, 647   | 680, 700      | -6.35°   | 1381x1381 |
| dr04  | left  | 2640, 1661  | 1660, 1791    | -7.56°   | 3419x3419 |
| dr04  | right | 2844, 1575  | 1853, 1640    | -3.75°   | 3439x3439 |

## Image Counts

- Stage 0: 5 grades x 2 eyes = **10 images**
- Stage 1 annotated: 5 grades x 2 eyes = **10 images**
- Stage 1 rotations: 5 grades x 2 eyes x 4 centers = **40 images**
- Stage 2: 5 grades x 2 eyes = **10 images**
- Stage 3: 5 grades x 2 eyes = **10 images**
- Stage 4: 5 grades x 2 eyes = **10 images**
- Stage 5 upgraded_clahe: 5 grades x 2 eyes = **10 images**
- Stage 5 cv2: 5 grades x 2 eyes = **10 images**
- Stage 5 polar (final + 5 substeps): 5 grades x 2 eyes x 6 = **60 images**
- Stage 6 augmentation: 5 grades x 5 types x (4 images + 1 distribution) = **125 images**
- Stage 6 rotation vis: 5 grades x (2 eyes x 3 variants + 1 distribution) = **35 images**
- **Total so far: 330 images**
