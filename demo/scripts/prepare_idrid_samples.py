"""
prepare_idrid_samples.py — Build a pool of IDRiD localization **patients** (a
left + right eye each) for the Demo tab's "Random sample" button, carrying
ground-truth optic-disc and fovea centres.

IDRiD is monocular (one image per record) and ships pixel-accurate OD-centre and
fovea-centre markups for its Localization sub-challenge. We:
  * derive each image's true laterality from anatomy — the fovea is temporal to
    the disc, so ``fovea_x > od_x`` ⇒ LEFT eye (OS), else RIGHT eye (OD);
  * pair one left-eye image with one right-eye image of the same DR grade into a
    synthetic bilateral "patient", so the demo fills BOTH eye slots.

Patient numbering is sequential across grades (4 patients per grade):
    dr0 → p01–p04, dr1 → p05–p08, dr2 → p09–p12, dr3 → p13–p16, dr4 → p17–p20
→ 20 patients, 40 images.

Each saved file is named ``IDRiD_p{NN}_{L|R}_{id}_{split}`` where NN is the
patient number, L/R the eye orientation, id the original IDRiD number, and split
train/test.

Because the markups are in the **original-image frame**, displaying the resized
original (not the analysis-space crop) lets the demo overlay GT markers by simple
scaling — no canonical flip / rotation / FOV-crop transform needed.

This script writes images + a display-frame FOV mask per eye, plus two manifests:
    - demo/public/datasets/idrid/samples/patients.json (canonical)
    - demo/src/tabs/_idridSamples.js (importable by Demo.js — IDRID_PATIENTS)

Run from the project root:

    python demo/scripts/prepare_idrid_samples.py [--per-grade 4] [--max-size 512]

Re-running is safe — the output directory is wiped and recreated.
"""

from __future__ import annotations

import argparse
import csv
import json
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

# (image dir, OD markup csv, fovea markup csv, grade labels csv) per split.
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
OUT_JSON_PATH  = OUT_PUBLIC_DIR / "patients.json"
OUT_LOOKUP_PATH = DEMO_DIR / "src" / "tabs" / "_idridGtLookup.js"
PUBLIC_ROOT    = DEMO_DIR / "public"

