"""
Stage 1 — Step 2: Draw 4 rotation centers on stage_1 images

Reads coordinates from coords.json and draws annotated markers
on the stage_1_od_fovea_rotation/left.png and right.png images:

  Cyan    (#00E5FF, BGR 255,229,0)   — OD center
  Magenta (#FF2D95, BGR 149,45,255)  — Fovea center
  White   (#FFFFFF, BGR 255,255,255) — Image center
  Lime    (#00FF66, BGR 102,255,0)   — Midpoint OD-Fovea

Also draws a white OD-Fovea axis line.

Input:  stage_1_od_fovea_rotation/{side}.png (with Paint markers)
Output: overwrites same files with clean Python-drawn markers
"""

import cv2
import json
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
SIDES = ["left", "right"]

# BGR colors
CYAN = (255, 229, 0)
MAGENTA = (149, 45, 255)
WHITE = (255, 255, 255)
LIME = (102, 255, 0)

RADIUS = 18
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1.5
FONT_THICK = 3


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
            od = tuple(c["od"])
            fov = tuple(c["fovea"])
            img_c = tuple(c["image"])
            mid = tuple(c["midpoint"])

            path = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_1_od_fovea_rotation", f"{side}.png"
            )
            img = cv2.imread(path)
            if img is None:
                print(f"SKIP {gr}/{side}")
                continue

            out = img.copy()

            # Axis line
            cv2.line(out, fov, od, WHITE, 2, cv2.LINE_AA)

            # OD - Cyan
            cv2.circle(out, od, RADIUS, CYAN, -1)
            cv2.putText(out, "OD", (od[0] + 30, od[1] - 20), FONT, FONT_SCALE, CYAN, FONT_THICK)

            # Fovea - Magenta
            cv2.circle(out, fov, RADIUS, MAGENTA, -1)
            cv2.putText(out, "Fovea", (fov[0] + 30, fov[1] - 20), FONT, FONT_SCALE, MAGENTA, FONT_THICK)

            # Image center - White
            cv2.circle(out, img_c, RADIUS, WHITE, -1)
            cv2.putText(out, "Image", (img_c[0] + 30, img_c[1] - 20), FONT, FONT_SCALE, WHITE, FONT_THICK)

            # Midpoint - Lime
            cv2.circle(out, mid, RADIUS, LIME, -1)
            cv2.putText(out, "Midpoint", (mid[0] + 30, mid[1] - 20), FONT, FONT_SCALE, LIME, FONT_THICK)

            cv2.imwrite(path, out)
            print(f"{gr}/{side} annotated")


if __name__ == "__main__":
    run()
