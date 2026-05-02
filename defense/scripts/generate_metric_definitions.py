"""Generate didactic metric-definition diagrams for slide 31.

Produces 5 PNGs in defense/assets/metrics/:
  def_f1.png     — F1: 2x2 toy confusion matrix + P/R/F1 formulas
  def_auc.png    — AUC: random / realistic / perfect ROC curves
  def_kappa.png  — Cohen's kappa: po / pe / kappa formula on same matrix
  def_g.png      — Generalization Ratio G with H-4 threshold (0.85) on number line
  def_alo.png    — ALO: 3-panel attention / lesion / intersection schematic
"""
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

C = {
    "blue": "#378ADD", "teal": "#1D9E75", "coral": "#D85A30",
    "purple": "#7F77DD", "amber": "#EF9F27", "gray": "#888780",
    "green": "#639922", "red": "#E24B4A",
    "blueBg": "#E6F1FB", "tealBg": "#E1F5EE", "coralBg": "#FAECE7",
    "grayBg": "#F1EFE8", "amberBg": "#FAEEDA",
    "blueT": "#0C447C", "tealT": "#085041", "coralT": "#712B13",
    "grayT": "#444441", "amberT": "#633806",
}

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "metrics"
DPI = 200


def save(fig: plt.Figure, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {path.name}")


def make_f1() -> plt.Figure:
    fig, (ax_cm, ax_text) = plt.subplots(
        1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1, 1.1]}
    )
    cells = np.array([["TP\n80", "FN\n20"], ["FP\n10", "TN\n90"]])
    colors = np.array([[C["tealBg"], C["coralBg"]],
                       [C["coralBg"], C["tealBg"]]])
    for i in range(2):
        for j in range(2):
            ax_cm.add_patch(patches.Rectangle(
                (j, 1 - i), 1, 1, facecolor=colors[i, j],
                edgecolor=C["grayT"], linewidth=1.5,
            ))
            ax_cm.text(j + 0.5, 1.5 - i, cells[i, j],
                       ha="center", va="center",
                       fontsize=18, fontweight="bold", color=C["grayT"])
    ax_cm.set_xlim(-0.05, 2.05)
    ax_cm.set_ylim(-0.05, 2.05)
    ax_cm.set_xticks([0.5, 1.5])
    ax_cm.set_yticks([0.5, 1.5])
    ax_cm.set_xticklabels(["Predicted +", "Predicted −"], fontsize=12)
    ax_cm.set_yticklabels(["Actual −", "Actual +"], fontsize=12)
    for s in ax_cm.spines.values():
        s.set_visible(False)
    ax_cm.tick_params(length=0)
    ax_cm.set_title("Confusion matrix (toy example)",
                    fontsize=13, fontweight="bold", pad=12)

    ax_text.axis("off")
    items = [
        ("Precision  =  TP / (TP + FP)",
         "= 80 / (80 + 10) = 0.889", C["blueT"]),
        ("Recall  =  TP / (TP + FN)",
         "= 80 / (80 + 20) = 0.800", C["tealT"]),
        ("F1  =  2 · P · R / (P + R)",
         "= 2 · 0.889 · 0.800 / 1.689 = 0.842", C["coralT"]),
    ]
    y = 0.9
    for label, value, color in items:
        ax_text.text(0.02, y, label, fontsize=14, fontweight="bold",
                     color=color, transform=ax_text.transAxes,
                     family="monospace")
        ax_text.text(0.02, y - 0.07, value, fontsize=11, color=C["grayT"],
                     transform=ax_text.transAxes, family="monospace")
        y -= 0.24
    ax_text.text(
        0.02, 0.05,
        "F1 — harmonic mean of P and R.\nPenalises imbalance: low P or low R drags F1 down.",
        fontsize=11, style="italic", color=C["grayT"],
        transform=ax_text.transAxes,
    )

    fig.suptitle("F1-score", fontsize=17, fontweight="bold", y=1.02)
    return fig


