"""
Stage 1 — Step 1: Detect user-placed Paint markers

User manually marks OD center (black dot) and Fovea center (purple/lilac dot)
on copies of stage_0 images placed in stage_1_od_fovea_rotation/.

This script detects those markers via HSV color filtering:
  - Black dot (OD):    H=any, S=any, V < 25, area 30..10000, circularity > 0.5
  - Purple dot (Fovea): H=90..170, S > 20, V > 100, area 30..10000

It also computes:
  - Image center:  (width // 2, height // 2)
  - Midpoint:      average of OD and Fovea coordinates

Detection is restricted to a circle of radius 0.45 * min(w,h) from image center
to exclude the black border around the fundus.

Output: prints coordinates and saves to coords.json
"""

import cv2
import numpy as np
import json
import math
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
SIDES = ["left", "right"]


def detect_black_dot(hsv, h, w):
    """Detect the darkest small circular blob inside the fundus area (OD marker)."""
    mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 25))
    center_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(center_mask, (w // 2, h // 2), int(min(w, h) * 0.45), 255, -1)
    mask = cv2.bitwise_and(mask, center_mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best, best_circ = None, 0
    for c in contours:
        area = cv2.contourArea(c)
        perim = cv2.arcLength(c, True)
        if 30 < area < 10000 and perim > 0:
            circ = 4 * np.pi * area / (perim ** 2)
            if circ > 0.5 and circ > best_circ:
                M = cv2.moments(c)
                if M["m00"] > 0:
                    best = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    best_circ = circ
    return best


def detect_purple_dot(hsv):
    """Detect the purple/lilac blob (Fovea marker)."""
    mask = cv2.inRange(hsv, (90, 20, 100), (170, 255, 255))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best, best_area = None, 0
    for c in contours:
        area = cv2.contourArea(c)
        if 30 < area < 10000 and area > best_area:
            M = cv2.moments(c)
            if M["m00"] > 0:
                best = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                best_area = area
    return best


def run():
    results = {
        "description": "OD and Fovea centers detected from user Paint annotations."
    }

    for gr in GRADES:
        results[gr] = {}
        for side in SIDES:
            path = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_1_od_fovea_rotation", f"{side}.png"
            )
            img = cv2.imread(path)
            if img is None:
                print(f"SKIP {gr}/{side}")
                continue

            h, w = img.shape[:2]
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            od = detect_black_dot(hsv, h, w)
            fov = detect_purple_dot(hsv)

            if od is None or fov is None:
                print(f"FAIL {gr}/{side}: od={od}, fov={fov}")
                continue

            img_c = (w // 2, h // 2)
            mid = ((od[0] + fov[0]) // 2, (od[1] + fov[1]) // 2)
            angle = math.degrees(math.atan2(od[1] - fov[1], od[0] - fov[0]))

            results[gr][side] = {
                "od": list(od), "fovea": list(fov),
                "image": list(img_c), "midpoint": list(mid),
                "size": [w, h], "angle_deg": round(angle, 2)
            }
            print(f"{gr}/{side}: OD={od}, Fov={fov}, angle={angle:.2f}")

    out_path = os.path.join(os.path.dirname(__file__), "coords.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    run()
