"""Generate images for empty slide folders.

Targets:
  defense/assets/architecture/07_cnn/cnn_architecture.png
  defense/assets/architecture/09_training/focal_loss.png
  defense/assets/architecture/09_training/cv_5fold.png
  defense/assets/preprocessing/20_aug_translation/left_max.png
  defense/assets/preprocessing/20_aug_translation/left_min.png
  defense/assets/preprocessing/20_aug_translation/distribution.png
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from PIL import Image

C = {
    "blue": "#378ADD", "teal": "#1D9E75", "coral": "#D85A30",
    "purple": "#7F77DD", "amber": "#EF9F27", "gray": "#888780",
    "green": "#639922", "red": "#E24B4A",
    "blueBg": "#E6F1FB", "tealBg": "#E1F5EE", "coralBg": "#FAECE7",
    "purpleBg": "#EEEDFE",
    "grayBg": "#F1EFE8", "amberBg": "#FAEEDA",
    "blueT": "#0C447C", "tealT": "#085041", "coralT": "#712B13",
    "purpleT": "#3C3489",
    "grayT": "#444441", "amberT": "#633806",
}

ROOT = Path(__file__).resolve().parent.parent / "assets"
DPI = 200


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {path.relative_to(ROOT.parent)}")


# --------------------------------------------------------------- 07_cnn

def make_cnn_architecture() -> plt.Figure:
    fig = plt.figure(figsize=(14, 8.5))
    gs = fig.add_gridspec(2, 1, hspace=0.45)
    ax_r = fig.add_subplot(gs[0])
    ax_e = fig.add_subplot(gs[1])

    def draw_block(ax, x, y, w, h, label, fc, fw="normal", fs=9):
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=fc, edgecolor=C["grayT"], linewidth=1.3,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, fontweight=fw, color=C["grayT"])

    def arrow(ax, x1, x2, y):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=C["grayT"], lw=1.5))

    # --- ResNet-50 ---
    ax_r.set_xlim(0, 14)
    ax_r.set_ylim(0, 3)
    ax_r.axis("off")
    ax_r.set_title(
        "ResNet-50  ·  25.6 M params  ·  ImageNet-pretrained",
        fontsize=13, fontweight="bold", color=C["grayT"],
        loc="left", pad=4,
    )

    blocks_r = [
        (0.0, 1.4, 1.5, 1.0, "Input\n4 × 512 × 512", C["grayBg"], "normal"),
        (1.7, 1.3, 1.7, 1.2, "Conv1 7×7, /2\n4ch → 64", C["coralBg"], "bold"),
        (3.7, 1.4, 1.4, 1.0, "MaxPool\n3×3, /2", C["grayBg"], "normal"),
        (5.4, 1.3, 1.4, 1.2, "Stage 1\n3 × BN", C["tealBg"], "normal"),
        (7.0, 1.3, 1.4, 1.2, "Stage 2\n4 × BN", C["tealBg"], "normal"),
        (8.6, 1.3, 1.4, 1.2, "Stage 3\n6 × BN", C["tealBg"], "normal"),
        (10.2, 1.3, 1.4, 1.2, "Stage 4\n3 × BN", C["tealBg"], "normal"),
        (11.8, 1.4, 1.1, 1.0, "GAP\n2048-d", C["grayBg"], "normal"),
        (13.1, 1.4, 0.9, 1.0, "FC\n→ 5", C["amberBg"], "bold"),
    ]
    for x, y, w, h, label, fc, fw in blocks_r:
        draw_block(ax_r, x, y, w, h, label, fc, fw=fw)

    pairs_r = [(1.5, 1.7), (3.4, 3.7), (5.1, 5.4), (6.8, 7.0),
               (8.4, 8.6), (10.0, 10.2), (11.6, 11.8), (12.9, 13.1)]
    for x1, x2 in pairs_r:
        arrow(ax_r, x1, x2, 1.9)

    ax_r.text(
        2.55, 0.55,
        "▲ 4-ch conv1 — pretrained RGB weights preserved,\n"
        "    mask channel initialised as mean(RGB weights)",
        ha="center", fontsize=9.5, style="italic", color=C["coralT"],
    )

    # --- EfficientNet-B3 ---
    ax_e.set_xlim(0, 14)
    ax_e.set_ylim(0, 3)
    ax_e.axis("off")
    ax_e.set_title(
        "EfficientNet-B3  ·  12.2 M params  ·  ImageNet-pretrained",
        fontsize=13, fontweight="bold", color=C["grayT"],
        loc="left", pad=4,
    )

    blocks_e = [
        (0.0, 1.4, 1.5, 1.0, "Input\n4 × 512 × 512", C["grayBg"], "normal"),
        (1.7, 1.3, 1.7, 1.2, "Stem 3×3, /2\n4ch → 40", C["coralBg"], "bold"),
        (3.7, 1.3, 1.4, 1.2, "MBConv1\n×2 → 24", C["tealBg"], "normal"),
        (5.3, 1.3, 1.4, 1.2, "MBConv6\n×3 → 32", C["tealBg"], "normal"),
        (6.9, 1.3, 1.4, 1.2, "MBConv6\n×3 → 48", C["tealBg"], "normal"),
        (8.5, 1.3, 1.4, 1.2, "MBConv6\n×5 → 136", C["tealBg"], "normal"),
        (10.1, 1.3, 1.4, 1.2, "MBConv6\n×6 → 384", C["tealBg"], "normal"),
        (11.8, 1.4, 1.1, 1.0, "GAP\n1536-d", C["grayBg"], "normal"),
        (13.1, 1.4, 0.9, 1.0, "FC\n→ 5", C["amberBg"], "bold"),
    ]
    for x, y, w, h, label, fc, fw in blocks_e:
        draw_block(ax_e, x, y, w, h, label, fc, fw=fw)

    pairs_e = [(1.5, 1.7), (3.4, 3.7), (5.1, 5.3), (6.7, 6.9),
               (8.3, 8.5), (9.9, 10.1), (11.5, 11.8), (12.9, 13.1)]
    for x1, x2 in pairs_e:
        arrow(ax_e, x1, x2, 1.9)

    ax_e.text(
        2.55, 0.55,
        "▲ Compound-scaled MBConv with squeeze-and-excite\n"
        "    Stem stride=2; modified for 4-channel input",
        ha="center", fontsize=9.5, style="italic", color=C["coralT"],
    )

    fig.suptitle(
        "CNN Backbones  —  4-channel conv1 modification (V5 contribution)",
        fontsize=15, fontweight="bold", y=0.99,
    )
    return fig


# ----------------------------------------------------------- 09_training

def make_focal_loss() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    p = np.linspace(0.01, 1.0, 400)

    series = [
        (0,   "γ = 0  (cross-entropy)", C["gray"],   1.6),
        (0.5, "γ = 0.5",                C["amber"],  1.6),
        (1,   "γ = 1",                  C["green"],  1.6),
        (2,   "γ = 2  (this work)",     C["coral"],  3.2),
        (5,   "γ = 5",                  C["red"],    1.6),
    ]
    for g, label, color, lw in series:
        loss = -(1 - p) ** g * np.log(p)
        ax.plot(p, loss, color=color, linewidth=lw, label=label)

    ax.annotate(
        "Easy examples\ndown-weighted",
        xy=(0.85, 0.05), xytext=(0.55, 1.6),
        fontsize=10, color=C["coralT"], style="italic",
        arrowprops=dict(arrowstyle="->", color=C["coralT"]),
    )
    ax.annotate(
        "Hard examples\nstill heavily penalised",
        xy=(0.05, 3.0), xytext=(0.20, 3.5),
        fontsize=10, color=C["coralT"], style="italic",
        arrowprops=dict(arrowstyle="->", color=C["coralT"]),
    )

    ax.set_xlabel("Predicted probability of true class  p", fontsize=12)
    ax.set_ylabel("Loss", fontsize=12)
    ax.set_title(
        r"Focal Loss   $\mathrm{FL}(p) = -\,\alpha\,(1-p)^{\gamma}\,\log p$"
        "\n" "α = inverse-frequency class weights,  γ = 2",
        fontsize=12.5, fontweight="bold", pad=10,
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 5)
    ax.legend(loc="upper right", fontsize=10, frameon=True)
    ax.grid(alpha=0.3)
    return fig


def make_cv_diagram() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11, 4.8))
    n_folds = 5

    for fold in range(n_folds):
        y = n_folds - fold - 1
        for k in range(n_folds):
            x_start = k * 1.9
            is_val = (k == fold)
            color = C["coral"] if is_val else C["teal"]
            label = "Val" if is_val else "Train"
            ax.add_patch(mpatches.Rectangle(
                (x_start, y), 1.8, 0.85,
                facecolor=color, edgecolor="white", linewidth=2,
            ))
            ax.text(x_start + 0.9, y + 0.42, label,
                    ha="center", va="center",
                    color="white", fontsize=11, fontweight="bold")
        ax.text(-0.25, y + 0.42, f"Fold {fold + 1}",
                ha="right", va="center",
                fontsize=11, fontweight="bold", color=C["grayT"])

    for k in range(n_folds):
        ax.text(k * 1.9 + 0.9, n_folds + 0.15,
                f"Patient\ngroup {k + 1}",
                ha="center", va="bottom",
                fontsize=9.5, color=C["grayT"], fontweight="bold")

    legend_handles = [
        mpatches.Patch(facecolor=C["teal"], edgecolor="white", label="Train  (≈80%)"),
        mpatches.Patch(facecolor=C["coral"], edgecolor="white", label="Validation  (≈20%)"),
    ]
    ax.legend(handles=legend_handles, loc="lower center",
              bbox_to_anchor=(0.5, -0.12), ncol=2,
              fontsize=10.5, frameon=False)

    ax.set_xlim(-1.6, n_folds * 1.9 + 0.4)
    ax.set_ylim(-0.6, n_folds + 1.1)
    ax.axis("off")

    ax.set_title(
        "5-Fold Patient-Level Stratified Cross-Validation\n"
        "(no patient appears in train and val of the same fold)",
        fontsize=13, fontweight="bold", color=C["grayT"], pad=18,
    )
    return fig


# ------------------------------------------------------ 20_aug_translation

def make_translation_images() -> None:
    src_path = ROOT / "preprocessing" / "22_aug_shear" / "left_min.png"
    img = np.array(Image.open(src_path).convert("RGB"))
    H, W = img.shape[:2]

    tx, ty = 30, 20

    def shift(arr: np.ndarray, dx: int, dy: int) -> np.ndarray:
        out = np.zeros_like(arr)
        sx1, sx2 = max(0, -dx), min(W, W - dx)
        sy1, sy2 = max(0, -dy), min(H, H - dy)
        dx1 = max(0, dx)
        dy1 = max(0, dy)
        dx2 = dx1 + (sx2 - sx1)
        dy2 = dy1 + (sy2 - sy1)
        out[dy1:dy2, dx1:dx2] = arr[sy1:sy2, sx1:sx2]
        return out

    out_dir = ROOT / "preprocessing" / "20_aug_translation"
    out_dir.mkdir(parents=True, exist_ok=True)

    Image.fromarray(shift(img, tx, ty)).save(out_dir / "left_max.png")
    print(f"  -> {(out_dir / 'left_max.png').relative_to(ROOT.parent)}")
    Image.fromarray(shift(img, -tx, -ty)).save(out_dir / "left_min.png")
    print(f"  -> {(out_dir / 'left_min.png').relative_to(ROOT.parent)}")


def make_translation_distribution() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 3.5))
    delta = 30
    x = np.linspace(-delta - 8, delta + 8, 1000)
    y = np.where(np.abs(x) <= delta, 1.0 / (2 * delta), 0.0)

    ax.plot(x, y, color=C["blue"], linewidth=2.2)
    ax.fill_between(x, 0, y, color=C["blueBg"], alpha=0.85)

    ax.set_title(f"Uniform [−{delta}, +{delta}] px,  P(apply) = 0.5",
                 fontsize=11)
    ax.set_xlabel("Translation offset (pixels, per axis)")
    ax.set_ylabel("Probability density")
    ax.grid(alpha=0.25)
    ax.set_ylim(0, 0.025)
    return fig


# -------------------------------------------------------------- main

def main() -> None:
    print(f"Output root: {ROOT}")
    print("Generating CNN architecture (07)...")
    save(make_cnn_architecture(),
         ROOT / "architecture" / "07_cnn" / "cnn_architecture.png")

    print("Generating training params (09)...")
    save(make_focal_loss(),
         ROOT / "architecture" / "09_training" / "focal_loss.png")
    save(make_cv_diagram(),
         ROOT / "architecture" / "09_training" / "cv_5fold.png")

    print("Generating translation augmentation (20)...")
    make_translation_images()
    save(make_translation_distribution(),
         ROOT / "preprocessing" / "20_aug_translation" / "distribution.png")

    print("Done.")


if __name__ == "__main__":
    main()
