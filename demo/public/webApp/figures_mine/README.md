# figures_mine/

Generated figures (analogs of Omarov's figures). See `../TASK.md` for the full plan.

| File                                    | How it is produced                                  | Status |
|-----------------------------------------|-----------------------------------------------------|--------|
| `fig1_per_class.png`                    | `../scripts/fig1_grid_per_class.py`                 | TODO   |
| `fig2_lesion_overlays.png`              | `../scripts/fig2_lesion_overlays.py`                | TODO   |
| `fig3_dataset_contents.png`             | `../scripts/fig3_dataset_contents.py`               | TODO   |
| `fig4_flowchart.png`                    | draw.io / Excalidraw / Mermaid (manual)             | TODO   |
| `fig5_architecture_artistic.png`        | NN-SVG / PlotNeuralNet (manual)                     | TODO   |
| `fig6_model_graph.png`                  | `../scripts/fig6_model_graph.py` (torchviz/Netron)  | TODO   |
| `fig7_pr_curves.png`                    | `../scripts/fig7_pr_curves.py` (needs `predictions.npz`) | TODO |
| `fig8_training_curves.png`              | `../scripts/copy_ready_figures.py` (copies `exp1/19_*`) | ready as `exp1/19_training_curves.png` |
| `fig9_confusion_matrix.png`             | `../scripts/copy_ready_figures.py` (copies `exp1/20_*`) | ready as `exp1/20_confusion_matrix.png` |
| `fig10_webapp_screenshot_1.png`         | Manual screenshot of the **top** of the demo page (upload form + walk-through cases + Run inference button) | TO RENAME from `image copy.png` |
| `fig10_webapp_screenshot_2.png`         | Manual screenshot of the **bottom** of the demo page (Model result + Per-eye prediction + Grad-CAM/attention + Confirm/Reject + Relabeling buffer) | TO RENAME from `image.png` |

## Renaming the current screenshots

```powershell
# from PowerShell in this folder:
Rename-Item ".\image copy.png" "fig10_webapp_screenshot_1.png"
Rename-Item ".\image.png"      "fig10_webapp_screenshot_2.png"
```

## Language policy

All generated images and scripts use **English only** (labels, captions, titles, comments). This matches the language used in the rest of the demo (`demo/src/tabs/*.js` defaults to English).
