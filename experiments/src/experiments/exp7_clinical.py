"""Experiment 7: Small Data Training (IDRiD → Clinical).

5-fold CV on IDRiD (516 grading images = 413 training + 103 testing sets
pooled) as training data; the Clinical dataset (60 images) is held out as a
fixed test set. Per RESEARCH_ARCHITECTURE §5.7, **both** the baseline
(stretch-resize + ImageNet-norm, 3ch) and the full preprocessing pipeline
(4ch) are trained, and results are reported as mean ± std across the 5 folds
with a bootstrap CI (≥1000 resamples) on the small Clinical test set (§6.8).

Each fold trains a fresh model on its IDRiD train split (early-stopped on the
IDRiD val split) and is then evaluated on the SAME held-out Clinical set, so
the 5 fold-models give a distribution of Clinical performance — the measure of
small-data trainability.

Normalization (TASK-fix #3): Exp 7 is the only experiment that *trains* on
IDRiD, so the full pipeline's Stage 7 uses IDRiD-specific normalize stats
(``data/processed/idrid_norm_stats.json`` via :func:`load_idrid_norm_stats`)
rather than the EyePACS stats reused by the cross-dataset transfer runs.

Output: <output_dir>/exp7/small_data_results.json
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader

from src.data.clinical_dataset import ClinicalDataset
from src.data.datasets import IDRiDDataset
from src.data.splits import PatientLevelKFold
from src.experiments._eval_utils import infer_dataset
# Canonical pipeline factory (handles preset selection, augmentation, and
# dataset-specific Stage-7 stats) — reused so Exp 7 builds the full/baseline
# pipelines identically to Exp 1.
from src.experiments.exp1_factorial import _make_preprocessing
from src.models.factory import create_model
from src.training.checkpoint import CheckpointManager
from src.training.trainer import Trainer
from src.utils.seed import set_seed

_PRIMARY_KEYS = (
    "weighted_f1",
    "roc_auc",
    "cohen_kappa_quadratic",
    "accuracy",
)
_BOOTSTRAP_ITERS = 1000
_CONFIDENCE = 0.95


def load_idrid_norm_stats(
    config: dict[str, Any],
) -> tuple[tuple[float, float, float], tuple[float, float, float]] | None:
    """Load IDRiD Stage 7 normalize stats, mirroring ``exp1_factorial``.

    Resolves ``data/processed/idrid_norm_stats.json`` relative to the
    configured output directory (same convention as the EyePACS loader in
    ``exp1_factorial``) and returns the per-channel ``(mean, std)`` tuples for
    the full pipeline (Stage 7, ``normalize_mode="dataset_specific"``).

    Args:
        config: Parsed experiment config dict (reads ``paths.output_dir``).

    Returns:
        ``(mean, std)`` 3-tuples in the [0, 1] scale, or ``None`` if the stats
        file is absent (caller should fall back to ImageNet and warn — NOT
        thesis-faithful for a train-on-IDRiD run).
    """
    processed_dir = (
        Path(config.get("paths", {}).get("output_dir", "outputs/")).parent
        / "data" / "processed"
    )
    stats_path = processed_dir / "idrid_norm_stats.json"
    if not stats_path.exists():
        print(f"  IDRiD normalize stats not found at {stats_path} — run "
              "scripts/compute_dataset_stats.py --dataset idrid to fix.")
        return None

    with open(stats_path) as f:
        stats = json.load(f)
    mean = tuple(float(x) for x in stats["mean"])
    std = tuple(float(x) for x in stats["std"])
    print(f"  IDRiD normalize stats loaded from {stats_path}")
    print(f"    mean={[round(x, 4) for x in mean]} std={[round(x, 4) for x in std]}")
    return mean, std  # type: ignore[return-value]


# ── Entry point ───────────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _configs_to_run: list[str] | None = None,
) -> None:
    """Run Experiment 7: small-data training IDRiD → Clinical.

    Args:
        config: Full merged config dict (global + ``experiment`` section).
        fold: If set, run only this fold index (0-based). Runs all folds if None.
            Cross-fold summary/bootstrap are emitted only on full (all-fold) runs.
        resume: Resume interrupted fold training from the last checkpoint.
        _subset_size: Limit IDRiD pool and Clinical rows for smoke tests.
        _configs_to_run: Unused — included for dispatch interface consistency.
            Exp 7 always trains both arms (baseline + full).
    """
    set_seed(config.get("seed", 42))

    output_dir = Path(config["paths"]["output_dir"]) / "exp7"
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_csv = output_dir / "metrics.csv"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = config.get("experiment", {}).get("model", "efficientnet_b3")

    # ── IDRiD Stage-7 normalize stats (full pipeline) ─────────────────────────
    stats = load_idrid_norm_stats(config)
    if stats is None:
        warnings.warn(
            "IDRiD normalize stats missing — full pipeline falls back to "
            "ImageNet normalization (NOT thesis-faithful for a train-on-IDRiD "
            "run). Run scripts/compute_dataset_stats.py --dataset idrid.",
            UserWarning,
        )
        idrid_mean = idrid_std = None
    else:
        idrid_mean, idrid_std = stats

    # ── IDRiD training pool (413 + 103 = 516) ─────────────────────────────────
    paths, labels, stems = _load_idrid_index(config, _subset_size)
    print(f"  IDRiD pool: {len(paths)} images | {len(set(stems))} unique stems")

    cv_cfg  = config["cross_validation"]
    n_folds = cv_cfg["n_folds"]
    splitter = PatientLevelKFold(
        n_folds=n_folds, seed=config.get("seed", 42),
        stratified=cv_cfg.get("stratified", True),
    )
    splits = splitter.split(paths, labels, stems)
    fold_range = [fold] if fold is not None else list(range(n_folds))

    # ── Shared trainer ────────────────────────────────────────────────────────
    trainer = Trainer(config, device="auto")
    trainer.mixed_precision = config.get("models", {}).get(
        model_name, {}
    ).get("mixed_precision", True)

    results: dict[str, Any] = {
        "experiment":   "exp7",
        "purpose":      "small-data trainability (IDRiD → Clinical)",
        "train_dataset": "idrid",
        "test_dataset":  "clinical",
        "model":        model_name,
        "n_idrid":      len(paths),
        "n_folds":      n_folds,
        "arms":         {},
    }

    for kind in ("baseline", "full"):
        print(f"\n{'#'*65}")
        print(f"#  Arm: {kind} preprocessing ({model_name})")
        print(f"{'#'*65}")
        results["arms"][kind] = _run_arm(
            kind, model_name, config, device, trainer,
            paths, labels, stems, splits, fold_range,
            idrid_mean, idrid_std, metrics_csv, output_dir, resume,
            single_fold=(fold is not None),
        )

    # ── Cross-arm comparison (full vs baseline) ───────────────────────────────
    if fold is None:
        b = results["arms"]["baseline"].get("clinical_mean", {}).get("weighted_f1")
        fl = results["arms"]["full"].get("clinical_mean", {}).get("weighted_f1")
        if isinstance(b, float) and isinstance(fl, float):
            results["full_minus_baseline_weighted_f1"] = round(fl - b, 6)

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = output_dir / "small_data_results.json"
    with open(out_path, "w") as f:
        json.dump(
            results, f, indent=2,
            default=lambda x: float(x) if isinstance(x, np.floating) else x,
        )
    print(f"\nResults saved → {out_path}")

    # ── Summary ───────────────────────────────────────────────────────────────
    if fold is not None:
        print(f"\nSingle-fold run complete (fold {fold}). "
              "Cross-fold summary emitted only on all-fold runs.")
        return

    print(f"\n{'='*65}")
    print("Experiment 7 — Small Data Training (IDRiD → Clinical) Summary")
    print(f"{'='*65}")
    for kind in ("baseline", "full"):
        arm = results["arms"][kind]
        summ = arm.get("clinical_summary", {})
        ci = arm.get("clinical_mean_f1_bootstrap_ci", {})
        print(f"  {kind:<9}: Clinical " +
              "  ".join(f"{k}={summ.get(k, 'n/a')}" for k in _PRIMARY_KEYS))
        if ci:
            print(f"             weighted_f1 mean={ci['mean']:.4f} "
                  f"[95% CI {ci['ci_lower']:.4f}, {ci['ci_upper']:.4f}]")
    if "full_minus_baseline_weighted_f1" in results:
        print(f"\n  Δ(full − baseline) Clinical weighted_f1 = "
              f"{results['full_minus_baseline_weighted_f1']:+.4f}")


# ── Per-arm training + evaluation ─────────────────────────────────────────────

def _run_arm(
    kind: str,
    model_name: str,
    config: dict[str, Any],
    device: torch.device,
    trainer: Trainer,
    paths: list[str],
    labels: list[int],
    stems: list[str],
    splits: list[tuple[list[int], list[int]]],
    fold_range: list[int],
    idrid_mean: tuple | None,
    idrid_std: tuple | None,
    metrics_csv: Path,
    output_dir: Path,
    resume: bool,
    single_fold: bool,
) -> dict[str, Any]:
    """Train one preprocessing arm over the requested folds and test on Clinical.

    Returns:
        Dict with per-fold Clinical metrics, mean±std summary, and a
        bootstrap CI on the across-fold mean Clinical weighted-F1.
    """
    in_channels = 3 if kind == "baseline" else 4
    model_cfg = {**config["models"][model_name], "in_channels": in_channels}

    per_fold: list[dict[str, Any]] = []
    clinical_preds: list[np.ndarray] = []
    clinical_true: np.ndarray | None = None

    for fold_idx in fold_range:
        train_idx, val_idx = splits[fold_idx]
        print(f"\n  [{kind} | Fold {fold_idx + 1}] "
              f"train={len(train_idx)}  val={len(val_idx)}")

        train_pp = _make_preprocessing(
            kind, model_name, is_training=True,
            dataset_mean=idrid_mean, dataset_std=idrid_std,
        )
        val_pp = _make_preprocessing(
            kind, model_name, is_training=False,
            dataset_mean=idrid_mean, dataset_std=idrid_std,
        )

        train_ds = _make_idrid_ds(paths, labels, stems, train_idx, train_pp)
        val_ds   = _make_idrid_ds(paths, labels, stems, val_idx, val_pp)
        clinical_ds = _build_clinical(config, val_pp, _clinical_subset(paths))

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

        ckpt_dir = output_dir / "checkpoints" / f"{kind}_fold{fold_idx}"
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_mgr = CheckpointManager(ckpt_dir, max_keep=2)

        model = create_model(model_name, model_cfg)
        best_val = trainer.train_fold(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            fold=fold_idx,
            config_name=f"exp7_{kind}",
            checkpoint_mgr=ckpt_mgr,
            metrics_csv_path=metrics_csv,
            resume=resume,
        )
        ckpt_mgr.load_best(model)
        model = model.to(device).eval()

        # ── Evaluate the trained fold-model on the held-out Clinical set ──────
        y_true, y_pred, _, cmetrics = infer_dataset(model, clinical_ds, config, device)
        clinical = {k.replace("val_", ""): cmetrics.get(f"val_{k}", float("nan"))
                    for k in _PRIMARY_KEYS}
        per_fold.append({
            "fold":         fold_idx,
            "idrid_val_f1": best_val.get("val_weighted_f1", float("nan")),
            "clinical":     clinical,
        })
        clinical_preds.append(y_pred)
        clinical_true = y_true
        print(f"    IDRiD val F1={best_val.get('val_weighted_f1', float('nan')):.4f}"
              f"  →  Clinical F1={clinical['weighted_f1']:.4f}")

    arm: dict[str, Any] = {"in_channels": in_channels, "per_fold": per_fold}

    # Cross-fold aggregation only makes sense for full (all-fold) runs.
    if not single_fold and per_fold:
        summary, means = _aggregate(per_fold)
        arm["clinical_summary"] = summary
        arm["clinical_mean"] = means
        if clinical_true is not None and len(clinical_preds) > 1:
            arm["clinical_mean_f1_bootstrap_ci"] = _bootstrap_mean_f1(
                clinical_true, clinical_preds
            )
    return arm


# ── Data helpers ──────────────────────────────────────────────────────────────

def _load_idrid_index(
    config: dict[str, Any], subset_size: int | None = None,
) -> tuple[list[str], list[int], list[str]]:
    """Read the pooled IDRiD grading index (training + testing sets).

    Args:
        config: Merged config (reads ``paths.idrid``).
        subset_size: Optional cap on the number of images (smoke tests).

    Returns:
        Tuple ``(image_paths, labels, patient_ids)``. IDRiD grading images are
        one-per-patient, so each gets a unique patient_id. The training and
        testing sets reuse the same stem numbering (``IDRiD_001`` appears in
        both for *different* patients), so the source set is prefixed to keep
        patient_ids unique and prevent erroneous CV grouping.
    """
    grading = Path(config["paths"]["idrid"]) / "B. Disease Grading"
    sources = [
        ("train",
         grading / "1. Original Images" / "a. Training Set",
         grading / "2. Groundtruths" / "a. IDRiD_Disease Grading_Training Labels.csv"),
        ("test",
         grading / "1. Original Images" / "b. Testing Set",
         grading / "2. Groundtruths" / "b. IDRiD_Disease Grading_Testing Labels.csv"),
    ]

    paths: list[str] = []
    labels: list[int] = []
    patient_ids: list[str] = []
    for set_tag, img_dir, csv_path in sources:
        df = pd.read_csv(csv_path, usecols=[0, 1])
        df.columns = ["image_name", "grade"]
        for _, row in df.iterrows():
            if pd.isna(row["image_name"]) or pd.isna(row["grade"]):
                continue
            stem = str(row["image_name"]).strip()
            img_path = img_dir / f"{stem}.jpg"
            if not img_path.exists():
                continue
            paths.append(str(img_path))
            labels.append(int(row["grade"]))
            patient_ids.append(f"{set_tag}_{stem}")   # unique per image/patient

    if subset_size is not None:
        paths = paths[:subset_size]
        labels = labels[:subset_size]
        patient_ids = patient_ids[:subset_size]
    return paths, labels, patient_ids


def _make_idrid_ds(
    paths: list[str],
    labels: list[int],
    stems: list[str],
    indices: list[int],
    preprocessing: Any,
) -> IDRiDDataset:
    """Construct an IDRiDDataset over the given row indices (no lesion masks)."""
    sub_paths = [paths[i] for i in indices]
    sub_labels = [labels[i] for i in indices]
    sub_stems = [stems[i] for i in indices]
    return IDRiDDataset(
        image_paths=sub_paths,
        labels=sub_labels,
        patient_ids=sub_stems,
        image_stems=sub_stems,
        masks_root=None,
        preprocessing=preprocessing,
        augmentation=None,
    )


def _clinical_subset(idrid_paths: list[str]) -> int | None:
    """Return a Clinical subset cap when running in smoke-test (subset) mode.

    The IDRiD pool is capped by ``_subset_size`` in smoke tests; mirror that on
    the Clinical side so the test set stays small too. Full runs return None.
    """
    # Heuristic: the full IDRiD pool is 516; anything materially smaller means
    # a subset/smoke run, so cap Clinical to a handful of images.
    return 8 if len(idrid_paths) < 100 else None


def _build_clinical(config: dict[str, Any], preprocessing: Any, subset: int | None):
    """Build the held-out Clinical dataset with the arm's inference pipeline."""
    clinical_root = Path(config["paths"]["clinical"])
    subset_indices = list(range(subset)) if subset else None
    return ClinicalDataset.from_directory(
        root=clinical_root,
        subset_indices=subset_indices,
        preprocessing=preprocessing,
    )


