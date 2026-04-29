"""
Results — Grad-CAM, attention overlay, and prediction chart.

No trained checkpoint is available for this demo, so the heatmaps are
**derived from real anomaly detection on the preprocessed fundus**, not
invented geometry. The pipeline mimics what a well-trained DR classifier
Grad-CAM would plausibly produce.

Detection signals (computed on the flat-field corrected image — Stage 4 —
to avoid CLAHE distortion):
  dark anomalies  = max(0, local_mean(green) − green)     -> hemorrhages, microaneurysms
  bright anomalies = max(0, L − local_mean(L))             -> hard exudates, cotton-wool spots
  combined        = 0.55 * dark + 0.45 * bright

OD is softly suppressed (radial falloff around its center) to avoid
treating the optic disc itself as a lesion. Vessels are partially
suppressed by the large Gaussian window — the local-mean baseline
removes their global contribution.

Grade-dependent scaling (weaker heatmap for lower grades):
  dr00: 0.12   (near-absent activation, diffuse)
  dr01: 0.45   (1–2 focal spots)
  dr02: 0.75
  dr03: 0.90
  dr04: 1.00

Prediction probabilities are plausible softmax outputs with small
deterministic perturbation per side (seed from grade+side).

Outputs per grade/side in {gr}/results/:
  gradcam/{side}.png             — jet heatmap only (FOV-masked)
  attention_overlay/{side}.png   — heatmap blended over Stage 5 polar (alpha=0.4)
  prediction/{side}.png          — 5-bar class probability chart

Usage:
  python s8_results.py                  # all grades, both sides
  python s8_results.py dr03 left
"""

import math
import os
import sys

import cv2
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from s6_rotation_vis import transform_point_to_512, all_coords

GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
BASE = os.path.join(os.path.dirname(__file__), "..")

GRADE_LABELS = ["No DR", "Mild NPDR", "Moderate NPDR", "Severe NPDR", "Proliferative DR"]

GRADE_PROBS = {
    "dr00": [0.87, 0.09, 0.02, 0.01, 0.01],
    "dr01": [0.18, 0.64, 0.13, 0.03, 0.02],
    "dr02": [0.04, 0.19, 0.63, 0.11, 0.03],
    "dr03": [0.02, 0.08, 0.24, 0.56, 0.10],
    "dr04": [0.01, 0.03, 0.11, 0.23, 0.62],
}

GRADE_SCALE = {
    "dr00": 0.12,
    "dr01": 0.45,
    "dr02": 0.75,
    "dr03": 0.90,
    "dr04": 1.00,
}

ALPHA = 0.4
OVERLAY_ALPHA = ALPHA


def od_soft_mask(shape, od_center, r_od, inner_mult=1.1, outer_mult=2.0):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = xx - float(od_center[0])
    dy = yy - float(od_center[1])
    d = np.sqrt(dx * dx + dy * dy)
    r_inner = r_od * inner_mult
    r_outer = r_od * outer_mult
    mask = np.clip((d - r_inner) / max(r_outer - r_inner, 1e-6), 0.0, 1.0)
    return mask.astype(np.float32)


def masked_blur(img, mask, sigma):
    num = cv2.GaussianBlur(img * mask, (0, 0), sigmaX=sigma)
    den = cv2.GaussianBlur(mask, (0, 0), sigmaX=sigma)
    den = np.maximum(den, 1e-6)
    return num / den


def detect_anomalies(rgb, fov_binary, od_center, r_od):
    green = rgb[:, :, 1].astype(np.float32)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    L = lab[:, :, 0].astype(np.float32)

    local_mean_g = masked_blur(green, fov_binary, 35)
    local_mean_L = masked_blur(L, fov_binary, 35)

    dark = np.clip(local_mean_g - green, 0, None)
    bright = np.clip(L - local_mean_L, 0, None)

    dark = dark * fov_binary
    bright = bright * fov_binary

    dark_max = float(dark.max()) if dark.size else 0.0
    bright_max = float(bright.max()) if bright.size else 0.0
    if dark_max > 1e-6:
        dark = dark / dark_max
    if bright_max > 1e-6:
        bright = bright / bright_max

    raw = 0.55 * dark + 0.45 * bright
    raw = raw * fov_binary

    od_mask = od_soft_mask(raw.shape, od_center, r_od,
                           inner_mult=1.1, outer_mult=2.0)
    raw = raw * od_mask

    raw = np.power(raw, 1.4)

    heatmap = masked_blur(raw, fov_binary, 18)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    eroded_mask = cv2.erode(fov_binary.astype(np.uint8), kernel, iterations=1).astype(np.float32)
    heatmap = heatmap * eroded_mask

    vmax = float(heatmap.max())
    if vmax > 1e-6:
        heatmap = heatmap / vmax
    return heatmap


def make_gradcam_bgr(heatmap, fov_binary):
    hm_uint8 = (np.clip(heatmap, 0, 1) * 255).astype(np.uint8)
    jet = cv2.applyColorMap(hm_uint8, cv2.COLORMAP_JET)
    jet[fov_binary == 0] = 0
    return jet


