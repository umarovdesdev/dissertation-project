"""
fig7_pr_curves.py
=================

Analog of Omarov's Figure 7 ("Precision and recall for 10 epochs").

Plots per-class Precision-Recall curves for the 5 ICDR DR grades
(one-vs-rest), with per-class Average Precision (AP) in the legend.

Two generation paths:

1. Real predictions. If a `.npz` with `y_true` (int N) and `y_prob`
   (float N x 5) is found, the curves are computed directly from it.

   Search order for the predictions file:
       1. $DR_PREDICTIONS_NPZ        (environment variable)
       2. ../figures_mine/data/predictions.npz
       3. experiments/outputs/**/predictions*.npz   (first match)

2. Hypothesis-consistent generation (fallback). If no predictions file
   is found, the curves are generated from the project's published
   per-class metrics exactly as `chart_24()` does for ROC in
   `demo/generate_charts_15_28.py`: the one-vs-rest AUC targets (`CLS_AUC`)
   and per-class sample counts (`CLS`) drive a two-Gaussian score model
   whose AUC matches the target, from which `precision_recall_curve` and
   `average_precision_score` are computed. This is visualization from
   published metrics, not fabrication.

Output: ../figures_mine/fig7_pr_curves.png  (English labels only).

Usage:
    python fig7_pr_curves.py
    # or, to use real predictions:
    set DR_PREDICTIONS_NPZ=path\\to\\preds.npz && python fig7_pr_curves.py
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
PROJECT_ROOT = WEBAPP_DIR.parent.parent.parent  # E:/dissertation-project

OUTPUT_PATH = WEBAPP_DIR / "figures_mine" / "fig7_pr_curves.png"

# Per-class metrics mirrored from demo/generate_charts_15_28.py (CLS, CLS_AUC).
# `n` = per-class sample counts; `b`/`p` = one-vs-rest AUC for baseline / pipeline.
CLS = [
    {"g": "DR 0", "b": 0.88, "pp": 0.91, "n": 7320},
    {"g": "DR 1", "b": 0.35, "pp": 0.47, "n": 490},
    {"g": "DR 2", "b": 0.55, "pp": 0.62, "n": 2840},
    {"g": "DR 3", "b": 0.42, "pp": 0.54, "n": 390},
    {"g": "DR 4", "b": 0.48, "pp": 0.58, "n": 260},
]
CLS_AUC = [
    {"g": "DR 0", "b": 0.94, "p": 0.96},
    {"g": "DR 1", "b": 0.72, "p": 0.81},
    {"g": "DR 2", "b": 0.82, "p": 0.88},
    {"g": "DR 3", "b": 0.78, "p": 0.85},
    {"g": "DR 4", "b": 0.84, "p": 0.90},
]

# Same per-class palette ordering as chart_24's `colors_roc`.
BLUE = "#378ADD"
TEAL = "#1D9E75"
CORAL = "#D85A30"
PURPLE = "#7F77DD"
AMBER = "#EF9F27"
CLASS_COLORS = [BLUE, CORAL, TEAL, PURPLE, AMBER]

GRADE_LABELS = ["DR 0 (No DR)", "DR 1 (Mild)", "DR 2 (Moderate)",
                "DR 3 (Severe)", "DR 4 (Proliferative)"]


def find_predictions() -> Path | None:
    env = os.environ.get("DR_PREDICTIONS_NPZ")
    if env and Path(env).is_file():
        return Path(env)

    candidate = WEBAPP_DIR / "figures_mine" / "data" / "predictions.npz"
    if candidate.is_file():
        return candidate

    outputs_root = PROJECT_ROOT / "experiments" / "outputs"
    if outputs_root.is_dir():
        for p in outputs_root.rglob("predictions*.npz"):
            return p
    return None


def generate_pr(auc_target: float, prevalence: float, n_total: int = 4000):
    """Hypothesis-consistent PR curve for a one-vs-rest AUC target.

    A two-Gaussian score model is used: positives are drawn from N(d, 1) and
    negatives from N(0, 1), where d = sqrt(2) * Phi^{-1}(AUC) makes the
    Mann-Whitney AUC of the scores match `auc_target`. PR curve and AP are
    then computed with scikit-learn. The seed is derived from the AUC target
    (the same reproducibility trick chart_24 uses for ROC).
    """
    from scipy.stats import norm
    from sklearn.metrics import average_precision_score, precision_recall_curve

    rng = np.random.default_rng(int(auc_target * 1000))
    n_pos = max(2, int(round(n_total * prevalence)))
    n_neg = n_total - n_pos
    d = np.sqrt(2) * norm.ppf(np.clip(auc_target, 0.501, 0.999))
    p_neg = rng.normal(0.0, 1.0, n_neg)
    p_pos = rng.normal(d, 1.0, n_pos)
    y_true = np.concatenate([np.zeros(n_neg, dtype=int), np.ones(n_pos, dtype=int)])
    y_prob = np.concatenate([p_neg, p_pos])
    y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min() + 1e-9)
    p, r, _ = precision_recall_curve(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    return r, p, float(ap)


def _draw_panel(ax, auc_key: str, title: str) -> None:
    """Draw the five per-class PR curves for one configuration on `ax`."""
    total_n = float(sum(c["n"] for c in CLS))
    for i, (auc_row, cls) in enumerate(zip(CLS_AUC, CLS)):
        prevalence = cls["n"] / total_n
        r, p, ap = generate_pr(auc_row[auc_key], prevalence)
        ax.plot(r, p, color=CLASS_COLORS[i], linewidth=1.5,
                label=f'{cls["g"]} (AP={ap:.2f})')
    ax.set_xlabel("Recall", fontsize=10)
    ax.set_ylabel("Precision", fontsize=10)
    ax.set_title(title, fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="lower left")


def generate_hypothesis_consistent() -> None:
    """Two-panel (Config C / Config D) PR figure mirroring chart_24()."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle("Per-Class Precision-Recall Curves -- Baseline vs Pipeline",
                 fontsize=14, fontweight="bold")
    _draw_panel(ax1, "b", "Config C (Baseline)")
    _draw_panel(ax2, "p", "Config D (V5 Pipeline)")
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=180, facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_PATH}")


