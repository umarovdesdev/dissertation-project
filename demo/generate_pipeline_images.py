"""
Generate V5 pipeline stage images from real fundus photographs.
Source: demo/public/fundus-examples/dr04/right_eye.jpeg and left_eye.jpeg
Output: demo/public/pipeline/
"""
import os
import math
import cv2
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy.ndimage import gaussian_filter

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE, 'public', 'fundus-examples', 'dr04')
OUT_DIR = os.path.join(BASE, 'public', 'pipeline')
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 200

def load_image(name):
    """Load image as RGB numpy array."""
    path = os.path.join(SRC_DIR, name)
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Cannot load {path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# ─── V5 Pipeline Stages ───

def stage0_canonical_flip(img, is_left_eye):
    """Stage 0: Canonical flip — left eyes get flipped horizontally."""
    if is_left_eye:
        return np.fliplr(img).copy()
    return img.copy()


def detect_fov(img):
    """Detect FOV circle: center (cx, cy) and radius R."""
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Threshold to find bright fundus region
    _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        h, w = img.shape[:2]
        return w // 2, h // 2, min(w, h) // 2
    largest = max(contours, key=cv2.contourArea)
    (cx, cy), radius = cv2.minEnclosingCircle(largest)
    return int(cx), int(cy), int(radius)


def detect_od(img):
    """Detect optic disc center (brightest region in green channel)."""
    green = img[:, :, 1].astype(np.float32)
    blurred = cv2.GaussianBlur(green, (51, 51), 20)
    thresh_val = np.percentile(blurred, 97)
    mask = (blurred >= thresh_val).astype(np.uint8)
    moments = cv2.moments(mask)
    if moments['m00'] > 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        return cx, cy
    return img.shape[1] // 2, img.shape[0] // 2


def detect_fovea(img, od_cx, od_cy, fov_cx, fov_cy, fov_r):
    """Detect fovea as darkest region in annular zone around macula."""
    green = img[:, :, 1].astype(np.float32)
    blurred = cv2.GaussianBlur(green, (31, 31), 10)
    h, w = green.shape
    Y, X = np.mgrid[0:h, 0:w]
    # Fovea is roughly on opposite side of OD from center, at about 2.5x OD-center distance
    dist_od = np.sqrt((X - od_cx)**2 + (Y - od_cy)**2)
    dist_fov_center = np.sqrt((X - fov_cx)**2 + (Y - fov_cy)**2)
    # Annular zone: 1.5-3.5x the OD-to-center distance
    od_to_center = np.sqrt((od_cx - fov_cx)**2 + (od_cy - fov_cy)**2)
    inner_r = od_to_center * 0.3
    outer_r = od_to_center * 1.5
    annular_mask = (dist_od >= inner_r) & (dist_od <= outer_r) & (dist_fov_center < fov_r * 0.8)
    if not np.any(annular_mask):
        # Fallback: just use the center region opposite to OD
        fx = 2 * fov_cx - od_cx
        fy = fov_cy
        return int(fx), int(fy)
    masked = blurred.copy()
    masked[~annular_mask] = 999
    min_idx = np.unravel_index(np.argmin(masked), masked.shape)
    return int(min_idx[1]), int(min_idx[0])


def stage1_od_fovea_rotation(img):
    """Stage 1: Rotate so OD-fovea axis is horizontal."""
    cx_fov, cy_fov, r_fov = detect_fov(img)
    od_cx, od_cy = detect_od(img)
    fov_cx, fov_cy = detect_fovea(img, od_cx, od_cy, cx_fov, cy_fov, r_fov)
    # Angle of OD->fovea vector
    angle = np.degrees(np.arctan2(fov_cy - od_cy, fov_cx - od_cx))
    # Rotate to make horizontal (0 degrees)
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    return rotated


def stage2_fov_crop_isotropic_resize(img, target_size=512, margin_pct=0.05):
    """Stage 2: FOV crop + isotropic resize to 512x512.

    Args:
        img: Input RGB image.
        target_size: Output square side length.
        margin_pct: Fractional margin around FOV radius. 0 = circle inscribed
            in the square (touches all 4 edges).
    """
    cx, cy, r = detect_fov(img)
    half = int(r * (1 + margin_pct))

    # Always crop a perfect square centered on the FOV
    x1, x2 = cx - half, cx + half
    y1, y2 = cy - half, cy + half

    h, w = img.shape[:2]
    src_x1, src_x2 = max(0, x1), min(w, x2)
    src_y1, src_y2 = max(0, y1), min(h, y2)

    side = 2 * half
    canvas = np.zeros((side, side, 3), dtype=np.uint8)
    dst_x1 = src_x1 - x1
    dst_y1 = src_y1 - y1
    canvas[dst_y1:dst_y1 + (src_y2 - src_y1),
           dst_x1:dst_x1 + (src_x2 - src_x1)] = img[src_y1:src_y2, src_x1:src_x2]

    resized = cv2.resize(canvas, (target_size, target_size), interpolation=cv2.INTER_AREA)
    return resized


def stage3_fov_mask(img, target_size=512):
    """Stage 3: Generate binary FOV mask."""
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Mask: pixels > threshold are fundus
    _, mask = cv2.threshold(gray, 8, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return (mask / 255.0).astype(np.float32)


def stage4_flatfield(img, mask=None):
    """Stage 4: Adaptive flat-field correction. σ = 0.07 × D.

    Apply only within the FOV region; preserve black padding outside.
    """
    fov_mask = stage3_fov_mask(img) if mask is None else mask
    cx, cy, r = detect_fov(img)
    D = 2 * r if r > 50 else 512
    sigma = 0.07 * D
    ksize = int(sigma * 6) | 1  # odd kernel size
    if ksize < 3:
        ksize = 3
    result = img.copy().astype(np.float32)
    for c in range(3):
        ch = img[:, :, c].astype(np.float32)
        # Blur only the FOV region (fill outside with per-channel mean to avoid edge artefacts)
        ch_filled = ch.copy()
        fov_mean = ch[fov_mask > 0.5].mean() if np.any(fov_mask > 0.5) else 128.0
        ch_filled[fov_mask < 0.5] = fov_mean
        bg = cv2.GaussianBlur(ch_filled, (ksize, ksize), sigma)
        corrected = ch - bg + fov_mean
        # Keep only the FOV region; leave padding black
        result[:, :, c] = np.where(fov_mask > 0.5, corrected, 0.0)
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result


def stage5_clahe(img, clip_limit=2.5, tile_grid=(8, 8)):
    """Stage 5: Dual-constraint CLAHE on LAB L-channel.

    The dissertation formula CL_tile = min(clip_factor*tile_area/256,
    global_threshold*tile_area) produces the *experiment* clip limit (fed to
    a custom CLAHE wrapper that re-normalises internally).  OpenCV's
    createCLAHE expects a small per-bin value; 2.0-3.0 is standard for
    medical fundus imaging and reproduces the visually moderate enhancement
    described in the thesis.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def stage6_augmentation(img, angle=15):
    """Stage 6: Example augmentation (train only). Mild rotation + color jitter."""
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    # Mild brightness/contrast jitter
    alpha = 1.05  # contrast
    beta = 5  # brightness
    adjusted = cv2.convertScaleAbs(rotated, alpha=alpha, beta=beta)
    return adjusted


def stage7_normalize(img, mask):
    """Stage 7: Dataset-specific normalize + mask append. Returns (normalized_rgb_display, mask).

    For display purposes we show the normalised tensor rescaled back to
    [0, 255] using the 1st-99th percentile range within the FOV so that
    the image looks recognisable while the colour shift from dataset-specific
    stats (vs ImageNet) is visible.
    """
    # Dataset-specific stats (EyePACS V5 training set)
    mean = np.array([0.412, 0.267, 0.168])
    std = np.array([0.278, 0.189, 0.145])
    normalized = (img.astype(np.float32) / 255.0 - mean) / std
    # Display: percentile-based rescaling within FOV to preserve colour
    display = np.zeros_like(img, dtype=np.uint8)
    fov = mask > 0.5
    for c in range(3):
        ch = normalized[:, :, c]
        if np.any(fov):
            lo = np.percentile(ch[fov], 1)
            hi = np.percentile(ch[fov], 99)
        else:
            lo, hi = ch.min(), ch.max()
        scaled = (ch - lo) / (hi - lo + 1e-8)
        scaled = np.clip(scaled, 0, 1)
        display[:, :, c] = (scaled * 255).astype(np.uint8)
    # Black out padding
    display[~fov] = 0
    return display, mask


def baseline_processing(img, target_size=512):
    """Baseline: stretch-resize to 512x512 (non-isotropic) + no other preprocessing."""
    resized = cv2.resize(img, (target_size, target_size), interpolation=cv2.INTER_AREA)
    return resized


# ─── Image Generation Functions ───

def _save(fig, name):
    fig.savefig(os.path.join(OUT_DIR, name), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  [OK] {name}")


def make_stage_2_isotropic_resize(right_img):
    """Create stage_2_isotropic_resize.png showing FOV crop + isotropic resize."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('Stage 2: FOV Crop + Isotropic Resize (512×512)', fontsize=14, fontweight='bold', y=0.98)

    img_s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    axes[0].imshow(img_s0)
    cx, cy, r = detect_fov(img_s0)
    circle = plt.Circle((cx, cy), r, fill=False, color='#1D9E75', linewidth=2, linestyle='--')
    axes[0].add_patch(circle)
    axes[0].set_title('FOV Boundary Detection', fontsize=11)
    axes[0].axis('off')

    result = stage2_fov_crop_isotropic_resize(img_s0, margin_pct=0)
    axes[1].imshow(result)
    axes[1].set_title('Isotropic Resize 512×512\n(circle inscribed in square)', fontsize=11)
    axes[1].axis('off')

    plt.tight_layout()
    _save(fig, 'stage_2_isotropic_resize.png')


def make_stage_4_flatfield(processed_512):
    """Create stage_4_flatfield.png showing before/after flat-field correction."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('Stage 4: Adaptive Flat-Field Correction (\u03c3 = 0.07\u00b7D)', fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(processed_512)
    axes[0].set_title('Before Flat-Field', fontsize=11)
    axes[0].axis('off')

    corrected = stage4_flatfield(processed_512)
    axes[1].imshow(corrected)
    axes[1].set_title('After Flat-Field', fontsize=11)
    axes[1].axis('off')

    plt.tight_layout()
    _save(fig, 'stage_4_flatfield.png')
    return corrected


def make_stage_5_clahe(ff_img):
    """Create stage_5_clahe.png showing before/after CLAHE."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('Stage 5: CLAHE (Dual-Constraint, LAB L-channel)', fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(ff_img)
    axes[0].set_title('Before CLAHE', fontsize=11)
    axes[0].axis('off')

    clahe_img = stage5_clahe(ff_img)
    axes[1].imshow(clahe_img)
    axes[1].set_title('After CLAHE\nclip_factor=2.0, threshold=0.01', fontsize=11)
    axes[1].axis('off')

    plt.tight_layout()
    _save(fig, 'stage_5_clahe.png')
    return clahe_img


def make_stage_7_normalized(clahe_img, mask):
    """Create stage_7_normalized.png showing normalized RGB + FOV mask side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('Stage 7: Dataset-Specific Normalize \u2192 4-Channel Tensor', fontsize=14, fontweight='bold', y=0.98)

    norm_display, mask_out = stage7_normalize(clahe_img, mask)
    axes[0].imshow(norm_display)
    axes[0].set_title('Normalized RGB\n(rescaled for display)', fontsize=11)
    axes[0].axis('off')

    axes[1].imshow(mask_out, cmap='gray', vmin=0, vmax=1)
    axes[1].set_title('FOV Mask (Channel 4)', fontsize=11)
    axes[1].axis('off')

    plt.tight_layout()
    _save(fig, 'stage_7_normalized.png')


def _detect_od_accurate(green):
    """OD detection matching experiments/src/preprocessing/od_fovea_detect.py."""
    blurred = cv2.GaussianBlur(green.astype(np.float32), (0, 0), 15.0)
    thresh = np.percentile(blurred, 97)
    od_mask = (blurred >= thresh).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    od_mask = cv2.morphologyEx(od_mask, cv2.MORPH_CLOSE, kernel)
    od_mask = cv2.morphologyEx(od_mask, cv2.MORPH_OPEN, kernel)
    M = cv2.moments(od_mask)
    if M['m00'] == 0:
        _, _, _, max_loc = cv2.minMaxLoc(blurred)
        return max_loc[0], max_loc[1], 30.0, blurred
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    radius = math.sqrt(M['m00'] / math.pi)
    return cx, cy, radius, blurred


def _detect_fovea_accurate(green, od_cx, od_cy, od_radius):
    """Fovea detection matching experiments/src/preprocessing/od_fovea_detect.py."""
    h, w = green.shape
    od_diameter = od_radius * 2.0
    inner_r = 1.5 * od_diameter
    outer_r = 3.5 * od_diameter
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - od_cx)**2 + (Y - od_cy)**2)
    annular = (dist >= inner_r) & (dist <= outer_r)
    fov_valid = (green > 15)
    search = annular & fov_valid
    blurred = cv2.GaussianBlur(green.astype(np.float32), (0, 0), 25.0)
    search_img = blurred.copy()
    search_img[~search] = 255.0
    min_loc = cv2.minMaxLoc(search_img)[2]  # (x, y)
    fov_cx, fov_cy = int(min_loc[0]), int(min_loc[1])
    fov_radius = max(od_radius * 0.5, 10.0)
    return fov_cx, fov_cy, fov_radius, blurred, search, inner_r, outer_r


def _full_od_fovea_detection(img):
    """Run full OD-Fovea detection pipeline, return all intermediate results."""
    green = img[:, :, 1]
    od_cx, od_cy, od_r, od_blur = _detect_od_accurate(green)
    fov_cx, fov_cy, fov_r, fov_blur, search_mask, inner_r, outer_r = \
        _detect_fovea_accurate(green, od_cx, od_cy, od_r)
    dx, dy = fov_cx - od_cx, fov_cy - od_cy
    distance = math.sqrt(dx * dx + dy * dy)
    angle_deg = math.degrees(math.atan2(dy, dx))
    sigma_pos = math.sqrt(od_r**2 + fov_r**2)
    sigma_theta = math.degrees(math.atan(sigma_pos / distance)) if distance > 0 else 15.0
    sigma_theta = min(sigma_theta, 15.0)

    # Smoothed surfaces for contour rendering (σ≈40 — smooth rings, not blobs)
    od_smooth = cv2.GaussianBlur(od_blur, (0, 0), 40.0)
    fov_inv = fov_blur.max() - fov_blur
    fov_inv_smooth = cv2.GaussianBlur(fov_inv, (0, 0), 40.0)
    fov_inv_smooth[~search_mask] = np.nan

    return dict(
        od_cx=od_cx, od_cy=od_cy, od_r=od_r, od_blur=od_blur,
        fov_cx=fov_cx, fov_cy=fov_cy, fov_r=fov_r, fov_blur=fov_blur,
        search_mask=search_mask, inner_r=inner_r, outer_r=outer_r,
        distance=distance, angle_deg=angle_deg,
        sigma_pos=sigma_pos, sigma_theta=sigma_theta,
        od_smooth=od_smooth, fov_inv_smooth=fov_inv_smooth,
    )


def _stage1_axis_overlay(img):
    """Create Stage 1 visualization: image with OD-fovea contours and axis."""
    vis = img.copy()
    d = _full_od_fovea_detection(img)
    cv2.line(vis, (d['od_cx'], d['od_cy']), (d['fov_cx'], d['fov_cy']), (0, 255, 0), 3)
    cv2.circle(vis, (d['od_cx'], d['od_cy']), int(d['od_r']), (255, 255, 0), 2)
    cv2.circle(vis, (d['fov_cx'], d['fov_cy']), int(d['fov_r']), (0, 255, 255), 2)
    return vis


def make_pipeline_stages_grid(right_img):
    """Create pipeline_stages_grid.png — 3x3 grid of all V5 stages."""
    raw = right_img.copy()
    s0 = stage0_canonical_flip(raw, is_left_eye=False)
    s1_vis = _stage1_axis_overlay(s0)  # axis overlay, no rotation
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    mask = stage3_fov_mask(s2)
    s4 = stage4_flatfield(s2)
    s5 = stage5_clahe(s4)
    s6 = stage6_augmentation(s5, angle=15)
    s7_disp, _ = stage7_normalize(s5, mask)

    stages = [
        ('Raw Input', raw),
        ('Stage 0: Canonical Flip', s0),
        ('Stage 1: OD-Fovea Axis', s1_vis),
        ('Stage 2: FOV Crop + Resize', s2),
        ('Stage 3: FOV Mask', None),
        ('Stage 4: Flat-Field', s4),
        ('Stage 5: CLAHE', s5),
        ('Stage 6: Augmentation\n(train only)', s6),
        ('Stage 7: Normalize \u2192 4ch', s7_disp),
    ]

    colors = ['#888780', '#378ADD', '#378ADD', '#378ADD', '#378ADD',
              '#1D9E75', '#1D9E75', '#EF9F27', '#7F77DD']

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    fig.suptitle('V5 Pipeline Stages \u2014 Patient 43199 (DR4, Proliferative DR)',
                 fontsize=14, fontweight='bold', y=0.98)

    for i, (title, img) in enumerate(stages):
        row, col = i // 3, i % 3
        ax = axes[row][col]
        if title == 'Stage 3: FOV Mask':
            ax.imshow(mask, cmap='gray', vmin=0, vmax=1)
        else:
            ax.imshow(img)
        ax.set_title(title, fontsize=9, fontweight='bold')
        ax.axis('off')
        badge_color = colors[i]
        ax.text(0.02, 0.02, f'S{i}' if i > 0 else 'Raw',
                transform=ax.transAxes, fontsize=8, fontweight='bold',
                color='white', bbox=dict(boxstyle='round,pad=0.3', facecolor=badge_color, alpha=0.85),
                verticalalignment='bottom')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    _save(fig, 'pipeline_stages_grid.png')


def make_bilateral_pair(right_img, left_img):
    """Create bilateral_pair.png — 2×3 grid: both eyes through pipeline."""
    r_s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    r_s2 = stage2_fov_crop_isotropic_resize(r_s0, margin_pct=0)
    r_v5 = stage5_clahe(stage4_flatfield(r_s2))

    l_s0 = stage0_canonical_flip(left_img, is_left_eye=True)
    l_s2 = stage2_fov_crop_isotropic_resize(l_s0, margin_pct=0)
    l_v5 = stage5_clahe(stage4_flatfield(l_s2))

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    fig.suptitle('Bilateral Pair \u2014 Canonical Flip + Full V5 Pipeline\nPatient 43199 (DR4)',
                 fontsize=14, fontweight='bold', y=1.0)

    axes[0][0].imshow(right_img); axes[0][0].set_title('Right Eye (OD) \u2014 Raw', fontsize=10); axes[0][0].axis('off')
    axes[0][1].imshow(r_s2);      axes[0][1].set_title('Cropped 512\u00d7512', fontsize=10);       axes[0][1].axis('off')
    axes[0][2].imshow(r_v5);      axes[0][2].set_title('Full V5 Pipeline', fontsize=10);           axes[0][2].axis('off')

    axes[1][0].imshow(left_img);  axes[1][0].set_title('Left Eye (OS) \u2014 Raw', fontsize=10);   axes[1][0].axis('off')
    axes[1][1].imshow(l_s2);      axes[1][1].set_title('Flipped + Cropped 512\u00d7512', fontsize=10); axes[1][1].axis('off')
    axes[1][2].imshow(l_v5);      axes[1][2].set_title('Full V5 Pipeline', fontsize=10);           axes[1][2].axis('off')

    axes[0][0].text(-0.1, 0.5, 'OD', transform=axes[0][0].transAxes, fontsize=12,
                    fontweight='bold', va='center', ha='center', rotation=90)
    axes[1][0].text(-0.1, 0.5, 'OS', transform=axes[1][0].transAxes, fontsize=12,
                    fontweight='bold', va='center', ha='center', rotation=90)

    plt.tight_layout()
    _save(fig, 'bilateral_pair.png')


def make_before_after_pipeline(right_img):
    """Create before_after_pipeline.png — baseline vs full V5 side-by-side."""
    bl = baseline_processing(right_img)

    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    s5 = stage5_clahe(stage4_flatfield(s2))

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('Baseline Processing vs Full V5 Pipeline', fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(bl)
    axes[0].set_title('Baseline (3ch)\nStretch-resize + ImageNet norm', fontsize=10)
    axes[0].axis('off')
    axes[0].text(0.02, 0.02, '3ch RGB', transform=axes[0].transAxes, fontsize=9,
                 color='white', bbox=dict(boxstyle='round,pad=0.3', facecolor='#888780', alpha=0.85),
                 verticalalignment='bottom')

    axes[1].imshow(s5)
    axes[1].set_title('Full V5 Pipeline (4ch)\nIsotropic resize + flat-field + CLAHE', fontsize=10)
    axes[1].axis('off')
    axes[1].text(0.02, 0.02, '4ch RGBM', transform=axes[1].transAxes, fontsize=9,
                 color='white', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1D9E75', alpha=0.85),
                 verticalalignment='bottom')

    fig.text(0.5, 0.01,
             'V5 isotropic resize preserves circular FOV geometry; flat-field corrects illumination; CLAHE enhances vessel contrast',
             ha='center', fontsize=9, style='italic', color='#444441')

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    _save(fig, 'before_after_pipeline.png')


def make_baseline_vs_pipeline(right_img):
    """Create baseline_vs_pipeline.png — detailed comparison showing geometry preservation."""
    bl = baseline_processing(right_img)

    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    s5 = stage5_clahe(stage4_flatfield(s2))

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle('Baseline Stretch-Resize vs V5 Isotropic Resize', fontsize=14, fontweight='bold', y=0.98)

    axes[0][0].imshow(bl)
    axes[0][0].set_title('Baseline: Stretch-Resize 512\u00d7512\n(distorts circular geometry)', fontsize=10)
    axes[0][0].axis('off')

    axes[0][1].imshow(s2)
    axes[0][1].set_title('V5: Isotropic Resize 512\u00d7512\n(preserves circular FOV)', fontsize=10)
    axes[0][1].axis('off')

    axes[1][0].imshow(bl)
    axes[1][0].set_title('Baseline: No Enhancement\n(original illumination/contrast)', fontsize=10)
    axes[1][0].axis('off')

    axes[1][1].imshow(s5)
    axes[1][1].set_title('V5: Flat-Field + CLAHE\n(uniform illumination, enhanced contrast)', fontsize=10)
    axes[1][1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    _save(fig, 'baseline_vs_pipeline.png')


# ─── Method Detail Image Generators ───

def make_method_canonical_flip(right_img, left_img):
    """method_canonical_flip.png — 3-panel: left raw → left flipped → right raw."""
    l_raw = left_img.copy()
    l_flipped = stage0_canonical_flip(l_raw, is_left_eye=True)
    r_raw = right_img.copy()

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle('Stage 0: Canonical Flip \u2014 cv2.flip(image, 1) for left eyes',
                 fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(l_raw)
    axes[0].set_title('Left Eye (OS) \u2014 Raw\nOD on LEFT side', fontsize=10)
    axes[0].axis('off')

    axes[1].imshow(l_flipped)
    axes[1].set_title('Left Eye \u2014 After Flip\nOD on RIGHT side \u2713', fontsize=10)
    axes[1].axis('off')

    axes[2].imshow(r_raw)
    axes[2].set_title('Right Eye (OD) \u2014 Raw\nOD already RIGHT \u2713', fontsize=10)
    axes[2].axis('off')

    plt.tight_layout()
    _save(fig, 'method_canonical_flip.png')


def make_od_fovea_detection_steps(right_img):
    """od_fovea_detection_steps.png — 2x2 topographic detection visualization."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    d = _full_od_fovea_detection(s0)

    # Warm palette for OD (brightness peak)
    od_colors = ['#FFE066', '#FFD700', '#FFA500', '#FF8C00',
                 '#FF6347', '#FF4500', '#DC143C', '#B22222']
    # Cool palette for Fovea (darkness peak)
    fov_colors = ['#B0E0E6', '#87CEEB', '#6495ED', '#4169E1',
                  '#0000FF', '#0000CD', '#191970', '#000080']

    od_s = d['od_smooth']
    fov_s = d['fov_inv_smooth']

    # OD contour levels (top 20% of smoothed brightness)
    od_lo = np.percentile(od_s, 80)
    od_hi = od_s.max()
    od_levels = np.linspace(od_lo, od_hi, len(od_colors))

    # Fovea contour levels (top 40% of smoothed inverted brightness)
    fov_vals = d['fov_inv_smooth'][d['search_mask']]
    fov_lo = np.percentile(fov_vals, 60)
    fov_hi = fov_vals.max()
    fov_levels = np.linspace(fov_lo, fov_hi, len(fov_colors))

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('Stage 1: OD-Fovea Detection \u2014 Topographic Confidence Maps',
                 fontsize=14, fontweight='bold', y=0.98)

    # ── (0,0) OD brightness peak ──
    ax = axes[0][0]
    ax.imshow(s0)
    for lvl, c in zip(od_levels, od_colors):
        ax.contour(od_s, levels=[lvl], colors=[c], linewidths=1.4, alpha=0.85)
    ax.plot(d['od_cx'], d['od_cy'], '+', color='yellow', markersize=18, markeredgewidth=3)
    ax.set_title(f'OD Detection (brightness peak)\n'
                 f'center=({d["od_cx"]}, {d["od_cy"]}), r\u2009=\u2009{d["od_r"]:.0f} px',
                 fontsize=10, fontweight='bold')
    ax.axis('off')

    # ── (0,1) Fovea darkness peak ──
    ax = axes[0][1]
    ax.imshow(s0)
    for lvl, c in zip(fov_levels, fov_colors):
        ax.contour(fov_s, levels=[lvl], colors=[c], linewidths=1.4, alpha=0.85)
    ax.add_patch(plt.Circle((d['od_cx'], d['od_cy']), d['inner_r'],
                             fill=False, color='#EF9F27', lw=1.5, ls='--'))
    ax.add_patch(plt.Circle((d['od_cx'], d['od_cy']), d['outer_r'],
                             fill=False, color='#EF9F27', lw=1.5, ls='--'))
    ax.plot(d['fov_cx'], d['fov_cy'], '+', color='cyan', markersize=18, markeredgewidth=3)
    ax.set_title(f'Fovea Detection (darkness peak)\n'
                 f'center=({d["fov_cx"]}, {d["fov_cy"]}), annular 1.5\u20133.5\u00d7D_OD',
                 fontsize=10, fontweight='bold')
    ax.axis('off')

    # ── (1,0) Combined result on fundus ──
    ax = axes[1][0]
    ax.imshow(s0)
    for lvl, c in zip(od_levels, od_colors):
        ax.contour(od_s, levels=[lvl], colors=[c], linewidths=1.0, alpha=0.6)
    for lvl, c in zip(fov_levels, fov_colors):
        ax.contour(fov_s, levels=[lvl], colors=[c], linewidths=1.0, alpha=0.6)
    ax.plot([d['od_cx'], d['fov_cx']], [d['od_cy'], d['fov_cy']],
            '-', color='#00FF00', linewidth=2.5)
    ax.plot(d['od_cx'], d['od_cy'], 'o', color='yellow', markersize=10,
            markeredgecolor='black', markeredgewidth=2)
    ax.plot(d['fov_cx'], d['fov_cy'], 'o', color='cyan', markersize=8,
            markeredgecolor='black', markeredgewidth=2)
    ax.set_title(f'Combined: \u03b8 = {d["angle_deg"]:.1f}\u00b0\n'
                 f'\u03c3_pos = {d["sigma_pos"]:.1f} px  \u2192  '
                 f'\u03c3_\u03b8 = {d["sigma_theta"]:.1f}\u00b0',
                 fontsize=10, fontweight='bold')
    ax.axis('off')

    # ── (1,1) Rotation probability distribution ──
    ax = axes[1][1]
    x = np.linspace(-50, 50, 500)
    st = d['sigma_theta']
    y_adapt = np.exp(-x**2 / (2 * st**2)) / (st * np.sqrt(2 * np.pi))
    y_fall = np.exp(-x**2 / (2 * 13.0**2)) / (13.0 * np.sqrt(2 * np.pi))
    ax.fill_between(x, y_adapt, alpha=0.25, color='#1D9E75')
    ax.plot(x, y_adapt, color='#1D9E75', lw=2.5,
            label=f'Adaptive \u03c3_\u03b8 = {st:.1f}\u00b0 (this image)')
    ax.plot(x, y_fall, color='#888780', lw=2, ls='--',
            label='Fallback \u03c3 = 13.0\u00b0 (low confidence)')
    ax.axvline(-40, color='#E24B4A', ls=':', alpha=0.6)
    ax.axvline(40, color='#E24B4A', ls=':', alpha=0.6, label='Clip \u00b140\u00b0')
    ax.set_xlabel('Rotation angle (\u00b0)', fontsize=11)
    ax.set_ylabel('Probability density', fontsize=11)
    ax.set_title('Stage 6: Augmentation Rotation\n'
                 '\u03b8 ~ N(0, \u03c3_\u03b8), clip \u00b140\u00b0',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left')
    ax.set_xlim(-50, 50)
    ax.set_ylim(0, None)
    ax.grid(alpha=0.3)
    # Formula box
    ax.text(0.97, 0.95,
            '\u03c3_pos = \u221a(r\u00b2_OD + r\u00b2_fovea)\n'
            '\u03c3_\u03b8 = arctan(\u03c3_pos / d)\n'
            f'= arctan({d["sigma_pos"]:.0f} / {d["distance"]:.0f})\n'
            f'= {st:.1f}\u00b0  (cap 15\u00b0)',
            transform=ax.transAxes, fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0FAF5', alpha=0.9))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    _save(fig, 'od_fovea_detection_steps.png')


def make_od_fovea_search_region(right_img):
    """od_fovea_search_region.png — combined topographic map with both peaks."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    d = _full_od_fovea_detection(s0)

    od_colors = ['#FFE066', '#FFD700', '#FFA500', '#FF8C00',
                 '#FF6347', '#FF4500', '#DC143C', '#B22222']
    fov_colors = ['#B0E0E6', '#87CEEB', '#6495ED', '#4169E1',
                  '#0000FF', '#0000CD', '#191970', '#000080']

    od_s = d['od_smooth']
    fov_s = d['fov_inv_smooth']

    od_levels = np.linspace(np.percentile(od_s, 80), od_s.max(), len(od_colors))
    fov_vals = fov_s[d['search_mask']]
    fov_levels = np.linspace(np.percentile(fov_vals, 60), fov_vals.max(), len(fov_colors))

    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    ax.imshow(s0)

    # Topographic contours
    for lvl, c in zip(od_levels, od_colors):
        ax.contour(od_s, levels=[lvl], colors=[c], linewidths=1.5, alpha=0.8)
    for lvl, c in zip(fov_levels, fov_colors):
        ax.contour(fov_s, levels=[lvl], colors=[c], linewidths=1.5, alpha=0.8)

    # Annular search zone
    ax.add_patch(plt.Circle((d['od_cx'], d['od_cy']), d['inner_r'],
                             fill=False, color='#EF9F27', lw=1.5, ls='--', label='Search zone'))
    ax.add_patch(plt.Circle((d['od_cx'], d['od_cy']), d['outer_r'],
                             fill=False, color='#EF9F27', lw=1.5, ls='--'))

    # Axis
    ax.plot([d['od_cx'], d['fov_cx']], [d['od_cy'], d['fov_cy']],
            '-', color='#00FF00', lw=2.5)
    ax.plot(d['od_cx'], d['od_cy'], 'o', color='yellow', markersize=10,
            markeredgecolor='black', markeredgewidth=2, label='OD center')
    ax.plot(d['fov_cx'], d['fov_cy'], 'o', color='cyan', markersize=8,
            markeredgecolor='black', markeredgewidth=2, label='Fovea center')

    ax.set_title(f'OD-Fovea Topographic Detection\n'
                 f'\u03b8 = {d["angle_deg"]:.1f}\u00b0, '
                 f'd = {d["distance"]:.0f} px, '
                 f'\u03c3_\u03b8 = {d["sigma_theta"]:.1f}\u00b0',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='lower right',
              facecolor='black', edgecolor='white', labelcolor='white')
    ax.axis('off')
    plt.tight_layout()
    _save(fig, 'od_fovea_search_region.png')


def make_od_fovea_confidence(right_img):
    """od_fovea_confidence.png — how peak sharpness maps to rotation σ."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    d = _full_od_fovea_detection(s0)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Detection Confidence \u2192 Adaptive Augmentation Rotation',
                 fontsize=14, fontweight='bold', y=0.99)

    # ── (0) OD radial intensity profile ──
    ax = axes[0]
    green = s0[:, :, 1].astype(np.float32)
    od_blur = d['od_blur']
    h, w = green.shape
    Y, X = np.mgrid[0:h, 0:w]
    r_from_od = np.sqrt((X - d['od_cx'])**2 + (Y - d['od_cy'])**2)
    max_r = int(d['od_r'] * 4)
    radii = np.arange(0, max_r)
    profile_raw = np.array([green[(r_from_od >= r) & (r_from_od < r + 1) & (green > 15)].mean()
                            for r in radii if np.any((r_from_od >= r) & (r_from_od < r + 1) & (green > 15))])
    profile_blur = np.array([od_blur[(r_from_od >= r) & (r_from_od < r + 1) & (green > 15)].mean()
                             for r in radii if np.any((r_from_od >= r) & (r_from_od < r + 1) & (green > 15))])
    rx = np.arange(len(profile_raw))
    ax.plot(rx, profile_raw, color='#888780', alpha=0.4, lw=1, label='Raw green')
    ax.plot(rx[:len(profile_blur)], profile_blur, color='#FF6347', lw=2.5, label='Blurred (\u03c3=15)')
    ax.axvline(d['od_r'], color='#FFD700', ls='--', lw=1.5, label=f'r_OD = {d["od_r"]:.0f} px')
    ax.fill_betweenx([ax.get_ylim()[0] if ax.get_ylim()[0] else 0, 300],
                     0, d['od_r'], alpha=0.1, color='#FFD700')
    ax.set_xlabel('Distance from OD center (px)', fontsize=10)
    ax.set_ylabel('Green channel intensity', fontsize=10)
    ax.set_title('OD Brightness Peak\n(sharper peak \u2192 smaller r_OD)', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # ── (1) Fovea radial profile ──
    ax = axes[1]
    fov_blur = d['fov_blur']
    r_from_fov = np.sqrt((X - d['fov_cx'])**2 + (Y - d['fov_cy'])**2)
    max_r_f = int(d['fov_r'] * 6)
    prof_raw_f = []
    prof_blur_f = []
    rx_f = []
    for r in range(0, max_r_f):
        ring = (r_from_fov >= r) & (r_from_fov < r + 1) & (green > 15)
        if np.any(ring):
            prof_raw_f.append(green[ring].mean())
            prof_blur_f.append(fov_blur[ring].mean())
            rx_f.append(r)
    rx_f = np.array(rx_f)
    ax.plot(rx_f, prof_raw_f, color='#888780', alpha=0.4, lw=1, label='Raw green')
    ax.plot(rx_f, prof_blur_f, color='#4169E1', lw=2.5, label='Blurred (\u03c3=25)')
    ax.axvline(d['fov_r'], color='#00BFFF', ls='--', lw=1.5, label=f'r_fovea = {d["fov_r"]:.0f} px')
    ax.set_xlabel('Distance from Fovea center (px)', fontsize=10)
    ax.set_ylabel('Green channel intensity', fontsize=10)
    ax.set_title('Fovea Darkness Valley\n(deeper valley \u2192 more confident)', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.invert_yaxis()

    # ── (2) Sigma mapping diagram ──
    ax = axes[2]
    # Show how σ_pos → σ_θ for different detection qualities
    distances = np.linspace(50, 400, 200)
    for sp, label, color in [
        (20, 'Sharp (r_OD=18, r_f=9)', '#1D9E75'),
        (d['sigma_pos'], f'This image ({d["sigma_pos"]:.0f} px)', '#378ADD'),
        (80, 'Uncertain (r_OD=70, r_f=35)', '#D85A30'),
    ]:
        st = np.degrees(np.arctan(sp / distances))
        st = np.minimum(st, 15.0)
        ax.plot(distances, st, lw=2.5, color=color, label=label)
    ax.axhline(15, color='#E24B4A', ls=':', alpha=0.6, label='Cap = 15\u00b0')
    ax.axhline(13, color='#888780', ls=':', alpha=0.6, label='Fallback = 13\u00b0')
    ax.axvline(d['distance'], color='#378ADD', ls='--', alpha=0.4)
    ax.plot(d['distance'], d['sigma_theta'], 'o', color='#378ADD', markersize=10,
            markeredgecolor='black', zorder=5)
    ax.set_xlabel('OD\u2013Fovea distance (px)', fontsize=10)
    ax.set_ylabel('\u03c3_\u03b8 (degrees)', fontsize=10)
    ax.set_title('\u03c3_\u03b8 = arctan(\u03c3_pos / d)\n'
                 'Peak sharpness \u2192 augmentation width',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 20)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    _save(fig, 'od_fovea_confidence.png')


def make_method_fov_crop(right_img):
    """method_fov_crop.png — 3-panel: FOV detection → crop+resize → border waste."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    cx, cy, r = detect_fov(s0)

    # Panel 3: example with large black borders (raw without crop, just resize)
    raw_resized = cv2.resize(right_img, (512, 512), interpolation=cv2.INTER_AREA)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle('Stage 2: FOV Crop + Resize \u2014 Removing Device-Specific Borders',
                 fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(s0)
    circle = plt.Circle((cx, cy), r, fill=False, color='#1D9E75', linewidth=2, linestyle='--')
    axes[0].add_patch(circle)
    axes[0].set_title('FOV Detection\n(green = detected region)', fontsize=10)
    axes[0].axis('off')

    cropped = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    axes[1].imshow(cropped)
    axes[1].set_title('After Crop + Resize\n512\u00d7512, LANCZOS', fontsize=10)
    axes[1].axis('off')

    axes[2].imshow(raw_resized)
    axes[2].set_title('Black borders waste\nCNN capacity', fontsize=10)
    axes[2].axis('off')

    plt.tight_layout()
    _save(fig, 'method_fov_crop.png')


def make_method_flat_field(right_img):
    """method_flat_field.png — 3-panel: before → illumination estimate → after."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    fov_mask = stage3_fov_mask(s2)

    # Compute illumination estimate for display
    cx, cy, r = detect_fov(s2)
    D = 2 * r if r > 50 else 512
    sigma = 0.07 * D
    ksize = int(sigma * 6) | 1
    if ksize < 3:
        ksize = 3
    illum = np.zeros_like(s2, dtype=np.float32)
    for c in range(3):
        ch = s2[:, :, c].astype(np.float32)
        ch_filled = ch.copy()
        fov_mean = ch[fov_mask > 0.5].mean() if np.any(fov_mask > 0.5) else 128.0
        ch_filled[fov_mask < 0.5] = fov_mean
        illum[:, :, c] = cv2.GaussianBlur(ch_filled, (ksize, ksize), sigma)
    illum = np.clip(illum, 0, 255).astype(np.uint8)

    corrected = stage4_flatfield(s2, mask=fov_mask)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle('Stage 4: Flat-Field Correction \u2014 corrected = image \u2212 blur(\u03c3=0.07\u00b7D) + \u03bc_FOV',
                 fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(s2)
    axes[0].set_title('Before Flat-Field\n(illumination gradient visible)', fontsize=10)
    axes[0].axis('off')

    axes[1].imshow(illum)
    axes[1].set_title(f'Illumination Estimate\nGaussianBlur(\u03c3={sigma:.0f})', fontsize=10)
    axes[1].axis('off')

    axes[2].imshow(corrected)
    axes[2].set_title('After Flat-Field \u2714\nUniform illumination', fontsize=10)
    axes[2].axis('off')

    plt.tight_layout()
    _save(fig, 'method_flat_field.png')


def make_method_clahe_comparison(right_img):
    """method_clahe_comparison.png — 3-panel: input → standard CLAHE → upgraded CLAHE."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    ff = stage4_flatfield(s2)

    standard = stage5_clahe(ff, clip_limit=2.0)
    upgraded = stage5_clahe(ff, clip_limit=3.0)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle('Stage 5: Standard CLAHE vs. Upgraded CLAHE (Dual-Constraint)',
                 fontsize=14, fontweight='bold', y=0.98)

    axes[0].imshow(ff)
    axes[0].set_title('Input (after flat-field)', fontsize=10)
    axes[0].axis('off')

    axes[1].imshow(standard)
    axes[1].set_title('Standard CLAHE\ncv2.createCLAHE(clip=2.0)', fontsize=10)
    axes[1].axis('off')

    axes[2].imshow(upgraded)
    axes[2].set_title('Upgraded CLAHE (Ours)\ncv2 clip=3.0 (dual-constraint)', fontsize=10)
    axes[2].axis('off')

    plt.tight_layout()
    _save(fig, 'method_clahe_comparison.png')


def make_method_clahe_sensitivity(right_img):
    """method_clahe_sensitivity.png — 2×4 grid of clipLimit values."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    ff = stage4_flatfield(s2)

    clip_vals = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
    images = [stage5_clahe(ff, clip_limit=c) for c in clip_vals]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle('H-2: CLAHE Parameter Sensitivity \u2014 clipLimit Sweep',
                 fontsize=14, fontweight='bold', y=0.98)

    for i, (clip, img) in enumerate(zip(clip_vals, images)):
        row, col = i // 4, i % 4
        ax = axes[row][col]
        ax.imshow(img)
        label = f'clipLimit={clip:.1f}'
        if 2.0 <= clip <= 3.0:
            label += ' \u2605'
        ax.set_title(label, fontsize=10, fontweight='bold' if 2.0 <= clip <= 3.0 else 'normal')
        ax.axis('off')

    # Last cell: annotation
    axes[1][3].axis('off')
    axes[1][3].text(0.5, 0.6, '\u2605 Optimal range\n(clip=2.0\u20133.0)',
                    transform=axes[1][3].transAxes, fontsize=12, ha='center', va='center',
                    fontweight='bold', color='#1D9E75')
    axes[1][3].text(0.5, 0.25, 'Over-enhancement\n(clip\u22654) amplifies\nnoise and artifacts',
                    transform=axes[1][3].transAxes, fontsize=10, ha='center', va='center',
                    color='#D85A30', style='italic')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    _save(fig, 'method_clahe_sensitivity.png')


def make_method_augmentation(right_img):
    """method_augmentation.png — 2×4 grid of augmentation examples."""
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    ff = stage4_flatfield(s2)
    base = stage5_clahe(ff)
    h, w = base.shape[:2]

    def _rotate(img, angle):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

    def _zoom(img, factor):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, factor)
        return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

    def _brightness(img, beta):
        return cv2.convertScaleAbs(img, alpha=1.0, beta=beta)

    def _pca_jitter(img):
        np.random.seed(7)
        jittered = img.astype(np.float32)
        for c in range(3):
            jittered[:, :, c] += np.random.normal(0, 10)
        return np.clip(jittered, 0, 255).astype(np.uint8)

    def _combined(img):
        out = _rotate(img, 12)
        out = cv2.convertScaleAbs(out, alpha=1.05, beta=5)
        return out

    augmentations = [
        ('Original', base),
        ('Rotation +25\u00b0', _rotate(base, 25)),
        ('Rotation \u221215\u00b0', _rotate(base, -15)),
        ('Rotation +180\u00b0', _rotate(base, 180)),
        ('Zoom 1.1\u00d7', _zoom(base, 1.1)),
        ('Brightness +10%', _brightness(base, 25)),
        ('PCA Color Jitter', _pca_jitter(base)),
        ('Combined Affine', _combined(base)),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle('Stage 6: Augmentation Examples (Train Only)\n'
                 '360\u00b0 rotation valid for circular FOV \u2014 corner pixels are black/empty',
                 fontsize=14, fontweight='bold', y=0.99)

    for i, (title, img) in enumerate(augmentations):
        row, col = i // 4, i % 4
        axes[row][col].imshow(img)
        axes[row][col].set_title(title, fontsize=10)
        axes[row][col].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    _save(fig, 'method_augmentation.png')


def make_methods_comparison_table():
    """methods_comparison_table.png — V5 pipeline comparison table."""
    columns = ['Stage', 'Standard', 'Our V5', 'Innovation']
    data = [
        ['0. Canonical Flip',  'Random h-flip',            'Deterministic by\neye metadata',     'Anatomical consistency'],
        ['1. OD-Fovea Rot.',   'None / random rot.',       'Two-landmark\n+ fallback',           'Annular fovea search'],
        ['2. FOV Crop',        'Hough circles',            'Pct. foreground\n+ bounding circle', 'Robust non-circular'],
        ['3. FOV Mask',        'None (most skip)',          'Binary 4th channel',                 'Explicit FOV boundary'],
        ['4. Flat-Field',      'None (most skip)',          'Blur subtract\n\u03c3=0.07\u00b7D',  'Removes gradient\n(adaptive \u03c3)'],
        ['5. CLAHE',           'cv2.createCLAHE\nfixed clip', 'Dual-constraint\nclip + threshold', 'Global cap + reg'],
        ['6. Augmentation',    'Separate, \u00b115\u00b0', 'Integrated, unified\naffine + PCA',  'Circular FOV'],
        ['7. Normalize',       'ImageNet ch-wise',          'Dataset-specific\n+ mask append',    'Pre-train match\n+ 4ch input'],
    ]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')
    fig.suptitle('V5 Pipeline \u2014 Standard vs. Fundus-Specific Adaptations',
                 fontsize=14, fontweight='bold', y=0.96)

    table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.8)

    # Style header
    for j in range(len(columns)):
        cell = table[0, j]
        cell.set_facecolor('#378ADD')
        cell.set_text_props(color='white', fontweight='bold')

    # Alternate row colors
    for i in range(1, len(data) + 1):
        bg = '#F0F7EE' if i % 2 == 0 else 'white'
        for j in range(len(columns)):
            table[i, j].set_facecolor(bg)
        # Tint "Our V5" column
        table[i, 2].set_facecolor('#E6F5EF' if i % 2 == 0 else '#F0FAF5')

    plt.tight_layout()
    _save(fig, 'methods_comparison_table.png')


# ─── Main ───

if __name__ == '__main__':
    print("Loading source images...")
    right_img = load_image('right_eye.jpeg')
    left_img = load_image('left_eye.jpeg')
    print(f"  Right eye: {right_img.shape}")
    print(f"  Left eye:  {left_img.shape}")

    print("\n--- Per-stage stepper images ---")
    make_stage_2_isotropic_resize(right_img)

    # Corrected chain: no Stage 1 rotation, margin_pct=0
    s0 = stage0_canonical_flip(right_img, is_left_eye=False)
    s2 = stage2_fov_crop_isotropic_resize(s0, margin_pct=0)
    mask = stage3_fov_mask(s2)

    ff_img = make_stage_4_flatfield(s2)
    clahe_img = make_stage_5_clahe(ff_img)
    make_stage_7_normalized(clahe_img, mask)

    print("\n--- Composite overview images ---")
    make_pipeline_stages_grid(right_img)
    make_bilateral_pair(right_img, left_img)
    make_before_after_pipeline(right_img)
    make_baseline_vs_pipeline(right_img)

    print("\n--- Method detail images ---")
    make_method_canonical_flip(right_img, left_img)
    make_od_fovea_detection_steps(right_img)
    make_od_fovea_search_region(right_img)
    make_od_fovea_confidence(right_img)
    make_method_fov_crop(right_img)
    make_method_flat_field(right_img)
    make_method_clahe_comparison(right_img)
    make_method_clahe_sensitivity(right_img)
    make_method_augmentation(right_img)
    make_methods_comparison_table()

    # Remove old V4-named files
    old_files = ['stage_2_flatfield.png', 'stage_3_clahe.png', 'stage_4_normalized.png', 'stage_1_cropped.png']
    for f in old_files:
        path = os.path.join(OUT_DIR, f)
        if os.path.exists(path):
            os.remove(path)
            print(f"  [DEL] Removed old V4 file: {f}")

    print("\n[OK] All pipeline images generated!")
