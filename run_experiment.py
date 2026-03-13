#!/usr/bin/env python3
"""CLI entry point for DR-Classifier experiments.

Usage:
    python run_experiment.py exp1 --config configs/default.yaml
    python run_experiment.py exp1 --resume
    python run_experiment.py exp1 --fold 0
    python run_experiment.py --help
"""

import argparse
import csv
import sys
from pathlib import Path

from src.utils.config import load_config, get_experiment_config
from src.utils.seed import set_seed

METRICS_CSV_HEADER = [
    "epoch", "fold", "config",
    "train_loss", "val_loss",
    "weighted_f1", "roc_auc", "kappa", "accuracy",
]

VALID_EXPERIMENTS = ["exp1", "exp2", "exp3", "exp4", "exp5", "exp6"]


def _create_output_dirs(output_root: Path, exp_name: str, n_folds: int) -> None:
    """Create standard output directory structure for an experiment.

    Args:
        output_root: Base output directory (e.g. outputs/).
        exp_name: Experiment name, e.g. "exp1".
        n_folds: Number of CV folds.
    """
    exp_dir = output_root / exp_name
    for fold in range(n_folds):
        (exp_dir / "checkpoints" / f"fold_{fold}").mkdir(parents=True, exist_ok=True)
    (exp_dir / "logs").mkdir(parents=True, exist_ok=True)

    metrics_path = exp_dir / "metrics.csv"
    if not metrics_path.exists():
        with open(metrics_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(METRICS_CSV_HEADER)


_EXP_MODULES: dict[str, str] = {
    "exp1": "src.experiments.exp1_factorial",
    "exp2": "src.experiments.exp2_ablation",
    "exp3": "src.experiments.exp3_robustness",
    "exp4": "src.experiments.exp4_explainability",
    "exp5": "src.experiments.exp5_generalization",
    "exp6": "src.experiments.exp6_device_shift",
}


def _dispatch(exp_name: str, config: dict, fold: int | None, resume: bool) -> None:
    """Dispatch to the appropriate experiment module.

    Args:
        exp_name: Experiment identifier, e.g. "exp1".
        config: Merged experiment config dict.
        fold: Optional single fold index to run.
        resume: Whether to resume from the last checkpoint.
    """
    import importlib
    module_path = _EXP_MODULES.get(exp_name)
    if module_path is None:
        print(f"Experiment {exp_name} not yet implemented.")
        return
    try:
        mod = importlib.import_module(module_path)
        mod.run(config, fold=fold, resume=resume)
    except ModuleNotFoundError:
        print(f"Experiment {exp_name} not yet implemented.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="run_experiment.py",
        description="DR-Classifier experiment runner",
    )
    parser.add_argument(
        "experiment",
        choices=VALID_EXPERIMENTS,
        help="Experiment to run (exp1–exp6)",
    )
    parser.add_argument(
        "--config",
        default="configs/default.yaml",
        help="Path to YAML config file (default: configs/default.yaml)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume training from last checkpoint",
    )
    parser.add_argument(
        "--fold",
        type=int,
        default=None,
        help="Run a single fold index (0-based) instead of all folds",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    exp_config = get_experiment_config(config, args.experiment)

    set_seed(config.get("seed", 42))

    output_root = Path(config["paths"]["output_dir"])
    n_folds = config["cross_validation"]["n_folds"]
    _create_output_dirs(output_root, args.experiment, n_folds)

    print(f"Running {args.experiment} | config: {args.config} | resume: {args.resume}")
    if args.fold is not None:
        print(f"Single-fold mode: fold {args.fold}")

    _dispatch(args.experiment, exp_config, fold=args.fold, resume=args.resume)


if __name__ == "__main__":
    main()
