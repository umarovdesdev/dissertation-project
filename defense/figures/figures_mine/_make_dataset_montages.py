#!/usr/bin/env python3
"""Build the two montage figures that reference sample-image directories:
  FIG-1.1  §1.1.1  EyePACS fundus images across DR grades 0-4 (clinical grading)
  FIG-4.2  §4.1.1  representative fundus per DR grade across the dataset architecture

Reads representative samples from demo/web/public/datasets/<ds>/samples/dr{0..4}/,
center-crops to square, and tiles them with grade/dataset labels. Deterministic
(first sorted file per grade). Run: python _make_dataset_montages.py
"""
from __future__ import annotations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 11,
    "savefig.dpi": 200,
})

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # repo root (figures_mine -> figures -> defense -> root)
DATA = ROOT / "demo/web/public/datasets"
INK = "#1a1a1a"

GRADES = ["dr0", "dr1", "dr2", "dr3", "dr4"]
GRADE_LABELS = ["DR 0\n(No DR)", "DR 1\n(Mild)", "DR 2\n(Moderate)",
                "DR 3\n(Severe)", "DR 4\n(Proliferative)"]
# dataset dir -> display name, in display order (only the DR-0..4-graded datasets)
DATASETS = [("eyepacs", "EyePACS"), ("aptos", "APTOS 2019"), ("messidor2", "Messidor-2"),
            ("idrid", "IDRiD"), ("ddr", "DDR"), ("clinical", "Clinical")]


def load_square(path: Path, size: int = 320) -> np.ndarray:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((size, size))
    return np.asarray(im)


def pick(ds_dir: str, grade: str) -> Path | None:
    d = DATA / ds_dir / "samples" / grade
    files = sorted(f for f in d.glob("*") if f.suffix.lower() in (".jpg", ".jpeg", ".png"))
    return files[0] if files else None


def _blank(ax):
    ax.imshow(np.full((10, 10, 3), 0.93), aspect="auto")
    ax.text(0.5, 0.5, "n/a", transform=ax.transAxes, ha="center", va="center", color="#999")


def fig_grades_eyepacs(path: Path):
    fig, axes = plt.subplots(1, 5, figsize=(12, 3.1))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.80, bottom=0.14, wspace=0.06)
    for ax, grade, lab in zip(axes, GRADES, GRADE_LABELS):
        f = pick("eyepacs", grade)
        if f:
            ax.imshow(load_square(f))
        else:
            _blank(ax)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(INK); s.set_linewidth(1.0)
        ax.set_title(lab, fontsize=10.5, color=INK)
    fig.suptitle("Representative fundus images across the five-class DR grading scale (EyePACS)",
                 fontsize=12.5, y=0.975, color=INK)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)
    print(f"WROTE {path.name}")


def fig_dataset_matrix(path: Path):
    nrows, ncols = len(DATASETS), len(GRADES)
    fig, axes = plt.subplots(nrows, ncols, figsize=(10.5, 2.05 * nrows))
    fig.subplots_adjust(left=0.10, right=0.995, top=0.93, bottom=0.01, wspace=0.05, hspace=0.05)
    for i, (ds_dir, ds_name) in enumerate(DATASETS):
        for j, grade in enumerate(GRADES):
            ax = axes[i, j]
            f = pick(ds_dir, grade)
            if f:
                ax.imshow(load_square(f))
            else:
                _blank(ax)
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#bbbbbb"); s.set_linewidth(0.6)
            if i == 0:
                ax.set_title(f"DR {j}", fontsize=11, color=INK, pad=4)
            if j == 0:
                ax.set_ylabel(ds_name, fontsize=11, color=INK, rotation=90, labelpad=8)
    fig.suptitle("Representative fundus images per DR grade across the dataset architecture",
                 fontsize=12.5, y=0.985, color=INK)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)
    print(f"WROTE {path.name}")


def main():
    fig_grades_eyepacs(HERE / "fig1_1_dr_grades_eyepacs.png")
    fig_dataset_matrix(HERE / "fig4_2_dataset_grade_matrix.png")


if __name__ == "__main__":
    main()
