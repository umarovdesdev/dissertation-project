"""Fundus image dataset classes for DR classification."""

from pathlib import Path
from typing import Callable

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class BaseFundusDataset(Dataset):
    """Base dataset for fundus images.

    Handles image loading, optional preprocessing, optional augmentation,
    and conversion to float32 CHW tensors.

    Args:
        image_paths: List of absolute paths to image files.
        labels: List of integer DR grade labels (0–4).
        preprocessing: Optional callable applied to the raw BGR uint8 image.
            Expected to return a numpy array (uint8 or float32 [0,1]).
        augmentation: Optional callable applied after preprocessing.
            Expected to return a numpy array of the same dtype/range.
    """

    def __init__(
        self,
        image_paths: list[str],
        labels: list[int],
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> None:
        if len(image_paths) != len(labels):
            raise ValueError(
                f"image_paths and labels must have equal length, "
                f"got {len(image_paths)} and {len(labels)}"
            )
        self.image_paths = image_paths
        self.labels = labels
        self.preprocessing = preprocessing
        self.augmentation = augmentation

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        """Load and return one sample.

        Args:
            idx: Sample index.

        Returns:
            Tuple of (image_tensor, label) where image_tensor is float32
            with shape (C, H, W) and values in [0, 1].
        """
        image = cv2.imread(str(self.image_paths[idx]))
        if image is None:
            raise FileNotFoundError(f"Could not load image: {self.image_paths[idx]}")

        if self.preprocessing is not None:
            image = self.preprocessing(image)

        if self.augmentation is not None:
            image = self.augmentation(image)

        # Normalise to [0, 1] float32 only if still uint8
        if image.dtype == np.uint8:
            image = image.astype(np.float32) / 255.0
        else:
            image = image.astype(np.float32)

        # HWC → CHW
        tensor = torch.from_numpy(np.ascontiguousarray(image.transpose(2, 0, 1)))
        return tensor, self.labels[idx]


def _apply_subset(
    image_paths: list[str],
    labels: list[int],
    patient_ids: list[str],
    subset_indices: list[int] | None,
) -> tuple[list[str], list[int], list[str]]:
    """Filter lists to subset_indices if provided."""
    if subset_indices is None:
        return image_paths, labels, patient_ids
    return (
        [image_paths[i] for i in subset_indices],
        [labels[i] for i in subset_indices],
        [patient_ids[i] for i in subset_indices],
    )


class EyePACSDataset(BaseFundusDataset):
    """EyePACS fundus dataset (~88k images, 5-class DR grading).

    Patient ID = numeric prefix before _left / _right in the filename.
    Left and right eyes of the same patient share a patient_id, ensuring
    they are always assigned to the same CV fold.

    Args:
        image_paths: Absolute paths to .jpeg images.
        labels: DR grade labels (0–4).
        patient_ids: Numeric patient strings (e.g. "10").
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
    ) -> "EyePACSDataset":
        """Build dataset from EyePACS directory layout.

        Args:
            root: Path to the train/ image directory.
            labels_csv: Path to trainLabels.csv (columns: image, level).
                        Image names have no extension (e.g. "10_left").
            subset_indices: Optional list of row indices to load from the CSV.
                            If None, loads all rows.
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.

        Returns:
            Constructed EyePACSDataset with patient_ids attribute.
        """
        root = Path(root)
        df = pd.read_csv(labels_csv)
        if subset_indices is not None:
            df = df.iloc[subset_indices].reset_index(drop=True)

        image_paths, labels, patient_ids = [], [], []
        for _, row in df.iterrows():
            name: str = str(row["image"])
            img_path = root / f"{name}.jpeg"
            if not img_path.exists():
                continue
            image_paths.append(str(img_path))
            labels.append(int(row["level"]))
            patient_ids.append(name.split("_")[0])

        return cls(image_paths, labels, patient_ids, preprocessing, augmentation)


class APTOS2019Dataset(BaseFundusDataset):
    """APTOS 2019 Blindness Detection dataset (~3,662 images, 5-class DR).

    Each image corresponds to a unique patient.

    Args:
        image_paths: Absolute paths to .png images.
        labels: DR grade labels (0–4).
        patient_ids: id_code strings (one per image, equals patient ID).
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
    ) -> "APTOS2019Dataset":
        """Build dataset from APTOS 2019 directory layout.

        Args:
            root: Path to train_images/ directory.
            labels_csv: Path to train.csv (columns: id_code, diagnosis).
            subset_indices: Optional list of row indices to load from the CSV.
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.

        Returns:
            Constructed APTOS2019Dataset with patient_ids attribute.
        """
        root = Path(root)
        df = pd.read_csv(labels_csv)
        if subset_indices is not None:
            df = df.iloc[subset_indices].reset_index(drop=True)

        image_paths, labels, patient_ids = [], [], []
        for _, row in df.iterrows():
            id_code = str(row["id_code"])
            img_path = root / f"{id_code}.png"
            if not img_path.exists():
                continue
            image_paths.append(str(img_path))
            labels.append(int(row["diagnosis"]))
            patient_ids.append(id_code)

        return cls(image_paths, labels, patient_ids, preprocessing, augmentation)


