"""Loss functions for DR classification with class imbalance handling."""

from collections import Counter

import torch
import torch.nn as nn


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
    weights = []
    for cls in range(num_classes):
        n_c = counts.get(cls, 0)
        if n_c == 0:
            raise ValueError(
                f"Class {cls} has zero samples — cannot compute inverse-frequency weight."
            )
        weights.append(n_total / (num_classes * n_c))

    w_tensor = torch.tensor(weights, dtype=torch.float32)
    # Normalise so weights sum to num_classes (scale-invariant for the loss)
    w_tensor = w_tensor / w_tensor.sum() * num_classes
    return w_tensor


def create_weighted_loss(
    class_weights: torch.Tensor | None = None,
    device: str = "cpu",
) -> nn.CrossEntropyLoss:
    """Build a CrossEntropyLoss with optional class weights.

    Args:
        class_weights: Tensor of shape (num_classes,) from compute_class_weights,
                       or None for unweighted loss.
        device: Device string to move weights to (e.g. "cuda" or "cpu").

    Returns:
        Configured nn.CrossEntropyLoss instance.
    """
    if class_weights is not None:
        class_weights = class_weights.to(device)
    return nn.CrossEntropyLoss(weight=class_weights)
