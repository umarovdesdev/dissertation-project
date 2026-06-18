"""Torch-gated test: detect_od_fovea returns a well-formed ODFoveaResult.

Uses randomly-initialized weights (no trained checkpoint required) on a
synthetic image. This is a SHAPE/CONTRACT check, not an accuracy check. Skips
cleanly when torch/timm are unavailable.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

try:
    import torch  # noqa: F401
    import timm  # noqa: F401
    _HAS = True
except Exception:
    _HAS = False


@unittest.skipUnless(_HAS, "torch/timm not available")
class TestInferContract(unittest.TestCase):
    def test_result_contract(self) -> None:
        from src.infer import ODFoveaResult, detect_od_fovea, reset_cache

        reset_cache()
        rng = np.random.default_rng(0)
        h, w = 480, 640
        img = np.zeros((h, w, 3), dtype=np.uint8)
        cy, cx = h // 2, w // 2
        r = int(min(h, w) * 0.45)
        ys, xs = np.mgrid[0:h, 0:w]
        img[(xs - cx) ** 2 + (ys - cy) ** 2 <= r * r] = (180, 90, 60)

        res = detect_od_fovea(img, device="cpu")
        self.assertIsInstance(res, ODFoveaResult)
        # Coordinates are in input-image pixels.
        for cx_, cy_ in (res.od_center, res.fovea_center):
            self.assertTrue(-w <= cx_ <= 2 * w)
            self.assertTrue(-h <= cy_ <= 2 * h)
        self.assertTrue(0.0 <= res.od_confidence <= 1.0)
        self.assertTrue(0.0 <= res.fovea_confidence <= 1.0)
        self.assertIsInstance(res.confident, bool)
        self.assertLessEqual(res.rotation_sigma_deg, 15.0 + 1e-6)
        self.assertEqual(res.od_heatmap.shape, (h, w))
        self.assertEqual(res.fovea_heatmap.shape, (h, w))
        self.assertGreaterEqual(res.distance, 0.0)

    def test_no_heatmaps_flag(self) -> None:
        from src.infer import detect_od_fovea, reset_cache

        reset_cache()
        img = np.full((300, 300, 3), 100, dtype=np.uint8)
        res = detect_od_fovea(img, device="cpu", return_heatmaps=False)
        self.assertIsNone(res.od_heatmap)
        self.assertIsNone(res.fovea_heatmap)


if __name__ == "__main__":
    unittest.main()
