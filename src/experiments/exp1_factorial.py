"""Experiment 1: 2×2 Factorial Ablation — Preprocessing × Architecture (H-1).

Tests whether the 5-component preprocessing pipeline produces statistically
dominant improvement over resize-only baseline, independently for ResNet-50
and EfficientNet-B3 (EH-3 criteria, EH-4 replication requirement).

Configurations:
  A — resize only   + ResNet-50
  B — full pipeline + ResNet-50
  C — resize only   + EfficientNet-B3
  D — full pipeline + EfficientNet-B3
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Subset

from src.data.augmentation import FundusAugmentation
from src.data.datasets import EyePACSDataset
from src.data.splits import PatientLevelKFold
from src.evaluation.metrics import check_dominance
from src.models.factory import create_model
from src.preprocessing.pipeline import PreprocessingPipeline
from src.training.checkpoint import CheckpointManager
from src.training.trainer import Trainer
from src.utils.seed import set_seed


# ── Factorial design ──────────────────────────────────────────────────────────
_CONFIGS: dict[str, dict[str, str]] = {
    "A": {"preprocessing": "baseline", "model": "resnet50"},
    "B": {"preprocessing": "full",     "model": "resnet50"},
    "C": {"preprocessing": "baseline", "model": "efficientnet_b3"},
    "D": {"preprocessing": "full",     "model": "efficientnet_b3"},
}


def _make_preprocessing(kind: str, preproc_cfg: dict) -> PreprocessingPipeline:
    """Build the correct preprocessing pipeline variant.

    Args:
        kind: "baseline" (FOV/resize only) or "full" (all 5 components).
        preproc_cfg: preprocessing section of the global config.

    Returns:
        Configured PreprocessingPipeline.
    """
    target_size: int = preproc_cfg.get("target_size", 512)
    if kind == "baseline":
        return PreprocessingPipeline.create_baseline(target_size=target_size)
    return PreprocessingPipeline.create_full(
        config={
            "target_size": target_size,
            "clahe_clip_limit": preproc_cfg.get("clahe", {}).get("clip_limit", 2.0),
            "clahe_grid_size": preproc_cfg.get("clahe", {}).get("tile_grid_size", [8, 8]),
            "saturation_scale": preproc_cfg.get("hsv", {}).get("saturation_scale", 1.2),
            "value_scale": preproc_cfg.get("hsv", {}).get("value_scale", 1.1),
        }
    )


def _load_eyepacs_index(
    root: str, labels_csv: str, subset_size: int | None = None
) -> tuple[list[str], list[int], list[str]]:
    """Read EyePACS paths/labels/patient_ids without constructing a full Dataset.

    Filters to only files that exist on disk. Optionally limits to the
    first subset_size rows of the CSV (for smoke tests).

    Args:
        root: Path to train/ directory.
        labels_csv: Path to trainLabels.csv.
        subset_size: If set, use only the first N CSV rows.

    Returns:
        Tuple (image_paths, labels, patient_ids).
    """
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


def _compute_summary(per_fold: list[dict]) -> dict[str, str]:
    """Compute mean ± std across folds for primary metrics."""
    keys = ["val_weighted_f1", "val_roc_auc", "val_cohen_kappa_quadratic", "val_accuracy"]
    summary: dict[str, str] = {}
    for k in keys:
        vals = [m[k] for m in per_fold if k in m and not np.isnan(float(m[k]))]
        if vals:
            short = k.replace("val_", "")
            summary[short] = f"{np.mean(vals):.4f} ± {np.std(vals):.4f}"
    return summary


def _mean_primary(per_fold: list[dict]) -> dict[str, float]:
    """Return per-metric means over folds as a flat dict (for dominance check)."""
    keys = {
        "val_weighted_f1": "weighted_f1",
        "val_roc_auc": "roc_auc",
        "val_cohen_kappa_quadratic": "cohen_kappa_quadratic",
    }
    result: dict[str, float] = {}
    for src_k, dst_k in keys.items():
        vals = [m[src_k] for m in per_fold if src_k in m and not np.isnan(float(m[src_k]))]
        result[dst_k] = float(np.mean(vals)) if vals else float("nan")
    return result


def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _configs_to_run: list[str] | None = None,
) -> None:
    """Run Experiment 1: 2×2 factorial ablation on EyePACS.

    Args:
        config: Full merged config dict (global + experiment section).
        fold: If set, run only this fold index (0-based). Runs all 5 if None.
        resume: Resume interrupted training from last checkpoint.
        _subset_size: Internal override for smoke tests — limit CSV rows.
        _configs_to_run: Internal override — run only these config keys (e.g. ["A"]).
    """
    set_seed(config.get("seed", 42))

    # ── Paths ─────────────────────────────────────────────────────────────────
    eyepacs_root = config["paths"]["eyepacs"]
    labels_csv   = str(Path(eyepacs_root) / "trainLabels.csv")
    images_root  = str(Path(eyepacs_root) / "train")
    output_dir   = Path(config["paths"]["output_dir"]) / "exp1"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)
    metrics_csv  = output_dir / "metrics.csv"

    # ── Config sections ───────────────────────────────────────────────────────
    cv_cfg    = config["cross_validation"]
    aug_cfg   = config["augmentation"]
    preproc_cfg = config["preprocessing"]
    n_folds   = cv_cfg["n_folds"]
    fold_range = [fold] if fold is not None else list(range(n_folds))
    configs_to_run = _configs_to_run or list(_CONFIGS.keys())

    # ── Load index once ───────────────────────────────────────────────────────
    print(f"Loading EyePACS index from {labels_csv} …")
    all_paths, all_labels, all_pids = _load_eyepacs_index(
        images_root, labels_csv, subset_size=_subset_size
    )
    print(f"  Found {len(all_paths)} images | {len(set(all_pids))} patients")

    # ── Stratified patient-level subset ───────────────────────────────
    subset_cfg = config.get("subset", {})
    if subset_cfg.get("enabled", False):
        from sklearn.model_selection import train_test_split
        from collections import defaultdict, Counter

        fraction = subset_cfg["fraction"]
        sub_seed = subset_cfg.get("seed", 42)

        # Group by patient
        patient_to_indices: dict[str, list[int]] = defaultdict(list)
        for idx, pid in enumerate(all_pids):
            patient_to_indices[pid].append(idx)

        unique_patients = list(patient_to_indices.keys())
        patient_labels = [
            max(all_labels[i] for i in patient_to_indices[pid])
            for pid in unique_patients
        ]

        # Stratified patient-level subset
        selected_patients, _ = train_test_split(
            unique_patients,
            train_size=fraction,
            stratify=patient_labels,
            random_state=sub_seed,
        )
        selected_set = set(selected_patients)

        # Filter to selected patients only
        keep_idx = [i for i, pid in enumerate(all_pids) if pid in selected_set]
        all_paths = [all_paths[i] for i in keep_idx]
        all_labels = [all_labels[i] for i in keep_idx]
        all_pids = [all_pids[i] for i in keep_idx]

        print(f"  Subset mode: {fraction*100:.0f}% → {len(all_paths)} images | {len(selected_set)} patients")
        print(f"  Subset class distribution: {dict(sorted(Counter(all_labels).items()))}")

    # ── Patient-level splits ──────────────────────────────────────────────────
    splitter = PatientLevelKFold(
        n_folds=n_folds,
        seed=config.get("seed", 42),
        stratified=cv_cfg.get("stratified", True),
    )
    splits = splitter.split(all_paths, all_labels, all_pids)
    ok = splitter.verify_no_leakage(splits, all_pids)
    if not ok:
        raise RuntimeError("Patient leakage detected in CV splits — aborting.")
    print(f"  5-fold splits verified (no leakage)")

    # ── Trainer ───────────────────────────────────────────────────────────────
    trainer = Trainer(config, device="auto")
    augmentation = FundusAugmentation(aug_cfg)

    # ── Per-config results ────────────────────────────────────────────────────
    all_results: dict[str, list[dict]] = {cfg_key: [] for cfg_key in configs_to_run}

    for cfg_key in configs_to_run:
        cfg_spec = _CONFIGS[cfg_key]
        model_name   = cfg_spec["model"]
        preproc_kind = cfg_spec["preprocessing"]
        model_cfg    = config["models"][model_name]

        print(f"\n{'='*65}")
        print(f"  Config {cfg_key} | {preproc_kind} preprocessing | {model_name}")
        print(f"{'='*65}")

        # Build preprocessing pipelines (val never gets augmentation)
        train_preproc = _make_preprocessing(preproc_kind, preproc_cfg)
        val_preproc   = _make_preprocessing(preproc_kind, preproc_cfg)

        # Datasets — lazy, one per fold to avoid cross-contamination of aug
        for fold_idx in fold_range:
            train_idx, val_idx = splits[fold_idx]

            print(f"\n  [Config {cfg_key} | Fold {fold_idx+1}/{n_folds}]")
            print(f"  Train: {len(train_idx)} images | Val: {len(val_idx)} images")

            # Build train dataset (preprocessing + augmentation)
            train_ds = EyePACSDataset(
                image_paths=[all_paths[i] for i in train_idx],
                labels=[all_labels[i] for i in train_idx],
                patient_ids=[all_pids[i] for i in train_idx],
                preprocessing=train_preproc,
                augmentation=augmentation,
            )
            # Build val dataset (preprocessing only — no augmentation)
            val_ds = EyePACSDataset(
                image_paths=[all_paths[i] for i in val_idx],
                labels=[all_labels[i] for i in val_idx],
                patient_ids=[all_pids[i] for i in val_idx],
                preprocessing=val_preproc,
                augmentation=None,
            )

            train_loader = DataLoader(
                train_ds,
                batch_size=trainer.batch_size,
                shuffle=True,
                num_workers=trainer.num_workers,
                pin_memory=(trainer.device.type == "cuda"),
                drop_last=True,
                persistent_workers=(trainer.num_workers > 0),
                prefetch_factor=2 if trainer.num_workers > 0 else None,
            )
            val_loader = DataLoader(
                val_ds,
                batch_size=trainer.batch_size,
                shuffle=False,
                num_workers=trainer.num_workers,
                pin_memory=(trainer.device.type == "cuda"),
                persistent_workers=(trainer.num_workers > 0),
                prefetch_factor=2 if trainer.num_workers > 0 else None,
            )

            # Checkpoint directory per config + fold
            ckpt_dir = output_dir / "checkpoints" / f"{cfg_key}_fold{fold_idx}"
            ckpt_dir.mkdir(parents=True, exist_ok=True)
            ckpt_mgr = CheckpointManager(ckpt_dir, max_keep=5)

            # Fresh model for each fold
            model = create_model(model_name, model_cfg)

            best_metrics = trainer.train_fold(
                model=model,
                train_loader=train_loader,
                val_loader=val_loader,
                fold=fold_idx,
                config_name=cfg_key,
                checkpoint_mgr=ckpt_mgr,
                metrics_csv_path=metrics_csv,
                resume=resume,
            )
            all_results[cfg_key].append(best_metrics)

            f1  = best_metrics.get("val_weighted_f1",           float("nan"))
            auc = best_metrics.get("val_roc_auc",               float("nan"))
            kap = best_metrics.get("val_cohen_kappa_quadratic", float("nan"))
            acc = best_metrics.get("val_accuracy",              float("nan"))
            print(
                f"  Best → F1={f1:.4f}  AUC={auc:.4f}  "
                f"κ={kap:.4f}  acc={acc:.4f}"
            )

    # ── Summary + dominance tests ─────────────────────────────────────────────
    # Only emit summary when all requested folds for all configs have completed
    if fold is not None:
        print(f"\nSingle-fold run complete (fold {fold}). "
              f"Full summary emitted after all folds finish.")
        return

    # Compute mean metrics per config
    summary_configs: dict[str, dict] = {}
    for cfg_key in configs_to_run:
        if all_results[cfg_key]:
            summary_configs[cfg_key] = _compute_summary(all_results[cfg_key])

    dominance_tests: dict[str, dict] = {}
    h1_supported = False

    if all(k in summary_configs for k in ["A", "B", "C", "D"]):
        means_A = _mean_primary(all_results["A"])
        means_B = _mean_primary(all_results["B"])
        means_C = _mean_primary(all_results["C"])
        means_D = _mean_primary(all_results["D"])

        dom_B_vs_A = check_dominance(means_B, means_A)
        dom_D_vs_C = check_dominance(means_D, means_C)

        dominance_tests = {
            "B_vs_A": dom_B_vs_A,
            "D_vs_C": dom_D_vs_C,
        }
        h1_supported = dom_B_vs_A["overall_dominant"] and dom_D_vs_C["overall_dominant"]

    summary = {
        "configurations": summary_configs,
        "dominance_tests": dominance_tests,
        "h1_supported": h1_supported,
    }

    summary_path = output_dir / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    # ── Print summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Experiment 1 — Summary")
    print(f"{'='*65}")
    for cfg_key, cfg_summary in summary_configs.items():
        print(f"  Config {cfg_key} ({_CONFIGS.get(cfg_key, {}).get('preprocessing','?')}"
              f" + {_CONFIGS.get(cfg_key, {}).get('model','?')}):")
        for k, v in cfg_summary.items():
            print(f"    {k}: {v}")

    if dominance_tests:
        print(f"\n  Dominance tests (EH-3):")
        for test_name, result in dominance_tests.items():
            dom = result["overall_dominant"]
            print(f"    {test_name}: Δf1={result['f1_delta_pp']:.1f}pp  "
                  f"Δauc={result['auc_delta']:.4f}  "
                  f"Δκ={result['kappa_delta']:.4f}  "
                  f"dominant={dom}")

    h1_label = "SUPPORTED (EH-4)" if h1_supported else "NOT SUPPORTED"
    print(f"\n  H-1: {h1_label}")
    print(f"\n  Full summary saved to {summary_path}")
