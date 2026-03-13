"""Experiment 2: Preprocessing Component Ablation + CLAHE Sweep (H-2, PC-8).

Part A — Component ablation:
  5 pipeline levels trained on EyePACS with 5-fold CV using EfficientNet-B3.
  Image quality metrics (CNR, Entropy, SSIM) measured on 100 sample images.

Part B — CLAHE threshold sensitivity:
  Sweep clip_limit values on IDRiD, record per-class F1 for DR 1 and DR 2.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from src.data.augmentation import FundusAugmentation
from src.data.datasets import EyePACSDataset, IDRiDDataset
from src.data.splits import PatientLevelKFold
from src.models.factory import create_model
from src.preprocessing.pipeline import PreprocessingPipeline
from src.training.checkpoint import CheckpointManager
from src.training.trainer import Trainer
from src.utils.image_quality import compute_all_quality_metrics
from src.utils.seed import set_seed

# ── Ablation levels ───────────────────────────────────────────────────────────
_ABLATION_LEVELS: list[dict] = [
    {
        "name": "resize_only",
        "components": ["fov_standardization"],
    },
    {
        "name": "resize_norm",
        "components": ["fov_standardization", "normalize"],
    },
    {
        "name": "resize_clahe",
        "components": ["fov_standardization", "clahe"],
    },
    {
        "name": "resize_norm_clahe",
        "components": ["fov_standardization", "normalize", "clahe"],
    },
    {
        "name": "full_pipeline",
        "components": [
            "fov_standardization", "green_channel", "normalize",
            "clahe", "hsv_enhancement",
        ],
    },
]

_CLAHE_SWEEP_VALUES: list[float] = [
    0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 8.0, 10.0
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_eyepacs_index(
    root: str,
    labels_csv: str,
    subset_size: int | None = None,
) -> tuple[list[str], list[int], list[str]]:
    root = Path(root)
    df = pd.read_csv(labels_csv)
    if subset_size is not None:
        df = df.iloc[:subset_size].reset_index(drop=True)
    paths, labels, pids = [], [], []
    for _, row in df.iterrows():
        name = str(row["image"])
        p = root / f"{name}.jpeg"
        if not p.exists():
            continue
        paths.append(str(p))
        labels.append(int(row["level"]))
        pids.append(name.split("_")[0])
    return paths, labels, pids


def _measure_quality_on_sample(
    image_paths: list[str],
    pipeline: PreprocessingPipeline,
    n_samples: int = 100,
    seed: int = 42,
) -> dict[str, float]:
    """Compute mean CNR, Entropy, SSIM over n_samples images.

    Args:
        image_paths: Pool of image paths to sample from.
        pipeline: Preprocessing pipeline to apply.
        n_samples: Number of images to sample.
        seed: RNG seed for reproducible sampling.

    Returns:
        Dict with mean_cnr, mean_entropy, mean_ssim.
    """
    rng = np.random.default_rng(seed)
    n = min(n_samples, len(image_paths))
    indices = rng.choice(len(image_paths), size=n, replace=False)

    cnrs, entropies, ssims = [], [], []
    for idx in indices:
        raw = cv2.imread(image_paths[idx])
        if raw is None:
            continue
        processed = pipeline(raw)
        q = compute_all_quality_metrics(processed, original=raw)
        cnrs.append(q["cnr"])
        entropies.append(q["entropy"])
        if q["ssim"] is not None:
            ssims.append(q["ssim"])

    result: dict[str, float] = {}
    if cnrs:
        result["mean_cnr"] = float(np.mean(cnrs))
    if entropies:
        result["mean_entropy"] = float(np.mean(entropies))
    if ssims:
        result["mean_ssim"] = float(np.mean(ssims))
    return result


def _compute_summary(per_fold: list[dict]) -> dict[str, str]:
    keys = [
        "val_weighted_f1", "val_roc_auc",
        "val_cohen_kappa_quadratic", "val_accuracy",
    ]
    summary: dict[str, str] = {}
    for k in keys:
        vals = [
            m[k] for m in per_fold
            if k in m and not np.isnan(float(m[k]))
        ]
        if vals:
            summary[k.replace("val_", "")] = f"{np.mean(vals):.4f} ± {np.std(vals):.4f}"
    return summary


# ── Part A ────────────────────────────────────────────────────────────────────

def _run_ablation(
    config: dict[str, Any],
    all_paths: list[str],
    all_labels: list[int],
    all_pids: list[str],
    splits: list[tuple[list[int], list[int]]],
    output_dir: Path,
    metrics_csv: Path,
    trainer: Trainer,
    fold_range: list[int],
    levels_to_run: list[str] | None,
    preproc_cfg: dict,
    aug_cfg: dict,
    model_name: str,
    model_cfg: dict,
    quality_n_samples: int,
    seed: int,
) -> dict[str, Any]:
    """Run Part A: component ablation training and quality measurement.

    Returns dict mapping level_name -> {"per_fold": [...], "quality": {...}}.
    """
    results: dict[str, Any] = {}

    for level_spec in _ABLATION_LEVELS:
        level_name = level_spec["name"]
        if levels_to_run is not None and level_name not in levels_to_run:
            continue

        components = level_spec["components"]
        print(f"\n{'='*65}")
        print(f"  Ablation Level: {level_name}")
        print(f"  Components: {components}")
        print(f"{'='*65}")

        pipeline = PreprocessingPipeline.create_ablation(
            config={
                "target_size": preproc_cfg.get("target_size", 512),
                "clahe_clip_limit": preproc_cfg.get("clahe", {}).get("clip_limit", 2.0),
                "clahe_grid_size":  preproc_cfg.get("clahe", {}).get("tile_grid_size", [8, 8]),
                "saturation_scale": preproc_cfg.get("hsv", {}).get("saturation_scale", 1.2),
                "value_scale":      preproc_cfg.get("hsv", {}).get("value_scale", 1.1),
            },
            components=components,
        )
        augmentation = FundusAugmentation(aug_cfg)

        # Image quality on sample images (train pool only — fold 0 train split)
        train_idx_0 = splits[0][0]
        sample_paths = [all_paths[i] for i in train_idx_0]
        quality = _measure_quality_on_sample(
            sample_paths, pipeline, n_samples=quality_n_samples, seed=seed
        )
        print(f"  Quality — CNR={quality.get('mean_cnr', float('nan')):.3f}  "
              f"Entropy={quality.get('mean_entropy', float('nan')):.3f}  "
              f"SSIM={quality.get('mean_ssim', float('nan')):.3f}")

        per_fold: list[dict] = []
        n_folds = len(splits)

        for fold_idx in fold_range:
            train_idx, val_idx = splits[fold_idx]
            print(f"\n  [Level {level_name} | Fold {fold_idx+1}/{n_folds}]")

            train_ds = EyePACSDataset(
                image_paths=[all_paths[i] for i in train_idx],
                labels=[all_labels[i] for i in train_idx],
                patient_ids=[all_pids[i] for i in train_idx],
                preprocessing=pipeline,
                augmentation=augmentation,
            )
            val_ds = EyePACSDataset(
                image_paths=[all_paths[i] for i in val_idx],
                labels=[all_labels[i] for i in val_idx],
                patient_ids=[all_pids[i] for i in val_idx],
                preprocessing=pipeline,
                augmentation=None,
            )

            train_loader = DataLoader(
                train_ds, batch_size=trainer.batch_size, shuffle=True,
                num_workers=trainer.num_workers,
                pin_memory=(trainer.device.type == "cuda"), drop_last=True,
            )
            val_loader = DataLoader(
                val_ds, batch_size=trainer.batch_size, shuffle=False,
                num_workers=trainer.num_workers,
                pin_memory=(trainer.device.type == "cuda"),
            )

            ckpt_dir = output_dir / "checkpoints" / f"{level_name}_fold{fold_idx}"
            ckpt_dir.mkdir(parents=True, exist_ok=True)
            ckpt_mgr = CheckpointManager(ckpt_dir, max_keep=5)
            model = create_model(model_name, model_cfg)

            best = trainer.train_fold(
                model=model,
                train_loader=train_loader,
                val_loader=val_loader,
                fold=fold_idx,
                config_name=level_name,
                checkpoint_mgr=ckpt_mgr,
                metrics_csv_path=metrics_csv,
                resume=False,
            )
            per_fold.append(best)
            f1 = best.get("val_weighted_f1", float("nan"))
            print(f"  Best F1={f1:.4f}")

        results[level_name] = {"per_fold": per_fold, "quality": quality}

    return results


# ── Part B ────────────────────────────────────────────────────────────────────

def _run_clahe_sweep(
    config: dict[str, Any],
    output_dir: Path,
    metrics_csv: Path,
    trainer: Trainer,
    clip_values: list[float],
    seed: int,
    subset_size: int | None,
    max_epochs: int | None,
) -> dict[str, Any]:
    """Run Part B: CLAHE clip_limit sweep on IDRiD.

    Returns dict mapping str(clip_limit) -> {"per_class_f1": [...], "dr1_f1", "dr2_f1"}.
    """
    preproc_cfg = config["preprocessing"]
    target_size = preproc_cfg.get("target_size", 512)

    # Load IDRiD
    idrid_ds_full = IDRiDDataset.from_directory(
        root="/mnt/d/datasets/IDRiD/B. Disease Grading/1. Original Images/a. Training Set",
        labels_csv="/mnt/d/datasets/IDRiD/B. Disease Grading/2. Groundtruths/"
                   "a. IDRiD_Disease Grading_Training Labels.csv",
        subset_indices=list(range(subset_size)) if subset_size else None,
    )
    print(f"  IDRiD: {len(idrid_ds_full)} images for CLAHE sweep")

    # Simple 80/20 train/val split (IDRiD is too small for patient-level 5-fold)
    n = len(idrid_ds_full)
    n_train = int(n * 0.8)
    idx_all = list(range(n))
    rng = np.random.default_rng(seed)
    rng.shuffle(idx_all)
    train_idx = idx_all[:n_train]
    val_idx   = idx_all[n_train:]

    model_name = "efficientnet_b3"
    model_cfg  = dict(config["models"][model_name])
    if max_epochs is not None:
        config = dict(config)
        config["training"] = dict(config["training"])
        config["training"]["max_epochs"] = max_epochs

    sweep_results: dict[str, Any] = {}

    for clip_limit in clip_values:
        key = str(clip_limit)
        print(f"\n  CLAHE sweep — clip_limit={clip_limit}")

        pipeline = PreprocessingPipeline.create_ablation(
            config={
                "target_size": target_size,
                "clahe_clip_limit": clip_limit,
                "clahe_grid_size":  preproc_cfg.get("clahe", {}).get("tile_grid_size", [8, 8]),
            },
            components=["fov_standardization", "clahe"],
        )

        train_ds = IDRiDDataset(
            image_paths=[idrid_ds_full.image_paths[i] for i in train_idx],
            labels=[idrid_ds_full.labels[i] for i in train_idx],
            patient_ids=[idrid_ds_full.patient_ids[i] for i in train_idx],
            image_stems=[idrid_ds_full.image_stems[i] for i in train_idx],
            masks_root=None,
            preprocessing=pipeline,
            augmentation=FundusAugmentation(config["augmentation"]),
        )
        val_ds = IDRiDDataset(
            image_paths=[idrid_ds_full.image_paths[i] for i in val_idx],
            labels=[idrid_ds_full.labels[i] for i in val_idx],
            patient_ids=[idrid_ds_full.patient_ids[i] for i in val_idx],
            image_stems=[idrid_ds_full.image_stems[i] for i in val_idx],
            masks_root=None,
            preprocessing=pipeline,
            augmentation=None,
        )

        train_loader = DataLoader(
            train_ds, batch_size=trainer.batch_size, shuffle=True,
            num_workers=trainer.num_workers,
            pin_memory=(trainer.device.type == "cuda"), drop_last=False,
        )
        val_loader = DataLoader(
            val_ds, batch_size=trainer.batch_size, shuffle=False,
            num_workers=trainer.num_workers,
            pin_memory=(trainer.device.type == "cuda"),
        )

        ckpt_dir = output_dir / "checkpoints" / f"clahe_{key.replace('.','p')}"
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_mgr  = CheckpointManager(ckpt_dir, max_keep=2)
        sweep_csv = output_dir / "metrics_clahe_sweep.csv"
        model     = create_model(model_name, model_cfg)

        # Build a local trainer with potentially overridden max_epochs
        local_trainer = Trainer(config, device="auto")
        best = local_trainer.train_fold(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            fold=0,
            config_name=f"clahe_{key}",
            checkpoint_mgr=ckpt_mgr,
            metrics_csv_path=sweep_csv,
            resume=False,
        )

        per_class_f1 = best.get("val_per_class_f1", [])
        dr1_f1 = per_class_f1[1] if len(per_class_f1) > 1 else float("nan")
        dr2_f1 = per_class_f1[2] if len(per_class_f1) > 2 else float("nan")
        print(f"  clip={clip_limit}: weighted_F1={best.get('val_weighted_f1', float('nan')):.4f}  "
              f"DR1_F1={dr1_f1:.4f}  DR2_F1={dr2_f1:.4f}")

        sweep_results[key] = {
            "clip_limit":    clip_limit,
            "weighted_f1":   best.get("val_weighted_f1", float("nan")),
            "per_class_f1":  per_class_f1,
            "dr1_f1":        dr1_f1,
            "dr2_f1":        dr2_f1,
        }

    return sweep_results


# ── Entry point ───────────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _levels_to_run: list[str] | None = None,
    _clahe_values: list[float] | None = None,
    _quality_n_samples: int = 100,
) -> None:
    """Run Experiment 2: component ablation + CLAHE sweep.

    Args:
        config: Full merged config dict.
        fold: If set, run only this fold index for Part A.
        resume: Resume from checkpoint (Part A only).
        _subset_size: Limit EyePACS CSV rows (smoke test).
        _levels_to_run: Run only these level names (smoke test).
        _clahe_values: Override CLAHE sweep values (smoke test).
        _quality_n_samples: Number of images for quality metric sampling.
    """
    set_seed(config.get("seed", 42))
    seed = config.get("seed", 42)

    output_dir = Path(config["paths"]["output_dir"]) / "exp2"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)
    metrics_csv = output_dir / "metrics.csv"

    cv_cfg    = config["cross_validation"]
    preproc_cfg = config["preprocessing"]
    aug_cfg   = config["augmentation"]
    n_folds   = cv_cfg["n_folds"]
    fold_range = [fold] if fold is not None else list(range(n_folds))

    model_name = "efficientnet_b3"
    model_cfg  = config["models"][model_name]

    trainer = Trainer(config, device="auto")

    # ── Load EyePACS index ────────────────────────────────────────────────────
    eyepacs_root = config["paths"]["eyepacs"]
    labels_csv   = str(Path(eyepacs_root) / "trainLabels.csv")
    images_root  = str(Path(eyepacs_root) / "train")

    print(f"Loading EyePACS index …")
    all_paths, all_labels, all_pids = _load_eyepacs_index(
        images_root, labels_csv, subset_size=_subset_size
    )
    print(f"  {len(all_paths)} images | {len(set(all_pids))} patients")

    splitter = PatientLevelKFold(n_folds=n_folds, seed=seed,
                                 stratified=cv_cfg.get("stratified", True))
    splits = splitter.split(all_paths, all_labels, all_pids)
    ok = splitter.verify_no_leakage(splits, all_pids)
    if not ok:
        raise RuntimeError("Patient leakage in CV splits — aborting.")
    print(f"  5-fold splits verified (no leakage)")

    # ════════════════════════════════════════════════════════════
    # PART A — Component Ablation
    # ════════════════════════════════════════════════════════════
    print(f"\n{'='*65}")
    print("PART A — Component Ablation")
    print(f"{'='*65}")

    ablation_results = _run_ablation(
        config=config,
        all_paths=all_paths,
        all_labels=all_labels,
        all_pids=all_pids,
        splits=splits,
        output_dir=output_dir,
        metrics_csv=metrics_csv,
        trainer=trainer,
        fold_range=fold_range,
        levels_to_run=_levels_to_run,
        preproc_cfg=preproc_cfg,
        aug_cfg=aug_cfg,
        model_name=model_name,
        model_cfg=model_cfg,
        quality_n_samples=_quality_n_samples,
        seed=seed,
    )

    # Ablation summary
    ablation_summary: dict[str, Any] = {}
    if fold is None:
        for level_name, res in ablation_results.items():
            ablation_summary[level_name] = {
                "metrics": _compute_summary(res["per_fold"]),
                "quality": res["quality"],
            }
        summary_path = output_dir / "ablation_summary.json"
        with open(summary_path, "w") as f:
            json.dump(ablation_summary, f, indent=2)
        print(f"\n  Ablation summary saved to {summary_path}")

    # ════════════════════════════════════════════════════════════
    # PART B — CLAHE Sweep
    # ════════════════════════════════════════════════════════════
    print(f"\n{'='*65}")
    print("PART B — CLAHE Clip Limit Sweep (H-2)")
    print(f"{'='*65}")

    clahe_values = _clahe_values if _clahe_values is not None else _CLAHE_SWEEP_VALUES

    # For the sweep on IDRiD, use max_epochs from config (or overridden)
    sweep_results = _run_clahe_sweep(
        config=config,
        output_dir=output_dir,
        metrics_csv=metrics_csv,
        trainer=trainer,
        clip_values=clahe_values,
        seed=seed,
        subset_size=_subset_size,
        max_epochs=None,
    )

    clahe_path = output_dir / "clahe_sweep.json"
    with open(clahe_path, "w") as f:
        json.dump(sweep_results, f, indent=2)
    print(f"\n  CLAHE sweep results saved to {clahe_path}")

    # ── Final summary ─────────────────────────────────────────────────────────
    if fold is None and ablation_summary:
        print(f"\n{'='*65}")
        print("Experiment 2 — Ablation Summary")
        print(f"{'='*65}")
        for level_name, entry in ablation_summary.items():
            f1_str = entry["metrics"].get("weighted_f1", "N/A")
            cnr    = entry["quality"].get("mean_cnr", float("nan"))
            ent    = entry["quality"].get("mean_entropy", float("nan"))
            print(f"  {level_name:<22s}: F1={f1_str}  CNR={cnr:.3f}  Entropy={ent:.3f}")
