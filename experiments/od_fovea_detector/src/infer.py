"""Inference entry point — the binding §6 public API.

Exposes ``detect_od_fovea(image_rgb) -> ODFoveaResult`` with the *exact*
monorepo signature plus the additive confidence/heatmap fields. The maintainer
can wrap this behind the existing ``src/preprocessing/od_fovea_detect.py``
facade with no downstream changes.

Pipeline for a single image (brief §6 hard requirements):
  1. accept an arbitrary-resolution RGB uint8 array;
  2. FOV-crop + isotropic-resize to the input frame (kills the vignette);
  3. run the net -> 2 heatmaps;
  4. decode each heatmap to a sub-pixel frame coordinate + genuine confidence;
  5. map coordinates back to **input-image pixels** via the inverse affine;
  6. assemble ``ODFoveaResult`` (radii, distance, angle, rotation sigma,
     per-landmark confidence, and optional resized heatmaps).

Weights load once (lazy singleton); CPU and CUDA both supported; weights path
from config/argument. Deterministic, no global state beyond the cached model.
"""

from __future__ import annotations

import math
import pathlib
from dataclasses import dataclass

import cv2
import numpy as np

from .confidence import decode_heatmap
from .geometry import crop_and_resize
from .utils import load_config, resolve_device

_DEFAULT_CONFIG = pathlib.Path(__file__).resolve().parent.parent / "configs" / "default.yaml"


@dataclass
class ODFoveaResult:
    """OD/fovea detection result (monorepo-compatible + additive fields).

    The first block reproduces the monorepo ``ODFoveaResult`` exactly. The
    fields below ``confident`` are additive (brief §6): genuine per-landmark
    confidence and optional probability heatmaps resized to the input frame.

    Attributes:
        od_center: ``(x, y)`` OD center in INPUT-image pixels.
        od_radius: OD radius estimate in pixels.
        fovea_center: ``(x, y)`` fovea center in INPUT-image pixels.
        fovea_radius: Fovea radius estimate in pixels.
        distance: Euclidean OD<->fovea distance in pixels.
        angle_rad: ``atan2(dy, dx)`` of the OD->fovea vector (radians).
        angle_deg: Same angle in degrees.
        rotation_sigma_deg: Adaptive rotation sigma (degrees), from heatmap
            spread, capped.
        confident: True iff both landmark confidences exceed the threshold.
        od_confidence: OD confidence in ``[0, 1]`` (from the OD heatmap).
        fovea_confidence: Fovea confidence in ``[0, 1]``.
        od_heatmap: float32 OD probability map resized to the input frame, or
            ``None`` if heatmaps were not requested.
        fovea_heatmap: float32 fovea probability map, or ``None``.
    """

    od_center: tuple[int, int]
    od_radius: float
    fovea_center: tuple[int, int]
    fovea_radius: float
    distance: float
    angle_rad: float
    angle_deg: float
    rotation_sigma_deg: float
    confident: bool
    od_confidence: float
    fovea_confidence: float
    od_heatmap: np.ndarray | None
    fovea_heatmap: np.ndarray | None


class _Detector:
    """Lazy-loaded, cached detector (weights load once)."""

    def __init__(self, config_path: pathlib.Path, weights_path: pathlib.Path | None,
                 device: str | None) -> None:
        import torch  # local import: torch only needed at inference time
        from .model import build_model

        self.cfg = load_config(config_path)
        self.device = resolve_device(device or self.cfg["io"]["device"])
        self.input_size = self.cfg["data"]["input_size"]
        self.heatmap_size = self.cfg["data"]["heatmap_size"]
        conf = self.cfg["confidence"]
        self.sigma_ref = conf["sigma_ref_frac"] * self.heatmap_size
        self.threshold = conf["threshold"]
        self.max_rot_sigma = conf["max_rotation_sigma_deg"]

        self.model = build_model(self.cfg["model"], self.heatmap_size)
        wp = pathlib.Path(weights_path or self.cfg["io"]["weights_path"])
        if not wp.is_absolute():
            wp = config_path.resolve().parent.parent / wp
        if wp.exists():
            ckpt = torch.load(wp, map_location=self.device, weights_only=False)
            state = ckpt.get("state_dict", ckpt) if isinstance(ckpt, dict) else ckpt
            self.model.load_state_dict(state)
            self.loaded_weights = str(wp)
        else:
            # No trained weights present: run with the (randomly initialized)
            # network. Shape/contract is valid; coordinates are not meaningful.
            self.loaded_weights = None
        self.model.to(self.device).eval()
        self._torch = torch


# Module-level singleton cache keyed by (config, weights, device).
_CACHE: dict[tuple, _Detector] = {}


