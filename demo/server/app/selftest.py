"""Self-test: exercise predict + gradcam + visualize end-to-end (§C.7).

Uses synthetic fundus-like images so the test runs anywhere (no bundled EyePACS
assets, no network). It validates the *plumbing* (shapes, encodings, no
exceptions), not prediction accuracy — accuracy needs a real checkpoint.
"""

from __future__ import annotations

import base64
import io

import numpy as np
from PIL import Image

from . import gradcam as gradcam_mod
from . import visualize as visualize_mod


def _synthetic_fundus(seed: int, size: int = 600) -> bytes:
    """Generate a fundus-like PNG (bright disc + a few lesion-like spots)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    cx = cy = size / 2
    r = size * 0.45
    disc = ((xx - cx) ** 2 + (yy - cy) ** 2) <= r ** 2
    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[disc] = (170, 90, 45)
    # A bright OD-like blob off-center and a few dark spots.
    for _ in range(3 + seed % 3):
        sx, sy = rng.integers(size * 0.2, size * 0.8, size=2)
        rr = int(rng.integers(8, 24))
        spot = ((xx - sx) ** 2 + (yy - sy) ** 2) <= rr ** 2
        img[spot & disc] = (40, 20, 10)
    odx, ody = int(size * 0.7), int(size * 0.5)
    odblob = ((xx - odx) ** 2 + (yy - ody) ** 2) <= (size * 0.06) ** 2
    img[odblob & disc] = (240, 220, 180)
    buf = io.BytesIO()
    Image.fromarray(img, "RGB").save(buf, format="PNG")
    return buf.getvalue()


def run_selftest(engine, n: int = 3) -> dict:
    """Run predict/gradcam/visualize on ``n`` synthetic images.

    Args:
        engine: The loaded :class:`InferenceEngine`.
        n: Number of synthetic images to test.

    Returns:
        Dict with ``predict``/``gradcam``/``visualize`` ("pass"/"fail …") and
        a ``details`` list.
    """
    details: list[str] = []
    status = {"predict": "pass", "gradcam": "pass", "visualize": "pass"}

    for i in range(n):
        img = _synthetic_fundus(i)

        try:
            r = engine.predict_patient(img, None)
            assert len(r.probs) == 5 and abs(sum(r.probs) - 1.0) < 1e-2
        except Exception as exc:  # noqa: BLE001
            status["predict"] = "fail"
            details.append(f"predict[{i}]: {exc}")

        try:
            g = gradcam_mod.compute_gradcam(engine, img, "left")
            assert base64.b64decode(g["gradcam_png_b64"])
            assert base64.b64decode(g["attention_overlay_png_b64"])
        except Exception as exc:  # noqa: BLE001
            status["gradcam"] = "fail"
            details.append(f"gradcam[{i}]: {exc}")

        try:
            v = visualize_mod.compute_visualization(engine, img, "left")
            assert base64.b64decode(v["preview_png_b64"])
            assert base64.b64decode(v["fov_mask_png_b64"])
            assert "confident" in v["od_fovea"]
        except Exception as exc:  # noqa: BLE001
            status["visualize"] = "fail"
            details.append(f"visualize[{i}]: {exc}")

    return {**status, "details": details}
