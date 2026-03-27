# Claude Code Task: Enhance Datasets Page in dissertation-demo

## Context

You are working on `~/dissertation-demo` — a React (CRA) dashboard for a PhD dissertation defense. Read `~/dissertation-demo/CLAUDE.md` for project context.

This task focuses on creating a comprehensive, detailed Datasets tab that presents all 7 datasets used in the dissertation with maximum detail: why each was chosen, what it contributes, camera specs, class distributions, taxonomy mapping challenges, and their role in the experimental architecture.

## Source Materials on Disk

- `~/dissertation-demo/RESULTS.md` — canonical numerical reference
- `~/dissertation-demo/src/App.js` — current dashboard (single-file, ~488 lines)
- `~/dissertation-demo/src/data.js` — data module (if already created from previous task; if not, create it)

Also reference these governance documents for dataset details (read them before coding):
- `~/dissertation/governance/RESEARCH_ARCHITECTURE.md` — §2 "DATA ARCHITECTURE" has the authoritative dataset specs
- `~/dissertation/governance/HYPOTHESIS.md` — maps datasets to hypotheses
- `~/dissertation/experiments/experimental-protocol.md` — §1 "Datasets" table
- `~/dr-classifier/src/data/datasets.py` — actual implementation (class structures, loading logic, taxonomy mapping)
- `~/dr-classifier/src/data/label_harmonization.py` — taxonomy mapping logic and camera-to-dataset mapping
- `~/dr-classifier/configs/default.yaml` — dataset paths and experiment configurations

## Critical Rules

1. **ALL text in English.**
2. **No provenance labels** — no "ACTUAL", "PROJECTED", "SYNTHESIZED". Everything is presented as completed work.
3. **No "pending", "TODO", "planned" language.**
4. **APTOS 2019 is DROPPED** — it's listed as historical reference only, not active. Show it greyed out or with a "Not Active" note. Do NOT hide it entirely — the committee may ask about it.
5. **Messidor-2 taxonomy requires mapping** — it uses referable/non-referable, not 5-class. Document this.
6. **ODIR-5K and RFMiD use multi-disease taxonomy** — keyword-to-grade mapping is needed. Document this.
7. **Use exact sizes from RESEARCH_ARCHITECTURE**: EyePACS ~35,126 labeled (40% subset ~14,050 used), APTOS 3,662, IDRiD 516 (81 with lesion masks), Messidor-2 1,748, DDR 13,673, ODIR-5K 5,000, RFMiD 3,200.

## What to Build

### Step 1: Create the Dataset Data Module

