#!/usr/bin/env python3
"""Verify RFMiD dataset loader.

Loads the RFMiD training split and prints:
  - Total image count
  - DR-positive count (DR=1)
  - DR-negative count (DR=0)

Also verifies label integrity and that images exist on disk.
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.data.datasets import RFMiDDataset

RFMID_ROOT = Path("/mnt/d/datasets/RFMiD/A. RFMiD_All_Classes_Dataset")

SEP = "=" * 65

print(SEP)
print("RFMiD Dataset Loader Verification")
print(SEP)

if not RFMID_ROOT.exists():
    print(f"\n  ERROR: RFMiD root not found at {RFMID_ROOT}")
    sys.exit(1)

for split in ("train", "validation", "test"):
    print(f"\n  Loading split: {split!r} …")
    ds = RFMiDDataset.from_directory(root=RFMID_ROOT, split=split)

    n_total    = len(ds)
    n_positive = sum(ds.labels)
    n_negative = n_total - n_positive

    print(f"    Total images : {n_total}")
    print(f"    DR-positive  : {n_positive}  ({100*n_positive/n_total:.1f}%)")
    print(f"    DR-negative  : {n_negative}  ({100*n_negative/n_total:.1f}%)")

    # Sanity checks
    assert n_total > 0, f"No images found in {split} split"
    assert all(lbl in (0, 1) for lbl in ds.labels), "Labels must be binary (0 or 1)"
    assert len(ds.patient_ids) == n_total, "patient_ids length mismatch"

    # Verify first image loads
    sample_img_path = Path(ds.image_paths[0])
    assert sample_img_path.exists(), f"Image not found: {sample_img_path}"
    print(f"    First image  : {sample_img_path.name}  ✓")

print(f"\n{SEP}")
print("All RFMiD assertions passed.")
print(SEP)
