"""Clinical (Kazakh) dataset for DR classification.

60 fundus images from 30 patients (2 eyes each), 5-class DR staging.
Balanced: 12 images per class. PNG format.

Disk layout (E:/datasets/clinical):
    images/<image_id>.png            e.g. patient001_L.png
    metadata.csv                     columns: image_id, patient_id, eye, grade

Used in Experiments 4 (qualitative Grad-CAM), 5 (clinical degradation,
optional), and 7 (small-data test set).
"""

from pathlib import Path
from typing import Callable

import pandas as pd

from src.data.datasets import BaseFundusDataset, _apply_subset


class ClinicalDataset(BaseFundusDataset):
    """Dataset class for Kazakh clinical fundus images (5-class DR grading).

    Args:
        image_paths: Absolute paths to ``.png`` images.
        labels: DR grade labels (0–4).
        patient_ids: One patient id per image (left/right eyes of the same
            patient share an id, enabling patient-level CV without leakage).
        eye_sides: ``"L"`` / ``"R"`` per image (empty list if unavailable).
        preprocessing: Optional preprocessing callable.
        augmentation: Optional augmentation callable.
    """

    def __init__(
        self,
        image_paths: list[str],
        labels: list[int],
        patient_ids: list[str],
        eye_sides: list[str] | None = None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> None:
        super().__init__(image_paths, labels, preprocessing, augmentation)
        self.patient_ids = patient_ids
        self.eye_sides: list[str] = eye_sides if eye_sides is not None else []

    @classmethod
    def from_directory(
        cls,
        root: str | Path,
        labels_csv: str | Path | None = None,
        images_subdir: str = "images",
        subset_indices: list[int] | None = None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> "ClinicalDataset":
        """Build the dataset from the clinical directory layout.

        Args:
            root: Path to the clinical dataset directory.
            labels_csv: Path to the metadata CSV (columns: image_id,
                patient_id, eye, grade). Defaults to ``root/metadata.csv``.
            images_subdir: Sub-directory holding the images. Default ``images``.
            subset_indices: Optional row indices applied after loading (smoke
                tests).
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.

        Returns:
            Constructed :class:`ClinicalDataset`.
        """
        root = Path(root)
        labels_csv = Path(labels_csv) if labels_csv is not None else root / "metadata.csv"
        images_root = root / images_subdir

        df = pd.read_csv(labels_csv)
        required = {"image_id", "grade"}
        if not required.issubset(df.columns):
            raise ValueError(
                f"Clinical metadata at {str(labels_csv)!r} must contain columns "
                f"{required}. Got {list(df.columns)}."
            )

        image_paths: list[str] = []
        labels: list[int] = []
        patient_ids: list[str] = []
        eye_sides: list[str] = []
        for _, row in df.iterrows():
            image_id = str(row["image_id"]).strip()
            img_path = images_root / image_id
            if not img_path.exists():
                continue
            image_paths.append(str(img_path))
            labels.append(min(max(int(row["grade"]), 0), 4))   # clip to 5-class
            # patient_id column if present, else strip the _L/_R eye suffix.
            if "patient_id" in df.columns and pd.notna(row["patient_id"]):
                patient_ids.append(str(row["patient_id"]).strip())
            else:
                patient_ids.append(Path(image_id).stem.rsplit("_", 1)[0])
            eye_sides.append(
                str(row["eye"]).strip() if "eye" in df.columns and pd.notna(row.get("eye"))
                else ""
            )

        image_paths, labels, patient_ids = _apply_subset(
            image_paths, labels, patient_ids, subset_indices
        )
        if subset_indices is not None:
            eye_sides = [eye_sides[i] for i in subset_indices]

        return cls(
            image_paths, labels, patient_ids, eye_sides,
            preprocessing, augmentation,
        )
