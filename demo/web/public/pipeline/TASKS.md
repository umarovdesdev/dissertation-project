# Pipeline Stage Images — Task List

**Goal:** Generate per-stage demonstration images for the full DR diagnosis system.
Source: `../fundus-examples/{dr00,dr01,dr02,dr03,dr04}/{left_eye,right_eye}.{jpg,jpeg}`

All reproduction scripts live in `helpers/` — see `helpers/README.md` for parameters and decision rationale.

---

## Directory Structure

```
pipeline/
│
├── drNN/                                      DR Grade N
│   │
│   ├── input/                                 Raw fundus (before any processing)
│   │   ├── left.png                             OD on LEFT side
│   │   └── right.png                            OD on RIGHT side
│   │
│   ├── preprocessing/                         ─── 8-stage pipeline ───
│   │   │         │
│   │   │         ▼ stage 0 takes input/
│   │   ├── stage_0_canonical_flip/            Normalize eye laterality
│   │   │   ├── left.png                         FLIPPED horizontally → OD now on right
│   │   │   └── right.png                        unchanged
│   │   │         │
│   │   │         ▼ stage 1 takes stage_0/
│   │   ├── stage_1_od_fovea_rotation/         Align OD-fovea axis to horizontal
│   │   │   ├── left.png                         Final rotation result (image-center variant)
│   │   │   ├── right.png
│   │   │   ├── od/                              Rotation around OD center
│   │   │   ├── fovea/                           Rotation around fovea center
│   │   │   ├── midpoint/                        Rotation around OD-fovea midpoint
│   │   │   └── image/                           Rotation around image center (canonical)
│   │   │         │
│   │   │         ▼ stage 2 takes stage_1/image/
│   │   ├── stage_2_fov_crop_resize/           FOV crop + isotropic resize 512x512 + zero-pad
│   │   │   ├── left.png
│   │   │   └── right.png
│   │   │         │
│   │   │         ├────────────────────────┐
│   │   │         ▼                        ▼ side output (mask from clean stage_0)
│   │   ├── stage_4_flatfield/             stage_3_fov_mask/
│   │   │   ├── left.png                   │   ├── left.png    (binary: white=fundus)
│   │   │   └── right.png                  │   └── right.png   (binary: black=padding)
│   │   │         │                                │
│   │   │         ▼ stage 5 takes stage_4/         │ (mask saved for stage_7)
│   │   ├── stage_5_clahe/                         │
│   │   │   ├── left.png             (upgraded_clahe — dual-constraint, visible grid)
│   │   │   ├── right.png                          │
│   │   │   ├── cv2/                               │
│   │   │   │   ├── left.png         (cv2.createCLAHE — bilinear, smooth)
│   │   │   │   └── right.png                      │
│   │   │   └── polar/               (NOVEL — adaptive polar CLAHE)
│   │   │       ├── left.png                       │
│   │   │       ├── right.png                      │
│   │   │       ├── 1_vessel_detection/            │
│   │   │       ├── 2_vessel_density/              │
│   │   │       ├── 3_polar_grid_adaptive/         │
│   │   │       ├── 4_density_grid_adaptive/       │
│   │   │       └── 5_clahe_no_interpolation/      │
│   │   │         │                                │
│   │   │         ▼ stage 6 takes stage_5/polar/   │
│   │   ├── stage_6_augmentation/                  │
│   │   │   ├── 1_rotation/                        │
│   │   │   │   ├── {side}_contours.png        Iso-intensity rings (OD + Fovea)
│   │   │   │   ├── {side}_peaks.png           Rings + black vertical peaks (top/bottom of each ring)
│   │   │   │   ├── {side}_sectors.png         Peaks + all-to-all sector lines
│   │   │   │   ├── {side}_distribution_step.png   Empirical step histogram from sector angles
│   │   │   │   ├── {side}_distribution_normal.png Truncated Gaussian (σ from outer-ring formula)
│   │   │   │   └── params.md                      │
│   │   │   ├── 2_scale/             {side}_min/max.png + distribution.png + params.md
│   │   │   ├── 3_shear/             {side}_min/max.png + distribution.png + params.md
│   │   │   ├── 4_color_jitter/      {side}_min/max.png + distribution.png + params.md
│   │   │   └── 5_acquisition_variability/ {side}_min/max.png + distribution.png + params.md
│   │   │         │                                │
│   │   │         ▼ stage 7 = stage_5/polar RGB + stage_3 mask
│   │   └── stage_7_normalize/
│   │       ├── left.png             ImageNet normalize roundtrip + FOV mask applied
│   │       └── right.png            (preview of CNN's RGB input branch; mask = 4th channel)
│   │
│   └── results/                               ─── Model inference outputs (simulated) ───
│       │
│       ├── gradcam/                           Raw Grad-CAM heatmap (jet colormap)
│       │   ├── left.png
│       │   └── right.png
│       │
│       ├── attention_overlay/                 Heatmap blended over fundus (intensity-weighted, alpha=0.4)
│       │   ├── left.png
│       │   └── right.png
│       │
│       └── prediction/                        Class probability bar chart (5 classes)
│           ├── left.png
│           └── right.png
```

