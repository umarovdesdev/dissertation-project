"""
Stage 2: FOV Crop + Isotropic Resize to 512x512 + Zero-Padding

Takes rotated images from stage_1_od_fovea_rotation/image/ (image-center rotation)
and produces 512x512 output with isotropic scaling and zero-padding.

Detection strategy:
  1. Landscape images (w > 1.2*h): PIL-based background sampling from left/right edges
  2. Square images: grayscale threshold (V > 15) to find fundus region
  3. Fallback: center-square crop

Isotropic resize: scale = 512 / max(crop_h, crop_w), then center on black canvas.

Input:  stage_1_od_fovea_rotation/image/{side}.png
Output: stage_2_fov_crop_resize/{side}.png (512x512)
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter
import os

PIPELINE_ROOT = os.path.join(os.path.dirname(__file__), "..")
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]
SIDES = ["left", "right"]
TARGET = 512


def detect_fov_bbox_landscape(pil_img):
    blurred = pil_img.filter(ImageFilter.BLUR)
    ba = np.array(blurred)
    h, w, _ = ba.shape
    if w > 1.2 * h:
        left_max = ba[:, :w // 32, :].max(axis=(0, 1)).astype(int)
        right_max = ba[:, -w // 32:, :].max(axis=(0, 1)).astype(int)
        max_bg = np.maximum(left_max, right_max)
        foreground = (ba > max_bg + 10).any(axis=2).astype(np.uint8)
        bbox = Image.fromarray(foreground).getbbox()
        if bbox is not None:
            left, upper, right, lower = bbox
            if (right - left) < 0.8 * h or (lower - upper) < 0.8 * h:
                bbox = None
        return bbox
    return None


def detect_fov_bbox_square(image_rgb):
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(binary > 0)
    if len(ys) == 0:
        return None
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)


def run():
    for gr in GRADES:
        for side in SIDES:
            src = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing",
                "stage_1_od_fovea_rotation", "image", f"{side}.png"
            )
            img_bgr = cv2.imread(src)
            if img_bgr is None:
                print(f"SKIP {gr}/{side}")
                continue

            h, w = img_bgr.shape[:2]
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)

            bbox = detect_fov_bbox_landscape(pil_img)
            if bbox is None:
                bbox = detect_fov_bbox_square(img_rgb)
            if bbox is None:
                left = max((w - h) // 2, 0)
                bbox = (left, 0, min(w - (w - h) // 2, w), h)

            x1, y1, x2, y2 = bbox
            cropped = img_rgb[y1:y2, x1:x2]
            ch, cw = cropped.shape[:2]

            scale = TARGET / max(ch, cw)
            new_w = int(cw * scale)
            new_h = int(ch * scale)
            resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

            canvas = np.zeros((TARGET, TARGET, 3), dtype=np.uint8)
            y_off = (TARGET - new_h) // 2
            x_off = (TARGET - new_w) // 2
            canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized

            out_dir = os.path.join(
                PIPELINE_ROOT, gr, "preprocessing", "stage_2_fov_crop_resize"
            )
            os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(
                os.path.join(out_dir, f"{side}.png"),
                cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR),
            )
            print(f"{gr}/{side}: {w}x{h} -> crop {cw}x{ch} -> resize {new_w}x{new_h} -> 512x512")


if __name__ == "__main__":
    run()
