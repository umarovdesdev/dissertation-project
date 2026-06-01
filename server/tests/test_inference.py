"""Smoke tests for the inference API.

Run from the repo root:
    pytest server/tests/test_inference.py

These boot the app via FastAPI's TestClient (triggers startup model load).
They pass without a trained checkpoint — the model runs on random-init weights,
which still yields a valid softmax. They assert *shape/behaviour*, not accuracy.
"""

from __future__ import annotations

import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from server.app.main import app


def _synthetic_fundus(size: int = 600) -> bytes:
    """Make a fundus-like image (bright disc on black) so FOV crop succeeds."""
    yy, xx = np.mgrid[0:size, 0:size]
    cx = cy = size / 2
    r = size * 0.45
    disc = ((xx - cx) ** 2 + (yy - cy) ** 2) <= r ** 2
    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[disc] = (180, 90, 40)  # warm retina-ish tone
    buf = io.BytesIO()
    Image.fromarray(img, "RGB").save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model"] == "config-D"
    assert "checkpoint_loaded" in body
    # Provenance fields for the demo footer (§D.7).
    assert "version" in body and "git_sha" in body


def test_predict_left_only(client: TestClient) -> None:
    r = client.post("/api/predict", files={"left": ("left.png", _synthetic_fundus(), "image/png")})
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["probs"]) == 5
    assert abs(sum(body["probs"]) - 1.0) < 1e-3
    assert 0 <= body["pred"] <= 4
    assert len(body["per_eye"]) == 1


def test_predict_both_eyes(client: TestClient) -> None:
    files = {
        "left": ("left.png", _synthetic_fundus(), "image/png"),
        "right": ("right.png", _synthetic_fundus(), "image/png"),
    }
    r = client.post("/api/predict", files=files)
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["per_eye"]) == 2
    assert body["pred"] == max(e["pred"] for e in body["per_eye"])


def test_predict_rejects_non_image(client: TestClient) -> None:
    # text/plain is rejected by the MIME gate (415); a mislabeled image would
    # be caught by the decoder (400). Either is an acceptable rejection.
    r = client.post("/api/predict", files={"left": ("note.txt", b"not an image", "text/plain")})
    assert r.status_code in (400, 415)


def test_predict_requires_an_eye(client: TestClient) -> None:
    r = client.post("/api/predict")
    assert r.status_code == 400


def test_gradcam(client: TestClient) -> None:
    r = client.post(
        "/api/gradcam",
        data={"eye": "left"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["gradcam_png_b64"] and body["attention_overlay_png_b64"]
    assert 0 <= body["target_class"] <= 4


def test_visualize(client: TestClient) -> None:
    r = client.post(
        "/api/visualize",
        data={"eye": "left"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["v5_preview_png_b64"] and body["fov_mask_png_b64"]
    assert "confident" in body["od_fovea"]


def test_selftest(client: TestClient) -> None:
    r = client.get("/api/selftest")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["predict"] == "pass"
    assert body["gradcam"] == "pass"
    assert body["visualize"] == "pass"
