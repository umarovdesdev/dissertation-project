"""
Stage 4: Flat-Field Correction

Reduces uneven illumination by subtracting a heavily blurred version
of the image and re-centering at 128:

    corrected = image - GaussianBlur(image, sigma) + 128

Sigma is adaptive: sigma = 0.07 * FOV_diameter, where FOV_diameter is
estimated from the stage_3 mask area (d = 2 * sqrt(area / pi)).

Correction is applied only inside the FOV mask — padding pixels are
zeroed out. This also removes any BORDER_REFLECT artifacts from stage_1
rotation that may remain in the stage_2 RGB.

Input:  stage_2_fov_crop_resize/{side}.png (RGB) + stage_3_fov_mask/{side}.png
Output: stage_4_flatfield/{side}.png (512x512, corrected RGB)
"""

import cv2
import numpy as np
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
SIDES = ["left", "right"]


def run():
    for gr in GRADES:
        for side in SIDES:
            rgb_path = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_2_fov_crop_resize", f"{side}.png"
            )
            mask_path = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_3_fov_mask", f"{side}.png"
            )
            img = cv2.imread(rgb_path)
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

            if img is None or mask is None:
                print(f"SKIP {gr}/{side}")
                continue

            # Adaptive sigma = 0.07 * FOV diameter
            fundus_area = (mask > 0).sum()
            fov_diameter = 2.0 * np.sqrt(fundus_area / np.pi)
            sigma = 0.07 * fov_diameter

            # Flat-field: corrected = image - blur + 128
            blur = cv2.GaussianBlur(img, (0, 0), sigma)
            corrected = img.astype(np.float32) - blur.astype(np.float32) + 128.0
            corrected = np.clip(corrected, 0, 255).astype(np.uint8)

            # Zero out padding using mask
            mask_3ch = np.expand_dims(mask > 0, axis=-1).astype(np.uint8)
            corrected = corrected * mask_3ch

            out_dir = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing", "stage_4_flatfield"
            )
            os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(os.path.join(out_dir, f"{side}.png"), corrected)
            print(f"{gr}/{side}: sigma={sigma:.1f} (FOV_d={fov_diameter:.0f}px)")


if __name__ == "__main__":
    run()
