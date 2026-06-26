"""Durable store for clinician OD/fovea corrections (Phase 3/4).

Each correction is appended as one JSON line to ``corrections.jsonl`` under the
configured corrections directory, and the original uploaded image is saved once
(content-addressed by SHA-256) under ``images/`` so the offline fine-tune loop
(Phase 4) can rebuild ``(image, od_xy, fovea_xy)`` training samples. The store
lives on the E: drive like the datasets and is gitignored — it is the only
persisted state in the otherwise-stateless demo.

Corrected centres are recorded in BOTH the flipped (pre-rotation) frame — what
the clinician edited on the detection slide — and **original-image pixels**
(inverse of the canonical flip), so Phase 4 can FOV-crop the stored original and
regenerate Gaussian targets without re-deriving the transform.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path

# One process-wide lock: appends are tiny and the demo serialises GPU work
# anyway, so a coarse lock keeps the JSONL well-formed under concurrent saves.
_WRITE_LOCK = threading.Lock()

_JSONL_NAME = "corrections.jsonl"
_IMAGES_SUBDIR = "images"


def _ensure_dirs(base_dir: Path) -> Path:
    """Create the corrections dir + ``images/`` subdir, returning the images dir."""
    images_dir = base_dir / _IMAGES_SUBDIR
    images_dir.mkdir(parents=True, exist_ok=True)
    return images_dir


def save_correction(
    base_dir: Path,
    record: dict,
    image_bytes: bytes,
    image_hash: str,
    image_ext: str = "png",
) -> str:
    """Persist one correction record + its original image.

    Args:
        base_dir: Corrections directory (``settings.corrections_dir``).
        record: Correction payload (eye, corrected centres in analysis +
            original pixels, space dims, confidence-at-capture, notes, …).
            ``image_hash`` and ``timestamp`` are added/overwritten here.
        image_bytes: Raw original upload bytes (saved once, content-addressed).
        image_hash: SHA-256 hex digest of ``image_bytes`` (the record id).
        image_ext: File extension for the saved image (no dot).

    Returns:
        The ``image_hash`` (record id).
    """
    images_dir = _ensure_dirs(base_dir)
    image_path = images_dir / f"{image_hash}.{image_ext}"

    full = dict(record)
    full["image_hash"] = image_hash
    full["image_file"] = str(Path(_IMAGES_SUBDIR) / image_path.name)
    full["timestamp"] = datetime.now(timezone.utc).isoformat()

    with _WRITE_LOCK:
        if not image_path.exists():
            image_path.write_bytes(image_bytes)
        with (base_dir / _JSONL_NAME).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(full, ensure_ascii=False) + "\n")

    return image_hash
