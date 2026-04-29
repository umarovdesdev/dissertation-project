# Rotation Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Distribution | Truncated Gaussian | `augmentation_v4.py:147-148` |
| σ (sigma) | 13.0° | `default.yaml:54` |
| Clip boundary | ±40.0° | `default.yaml:55` |
| Adaptive sigma | Enabled | `default.yaml:32` |
| Fallback sigma | 13.0° | `default.yaml:33` |
| Probability | 100% (always applied) | — |
| Interpolation | Stochastic: 60% linear, 30% cubic, 10% nearest | `default.yaml:60` |
| Border mode | BORDER_REFLECT | `default.yaml:61` |

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
