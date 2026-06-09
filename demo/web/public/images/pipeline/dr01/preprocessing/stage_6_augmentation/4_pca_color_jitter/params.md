# PCA Color Jitter

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| σ (sigma) | 0.1 | `default.yaml:62` |
| Distribution | Gaussian per component | `augmentation_unified.py:272` |
| Probability | 0.5 (50%) | `default.yaml:63` |
| Components | 3 (RGB PCA) | — |

## Algorithm

PCA color jitter (AlexNet-style) applied with probability 50%:

```python
alpha = np.random.normal(0.0, 0.1, size=3)
noise = eigvecs @ (alpha * eigvals)
pixel_out = pixel_in + noise   # per-channel additive shift
```

Adds noise along principal color axes of the training dataset.
Simulates natural illumination variations while preserving fundus color structure.

## PCA Eigenvalues

```
[1783.8425, 109.7929, 22.1162]
```

## PCA Eigenvectors

```
[-0.6750, -0.7056, +0.2155]
[-0.5850, +0.3340, -0.7390]
[-0.4495, +0.6250, +0.6382]
```

Note: PCA computed from demo fundus images (10 images, 1000 pixels each).
In production, PCA is computed from the full EyePACS training set
(5000 images × 1000 pixels, see `experiments/scripts/compute_pca_eigvecs.py`).

## Demo images

- `left_min / right_min` — α = [-σ, -σ, -σ] = [-0.1, -0.1, -0.1] (1σ negative shift)
- `left_max / right_max` — α = [+σ, +σ, +σ] = [+0.1, +0.1, +0.1] (1σ positive shift)
