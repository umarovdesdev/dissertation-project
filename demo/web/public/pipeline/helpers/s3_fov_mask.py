"""
Stage 3: FOV Mask Generation

Creates a binary mask (white=fundus, black=padding) for each 512x512 image.

Key decision: mask is generated from the CLEAN pre-rotation image (stage_0),
not from stage_2. This avoids BORDER_REFLECT artifacts ("ears") that appear
in corners after rotation. The mask is then transformed identically to the RGB:
  1. Threshold stage_0 grayscale (V > 15) to get clean fundus boundary
  2. Rotate mask with BORDER_CONSTANT=0 (same angle & center as RGB rotation)
  3. Crop + resize 512x512 (same bbox as stage_2)

BORDER_REFLECT artifacts in RGB are real pixel data for the model but should
NOT be included in the mask — the mask must indicate only genuine fundus area.

Small edge artifacts from camera frame in original images are preserved
(they are real, not rotation artifacts).

Input:  stage_0_canonical_flip/{side}.png + coords.json
Output: stage_3_fov_mask/{side}.png (512x512, binary: 0 or 255)
"""

import cv2
import numpy as np
import json
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
SIDES = ["left", "right"]
TARGET = 512


def run():
    coords_path = os.path.join(os.path.dirname(__file__), "coords.json")
    with open(coords_path) as f:
        coords = json.load(f)

    for gr in GRADES:
        if gr not in coords:
            continue
        for side in SIDES:
            if side not in coords[gr]:
                continue

            c = coords[gr][side]
            angle_deg = c["angle_deg"]
            img_c = tuple(c["image"])

            # 1. Clean stage_0 -> binary mask
            s0_path = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_0_canonical_flip", f"{side}.png"
            )
            s0 = cv2.imread(s0_path)
            if s0 is None:
                print(f"SKIP {gr}/{side}")
                continue

            h, w = s0.shape[:2]
            gray = cv2.cvtColor(s0, cv2.COLOR_BGR2GRAY)
            _, mask_raw = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5, 5), np.uint8)
            mask_raw = cv2.morphologyEx(mask_raw, cv2.MORPH_OPEN, kernel)
            mask_raw = cv2.morphologyEx(mask_raw, cv2.MORPH_CLOSE, kernel)

            # 2. Rotate mask with BORDER_CONSTANT=0
            M = cv2.getRotationMatrix2D(
                (float(img_c[0]), float(img_c[1])), angle_deg, 1.0
            )
            mask_rotated = cv2.warpAffine(
                mask_raw, M, (w, h),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            )
            _, mask_rotated = cv2.threshold(mask_rotated, 127, 255, cv2.THRESH_BINARY)

            # 3. Crop + resize (same bbox as stage_2)
            ys, xs = np.where(mask_rotated > 0)
            x1, y1 = xs.min(), ys.min()
            x2, y2 = xs.max() + 1, ys.max() + 1

            cropped = mask_rotated[y1:y2, x1:x2]
            ch, cw = cropped.shape[:2]

            scale = TARGET / max(ch, cw)
            new_w = int(cw * scale)
            new_h = int(ch * scale)
            resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            _, resized = cv2.threshold(resized, 127, 255, cv2.THRESH_BINARY)

            canvas = np.zeros((TARGET, TARGET), dtype=np.uint8)
            y_off = (TARGET - new_h) // 2
            x_off = (TARGET - new_w) // 2
            canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized

            out_dir = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing", "stage_3_fov_mask"
            )
            os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(os.path.join(out_dir, f"{side}.png"), canvas)

            fundus_pct = (canvas > 0).sum() / canvas.size * 100
            print(f"{gr}/{side}: {w}x{h} -> 512x512, fundus={fundus_pct:.1f}%")


if __name__ == "__main__":
    run()
