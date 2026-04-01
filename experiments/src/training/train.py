"""
Training script for the DR classifier.

Usage:
    python src/training/train.py --config configs/training_config.yaml
    python src/training/train.py --config configs/training_config.yaml --resume experiments/checkpoints/last.pt
"""

import argparse
import sys
from pathlib import Path

import torch
import torch.nn as nn
import yaml
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from tqdm import tqdm

# Add project root to path so src imports resolve when run as a script
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.resnet50_model import build_model
from src.evaluation.metrics import compute_metrics


# ---------------------------------------------------------------------------
# Dataset placeholder
# ---------------------------------------------------------------------------

class FundusDataset(Dataset):
    """
    Loads preprocessed fundus images and their DR grade labels.

    Expects a CSV file in data/splits/ with columns: image_path, label.
    Replace this placeholder with your actual dataset implementation.
    """

    def __init__(self, split_csv: Path, transform=None) -> None:
        import pandas as pd
        self.df = pd.read_csv(split_csv)
        self.transform = transform

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        from PIL import Image
        row = self.df.iloc[idx]
        image = Image.open(row["image_path"]).convert("RGB")
        label = int(row["label"])
        if self.transform:
            image = self.transform(image)
        return image, label


# ---------------------------------------------------------------------------
# Transforms
# ---------------------------------------------------------------------------

def get_transforms(config: dict, split: str) -> transforms.Compose:
    """Return torchvision transforms for train or val/test splits."""
    aug = config["data"].get("augmentation", {})
    size = config["data"]["image_size"]

    mean = [0.485, 0.456, 0.406]  # ImageNet statistics
    std  = [0.229, 0.224, 0.225]

    if split == "train":
        ops = [transforms.RandomHorizontalFlip()] if aug.get("horizontal_flip") else []
        if aug.get("vertical_flip"):
            ops.append(transforms.RandomVerticalFlip())
        if deg := aug.get("rotation_degrees"):
            ops.append(transforms.RandomRotation(deg))
        if aug.get("color_jitter"):
            ops.append(transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1))
        ops += [transforms.Resize((size, size)), transforms.ToTensor(), transforms.Normalize(mean, std)]
        return transforms.Compose(ops)

    return transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])


# ---------------------------------------------------------------------------
# Loss
# ---------------------------------------------------------------------------

def build_loss(config: dict) -> nn.Module:
    """Instantiate the loss function specified in config."""
    loss_cfg = config.get("loss", {})
    loss_type = loss_cfg.get("type", "cross_entropy")

    if loss_type == "label_smoothing":
        return nn.CrossEntropyLoss(label_smoothing=loss_cfg.get("label_smoothing", 0.1))
    # TODO: add focal loss support
    return nn.CrossEntropyLoss()


# ---------------------------------------------------------------------------
# Optimiser & scheduler
# ---------------------------------------------------------------------------

def build_optimizer(model: nn.Module, config: dict) -> torch.optim.Optimizer:
    lr = config["training"]["learning_rate"]
    wd = config["training"]["weight_decay"]
    opt_name = config["training"].get("optimizer", "adam").lower()

    if opt_name == "sgd":
        return torch.optim.SGD(model.parameters(), lr=lr, weight_decay=wd, momentum=0.9)
    return torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)


def build_scheduler(optimizer: torch.optim.Optimizer, config: dict):
    scheduler_name = config["training"].get("scheduler", "cosine").lower()
    epochs = config["training"]["epochs"]

    if scheduler_name == "step":
        return torch.optim.lr_scheduler.StepLR(
            optimizer,
            step_size=config["training"].get("step_size", 10),
            gamma=config["training"].get("gamma", 0.1),
        )
    if scheduler_name == "cosine":
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    return None


# ---------------------------------------------------------------------------
# One epoch helpers
# ---------------------------------------------------------------------------