DR grades: dr00 (No DR), dr01 (Mild NPDR), dr02 (Moderate NPDR), dr03 (Severe NPDR), dr04 (Proliferative DR).

---

## Data Flow

Each stage takes the OUTPUT of the previous stage — sequential chain, not parallel from raw.

```
input ─→ S0 (flip) ─→ S1 (rotation) ─→ S2 (resize) ─┬─→ S4 (flatfield) ─→ S5 (CLAHE) ─→ S6 (aug) ─┐
                                                       │                                               │
                                                       └─→ S3 (FOV mask, from clean S0 source) ───────→ S7 (normalize + merge)
```

| Folder | Stage | Input from | What it does | Helper |
|--------|-------|------------|--------------|--------|
| `input/` | — | source file | Raw image, no processing | — |
| `stage_0_canonical_flip/` | S0 | `input/` | Left: mirror horizontal. Right: no-op | `s0_canonical_flip.py` |
| `stage_1_od_fovea_rotation/` | S1 | `stage_0/` | Manual annotation → 4 rotation centers | `s1_detect_markers.py` + `s1_draw_centers.py` + `s1_rotate.py` |
| `stage_2_fov_crop_resize/` | S2 | `stage_1/image/` | FOV crop + isotropic resize 512×512 + zero-pad | `s2_crop_resize.py` |
| `stage_3_fov_mask/` | S3 | clean `stage_0/` + coords.json | Binary mask from pre-rotation source (no BORDER_REFLECT artifacts) | `s3_fov_mask.py` |
| `stage_4_flatfield/` | S4 | `stage_2/` + `stage_3/` | Subtract low-freq illumination (σ=0.07·D) | `s4_flatfield.py` |
| `stage_5_clahe/` | S5 | `stage_4/` | 3 CLAHE variants (upgraded / cv2 / polar adaptive) | `s5_polar_adaptive.py` + `s5_all_grades.py` |
| `stage_6_augmentation/` | S6 | `stage_5/polar/` | Per-type min/max extremes + distributions | `s6_augmentation.py` (types 1–5) + `s6_rotation_vis.py` (contours) + `s6_rotation_peaks.py` (peaks/sectors/step+normal) |
| `stage_7_normalize/` | S7 | `stage_5/polar/` + `stage_3/` | ImageNet normalize roundtrip preview + FOV mask | `s7_normalize.py` |
| `results/` | — | `stage_4/` + `stage_5/polar/` + `stage_3/` + coords.json | Anomaly-driven Grad-CAM + overlay + prediction chart | `s8_results.py` |

S3 is generated from the clean stage_0 source (not from rotated images) to avoid `BORDER_REFLECT` "ears" in corners.
S4 takes RGB from S2 (not from S3).
S7 merges S5/polar RGB + S3 mask into final 4-channel tensor at training time; demo PNG shows the RGB branch only.

---

## Stage Ordering Rationale: flip → rotate → crop

### Why flip first?
OD-fovea detection depends on orientation. The algorithm looks for OD as the bright region on the right, fovea as the dark region on the left. Without flip, it doesn't know which side OD is on. After flip, OD is always on the right — detection is more reliable.

