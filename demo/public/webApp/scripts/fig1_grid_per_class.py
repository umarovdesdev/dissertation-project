"""
fig1_grid_per_class.py
======================

Analog of Omarov's Figure 1 ("Sample CT images of (a) ischemic, (b) hemorrhagic
stroke and (c) normal brain").

Produces a 5 x 4 grid of fundus images, one row per ICDR diabetic retinopathy
grade:
    (a) No DR              (DR 0)
    (b) Mild NPDR          (DR 1)
    (c) Moderate NPDR      (DR 2)
    (d) Severe NPDR        (DR 3)
    (e) Proliferative DR   (DR 4)

Output: ../figures_mine/fig1_per_class.png  (English captions only).

Usage:
    cd E:\\dissertation-project\\demo\\public\\webApp\\scripts
    python fig1_grid_per_class.py
"""

from __future__ import annotations

import os
import random
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
DEMO_PUBLIC = WEBAPP_DIR.parent  # demo/public

# Preferred dataset for the gallery: IDRiD (clean, high-resolution).
# Falls back to EyePACS if IDRiD samples are missing.
DATASET_PRIORITY = ["idrid", "messidor2", "eyepacs", "ddr"]

# Per-row label (Omarov-style: (a), (b), (c), ...)
ROW_LABELS = [
    "(a) DR 0 — No DR",
    "(b) DR 1 — Mild NPDR",
    "(c) DR 2 — Moderate NPDR",
    "(d) DR 3 — Severe NPDR",
    "(e) DR 4 — Proliferative DR",
]

N_COLS = 4
RANDOM_SEED = 42

OUTPUT_PATH = WEBAPP_DIR / "figures_mine" / "fig1_per_class.png"


# ---------------------------------------------------------------------------
# Sample discovery
# ---------------------------------------------------------------------------
def find_samples_for_grade(grade: int, n: int) -> list[Path]:
    """Return up to `n` image paths for the given DR grade.

    Walks DATASET_PRIORITY in order and concatenates available samples until
    `n` files are collected (or the pool is exhausted).
    """
    rng = random.Random(RANDOM_SEED + grade)
    pool: list[Path] = []
    for ds in DATASET_PRIORITY:
        folder = DEMO_PUBLIC / "datasets" / ds / "samples" / f"dr{grade}"
        if not folder.is_dir():
            continue
        for p in sorted(folder.iterdir()):
            if p.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                pool.append(p)
    rng.shuffle(pool)
    return pool[:n]


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------
def main() -> None:
    fig, axes = plt.subplots(
        nrows=5,
        ncols=N_COLS,
        figsize=(N_COLS * 2.8, 5 * 2.8),
        gridspec_kw={"wspace": 0.04, "hspace": 0.40},
    )

    for row, grade in enumerate(range(5)):
        samples = find_samples_for_grade(grade, N_COLS)
        for col in range(N_COLS):
            ax = axes[row, col]
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            if col < len(samples):
                img = Image.open(samples[col]).convert("RGB")
                ax.imshow(img)
            else:
                ax.text(
                    0.5,
                    0.5,
                    "n/a",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                    color="#888",
                )

        # Row label placed as the y-axis label on the leftmost axis.
        # Unlike fig.text, matplotlib reserves layout space for axis labels, so
        # the label no longer collides with the row of images below it.
        left_ax = axes[row, 0]
        left_ax.set_ylabel(
            ROW_LABELS[row],
            labelpad=18,
            rotation=0,
            ha="right",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
