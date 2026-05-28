# Scale Augmentation (Zoom + Stretch)

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Zoom range | [0.9, 1.1] | `default.yaml:56` |
| Zoom distribution | Log-uniform | `augmentation_v4.py:151-155` |
| Stretch range | [0.952381, 1.05] (= [1/1.05, 1.05]) | `default.yaml:57` |
| Stretch distribution | Log-uniform | `augmentation_v4.py:159-163` |
| Probability | 100% (always applied) | — |

## Algorithm

Zoom (isotropic) and stretch (anisotropic) combined into one affine:

```python
log_zoom = np.random.uniform(np.log(0.9), np.log(1.1))
zoom = np.exp(log_zoom)

log_stretch = np.random.uniform(np.log(1/1.05), np.log(1.05))
stretch = np.exp(log_stretch)

sx = zoom * stretch   # horizontal scale
sy = zoom / stretch   # vertical scale
```

Zoom controls overall magnification, stretch adds slight anisotropy
(simulates different camera distances / fundus curvature).

## Demo images

- `left_min / right_min` — zoom = 0.9 (10% zoom out)
- `left_max / right_max` — zoom = 1.1 (10% zoom in)
