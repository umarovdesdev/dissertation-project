"""Unit tests for the adaptive polar CLAHE (Stage 5 polar variant)."""

import numpy as np
import pytest

from src.preprocessing.polar_clahe import (
    PolarClaheParams,
    apply_polar_clahe,
    maybe_apply_polar_clahe,
    resolve_pivot,
)


def _make_fundus(size: int = 256, pad: int = 40) -> tuple[np.ndarray, np.ndarray]:
    """Synthetic RGB fundus + circular FOV mask with a zero-padding border.

    Returns:
        ``(image_rgb_uint8, fov_mask_float32)`` of shape ``(size, size, 3)`` and
        ``(size, size)``; the mask is 1.0 inside a centred disc, 0.0 outside.
    """
    rng = np.random.default_rng(0)
    yy, xx = np.mgrid[0:size, 0:size]
    cx = cy = size / 2.0
    radius = size / 2.0 - pad
    mask = (((xx - cx) ** 2 + (yy - cy) ** 2) <= radius ** 2).astype(np.float32)

    base = rng.integers(60, 180, size=(size, size, 3), dtype=np.uint8)
    image = (base * mask[..., None]).astype(np.uint8)  # zero padding outside FOV
    return image, mask


def test_output_shape_and_dtype_preserved() -> None:
    image, mask = _make_fundus()
    out = apply_polar_clahe(image, mask, PolarClaheParams())
    assert out.shape == image.shape
    assert out.dtype == np.uint8


def test_padding_outside_mask_untouched() -> None:
    image, mask = _make_fundus()
    out = apply_polar_clahe(image, mask, PolarClaheParams())
    outside = mask < 0.5
    # Outside the FOV the image is left unchanged (padding preserved).
    assert np.array_equal(out[outside], image[outside])


def test_fov_region_is_modified() -> None:
    image, mask = _make_fundus()
    out = apply_polar_clahe(image, mask, PolarClaheParams())
    inside = mask > 0.5
    # Contrast enhancement must actually change pixels inside the FOV.
    assert not np.array_equal(out[inside], image[inside])


def test_deterministic_at_inference() -> None:
    image, mask = _make_fundus()
    a = apply_polar_clahe(image, mask, PolarClaheParams())
    b = apply_polar_clahe(image, mask, PolarClaheParams())
    assert np.array_equal(a, b)


def test_maybe_apply_always_runs_at_inference() -> None:
    image, mask = _make_fundus()
    out = maybe_apply_polar_clahe(image, mask, is_training=False)
    ref = apply_polar_clahe(image, mask)
    assert np.array_equal(out, ref)


def test_pivot_falls_back_to_centroid_for_bad_fovea() -> None:
    _, mask = _make_fundus()
    ys, xs = np.where(mask > 0)
    centroid = (float(xs.mean()), float(ys.mean()))

    # A fovea outside the FOV (in the padding) is rejected → centroid used.
    out_of_fov = resolve_pivot(mask, (1.0, 1.0))
    assert out_of_fov == pytest.approx(centroid, abs=1.0)

    # A fovea inside the FOV is honoured.
    inside = resolve_pivot(mask, centroid)
    assert inside == pytest.approx(centroid, abs=1.0)


def test_graceful_on_empty_mask() -> None:
    image = np.full((64, 64, 3), 100, dtype=np.uint8)
    empty = np.zeros((64, 64), dtype=np.float32)
    out = apply_polar_clahe(image, empty)
    assert np.array_equal(out, image)  # nothing to enhance → input returned
