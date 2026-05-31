# TASK-fix.md — Corrections to the first generation pass

This file lists everything that must be fixed in
`E:\dissertation-project\demo\public\webApp\figures_mine\`. All scripts and all
rendered figure text remain **English only**. Do not touch `TASK.md`,
`figures_omarov\`, or the `figures_mine\README.md`.

The reference for the project's hypothesis-consistent generation style is
`E:\dissertation-project\demo\generate_charts_15_28.py` — in particular
`chart_24()` (per-class ROC curves) and the `CLS`, `CLS_AUC` tables at the
top of the file.

---

## Figure 1 — Per-class sample grid

**Symptom:** the `(a) DR 0 — No DR` … `(e) DR 4 — Proliferative DR` row labels
are drawn directly under each row using `fig.text` and visually collide with
the next row of images, so the bottom of every label is clipped by the image
above it.

**Fix:**

1. Increase the inter-row gap. In `scripts/fig1_grid_per_class.py`, change
   `gridspec_kw={"wspace": 0.04, "hspace": 0.12}` to
   `gridspec_kw={"wspace": 0.04, "hspace": 0.40}`.
2. Move the row label out of the `fig.text` overlay and place it as the
   left-column axis title for the row, or as `ax.set_ylabel` on the leftmost
   axis with `labelpad=18, rotation=0, ha='right', va='center', fontweight='bold'`.
   Either approach avoids overlap because matplotlib reserves space for axis
   text but not for `fig.text`.
3. Keep all five English row labels exactly: `(a) DR 0 — No DR`,
   `(b) DR 1 — Mild NPDR`, `(c) DR 2 — Moderate NPDR`,
   `(d) DR 3 — Severe NPDR`, `(e) DR 4 — Proliferative DR`.
4. Regenerate: `python fig1_grid_per_class.py`.

---

## Figure 2 — Lesion overlays

**Symptoms:**

- The red contours are not visible. The script draws contours with
  `cv2.drawContours(..., thickness=3)` on the **full-resolution** RGB image
  (~4000 px wide); when matplotlib down-samples to ~400 px for the cell,
  3-pixel lines collapse to sub-pixel and disappear.
- The right-side chevron contains two overlapping text labels (`(a)` and
  `Microaneurysms`) drawn at the same position, so they print on top of each
  other.

**Fix:**

1. Change the overlay color from red to **teal** (`#2a9d8f`) — it is far
   more visible against the brown/orange fundus background and matches the
   accent color used elsewhere in the project (see `BLUE`, `TEAL`, `CORAL`
   constants in `generate_charts_15_28.py`).
2. Make contours actually visible:
   - Either bump `CONTOUR_THICKNESS` from `3` to `12` (so they survive
     down-sampling); or
   - Better: down-sample the RGB to ~512 px first, down-sample the mask to
     match with `cv2.INTER_NEAREST`, then call `cv2.drawContours(...,
     thickness=2)` at the final resolution before passing to matplotlib.
3. Replace the two-text chevron with a single combined string. For row (a)
   the chevron should display one centered line: `(a) Microaneurysms`
   (with `fontsize=11, fontweight='bold'`). Same pattern for rows (b)–(e).
   Remove the second `cax.text(...)` call entirely.
4. Keep the same five rows in the same order:
   `(a) Microaneurysms`, `(b) Haemorrhages`, `(c) Hard Exudates`,
   `(d) Soft Exudates`, `(e) Optic Disc`.
5. Regenerate: `python fig2_lesion_overlays.py`.

---

## Figure 4 — System flowchart

**Symptom:** some text inside the boxes is partly invisible — characters
appear "broken" or partially clipped at the box edges (caused by Graphviz
auto-sizing the box too tight around DejaVu Sans glyph metrics).

**Fix:** in `scripts/fig4_flowchart.py`:

