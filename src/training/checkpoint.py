"""Checkpoint management for training runs."""

from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler


class CheckpointManager:
    """Manages saving and loading of training checkpoints.

    Maintains:
    - Per-epoch checkpoint files (capped at max_keep latest)
    - last_checkpoint.pt — always updated each epoch
    - best_model.pt — updated when weighted_f1 improves

    Args:
        checkpoint_dir: Directory to store checkpoint files.
        max_keep: Maximum number of epoch checkpoint files to retain.
    """

    def __init__(self, checkpoint_dir: Path, max_keep: int = 5) -> None:
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.max_keep = max_keep
        self._best_f1: float = -1.0
        self._saved_epochs: list[Path] = []

    def save_epoch(
        self,
        epoch: int,
        model: nn.Module,
        optimizer: Optimizer,
        scheduler: Any,
        metrics: dict[str, float],
        fold: int,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Save a checkpoint for the given epoch.

        Saves epoch_{EE:02d}.pt, updates last_checkpoint.pt, and
        updates best_model.pt if metrics["weighted_f1"] is a new best.
        Removes oldest epoch files beyond max_keep.

        Args:
            epoch: Current epoch number (0-indexed).
            model: The model whose state_dict will be saved.
            optimizer: Optimizer whose state_dict will be saved.
            scheduler: LR scheduler whose state_dict will be saved.
            metrics: Dict containing at minimum "weighted_f1".
            fold: Current fold index.
            config: Optional config dict to embed in checkpoint.
        """
        checkpoint: dict[str, Any] = {
            "epoch": epoch,
            "fold": fold,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict() if scheduler is not None else None,
            "metrics": metrics,
            "config": config,
        }

        epoch_path = self.checkpoint_dir / f"epoch_{epoch:02d}.pt"
        torch.save(checkpoint, epoch_path)
        self._saved_epochs.append(epoch_path)

        # Keep only the last max_keep epoch files
        while len(self._saved_epochs) > self.max_keep:
            old = self._saved_epochs.pop(0)
            if old.exists():
                old.unlink()

        # Always update last checkpoint
        torch.save(checkpoint, self.checkpoint_dir / "last_checkpoint.pt")

        # Update best model if improved
        # Accept both "val_weighted_f1" (trainer output) and "weighted_f1" (raw)
        current_f1 = metrics.get("val_weighted_f1", metrics.get("weighted_f1", -1.0))
        if current_f1 > self._best_f1:
            self._best_f1 = current_f1
            torch.save(checkpoint, self.checkpoint_dir / "best_model.pt")

    def load_latest(
        self,
        model: nn.Module,
        optimizer: Optimizer,
        scheduler: Any,
    ) -> dict[str, Any]:
        """Load last_checkpoint.pt and restore model/optimizer/scheduler state.

        Args:
            model: Model to restore state into.
            optimizer: Optimizer to restore state into.
            scheduler: LR scheduler to restore state into.

        Returns:
            Full checkpoint dict including epoch, fold, metrics, config.

        Raises:
            FileNotFoundError: If last_checkpoint.pt does not exist.
        """
        path = self.checkpoint_dir / "last_checkpoint.pt"
        if not path.exists():
            raise FileNotFoundError(f"No checkpoint found at {path}")
        checkpoint = torch.load(path, map_location="cpu")
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        if scheduler is not None and checkpoint.get("scheduler_state_dict") is not None:
            scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        return checkpoint

    def load_best(self, model: nn.Module) -> dict[str, Any]:
        """Load best_model.pt for inference.

        Args:
            model: Model to restore state into.

        Returns:
            Full checkpoint dict including epoch, fold, metrics, config.

        Raises:
            FileNotFoundError: If best_model.pt does not exist.
        """
        path = self.checkpoint_dir / "best_model.pt"
        if not path.exists():
            raise FileNotFoundError(f"No best model checkpoint found at {path}")
        checkpoint = torch.load(path, map_location="cpu")
        model.load_state_dict(checkpoint["model_state_dict"])
        return checkpoint