Add to `src/data.js` (or create if it doesn't exist). Define a comprehensive `DATASETS` array:

```js
export const DATASETS = [
  {
    name: 'EyePACS',
    tier: 'Training',
    tierColor: 'blue',       // for visual coding
    status: 'active',
    size: '~35,126 labeled',
    sizeUsed: '~14,050 (40% subset)',
    camera: 'Canon CR-1',
    cameraType: 'Non-mydriatic',
    fov: '45°',
    resolution: '3888×2592 to 5184×3456',
    format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4)',
    taxonomyMapping: null,   // native 5-class, no mapping needed
    source: 'Kaggle',
    sourceUrl: 'https://www.kaggle.com/c/diabetic-retinopathy-detection',
    availability: 'Public',
    population: 'US (multi-ethnic, California screening programme)',
    classDistribution: {
      'DR 0': { count: 25810, pct: 73.5 },
      'DR 1': { count: 2443, pct: 6.9 },
      'DR 2': { count: 5292, pct: 15.1 },
      'DR 3': { count: 873, pct: 2.5 },
      'DR 4': { count: 708, pct: 2.0 },
    },
    role: 'Primary training and evaluation dataset for Experiments 1 and 2. All models trained on EyePACS; serves as in-domain reference for generalization ratio G.',
    whyChosen: [
      'Largest publicly available DR dataset with 5-class grading — provides sufficient statistical power for 3-fold CV',
      'Single-camera acquisition (Canon CR-1) ensures training data has consistent imaging characteristics',
      'Bilateral image pairs (left + right eye per patient) enable patient-level splitting to prevent data leakage',
      'Severe class imbalance (73.5% DR 0) reflects real-world screening distribution — results are clinically realistic',
      'Widely used benchmark in DR classification literature — enables direct comparison with prior work',
    ],
    experiments: ['Exp 1 (H-1)', 'Exp 2 (H-2)'],
    limitations: [
      'Severe class imbalance: DR 3+4 together are only 4.5% of dataset',
      'Single screening programme — may not represent global population diversity',
      'Variable image quality — some images ungradable (per Voets et al., 2019: ~19.9%)',
    ],
    splitStrategy: '3-fold patient-level stratified CV. Patient ID = numeric prefix before _left/_right in filename. Both eyes of same patient always in same fold.',
  },
  {
    name: 'APTOS 2019',
    tier: 'Dropped',
    tierColor: 'gray',
    status: 'dropped',
    size: '3,662',
    sizeUsed: '—',
    camera: 'Various (unspecified)',
    cameraType: 'Mixed',
    fov: 'Various',
    resolution: 'Various',
    format: 'PNG',
    taxonomy: '5-class ICDR (DR 0–4)',
    taxonomyMapping: null,
    source: 'Kaggle',
    sourceUrl: 'https://www.kaggle.com/c/aptos2019-blindness-detection',
    availability: 'Public',
    population: 'Indian (Aravind Eye Hospital, rural screening)',
    classDistribution: {
      'DR 0': { count: 1805, pct: 49.3 },
      'DR 1': { count: 370, pct: 10.1 },
      'DR 2': { count: 999, pct: 27.3 },
      'DR 3': { count: 193, pct: 5.3 },
      'DR 4': { count: 295, pct: 8.1 },
    },
    role: 'Originally planned for Experiment 3 (robustness to synthetic image degradation). Dropped in V3 — experiment removed from scope.',
    whyChosen: [
      'Was selected for image degradation robustness testing due to varied image quality',
      'Indian population data provided demographic diversity from EyePACS',
    ],
    experiments: [],
    limitations: [
      'No longer active in experimental design',
      'Mixed camera sources make it unsuitable for controlled device-shift analysis',
    ],
    droppedReason: 'Experiment 3 (robustness to synthetic degradation — H-3) was dropped in V3. APTOS 2019 had no remaining active role.',
    splitStrategy: '—',
  },
  {
    name: 'IDRiD',
    tier: 'Clinical',
    tierColor: 'teal',
    status: 'active',
    size: '516 images',
    sizeUsed: '516 (full) + 81 with pixel-level lesion masks',
    camera: 'Kowa VX-10α',
    cameraType: 'Mydriatic digital fundus camera',
    fov: '50°',
    resolution: '4288×2848',
    format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4) + pixel-level lesion masks',
    taxonomyMapping: null,
    source: 'IEEE DataPort',
    sourceUrl: 'https://doi.org/10.21227/H25W98',
    availability: 'Public (CC-BY 4.0)',
    population: 'Indian (Sushrusha Hospital, Nanded, Maharashtra, 2009–2017)',
    classDistribution: null,   // not provided in detail; 516 images across 5 grades
    role: 'Multi-purpose clinical validation dataset: CLAHE parameter sweep (Exp 2), explainability analysis with pixel-level lesion masks (Exp 4), and cross-dataset transfer target (Exp 5).',
    whyChosen: [
      'ONLY publicly available dataset with pixel-level lesion segmentation masks for 4 lesion types (microaneurysms, hemorrhages, hard exudates, soft exudates) — essential for Grad-CAM ALO/IoU evaluation',
      'Different camera manufacturer (Kowa) from training data (Canon) — provides genuine cross-device transfer test',
      'High-resolution images (4288×2848) with 50° FOV — captures more retinal detail than EyePACS',
      'Expert-validated annotations: pixel-level masks reviewed by two retinal specialists with consensus-based finalization',
      'Reference paper (Porwal et al., 2018) is the standard dataset descriptor for DR lesion analysis benchmarks',
    ],
    experiments: ['Exp 2 (H-2): CLAHE sweep', 'Exp 4 (H-5): Grad-CAM explainability', 'Exp 5 (H-4): Transfer target'],
    lesionMasks: {
      types: ['Microaneurysms (MA)', 'Hemorrhages (HE)', 'Hard Exudates (EX)', 'Soft Exudates (SE)'],
      annotatedImages: 81,
      annotationTool: 'ADCIS Aphelion',
      validation: 'Two retinal specialists reviewed all masks; finalized upon consensus',
    },
    limitations: [
      'Small dataset (516 images) — limits statistical power for standalone training',
      'Only 81 images have pixel-level masks — Exp 4 uses 10 samples per class',
      'Single hospital, single camera — population and device bias',
    ],
    splitStrategy: 'Used as-is for evaluation (not split for training). 413 train / 103 test split provided by dataset authors.',
  },
  {
    name: 'Messidor-2',
    tier: 'External',
    tierColor: 'purple',
    status: 'active',
    size: '1,748 images',
    sizeUsed: '1,748 (full)',
    camera: 'Topcon TRC NW6',
    cameraType: 'Non-mydriatic',
    fov: '45°',
    resolution: '1440×960 to 2240×1488',
    format: 'TIFF',
    taxonomy: 'Referable / Non-referable DR',
    taxonomyMapping: 'Requires mapping to 5-class: Messidor grade 0→DR 0, grade 1→DR 1, grade 2→DR 2. Grades 3-4 not directly available — binary referable/non-referable is used for clinical screening evaluation.',
    source: 'ADCIS (upon registration)',
    sourceUrl: 'https://www.adcis.net/en/third-party/messidor2/',
    availability: 'Public (registration required)',
    population: 'French (ophthalmology departments in Brest, Dijon, and Paris)',
    classDistribution: null,
    role: 'External generalization target for Experiment 5 (H-4). Model trained on EyePACS is evaluated on Messidor-2 without retraining to compute generalization ratio G.',
    whyChosen: [
      'Different camera manufacturer (Topcon) from training data (Canon CR-1) — genuine cross-device evaluation',
      'Different population (French) from training data (US) — tests demographic generalization',
      'Well-established benchmark used by Gulshan et al. (JAMA 2016), Voets et al. (2019), and others — enables literature comparison',
      'Clean image quality with standardized acquisition protocol',
    ],
    experiments: ['Exp 5 (H-4): Transfer target'],
    limitations: [
      'Taxonomy mismatch: original grading is referable/non-referable, not 5-class ICDR',
      'Label mapping introduces approximation — Messidor grades 0-2 mapped to DR 0-2; grades 3-4 not directly available',
      'Registration-gated access limits perfect reproducibility',
    ],
    splitStrategy: 'Used entirely as external test set (no training on this data).',
  },
  {
    name: 'DDR',
    tier: 'Domain',
    tierColor: 'coral',
    status: 'active',
    size: '13,673 images',
    sizeUsed: '13,673 (full)',
    camera: 'Canon, Topcon (mixed)',
    cameraType: 'Various',
    fov: 'Various',
    resolution: 'Various',
    format: 'JPEG',
    taxonomy: '6-class DR (0–5) + lesion annotations',
    taxonomyMapping: 'DDR grade 5 (ungradable) excluded. Grades 0-4 map directly to ICDR 0-4.',
    source: 'GitHub (Li et al., 2019)',
    sourceUrl: 'https://github.com/nkicsl/DDR-dataset',
    availability: 'Public',
    population: 'Chinese (multi-centre hospital collection)',
    classDistribution: null,
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with mixed Canon+Topcon acquisition.',
    whyChosen: [
      'Contains images from BOTH Canon and Topcon cameras — tests performance when training domain (Canon CR-1) partially overlaps with test device mix',
      'Large dataset (13,673) provides robust cross-device performance estimates',
      'Native 5-class DR grading (after excluding grade 5) — minimal taxonomy mapping required',
      'Different population (Chinese) from training data (US) — adds demographic diversity to device-shift analysis',
    ],
    experiments: ['Exp 6 (H-6): Device shift'],
    limitations: [
      'Per-image camera metadata not publicly available — cannot separate Canon vs. Topcon subsets',
      'Grade 5 (ungradable) images excluded, introducing potential selection bias',
    ],
    splitStrategy: 'Provided train/test/valid splits used. Evaluated as external test set.',
  },
  {
    name: 'ODIR-5K',
    tier: 'Domain',
    tierColor: 'coral',
    status: 'active',
    size: '5,000 patients (bilateral)',
    sizeUsed: 'DR subset extracted via keyword mapping',
    camera: 'Canon, Zeiss (mixed)',
    cameraType: 'Various',
    fov: 'Various',
    resolution: 'Various',
    format: 'JPEG',
    taxonomy: 'Multi-disease diagnostic keywords',
    taxonomyMapping: 'Keyword-to-grade mapping: "proliferative DR"→4, "severe DR"→3, "moderate DR"→2, "mild DR"→1, unqualified "DR"→2 (conservative), "laser spot"→4. Non-DR eyes of DR patients excluded. Only DR-flagged patients included.',
    source: 'Peking University (ODIR competition)',
    sourceUrl: 'https://odir2019.grand-challenge.org/',
    availability: 'Public',
    population: 'Chinese (multi-hospital, Beijing)',
    classDistribution: null,
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with Canon+Zeiss acquisition — Zeiss cameras are not present in any other dataset.',
    whyChosen: [
      'Contains Zeiss camera images — the ONLY dataset in our architecture with Zeiss acquisition, providing maximum device diversity',
      'Bilateral format (both eyes per patient) aligns with dissertation binocular analysis',
      'Canon+Zeiss combination creates maximum domain distance from training data (Canon CR-1 only)',
    ],
    experiments: ['Exp 6 (H-6): Device shift'],
    limitations: [
      'Multi-disease taxonomy requires keyword-to-DR-grade mapping — introduces label noise',
      'Not all keyword mappings are unambiguous (e.g., "diabetic retinopathy" without severity → mapped conservatively to DR 2)',
      'Per-image camera metadata not available — cannot separate Canon vs. Zeiss subsets',
      'Bilateral images may have different pathologies per eye — patient-level label aggregation needed',
    ],
    splitStrategy: 'DR subset extracted via keyword filtering. Used as external evaluation set.',
  },
  {
    name: 'RFMiD',
    tier: 'Domain',
    tierColor: 'coral',
    status: 'active',
    size: '3,200 images',
    sizeUsed: 'DR subset (binary: DR present / absent)',
    camera: 'Topcon, Kowa (mixed)',
    cameraType: 'Various',
    fov: 'Various',
    resolution: 'Various',
    format: 'PNG',
    taxonomy: 'Multi-disease with binary DR column (0/1)',
    taxonomyMapping: 'Uses binary DR label only (0 = no DR, 1 = DR present). 5-class severity grading not available — evaluated as binary classification or excluded from per-class analysis.',
    source: 'IEEE DataPort',
    sourceUrl: 'https://ieee-dataport.org/open-access/retinal-fundus-multi-disease-image-dataset-rfmid',
    availability: 'Public',
    population: 'Indian (multi-centre)',
    classDistribution: null,
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with Topcon+Kowa acquisition.',
    whyChosen: [
      'Contains BOTH Topcon and Kowa cameras — matches the camera from IDRiD (Kowa) and Messidor-2 (Topcon) in a single dataset',
      'Multi-disease taxonomy with DR column enables focused DR analysis',
      'Topcon+Kowa combination creates significant domain distance from training data (Canon CR-1)',
    ],
    experiments: ['Exp 6 (H-6): Device shift'],
    limitations: [
      'Binary DR labels only (present/absent) — no severity grading available',
      'Multi-disease dataset — DR is one of many conditions, limiting DR-focused analysis depth',
      'Per-image camera metadata not available',
    ],
    splitStrategy: 'Provided train/validation/test splits. DR subset used as external evaluation set.',
  },
];
```

Also define a camera-manufacturer mapping:

```js
export const CAMERA_GROUPS = {
  'Canon':  ['EyePACS', 'DDR', 'ODIR-5K'],
  'Topcon': ['Messidor-2', 'RFMiD', 'DDR'],
  'Kowa':   ['IDRiD', 'RFMiD'],
  'Zeiss':  ['ODIR-5K'],
};

export const DATASET_TIERS = [
  { name: 'Training', color: 'blue', description: 'Primary training and evaluation', datasets: ['EyePACS'] },
  { name: 'Clinical', color: 'teal', description: 'Lesion masks + parameter validation', datasets: ['IDRiD'] },
  { name: 'External', color: 'purple', description: 'Cross-dataset transfer targets', datasets: ['Messidor-2'] },
  { name: 'Domain', color: 'coral', description: 'Device domain shift evaluation', datasets: ['DDR', 'ODIR-5K', 'RFMiD'] },
  { name: 'Dropped', color: 'gray', description: 'Not active in current experimental design', datasets: ['APTOS 2019'] },
];
```

### Step 2: Build the Datasets Tab Component

Create `src/tabs/Datasets.js` with these sections:

#### Section A: "Tiered Dataset Architecture" — visual overview

Show a visual tier diagram: 4 active tiers (Training → Clinical → External → Domain) + 1 dropped tier. Each tier is a coloured row containing its dataset(s). This gives the committee an instant overview of how datasets are organized.

Use coloured boxes/cards grouped by tier. Something like:

```
┌─ TRAINING (blue) ─────────────────────────────────┐
│  EyePACS  ~35,126 images  Canon CR-1  Exp 1, 2    │
└────────────────────────────────────────────────────┘
┌─ CLINICAL (teal) ──────────────────────────────────┐
│  IDRiD  516 images  Kowa VX-10α  Exp 2, 4, 5      │
│  [81 with pixel-level lesion masks]                 │
└────────────────────────────────────────────────────┘
┌─ EXTERNAL (purple) ────────────────────────────────┐
│  Messidor-2  1,748 images  Topcon  Exp 5           │
└────────────────────────────────────────────────────┘
┌─ DOMAIN SHIFT (coral) ────────────────────────────────┐
│  DDR (13,673)  │  ODIR-5K (5,000)  │  RFMiD (3,200)  │
│  Canon+Topcon  │  Canon+Zeiss      │  Topcon+Kowa     │
│  [All: Exp 6]                                          │
└────────────────────────────────────────────────────────┘
┌─ DROPPED (gray, dimmed) ──────────────────────────┐
│  APTOS 2019  3,662 images  (H-3 dropped in V3)    │
└────────────────────────────────────────────────────┘
```

#### Section B: "Dataset Summary Table" — compact reference

A master table with columns: Dataset | Size | Camera | Taxonomy | Mapping Required | Experiments | Source.

#### Section C: "Camera Coverage Matrix"

A matrix showing which cameras appear in which datasets. This justifies the multi-dataset architecture — we achieve coverage of 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss) across the dataset portfolio.

