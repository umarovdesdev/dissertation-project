"""
Stage 6: Augmentation demo — isolated min/max for each augmentation type.
Parameters from experiments/configs/default.yaml and experiments/src/data/augmentation_unified.py.
Generates left_min/max, right_min/max, distribution.png, and params.md per type.

Sub-steps (matching the production order in augmentation_unified.py):
  1_rotation, 2_scale, 3_shear  — unified affine (geometric)
  4_color_jitter                — ColorJitter (brightness/contrast/saturation/hue)
  5_acquisition_variability     — Gaussian noise + JPEG compression
"""

import cv2
import numpy as np
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]

# === From experiments/configs/default.yaml + augmentation_unified.py ===
ROTATION_SIGMA = 13.0
ROTATION_CLIP = 40.0
ZOOM_RANGE = (0.9, 1.1)
STRETCH_RANGE = (1.0 / 1.05, 1.05)
SHEAR_RANGE = (-2.0, 2.0)
SHEAR_PROB = 0.3
# ColorJitter (each component sampled and applied independently with CJ_PROB)
CJ_BRIGHTNESS_RANGE = (0.9, 1.1)
CJ_CONTRAST_RANGE = (0.9, 1.1)
CJ_SATURATION_RANGE = (0.9, 1.1)
CJ_HUE_RANGE = (-0.02, 0.02)
CJ_PROB = 0.5
# Acquisition variability
NOISE_SIGMA_RANGE = (2.0, 6.0)
NOISE_PROB = 0.15
JPEG_QUALITY_RANGE = (70, 100)
JPEG_PROB = 0.20
BORDER_MODE = cv2.BORDER_REFLECT

_LUMA = np.array([0.299, 0.587, 0.114], dtype=np.float32)


def load_pair(gr, side):
    img = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png"))
    mask = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"), cv2.IMREAD_GRAYSCALE)
    return img, mask


def masked(img, mask):
    return img * np.expand_dims(mask > 0, axis=-1).astype(np.uint8)


# === Geometric augmentations (matching augmentation_unified.py) ===

def aug_rotation(img, mask, angle_deg):
    h, w = img.shape[:2]
    center = (w / 2.0, h / 2.0)
    M = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    out = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=BORDER_MODE)
    return masked(out, mask)


def aug_scale(img, mask, zoom):
    h, w = img.shape[:2]
    center = (w / 2.0, h / 2.0)
    M = cv2.getRotationMatrix2D(center, 0, zoom)
    out = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=BORDER_MODE)
    m_out = cv2.warpAffine(mask, M, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT)
    return masked(out, m_out)


def aug_shear(img, mask, shear_deg):
    h, w = img.shape[:2]
    center = (w / 2.0, h / 2.0)
    M = cv2.getRotationMatrix2D(center, 0, 1.0)
    M[0, 1] += np.tan(np.radians(shear_deg))
    out = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=BORDER_MODE)
    m_out = cv2.warpAffine(mask, M, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT)
    return masked(out, m_out)


# === ColorJitter (matching augmentation_unified._apply_color_jitter) ===

def aug_color_jitter(img_bgr, mask, brightness, contrast, saturation, hue):
    """Apply all four ColorJitter components deterministically (for min/max demo)."""
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
    # Brightness
    rgb = rgb * brightness
    # Contrast — blend toward the per-image grayscale mean
    gray_mean = float(np.mean(rgb @ _LUMA))
    rgb = (rgb - gray_mean) * contrast + gray_mean
    rgb = np.clip(rgb, 0, 255)
    # Saturation — blend toward the per-pixel grayscale image
    gray = rgb @ _LUMA
    rgb = gray[..., None] + saturation * (rgb - gray[..., None])
    rgb = np.clip(rgb, 0, 255)
    # Hue — rotate the H channel in HSV ([0,180) in OpenCV); hue is a fraction of the circle
    shift = hue * 180.0
    hsv = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 0] = (hsv[..., 0] + shift) % 180.0
    rgb = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    out = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return masked(out, mask)


# === Acquisition variability: Gaussian noise + JPEG compression ===

def aug_acquisition(img_bgr, mask, sigma, jpeg_quality, seed=0):
    """Additive Gaussian noise then lossy JPEG re-compression (deterministic via seed)."""
    rng = np.random.RandomState(seed)
    noisy = img_bgr.astype(np.float32) + rng.normal(0.0, sigma, img_bgr.shape).astype(np.float32)
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    ok, buf = cv2.imencode(".jpg", noisy, [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)])
    out = cv2.imdecode(buf, cv2.IMREAD_COLOR) if ok else noisy
    return masked(out, mask)


