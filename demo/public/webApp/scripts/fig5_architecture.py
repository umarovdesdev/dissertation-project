"""
fig5_architecture.py
====================

Render an artistic, perspective-style architecture diagram of the 4-channel
EfficientNet-B3 classifier (Config D) used in Experiment 1.

This is the scriptable equivalent of the NN-SVG "AlexNet" style figure referred
to in TASK.md (figure 5). NN-SVG is a browser-only interactive tool, so this
script reproduces the same grouped-block visual with matplotlib so the figure
can be regenerated reproducibly.

Pipeline depicted (English-only labels):
    Input 512x512x4 -> Stem -> MBConv blocks 1..7 -> 1x1 Conv (1536)
    -> GAP -> FC (5) -> Softmax

Output (into webApp/figures_mine/):
    * fig5_architecture_artistic.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch

HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
FIGURES_MINE = WEBAPP_DIR / "figures_mine"

# EfficientNet-B3 grouped stages.
# (label, detail, box-height, box-width, face colour).
# Heights/widths are purely artistic (perspective hints).
STAGES = [
    ("Input",     "512x512x4",    3.6,  0.55, "#4c78a8"),
    ("Stem",      "Conv 3x3 s2",  3.2,  0.55, "#5b8bb5"),
    ("MBConv1",   "256x256, 24",  3.0,  0.60, "#6aa0c4"),
    ("MBConv2",   "128x128, 32",  2.5,  0.70, "#54a24b"),
    ("MBConv3",   "64x64, 48",    2.0,  0.80, "#6cb35f"),
    ("MBConv4",   "32x32, 96",    1.5,  0.95, "#83c275"),
    ("MBConv5",   "16x16, 136",   1.15, 1.10, "#e6a23c"),
    ("MBConv6",   "8x8, 232",     0.85, 1.30, "#eab455"),
    ("MBConv7",   "8x8, 384",     0.70, 1.45, "#edc06f"),
    ("1x1 Conv",  "8x8, 1536",    0.60, 1.55, "#e0654f"),
    ("GAP",       "1x1x1536",     0.35, 0.45, "#b07aa1"),
    ("FC",        "5 logits",     1.60, 0.30, "#9c6b95"),
    ("Softmax",   "DR 0..4",      1.60, 0.30, "#8a5d84"),
]


def draw_block(ax, x: float, height: float, width: float, color: str,
               depth: float = 0.32) -> float:
    """Draw a single 3D-perspective box at horizontal position x; return right x."""
    h = height / 2.0
    w = width
    front = [(x, -h), (x + w, -h), (x + w, h), (x, h)]
    ax.add_patch(Polygon(front, closed=True, facecolor=color,
                         edgecolor="#222222", linewidth=1.0, zorder=3))
    top = [(x, h), (x + w, h), (x + w + depth, h + depth), (x + depth, h + depth)]
    ax.add_patch(Polygon(top, closed=True, facecolor=color,
                         edgecolor="#222222", linewidth=1.0, alpha=0.78, zorder=2))
    side = [(x + w, -h), (x + w + depth, -h + depth),
            (x + w + depth, h + depth), (x + w, h)]
    ax.add_patch(Polygon(side, closed=True, facecolor=color,
                         edgecolor="#222222", linewidth=1.0, alpha=0.60, zorder=2))
    return x + w


def main() -> None:
    FIGURES_MINE.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 6.5))
    ax.set_xlim(-0.5, 21.5)
    ax.set_ylim(-3.4, 3.6)
    ax.axis("off")

    gap = 1.05
    x = 0.0
    centers = []
    for (label, detail, height, width, color) in STAGES:
        x_end = draw_block(ax, x, height, width, color)
        cx = (x + x_end) / 2.0
        centers.append((x_end, x))
        ax.text(cx + 0.16, height / 2.0 + 0.55, label, ha="center", va="bottom",
                fontsize=10.5, fontweight="bold", color="#1a1a1a")
        ax.text(cx, -height / 2.0 - 0.30, detail, ha="center", va="top",
                fontsize=8.0, color="#444444")
        x = x_end + gap

    for i in range(len(centers) - 1):
        x_end_a = centers[i][0]
        x_start_b = centers[i + 1][1]
        ax.add_patch(FancyArrowPatch((x_end_a + 0.30, 0), (x_start_b, 0),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color="#555555", linewidth=1.1, zorder=1))

    ax.set_title("EfficientNet-B3 (Config D) -- 4-channel Diabetic Retinopathy "
                 "Classifier", fontsize=14, fontweight="bold", pad=18)

    legend_items = [
        ("#4c78a8", "Input / Stem"),
        ("#54a24b", "MBConv blocks (1-7)"),
        ("#e0654f", "Head 1x1 Conv (1536)"),
        ("#b07aa1", "GAP / FC / Softmax"),
    ]
    handles = [plt.Line2D([0], [0], marker="s", linestyle="", markersize=12,
                          markerfacecolor=c, markeredgecolor="#222222", label=l)
               for c, l in legend_items]
    ax.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
              fontsize=9.5, bbox_to_anchor=(0.5, -0.02))

    out = FIGURES_MINE / "fig5_architecture_artistic.png"
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[fig5] saved: {out}")


if __name__ == "__main__":
    main()