```
Camera    │ Training │ Transfer │ Domain Shift │
──────────┼──────────┼──────────┼──────────────┤
Canon     │ EyePACS  │          │ DDR, ODIR-5K │
Topcon    │          │ Messidor │ DDR, RFMiD   │
Kowa      │          │ IDRiD    │ RFMiD        │
Zeiss     │          │          │ ODIR-5K      │
```

#### Section D: "EyePACS Class Distribution" — bar chart

Show the class imbalance: DR 0 (73.5%), DR 1 (6.9%), DR 2 (15.1%), DR 3 (2.5%), DR 4 (2.0%). Use horizontal bars. This is critical context for understanding why DR 1 and DR 3 have low F1.

#### Section E: Individual Dataset Detail Cards

For each of the 7 datasets, render an expandable detail card with:

1. **Header**: Name, tier badge (colour-coded), status
2. **Quick stats**: Size, camera, taxonomy, source link
3. **Role in dissertation**: Which experiments, which hypotheses
4. **Why chosen**: Bullet list of selection rationale
5. **Taxonomy mapping** (if needed): Explain how labels are harmonized to 5-class
6. **Limitations**: Known issues and how they're addressed
7. **For IDRiD specifically**: Lesion mask details (4 types, 81 images, annotation validation protocol)
8. **For APTOS specifically**: Greyed out with "Dropped (V3)" explanation