def make_auc() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 7))
    fpr = np.linspace(0, 1, 200)
    realistic = 1 - (1 - fpr) ** 6  # AUC ≈ 0.857

    ax.plot([0, 0, 1], [0, 1, 1], color=C["blue"], linestyle="--",
            linewidth=2.5, label="Perfect classifier (AUC = 1.00)")
    ax.plot(fpr, realistic, color=C["teal"], linewidth=3,
            label="Realistic model (AUC ≈ 0.86)")
    ax.fill_between(fpr, 0, realistic, color=C["tealBg"], alpha=0.7)
    ax.plot([0, 1], [0, 1], color=C["gray"], linestyle=":",
            linewidth=2, label="Random classifier (AUC = 0.50)")

    ax.text(0.55, 0.42, "AUC =\narea under curve",
            fontsize=13, fontweight="bold", color=C["tealT"], ha="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=C["teal"], linewidth=1.5))

    ax.set_xlabel("False Positive Rate (FPR)", fontsize=13)
    ax.set_ylabel("True Positive Rate (TPR)", fontsize=13)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")
    ax.legend(loc="lower right", fontsize=11, frameon=True)
    ax.grid(alpha=0.25)
    ax.set_title("ROC-AUC", fontsize=17, fontweight="bold", pad=12)
    return fig


def make_kappa() -> plt.Figure:
    fig, (ax_cm, ax_text) = plt.subplots(
        1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1, 1.1]}
    )
    cm = np.array([[80, 20], [10, 90]])
    total = cm.sum()
    po = (cm[0, 0] + cm[1, 1]) / total
    row_marg = cm.sum(axis=1) / total
    col_marg = cm.sum(axis=0) / total
    pe = row_marg[0] * col_marg[0] + row_marg[1] * col_marg[1]
    kappa = (po - pe) / (1 - pe)

    cells = np.array([["80", "20"], ["10", "90"]])
    colors = np.array([[C["tealBg"], C["grayBg"]],
                       [C["grayBg"], C["tealBg"]]])
    for i in range(2):
        for j in range(2):
            ax_cm.add_patch(patches.Rectangle(
                (j, 1 - i), 1, 1, facecolor=colors[i, j],
                edgecolor=C["grayT"], linewidth=1.5,
            ))
            ax_cm.text(j + 0.5, 1.5 - i, cells[i, j],
                       ha="center", va="center",
                       fontsize=22, fontweight="bold", color=C["grayT"])
    ax_cm.text(2.15, 1.5, f"row Σ={cm[0].sum()}",
               fontsize=10, color=C["blueT"], va="center")
    ax_cm.text(2.15, 0.5, f"row Σ={cm[1].sum()}",
               fontsize=10, color=C["blueT"], va="center")
    ax_cm.text(0.5, -0.25, f"col Σ={cm[:, 0].sum()}",
               fontsize=10, color=C["blueT"], ha="center")
    ax_cm.text(1.5, -0.25, f"col Σ={cm[:, 1].sum()}",
               fontsize=10, color=C["blueT"], ha="center")

    ax_cm.set_xlim(-0.05, 2.6)
    ax_cm.set_ylim(-0.45, 2.05)
    ax_cm.set_xticks([0.5, 1.5])
    ax_cm.set_yticks([0.5, 1.5])
    ax_cm.set_xticklabels(["Pred +", "Pred −"], fontsize=12)
    ax_cm.set_yticklabels(["Actual −", "Actual +"], fontsize=12)
    for s in ax_cm.spines.values():
        s.set_visible(False)
    ax_cm.tick_params(length=0)
    ax_cm.set_title("2×2 with marginals",
                    fontsize=13, fontweight="bold", pad=12)

    ax_text.axis("off")
    items = [
        ("p_o  (observed agreement)",
         f"= (80 + 90) / 200 = {po:.3f}", C["blueT"]),
        ("p_e  (expected by chance)",
         f"= {row_marg[0]:.2f}·{col_marg[0]:.2f} + "
         f"{row_marg[1]:.2f}·{col_marg[1]:.2f} = {pe:.3f}", C["amberT"]),
        ("κ  =  (p_o − p_e) / (1 − p_e)",
         f"= ({po:.3f} − {pe:.3f}) / (1 − {pe:.3f}) = {kappa:.3f}",
         C["coralT"]),
    ]
    y = 0.92
    for label, value, color in items:
        ax_text.text(0.02, y, label, fontsize=13, fontweight="bold",
                     color=color, transform=ax_text.transAxes,
                     family="monospace")
        ax_text.text(0.02, y - 0.06, value, fontsize=10.5, color=C["grayT"],
                     transform=ax_text.transAxes, family="monospace")
        y -= 0.21

    interp = (
        "Landis & Koch (1977):\n"
        "  0.0–0.2 slight       0.6–0.8 substantial\n"
        "  0.2–0.4 fair         0.8–1.0 almost perfect\n"
        "  0.4–0.6 moderate"
    )
    ax_text.text(0.02, 0.04, interp, fontsize=10, color=C["grayT"],
                 transform=ax_text.transAxes, family="monospace",
                 bbox=dict(boxstyle="round,pad=0.4", facecolor=C["grayBg"],
                           edgecolor=C["gray"]))

    fig.suptitle("Cohen's κ — agreement above chance",
                 fontsize=17, fontweight="bold", y=1.02)
    return fig


