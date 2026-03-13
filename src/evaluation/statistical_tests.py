"""Statistical tests for DR classification experiments (§6.8).

Mandatory tests per RESEARCH_ARCHITECTURE §6.8:
  - McNemar test (paired classification comparison) — Exp 1
  - DeLong test (ROC-AUC comparison) — Exp 1, 5
  - Bootstrap 95% CI (≥1000 iterations) — all experiments
  - Holm-Bonferroni correction (multiple comparisons) — Exp 1, 2
  - Mixed-effects fold summary (fold as random effect) — Exp 1

Source interpretation rules (INVARIANTS §VII) apply to all statistical
conclusions derived from these tests.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy import stats
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    f1_score,
    roc_auc_score,
)


# ── McNemar test ──────────────────────────────────────────────────────────────

def mcnemar_test(
    y_true: np.ndarray,
    y_pred_a: np.ndarray,
    y_pred_b: np.ndarray,
    alpha: float = 0.05,
) -> dict:
    """McNemar test for paired classification comparison.

    Tests whether two classifiers make statistically different errors on the
    same test set.  Typically used to compare preprocessing vs. baseline
    configurations in Experiment 1.

    Contingency table:
        b = cases where A is correct  AND B is wrong
        c = cases where A is wrong    AND B is correct

    Uses the continuity-corrected McNemar statistic:
        χ² = (|b - c| - 1)² / (b + c)

    If b + c < 25 the exact binomial p-value is returned instead.

    Args:
        y_true:   Ground-truth integer labels, shape (N,).
        y_pred_a: Predictions from model A, shape (N,).
        y_pred_b: Predictions from model B, shape (N,).
        alpha:    Significance level.  Default: 0.05.

    Returns:
        Dict with keys: b (int), c (int), statistic (float),
        p_value (float), significant (bool), test_type (str).
    """
    y_true  = np.asarray(y_true)
    y_pred_a = np.asarray(y_pred_a)
    y_pred_b = np.asarray(y_pred_b)

    correct_a = (y_pred_a == y_true)
    correct_b = (y_pred_b == y_true)

    b = int(( correct_a & ~correct_b).sum())   # A correct, B wrong
    c = int((~correct_a &  correct_b).sum())   # A wrong, B correct

    if (b + c) == 0:
        return {
            "b": b, "c": c,
            "statistic": float("nan"),
            "p_value": 1.0,
            "significant": False,
            "test_type": "mcnemar_no_discordant_pairs",
        }

    if (b + c) < 25:
        # Exact binomial test (two-sided)
        p_value = float(2 * min(
            stats.binom.cdf(min(b, c), b + c, 0.5),
            stats.binom.sf(max(b, c) - 1, b + c, 0.5),
        ))
        statistic = float("nan")
        test_type = "mcnemar_exact_binomial"
    else:
        # Continuity-corrected chi-squared approximation
        statistic = float((abs(b - c) - 1) ** 2 / (b + c))
        p_value   = float(stats.chi2.sf(statistic, df=1))
        test_type = "mcnemar_chi2_continuity_corrected"

    return {
        "b": b,
        "c": c,
        "statistic": statistic,
        "p_value": round(p_value, 6),
        "significant": p_value < alpha,
        "test_type": test_type,
    }


# ── DeLong test ───────────────────────────────────────────────────────────────

def delong_test(
    y_true: np.ndarray,
    y_prob_a: np.ndarray,
    y_prob_b: np.ndarray,
    alpha: float = 0.05,
    referable_threshold: int = 2,
) -> dict:
    """DeLong test for comparing two ROC-AUC values on the same test set.

    Uses the DeLong–DeLong–Clarke-Pearson (1988) variance estimator based on
    placement values (structural components).  When probability arrays are
    multi-class (N × C), the binary referable-DR score is derived as the sum
    of softmax probabilities for classes >= referable_threshold.

    Args:
        y_true:   Ground-truth integer labels, shape (N,).
        y_prob_a: Predicted probabilities for model A.
                  Shape (N,) for binary scores, or (N, C) for multi-class.
        y_prob_b: Predicted probabilities for model B (same shapes as A).
        alpha:    Significance level.  Default: 0.05.
        referable_threshold: Grade >= which DR is considered referable.
                             Used when inputs are multi-class.  Default: 2.

    Returns:
        Dict with keys: auc_a (float), auc_b (float), auc_diff (float),
        z_statistic (float), p_value (float), significant (bool).
    """
    y_true  = np.asarray(y_true,   dtype=np.int64)
    y_prob_a = np.asarray(y_prob_a, dtype=np.float64)
    y_prob_b = np.asarray(y_prob_b, dtype=np.float64)

    # Extract binary score if multi-class
    score_a = _to_binary_score(y_prob_a, referable_threshold)
    score_b = _to_binary_score(y_prob_b, referable_threshold)
    y_bin   = (y_true >= referable_threshold).astype(np.int64)

    try:
        auc_a = float(roc_auc_score(y_bin, score_a))
        auc_b = float(roc_auc_score(y_bin, score_b))
    except ValueError:
        return {
            "auc_a": float("nan"), "auc_b": float("nan"),
            "auc_diff": float("nan"),
            "z_statistic": float("nan"),
            "p_value": 1.0,
            "significant": False,
        }

    var_a, var_b, cov_ab = _delong_variance(y_bin, score_a, score_b)
    var_diff = var_a + var_b - 2 * cov_ab

    if var_diff <= 0:
        return {
            "auc_a": round(auc_a, 6), "auc_b": round(auc_b, 6),
            "auc_diff": round(auc_a - auc_b, 6),
            "z_statistic": float("nan"),
            "p_value": 1.0,
            "significant": False,
        }

    z = (auc_a - auc_b) / np.sqrt(var_diff)
    p = float(2 * stats.norm.sf(abs(z)))

    return {
        "auc_a":        round(auc_a, 6),
        "auc_b":        round(auc_b, 6),
        "auc_diff":     round(auc_a - auc_b, 6),
        "z_statistic":  round(float(z), 4),
        "p_value":      round(p, 6),
        "significant":  p < alpha,
    }


def _to_binary_score(y_prob: np.ndarray, threshold: int) -> np.ndarray:
    """Extract binary referable-DR probability from a 1-D or 2-D array."""
    if y_prob.ndim == 1:
        return y_prob
    # Sum probabilities for classes >= threshold
    return y_prob[:, threshold:].sum(axis=1)


def _placement_values(
    y_bin: np.ndarray,
    scores: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute DeLong structural components V10 and V01.

    V10[i] = Ψ(x_i, Y) = mean_j ψ(x_i, y_j)  for positive samples x_i
    V01[j] = Ψ(X, y_j) = mean_i ψ(x_i, y_j)  for negative samples y_j
    where ψ(x,y) = 1 if x>y, 0.5 if x==y, 0 if x<y.
    """
    pos = scores[y_bin == 1]
    neg = scores[y_bin == 0]

    # V10: for each positive sample, mean kernel vs negatives
    # V01: for each negative sample, mean kernel vs positives
    # Use broadcasting: (n_pos, n_neg) kernel matrix
    # ψ(x_i, y_j): x_i is positive score, y_j is negative score
    diff = pos[:, None] - neg[None, :]        # (n_pos, n_neg)
    psi  = np.where(diff > 0, 1.0, np.where(diff == 0, 0.5, 0.0))

    v10 = psi.mean(axis=1)   # mean over negatives, one value per positive
    v01 = psi.mean(axis=0)   # mean over positives, one value per negative
    return v10, v01


