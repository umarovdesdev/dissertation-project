"""
Fundus image preprocessing pipeline for diabetic retinopathy classification.

Preprocessing steps:
  1. Load raw fundus images
  2. Resize / crop to a standard field of view
  3. Apply CLAHE contrast enhancement
  4. Remove low-quality / dark images
  5. Normalise pixel values and save processed images
"""

import cv2
import numpy as np
from pathlib import Path


# ---------------------------------------------------------------------------
# Quality filtering
# ---------------------------------------------------------------------------

def is_valid_image(image: np.ndarray, min_brightness: float = 10.0) -> bool:
    """Return False for images that are too dark or mostly black (poor quality)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(gray.mean()) >= min_brightness


# ---------------------------------------------------------------------------
# Field-of-view cropping
# ---------------------------------------------------------------------------

def crop_to_fundus(image: np.ndarray, threshold: int = 7) -> np.ndarray:
    """
    Crop out the black border surrounding the circular fundus region.

    Args:
        image: BGR image as a NumPy array.
        threshold: Pixel intensity threshold used to detect the fundus circle.

    Returns:
        Cropped image containing only the fundus disk area.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return image

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    return image[y : y + h, x : x + w]


# ---------------------------------------------------------------------------
# Contrast enhancement
# ---------------------------------------------------------------------------

def apply_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid: int = 8) -> np.ndarray:
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalisation) to the
    green channel, which carries the most diagnostic information in fundus images.

    Args:
        image: BGR image as a NumPy array.
        clip_limit: Threshold for contrast limiting.
        tile_grid: Size of the grid for histogram equalisation (NxN).

    Returns:
        Contrast-enhanced BGR image.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid, tile_grid))
    l_enhanced = clahe.apply(l_channel)

    enhanced = cv2.merge([l_enhanced, a, b])
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)


# ---------------------------------------------------------------------------
# Resize
# ---------------------------------------------------------------------------

def resize_image(image: np.ndarray, size: int = 224) -> np.ndarray:
    """Resize image to (size x size) using high-quality Lanczos interpolation."""
    return cv2.resize(image, (size, size), interpolation=cv2.INTER_LANCZOS4)


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

def preprocess_image(
    image_path: str | Path,
    output_path: str | Path,
    image_size: int = 224,
    apply_contrast: bool = True,
) -> bool:
    """
    Run the full preprocessing pipeline on a single fundus image.

    Args:
        image_path: Path to the raw input image.
        output_path: Destination path for the processed image.
        image_size: Target spatial resolution in pixels.
        apply_contrast: Whether to apply CLAHE contrast enhancement.

    Returns:
        True if the image was processed and saved; False if it failed quality checks.
    """
    image = cv2.imread(str(image_path))
    if image is None:
        return False

    if not is_valid_image(image):
        return False

    image = crop_to_fundus(image)

    if apply_contrast:
        image = apply_clahe(image)

    image = resize_image(image, size=image_size)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)
    return True


def preprocess_dataset(
    raw_dir: str | Path,
    processed_dir: str | Path,
    image_size: int = 224,
    extensions: tuple[str, ...] = (".png", ".jpg", ".jpeg", ".tiff"),
) -> dict[str, int]:
    """
    Batch-preprocess all fundus images in *raw_dir* and write results to
    *processed_dir*, preserving the original sub-directory structure.

    Args:
        raw_dir: Root directory containing raw fundus images.
        processed_dir: Root directory for processed output images.
        image_size: Target spatial resolution in pixels.
        extensions: Accepted image file extensions.

    Returns:
        Dict with counts: {"processed": N, "skipped": M}.
    """
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)

    counts = {"processed": 0, "skipped": 0}

    image_paths = [p for p in raw_dir.rglob("*") if p.suffix.lower() in extensions]

    for img_path in image_paths:
        relative = img_path.relative_to(raw_dir)
        out_path = processed_dir / relative

        success = preprocess_image(img_path, out_path, image_size=image_size)
        if success:
            counts["processed"] += 1
        else:
            counts["skipped"] += 1

    return counts
