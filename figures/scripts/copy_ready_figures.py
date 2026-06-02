"""
copy_ready_figures.py
=====================

Copies the already-generated experiment plots used as analogs of Omarov's
Figures 8 and 9 into the `figures_mine/` folder under their canonical names.

Source -> Destination
    demo/public/images/results/exp1/19_training_curves.png -> figures_mine/fig8_training_curves.png
    demo/public/images/results/exp1/20_confusion_matrix.png -> figures_mine/fig9_confusion_matrix.png

Both source files are already in English. The copy is intentional so that all
final figures live in one folder for easy reference.

Usage:
    python copy_ready_figures.py
"""

from __future__ import annotations

import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
DEMO_PUBLIC = WEBAPP_DIR.parent  # demo/public

MAPPING = {
    DEMO_PUBLIC / "images" / "results" / "exp1" / "19_training_curves.png":
        WEBAPP_DIR / "figures_mine" / "fig8_training_curves.png",
    DEMO_PUBLIC / "images" / "results" / "exp1" / "20_confusion_matrix.png":
        WEBAPP_DIR / "figures_mine" / "fig9_confusion_matrix.png",
}


def main() -> None:
    for src, dst in MAPPING.items():
        if not src.is_file():
            print(f"[skip] source missing: {src}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied: {src.name} -> {dst}")


if __name__ == "__main__":
    main()