### Why rotate before crop?
Rotation on the full-size image has a "buffer" of black background at the edges. If you crop first (tight crop) then rotate — part of the fundus exits the canvas boundary, losing pixels.

### Conclusion
```
flip → rotate → crop
 ✓ Flip enables correct OD detection
 ✓ Rotate on full image — buffer available
 ✓ Crop last — clean trim of aligned image
```

---

## Stage 1: Rotation Center Comparison

For each image, 4 rotation center variants are generated for visual comparison:

| Center | Folder | Description |
|--------|--------|-------------|
| OD center | `od/` | Rotation around optic disc center |
| Fovea center | `fovea/` | Rotation around fovea center |
| Midpoint OD-fovea | `midpoint/` | Rotation around midpoint of the axis |
| Image center | `image/` | Rotation around geometric image center (canonical, used downstream) |

Stage 2+ takes `image/` as input. See helpers/README.md decision D2.

---

## Stage 2: Full pipeline (crop + isotropic resize)

Stage 2 performs FOV crop + isotropic resize to 512×512 + zero-padding (helpers/README.md decision D1). All subsequent stages (flat-field, CLAHE, etc.) operate on 512×512.

---

## Stage 5: Three CLAHE Variants

| Variant | Method | Notes |
|---------|--------|-------|
| `stage_5_clahe/{side}.png` | upgraded_clahe (8×8 rect) | Dual-constraint, no interpolation → **visible grid** |
| `stage_5_clahe/cv2/{side}.png` | cv2.createCLAHE | Standard CLAHE with bilinear interpolation → smooth |
| `stage_5_clahe/polar/{side}.png` | Adaptive Polar CLAHE | **Novel**: vessel-density grid + dual-constraint + polar bilinear interpolation |

Polar CLAHE substeps (`stage_5_clahe/polar/`):
- `1_vessel_detection/` — Frangi multi-scale Hessian response
- `2_vessel_density/` — Smoothed density heatmap (JET colormap)
- `3_polar_grid_adaptive/` — Non-uniform polar grid overlay
- `4_density_grid_adaptive/` — Density heatmap + grid overlay combined
- `5_clahe_no_interpolation/` — Per-sector dual-constraint CLAHE, NO blending (shows seams)

Polar CLAHE is the canonical S5 output for downstream stages (S6, S7, results).

**Sector area constraint (MIN_SECTOR_AREA_FRAC = 0.01):** every tile (ring × angular sector) must cover ≥ 1% of the per-image FOV pixel count (`mask.sum()`, ~189-205k px → threshold ~1,890-2,059 px). Rings whose total annular area is below the threshold collapse to a single 360° sector; remaining sectors are validated with `merge_small_sectors()` post-pass that merges any sub-threshold tile with its smaller-area neighbor. Rationale: ~8 samples per 256-bin LUT is the working minimum for stable CLAHE; tighter bound (0.5%) gives noisy LUTs, looser bound (2%) collapses inner rings and loses the vessel-density adaptivity in the macula.

---

## Stage 6: Augmentation Min/Max Extremes

Stage 6 is applied on-the-fly during training. For demo, we generate min/max extremes per augmentation type.

| Folder | Method | Min/Max | Probability |
|--------|--------|---------|-------------|
| `1_rotation/` | Truncated Gaussian, **adaptive σ** per image | ±40° clip | 100% |
| `2_scale/` | Log-uniform zoom | 0.9× / 1.1× | 100% |
| `3_shear/` | Uniform shear | ±2° | 30% |
| `4_color_jitter/` | ColorJitter (brightness/contrast/saturation/hue) | factors ∈ [0.9,1.1], hue ∈ [−0.02,0.02] | 50% per component |
| `5_acquisition_variability/` | Gaussian noise + JPEG compression | σ ∈ [2,6] / quality ∈ [70,100] | 15% / 20% |

**Adaptive σ formula** (from `experiments/src/preprocessing/od_fovea_detect.py`):
```
σ_pos = sqrt(r_od_outer² + r_fov_outer²)
σ_θ   = degrees(atan(σ_pos / OD_Fovea_distance))
σ_θ   = min(σ_θ, 15°)
```

