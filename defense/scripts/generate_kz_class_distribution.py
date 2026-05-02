"""Generate Kazakh-language class distribution SVG with all 8 datasets.

Output: defense/assets/datasets/27_overview/12_dataset_class_distribution.svg

Modeled after demo/public/datasets/general/class_imbalance_comparison.svg
but with Kazakh title and annotations.
"""
from pathlib import Path

OUT = (
    Path(__file__).resolve().parent.parent
    / "assets" / "datasets" / "27_overview" / "12_dataset_class_distribution.svg"
)

# 5-class ICDR datasets: (name, n, DR0%, DR1%, DR2%, DR3%, DR4%, camera_label)
DATASETS_5CLASS = [
    ("EyePACS",     "35 126", 73.5,  6.9, 15.1,  2.5,  2.0, "Canon CR-1"),
    ("Messidor-2",  "1 744",  58.3, 15.5, 19.9,  4.3,  2.0, "Topcon TRC NW6"),
    ("DDR",         "12 522", 50.0,  5.0, 35.8,  1.9,  7.3, "Canon + Topcon"),
    ("APTOS 2019",  "3 662",  49.3, 10.1, 27.3,  5.3,  8.1, "Аралас камералар"),
    ("IDRiD",       "516",    32.6,  4.8, 32.6, 18.0, 12.0, "Kowa VX-10α"),
    ("Clinical",    "60",     20.0, 20.0, 20.0, 20.0, 20.0, "Алматы, ҚР"),
]

# DR-positive-only and binary datasets:
#   ODIR-5K: DR1, DR2, DR3, DR4 (no DR0)
#   RFMiD: binary [absent, present]
ODIR_DATA  = ("ODIR-5K", "1 818 көз", [30.2, 58.1, 8.9, 2.9], "Canon + Zeiss", "тек DR-positive")
RFMID_DATA = ("RFMiD",   "3 200",     [80.3, 19.8],            "Topcon + Kowa",  "тек бинарлы")

COLORS = {
    "DR0": "#2E7D32",  # green
    "DR1": "#F9A825",  # yellow
    "DR2": "#EF6C00",  # orange
    "DR3": "#D32F2F",  # red
    "DR4": "#6A1B9A",  # purple
}

BAR_X = 220
BAR_W_TOTAL = 500
BAR_H = 30


def pct_to_w(pct: float) -> float:
    return BAR_W_TOTAL * pct / 100.0


def make_5class_row(y: int, name: str, n: str, percents: list[float], cam: str) -> str:
    p0, p1, p2, p3, p4 = percents
    parts = []
    parts.append(f'<text x="210" y="{y + 12}" text-anchor="end" font-size="12" font-weight="600" fill="#1a1a2e">{name}</text>')
    parts.append(f'<text x="210" y="{y + 25}" text-anchor="end" font-size="9" fill="#999">n = {n}</text>')

    x = BAR_X
    for pct, cls, label_dark in [
        (p0, "DR0", False), (p1, "DR1", True),
        (p2, "DR2", False), (p3, "DR3", False), (p4, "DR4", False),
    ]:
        w = pct_to_w(pct)
        if w > 0:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" fill="{COLORS[cls]}"/>')
            if w >= 26:
                txt_color = "#444" if label_dark else "white"
                parts.append(
                    f'<text x="{x + w / 2}" y="{y + 20}" text-anchor="middle" '
                    f'font-size="10" fill="{txt_color}" font-weight="600">{int(round(pct))}%</text>'
                )
            x += w

    parts.append(f'<text x="760" y="{y + 18}" font-size="9" fill="#aaa" font-style="italic">{cam}</text>')
    return "\n  ".join(parts)


