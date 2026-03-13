"""Evaluation metrics for DR classification (EH-1, EH-2, EH-3)."""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def compute_primary_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray | None = None,
    num_classes: int = 5,
) -> dict:
    """Compute primary evaluation metrics (EH-1 descending priority order).

    Args:
        y_true: Ground-truth integer labels, shape (N,).
        y_pred: Predicted integer labels, shape (N,).
        y_prob: Predicted class probabilities, shape (N, num_classes).
                Required for roc_auc; if None, roc_auc is set to NaN.
        num_classes: Number of DR grade classes. Default: 5.

    Returns:
        Dict with keys: weighted_f1, roc_auc, cohen_kappa_quadratic, accuracy.
    """
    labels = list(range(num_classes))
    metrics: dict = {}

    metrics["weighted_f1"] = float(
        f1_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)
    )

    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(
                roc_auc_score(y_true, y_prob, multi_class="ovr", average="macro")
            )
        except ValueError:
            metrics["roc_auc"] = float("nan")
    else:
        metrics["roc_auc"] = float("nan")

    metrics["cohen_kappa_quadratic"] = float(
        cohen_kappa_score(y_true, y_pred, weights="quadratic", labels=labels)
    )

    metrics["accuracy"] = float(accuracy_score(y_true, y_pred))

    return metrics


def compute_secondary_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    num_classes: int = 5,
) -> dict:
    """Compute secondary / supplementary metrics (EH-2).

    Args:
        y_true: Ground-truth integer labels, shape (N,).
        y_pred: Predicted integer labels, shape (N,).
        num_classes: Number of DR grade classes. Default: 5.

    Returns:
        Dict with per-class F1/precision/recall, macro_f1, confusion_matrix.
    """
    labels = list(range(num_classes))
    metrics: dict = {}

    metrics["per_class_f1"] = f1_score(
        y_true, y_pred, average=None, labels=labels, zero_division=0
    ).tolist()
    metrics["per_class_precision"] = precision_score(
        y_true, y_pred, average=None, labels=labels, zero_division=0
    ).tolist()
    metrics["per_class_recall"] = recall_score(
        y_true, y_pred, average=None, labels=labels, zero_division=0
    ).tolist()
    metrics["macro_f1"] = float(
        f1_score(y_true, y_pred, average="macro", labels=labels, zero_division=0)
    )
    metrics["confusion_matrix"] = confusion_matrix(
        y_true, y_pred, labels=labels
    ).tolist()

    return metrics


def compute_clinical_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    referable_threshold: int = 2,
) -> dict:
    """Compute binary clinical screening metrics for referable DR (EH-2).

    Binarises labels: 0 = non-referable (grade < threshold),
    1 = referable (grade >= threshold).

    Args:
        y_true: Ground-truth integer labels, shape (N,).
        y_pred: Predicted integer labels, shape (N,).
        referable_threshold: Grade at which DR becomes referable. Default: 2.

    Returns:
        Dict with sensitivity, specificity, ppv, npv.
    """
    y_true_bin = (np.asarray(y_true) >= referable_threshold).astype(int)
    y_pred_bin = (np.asarray(y_pred) >= referable_threshold).astype(int)

    tp = int(((y_pred_bin == 1) & (y_true_bin == 1)).sum())
    tn = int(((y_pred_bin == 0) & (y_true_bin == 0)).sum())
    fp = int(((y_pred_bin == 1) & (y_true_bin == 0)).sum())
    fn = int(((y_pred_bin == 0) & (y_true_bin == 1)).sum())

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0

    return {
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "ppv": float(ppv),
        "npv": float(npv),
    }


def check_dominance(
    metrics_preproc: dict,
    metrics_baseline: dict,
) -> dict:
    """Check EH-3 Empirical Dominance Criterion.

    A preprocessing condition is dominant iff ALL THREE hold:
      - Δ weighted_f1 >= 0.05 (5 percentage points)
      - Δ roc_auc >= 0.02
      - Δ cohen_kappa_quadratic >= 0 (no degradation)

    Args:
        metrics_preproc: Primary metrics dict for the preprocessed config.
        metrics_baseline: Primary metrics dict for the baseline config.

    Returns:
        Dict with f1_delta_pp, auc_delta, kappa_delta, overall_dominant.
    """
    f1_delta = metrics_preproc["weighted_f1"] - metrics_baseline["weighted_f1"]
    auc_delta = metrics_preproc["roc_auc"] - metrics_baseline["roc_auc"]
    kappa_delta = (
        metrics_preproc["cohen_kappa_quadratic"]
        - metrics_baseline["cohen_kappa_quadratic"]
    )

    f1_ok = f1_delta >= 0.05
    auc_ok = auc_delta >= 0.02
    kappa_ok = kappa_delta >= 0.0

    return {
        "f1_delta_pp": round(f1_delta * 100, 2),
        "auc_delta": round(auc_delta, 4),
        "kappa_delta": round(kappa_delta, 4),
        "f1_criterion_met": f1_ok,
        "auc_criterion_met": auc_ok,
        "kappa_criterion_met": kappa_ok,
        "overall_dominant": f1_ok and auc_ok and kappa_ok,
    }


def check_overfitting(
    train_metrics: dict,
    test_metrics: dict,
    threshold_pp: float = 15.0,
) -> dict:
    """Detect overfitting per OD-4 (gap > 15 pp on any primary metric).

    Args:
        train_metrics: Primary metrics on the training partition.
        test_metrics: Primary metrics on the held-out test partition.
        threshold_pp: Overfitting threshold in percentage points. Default: 15.

    Returns:
        Dict with per-metric gap_pp and is_overfitting bool.
    """
    result: dict = {}
    threshold = threshold_pp / 100.0

    for metric in ("weighted_f1", "accuracy"):
        train_val = train_metrics.get(metric, float("nan"))
        test_val = test_metrics.get(metric, float("nan"))
        gap = train_val - test_val
        result[f"{metric}_gap_pp"] = round(gap * 100, 2)
        result[f"{metric}_is_overfitting"] = gap > threshold

    result["overall_is_overfitting"] = any(
        result[k] for k in result if k.endswith("_is_overfitting")
    )
    return result
