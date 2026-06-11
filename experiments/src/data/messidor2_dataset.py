"""Messidor-2 dataset for DR classification.

Messidor-2 provides ~1,748 fundus images with adjudicated 5-class DR grades.
Used in Experiment 5 (Clinical Degradation Resistance, H-7) and as the Topcon
camera group in Experiment 6 (device domain shift).

Camera: Topcon.
Grades: ``messidor_data.csv`` ships adjudicated 5-class DR grades (0–4) in the
``adjudicated_dr_grade`` column, plus an ``adjudicated_gradable`` flag. Ungradable
images (flag == 0, grade blank) are dropped.

Disk layout (E:/datasets/Messidor-2):
    IMAGES/<image_id>.png
    messidor_data.csv   columns: image_id, adjudicated_dr_grade,
                                 adjudicated_dme, adjudicated_gradable
"""

from pathlib import Path
from typing import Callable

import pandas as pd

from src.data.datasets import BaseFundusDataset, _apply_subset


class Messidor2Dataset(BaseFundusDataset):
    """Dataset class for Messidor-2 fundus images (5-class DR grading).

    Args:
        image_paths: Absolute paths to ``.png`` images.
        labels: DR grade labels (0–4).
        patient_ids: One id_code per image (defaults to the file stem).
        preprocessing: Optional preprocessing callable.
        augmentation: Optional augmentation callable.
    """

    def __init__(
        self,
        image_paths: list[str],
        labels: list[int],
        patient_ids: list[str],
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> None:
        super().__init__(image_paths, labels, preprocessing, augmentation)
        self.patient_ids = patient_ids

    @classmethod
    def from_directory(
        cls,
        root: str | Path,
        labels_csv: str | Path,
        subset_indices: list[int] | None = None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
        require_gradable: bool = True,
    ) -> "Messidor2Dataset":
        """Build the dataset from the Messidor-2 directory layout.

        Args:
            root: Path to the ``IMAGES/`` directory.
            labels_csv: Path to ``messidor_data.csv`` (columns: image_id,
                adjudicated_dr_grade, adjudicated_dme, adjudicated_gradable).
            subset_indices: Optional row indices applied AFTER gradable
                filtering (used for smoke tests).
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.
            require_gradable: Drop rows with ``adjudicated_gradable != 1`` or a
                blank DR grade. Default ``True``.

        Returns:
            Constructed :class:`Messidor2Dataset`.
        """
        root = Path(root)
        df = pd.read_csv(labels_csv)

        if "image_id" not in df.columns or "adjudicated_dr_grade" not in df.columns:
            raise ValueError(
                f"Messidor-2 CSV at {str(labels_csv)!r} must contain columns "
                f"'image_id' and 'adjudicated_dr_grade'. Got {list(df.columns)}."
            )

        # Drop ungradable / blank-grade rows before indexing.
        df = df[df["adjudicated_dr_grade"].notna()]
        if require_gradable and "adjudicated_gradable" in df.columns:
            df = df[df["adjudicated_gradable"] == 1]
        df = df.reset_index(drop=True)

        image_paths: list[str] = []
        labels: list[int] = []
        patient_ids: list[str] = []
        for _, row in df.iterrows():
            image_id = str(row["image_id"]).strip()
            img_path = root / image_id
            if not img_path.exists():
                continue
            grade = int(row["adjudicated_dr_grade"])
            image_paths.append(str(img_path))
            labels.append(min(max(grade, 0), 4))   # clip to 5-class taxonomy
            patient_ids.append(Path(image_id).stem)

        image_paths, labels, patient_ids = _apply_subset(
            image_paths, labels, patient_ids, subset_indices
        )
        return cls(image_paths, labels, patient_ids, preprocessing, augmentation)