def make_other_row(y: int, name: str, n: str, percents: list[float],
                   cam: str, note: str, mode: str) -> str:
    parts = []
    parts.append(f'<text x="210" y="{y + 12}" text-anchor="end" font-size="12" font-weight="600" fill="#1a1a2e">{name}</text>')
    parts.append(f'<text x="210" y="{y + 25}" text-anchor="end" font-size="9" fill="#999">n = {n}</text>')

    x = BAR_X
    if mode == "no_dr0":
        # DR1, DR2, DR3, DR4 only
        for pct, cls in zip(percents, ["DR1", "DR2", "DR3", "DR4"]):
            w = pct_to_w(pct)
            if w > 0:
                parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" fill="{COLORS[cls]}"/>')
                if w >= 26:
                    txt_color = "#444" if cls == "DR1" else "white"
                    parts.append(
                        f'<text x="{x + w / 2}" y="{y + 20}" text-anchor="middle" '
                        f'font-size="10" fill="{txt_color}" font-weight="600">{int(round(pct))}%</text>'
                    )
                x += w
    elif mode == "binary":
        absent_pct, present_pct = percents
        w_abs = pct_to_w(absent_pct)
        w_pres = pct_to_w(present_pct)
        parts.append(f'<rect x="{x}" y="{y}" width="{w_abs}" height="{BAR_H}" fill="{COLORS["DR0"]}"/>')
        parts.append(f'<text x="{x + w_abs / 2}" y="{y + 20}" text-anchor="middle" '
                     f'font-size="10" fill="white" font-weight="600">{absent_pct:.1f}% жоқ</text>')
        x += w_abs
        parts.append(f'<rect x="{x}" y="{y}" width="{w_pres}" height="{BAR_H}" fill="{COLORS["DR3"]}"/>')
        parts.append(f'<text x="{x + w_pres / 2}" y="{y + 20}" text-anchor="middle" '
                     f'font-size="9" fill="white" font-weight="600">{present_pct:.1f}% бар</text>')

    parts.append(f'<text x="760" y="{y + 12}" font-size="9" fill="#aaa" font-style="italic">{cam}</text>')
    parts.append(f'<text x="760" y="{y + 24}" font-size="8" fill="#D85A30">{note}</text>')
    return "\n  ".join(parts)


