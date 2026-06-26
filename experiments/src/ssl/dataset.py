"""Label-free SSL datasets + the leakage-invariant assertion (brief §2, §3).

- :class:`EyePACSSSLDataset` — reads the EyePACS original *test* split
  (53,576 images) label-free and returns **two augmented views** per item
  (the SSL positive pair), built on top of the project's deterministic
  Stage 0–5 preprocessing at 256² (the SSL base tensor).
- :class:`EyePACSProbeDataset` — reads ``testLabels15.csv`` *with* labels for
  the §8 linear-probe gate (a separate evaluation, never the pretext task),
  carving the slice by the ``Usage`` column.
- :func:`assert_ssl_corpus_disjoint` — enforces INV-SSL-2: the SSL corpus
  (``test/``) shares no image stem and no patient id with Exp-1's ``train/``
  corpus. Raises loudly on any overlap.

All paths come from config; nothing is hardcoded (project rule). Images are
loaded with ``cv2.imread`` (BGR); the preprocessing pipeline converts BGR→RGB on
entry, so we never double-convert.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from src.preprocessing.config import PreprocessingConfig
from src.preprocessing.pipeline import PreprocessingPipeline
from src.preprocessing.polar_clahe import PolarClaheParams, apply_polar_clahe
from src.preprocessing.upgraded_clahe import ClaheParams, maybe_apply_clahe


# ---------------------------------------------------------------------------
# Corpus indexing helpers
# ---------------------------------------------------------------------------

def _eye_side_from_name(name: str) -> str:
    """Return ``"left"``/``"right"``/``"unknown"`` from an EyePACS stem."""
    if "_left" in name:
        return "left"
    if "_right" in name:
        return "right"
    return "unknown"


def index_eyepacs_split(
    image_dir: str | Path,
    labels_csv: str | Path,
    image_glob_suffix: str = ".jpeg",
    subset_size: int | None = None,
) -> tuple[list[str], list[int], list[str], list[str]]:
    """Index an EyePACS split from its labels CSV, mirroring the Exp-1 loader.

    Enumerates rows of ``labels_csv`` (column ``image``), forms
    ``image_dir/<name><suffix>``, and skips rows whose file is missing so a
    partial download does not crash the run (matches
    ``EyePACSDataset.from_directory``).

    Args:
        image_dir: Directory holding ``<name><suffix>`` images.
        labels_csv: CSV with at least an ``image`` column (and ``level`` if
            labels are present; ``level`` is read but UNUSED by the SSL objective).
        image_glob_suffix: File suffix, e.g. ``".jpeg"``.
        subset_size: If set, use only the first N CSV rows (smoke tests).

    Returns:
        Tuple ``(image_paths, labels, patient_ids, eye_sides)``. ``labels`` are
        ``-1`` placeholders when the CSV has no ``level`` column.
    """
    image_dir = Path(image_dir)
    df = pd.read_csv(labels_csv)
    if subset_size is not None:
        df = df.iloc[:subset_size].reset_index(drop=True)

    has_level = "level" in df.columns
    paths: list[str] = []
    labels: list[int] = []
    pids: list[str] = []
    sides: list[str] = []
    for _, row in df.iterrows():
        name = str(row["image"])
        img_path = image_dir / f"{name}{image_glob_suffix}"
        if not img_path.exists():
            continue
        paths.append(str(img_path))
        labels.append(int(row["level"]) if has_level else -1)
        pids.append(name.split("_")[0])
        sides.append(_eye_side_from_name(name))
    return paths, labels, pids, sides


def _stems_and_patients(labels_csv: str | Path) -> tuple[set[str], set[str]]:
    """Read image stems and patient ids from a labels CSV ``image`` column."""
    df = pd.read_csv(labels_csv)
    stems = {str(v) for v in df["image"].tolist()}
    patients = {s.split("_")[0] for s in stems}
    return stems, patients


def assert_ssl_corpus_disjoint(
    eyepacs_root: str | Path,
    test_labels_csv: str,
    train_labels_csv: str,
) -> dict[str, Any]:
    """Enforce INV-SSL-2: SSL ``test/`` corpus is disjoint from Exp-1 ``train/``.

    Builds image-stem and patient-id sets for both corpora from their labels
    CSVs and asserts the SSL set shares **no image stem and no patient id** with
    the Exp-1 set. Raises (never warns-and-continues) on any overlap, listing the
    offending ids (brief §3.3).

    Args:
        eyepacs_root: EyePACS dataset root (``paths.eyepacs`` from config).
        test_labels_csv: SSL labels CSV filename joined onto ``eyepacs_root``
            (e.g. ``"testLabels15.csv"``).
        train_labels_csv: Exp-1 labels CSV filename joined onto ``eyepacs_root``
            (e.g. ``"trainLabels.csv"``).

    Returns:
        Audit dict ``{ssl_count, train_count, ssl_patients, train_patients,
        disjoint: True}`` for the run manifest.

    Raises:
        FileNotFoundError: If either labels CSV is missing.
        AssertionError: If any image stem or patient id is shared.
    """
    root = Path(eyepacs_root)
    test_csv = root / test_labels_csv
    train_csv = root / train_labels_csv
    for p in (test_csv, train_csv):
        if not p.exists():
            raise FileNotFoundError(f"Labels CSV not found: {p}")

    ssl_stems, ssl_patients = _stems_and_patients(test_csv)
    train_stems, train_patients = _stems_and_patients(train_csv)

    stem_overlap = ssl_stems & train_stems
    patient_overlap = ssl_patients & train_patients
    if stem_overlap or patient_overlap:
        raise AssertionError(
            "INV-SSL-2 VIOLATION — SSL corpus overlaps Exp-1 train corpus.\n"
            f"  shared image stems ({len(stem_overlap)}): "
            f"{sorted(stem_overlap)[:20]}\n"
            f"  shared patient ids ({len(patient_overlap)}): "
            f"{sorted(patient_overlap)[:20]}"
        )

    return {
        "ssl_count": len(ssl_stems),
        "train_count": len(train_stems),
        "ssl_patients": len(ssl_patients),
        "train_patients": len(train_patients),
        "disjoint": True,
    }


# ---------------------------------------------------------------------------
# Preprocessing factory for the SSL base tensor (Stages 0–5 at 256²)
# ---------------------------------------------------------------------------

def build_ssl_base_pipeline(
    preprocessing_cfg: dict[str, Any] | None,
    target_size: int,
) -> PreprocessingPipeline:
    """Build the deterministic Stage 0–5 pipeline for the SSL base tensor (§4.1).

    Runs in inference mode (``is_training=False``) so Stage 5 CLAHE is
    deterministic and Stage 6 augmentation is skipped — SSL view stochasticity
    comes solely from :class:`~src.ssl.transforms.TwoViewTransform` (§4.3). The
    Stage-2 target size is set to ``target_size`` (256 for SSL).

    Args:
        preprocessing_cfg: The project's ``preprocessing`` config dict
            (``config["preprocessing"]``), or ``None`` to use the full-pipeline
            preset defaults.
        target_size: Stage-2 output resolution (256 for SSL).

    Returns:
        An inference-mode :class:`PreprocessingPipeline`.
    """
    if preprocessing_cfg:
        config = PreprocessingConfig.from_dict(preprocessing_cfg)
    else:
        config = PreprocessingConfig.from_preset("efficientnet")
    config.target_size = int(target_size)
    config.mode = "full"
    return PreprocessingPipeline.create_for_inference(config)


# ---------------------------------------------------------------------------
# Two-view label-free SSL dataset
# ---------------------------------------------------------------------------

class EyePACSSSLDataset(Dataset):
    """Label-free EyePACS *test*-split dataset returning two augmented views.

    Each ``__getitem__`` builds the deterministic Stage 0–5 base 4-channel
    tensor (RGB in ``[0, 1]`` + binary FOV mask) at ``target_size`` and applies
    :class:`~src.ssl.transforms.TwoViewTransform` to yield the SSL positive pair
    ``(v1, v2)``. Labels are never read (the pretext task is label-free).

    Args:
        image_paths: Absolute paths to ``test/<name>.jpeg`` images.
        patient_ids: Patient id per image (numeric prefix).
        eye_sides: ``"left"``/``"right"``/``"unknown"`` per image.
        preprocessing: Inference pipeline from :func:`build_ssl_base_pipeline`.
        transform: A :class:`~src.ssl.transforms.TwoViewTransform`.
    """

    def __init__(
        self,
        image_paths: list[str],
        patient_ids: list[str],
        eye_sides: list[str],
        preprocessing: PreprocessingPipeline,
        transform: Callable[[torch.Tensor], tuple[torch.Tensor, torch.Tensor]],
    ) -> None:
        self.image_paths = image_paths
        self.patient_ids = patient_ids
        self.eye_sides = eye_sides
        self.preprocessing = preprocessing
        self.transform = transform

        cfg = preprocessing.config
        self._polar_params = PolarClaheParams(
            clip_factor=cfg.clahe_clip_factor,
            global_threshold=cfg.clahe_global_threshold,
            radial_rings=cfg.clahe_radial_rings,
            radial_exponent=cfg.clahe_radial_exponent,
            fine_bins=cfg.clahe_fine_bins,
            min_sector_area_frac=cfg.clahe_min_sector_area_frac,
        )
        self._tile_params = ClaheParams(
            tile_grid_size=cfg.clahe_tile_grid_size,
            clip_factor=cfg.clahe_clip_factor,
            global_threshold=cfg.clahe_global_threshold,
        )

    def __len__(self) -> int:
        return len(self.image_paths)

    def _base_tensor(self, idx: int) -> torch.Tensor:
        """Build the deterministic Stage 0–5 base 4-channel tensor for index.

        Args:
            idx: Sample index.

        Returns:
            Float tensor ``(4, H, W)`` — RGB in ``[0, 1]``, mask in ``{0, 1}``.
        """
        img_bgr = cv2.imread(str(self.image_paths[idx]))
        if img_bgr is None:
            raise FileNotFoundError(f"Could not load image: {self.image_paths[idx]}")

        flat_rgb, fov_mask, _confident, _rot, fovea_pivot = (
            self.preprocessing.precompute_deterministic(img_bgr, self.eye_sides[idx])
        )

        cfg = self.preprocessing.config
        if cfg.use_clahe and cfg.clahe_mode == "polar":
            base_rgb = apply_polar_clahe(
                flat_rgb, fov_mask, params=self._polar_params, fovea_xy=fovea_pivot
            )
        elif cfg.use_clahe:
            base_rgb = maybe_apply_clahe(
                flat_rgb, params=self._tile_params,
                is_training=False, train_prob=cfg.clahe_train_prob,
            )
        else:
            base_rgb = flat_rgb

        rgb01 = torch.from_numpy(
            np.ascontiguousarray(base_rgb.astype(np.float32) / 255.0).transpose(2, 0, 1)
        )
        mask = torch.from_numpy(np.ascontiguousarray(fov_mask.astype(np.float32))).unsqueeze(0)
        return torch.cat([rgb01, mask], dim=0)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Return the SSL positive pair ``(view1, view2)`` for one image.

        Args:
            idx: Sample index.

        Returns:
            Tuple of two normalized 4-channel view tensors.
        """
        return self.transform(self._base_tensor(idx))

    @classmethod
    def from_config(
        cls,
        config: dict[str, Any],
        transform: Callable[[torch.Tensor], tuple[torch.Tensor, torch.Tensor]],
        subset_size: int | None = None,
    ) -> "EyePACSSSLDataset":
        """Build from the project config, reading the SSL corpus paths (§3.1).

        Args:
            config: Full config dict (must contain ``paths.eyepacs`` and the
                ``ssl.corpus`` block).
            transform: A configured :class:`TwoViewTransform`.
            subset_size: Optional row cap for smoke tests.

        Returns:
            Constructed :class:`EyePACSSSLDataset`.
        """
        ssl_cfg = config["ssl"]
        corpus = ssl_cfg["corpus"]
        eyepacs_root = Path(config["paths"]["eyepacs"])
        test_dir = eyepacs_root / corpus["eyepacs_test_dir"]
        test_labels = eyepacs_root / corpus["test_labels_csv"]
        suffix = corpus.get("image_glob", "*.jpeg").replace("*", "")

        paths, _labels, pids, sides = index_eyepacs_split(
            test_dir, test_labels, image_glob_suffix=suffix, subset_size=subset_size
        )
        preprocessing = build_ssl_base_pipeline(
            config.get("preprocessing"), int(ssl_cfg.get("image_size", 256))
        )
        return cls(paths, pids, sides, preprocessing, transform)


