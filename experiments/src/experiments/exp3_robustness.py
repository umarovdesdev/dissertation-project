"""Experiment 3: Robustness to Image Degradation (H-3, PC-5).

Protocol:
  - Dataset: APTOS 2019 (patient-level 5-fold CV)
  - Model: EfficientNet-B3 with full preprocessing pipeline
  - Train on clean images; evaluate on clean AND degraded test folds
  - Degradation types: gaussian_noise, gaussian_blur, low_illumination
  - Severity levels: low, medium, high (parameters from config or defaults)
  - Binary clinical threshold: non-referable (0–1) vs referable (2–4)

Output: <output_dir>/exp3/degradation_results.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader

from src.data.augmentation import FundusAugmentation
from src.data.datasets import APTOS2019Dataset
from src.data.splits import PatientLevelKFold
from src.degradation.perturbations import DegradedDataset
from src.models.factory import create_model
from src.preprocessing.pipeline import PreprocessingPipeline
from src.training.checkpoint import CheckpointManager
from src.training.losses import compute_class_weights, create_weighted_loss
from src.training.trainer import Trainer
from src.utils.seed import set_seed

_DEGRADATION_TYPES: list[str] = [
    "gaussian_noise",
    "gaussian_blur",
    "low_illumination",
]
_SEVERITY_LEVELS: list[str] = ["low", "medium", "high"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_aptos_index(
    root: str,
    labels_csv: str,
    subset_size: int | None = None,
) -> tuple[list[str], list[int], list[str]]:
    """Load APTOS 2019 image paths, labels, and patient IDs.

    Args:
        root: Path to train_images/ directory.
        labels_csv: Path to train.csv (columns: id_code, diagnosis).
        subset_size: If set, limit to this many rows (for smoke tests).

    Returns:
        Tuple of (image_paths, labels, patient_ids).
    """
    import pandas as pd

    root = Path(root)
    df = pd.read_csv(labels_csv)
    if subset_size is not None:
        df = df.iloc[:subset_size].reset_index(drop=True)

    paths, labels, pids = [], [], []
    for _, row in df.iterrows():
        id_code = str(row["id_code"])
        p = root / f"{id_code}.png"
        if not p.exists():
            continue
        paths.append(str(p))
        labels.append(int(row["diagnosis"]))
        pids.append(id_code)
    return paths, labels, pids


def _compute_binary_clinical_roc_auc(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    referable_threshold: int = 2,
) -> float:
    """Compute ROC-AUC for binary referable DR screening.

    Positive class probability = sum of softmax probabilities for classes
    >= referable_threshold (grades 2, 3, 4).

    Args:
        y_true: Ground-truth integer labels, shape (N,).
        y_prob: Softmax probabilities, shape (N, num_classes).
        referable_threshold: Grade at which DR becomes referable.

    Returns:
        ROC-AUC scalar, or NaN if only one class is present.
    """
    y_true_bin = (np.asarray(y_true) >= referable_threshold).astype(int)
    referable_prob = y_prob[:, referable_threshold:].sum(axis=1)
    try:
        return float(roc_auc_score(y_true_bin, referable_prob))
    except ValueError:
        return float("nan")


def _evaluate_on_dataset(
    trainer: Trainer,
    model: torch.nn.Module,
    dataset: APTOS2019Dataset | DegradedDataset,
    batch_size: int,
    num_workers: int,
) -> tuple[dict[str, float], np.ndarray, np.ndarray, np.ndarray]:
    """Run trainer.evaluate on a dataset and return metrics + arrays.

    Args:
        trainer: Trained Trainer instance.
        model: Trained model.
        dataset: Dataset to evaluate on.
        batch_size: DataLoader batch size.
        num_workers: DataLoader num_workers.

    Returns:
        Tuple of (metrics_dict, all_preds, all_probs, all_labels).
    """
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=(trainer.device.type == "cuda"),
    )
    # Use a dummy unweighted criterion for evaluation (no weight needed)
    import torch.nn as nn
    criterion = nn.CrossEntropyLoss()
    return trainer.evaluate(model, loader, criterion)


def _metrics_subset(metrics: dict[str, float]) -> dict[str, float]:
    """Extract the primary metrics from a full metrics dict."""
    keys = [
        "val_weighted_f1", "val_roc_auc",
        "val_cohen_kappa_quadratic", "val_accuracy",
        "val_sensitivity", "val_specificity", "val_ppv", "val_npv",
    ]
    return {k.replace("val_", ""): metrics.get(k, float("nan")) for k in keys}


def _fold_mean_std(fold_dicts: list[dict[str, float]]) -> tuple[dict, dict]:
    """Compute per-key mean and std across folds."""
    keys = fold_dicts[0].keys() if fold_dicts else []
    mean_d: dict[str, float] = {}
    std_d:  dict[str, float] = {}
    for k in keys:
        vals = [d[k] for d in fold_dicts if not np.isnan(d.get(k, float("nan")))]
        mean_d[k] = float(np.mean(vals)) if vals else float("nan")
        std_d[k]  = float(np.std(vals))  if vals else float("nan")
    return mean_d, std_d


def _delta(degraded: dict[str, float], clean: dict[str, float]) -> dict[str, float]:
    """Compute per-key delta (degraded − clean)."""
    return {
        k: float(degraded.get(k, float("nan")) - clean.get(k, float("nan")))
        for k in clean
    }


# ── Main entry point ──────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _deg_types: list[str] | None = None,
    _severity_levels: list[str] | None = None,
) -> None:
    """Run Experiment 3: robustness to image degradation.

    Args:
        config: Full merged config dict.
        fold: If set, run only this fold index.
        resume: Resume from checkpoint if available.
        _subset_size: Limit APTOS images (smoke test).
        _deg_types: Override degradation types to test (smoke test).
        _severity_levels: Override severity levels (smoke test).
    """
    set_seed(config.get("seed", 42))
    seed = config.get("seed", 42)

    output_dir = Path(config["paths"]["output_dir"]) / "exp3"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)
    metrics_csv = output_dir / "metrics.csv"

    cv_cfg      = config["cross_validation"]
    preproc_cfg = config["preprocessing"]
    aug_cfg     = config["augmentation"]
    n_folds     = cv_cfg["n_folds"]
    fold_range  = [fold] if fold is not None else list(range(n_folds))

    model_name  = "efficientnet_b3"
    model_cfg   = config["models"][model_name]

    trainer     = Trainer(config, device="auto")

    deg_types      = _deg_types      if _deg_types      is not None else _DEGRADATION_TYPES
    severity_levels = _severity_levels if _severity_levels is not None else _SEVERITY_LEVELS

    # ── Load APTOS index ──────────────────────────────────────────────────────
    aptos_root  = config["paths"]["aptos"]
    labels_csv  = str(Path(aptos_root) / "train.csv")
    images_root = str(Path(aptos_root) / "train_images")

    print("Loading APTOS 2019 index …")
    all_paths, all_labels, all_pids = _load_aptos_index(
        images_root, labels_csv, subset_size=_subset_size
    )
    print(f"  {len(all_paths)} images | {len(set(all_pids))} patients")

    # Patient-level 5-fold CV
    splitter = PatientLevelKFold(
        n_folds=n_folds, seed=seed,
        stratified=cv_cfg.get("stratified", True),
    )
    splits = splitter.split(all_paths, all_labels, all_pids)
    ok = splitter.verify_no_leakage(splits, all_pids)
    if not ok:
        raise RuntimeError("Patient leakage in CV splits — aborting.")
    print(f"  {n_folds}-fold splits verified (no leakage)")

    # Full preprocessing pipeline (all 5 components)
    pipeline = PreprocessingPipeline.create_full(
        config={
            "target_size": preproc_cfg.get("target_size", 512),
            "clahe_clip_limit": preproc_cfg.get("clahe", {}).get("clip_limit", 2.0),
            "clahe_grid_size":  preproc_cfg.get("clahe", {}).get("tile_grid_size", [8, 8]),
            "saturation_scale": preproc_cfg.get("hsv", {}).get("saturation_scale", 1.2),
            "value_scale":      preproc_cfg.get("hsv", {}).get("value_scale", 1.1),
        }
    )
    augmentation = FundusAugmentation(aug_cfg)

    # ── Per-fold accumulators ─────────────────────────────────────────────────
    # clean_fold_metrics: list of per-fold metric dicts
    # deg_fold_metrics: {deg_type: {severity: [per-fold metric dict, ...]}}
    clean_fold_metrics: list[dict] = []
    clean_fold_binary_auc: list[float] = []

    deg_fold_metrics: dict[str, dict[str, list[dict]]] = {
        dt: {sv: [] for sv in severity_levels} for dt in deg_types
    }
    deg_fold_binary_auc: dict[str, dict[str, list[float]]] = {
        dt: {sv: [] for sv in severity_levels} for dt in deg_types
    }

    # ── Per-fold training + evaluation ────────────────────────────────────────
    for fold_idx in fold_range:
        train_idx, val_idx = splits[fold_idx]
        print(f"\n{'='*65}")
        print(f"Fold {fold_idx + 1}/{n_folds}")
        print(f"{'='*65}")

        # -- Build datasets ---------------------------------------------------
        train_ds = APTOS2019Dataset(
            image_paths=[all_paths[i] for i in train_idx],
            labels=[all_labels[i] for i in train_idx],
            patient_ids=[all_pids[i] for i in train_idx],
            preprocessing=pipeline,
            augmentation=augmentation,
        )
        # Clean validation dataset (no augmentation)
        val_ds_clean = APTOS2019Dataset(
            image_paths=[all_paths[i] for i in val_idx],
            labels=[all_labels[i] for i in val_idx],
            patient_ids=[all_pids[i] for i in val_idx],
            preprocessing=pipeline,
            augmentation=None,
        )

        train_loader = DataLoader(
            train_ds,
            batch_size=trainer.batch_size,
            shuffle=True,
            num_workers=trainer.num_workers,
            pin_memory=(trainer.device.type == "cuda"),
            drop_last=True,
        )
        val_loader_clean = DataLoader(
            val_ds_clean,
            batch_size=trainer.batch_size,
            shuffle=False,
            num_workers=trainer.num_workers,
            pin_memory=(trainer.device.type == "cuda"),
        )

        # -- Train ------------------------------------------------------------
        ckpt_dir = output_dir / "checkpoints" / f"full_pipeline_fold{fold_idx}"
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_mgr = CheckpointManager(ckpt_dir, max_keep=5)
        model    = create_model(model_name, model_cfg)

        best_metrics = trainer.train_fold(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader_clean,
            fold=fold_idx,
            config_name="exp3_full_pipeline",
            checkpoint_mgr=ckpt_mgr,
            metrics_csv_path=metrics_csv,
            resume=resume,
        )
        f1 = best_metrics.get("val_weighted_f1", float("nan"))
        print(f"  Training done — Best clean F1={f1:.4f}")

        # Load the best checkpoint for evaluation
        best_ckpt = ckpt_mgr.load_best(model)
        if best_ckpt is None:
            print("  WARNING: no best checkpoint found — using final model state")

        # -- Evaluate on clean ------------------------------------------------
        m_clean, preds_c, probs_c, labels_c = _evaluate_on_dataset(
            trainer, model, val_ds_clean,
            trainer.batch_size, trainer.num_workers,
        )
        bin_auc_clean = _compute_binary_clinical_roc_auc(labels_c, probs_c)
        clean_fold_metrics.append(_metrics_subset(m_clean))
        clean_fold_binary_auc.append(bin_auc_clean)
        print(f"  Clean eval: weighted_F1={m_clean.get('val_weighted_f1', float('nan')):.4f}  "
              f"binary_ROC-AUC={bin_auc_clean:.4f}")

        # -- Evaluate on degraded versions ------------------------------------
        for deg_type in deg_types:
            for severity in severity_levels:
                deg_ds = DegradedDataset(
                    base_dataset=val_ds_clean,
                    deg_type=deg_type,
                    severity=severity,
                    config=config,
                )
                m_deg, preds_d, probs_d, labels_d = _evaluate_on_dataset(
                    trainer, model, deg_ds,
                    trainer.batch_size, trainer.num_workers,
                )
                bin_auc_deg = _compute_binary_clinical_roc_auc(labels_d, probs_d)

                deg_fold_metrics[deg_type][severity].append(_metrics_subset(m_deg))
                deg_fold_binary_auc[deg_type][severity].append(bin_auc_deg)

                f1_deg = m_deg.get("val_weighted_f1", float("nan"))
                delta  = f1_deg - m_clean.get("val_weighted_f1", float("nan"))
                print(f"  [{deg_type}/{severity}] F1={f1_deg:.4f}  "
                      f"ΔF1={delta:+.4f}  binary_AUC={bin_auc_deg:.4f}")

    # ── Aggregate results across folds ────────────────────────────────────────
    clean_mean, clean_std = _fold_mean_std(clean_fold_metrics)
    clean_bin_auc_mean = float(np.nanmean(clean_fold_binary_auc))
    clean_bin_auc_std  = float(np.nanstd(clean_fold_binary_auc))

    results: dict[str, Any] = {
        "model":    model_name,
        "pipeline": "full_pipeline",
        "dataset":  "APTOS2019",
        "n_folds":  len(fold_range),
        "folds_run": fold_range,
        "clean": {
            "per_fold":           clean_fold_metrics,
            "mean":               clean_mean,
            "std":                clean_std,
            "binary_roc_auc_mean": clean_bin_auc_mean,
            "binary_roc_auc_std":  clean_bin_auc_std,
        },
        "degradations": {},
    }

    for deg_type in deg_types:
        results["degradations"][deg_type] = {}
        for severity in severity_levels:
            fold_mets  = deg_fold_metrics[deg_type][severity]
            fold_aucs  = deg_fold_binary_auc[deg_type][severity]

            mean_d, std_d = _fold_mean_std(fold_mets)
            delta_mean    = _delta(mean_d, clean_mean)

            bin_auc_mean = float(np.nanmean(fold_aucs))
            bin_auc_std  = float(np.nanstd(fold_aucs))
            bin_auc_delta = bin_auc_mean - clean_bin_auc_mean

            results["degradations"][deg_type][severity] = {
                "per_fold":             fold_mets,
                "mean":                 mean_d,
                "std":                  std_d,
                "delta_mean":           delta_mean,
                "binary_roc_auc_mean":  bin_auc_mean,
                "binary_roc_auc_std":   bin_auc_std,
                "binary_roc_auc_delta": bin_auc_delta,
            }

    # ── Save results ──────────────────────────────────────────────────────────
    out_path = output_dir / "degradation_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
    print(f"\nResults saved → {out_path}")

    # ── Print summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Experiment 3 — Degradation Robustness Summary")
    print(f"{'='*65}")
    print(f"  Clean F1={clean_mean.get('weighted_f1', float('nan')):.4f} "
          f"± {clean_std.get('weighted_f1', float('nan')):.4f}  "
          f"binary_AUC={clean_bin_auc_mean:.4f}")
    for deg_type in deg_types:
        for severity in severity_levels:
            entry = results["degradations"][deg_type][severity]
            f1    = entry["mean"].get("weighted_f1", float("nan"))
            df1   = entry["delta_mean"].get("weighted_f1", float("nan"))
            bauc  = entry["binary_roc_auc_mean"]
            print(f"  {deg_type}/{severity:<8}: F1={f1:.4f}  ΔF1={df1:+.4f}  "
                  f"binary_AUC={bauc:.4f}")
