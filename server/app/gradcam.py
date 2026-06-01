"""Grad-CAM on the live checkpoint.

Scaffold stub. The full implementation (TASK-Demo §C.5) uses
``pytorch-grad-cam`` on EfficientNet-B3's last MBConv block, overlays a JET
heatmap on the original RGB, and returns base64 PNGs. Wired as a 501 for now
so the API surface is stable while the frontend is built against it.
"""

from __future__ import annotations


def compute_gradcam(image_bytes: bytes, eye: str) -> dict:
    """Placeholder — see TASK-Demo §C.5 for the target behaviour.

    Args:
        image_bytes: Raw image bytes.
        eye: ``"left"`` or ``"right"``.

    Raises:
        NotImplementedError: Always, until the real Grad-CAM is wired.
    """
    raise NotImplementedError("Grad-CAM not yet implemented (scaffold).")
