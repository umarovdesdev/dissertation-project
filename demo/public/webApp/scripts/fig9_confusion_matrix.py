"""
fig9_confusion_matrix.py
========================

Analog of Omarov's Figure 9 ("Confusion matrix").

Renders the two normalized 5x5 confusion matrices (Config C baseline vs
Config D V5 pipeline) side by side, with a single shared colorbar placed on
its own dedicated axis well clear of the right-hand matrix so the 0.0-1.0
colour scale never overlaps the cells.

The matrix values mirror `chart_20()` in `demo/generate_charts_15_28.py`
(the project's own generation pipeline); they are not changed here.

Output: ../figures_mine/fig9_confusion_matrix.png  (English labels only).

Usage:
    python fig9_confusion_matrix.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
OUTPUT_PATH = WEBAPP_DIR / "figures_mine" / "fig9_confusion_matrix.png"

LABELS = ["DR 0", "DR 1", "DR 2", "DR 3", "DR 4"]

# Config C (baseline) — mirrored from chart_20().
CM_C = np.array([
    [0.88, 0.06, 0.04, 0.01, 0.01],
    [0.25, 0.35, 0.25, 0.10, 0.05],
    [0.08, 0.12, 0.55, 0.15, 0.10],
    [0.03, 0.08, 0.20, 0.42, 0.27],
    [0.02, 0.05, 0.12, 0.23, 0.58],
])
# Config D (V5 pipeline) — mirrored from chart_20().
CM_D = np.array([
    [0.91, 0.04, 0.03, 0.01, 0.01],
    [0.18, 0.47, 0.22, 0.08, 0.05],
    [0.06, 0.09, 0.62, 0.14, 0.09],
    [0.02, 0.06, 0.15, 0.54, 0.23],
    [0.02, 0.04, 0.08, 0.18, 0.68],
])


def _normalize_rows(cm: np.ndarray) -> np.ndarray:
    return cm / cm.sum(axis=1, keepdims=True)


def main() -> None:
    cm_c = _normalize_rows(CM_C)
    cm_d = _normalize_rows(CM_D)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Normalized Confusion Matrices", fontsize=14, fontweight="bold")

    im = None
    for ax, cm, title in [
        (axes[0], cm_c, "Config C (Baseline)"),
        (axes[1], cm_d, "Config D (V5 Pipeline)"),
    ]:
        im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=1)
        ax.set_xticks(range(5))
        ax.set_xticklabels(LABELS, fontsize=9, rotation=45, ha="right")
        ax.set_yticks(range(5))
        ax.set_yticklabels(LABELS, fontsize=9)
        ax.set_xlabel("Predicted", fontsize=10)
        ax.set_ylabel("True", fontsize=10)
        ax.set_title(title, fontsize=11)
        for i in range(5):
            for j in range(5):
                ax.text(j, i, f"{cm[i, j]:.2f}", ha="center", va="center",
                        fontsize=9, color="white" if cm[i, j] > 0.5 else "black")

    # Reserve a clear right-hand margin for the colorbar, then place the colorbar
    # on its own axis well to the right of the second matrix so the 0.0-1.0 scale
    # cannot overlap any cells.
    fig.subplots_adjust(left=0.06, right=0.86, top=0.88, bottom=0.12, wspace=0.28)
    cax = fig.add_axes([0.90, 0.15, 0.018, 0.66])
    fig.colorbar(im, cax=cax)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=180, facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
