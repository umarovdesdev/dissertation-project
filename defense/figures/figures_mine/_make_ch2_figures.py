#!/usr/bin/env python3
"""Generate the four conceptual Chapter-2 diagrams that were logged as
"ASSET TO BE CREATED" (FIG-2.1, 2.3, 2.4, 2.5). Content follows the approved
drafts:
  FIG-2.1  §2.1.1  CLAHE lineage: HE -> AHE -> CLAHE intensity redistribution
  FIG-2.3  §2.5.1  Grad-CAM formulation (gradient-weighted feature maps + ReLU)
  FIG-2.4  §2.4.1  coupled thermal-optical laser-tissue model
  FIG-2.5  §2.6    image-quality metrics: CNR/VVI/entropy vs SSIM guard

Schematic, grayscale-print-friendly, serif font. Run: python _make_ch2_figures.py
"""
from __future__ import annotations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.linewidth": 0.8,
    "savefig.dpi": 200,
})

HERE = Path(__file__).resolve().parent
INK = "#1a1a1a"
GRAY = "#6b6b6b"
LIGHT = "#d9d9d9"
ACC = "#37618e"   # muted blue accent
ACC2 = "#8c4a3b"  # muted brick accent


def _box(ax, x, y, w, h, text, *, fc="white", ec=INK, fs=10, lw=1.2, style="round,pad=0.02"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=3, color=INK)


def _arrow(ax, p0, p1, *, color=INK, lw=1.6, ls="-", style="-|>", ms=12):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, zorder=1,
                                 shrinkA=2, shrinkB=2))


# ----------------------------------------------------------------------------- FIG 2.1
def fig_clahe_lineage(path: Path):
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.3))
    fig.subplots_adjust(left=0.04, right=0.985, top=0.82, bottom=0.26, wspace=0.28)
    bins = np.linspace(0, 1, 40)

    # Panel A — global HE
    a = axes[0]
    src = np.clip(rng.normal(0.42, 0.07, 6000), 0, 1)        # narrow, low-contrast
    a.hist(src, bins=bins, color=LIGHT, ec=GRAY, lw=0.4)
    cdf_x = np.linspace(0, 1, 200)
    cdf = np.clip((cdf_x - 0.30) / 0.24, 0, 1)                # S-like transfer
    a.plot(cdf_x, cdf * a.get_ylim()[1], color=ACC, lw=2.0, label="transfer (global CDF)")
    a.set_title("Histogram equalization\n(global)", fontsize=11, color=INK)
    a.text(0.5, -0.24, "One mapping — the global CDF —\napplied to every pixel.",
           transform=a.transAxes, ha="center", va="top", fontsize=8.6, color=GRAY)
    a.legend(loc="upper left", fontsize=7.5, frameon=False)

    # Panel B — adaptive HE (per tile)
    b = axes[1]
    field = np.add.outer(np.linspace(0.2, 0.7, 8), np.linspace(0.0, 0.3, 8))
    field += rng.normal(0, 0.05, field.shape)
    b.imshow(field, cmap="gray", extent=(0, 1, 0, 1), vmin=0, vmax=1, aspect="auto")
    for g in np.linspace(0, 1, 4):
        b.axvline(g, color=ACC, lw=1.0)
        b.axhline(g, color=ACC, lw=1.0)
    b.set_xticks([]); b.set_yticks([])
    b.set_title("Adaptive HE\n(per-tile)", fontsize=11, color=INK)
    b.text(0.5, -0.24, "A local CDF per tile — strong local\ncontrast, but amplifies noise in flat tiles.",
           transform=b.transAxes, ha="center", va="top", fontsize=9, color=GRAY)

    # Panel C — CLAHE (clip + redistribute)
    c = axes[2]
    counts, edges = np.histogram(src, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    clip = counts.max() * 0.45
    base = np.minimum(counts, clip)
    excess = (counts - base).sum()
    redist = excess / len(counts)
    c.bar(centers, base, width=(edges[1] - edges[0]) * 0.9, color=LIGHT, ec=GRAY, lw=0.4)
    c.bar(centers, np.full_like(base, redist, dtype=float), bottom=base,
          width=(edges[1] - edges[0]) * 0.9, color="none", ec=ACC2, lw=0.6, hatch="////")
    over = np.clip(counts - clip, 0, None)
    c.bar(centers, over, bottom=clip, width=(edges[1] - edges[0]) * 0.9,
          color="none", ec=ACC2, lw=0.0, alpha=0.25)
    c.axhline(clip, color=ACC2, lw=1.8, ls="--")
    c.text(0.97, clip, " clip limit", color=ACC2, fontsize=8.5, va="bottom", ha="right",
           transform=c.get_yaxis_transform())
    c.annotate("", xy=(0.12, clip * 0.5), xytext=(0.42, clip * 1.7),
               arrowprops=dict(arrowstyle="-|>", color=ACC2, lw=1.3))
    c.set_title("Contrast-limited AHE\n(CLAHE)", fontsize=11, color=INK)
    c.text(0.5, -0.24, "Clip limit bounds amplification; the\nclipped mass is redistributed uniformly.",
           transform=c.transAxes, ha="center", va="top", fontsize=9, color=GRAY)

    for ax in (a, c):
        ax.set_yticks([]); ax.set_xlabel("intensity", fontsize=9)
        ax.set_xlim(0, 1)
    # lineage arrows between panels
    for x in (0.345, 0.675):
        fig.add_artist(FancyArrowPatch((x, 0.52), (x + 0.012, 0.52),
                       transform=fig.transFigure, arrowstyle="-|>", mutation_scale=18, color=INK, lw=1.6))
    fig.suptitle("Intensity-redistribution lineage of contrast enhancement",
                 fontsize=12.5, y=0.965, color=INK)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)