def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    scaler: GradScaler,
    config: dict,
    epoch: int,
) -> float:
    model.train()
    total_loss = 0.0
    log_interval = config["logging"].get("log_interval", 10)

    for batch_idx, (images, labels) in enumerate(tqdm(loader, desc=f"Train epoch {epoch}")):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()

        with autocast(enabled=config["training"].get("mixed_precision", True)):
            logits = model(images)
            loss = criterion(logits, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()

        if (batch_idx + 1) % log_interval == 0:
            avg = total_loss / (batch_idx + 1)
            tqdm.write(f"  batch {batch_idx + 1}/{len(loader)}  loss={avg:.4f}")

    return total_loss / len(loader)


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, dict]:
    model.eval()
    total_loss = 0.0
    all_preds, all_labels, all_probs = [], [], []

    for images, labels in tqdm(loader, desc="Validating"):
        images, labels = images.to(device), labels.to(device)
        logits = model(images)
        loss = criterion(logits, labels)

        probs = torch.softmax(logits, dim=1)
        preds = logits.argmax(dim=1)

        total_loss += loss.item()
        all_preds.extend(preds.cpu().tolist())
        all_labels.extend(labels.cpu().tolist())
        all_probs.extend(probs.cpu().tolist())

    metrics = compute_metrics(all_labels, all_preds, all_probs)
    return total_loss / len(loader), metrics


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def save_checkpoint(path: Path, model, optimizer, epoch: int, metrics: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "metrics": metrics,
    }, path)


def load_checkpoint(path: Path, model, optimizer=None):
    checkpoint = torch.load(path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state_dict"])
    if optimizer and "optimizer_state_dict" in checkpoint:
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    return checkpoint.get("epoch", 0), checkpoint.get("metrics", {})


# ---------------------------------------------------------------------------
# Main training loop
# ---------------------------------------------------------------------------

def train(config: dict, resume_path: Path | None = None) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data
    splits_dir = Path(config["data"]["splits_dir"])
    train_ds = FundusDataset(splits_dir / "train.csv", transform=get_transforms(config, "train"))
    val_ds   = FundusDataset(splits_dir / "val.csv",   transform=get_transforms(config, "val"))

    train_loader = DataLoader(train_ds, batch_size=config["training"]["batch_size"],
                              shuffle=True,  num_workers=config["data"]["num_workers"], pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=config["training"]["batch_size"],
                              shuffle=False, num_workers=config["data"]["num_workers"], pin_memory=True)

    # Model / loss / optimiser
    model     = build_model(config["model"]).to(device)
    criterion = build_loss(config)
    optimizer = build_optimizer(model, config)
    scheduler = build_scheduler(optimizer, config)
    scaler    = GradScaler(enabled=config["training"].get("mixed_precision", True))

    start_epoch = 0
    best_kappa  = -1.0
    patience    = config["training"].get("early_stopping_patience", 10)
    no_improve  = 0

    ckpt_dir  = Path(config["logging"]["checkpoint_dir"])
    best_path = ckpt_dir / "best.pt"
    last_path = ckpt_dir / "last.pt"

    if resume_path:
        start_epoch, _ = load_checkpoint(resume_path, model, optimizer)
        print(f"Resumed from epoch {start_epoch}")

    for epoch in range(start_epoch + 1, config["training"]["epochs"] + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device, scaler, config, epoch)
        val_loss, metrics = evaluate(model, val_loader, criterion, device)

        kappa = metrics.get("quadratic_kappa", 0.0)
        print(f"Epoch {epoch:3d}  train_loss={train_loss:.4f}  val_loss={val_loss:.4f}  kappa={kappa:.4f}  acc={metrics.get('accuracy', 0):.4f}")

        if scheduler:
            scheduler.step()

        save_checkpoint(last_path, model, optimizer, epoch, metrics)

        if kappa > best_kappa:
            best_kappa = kappa
            no_improve = 0
            save_checkpoint(best_path, model, optimizer, epoch, metrics)
            print(f"  -> New best kappa={best_kappa:.4f}, checkpoint saved.")
        else:
            no_improve += 1
            if no_improve >= patience:
                print(f"Early stopping triggered after {patience} epochs without improvement.")
                break

    print(f"Training complete. Best kappa: {best_kappa:.4f}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train DR classifier")
    parser.add_argument("--config", type=Path, default="configs/training_config.yaml")
    parser.add_argument("--resume", type=Path, default=None, help="Path to checkpoint to resume from")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    with open(args.config) as f:
        config = yaml.safe_load(f)
    train(config, resume_path=args.resume)
