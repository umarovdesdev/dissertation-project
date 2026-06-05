# webApp/scripts/

Figure-generation scripts. **All scripts produce English-only output** — captions,
titles, axis labels, table headers, and console messages.

See `../TASK.md` for the full per-figure plan and `../figures_mine/` for the
generated PNG/CSV files.

## Setup

```bash
pip install -r requirements.txt
# For fig6_model_graph.py: also install the Graphviz binary on the system
# (Windows: https://graphviz.org/download/, then ensure `dot.exe` is on PATH).
```

## Scripts

| Script                       | What it produces                                  | Inputs it reads                                                                 |
|------------------------------|---------------------------------------------------|---------------------------------------------------------------------------------|
| `fig1_grid_per_class.py`     | `figures_mine/fig1_per_class.png`                 | `demo/public/datasets/{idrid,messidor2,eyepacs,ddr}/samples/dr{0..4}/`           |
| `fig2_lesion_overlays.py`    | `figures_mine/fig2_lesion_overlays.png`           | `E:/datasets/IDRiD/A. Segmentation/{Original Images, All Segmentation Groundtruths}/...` |
| `fig3_dataset_contents.py`   | `figures_mine/fig3_dataset_contents.png` + `fig3_dataset_distribution.csv` | `demo/public/datasets/*/samples/` + `E:/datasets/EyePACS/trainLabels.csv` |
| `fig6_model_graph.py`        | `figures_mine/fig6_model_graph.png` + `fig6_model_summary.txt` (ONNX fallback: `fig6_model.onnx`) | `experiments/src/models/factory.py`                                          |
| `fig7_pr_curves.py`          | `figures_mine/fig7_pr_curves.png`                 | `figures_mine/data/predictions.npz` (y_true, y_prob) — must be created first   |
| `copy_ready_figures.py`      | `figures_mine/fig8_training_curves.png` + `fig9_confusion_matrix.png` | Existing `demo/public/images/results/exp1/19_*.png` and `20_*.png`        |

## Recommended run order

```powershell
cd E:\dissertation-project\demo\public\webApp\scripts

python copy_ready_figures.py     # fig8, fig9 (instant)
python fig1_grid_per_class.py    # fig1
python fig3_dataset_contents.py  # fig3 + distribution CSV
python fig2_lesion_overlays.py   # fig2 (needs IDRiD segmentation masks)
python fig6_model_graph.py       # fig6 (graphviz or ONNX fallback)
python fig7_pr_curves.py         # fig7 — requires predictions.npz first
```

## Figures produced outside Python

- **fig4_flowchart.png** — draw using draw.io / Excalidraw / Mermaid (a Mermaid
  stub is provided in `../TASK.md`). Keep all labels in English.
- **fig5_architecture_artistic.png** — use https://alexlenail.me/NN-SVG/ or
  PlotNeuralNet for a perspective-style architecture diagram.
- **fig10_webapp_screenshot_1.png / _2.png** — screenshots of the running React
  demo (`cd ../../../ && npm start`). The two-screenshot split corresponds to
  the top half (upload form + walk-through cases + Run inference) and the
  bottom half (Model result + Per-eye prediction + Grad-CAM + Confirm/Reject +
  Relabeling buffer) respectively.

## How to produce `predictions.npz` for fig7

`fig7_pr_curves.py` needs raw per-sample softmax outputs. Sketch of an
inference script (run inside the experiments env, with a trained Config D
checkpoint):

```python
import numpy as np, torch
from src.data.datasets import build_eyepacs_test_loader  # or your loader
from src.models.factory import create_model

model = create_model("efficientnet_b3", in_channels=4, num_classes=5)
model.load_state_dict(torch.load("path/to/config_d_best.pth", map_location="cpu"))
model.eval()

ys, ps = [], []
with torch.no_grad():
    for x, y in build_eyepacs_test_loader():
        logits = model(x)
        ps.append(torch.softmax(logits, dim=1).cpu().numpy())
        ys.append(y.cpu().numpy())
np.savez(
    r"E:/dissertation-project/demo/public/webApp/figures_mine/data/predictions.npz",
    y_true=np.concatenate(ys),
    y_prob=np.concatenate(ps),
)
```
