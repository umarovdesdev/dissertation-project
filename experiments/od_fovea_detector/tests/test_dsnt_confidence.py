"""Torch-free tests for DSNT decoding and confidence."""

from __future__ import annotations

import pathlib
import sys
import unittest

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.confidence import decode_heatmap  # noqa: E402
from src.dsnt import np_dsnt, norm_to_pixel  # noqa: E402
from src.geometry import render_gaussian_heatmap  # noqa: E402


class TestDSNTDecode(unittest.TestCase):
    def test_recovers_gaussian_peak(self) -> None:
        """np_dsnt soft-argmax recovers a synthetic Gaussian peak (sub-pixel)."""
        size = 128
        for (gx, gy) in [(30.0, 70.0), (64.0, 64.0), (10.0, 100.0)]:
            hm = render_gaussian_heatmap(gx, gy, size, sigma=2.56)
            xn, yn = np_dsnt(hm)
            x_px = float(norm_to_pixel(xn, size))
            y_px = float(norm_to_pixel(yn, size))
            self.assertAlmostEqual(x_px, gx, delta=0.5)
            self.assertAlmostEqual(y_px, gy, delta=0.5)


class TestConfidence(unittest.TestCase):
    def test_sharp_more_confident_than_diffuse(self) -> None:
        """A sharp peak must yield higher confidence than a diffuse map."""
        size = 128
        sigma_ref = 0.05 * size
        sharp = render_gaussian_heatmap(64.0, 64.0, size, sigma=2.0)
        diffuse = render_gaussian_heatmap(64.0, 64.0, size, sigma=25.0)
        d_sharp = decode_heatmap(sharp, sigma_ref)
        d_diffuse = decode_heatmap(diffuse, sigma_ref)
        self.assertGreater(d_sharp.confidence, d_diffuse.confidence)
        self.assertLess(d_sharp.sigma_eff, d_diffuse.sigma_eff)
        self.assertTrue(0.0 <= d_diffuse.confidence <= d_sharp.confidence <= 1.0)

    def test_uniform_map_low_confidence(self) -> None:
        size = 64
        uniform = np.full((size, size), 1.0 / (size * size), dtype=np.float32)
        d = decode_heatmap(uniform, sigma_ref=0.05 * size)
        self.assertLess(d.confidence, 0.2)

    def test_confidence_in_range(self) -> None:
        size = 128
        hm = render_gaussian_heatmap(40.0, 90.0, size, sigma=3.0)
        d = decode_heatmap(hm, sigma_ref=0.05 * size)
        self.assertTrue(0.0 <= d.confidence <= 1.0)
        self.assertTrue(0.0 <= d.p_max <= 1.0)


if __name__ == "__main__":
    unittest.main()
