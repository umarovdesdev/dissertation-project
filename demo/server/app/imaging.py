"""In-memory image decoding with safety limits (TASK-Demo §C.3/§C.4).

No disk writes: uploads are decoded straight from bytes. Limits are cheap
insurance (not security) against decode bombs and oversized payloads.
"""

from __future__ import annotations

import base64
import hashlib
import io

import cv2
import numpy as np
from PIL import Image

# --- Limits (TASK-Demo §C.4) ---
MAX_IMAGE_BYTES: int = 8 * 1024 * 1024          # 8 MB per image
MAX_DECODED_PX: int = 4096                       # reject > 4096×4096
ALLOWED_MIME: frozenset[str] = frozenset({"image/jpeg", "image/png", "image/webp"})


class PayloadTooLarge(Exception):
    """Raised when an upload exceeds the byte or pixel budget (→ HTTP 413)."""


class UnsupportedMedia(Exception):
    """Raised for a disallowed MIME type (→ HTTP 415)."""


class BadImage(Exception):
    """Raised when bytes cannot be decoded as an image (→ HTTP 400)."""


def check_upload(content_type: str | None, size: int) -> None:
    """Validate an upload's declared MIME type and byte size before decoding.

    Args:
        content_type: The ``Content-Type`` of the upload (may be ``None``).
        size: Number of bytes in the upload.

    Raises:
        PayloadTooLarge: If ``size`` exceeds :data:`MAX_IMAGE_BYTES`.
        UnsupportedMedia: If ``content_type`` is set and not in
            :data:`ALLOWED_MIME`.
    """
    if size > MAX_IMAGE_BYTES:
        raise PayloadTooLarge(
            f"Image is {size} bytes; limit is {MAX_IMAGE_BYTES} ({MAX_IMAGE_BYTES // (1024 * 1024)} MB)."
        )
    if content_type and content_type.split(";")[0].strip().lower() not in ALLOWED_MIME:
        raise UnsupportedMedia(
            f"Unsupported content-type {content_type!r}. Allowed: {sorted(ALLOWED_MIME)}."
        )


def decode_rgb(data: bytes) -> np.ndarray:
    """Decode raw bytes to an RGB uint8 array, enforcing the pixel limit.

    Args:
        data: Raw image bytes.

    Returns:
        ``(H, W, 3)`` uint8 RGB array.

    Raises:
        BadImage: If the bytes are not a decodable image.
        PayloadTooLarge: If the decoded resolution exceeds
            :data:`MAX_DECODED_PX` on either axis.
    """
    try:
        img = Image.open(io.BytesIO(data))
        img.verify()  # cheap structural check (catches truncated/non-images)
        img = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception as exc:  # noqa: BLE001
        raise BadImage("Uploaded file is not a decodable image.") from exc

    w, h = img.size
    if w > MAX_DECODED_PX or h > MAX_DECODED_PX:
        raise PayloadTooLarge(
            f"Decoded resolution {w}×{h} exceeds {MAX_DECODED_PX}×{MAX_DECODED_PX}."
        )
    return np.asarray(img, dtype=np.uint8)


def png_b64_from_bgr(image_bgr: np.ndarray) -> str:
    """Encode a BGR uint8 array as a base64 PNG string (no data: prefix).

    Args:
        image_bgr: BGR uint8 array (as produced by OpenCV).

    Returns:
        Base64-encoded PNG bytes.

    Raises:
        RuntimeError: If PNG encoding fails.
    """
    ok, buf = cv2.imencode(".png", image_bgr)
    if not ok:
        raise RuntimeError("PNG encoding failed.")
    return base64.b64encode(buf.tobytes()).decode("ascii")


def png_b64_from_rgb(image_rgb: np.ndarray) -> str:
    """Encode an RGB uint8 array as a base64 PNG string (no data: prefix).

    Args:
        image_rgb: RGB uint8 array.

    Returns:
        Base64-encoded PNG bytes.
    """
    return png_b64_from_bgr(cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))


def heatmap_png_b64(heatmap: np.ndarray) -> str:
    """Colorize a float32 probability heatmap to a translucent RGBA PNG.

    The map is peak-normalized (so the sharp DSNT blob is visible), colorized
    with a JET colormap, and given an alpha channel equal to the normalized
    intensity — low-probability background is transparent so the PNG can be
    overlaid directly on the analysis-space base image in the demo.

    Args:
        heatmap: float32 ``(H, W)`` probability map (any non-negative scale).

    Returns:
        Base64-encoded RGBA PNG bytes (no ``data:`` prefix).

    Raises:
        RuntimeError: If PNG encoding fails.
    """
    hm = np.asarray(heatmap, dtype=np.float32)
    peak = float(hm.max())
    norm = hm / peak if peak > 1e-12 else np.zeros_like(hm)
    u8 = np.clip(norm * 255.0, 0, 255).astype(np.uint8)
    color_bgr = cv2.applyColorMap(u8, cv2.COLORMAP_JET)          # (H, W, 3) BGR
    bgra = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = u8                                            # alpha = intensity
    ok, buf = cv2.imencode(".png", bgra)
    if not ok:
        raise RuntimeError("Heatmap PNG encoding failed.")
    return base64.b64encode(buf.tobytes()).decode("ascii")


def sha256_hex(data: bytes) -> str:
    """Return the hex SHA-256 digest of raw bytes (image content identity)."""
    return hashlib.sha256(data).hexdigest()