# ----------------------------------------------------------------------------- FIG 2.3
def fig_gradcam(path: Path):
    rng = np.random.default_rng(3)
    fig = plt.figure(figsize=(11.5, 4.7))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")

    # input image
    img = np.clip(np.add.outer(np.linspace(0.1, 0.6, 32), np.zeros(32)) +
                  0.5 * np.exp(-((np.add.outer((np.arange(32) - 18) ** 2, (np.arange(32) - 14) ** 2)) / 60)) +
                  rng.normal(0, 0.04, (32, 32)), 0, 1)
    ax.imshow(img, cmap="gray", extent=(3, 17, 33, 49), aspect="auto", zorder=2)
    ax.add_patch(Rectangle((3, 33), 14, 16, fill=False, ec=INK, lw=1.2, zorder=3))
    ax.text(10, 31, "fundus input", ha="center", va="top", fontsize=9, color=INK)

    # conv stack
    for i, dx in enumerate((0, 1.6, 3.2)):
        ax.add_patch(Rectangle((24 + dx, 34 - i * 0 + dx * 0.0), 4.2, 14, fc="white", ec=INK, lw=1.1, zorder=2))
    ax.text(29.5, 31, "CNN conv layers", ha="center", va="top", fontsize=9, color=INK)

    # feature maps A^k
    for j, dy in enumerate((0, 1.3, 2.6)):
        ax.add_patch(Rectangle((39 + dy * 0.5, 35 - dy), 6, 6, fc="#eef2f7", ec=ACC, lw=1.1, zorder=2))
    ax.text(43, 31, r"feature maps $A^k$", ha="center", va="top", fontsize=9, color=INK)

    _arrow(ax, (17.3, 41), (23.8, 41))
    _arrow(ax, (31.6, 41), (38.6, 40))

    # class score + backprop gradient
    _box(ax, 55, 47, 18, 8, r"class score $y^{c}$", fc="white", ec=INK, fs=10.5)
    _arrow(ax, (46.5, 40.5), (55, 50), color=INK)            # forward to score
    _arrow(ax, (64, 47), (46, 38.5), color=ACC2, ls="--")    # backward gradient
    ax.text(56.5, 43.6, r"$\partial y^{c}/\partial A^{k}$", color=ACC2, fontsize=10, ha="left")

    # weights (GAP) box
    _box(ax, 52, 28, 26, 9,
         r"$\alpha_k^{c}=\frac{1}{Z}\sum_i\sum_j \frac{\partial y^{c}}{\partial A_{ij}^{k}}$",
         fc="#fbf3f0", ec=ACC2, fs=11)
    ax.text(65, 38.4, "global-average-pool gradients", ha="center", va="bottom", fontsize=8.5, color=GRAY)
    _arrow(ax, (45, 36), (52, 33), color=ACC2)

    # combination + ReLU
    _box(ax, 52, 13, 30, 10,
         r"$L^{c}_{\mathrm{GradCAM}}=\mathrm{ReLU}\left(\sum_k \alpha_k^{c} A^{k}\right)$",
         fc="#eef2f7", ec=ACC, fs=11.5)
    _arrow(ax, (65, 28), (65, 23), color=INK)

    # heatmap overlay output
    heat = np.exp(-((np.add.outer((np.arange(32) - 18) ** 2, (np.arange(32) - 14) ** 2)) / 70))
    ax.imshow(img, cmap="gray", extent=(86, 97, 8, 22), aspect="auto", zorder=2)
    ax.imshow(heat, cmap="jet", alpha=0.5, extent=(86, 97, 8, 22), aspect="auto", zorder=3)
    ax.add_patch(Rectangle((86, 8), 11, 14, fill=False, ec=INK, lw=1.2, zorder=4))
    ax.text(91.5, 6.5, "upsample → overlay", ha="center", va="top", fontsize=9, color=INK)
    _arrow(ax, (82, 18), (85.6, 16), color=INK)

    fig.suptitle("Grad-CAM: gradient-weighted combination of final convolutional feature maps",
                 fontsize=12.5, y=0.98, color=INK)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)


