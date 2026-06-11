"""Label harmonization utilities for cross-database evaluation (Experiments 5 & 6).

Handles taxonomy differences between DR datasets and provides
camera-to-dataset mapping for device domain shift analysis.
"""

from __future__ import annotations

import warnings

DR_CLASSES: dict[int, str] = {
    0: "No DR",
    1: "Mild NPDR",
    2: "Moderate NPDR",
    3: "Severe NPDR",
    4: "Proliferative DR",
}


def to_binary_referable(dr_class: int, threshold: int = 2) -> int:
    """Convert a 5-class DR grade to a binary referable / non-referable label.

    Args:
        dr_class: DR grade in [0, 4].
        threshold: Grade at or above which DR is considered referable.
                   Default: 2 (Moderate NPDR and above).

    Returns:
        0 (non-referable) if dr_class < threshold, else 1 (referable).
    """
    return 0 if dr_class < threshold else 1


def harmonize_messidor2_labels(csv_path: str) -> tuple[list[str], list[int]]:
    """Load Messidor-2 image paths and DR grades from the dataset CSV.

    Messidor-2 DR grades are distributed separately from the image archive.
    The Kaggle "messidor-2" distribution includes a CSV with adjudicated
    DR grades (0–2, scaled to 0/1/2) that must be mapped to the 5-class
    taxonomy:
        Messidor-2 grade 0 → DR 0 (No DR)
        Messidor-2 grade 1 → DR 1 (Mild NPDR)
        Messidor-2 grade 2 → DR 2 (Moderate NPDR)

    NOTE: This is a stub.  Messidor-2 DR grades are not bundled with the
    original ADCIS image distribution.  To use this function, supply the
    CSV that accompanies the Kaggle messidor-2 dataset (columns: image,
    adjudicated_dr_grade) or the ADCIS grade file.  Until then, this
    function returns empty lists and emits a warning.

    Args:
        csv_path: Path to the Messidor-2 grade CSV.

    Returns:
        Tuple of (image_paths, labels).  Returns ([], []) with a warning
        when the grade file is not available or the format is unrecognised.
    """
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        required = {"image", "adjudicated_dr_grade"}
        if not required.issubset(df.columns):
            warnings.warn(
                f"harmonize_messidor2_labels: CSV at {csv_path!r} does not contain "
                f"expected columns {required}.  Got {list(df.columns)}.  "
                "Returning empty lists — Messidor-2 grades must be sourced from "
                "the Kaggle messidor-2 dataset or the ADCIS distribution.",
                UserWarning,
                stacklevel=2,
            )
            return [], []

        # Map Messidor-2 grades (0-2) to 5-class taxonomy
        # Messidor-2 uses: 0=no DR, 1=mild NPDR, 2=moderate/severe/PDR
        # We keep grade 0→0, 1→1, 2→2 as a conservative mapping
        paths: list[str] = []
        labels: list[int] = []
        for _, row in df.iterrows():
            grade = int(row["adjudicated_dr_grade"])
            # Clip to [0, 4] for safety
            paths.append(str(row["image"]))
            labels.append(min(max(grade, 0), 4))
        return paths, labels

    except FileNotFoundError:
        warnings.warn(
            f"harmonize_messidor2_labels: grade CSV not found at {csv_path!r}.  "
            "Messidor-2 DR grades must be sourced separately (Kaggle or ADCIS).  "
            "Returning empty lists — Messidor-2 evaluation will be skipped.",
            UserWarning,
            stacklevel=2,
        )
        return [], []


def get_dataset_camera_groups() -> dict[str, list[str]]:
    """Return the camera-manufacturer-to-dataset mapping for Experiment 6.

    Based on RESEARCH_ARCHITECTURE §5.6 table.  Note that DDR and ODIR-5K
    contain images from multiple camera manufacturers; per-image camera
    metadata is not available in the public releases, so those datasets are
    listed under all applicable manufacturers but evaluated as a whole
    (with the limitation acknowledged per SB-1.8).

    Returns:
        Dict mapping camera manufacturer (lowercase) to list of dataset keys.
        Dataset keys match those in config["paths"] and DATASET_REGISTRY.
    """
    return {
        "canon":  ["eyepacs", "ddr", "odir5k"],
        "topcon": ["messidor2", "rfmid", "ddr"],
        "kowa":   ["idrid", "rfmid"],
        "zeiss":  ["odir5k"],
    }