def make_f1_kappa() -> plt.Figure:
    """Combined diagram: shared confusion matrix + F1 (top) + κ (bottom)."""
    fig = plt.figure(figsize=(13, 6.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.25], wspace=0.1)
    ax_cm = fig.add_subplot(gs[0])
    ax_text = fig.add_subplot(gs[1])

    cm = np.array([[80, 20], [10, 90]])
    cells = np.array([["TP\n80", "FN\n20"], ["FP\n10", "TN\n90"]])
    colors = np.array([[C["tealBg"], C["coralBg"]],
                       [C["coralBg"], C["tealBg"]]])
    for i in range(2):
        for j in range(2):
            ax_cm.add_patch(patches.Rectangle(
                (j, 1 - i), 1, 1, facecolor=colors[i, j],
                edgecolor=C["grayT"], linewidth=1.5,
            ))
            ax_cm.text(j + 0.5, 1.5 - i, cells[i, j],
                       ha="center", va="center",
                       fontsize=19, fontweight="bold", color=C["grayT"])
    ax_cm.text(2.15, 1.5, f"Σ={cm[0].sum()}",
               fontsize=10, color=C["blueT"], va="center")
    ax_cm.text(2.15, 0.5, f"Σ={cm[1].sum()}",
               fontsize=10, color=C["blueT"], va="center")
    ax_cm.text(0.5, -0.22, f"Σ={cm[:, 0].sum()}",
               fontsize=10, color=C["blueT"], ha="center")
    ax_cm.text(1.5, -0.22, f"Σ={cm[:, 1].sum()}",
               fontsize=10, color=C["blueT"], ha="center")

    ax_cm.set_xlim(-0.05, 2.6)
    ax_cm.set_ylim(-0.45, 2.05)
    ax_cm.set_xticks([0.5, 1.5])
    ax_cm.set_yticks([0.5, 1.5])
    ax_cm.set_xticklabels(["Predicted +", "Predicted −"], fontsize=11)
    ax_cm.set_yticklabels(["Actual −", "Actual +"], fontsize=11)
    for s in ax_cm.spines.values():
        s.set_visible(False)
    ax_cm.tick_params(length=0)
    ax_cm.set_title("Confusion matrix (shared)",
                    fontsize=13, fontweight="bold", pad=12)

    ax_text.axis("off")

    # F1 block
    ax_text.text(0.02, 0.97, "F1-score", fontsize=16, fontweight="bold",
                 color=C["coralT"], transform=ax_text.transAxes)
    f1_items = [
        ("Precision = TP / (TP + FP)", "= 80 / 90 = 0.889"),
        ("Recall    = TP / (TP + FN)", "= 80 / 100 = 0.800"),
        ("F1        = 2·P·R / (P + R)", "= 2·0.889·0.800 / 1.689 = 0.842"),
    ]
    y = 0.87
    for label, value in f1_items:
        ax_text.text(0.02, y, label, fontsize=11.5, fontweight="bold",
                     color=C["coralT"], transform=ax_text.transAxes,
                     family="monospace")
        ax_text.text(0.04, y - 0.045, value, fontsize=10, color=C["grayT"],
                     transform=ax_text.transAxes, family="monospace")
        y -= 0.105

    # Separator
    ax_text.plot([0.02, 0.98], [0.50, 0.50], color=C["gray"], linewidth=1.2,
                 transform=ax_text.transAxes)

    # κ block
    ax_text.text(0.02, 0.45, "Cohen's κ", fontsize=16, fontweight="bold",
                 color=C["blueT"], transform=ax_text.transAxes)
    po = 0.85
    pe = 0.5
    kappa = (po - pe) / (1 - pe)
    kappa_items = [
        ("p_o (observed agreement)", "= (80+90) / 200 = 0.850"),
        ("p_e (expected by chance)", "= 0.50·0.45 + 0.50·0.55 = 0.500"),
        ("κ  =  (p_o − p_e) / (1 − p_e)",
         f"= (0.850 − 0.500) / (1 − 0.500) = {kappa:.3f}"),
    ]
    y = 0.35
    for label, value in kappa_items:
        ax_text.text(0.02, y, label, fontsize=11.5, fontweight="bold",
                     color=C["blueT"], transform=ax_text.transAxes,
                     family="monospace")
        ax_text.text(0.04, y - 0.045, value, fontsize=10, color=C["grayT"],
                     transform=ax_text.transAxes, family="monospace")
        y -= 0.105

    fig.suptitle("F1-score and Cohen's κ — derived from the same confusion matrix",
                 fontsize=15, fontweight="bold", y=1.0)
    return fig


