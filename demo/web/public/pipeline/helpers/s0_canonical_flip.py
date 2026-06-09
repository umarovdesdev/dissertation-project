"""
Stage 0: Canonical Flip

Takes raw fundus images from pipeline/drNN/input/ and produces
horizontally flipped left eye images. Right eye images are copied as-is.

After flip, OD is always on the RIGHT side for both eyes.

Input:  pipeline/drNN/input/left.png, right.png
Output: pipeline/drNN/preprocessing/stage_0_canonical_flip/left.png, right.png
"""

import cv2
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]


def run():
    for gr in GRADES:
        inp_dir = os.path.join(PIPELINE_ROOT, gr, "input")
        out_dir = os.path.join(PIPELINE_ROOT, gr, "preprocessing", "stage_0_canonical_flip")
        os.makedirs(out_dir, exist_ok=True)

        left = cv2.imread(os.path.join(inp_dir, "left.png"))
        right = cv2.imread(os.path.join(inp_dir, "right.png"))

        if left is None or right is None:
            print(f"SKIP {gr} — missing input images")
            continue

        # Left eye: flip horizontally (code 1) so OD moves to right side
        left_flipped = cv2.flip(left, 1)
        cv2.imwrite(os.path.join(out_dir, "left.png"), left_flipped)

        # Right eye: OD already on right, copy as-is
        cv2.imwrite(os.path.join(out_dir, "right.png"), right)

        print(f"{gr}: left flipped {left.shape[1]}x{left.shape[0]}, right copied {right.shape[1]}x{right.shape[0]}")


if __name__ == "__main__":
    run()
