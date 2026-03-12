"""
Quick smoke test for the preprocessing pipeline.

Loads one fundus image from the APTOS 2019 dataset, runs it through the
baseline and full pipelines, and saves a side-by-side comparison to
outputs/figures/preprocessing_comparison.png.

Usage:
    conda activate dr-classifier
    python scripts/test_preprocessing.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.preprocessing import PreprocessingPipeline

APTOS_DIR = Path("/mnt/d/datasets/APTOS 2019/train_images")
OUT_PATH = Path("outputs/figures/preprocessing_comparison.png")


def load_first_image(directory: Path) -> tuple[np.ndarray, Path]:
    """Return the first PNG/JPG found in *directory*."""
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        matches = sorted(directory.glob(ext))
        if matches:
            img = cv2.imread(str(matches[0]))
            if img is not None:
                return img, matches[0]
    raise FileNotFoundError(f"No images found in {directory}")


def to_uint8(image: np.ndarray) -> np.ndarray:
    """Convert float32 [0,1] back to uint8 [0,255] for saving."""
    if image.dtype == np.float32:
        return np.clip(image * 255.0, 0, 255).astype(np.uint8)
    return image


def make_comparison(images: list[np.ndarray], labels: list[str]) -> np.ndarray:
    """Stack images horizontally with a label bar."""
    h = max(img.shape[0] for img in images)
    label_bar_h = 30
    total_h = h + label_bar_h
    w_each = images[0].shape[1]
    canvas = np.zeros((total_h, w_each * len(images), 3), dtype=np.uint8)

    for i, (img, label) in enumerate(zip(images, labels)):
        x_off = i * w_each
        # Resize to common height if needed
        resized = cv2.resize(img, (w_each, h)) if img.shape[0] != h else img
        canvas[label_bar_h:, x_off : x_off + w_each] = resized
        cv2.putText(
            canvas,
            label,
            (x_off + 10, 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
    return canvas


def main() -> None:
    print(f"Looking for images in: {APTOS_DIR}")
    raw, src_path = load_first_image(APTOS_DIR)
    print(f"Loaded: {src_path.name}  shape={raw.shape}")

    baseline = PreprocessingPipeline.create_baseline(target_size=512)
    full = PreprocessingPipeline.create_full()

    assert baseline.is_absent(), "Baseline should report is_absent()==True"
    assert full.is_active(), "Full pipeline should report is_active()==True"

    out_baseline = to_uint8(baseline(raw.copy()))
    out_full = to_uint8(full(raw.copy()))

    # Resize raw to 512 for fair comparison display
    raw_512 = cv2.resize(raw, (512, 512), interpolation=cv2.INTER_LANCZOS4)

    comparison = make_comparison(
        [raw_512, out_baseline, out_full],
        ["Original", "Baseline (FOV only)", "Full Pipeline (5 stages)"],
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT_PATH), comparison)
    print(f"Saved comparison → {OUT_PATH}")

    # Print pipeline state summaries
    print("\nBaseline components:", baseline.enabled_components)
    print("Full pipeline components:", full.enabled_components)

    # Quick ablation example
    ablation = PreprocessingPipeline.create_ablation(
        components=["fov_standardization", "normalize", "clahe"]
    )
    print("\nAblation (resize+normalize+CLAHE) components:", ablation.enabled_components)
    out_ablation = to_uint8(ablation(raw.copy()))
    ablation_path = OUT_PATH.parent / "preprocessing_ablation_example.png"
    cv2.imwrite(str(ablation_path), out_ablation)
    print(f"Saved ablation example → {ablation_path}")


if __name__ == "__main__":
    main()