# === Distribution plots ===

def plot_rotation_dist(path):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.linspace(-50, 50, 1000)
    pdf = np.exp(-x**2 / (2 * ROTATION_SIGMA**2))
    pdf[np.abs(x) > ROTATION_CLIP] = 0
    pdf = pdf / (pdf.sum() * (x[1] - x[0]))
    ax.fill_between(x, pdf, alpha=0.3, color='steelblue')
    ax.plot(x, pdf, color='steelblue', lw=2)
    ax.axvline(-ROTATION_CLIP, color='red', ls='--', lw=1, label=f'clip = ±{ROTATION_CLIP}°')
    ax.axvline(ROTATION_CLIP, color='red', ls='--', lw=1)
    ax.set_xlabel('Rotation angle (degrees)')
    ax.set_ylabel('Probability density')
    ax.set_title(f'Truncated Gaussian (σ={ROTATION_SIGMA}°, clip=±{ROTATION_CLIP}°)')
    ax.legend()
    ax.set_xlim(-50, 50)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def plot_scale_dist(path):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.linspace(0.85, 1.15, 1000)
    log_range = np.log(ZOOM_RANGE[1]) - np.log(ZOOM_RANGE[0])
    pdf = np.where((x >= ZOOM_RANGE[0]) & (x <= ZOOM_RANGE[1]), 1.0 / (x * log_range), 0)
    ax.fill_between(x, pdf, alpha=0.3, color='forestgreen')
    ax.plot(x, pdf, color='forestgreen', lw=2)
    ax.set_xlabel('Zoom factor')
    ax.set_ylabel('Probability density')
    ax.set_title(f'Log-uniform [{ZOOM_RANGE[0]}, {ZOOM_RANGE[1]}]')
    ax.set_xlim(0.85, 1.15)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def plot_shear_dist(path):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.linspace(-4, 4, 1000)
    width = SHEAR_RANGE[1] - SHEAR_RANGE[0]
    pdf = np.where((x >= SHEAR_RANGE[0]) & (x <= SHEAR_RANGE[1]), SHEAR_PROB / width, 0)
    ax.fill_between(x, pdf, alpha=0.3, color='darkorange')
    ax.plot(x, pdf, color='darkorange', lw=2)
    ax.annotate(f'P(no shear) = {1 - SHEAR_PROB:.0%}', xy=(0, 0), xytext=(0, pdf.max() * 0.8),
                ha='center', fontsize=9, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
    ax.set_xlabel('Shear angle (degrees)')
    ax.set_ylabel('Probability density')
    ax.set_title(f'Uniform [{SHEAR_RANGE[0]}°, {SHEAR_RANGE[1]}°], P(apply)={SHEAR_PROB}')
    ax.set_xlim(-4, 4)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def plot_color_jitter_dist(path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
    # Brightness / contrast / saturation share the same [0.9, 1.1] band
    x1 = np.linspace(0.85, 1.15, 1000)
    w1 = CJ_BRIGHTNESS_RANGE[1] - CJ_BRIGHTNESS_RANGE[0]
    pdf1 = np.where((x1 >= CJ_BRIGHTNESS_RANGE[0]) & (x1 <= CJ_BRIGHTNESS_RANGE[1]), 1.0 / w1, 0)
    ax1.fill_between(x1, pdf1, alpha=0.3, color='teal')
    ax1.plot(x1, pdf1, color='teal', lw=2)
    ax1.set_xlabel('Factor (brightness / contrast / saturation)')
    ax1.set_ylabel('Probability density')
    ax1.set_title(f'Uniform [{CJ_BRIGHTNESS_RANGE[0]}, {CJ_BRIGHTNESS_RANGE[1]}]')

    x2 = np.linspace(-0.04, 0.04, 1000)
    w2 = CJ_HUE_RANGE[1] - CJ_HUE_RANGE[0]
    pdf2 = np.where((x2 >= CJ_HUE_RANGE[0]) & (x2 <= CJ_HUE_RANGE[1]), 1.0 / w2, 0)
    ax2.fill_between(x2, pdf2, alpha=0.3, color='purple')
    ax2.plot(x2, pdf2, color='purple', lw=2)
    ax2.set_xlabel('Hue shift (fraction of colour circle)')
    ax2.set_ylabel('Probability density')
    ax2.set_title(f'Uniform [{CJ_HUE_RANGE[0]}, {CJ_HUE_RANGE[1]}]')

    fig.suptitle(f'ColorJitter — each component applied independently, P(apply) = {CJ_PROB}', fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def plot_acquisition_dist(path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
    x1 = np.linspace(0, 8, 1000)
    w1 = NOISE_SIGMA_RANGE[1] - NOISE_SIGMA_RANGE[0]
    pdf1 = np.where((x1 >= NOISE_SIGMA_RANGE[0]) & (x1 <= NOISE_SIGMA_RANGE[1]), 1.0 / w1, 0)
    ax1.fill_between(x1, pdf1, alpha=0.3, color='slategray')
    ax1.plot(x1, pdf1, color='slategray', lw=2)
    ax1.set_xlabel('Gaussian noise σ (8-bit RGB)')
    ax1.set_ylabel('Probability density')
    ax1.set_title(f'Uniform [{NOISE_SIGMA_RANGE[0]}, {NOISE_SIGMA_RANGE[1]}], P(apply)={NOISE_PROB}')

    x2 = np.linspace(60, 100, 1000)
    w2 = JPEG_QUALITY_RANGE[1] - JPEG_QUALITY_RANGE[0]
    pdf2 = np.where((x2 >= JPEG_QUALITY_RANGE[0]) & (x2 <= JPEG_QUALITY_RANGE[1]), 1.0 / w2, 0)
    ax2.fill_between(x2, pdf2, alpha=0.3, color='indianred')
    ax2.plot(x2, pdf2, color='indianred', lw=2)
    ax2.set_xlabel('JPEG quality')
    ax2.set_ylabel('Probability density')
    ax2.set_title(f'Uniform [{JPEG_QUALITY_RANGE[0]}, {JPEG_QUALITY_RANGE[1]}], P(apply)={JPEG_PROB}')

    fig.suptitle('Acquisition variability — Gaussian noise + JPEG compression', fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


# === Params.md content ===

ROTATION_MD = f"""# Rotation Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Distribution | Truncated Gaussian | `augmentation_unified.py` (`_sample_affine_params`) |
| σ (sigma) | {ROTATION_SIGMA}° | `default.yaml: rotation_sigma` |
| Clip boundary | ±{ROTATION_CLIP}° | `default.yaml: rotation_clip` |
| Adaptive sigma | Enabled | `default.yaml: adaptive_rotation_sigma` |
| Fallback sigma | {ROTATION_SIGMA}° | `default.yaml: fallback_rotation_sigma` |
| Probability | 100% (always applied) | — |
| Interpolation | Stochastic: 60% linear, 30% cubic, 10% nearest | `default.yaml: interp_weights` |
| Border mode | BORDER_REFLECT | `default.yaml: border_mode` |

## Algorithm

Rotation angle sampled from truncated Gaussian:

```python
theta = np.random.normal(0.0, rotation_sigma)
theta = np.clip(theta, -rotation_clip, rotation_clip)
```

**Adaptive sigma** (key novelty): when OD-fovea detection succeeds,
σ is derived from the angular uncertainty of OD-fovea axis localization.
When detection fails, fallback σ = {ROTATION_SIGMA}° is used.

~68% of samples fall within ±{ROTATION_SIGMA}°, ~95% within ±{2 * ROTATION_SIGMA}°.
Hard clip at ±{ROTATION_CLIP}° prevents extreme rotations.

## Demo images

- `left.png / right.png` — source images (pre-augmentation)

Rotation demo with min/max angles will be added separately as part of the
adaptive rotation novelty presentation.
"""

SCALE_MD = f"""# Scale Augmentation (Zoom + Stretch)

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Zoom range | [{ZOOM_RANGE[0]}, {ZOOM_RANGE[1]}] | `default.yaml: zoom_range` |
| Zoom distribution | Log-uniform | `augmentation_unified.py` (`_sample_affine_params`) |
| Stretch range | [{STRETCH_RANGE[0]:.6f}, {STRETCH_RANGE[1]}] (= [1/1.05, 1.05]) | `default.yaml: stretch_range` |
| Stretch distribution | Log-uniform | `augmentation_unified.py` (`_sample_affine_params`) |
| Probability | 100% (always applied) | — |

## Algorithm

Zoom (isotropic) and stretch (anisotropic) combined into one affine:

```python
log_zoom = np.random.uniform(np.log(0.9), np.log(1.1))
zoom = np.exp(log_zoom)

log_stretch = np.random.uniform(np.log(1/1.05), np.log(1.05))
stretch = np.exp(log_stretch)

sx = zoom * stretch   # horizontal scale
sy = zoom / stretch   # vertical scale
```

Zoom controls overall magnification, stretch adds slight anisotropy
(simulates different camera distances / fundus curvature).

## Demo images

- `left_min / right_min` — zoom = {ZOOM_RANGE[0]} (10% zoom out)
- `left_max / right_max` — zoom = {ZOOM_RANGE[1]} (10% zoom in)
"""

SHEAR_MD = f"""# Shear Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Shear range | [{SHEAR_RANGE[0]}°, {SHEAR_RANGE[1]}°] | `default.yaml: shear_range` |
| Distribution | Uniform | `augmentation_unified.py` (`_sample_affine_params`) |
| Probability | {SHEAR_PROB} ({SHEAR_PROB * 100:.0f}%) | `default.yaml: shear_prob` |

## Algorithm

Horizontal shear applied with probability {SHEAR_PROB * 100:.0f}%:

```python
if np.random.rand() < {SHEAR_PROB}:
    shear_deg = np.random.uniform({SHEAR_RANGE[0]}, {SHEAR_RANGE[1]})
    shear_rad = np.radians(shear_deg)
else:
    shear_rad = 0.0
```

Integrated into the unified affine matrix (M[0,1] += tan(shear_rad)).
Simulates slight camera tilt / non-perpendicular imaging angle.

## Demo images

- `left_min / right_min` — shear = {SHEAR_RANGE[0]}° (maximum left skew)
- `left_max / right_max` — shear = {SHEAR_RANGE[1]}° (maximum right skew)
"""

COLOR_JITTER_MD = f"""# ColorJitter (Brightness / Contrast / Saturation / Hue)

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Brightness factor | [{CJ_BRIGHTNESS_RANGE[0]}, {CJ_BRIGHTNESS_RANGE[1]}] | `default.yaml: color_jitter_brightness_range` |
| Contrast factor | [{CJ_CONTRAST_RANGE[0]}, {CJ_CONTRAST_RANGE[1]}] | `default.yaml: color_jitter_contrast_range` |
| Saturation factor | [{CJ_SATURATION_RANGE[0]}, {CJ_SATURATION_RANGE[1]}] | `default.yaml: color_jitter_saturation_range` |
| Hue shift | [{CJ_HUE_RANGE[0]}, {CJ_HUE_RANGE[1]}] (fraction of colour circle) | `default.yaml: color_jitter_hue_range` |
| Distribution | Uniform (each component) | `augmentation_unified.py` (`_apply_color_jitter`) |
| Probability | {CJ_PROB} ({CJ_PROB * 100:.0f}%) per component, applied independently | `default.yaml: color_jitter_prob` |

## Algorithm

Each of the four components is sampled from its range and applied independently
with probability {CJ_PROB * 100:.0f}% (so a given image receives an arbitrary subset):

```python
# Brightness — scale RGB
if rand() < p: img = img * uniform(0.9, 1.1)
# Contrast — blend toward per-image grayscale mean
if rand() < p: img = (img - gray_mean) * uniform(0.9, 1.1) + gray_mean
# Saturation — blend toward per-pixel grayscale
if rand() < p: img = gray + uniform(0.9, 1.1) * (img - gray)
# Hue — rotate H channel in HSV by uniform(-0.02, 0.02) * 180
```

Replaces the previous PCA colour jitter. Bands are kept narrow so the
perturbation stays within plausible acquisition variation and does not
distort diagnostic lesion colour. Brightness/contrast operate in RGB;
saturation/hue operate in HSV.

## Demo images

- `left_min / right_min` — all factors at the low end (brightness/contrast/saturation = {CJ_BRIGHTNESS_RANGE[0]}, hue = {CJ_HUE_RANGE[0]})
- `left_max / right_max` — all factors at the high end (brightness/contrast/saturation = {CJ_BRIGHTNESS_RANGE[1]}, hue = +{CJ_HUE_RANGE[1]})
"""

ACQUISITION_MD = f"""# Acquisition Variability (Gaussian Noise + JPEG Compression)

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Gaussian noise σ | [{NOISE_SIGMA_RANGE[0]}, {NOISE_SIGMA_RANGE[1]}] (8-bit RGB) | `default.yaml: gaussian_noise_sigma_range` |
| Noise probability | {NOISE_PROB} ({NOISE_PROB * 100:.0f}%) | `default.yaml: gaussian_noise_prob` |
| JPEG quality | [{JPEG_QUALITY_RANGE[0]}, {JPEG_QUALITY_RANGE[1]}] | `default.yaml: jpeg_quality_range` |
| JPEG probability | {JPEG_PROB} ({JPEG_PROB * 100:.0f}%) | `default.yaml: jpeg_prob` |
| Distribution | Uniform (both) | `augmentation_unified.py` (`_apply_gaussian_noise`, `_apply_jpeg_compression`) |

## Algorithm

Two independent degradations that simulate real acquisition/storage:

```python
# Gaussian noise (sensor / acquisition noise)
if rand() < {NOISE_PROB}:
    sigma = uniform({NOISE_SIGMA_RANGE[0]}, {NOISE_SIGMA_RANGE[1]})
    img = clip(img + normal(0, sigma), 0, 255)

# JPEG re-compression (storage block / chroma artifacts)
if rand() < {JPEG_PROB}:
    quality = randint({JPEG_QUALITY_RANGE[0]}, {JPEG_QUALITY_RANGE[1]})
    img = jpeg_decode(jpeg_encode(img, quality))
```

Both probabilities are kept low: the goal is to expose the network to
occasional degraded examples, not to train predominantly on corrupted data.

## Demo images

- `left_min / right_min` — light degradation (σ = {NOISE_SIGMA_RANGE[0]}, JPEG quality = {JPEG_QUALITY_RANGE[1]})
- `left_max / right_max` — heavy degradation (σ = {NOISE_SIGMA_RANGE[1]}, JPEG quality = {JPEG_QUALITY_RANGE[0]})
"""


def process_grade(gr):
    print(f"\n=== {gr} ===")
    aug_base = os.path.join(BASE, gr, "preprocessing", "stage_6_augmentation")

    for side in ["left", "right"]:
        img, mask = load_pair(gr, side)
        if img is None:
            print(f"  {side}: SKIP (not found)")
            continue

        # 1. Rotation — placeholder: copy source image (novelty documented separately)
        d = os.path.join(aug_base, "1_rotation")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}.png"), img)

        # 2. Scale
        d = os.path.join(aug_base, "2_scale")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}_min.png"), aug_scale(img, mask, ZOOM_RANGE[0]))
        cv2.imwrite(os.path.join(d, f"{side}_max.png"), aug_scale(img, mask, ZOOM_RANGE[1]))

        # 3. Shear
        d = os.path.join(aug_base, "3_shear")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}_min.png"), aug_shear(img, mask, SHEAR_RANGE[0]))
        cv2.imwrite(os.path.join(d, f"{side}_max.png"), aug_shear(img, mask, SHEAR_RANGE[1]))

        # 4. ColorJitter (all four components at the low / high end of their ranges)
        d = os.path.join(aug_base, "4_color_jitter")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}_min.png"),
                    aug_color_jitter(img, mask, CJ_BRIGHTNESS_RANGE[0], CJ_CONTRAST_RANGE[0],
                                     CJ_SATURATION_RANGE[0], CJ_HUE_RANGE[0]))
        cv2.imwrite(os.path.join(d, f"{side}_max.png"),
                    aug_color_jitter(img, mask, CJ_BRIGHTNESS_RANGE[1], CJ_CONTRAST_RANGE[1],
                                     CJ_SATURATION_RANGE[1], CJ_HUE_RANGE[1]))

        # 5. Acquisition variability (light / heavy degradation)
        d = os.path.join(aug_base, "5_acquisition_variability")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}_min.png"),
                    aug_acquisition(img, mask, NOISE_SIGMA_RANGE[0], JPEG_QUALITY_RANGE[1], seed=42))
        cv2.imwrite(os.path.join(d, f"{side}_max.png"),
                    aug_acquisition(img, mask, NOISE_SIGMA_RANGE[1], JPEG_QUALITY_RANGE[0], seed=42))

        print(f"  {side}: done")

    # Distribution plots + params.md (same for all grades)
    plots = [
        ("1_rotation", plot_rotation_dist),
        ("2_scale", plot_scale_dist),
        ("3_shear", plot_shear_dist),
        ("4_color_jitter", plot_color_jitter_dist),
        ("5_acquisition_variability", plot_acquisition_dist),
    ]
    for name, plot_fn in plots:
        d = os.path.join(aug_base, name)
        os.makedirs(d, exist_ok=True)
        plot_fn(os.path.join(d, "distribution.png"))

    params = {
        "1_rotation": ROTATION_MD,
        "2_scale": SCALE_MD,
        "3_shear": SHEAR_MD,
        "4_color_jitter": COLOR_JITTER_MD,
        "5_acquisition_variability": ACQUISITION_MD,
    }
    for name, content in params.items():
        with open(os.path.join(aug_base, name, "params.md"), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  distribution + params: done")


def run():
    grades = sys.argv[1:] if len(sys.argv) > 1 else GRADES
    for gr in grades:
        process_grade(gr)


if __name__ == "__main__":
    run()
