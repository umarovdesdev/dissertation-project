"""
Stage 6 — Adaptive rotation uncertainty visualization.

Draws iso-intensity contour rings around OD and Fovea, angular fan
variants, and adaptive-vs-fallback distribution plots.

Contour approach (approved):
  1. Green channel of stage_2 (best fundus landmark contrast)
  2. Gaussian blur on grayscale → threshold at multiple levels
  3. Binary mask pre-blur (5×5 σ=1.5) before contour extraction
  4. Resample to 120 uniform points → circular moving average (window=11)
  5. Fallback chain: green → grayscale → LAB L → organic pseudo-ellipses

Coordinate transform uses OpenCV convention: [cos sin; -sin cos].

Output per grade/side in stage_6_augmentation/1_rotation/:
  {side}_contours.png     — smoothed iso-intensity rings only
  {side}_variant_A.png       — rings + tangent band fan
  {side}_variant_B.png       — rings + cone fan from midpoint
  distribution_adaptive.png  — adaptive σ vs fallback σ=13° plot

Usage:
  python s6_rotation_vis.py              # all grades
  python s6_rotation_vis.py dr03         # single grade
  python s6_rotation_vis.py dr00 dr03    # specific grades
"""

import cv2
import numpy as np
import json
import math
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]

ROTATION_SIGMA = 13.0
ROTATION_CLIP = 40.0

# Contour detection parameters
OD_BLUR_SIGMA = 10
OD_N_LEVELS = 4
OD_RADIUS_MULT = 2.0

FOV_BLUR_SIGMA = 5
FOV_N_LEVELS = 4
FOV_RADIUS_MULT = 3.0

CONTRAST_THRESHOLD = 5

# Smoothing parameters
RESAMPLE_POINTS = 120
SMOOTH_WINDOW = 11

# Fallback multipliers (× estimated radius)
FOV_FALLBACK_MULTS = [0.7, 1.2, 1.8, 2.3]
OD_FALLBACK_MULTS = [0.5, 0.9, 1.3, 1.8, 2.2]
FOV_ELONGATION = 1.1
OD_ELONGATION = 1.15

# Drawing colors (BGR)
OD_COLOR = (130, 165, 130)
FOV_COLOR = (145, 145, 145)
FAN_COLOR = (255, 255, 255)

with open(os.path.join(os.path.dirname(__file__), "coords.json")) as f:
    all_coords = json.load(f)


