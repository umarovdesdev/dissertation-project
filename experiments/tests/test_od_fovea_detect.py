"""Unit tests for OD/fovea detection module."""

import math

import cv2
import numpy as np
import pytest

from src.preprocessing.od_fovea_detect import (
    ODFoveaResult,
    # The public ``detect_od_fovea`` now delegates to the learned heatmap
    # detector (Phase 2). These tests exercise the classical-CV algorithm
    # (geometry on synthetic discs), which lives on as ``*_classical`` for
    # reference/fallback — alias it so the assertions keep their meaning.
    detect_od_fovea_classical as detect_od_fovea,
    rotate_to_horizontal,
    _detect_od_center,
    _detect_fovea_center,
)


def _make_synthetic_fundus(
    size: int = 512,
    od_pos: tuple[int, int] = (350, 256),
    fovea_pos: tuple[int, int] = (180, 256),
    od_brightness: int = 220,
    fovea_darkness: int = 80,
    bg_level: int = 150,
) -> np.ndarray:
    """Create a synthetic fundus-like image for testing."""
    image = np.full((size, size, 3), bg_level, dtype=np.uint8)

    # Draw FOV circle (slightly brighter than pure bg to mimic retina)
    cv2.circle(
        image, (size // 2, size // 2), size // 2 - 10,
        (bg_level, bg_level, bg_level), -1,
    )

    # Draw OD (bright disc)
    cv2.circle(image, od_pos, 40, (od_brightness,) * 3, -1)

    # Draw fovea (dark region)
    cv2.circle(image, fovea_pos, 20, (fovea_darkness,) * 3, -1)

    # Add some Gaussian noise for realism
    rng = np.random.RandomState(42)
    noise = rng.normal(0, 5, image.shape).astype(np.float32)
    image = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    return image


class TestODDetection:
    """Tests for OD center detection."""

    def test_finds_bright_region(self):
        image = _make_synthetic_fundus(od_pos=(350, 256))
        green = image[:, :, 1]
        center, radius = _detect_od_center(green)
        assert abs(center[0] - 350) < 20
        assert abs(center[1] - 256) < 20
        assert radius > 10

    def test_different_od_position(self):
        image = _make_synthetic_fundus(od_pos=(256, 150))
        green = image[:, :, 1]
        center, radius = _detect_od_center(green)
        assert abs(center[0] - 256) < 20
        assert abs(center[1] - 150) < 20


class TestFoveaDetection:
    """Tests for fovea center detection."""

    def test_finds_dark_region(self):
        image = _make_synthetic_fundus(od_pos=(350, 256), fovea_pos=(180, 256))
        green = image[:, :, 1]
        center, radius = _detect_fovea_center(green, (350, 256), 40.0)
        assert abs(center[0] - 180) < 30
        assert abs(center[1] - 256) < 30

    def test_fallback_when_no_annular_region(self):
        """When annular search mask is empty, returns image center."""
        green = np.full((100, 100), 128, dtype=np.uint8)
        center, radius = _detect_fovea_center(
            green, od_center=(50, 50), od_radius=1.0,
            inner_factor=100.0, outer_factor=200.0,  # impossible range
        )
        assert center == (50, 50)  # image center


class TestDetectODFovea:
    """Tests for the full detection pipeline."""

    def test_returns_valid_dataclass(self):
        image = _make_synthetic_fundus()
        result = detect_od_fovea(image)
        assert isinstance(result, ODFoveaResult)
        assert result.distance > 0
        assert result.rotation_sigma_deg > 0
        assert result.rotation_sigma_deg <= 15.0

    def test_horizontal_axis_angle_near_zero_or_180(self):
        image = _make_synthetic_fundus(od_pos=(350, 256), fovea_pos=(180, 256))
        result = detect_od_fovea(image)
        # OD right, fovea left → angle ≈ 180° (or ≈ -180°)
        assert abs(abs(result.angle_deg) - 180) < 20 or abs(result.angle_deg) < 20

    def test_tilted_axis_detected(self):
        image = _make_synthetic_fundus(od_pos=(350, 200), fovea_pos=(180, 310))
        result = detect_od_fovea(image)
        assert abs(result.angle_deg) > 5  # not horizontal

    def test_confidence_false_for_black_image(self):
        image = np.zeros((512, 512, 3), dtype=np.uint8)
        result = detect_od_fovea(image)
        assert result.confident is False

    def test_confidence_false_for_uniform_image(self):
        image = np.full((512, 512, 3), 128, dtype=np.uint8)
        result = detect_od_fovea(image)
        # Uniform image → OD and fovea detected at similar locations → distance too small
        assert result.confident is False

    def test_sigma_capped_at_maximum(self):
        image = _make_synthetic_fundus()
        result = detect_od_fovea(image)
        assert result.rotation_sigma_deg <= 15.0


class TestRotateToHorizontal:
    """Tests for rotation utility."""

    def test_zero_angle_is_identity(self):
        rng = np.random.RandomState(123)
        image = rng.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        rotated = rotate_to_horizontal(image, 0.0)
        np.testing.assert_array_equal(image, rotated)

    def test_preserves_shape(self):
        rng = np.random.RandomState(123)
        image = rng.randint(0, 255, (200, 300, 3), dtype=np.uint8)
        rotated = rotate_to_horizontal(image, 15.0)
        assert rotated.shape == image.shape

    def test_preserves_dtype(self):
        rng = np.random.RandomState(123)
        image = rng.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        rotated = rotate_to_horizontal(image, 10.0)
        assert rotated.dtype == np.uint8

    def test_180_rotation_flips(self):
        """Rotating 180° should roughly flip the image."""
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        image[10, 20] = 255  # single white pixel
        rotated = rotate_to_horizontal(image, 180.0)
        # After 180° rotation about center, (20,10) → roughly (79,89)
        assert rotated[10, 20, 0] == 0  # original pixel moved away
