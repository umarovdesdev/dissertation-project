"""
Evaluation metrics for diabetic retinopathy classification.

Primary metric: Quadratic Weighted Kappa (QWK) — the standard competition
metric for ordinal DR grading tasks (used in Kaggle DR challenges).

Secondary metrics: accuracy, per-class AUC-ROC, macro F1.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    f1_score,
    roc_auc_score,
)


def quadratic_weighted_kappa(y_true: list[int], y_pred: list[int], num_classes: int = 5) -> float:
    """
    Compute Cohen's Kappa with quadratic weighting.

    This is the primary evaluation metric for DR grading — it penalises
    predictions that are far from the true grade more heavily than close ones.

    Args:
        y_true: Ground-truth DR grade labels (0-4).
        y_pred: Predicted DR grade labels (0-4).
        num_classes: Total number of grade classes.

    Returns:
        Quadratic weighted kappa in [-1, 1].  Values ≥ 0.6 are generally
        considered clinically acceptable.
    """
    return cohen_kappa_score(y_true, y_pred, weights="quadratic",
                             labels=list(range(num_classes)))


def multiclass_auc(y_true: list[int], y_prob: list[list[float]]) -> float:
    """
    Macro-averaged One-vs-Rest AUC-ROC for multi-class classification.

    Args:
        y_true: Ground-truth integer labels.
        y_prob: Predicted class probabilities of shape (N, num_classes).

    Returns:
        Macro AUC-ROC score.
    """
    y_prob_arr = np.array(y_prob)
    try:
        return roc_auc_score(y_true, y_prob_arr, multi_class="ovr", average="macro")
    except ValueError:
        # Can happen if a class has no positive samples in the batch
        return float("nan")


def compute_metrics(
    y_true: list[int],
    y_pred: list[int],
    y_prob: list[list[float]] | None = None,
    num_classes: int = 5,
) -> dict[str, float]:
    """
    Compute the full evaluation suite for a DR grading model.

    Args:
        y_true: Ground-truth DR grade labels.
        y_pred: Predicted DR grade labels (argmax of logits).
        y_prob: Predicted class probabilities (optional, required for AUC).
        num_classes: Number of DR grade classes.

    Returns:
        Dictionary mapping metric name to scalar value.
    """
    metrics: dict[str, float] = {}

    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    metrics["quadratic_kappa"] = quadratic_weighted_kappa(y_true, y_pred, num_classes)
    metrics["f1_macro"] = f1_score(y_true, y_pred, average="macro", zero_division=0)

    if y_prob is not None:
        metrics["auc_roc"] = multiclass_auc(y_true, y_prob)

    return metrics


def per_class_accuracy(y_true: list[int], y_pred: list[int], num_classes: int = 5) -> dict[str, float]:
    """
    Per-class sensitivity (recall) for each DR grade.

    Useful for identifying which grades the model struggles with.

    Args:
        y_true: Ground-truth labels.
        y_pred: Predicted labels.
        num_classes: Number of classes.

    Returns:
        Dict mapping "class_N_recall" to recall value.
    """
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)
    result = {}
    for cls in range(num_classes):
        mask = y_true_arr == cls
        if mask.sum() == 0:
            result[f"class_{cls}_recall"] = float("nan")
        else:
            result[f"class_{cls}_recall"] = float((y_pred_arr[mask] == cls).mean())
    return result


def print_metrics(metrics: dict[str, float]) -> None:
    """Pretty-print a metrics dictionary."""
    for name, value in metrics.items():
        print(f"  {name:<25s}: {value:.4f}")
