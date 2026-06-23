"""Torch-free tests for the Phase-4 correction export (parse/dedup/leakage)."""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from export_corrections import load_correction_samples, read_correction_records  # noqa: E402


def _write_store(tmp_path: pathlib.Path, records: list[dict]) -> pathlib.Path:
    """Create a correction store dir with a JSONL + the referenced image files."""
    base = tmp_path / "store"
    images = base / "images"
    images.mkdir(parents=True)
    seen: set[str] = set()
    with (base / "corrections.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")
            h = rec.get("image_hash")
            if h and h not in seen and rec.get("image_file"):
                (base / rec["image_file"]).write_bytes(b"\x89PNG-stub")
                seen.add(h)
    return base


def _rec(image_hash: str, od, fovea, ts: str) -> dict:
    return {
        "image_hash": image_hash,
        "image_file": f"images/{image_hash}.png",
        "od_center_original": list(od),
        "fovea_center_original": list(fovea),
        "timestamp": ts,
    }


def test_empty_store_returns_nothing(tmp_path):
    assert read_correction_records(tmp_path / "nope") == []
    assert load_correction_samples(tmp_path / "nope") == []


def test_basic_export_maps_original_coords(tmp_path):
    base = _write_store(tmp_path, [_rec("aaa", (100, 200), (300, 220), "2026-06-23T10:00:00Z")])
    samples = load_correction_samples(base)
    assert len(samples) == 1
    s = samples[0]
    assert s.image_id == "aaa"
    assert s.od_xy == (100.0, 200.0)
    assert s.fovea_xy == (300.0, 220.0)
    assert s.image_path.exists()


def test_latest_correction_per_image_wins(tmp_path):
    base = _write_store(tmp_path, [
        _rec("aaa", (10, 10), (50, 10), "2026-06-23T10:00:00Z"),
        _rec("aaa", (12, 14), (55, 12), "2026-06-23T12:00:00Z"),  # newer
    ])
    samples = load_correction_samples(base)
    assert len(samples) == 1
    assert samples[0].od_xy == (12.0, 14.0)


def test_test_leakage_filter_excludes_hashes(tmp_path):
    base = _write_store(tmp_path, [
        _rec("keep", (1, 2), (3, 4), "2026-06-23T10:00:00Z"),
        _rec("leak", (5, 6), (7, 8), "2026-06-23T10:00:00Z"),
    ])
    samples = load_correction_samples(base, exclude_image_hashes={"leak"})
    assert [s.image_id for s in samples] == ["keep"]


def test_malformed_and_incomplete_records_skipped(tmp_path):
    base = tmp_path / "store"
    (base / "images").mkdir(parents=True)
    good = _rec("good", (1, 2), (3, 4), "2026-06-23T10:00:00Z")
    (base / good["image_file"]).write_bytes(b"x")
    with (base / "corrections.jsonl").open("w", encoding="utf-8") as fh:
        fh.write("{ not json\n")                                    # malformed line
        fh.write(json.dumps({"image_hash": "nocoords"}) + "\n")     # missing coords
        fh.write(json.dumps(_rec("missing_img", (1, 1), (2, 2),     # image not on disk
                                 "2026-06-23T10:00:00Z")) + "\n")
        fh.write(json.dumps(good) + "\n")
    samples = load_correction_samples(base)
    assert [s.image_id for s in samples] == ["good"]
