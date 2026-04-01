#!/usr/bin/env python3
"""Exp4 smoke test: Grad-CAM + IoU/ALO on one IDRiD image (no training needed).

Uses ImageNet pretrained EfficientNet-B4 weights to verify the full
explainability pipeline without any DR training.

Steps
-----
1. Load first IDRiD image that has at least one lesion mask.
2. Create pretrained EfficientNet-B4 (ImageNet weights only — no DR training).
3. Generate Grad-CAM heatmap.
4. Compute IoU and ALO against available lesion masks.
5. Save comparison figure to outputs/figures/gradcam_test.png.
6. Print IoU and ALO values per lesion type.
"""

import json
from pathlib import Path

import cv2
import numpy as np
import torch

from src.data.datasets import IDRiDDataset
from src.explainability import (
    GradCAMGenerator,
    compute_alo_per_lesion_type,
    compute_attention_overlap,
    compute_iou_per_lesion_type,
    create_comparison_figure,
    overlay_gradcam,
)
from src.models.efficientnet import create_efficientnet, get_gradcam_target_layer
from src.preprocessing.pipeline import PreprocessingPipeline
from src.utils.config import load_config
from src.utils.seed import set_seed

SEP = "=" * 65

config  = load_config("configs/default.yaml")
set_seed(config.get("seed", 42))
device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")

idrid_root  = config["paths"]["idrid"]
idrid_imgs  = str(Path(idrid_root) / "B. Disease Grading" /
                  "1. Original Images" / "a. Training Set")
idrid_csv   = str(Path(idrid_root) / "B. Disease Grading" / "2. Groundtruths" /
                  "a. IDRiD_Disease Grading_Training Labels.csv")
idrid_masks = str(Path(idrid_root) / "A. Segmentation" /
                  "2. All Segmentation Groundtruths" / "a. Training Set")

# ── Load IDRiD dataset ────────────────────────────────────────────────────────
print(SEP)
print("Loading IDRiD dataset …")
print(SEP)

idrid_ds = IDRiDDataset.from_directory(
    root=idrid_imgs,
    labels_csv=idrid_csv,
    lesion_mask_dir=idrid_masks,
)
print(f"  {len(idrid_ds)} images | {idrid_ds.count_images_with_masks()} with masks")

# Find first image with at least one mask
target_idx = None
for i in range(len(idrid_ds)):
    if idrid_ds.get_lesion_masks(i) is not None:
        target_idx = i
        break

assert target_idx is not None, "No IDRiD images with lesion masks found!"
stem     = idrid_ds.image_stems[target_idx]
dr_grade = idrid_ds.labels[target_idx]
masks    = idrid_ds.get_lesion_masks(target_idx)
print(f"  Using: {stem}  grade={dr_grade}  masks={list(masks.keys())}")

# ── Build preprocessing pipelines ────────────────────────────────────────────
preproc_cfg = config["preprocessing"]
kwargs = {
    "target_size":      preproc_cfg.get("target_size", 512),
    "clahe_clip_limit": preproc_cfg.get("clahe", {}).get("clip_limit", 2.0),
    "clahe_grid_size":  preproc_cfg.get("clahe", {}).get("tile_grid_size", [8, 8]),
    "saturation_scale": preproc_cfg.get("hsv", {}).get("saturation_scale", 1.2),
    "value_scale":      preproc_cfg.get("hsv", {}).get("value_scale", 1.1),
}
pipeline_baseline = PreprocessingPipeline.create_baseline(target_size=kwargs["target_size"])
pipeline_full     = PreprocessingPipeline.create_full(kwargs)

# ── Load and preprocess image ─────────────────────────────────────────────────
raw = cv2.imread(str(idrid_ds.image_paths[target_idx]))
assert raw is not None, f"Cannot load {idrid_ds.image_paths[target_idx]}"

img_base = pipeline_baseline(raw)
img_full = pipeline_full(raw)

def to_tensor(img: np.ndarray) -> torch.Tensor:
    """Convert HWC uint8/float32 to (1,C,H,W) float32 on device."""
    if img.dtype == np.uint8:
        img = img.astype(np.float32) / 255.0
    t = torch.from_numpy(
        np.ascontiguousarray(img.transpose(2, 0, 1))
    ).unsqueeze(0).to(device)
    return t

