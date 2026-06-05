"""
fig3_dataset_contents.py
========================

Analog of Omarov's Figure 3 ("Contents of the dataset").

Composes a 3 x 5 grid of fundus images with per-tile class captions
(`No DR / Mild / Moderate / Severe / Proliferative DR`) drawn above each
image, similar to Omarov's `normal / stroke` captions.

Source images: demo/public/datasets/{idrid,eyepacs,messidor2,ddr}/samples/dr{0..4}/.
Class-distribution table is computed from `E:/datasets/EyePACS/trainLabels.csv`
and saved as `fig3_dataset_distribution.csv` next to the figure.

Output:
    ../figures_mine/fig3_dataset_contents.png
    ../figures_mine/fig3_dataset_distribution.csv  (English headers)

Usage:
    python fig3_dataset_contents.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
DEMO_PUBLIC = WEBAPP_DIR.parent  # demo/public

DATASET_PRIORITY = ["idrid", "messidor2", "eyepacs", "ddr"]

GRADE_LABELS = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR",
}

N_ROWS = 3
N_COLS = 5
RANDOM_SEED = 7

EYEPACS_LABELS_CSV = Path(r"E:/datasets/EyePACS/trainLabels.csv")

OUTPUT_IMAGE = WEBAPP_DIR / "figures_mine" / "fig3_dataset_contents.png"
OUTPUT_TABLE = WEBAPP_DIR / "figures_mine" / "fig3_dataset_distribution.csv"


# ---------------------------------------------------------------------------
# Sample discovery
# ---------------------------------------------------------------------------
def collect_pool() -> list[tuple[Path, int]]:
    """Return a list of (image_path, dr_grade) candidates."""
    pool: list[tuple[Path, int]] = []
    for ds in DATASET_PRIORITY:
        for g in range(5):
            folder = DEMO_PUBLIC / "datasets" / ds / "samples" / f"dr{g}"
            if not folder.is_dir():
                continue
            for p in sorted(folder.iterdir()):
                if p.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                    pool.append((p, g))
    return pool


def build_assignment(pool: list[tuple[Path, int]]) -> list[tuple[Path, int]]:
    """Pick N_ROWS x N_COLS samples balanced across the 5 grades."""
    rng = random.Random(RANDOM_SEED)
    by_grade: dict[int, list[Path]] = {g: [] for g in range(5)}
    for p, g in pool:
        by_grade[g].append(p)
    for g in by_grade:
        rng.shuffle(by_grade[g])

    total = N_ROWS * N_COLS
    quota_per_grade = total // 5  # 3 each for a 3x5 grid
    leftover = total - 5 * quota_per_grade

    picks: list[tuple[Path, int]] = []
    for g in range(5):
        n = quota_per_grade + (1 if g < leftover else 0)
        for p in by_grade[g][:n]:
            picks.append((p, g))
    rng.shuffle(picks)
    return picks[:total]


# ---------------------------------------------------------------------------
# Class-distribution table
# ---------------------------------------------------------------------------
def build_distribution_table() -> pd.DataFrame:
    """Write a small CSV with class counts. EyePACS labels CSV is preferred;
    fallback returns demo sample counts only.
    """
    rows: list[dict] = []

    if EYEPACS_LABELS_CSV.is_file():
        df = pd.read_csv(EYEPACS_LABELS_CSV)
        # EyePACS columns: image,level
        counts = df["level"].value_counts().sort_index().to_dict()
        for g in range(5):
            rows.append({
                "dataset": "EyePACS (full)",
                "grade": g,
                "label": GRADE_LABELS[g],
                "count": int(counts.get(g, 0)),
            })

    # Demo sample counts.
    for ds in DATASET_PRIORITY:
        for g in range(5):
            folder = DEMO_PUBLIC / "datasets" / ds / "samples" / f"dr{g}"
            n = (
                sum(1 for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
                if folder.is_dir() else 0
            )
            rows.append({
                "dataset": f"{ds} (demo samples)",
                "grade": g,
                "label": GRADE_LABELS[g],
                "count": n,
            })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------
def main() -> None:
    pool = collect_pool()
    if not pool:
        raise RuntimeError("No sample images found under demo/public/datasets/*/samples/")

    picks = build_assignment(pool)

    fig, axes = plt.subplots(
        nrows=N_ROWS,
        ncols=N_COLS,
        figsize=(N_COLS * 2.6, N_ROWS * 2.9),
        gridspec_kw={"wspace": 0.06, "hspace": 0.35},
    )

    for idx in range(N_ROWS * N_COLS):
        row, col = divmod(idx, N_COLS)
        ax = axes[row, col]
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        if idx < len(picks):
            path, grade = picks[idx]
            img = Image.open(path).convert("RGB")
            ax.imshow(img)
            ax.set_title(GRADE_LABELS[grade], fontsize=10, fontweight="bold")

    OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_IMAGE, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_IMAGE}")

    table = build_distribution_table()
    table.to_csv(OUTPUT_TABLE, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"Saved: {OUTPUT_TABLE}")


if __name__ == "__main__":
    main()
