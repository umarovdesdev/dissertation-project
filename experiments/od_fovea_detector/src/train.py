"""Training loop for the OD/fovea heatmap detector.

Deterministic (seed=42), trains on the IDRiD 413-image TRAIN split only, with a
held-out slice of TRAIN (``data.val_fraction``) for early stopping and later
threshold calibration. The 103-image TEST split is never used here.

Loss type (DSNT vs heatmap baseline) is selected by config. Aggressive
augmentation is applied to the training slice only; the validation slice uses
the augmentation-off pass (brief §4).

Usage::

    python -m src.train --config configs/default.yaml
    python -m src.train --config configs/default.yaml --epochs 2   # quick run

Requires torch + timm + the IDRiD dataset.
"""

from __future__ import annotations

import argparse
import pathlib
import random

import numpy as np
import torch
from torch.utils.data import DataLoader

from .data import IDRiDLocalizationDataset, load_split
from .losses import build_loss
from .model import build_model
from .utils import load_config, resolve_device


def set_seed(seed: int) -> None:
    """Set all RNG seeds and enable deterministic mode.

    Args:
        seed: Random seed.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def _split_train_val(samples: list, val_fraction: float, seed: int):
    """Deterministically split TRAIN samples into train/val slices.

    Args:
        samples: All TRAIN samples.
        val_fraction: Fraction held out for validation.
        seed: Seed for the shuffle.

    Returns:
        ``(train_samples, val_samples)``.
    """
    rng = np.random.default_rng(seed)
    idx = np.arange(len(samples))
    rng.shuffle(idx)
    n_val = max(1, int(round(len(samples) * val_fraction)))
    val_idx = set(idx[:n_val].tolist())
    train = [s for i, s in enumerate(samples) if i not in val_idx]
    val = [s for i, s in enumerate(samples) if i in val_idx]
    return train, val


def _loss_target(loss_type: str, heatmaps, coords_norm):
    """Pick the right supervision target for the configured loss."""
    return coords_norm if loss_type == "dsnt" else heatmaps


def train(config_path: pathlib.Path, epochs_override: int | None = None) -> None:
    """Run training per the config.

    Args:
        config_path: Path to the YAML config.
        epochs_override: Optional override for ``train.epochs`` (quick runs).
    """
    cfg = load_config(config_path)
    set_seed(cfg["seed"])
    device = resolve_device(cfg["io"]["device"])

    root = pathlib.Path(cfg["data"]["idrid_root"])
    if not root.exists():
        raise FileNotFoundError(
            f"IDRiD localization root not found: {root}. Set data.idrid_root.")

    samples = load_split(root, "train")  # 413 only
    tr_samples, va_samples = _split_train_val(
        samples, cfg["data"]["val_fraction"], cfg["seed"])

    input_size = cfg["data"]["input_size"]
    heatmap_size = cfg["data"]["heatmap_size"]
    sigma = cfg["data"]["sigma_frac"] * heatmap_size

    tr_ds = IDRiDLocalizationDataset(
        tr_samples, input_size, heatmap_size, sigma,
        augment_cfg=cfg["train"]["augmentation"], seed=cfg["seed"])
    va_ds = IDRiDLocalizationDataset(
        va_samples, input_size, heatmap_size, sigma,
        augment_cfg=None, seed=cfg["seed"])  # augmentation-off val pass

    tr_loader = DataLoader(tr_ds, batch_size=cfg["train"]["batch_size"],
                           shuffle=True, num_workers=cfg["train"]["num_workers"],
                           drop_last=False)
    va_loader = DataLoader(va_ds, batch_size=cfg["train"]["batch_size"],
                           shuffle=False, num_workers=cfg["train"]["num_workers"])

    model = build_model(cfg["model"], heatmap_size).to(device)
    sigma_norm = 2.0 * sigma / heatmap_size  # heatmap px -> normalized units
    criterion = build_loss(cfg["loss"], sigma_norm)
    loss_type = cfg["loss"].get("type", "dsnt")

    opt = torch.optim.Adam(model.parameters(), lr=cfg["train"]["lr"],
                           weight_decay=cfg["train"]["weight_decay"])
    epochs = epochs_override or cfg["train"]["epochs"]
    patience = cfg["train"]["early_stopping_patience"]

    weights_path = pathlib.Path(cfg["io"]["weights_path"])
    weights_path.parent.mkdir(parents=True, exist_ok=True)

    best_val = float("inf")
    bad_epochs = 0
    for epoch in range(epochs):
        model.train()
        tr_loss = 0.0
        for img, heatmaps, coords in tr_loader:
            img = img.to(device)
            target = _loss_target(loss_type, heatmaps, coords).to(device)
            out = model(img)
            loss, _ = criterion(out, target)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tr_loss += float(loss.detach()) * img.size(0)
        tr_loss /= max(len(tr_ds), 1)

        model.eval()
        va_loss = 0.0
        with torch.no_grad():
            for img, heatmaps, coords in va_loader:
                img = img.to(device)
                target = _loss_target(loss_type, heatmaps, coords).to(device)
                out = model(img)
                loss, _ = criterion(out, target)
                va_loss += float(loss.detach()) * img.size(0)
        va_loss /= max(len(va_ds), 1)
        print(f"epoch {epoch + 1}/{epochs}  train {tr_loss:.4f}  val {va_loss:.4f}",
              flush=True)

        if va_loss < best_val - 1e-6:
            best_val = va_loss
            bad_epochs = 0
            torch.save({
                "state_dict": model.state_dict(),
                "config": cfg,
                "epoch": epoch,
                "val_loss": best_val,
            }, weights_path)
        else:
            bad_epochs += 1
            if bad_epochs >= patience:
                print(f"early stopping at epoch {epoch + 1}", flush=True)
                break
    print(f"best val loss {best_val:.4f}; weights -> {weights_path}", flush=True)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train the OD/fovea heatmap detector.")
    p.add_argument("--config", type=pathlib.Path,
                   default=pathlib.Path("configs/default.yaml"))
    p.add_argument("--epochs", type=int, default=None,
                   help="Override train.epochs (e.g. for a quick run).")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    train(args.config, args.epochs)


if __name__ == "__main__":
    main()