# ----------------------------------------------------------------------------- FIG 2.4
def fig_laser(path: Path):
    fig = plt.figure(figsize=(11.5, 5.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], left=0.06, right=0.975, top=0.86, bottom=0.10, wspace=0.16)
    ax = fig.add_subplot(gs[0, 0]); axr = fig.add_subplot(gs[0, 1]); axr.axis("off")

    # tissue layers (depth downwards)
    layers = [("Surface (cornea) — heats rapidly", 0.0, 0.16, "#cdcdcd"),
              ("Retina (NFL / photoreceptors)", 0.16, 0.42, "#dcdcdc"),
              ("RPE — strong absorber", 0.42, 0.55, "#9a9a9a"),
              ("Choroid — slow, stable rise", 0.55, 1.0, "#c4c4c4")]
    R = np.linspace(-1, 1, 240); Z = np.linspace(0, 1, 240)
    RR, ZZ = np.meshgrid(R, Z)
    a = 0.32
    beta = np.where(ZZ < 0.42, 1.4, np.where(ZZ < 0.55, 4.2, 2.2))    # absorption per layer
    cum = np.cumsum(beta, axis=0) * (Z[1] - Z[0])
    intensity = np.exp(-RR ** 2 / a ** 2) * np.exp(-cum)             # Gaussian * Beer-Lambert
    for name, z0, z1, col in layers:
        ax.add_patch(Rectangle((-1, z0), 2, z1 - z0, fc=col, ec="white", lw=1.0, zorder=1))
        ax.text(1.02, (z0 + z1) / 2, name, va="center", ha="left", fontsize=8.4, color=INK)
    ax.imshow(intensity, extent=(-1, 1, 1, 0), cmap="hot", alpha=0.85, aspect="auto", zorder=2, vmin=0, vmax=1)
    # Gaussian beam profile on top
    ax.plot(R, -0.02 - 0.16 * np.exp(-R ** 2 / a ** 2), color=ACC, lw=2.0, clip_on=False, zorder=5)
    ax.annotate(r"$I_0(r)=\frac{P}{\pi a^2}e^{-r^2/a^2}$", xy=(0, -0.13), xytext=(-0.95, -0.16),
                fontsize=10, color=ACC, annotation_clip=False)
    # heat-diffusion arrows
    for (x0, z0) in [(-0.35, 0.30), (0.35, 0.30), (0.0, 0.62)]:
        for ang in (0.0,):
            ax.add_patch(FancyArrowPatch((x0, z0), (x0, z0 + 0.14), arrowstyle="-|>",
                         mutation_scale=10, color="white", lw=1.4, zorder=4))
    ax.set_xlim(-1, 1); ax.set_ylim(1, -0.22)
    ax.set_xlabel("radial position  r", fontsize=9.5)
    ax.set_ylabel("depth  z", fontsize=9.5)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_title("Beam deposits energy; absorption decays it with depth", fontsize=10.5, color=INK)

    # equations / coupling on the right
    axr.set_xlim(0, 1); axr.set_ylim(0, 1)
    _box(axr, 0.04, 0.72, 0.92, 0.22,
         "Optical sub-model  (energy deposited where)\n\n"
         r"$I(r,z)=I_0(r)\,\exp\left(-\int_0^{z}\beta\,d\xi\right)$"
         "\nBeer–Lambert depth attenuation",
         fc="#eef2f7", ec=ACC, fs=10.5, style="round,pad=0.03")
    axr.add_patch(FancyArrowPatch((0.5, 0.71), (0.5, 0.63), arrowstyle="-|>", mutation_scale=16, color=INK, lw=1.6))
    axr.text(0.52, 0.67, "couples via absorbed power", fontsize=8.3, color=GRAY, va="center")
    _box(axr, 0.04, 0.36, 0.92, 0.26,
         "Optical → thermal coupling\n\n"
         r"$\Delta T=\frac{I_0\,e^{-\int\beta\,d\xi}\,\beta\,\Delta t}{C_o\,\sigma}$",
         fc="#fbf3f0", ec=ACC2, fs=10.5, style="round,pad=0.03")
    axr.add_patch(FancyArrowPatch((0.5, 0.35), (0.5, 0.29), arrowstyle="-|>", mutation_scale=16, color=INK, lw=1.6))
    _box(axr, 0.04, 0.02, 0.92, 0.26,
         "Thermal sub-model  (how heat diffuses)\n\n"
         r"$C_o\,\sigma\,\frac{\partial T}{\partial t}=\nabla\cdot(k\,\nabla T)$"
         "\nheat conduction, spatially varying $k$",
         fc="#eef2f7", ec=ACC, fs=10.5, style="round,pad=0.03")

    fig.suptitle("Coupled thermal–optical model of laser–tissue interaction (qualitative)",
                 fontsize=12.5, y=0.965, color=INK)
    fig.savefig(path); plt.close(fig)


