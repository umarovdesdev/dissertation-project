"""Loss functions for DR classification with class imbalance handling."""

from collections import Counter

import torch
import torch.nn as nn
import torch.nn.functional as F


def compute_class_weights(
    labels: list[int],
    num_classes: int = 5,
    method: str = "inverse_frequency",
) -> torch.Tensor:
    """Compute per-class weights to counteract class imbalance.

    Args:
        labels: Integer label list over the training split.
        num_classes: Total number of classes. Default: 5.
        method: Weight method. Only "inverse_frequency" is supported.
            w_c = N / (K * n_c), normalised so weights sum to K.

    Returns:
        Float32 tensor of shape (num_classes,).

    Raises:
        ValueError: If a class has zero samples.
    """
    if method != "inverse_frequency":
        raise ValueError(f"Unsupported weight method: '{method}'")

    counts = Counter(labels)
    n_total = len(labels)
    missing = [c for c in range(num_classes) if counts.get(c, 0) == 0]
    if missing:
        import warnings
        warnings.warn(
            f"compute_class_weights: classes {missing} have zero samples. "
            "Using count=1 as fallback weight — check dataset split.",
            UserWarning,
            stacklevel=2,
        )
    weights = []
    for cls in range(num_classes):
        n_c = counts.get(cls, 0) or 1  # fallback to 1 to avoid division by zero
        weights.append(n_total / (num_classes * n_c))

    w_tensor = torch.tensor(weights, dtype=torch.float32)
    # Normalise so weights sum to num_classes (scale-invariant for the loss)
    w_tensor = w_tensor / w_tensor.sum() * num_classes
    return w_tensor


class FocalLoss(nn.Module):
    """Focal Loss for multi-class classification (Lin et al., 2017).

    Reduces the relative loss for well-classified examples (p_t > 0.5),
    focusing training on hard, misclassified examples.

    FL(p_t) = -α_t · (1 - p_t)^γ · log(p_t)

    Args:
        alpha: Per-class balance weights of shape (num_classes,).
            Typically inverse-frequency weights from compute_class_weights().
            Registered as a buffer (moves with .to(device) automatically).
        gamma: Focusing parameter. γ=0 recovers standard CE.
            γ=2 is the standard value from the original paper.
    """

    def __init__(self, alpha: torch.Tensor, gamma: float = 2.0) -> None:
        super().__init__()
        self.register_buffer("alpha", alpha)
        self.gamma = gamma

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Compute focal loss.

        Args:
            logits: Raw model output of shape (batch_size, num_classes).
            targets: Ground truth class indices of shape (batch_size,).

        Returns:
            Scalar loss tensor (mean over batch).
        """
        ce_loss = F.cross_entropy(logits, targets, reduction="none")
        p_t = torch.exp(-ce_loss)
        alpha_t = self.alpha[targets]
        focal_weight = alpha_t * (1.0 - p_t) ** self.gamma
        return (focal_weight * ce_loss).mean()


def create_loss(
    class_weights: torch.Tensor | None = None,
    device: str = "cpu",
    loss_type: str = "focal",
    gamma: float = 2.0,
) -> nn.Module:
    """Build the training loss function.

    Args:
        class_weights: Tensor of shape (num_classes,) from compute_class_weights(),
                       or None for unweighted loss.
        device: Device string to move weights to (e.g. "cuda" or "cpu").
        loss_type: "focal" (default) for FocalLoss, "ce" for weighted CrossEntropyLoss.
        gamma: Focusing parameter for Focal Loss. Ignored when loss_type="ce".

    Returns:
        Configured loss module (FocalLoss or nn.CrossEntropyLoss).
    """
    if class_weights is not None:
        class_weights = class_weights.to(device)

    if loss_type == "focal":
        if class_weights is None:
            raise ValueError("FocalLoss requires class_weights (alpha). Pass class_weights.")
        return FocalLoss(alpha=class_weights, gamma=gamma)
    elif loss_type == "ce":
        return nn.CrossEntropyLoss(weight=class_weights)
    else:
        raise ValueError(f"Unknown loss_type '{loss_type}'. Use 'focal' or 'ce'.")


# Backward-compatible alias
create_weighted_loss = create_loss