1. Set explicit width with `node[width=3.2, fixedsize=false, margin="0.30,0.18"]`
   so each box has comfortable horizontal padding.
2. Use a font that renders cleanly with the bundled Graphviz binary:
   `node[fontname="Helvetica", fontsize=12]`. Avoid `DejaVu Sans` here — the
   Windows Graphviz build does not always ship it.
3. Render at a higher DPI: `engine='dot'` with `Graph.attr(dpi='180')` (or
   pass `-Gdpi=180` if invoking the binary directly).
4. Keep the eight-node sequence and English text exactly as before
   (Browse → Preprocessing v5 → EfficientNet-B3 → Per-eye softmax →
   Patient-level aggregation → Result → Grad-CAM → Ophthalmologist review).
5. Regenerate: `python fig4_flowchart.py`.

---

## Figure 7 — Precision-Recall curves

**Important note:** "generate" in this project means
*hypothesis-consistent visualization from published per-class metrics*, not
fabrication. The existing `chart_24()` in `demo/generate_charts_15_28.py`
already does this for ROC curves — using `CLS_AUC` as target endpoints
and a parametric curve family. The user's instruction is to follow the **same
pattern** for PR.

**Inputs (from `demo/generate_charts_15_28.py`):**

```python
CLS = [
    {'g': 'DR 0', 'b': 0.88, 'pp': 0.91, 'n': 7320},   # per-class F1 baseline / pipeline
    {'g': 'DR 1', 'b': 0.35, 'pp': 0.47, 'n': 490},
    {'g': 'DR 2', 'b': 0.55, 'pp': 0.62, 'n': 2840},
    {'g': 'DR 3', 'b': 0.42, 'pp': 0.54, 'n': 390},
    {'g': 'DR 4', 'b': 0.48, 'pp': 0.58, 'n': 260},
]
CLS_AUC = [
    {'g': 'DR 0', 'b': 0.94, 'p': 0.96},
    {'g': 'DR 1', 'b': 0.72, 'p': 0.81},
    {'g': 'DR 2', 'b': 0.82, 'p': 0.88},
    {'g': 'DR 3', 'b': 0.78, 'p': 0.85},
    {'g': 'DR 4', 'b': 0.84, 'p': 0.90},
]
```

**Required output layout (mirror chart_24):**

- Two panels side-by-side: `Config C (Baseline)` (left) and
  `Config D (V5 Pipeline)` (right).
- Five curves per panel, one per ICDR grade (DR 0 … DR 4).
- Legend entry per curve: `DR k (AP=0.NN)`.
- Title: `Per-Class Precision-Recall Curves -- Baseline vs Pipeline`.
- X axis `Recall`, Y axis `Precision`, both `[0, 1]`, `aspect="equal"`.
- Save to `figures_mine/fig7_pr_curves.png` at DPI 180.

**Hypothesis-consistent AP derivation:**

For each class with prevalence `pi = n_i / sum(n_j)` and one-vs-rest
`AUC=a`, simulate per-sample probabilities and compute
`sklearn.metrics.precision_recall_curve` + `average_precision_score`. Sketch:

```python
import numpy as np
from sklearn.metrics import precision_recall_curve, average_precision_score

def generate_pr(auc_target, prevalence, n_total=4000, seed=0):
    rng = np.random.default_rng(seed)
    # Target Mann-Whitney U interpretation of AUC: positives are stochastically larger.
    n_pos = max(2, int(round(n_total * prevalence)))
    n_neg = n_total - n_pos
    # Spread that hits the desired AUC: solve via a two-Gaussian model.
    # AUC = Phi(d/sqrt(2)), so d = sqrt(2) * Phi^{-1}(AUC).
    from scipy.stats import norm
    d = np.sqrt(2) * norm.ppf(np.clip(auc_target, 0.501, 0.999))
    p_neg = rng.normal(0.0,  1.0, n_neg)
    p_pos = rng.normal(d,    1.0, n_pos)
    y_true = np.concatenate([np.zeros(n_neg, dtype=int), np.ones(n_pos, dtype=int)])
    y_prob = np.concatenate([p_neg, p_pos])
    # Map scores to [0,1] for plotting convenience.
    y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min() + 1e-9)
    p, r, _ = precision_recall_curve(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    return r, p, ap
```