def main():
    rows_5class = []
    y = 116
    for name, n, p0, p1, p2, p3, p4, cam in DATASETS_5CLASS:
        rows_5class.append(make_5class_row(y, name, n, [p0, p1, p2, p3, p4], cam))
        y += 50

    rows_other = []
    other_y = y + 22
    rows_other.append(make_other_row(
        other_y, ODIR_DATA[0], ODIR_DATA[1], ODIR_DATA[2],
        ODIR_DATA[3], ODIR_DATA[4], "no_dr0",
    ))
    other_y += 50
    rows_other.append(make_other_row(
        other_y, RFMID_DATA[0], RFMID_DATA[1], RFMID_DATA[2],
        RFMID_DATA[3], RFMID_DATA[4], "binary",
    ))
    other_y += 38
    sep_after_other = other_y

    rows_5class_block = "\n\n  ".join(rows_5class)
    rows_other_block = "\n\n  ".join(rows_other)

    sep_y_between = y + 4

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif">
  <rect width="960" height="720" fill="white"/>

  <!-- Title -->
  <text x="480" y="28" text-anchor="middle" font-size="17" font-weight="700" fill="#1a1a2e">Деректер жиынтықтарының класс бөлінісі (DR 0–4)</text>
  <text x="480" y="46" text-anchor="middle" font-size="11" fill="#999">DR деңгей таралымы (%) — стектік bar диаграммалары, 100% = толық бар ені</text>

  <!-- Legend -->
  <g transform="translate(195, 60)">
    <rect x="0"   y="0" width="12" height="12" rx="2" fill="{COLORS["DR0"]}"/>
    <text x="16"  y="10" font-size="10" fill="#444">DR 0 — DR жоқ</text>
    <rect x="115" y="0" width="12" height="12" rx="2" fill="{COLORS["DR1"]}"/>
    <text x="131" y="10" font-size="10" fill="#444">DR 1 — Жеңіл</text>
    <rect x="225" y="0" width="12" height="12" rx="2" fill="{COLORS["DR2"]}"/>
    <text x="241" y="10" font-size="10" fill="#444">DR 2 — Орташа</text>
    <rect x="345" y="0" width="12" height="12" rx="2" fill="{COLORS["DR3"]}"/>
    <text x="361" y="10" font-size="10" fill="#444">DR 3 — Ауыр</text>
    <rect x="445" y="0" width="12" height="12" rx="2" fill="{COLORS["DR4"]}"/>
    <text x="461" y="10" font-size="10" fill="#444">DR 4 — PDR</text>
  </g>

  <line x1="30" y1="84" x2="930" y2="84" stroke="#E0E0E0" stroke-width="1"/>

  <!-- 100% reference line -->
  <line x1="720" y1="92" x2="720" y2="{sep_y_between - 4}" stroke="#E0E0E0" stroke-width="0.5" stroke-dasharray="4,3"/>

  <!-- 5-class section header -->
  <text x="24" y="106" font-size="9" fill="#999" font-weight="700" letter-spacing="0.5">5-КЛАСС ICDR ЖІКТЕМЕСІ</text>

  {rows_5class_block}

  <!-- Separator between sections -->
  <line x1="220" y1="{sep_y_between}" x2="720" y2="{sep_y_between}" stroke="#E0E0E0" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- Other-taxonomy section header -->
  <text x="24" y="{sep_y_between + 18}" font-size="9" fill="#999" font-weight="700" letter-spacing="0.5">КІЛТ СӨЗ / БИНАРЛЫ ЖІКТЕМЕ</text>

  {rows_other_block}

  <!-- Bottom separator -->
  <line x1="30" y1="{sep_after_other}" x2="930" y2="{sep_after_other}" stroke="#E0E0E0" stroke-width="1"/>

  <!-- Annotations -->
  <text x="40" y="{sep_after_other + 22}" font-size="10" fill="#D32F2F" font-weight="600">Класс теңгерімсіздігі әмбебап, бірақ деңгейі әртүрлі</text>
  <text x="40" y="{sep_after_other + 38}" font-size="10" fill="#888">EyePACS: экстремалды теңгерімсіздік (73.5% DR 0) → Focal Loss қажет</text>
  <text x="40" y="{sep_after_other + 54}" font-size="10" fill="#888">DDR: биомодальді — DR 0 (50%) + DR 2 (36%); DR 3 ең сирек (1.9%)</text>
  <text x="40" y="{sep_after_other + 70}" font-size="10" fill="#888">IDRiD: ең теңгерімді 5-класс → класс бойынша бағалауға идеалды</text>

  <text x="500" y="{sep_after_other + 22}" font-size="10" fill="#1D9E75" font-weight="600">Clinical (KZ): жобалау бойынша толық теңгерімді</text>
  <text x="500" y="{sep_after_other + 38}" font-size="10" fill="#888">Класс бойынша 12 сурет, Grad-CAM бағалау үшін таңдалған</text>
  <text x="500" y="{sep_after_other + 54}" font-size="10" fill="#888">ODIR-5K: DR 0 жоқ — кілт сөз шығаруы тек DR-positive</text>
  <text x="500" y="{sep_after_other + 70}" font-size="10" fill="#888">RFMiD: бинарлы (тяжелік жоқ) — 4:1 қатынас (жоқ:бар)</text>

  <text x="480" y="{sep_after_other + 96}" text-anchor="middle" font-size="10" fill="#888" font-style="italic">Теңгерімсіздік үлгісі классификатор өнімділігіне тікелей әсер етеді — минорлы кластар (DR 1, DR 3) тұрақты түрде ең төмен класс бойынша F1 көрсетеді</text>
</svg>"""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