def _get_detector(
    config_path: pathlib.Path | str = _DEFAULT_CONFIG,
    weights_path: pathlib.Path | str | None = None,
    device: str | None = None,
) -> _Detector:
    """Return the cached detector, building it on first use.

    Args:
        config_path: Path to the YAML config.
        weights_path: Optional override for the weights file.
        device: Optional device override.

    Returns:
        The cached :class:`_Detector`.
    """
    key = (str(config_path), str(weights_path), str(device))
    det = _CACHE.get(key)
    if det is None:
        det = _Detector(pathlib.Path(config_path),
                        pathlib.Path(weights_path) if weights_path else None,
                        device)
        _CACHE[key] = det
    return det


def reset_cache() -> None:
    """Clear the cached detector(s). Mainly for tests."""
    _CACHE.clear()


def detect_od_fovea(
    image_rgb: np.ndarray,
    config_path: pathlib.Path | str = _DEFAULT_CONFIG,
    weights_path: pathlib.Path | str | None = None,
    device: str | None = None,
    return_heatmaps: bool = True,
) -> ODFoveaResult:
    """Detect OD and fovea centers in a fundus image (learned heatmaps).

    Args:
        image_rgb: RGB uint8 array ``(H, W, 3)`` at arbitrary resolution.
        config_path: Path to the YAML config (defaults to bundled config).
        weights_path: Optional weights override (defaults to config value).
        device: Optional device override (``"cpu"``/``"cuda"``/``"auto"``).
        return_heatmaps: If True, attach probability heatmaps resized to the
            input frame; if False, the heatmap fields are ``None`` (faster).

    Returns:
        An :class:`ODFoveaResult` with coordinates in INPUT-image pixels and a
        genuine per-landmark confidence derived from heatmap spread.
    """
    if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
        raise ValueError(f"expected RGB (H, W, 3), got shape {image_rgb.shape}")
    h_in, w_in = image_rgb.shape[:2]

    det = _get_detector(config_path, weights_path, device)
    torch = det._torch

    # 2. FOV-crop + resize to the input frame.
    frame, _mask, transform = crop_and_resize(image_rgb, det.input_size)

    # 3. Run the net.
    x = torch.from_numpy(
        frame.astype(np.float32).transpose(2, 0, 1) / 255.0
    ).unsqueeze(0).to(det.device)
    with torch.no_grad():
        out = det.model(x)
    prob = out["heatmap"][0].cpu().numpy()  # (2, Hh, Hw), sums to 1 per channel

    # 4-5. Decode + map back to input-image pixels.
    ratio = det.input_size / det.heatmap_size  # heatmap px -> frame px
    decoded = []
    centers_in: list[tuple[int, int]] = []
    sigma_pos_frame: list[float] = []
    for c in range(2):
        d = decode_heatmap(prob[c], det.sigma_ref, already_prob=True)
        decoded.append(d)
        fx, fy = d.x * ratio, d.y * ratio          # frame pixels
        sx, sy = transform.invert(fx, fy)          # input-image pixels
        centers_in.append((int(round(sx)), int(round(sy))))
        # Heatmap spread expressed in frame pixels -> input pixels via 1/scale.
        sigma_pos_frame.append(d.sigma_eff * ratio / max(transform.scale, 1e-9))

    od_d, fovea_d = decoded
    od_center, fovea_center = centers_in

    # Radii: OD radius from a prior fraction of OD<->fovea distance; fovea ~0.5x.
    dx = fovea_center[0] - od_center[0]
    dy = fovea_center[1] - od_center[1]
    distance = math.hypot(dx, dy)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    od_radius = max(distance / 4.0, 10.0)  # anatomical: OD-fovea ~ 4 OD radii
    fovea_radius = max(od_radius * 0.5, 5.0)

    # rotation_sigma_deg from real positional uncertainty (heatmap spread).
    sigma_pos = math.hypot(*sigma_pos_frame)
    if distance > 0:
        rotation_sigma_deg = math.degrees(math.atan(sigma_pos / distance))
    else:
        rotation_sigma_deg = det.max_rot_sigma
    rotation_sigma_deg = min(rotation_sigma_deg, det.max_rot_sigma)

    od_conf = od_d.confidence
    fovea_conf = fovea_d.confidence
    confident = (od_conf >= det.threshold) and (fovea_conf >= det.threshold)

    od_hm = fovea_hm = None
    if return_heatmaps:
        od_hm = cv2.resize(prob[0], (w_in, h_in), interpolation=cv2.INTER_LINEAR)
        fovea_hm = cv2.resize(prob[1], (w_in, h_in), interpolation=cv2.INTER_LINEAR)

    return ODFoveaResult(
        od_center=od_center,
        od_radius=float(od_radius),
        fovea_center=fovea_center,
        fovea_radius=float(fovea_radius),
        distance=float(distance),
        angle_rad=float(angle_rad),
        angle_deg=float(angle_deg),
        rotation_sigma_deg=float(rotation_sigma_deg),
        confident=bool(confident),
        od_confidence=float(od_conf),
        fovea_confidence=float(fovea_conf),
        od_heatmap=od_hm,
        fovea_heatmap=fovea_hm,
    )
