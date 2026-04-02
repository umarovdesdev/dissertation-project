#!/usr/bin/env python3
"""
Generate all preprocessing pipeline demonstration images for dissertation-demo.

Input:  43199_left.jpeg, 43199_right.jpeg (raw EyePACS fundus, DR4)
Output: 20+ annotated PNG images in /home/claude/output/

Reproduces the actual V4 preprocessing pipeline stages and generates
comparison figures (standard vs. our method) for the Methods page.
"""

import math
import os

import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from PIL import Image, ImageFilter

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
INPUT_DIR = "/mnt/user-data/uploads"
OUT = "/home/claude/output"
os.makedirs(OUT, exist_ok=True)

DPI = 150
TEAL = (29, 158, 117)
CYAN = (0, 220, 255)
GREEN = (0, 255, 0)
BLUE = (80, 120, 255)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)

right_bgr = cv2.imread(f"{INPUT_DIR}/43199_right.jpeg")
left_bgr = cv2.imread(f"{INPUT_DIR}/43199_left.jpeg")
right_rgb = cv2.cvtColor(right_bgr, cv2.COLOR_BGR2RGB)
left_rgb = cv2.cvtColor(left_bgr, cv2.COLOR_BGR2RGB)

print(f"Right eye: {right_rgb.shape}, Left eye: {left_rgb.shape}")


# ===================================================================
# PIPELINE STAGE IMPLEMENTATIONS (from dr-classifier)
# ===================================================================

def canonical_flip(image_rgb, eye_side):
    """Stage 0a: Flip left eye to right-eye canonical orientation."""
    if eye_side == "left":
        return cv2.flip(image_rgb, 1)
    return image_rgb.copy()


def detect_od_center(green, blur_sigma=15.0, percentile=97.0):
    """Detect optic disc as brightest region centroid."""
    blurred = cv2.GaussianBlur(green, (0, 0), blur_sigma)
    threshold = np.percentile(blurred, percentile)
    od_mask = (blurred >= threshold).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    od_mask = cv2.morphologyEx(od_mask, cv2.MORPH_CLOSE, kernel)
    od_mask = cv2.morphologyEx(od_mask, cv2.MORPH_OPEN, kernel)
    M = cv2.moments(od_mask)
    if M["m00"] == 0:
        _, _, _, max_loc = cv2.minMaxLoc(blurred)
        return max_loc, 30.0
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    radius = math.sqrt(M["m00"] / math.pi)
    return (cx, cy), radius


def detect_fovea_center(green, od_center, od_radius, blur_sigma=25.0,
                        inner_factor=1.5, outer_factor=3.5):
    """Detect fovea as darkest point in annular search region."""
    h, w = green.shape
    od_diameter = od_radius * 2.0
    inner_r = inner_factor * od_diameter
    outer_r = outer_factor * od_diameter
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - od_center[0])**2 + (Y - od_center[1])**2)
    annular = ((dist >= inner_r) & (dist <= outer_r)).astype(np.uint8)
    fov_mask = (green > 15).astype(np.uint8)
    search = annular & fov_mask
    if search.sum() == 0:
        return (w // 2, h // 2), max(od_radius * 0.5, 10.0)
    blurred = cv2.GaussianBlur(green, (0, 0), blur_sigma)
    search_img = blurred.copy()
    search_img[search == 0] = 255
    _, _, min_loc, _ = cv2.minMaxLoc(search_img)
    return min_loc, max(od_radius * 0.5, 10.0)


def rotate_to_horizontal(image, angle_deg):
    """Rotate so OD-fovea axis is horizontal."""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT)


