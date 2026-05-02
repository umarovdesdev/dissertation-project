"""Fix slide 27 (cross-dataset SVG with Clinical) and slide 28 (matrix PNG).

  Slide 27: regenerate cross_dataset_comparison.svg with all 8 datasets (adds Clinical)
  Slide 28: replace experiments.png with a clean datasets × experiments matrix
"""
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt

C = {
    "blue": "#378ADD", "teal": "#1D9E75", "coral": "#D85A30",
    "purple": "#7F77DD", "amber": "#EF9F27", "gray": "#888780",
    "blueBg": "#E6F1FB", "tealBg": "#E1F5EE", "coralBg": "#FAECE7",
    "purpleBg": "#EEEDFE", "grayBg": "#F1EFE8",
    "blueT": "#0C447C", "tealT": "#085041", "coralT": "#712B13",
    "purpleT": "#3C3489", "grayT": "#444441",
}

ROOT = Path(__file__).resolve().parent.parent / "assets" / "datasets"


# ---------------------------------------------- 27_overview/cross_dataset.svg

PALETTE_SVG = {
    "blue":   ("#378ADD", "#E6F1FB", "#0C447C"),
    "teal":   ("#1D9E75", "#E1F5EE", "#085041"),
    "purple": ("#7F77DD", "#EEEDFE", "#3C3489"),
    "coral":  ("#D85A30", "#FAECE7", "#712B13"),
}

ROWS = [
    ("EyePACS",       "~35,126",   "Canon CR-1",       "3888×2592–5184×3456",
     "45°",  "US (California)",   "5-class ICDR",          "Training",    "blue"),
    ("APTOS 2019",    "3,662",     "Various (mixed)",  "Various",
     "Var.", "Indian (rural)",    "5-class ICDR",          "Transfer",    "blue"),
    ("IDRiD",         "516",       "Kowa VX-10α", "4288×2848",
     "50°", "Indian (Nanded)",   "5-class + masks",       "Clinical",    "teal"),
    ("Messidor-2",    "1,748",     "Topcon TRC NW6",   "1440×960–2240×1488",
     "45°", "French",            "Referable / Non-ref.",  "Degradation", "purple"),
    ("DDR",           "13,673",    "Canon, Topcon",    "Various",
     "Var.", "Chinese",           "6-class (excl. gr. 5)", "Domain",      "coral"),
    ("ODIR-5K",       "5,000 pts", "Canon, Zeiss",     "Various",
     "Var.", "Chinese (Beijing)", "Keyword → DR grade", "Domain",      "coral"),
    ("RFMiD",         "3,200",     "Topcon, Kowa",     "Various",
     "Var.", "Indian",            "Binary DR (0/1)",       "Domain",      "coral"),
    ("Clinical (KZ)", "60",        "Mixed (regional)", "Various",
     "45°", "Kazakh (Almaty)",   "5-class ICDR",          "Local val.", "teal"),
]


