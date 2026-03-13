"""Patient-level k-fold cross-validation for fundus datasets."""

from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedKFold, KFold


def extract_patient_id(filename: str, dataset_name: str) -> str:
    """Extract a stable patient identifier from an image filename.

    Args:
        filename: Image filename or path stem (with or without extension).
            Examples: "10_left.jpeg", "000c1434d8d7.png", "IDRiD_001.jpg".
        dataset_name: One of "eyepacs", "aptos2019", "idrid".

    Returns:
        Patient ID string.

    Raises:
        ValueError: If dataset_name is not recognised.
    """
    stem = Path(filename).stem  # strip extension if present
    if dataset_name == "eyepacs":
        # "10_left" → "10", "13_right" → "13"
        return stem.split("_")[0]
    elif dataset_name == "aptos2019":
        # id_code is the full stem — one image per patient
        return stem
    elif dataset_name == "idrid":
        # "IDRiD_001" → use full stem as patient ID
        return stem
    else:
        raise ValueError(
            f"Unknown dataset_name '{dataset_name}'. "
            "Expected one of: eyepacs, aptos2019, idrid."
        )


class PatientLevelKFold:
    """5-fold cross-validation with strict patient-level split.

    Groups images by patient_id so that both eyes of the same patient
    are always in the same fold. Stratification is performed on the
    patient's most severe DR grade.

    Args:
        n_folds: Number of CV folds. Default: 5.
        seed: Random seed for reproducibility. Default: 42.
        stratified: Whether to use stratified splitting. Default: True.
    """

    def __init__(self, n_folds: int = 5, seed: int = 42, stratified: bool = True) -> None:
        self.n_folds = n_folds
        self.seed = seed
        self.stratified = stratified

    def split(
        self,
        image_paths: list[str],
        labels: list[int],
        patient_ids: list[str],
    ) -> list[tuple[list[int], list[int]]]:
        """Generate train/test index splits at the image level.

        Groups images by patient, assigns each patient a primary label
        (maximum DR grade across their images), performs k-fold on
        patients, then expands back to per-image indices.

        Args:
            image_paths: List of image file paths (unused directly, kept
                         for API consistency).
            labels: Integer DR grade per image (0–4).
            patient_ids: Patient identifier per image (one-to-many).

        Returns:
            List of (train_indices, test_indices) tuples, one per fold.
            Indices refer to positions in the original image_paths list.
        """
        # Map patient → list of image indices
        patient_to_indices: dict[str, list[int]] = defaultdict(list)
        for img_idx, pid in enumerate(patient_ids):
            patient_to_indices[pid].append(img_idx)

        # Assign each patient their most severe grade (max label)
        unique_patients = list(patient_to_indices.keys())
        patient_labels = [
            max(labels[i] for i in patient_to_indices[pid])
            for pid in unique_patients
        ]
        patient_arr = np.array(unique_patients)
        label_arr = np.array(patient_labels)

        if self.stratified:
            splitter = StratifiedKFold(
                n_splits=self.n_folds, shuffle=True, random_state=self.seed
            )
            fold_iter = splitter.split(patient_arr, label_arr)
        else:
            splitter = KFold(
                n_splits=self.n_folds, shuffle=True, random_state=self.seed
            )
            fold_iter = splitter.split(patient_arr)

        folds: list[tuple[list[int], list[int]]] = []
        for train_patient_idx, test_patient_idx in fold_iter:
            train_patients = set(patient_arr[train_patient_idx])
            test_patients = set(patient_arr[test_patient_idx])

            train_img_idx = [
                i for i, pid in enumerate(patient_ids) if pid in train_patients
            ]
            test_img_idx = [
                i for i, pid in enumerate(patient_ids) if pid in test_patients
            ]
            folds.append((train_img_idx, test_img_idx))

        return folds

    def verify_no_leakage(
        self,
        splits: list[tuple[list[int], list[int]]],
        patient_ids: list[str],
    ) -> bool:
        """Check that no patient appears in both train and test of any fold.

        Args:
            splits: Output of split() — list of (train_indices, test_indices).
            patient_ids: Patient identifier per image index.

        Returns:
            True if no leakage is detected across all folds.
        """
        for fold_idx, (train_idx, test_idx) in enumerate(splits):
            train_patients = {patient_ids[i] for i in train_idx}
            test_patients = {patient_ids[i] for i in test_idx}
            overlap = train_patients & test_patients
            if overlap:
                print(
                    f"[LEAKAGE] Fold {fold_idx}: {len(overlap)} patient(s) in "
                    f"both train and test: {list(overlap)[:5]}"
                )
                return False
        return True
