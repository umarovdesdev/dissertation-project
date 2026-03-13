#!/usr/bin/env python3
"""Verification script for data loading and patient-level CV splits."""

from collections import Counter
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Subset

from src.data.datasets import APTOS2019Dataset, EyePACSDataset, IDRiDDataset
from src.data.splits import PatientLevelKFold


def print_class_dist(labels: list[int], name: str) -> None:
    dist = Counter(labels)
    print(f"  Class distribution: {dict(sorted(dist.items()))}")
    total = sum(dist.values())
    for grade, count in sorted(dist.items()):
        print(f"    Grade {grade}: {count:6d}  ({100*count/total:.1f}%)")


# ==========================================================================
# APTOS 2019
# ==========================================================================
print("=" * 60)
print("APTOS 2019")
print("=" * 60)

aptos = APTOS2019Dataset.from_directory(
    root="/mnt/d/datasets/APTOS 2019/train_images",
    labels_csv="/mnt/d/datasets/APTOS 2019/train.csv",
)
print(f"  Total images : {len(aptos)}")
print_class_dist(aptos.labels, "APTOS")
print(f"  Unique patients: {len(set(aptos.patient_ids))} (= images, one eye per patient)")

splitter = PatientLevelKFold(n_folds=5, seed=42, stratified=True)
splits = splitter.split(aptos.image_paths, aptos.labels, aptos.patient_ids)
print(f"\n  5-fold splits:")
for i, (train_idx, test_idx) in enumerate(splits):
    print(f"    Fold {i}: train={len(train_idx):4d}  test={len(test_idx):4d}")
ok = splitter.verify_no_leakage(splits, aptos.patient_ids)
print(f"  No leakage: {ok}")

# One DataLoader batch — use a resize-only preprocessing so images are uniform
import cv2 as _cv2
import numpy as _np

def _resize512(img: _np.ndarray) -> _np.ndarray:
    return _cv2.resize(img, (512, 512), interpolation=_cv2.INTER_LINEAR)

aptos_resized = APTOS2019Dataset.from_directory(
    root="/mnt/d/datasets/APTOS 2019/train_images",
    labels_csv="/mnt/d/datasets/APTOS 2019/train.csv",
    preprocessing=_resize512,
)
subset = Subset(aptos_resized, splits[0][1][:4])
loader = DataLoader(subset, batch_size=4, num_workers=0)
imgs, lbls = next(iter(loader))
print(f"\n  Batch tensor shape : {imgs.shape}  dtype={imgs.dtype}")
print(f"  Batch value range  : [{imgs.min():.3f}, {imgs.max():.3f}]")
print(f"  Batch labels       : {lbls.tolist()}")


# ==========================================================================
# EyePACS
# ==========================================================================
print("\n" + "=" * 60)
print("EyePACS")
print("=" * 60)

eyepacs = EyePACSDataset.from_directory(
    root="/mnt/d/datasets/EyePACS/train",
    labels_csv="/mnt/d/datasets/EyePACS/trainLabels.csv",
)
print(f"  Total images   : {len(eyepacs)}")
print(f"  Unique patients: {len(set(eyepacs.patient_ids))}")
print_class_dist(eyepacs.labels, "EyePACS")

splits_ep = splitter.split(eyepacs.image_paths, eyepacs.labels, eyepacs.patient_ids)
print(f"\n  5-fold splits:")
for i, (train_idx, test_idx) in enumerate(splits_ep):
    train_patients = len({eyepacs.patient_ids[j] for j in train_idx})
    test_patients = len({eyepacs.patient_ids[j] for j in test_idx})
    print(
        f"    Fold {i}: train={len(train_idx):6d} imgs ({train_patients:5d} pts)  "
        f"test={len(test_idx):6d} imgs ({test_patients:5d} pts)"
    )
ok_ep = splitter.verify_no_leakage(splits_ep, eyepacs.patient_ids)
print(f"  No leakage: {ok_ep}")


# ==========================================================================
# IDRiD
# ==========================================================================
print("\n" + "=" * 60)
print("IDRiD")
print("=" * 60)

idrid = IDRiDDataset.from_directory()
print(f"  Total images : {len(idrid)}")
print_class_dist(idrid.labels, "IDRiD")

n_with_masks = idrid.count_images_with_masks()
print(f"\n  Images with ≥1 lesion mask : {n_with_masks}")

# Show mask types available for first masked image
for i in range(len(idrid)):
    masks = idrid.get_lesion_masks(i)
    if masks:
        print(f"  Example masks for '{idrid.image_stems[i]}':")
        for lesion, m in masks.items():
            print(f"    {lesion}: shape={m.shape}  nonzero={m.any()}")
        break

print("\nAll verifications complete.")
