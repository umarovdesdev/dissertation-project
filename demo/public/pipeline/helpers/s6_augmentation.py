"""
Stage 6: Augmentation demo — isolated min/max for each augmentation type.
Parameters from experiments/configs/default.yaml and experiments/src/data/augmentation_v4.py.
Generates left_min/max, right_min/max, distribution.png, and params.md per type.
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

# === From experiments/configs/default.yaml (lines 54-70) ===
ROTATION_SIGMA = 13.0
ROTATION_CLIP = 40.0
ZOOM_RANGE = (0.9, 1.1)
STRETCH_RANGE = (1.0 / 1.05, 1.05)
SHEAR_RANGE = (-2.0, 2.0)
SHEAR_PROB = 0.3
PCA_SIGMA = 0.1
PCA_PROB = 0.5
ALPHA_RANGE = (0.9, 1.1)
BETA_RANGE = (-10.0, 10.0)
BC_PROB = 0.5
BORDER_MODE = cv2.BORDER_REFLECT


def load_pair(gr, side):
    img = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png"))
    mask = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"), cv2.IMREAD_GRAYSCALE)
    return img, mask


def masked(img, mask):
    return img * np.expand_dims(mask > 0, axis=-1).astype(np.uint8)


# === Geometric augmentations (matching augmentation_v4.py) ===

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


# === Color augmentations ===

def compute_pca_from_demo():
    np.random.seed(42)
    pixels = []
    for gr in GRADES:
        for side in ["left", "right"]:
            img = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png"))
            mask_img = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"), cv2.IMREAD_GRAYSCALE)
            if img is None or mask_img is None:
                continue
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
            ys, xs = np.where(mask_img > 0)
            if len(ys) > 1000:
                idx = np.random.choice(len(ys), 1000, replace=False)
                ys, xs = ys[idx], xs[idx]
            pixels.append(rgb[ys, xs])
    all_px = np.vstack(pixels)
    centered = all_px - all_px.mean(axis=0)
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    idx = np.argsort(eigvals)[::-1]
    return eigvecs[:, idx], eigvals[idx]


def aug_pca_color(img, mask, alpha_vec, eigvecs, eigvals):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    noise = eigvecs @ (alpha_vec * eigvals)
    rgb = np.clip(rgb + noise, 0, 255).astype(np.uint8)
    out = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return masked(out, mask)


def aug_brightness_contrast(img, mask, alpha, beta):
    out = np.clip(img.astype(np.float32) * alpha + beta, 0, 255).astype(np.uint8)
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


def plot_pca_dist(path):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.linspace(-0.5, 0.5, 1000)
    pdf = np.exp(-x**2 / (2 * PCA_SIGMA**2)) / (PCA_SIGMA * np.sqrt(2 * np.pi))
    ax.fill_between(x, pdf, alpha=0.3, color='purple')
    ax.plot(x, pdf, color='purple', lw=2)
    ax.axvline(-3 * PCA_SIGMA, color='red', ls=':', lw=1, label=f'±3σ = ±{3 * PCA_SIGMA}')
    ax.axvline(3 * PCA_SIGMA, color='red', ls=':', lw=1)
    ax.set_xlabel('α (per-component noise)')
    ax.set_ylabel('Probability density')
    ax.set_title(f'Gaussian (σ={PCA_SIGMA}), P(apply)={PCA_PROB}')
    ax.legend()
    ax.set_xlim(-0.5, 0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def plot_bc_dist(path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
    x1 = np.linspace(0.8, 1.2, 1000)
    w1 = ALPHA_RANGE[1] - ALPHA_RANGE[0]
    pdf1 = np.where((x1 >= ALPHA_RANGE[0]) & (x1 <= ALPHA_RANGE[1]), 1.0 / w1, 0)
    ax1.fill_between(x1, pdf1, alpha=0.3, color='teal')
    ax1.plot(x1, pdf1, color='teal', lw=2)
    ax1.set_xlabel('α (contrast multiplier)')
    ax1.set_ylabel('Probability density')
    ax1.set_title(f'Contrast: Uniform [{ALPHA_RANGE[0]}, {ALPHA_RANGE[1]}]')

    x2 = np.linspace(-15, 15, 1000)
    w2 = BETA_RANGE[1] - BETA_RANGE[0]
    pdf2 = np.where((x2 >= BETA_RANGE[0]) & (x2 <= BETA_RANGE[1]), 1.0 / w2, 0)
    ax2.fill_between(x2, pdf2, alpha=0.3, color='coral')
    ax2.plot(x2, pdf2, color='coral', lw=2)
    ax2.set_xlabel('β (brightness offset, uint8)')
    ax2.set_ylabel('Probability density')
    ax2.set_title(f'Brightness: Uniform [{BETA_RANGE[0]}, {BETA_RANGE[1]}]')

    fig.suptitle(f'P(apply) = {BC_PROB}', fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


# === Params.md content ===

ROTATION_MD = f"""# Rotation Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Distribution | Truncated Gaussian | `augmentation_v4.py:147-148` |
| σ (sigma) | {ROTATION_SIGMA}° | `default.yaml:54` |
| Clip boundary | ±{ROTATION_CLIP}° | `default.yaml:55` |
| Adaptive sigma | Enabled | `default.yaml:32` |
| Fallback sigma | {ROTATION_SIGMA}° | `default.yaml:33` |
| Probability | 100% (always applied) | — |
| Interpolation | Stochastic: 60% linear, 30% cubic, 10% nearest | `default.yaml:60` |
| Border mode | BORDER_REFLECT | `default.yaml:61` |

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
| Zoom range | [{ZOOM_RANGE[0]}, {ZOOM_RANGE[1]}] | `default.yaml:56` |
| Zoom distribution | Log-uniform | `augmentation_v4.py:151-155` |
| Stretch range | [{STRETCH_RANGE[0]:.6f}, {STRETCH_RANGE[1]}] (= [1/1.05, 1.05]) | `default.yaml:57` |
| Stretch distribution | Log-uniform | `augmentation_v4.py:159-163` |
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
| Shear range | [{SHEAR_RANGE[0]}°, {SHEAR_RANGE[1]}°] | `default.yaml:58` |
| Distribution | Uniform | `augmentation_v4.py:172` |
| Probability | {SHEAR_PROB} ({SHEAR_PROB * 100:.0f}%) | `default.yaml:59` |

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

