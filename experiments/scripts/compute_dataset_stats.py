"""Compute dataset-specific mean and std for V5 normalization (Stage 7).

Computes channel-wise mean and std from the EyePACS training set AFTER
applying Stages 0–4 (canonical flip, OD-fovea rotation, isotropic resize,
FOV mask, flat-field correction). Only mask=1.0 pixels are included.

Usage:
    python scripts/compute_dataset_stats.py --config configs/default.yaml

Output:
    Prints mean and std values to paste into default.yaml.
"""

import argparse
from pathlib import Path

def main():
    # TODO: Implement
    # 1. Load EyePACS training images
    # 2. Apply stages 0-4 of V5 pipeline
    # 3. For each image, extract RGB values where fov_mask == 1.0
    # 4. Compute running mean and std across all images
    # 5. Print results
    raise NotImplementedError(
        "compute_dataset_stats.py not yet implemented. "
        "Compute EyePACS train mean/std after V5 Stages 0-4, mask=1.0 only."
    )

if __name__ == "__main__":
    main()
