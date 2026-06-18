"""IDRiD localization data loading + target-heatmap rendering.

Responsibilities:
  * parse the IDRiD OD-center and fovea-center markup CSVs (original-image
    pixel coordinates);
  * FOV-crop + isotropic-resize each image to the input frame, transforming the
    GT coordinates through the *same* affine;
  * render 2D-Gaussian target heatmaps on the decoder output grid;
  * apply aggressive, geometry-consistent augmentation (image + coordinates).

Training uses the **413-image Training Set only**. The 103-image Testing Set is
a held-out honest test set and is never loaded by the training dataset. A
held-out slice of TRAIN (``val_fraction``) is used for early stopping and
threshold calibration.

The torch ``Dataset`` is only defined when torch is importable; the CSV parser,
coordinate transform, and heatmap rendering are pure numpy so they can be
unit-tested without torch.
"""

from __future__ import annotations

import csv
import math
import pathlib
from dataclasses import dataclass

import cv2
import numpy as np

from .geometry import FovTransform, crop_and_resize, render_gaussian_heatmap

try:
    import torch
    from torch.utils.data import Dataset
    _HAS_TORCH = True
except Exception:  # pragma: no cover
    torch = None  # type: ignore
    Dataset = object  # type: ignore
    _HAS_TORCH = False


# Relative paths inside the "C. Localization" tree (match the monorepo harness).
_OD_CSV = {
    "train": "2. Groundtruths/1. Optic Disc Center Location/"
             "a. IDRiD_OD_Center_Training Set_Markups.csv",
    "test": "2. Groundtruths/1. Optic Disc Center Location/"
            "b. IDRiD_OD_Center_Testing Set_Markups.csv",
}
_FOVEA_CSV = {
    "train": "2. Groundtruths/2. Fovea Center Location/"
             "IDRiD_Fovea_Center_Training Set_Markups.csv",
    "test": "2. Groundtruths/2. Fovea Center Location/"
            "IDRiD_Fovea_Center_Testing Set_Markups.csv",
}
_IMAGES_DIR = {
    "train": "1. Original Images/a. Training Set",
    "test": "1. Original Images/b. Testing Set",
}


@dataclass
class Sample:
    """One annotated IDRiD image (paths + GT in original-image pixels).

    Attributes:
        image_id: e.g. ``"IDRiD_001"``.
        image_path: Path to the JPEG.
        od_xy: OD center ``(x, y)`` in original-image pixels.
        fovea_xy: Fovea center ``(x, y)`` in original-image pixels.
    """

    image_id: str
    image_path: pathlib.Path
    od_xy: tuple[float, float]
    fovea_xy: tuple[float, float]


def parse_markup_csv(path: pathlib.Path) -> dict[str, tuple[float, float]]:
    """Parse an IDRiD localization markup CSV into ``{image_no: (x, y)}``.

    Only the first three fields (``Image No``, ``X- Coordinate``,
    ``Y - Coordinate``) are read; rows whose first cell is not an ``IDRiD_*``
    id are skipped.

    Args:
        path: Path to the markup CSV.

    Returns:
        Mapping from image id to ``(x, y)`` in original-image pixels.
    """
    out: dict[str, tuple[float, float]] = {}
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 3:
                continue
            name = row[0].strip()
            if not name.startswith("IDRiD_"):
                continue
            try:
                x, y = float(row[1]), float(row[2])
            except ValueError:
                continue
            out[name] = (x, y)
    return out


def load_split(root: pathlib.Path, split: str) -> list[Sample]:
    """Load the annotated samples for one IDRiD split.

    Args:
        root: ``C. Localization`` directory.
        split: ``"train"`` or ``"test"``.

    Returns:
        List of :class:`Sample`, sorted by image id, for ids present in both
        the OD and fovea markup files and on disk.
    """
    od_gt = parse_markup_csv(root / _OD_CSV[split])
    fovea_gt = parse_markup_csv(root / _FOVEA_CSV[split])
    images_dir = root / _IMAGES_DIR[split]
    ids = sorted(set(od_gt) & set(fovea_gt))
    samples: list[Sample] = []
    for name in ids:
        img_path = images_dir / f"{name}.jpg"
        if not img_path.exists():
            continue
        samples.append(
            Sample(name, img_path, od_gt[name], fovea_gt[name])
        )
    return samples