# ── Aggregation / statistics ──────────────────────────────────────────────────

def _aggregate(
    per_fold: list[dict[str, Any]],
) -> tuple[dict[str, str], dict[str, float]]:
    """Mean ± std (string) and mean (float) per primary Clinical metric."""
    summary: dict[str, str] = {}
    means: dict[str, float] = {}
    for k in _PRIMARY_KEYS:
        vals = [
            f["clinical"][k] for f in per_fold
            if k in f["clinical"] and not np.isnan(float(f["clinical"][k]))
        ]
        if vals:
            summary[k] = f"{np.mean(vals):.4f} ± {np.std(vals):.4f}"
            means[k] = float(np.mean(vals))
    return summary, means


def _bootstrap_mean_f1(
    y_true: np.ndarray,
    preds_per_fold: list[np.ndarray],
    n_iterations: int = _BOOTSTRAP_ITERS,
    confidence: float = _CONFIDENCE,
    seed: int = 42,
) -> dict[str, float]:
    """Bootstrap CI on the across-fold mean Clinical weighted-F1 (§6.8).

    Resamples the (small) Clinical test set with replacement; for each resample
    every fold-model is re-scored on the SAME indices and the per-fold F1s are
    averaged, yielding one bootstrap draw of the cross-fold mean F1.

    Args:
        y_true: Clinical ground-truth labels (shared across folds).
        preds_per_fold: Per-fold predicted labels on the Clinical set.
        n_iterations: Bootstrap resamples (≥1000 per §6.8).
        confidence: CI confidence level.
        seed: RNG seed.

    Returns:
        Dict with mean, ci_lower, ci_upper, std.
    """
    rng = np.random.default_rng(seed)
    n = len(y_true)
    draws: list[float] = []
    for _ in range(n_iterations):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        fold_f1s = [
            f1_score(yt, p[idx], average="weighted", zero_division=0)
            for p in preds_per_fold
        ]
        draws.append(float(np.mean(fold_f1s)))

    draws_arr = np.asarray(draws)
    tail = (1.0 - confidence) / 2
    return {
        "mean":     round(float(np.mean(draws_arr)), 6),
        "ci_lower": round(float(np.percentile(draws_arr, 100 * tail)), 6),
        "ci_upper": round(float(np.percentile(draws_arr, 100 * (1 - tail))), 6),
        "std":      round(float(np.std(draws_arr)), 6),
    }
