# Shear Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Shear range | [-2.0°, 2.0°] | `default.yaml: shear_range` |
| Distribution | Uniform | `augmentation_unified.py` (`_sample_affine_params`) |
| Probability | 0.3 (30%) | `default.yaml: shear_prob` |

## Algorithm

Horizontal shear applied with probability 30%:

```python
if np.random.rand() < 0.3:
    shear_deg = np.random.uniform(-2.0, 2.0)
    shear_rad = np.radians(shear_deg)
else:
    shear_rad = 0.0
```

Integrated into the unified affine matrix (M[0,1] += tan(shear_rad)).
Simulates slight camera tilt / non-perpendicular imaging angle.

## Demo images

- `left_min / right_min` — shear = -2.0° (maximum left skew)
- `left_max / right_max` — shear = 2.0° (maximum right skew)
