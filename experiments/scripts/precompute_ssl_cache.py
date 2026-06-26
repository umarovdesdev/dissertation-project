#!/usr/bin/env python3
"""Optional: precompute the Stage 0–4 cache for the SSL test corpus (brief §4.1/§12).

Throughput fix for SSL: 53k images × hundreds of epochs makes the deterministic
Stages 0–4 (OD/fovea, crop+resize, flat-field) the bottleneck. They carry no
train-time randomness, so they are cached once at the SSL resolution (256²); the
per-epoch two-view path then runs only Stage 5 (CLAHE) + the augmentation.

This mirrors ``scripts/precompute_cache.py`` exactly (it *is*
``PreprocessingPipeline.precompute_deterministic``) but targets the SSL corpus
(``<paths.eyepacs>/test``) at ``ssl.image_size``. Output per image is a 4-channel
PNG (BGR Stage-4 + binary FOV-mask alpha) plus ``cache_meta.csv``.

NOTE: the cached-read SSL dataset path is a deferred Phase-4 throughput
follow-up; the live :class:`~src.ssl.dataset.EyePACSSSLDataset` is the primary
path. This script produces the cache so that wiring is a drop-in later.

Usage:
    python scripts/precompute_ssl_cache.py \
        --config configs/default.yaml --output-dir E:/datasets/EyePACS/ssl_cache_256 \
        --num-workers 8
"""

from __future__ import annotations

import argparse
import csv
import os
import pathlib
import sys

import cv2
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# Force UTF-8 stdout/stderr so non-ASCII log glyphs do not crash on Windows
# consoles using a legacy code page (e.g. cp1251).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

from src.utils.config import load_configs  # noqa: E402

_PIPELINE = None
_OUT_DIR: pathlib.Path | None = None
_PNG_COMPRESSION = 6


def _init_worker(
    preprocessing_cfg: dict | None, target_size: int, out_dir: str, png_compression: int
) -> None:
    """Pool initializer: build one inference SSL-base pipeline per worker."""
    global _PIPELINE, _OUT_DIR, _PNG_COMPRESSION
    from src.ssl.dataset import build_ssl_base_pipeline  # noqa: PLC0415

    _PIPELINE = build_ssl_base_pipeline(preprocessing_cfg, target_size)
    _OUT_DIR = pathlib.Path(out_dir)
    _PNG_COMPRESSION = png_compression


def _process_one(task: tuple[str, str, str]) -> tuple[str, str, float, float, float]:
    """Cache one image's Stages 0–4 (runs in a worker)."""
    name, image_path, eye_side = task
    assert _PIPELINE is not None and _OUT_DIR is not None

    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        return (name, "ERROR_READ", 0.0, float("nan"), float("nan"))

    flat_rgb, fov_mask, confident, rot, pivot = _PIPELINE.precompute_deterministic(
        img_bgr, eye_side
    )
    bgr = cv2.cvtColor(flat_rgb, cv2.COLOR_RGB2BGR)
    alpha = (fov_mask > 0.5).astype(np.uint8) * 255
    bgra = np.dstack([bgr, alpha])
    out_png = _OUT_DIR / f"{name}.png"
    ok = cv2.imwrite(str(out_png), bgra, [cv2.IMWRITE_PNG_COMPRESSION, _PNG_COMPRESSION])
    if not ok:
        return (name, "ERROR_WRITE", 0.0, float("nan"), float("nan"))

    fx, fy = pivot if pivot is not None else (float("nan"), float("nan"))
    return (name, f"ok:{bool(confident)}", float(rot), float(fx), float(fy))


def _discover(test_dir: pathlib.Path, labels_csv: pathlib.Path, suffix: str, limit: int):
    """Build ``(name, path, eye_side)`` tasks from the SSL labels CSV."""
    tasks = []
    with open(labels_csv, newline="") as fh:
        for row in csv.DictReader(fh):
            name = row.get("image", "")
            if not name:
                continue
            path = test_dir / f"{name}{suffix}"
            if not path.exists():
                continue
            side = "left" if "_left" in name else "right" if "_right" in name else "unknown"
            tasks.append((name, str(path), side))
            if limit and len(tasks) >= limit:
                break
    return tasks


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precompute SSL Stage 0–4 cache.")
    parser.add_argument("--config", action="append", default=None,
                        help="YAML config(s). Default: configs/default.yaml.")
    parser.add_argument("--output-dir", required=True, type=pathlib.Path)
    parser.add_argument("--num-workers", default=max(1, os.cpu_count() or 1), type=int)
    parser.add_argument("--png-compression", default=_PNG_COMPRESSION, type=int)
    parser.add_argument("--limit", default=0, type=int)
    return parser.parse_args()


def main() -> None:
    import multiprocessing as mp

    args = _parse_args()
    config = load_configs(*(args.config or ["configs/default.yaml"]))
    ssl_cfg = config["ssl"]
    corpus = ssl_cfg["corpus"]
    eyepacs_root = pathlib.Path(config["paths"]["eyepacs"])
    test_dir = eyepacs_root / corpus["eyepacs_test_dir"]
    labels_csv = eyepacs_root / corpus["test_labels_csv"]
    suffix = corpus.get("image_glob", "*.jpeg").replace("*", "")
    target_size = int(ssl_cfg.get("image_size", 256))

    out_dir: pathlib.Path = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / "cache_meta.csv"

    tasks = _discover(test_dir, labels_csv, suffix, args.limit)
    print(f"Discovered {len(tasks)} SSL image(s) at {target_size}px → {out_dir}")
    if not tasks:
        print("ERROR: No images found.", file=sys.stderr)
        sys.exit(1)

    n_ok = n_err = 0
    with open(meta_path, "w", newline="") as meta_fh:
        writer = csv.writer(meta_fh)
        writer.writerow(["image", "confident", "rotation_sigma_deg", "fovea_x", "fovea_y"])
        ctx = mp.get_context("spawn")
        with ctx.Pool(
            processes=max(1, args.num_workers),
            initializer=_init_worker,
            initargs=(config.get("preprocessing"), target_size, str(out_dir), args.png_compression),
        ) as pool:
            for i, (name, status, rot, fx, fy) in enumerate(
                pool.imap_unordered(_process_one, tasks, chunksize=8), start=1
            ):
                if status.startswith("ok"):
                    confident = status.split(":", 1)[1]
                    fx_s = "" if fx != fx else f"{fx:.4f}"
                    fy_s = "" if fy != fy else f"{fy:.4f}"
                    writer.writerow([name, confident, f"{rot:.6f}", fx_s, fy_s])
                    n_ok += 1
                else:
                    n_err += 1
                if i % 500 == 0 or i == len(tasks):
                    meta_fh.flush()
                    print(f"  {i}/{len(tasks)} (ok={n_ok}, err={n_err})…", flush=True)

    print(f"Done. ok={n_ok} err={n_err} | cache={out_dir}")


if __name__ == "__main__":
    main()
