"""
Stage 6 — Rotation uncertainty via peak-based sector fans.

Pipeline:
  1. Detect iso-intensity contour rings around OD and Fovea
     (reuse detection logic from s6_rotation_vis.py).
  2. Extract vertical peaks (top / bottom) of each ring.
  3. Connect every Fovea peak to every OD peak (all-to-all) — sector lines.
  4. Compute per-line angle relative to the nominal OD-Fovea axis.
  5. Produce empirical step distribution + analytical normal distribution.

Outputs per grade/side in stage_6_augmentation/1_rotation/:
  {side}_peaks.png                — rings + black vertical peaks
  {side}_sectors.png              — rings + peaks + all-to-all sector lines
  {side}_distribution_step.png    — empirical step histogram from sector angles
  {side}_distribution_normal.png  — truncated Gaussian fit (σ from outer-ring formula)

σ formula (from experiments/src/preprocessing/od_fovea_detect.py):
  σ_pos = sqrt(r_od_outer² + r_fov_outer²)
  σ_θ   = degrees(atan(σ_pos / distance))
  σ_θ   = min(σ_θ, 15°)

Usage:
  python s6_rotation_peaks.py                  # default: dr03 left
  python s6_rotation_peaks.py dr03 left
  python s6_rotation_peaks.py dr00 dr03 left
  python s6_rotation_peaks.py dr03 right
"""

import math
import os
import sys

import cv2
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from s6_rotation_vis import (
    BASE,
    all_coords,
    transform_point_to_512,
    detect_contours_with_fallback,
    OD_N_LEVELS, OD_BLUR_SIGMA, OD_RADIUS_MULT,
    OD_FALLBACK_MULTS, OD_ELONGATION,
    FOV_N_LEVELS, FOV_BLUR_SIGMA, FOV_RADIUS_MULT,
    FOV_FALLBACK_MULTS, FOV_ELONGATION,
)

ROTATION_SIGMA_CAP = 15.0
ROTATION_CLIP = 40.0
DISPLAY_RANGE = 22.5

OD_COLOR = (130, 165, 130)
FOV_COLOR = (145, 145, 145)
PEAK_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
FOV_CENTER_COLOR = (0, 0, 220)
OD_CENTER_COLOR = (0, 220, 0)
MID_CENTER_COLOR = (0, 200, 0)

LINE_EXTENSION_PX = 250


def extract_vertical_peaks(contours):
    peaks = []
    for cnt in contours:
        pts = cnt.reshape(-1, 2)
        top_idx = int(np.argmin(pts[:, 1]))
        bot_idx = int(np.argmax(pts[:, 1]))
        peaks.append((int(pts[top_idx, 0]), int(pts[top_idx, 1])))
        peaks.append((int(pts[bot_idx, 0]), int(pts[bot_idx, 1])))
    return peaks


def outer_ring_radius(contours, center):
    if not contours:
        return 0.0
    outer = contours[-1].reshape(-1, 2).astype(np.float64)
    dx = outer[:, 0] - center[0]
    dy = outer[:, 1] - center[1]
    return float(np.sqrt(dx * dx + dy * dy).max())


def draw_rings(vis, od_contours, fov_contours, od_pt, fov_pt, mid_pt):
    for cnt in od_contours:
        cv2.drawContours(vis, [cnt], -1, OD_COLOR, 1, cv2.LINE_AA)
    for cnt in fov_contours:
        cv2.drawContours(vis, [cnt], -1, FOV_COLOR, 1, cv2.LINE_AA)
    cv2.circle(vis, fov_pt, 3, FOV_CENTER_COLOR, -1, cv2.LINE_AA)
    cv2.circle(vis, od_pt, 3, OD_CENTER_COLOR, -1, cv2.LINE_AA)
    cv2.circle(vis, mid_pt, 2, MID_CENTER_COLOR, -1, cv2.LINE_AA)


