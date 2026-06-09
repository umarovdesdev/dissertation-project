"""
Stage 1 — Step 3: Rotate around 4 different centers

Takes CLEAN images from stage_0_canonical_flip/ (no markers) and rotates
each by the OD-Fovea axis angle to make the axis horizontal.

Four rotation variants per image:
  od/       — rotate around OD center (OD stays fixed)
  fovea/    — rotate around Fovea center (Fovea stays fixed)
  midpoint/ — rotate around midpoint of OD-Fovea axis (balanced)
  image/    — rotate around geometric image center (fundus centered on canvas)

Rotation uses cv2.warpAffine with:
  - scale = 1.0 (no resize)
  - output size = input size (no crop)
  - borderMode = BORDER_REFLECT (fills corners with reflected pixels;
    these artifacts are removed by FOV crop in stage_2 and masked in stage_3)

Angle: atan2(od_y - fov_y, od_x - fov_x) — the tilt of OD-Fovea axis.
cv2.getRotationMatrix2D rotates counter-clockwise by this angle,
which aligns the axis to horizontal.

Input:  stage_0_canonical_flip/{side}.png + coords.json
Output: stage_1_od_fovea_rotation/{od,fovea,midpoint,image}/{side}.png
"""

import cv2
import json
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
SIDES = ["left", "right"]
CENTERS = ["od", "fovea", "midpoint", "image"]


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

            center_map = {
                "od": tuple(c["od"]),
                "fovea": tuple(c["fovea"]),
                "midpoint": tuple(c["midpoint"]),
                "image": tuple(c["image"]),
            }

            src_path = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_0_canonical_flip", f"{side}.png"
            )
            img = cv2.imread(src_path)
            if img is None:
                print(f"SKIP {gr}/{side} — source not found")
                continue

            h, w = img.shape[:2]

            for name in CENTERS:
                center = center_map[name]
                M = cv2.getRotationMatrix2D(
                    (float(center[0]), float(center[1])),
                    angle_deg, 1.0
                )
                rotated = cv2.warpAffine(
                    img, M, (w, h),
                    flags=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REFLECT
                )

                out_dir = os.path.join(
                    PIPELINE_ROOT, gr, "preprocessing",
                    "stage_1_od_fovea_rotation", name
                )
                os.makedirs(out_dir, exist_ok=True)
                cv2.imwrite(os.path.join(out_dir, f"{side}.png"), rotated)

            print(f"{gr}/{side}: angle={angle_deg:.2f}, 4 rotations saved")


if __name__ == "__main__":
    run()
