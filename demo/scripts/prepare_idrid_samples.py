"""
prepare_idrid_samples.py — Build a pool of IDRiD localization samples for the
Demo tab's "Random sample" button, carrying **ground-truth** optic-disc and
fovea centres.

Unlike EyePACS (no OD/fovea annotation — centres are detected algorithmically),
IDRiD ships pixel-accurate OD-centre and fovea-centre markups for its
Localization sub-challenge (516 images, IDRiD_NNN). Part B (Disease Grading) and
Part C (Localization) share the same image set, so we join the DR grade by id.

Because the markups are in the **original-image frame**, displaying the resized
original (not the analysis-space crop) lets the demo overlay GT markers by simple
scaling — no canonical flip / rotation / FOV-crop transform needed. That is what
makes the IDRiD markers align exactly in the demo.

This script:
  1. Reads the OD-centre + fovea-centre markups (train + test) and the Disease
     Grading labels.
  2. Samples up to `--per-grade` images per DR grade that have both centres.
  3. Resizes each image to a `--max-size` long side (scaling the centres to
     match) and writes it to demo/public/datasets/idrid/samples/dr{grade}/.
  4. Generates a display-frame FOV mask PNG per image (so the demo's mask toggle
     aligns with the shown image).
  5. Emits two manifests:
        - demo/public/datasets/idrid/samples/samples.json (canonical)
        - demo/src/tabs/_idridSamples.js (importable by Demo.js)

Run from the project root:

    python demo/scripts/prepare_idrid_samples.py [--per-grade 8] [--max-size 512]

Re-running is safe — the output directory is wiped and recreated.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit(
        "Pillow, OpenCV and NumPy are required.\n"
        "Install with: pip install Pillow opencv-python numpy"
    )

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR  = Path(__file__).resolve().parent
DEMO_DIR    = SCRIPT_DIR.parent                       # demo/
PROJECT_DIR = DEMO_DIR.parent                          # dissertation-project/
DRIVE_ROOT  = PROJECT_DIR.parent                       # E:\

IDRID_DIR = DRIVE_ROOT / "datasets" / "IDRiD"
LOC_DIR   = IDRID_DIR / "C. Localization"
GRADE_DIR = IDRID_DIR / "B. Disease Grading"

# (image dir, OD markup csv, fovea markup csv) per split.
SPLITS = {
    "train": (
        LOC_DIR / "1. Original Images" / "a. Training Set",
        LOC_DIR / "2. Groundtruths" / "1. Optic Disc Center Location"
                / "a. IDRiD_OD_Center_Training Set_Markups.csv",
        LOC_DIR / "2. Groundtruths" / "2. Fovea Center Location"
                / "IDRiD_Fovea_Center_Training Set_Markups.csv",
        GRADE_DIR / "2. Groundtruths" / "a. IDRiD_Disease Grading_Training Labels.csv",
    ),
    "test": (
        LOC_DIR / "1. Original Images" / "b. Testing Set",
        LOC_DIR / "2. Groundtruths" / "1. Optic Disc Center Location"
                / "b. IDRiD_OD_Center_Testing Set_Markups.csv",
        LOC_DIR / "2. Groundtruths" / "2. Fovea Center Location"
                / "IDRiD_Fovea_Center_Testing Set_Markups.csv",
        GRADE_DIR / "2. Groundtruths" / "b. IDRiD_Disease Grading_Testing Labels.csv",
    ),
}

OUT_PUBLIC_DIR = DEMO_DIR / "public" / "datasets" / "idrid" / "samples"
OUT_JS_PATH    = DEMO_DIR / "src" / "tabs" / "_idridSamples.js"
OUT_JSON_PATH  = OUT_PUBLIC_DIR / "samples.json"

# OD radius is not annotated in the localization markups; estimate it as a
# fraction of image width (optic-disc diameter ≈ image_width / 9 in fundus
# imaging → radius ≈ width / 18). Used only for the demo's disc circle.
OD_RADIUS_WIDTH_FRAC = 1.0 / 18.0


def _parse_centers(csv_path: Path) -> dict[str, tuple[float, float]]:
    """Parse an IDRiD centre-markup CSV → {image_id: (x, y)}.

    The markup files have a ``Image No, X- Coordinate, Y - Coordinate`` header
    followed by many trailing empty columns and blank rows; we read only the
    first three fields and skip rows without a valid ``IDRiD_*`` id + coords.
    """
    out: dict[str, tuple[float, float]] = {}
    with csv_path.open(newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # header
        for row in reader:
            if len(row) < 3:
                continue
            img_id, sx, sy = row[0].strip(), row[1].strip(), row[2].strip()
            if not img_id.startswith("IDRiD_") or not sx or not sy:
                continue
            try:
                out[img_id] = (float(sx), float(sy))
            except ValueError:
                continue
    return out


def _parse_grades(csv_path: Path) -> dict[str, int]:
    """Parse a Disease Grading labels CSV → {image_id: retinopathy_grade}."""
    out: dict[str, int] = {}
    if not csv_path.exists():
        return out
    with csv_path.open(newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # header
        for row in reader:
            if len(row) < 2:
                continue
            img_id, grade = row[0].strip(), row[1].strip()
            if not img_id.startswith("IDRiD_") or not grade:
                continue
            try:
                out[img_id] = int(grade)
            except ValueError:
                continue
    return out


def _gen_fov_mask(bgr: np.ndarray) -> np.ndarray:
    """Binary FOV mask (uint8 0/255) from a resized fundus image.

    Mirrors the threshold+morphology used elsewhere in the demo pipeline so the
    mask the user toggles matches the analysis FOV region.
    """
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return binary


def _collect(per_grade: int) -> dict[int, list[dict]]:
    """Gather candidate samples grouped by DR grade across both splits."""
    by_grade: dict[int, list[dict]] = defaultdict(list)
    for split, (img_dir, od_csv, fovea_csv, grade_csv) in SPLITS.items():
        if not img_dir.exists():
            print(f"  warn: missing {img_dir}")
            continue
        od = _parse_centers(od_csv)
        fovea = _parse_centers(fovea_csv)
        grades = _parse_grades(grade_csv)
        for img_path in sorted(img_dir.glob("IDRiD_*.jpg")):
            img_id = img_path.stem
            if img_id not in od or img_id not in fovea:
                continue
            grade = grades.get(img_id)
            if grade is None:
                continue
            by_grade[grade].append({
                "id": img_id, "split": split, "path": img_path,
                "od": od[img_id], "fovea": fovea[img_id], "grade": grade,
            })
    # Deterministic subset per grade.
    for grade in by_grade:
        by_grade[grade] = sorted(by_grade[grade], key=lambda d: d["id"])[:per_grade]
    return by_grade


def _process_one(entry: dict, max_side: int) -> dict:
    """Resize image + mask, scale centres, write files; return manifest row."""
    grade = entry["grade"]
    grade_dir = OUT_PUBLIC_DIR / f"dr{grade}"
    grade_dir.mkdir(parents=True, exist_ok=True)

    # Localization train/test reuse IDRiD_NNN ids → namespace by split so a
    # train and test image with the same id+grade don't overwrite each other.
    uid = f"{entry['id']}_{entry['split']}"

    with Image.open(entry["path"]) as im:
        im = im.convert("RGB")
        w0, h0 = im.size
        scale = min(1.0, max_side / max(w0, h0))
        new_w, new_h = int(round(w0 * scale)), int(round(h0 * scale))
        im_resized = im.resize((new_w, new_h), Image.LANCZOS) if scale < 1.0 else im
        img_rel = f"datasets/idrid/samples/dr{grade}/{uid}.jpg"
        im_resized.save(OUT_PUBLIC_DIR.parent.parent.parent / img_rel,
                        "JPEG", quality=85, optimize=True)

        # FOV mask in the same (resized) display frame.
        bgr = cv2.cvtColor(np.array(im_resized), cv2.COLOR_RGB2BGR)
        mask = _gen_fov_mask(bgr)
        mask_rel = f"datasets/idrid/samples/dr{grade}/{uid}_mask.png"
        cv2.imwrite(str(OUT_PUBLIC_DIR.parent.parent.parent / mask_rel), mask)

    odx, ody = entry["od"][0] * scale, entry["od"][1] * scale
    fvx, fvy = entry["fovea"][0] * scale, entry["fovea"][1] * scale
    od_radius = (w0 * scale) * OD_RADIUS_WIDTH_FRAC

    return {
        "id": uid,
        "grade": grade,
        "split": entry["split"],
        "image": img_rel,
        "mask": mask_rel,
        "width": new_w,
        "height": new_h,
        "od_center": [round(odx, 1), round(ody, 1)],
        "fovea_center": [round(fvx, 1), round(fvy, 1)],
        "od_radius": round(od_radius, 1),
    }


def _write_js(entries: list[dict]) -> None:
    OUT_JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "// Auto-generated by demo/scripts/prepare_idrid_samples.py.\n"
        "// Edit the script and re-run; do not modify this file by hand.\n"
        "// Source: IDRiD (CC-BY-4.0) — Localization sub-challenge.\n"
        "// Each entry carries GROUND-TRUTH od_center / fovea_center (display-frame\n"
        "// pixels) so the demo overlays real markers, not detector estimates.\n"
        f"// {len(entries)} samples.\n\n"
    )
    body = "export const IDRID_SAMPLES = " + json.dumps(entries, indent=2) + ";\n"
    OUT_JS_PATH.write_text(header + body, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--per-grade", type=int, default=8,
                   help="Max samples per DR grade (default: 8)")
    p.add_argument("--max-size", type=int, default=512,
                   help="Max image side in pixels (default: 512)")
    args = p.parse_args()

    if not LOC_DIR.exists():
        sys.exit(f"IDRiD Localization dir not found: {LOC_DIR}")

    print("Collecting IDRiD localization samples with OD+fovea GT...")
    by_grade = _collect(args.per_grade)
    total = sum(len(v) for v in by_grade.values())
    if total == 0:
        sys.exit("No samples collected — check IDRiD paths/markups.")

    if OUT_PUBLIC_DIR.exists():
        shutil.rmtree(OUT_PUBLIC_DIR)
    OUT_PUBLIC_DIR.mkdir(parents=True)

    manifest: list[dict] = []
    for grade in sorted(by_grade):
        for entry in by_grade[grade]:
            try:
                manifest.append(_process_one(entry, args.max_size))
                print(f"  ok {entry['id']} dr{grade} ({entry['split']})")
            except Exception as exc:  # pragma: no cover
                print(f"  skip {entry['id']}: {exc}")

    OUT_JSON_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _write_js(manifest)

    print(f"\nDone. {len(manifest)} samples.")
    print(f"  JSON: {OUT_JSON_PATH}")
    print(f"  JS:   {OUT_JS_PATH}")
    print(f"  Images: {OUT_PUBLIC_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