BC_MD = f"""# Brightness / Contrast Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Contrast (α) range | [{ALPHA_RANGE[0]}, {ALPHA_RANGE[1]}] | `default.yaml:63` |
| Brightness (β) range | [{BETA_RANGE[0]}, {BETA_RANGE[1]}] | `default.yaml:64` |
| Distribution | Uniform (both) | `augmentation_v4.py:290-291` |
| Probability | {BC_PROB} ({BC_PROB * 100:.0f}%) | `default.yaml:65` |

## Algorithm

Simple linear transform applied with probability {BC_PROB * 100:.0f}%:

```python
alpha = np.random.uniform({ALPHA_RANGE[0]}, {ALPHA_RANGE[1]})   # contrast
beta = np.random.uniform({BETA_RANGE[0]}, {BETA_RANGE[1]})    # brightness (uint8)
pixel_out = pixel_in * alpha + beta
```

- α < 1 reduces contrast, α > 1 increases contrast
- β < 0 darkens, β > 0 brightens

Applied after CLAHE — these are small perturbations around already-normalized contrast.
Makes the model robust to inter-device brightness/contrast differences.

## Demo images

- `left_min / right_min` — α={ALPHA_RANGE[0]}, β={BETA_RANGE[0]} (darker, less contrast)
- `left_max / right_max` — α={ALPHA_RANGE[1]}, β={BETA_RANGE[1]} (brighter, more contrast)
"""