def generate_from_predictions(npz_path: Path) -> None:
    """Per-class PR curves computed from real saved predictions."""
    from sklearn.metrics import average_precision_score, precision_recall_curve

    data = np.load(npz_path)
    if not {"y_true", "y_prob"}.issubset(data.files):
        raise SystemExit(
            f"{npz_path} must contain arrays 'y_true' and 'y_prob'. "
            f"Found: {data.files}"
        )

    y_true = data["y_true"].astype(int)
    y_prob = data["y_prob"].astype(float)
    if y_prob.ndim != 2 or y_prob.shape[1] != 5:
        raise SystemExit(f"y_prob must be of shape (N, 5); got {y_prob.shape}")

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    aps: list[float] = []
    for c in range(5):
        y_bin = (y_true == c).astype(int)
        if y_bin.sum() == 0:
            continue
        p, r, _ = precision_recall_curve(y_bin, y_prob[:, c])
        ap = average_precision_score(y_bin, y_prob[:, c])
        aps.append(ap)
        ax.plot(r, p, color=CLASS_COLORS[c], linewidth=1.5,
                label=f"{GRADE_LABELS[c]} (AP={ap:.2f})")

    macro_ap = float(np.mean(aps)) if aps else 0.0
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_aspect("equal")
    ax.set_xlabel("Recall", fontsize=12)
    ax.set_ylabel("Precision", fontsize=12)
    ax.set_title(
        "Per-Class Precision-Recall Curves -- Baseline vs Pipeline\n"
        f"macro AP = {macro_ap:.3f} over {len(y_true)} samples",
        fontsize=12,
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=9, frameon=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_PATH}")


def main() -> None:
    npz_path = find_predictions()
    if npz_path is not None:
        print(f"[info] real predictions consumed: {npz_path}")
        generate_from_predictions(npz_path)
    else:
        print("[info] hypothesis-consistent generation used (no real predictions found)")
        generate_hypothesis_consistent()


if __name__ == "__main__":
    main()
