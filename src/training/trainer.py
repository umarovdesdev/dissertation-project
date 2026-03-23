"""Training loop with mixed precision, early stopping, and 5-fold CV."""

import csv
import time
from pathlib import Path
from typing import Callable

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset

from src.evaluation.metrics import (
    compute_primary_metrics,
    compute_secondary_metrics,
    compute_clinical_metrics,
)
from src.training.checkpoint import CheckpointManager
from src.training.losses import compute_class_weights, create_weighted_loss


class Trainer:
    """Full training loop: mixed precision, early stopping, checkpointing.

    Args:
        config: Full config dict (from default.yaml). Reads:
            training.{learning_rate, weight_decay, batch_size, max_epochs,
                       mixed_precision, num_workers,
                       early_stopping.{patience, monitor},
                       scheduler.{type, factor, patience, min_lr},
                       class_weights}
            paths.output_dir
        device: "auto" (default) picks cuda if available, else cpu.
    """

    def __init__(self, config: dict, device: str = "auto") -> None:
        self.config = config
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        tc = config.get("training", {})
        self.lr: float = tc.get("learning_rate", 1e-4)
        self.weight_decay: float = tc.get("weight_decay", 1e-4)
        self.batch_size: int = tc.get("batch_size", 16)
        self.max_epochs: int = tc.get("max_epochs", 100)
        self.mixed_precision: bool = tc.get("mixed_precision", True)
        self.num_workers: int = tc.get("num_workers", 4)
        self.use_class_weights: bool = tc.get("class_weights") == "inverse_frequency"

        es = tc.get("early_stopping", {})
        self.es_patience: int = es.get("patience", 10)
        self.es_monitor: str = es.get("monitor", "val_weighted_f1")

        sched = tc.get("scheduler", {})
        self.sched_factor: float = sched.get("factor", 0.5)
        self.sched_patience: int = sched.get("patience", 5)
        self.sched_min_lr: float = sched.get("min_lr", 1e-6)

        self.output_dir = Path(config.get("paths", {}).get("output_dir", "outputs/"))
        self.num_classes: int = 5

    # ------------------------------------------------------------------
    # Core epoch routines
    # ------------------------------------------------------------------

    def train_one_epoch(
        self,
        model: nn.Module,
        dataloader: DataLoader,
        criterion: nn.Module,
        optimizer: torch.optim.Optimizer,
        scaler: torch.cuda.amp.GradScaler,
    ) -> dict:
        """Run one training epoch with mixed-precision forward+backward.

        Args:
            model: Model to train (moved to self.device before call).
            dataloader: Training DataLoader.
            criterion: Loss function.
            optimizer: Optimiser.
            scaler: GradScaler for AMP (no-op if mixed_precision=False).

        Returns:
            Dict with train_loss (float) and train_accuracy (float).
        """
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for images, labels in dataloader:
            images = images.to(self.device, non_blocking=True)
            labels = labels.to(self.device, non_blocking=True)

            optimizer.zero_grad()

            with torch.amp.autocast("cuda", enabled=self.mixed_precision):
                logits = model(images)
                loss = criterion(logits, labels)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item() * images.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += images.size(0)

        return {
            "train_loss": total_loss / total,
            "train_accuracy": correct / total,
        }

    def evaluate(
        self,
        model: nn.Module,
        dataloader: DataLoader,
        criterion: nn.Module,
    ) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray]:
        """Evaluate model on a dataloader, computing all metrics.

        Args:
            model: Trained model (moved to self.device before call).
            dataloader: Evaluation DataLoader.
            criterion: Loss function (for val_loss tracking).

        Returns:
            Tuple of:
              - metrics_dict: primary + secondary + clinical metrics
              - all_preds: shape (N,) int array
              - all_probs: shape (N, num_classes) float array
              - all_labels: shape (N,) int array
        """
        model.eval()
        total_loss = 0.0
        all_preds, all_probs, all_labels = [], [], []

        with torch.no_grad():
            for images, labels in dataloader:
                images = images.to(self.device, non_blocking=True)
                labels = labels.to(self.device, non_blocking=True)

                logits = model(images)
                loss = criterion(logits.float(), labels)

                total_loss += loss.item() * images.size(0)
                probs = torch.softmax(logits.float(), dim=1)
                preds = logits.argmax(dim=1)

                all_preds.append(preds.cpu().numpy())
                all_probs.append(probs.cpu().float().numpy())
                all_labels.append(labels.cpu().numpy())

        all_preds = np.concatenate(all_preds)
        all_probs = np.concatenate(all_probs)
        all_labels = np.concatenate(all_labels)

        primary = compute_primary_metrics(all_labels, all_preds, all_probs, self.num_classes)
        secondary = compute_secondary_metrics(all_labels, all_preds, self.num_classes)
        clinical = compute_clinical_metrics(all_labels, all_preds)

        metrics = {
            "val_loss": total_loss / len(all_labels),
            **{f"val_{k}": v for k, v in primary.items()},
            **{f"val_{k}": v for k, v in secondary.items()},
            **{f"val_{k}": v for k, v in clinical.items()},
        }
        return metrics, all_preds, all_probs, all_labels

    # ------------------------------------------------------------------
    # Fold-level training
    # ------------------------------------------------------------------

    def train_fold(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        fold: int,
        config_name: str,
        checkpoint_mgr: CheckpointManager,
        metrics_csv_path: Path,
        resume: bool = False,
    ) -> dict:
        """Train one CV fold from start (or resume) to early stopping.

        Args:
            model: Fresh model for this fold (on CPU; moved to device here).
            train_loader: DataLoader for training split.
            val_loader: DataLoader for validation split.
            fold: Fold index (0-based).
            config_name: Config label for metrics.csv (e.g. "B_full_resnet50").
            checkpoint_mgr: CheckpointManager for this fold's checkpoint dir.
            metrics_csv_path: Path to the experiment-level metrics.csv file.
            resume: If True, attempt to load last_checkpoint.pt and continue.

        Returns:
            Best validation primary metrics dict.
        """
        model = model.to(self.device)

        # Class weights from training labels — handle torch.utils.data.Subset
        ds = train_loader.dataset
        if hasattr(ds, "indices"):  # Subset
            train_labels = [ds.dataset.labels[i] for i in ds.indices]
        else:
            train_labels = ds.labels

        if self.use_class_weights:
            weights = compute_class_weights(train_labels, self.num_classes)
        else:
            weights = None
        criterion = create_weighted_loss(weights, device=str(self.device))

        optimizer = torch.optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=self.lr,
            weight_decay=self.weight_decay,
        )
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode="max",
            factor=self.sched_factor,
            patience=self.sched_patience,
            min_lr=self.sched_min_lr,
        )
        scaler = torch.amp.GradScaler("cuda", enabled=self.mixed_precision)

        start_epoch = 0
        best_f1 = -1.0
        no_improve = 0

        # Resume from checkpoint if requested
        if resume:
            try:
                ckpt = checkpoint_mgr.load_latest(model, optimizer, scheduler)
                start_epoch = ckpt["epoch"] + 1
                best_f1 = ckpt["metrics"].get("val_weighted_f1", -1.0)
                print(f"  Resumed fold {fold} from epoch {start_epoch}")
            except FileNotFoundError:
                print(f"  No checkpoint found for fold {fold}, starting fresh.")

        for epoch in range(start_epoch, self.max_epochs):
            t0 = time.time()

            train_metrics = self.train_one_epoch(
                model, train_loader, criterion, optimizer, scaler
            )
            val_metrics, _, _, _ = self.evaluate(model, val_loader, criterion)

            current_f1 = val_metrics.get("val_weighted_f1", 0.0)
            scheduler.step(current_f1)

            # Checkpoint
            all_metrics = {**train_metrics, **val_metrics}
            checkpoint_mgr.save_epoch(
                epoch=epoch,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                metrics=all_metrics,
                fold=fold,
                config=self.config,
            )

            # Write metrics.csv row
            self._append_metrics_csv(
                path=metrics_csv_path,
                epoch=epoch,
                fold=fold,
                config_name=config_name,
                train_loss=train_metrics["train_loss"],
                val_loss=val_metrics["val_loss"],
                val_metrics=val_metrics,
            )

            elapsed = time.time() - t0
            print(
                f"  Fold {fold} | Epoch {epoch:03d} | "
                f"loss {train_metrics['train_loss']:.4f} → {val_metrics['val_loss']:.4f} | "
                f"F1 {current_f1:.4f} | "
                f"AUC {val_metrics.get('val_roc_auc', float('nan')):.4f} | "
                f"κ {val_metrics.get('val_cohen_kappa_quadratic', float('nan')):.4f} | "
                f"{elapsed:.1f}s"
            )

            # Early stopping
            if current_f1 > best_f1:
                best_f1 = current_f1
                no_improve = 0
            else:
                no_improve += 1
                if no_improve >= self.es_patience:
                    print(f"  Early stopping at epoch {epoch} (patience={self.es_patience})")
                    break

        # Return best-checkpoint metrics
        best_ckpt = checkpoint_mgr.load_best(model)
        return best_ckpt["metrics"]

    # ------------------------------------------------------------------
    # Cross-validation orchestration
    # ------------------------------------------------------------------

    def run_cross_validation(
        self,
        create_model_fn: Callable[[], nn.Module],
        dataset,
        splits: list[tuple[list[int], list[int]]],
        config_name: str,
        exp_name: str,
        resume: bool = False,
    ) -> dict:
        """Run full 5-fold cross-validation.

        Args:
            create_model_fn: Zero-argument callable returning a fresh model.
            dataset: Full dataset (BaseFundusDataset subclass).
            splits: List of (train_indices, test_indices) from PatientLevelKFold.
            config_name: Label for this config (e.g. "B_full_resnet50").
            exp_name: Experiment name (e.g. "exp1"); used for output paths.
            resume: Pass through to train_fold for checkpoint resumption.

        Returns:
            Dict with:
              "per_fold": list of best-metrics dicts per fold
              "summary": mean ± std strings for primary metrics
        """
        exp_dir = self.output_dir / exp_name
        metrics_csv = exp_dir / "metrics.csv"

        per_fold_metrics = []

        for fold_idx, (train_idx, val_idx) in enumerate(splits):
            print(f"\n{'='*60}")
            print(f"Fold {fold_idx + 1}/{len(splits)} — {config_name}")
            print(f"{'='*60}")
            print(f"  Train: {len(train_idx)} images | Val: {len(val_idx)} images")

            train_subset = Subset(dataset, train_idx)
            val_subset = Subset(dataset, val_idx)

            train_loader = DataLoader(
                train_subset,
                batch_size=self.batch_size,
                shuffle=True,
                num_workers=self.num_workers,
                pin_memory=(self.device.type == "cuda"),
                drop_last=True,
                persistent_workers=(self.num_workers > 0),
                prefetch_factor=2 if self.num_workers > 0 else None,
            )
            val_loader = DataLoader(
                val_subset,
                batch_size=self.batch_size,
                shuffle=False,
                num_workers=self.num_workers,
                pin_memory=(self.device.type == "cuda"),
                persistent_workers=(self.num_workers > 0),
                prefetch_factor=2 if self.num_workers > 0 else None,
            )

            ckpt_dir = exp_dir / "checkpoints" / f"fold_{fold_idx}"
            ckpt_dir.mkdir(parents=True, exist_ok=True)
            checkpoint_mgr = CheckpointManager(ckpt_dir, max_keep=5)

            model = create_model_fn()
            best_metrics = self.train_fold(
                model=model,
                train_loader=train_loader,
                val_loader=val_loader,
                fold=fold_idx,
                config_name=config_name,
                checkpoint_mgr=checkpoint_mgr,
                metrics_csv_path=metrics_csv,
                resume=resume,
            )
            per_fold_metrics.append(best_metrics)

        # Aggregate summary
        summary = self._aggregate_cv_results(per_fold_metrics)
        print(f"\n{'='*60}")
        print(f"CV Summary — {config_name}")
        for k, v in summary.items():
            print(f"  {k}: {v}")

        return {"per_fold": per_fold_metrics, "summary": summary}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _append_metrics_csv(
        self,
        path: Path,
        epoch: int,
        fold: int,
        config_name: str,
        train_loss: float,
        val_loss: float,
        val_metrics: dict,
    ) -> None:
        """Append one row to the experiment metrics.csv."""
        row = {
            "epoch": epoch,
            "fold": fold,
            "config": config_name,
            "train_loss": f"{train_loss:.6f}",
            "val_loss": f"{val_loss:.6f}",
            "weighted_f1": f"{val_metrics.get('val_weighted_f1', float('nan')):.6f}",
            "roc_auc": f"{val_metrics.get('val_roc_auc', float('nan')):.6f}",
            "kappa": f"{val_metrics.get('val_cohen_kappa_quadratic', float('nan')):.6f}",
            "accuracy": f"{val_metrics.get('val_accuracy', float('nan')):.6f}",
        }
        write_header = not path.exists()
        with open(path, "a", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["epoch", "fold", "config", "train_loss", "val_loss",
                            "weighted_f1", "roc_auc", "kappa", "accuracy"],
            )
            if write_header:
                writer.writeheader()
            writer.writerow(row)

    def _aggregate_cv_results(self, per_fold: list[dict]) -> dict:
        """Compute mean ± std across folds for primary metrics."""
        primary_keys = [
            "val_weighted_f1", "val_roc_auc",
            "val_cohen_kappa_quadratic", "val_accuracy",
        ]
        summary = {}
        for key in primary_keys:
            values = [m[key] for m in per_fold if key in m and not np.isnan(m[key])]
            if values:
                mean = np.mean(values)
                std = np.std(values)
                short_key = key.replace("val_", "")
                summary[short_key] = f"{mean:.4f} ± {std:.4f}"
        return summary