def pca_params_md(eigvecs, eigvals):
    return f"""# PCA Color Jitter

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| σ (sigma) | {PCA_SIGMA} | `default.yaml:62` |
| Distribution | Gaussian per component | `augmentation_v4.py:272` |
| Probability | {PCA_PROB} ({PCA_PROB * 100:.0f}%) | `default.yaml:63` |
| Components | 3 (RGB PCA) | — |

## Algorithm

PCA color jitter (AlexNet-style) applied with probability {PCA_PROB * 100:.0f}%:

```python
alpha = np.random.normal(0.0, {PCA_SIGMA}, size=3)
noise = eigvecs @ (alpha * eigvals)
pixel_out = pixel_in + noise   # per-channel additive shift
```

Adds noise along principal color axes of the training dataset.
Simulates natural illumination variations while preserving fundus color structure.

## PCA Eigenvalues

```
[{eigvals[0]:.4f}, {eigvals[1]:.4f}, {eigvals[2]:.4f}]
```

## PCA Eigenvectors

```
[{eigvecs[0, 0]:+.4f}, {eigvecs[0, 1]:+.4f}, {eigvecs[0, 2]:+.4f}]
[{eigvecs[1, 0]:+.4f}, {eigvecs[1, 1]:+.4f}, {eigvecs[1, 2]:+.4f}]
[{eigvecs[2, 0]:+.4f}, {eigvecs[2, 1]:+.4f}, {eigvecs[2, 2]:+.4f}]
```

Note: PCA computed from demo fundus images (10 images, 1000 pixels each).
In production, PCA is computed from the full EyePACS training set
(5000 images × 1000 pixels, see `experiments/scripts/compute_pca_eigvecs.py`).

## Demo images

- `left_min / right_min` — α = [-σ, -σ, -σ] = [{-PCA_SIGMA}, {-PCA_SIGMA}, {-PCA_SIGMA}] (1σ negative shift)
- `left_max / right_max` — α = [+σ, +σ, +σ] = [+{PCA_SIGMA}, +{PCA_SIGMA}, +{PCA_SIGMA}] (1σ positive shift)
"""


def process_grade(gr, eigvecs, eigvals):
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

        # 4. PCA color jitter (±1σ matching production augmentation_v4.py)
        d = os.path.join(aug_base, "4_pca_color_jitter")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}_min.png"),
                    aug_pca_color(img, mask, np.full(3, -PCA_SIGMA), eigvecs, eigvals))
        cv2.imwrite(os.path.join(d, f"{side}_max.png"),
                    aug_pca_color(img, mask, np.full(3, PCA_SIGMA), eigvecs, eigvals))

        # 5. Brightness/contrast
        d = os.path.join(aug_base, "5_brightness_contrast")
        os.makedirs(d, exist_ok=True)
        cv2.imwrite(os.path.join(d, f"{side}_min.png"),
                    aug_brightness_contrast(img, mask, ALPHA_RANGE[0], BETA_RANGE[0]))
        cv2.imwrite(os.path.join(d, f"{side}_max.png"),
                    aug_brightness_contrast(img, mask, ALPHA_RANGE[1], BETA_RANGE[1]))

        print(f"  {side}: done")

    # Distribution plots + params.md (same for all grades)
    plots = [
        ("1_rotation", plot_rotation_dist),
        ("2_scale", plot_scale_dist),
        ("3_shear", plot_shear_dist),
        ("4_pca_color_jitter", plot_pca_dist),
        ("5_brightness_contrast", plot_bc_dist),
    ]
    for name, plot_fn in plots:
        d = os.path.join(aug_base, name)
        os.makedirs(d, exist_ok=True)
        plot_fn(os.path.join(d, "distribution.png"))

    params = {
        "1_rotation": ROTATION_MD,
        "2_scale": SCALE_MD,
        "3_shear": SHEAR_MD,
        "4_pca_color_jitter": pca_params_md(eigvecs, eigvals),
        "5_brightness_contrast": BC_MD,
    }
    for name, content in params.items():
        with open(os.path.join(aug_base, name, "params.md"), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  distribution + params: done")


def run():
    print("Computing PCA from demo images...")
    eigvecs, eigvals = compute_pca_from_demo()
    print(f"PCA eigenvalues: {eigvals}")

    grades = sys.argv[1:] if len(sys.argv) > 1 else GRADES
    for gr in grades:
        process_grade(gr, eigvecs, eigvals)


if __name__ == "__main__":
    run()