def regenerate_cross_dataset_svg():
    n = len(ROWS)
    rows_svg = []
    for i, row in enumerate(ROWS):
        ds, size, cam, res, fov, pop, tax, tier, color = row
        y = 84 + i * 36
        bg = "white" if i % 2 == 0 else "#FAFAFA"
        c_main, c_bg, c_text = PALETTE_SVG[color]
        rows_svg.append(f"""
  <!-- Row {i + 1}: {ds} -->
  <rect x="20" y="{y}" width="920" height="36" fill="{bg}"/>
  <rect x="24" y="{y + 4}" width="4" height="28" rx="2" fill="{c_main}"/>
  <text x="34"  y="{y + 23}" font-size="11" font-weight="600" fill="#1a1a2e">{ds}</text>
  <text x="130" y="{y + 23}" font-size="10" fill="#444">{size}</text>
  <text x="245" y="{y + 23}" font-size="10" fill="#444">{cam}</text>
  <text x="385" y="{y + 23}" font-size="10" fill="#444">{res}</text>
  <text x="520" y="{y + 23}" font-size="10" fill="#444">{fov}</text>
  <text x="560" y="{y + 23}" font-size="10" fill="#444">{pop}</text>
  <text x="660" y="{y + 23}" font-size="10" fill="#444">{tax}</text>
  <rect x="816" y="{y + 10}" width="80" height="18" rx="3" fill="{c_bg}"/>
  <text x="856" y="{y + 23}" text-anchor="middle" font-size="9" font-weight="600" fill="{c_text}">{tier}</text>""")

    rows_block = "".join(rows_svg)
    table_end = 84 + n * 36
    sep_y = table_end + 8
    foot_top = sep_y + 12
    total_h = foot_top + 60

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {total_h}" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif">
  <rect width="960" height="{total_h}" fill="white"/>

  <!-- Title -->
  <text x="480" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#1a1a2e">Cross-Dataset Comparison &#8212; 8 Active Datasets</text>
  <text x="480" y="44" text-anchor="middle" font-size="11" fill="#999">All datasets used in dissertation experiments (H-1 through H-7)</text>

  <!-- Table header -->
  <rect x="20" y="56" width="920" height="26" rx="4" fill="#F1EFE8"/>
  <text x="30"  y="74" font-size="10" font-weight="700" fill="#444">Dataset</text>
  <text x="130" y="74" font-size="10" font-weight="700" fill="#444">Size</text>
  <text x="245" y="74" font-size="10" font-weight="700" fill="#444">Camera</text>
  <text x="385" y="74" font-size="10" font-weight="700" fill="#444">Resolution</text>
  <text x="520" y="74" font-size="10" font-weight="700" fill="#444">FOV</text>
  <text x="560" y="74" font-size="10" font-weight="700" fill="#444">Population</text>
  <text x="660" y="74" font-size="10" font-weight="700" fill="#444">Taxonomy</text>
  <text x="856" y="74" text-anchor="middle" font-size="10" font-weight="700" fill="#444">Tier</text>
{rows_block}

  <!-- Bottom separator -->
  <line x1="20" y1="{sep_y}" x2="940" y2="{sep_y}" stroke="#E0E0E0" stroke-width="1"/>

  <!-- Footer: camera coverage -->
  <text x="30" y="{foot_top + 14}" font-size="10" font-weight="600" fill="#444">Camera coverage:</text>
  <rect x="130" y="{foot_top + 2}" width="50" height="18" rx="3" fill="#E6F1FB"/>
  <text x="155" y="{foot_top + 15}" text-anchor="middle" font-size="9" font-weight="500" fill="#0C447C">Canon</text>
  <rect x="186" y="{foot_top + 2}" width="52" height="18" rx="3" fill="#EEEDFE"/>
  <text x="212" y="{foot_top + 15}" text-anchor="middle" font-size="9" font-weight="500" fill="#3C3489">Topcon</text>
  <rect x="244" y="{foot_top + 2}" width="46" height="18" rx="3" fill="#E1F5EE"/>
  <text x="267" y="{foot_top + 15}" text-anchor="middle" font-size="9" font-weight="500" fill="#085041">Kowa</text>
  <rect x="296" y="{foot_top + 2}" width="46" height="18" rx="3" fill="#FAECE7"/>
  <text x="319" y="{foot_top + 15}" text-anchor="middle" font-size="9" font-weight="500" fill="#712B13">Zeiss</text>
  <text x="354" y="{foot_top + 15}" font-size="10" fill="#888">&#8212; 4 manufacturers across 8 datasets</text>

  <text x="30" y="{foot_top + 36}" font-size="10" fill="#888">Total labeled images: ~63,589  &#183;  Populations: US, Indian, French, Chinese, Kazakh.</text>