def _delong_variance(
    y_bin: np.ndarray,
    score_a: np.ndarray,
    score_b: np.ndarray,
) -> tuple[float, float, float]:
    """Estimate Var(AUC_a), Var(AUC_b), Cov(AUC_a, AUC_b) via DeLong method."""
    n_pos = int((y_bin == 1).sum())
    n_neg = int((y_bin == 0).sum())

    if n_pos == 0 or n_neg == 0:
        return 0.0, 0.0, 0.0

    v10_a, v01_a = _placement_values(y_bin, score_a)
    v10_b, v01_b = _placement_values(y_bin, score_b)

    var_a  = np.var(v10_a, ddof=1) / n_pos + np.var(v01_a, ddof=1) / n_neg
    var_b  = np.var(v10_b, ddof=1) / n_pos + np.var(v01_b, ddof=1) / n_neg
    cov_ab = (np.cov(v10_a, v10_b)[0, 1] / n_pos
              + np.cov(v01_a, v01_b)[0, 1] / n_neg)

    return float(var_a), float(var_b), float(cov_ab)


# ── Bootstrap confidence intervals ────────────────────────────────────────────

def bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray | None = None,
    metric_fn: Callable | None = None,
    n_iterations: int = 1000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict:
    """Bootstrap confidence interval for a single metric.

    Args:
        y_true:       Ground-truth labels, shape (N,).
        y_pred:       Predicted labels, shape (N,).
        y_prob:       Predicted probabilities, shape (N, C) or None.
        metric_fn:    Callable(y_true, y_pred, y_prob) → float.
                      Defaults to weighted F1-score.
        n_iterations: Number of bootstrap resamples.  Default: 1000.
        confidence:   Confidence level.  Default: 0.95.
        seed:         Random seed for reproducibility.

    Returns:
        Dict with keys: mean (float), ci_lower (float),
        ci_upper (float), std (float).
    """
    if metric_fn is None:
        def metric_fn(yt, yp, ypr):  # type: ignore[misc]
            return float(f1_score(yt, yp, average="weighted", zero_division=0))

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n      = len(y_true)

    rng    = np.random.default_rng(seed)
    scores: list[float] = []

    for _ in range(n_iterations):
        idx    = rng.integers(0, n, size=n)
        yt_    = y_true[idx]
        yp_    = y_pred[idx]
        ypr_   = y_prob[idx] if y_prob is not None else None
        try:
            scores.append(float(metric_fn(yt_, yp_, ypr_)))
        except Exception:
            pass

    if not scores:
        return {"mean": float("nan"), "ci_lower": float("nan"),
                "ci_upper": float("nan"), "std": float("nan")}

    scores_arr = np.array(scores)
    tail = (1.0 - confidence) / 2
    return {
        "mean":     round(float(np.mean(scores_arr)), 6),
        "ci_lower": round(float(np.percentile(scores_arr, 100 * tail)), 6),
        "ci_upper": round(float(np.percentile(scores_arr, 100 * (1 - tail))), 6),
        "std":      round(float(np.std(scores_arr)), 6),
    }


