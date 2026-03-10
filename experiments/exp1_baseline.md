# Experiment 1 — ResNet-50 Baseline

## Objective
Establish a baseline quadratic weighted kappa (QWK) score for 5-class DR grading
using a pretrained ResNet-50 with minimal augmentation.

## Configuration
- Config file: `configs/training_config.yaml`
- Model: ResNet-50 (ImageNet pretrained)
- Epochs: 50
- Batch size: 32
- Optimiser: Adam (lr=1e-4, weight_decay=1e-4)
- Scheduler: Cosine annealing
- Loss: CrossEntropyLoss
- Image size: 224×224
- Augmentation: horizontal flip, ±15° rotation, colour jitter

## Dataset
<!-- Fill in dataset name, version, and split sizes -->
- Dataset:
- Train:
- Val:
- Test:

## Results

| Metric            | Train | Val | Test |
|-------------------|-------|-----|------|
| Accuracy          |       |     |      |
| Quadratic Kappa   |       |     |      |
| Macro AUC-ROC     |       |     |      |
| Macro F1          |       |     |      |

## Per-class Val Recall

| Grade | Recall |
|-------|--------|
| 0 (No DR)          |  |
| 1 (Mild)           |  |
| 2 (Moderate)       |  |
| 3 (Severe)         |  |
| 4 (Proliferative)  |  |

## Observations
<!-- Fill in after running the experiment -->

## Next Steps
<!-- Potential improvements based on results -->
- [ ] Class-weighted loss / focal loss for grade imbalance
- [ ] Stronger augmentation (GridDistortion, elastic transforms)
- [ ] Larger input resolution (384×384, 512×512)
- [ ] EfficientNet / ViT backbone comparison
- [ ] Test-time augmentation (TTA)
