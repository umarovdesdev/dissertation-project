"""Calibration metrics: ECE and Brier score (EH-2, SB-1.10)."""

import numpy as np


def compute_ece(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 15,
) -> float:
    """Compute Expected Calibration Error (ECE).

    Bins predictions by maximum predicted confidence, then computes
    the weighted average absolute gap between bin accuracy and bin confidence.

    Args:
        y_true: Ground-truth integer labels, shape (N,).
        y_prob: Predicted class probabilities, shape (N, num_classes).
        n_bins: Number of equal-width confidence bins. Default: 15.

    Returns:
        ECE scalar in [0, 1].
    """
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    confidences = y_prob.max(axis=1)
    predictions = y_prob.argmax(axis=1)
    accuracies = (predictions == y_true).astype(float)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_true)

    for lo, hi in zip(bin_edges[:-1], bin_edges[1:]):
        mask = (confidences > lo) & (confidences <= hi)
        if mask.sum() == 0:
            continue
        bin_acc = accuracies[mask].mean()
        bin_conf = confidences[mask].mean()
        ece += (mask.sum() / n) * abs(bin_acc - bin_conf)

    return float(ece)


def compute_brier_score(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    num_classes: int = 5,
) -> float:
    """Compute multiclass Brier score.

    One-hot encodes y_true, then computes the mean squared error between
    one-hot targets and predicted probabilities across all classes.

    Args:
        y_true: Ground-truth integer labels, shape (N,).
        y_prob: Predicted class probabilities, shape (N, num_classes).
        num_classes: Number of classes. Default: 5.

    Returns:
        Brier score in [0, 2]. Lower is better; 0 = perfect calibration.
    """
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    n = len(y_true)

    one_hot = np.zeros((n, num_classes), dtype=np.float32)
    one_hot[np.arange(n), y_true] = 1.0

    return float(np.mean((y_prob - one_hot) ** 2))
