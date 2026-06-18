"""Synthetic end-to-end smoke test: train -> infer -> eval, no dataset.

Proves the full pipeline executes without the IDRiD dataset:
  1. build the model;
  2. run 2 optimizer steps on randomly generated images + target heatmaps
     (both DSNT and heatmap losses exercised);
  3. run ``detect_od_fovea`` on a synthetic image (contract check);
  4. run the eval aggregation + Spearman on synthetic records;
  5. render a montage from synthetic records.

This is NOT a training run and makes no accuracy claim. Requires torch + timm.

Usage::

    python scripts/smoke_test.py
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    try:
        import torch
        import timm  # noqa: F401
    except Exception as exc:  # pragma: no cover
        print(f"SKIP: torch/timm not available ({exc}). "
              "Run inside the `dr-classifier` conda env.")
        return 0

    from src.model import build_model
    from src.losses import build_loss
    from src.geometry import render_gaussian_heatmap
    from src.infer import detect_od_fovea, reset_cache
    from src.eval import _summarize, make_montage

    torch.manual_seed(42)
    np.random.seed(42)

    input_size, heatmap_size = 256, 64  # smaller for a fast smoke run
    model_cfg = {"backbone": "resnet18", "pretrained": False,
                 "out_channels": 2, "decoder_channels": [128, 64, 32, 16]}
    model = build_model(model_cfg, heatmap_size)
    print(f"[1/5] built model ({sum(p.numel() for p in model.parameters()):,} params)")

    # --- 2 training steps, both losses ---
    sigma = 0.02 * heatmap_size
    sigma_norm = 2.0 * sigma / heatmap_size
    for loss_type in ("dsnt", "heatmap"):
        criterion = build_loss({"type": loss_type, "js_weight": 1.0,
                                "heatmap_loss": "mse"}, sigma_norm)
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        for step in range(2):
            b = 2
            imgs = torch.rand(b, 3, input_size, input_size)
            hms = np.zeros((b, 2, heatmap_size, heatmap_size), dtype=np.float32)
            coords = np.zeros((b, 2, 2), dtype=np.float32)
            for bi in range(b):
                for ci in range(2):
                    gx = np.random.uniform(10, heatmap_size - 10)
                    gy = np.random.uniform(10, heatmap_size - 10)
                    hms[bi, ci] = render_gaussian_heatmap(gx, gy, heatmap_size, sigma)
                    coords[bi, ci] = (2 * gx / heatmap_size - 1, 2 * gy / heatmap_size - 1)
            out = model(imgs)
            target = (torch.from_numpy(coords) if loss_type == "dsnt"
                      else torch.from_numpy(hms))
            loss, parts = criterion(out, target)
            opt.zero_grad()
            loss.backward()
            opt.step()
        print(f"[2/5] {loss_type} loss step ok (loss={float(loss):.4f}, {parts})")

    # --- inference contract ---
    reset_cache()
    h, w = 360, 480
    img = np.zeros((h, w, 3), dtype=np.uint8)
    cy, cx, r = h // 2, w // 2, int(min(h, w) * 0.45)
    ys, xs = np.mgrid[0:h, 0:w]
    img[(xs - cx) ** 2 + (ys - cy) ** 2 <= r * r] = (180, 90, 60)
    res = detect_od_fovea(img, device="cpu")
    assert res.od_heatmap.shape == (h, w)
    assert 0.0 <= res.od_confidence <= 1.0
    print(f"[3/5] detect_od_fovea ok: OD={res.od_center} fovea={res.fovea_center} "
          f"od_conf={res.od_confidence:.3f} fovea_conf={res.fovea_confidence:.3f} "
          f"confident={res.confident}")

    # --- eval aggregation + Spearman on synthetic records ---
    records = []
    for i in range(8):
        oerr = float(np.random.uniform(5, 200))
        ferr = float(np.random.uniform(5, 300))
        records.append({
            "id": f"SYN_{i}", "split": "test",
            "od_pred": [10, 10], "od_gt": [12, 12],
            "fovea_pred": [20, 20], "fovea_gt": [25, 25],
            "od_radius": 40.0,
            "od_err_px": oerr, "fovea_err_px": ferr,
            "od_err_norm": oerr / 600, "fovea_err_norm": ferr / 600,
            "od_err_radii": oerr / 40, "fovea_err_radii": ferr / 40,
            "od_confidence": float(np.clip(1 - oerr / 250, 0, 1)),
            "fovea_confidence": float(np.clip(1 - ferr / 350, 0, 1)),
            "confident": True,
            "od_sigma_proxy": oerr / 250, "fovea_sigma_proxy": ferr / 350,
        })
    summary = _summarize(records)
    rho = summary["confidence_vs_error"]["fovea_spearman_sigma_vs_err"]["rho"]
    print(f"[4/5] eval summary ok: fovea median "
          f"{summary['fovea']['error_px']['median']:.1f}px, "
          f"confidence_vs_error rho={rho:.3f}")

    montage = make_montage(records, {}, n=0)  # no images on disk -> None
    print(f"[5/5] montage path ok (montage={'None (no images)' if montage is None else montage.shape})")

    print("\nSMOKE TEST PASSED: train -> infer -> eval pipeline executes end-to-end.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
