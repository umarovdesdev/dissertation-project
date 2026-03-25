"""
Visualize OD/fovea detection on sample fundus images.

Usage:
    python scripts/visualize_od_fovea.py --input /path/to/image.jpeg --output viz_output.png
    python scripts/visualize_od_fovea.py --input /mnt/d/datasets/EyePACS/train/ --output viz_dir/ --n 20
"""

import argparse
import pathlib
import random
import sys

import cv2
import numpy as np

# Allow imports from project root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.preprocessing.od_fovea_detect import detect_od_fovea, rotate_to_horizontal


def visualize_single(image_path: pathlib.Path, output_path: pathlib.Path) -> None:
    """Draw detection result on a single image and save."""
    bgr = cv2.imread(str(image_path))
    if bgr is None:
        print(f"Cannot read: {image_path}")
        return
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    result = detect_od_fovea(rgb)

    # Draw on BGR copy for cv2.imwrite
    viz = bgr.copy()

    # OD: green circle + center dot
    cv2.circle(viz, result.od_center, int(result.od_radius), (0, 255, 0), 2)
    cv2.circle(viz, result.od_center, 3, (0, 255, 0), -1)

    # Fovea: red circle + center dot
    cv2.circle(viz, result.fovea_center, int(result.fovea_radius), (0, 0, 255), 2)
    cv2.circle(viz, result.fovea_center, 3, (0, 0, 255), -1)

    # OD→fovea line (blue)
    cv2.line(viz, result.od_center, result.fovea_center, (255, 0, 0), 2)

    # Text info
    info = (
        f"angle={result.angle_deg:.1f} "
        f"sigma={result.rotation_sigma_deg:.1f} "
        f"conf={'Y' if result.confident else 'N'}"
    )
    cv2.putText(viz, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Side-by-side: original with annotations + rotated
    if result.confident:
        rotated_rgb = rotate_to_horizontal(rgb, result.angle_deg)
        rotated_bgr = cv2.cvtColor(rotated_rgb, cv2.COLOR_RGB2BGR)
    else:
        rotated_bgr = bgr.copy()
        cv2.putText(
            rotated_bgr, "SKIP (low confidence)", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
        )

    # Resize both to same height for concatenation
    target_h = 512
    scale = target_h / viz.shape[0]
    viz_resized = cv2.resize(viz, None, fx=scale, fy=scale)
    rot_resized = cv2.resize(rotated_bgr, None, fx=scale, fy=scale)
    combined = np.hstack([viz_resized, rot_resized])

    cv2.imwrite(str(output_path), combined)
    print(
        f"Saved: {output_path}  "
        f"(confident={result.confident}, "
        f"angle={result.angle_deg:.1f}deg, "
        f"sigma={result.rotation_sigma_deg:.1f}deg)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize OD/fovea detection")
    parser.add_argument("--input", required=True, help="Image file or directory")
    parser.add_argument("--output", required=True, help="Output file or directory")
    parser.add_argument(
        "--n", type=int, default=20,
        help="Number of images to sample (if input is directory)",
    )
    args = parser.parse_args()

    inp = pathlib.Path(args.input)
    out = pathlib.Path(args.output)

    if inp.is_file():
        visualize_single(inp, out)
    elif inp.is_dir():
        out.mkdir(parents=True, exist_ok=True)
        images = (
            list(inp.glob("*.jpeg"))
            + list(inp.glob("*.jpg"))
            + list(inp.glob("*.png"))
        )
        sample = random.sample(images, min(args.n, len(images)))
        for img_path in sample:
            visualize_single(img_path, out / f"viz_{img_path.stem}.png")
    else:
        print(f"Input not found: {inp}")


if __name__ == "__main__":
    main()
