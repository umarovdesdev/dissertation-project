"""
fig2_lesion_overlays.py
=======================

Analog of Omarov's Figure 2 ("Red area marks the location of ischemic and
hemorrhagic lesions on the images").

Produces a 5 x 4 grid of IDRiD fundus images, one row per lesion type, with
red overlay drawn from the IDRiD pixel-level groundtruth masks:

    (a) Microaneurysms
    (b) Haemorrhages
    (c) Hard Exudates
    (d) Soft Exudates
    (e) Optic Disc

Right side of each row contains a chevron-style label with the lesion name
(same style as Omarov's Fig. 2).

Output: ../figures_mine/fig2_lesion_overlays.png  (English captions only).

Required data:
    E:/datasets/IDRiD/A. Segmentation/1. Original Images/{a. Training Set,b. Testing Set}/IDRiD_NN.jpg
    E:/datasets/IDRiD/A. Segmentation/2. All Segmentation Groundtruths/{a. Training Set,b. Testing Set}/<lesion-folder>/IDRiD_NN_<suffix>.tif

Usage:
    python fig2_lesion_overlays.py
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent

IDRID_ROOT = Path(r"E:/datasets/IDRiD/A. Segmentation")
RGB_DIRS = [
    IDRID_ROOT / "1. Original Images" / "a. Training Set",
    IDRID_ROOT / "1. Original Images" / "b. Testing Set",
]
MASK_ROOTS = [
    IDRID_ROOT / "2. All Segmentation Groundtruths" / "a. Training Set",
    IDRID_ROOT / "2. All Segmentation Groundtruths" / "b. Testing Set",
]

# Per-row label, mask folder name, file-name suffix used by IDRiD.
ROWS = [
    ("(a) Microaneurysms", "1. Microaneurysms", "MA"),
    ("(b) Haemorrhages",   "2. Haemorrhages",   "HE"),
    ("(c) Hard Exudates",  "3. Hard Exudates",  "EX"),
    ("(d) Soft Exudates",  "4. Soft Exudates",  "SE"),
    ("(e) Optic Disc",     "5. Optic Disc",     "OD"),
]

N_COLS = 4
# Teal contour color (#2a9d8f). Far more visible against the brown/orange
# fundus background than red, and matches the project accent palette.
TEAL_RGB = (42, 157, 143)  # 0x2a, 0x9d, 0x8f
CONTOUR_THICKNESS = 2
TARGET_WIDTH = 512  # down-sample width so thin contours survive rendering
MIN_MASK_PIXELS = 50  # skip near-empty masks

OUTPUT_PATH = WEBAPP_DIR / "figures_mine" / "fig2_lesion_overlays.png"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_rgb(case_id: str) -> Path | None:
    """Locate the RGB image for an IDRiD case id like 'IDRiD_01'."""
    for d in RGB_DIRS:
        p = d / f"{case_id}.jpg"
        if p.is_file():
            return p
    return None


def list_masks(folder_name: str, suffix: str) -> list[tuple[str, Path]]:
    """Return [(case_id, mask_path), ...] for a given lesion folder."""
    items: list[tuple[str, Path]] = []
    for root in MASK_ROOTS:
        d = root / folder_name
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir()):
            if not p.is_file():
                continue
            m = re.match(rf"(IDRiD_\d+)_{suffix}\.tif$", p.name, re.IGNORECASE)
            if not m:
                continue
            items.append((m.group(1), p))
    return items


def overlay_teal_contours(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Draw teal contours of binary `mask` on top of `rgb` (uint8 HxWx3).

    The RGB image is down-sampled to ``TARGET_WIDTH`` first and the mask is
    matched with nearest-neighbour interpolation, so the contours are drawn at
    (close to) the final display resolution and survive matplotlib's own
    down-sampling instead of collapsing to sub-pixel lines.
    """
    binm = (mask > 0).astype(np.uint8) * 255
    if binm.shape != rgb.shape[:2]:
        binm = cv2.resize(binm, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_NEAREST)

    scale = TARGET_WIDTH / float(rgb.shape[1])
    new_w = TARGET_WIDTH
    new_h = max(1, int(round(rgb.shape[0] * scale)))
    rgb_small = cv2.resize(rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)
    mask_small = cv2.resize(binm, (new_w, new_h), interpolation=cv2.INTER_NEAREST)

    out = rgb_small.copy()
    contours, _ = cv2.findContours(mask_small, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, contours, -1, TEAL_RGB, CONTOUR_THICKNESS)
    return out


def pick_overlays_for_row(folder_name: str, suffix: str, n: int) -> list[np.ndarray]:
    """Build up to `n` overlay images for one row."""
    out: list[np.ndarray] = []
    for case_id, mpath in list_masks(folder_name, suffix):
        rgb_path = find_rgb(case_id)
        if rgb_path is None:
            continue
        mask = cv2.imread(str(mpath), cv2.IMREAD_GRAYSCALE)
        if mask is None or int((mask > 0).sum()) < MIN_MASK_PIXELS:
            continue
        rgb_bgr = cv2.imread(str(rgb_path), cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(rgb_bgr, cv2.COLOR_BGR2RGB)
        out.append(overlay_teal_contours(rgb, mask))
        if len(out) >= n:
            break
    return out


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------
def main() -> None:
    # The label column is given a generous width ratio (and the whole figure is
    # widened) so the combined chevron label fits completely inside its axis and
    # never overlaps the rightmost image column.
    label_ratio = 1.6
    fig, axes = plt.subplots(
        nrows=5,
        ncols=N_COLS + 1,  # extra column for chevron labels
        figsize=((N_COLS + label_ratio) * 2.8, 5 * 2.6),
        gridspec_kw={"width_ratios": [1] * N_COLS + [label_ratio],
                     "wspace": 0.06, "hspace": 0.12},
    )

    for row, (label, folder_name, suffix) in enumerate(ROWS):
        images = pick_overlays_for_row(folder_name, suffix, N_COLS)
        for col in range(N_COLS):
            ax = axes[row, col]
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            if col < len(images):
                ax.imshow(images[col])
            else:
                ax.text(0.5, 0.5, "no mask", ha="center", va="center",
                        transform=ax.transAxes, color="#888")

        # Chevron-style right label.
        cax = axes[row, N_COLS]
        cax.set_xlim(0, 1)
        cax.set_ylim(0, 1)
        cax.axis("off")
        # Pentagon pointing left  --> Omarov-style arrow. The body spans almost
        # the full (now wider) axis so the label has room inside it.
        verts = np.array([
            [0.02, 0.5],
            [0.16, 0.85],
            [0.98, 0.85],
            [0.98, 0.15],
            [0.16, 0.15],
        ])
        cax.add_patch(mpatches.Polygon(verts, closed=True, facecolor="#ffffff",
                                       edgecolor="black", linewidth=1.2))
        # Single combined label, e.g. "(a) Microaneurysms", centered in the chevron body.
        cax.text(0.57, 0.5, label,
                 ha="center", va="center", fontsize=11, fontweight="bold")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
