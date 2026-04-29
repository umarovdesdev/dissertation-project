"""
Generate all Stage 5 CLAHE variants for dr00-dr04.
- upgraded_clahe (8x8 rect, dual-constraint, no interpolation)
- cv2.createCLAHE (standard with bilinear interpolation)
- Adaptive Polar CLAHE (fovea-centered, vessel-density non-uniform grid
  + dual-constraint + polar bilinear interpolation)
  with 5 substep visualizations
"""

import cv2
import numpy as np
import sys
import os

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "experiments", "src", "preprocessing"))

GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]


def process_grade(gr):
    print(f"\n=== {gr} ===")

    for side in ["left", "right"]:
        img_bgr = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_4_flatfield", f"{side}.png"))
        mask = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"), cv2.IMREAD_GRAYSCALE)
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        L, A, B = cv2.split(lab)
        mask_3ch = np.expand_dims(mask > 0, axis=-1).astype(np.uint8)

        # 1. upgraded_clahe (rect 8x8)
        try:
            from upgraded_clahe import apply_upgraded_clahe, ClaheParams
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            params = ClaheParams(tile_grid_size=(8, 8), clip_factor=2.0, global_threshold=0.01)
            enhanced_rgb = apply_upgraded_clahe(img_rgb, params)
            enhanced_rgb = enhanced_rgb * np.expand_dims(mask > 0, axis=-1).astype(np.uint8)
            out_dir = os.path.join(BASE, gr, "preprocessing", "stage_5_clahe")
            os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(os.path.join(out_dir, f"{side}.png"), cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR))
            print(f"  {side}: upgraded_clahe done")
        except ImportError:
            print(f"  {side}: upgraded_clahe SKIP (import failed)")

        # 2. cv2.createCLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_cv2 = clahe.apply(L)
        merged_cv2 = cv2.merge((l_cv2, A, B))
        result_cv2 = cv2.cvtColor(merged_cv2, cv2.COLOR_LAB2BGR) * mask_3ch
        out_dir = os.path.join(BASE, gr, "preprocessing", "stage_5_clahe", "cv2")
        os.makedirs(out_dir, exist_ok=True)
        cv2.imwrite(os.path.join(out_dir, f"{side}.png"), result_cv2)
        print(f"  {side}: cv2 done")

    # 3. Adaptive Polar CLAHE (fovea-centered, non-uniform sectors)
    from s5_polar_adaptive import process_grade as polar_process
    import json
    with open(os.path.join(os.path.dirname(__file__), "coords.json")) as f:
        all_coords = json.load(f)
    polar_process(gr, all_coords)


if __name__ == "__main__":
    for gr in GRADES:
        process_grade(gr)