def make_frame_targets(
    image_rgb: np.ndarray,
    od_xy: tuple[float, float],
    fovea_xy: tuple[float, float],
    input_size: int,
    heatmap_size: int,
    sigma: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, FovTransform]:
    """FOV-crop an image and build target heatmaps in the frame.

    Args:
        image_rgb: RGB uint8 array ``(H, W, 3)``.
        od_xy: OD center in original-image pixels.
        fovea_xy: Fovea center in original-image pixels.
        input_size: Square input frame side (e.g. 512).
        heatmap_size: Square decoder output side (e.g. 128).
        sigma: Gaussian target sigma in heatmap-grid pixels.

    Returns:
        Tuple of:
          * frame: RGB uint8 ``(input_size, input_size, 3)``.
          * heatmaps: float32 ``(2, heatmap_size, heatmap_size)`` (OD, fovea),
            each summing to 1.
          * coords_frame: float32 ``(2, 2)`` GT coords in *input-frame* pixels
            (OD, fovea), used by augmentation.
          * transform: the :class:`FovTransform`.
    """
    frame, _mask, transform = crop_and_resize(image_rgb, input_size)
    ratio = heatmap_size / input_size

    coords_frame = np.zeros((2, 2), dtype=np.float32)
    heatmaps = np.zeros((2, heatmap_size, heatmap_size), dtype=np.float32)
    for i, (x, y) in enumerate((od_xy, fovea_xy)):
        fx, fy = transform.apply(x, y)
        coords_frame[i] = (fx, fy)
        heatmaps[i] = render_gaussian_heatmap(fx * ratio, fy * ratio,
                                              heatmap_size, sigma)
    return frame, heatmaps, coords_frame, transform


