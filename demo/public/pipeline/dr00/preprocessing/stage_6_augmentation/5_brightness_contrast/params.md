# Brightness / Contrast Augmentation

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Contrast (α) range | [0.9, 1.1] | `default.yaml:63` |
| Brightness (β) range | [-10.0, 10.0] | `default.yaml:64` |
| Distribution | Uniform (both) | `augmentation_unified.py:290-291` |
| Probability | 0.5 (50%) | `default.yaml:65` |

## Algorithm

Simple linear transform applied with probability 50%:

```python
alpha = np.random.uniform(0.9, 1.1)   # contrast
beta = np.random.uniform(-10.0, 10.0)    # brightness (uint8)
pixel_out = pixel_in * alpha + beta
```

- α < 1 reduces contrast, α > 1 increases contrast
- β < 0 darkens, β > 0 brightens

Applied after CLAHE — these are small perturbations around already-normalized contrast.
Makes the model robust to inter-device brightness/contrast differences.

## Demo images

- `left_min / right_min` — α=0.9, β=-10.0 (darker, less contrast)
- `left_max / right_max` — α=1.1, β=10.0 (brighter, more contrast)
