"""Validate the OD/fovea detector against IDRiD ground-truth (TASK-fix #4).

EyePACS has no OD/fovea annotations, so Stage 1 detects OD/fovea via the
pre-trained, frozen learned heatmap detector (``src/preprocessing/od_fovea_detect
.detect_od_fovea`` → ``src/preprocessing/od_fovea_net``). That detector drives
(a) the rotation normalization, (b) the OD/fovea markers in the demo, and (c) the
fovea centre that polar CLAHE pivots on. IDRiD provides real ground-truth OD and
fovea centres, so this script quantifies the detector error directly and is the
in-repo reproduction of the standalone Phase-1 acceptance check.

Coordinate frame
----------------
``detect_od_fovea`` accepts the **full-resolution** image and FOV-crops
internally, returning coordinates back in **original-image pixels**. IDRiD
localization markups are likewise expressed in original-image pixels, and IDRiD
has no left/right filename encoding (no canonical flip). Predicted and GT centres
therefore share one frame and compare directly — no transform required.

Usage::

    python scripts/validate_od_fovea_idrid.py \
        --localization-root "E:/datasets/IDRiD/C. Localization" \
        --output-dir outputs/validation \
        --montage-n 12

Output:
    ``<output-dir>/od_fovea_idrid_metrics.json`` — OD + fovea error
    distributions (px and normalized), success rates, and the correlation of
    the detector ``confident`` flag with low error, for train + test splits.
    ``<output-dir>/od_fovea_idrid_montage.png`` — predicted (solid) vs GT
    (dashed) markers on a sample of images.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import pathlib
import sys

import cv2
import numpy as np

# Allow running from repo root without installing the package.
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from src.preprocessing.od_fovea_detect import detect_od_fovea

# Relative paths inside the "C. Localization" tree.
_OD_CSV = {
    "train": "2. Groundtruths/1. Optic Disc Center Location/"
             "a. IDRiD_OD_Center_Training Set_Markups.csv",
    "test": "2. Groundtruths/1. Optic Disc Center Location/"
            "b. IDRiD_OD_Center_Testing Set_Markups.csv",
}
_FOVEA_CSV = {
    "train": "2. Groundtruths/2. Fovea Center Location/"
             "IDRiD_Fovea_Center_Training Set_Markups.csv",
    "test": "2. Groundtruths/2. Fovea Center Location/"
            "IDRiD_Fovea_Center_Testing Set_Markups.csv",
}
_IMAGES_DIR = {
    "train": "1. Original Images/a. Training Set",
    "test": "1. Original Images/b. Testing Set",
}


def _parse_markup_csv(path: pathlib.Path) -> dict[str, tuple[float, float]]:
    """Parse an IDRiD localization markup CSV into ``{image_no: (x, y)}``.

    The files carry many trailing empty columns; only the first three fields
    (``Image No``, ``X- Coordinate``, ``Y - Coordinate``) are read. Rows whose
    first cell is not an ``IDRiD_*`` id (header, blank) are skipped.

    Args:
        path: Path to the markup CSV.

    Returns:
        Mapping from image id (e.g. ``"IDRiD_001"``) to ``(x, y)`` centre in
        original-image pixels.
    """
    out: dict[str, tuple[float, float]] = {}
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 3:
                continue
            name = row[0].strip()
            if not name.startswith("IDRiD_"):
                continue
            try:
                x, y = float(row[1]), float(row[2])
            except ValueError:
                continue
            out[name] = (x, y)
    return out


def _percentiles(values: list[float]) -> dict[str, float]:
    """Return median / mean / p90 / max summary of a list of errors."""
    if not values:
        return {"median": float("nan"), "mean": float("nan"),
                "p90": float("nan"), "max": float("nan"), "n": 0}
    arr = np.asarray(values, dtype=np.float64)
    return {
        "median": float(np.median(arr)),
        "mean": float(arr.mean()),
        "p90": float(np.percentile(arr, 90)),
        "max": float(arr.max()),
        "n": int(arr.size),
    }


def _evaluate_split(
    root: pathlib.Path,
    split: str,
    limit: int,
) -> tuple[dict, list[dict]]:
    """Run the detector over one IDRiD split and collect per-image errors.

    Args:
        root: ``C. Localization`` directory.
        split: ``"train"`` or ``"test"``.
        limit: Max images to process (0 = all). Useful for quick checks.

    Returns:
        ``(summary, records)`` where ``summary`` aggregates error statistics and
        ``records`` is a list of per-image dicts (for the montage + JSON).
    """
    od_gt = _parse_markup_csv(root / _OD_CSV[split])
    fovea_gt = _parse_markup_csv(root / _FOVEA_CSV[split])
    images_dir = root / _IMAGES_DIR[split]

    ids = sorted(set(od_gt) & set(fovea_gt))
    if limit:
        ids = ids[:limit]

    records: list[dict] = []
    for i, name in enumerate(ids):
        img_path = images_dir / f"{name}.jpg"
        img_bgr = cv2.imread(str(img_path))
        if img_bgr is None:
            continue
        image_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w = image_rgb.shape[:2]
        diag = math.hypot(w, h)

        res = detect_od_fovea(image_rgb)

        od_err = math.dist(res.od_center, od_gt[name])
        fv_err = math.dist(res.fovea_center, fovea_gt[name])
        od_r = max(float(res.od_radius), 1.0)

        records.append({
            "id": name, "split": split,
            "width": w, "height": h,
            "confident": bool(res.confident),
            "od_radius": float(res.od_radius),
            "od_pred": [float(res.od_center[0]), float(res.od_center[1])],
            "od_gt": [od_gt[name][0], od_gt[name][1]],
            "fovea_pred": [float(res.fovea_center[0]), float(res.fovea_center[1])],
            "fovea_gt": [fovea_gt[name][0], fovea_gt[name][1]],
            "od_err_px": od_err,
            "fovea_err_px": fv_err,
            "od_err_norm": od_err / diag,
            "fovea_err_norm": fv_err / diag,
            "od_err_radii": od_err / od_r,
            "fovea_err_radii": fv_err / od_r,
        })

        if (i + 1) % 25 == 0 or (i + 1) == len(ids):
            print(f"  [{split}] {i + 1}/{len(ids)} processed…", flush=True)

    summary = _summarize(records)
    return summary, records


def _summarize(records: list[dict]) -> dict:
    """Aggregate per-image records into error stats + success/flag analysis."""
    od_px = [r["od_err_px"] for r in records]
    fv_px = [r["fovea_err_px"] for r in records]
    od_norm = [r["od_err_norm"] for r in records]
    fv_norm = [r["fovea_err_norm"] for r in records]
    od_radii = [r["od_err_radii"] for r in records]
    fv_radii = [r["fovea_err_radii"] for r in records]

    def _success_rate(radii: list[float], thresh: float) -> float:
        if not radii:
            return float("nan")
        return float(np.mean([e < thresh for e in radii]))

    # Confident-flag vs error: does the flag gate bad detections?
    conf = [r for r in records if r["confident"]]
    nconf = [r for r in records if not r["confident"]]

    return {
        "n_images": len(records),
        "od": {
            "error_px": _percentiles(od_px),
            "error_norm_diag": _percentiles(od_norm),
            "error_od_radii": _percentiles(od_radii),
            "success_within_1_od_radius": _success_rate(od_radii, 1.0),
            "success_within_0_5_od_radius": _success_rate(od_radii, 0.5),
        },
        "fovea": {
            "error_px": _percentiles(fv_px),
            "error_norm_diag": _percentiles(fv_norm),
            "error_od_radii": _percentiles(fv_radii),
            "success_within_1_od_radius": _success_rate(fv_radii, 1.0),
            "success_within_2_od_radii": _success_rate(fv_radii, 2.0),
        },
        "confident_flag": {
            "n_confident": len(conf),
            "n_not_confident": len(nconf),
            "fraction_confident": (len(conf) / len(records)) if records else float("nan"),
            "od_err_px_confident": _percentiles([r["od_err_px"] for r in conf]),
            "od_err_px_not_confident": _percentiles([r["od_err_px"] for r in nconf]),
            "fovea_err_px_confident": _percentiles([r["fovea_err_px"] for r in conf]),
            "fovea_err_px_not_confident": _percentiles([r["fovea_err_px"] for r in nconf]),
        },
    }


def _make_montage(
    root: pathlib.Path,
    records: list[dict],
    n: int,
    cell: int = 320,
    cols: int = 4,
) -> np.ndarray | None:
    """Render predicted (solid) vs GT (dashed) markers on a sample of images.

    Args:
        root: ``C. Localization`` directory.
        records: Per-image records (any split).
        n: Number of sample images to draw.
        cell: Side length of each montage cell in pixels.
        cols: Cells per row.

    Returns:
        BGR uint8 montage image, or ``None`` if no images could be drawn.
    """
    if not records or n <= 0:
        return None
    rng = np.random.default_rng(42)
    pick = sorted(rng.choice(len(records), min(n, len(records)), replace=False))
    cells: list[np.ndarray] = []

    for idx in pick:
        r = records[idx]
        img_dir = root / _IMAGES_DIR[r["split"]]
        img = cv2.imread(str(img_dir / f"{r['id']}.jpg"))
        if img is None:
            continue
        h, w = img.shape[:2]
        scale = cell / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

        def _pt(p: list[float]) -> tuple[int, int]:
            return int(p[0] * scale), int(p[1] * scale)

        # Predicted: solid (teal OD, coral fovea). GT: filled cross markers.
        rad = max(int(r["od_radius"] * scale), 4)
        cv2.circle(img, _pt(r["od_pred"]), rad, (200, 200, 0), 2)       # OD pred (teal-ish, BGR)
        cv2.circle(img, _pt(r["fovea_pred"]), max(rad // 2, 3), (80, 80, 255), 2)  # fovea pred (coral)
        cv2.drawMarker(img, _pt(r["od_gt"]), (200, 200, 0), cv2.MARKER_CROSS, 18, 2)
        cv2.drawMarker(img, _pt(r["fovea_gt"]), (80, 80, 255), cv2.MARKER_CROSS, 18, 2)

        label = f"{r['id']} OD {r['od_err_px']:.0f}px fv {r['fovea_err_px']:.0f}px"
        cv2.putText(img, label, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (255, 255, 255), 1, cv2.LINE_AA)

        canvas = np.zeros((cell, cell, 3), dtype=np.uint8)
        canvas[:img.shape[0], :img.shape[1]] = img
        cells.append(canvas)

    if not cells:
        return None
    while len(cells) % cols != 0:
        cells.append(np.zeros((cell, cell, 3), dtype=np.uint8))
    rows = [np.hstack(cells[i:i + cols]) for i in range(0, len(cells), cols)]
    return np.vstack(rows)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the OD/fovea detector against IDRiD ground-truth.",
    )
    parser.add_argument(
        "--localization-root", type=pathlib.Path,
        default=pathlib.Path("E:/datasets/IDRiD/C. Localization"),
        help='Path to the IDRiD "C. Localization" directory.',
    )
    parser.add_argument("--output-dir", default="outputs/validation", type=pathlib.Path,
                        help="Directory for metrics JSON + montage PNG.")
    parser.add_argument("--splits", default="train,test",
                        help="Comma-separated splits to evaluate.")
    parser.add_argument("--limit", default=0, type=int,
                        help="Max images per split (0 = all). For quick checks.")
    parser.add_argument("--montage-n", default=12, type=int,
                        help="Sample images to draw in the montage (0 = skip).")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    root: pathlib.Path = args.localization_root
    if not root.exists():
        print(f"ERROR: localization root not found: {root}", file=sys.stderr)
        sys.exit(1)

    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    per_split: dict[str, dict] = {}
    all_records: list[dict] = []

    for split in splits:
        print(f"Evaluating IDRiD {split} split…")
        summary, records = _evaluate_split(root, split, args.limit)
        per_split[split] = summary
        all_records.extend(records)
        od = summary["od"]["error_px"]
        fv = summary["fovea"]["error_px"]
        print(f"  OD    median {od['median']:.0f}px  p90 {od['p90']:.0f}px")
        print(f"  fovea median {fv['median']:.0f}px  p90 {fv['p90']:.0f}px")
        print(f"  success@1R: OD {summary['od']['success_within_1_od_radius']:.2f}  "
              f"fovea {summary['fovea']['success_within_2_od_radii']:.2f} (2R)\n")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = args.output_dir / "od_fovea_idrid_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump({"per_split": per_split, "n_total": len(all_records)}, f, indent=2)
    print(f"Saved metrics -> {metrics_path}")

    montage = _make_montage(root, all_records, args.montage_n)
    if montage is not None:
        montage_path = args.output_dir / "od_fovea_idrid_montage.png"
        cv2.imwrite(str(montage_path), montage)
        print(f"Saved montage -> {montage_path}")


if __name__ == "__main__":
    main()
