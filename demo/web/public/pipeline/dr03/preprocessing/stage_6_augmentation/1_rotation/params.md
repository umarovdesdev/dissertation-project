# Rotation Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Distribution | Truncated Gaussian | `augmentation_unified.py` (`_sample_affine_params`) |
| σ (sigma) | 13.0° | `default.yaml: rotation_sigma` |
| Clip boundary | ±40.0° | `default.yaml: rotation_clip` |
| Adaptive sigma | Enabled | `default.yaml: adaptive_rotation_sigma` |
| Fallback sigma | 13.0° | `default.yaml: fallback_rotation_sigma` |
| Probability | 100% (always applied) | — |
| Interpolation | Stochastic: 60% linear, 30% cubic, 10% nearest | `default.yaml: interp_weights` |
| Border mode | BORDER_REFLECT | `default.yaml: border_mode` |

## Algorithm

Rotation angle sampled from truncated Gaussian:

```python
theta = np.random.normal(0.0, rotation_sigma)
theta = np.clip(theta, -rotation_clip, rotation_clip)
```

**Adaptive sigma** (key novelty): when OD-fovea detection succeeds,
σ is derived from the angular uncertainty of OD-fovea axis localization.
When detection fails, fallback σ = 13.0° is used.

~68% of samples fall within ±13.0°, ~95% within ±26.0°.
Hard clip at ±40.0° prevents extreme rotations.

## Demo images

- `left.png / right.png` — source images (pre-augmentation)

Rotation demo with min/max angles will be added separately as part of the
adaptive rotation novelty presentation.
