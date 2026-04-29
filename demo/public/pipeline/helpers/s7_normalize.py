"""
Stage 7 — Normalize → 4ch tensor (RGB preview).

Full V5 Stage 7:
  1. RGB (from Stage 5) ---ToTensor---> float32 CHW in [0, 1]
  2. ImageNet normalize: (x - mean) / std
  3. Concatenate FOV mask as 4th channel → (4, H, W) tensor

For demo: we apply the normalize → denormalize roundtrip to produce a
visual RGB preview of what the CNN receives on the RGB branch (it is
mathematically ≈ Stage 5 minus rounding), then multiply by the binary
FOV mask so the padding is explicitly zeroed — matching the CNN's
effective view when the 4th-channel mask gates the receptive field.

ImageNet stats (from experiments/configs/default.yaml, baseline path):
  mean = (0.485, 0.456, 0.406)
  std  = (0.229, 0.224, 0.225)

Input:
  stage_5_clahe/polar/{side}.png  — final CLAHE RGB (novel polar variant)
  stage_3_fov_mask/{side}.png     — binary FOV mask

Output:
  stage_7_normalize/{side}.png    — RGB preview, padding zeroed

Usage:
  python s7_normalize.py                   # all grades, both sides
  python s7_normalize.py dr03              # single grade
  python s7_normalize.py dr00 dr02 left    # subset of grades + side filter
"""

import os
import sys

import cv2
import numpy as np

GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
BASE = os.path.join(os.path.dirname(__file__), "..")

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def normalize_roundtrip(rgb_uint8):
    x = rgb_uint8.astype(np.float32) / 255.0
    x_norm = (x - IMAGENET_MEAN) / IMAGENET_STD
    x_back = x_norm * IMAGENET_STD + IMAGENET_MEAN
    x_back = np.clip(x_back * 255.0, 0, 255)
    return x_back.astype(np.uint8)


def process(gr, side):
    src_rgb = os.path.join(
        BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png")
    src_mask = os.path.join(
        BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png")

    img_bgr = cv2.imread(src_rgb)
    mask = cv2.imread(src_mask, cv2.IMREAD_GRAYSCALE)

    if img_bgr is None or mask is None:
        print(f"  {gr}/{side}: MISSING input — rgb={img_bgr is not None}, "
              f"mask={mask is not None}")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    preview_rgb = normalize_roundtrip(img_rgb)

    mask_binary = (mask > 127).astype(np.uint8)
    preview_rgb[mask_binary == 0] = 0

    out_dir = os.path.join(BASE, gr, "preprocessing", "stage_7_normalize")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{side}.png")

    out_bgr = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_path, out_bgr)

    fov_px = int(mask_binary.sum())
    print(f"  {gr}/{side}: {img_rgb.shape} -> {out_path}  (FOV={fov_px} px)")


def parse_args(argv):
    grades, sides = [], []
    for a in argv:
        if a in ("left", "right"):
            sides.append(a)
        elif a in GRADES:
            grades.append(a)
        else:
            print(f"WARNING: unknown arg '{a}' — skipping")
    if not grades:
        grades = GRADES
    if not sides:
        sides = ["left", "right"]
    return grades, sides


if __name__ == "__main__":
    grades, sides = parse_args(sys.argv[1:])
    print(f"Stage 7 normalize — grades={grades}, sides={sides}")
    for gr in grades:
        for side in sides:
            process(gr, side)
