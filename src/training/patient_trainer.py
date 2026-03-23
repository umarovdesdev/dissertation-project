"""
Patient-level training loop for per-patient blending models.

Handles dict-based batches from :class:`~src.data.datasets.EyePACSPatientPairDataset`
and implements a two-stage training protocol:

Stage 1 — Backbone pre-training as a single-image classifier.
    The backbone (with Identity head) is temporarily wrapped in a thin linear
    head and trained using the standard :class:`~src.training.trainer.Trainer`.
    After Stage 1 the linear head is discarded; the backbone retains its
    fine-tuned weights.

Stage 2 — Patient-pair blending.
    (a) Backbone is frozen.  :class:`~src.models.patient_model.PatientHead`
        is trained for ``head_warmup_epochs`` on patient-pair batches.
    (b) Backbone is unfrozen with a lower LR (1 × 10⁻⁵) while the head
        continues with a higher LR (1 × 10⁻⁴).  Training continues until
        early stopping.
"""

from __future__ import annotations

import csv
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.evaluation.metrics import (
    compute_primary_metrics,
    compute_secondary_metrics,
    compute_clinical_metrics,
)
from src.models.patient_model import DRPatientModel
from src.training.checkpoint import CheckpointManager
from src.training.losses import compute_class_weights, create_weighted_loss
from src.training.trainer import Trainer


# ---------------------------------------------------------------------------
# Temporary single-image wrapper (Stage 1 helper)
# ---------------------------------------------------------------------------

class _SingleImageWrapper(nn.Module):
    """Wraps a :class:`~src.models.patient_model.Backbone` + linear head
    so Stage 1 can reuse the standard single-image :class:`Trainer`.

    Args:
        backbone: Backbone with Identity classifier (as produced by
            :func:`~src.models.factory.create_patient_model`).
        num_classes: Number of output classes.
    """

    def __init__(self, backbone: nn.Module, num_classes: int) -> None:
        super().__init__()
        self.backbone = backbone
        self.head = nn.Linear(backbone.feat_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.backbone(x))

    # Expose labels attribute passthrough for Trainer class-weight extraction
    @property
    def labels(self) -> list[int]:
        return []


# ---------------------------------------------------------------------------
# PatientTrainer
# ---------------------------------------------------------------------------