def detect_fov_bbox(pil_img):
    """PIL-based FOV detection."""
    blurred = pil_img.filter(ImageFilter.BLUR)
    ba = np.array(blurred)
    h, w, _ = ba.shape
    if w > 1.2 * h:
        left_max = ba[:, :w//32, :].max(axis=(0, 1)).astype(int)
        right_max = ba[:, -w//32:, :].max(axis=(0, 1)).astype(int)
        max_bg = np.maximum(left_max, right_max)
        foreground = (ba > max_bg + 10).any(axis=2).astype(np.uint8)
        bbox = Image.fromarray(foreground).getbbox()
        if bbox:
            l, u, r, lo = bbox
            if (r - l) < 0.8 * h or (lo - u) < 0.8 * h:
                bbox = None
        return bbox
    return None


def crop_and_resize(image_rgb, target_size=512):
    """Stage 1: FOV crop + resize."""
    pil_img = Image.fromarray(image_rgb)
    w, h = pil_img.size
    bbox = detect_fov_bbox(pil_img)
    if bbox is None:
        left = max((w - h) // 2, 0)
        bbox = (left, 0, min(w - (w - h) // 2, w), h)
    cropped = pil_img.crop(bbox)
    resized = cropped.resize((target_size, target_size), Image.LANCZOS)
    return np.array(resized, dtype=np.uint8)


def apply_flat_field(image_rgb, sigma=45.0):
    """Stage 2: Flat-field correction."""
    blur = cv2.GaussianBlur(image_rgb, (0, 0), sigma)
    corrected = image_rgb.astype(np.float32) - blur.astype(np.float32) + 128.0
    return np.clip(corrected, 0, 255).astype(np.uint8)


def apply_standard_clahe(image_rgb, clip_limit=2.0, tile_grid=(8, 8)):
    """Standard OpenCV CLAHE for comparison."""
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
    l_eq = clahe.apply(l)
    merged = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)


def clip_histogram(hist, clip_limit):
    """Clip and redistribute excess counts."""
    excess = np.maximum(hist - clip_limit, 0.0)
    clipped = hist - excess
    redistribute = excess.sum()
    if redistribute > 0:
        clipped += redistribute // 256
        remainder = int(redistribute % 256)
        if remainder > 0:
            clipped[:remainder] += 1
    return clipped


def apply_upgraded_clahe(image_rgb, clip_factor=2.0, global_threshold=0.01,
                         tile_grid=(8, 8)):
    """Stage 3: Upgraded CLAHE with dual-constraint clip limit."""
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)
    h, w = l_ch.shape
    ty, tx = tile_grid
    th = max(h // ty, 1)
    tw = max(w // tx, 1)
    enhanced = np.zeros_like(l_ch)
    for y in range(0, h, th):
        for x in range(0, w, tw):
            tile = l_ch[y:y+th, x:x+tw]
            area = tile.size
            cl = clip_factor * (area / 256)
            if global_threshold > 0:
                cl = min(cl, global_threshold * area)
            hist, _ = np.histogram(tile.flatten(), bins=256, range=(0, 256))
            hist = hist.astype(np.float32)
            clipped = clip_histogram(hist, cl)
            cdf = np.cumsum(clipped)
            cdf_min = cdf.min()
            cdf_range = cdf.max() - cdf_min
            cdf_norm = (cdf - cdf_min) / (cdf_range + 1e-6)
            lut = np.clip(cdf_norm * 255.0, 0, 255).astype(np.uint8)
            enhanced[y:y+th, x:x+tw] = lut[tile]
    merged = cv2.merge((enhanced, a_ch, b_ch))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)


def imagenet_normalize(image_rgb):
    """Stage 4: ImageNet normalization (visual: denorm for display)."""
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    tensor = image_rgb.astype(np.float32) / 255.0
    normalized = (tensor - mean) / std
    # For display: shift back to visible range
    display = np.clip(normalized * 0.2 + 0.5, 0, 1)
    return (display * 255).astype(np.uint8)


# ===================================================================
# RUN PIPELINE ON RIGHT EYE
# ===================================================================
print("Running V4 pipeline on 43199_right...")

raw_right = right_rgb.copy()
s0a_right = canonical_flip(right_rgb, "right")  # no flip needed

# Stage 0b: OD-fovea detection
green_r = right_rgb[:, :, 1]
od_center_r, od_radius_r = detect_od_center(green_r)
fov_center_r, fov_radius_r = detect_fovea_center(green_r, od_center_r, od_radius_r)
dx = fov_center_r[0] - od_center_r[0]
dy = fov_center_r[1] - od_center_r[1]
dist_r = math.sqrt(dx*dx + dy*dy)
angle_r = math.degrees(math.atan2(dy, dx))
s0b_right = rotate_to_horizontal(s0a_right, angle_r)

s1_right = crop_and_resize(s0b_right, 512)
s2_right = apply_flat_field(s1_right, 45.0)
s3_right = apply_upgraded_clahe(s2_right, 2.0, 0.01)
s4_right = imagenet_normalize(s3_right)

print(f"  OD center: {od_center_r}, radius: {od_radius_r:.1f}")
print(f"  Fovea center: {fov_center_r}")
print(f"  Angle: {angle_r:.1f}°, Distance: {dist_r:.1f}px")

# Also for left eye
print("Running V4 pipeline on 43199_left...")
raw_left = left_rgb.copy()
s0a_left = canonical_flip(left_rgb, "left")  # FLIP

green_l = s0a_left[:, :, 1]
od_center_l, od_radius_l = detect_od_center(green_l)
fov_center_l, fov_radius_l = detect_fovea_center(green_l, od_center_l, od_radius_l)
dx_l = fov_center_l[0] - od_center_l[0]
dy_l = fov_center_l[1] - od_center_l[1]
angle_l = math.degrees(math.atan2(dy_l, dx_l))
s0b_left = rotate_to_horizontal(s0a_left, angle_l)

s1_left = crop_and_resize(s0b_left, 512)
s2_left = apply_flat_field(s1_left, 45.0)
s3_left = apply_upgraded_clahe(s2_left, 2.0, 0.01)

# Standard CLAHE for comparison
s3_std_right = apply_standard_clahe(s2_right, 2.0)
# No flat-field for comparison
s1_no_ff = s1_right.copy()
s3_no_ff = apply_standard_clahe(s1_no_ff, 2.0)


# ===================================================================
# GENERATE IMAGES
# ===================================================================

def save(fig, name):
    path = f"{OUT}/{name}"
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white',
                pad_inches=0.15)
    plt.close(fig)
    print(f"  Saved: {name}")


def save_img(img, name):
    """Save a plain image as PNG."""
    path = f"{OUT}/{name}"
    Image.fromarray(img).save(path)
    print(f"  Saved: {name}")


# --- 1. Individual stage outputs (for Pipeline walkthrough) ---
print("\n=== Individual Stage Images ===")
save_img(raw_right, "stage_raw_right.png")
save_img(raw_left, "stage_raw_left.png")
save_img(s0a_right, "stage_0a_right.png")
save_img(s0a_left, "stage_0a_left.png")  # flipped
save_img(s1_right, "stage_1_cropped.png")
save_img(s2_right, "stage_2_flatfield.png")
save_img(s3_right, "stage_3_clahe.png")
save_img(s4_right, "stage_4_normalized.png")
save_img(s1_left, "stage_1_left_cropped.png")
save_img(s2_left, "stage_2_left_flatfield.png")
save_img(s3_left, "stage_3_left_clahe.png")


# --- 2. OD-Fovea Detection Visualization ---
print("\n=== OD-Fovea Detection ===")

def draw_od_fovea_detection(image_rgb, od_c, od_r, fov_c, fov_r, angle_deg):
    """Draw clean OD-fovea detection result with circles and axis line."""
    vis = image_rgb.copy()
    h, w = vis.shape[:2]
    # OD circles (larger)
    cv2.circle(vis, od_c, int(od_r), CYAN, 3)
    cv2.circle(vis, od_c, int(od_r * 0.3), CYAN, 2)
    cv2.circle(vis, od_c, 4, CYAN, -1)
    # Fovea circles (smaller)
    cv2.circle(vis, fov_c, int(fov_r * 1.5), CYAN, 3)
    cv2.circle(vis, fov_c, int(fov_r * 0.5), CYAN, 2)
    cv2.circle(vis, fov_c, 4, CYAN, -1)
    # OD→Fovea axis line (blue)
    ext = 300
    dx = math.cos(math.radians(angle_deg))
    dy = math.sin(math.radians(angle_deg))
    p1 = (int(od_c[0] - ext * dx), int(od_c[1] - ext * dy))
    p2 = (int(fov_c[0] + ext * dx), int(fov_c[1] + ext * dy))
    cv2.line(vis, p1, p2, BLUE, 2, cv2.LINE_AA)
    # Horizontal reference (green)
    cv2.line(vis, (0, od_c[1]), (w, od_c[1]), GREEN, 2, cv2.LINE_AA)
    return vis

od_vis_right = draw_od_fovea_detection(
    raw_right, od_center_r, od_radius_r, fov_center_r, fov_radius_r, angle_r)
save_img(od_vis_right, "od_fovea_detection_right.png")

# Left eye (after flip)
od_vis_left = draw_od_fovea_detection(
    s0a_left, od_center_l, od_radius_l, fov_center_l, fov_radius_l, angle_l)
save_img(od_vis_left, "od_fovea_detection_left.png")

# Detection search region visualization
def draw_search_region(image_rgb, od_c, od_r, fov_c):
    """Show the annular search region for fovea detection."""
    vis = image_rgb.copy()
    od_d = od_r * 2
    inner = int(1.5 * od_d)
    outer = int(3.5 * od_d)
    # Draw annular search region
    overlay = vis.copy()
    cv2.circle(overlay, od_c, outer, (0, 255, 200), 2, cv2.LINE_AA)
    cv2.circle(overlay, od_c, inner, (0, 255, 200), 2, cv2.LINE_AA)
    # Fill annular region with semi-transparent green
    mask = np.zeros(vis.shape[:2], np.uint8)
    cv2.circle(mask, od_c, outer, 255, -1)
    cv2.circle(mask, od_c, inner, 0, -1)
    green_overlay = vis.copy()
    green_overlay[mask > 0] = (
        vis[mask > 0] * 0.7 + np.array([0, 80, 50]) * 0.3
    ).astype(np.uint8)
    vis = green_overlay
    # OD marker
    cv2.circle(vis, od_c, int(od_r), CYAN, 3)
    cv2.circle(vis, od_c, 5, CYAN, -1)
    # Fovea marker
    cv2.circle(vis, fov_c, 8, RED, -1)
    cv2.circle(vis, fov_c, 20, RED, 3)
    # Labels
    cv2.putText(vis, "OD", (od_c[0]-15, od_c[1]-int(od_r)-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, CYAN, 2)
    cv2.putText(vis, "Fovea", (fov_c[0]-25, fov_c[1]-25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED, 2)
    cv2.putText(vis, "Search region (1.5-3.5 OD diameters)",
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, GREEN, 2)
    return vis

search_vis = draw_search_region(raw_right, od_center_r, od_radius_r, fov_center_r)
save_img(search_vis, "od_fovea_search_region.png")


# --- 3. Pipeline Stages Grid (2×3) ---
print("\n=== Pipeline Stages Grid ===")
fig, axes = plt.subplots(2, 3, figsize=(14, 9.5))
stages = [
    (raw_right, "Raw Input\n(43199_right, DR4)"),
    (s0a_right, "Stage 0a: Canonical Flip\n(OD → no flip needed)"),
    (s1_right, "Stage 1: FOV Crop\n+ Resize 512×512"),
    (s2_right, "Stage 2: Flat-Field\nCorrection (σ=45)"),
    (s3_right, "Stage 3: CLAHE\n(dual-constraint)"),
    (s4_right, "Stage 4+: Normalized\n(visual ≈ CLAHE output)"),
]
labels = ["INPUT", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"]
for ax, (img, title), lbl in zip(axes.flat, stages, labels):
    ax.imshow(img)
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.axis('off')
    # Stage label badge
    color = '#1D9E75' if lbl != 'INPUT' else '#888780'
    ax.text(0.02, 0.98, lbl, transform=ax.transAxes, fontsize=8,
            va='top', ha='left', color='white', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.85))
fig.suptitle("V4 Pipeline Stages — Patient 43199 Right Eye (DR4, Proliferative DR)\n"
             "Actual EyePACS fundus image", fontsize=13, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.93])
save(fig, "pipeline_stages_grid.png")


# --- 4. Bilateral Pair Demo ---
print("\n=== Bilateral Pair ===")
fig, axes = plt.subplots(2, 3, figsize=(14, 9.5))
# Top row: Right eye
axes[0, 0].imshow(raw_right); axes[0, 0].set_title("Right Eye (OD)\nRaw", fontsize=10)
axes[0, 1].imshow(s1_right); axes[0, 1].set_title("Right Eye\nCropped 512×512", fontsize=10)
axes[0, 2].imshow(s3_right); axes[0, 2].set_title("Right Eye\nFull Pipeline", fontsize=10)
# Bottom row: Left eye
axes[1, 0].imshow(raw_left); axes[1, 0].set_title("Left Eye (OS)\nRaw", fontsize=10)
axes[1, 1].imshow(s0a_left); axes[1, 1].set_title("Left Eye\nFlipped → OD orientation", fontsize=10)
axes[1, 2].imshow(s3_left); axes[1, 2].set_title("Left Eye\nFull Pipeline", fontsize=10)
for ax in axes.flat:
    ax.axis('off')
# Arrow annotations
axes[1, 0].annotate('', xy=(0.95, 0.5), xytext=(1.08, 0.5),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle='->', color='#1D9E75', lw=2))
fig.suptitle("Bilateral Pair — Patient 43199 (DR4, Proliferative DR)\n"
             "After Stage 0a: both eyes have optic disc on the right",
             fontsize=13, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.92])
save(fig, "bilateral_pair.png")


# --- 5. Canonical Flip Comparison ---
print("\n=== Canonical Flip ===")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
axes[0].imshow(raw_left); axes[0].set_title("Left Eye (OS) — Raw\nOD on LEFT side", fontsize=10)
axes[1].imshow(s0a_left); axes[1].set_title("Left Eye — After Canonical Flip\nOD on RIGHT side ✓", fontsize=10)
axes[2].imshow(raw_right); axes[2].set_title("Right Eye (OD) — Raw\nOD already on RIGHT ✓", fontsize=10)
for ax in axes:
    ax.axis('off')
axes[0].annotate('cv2.flip(img, 1)', xy=(0.5, -0.05), xycoords='axes fraction',
                ha='center', fontsize=9, fontstyle='italic', color='#1D9E75')
fig.suptitle("Stage 0a: Canonical Flip — Standardizing Eye Laterality",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "method_canonical_flip.png")


# --- 6. Flat-Field Before/After ---
print("\n=== Flat-Field Comparison ===")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
axes[0].imshow(s1_right); axes[0].set_title("Before Flat-Field\n(visible illumination gradient)", fontsize=10)
# Show the blur (illumination estimate)
blur_vis = cv2.GaussianBlur(s1_right, (0, 0), 45.0)
axes[1].imshow(blur_vis); axes[1].set_title("Illumination Estimate\n(GaussianBlur σ=45)", fontsize=10)
axes[2].imshow(s2_right); axes[2].set_title("After Flat-Field\n(uniform illumination ✓)", fontsize=10)
for ax in axes:
    ax.axis('off')
fig.suptitle("Stage 2: Flat-Field Correction — corrected = image − blur(σ=45) + 128",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "method_flat_field.png")


# --- 7. CLAHE Comparison: Standard vs Upgraded ---
print("\n=== CLAHE Comparison ===")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
axes[0].imshow(s2_right)
axes[0].set_title("Input (after flat-field)\nBefore contrast enhancement", fontsize=10)
axes[1].imshow(s3_std_right)
axes[1].set_title("Standard CLAHE\ncv2.createCLAHE(clipLimit=2.0)", fontsize=10)
axes[2].imshow(s3_right)
axes[2].set_title("Upgraded CLAHE (Ours)\nDual-constraint clip limit", fontsize=10)
for ax in axes:
    ax.axis('off')
# Highlight border on "ours"
for spine in axes[2].spines.values():
    spine.set_visible(True)
    spine.set_color('#1D9E75')
    spine.set_linewidth(3)
fig.suptitle("Stage 3: Standard CLAHE vs. Upgraded CLAHE (Dual-Constraint)",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "method_clahe_comparison.png")


# --- 8. No Preprocessing vs Full Pipeline ---
print("\n=== Baseline vs Pipeline ===")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
# Baseline = just crop+resize (no flat-field, no CLAHE)
baseline = crop_and_resize(right_rgb, 512)
axes[0].imshow(baseline)
axes[0].set_title("Baseline\n(crop + resize only)", fontsize=10)
axes[1].imshow(s3_right)
axes[1].set_title("Full V4 Pipeline\n(all 6 stages)", fontsize=10)
# Difference map
diff = cv2.absdiff(baseline, s3_right)
diff_enhanced = np.clip(diff.astype(np.float32) * 3, 0, 255).astype(np.uint8)
axes[2].imshow(diff_enhanced)
axes[2].set_title("Difference (×3 enhanced)\nHighlights pipeline effect", fontsize=10)
for ax in axes:
    ax.axis('off')
fig.suptitle("Baseline (Config A/C) vs. Full V4 Pipeline (Config B/D)",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "baseline_vs_pipeline.png")


# --- 9. CLAHE with different clip factors (parameter sensitivity) ---
print("\n=== CLAHE Parameter Sensitivity ===")
fig, axes = plt.subplots(2, 4, figsize=(15, 8))
clip_factors = [0.5, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0]
for i, cf in enumerate(clip_factors):
    row, col = divmod(i, 4)
    result = apply_upgraded_clahe(s2_right, clip_factor=cf, global_threshold=0.03)
    axes[row, col].imshow(result)
    optimal = " ★" if cf == 2.5 else ""
    axes[row, col].set_title(f"clip_factor={cf}{optimal}", fontsize=9)
    axes[row, col].axis('off')
    if cf == 2.5:
        for spine in axes[row, col].spines.values():
            spine.set_visible(True)
            spine.set_color('#1D9E75')
            spine.set_linewidth(3)
# Last cell: text
axes[1, 3].text(0.5, 0.5,
    "★ Optimal for\nDR Grade 1\n(clip_factor=2.5\nglobal_threshold=0.03)\n\n"
    "Over-enhancement\n(cf>3.0) amplifies\nnoise and artifacts",
    ha='center', va='center', fontsize=10, transform=axes[1, 3].transAxes,
    bbox=dict(boxstyle='round', facecolor='#E1F5EE', alpha=0.9))
axes[1, 3].axis('off')
fig.suptitle("H-2: CLAHE Parameter Sensitivity — Effect of clip_factor\n"
             "(global_threshold=0.03, tile_grid=8×8)", fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.92])
save(fig, "method_clahe_sensitivity.png")


# --- 10. Full Pipeline Before/After (side by side, large) ---
print("\n=== Full Before/After ===")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(baseline); axes[0].set_title("Before\n(Baseline preprocessing)", fontsize=11, fontweight='bold')
axes[1].imshow(s3_right); axes[1].set_title("After\n(Full V4 Pipeline)", fontsize=11, fontweight='bold')
for ax in axes:
    ax.axis('off')
fig.suptitle("Patient 43199 Right Eye — DR Grade 4 (Proliferative DR)\n"
             "Preprocessing dramatically enhances vessel and lesion visibility",
             fontsize=11, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.88])
