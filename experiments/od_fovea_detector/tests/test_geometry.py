"""Torch-free tests for the FOV-crop affine and target-heatmap rendering."""

from __future__ import annotations

import pathlib
import sys
import unittest

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.geometry import (  # noqa: E402
    crop_and_resize,
    render_gaussian_heatmap,
)


def _synthetic_fundus(h: int = 600, w: int = 800, radius_frac: float = 0.45) -> np.ndarray:
    """Make a synthetic fundus: bright disc on a dark vignetted background."""
    img = np.zeros((h, w, 3), dtype=np.uint8)
    cy, cx = h // 2, w // 2
    r = int(min(h, w) * radius_frac)
    ys, xs = np.mgrid[0:h, 0:w]
    disc = (xs - cx) ** 2 + (ys - cy) ** 2 <= r * r
    img[disc] = (180, 90, 60)
    return img


class TestFovAffine(unittest.TestCase):
    def test_round_trip_identity(self) -> None:
        """forward(apply) then inverse(invert) recovers the input point."""
        img = _synthetic_fundus()
        _frame, _mask, t = crop_and_resize(img, target_size=512)
        rng = np.random.default_rng(0)
        for _ in range(200):
            x = float(rng.uniform(0, img.shape[1]))
            y = float(rng.uniform(0, img.shape[0]))
            fx, fy = t.apply(x, y)
            rx, ry = t.invert(fx, fy)
            self.assertAlmostEqual(x, rx, places=4)
            self.assertAlmostEqual(y, ry, places=4)

    def test_frame_shape_and_mask(self) -> None:
        img = _synthetic_fundus()
        frame, mask, t = crop_and_resize(img, target_size=512)
        self.assertEqual(frame.shape, (512, 512, 3))
        self.assertEqual(mask.shape, (512, 512))
        self.assertTrue(0.0 <= mask.min() <= mask.max() <= 1.0)
        self.assertEqual(t.target_size, 512)

    def test_center_maps_into_frame(self) -> None:
        """The disc center should land inside the FOV frame after transform."""
        img = _synthetic_fundus()
        _frame, _mask, t = crop_and_resize(img, target_size=512)
        cx, cy = img.shape[1] / 2, img.shape[0] / 2
        fx, fy = t.apply(cx, cy)
        self.assertTrue(0 <= fx <= 512)
        self.assertTrue(0 <= fy <= 512)


class TestHeatmapRender(unittest.TestCase):
    def test_sums_to_one(self) -> None:
        hm = render_gaussian_heatmap(64.0, 64.0, 128, sigma=2.56)
        self.assertAlmostEqual(float(hm.sum()), 1.0, places=4)

    def test_peak_at_center(self) -> None:
        hm = render_gaussian_heatmap(30.0, 70.0, 128, sigma=2.56)
        peak = np.unravel_index(int(np.argmax(hm)), hm.shape)  # (row, col)=(y, x)
        self.assertLessEqual(abs(peak[1] - 30), 1)
        self.assertLessEqual(abs(peak[0] - 70), 1)


if __name__ == "__main__":
    unittest.main()
