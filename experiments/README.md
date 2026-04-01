# dr-classifier

Diabetic retinopathy (DR) grading from fundus images using deep learning.

Classifies fundus photographs into five DR severity grades (0–4) following
the International Clinical DR Disease Severity Scale.

## Quickstart

```bash
# 1. Install dependencies (Python 3.10+)
pip install -r requirements.txt

# 2. Place raw fundus images in data/raw/

# 3. Preprocess images
python -c "
from src.preprocessing.fundus_preprocessing import preprocess_dataset
print(preprocess_dataset('data/raw', 'data/processed'))
"

# 4. Generate train/val/test CSVs in data/splits/
#    (see docs/experimental_protocol.md)

# 5. Train
python src/training/train.py --config configs/training_config.yaml
```

## Project Layout

```
configs/               YAML training configuration
data/
  raw/                 Original fundus images (not committed)
  processed/           Preprocessed images (not committed)
  splits/              train.csv / val.csv / test.csv
docs/                  Experimental protocol and notes
experiments/           Per-experiment markdown logs and checkpoints
notebooks/             Exploratory notebooks
src/
  preprocessing/       Fundus image preprocessing pipeline
  models/              Model definitions (ResNet-50 baseline)
  training/            Training loop and utilities
  evaluation/          Metrics (QWK, AUC, F1)
```

## Grading Scale

| Grade | Stage                |
|-------|----------------------|
| 0     | No DR                |
| 1     | Mild NPDR            |
| 2     | Moderate NPDR        |
| 3     | Severe NPDR          |
| 4     | Proliferative DR     |

## Primary Metric

**Quadratic Weighted Kappa (QWK)** — standard metric for ordinal DR grading.
Target: QWK ≥ 0.85 on the test set.

## Configuration

All training hyperparameters live in `configs/training_config.yaml`.
See `docs/experimental_protocol.md` for the full workflow.