def bootstrap_ci_all_primary(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    n_iterations: int = 1000,
    seed: int = 42,
) -> dict:
    """Compute bootstrap 95% CI for all four primary metrics simultaneously.

    Args:
        y_true:       Ground-truth labels, shape (N,).
        y_pred:       Predicted labels, shape (N,).
        y_prob:       Predicted class probabilities, shape (N, C).
        n_iterations: Bootstrap iterations.  Default: 1000.
        seed:         Random seed.

    Returns:
        Dict mapping metric name to {"mean", "ci_lower", "ci_upper", "std"}.
        Metrics: weighted_f1, roc_auc, cohen_kappa_quadratic, accuracy.
    """
    num_classes = y_prob.shape[1] if y_prob.ndim == 2 else 5
    labels      = list(range(num_classes))

    def _f1(yt, yp, ypr):
        return float(f1_score(yt, yp, average="weighted", labels=labels, zero_division=0))

    def _auc(yt, yp, ypr):
        if ypr is None:
            return float("nan")
        try:
            return float(roc_auc_score(yt, ypr, multi_class="ovr", average="macro"))
        except ValueError:
            return float("nan")

    def _kappa(yt, yp, ypr):
        return float(cohen_kappa_score(yt, yp, weights="quadratic", labels=labels))

    def _acc(yt, yp, ypr):
        return float(accuracy_score(yt, yp))

    return {
        "weighted_f1":            bootstrap_ci(y_true, y_pred, y_prob, _f1,   n_iterations, seed=seed),
        "roc_auc":                bootstrap_ci(y_true, y_pred, y_prob, _auc,  n_iterations, seed=seed + 1),
        "cohen_kappa_quadratic":  bootstrap_ci(y_true, y_pred, y_prob, _kappa, n_iterations, seed=seed + 2),
        "accuracy":               bootstrap_ci(y_true, y_pred, y_prob, _acc,  n_iterations, seed=seed + 3),
    }