def transform_point_to_512(point, coords_entry, base_path, gr, side):
    c = coords_entry
    pt = np.array(point, dtype=np.float64)
    img_c = np.array(c["image"], dtype=np.float64)
    angle_rad = math.radians(c["angle_deg"])
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    dx, dy = pt[0] - img_c[0], pt[1] - img_c[1]
    pt_rot = np.array([
        cos_a * dx + sin_a * dy + img_c[0],
        -sin_a * dx + cos_a * dy + img_c[1]
    ])
    rot_img = cv2.imread(os.path.join(
        base_path, gr, "preprocessing", "stage_1_od_fovea_rotation", "image", f"{side}.png"
    ))
    gray_r = cv2.cvtColor(rot_img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_r, 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(binary > 0)
    x1, y1 = xs.min(), ys.min()
    x2, y2 = xs.max() + 1, ys.max() + 1
    cw, ch = x2 - x1, y2 - y1
    pt_crop = pt_rot - np.array([x1, y1])
    scale = 512 / max(ch, cw)
    new_w, new_h = int(cw * scale), int(ch * scale)
    x_off = (512 - new_w) // 2
    y_off = (512 - new_h) // 2
    return int(pt_crop[0] * scale + x_off), int(pt_crop[1] * scale + y_off)


def smooth_contour(cnt, n_points=RESAMPLE_POINTS, smooth_window=SMOOTH_WINDOW):
    pts = cnt.reshape(-1, 2).astype(np.float64)
    if len(pts) < 5:
        return cnt
    pts_closed = np.vstack([pts, pts[0:1]])
    diffs = np.diff(pts_closed, axis=0)
    dists = np.sqrt((diffs ** 2).sum(axis=1))
    cum = np.concatenate([[0], np.cumsum(dists)])
    total = cum[-1]
    if total < 1:
        return cnt
    targets = np.linspace(0, total, n_points, endpoint=False)
    resampled = np.zeros((n_points, 2))
    for d in range(2):
        resampled[:, d] = np.interp(targets, cum, pts_closed[:, d])
    half = smooth_window // 2
    pad = np.vstack([resampled[-half:], resampled, resampled[:half]])
    smoothed = np.zeros_like(resampled)
    for i in range(n_points):
        smoothed[i] = pad[i:i + smooth_window].mean(axis=0)
    return smoothed.astype(np.int32).reshape(-1, 1, 2)


def find_smooth_contours(gray_ch, center, fov_mask, n_levels, is_bright,
                         blur_sigma, max_radius):
    h, w = gray_ch.shape
    cx, cy = int(center[0]), int(center[1])
    cx, cy = max(0, min(cx, w - 1)), max(0, min(cy, h - 1))
    blurred = cv2.GaussianBlur(gray_ch, (0, 0), blur_sigma)
    roi = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(roi, (cx, cy), max_radius, 255, -1)
    roi = cv2.bitwise_and(roi, fov_mask)
    center_val = float(blurred[cy, cx])
    ring = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(ring, (cx, cy), max_radius, 255, -1)
    cv2.circle(ring, (cx, cy), int(max_radius * 0.7), 0, -1)
    ring = cv2.bitwise_and(ring, fov_mask)
    bg_pix = blurred[ring > 0]
    bg_val = float(np.mean(bg_pix)) if len(bg_pix) > 0 else 128.0
    diff = abs(center_val - bg_val)
    label = 'OD' if is_bright else 'Fovea'
    print(f"    {label}: center={center_val:.0f}, bg={bg_val:.0f}, diff={diff:.0f}")
    contours_out = []
    for i in range(1, n_levels + 1):
        if is_bright:
            frac = 1.0 - i / (n_levels + 1)
            thresh = int(bg_val + frac * (center_val - bg_val))
            _, bw = cv2.threshold(blurred, thresh, 255, cv2.THRESH_BINARY)
        else:
            frac = i / (n_levels + 1)
            thresh = int(center_val + frac * (bg_val - center_val))
            _, bw = cv2.threshold(blurred, thresh, 255, cv2.THRESH_BINARY_INV)
        bw = cv2.bitwise_and(bw, roi)
        bw = cv2.GaussianBlur(bw, (5, 5), 1.5)
        _, bw = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)
        cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        best, best_area = None, float('inf')
        for cnt in cnts:
            if cv2.pointPolygonTest(cnt, (float(cx), float(cy)), False) >= 0:
                a = cv2.contourArea(cnt)
                if 30 < a < best_area:
                    best, best_area = cnt, a
        if best is not None:
            smoothed = smooth_contour(best)
            contours_out.append(smoothed)
            print(f"      level {i}: thresh={thresh}, area={best_area:.0f}, "
                  f"~r={math.sqrt(best_area / math.pi):.0f}")
    return contours_out, diff


def detect_contours_with_fallback(s2_img, center, fov_mask, is_bright,
                                  n_levels, blur_sigma, max_radius,
                                  fallback_mults, fallback_elong):
    green_ch = s2_img[:, :, 1]
    contours, diff = find_smooth_contours(
        green_ch, center, fov_mask, n_levels, is_bright, blur_sigma, max_radius)

    if not is_bright and diff < CONTRAST_THRESHOLD:
        print("    retrying with grayscale...")
        gray_s2 = cv2.cvtColor(s2_img, cv2.COLOR_BGR2GRAY)
        contours, diff = find_smooth_contours(
            gray_s2, center, fov_mask, n_levels, is_bright, blur_sigma, max_radius)

    if not is_bright and diff < CONTRAST_THRESHOLD:
        print("    retrying with LAB L...")
        lab = cv2.cvtColor(s2_img, cv2.COLOR_BGR2LAB)
        contours, diff = find_smooth_contours(
            lab[:, :, 0], center, fov_mask, n_levels, is_bright, blur_sigma, max_radius)

    MIN_RINGS = 2
    if diff < CONTRAST_THRESHOLD or len(contours) < MIN_RINGS:
        label = 'OD' if is_bright else 'Fovea'
        r_base = max_radius / (OD_RADIUS_MULT if is_bright else FOV_RADIUS_MULT)
        reason = f"diff={diff:.0f}" if diff < CONTRAST_THRESHOLD else f"only {len(contours)} rings"
        print(f"    {label}: fallback pseudo-ellipses (r_base={r_base:.1f}, {reason})")
        contours = make_fallback_contours(center, r_base, fallback_mults, fallback_elong)

    return contours


def make_fallback_contours(center, base_radius, multipliers, elongation):
    cx, cy = center
    contours = []
    for m in multipliers:
        r = max(4, base_radius * m)
        n_pts = 100
        angles = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
        rx, ry = r * elongation, r
        np.random.seed(int(r * 100))
        perturb = 1.0 + 0.03 * np.sin(angles * 3) + 0.02 * np.sin(angles * 5 + 1.0)
        pts = np.column_stack([
            cx + rx * np.cos(angles) * perturb,
            cy + ry * np.sin(angles) * perturb
        ]).astype(np.int32).reshape(-1, 1, 2)
        contours.append(pts)
    return contours


