"""Export the demo clinician-correction store into trainable samples (Phase 4).

The demo backend persists each clinician OD/fovea correction as one JSON line in
``corrections.jsonl`` under the corrections directory, alongside the original
uploaded image (content-addressed by SHA-256 under ``images/``). Each record
already carries the corrected OD/fovea centres in **original-image pixels**
(``od_center_original`` / ``fovea_center_original``) — exactly the form
:class:`src.data.Sample` expects — so converting the store to training samples
is a parse + dedup + leakage-filter, not a re-projection.

This module both exposes :func:`load_correction_samples` (consumed by
``finetune_corrections.py``) and runs as a CLI that writes a manifest and prints
a summary::

    python scripts/export_corrections.py \
        --corrections-dir ../../demo/server/data/od_fovea_corrections \
        --idrid-root "E:/datasets/IDRiD/C. Localization" \
        --out outputs/corrections_manifest.jsonl

``--idrid-root`` is used only to compute the SHA-256 of the 103 IDRiD **test**
images so any correction made on a test image is dropped — the test split must
never leak into fine-tuning (binding contract §3). It needs no torch.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data import Sample, load_split  # noqa: E402

_JSONL_NAME = "corrections.jsonl"


def _coord(value) -> tuple[float, float] | None:
    """Coerce a stored ``[x, y]`` pair into a float tuple, or ``None``."""
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return None
    try:
        return (float(value[0]), float(value[1]))
    except (TypeError, ValueError):
        return None


def read_correction_records(corrections_dir: pathlib.Path) -> list[dict]:
    """Read every correction record from the store, in file order.

    Args:
        corrections_dir: Directory holding ``corrections.jsonl`` + ``images/``.

    Returns:
        List of parsed JSON records (malformed lines are skipped). Empty if the
        store does not exist yet.
    """
    jsonl = corrections_dir / _JSONL_NAME
    if not jsonl.exists():
        return []
    records: list[dict] = []
    with jsonl.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def idrid_test_hashes(idrid_root: pathlib.Path) -> set[str]:
    """SHA-256 digests of every IDRiD **test** image (for leakage filtering).

    Args:
        idrid_root: ``C. Localization`` directory.

    Returns:
        Set of lowercase hex SHA-256 digests of the 103 test JPEGs. Empty if the
        root is absent.
    """
    hashes: set[str] = set()
    if not idrid_root.exists():
        return hashes
    for sample in load_split(idrid_root, "test"):
        try:
            hashes.add(hashlib.sha256(sample.image_path.read_bytes()).hexdigest())
        except OSError:
            continue
    return hashes


def load_correction_samples(
    corrections_dir: pathlib.Path,
    exclude_image_hashes: set[str] | None = None,
) -> list[Sample]:
    """Convert the correction store into deduplicated training samples.

    The latest correction per image (by ``timestamp``) wins, so a clinician who
    re-edits an image supersedes their earlier fix. Records missing an original
    image file or original-pixel coordinates are skipped, as are any whose image
    hash is in ``exclude_image_hashes`` (the IDRiD test set).

    Args:
        corrections_dir: Directory holding ``corrections.jsonl`` + ``images/``.
        exclude_image_hashes: Image hashes to drop (test-leakage guard).

    Returns:
        List of :class:`Sample` with ``od_xy``/``fovea_xy`` in original-image
        pixels, sorted by image hash for determinism.
    """
    exclude = exclude_image_hashes or set()
    latest: dict[str, dict] = {}
    for rec in read_correction_records(corrections_dir):
        image_hash = rec.get("image_hash")
        if not image_hash or image_hash in exclude:
            continue
        prev = latest.get(image_hash)
        if prev is None or str(rec.get("timestamp", "")) >= str(prev.get("timestamp", "")):
            latest[image_hash] = rec

    samples: list[Sample] = []
    for image_hash in sorted(latest):
        rec = latest[image_hash]
        od_xy = _coord(rec.get("od_center_original"))
        fovea_xy = _coord(rec.get("fovea_center_original"))
        image_file = rec.get("image_file")
        if od_xy is None or fovea_xy is None or not image_file:
            continue
        image_path = corrections_dir / image_file
        if not image_path.exists():
            continue
        samples.append(Sample(image_hash, image_path, od_xy, fovea_xy))
    return samples


def _write_manifest(samples: list[Sample], out_path: pathlib.Path) -> None:
    """Write the exported samples as a JSONL manifest for inspection."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for s in samples:
            fh.write(json.dumps({
                "image_id": s.image_id,
                "image_path": str(s.image_path),
                "od_xy": list(s.od_xy),
                "fovea_xy": list(s.fovea_xy),
            }, ensure_ascii=False) + "\n")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Export clinician OD/fovea corrections into training samples.")
    p.add_argument(
        "--corrections-dir", type=pathlib.Path,
        default=ROOT.parent.parent / "demo" / "server" / "data" / "od_fovea_corrections",
        help="Correction store directory (corrections.jsonl + images/).")
    p.add_argument(
        "--idrid-root", type=pathlib.Path, default=None,
        help="IDRiD 'C. Localization' root; used to exclude test-image corrections.")
    p.add_argument(
        "--out", type=pathlib.Path, default=ROOT / "outputs" / "corrections_manifest.jsonl",
        help="Manifest output path (JSONL).")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    exclude = idrid_test_hashes(args.idrid_root) if args.idrid_root else set()
    if args.idrid_root and not exclude:
        print(f"[WARN] no IDRiD test hashes computed from {args.idrid_root} — "
              "test-leakage filter is inactive.")

    n_records = len(read_correction_records(args.corrections_dir))
    samples = load_correction_samples(args.corrections_dir, exclude)
    _write_manifest(samples, args.out)

    print(f"correction store : {args.corrections_dir}")
    print(f"raw records      : {n_records}")
    print(f"test exclusions  : {len(exclude)} IDRiD-test hashes")
    print(f"export samples   : {len(samples)} (deduped, latest-per-image)")
    print(f"manifest         : {args.out}")
    if not samples:
        print("No usable corrections yet - fine-tuning has nothing to add.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
