#!/usr/bin/env python3
"""Stage 2 verification: dataset loading, splits, augmentation."""

from collections import Counter
from pathlib import Path

import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Subset

from src.data.datasets import APTOS2019Dataset, EyePACSDataset, IDRiDDataset, DATASET_REGISTRY
from src.data.splits import PatientLevelKFold, extract_patient_id
from src.data.augmentation import FundusAugmentation

SEP = "=" * 60


# ─────────────────────────────────────────────────────────────
# Test 1 — APTOS 2019 loading
# ─────────────────────────────────────────────────────────────
print(SEP)
print("Test 1 — APTOS 2019 loading")
print(SEP)

ds_aptos = APTOS2019Dataset.from_directory(
    root="/mnt/d/datasets/APTOS 2019/train_images",
    labels_csv="/mnt/d/datasets/APTOS 2019/train.csv",
)
dist = Counter(ds_aptos.labels)
print(f"  Total images : {len(ds_aptos)}")
print(f"  Class distribution:")
for grade in sorted(dist):
    print(f"    Grade {grade}: {dist[grade]:5d}  ({100*dist[grade]/len(ds_aptos):.1f}%)")


# ─────────────────────────────────────────────────────────────
# Test 2 — EyePACS loading (first 1000 rows)
# ─────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 2 — EyePACS loading (first 1000 rows)")
print(SEP)

ds_ep = EyePACSDataset.from_directory(
    root="/mnt/d/datasets/EyePACS/train",
    labels_csv="/mnt/d/datasets/EyePACS/trainLabels.csv",
    subset_indices=list(range(1000)),
)
dist_ep = Counter(ds_ep.labels)
print(f"  Total images loaded : {len(ds_ep)}")
print(f"  Unique patients     : {len(set(ds_ep.patient_ids))}")
print(f"  Class distribution:")
for grade in sorted(dist_ep):
    print(f"    Grade {grade}: {dist_ep[grade]:5d}  ({100*dist_ep[grade]/len(ds_ep):.1f}%)")

# Spot-check extract_patient_id
pid = extract_patient_id("10_left.jpeg", "eyepacs")
assert pid == "10", f"Expected '10', got '{pid}'"
pid2 = extract_patient_id("000c1434d8d7.png", "aptos2019")
assert pid2 == "000c1434d8d7", f"Got '{pid2}'"
pid3 = extract_patient_id("IDRiD_001.jpg", "idrid")
assert pid3 == "IDRiD_001", f"Got '{pid3}'"
print(f"  extract_patient_id: OK")

# Dataset registry check
assert "eyepacs" in DATASET_REGISTRY
assert "aptos2019" in DATASET_REGISTRY
assert "idrid" in DATASET_REGISTRY
assert "ddr" in DATASET_REGISTRY
assert "odir5k" in DATASET_REGISTRY
print(f"  DATASET_REGISTRY keys: {sorted(DATASET_REGISTRY.keys())}")


# ─────────────────────────────────────────────────────────────
# Test 3 — IDRiD loading + lesion masks
# ─────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 3 — IDRiD loading + lesion masks")
print(SEP)

ds_idrid = IDRiDDataset.from_directory(
    root="/mnt/d/datasets/IDRiD/B. Disease Grading/1. Original Images/a. Training Set",
    labels_csv="/mnt/d/datasets/IDRiD/B. Disease Grading/2. Groundtruths/a. IDRiD_Disease Grading_Training Labels.csv",
    lesion_mask_dir="/mnt/d/datasets/IDRiD/A. Segmentation/2. All Segmentation Groundtruths/a. Training Set",
)
dist_id = Counter(ds_idrid.labels)
print(f"  Total images : {len(ds_idrid)}")
print(f"  Class distribution:")
for grade in sorted(dist_id):
    print(f"    Grade {grade}: {dist_id[grade]:5d}  ({100*dist_id[grade]/len(ds_idrid):.1f}%)")

masks = ds_idrid.get_lesion_masks(0)
print(f"\n  get_lesion_masks(0) for '{ds_idrid.image_stems[0]}':")
if masks:
    for k, m in masks.items():
        print(f"    {k}: shape={m.shape}  has_annotations={m.any()}")
else:
    print("    None")

n_masked = ds_idrid.count_images_with_masks()
print(f"\n  Images with ≥1 lesion mask: {n_masked}")


# ─────────────────────────────────────────────────────────────
# Test 4 — Patient-level split on APTOS
# ─────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 4 — PatientLevelKFold on APTOS 2019")
print(SEP)

splitter = PatientLevelKFold(n_folds=5, seed=42)
splits = splitter.split(ds_aptos.image_paths, ds_aptos.labels, ds_aptos.patient_ids)

print(f"  Fold sizes:")
for i, (train_idx, test_idx) in enumerate(splits):
    print(f"    Fold {i}: train={len(train_idx):4d}  test={len(test_idx):4d}")

ok = splitter.verify_no_leakage(splits, ds_aptos.patient_ids)
print(f"  verify_no_leakage: {ok}")
assert ok, "LEAKAGE DETECTED — patient-level split is broken!"


# ─────────────────────────────────────────────────────────────
# Test 5 — FundusAugmentation
# ─────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Test 5 — FundusAugmentation")
print(SEP)

aug_config = {
    "horizontal_flip": True,
    "vertical_flip": True,
    "rotation_degrees": 15,
    "zoom_range": 0.10,
    "brightness_range": [0.9, 1.1],
}
aug = FundusAugmentation(aug_config)

# Load one real image
sample_path = ds_aptos.image_paths[0]
img = cv2.imread(sample_path)
assert img is not None, f"Could not load {sample_path}"
original_shape = img.shape

out = aug(img)
print(f"  Input  shape: {original_shape}")
print(f"  Output shape: {out.shape}")
assert out.shape == original_shape, (
    f"Shape mismatch after augmentation: {out.shape} != {original_shape}"
)
print(f"  Output dtype: {out.dtype}  (uint8 expected)")
assert out.dtype == np.uint8, f"Expected uint8, got {out.dtype}"

# Also verify float32 input passes through
img_f = img.astype(np.float32) / 255.0
out_f = aug(img_f)
assert out_f.dtype == np.float32, f"Expected float32, got {out_f.dtype}"
assert out_f.min() >= 0.0 and out_f.max() <= 1.0, "Float output out of [0,1] range"
print(f"  Float32 pass: shape={out_f.shape}  range=[{out_f.min():.3f}, {out_f.max():.3f}]")

print(f"\nAll 5 tests passed.")