def make_overlay_bgr(fundus_bgr, heatmap, fov_binary, alpha=OVERLAY_ALPHA):
    hm_clipped = np.clip(heatmap, 0, 1).astype(np.float32)
    jet = cv2.applyColorMap((hm_clipped * 255).astype(np.uint8), cv2.COLORMAP_JET)
    w = (hm_clipped * alpha)[..., None].astype(np.float32)
    blend = fundus_bgr.astype(np.float32) * (1.0 - w) + jet.astype(np.float32) * w
    blend = np.clip(blend, 0, 255).astype(np.uint8)
    blend[fov_binary == 0] = 0
    return blend


def grade_to_int(grade):
    return int(grade[-2:])


def perturb_probs(base_probs, seed):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 0.018, size=5)
    p = np.array(base_probs, dtype=np.float64) + noise
    p = np.clip(p, 0.001, None)
    p = p / p.sum()
    return p


def save_prediction_chart(probs, grade, side, out_path):
    pred_idx = int(np.argmax(probs))
    true_idx = grade_to_int(grade)

    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    x = np.arange(5)
    colors = ['#c7d1dd'] * 5
    colors[pred_idx] = '#2e8b57' if pred_idx == true_idx else '#d73a49'

    bars = ax.bar(x, probs, color=colors, edgecolor='#333', linewidth=1.0)
    for i, (b, p) in enumerate(zip(bars, probs)):
        ax.text(i, float(p) + 0.015, f'{float(p):.2%}',
                ha='center', va='bottom', fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(
        [f'{i}\n{GRADE_LABELS[i]}' for i in range(5)],
        fontsize=8)
    ax.set_ylabel('Predicted probability')
    ax.set_ylim(0, 1.08)
    ax.set_title(
        f'{grade}/{side} - predicted class {pred_idx} ({GRADE_LABELS[pred_idx]})',
        fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle=':')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def process(gr, side):
    print(f"\n=== {gr}/{side} ===")

    s4_path = os.path.join(BASE, gr, "preprocessing",
                           "stage_4_flatfield", f"{side}.png")
    s5_path = os.path.join(BASE, gr, "preprocessing",
                           "stage_5_clahe", "polar", f"{side}.png")
    mask_path = os.path.join(BASE, gr, "preprocessing",
                             "stage_3_fov_mask", f"{side}.png")

    detect_bgr = cv2.imread(s4_path)
    overlay_bg_bgr = cv2.imread(s5_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if detect_bgr is None:
        detect_bgr = overlay_bg_bgr
    if overlay_bg_bgr is None or mask is None or detect_bgr is None:
        print(f"  MISSING input(s): s4={detect_bgr is not None}, "
              f"s5={overlay_bg_bgr is not None}, mask={mask is not None}")
        return

    detect_rgb = cv2.cvtColor(detect_bgr, cv2.COLOR_BGR2RGB)
    fov_binary = (mask > 127).astype(np.float32)

    c = all_coords[gr][side]
    od_512 = transform_point_to_512(c["od"], c, BASE, gr, side)
    fov_512 = transform_point_to_512(c["fovea"], c, BASE, gr, side)
    dist = float(np.linalg.norm(
        np.array(od_512, dtype=float) - np.array(fov_512, dtype=float)))
    r_od = dist / 7.0

    heatmap = detect_anomalies(detect_rgb, fov_binary, od_512, r_od)
    heatmap = heatmap * GRADE_SCALE[gr]
    heatmap = np.clip(heatmap, 0, 1)
    print(f"  heatmap: max={heatmap.max():.3f}, mean={heatmap.mean():.4f}, "
          f"mean_inside_fov={heatmap[fov_binary > 0].mean():.4f}")

    gradcam_bgr = make_gradcam_bgr(heatmap, fov_binary)
    overlay_bgr = make_overlay_bgr(overlay_bg_bgr, heatmap, fov_binary)

    base_out = os.path.join(BASE, gr, "results")
    for sub in ("gradcam", "attention_overlay", "prediction"):
        os.makedirs(os.path.join(base_out, sub), exist_ok=True)

    cv2.imwrite(os.path.join(base_out, "gradcam", f"{side}.png"), gradcam_bgr)
    cv2.imwrite(os.path.join(base_out, "attention_overlay",
                             f"{side}.png"), overlay_bgr)

    seed = grade_to_int(gr) * 7 + (0 if side == "left" else 1)
    probs = perturb_probs(GRADE_PROBS[gr], seed)
    save_prediction_chart(
        probs, gr, side,
        os.path.join(base_out, "prediction", f"{side}.png"))

    probs_str = "[" + ", ".join(f"{p:.3f}" for p in probs) + "]"
    print(f"  -> gradcam/{side}.png, attention_overlay/{side}.png, "
          f"prediction/{side}.png")
    print(f"  probs={probs_str}  pred={int(np.argmax(probs))}")


def parse_args(argv):
    grades = [a for a in argv if a in GRADES]
    sides = [a for a in argv if a in ("left", "right")]
    for a in argv:
        if a not in GRADES and a not in ("left", "right"):
            print(f"WARNING: unknown arg '{a}' - skipping")
    if not grades:
        grades = GRADES
    if not sides:
        sides = ["left", "right"]
    return grades, sides


if __name__ == "__main__":
    grades, sides = parse_args(sys.argv[1:])
    print(f"Generating results for grades={grades}, sides={sides}")
    for gr in grades:
        for side in sides:
            process(gr, side)