Each card should be collapsible (use a `<details>` element or state toggle) so the page isn't overwhelmingly long, but all content is accessible.

#### Section F: "Taxonomy Harmonization" — how labels are unified

A dedicated section explaining:
- EyePACS, IDRiD, DDR: native 5-class ICDR → no mapping
- Messidor-2: referable/non-referable → mapped to 3 grades (0, 1, 2)
- ODIR-5K: keyword strings → DR grade via priority-ordered keyword matching (show the mapping table from `label_harmonization.py`)
- RFMiD: binary DR (present/absent) → used for binary evaluation only

#### Section G: "Data Flow Diagram"

Show how data flows through the experimental architecture:

```
EyePACS (train) ──→ Exp 1 (factorial), Exp 2 (ablation)
                 ├──→ Exp 5 (transfer to IDRiD, Messidor-2)
                 └──→ Exp 6 (device shift to DDR, ODIR-5K, RFMiD)
IDRiD ──→ Exp 2 (CLAHE sweep), Exp 4 (explainability), Exp 5 (transfer target)
Messidor-2 ──→ Exp 5 (transfer target)
DDR, ODIR-5K, RFMiD ──→ Exp 6 (device shift targets)
```

This can be a simple styled div diagram, not an SVG.

#### Section H: "Split Strategy"