class IDRiDDataset(BaseFundusDataset):
    """IDRiD disease grading dataset (~413 training images, 5-class DR).

    Also provides access to pixel-level lesion masks for the 54-image
    segmentation subset (Microaneurysms, Haemorrhages, Hard Exudates,
    Soft Exudates).

    Mask naming convention:
        Grading image IDRiD_XXX.jpg (3-digit) corresponds to mask
        IDRiD_YY_<suffix>.tif (2-digit) where YY = int(XXX).

    Args:
        image_paths: Absolute paths to .jpg images.
        labels: DR grade labels (0–4).
        patient_ids: Image name stems used as patient IDs.
        image_stems: Image name stems (e.g. "IDRiD_001") for mask lookup.
        masks_root: Root of segmentation groundtruths directory, or None.
        preprocessing: Optional preprocessing callable.
        augmentation: Optional augmentation callable.
    """

    LESION_DIRS: dict[str, str] = {
        "microaneurysms": "1. Microaneurysms",
        "haemorrhages": "2. Haemorrhages",
        "hard_exudates": "3. Hard Exudates",
        "soft_exudates": "4. Soft Exudates",
    }
    LESION_SUFFIXES: dict[str, str] = {
        "microaneurysms": "MA",
        "haemorrhages": "HE",
        "hard_exudates": "EX",
        "soft_exudates": "SE",
    }

    def __init__(
        self,
        image_paths: list[str],
        labels: list[int],
        patient_ids: list[str],
        image_stems: list[str],
        masks_root: Path | None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> None:
        super().__init__(image_paths, labels, preprocessing, augmentation)
        self.patient_ids = patient_ids
        self.image_stems = image_stems
        self.masks_root = masks_root

    @classmethod
    def from_directory(
        cls,
        root: str | Path,
        labels_csv: str | Path,
        subset_indices: list[int] | None = None,
        lesion_mask_dir: str | Path | None = None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> "IDRiDDataset":
        """Build dataset from IDRiD directory layout.

        Args:
            root: Path to grading images directory
                  (.../B. Disease Grading/1. Original Images/a. Training Set/).
            labels_csv: Path to grading training labels CSV.
            subset_indices: Optional list of row indices to load from the CSV.
            lesion_mask_dir: Path to segmentation groundtruths directory
                  (.../A. Segmentation/2. All Segmentation Groundtruths/a. Training Set/).
                  If None, mask loading is disabled.
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.

        Returns:
            Constructed IDRiDDataset with lesion mask support.
        """
        root = Path(root)
        labels_csv = Path(labels_csv)

        # CSV has trailing commas — use only the first 2 columns
        df = pd.read_csv(labels_csv, usecols=[0, 1])
        df.columns = ["image_name", "retinopathy_grade"]
        if subset_indices is not None:
            df = df.iloc[subset_indices].reset_index(drop=True)

        image_paths, labels, patient_ids, image_stems = [], [], [], []
        for _, row in df.iterrows():
            stem = str(row["image_name"]).strip()
            img_path = root / f"{stem}.jpg"
            if not img_path.exists():
                continue
            image_paths.append(str(img_path))
            labels.append(int(row["retinopathy_grade"]))
            patient_ids.append(stem)
            image_stems.append(stem)

        masks_root: Path | None = None
        if lesion_mask_dir is not None:
            masks_root = Path(lesion_mask_dir)
            if not masks_root.exists():
                masks_root = None

        return cls(
            image_paths, labels, patient_ids, image_stems,
            masks_root, preprocessing, augmentation,
        )

    def get_lesion_masks(self, idx: int) -> dict[str, np.ndarray] | None:
        """Load available lesion masks for a given sample index.

        Masks exist only for the 54-image segmentation subset.
        Image names use 3-digit IDs (IDRiD_001); mask files use 2-digit IDs
        (IDRiD_01_MA.tif).

        Args:
            idx: Sample index.

        Returns:
            Dict mapping lesion type key to binary mask (H×W uint8), or None
            if no masks are available for this image.
        """
        if self.masks_root is None:
            return None

        stem = self.image_stems[idx]        # e.g. "IDRiD_001"
        num_str = stem.split("_")[1]        # "001"
        mask_num = f"{int(num_str):02d}"    # "01"
        mask_stem = f"IDRiD_{mask_num}"     # "IDRiD_01"

        masks: dict[str, np.ndarray] = {}
        for lesion_key, lesion_dir in self.LESION_DIRS.items():
            suffix = self.LESION_SUFFIXES[lesion_key]
            mask_path = self.masks_root / lesion_dir / f"{mask_stem}_{suffix}.tif"
            if mask_path.exists():
                mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
                if mask is not None:
                    masks[lesion_key] = mask

        return masks if masks else None

    def count_images_with_masks(self) -> int:
        """Count images that have at least one lesion mask available.

        Returns:
            Number of images for which get_lesion_masks returns non-None.
        """
        return sum(
            1 for i in range(len(self)) if self.get_lesion_masks(i) is not None
        )


class DDRDataset(BaseFundusDataset):
    """DDR dataset for DR grading (~13,673 images, 5-class DR).

    Supports loading train, test, and valid splits.

    Args:
        image_paths: Absolute paths to .jpg images.
        labels: DR grade labels (0–4).
        patient_ids: Filename stems used as patient IDs.
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
        split: str = "train",
        subset_indices: list[int] | None = None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> "DDRDataset":
        """Build dataset from DDR DR_grading directory layout.

        Args:
            root: Path to DR_grading/ directory (contains train/, test/,
                  valid/ subdirs and train.txt, test.txt, valid.txt).
            split: One of "train", "test", "valid".
            subset_indices: Optional list of row indices within the split file.
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.

        Returns:
            Constructed DDRDataset.
        """
        root = Path(root)
        split_txt = root / f"{split}.txt"
        images_dir = root / split

        with open(split_txt, "r") as f:
            lines = [l.strip() for l in f if l.strip()]

        if subset_indices is not None:
            lines = [lines[i] for i in subset_indices]

        image_paths, labels, patient_ids = [], [], []
        for line in lines:
            parts = line.split()
            filename, grade = parts[0], int(parts[1])
            img_path = images_dir / filename
            if not img_path.exists():
                continue
            image_paths.append(str(img_path))
            labels.append(grade)
            patient_ids.append(Path(filename).stem)

        return cls(image_paths, labels, patient_ids, preprocessing, augmentation)


# ---------------------------------------------------------------------------
# DR keyword → grade mapping for ODIR-5K
# ---------------------------------------------------------------------------
_DR_KEYWORD_GRADE: list[tuple[str, int]] = [
    ("proliferative diabetic retinopathy", 4),
    ("very severe", 4),
    ("severe non proliferative retinopathy", 3),
    ("severe diabetic retinopathy", 3),
    ("moderate non proliferative retinopathy", 2),
    ("moderate diabetic retinopathy", 2),
    ("mild non proliferative retinopathy", 1),
    ("mild diabetic retinopathy", 1),
    ("diabetic retinopathy", 2),  # unqualified → treat as moderate
    ("laser spot", 4),            # laser treatment implies previous PDR
    ("non proliferative retinopathy", 2),
]


def _keyword_to_grade(keyword: str) -> int | None:
    """Map ODIR diagnostic keyword string to DR grade (0–4) or None.

    Args:
        keyword: Lowercased diagnostic keyword string for one eye.

    Returns:
        Estimated DR grade, or None if the keyword contains no DR signal.
    """
    kw = keyword.lower()
    for phrase, grade in _DR_KEYWORD_GRADE:
        if phrase in kw:
            return grade
    return None


class ODIR5KDataset(BaseFundusDataset):
    """ODIR-5K fundus dataset — DR subset (5-class DR grading).

    ODIR-5K is a bilateral multi-disease dataset. This class extracts only
    the DR-relevant eyes by filtering on diagnostic keywords, then maps
    keyword descriptions to DR grades 0–4.

    Non-DR eyes of patients that also have a DR eye are excluded to avoid
    label ambiguity.

    Args:
        image_paths: Absolute paths to .jpg images (left/right mixed).
        labels: DR grade labels (0–4).
        patient_ids: Patient ID strings (same for left and right eye).
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
        subset_indices: list[int] | None = None,
        preprocessing: Callable | None = None,
        augmentation: Callable | None = None,
    ) -> "ODIR5KDataset":
        """Build DR-subset dataset from ODIR-5K Training Set layout.

        Args:
            root: Path to the ODIR-5K Training Set directory (contains
                  Images/ and Annotation/).
            subset_indices: Optional list of sample indices after DR filtering.
            preprocessing: Optional preprocessing callable.
            augmentation: Optional augmentation callable.

        Returns:
            Constructed ODIR5KDataset with patient_ids attribute.
        """
        root = Path(root)
        images_dir = root / "Images"
        annotation_path = root / "Annotation" / "training annotation (English).xlsx"

        df = pd.read_excel(annotation_path, engine="openpyxl")

        image_paths, labels, patient_ids = [], [], []

        for _, row in df.iterrows():
            pid = str(int(row["ID"]))

            for side, fname_col, kw_col in [
                ("left", "Left-Fundus", "Left-Diagnostic Keywords"),
                ("right", "Right-Fundus", "Right-Diagnostic Keywords"),
            ]:
                keyword = str(row[kw_col]).lower().strip()
                grade = _keyword_to_grade(keyword)

                # Include only eyes with a DR signal; non-DR eyes → grade 0
                # Only include if D flag=1 or keyword maps to a grade
                is_dr_patient = int(row.get("D", 0)) == 1
                if not is_dr_patient and grade is None:
                    continue

                final_grade = grade if grade is not None else 0

                fname = str(row[fname_col]).strip()
                img_path = images_dir / fname
                if not img_path.exists():
                    continue

                image_paths.append(str(img_path))
                labels.append(final_grade)
                patient_ids.append(pid)

        if subset_indices is not None:
            image_paths = [image_paths[i] for i in subset_indices]
            labels = [labels[i] for i in subset_indices]
            patient_ids = [patient_ids[i] for i in subset_indices]

        return cls(image_paths, labels, patient_ids, preprocessing, augmentation)


# ---------------------------------------------------------------------------
# Dataset registry — maps dataset name to class for factory access
# ---------------------------------------------------------------------------
DATASET_REGISTRY: dict[str, type] = {
    "eyepacs": EyePACSDataset,
    "aptos2019": APTOS2019Dataset,
    "idrid": IDRiDDataset,
    "ddr": DDRDataset,
    "odir5k": ODIR5KDataset,
}