</svg>"""

    out = ROOT / "27_overview" / "cross_dataset_comparison.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Saved: {out}")


# -------------------------------------- 28_experiments/datasets_matrix.png

DATASETS = [
    ("EyePACS",       "~35 126"),
    ("APTOS 2019",    "3 662"),
    ("IDRiD",         "516"),
    ("Messidor-2",    "1 748"),
    ("DDR",           "13 673"),
    ("ODIR-5K",       "~5 000"),
    ("RFMiD",         "~3 200"),
    ("Clinical (KZ)", "60"),
]

# (experiment_label, hypothesis_tag, brief_description_KZ)
EXPS = [
    ("Exp 1", "H-1",        "Препроцессинг доминанттылығы"),
    ("Exp 2", "H-2",        "Компоненттер абляциясы"),
    ("Exp 3", "H-4",        "Кросс-датасет жалпылау"),
    ("Exp 4", "H-5",        "Түсіндірмелілік · ALO"),
    ("Exp 5", "H-7",        "Деградацияға төзімділік"),
    ("Exp 6", "H-6",        "Камералық домен ауысуы"),
    ("Exp 7", "small-data", "Кіші деректермен оқыту"),
]

# Indexed by experiment → dataset role.  T = Train / source, E = Eval / target.
MATRIX = {
    "Exp 1": {"EyePACS": "T"},
    "Exp 2": {"EyePACS": "T"},
    "Exp 3": {"EyePACS": "T", "APTOS 2019": "E"},
    "Exp 4": {"EyePACS": "T", "IDRiD": "E", "Clinical (KZ)": "E"},
    "Exp 5": {"EyePACS": "T", "IDRiD": "E", "Messidor-2": "E"},
    "Exp 6": {"EyePACS": "T", "DDR": "E", "ODIR-5K": "E", "RFMiD": "E"},
    "Exp 7": {"IDRiD": "T", "Clinical (KZ)": "E"},
}


def make_experiments_matrix() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(17, 7.5))

    n_exp = len(EXPS)
    n_ds = len(DATASETS)
    cell_w, cell_h = 1.45, 1.0

    for i, (exp, hyp, descr) in enumerate(EXPS):
        y = n_exp - 1 - i  # top-to-bottom
        exp_data = MATRIX.get(exp, {})

        for j, (ds, _) in enumerate(DATASETS):
            x = j * cell_w
            role = exp_data.get(ds, "")
            if role == "T":
                color, label, tc = C["blue"], "Train", "white"
            elif role == "E":
                color, label, tc = C["teal"], "Eval", "white"
            else:
                color, label, tc = "#F5F5F5", "", C["gray"]

            rect = patches.FancyBboxPatch(
                (x + 0.06, y * cell_h + 0.06),
                cell_w - 0.12, cell_h - 0.12,
                boxstyle="round,pad=0.0,rounding_size=0.06",
                facecolor=color, edgecolor="white", linewidth=2,
            )
            ax.add_patch(rect)
            if label:
                ax.text(x + cell_w / 2, y * cell_h + cell_h / 2, label,
                        ha="center", va="center",
                        color=tc, fontsize=11.5, fontweight="bold")

        # Left-side row label: Exp + hypothesis tag
        ax.text(-0.25, y * cell_h + cell_h / 2 + 0.12, exp,
                ha="right", va="center",
                fontsize=12, fontweight="bold", color=C["grayT"])
        ax.text(-0.25, y * cell_h + cell_h / 2 - 0.18, hyp,
                ha="right", va="center",
                fontsize=10, color=C["coralT"], fontweight="bold")

        # Right-side hypothesis description
        x_right = n_ds * cell_w + 0.35
        ax.text(x_right, y * cell_h + cell_h / 2, descr,
                ha="left", va="center",
                fontsize=11, color=C["grayT"], style="italic")

    # Top: dataset column headers (name + n)
    for j, (ds, n) in enumerate(DATASETS):
        x = j * cell_w + cell_w / 2
        ax.text(x, n_exp * cell_h + 0.55, ds,
                ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=C["grayT"])
        ax.text(x, n_exp * cell_h + 0.18, f"n = {n}",
                ha="center", va="bottom",
                fontsize=8.5, color=C["gray"])

    ax.set_xlim(-2.4, n_ds * cell_w + 6.5)
    ax.set_ylim(-0.9, n_exp * cell_h + 1.1)
    ax.set_aspect("equal")
    ax.axis("off")

    train_patch = patches.Patch(facecolor=C["blue"], edgecolor="white",
                                label="Train  (source)")
    eval_patch = patches.Patch(facecolor=C["teal"], edgecolor="white",
                               label="Eval  (target / zero-shot)")
    ax.legend(handles=[train_patch, eval_patch],
              loc="lower center", bbox_to_anchor=(0.42, -0.06),
              ncol=2, fontsize=11, frameon=False)

    fig.suptitle(
        "Эксперименттер бойынша деректер жиындары  ·  Datasets per experiment",
        fontsize=15, fontweight="bold", y=0.99, color="#1a1a2e",
    )
    return fig


def main():
    print("Slide 27 - regenerating cross-dataset SVG with Clinical row...")
    regenerate_cross_dataset_svg()

    print("Slide 28 - generating datasets x experiments matrix...")
    fig = make_experiments_matrix()
    out = ROOT / "28_experiments" / "datasets_matrix.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