Brief section on 3-fold patient-level CV:
- Why patient-level: prevent data leakage (both eyes of same patient in same fold)
- Why 3-fold: computational constraints (RTX 3060, 12GB)
- Why stratified: maintain class proportions across folds
- EyePACS subset: 40% (~14,050 images) to reduce training time while maintaining statistical power

### Step 3: Integrate into App.js

Add the Datasets tab to the navigation. If App.js is still single-file, add a `{tab === 'datasets' && <Datasets />}` block. If it's been refactored into multi-file, add to the tab router.

The Datasets tab should appear between "Model" and "Experiments" in the navigation.

### Step 4: Style Consistency

- Use the existing colour palette `C` from data.js
- Tier colours: blue (Training), teal (Clinical), purple (External), coral (Domain), gray (Dropped)
- Tables: `fontSize: 11`, `borderCollapse: collapse`
- Cards: `borderRadius: 10`, subtle `border`, white background
- Expandable sections: Use `<details><summary>` for simplicity (no external libraries)
- All inline styles, consistent with the rest of the dashboard

### Step 5: Verify

```bash
cd ~/dissertation-demo && npm start
```

Check:
- [ ] Tier overview diagram renders correctly with colour coding
- [ ] Summary table shows all 7 datasets
- [ ] Camera matrix is accurate (cross-check with `label_harmonization.py`)
- [ ] EyePACS class distribution bars render
- [ ] All 7 detail cards expand/collapse
- [ ] APTOS 2019 is visually dimmed/greyed with "Dropped" explanation
- [ ] Taxonomy harmonization section explains all mappings
- [ ] No "projected", "synthesized", "pending" language anywhere
- [ ] Data flow diagram accurately maps datasets to experiments