def draw_rings(vis, od_contours, fov_contours, od_512, fov_512, mid_512):
    for cnt in od_contours:
        cv2.drawContours(vis, [cnt], -1, OD_COLOR, 1, cv2.LINE_AA)
    for cnt in fov_contours:
        cv2.drawContours(vis, [cnt], -1, FOV_COLOR, 1, cv2.LINE_AA)
    cv2.circle(vis, fov_512, 3, (0, 0, 220), -1, cv2.LINE_AA)
    cv2.circle(vis, od_512, 3, (0, 220, 0), -1, cv2.LINE_AA)
    cv2.circle(vis, mid_512, 2, (0, 200, 0), -1, cv2.LINE_AA)


def contour_y_half_span(contours, fallback):
    if contours:
        pts = contours[-1].reshape(-1, 2)
        return (pts[:, 1].max() - pts[:, 1].min()) / 2.0
    return fallback


def draw_fan_A(vis, od_512, fov_512, fov_half_y, od_half_y):
    n_lines, ext = 9, 100
    for i in range(n_lines):
        t = -1.0 + 2.0 * i / (n_lines - 1)
        fx, fy = float(fov_512[0]), float(fov_512[1]) + t * fov_half_y
        ox, oy = float(od_512[0]), float(od_512[1]) + t * od_half_y
        ddx, ddy = ox - fx, oy - fy
        ln = math.sqrt(ddx ** 2 + ddy ** 2)
        if ln > 0:
            ux, uy = ddx / ln, ddy / ln
            p1 = (int(fx - ux * ext), int(fy - uy * ext))
            p2 = (int(ox + ux * ext), int(oy + uy * ext))
            cv2.line(vis, p1, p2, FAN_COLOR, 1, cv2.LINE_AA)


def draw_fan_B(vis, mid_512, axis_deg, sigma_theta, dist):
    fan_radius = int(dist * 1.4)
    n_fan, half_spread = 9, 2.5 * sigma_theta
    for i in range(n_fan):
        t = -1 + 2 * i / (n_fan - 1)
        angle = axis_deg + t * half_spread
        a_rad = math.radians(angle)
        x_end = int(mid_512[0] + fan_radius * math.cos(a_rad))
        y_end = int(mid_512[1] + fan_radius * math.sin(a_rad))
        cv2.line(vis, mid_512, (x_end, y_end), FAN_COLOR, 1, cv2.LINE_AA)


