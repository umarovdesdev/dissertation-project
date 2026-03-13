#!/usr/bin/env python3
"""Stage 3 verification: model definitions."""

import torch
from src.models import (
    create_model, get_gradcam_target_layer,
    freeze_base_layers, unfreeze_top_layers, get_two_stage_param_groups,
)

SEP = "=" * 60

def param_counts(model):
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total, trainable


cfg = {"pretrained": True, "num_classes": 5, "dropout": 0.4, "freeze_base": False}
x = torch.randn(2, 3, 512, 512)

# ── Test 1: ResNet-50 ──────────────────────────────────────────
print(SEP)
print("Test 1 — ResNet-50")
print(SEP)
model_rn = create_model("resnet50", cfg)
out = model_rn(x)
total, trainable = param_counts(model_rn)
print(f"  Output shape   : {list(out.shape)}")
print(f"  Total params   : {total:,}")
print(f"  Trainable      : {trainable:,}")
assert list(out.shape) == [2, 5]

# ── Test 2: EfficientNet-B3 ───────────────────────────────────
print(f"\n{SEP}")
print("Test 2 — EfficientNet-B3")
print(SEP)
model_b3 = create_model("efficientnet_b3", cfg)
out_b3 = model_b3(x)
total_b3, trainable_b3 = param_counts(model_b3)
print(f"  Output shape   : {list(out_b3.shape)}")
print(f"  Total params   : {total_b3:,}")
print(f"  Trainable      : {trainable_b3:,}")
assert list(out_b3.shape) == [2, 5]

# ── Test 3: EfficientNet-B4 + Grad-CAM target ─────────────────
print(f"\n{SEP}")
print("Test 3 — EfficientNet-B4 + Grad-CAM target layer")
print(SEP)
model_b4 = create_model("efficientnet_b4", cfg)
layer = get_gradcam_target_layer(model_b4, "b4")
print(f"  Target layer type : {type(layer).__name__}")
print(f"  Target layer      : {layer}")
out_b4 = model_b4(x)
assert list(out_b4.shape) == [2, 5]
print(f"  Forward pass OK   : {list(out_b4.shape)}")

# ── Test 4: Freeze / unfreeze ─────────────────────────────────
print(f"\n{SEP}")
print("Test 4 — freeze_base_layers / unfreeze_top_layers (B0)")
print(SEP)
model_b0 = create_model("efficientnet_b0", cfg)

freeze_base_layers(model_b0)
_, frozen_trainable = param_counts(model_b0)
print(f"  After freeze_base_layers — trainable: {frozen_trainable:,}")
assert frozen_trainable < 10_000, "Expected only classifier to be trainable"

unfrozen = unfreeze_top_layers(model_b0, num_blocks=3)
_, after_unfreeze = param_counts(model_b0)
print(f"  After unfreeze_top_layers(3) — trainable: {after_unfreeze:,}")
print(f"  Unfrozen param tensors: {len(unfrozen)}")
assert after_unfreeze > frozen_trainable

# ── Test 5: Two-stage param groups ────────────────────────────
print(f"\n{SEP}")
print("Test 5 — get_two_stage_param_groups")
print(SEP)
groups = get_two_stage_param_groups(model_b0, base_lr=0.0001, classifier_lr=0.001)
print(f"  Number of param groups : {len(groups)}")
for i, g in enumerate(groups):
    n = sum(p.numel() for p in g["params"])
    print(f"  Group {i}: lr={g['lr']}  params={n:,}")
assert len(groups) == 2
assert groups[0]["lr"] == 0.0001
assert groups[1]["lr"] == 0.001

print(f"\nAll 5 tests passed.")
