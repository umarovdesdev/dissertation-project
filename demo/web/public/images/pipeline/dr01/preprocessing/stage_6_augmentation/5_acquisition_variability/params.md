# Acquisition Variability (Gaussian Noise + JPEG Compression)

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Gaussian noise σ | [2.0, 6.0] (8-bit RGB) | `default.yaml: gaussian_noise_sigma_range` |
| Noise probability | 0.15 (15%) | `default.yaml: gaussian_noise_prob` |
| JPEG quality | [70, 100] | `default.yaml: jpeg_quality_range` |
| JPEG probability | 0.2 (20%) | `default.yaml: jpeg_prob` |
| Distribution | Uniform (both) | `augmentation_unified.py` (`_apply_gaussian_noise`, `_apply_jpeg_compression`) |

## Algorithm

Two independent degradations that simulate real acquisition/storage:

```python
# Gaussian noise (sensor / acquisition noise)
if rand() < 0.15:
    sigma = uniform(2.0, 6.0)
    img = clip(img + normal(0, sigma), 0, 255)

# JPEG re-compression (storage block / chroma artifacts)
if rand() < 0.2:
    quality = randint(70, 100)
    img = jpeg_decode(jpeg_encode(img, quality))
```

Both probabilities are kept low: the goal is to expose the network to
occasional degraded examples, not to train predominantly on corrupted data.

## Demo images

- `left_min / right_min` — light degradation (σ = 2.0, JPEG quality = 100)
- `left_max / right_max` — heavy degradation (σ = 6.0, JPEG quality = 70)