# ---------------------------------------------------------------------------
# Labelled probe dataset (linear-probe gate, §8)
# ---------------------------------------------------------------------------

class EyePACSProbeDataset(Dataset):
    """Labelled single-view EyePACS *test*-split dataset for the probe gate.

    Returns ``(tensor, label)`` where ``tensor`` is the deterministic 4-channel
    pipeline output (Stages 0–5 + Stage-7 normalize) at the probe resolution.
    Labels come from ``testLabels15.csv`` — permitted here because the probe is a
    separate evaluation, not the SSL objective (§8.1).

    Args:
        image_paths: Absolute paths to ``test/<name>.jpeg`` images.
        labels: DR grade labels (0–4).
        eye_sides: ``"left"``/``"right"``/``"unknown"`` per image.
        preprocessing: Inference pipeline (full mode) producing a 4-channel
            normalized tensor via ``__call__``.
    """

    def __init__(
        self,
        image_paths: list[str],
        labels: list[int],
        eye_sides: list[str],
        preprocessing: PreprocessingPipeline,
    ) -> None:
        self.image_paths = image_paths
        self.labels = labels
        self.eye_sides = eye_sides
        self.preprocessing = preprocessing

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        """Return ``(normalized_4ch_tensor, label)`` for one image.

        Args:
            idx: Sample index.

        Returns:
            Tuple of the 4-channel tensor and the integer DR grade.
        """
        img_bgr = cv2.imread(str(self.image_paths[idx]))
        if img_bgr is None:
            raise FileNotFoundError(f"Could not load image: {self.image_paths[idx]}")
        tensor = self.preprocessing(img_bgr, eye_side=self.eye_sides[idx])
        return tensor, self.labels[idx]

    @classmethod
    def build_probe_splits(
        cls,
        config: dict[str, Any],
        subset_size: int | None = None,
    ) -> tuple["EyePACSProbeDataset", "EyePACSProbeDataset"]:
        """Carve probe-train / probe-test by the ``Usage`` column (§8.1).

        Probe-train = rows with ``Usage == probe.holdout_usage`` complement;
        probe-test = rows with ``Usage == probe.holdout_usage`` (default
        ``"Private"``). Falls back to a seed-42 stratified 80/20 split if the
        ``Usage`` column is absent.

        Args:
            config: Full config dict (``paths.eyepacs``, ``ssl`` block).
            subset_size: Optional row cap for smoke tests.

        Returns:
            Tuple ``(probe_train_ds, probe_test_ds)``.
        """
        ssl_cfg = config["ssl"]
        corpus = ssl_cfg["corpus"]
        probe_cfg = ssl_cfg.get("probe", {})
        holdout_usage = probe_cfg.get("holdout_usage", "Private")

        eyepacs_root = Path(config["paths"]["eyepacs"])
        test_dir = eyepacs_root / corpus["eyepacs_test_dir"]
        test_labels = eyepacs_root / corpus["test_labels_csv"]
        suffix = corpus.get("image_glob", "*.jpeg").replace("*", "")

        df = pd.read_csv(test_labels)
        if subset_size is not None:
            df = df.iloc[:subset_size].reset_index(drop=True)

        if "Usage" in df.columns:
            test_mask = df["Usage"].astype(str).str.lower() == str(holdout_usage).lower()
        else:
            rng = np.random.default_rng(config.get("seed", 42))
            test_mask = rng.random(len(df)) < 0.2

        preprocessing = build_ssl_base_pipeline(
            config.get("preprocessing"),
            int(probe_cfg.get("image_size", ssl_cfg.get("image_size", 256))),
        )

        def _make(sub: pd.DataFrame) -> "EyePACSProbeDataset":
            paths, labels, sides = [], [], []
            for _, row in sub.iterrows():
                name = str(row["image"])
                p = test_dir / f"{name}{suffix}"
                if not p.exists():
                    continue
                paths.append(str(p))
                labels.append(int(row["level"]))
                sides.append(_eye_side_from_name(name))
            return cls(paths, labels, sides, preprocessing)

        train_ds = _make(df[~test_mask].reset_index(drop=True))
        test_ds = _make(df[test_mask].reset_index(drop=True))
        return train_ds, test_ds