save(fig, "before_after_pipeline.png")


# --- 11. OD-Fovea Detection Steps ---
print("\n=== OD-Fovea Detection Steps ===")
fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))
# Step 1: Green channel
axes[0].imshow(green_r, cmap='gray')
axes[0].set_title("Step 1: Green Channel\n(best vessel/OD contrast)", fontsize=9)
# Step 2: Blurred + threshold
blurred_g = cv2.GaussianBlur(green_r, (0, 0), 15.0)
thresh = np.percentile(blurred_g, 97)
od_mask = (blurred_g >= thresh).astype(np.uint8) * 255
axes[1].imshow(od_mask, cmap='gray')
axes[1].set_title("Step 2: OD Detection\n(blur σ=15, 97th percentile)", fontsize=9)
# Step 3: Search region
axes[2].imshow(search_vis)
axes[2].set_title("Step 3: Fovea Search\n(annular 1.5–3.5 OD diameters)", fontsize=9)
# Step 4: Final result
axes[3].imshow(od_vis_right)
axes[3].set_title(f"Step 4: Result\n(angle={angle_r:.1f}°, dist={dist_r:.0f}px)", fontsize=9)
for ax in axes:
    ax.axis('off')
fig.suptitle("Stage 0b: OD-Fovea Detection Algorithm — Classical CV Approach",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "od_fovea_detection_steps.png")


