# demo/ — DR Diagnosis Dashboard

## TODO

- [ ] Regenerate all pipeline demonstration images using full pipeline (isotropic resize + padding + adaptive flat-field). Current images show old stretch-resize.

---

Interactive React dashboard for PhD dissertation defense. Visualises all experiment results, hypothesis status, and the preprocessing pipeline walkthrough.

## Stack

React 19 (Create React App), single-page app, no router, no external UI library.
Runs at localhost:3000 (`npm start`).

## Architecture

```
src/
├── App.js           — Shell: sidebar nav (192px) + tab routing (~100 lines)
├── data.js          — ALL data constants (single source of truth for metrics)
├── components.js    — Reusable UI: Card, Note, Hbar, Paired, Sec, DataTable, ImageFigure, DiagramViewer, LangSwitcher
├── i18n.js          — EN/KZ internationalization (LangContext + useLang hook)
├── index.js         — CRA entry point
├── index.css        — Base styles
└── tabs/            — 17 tab components (one file each)
    ├── Overview.js
    ├── ModelArchitecture.js, ModelPipeline.js, ModelMethods.js, ModelExplainability.js
    ├── Datasets.js
    ├── ExpH1.js, ExpH2.js, ExpH4.js, ExpH5.js, ExpH6.js
    ├── ResultsMain.js, ResultsBestConfig.js, ResultsStatistical.js
    └── ValClinical.js, ValQuality.js, ValComputational.js

public/
├── results/         — 28 PNG result charts (01–28)
├── pipeline/        — 17 PNG pipeline stage illustrations
├── diagrams/        — SVG + spec files for system and pipeline architecture
├── fundus-examples/ — Example fundus images by DR grade (dr00, dr02, dr03)
└── RESULTS.md       — Results summary document
```

## Data Flow

`experiments/` runs → produces metrics → numbers transcribed into `src/data.js` → tabs render them.

All experiment metrics come from `src/data.js`. When experiment results update, edit data.js — tabs read from it automatically.

## Key Data Constants in data.js

- `C` — colour palette (blue/teal/coral/purple/amber/gray/green/red + backgrounds + text variants)
- `CONFIGS` (A–D) — Experiment 1 results: f1, auc, kappa, accuracy ± std
- `ABL`, `ABL_INDIV` — Experiment 2 ablation data
- `ALO`, `IOU`, `ATTENTION_CONSISTENCY` — Experiment 4 explainability
- `GEN`, `GEN_AUC`, `G_RATIO` — Experiment 3 generalization
- `DEV` — Experiment 6 device domain shift
- `CLS`, `CLS_AUC` — per-class metrics
- `CLIN`, `CALIBRATION` — clinical validation
- `IQ` — image quality metrics
- `CLAHE1`, `CLAHE2` — CLAHE parameter sweep heatmaps
- `PIPE` — pipeline stage definitions
- `COMPUTE` — computational benchmarks
- `STAT_TESTS`, `TRAIN_TEST_GAP` — statistical analysis
- `DATASETS` — 8 datasets
- `HYPOTHESES` — 6 confirmed hypotheses (H-1, H-2, H-4, H-5, H-6, H-7)

## Design Decisions

- All inline styles (CSS-in-JS). No external CSS framework.
- No external charting library — all charts are hand-rolled divs.
- No status badges/labels — everything presented as completed work.
- Tab IDs: exph1, exph2, exph4, exph5, exph6 (no exph3 — H-3 dropped in V3).
- Images use `process.env.PUBLIC_URL` prefix for CRA compatibility.
- Numbers: 3 decimal places for metrics, percentages as `pp`.

## Governance Alignment

Dashboard data must match `../thesis/governance/` invariants exactly:
- Pipeline: 8-stage
- EyePACS: ~35,126 labeled images; Exp 1: 100%, 5-fold CV
- Hypotheses: H-1, H-2, H-4, H-5, H-6, H-7 (H-3 dropped)
- ALO is primary explainability metric; IoU is secondary
- EH-3 threshold: ΔF1 ≥ 5pp, ΔAUC ≥ 2pp, no κ degradation
- H-4 threshold: generalization ratio G ≥ 0.85

## Common Tasks

**Update experiment data:** Edit constants in `src/data.js`.

**Add a new tab:**
1. Create `src/tabs/NewTab.js`
2. Import in App.js
3. Add to NAV array and COMPONENTS map in App.js
4. Use components from components.js

**Add result images:** Place PNG in `public/results/`, reference with `ImageFigure` component.

## Commands

```bash
npm start     # dev server → localhost:3000
npm run build # production build → build/
```
