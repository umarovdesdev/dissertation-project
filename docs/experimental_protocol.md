# Experimental Protocol

## Dataset Preparation

### 1. Data Acquisition
Place raw fundus images under `data/raw/` organised by class label or dataset source.
Accepted formats: PNG, JPEG, TIFF.

### 2. Preprocessing
Run the preprocessing pipeline to produce standardised 224×224 CLAHE-enhanced images:

```bash
python -c "
from src.preprocessing.fundus_preprocessing import preprocess_dataset
counts = preprocess_dataset('data/raw', 'data/processed', image_size=224)
print(counts)
"
```

### 3. Dataset Splits
Generate `data/splits/train.csv`, `data/splits/val.csv`, and `data/splits/test.csv`.
Each CSV must contain at minimum:
- `image_path` — absolute or project-relative path to the processed image
- `label`      — integer DR grade (0–4)

Recommended split ratio: 70 / 15 / 15 (train / val / test), stratified by label.

---

## Training

### Standard run
```bash
python src/training/train.py --config configs/training_config.yaml
```

### Resume from checkpoint
```bash
python src/training/train.py --config configs/training_config.yaml \
    --resume experiments/checkpoints/last.pt
```

Checkpoints are saved to `experiments/checkpoints/`:
- `best.pt` — highest val QWK so far
- `last.pt` — most recent epoch (for resuming)

---

## Evaluation

Load `best.pt` and evaluate on the held-out test set:

```python
import torch, yaml
from src.models.resnet50_model import build_model
from src.evaluation.metrics import compute_metrics, print_metrics

with open("configs/training_config.yaml") as f:
    config = yaml.safe_load(f)

model = build_model(config["model"])
ckpt = torch.load("experiments/checkpoints/best.pt", map_location="cpu")
model.load_state_dict(ckpt["model_state_dict"])
model.eval()

# ... run inference on test set, then:
metrics = compute_metrics(y_true, y_pred, y_prob)
print_metrics(metrics)
```

---

## Experiment Logging

For each experiment:
1. Copy `experiments/exp1_baseline.md` to `experiments/expN_<short_name>.md`.
2. Record the exact config diff from the baseline.
3. Fill in the results table after evaluation.
4. Note observations and next steps.

---

## Grading Scale Reference

| Grade | Clinical Stage       | Approximate Prevalence |
|-------|----------------------|------------------------|
| 0     | No DR                | ~73 %                  |
| 1     | Mild NPDR            | ~7 %                   |
| 2     | Moderate NPDR        | ~15 %                  |
| 3     | Severe NPDR          | ~2 %                   |
| 4     | Proliferative DR     | ~3 %                   |

Class imbalance is severe — factor this into loss function and sampling strategy.

---

## Reproducibility Checklist
- [ ] Random seeds fixed (`torch.manual_seed`, `np.random.seed`)
- [ ] Config file committed alongside experiment notes
- [ ] Dataset version / source recorded
- [ ] Preprocessing parameters recorded
- [ ] Checkpoint saved and linked in experiment notes