def make_g() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11, 5.4))

    ax.plot([0, 1], [0.4, 0.4], color=C["grayT"], linewidth=2.5)
    for t in np.arange(0, 1.01, 0.1):
        ax.plot([t, t], [0.385, 0.415], color=C["grayT"], linewidth=1.5)
        ax.text(t, 0.34, f"{t:.1f}", ha="center", fontsize=10,
                color=C["grayT"])

    ax.plot([0.85, 0.85], [0.18, 0.78], color=C["red"],
            linestyle="--", linewidth=2.5)
    ax.text(0.85, 0.81, "H-4 threshold\nG = 0.85",
            ha="center", va="bottom", fontsize=11, fontweight="bold",
            color=C["red"])

    ax.annotate(
        "Baseline\nG = 0.82",
        xy=(0.82, 0.40), xytext=(0.65, 0.18),
        fontsize=11, fontweight="bold", color=C["coralT"], ha="center",
        arrowprops=dict(arrowstyle="-", color=C["coral"], lw=1.2),
    )
    ax.plot(0.82, 0.4, marker="v", markersize=18, color=C["coral"])

    ax.annotate(
        "Pipeline\nG = 0.89 ✓",
        xy=(0.89, 0.40), xytext=(0.96, 0.18),
        fontsize=11, fontweight="bold", color=C["tealT"], ha="center",
        arrowprops=dict(arrowstyle="-", color=C["teal"], lw=1.2),
    )
    ax.plot(0.89, 0.4, marker="v", markersize=18, color=C["teal"])

    ax.text(0.5, 0.95, "Generalization Ratio",
            ha="center", fontsize=18, fontweight="bold", color=C["grayT"])
    ax.text(0.5, 0.62, r"$G = \dfrac{F1_{external}}{F1_{train}}$",
            ha="center", fontsize=22, color=C["blueT"])
    ax.text(0.5, 0.51,
            "Pipeline transfers well across datasets when G ≥ 0.85.",
            ha="center", fontsize=11, style="italic", color=C["grayT"])

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0.05, 1.0)
    ax.axis("off")
    return fig


def make_alo() -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.4))

    yy, xx = np.mgrid[:100, :100]
    attention = np.exp(-((xx - 50) ** 2 + (yy - 50) ** 2) / (2 * 12 ** 2))

    lesion = np.zeros((100, 100))
    for cx, cy, r in [(42, 45, 6), (55, 52, 5), (52, 70, 5)]:
        lesion += ((xx - cx) ** 2 + (yy - cy) ** 2 < r ** 2).astype(float)
    lesion = (lesion > 0).astype(float)

    att_thresh = (attention > 0.5).astype(float)
    intersection = att_thresh * lesion
    lesion_outside = lesion * (1 - att_thresh)

    axes[0].imshow(attention, cmap="Reds", vmin=0, vmax=1)
    axes[0].set_title("Attention map  A\n(Grad-CAM, soft heatmap)",
                      fontsize=12, fontweight="bold")

    axes[1].imshow(lesion, cmap="Greens", vmin=0, vmax=1)
    axes[1].set_title("Lesion mask  L\n(ground-truth segmentation)",
                      fontsize=12, fontweight="bold")

    # composite panel: attention region (pink), lesion outside (green),
    # intersection (amber)
    rgb = np.ones((100, 100, 3))
    att_only = att_thresh * (1 - lesion)
    rgb[att_only.astype(bool)] = [0.97, 0.85, 0.85]
    rgb[lesion_outside.astype(bool)] = [0.55, 0.78, 0.55]
    rgb[intersection.astype(bool)] = [0.94, 0.62, 0.15]
    axes[2].imshow(rgb)

    inter_pixels = int(intersection.sum())
    lesion_pixels = int(lesion.sum())
    alo_val = inter_pixels / max(lesion_pixels, 1)
    axes[2].set_title(
        f"ALO = |A ∩ L| / |L| = {alo_val:.2f}",
        fontsize=12, fontweight="bold",
    )

    # legend for composite panel
    legend_handles = [
        patches.Patch(facecolor=[0.97, 0.85, 0.85],
                      edgecolor=C["grayT"], label="Attention only (no lesion)"),
        patches.Patch(facecolor=[0.55, 0.78, 0.55],
                      edgecolor=C["grayT"], label="Lesion outside attention"),
        patches.Patch(facecolor=[0.94, 0.62, 0.15],
                      edgecolor=C["grayT"], label="A ∩ L  (counted in ALO)"),
    ]
    axes[2].legend(
        handles=legend_handles, loc="upper center",
        bbox_to_anchor=(0.5, -0.02), ncol=1, fontsize=9,
        frameon=True, handlelength=1.5,
    )

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("ALO — Attention-Lesion Overlap",
                 fontsize=17, fontweight="bold", y=1.01)
    return fig


def main() -> None:
    print(f"Output directory: {OUT_DIR}")
    print("Generating metric-definition diagrams...")
    save(make_f1(), "def_f1")
    save(make_auc(), "def_auc")
    save(make_kappa(), "def_kappa")
    save(make_f1_kappa(), "def_f1_kappa")
    save(make_g(), "def_g")
    save(make_alo(), "def_alo")
    print("Done.")


if __name__ == "__main__":
    main()