**Rotation visualization** (`1_rotation/` extends beyond min/max with):
- `{side}_contours.png` — iso-intensity rings only (`s6_rotation_vis.py`)
- `{side}_peaks.png` — vertical peaks (top/bottom) on each ring (`s6_rotation_peaks.py`)
- `{side}_sectors.png` — all-to-all (Fovea_peak ↔ OD_peak) sector lines
- `{side}_distribution_step.png` — empirical step histogram, bins between sorted θ_ij, p_k = 1/N
- `{side}_distribution_normal.png` — truncated Gaussian fit, x-axis ±22.5°

---

## Stage 7: Normalize Preview

`s7_normalize.py` produces visual preview of CNN's RGB input branch:
1. Input: `stage_5_clahe/polar/{side}.png` (RGB) + `stage_3_fov_mask/{side}.png`
2. ImageNet normalize: `(x/255 - mean) / std`, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)
3. Roundtrip denormalize back to uint8 (≈ identity, with rounding) → preview
4. Multiply by binary FOV mask (padding zeroed; the 4th-channel mask gates the receptive field)

Mask is **not** rendered in the preview PNG — at training time it is concatenated as the 4th tensor channel.

---

## Results: Simulated Inference

`s8_results.py` produces plausible Grad-CAM, attention overlay, and prediction chart **without a trained checkpoint** by detecting real anatomical anomalies in the preprocessed fundus and weighting by grade severity.

**Detection on `stage_4_flatfield/{side}.png`** (no CLAHE distortion, flat illumination):
- Dark anomalies = `max(0, masked_blur(green) − green)` → hemorrhages, microaneurysms
- Bright anomalies = `max(0, L − masked_blur(L))` → hard exudates, cotton-wool spots
- Combined = `0.55·dark + 0.45·bright`
- OD softly suppressed (radial falloff, inner=1.1·r_od, outer=2.0·r_od)
- Power(1.4) sharpening, masked Gaussian blur σ=18 to mimic Grad-CAM smoothness
- Eroded FOV mask (25×25 ellipse) for boundary safety
- Per-grade scale: dr00=0.12, dr01=0.45, dr02=0.75, dr03=0.90, dr04=1.00

**Overlay** (`stage_5_clahe/polar/{side}.png` background): intensity-weighted blend, per-pixel weight = heatmap·α, α=0.4 — weak heatmap regions stay as pure fundus (no false-color rim).

**Prediction chart**: 5-bar matplotlib softmax-style probabilities, deterministic ±0.018σ perturbation per side. Predicted class is highlighted green when it matches the true grade.

---

## Helper Scripts

| Script | Purpose | Reproduces |
|--------|---------|------------|
| `s0_canonical_flip.py` | Stage 0 — horizontal flip for left eye | `stage_0_canonical_flip/{side}.png` |
| `s1_detect_markers.py` | Stage 1 step 2 — detect Paint dots → coords.json | `coords.json` |
| `s1_draw_centers.py` | Stage 1 step 3 — annotate 4 centers + axis line | `stage_1_od_fovea_rotation/{side}.png` |
| `s1_rotate.py` | Stage 1 step 4 — rotate around 4 centers | `stage_1_od_fovea_rotation/{od,fovea,midpoint,image}/{side}.png` |
| `s2_crop_resize.py` | Stage 2 — FOV crop + isotropic resize 512×512 | `stage_2_fov_crop_resize/{side}.png` |
| `s3_fov_mask.py` | Stage 3 — binary FOV mask from clean source | `stage_3_fov_mask/{side}.png` |
| `s4_flatfield.py` | Stage 4 — adaptive flat-field correction | `stage_4_flatfield/{side}.png` |
| `s5_polar_adaptive.py` | Stage 5 — polar CLAHE + 5 substeps | `stage_5_clahe/polar/...` |
| `s5_all_grades.py` | Stage 5 — all 3 CLAHE variants | `stage_5_clahe/{,cv2/,polar/}{side}.png` |
| `s6_augmentation.py` | Stage 6 types 1–5 — min/max + distributions + params | `stage_6_augmentation/{1..5}_*/...` |
| `s6_rotation_vis.py` | Stage 6 type 1 — iso-intensity rings + fan variants | `1_rotation/{side}_contours.png`, `{side}_variant_A/B.png`, `distribution_adaptive.png` |
| `s6_rotation_peaks.py` | Stage 6 type 1 — vertical peaks + sectors + step/normal distributions | `1_rotation/{side}_peaks.png`, `{side}_sectors.png`, `{side}_distribution_step.png`, `{side}_distribution_normal.png` |
| `s7_normalize.py` | Stage 7 — ImageNet normalize roundtrip + mask | `stage_7_normalize/{side}.png` |
| `s8_results.py` | Results — anomaly-based Grad-CAM + overlay + prediction | `results/{gradcam,attention_overlay,prediction}/{side}.png` |