def draw_peaks(vis, peaks, radius=3):
    for (x, y) in peaks:
        cv2.circle(vis, (int(x), int(y)), radius, PEAK_COLOR, -1, cv2.LINE_AA)


def extend_line(p1, p2, ext=LINE_EXTENSION_PX):
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])
    dx, dy = x2 - x1, y2 - y1
    ln = math.sqrt(dx * dx + dy * dy)
    if ln < 1e-6:
        return None
    ux, uy = dx / ln, dy / ln
    a = (int(round(x1 - ux * ext)), int(round(y1 - uy * ext)))
    b = (int(round(x2 + ux * ext)), int(round(y2 + uy * ext)))
    return a, b


def draw_sectors(vis, fov_peaks, od_peaks):
    for fov_pk in fov_peaks:
        for od_pk in od_peaks:
            ends = extend_line(fov_pk, od_pk)
            if ends is None:
                continue
            a, b = ends
            cv2.line(vis, a, b, LINE_COLOR, 1, cv2.LINE_AA)


def mono_pairs(fov_peaks, od_peaks):
    n = min(len(fov_peaks), len(od_peaks))
    return [(fov_peaks[i], od_peaks[i]) for i in range(n)]


def draw_sectors_mono(vis, fov_peaks, od_peaks, thickness=2):
    for fov_pk, od_pk in mono_pairs(fov_peaks, od_peaks):
        ends = extend_line(fov_pk, od_pk)
        if ends is None:
            continue
        a, b = ends
        cv2.line(vis, a, b, LINE_COLOR, thickness, cv2.LINE_AA)


def compute_sector_angles(fov_peaks, od_peaks, axis_deg):
    thetas = []
    for fov_pk in fov_peaks:
        for od_pk in od_peaks:
            dx = od_pk[0] - fov_pk[0]
            dy = od_pk[1] - fov_pk[1]
            line_deg = math.degrees(math.atan2(dy, dx))
            delta = line_deg - axis_deg
            while delta > 180.0:
                delta -= 360.0
            while delta <= -180.0:
                delta += 360.0
            thetas.append(delta)
    thetas.sort()
    return thetas


def compute_sector_angles_mono(fov_peaks, od_peaks, axis_deg):
    thetas = []
    for fov_pk, od_pk in mono_pairs(fov_peaks, od_peaks):
        dx = od_pk[0] - fov_pk[0]
        dy = od_pk[1] - fov_pk[1]
        line_deg = math.degrees(math.atan2(dy, dx))
        delta = line_deg - axis_deg
        while delta > 180.0:
            delta -= 360.0
        while delta <= -180.0:
            delta += 360.0
        thetas.append(delta)
    thetas.sort()
    return thetas