# OD radius is not annotated in the localization markups; estimate it as a
# fraction of image width (optic-disc diameter ≈ image_width / 9 → radius ≈
# width / 18). Used only for the demo's disc circle.
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
    """Binary FOV mask (uint8 0/255) from a resized fundus image."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return binary


def _collect_sides(per_grade: int) -> dict[int, dict[str, list[dict]]]:
    """Gather candidates grouped by ``grade → side`` (truncated to per_grade).

    Side is derived from anatomy (fovea temporal to the disc). Candidates are
    sorted by (id, split) for deterministic, reproducible selection.
    """
    by_grade: dict[int, dict[str, list[dict]]] = defaultdict(
        lambda: {"left": [], "right": []}
    )
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
            side = "left" if fovea[img_id][0] > od[img_id][0] else "right"
            by_grade[grade][side].append({
                "id": img_id, "split": split, "path": img_path,
                "od": od[img_id], "fovea": fovea[img_id], "grade": grade,
            })
    for grade in by_grade:
        for side in ("left", "right"):
            by_grade[grade][side] = sorted(
                by_grade[grade][side], key=lambda d: (d["id"], d["split"])
            )[:per_grade]
    return by_grade


def _process_eye(entry: dict, side_label: str, patient_no: int, max_side: int) -> dict:
    """Resize image + mask, scale centres, write files; return an eye manifest row.

    Args:
        entry: candidate dict from :func:`_collect_sides`.
        side_label: ``"L"`` or ``"R"`` (eye orientation in the filename).
        patient_no: sequential patient number (1-based).
        max_side: max image side in pixels.
    """
    grade = entry["grade"]
    grade_dir = OUT_PUBLIC_DIR / f"dr{grade}"
    grade_dir.mkdir(parents=True, exist_ok=True)

    num = entry["id"].replace("IDRiD_", "")  # e.g. "029"
    uid = f"IDRiD_p{patient_no:02d}_{side_label}_{num}_{entry['split']}"

    with Image.open(entry["path"]) as im:
        im = im.convert("RGB")
        w0, h0 = im.size
        scale = min(1.0, max_side / max(w0, h0))
        new_w, new_h = int(round(w0 * scale)), int(round(h0 * scale))
        im_resized = im.resize((new_w, new_h), Image.LANCZOS) if scale < 1.0 else im
        img_rel = f"datasets/idrid/samples/dr{grade}/{uid}.jpg"
        im_resized.save(PUBLIC_ROOT / img_rel, "JPEG", quality=85, optimize=True)

        bgr = cv2.cvtColor(np.array(im_resized), cv2.COLOR_RGB2BGR)
        mask = _gen_fov_mask(bgr)
        mask_rel = f"datasets/idrid/samples/dr{grade}/{uid}_mask.png"
        cv2.imwrite(str(PUBLIC_ROOT / mask_rel), mask)

    odx, ody = entry["od"][0] * scale, entry["od"][1] * scale
    fvx, fvy = entry["fovea"][0] * scale, entry["fovea"][1] * scale
    od_radius = (w0 * scale) * OD_RADIUS_WIDTH_FRAC

    return {
        "id": uid,
        "orig_id": entry["id"],
        "split": entry["split"],
        "side": "left" if side_label == "L" else "right",
        "image": img_rel,
        "mask": mask_rel,
        "width": new_w,
        "height": new_h,
        "od_center": [round(odx, 1), round(ody, 1)],
        "fovea_center": [round(fvx, 1), round(fvy, 1)],
        "od_radius": round(od_radius, 1),
    }


def _write_js(patients: list[dict]) -> None:
    OUT_JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "// Auto-generated by demo/scripts/prepare_idrid_samples.py.\n"
        "// Edit the script and re-run; do not modify this file by hand.\n"
        "// Source: IDRiD (CC-BY-4.0) — Localization sub-challenge.\n"
        "// Synthetic bilateral patients (one left + one right eye, same grade).\n"
        "// Each eye carries GROUND-TRUTH od_center / fovea_center (display-frame\n"
        "// pixels) so the demo overlays real markers, not detector estimates.\n"
        f"// {len(patients)} patients ({len(patients) * 2} images).\n\n"
    )
    body = "export const IDRID_PATIENTS = " + json.dumps(patients, indent=2) + ";\n"
    OUT_JS_PATH.write_text(header + body, encoding="utf-8")


def _write_gt_lookup() -> int:
    """Write `_idridGtLookup.js` for matching MANUAL uploads by filename.

    Covers the Localization **training set** (3-digit ids ``IDRiD_001``..) with
    OD + fovea centres in ORIGINAL-image pixels. Only the training split is
    bundled: train and test reuse ids, and a bare filename can't disambiguate
    them, so the demo instructs users to upload from the training-set folder.

    Returns the number of entries written.
    """
    img_dir, od_csv, fovea_csv, grade_csv = SPLITS["train"]
    od = _parse_centers(od_csv)
    fovea = _parse_centers(fovea_csv)
    lookup: dict[str, dict] = {}
    for img_id in sorted(od):
        if img_id in fovea:
            lookup[img_id] = {
                "od": [round(od[img_id][0], 1), round(od[img_id][1], 1)],
                "fovea": [round(fovea[img_id][0], 1), round(fovea[img_id][1], 1)],
            }
    header = (
        "// Auto-generated by demo/scripts/prepare_idrid_samples.py.\n"
        "// Edit the script and re-run; do not modify this file by hand.\n"
        "// Source: IDRiD (CC-BY-4.0) — Localization sub-challenge, TRAINING set.\n"
        "// Maps filename id (IDRiD_NNN) → ground-truth OD + fovea centres in\n"
        "// ORIGINAL-image pixels, for matching MANUAL uploads by filename.\n"
        f"// {len(lookup)} entries.\n\n"
    )
    body = "export const IDRID_GT = " + json.dumps(lookup, indent=0) + ";\n"
    OUT_LOOKUP_PATH.write_text(header + body, encoding="utf-8")
    return len(lookup)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--per-grade", type=int, default=4,
                   help="Patients per DR grade (each = L+R eye). Default: 4")
    p.add_argument("--max-size", type=int, default=512,
                   help="Max image side in pixels (default: 512)")
    args = p.parse_args()

    if not LOC_DIR.exists():
        sys.exit(f"IDRiD Localization dir not found: {LOC_DIR}")

    print("Collecting IDRiD localization samples (by grade x side)...")
    by_grade = _collect_sides(args.per_grade)

    # Clean stale files. We unlink files rather than rmtree the tree: on Windows
    # a directory handle held by an indexer/watcher blocks rmdir but not file
    # creation, so reusing the dirs is robust. Stale files are removed where the
    # OS allows; the run then writes the canonical set.
    if OUT_PUBLIC_DIR.exists():
        for f in OUT_PUBLIC_DIR.rglob("*"):
            if f.is_file():
                try:
                    f.unlink()
                except OSError:
                    pass
    OUT_PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    patients: list[dict] = []
    for grade in sorted(by_grade):
        lefts = by_grade[grade]["left"]
        rights = by_grade[grade]["right"]
        n = min(len(lefts), len(rights), args.per_grade)
        if n < args.per_grade:
            print(f"  warn: grade {grade} only has {n} L+R pairs "
                  f"(L={len(lefts)}, R={len(rights)})")
        for i in range(n):
            patient_no = grade * args.per_grade + i + 1
            left_eye = _process_eye(lefts[i], "L", patient_no, args.max_size)
            right_eye = _process_eye(rights[i], "R", patient_no, args.max_size)
            patients.append({
                "patient": f"p{patient_no:02d}",
                "grade": grade,
                "left": left_eye,
                "right": right_eye,
            })
            print(f"  ok p{patient_no:02d} dr{grade}  "
                  f"L={left_eye['id']}  R={right_eye['id']}")

    if not patients:
        sys.exit("No patients built — check IDRiD paths/markups.")

    OUT_JSON_PATH.write_text(json.dumps(patients, indent=2), encoding="utf-8")
    _write_js(patients)
    n_lookup = _write_gt_lookup()

    print(f"\nDone. {len(patients)} patients ({len(patients) * 2} images).")
    print(f"  JSON:   {OUT_JSON_PATH}")
    print(f"  JS:     {OUT_JS_PATH}")
    print(f"  Lookup: {OUT_LOOKUP_PATH} ({n_lookup} upload-matchable ids)")
    print(f"  Images: {OUT_PUBLIC_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
