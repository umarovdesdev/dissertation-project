"""
Offline PCA eigenvector computation for PCA colour augmentation.

Samples ``n_samples`` images from a dataset, applies preprocessing
stages 0–3 (canonical flip, crop+resize, flat-field, CLAHE — but NOT
normalisation or augmentation), randomly samples ``pixels_per_image``
pixels from each preprocessed image, and computes the PCA of the resulting
pixel distribution.

The eigenvectors and eigenvalues are saved as ``.npy`` files and consumed
by :class:`~src.data.augmentation_unified.UnifiedFundusAugmentation` at training time.

Usage
-----
python scripts/compute_pca_eigvecs.py \\
    --dataset eyepacs \\
    --images-root /mnt/d/datasets/EyePACS/train \\
    --labels-csv /mnt/d/datasets/EyePACS/trainLabels.csv \\
    --output-dir data/processed/ \\
    --n-samples 5000 \\
    --pixels-per-image 1000 \\
    --seed 42
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import cv2
import numpy as np

# Allow running from repo root without installing the package
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from src.preprocessing.canonical_flip import detect_eye_side, canonical_flip
from src.preprocessing.crop_resize import crop_and_resize
from src.preprocessing.flat_field import apply_flat_field
from src.preprocessing.upgraded_clahe import ClaheParams, apply_upgraded_clahe


# ---------------------------------------------------------------------------
# Image discovery helpers
# ---------------------------------------------------------------------------

def _discover_eyepacs(
    images_root: pathlib.Path,
    labels_csv: pathlib.Path | None,
    rng: np.random.Generator,
    n_samples: int,
) -> list[tuple[pathlib.Path, str]]:
    """Return up to *n_samples* (path, eye_side) pairs for EyePACS."""
    if labels_csv is not None and labels_csv.exists():
        import csv
        rows: list[tuple[pathlib.Path, str]] = []
        with open(labels_csv, newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                name = row.get("image", "")
                # filenames in CSV have no extension; find actual file
                candidates = list(images_root.glob(f"{name}.*"))
                if candidates:
                    side = detect_eye_side(candidates[0].name, "eyepacs")
                    rows.append((candidates[0], side))
        if len(rows) > n_samples:
            idx = rng.choice(len(rows), n_samples, replace=False)
            rows = [rows[i] for i in idx]
        return rows

    # Fallback: glob all images
    return _glob_images(images_root, "eyepacs", rng, n_samples)


def _glob_images(
    images_root: pathlib.Path,
    dataset_name: str,
    rng: np.random.Generator,
    n_samples: int,
) -> list[tuple[pathlib.Path, str]]:
    """Return up to *n_samples* (path, eye_side) pairs by globbing the directory."""
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff")
    paths: list[pathlib.Path] = []
    for ext in extensions:
        paths.extend(images_root.glob(ext))
    if not paths:
        for ext in extensions:
            paths.extend(images_root.rglob(ext))

    if len(paths) > n_samples:
        idx = rng.choice(len(paths), n_samples, replace=False)
        paths = [paths[i] for i in idx]

    return [(p, detect_eye_side(p.name, dataset_name)) for p in paths]


_DISCOVER: dict[str, type] = {}  # populated dynamically below


def discover_images(
    dataset_name: str,
    images_root: pathlib.Path,
    labels_csv: pathlib.Path | None,
    rng: np.random.Generator,
    n_samples: int,
) -> list[tuple[pathlib.Path, str]]:
    """Return up to *n_samples* (path, eye_side) pairs for *dataset_name*."""
    if dataset_name == "eyepacs":
        return _discover_eyepacs(images_root, labels_csv, rng, n_samples)
    # All other datasets: glob + unknown eye side
    return _glob_images(images_root, dataset_name, rng, n_samples)


# ---------------------------------------------------------------------------
# Preprocessing stages 0–3 (no normalisation, no augmentation)
# ---------------------------------------------------------------------------

def preprocess_for_pca(
    image_bgr: np.ndarray,
    eye_side: str,
    target_size: int,
    clahe_params: ClaheParams,
) -> np.ndarray:
    """
    Apply stages 0–3 to one image.

    Stages applied: canonical flip → crop+resize → flat-field → CLAHE.
    Normalisation and augmentation are intentionally excluded so that the
    PCA is computed on the natural pixel distribution.

    Args:
        image_bgr: BGR uint8 array as loaded by ``cv2.imread``.
        eye_side: ``"left"``, ``"right"``, or ``"unknown"``.
        target_size: Output size after crop+resize.
        clahe_params: CLAHE parameters.

    Returns:
        RGB uint8 array of shape ``(target_size, target_size, 3)``.
    """
    # BGR → RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    # Stage 0: canonical flip
    image_rgb = canonical_flip(image_rgb, eye_side)
    # Stage 1: crop + resize (discard mask — PCA only needs the image)
    image_rgb, _ = crop_and_resize(image_rgb, target_size)
    # Stage 2: flat-field
    image_rgb = apply_flat_field(image_rgb)
    # Stage 3: CLAHE (deterministic — inference mode)
    image_rgb = apply_upgraded_clahe(image_rgb, clahe_params)
    return image_rgb


# ---------------------------------------------------------------------------
# PCA computation
# ---------------------------------------------------------------------------

def compute_pca(
    samples: list[tuple[pathlib.Path, str]],
    pixels_per_image: int,
    target_size: int,
    clahe_params: ClaheParams,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute PCA eigenvectors and eigenvalues from sampled pixels.

    Args:
        samples: List of ``(path, eye_side)`` pairs.
        pixels_per_image: Number of pixels to sample from each image.
        target_size: Target size for crop+resize.
        clahe_params: CLAHE parameters for stage 3.
        rng: NumPy random generator for reproducibility.

    Returns:
        Tuple ``(eigvals, eigvecs)`` where ``eigvecs`` has shape ``(3, 3)``
        and ``eigvals`` has shape ``(3,)``.  Eigenvalues are in ascending
        order (numpy ``eigh`` convention).
    """
    all_pixels: list[np.ndarray] = []
    n_failed = 0

    for i, (path, eye_side) in enumerate(samples):
        img_bgr = cv2.imread(str(path))
        if img_bgr is None:
            n_failed += 1
            continue

        img_rgb = preprocess_for_pca(img_bgr, eye_side, target_size, clahe_params)

        flat = img_rgb.reshape(-1, 3).astype(np.float32)  # (H*W, 3)
        n_pixels = len(flat)
        n_draw = min(pixels_per_image, n_pixels)
        chosen = rng.choice(n_pixels, n_draw, replace=False)
        all_pixels.append(flat[chosen])

        if (i + 1) % 500 == 0 or (i + 1) == len(samples):
            print(f"  Processed {i + 1}/{len(samples)} images "
                  f"({n_failed} failed)…", flush=True)

    if not all_pixels:
        raise RuntimeError("No pixels collected — check images-root path.")

    pixels = np.vstack(all_pixels)  # (N, 3)
    print(f"Total pixels collected: {len(pixels):,}")

    mean_rgb = np.mean(pixels, axis=0)
    cov = np.cov(pixels - mean_rgb, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)

    return eigvals.astype(np.float32), eigvecs.astype(np.float32)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute PCA eigenvectors for colour augmentation.",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        choices=["eyepacs", "aptos2019", "idrid", "ddr", "odir5k", "rfmid"],
        help="Dataset name.",
    )
    parser.add_argument(
        "--images-root",
        required=True,
        type=pathlib.Path,
        help="Root directory containing image files.",
    )
    parser.add_argument(
        "--labels-csv",
        default=None,
        type=pathlib.Path,
        help="Path to labels CSV (optional; used by EyePACS for L/R detection).",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed/",
        type=pathlib.Path,
        help="Directory to write .npy output files.",
    )
    parser.add_argument(
        "--n-samples",
        default=5000,
        type=int,
        help="Number of images to sample from the dataset.",
    )
    parser.add_argument(
        "--pixels-per-image",
        default=1000,
        type=int,
        help="Number of pixels to sample from each image.",
    )
    parser.add_argument(
        "--target-size",
        default=512,
        type=int,
        help="Resize target (must match training config).",
    )
    parser.add_argument(
        "--seed",
        default=42,
        type=int,
        help="Random seed for reproducibility.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    rng = np.random.default_rng(args.seed)

    print(f"Dataset      : {args.dataset}")
    print(f"Images root  : {args.images_root}")
    print(f"n_samples    : {args.n_samples}")
    print(f"pixels/image : {args.pixels_per_image}")
    print(f"seed         : {args.seed}")
    print()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Discover images
    print(f"Discovering images in {args.images_root} …")
    samples = discover_images(
        dataset_name=args.dataset,
        images_root=args.images_root,
        labels_csv=args.labels_csv,
        rng=rng,
        n_samples=args.n_samples,
    )
    print(f"Found {len(samples)} image(s) to process.\n")

    if not samples:
        print("ERROR: No images found. Check --images-root.", file=sys.stderr)
        sys.exit(1)

    # CLAHE params (defaults match PreprocessingConfig)
    clahe_params = ClaheParams(
        tile_grid_size=(8, 8),
        clip_factor=2.0,
        global_threshold=0.01,
    )

    # Compute PCA
    print("Computing PCA …")
    eigvals, eigvecs = compute_pca(
        samples=samples,
        pixels_per_image=args.pixels_per_image,
        target_size=args.target_size,
        clahe_params=clahe_params,
        rng=rng,
    )

    # Save
    eigvecs_path = args.output_dir / f"{args.dataset}_pca_eigvecs.npy"
    eigvals_path = args.output_dir / f"{args.dataset}_pca_eigvals.npy"
    np.save(eigvecs_path, eigvecs)
    np.save(eigvals_path, eigvals)

    print()
    print("─" * 50)
    print(f"Eigvals  : {eigvals}")
    print(f"Eigvecs shape : {eigvecs.shape}")
    print(f"Saved eigvecs → {eigvecs_path}")
    print(f"Saved eigvals → {eigvals_path}")
    print("─" * 50)


if __name__ == "__main__":
    main()