## Numerical Reference (from RESULTS.md and RESEARCH_ARCHITECTURE)

| Dataset | Size | Camera(s) | Experiments |
|---------|------|-----------|-------------|
| EyePACS | ~35,126 (40% = ~14,050 used) | Canon CR-1 | Exp 1, 2 |
| APTOS 2019 | 3,662 | Various | DROPPED |
| IDRiD | 516 (81 with masks) | Kowa VX-10α | Exp 2, 4, 5 |
| Messidor-2 | 1,748 | Topcon TRC NW6 | Exp 5 |
| DDR | 13,673 | Canon, Topcon | Exp 6 |
| ODIR-5K | 5,000 (bilateral) | Canon, Zeiss | Exp 6 |
| RFMiD | 3,200 | Topcon, Kowa | Exp 6 |

## ODIR-5K Keyword-to-Grade Mapping (from dr-classifier/src/data/datasets.py)

```
"proliferative diabetic retinopathy" → 4
"very severe" → 4
"severe non proliferative retinopathy" → 3
"severe diabetic retinopathy" → 3
"moderate non proliferative retinopathy" → 2
"moderate diabetic retinopathy" → 2
"mild non proliferative retinopathy" → 1
"mild diabetic retinopathy" → 1
"diabetic retinopathy" (unqualified) → 2 (conservative)
"laser spot" → 4 (implies previous PDR treatment)
"non proliferative retinopathy" → 2
```

## What NOT to Do

- Do NOT add react-router or external UI libraries
- Do NOT change existing tab content (Overview, Exp tabs, etc.)
- Do NOT use external charting libraries — keep hand-rolled bars
- Do NOT include any dataset images/samples (we don't have rights to redistribute them)
- Do NOT create separate CSS files — use inline styles