# ---------------------------------------------------------------------------
# Augmentation (geometry-consistent on image + frame coordinates)
# ---------------------------------------------------------------------------
def _augment(
    frame: np.ndarray,
    coords_frame: np.ndarray,
    cfg: dict,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply geometry-consistent augmentation to a frame and its coords.

    Rotation/scale/translation/flip are applied as a single affine to both the
    image and the coordinates; photometric ops (brightness, contrast, gamma,
    color jitter, blur, vignette) touch only the image.

    Args:
        frame: RGB uint8 ``(S, S, 3)``.
        coords_frame: float32 ``(2, 2)`` coords in frame pixels.
        cfg: ``train.augmentation`` config dict.
        rng: NumPy random generator (seeded).

    Returns:
        ``(aug_frame, aug_coords)``.
    """
    s = frame.shape[0]
    angle = rng.uniform(-cfg["rotation_deg"], cfg["rotation_deg"])
    scale = rng.uniform(cfg["scale_min"], cfg["scale_max"])
    tx = rng.uniform(-cfg["translate_frac"], cfg["translate_frac"]) * s
    ty = rng.uniform(-cfg["translate_frac"], cfg["translate_frac"]) * s

    center = (s / 2.0, s / 2.0)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    M[0, 2] += tx
    M[1, 2] += ty
    frame = cv2.warpAffine(frame, M, (s, s), flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    pts = np.hstack([coords_frame, np.ones((2, 1), dtype=np.float32)])
    coords_frame = (M @ pts.T).T.astype(np.float32)

    if cfg.get("hflip") and rng.random() < 0.5:
        frame = frame[:, ::-1].copy()
        coords_frame[:, 0] = (s - 1) - coords_frame[:, 0]

    img = frame.astype(np.float32) / 255.0
    # Brightness / contrast.
    b = 1.0 + rng.uniform(-cfg["brightness"], cfg["brightness"])
    c = 1.0 + rng.uniform(-cfg["contrast"], cfg["contrast"])
    img = np.clip((img - 0.5) * c + 0.5 * b, 0.0, 1.0)
    # Gamma.
    g = rng.uniform(cfg["gamma_min"], cfg["gamma_max"])
    img = np.power(img, g)
    # Mild per-channel color jitter.
    cj = cfg["color_jitter"]
    img *= (1.0 + rng.uniform(-cj, cj, size=(1, 1, 3))).astype(np.float32)
    img = np.clip(img, 0.0, 1.0)
    # Mild Gaussian blur.
    if rng.random() < cfg["blur_prob"]:
        sig = rng.uniform(0.1, cfg["blur_sigma_max"])
        img = cv2.GaussianBlur(img, (0, 0), sig)
    # Simulated vignette (hardens against the old fovea failure mode).
    if rng.random() < cfg["vignette_prob"]:
        ys, xs = np.mgrid[0:s, 0:s].astype(np.float32)
        cx, cy = rng.uniform(0.3, 0.7) * s, rng.uniform(0.3, 0.7) * s
        r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / (s * 0.7)
        vig = 1.0 - cfg["vignette_strength"] * np.clip(r, 0, 1) ** 2
        img *= vig[..., None]

    frame = np.clip(img * 255.0, 0, 255).astype(np.uint8)
    return frame, coords_frame


if _HAS_TORCH:

    class IDRiDLocalizationDataset(Dataset):
        """IDRiD OD/fovea localization dataset for heatmap regression.

        Yields ``(image_tensor, heatmaps, coords_norm)`` where ``image_tensor``
        is ``(3, S, S)`` float in ``[0, 1]``, ``heatmaps`` is
        ``(2, Hh, Hw)`` float summing to 1 per channel, and ``coords_norm`` is
        ``(2, 2)`` normalized ``[-1, 1]`` GT coords (for the DSNT euclidean
        term).
        """

        def __init__(
            self,
            samples: list[Sample],
            input_size: int,
            heatmap_size: int,
            sigma: float,
            augment_cfg: dict | None = None,
            seed: int = 42,
        ) -> None:
            """Initialize the dataset.

            Args:
                samples: Annotated samples (TRAIN only for training).
                input_size: Input frame side.
                heatmap_size: Decoder output side.
                sigma: Gaussian target sigma in heatmap pixels.
                augment_cfg: ``train.augmentation`` config; ``None`` disables
                    augmentation (validation pass).
                seed: Base RNG seed.
            """
            self.samples = samples
            self.input_size = input_size
            self.heatmap_size = heatmap_size
            self.sigma = sigma
            self.augment_cfg = augment_cfg
            self.seed = seed

        def __len__(self) -> int:
            return len(self.samples)

        def __getitem__(self, idx: int):
            sample = self.samples[idx]
            img_bgr = cv2.imread(str(sample.image_path))
            if img_bgr is None:
                raise FileNotFoundError(sample.image_path)
            image_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

            frame, heatmaps, coords_frame, _t = make_frame_targets(
                image_rgb, sample.od_xy, sample.fovea_xy,
                self.input_size, self.heatmap_size, self.sigma,
            )
            if self.augment_cfg is not None:
                rng = np.random.default_rng(self.seed * 1_000_003 + idx)
                frame, coords_frame = _augment(frame, coords_frame,
                                               self.augment_cfg, rng)
                # Re-render heatmaps from augmented coords.
                ratio = self.heatmap_size / self.input_size
                heatmaps = np.zeros_like(heatmaps)
                for i in range(2):
                    heatmaps[i] = render_gaussian_heatmap(
                        coords_frame[i, 0] * ratio, coords_frame[i, 1] * ratio,
                        self.heatmap_size, self.sigma,
                    )

            # Normalized [-1, 1] coords for the euclidean DSNT term.
            coords_norm = np.zeros((2, 2), dtype=np.float32)
            coords_norm[:, 0] = 2.0 * coords_frame[:, 0] / self.input_size - 1.0
            coords_norm[:, 1] = 2.0 * coords_frame[:, 1] / self.input_size - 1.0

            img_t = torch.from_numpy(
                frame.astype(np.float32).transpose(2, 0, 1) / 255.0
            )
            hm_t = torch.from_numpy(heatmaps)
            cn_t = torch.from_numpy(coords_norm)
            return img_t, hm_t, cn_t