def draw_distribution(out_path, sigma_adaptive, gr, side):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    x = np.linspace(-50, 50, 1000)

    pdf_fixed = np.exp(-x ** 2 / (2 * ROTATION_SIGMA ** 2))
    pdf_fixed[np.abs(x) > ROTATION_CLIP] = 0
    pdf_fixed = pdf_fixed / (pdf_fixed.sum() * (x[1] - x[0]))

    pdf_adaptive = np.exp(-x ** 2 / (2 * sigma_adaptive ** 2))
    pdf_adaptive[np.abs(x) > ROTATION_CLIP] = 0
    pdf_adaptive = pdf_adaptive / (pdf_adaptive.sum() * (x[1] - x[0]))

    ax.fill_between(x, pdf_fixed, alpha=0.15, color='steelblue')
    ax.plot(x, pdf_fixed, color='steelblue', lw=1.5, ls='--',
            label=f'Fallback: $\\sigma$={ROTATION_SIGMA}$^\\circ$')
    ax.fill_between(x, pdf_adaptive, alpha=0.35, color='green')
    ax.plot(x, pdf_adaptive, color='green', lw=2,
            label=f'Adaptive: $\\sigma$={sigma_adaptive:.1f}$^\\circ$ ({gr}/{side})')
    ax.axvline(-ROTATION_CLIP, color='red', ls='--', lw=1,
               label=f'clip = $\\pm${ROTATION_CLIP}$^\\circ$')
    ax.axvline(ROTATION_CLIP, color='red', ls='--', lw=1)

    ax.set_xlabel('Rotation angle (degrees)')
    ax.set_ylabel('Probability density')
    ax.set_title('Adaptive vs Fallback Rotation Distribution')
    ax.legend(fontsize=8)
    ax.set_xlim(-50, 50)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def process_grade(gr):
    print(f"\n{'='*40}")
    print(f"  {gr}")
    print(f"{'='*40}")

    sigma_values = {}

    for side in ["left", "right"]:
        c = all_coords[gr][side]
        od_512 = transform_point_to_512(c["od"], c, BASE, gr, side)
        fov_512 = transform_point_to_512(c["fovea"], c, BASE, gr, side)
        mid_512 = transform_point_to_512(c["midpoint"], c, BASE, gr, side)

        img = cv2.imread(os.path.join(
            BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png"))
        mask = cv2.imread(os.path.join(
            BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"),
            cv2.IMREAD_GRAYSCALE)
        s2_img = cv2.imread(os.path.join(
            BASE, gr, "preprocessing", "stage_2_fov_crop_resize", f"{side}.png"))

        print(f"\n  --- {side} ---")
        print(f"  OD={od_512}, Fov={fov_512}, Mid={mid_512}")

        dist = np.linalg.norm(
            np.array(od_512, dtype=float) - np.array(fov_512, dtype=float))
        r_od = dist / 7.0
        r_fovea = r_od * 0.5
        sigma_pos = math.sqrt(r_od ** 2 + r_fovea ** 2)
        sigma_theta = math.degrees(math.atan(sigma_pos / dist)) if dist > 0 else 15.0
        sigma_theta = min(sigma_theta, 15.0)
        sigma_values[side] = sigma_theta

        dx_ax = od_512[0] - fov_512[0]
        dy_ax = od_512[1] - fov_512[1]
        axis_deg = math.degrees(math.atan2(dy_ax, dx_ax))

        print(f"  dist={dist:.1f}, r_od={r_od:.1f}, r_fov={r_fovea:.1f}, "
              f"sigma_theta={sigma_theta:.2f}, axis={axis_deg:.2f}")

        # Detect contours
        od_contours = detect_contours_with_fallback(
            s2_img, od_512, mask, is_bright=True,
            n_levels=OD_N_LEVELS, blur_sigma=OD_BLUR_SIGMA,
            max_radius=int(r_od * OD_RADIUS_MULT),
            fallback_mults=OD_FALLBACK_MULTS, fallback_elong=OD_ELONGATION)

        fov_contours = detect_contours_with_fallback(
            s2_img, fov_512, mask, is_bright=False,
            n_levels=FOV_N_LEVELS, blur_sigma=FOV_BLUR_SIGMA,
            max_radius=int(r_fovea * FOV_RADIUS_MULT),
            fallback_mults=FOV_FALLBACK_MULTS, fallback_elong=FOV_ELONGATION)

        print(f"  OD: {len(od_contours)} rings, Fov: {len(fov_contours)} rings")

        fov_half_y = contour_y_half_span(fov_contours, r_fovea)
        od_half_y = contour_y_half_span(od_contours, r_od)

        out_dir = os.path.join(
            BASE, gr, "preprocessing", "stage_6_augmentation", "1_rotation")
        os.makedirs(out_dir, exist_ok=True)

        # 1. Contours only
        vis = img.copy()
        draw_rings(vis, od_contours, fov_contours, od_512, fov_512, mid_512)
        vis[mask == 0] = 0
        cv2.imwrite(os.path.join(out_dir, f"{side}_contours.png"), vis)

        # 2. Variant A — tangent band
        vis_a = img.copy()
        draw_rings(vis_a, od_contours, fov_contours, od_512, fov_512, mid_512)
        draw_fan_A(vis_a, od_512, fov_512, fov_half_y, od_half_y)
        vis_a[mask == 0] = 0
        cv2.imwrite(os.path.join(out_dir, f"{side}_variant_A.png"), vis_a)

        # 3. Variant B — cone from midpoint
        vis_b = img.copy()
        draw_rings(vis_b, od_contours, fov_contours, od_512, fov_512, mid_512)
        draw_fan_B(vis_b, mid_512, axis_deg, sigma_theta, dist)
        vis_b[mask == 0] = 0
        cv2.imwrite(os.path.join(out_dir, f"{side}_variant_B.png"), vis_b)

        print(f"  -> {side}: contours, variant_A, variant_B")

    # Distribution plot (use left eye sigma)
    out_dir = os.path.join(
        BASE, gr, "preprocessing", "stage_6_augmentation", "1_rotation")
    dist_path = os.path.join(out_dir, "distribution_adaptive.png")
    draw_distribution(dist_path, sigma_values["left"], gr, "left")
    print(f"  -> distribution_adaptive.png (sigma={sigma_values['left']:.2f})")


if __name__ == "__main__":
    grades = sys.argv[1:] if len(sys.argv) > 1 else GRADES
    for gr in grades:
        if gr not in all_coords:
            print(f"WARNING: {gr} not in coords.json, skipping")
            continue
        process_grade(gr)
