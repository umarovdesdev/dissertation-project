"""Split V5 preprocessing SVG into 8 separate stage cards and convert each to PNG.

Reads the source diagram, extracts each stage's <g transform="translate(...)"> group,
wraps it in a standalone SVG (with the original <defs>/styles), then renders to PNG via
headless Chrome --screenshot.

Output: 8 PNG files in defense/assets/preprocessing/stages/.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC_SVG = Path(r"E:/dissertation-project/demo/public/diagrams/03_preprocessing_stages_detailed.svg")
TMP_DIR = Path(r"E:/dissertation-project/defense/scripts/_tmp_preproc")
OUT_DIR = Path(r"E:/dissertation-project/defense/assets/preprocessing/stages")
CHROME = Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe")

# (stage_index, file_basename, x_origin, y_origin)
STAGES = [
    (0, "stage0_canonical_flip",       20,   70),
    (1, "stage1_od_fovea_rotation",   480,   70),
    (2, "stage2_fov_crop_resize",     940,   70),
    (3, "stage3_fov_mask",           1400,   70),
    (4, "stage4_flatfield",            20,  590),
    (5, "stage5_clahe",               480,  590),
    (6, "stage6_augmentation",        940,  590),
    (7, "stage7_normalize",          1400,  590),
]

PANEL_W, PANEL_H = 440, 500
PAD = 24
PAD_BOTTOM_EXTRA = 40  # extra room: Chrome window-size loses a few px to chrome
CARD_W = PANEL_W + 2 * PAD
CARD_H = PANEL_H + 2 * PAD + PAD_BOTTOM_EXTRA
RENDER_SCALE = 3  # PNG pixel scale factor for crisp output


def extract_block(text: str, marker: str) -> str:
    """Return the <g transform="translate(x, y)">…</g> block whose comment header
    contains `marker` (e.g. 'STAGE 0')."""
    # Find the section starting from the comment marker
    start = text.find(marker)
    if start == -1:
        raise ValueError(f"Marker not found: {marker}")
    g_start = text.find("<g ", start)
    # Walk to matching </g> (these blocks are flat — no nested <g>)
    g_end = text.find("</g>", g_start)
    if g_end == -1:
        raise ValueError(f"No </g> after marker: {marker}")
    return text[g_start:g_end + 4]


def extract_defs(text: str) -> str:
    m = re.search(r"<defs>.*?</defs>", text, flags=re.DOTALL)
    if not m:
        raise ValueError("No <defs> block found")
    return m.group(0)


def build_card_svg(defs: str, group_block: str, x_orig: int, y_orig: int) -> str:
    """Translate the panel's group so the panel sits at (PAD, PAD) inside the new SVG.

    The original transform placed the panel at (x_orig, y_orig) in the parent SVG.
    We need the panel at (PAD, PAD) in our card SVG, so the new transform is just
    (PAD, PAD) — the x_orig/y_orig args are kept for symmetry/debugging but unused.
    """
    del x_orig, y_orig
    repositioned = re.sub(
        r'transform="translate\([^)]*\)"',
        f'transform="translate({PAD}, {PAD})"',
        group_block,
        count=1,
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CARD_W} {CARD_H}" width="{CARD_W}" height="{CARD_H}">\n'
        f'  {defs}\n'
        f'  <rect width="{CARD_W}" height="{CARD_H}" fill="#ffffff"/>\n'
        f'  {repositioned}\n'
        f'</svg>\n'
    )


def render_to_png(svg_path: Path, png_path: Path) -> None:
    px_w = CARD_W * RENDER_SCALE
    px_h = CARD_H * RENDER_SCALE
    file_url = "file:///" + str(svg_path.resolve()).replace("\\", "/")
    # Each invocation needs an isolated user-data-dir; otherwise a second concurrent
    # (or quickly-relaunched) Chrome attaches to an existing instance and exits early
    # with an empty/blank PNG.
    with tempfile.TemporaryDirectory(prefix="chrome_svg_") as udd:
        cmd = [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={udd}",
            f"--force-device-scale-factor={RENDER_SCALE}",
            f"--window-size={CARD_W},{CARD_H}",
            f"--screenshot={png_path}",
            file_url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not png_path.exists() or png_path.stat().st_size < 4096:
        raise RuntimeError(
            f"Chrome render failed (rc={result.returncode}): {result.stderr or result.stdout}"
        )


def main() -> None:
    if not SRC_SVG.exists():
        sys.exit(f"Source SVG missing: {SRC_SVG}")
    if not CHROME.exists():
        sys.exit(f"Chrome not found at: {CHROME}")

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = SRC_SVG.read_text(encoding="utf-8")
    defs = extract_defs(raw)

    for idx, basename, x_orig, y_orig in STAGES:
        marker = f"STAGE {idx} "
        block = extract_block(raw, marker)
        card = build_card_svg(defs, block, x_orig, y_orig)
        svg_path = TMP_DIR / f"{basename}.svg"
        png_path = OUT_DIR / f"{basename}.png"
        svg_path.write_text(card, encoding="utf-8")
        render_to_png(svg_path, png_path)
        print(f"  [{idx}] {basename}.png  ({png_path.stat().st_size // 1024} KB)")

    print(f"\nDone. PNGs written to: {OUT_DIR}")
    # leave intermediate SVGs in place for inspection; uncomment to clean:
    # shutil.rmtree(TMP_DIR, ignore_errors=True)


if __name__ == "__main__":
    main()