Manual step (between s1_detect_markers and s1_draw_centers): annotate OD as black dot and Fovea as purple dot in MS Paint on `stage_0_canonical_flip/{side}.png`. See `helpers/README.md` step 1 for color codes and dot size.

---

## Image Counts

- Stage 0: 5 grades × 2 eyes = **10**
- Stage 1 final + 4 variants: 5 × 2 × 5 = **50**
- Stage 2: 5 × 2 = **10**
- Stage 3: 5 × 2 = **10**
- Stage 4: 5 × 2 = **10**
- Stage 5 (upgraded + cv2 + polar final): 5 × 2 × 3 = **30**
- Stage 5 polar substeps (5 substeps × 2 eyes × 5 grades): **50**
- Stage 6 augmentation (5 types × (4 min/max + 1 distribution) × 5 grades): **125**
- Stage 6 rotation extras (contours + peaks + sectors + dist_step + dist_normal + variant_A + variant_B + adaptive_dist): 5 × 2 × ~7 + extras: **~80**
- Stage 7: 5 × 2 = **10**
- Results (gradcam + attention_overlay + prediction): 5 × 2 × 3 = **30**
- **Total: ~415 images**

---

## Progress

| Stage | Status | Helper |
|-------|--------|--------|
| `input/` | done | (manual) |
| `stage_0_canonical_flip/` | done | `s0_canonical_flip.py` |
| `stage_1_od_fovea_rotation/` (4 variants + final) | done | `s1_*.py` |
| `stage_2_fov_crop_resize/` | done | `s2_crop_resize.py` |
| `stage_3_fov_mask/` | done | `s3_fov_mask.py` |
| `stage_4_flatfield/` | done | `s4_flatfield.py` |
| `stage_5_clahe/` (3 variants + 5 polar substeps) | done | `s5_polar_adaptive.py`, `s5_all_grades.py` |
| `stage_6_augmentation/` types 1–5 | done | `s6_augmentation.py` |
| `stage_6_augmentation/1_rotation/` contours + peaks + sectors + step/normal | done | `s6_rotation_vis.py`, `s6_rotation_peaks.py` |
| `stage_7_normalize/` | done | `s7_normalize.py` |
| `results/gradcam/` | done | `s8_results.py` |
| `results/attention_overlay/` | done | `s8_results.py` |
| `results/prediction/` | done | `s8_results.py` |

---

## Technical Notes

- Output format: 512×512 PNG (lossless), 3-channel RGB except FOV mask (1-channel grayscale)
- Coordinate transform: OpenCV `getRotationMatrix2D` convention `[cos sin; -sin cos]`, applied to coords.json landmarks → stage_1 crop bbox → stage_2 resize to 512×512
- FOV mask: binary uint8 (white=fundus, black=padding), generated from pre-rotation source
- Stage 7: ImageNet stats (baseline path); training pipeline uses dataset-specific stats from EyePACS
- Grad-CAM target (real pipeline): `layer4[-1]` (ResNet-50) / `conv_head` (EfficientNet)
- Attention overlay: intensity-weighted blend (per-pixel weight = heatmap·α), α=0.4
- Prediction chart: matplotlib, 5 bars (grades 0–4), green if pred matches true grade, red otherwise