# --- 12. FOV Crop Visualization ---
print("\n=== FOV Crop ===")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
axes[0].imshow(s0a_right)
# Draw bounding box on raw
pil_raw = Image.fromarray(s0a_right)
bbox = detect_fov_bbox(pil_raw)
if bbox:
    vis_crop = s0a_right.copy()
    l, u, r, lo = bbox
    cv2.rectangle(vis_crop, (l, u), (r, lo), TEAL, 3)
    axes[0].imshow(vis_crop)
axes[0].set_title("Raw Image\n(green box = detected FOV)", fontsize=10)
axes[1].imshow(s1_right)
axes[1].set_title("After FOV Crop + Resize\n(512×512, LANCZOS)", fontsize=10)
# Show black border problem
axes[2].imshow(raw_right[:, :raw_right.shape[1]//3])
axes[2].set_title("Why crop is needed:\nblack borders waste CNN capacity", fontsize=10)
for ax in axes:
    ax.axis('off')
fig.suptitle("Stage 1: FOV Crop + Resize — Removing Device-Specific Borders",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "method_fov_crop.png")


# --- 13. Augmentation Examples ---
print("\n=== Augmentation Examples ===")
np.random.seed(42)
fig, axes = plt.subplots(2, 4, figsize=(15, 8))
axes[0, 0].imshow(s3_right); axes[0, 0].set_title("Original", fontsize=9)
axes[0, 0].axis('off')
aug_titles = [
    "Rotation +25°", "Rotation −15°", "Rotation +180°",
    "Zoom 1.1×", "Brightness +10%", "PCA Color Jitter", "Combined"
]
aug_images = []
# Rotation examples
for angle in [25, -15, 180]:
    h, w = s3_right.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    rotated = cv2.warpAffine(s3_right, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    aug_images.append(rotated)
# Zoom
M_z = cv2.getRotationMatrix2D((256, 256), 0, 1.1)
zoomed = cv2.warpAffine(s3_right, M_z, (512, 512), borderMode=cv2.BORDER_REFLECT)
aug_images.append(zoomed)
# Brightness
bright = np.clip(s3_right.astype(np.float32) * 1.1 + 5, 0, 255).astype(np.uint8)
aug_images.append(bright)
# PCA color jitter (simplified)
pca_jitter = s3_right.copy().astype(np.float32)
pca_jitter[:, :, 0] += np.random.randn() * 10
pca_jitter[:, :, 1] += np.random.randn() * 8
pca_jitter[:, :, 2] += np.random.randn() * 12
aug_images.append(np.clip(pca_jitter, 0, 255).astype(np.uint8))
# Combined
M_c = cv2.getRotationMatrix2D((256, 256), 35, 1.05)
combined = cv2.warpAffine(s3_right, M_c, (512, 512), borderMode=cv2.BORDER_REFLECT)
combined = np.clip(combined.astype(np.float32) * 0.95 - 3, 0, 255).astype(np.uint8)
aug_images.append(combined)

for i, (img, title) in enumerate(zip(aug_images, aug_titles)):
    row, col = divmod(i + 1, 4)
    axes[row, col].imshow(img)
    axes[row, col].set_title(title, fontsize=9)
    axes[row, col].axis('off')
fig.suptitle("Stage 5: Integrated Augmentation Examples (Train Only)\n"
             "360° rotation justified by circular FOV — corner pixels are semantically empty",
             fontsize=11, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.9])
save(fig, "method_augmentation.png")


# --- 14. Methods comparison summary (visual table) ---
print("\n=== Methods Summary Table ===")
fig, ax = plt.subplots(figsize=(14, 5))
ax.axis('off')
table_data = [
    ["Stage 0a", "Canonical Flip", "Random H-flip\n(augmentation)", "Deterministic\nby eye metadata", "Anatomical\nconsistency"],
    ["Stage 0b", "OD-Fovea\nRotation", "None /\nrandom rotation", "Two-landmark\ndetection + rotate", "Annular fovea\nsearch prior"],
    ["Stage 1", "FOV Crop", "Hough circle\ndetection", "PIL foreground\nedge sampling", "Robust to\nnon-circular FOV"],
    ["Stage 2", "Flat-Field", "None\n(most skip)", "Blur subtraction\nσ=45", "Removes gradient\npreserves lesions"],
    ["Stage 3", "CLAHE", "cv2.createCLAHE\nfixed clip", "Dual-constraint\n+ stochastic 80%", "Global cap +\nregularization"],
    ["Stage 4", "Normalize", "ImageNet\nchannel-wise", "Same\n(standard)", "Matches\npre-training"],
    ["Stage 5", "Augmentation", "Separate layer\n±15° rotation", "Integrated, 360°\nadaptive σ, PCA", "Circular FOV\nenables full rot."],
]
cols = ["Stage", "Name", "Standard\nApproach", "Our V4\nAdaptation", "Key\nInnovation"]
table = ax.table(cellText=table_data, colLabels=cols, loc='center',
                cellLoc='center', colColours=['#E1F5EE']*5)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 2.2)
# Style header
for j in range(5):
    table[0, j].set_text_props(fontweight='bold', fontsize=9)
# Green background for "our" column
for i in range(1, 8):
    table[i, 3].set_facecolor('#E6F9F1')
    table[i, 4].set_facecolor('#FFF8E6')
fig.suptitle("V4 Pipeline Methods — Standard vs. Our Fundus-Specific Adaptations",
             fontsize=12, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.92])
save(fig, "methods_comparison_table.png")


# --- Summary ---
print("\n" + "="*60)
print("GENERATION COMPLETE")
print("="*60)
files = sorted(os.listdir(OUT))
print(f"\nTotal files: {len(files)}")
for f in files:
    size = os.path.getsize(f"{OUT}/{f}")
    print(f"  {f:45s} {size//1024:>5d} KB")