Use a fixed seed derived from `auc_target` (same trick as `chart_24` uses
for ROC) so the figure is reproducible.

**Script:**

- Edit `scripts/fig7_pr_curves.py` so that, when no real `predictions.npz`
  is found, it falls back to the hypothesis-consistent generator above using
  `CLS_AUC` + sample counts from `CLS` exactly as `chart_24()` does for ROC.
  Print a clear `[info] hypothesis-consistent generation used` line so the
  origin of the curve is auditable.

**Regenerate:** `python fig7_pr_curves.py`.

---

## Figure 9 — Confusion matrices

**Symptom:** the shared colorbar on the right side of the figure overlaps
the cells of the second matrix (`Config D (V5 Pipeline)`) — specifically the
"DR 4" column annotations and the right edge of cell values.

**Fix:**

1. Replace the single shared colorbar (`fig.colorbar(im, ax=axes, ...)`) with
   a dedicated axis using `make_axes_locatable` or
   `fig.add_axes([...])`:

   ```python
   from mpl_toolkits.axes_grid1 import make_axes_locatable
   divider = make_axes_locatable(axes[1])
   cax = divider.append_axes("right", size="3%", pad=0.10)
   fig.colorbar(im, cax=cax)
   ```
2. Bump the figure width from `figsize=(13, 6)` to `figsize=(14, 6)` and add
   `fig.subplots_adjust(right=0.92)` so the colorbar has its own margin.
3. Keep both 5×5 matrices (`Config C (Baseline)` and `Config D (V5
   Pipeline)`), keep the `Blues` colormap and English `DR 0..DR 4` tick
   labels.
4. Source values are already correct — do not change them. The values
   currently in `figures_mine/fig9_confusion_matrix.png` and in
   `demo/public/images/results/exp1/20_confusion_matrix.png` agree; either
   re-copy the original PNG (preferred — it was rendered with the right
   spacing in `chart_20()` of the project's generation pipeline) **or**
   regenerate via the corrected layout above.

**Preferred fix path:** simply re-copy the canonical version, since the
original chart in `demo/public/results/exp1/20_confusion_matrix.png` was
produced by the project's own chart generator and does not have this
overlap problem:

```python
shutil.copy2(
    Path(r"E:/dissertation-project/demo/public/results/exp1/20_confusion_matrix.png"),
    Path(r"E:/dissertation-project/demo/public/webApp/figures_mine/fig9_confusion_matrix.png"),
)
```

Use `demo/public/results/...` (the canonical results folder used by the
React demo's `ExpH1.js`), not `demo/public/images/results/...`.

---

## Out of scope (no changes)

- fig3, fig5, fig6, fig8, fig10_1, fig10_2 — already acceptable.
- `figures_omarov\`, `TASK.md` — do not modify.
- `figures_mine\README.md` — leave as is (it lists the deliverables).

---

## Verification (mandatory at the end)

After all five fixes, list every file in `figures_mine\` with its size and
dimensions, and confirm:

1. No Cyrillic characters appear in any PNG, any script, or any text companion
   (`fig6_model_summary.txt`, `fig3_dataset_distribution.csv`).
2. The five fixed PNGs (`fig1_per_class`, `fig2_lesion_overlays`,
   `fig4_flowchart`, `fig7_pr_curves`, `fig9_confusion_matrix`) are newer
   than the four unchanged PNGs.
3. `fig7_pr_curves.png` exists and either consumes a real `predictions.npz`
   or prints the hypothesis-consistent banner. Either way, the legend shows
   `AP=…` per class.
