"""Generate slide 29 camera-alignment chart.

Compares camera brand distribution in:
  1. Central Asian ophthalmology clinics (36 clinics, central_asia.md)
     · with country-level breakdown and representative clinics
  2. Dissertation training datasets (8 datasets, cross_dataset_comparison.svg)

Output: defense/assets/datasets/29_cameras/cameras_alignment.png
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

C = {
    "blue": "#378ADD", "teal": "#1D9E75", "coral": "#D85A30",
    "purple": "#7F77DD", "amber": "#EF9F27", "gray": "#888780",
    "green": "#639922",
    "blueBg": "#E6F1FB", "tealBg": "#E1F5EE", "coralBg": "#FAECE7",
    "grayBg": "#F1EFE8",
    "blueT": "#0C447C", "tealT": "#085041", "coralT": "#712B13",
    "purpleT": "#3C3489", "grayT": "#444441",
}

BRAND_COLORS = {
    "Topcon": C["purple"],
    "Canon":  C["blue"],
    "Zeiss":  C["coral"],
    "Kowa":   C["teal"],
    "Other":  C["gray"],
}

# Aggregated from central_asia.md (rows 1–36, primary brand only)
CA_DATA = {"Topcon": 19, "Canon": 11, "Zeiss": 5, "Kowa": 0, "Other": 1}

DS_DATA = {"Canon": 4, "Topcon": 4, "Kowa": 2, "Zeiss": 1, "Other": 0}

# Per-country breakdown (re-counted from central_asia.md)
COUNTRY_DATA = {
    "Қазақстан":    {"Topcon": 14, "Canon": 6, "Zeiss": 3, "Other": 1},  # n = 24
    "Өзбекстан":    {"Topcon": 2,  "Canon": 2, "Zeiss": 1, "Other": 0},  # n = 5
    "Қырғызстан":   {"Topcon": 2,  "Canon": 1, "Zeiss": 0, "Other": 0},  # n = 3
    "Тәжікстан":    {"Topcon": 1,  "Canon": 1, "Zeiss": 0, "Other": 0},  # n = 2
    "Түрікменстан": {"Topcon": 0,  "Canon": 1, "Zeiss": 1, "Other": 0},  # n = 2
}

# Representative clinics per country
SAMPLE_CLINICS = {
    "Қазақстан":    "КазНИИ глазных болезней (Алматы, Астана) · Focus Eye Center · "
                    "Astana Vision (сеть) · Konovalov Eye Center",
    "Өзбекстан":    "Republican Specialized Eye Center (Ташкент) · Samarkand Eye Hospital",
    "Қырғызстан":   "Кыргызский НИИ глазных болезней (Бишкек) · Eye Clinic Bishkek",
    "Тәжікстан":    "National Eye Center · Vision Tajikistan Clinic (Душанбе)",
    "Түрікменстан": "International Eye Center · Ashgabat Eye Clinic (Ашхабад)",
}

OUT = (
    Path(__file__).resolve().parent.parent
    / "assets" / "datasets" / "29_cameras" / "cameras_alignment.png"
)


def make_donut(ax, data, title, center_total, center_label):
    items = [(k, v) for k, v in data.items() if v > 0]
    labels, values = zip(*items)
    colors = [BRAND_COLORS[k] for k in labels]

    wedges, _, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct=lambda p: f"{p:.0f}%" if p >= 3 else "",
        startangle=90, counterclock=False,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2.5),
        textprops=dict(fontsize=11.5, fontweight="bold", color=C["grayT"]),
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(11)
        at.set_fontweight("bold")

    ax.text(0, 0.08, str(center_total), ha="center", va="center",
            fontsize=26, fontweight="bold", color=C["grayT"])
    ax.text(0, -0.16, center_label, ha="center", va="center",
            fontsize=10, color=C["grayT"])

    ax.set_title(title, fontsize=12.5, fontweight="bold",
                 pad=10, color=C["grayT"])


def make_country_bars(ax):
    countries = list(COUNTRY_DATA.keys())
    n = len(countries)
    bar_h = 0.55

    for i, country in enumerate(countries):
        y = n - 1 - i
        brands = COUNTRY_DATA[country]
        x = 0
        for brand in ["Topcon", "Canon", "Zeiss", "Kowa", "Other"]:
            cnt = brands.get(brand, 0)
            if cnt > 0:
                ax.barh(y, cnt, left=x, height=bar_h,
                        color=BRAND_COLORS[brand],
                        edgecolor="white", linewidth=2)
                if cnt >= 2:
                    ax.text(x + cnt / 2, y, str(cnt),
                            ha="center", va="center",
                            color="white", fontsize=11, fontweight="bold")
                x += cnt

        total = sum(brands.values())
        ax.text(-0.5, y, country, ha="right", va="center",
                fontsize=12, fontweight="bold", color=C["grayT"])
        ax.text(total + 0.3, y, f"n = {total}",
                ha="left", va="center",
                fontsize=10, color=C["grayT"])
        ax.text(total + 2.6, y, SAMPLE_CLINICS[country],
                ha="left", va="center",
                fontsize=8.5, color=C["grayT"], style="italic")

    ax.set_xlim(-3.5, 30)
    ax.set_ylim(-0.6, n - 0.2)
    ax.axis("off")
    ax.set_title(
        "Елдер бойынша таралым және өкілдік клиникалар  (n = 36)",
        fontsize=12.5, fontweight="bold", color=C["grayT"], pad=8, loc="left",
    )


def main():
    fig = plt.figure(figsize=(15, 11.5))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 0.95, 0.32],
                          hspace=0.30, wspace=0.05)

    ax_ca = fig.add_subplot(gs[0, 0])
    ax_ds = fig.add_subplot(gs[0, 1])
    ax_geo = fig.add_subplot(gs[1, :])
    ax_msg = fig.add_subplot(gs[2, :])

    make_donut(ax_ca, CA_DATA,
               title="Орталық Азия клиникалары",
               center_total=sum(CA_DATA.values()),
               center_label="клиника")
    make_donut(ax_ds, DS_DATA,
               title="Оқыту датасеттері",
               center_total=sum(DS_DATA.values()),
               center_label="бренд-аталым")

    make_country_bars(ax_geo)

    ax_msg.axis("off")
    ax_msg.text(
        0.5, 0.78,
        "Topcon + Canon  =  83% Орталық Азия клиникаларында  ·  73% датасет аталымдарында",
        ha="center", fontsize=14, fontweight="bold", color="#1a1a2e",
        transform=ax_msg.transAxes,
    )
    ax_msg.text(
        0.5, 0.40,
        "Аймақтық клиникалық қолдану доменін оқыту таралымы жабады  →  "
        "құрылғы-индукцияланған domain shift минималды",
        ha="center", fontsize=11, color=C["grayT"], style="italic",
        transform=ax_msg.transAxes,
    )
    ax_msg.text(
        0.5, 0.05,
        "✓  Камералық сәйкестік аймақтық қолдану сценарийін растайды  (H-6 негіздемесі)",
        ha="center", fontsize=11.5, color=C["tealT"], fontweight="bold",
        transform=ax_msg.transAxes,
        bbox=dict(boxstyle="round,pad=0.4",
                  facecolor=C["tealBg"], edgecolor=C["teal"], linewidth=1.5),
    )

    fig.suptitle(
        "Камералардың таралуы:  Орталық Азия клиникалары  ↔  Оқыту датасеттері",
        fontsize=15.5, fontweight="bold", y=0.995, color="#1a1a2e",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