class PatientTrainer:
    """Training loop for per-patient blending models.

    Parses the same config keys as :class:`~src.training.trainer.Trainer`
    and adds patient-pair epoch routines and the two-stage protocol.

    Args:
        config: Full config dict (from ``default.yaml``).  Reads the same
            ``training.*`` sub-keys as :class:`Trainer`.
        device: ``"auto"`` selects CUDA when available, otherwise CPU.
    """

    # Stage 2 hyper-parameters (can be overridden via config)
    HEAD_WARMUP_EPOCHS: int = 5
    BACKBONE_LR_STAGE2: float = 1e-5
    HEAD_LR_STAGE2: float = 1e-4

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

        sched = tc.get("scheduler", {})
        self.sched_factor: float = sched.get("factor", 0.5)
        self.sched_patience: int = sched.get("patience", 5)
        self.sched_min_lr: float = sched.get("min_lr", 1e-6)

        self.output_dir = Path(config.get("paths", {}).get("output_dir", "outputs/"))
        self.num_classes: int = 5

    # ------------------------------------------------------------------
    # Core epoch routines — patient-pair batches
    # ------------------------------------------------------------------

    def train_one_epoch_patient(
        self,
        model: DRPatientModel,
        dataloader: DataLoader,
        criterion: nn.Module,
        optimizer: torch.optim.Optimizer,
        scaler: torch.cuda.amp.GradScaler,
    ) -> dict:
        """Run one training epoch on patient-pair dict batches.

        Args:
            model: :class:`~src.models.patient_model.DRPatientModel`.
            dataloader: DataLoader yielding dicts with keys
                ``"left"``, ``"right"``, ``"label"``.
            criterion: Loss function.
            optimizer: Optimiser.
            scaler: GradScaler (no-op when mixed_precision=False).

        Returns:
            Dict with ``train_loss`` (float) and ``train_accuracy`` (float).
        """
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for batch in dataloader:
            img_L = batch["left"].to(self.device, non_blocking=True)
            img_R = batch["right"].to(self.device, non_blocking=True)
            labels = batch["label"].to(self.device, non_blocking=True)

            optimizer.zero_grad()

            with torch.amp.autocast("cuda", enabled=self.mixed_precision):
                logits = model(img_L, img_R)
                loss = criterion(logits, labels)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item() * labels.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        n = max(total, 1)
        return {"train_loss": total_loss / n, "train_accuracy": correct / n}

    def evaluate_patient(
        self,
        model: DRPatientModel,
        dataloader: DataLoader,
        criterion: nn.Module,
    ) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray]:
        """Evaluate a patient model on dict-based batches.

        Args:
            model: :class:`~src.models.patient_model.DRPatientModel`.
            dataloader: DataLoader yielding dicts with keys
                ``"left"``, ``"right"``, ``"label"``.
            criterion: Loss function (for ``val_loss`` tracking).

        Returns:
            Tuple of:
              - metrics_dict: primary + secondary + clinical metrics
              - all_preds: shape ``(N,)`` int array
              - all_probs: shape ``(N, num_classes)`` float array
              - all_labels: shape ``(N,)`` int array
        """
        model.eval()
        total_loss = 0.0
        all_preds: list[np.ndarray] = []
        all_probs: list[np.ndarray] = []
        all_labels: list[np.ndarray] = []

        with torch.no_grad():
            for batch in dataloader:
                img_L = batch["left"].to(self.device, non_blocking=True)
                img_R = batch["right"].to(self.device, non_blocking=True)
                labels = batch["label"].to(self.device, non_blocking=True)

                logits = model(img_L, img_R)
                loss = criterion(logits.float(), labels)

                total_loss += loss.item() * labels.size(0)
                probs = torch.softmax(logits.float(), dim=1)
                preds = logits.argmax(dim=1)

                all_preds.append(preds.cpu().numpy())
                all_probs.append(probs.cpu().float().numpy())
                all_labels.append(labels.cpu().numpy())

        preds_arr = np.concatenate(all_preds)
        probs_arr = np.concatenate(all_probs)
        labels_arr = np.concatenate(all_labels)

        primary = compute_primary_metrics(labels_arr, preds_arr, probs_arr, self.num_classes)
        secondary = compute_secondary_metrics(labels_arr, preds_arr, self.num_classes)
        clinical = compute_clinical_metrics(labels_arr, preds_arr)

        metrics = {
            "val_loss": total_loss / max(len(labels_arr), 1),
            **{f"val_{k}": v for k, v in primary.items()},
            **{f"val_{k}": v for k, v in secondary.items()},
            **{f"val_{k}": v for k, v in clinical.items()},
        }
        return metrics, preds_arr, probs_arr, labels_arr

    # ------------------------------------------------------------------
    # Two-stage training protocol
    # ------------------------------------------------------------------

    def train_two_stage(
        self,
        patient_model: DRPatientModel,
        single_image_train_loader: DataLoader,
        single_image_val_loader: DataLoader,
        patient_train_loader: DataLoader,
        patient_val_loader: DataLoader,
        fold: int,
        config_name: str,
        checkpoint_dir: Path,
        metrics_csv_path: Path,
    ) -> dict:
        """Two-stage training: backbone pre-train → patient-pair blending.

        **Stage 1** — Single-image backbone pre-training.
        The backbone is wrapped in :class:`_SingleImageWrapper` (backbone +
        linear head) and trained with the standard :class:`Trainer`.  After
        Stage 1 the linear head is discarded.

        **Stage 2a** — Head-only warm-up.
        The backbone is frozen.  The :class:`~src.models.patient_model.PatientHead`
        is trained for :attr:`HEAD_WARMUP_EPOCHS` epochs on patient-pair batches.

        **Stage 2b** — Joint fine-tuning with differential LR.
        Backbone is unfrozen at ``backbone_lr=1e-5``, head continues at
        ``head_lr=1e-4``.  Training runs until early stopping.

        Args:
            patient_model: :class:`~src.models.patient_model.DRPatientModel`
                (backbone already has Identity head from factory).
            single_image_train_loader: Standard (image, label) DataLoader
                for Stage 1.
            single_image_val_loader: Validation DataLoader for Stage 1.
            patient_train_loader: Dict-batch DataLoader for Stage 2.
            patient_val_loader: Dict-batch validation DataLoader for Stage 2.
            fold: Fold index (0-based) for logging and checkpoint paths.
            config_name: Label for metrics.csv (e.g. ``"patient_resnet50"``).
            checkpoint_dir: Directory for checkpoint files.
            metrics_csv_path: Path to the experiment-level ``metrics.csv``.

        Returns:
            Best Stage-2 validation metrics dict.
        """
        patient_model = patient_model.to(self.device)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # ------------------------------------------------------------------
        # Stage 1: Single-image backbone pre-training
        # ------------------------------------------------------------------
        print(f"\n{'─'*60}")
        print(f"Stage 1 — Backbone pre-training (fold {fold})")
        print(f"{'─'*60}")

        wrapper = _SingleImageWrapper(patient_model.backbone, self.num_classes)
        wrapper = wrapper.to(self.device)

        stage1_ckpt_dir = checkpoint_dir / "stage1"
        stage1_ckpt_dir.mkdir(parents=True, exist_ok=True)
        stage1_ckpt_mgr = CheckpointManager(stage1_ckpt_dir, max_keep=3)

        trainer = Trainer(self.config, device=str(self.device))
        trainer.train_fold(
            model=wrapper,
            train_loader=single_image_train_loader,
            val_loader=single_image_val_loader,
            fold=fold,
            config_name=f"{config_name}_stage1",
            checkpoint_mgr=stage1_ckpt_mgr,
            metrics_csv_path=metrics_csv_path,
        )
        # Stage 1 complete — backbone weights updated in-place via shared ref.
        # Discard the wrapper's linear head.
        del wrapper

        # ------------------------------------------------------------------
        # Stage 2 setup
        # ------------------------------------------------------------------
        if self.use_class_weights:
            # Extract labels from patient_train_loader
            train_labels: list[int] = []
            for batch in patient_train_loader:
                train_labels.extend(batch["label"].tolist())
            weights = compute_class_weights(train_labels, self.num_classes)
        else:
            weights = None
        criterion = create_weighted_loss(weights, device=str(self.device))

        stage2_ckpt_dir = checkpoint_dir / "stage2"
        stage2_ckpt_dir.mkdir(parents=True, exist_ok=True)
        stage2_ckpt_mgr = CheckpointManager(stage2_ckpt_dir, max_keep=5)

        # ------------------------------------------------------------------
        # Stage 2a: Head-only warm-up (backbone frozen)
        # ------------------------------------------------------------------
        print(f"\n{'─'*60}")
        print(f"Stage 2a — Head warm-up, backbone frozen (fold {fold})")
        print(f"{'─'*60}")

        for p in patient_model.backbone.parameters():
            p.requires_grad = False

        head_optimizer = torch.optim.Adam(
            patient_model.head.parameters(),
            lr=self.HEAD_LR_STAGE2,
            weight_decay=self.weight_decay,
        )
        scaler = torch.amp.GradScaler("cuda", enabled=self.mixed_precision)

        for epoch in range(self.HEAD_WARMUP_EPOCHS):
            t0 = time.time()
            train_m = self.train_one_epoch_patient(
                patient_model, patient_train_loader, criterion, head_optimizer, scaler
            )
            val_m, _, _, _ = self.evaluate_patient(
                patient_model, patient_val_loader, criterion
            )
            elapsed = time.time() - t0
            print(
                f"  Warmup epoch {epoch:02d} | "
                f"loss {train_m['train_loss']:.4f} → {val_m['val_loss']:.4f} | "
                f"F1 {val_m.get('val_weighted_f1', float('nan')):.4f} | "
                f"{elapsed:.1f}s"
            )

        # ------------------------------------------------------------------
        # Stage 2b: Joint fine-tuning with differential LR
        # ------------------------------------------------------------------
        print(f"\n{'─'*60}")
        print(f"Stage 2b — Joint fine-tuning, differential LR (fold {fold})")
        print(f"{'─'*60}")

        for p in patient_model.backbone.parameters():
            p.requires_grad = True

        param_groups = [
            {"params": patient_model.backbone.parameters(), "lr": self.BACKBONE_LR_STAGE2},
            {"params": patient_model.head.parameters(),     "lr": self.HEAD_LR_STAGE2},
        ]
        joint_optimizer = torch.optim.Adam(
            param_groups,
            weight_decay=self.weight_decay,
        )
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            joint_optimizer,
            mode="max",
            factor=self.sched_factor,
            patience=self.sched_patience,
            min_lr=self.sched_min_lr,
        )
        scaler = torch.amp.GradScaler("cuda", enabled=self.mixed_precision)

        best_f1 = -1.0
        no_improve = 0
        best_metrics: dict = {}

        for epoch in range(self.max_epochs):
            t0 = time.time()
            train_m = self.train_one_epoch_patient(
                patient_model, patient_train_loader, criterion, joint_optimizer, scaler
            )
            val_m, _, _, _ = self.evaluate_patient(
                patient_model, patient_val_loader, criterion
            )
            current_f1 = val_m.get("val_weighted_f1", 0.0)
            scheduler.step(current_f1)

            all_metrics = {**train_m, **val_m}
            stage2_ckpt_mgr.save_epoch(
                epoch=epoch,
                model=patient_model,
                optimizer=joint_optimizer,
                scheduler=scheduler,
                metrics=all_metrics,
                fold=fold,
                config=self.config,
            )
            self._append_metrics_csv(
                path=metrics_csv_path,
                epoch=epoch,
                fold=fold,
                config_name=f"{config_name}_stage2",
                train_loss=train_m["train_loss"],
                val_loss=val_m["val_loss"],
                val_metrics=val_m,
            )

            elapsed = time.time() - t0
            print(
                f"  Fold {fold} | Epoch {epoch:03d} | "
                f"loss {train_m['train_loss']:.4f} → {val_m['val_loss']:.4f} | "
                f"F1 {current_f1:.4f} | "
                f"AUC {val_m.get('val_roc_auc', float('nan')):.4f} | "
                f"κ {val_m.get('val_cohen_kappa_quadratic', float('nan')):.4f} | "
                f"{elapsed:.1f}s"
            )

            if current_f1 > best_f1:
                best_f1 = current_f1
                best_metrics = val_m
                no_improve = 0
            else:
                no_improve += 1
                if no_improve >= self.es_patience:
                    print(f"  Early stopping at epoch {epoch} (patience={self.es_patience})")
                    break

        best_ckpt = stage2_ckpt_mgr.load_best(patient_model)
        return best_ckpt["metrics"]

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
        """Append one row to the experiment metrics CSV."""
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
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", newline="") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["epoch", "fold", "config", "train_loss", "val_loss",
                            "weighted_f1", "roc_auc", "kappa", "accuracy"],
            )
            if write_header:
                writer.writeheader()
            writer.writerow(row)
