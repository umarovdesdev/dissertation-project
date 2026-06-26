"""Experiment 1: 2×2 Factorial — Preprocessing Dominance (H-1).

Tests whether the preprocessing pipeline produces statistically dominant
improvement over resize-only baseline, independently for ResNet-50 and
EfficientNet-B3 (dominance criteria: ΔF1≥5pp, ΔAUC≥0.02, no κ degradation).

Configurations:
  A — baseline (stretch-resize+ImageNet norm, 3ch) + ResNet-50
  B — full pipeline (4ch)                       + ResNet-50
  C — baseline (stretch-resize+ImageNet norm, 3ch) + EfficientNet-B3
  D — full pipeline (4ch)                       + EfficientNet-B3
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from src.data.datasets import (
    CachedEyePACSDataset,
    EyePACSDataset,
    EyePACSPatientPairDataset,
    load_cache_meta,
    patient_pair_collate,
)
from src.data.splits import PatientLevelKFold
from src.evaluation.metrics import check_dominance
from src.models.factory import create_model, create_patient_model
from src.ssl.loader import load_ssl_backbone
from src.preprocessing.config import PreprocessingConfig
from src.preprocessing.pipeline import PreprocessingPipeline
from src.training.checkpoint import CheckpointManager
from src.training.patient_trainer import PatientTrainer
from src.training.trainer import Trainer
from src.utils.seed import set_seed


# ── Factorial design ──────────────────────────────────────────────────────────
_CONFIGS: dict[str, dict[str, Any]] = {
    "A": {"preprocessing": "baseline", "model": "resnet50",        "in_channels": 3},
    "B": {"preprocessing": "full",     "model": "resnet50",        "in_channels": 4},
    "C": {"preprocessing": "baseline", "model": "efficientnet_b3", "in_channels": 3},
    "D": {"preprocessing": "full",     "model": "efficientnet_b3", "in_channels": 4},
}


# ── preprocessing factory ──────────────────────────────────────────────────

def _make_preprocessing(
    kind: str,
    model_name: str,
    is_training: bool,
    dataset_mean: tuple[float, float, float] | None = None,
    dataset_std: tuple[float, float, float] | None = None,
) -> PreprocessingPipeline:
    """Build a preprocessing pipeline.

    Args:
        kind: ``"baseline"`` (stretch-resize + ImageNet normalize, 3ch) or
            ``"full"`` (all stages, 4ch, model-specific preset).
        model_name: ``"resnet50"`` or ``"efficientnet_b3"`` — selects the
            augmentation preset for the full pipeline.
        is_training: Enables stochastic CLAHE and augmentation when ``True``.
        dataset_mean: EyePACS-computed per-channel mean for Stage 7
            dataset-specific normalize (full pipeline only). ``None`` falls
            back to ImageNet stats (and prints a warning).
        dataset_std: EyePACS-computed per-channel std (see ``dataset_mean``).

    Returns:
        Configured :class:`~src.preprocessing.pipeline.PreprocessingPipeline`.
    """
    if kind == "baseline":
        return PreprocessingPipeline.create_baseline(
            target_size=512,
            is_training=is_training,
        )

    preset_name = "efficientnet" if "efficientnet" in model_name else "resnet"
    config = PreprocessingConfig.from_preset(preset_name)

    # Stage 7: dataset-specific normalize (D-2). The preset leaves these None,
    # which silently falls back to ImageNet — not the thesis-defended pipeline
    # for the full configs. Inject EyePACS-computed stats when available.
    if dataset_mean is not None and dataset_std is not None:
        config.dataset_mean = tuple(dataset_mean)
        config.dataset_std = tuple(dataset_std)

    if is_training:
        return PreprocessingPipeline.create_for_training(config)
    return PreprocessingPipeline.create_for_inference(config)


# ── Initialization (CFC-2.8): ImageNet vs gated fundus-SSL ─────────────────────

# experiments/ root, used to resolve relative SSL checkpoint paths from config.
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_init(config: dict[str, Any], cfg_key: str) -> dict[str, Any]:
    """Resolve the per-config init spec from the Exp-1 config (brief §10.2).

    Reads ``config["experiment"]["configurations"][cfg_key]["init"]``. Defaults
    to ImageNet when absent, preserving the legacy behaviour for any config that
    does not declare an ``init`` block.

    Args:
        config: Full merged config dict (with an ``experiment`` section).
        cfg_key: Config key (``"A"``–``"D"``).

    Returns:
        Init spec dict, e.g. ``{"source": "imagenet"}`` or
        ``{"source": "ssl", "ckpt": "outputs/ssl/.../*.pt"}``.
    """
    confs = config.get("experiment", {}).get("configurations", {})
    entry = confs.get(cfg_key, {}) if isinstance(confs, dict) else {}
    init = entry.get("init") if isinstance(entry, dict) else None
    return init if isinstance(init, dict) else {"source": "imagenet"}


def _build_model_with_init(
    model_name: str,
    model_cfg: dict[str, Any],
    cfg_key: str,
    config: dict[str, Any],
):
    """Build the config's model, honouring CFC-2.8 initialization (brief §10).

    - ``source: imagenet`` (baseline arm A/C) → factory ``pretrained=True``.
    - ``source: ssl`` (pipeline arm B/D) → factory ``pretrained=False`` then
      :func:`load_ssl_backbone`, with a fail-fast ``gate_passed`` guard so no
      ungated init enters the experiment.

    Args:
        model_name: Backbone name.
        model_cfg: Model config dict (carries ``in_channels`` etc.).
        cfg_key: Config key (``"A"``–``"D"``).
        config: Full merged config dict.

    Returns:
        A model ready for fine-tuning (fresh 5-class head for the SSL arm).
    """
    init = _resolve_init(config, cfg_key)
    source = str(init.get("source", "imagenet")).lower()
    if source != "ssl":
        return create_model(model_name, model_cfg)

    ckpt_rel = init.get("ckpt")
    if not ckpt_rel:
        raise ValueError(
            f"Config {cfg_key} declares init.source=ssl but no init.ckpt path."
        )
    ckpt_path = Path(ckpt_rel)
    if not ckpt_path.is_absolute():
        ckpt_path = _REPO_ROOT / ckpt_path

    ssl_model_cfg = {**model_cfg, "pretrained": False}
    model = create_model(model_name, ssl_model_cfg)
    meta = load_ssl_backbone(model, ckpt_path, require_gate_passed=True)
    print(f"  Init: SSL ({meta.get('method')} / {meta.get('ssl_corpus')}) "
          f"loaded from {ckpt_path.name}; gate_passed={meta.get('gate_passed')}")
    return model


# ── Data helpers ──────────────────────────────────────────────────────────────

def _load_eyepacs_index(
    root: str,
    labels_csv: str,
    subset_size: int | None = None,
) -> tuple[list[str], list[int], list[str], list[str]]:
    """Read EyePACS paths/labels/patient_ids/eye_sides without constructing a Dataset.

    Filters to only files that exist on disk. Optionally limits to the first
    *subset_size* rows of the CSV (for smoke tests).

    Args:
        root: Path to train/ directory.
        labels_csv: Path to trainLabels.csv.
        subset_size: If set, use only the first N CSV rows.

    Returns:
        Tuple ``(image_paths, labels, patient_ids, eye_sides)``.
    """
    root_path = Path(root)
    df = pd.read_csv(labels_csv)
    if subset_size is not None:
        df = df.iloc[:subset_size].reset_index(drop=True)

    paths: list[str] = []
    labels: list[int] = []
    pids: list[str] = []
    eye_sides: list[str] = []

    for _, row in df.iterrows():
        name = str(row["image"])
        p = root_path / f"{name}.jpeg"
        if not p.exists():
            continue
        paths.append(str(p))
        labels.append(int(row["level"]))
        pids.append(name.split("_")[0])
        eye_sides.append("left" if "_left" in name else "right")

    return paths, labels, pids, eye_sides


def _load_cache_index(
    cache_dir: str,
    subset_size: int | None = None,
) -> tuple[list[str], list[int], list[str], list[str]]:
    """Read the cache index (drop-in for :func:`_load_eyepacs_index`).

    Uses the cache's self-contained ``trainLabels.csv``; "paths" are the cached
    ``<name>.png`` files, filtered to those present on disk.

    Args:
        cache_dir: Directory written by ``scripts/precompute_cache.py``.
        subset_size: If set, use only the first N CSV rows (smoke tests).

    Returns:
        Tuple ``(cache_png_paths, labels, patient_ids, eye_sides)``.
    """
    cache_path = Path(cache_dir)
    df = pd.read_csv(cache_path / "trainLabels.csv")
    if subset_size is not None:
        df = df.iloc[:subset_size].reset_index(drop=True)

    paths: list[str] = []
    labels: list[int] = []
    pids: list[str] = []
    eye_sides: list[str] = []

    for _, row in df.iterrows():
        name = str(row["image"])
        p = cache_path / f"{name}.png"
        if not p.exists():
            continue
        paths.append(str(p))
        labels.append(int(row["level"]))
        pids.append(name.split("_")[0])
        eye_sides.append("left" if "_left" in name else "right")

    return paths, labels, pids, eye_sides


def _build_patient_data(
    paths: list[str],
    labels: list[int],
    pids: list[str],
    eye_sides: list[str],
) -> dict[str, dict]:
    """Group image-level lists into a patient_data dict for EyePACSPatientPairDataset.

    Args:
        paths: Image paths.
        labels: DR grade labels.
        pids: Patient ID strings.
        eye_sides: ``"left"`` or ``"right"`` per image.

    Returns:
        Dict mapping patient_id → ``{left_path, right_path, left_label, right_label}``.
    """
    patient_data: dict[str, dict] = {}
    for path, label, pid, side in zip(paths, labels, pids, eye_sides):
        if pid not in patient_data:
            patient_data[pid] = {
                "left_path": None,
                "right_path": None,
                "left_label": None,
                "right_label": None,
            }
        patient_data[pid][f"{side}_path"] = path
        patient_data[pid][f"{side}_label"] = label
    return patient_data


# ── Summary helpers ───────────────────────────────────────────────────────────

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


# ── Main entry point ──────────────────────────────────────────────────────────

def run(
    config: dict[str, Any],
    fold: int | None = None,
    resume: bool = False,
    _subset_size: int | None = None,
    _configs_to_run: list[str] | None = None,
) -> None:
    """Run Experiment 1: 2×2 factorial ablation (+ optional blending) on EyePACS.

    Args:
        config: Full merged config dict (global + experiment section).
        fold: If set, run only this fold index (0-based). Runs all folds if None.
        resume: Resume interrupted training from last checkpoint.
        _subset_size: Internal override for smoke tests — limit CSV rows.
        _configs_to_run: Internal override — run only these config keys (e.g. ``["A"]``).
    """
    set_seed(config.get("seed", 42))

    # ── Paths ─────────────────────────────────────────────────────────────────
    eyepacs_root = config["paths"]["eyepacs"]
    labels_csv   = str(Path(eyepacs_root) / "trainLabels.csv")
    images_root  = str(Path(eyepacs_root) / "train")
    # Optional Stage 0–4 cache (throughput fix, TASK §2). When set, the full
    # configs (B/D) read cached PNGs and run only Stages 5–7 per epoch.
    cache_dir = config.get("paths", {}).get("cache_dir")
    output_dir   = Path(config["paths"]["output_dir"]) / "exp1"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)
    metrics_csv  = output_dir / "metrics.csv"

    # ── Config sections ───────────────────────────────────────────────────────
    cv_cfg    = config["cross_validation"]
    n_folds   = cv_cfg["n_folds"]
    fold_range = [fold] if fold is not None else list(range(n_folds))
    configs_to_run = _configs_to_run or list(_CONFIGS.keys())

    # ── Dataset-specific normalize stats (Stage 7, D-2) ───────────────────────
    # Computed by scripts/compute_dataset_stats.py (Stages 0–4, mask=1.0 only).
    # Consumed by the full configs (B/D). Absent → ImageNet fallback (warned).
    processed_dir = Path(config.get("paths", {}).get("output_dir", "outputs/")).parent / "data" / "processed"
    dataset_mean: tuple[float, float, float] | None = None
    dataset_std: tuple[float, float, float] | None = None
    stats_path = processed_dir / "eyepacs_norm_stats.json"
    if stats_path.exists():
        with open(stats_path) as f:
            _stats = json.load(f)
        dataset_mean = tuple(_stats["mean"])
        dataset_std = tuple(_stats["std"])
        print(f"  Dataset normalize stats loaded from {stats_path}")
        print(f"    mean={[round(x, 4) for x in dataset_mean]} "
              f"std={[round(x, 4) for x in dataset_std]}")
    else:
        print("  Dataset normalize stats not found — full configs (B/D) will "
              "fall back to ImageNet (NOT thesis-faithful). Run "
              "scripts/compute_dataset_stats.py to fix.")

    # ── Load index once ───────────────────────────────────────────────────────
    cache_meta: dict[str, tuple[bool, float]] | None = None
    if cache_dir:
        print(f"Loading cache index from {cache_dir} …")
        all_paths, all_labels, all_pids, all_eye_sides = _load_cache_index(
            cache_dir, subset_size=_subset_size
        )
        cache_meta = load_cache_meta(cache_dir)
        print(f"  Found {len(all_paths)} cached images | {len(set(all_pids))} patients "
              f"| {len(cache_meta)} meta rows")
    else:
        print(f"Loading EyePACS index from {labels_csv} …")
        all_paths, all_labels, all_pids, all_eye_sides = _load_eyepacs_index(
            images_root, labels_csv, subset_size=_subset_size
        )
        print(f"  Found {len(all_paths)} images | {len(set(all_pids))} patients")

    # ── Stratified patient-level subset ───────────────────────────────────────
    subset_cfg = config.get("subset", {})
    if subset_cfg.get("enabled", False):
        from collections import Counter, defaultdict
        from sklearn.model_selection import train_test_split

        fraction = subset_cfg["fraction"]
        sub_seed = subset_cfg.get("seed", 42)

        patient_to_indices: dict[str, list[int]] = defaultdict(list)
        for idx, pid in enumerate(all_pids):
            patient_to_indices[pid].append(idx)

        unique_patients = list(patient_to_indices.keys())
        patient_labels = [
            max(all_labels[i] for i in patient_to_indices[pid])
            for pid in unique_patients
        ]

        selected_patients, _ = train_test_split(
            unique_patients,
            train_size=fraction,
            stratify=patient_labels,
            random_state=sub_seed,
        )
        selected_set = set(selected_patients)

        keep_idx = [i for i, pid in enumerate(all_pids) if pid in selected_set]
        all_paths     = [all_paths[i]     for i in keep_idx]
        all_labels    = [all_labels[i]    for i in keep_idx]
        all_pids      = [all_pids[i]      for i in keep_idx]
        all_eye_sides = [all_eye_sides[i] for i in keep_idx]

        print(f"  Subset mode: {fraction*100:.0f}% → {len(all_paths)} images | "
              f"{len(selected_set)} patients")
        print(f"  Subset class distribution: {dict(sorted(Counter(all_labels).items()))}")

    # ── Patient-level splits ──────────────────────────────────────────────────
    splitter = PatientLevelKFold(
        n_folds=n_folds,
        seed=config.get("seed", 42),
        stratified=cv_cfg.get("stratified", True),
    )
    splits = splitter.split(all_paths, all_labels, all_pids)
    if not splitter.verify_no_leakage(splits, all_pids):
        raise RuntimeError("Patient leakage detected in CV splits — aborting.")
    print(f"  {n_folds}-fold splits verified (no leakage)")

    # ── Trainers ──────────────────────────────────────────────────────────────
    trainer         = Trainer(config, device="auto")
    patient_trainer = PatientTrainer(config, device="auto")

    # ── Per-config results ────────────────────────────────────────────────────
    all_results: dict[str, list[dict]] = {cfg_key: [] for cfg_key in configs_to_run}

    for cfg_key in configs_to_run:
        cfg_spec     = _CONFIGS[cfg_key]
        model_name   = cfg_spec["model"]
        preproc_kind = cfg_spec["preprocessing"]
        in_channels  = cfg_spec.get("in_channels", 4)
        model_cfg    = {**config["models"][model_name], "in_channels": in_channels}

        # Mixed precision: read from per-model config (D-6 design decision)
        use_amp = config.get("models", {}).get(model_name, {}).get("mixed_precision", True)
        trainer.mixed_precision         = use_amp
        patient_trainer.mixed_precision = use_amp

        print(f"\n{'='*65}")
        print(f"  Config {cfg_key} | {preproc_kind} preprocessing | {model_name} | in_channels={in_channels}")
        print(f"{'='*65}")

        for fold_idx in fold_range:
            train_idx, val_idx = splits[fold_idx]

            print(f"\n  [Config {cfg_key} | Fold {fold_idx+1}/{n_folds}]")
            print(f"  Train: {len(train_idx)} images | Val: {len(val_idx)} images")

            # Slice index lists for this fold
            tr_paths  = [all_paths[i]     for i in train_idx]
            tr_labels = [all_labels[i]    for i in train_idx]
            tr_pids   = [all_pids[i]      for i in train_idx]
            tr_sides  = [all_eye_sides[i] for i in train_idx]

            va_paths  = [all_paths[i]     for i in val_idx]
            va_labels = [all_labels[i]    for i in val_idx]
            va_pids   = [all_pids[i]      for i in val_idx]
            va_sides  = [all_eye_sides[i] for i in val_idx]

            # preprocessing pipelines (augmentation integrated into train pipeline)
            train_preproc = _make_preprocessing(
                preproc_kind, model_name, is_training=True,
                dataset_mean=dataset_mean, dataset_std=dataset_std,
            )
            val_preproc = _make_preprocessing(
                preproc_kind, model_name, is_training=False,
                dataset_mean=dataset_mean, dataset_std=dataset_std,
            )

            ckpt_dir = output_dir / "checkpoints" / f"{cfg_key}_fold{fold_idx}"
            ckpt_dir.mkdir(parents=True, exist_ok=True)

            # ── Configs A–D: standard single-image training ────────────────
            if cache_dir and preproc_kind == "full":
                # Throughput fix: read cached Stage 0–4 PNGs, run only 5–7.
                train_ds = CachedEyePACSDataset(
                    image_paths=tr_paths, labels=tr_labels, patient_ids=tr_pids,
                    preprocessing=train_preproc, cache_meta=cache_meta,
                    eye_sides=tr_sides,
                )
                val_ds = CachedEyePACSDataset(
                    image_paths=va_paths, labels=va_labels, patient_ids=va_pids,
                    preprocessing=val_preproc, cache_meta=cache_meta,
                    eye_sides=va_sides,
                )
            elif cache_dir and preproc_kind == "baseline":
                raise ValueError(
                    f"paths.cache_dir is set but Config {cfg_key} is baseline; "
                    "the cache only covers full-pipeline configs (B/D). "
                    "Run baseline configs (A/C) without cache_dir."
                )
            else:
                train_ds = EyePACSDataset(
                    image_paths=tr_paths,
                    labels=tr_labels,
                    patient_ids=tr_pids,
                    preprocessing=train_preproc,
                    augmentation=None,   # augmentation is inside pipeline
                    eye_sides=tr_sides,
                )
                val_ds = EyePACSDataset(
                    image_paths=va_paths,
                    labels=va_labels,
                    patient_ids=va_pids,
                    preprocessing=val_preproc,
                    augmentation=None,
                    eye_sides=va_sides,
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

            ckpt_mgr = CheckpointManager(ckpt_dir, max_keep=5)
            model = _build_model_with_init(model_name, model_cfg, cfg_key, config)

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
            print(f"  Best → F1={f1:.4f}  AUC={auc:.4f}  κ={kap:.4f}  acc={acc:.4f}")

    # ── Summary + dominance tests ─────────────────────────────────────────────
    if fold is not None:
        print(f"\nSingle-fold run complete (fold {fold}). "
              "Full summary emitted after all folds finish.")
        return

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

        dominance_tests = {"B_vs_A": dom_B_vs_A, "D_vs_C": dom_D_vs_C}
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
        spec = _CONFIGS.get(cfg_key, {})
        print(f"  Config {cfg_key} ({spec.get('preprocessing','?')}"
              f" + {spec.get('model','?')} in_channels={spec.get('in_channels','?')}):")
        for k, v in cfg_summary.items():
            print(f"    {k}: {v}")

    if dominance_tests:
        print("\n  Dominance tests (EH-3):")
        for test_name, result in dominance_tests.items():
            dom = result["overall_dominant"]
            print(f"    {test_name}: Δf1={result['f1_delta_pp']:.1f}pp  "
                  f"Δauc={result['auc_delta']:.4f}  "
                  f"Δκ={result['kappa_delta']:.4f}  "
                  f"dominant={dom}")

    h1_label = "SUPPORTED (EH-4)" if h1_supported else "NOT SUPPORTED"
    print(f"\n  H-1: {h1_label}")
    print(f"\n  Full summary saved to {summary_path}")