# ----------------------------------------------------------------------------- FIG 2.5
def fig_quality_metrics(path: Path):
    fig = plt.figure(figsize=(10.5, 5.0))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off")

    # fulcrum + beam (balanced)
    ax.add_patch(Polygon([(50, 18), (45, 8), (55, 8)], closed=True, fc=GRAY, ec=INK, lw=1.0, zorder=2))
    ax.plot([18, 82], [40, 40], color=INK, lw=3, solid_capstyle="round", zorder=3)
    ax.plot([50, 50], [18, 40], color=INK, lw=3, zorder=3)
    for xc in (28, 72):                                   # hangers + pans
        ax.plot([xc, xc], [40, 30], color=GRAY, lw=1.2, zorder=2)
        ax.add_patch(FancyBboxPatch((xc - 12, 24), 24, 6, boxstyle="round,pad=0.2",
                     fc="#f3f3f3", ec=INK, lw=1.0, zorder=2))

    # left pan — enhancement measures
    ax.text(28, 27, "ENHANCEMENT  (↑ desired)", ha="center", va="center", fontsize=10, color=ACC, zorder=4)
    chips = [("CNR", "contrast-to-noise:\nvessel–background\ncontrast ÷ noise"),
             ("VVI", "vessel visibility:\nhow clearly the\nvasculature is seen"),
             ("Entropy", "information content:\nwider intensity-range\nutilisation")]
    for i, (name, desc) in enumerate(chips):
        x = 12 + i * 12
        _box(ax, x, 47, 11, 8, name, fc="#eef2f7", ec=ACC, fs=10)
        ax.text(x + 5.5, 45.5, desc, ha="center", va="top", fontsize=7.4, color=GRAY)
    _arrow(ax, (28, 46.5), (28, 30.5), color=ACC, lw=1.4)

    ax.text(72, 27, "STRUCTURAL FIDELITY  (guard)", ha="center", va="center", fontsize=10, color=ACC2, zorder=4)
    # right pan — SSIM guard
    _box(ax, 64, 47, 16, 8, "SSIM", fc="#fbf3f0", ec=ACC2, fs=11)
    ax.text(72, 45.5, "structural-similarity guard:\nconfirms enhancement preserved\nanatomy (no over-processing)",
            ha="center", va="top", fontsize=7.6, color=GRAY)
    _arrow(ax, (72, 46.5), (72, 30.5), color=ACC2, lw=1.4)

    ax.text(50, 4, "Three metrics reward enhancement; SSIM guards structural fidelity — together they are complementary.",
            ha="center", va="center", fontsize=9.2, color=INK)
    fig.suptitle("Image-quality metrics for preprocessing evaluation", fontsize=12.5, y=0.97, color=INK)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)


def main():
    out = {
        "fig2_1_clahe_lineage.png": fig_clahe_lineage,
        "fig2_3_gradcam.png": fig_gradcam,
        "fig2_4_laser_thermal_optical.png": fig_laser,
        "fig2_5_quality_metrics.png": fig_quality_metrics,
    }
    for name, fn in out.items():
        p = HERE / name
        fn(p)
        print(f"WROTE {name}")


if __name__ == "__main__":
    main()