def draw_step_distribution(out_path, thetas, gr, side):
    N = len(thetas)
    fig, ax = plt.subplots(figsize=(7, 3.5))

    edges_left = []
    edges_right = []
    heights = []
    for k in range(N - 1):
        left = thetas[k]
        right = thetas[k + 1]
        width = right - left
        if width <= 1e-9:
            continue
        density = (1.0 / N) / width
        edges_left.append(left)
        edges_right.append(right)
        heights.append(density)

    for left, right, h in zip(edges_left, edges_right, heights):
        ax.fill_between([left, right], [h, h], color='steelblue', alpha=0.35)
        ax.plot([left, right], [h, h], color='steelblue', linewidth=1.5)
    for i in range(len(edges_left) - 1):
        x_edge = edges_right[i]
        ax.plot([x_edge, x_edge], [heights[i], heights[i + 1]],
                color='steelblue', linewidth=1.0)
    if edges_left:
        ax.plot([edges_left[0], edges_left[0]], [0, heights[0]],
                color='steelblue', linewidth=1.0)
        ax.plot([edges_right[-1], edges_right[-1]], [heights[-1], 0],
                color='steelblue', linewidth=1.0)

    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_xlim(-DISPLAY_RANGE, DISPLAY_RANGE)
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Rotation angle θ (degrees)')
    ax.set_ylabel('Empirical density')
    ax.set_title(f'Step distribution from sectors — {gr}/{side}  (N = {N} pairs)')
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def draw_normal_distribution(out_path, sigma_theta, gr, side):
    fig, ax = plt.subplots(figsize=(7, 3.5))

    x = np.linspace(-DISPLAY_RANGE, DISPLAY_RANGE, 1000)
    full_x = np.linspace(-ROTATION_CLIP, ROTATION_CLIP, 4000)
    full_pdf = np.exp(-full_x ** 2 / (2.0 * sigma_theta ** 2))
    norm_const = np.trapezoid(full_pdf, full_x)
    pdf = np.exp(-x ** 2 / (2.0 * sigma_theta ** 2)) / norm_const

    ax.fill_between(x, pdf, color='green', alpha=0.35)
    ax.plot(x, pdf, color='green', linewidth=2,
            label=f'σ_θ = {sigma_theta:.2f}°  (truncated at ±{ROTATION_CLIP:.0f}°)')

    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_xlim(-DISPLAY_RANGE, DISPLAY_RANGE)
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Rotation angle θ (degrees)')
    ax.set_ylabel('Probability density')
    ax.set_title(f'Truncated normal fit — {gr}/{side}')
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def process(gr, side):
    print(f"\n=== {gr}/{side} ===")

    c = all_coords[gr][side]
    od_512 = transform_point_to_512(c["od"], c, BASE, gr, side)
    fov_512 = transform_point_to_512(c["fovea"], c, BASE, gr, side)
    mid_512 = transform_point_to_512(c["midpoint"], c, BASE, gr, side)

    bg_path = os.path.join(
        BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png")
    mask_path = os.path.join(
        BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png")
    s2_path = os.path.join(
        BASE, gr, "preprocessing", "stage_2_fov_crop_resize", f"{side}.png")

    bg_img = cv2.imread(bg_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    s2_img = cv2.imread(s2_path)

    if bg_img is None or mask is None or s2_img is None:
        print(f"  MISSING input(s): bg={bg_img is not None}, "
              f"mask={mask is not None}, s2={s2_img is not None}")
        return

    dist = float(np.linalg.norm(
        np.array(od_512, dtype=float) - np.array(fov_512, dtype=float)))
    r_od = dist / 7.0
    r_fov = r_od * 0.5
    axis_deg = math.degrees(math.atan2(
        od_512[1] - fov_512[1], od_512[0] - fov_512[0]))

    print(f"  OD={od_512}  Fov={fov_512}  Mid={mid_512}")
    print(f"  dist={dist:.1f}  r_od_init={r_od:.1f}  r_fov_init={r_fov:.1f}  axis={axis_deg:.2f}deg")

    od_contours = detect_contours_with_fallback(
        s2_img, od_512, mask, is_bright=True,
        n_levels=OD_N_LEVELS, blur_sigma=OD_BLUR_SIGMA,
        max_radius=int(r_od * OD_RADIUS_MULT),
        fallback_mults=OD_FALLBACK_MULTS, fallback_elong=OD_ELONGATION)

    fov_contours = detect_contours_with_fallback(
        s2_img, fov_512, mask, is_bright=False,
        n_levels=FOV_N_LEVELS, blur_sigma=FOV_BLUR_SIGMA,
        max_radius=int(r_fov * FOV_RADIUS_MULT),
        fallback_mults=FOV_FALLBACK_MULTS, fallback_elong=FOV_ELONGATION)

    print(f"  rings: OD={len(od_contours)}, Fov={len(fov_contours)}")

    od_peaks = extract_vertical_peaks(od_contours)
    fov_peaks = extract_vertical_peaks(fov_contours)
    print(f"  peaks: OD={len(od_peaks)}, Fov={len(fov_peaks)}, "
          f"pairs={len(od_peaks) * len(fov_peaks)}")

    r_od_outer = outer_ring_radius(od_contours, od_512)
    r_fov_outer = outer_ring_radius(fov_contours, fov_512)
    sigma_pos = math.sqrt(r_od_outer ** 2 + r_fov_outer ** 2)
    sigma_theta = math.degrees(math.atan(sigma_pos / dist)) if dist > 0 else ROTATION_SIGMA_CAP
    sigma_theta = min(sigma_theta, ROTATION_SIGMA_CAP)
    print(f"  r_od_outer={r_od_outer:.1f}  r_fov_outer={r_fov_outer:.1f}  "
          f"sigma_pos={sigma_pos:.1f}  sigma_theta={sigma_theta:.2f}deg")

    thetas = compute_sector_angles(fov_peaks, od_peaks, axis_deg)
    if thetas:
        print(f"  theta range: [{thetas[0]:.2f}deg, {thetas[-1]:.2f}deg]  "
              f"mean={np.mean(thetas):.2f}deg  std={np.std(thetas):.2f}deg")

    out_dir = os.path.join(
        BASE, gr, "preprocessing", "stage_6_augmentation", "1_rotation")
    os.makedirs(out_dir, exist_ok=True)

    vis_peaks = bg_img.copy()
    draw_rings(vis_peaks, od_contours, fov_contours, od_512, fov_512, mid_512)
    draw_peaks(vis_peaks, od_peaks)
    draw_peaks(vis_peaks, fov_peaks)
    vis_peaks[mask == 0] = 0
    cv2.imwrite(os.path.join(out_dir, f"{side}_peaks.png"), vis_peaks)

    vis_sect = bg_img.copy()
    draw_sectors(vis_sect, fov_peaks, od_peaks)
    draw_rings(vis_sect, od_contours, fov_contours, od_512, fov_512, mid_512)
    draw_peaks(vis_sect, od_peaks)
    draw_peaks(vis_sect, fov_peaks)
    vis_sect[mask == 0] = 0
    cv2.imwrite(os.path.join(out_dir, f"{side}_sectors.png"), vis_sect)

    vis_mono = bg_img.copy()
    draw_sectors_mono(vis_mono, fov_peaks, od_peaks, thickness=1)
    draw_rings(vis_mono, od_contours, fov_contours, od_512, fov_512, mid_512)
    draw_peaks(vis_mono, od_peaks)
    draw_peaks(vis_mono, fov_peaks)
    vis_mono[mask == 0] = 0
    cv2.imwrite(os.path.join(out_dir, f"{side}_sectors_mono.png"), vis_mono)

    thetas_mono = compute_sector_angles_mono(fov_peaks, od_peaks, axis_deg)
    if thetas_mono:
        print(f"  mono theta range: [{thetas_mono[0]:.2f}deg, {thetas_mono[-1]:.2f}deg]  "
              f"N={len(thetas_mono)}  std={np.std(thetas_mono):.2f}deg")

    draw_step_distribution(
        os.path.join(out_dir, f"{side}_distribution_step.png"),
        thetas, gr, side)
    draw_step_distribution(
        os.path.join(out_dir, f"{side}_distribution_step_mono.png"),
        thetas_mono, gr, side)

    draw_normal_distribution(
        os.path.join(out_dir, f"{side}_distribution_normal.png"),
        sigma_theta, gr, side)

    print(f"  -> {side}_peaks.png, {side}_sectors.png, "
          f"{side}_distribution_step.png, {side}_distribution_normal.png")


def parse_args(argv):
    grades, side = [], "left"
    for a in argv:
        if a in ("left", "right"):
            side = a
        elif a in all_coords:
            grades.append(a)
        else:
            print(f"WARNING: unknown arg '{a}' — skipping")
    if not grades:
        grades = ["dr03"]
    return grades, side


if __name__ == "__main__":
    grades, side = parse_args(sys.argv[1:])
    for gr in grades:
        process(gr, side)