t_base = to_tensor(img_base)
t_full = to_tensor(img_full)

# ── Create model (ImageNet pretrained — no DR fine-tuning for smoke test) ──────
print(f"\n{SEP}")
print("Creating pretrained EfficientNet-B4 (ImageNet weights, no DR training)")
print(SEP)

model_cfg = config["models"]["efficientnet_b4"]
model = create_efficientnet(
    variant="b4",
    num_classes=model_cfg["num_classes"],
    pretrained=model_cfg["pretrained"],
    dropout=model_cfg["dropout"],
)
model = model.to(device).eval()
target_layer = get_gradcam_target_layer(model, variant="b4")
print(f"  Target layer: {type(target_layer).__name__}  "
      f"(model.conv_head)")

# ── Generate Grad-CAM heatmaps ────────────────────────────────────────────────
print(f"\n{SEP}")
print("Generating Grad-CAM heatmaps …")
print(SEP)

cam = GradCAMGenerator(model, target_layer, device=str(device))
hm_baseline = cam.generate(t_base, target_class=None)
hm_full     = cam.generate(t_full, target_class=None)

assert hm_baseline.dtype == np.float32, "Heatmap must be float32"
assert hm_baseline.shape == (512, 512), f"Unexpected shape: {hm_baseline.shape}"
assert 0.0 <= hm_baseline.min() and hm_baseline.max() <= 1.0, "Heatmap out of [0,1]"
print(f"  Baseline heatmap: shape={hm_baseline.shape} "
      f"min={hm_baseline.min():.3f} max={hm_baseline.max():.3f}")
print(f"  Full heatmap:     shape={hm_full.shape} "
      f"min={hm_full.min():.3f} max={hm_full.max():.3f}")

# ── Compute IoU and ALO per lesion type ───────────────────────────────────────
print(f"\n{SEP}")
print("Computing IoU and ALO per lesion type …")
print(SEP)

iou_base = compute_iou_per_lesion_type(hm_baseline, masks)
iou_full = compute_iou_per_lesion_type(hm_full,     masks)
alo_base = compute_alo_per_lesion_type(hm_baseline, masks)
alo_full = compute_alo_per_lesion_type(hm_full,     masks)
attn_overlap = compute_attention_overlap(hm_full, hm_baseline)

print(f"  Attention overlap (IoU between the two heatmaps): {attn_overlap:.4f}")
print(f"\n  {'Lesion type':<22} {'IoU base':>10} {'IoU full':>10} "
      f"{'ALO base':>10} {'ALO full':>10}")
print(f"  {'-'*65}")
all_lesion_types = ["microaneurysms", "haemorrhages", "hard_exudates", "soft_exudates"]
for lt in all_lesion_types:
    ib = iou_base.get(lt, float("nan"))
    if_ = iou_full.get(lt, float("nan"))
    ab = alo_base.get(lt, float("nan"))
    af = alo_full.get(lt, float("nan"))
    print(f"  {lt:<22} {ib:>10.4f} {if_:>10.4f} {ab:>10.4f} {af:>10.4f}")

# ── Save comparison figure ────────────────────────────────────────────────────
print(f"\n{SEP}")
print("Saving comparison figure …")
print(SEP)

figures_dir = Path("outputs/figures")
figures_dir.mkdir(parents=True, exist_ok=True)
fig_path = figures_dir / "gradcam_test.png"

create_comparison_figure(
    image=img_base,
    heatmap_baseline=hm_baseline,
    heatmap_preproc=hm_full,
    lesion_masks=masks,
    save_path=fig_path,
)
assert fig_path.exists(), f"Figure not saved: {fig_path}"
print(f"  Saved → {fig_path}")

# ── Verify overlay_gradcam ───────────────────────────────────────────────────
overlay = overlay_gradcam(img_base, hm_baseline, alpha=0.4)
assert overlay.dtype == np.uint8,           "Overlay must be uint8"
assert overlay.shape == img_base.shape[:3], "Overlay must match image shape"
assert overlay.ndim == 3,                   "Overlay must be 3-channel"
print("  overlay_gradcam assertions passed.")

print(f"\nAll Exp4 smoke-test assertions passed.")
print("NC-14: Grad-CAM activation is interpretability evidence only, "
      "not clinical lesion localization.")
