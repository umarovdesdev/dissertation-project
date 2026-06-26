# ColorJitter (Brightness / Contrast / Saturation / Hue)

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Brightness factor | [0.9, 1.1] | `default.yaml: color_jitter_brightness_range` |
| Contrast factor | [0.9, 1.1] | `default.yaml: color_jitter_contrast_range` |
| Saturation factor | [0.9, 1.1] | `default.yaml: color_jitter_saturation_range` |
| Hue shift | [-0.02, 0.02] (fraction of colour circle) | `default.yaml: color_jitter_hue_range` |
| Distribution | Uniform (each component) | `augmentation_unified.py` (`_apply_color_jitter`) |
| Probability | 0.5 (50%) per component, applied independently | `default.yaml: color_jitter_prob` |

## Algorithm

Each of the four components is sampled from its range and applied independently
with probability 50% (so a given image receives an arbitrary subset):

```python
# Brightness — scale RGB
if rand() < p: img = img * uniform(0.9, 1.1)
# Contrast — blend toward per-image grayscale mean
if rand() < p: img = (img - gray_mean) * uniform(0.9, 1.1) + gray_mean
# Saturation — blend toward per-pixel grayscale
if rand() < p: img = gray + uniform(0.9, 1.1) * (img - gray)
# Hue — rotate H channel in HSV by uniform(-0.02, 0.02) * 180
```

Replaces the previous PCA colour jitter. Bands are kept narrow so the
perturbation stays within plausible acquisition variation and does not
distort diagnostic lesion colour. Brightness/contrast operate in RGB;
saturation/hue operate in HSV.

## Demo images

- `left_min / right_min` — all factors at the low end (brightness/contrast/saturation = 0.9, hue = -0.02)
- `left_max / right_max` — all factors at the high end (brightness/contrast/saturation = 1.1, hue = +0.02)
