"""Evaluate the detector on IDRiD and emit a monorepo-compatible metrics JSON.

The JSON has the **same shape** as the monorepo's
``outputs/validation/od_fovea_idrid_metrics.json`` (per-split ``od``/``fovea``
blocks with ``error_px`` {median,mean,p90,max,n}, ``error_od_radii``,
``success_within_1_od_radius``, ``success_within_2_od_radii``), plus a
``confidence_vs_error`` block giving the Spearman correlation between
``sigma_eff`` (heatmap spread) and the actual Euclidean error — the proof that
confidence tracks error (brief §7, §9).

Acceptance numbers (brief §9) are TEST-split only; this script reports per
split so the caller reads the test block.

Also renders ``montage.png`` (predicted solid markers vs GT crosses).

Requires torch + the IDRiD dataset.

Usage::

    python -m src.eval --config configs/default.yaml --split test
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib

import cv2
import numpy as np

from .data import load_split
from .infer import detect_od_fovea
from .utils import load_config


def _percentiles(values: list[float]) -> dict:
    """Median / mean / p90 / max / n summary of a list of errors."""
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


def _spearman(a: list[float], b: list[float]) -> dict:
    """Spearman rank correlation between two equal-length sequences.

    Computed via Pearson on ranks (no scipy dependency).

    Args:
        a: First sequence.
        b: Second sequence.

    Returns:
        Dict with ``rho`` and ``n`` (``rho`` is NaN for n < 3).
    """
    n = len(a)
    if n < 3:
        return {"rho": float("nan"), "n": n}
    ra = np.argsort(np.argsort(np.asarray(a, dtype=np.float64)))
    rb = np.argsort(np.argsort(np.asarray(b, dtype=np.float64)))
    ra = ra - ra.mean()
    rb = rb - rb.mean()
    denom = math.sqrt(float((ra ** 2).sum()) * float((rb ** 2).sum()))
    rho = float((ra * rb).sum() / denom) if denom > 0 else float("nan")
    return {"rho": rho, "n": n}


def evaluate_split(
    root: pathlib.Path,
    split: str,
    config_path: pathlib.Path,
    weights_path: pathlib.Path | None,
    limit: int = 0,
) -> tuple[dict, list[dict]]:
    """Run the detector over one IDRiD split and aggregate metrics.

    Args:
        root: ``C. Localization`` directory.
        split: ``"train"`` or ``"test"``.
        config_path: YAML config path.
        weights_path: Optional weights override.
        limit: Max images (0 = all).

    Returns:
        ``(summary, records)``.
    """
    samples = load_split(root, split)
    if limit:
        samples = samples[:limit]

    records: list[dict] = []
    for i, s in enumerate(samples):
        img_bgr = cv2.imread(str(s.image_path))
        if img_bgr is None:
            continue
        image_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w = image_rgb.shape[:2]
        diag = math.hypot(w, h)

        res = detect_od_fovea(image_rgb, config_path=config_path,
                              weights_path=weights_path, return_heatmaps=False)
        od_err = math.dist(res.od_center, s.od_xy)
        fv_err = math.dist(res.fovea_center, s.fovea_xy)
        od_r = max(float(res.od_radius), 1.0)
        records.append({
            "id": s.image_id, "split": split, "width": w, "height": h,
            "od_pred": list(res.od_center), "od_gt": list(s.od_xy),
            "fovea_pred": list(res.fovea_center), "fovea_gt": list(s.fovea_xy),
            "od_radius": float(res.od_radius),
            "od_err_px": od_err, "fovea_err_px": fv_err,
            "od_err_norm": od_err / diag, "fovea_err_norm": fv_err / diag,
            "od_err_radii": od_err / od_r, "fovea_err_radii": fv_err / od_r,
            "od_confidence": res.od_confidence,
            "fovea_confidence": res.fovea_confidence,
            "confident": bool(res.confident),
            # sigma_eff proxy: lower confidence == higher spread.
            "od_sigma_proxy": 1.0 - res.od_confidence,
            "fovea_sigma_proxy": 1.0 - res.fovea_confidence,
        })
        if (i + 1) % 25 == 0 or (i + 1) == len(samples):
            print(f"  [{split}] {i + 1}/{len(samples)}", flush=True)

    summary = _summarize(records)
    return summary, records


def _summarize(records: list[dict]) -> dict:
    """Aggregate per-image records into the monorepo-shaped summary."""
    def col(name: str) -> list[float]:
        return [r[name] for r in records]

    def success(radii: list[float], thresh: float) -> float:
        if not radii:
            return float("nan")
        return float(np.mean([e < thresh for e in radii]))

    od_radii = col("od_err_radii")
    fv_radii = col("fovea_err_radii")
    return {
        "n_images": len(records),
        "od": {
            "error_px": _percentiles(col("od_err_px")),
            "error_norm_diag": _percentiles(col("od_err_norm")),
            "error_od_radii": _percentiles(od_radii),
            "success_within_1_od_radius": success(od_radii, 1.0),
            "success_within_0_5_od_radius": success(od_radii, 0.5),
        },
        "fovea": {
            "error_px": _percentiles(col("fovea_err_px")),
            "error_norm_diag": _percentiles(col("fovea_err_norm")),
            "error_od_radii": _percentiles(fv_radii),
            "success_within_1_od_radius": success(fv_radii, 1.0),
            "success_within_2_od_radii": success(fv_radii, 2.0),
        },
        "confidence_vs_error": {
            "od_spearman_sigma_vs_err": _spearman(
                col("od_sigma_proxy"), col("od_err_px")),
            "fovea_spearman_sigma_vs_err": _spearman(
                col("fovea_sigma_proxy"), col("fovea_err_px")),
        },
    }


def make_montage(records: list[dict], samples_by_id: dict, n: int,
                 cell: int = 320, cols: int = 4) -> np.ndarray | None:
    """Render predicted (solid) vs GT (cross) markers on a sample.

    Args:
        records: Per-image records.
        samples_by_id: ``{image_id: Sample}`` for image paths.
        n: Number of sample cells.
        cell: Cell side in pixels.
        cols: Cells per row.

    Returns:
        BGR uint8 montage, or ``None`` if nothing drawable.
    """
    if not records or n <= 0:
        return None
    rng = np.random.default_rng(42)
    pick = sorted(rng.choice(len(records), min(n, len(records)), replace=False))
    cells: list[np.ndarray] = []
    for idx in pick:
        r = records[idx]
        s = samples_by_id.get(r["id"])
        if s is None:
            continue
        img = cv2.imread(str(s.image_path))
        if img is None:
            continue
        h, w = img.shape[:2]
        scale = cell / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

        def pt(p):
            return int(p[0] * scale), int(p[1] * scale)

        rad = max(int(r["od_radius"] * scale), 4)
        cv2.circle(img, pt(r["od_pred"]), rad, (200, 200, 0), 2)
        cv2.circle(img, pt(r["fovea_pred"]), max(rad // 2, 3), (80, 80, 255), 2)
        cv2.drawMarker(img, pt(r["od_gt"]), (200, 200, 0), cv2.MARKER_CROSS, 18, 2)
        cv2.drawMarker(img, pt(r["fovea_gt"]), (80, 80, 255), cv2.MARKER_CROSS, 18, 2)
        label = (f"{r['id']} OD {r['od_err_px']:.0f}px fv {r['fovea_err_px']:.0f}px "
                 f"c {r['fovea_confidence']:.2f}")
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
    p = argparse.ArgumentParser(description="Evaluate the OD/fovea detector on IDRiD.")
    p.add_argument("--config", type=pathlib.Path,
                   default=pathlib.Path("configs/default.yaml"))
    p.add_argument("--weights", type=pathlib.Path, default=None)
    p.add_argument("--split", default="test", help="test | train | train,test")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--montage-n", type=int, default=12)
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    cfg = load_config(args.config)
    root = pathlib.Path(cfg["data"]["idrid_root"])
    if not root.exists():
        raise FileNotFoundError(f"IDRiD localization root not found: {root}")
    out_dir = pathlib.Path(cfg["io"]["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    splits = [s.strip() for s in args.split.split(",") if s.strip()]
    per_split: dict[str, dict] = {}
    all_records: list[dict] = []
    samples_by_id: dict = {}
    for split in splits:
        print(f"Evaluating IDRiD {split}…")
        summary, records = evaluate_split(
            root, split, args.config, args.weights, args.limit)
        per_split[split] = summary
        all_records.extend(records)
        for s in load_split(root, split):
            samples_by_id[s.image_id] = s
        fv = summary["fovea"]["error_px"]
        od = summary["od"]["error_px"]
        print(f"  OD median {od['median']:.0f}px  fovea median {fv['median']:.0f}px")

    report_path = out_dir / "eval_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({"per_split": per_split, "n_total": len(all_records)}, f, indent=2)
    print(f"Saved metrics -> {report_path}")

    montage = make_montage(all_records, samples_by_id, args.montage_n)
    if montage is not None:
        montage_path = out_dir / "montage.png"
        cv2.imwrite(str(montage_path), montage)
        print(f"Saved montage -> {montage_path}")


if __name__ == "__main__":
    main()