# ── Holm-Bonferroni correction ────────────────────────────────────────────────

def holm_bonferroni_correction(
    p_values: list[float],
    alpha: float = 0.05,
) -> list[dict]:
    """Holm-Bonferroni step-down correction for multiple comparisons.

    For m tests with sorted p-values p_(1) ≤ ... ≤ p_(m):
        Reject H_(k) if p_(k) ≤ α / (m - k + 1) AND all p_(j) for j < k
        were also rejected (step-down property).
    The adjusted p-value is: min(1, max_{j≤k}( (m - j + 1) * p_(j) )).

    Args:
        p_values: List of raw p-values from multiple comparisons.
        alpha:    Family-wise error rate.  Default: 0.05.

    Returns:
        List of dicts — one per input p-value — each with:
        {"original_p", "adjusted_p", "significant", "rank"}.
        List is in the ORIGINAL order (not sorted by rank).
    """
    m = len(p_values)
    if m == 0:
        return []

    # Sort by p-value, remember original positions
    order   = sorted(range(m), key=lambda i: p_values[i])
    sorted_p = [p_values[i] for i in order]

    # Compute adjusted p-values (cumulative max of (m-k+1)*p(k))
    adjusted = [0.0] * m
    running_max = 0.0
    for k, orig_idx in enumerate(order):
        adj = (m - k) * sorted_p[k]   # rank is 0-indexed: (m - k) = m - (k+1) + 1
        running_max = max(running_max, adj)
        adjusted[k] = min(1.0, running_max)

    # Map back to original order
    result_by_rank = [
        {
            "rank":        k + 1,
            "original_p":  round(sorted_p[k], 8),
            "adjusted_p":  round(adjusted[k], 8),
            "significant": adjusted[k] < alpha,
        }
        for k in range(m)
    ]

    # Reconstruct in original input order
    rank_of = {orig_idx: k for k, orig_idx in enumerate(order)}
    return [result_by_rank[rank_of[i]] for i in range(m)]


# ── Mixed-effects fold summary ────────────────────────────────────────────────

def compute_mixed_effects_summary(
    fold_metrics: list[dict],
    metric_key: str = "val_weighted_f1",
) -> dict:
    """Summarise cross-fold results treating fold as a random effect.

    This is a simplified approximation of a mixed-effects model: fold is
    treated as a blocking factor, and between-fold and within-fold variance
    are estimated from the fold-level scalar metrics.  For a full mixed-effects
    model (lme4-style) use statsmodels.regression.mixed_linear_model.MixedLM.

    Args:
        fold_metrics: List of per-fold metric dicts (one dict per fold).
                      Each dict must contain metric_key.
        metric_key:   Metric to summarise.  Default: "val_weighted_f1".

    Returns:
        Dict with grand_mean (float), between_fold_std (float),
        within_fold_std (float — NaN when only one value per fold),
        n_folds (int), metric_key (str).
    """
    values = [
        float(m[metric_key])
        for m in fold_metrics
        if metric_key in m and not np.isnan(float(m[metric_key]))
    ]
    if not values:
        return {
            "grand_mean":       float("nan"),
            "between_fold_std": float("nan"),
            "within_fold_std":  float("nan"),
            "n_folds":          0,
            "metric_key":       metric_key,
        }

    grand_mean       = float(np.mean(values))
    between_fold_std = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0

    # Within-fold std not estimable from single-point-per-fold summaries
    return {
        "grand_mean":       round(grand_mean, 6),
        "between_fold_std": round(between_fold_std, 6),
        "within_fold_std":  float("nan"),   # requires epoch-level data per fold
        "n_folds":          len(values),
        "metric_key":       metric_key,
    }
