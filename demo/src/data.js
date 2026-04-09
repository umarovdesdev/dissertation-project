// src/data.js — Canonical data for DR Diagnosis Dashboard

// Colour palette
export const C = {
  blue: '#378ADD', teal: '#1D9E75', coral: '#D85A30', purple: '#7F77DD',
  amber: '#EF9F27', gray: '#888780', green: '#639922', red: '#E24B4A',
  blueBg: '#E6F1FB', tealBg: '#E1F5EE', coralBg: '#FAECE7', purpleBg: '#EEEDFE',
  amberBg: '#FAEEDA', grayBg: '#F1EFE8', greenBg: '#EAF3DE', redBg: '#FCEBEB',
  blueT: '#0C447C', tealT: '#085041', coralT: '#712B13', purpleT: '#3C3489',
  amberT: '#633806', grayT: '#444441', greenT: '#27500A', redT: '#791F1F',
};

// Exp 1: 4 configurations (A–D)
export const CONFIGS = {
  A: { f1: 0.762, f1s: 0.006, auc: 0.853, aucs: 0.013, k: 0.654, ks: 0.033, acc: 0.755, lbl: 'Baseline (3ch) + ResNet-50', preprocessing: 'Baseline (3ch)', cnn: 'ResNet-50' },
  B: { f1: 0.761, f1s: 0.018, auc: 0.850, aucs: 0.012, k: 0.656, ks: 0.026, acc: 0.765, lbl: 'Full V5 Pipeline (4ch) + ResNet-50', preprocessing: 'Full V5', cnn: 'ResNet-50' },
  C: { f1: 0.727, f1s: 0.033, auc: 0.821, aucs: 0.019, k: 0.620, ks: 0.067, acc: 0.719, lbl: 'Baseline (3ch) + EfficientNet-B3', preprocessing: 'Baseline (3ch)', cnn: 'EfficientNet-B3' },
  D: { f1: 0.780, f1s: 0.022, auc: 0.865, aucs: 0.015, k: 0.700, ks: 0.030, acc: 0.770, lbl: 'Full V5 Pipeline (4ch) + EfficientNet-B3', preprocessing: 'Full V5', cnn: 'EfficientNet-B3' },
};

// Exp 2: Cumulative ablation — 7 rows
export const ABL = [
  { n: 'Baseline (crop+resize+norm)', f1: 0.727, auc: 0.821 },
  { n: '+Canonical flip (0a)', f1: 0.738, auc: 0.830 },
  { n: '+OD-fovea rotation (0b)', f1: 0.748, auc: 0.840 },
  { n: '+Flat-field (Stage 2)', f1: 0.758, auc: 0.848 },
  { n: '+CLAHE (Stage 3)', f1: 0.772, auc: 0.858 },
  { n: '+Augmentation (Stage 5)', f1: 0.778, auc: 0.863 },
  { n: 'Full V5 pipeline', f1: 0.780, auc: 0.865 },
];

// Exp 2: Individual ablation — 5 stages
export const ABL_INDIV = [
  { stage: 'Stage 0a: Canonical flip', individual_f1: 0.8 },
  { stage: 'Stage 0b: OD-fovea rotation', individual_f1: 0.7 },
  { stage: 'Stage 2: Flat-field correction', individual_f1: 1.0 },
  { stage: 'Stage 3: CLAHE (dual-constraint)', individual_f1: 1.4 },
  { stage: 'Stage 5: Augmentation', individual_f1: 0.6 },
];

// Exp 4: ALO by lesion type
export const ALO = [
  { l: 'Microaneurysms', ab: 0.28, ap: 0.45, ib: 0.12, ip: 0.22 },
  { l: 'Hemorrhages', ab: 0.42, ap: 0.62, ib: 0.20, ip: 0.35 },
  { l: 'Hard exudates', ab: 0.55, ap: 0.72, ib: 0.28, ip: 0.42 },
  { l: 'Soft exudates', ab: 0.38, ap: 0.56, ib: 0.18, ip: 0.32 },
];

// Exp 4: IoU by lesion type
export const IOU = [
  { l: 'Microaneurysms', baseline: 0.12, pipeline: 0.22 },
  { l: 'Hemorrhages', baseline: 0.20, pipeline: 0.35 },
  { l: 'Hard exudates', baseline: 0.28, pipeline: 0.42 },
  { l: 'Soft exudates', baseline: 0.18, pipeline: 0.32 },
];

// Exp 4: Attention consistency across dataset pairs
export const ATTENTION_CONSISTENCY = [
  { pair: 'EyePACS vs IDRiD', baseline: 0.58, pipeline: 0.78 },
  { pair: 'EyePACS vs Messidor-2', baseline: 0.62, pipeline: 0.82 },
  { pair: 'IDRiD vs Messidor-2', baseline: 0.64, pipeline: 0.84 },
];

// Exp 5: Cross-dataset generalization — F1
export const GEN = [
  { d: 'EyePACS (train)', fb: 0.762, fp: 0.780 },
  { d: 'IDRiD', fb: 0.620, fp: 0.690, Gb: 0.81, Gp: 0.88 },
  { d: 'Messidor-2', fb: 0.640, fp: 0.700, Gb: 0.84, Gp: 0.90 },
];

// Exp 5: Cross-dataset generalization — AUC
export const GEN_AUC = [
  { dataset: 'EyePACS (train)', baseline: 0.853, pipeline: 0.865 },
  { dataset: 'IDRiD', baseline: 0.780, pipeline: 0.830 },
  { dataset: 'Messidor-2', baseline: 0.790, pipeline: 0.840 },
];

// Exp 5: Generalization ratio G
export const G_RATIO = [
  { dataset: 'IDRiD', G_baseline: 0.81, G_pipeline: 0.88, threshold: 0.85 },
  { dataset: 'Messidor-2', G_baseline: 0.84, G_pipeline: 0.90, threshold: 0.85 },
];

// Exp 6: Cross-device performance — 6 rows
export const DEV = [
  { c: 'Canon CR-1 (EyePACS)', fb: 0.762, fp: 0.780 },
  { c: 'Topcon (Messidor-2)', fb: 0.640, fp: 0.700 },
  { c: 'Kowa (IDRiD)', fb: 0.620, fp: 0.690 },
  { c: 'Canon+Topcon (DDR)', fb: 0.590, fp: 0.670 },
  { c: 'Canon+Zeiss (ODIR-5K)', fb: 0.560, fp: 0.650 },
  { c: 'Topcon+Kowa (RFMiD)', fb: 0.550, fp: 0.640 },
];

// Per-class F1
export const CLS = [
  { g: 'DR 0', b: 0.88, pp: 0.91, n: 7320 },
  { g: 'DR 1', b: 0.35, pp: 0.47, n: 490 },
  { g: 'DR 2', b: 0.55, pp: 0.62, n: 2840 },
  { g: 'DR 3', b: 0.42, pp: 0.54, n: 390 },
  { g: 'DR 4', b: 0.48, pp: 0.58, n: 260 },
];

// Per-class ROC-AUC
export const CLS_AUC = [
  { g: 'DR 0', baseline: 0.94, pipeline: 0.96 },
  { g: 'DR 1', baseline: 0.72, pipeline: 0.81 },
  { g: 'DR 2', baseline: 0.82, pipeline: 0.88 },
  { g: 'DR 3', baseline: 0.78, pipeline: 0.85 },
  { g: 'DR 4', baseline: 0.84, pipeline: 0.90 },
];

// Clinical metrics
export const CLIN = [
  { m: 'Sensitivity', b: 0.82, v: 0.90 },
  { m: 'Specificity', b: 0.88, v: 0.91 },
  { m: 'PPV', b: 0.76, v: 0.82 },
  { m: 'NPV', b: 0.92, v: 0.96 },
];

// Calibration metrics
export const CALIBRATION = [
  { metric: 'ECE', baseline: 0.082, pipeline: 0.045, improvement: '-45%' },
  { metric: 'Brier Score', baseline: 0.185, pipeline: 0.142, improvement: '-23%' },
];

// Image quality metrics
export const IQ = [
  { m: 'CNR', b: 2.1, a: 3.8, pct: '+81%' },
  { m: 'Vessel Visibility Index', b: 0.45, a: 0.68, pct: '+51%' },
  { m: 'Image Entropy (bits)', b: 6.2, a: 7.1, pct: '+15%' },
  { m: 'SSIM', b: 0.72, a: 0.85, pct: '+18%' },
];

// CLAHE heatmap grids
export const CLAHE1 = [[.32,.35,.37,.36,.34],[.36,.39,.41,.40,.38],[.38,.42,.44,.43,.41],[.40,.44,.47,.46,.43],[.39,.43,.45,.44,.42],[.37,.41,.43,.42,.40],[.35,.38,.40,.39,.37]];
export const CLAHE2 = [[.48,.51,.53,.52,.50],[.52,.55,.58,.57,.54],[.54,.58,.62,.61,.57],[.53,.57,.60,.59,.56],[.51,.55,.57,.56,.54],[.49,.53,.55,.54,.52],[.47,.50,.52,.51,.49]];

// Pipeline stages — V5 8-stage pipeline + raw input = 9 entries
export const PIPE = [
  { id: 0, nm: 'Raw input', desc: 'Original fundus photographs. Variable illumination, vignetting, different eye orientations. Canon CR-1 at EyePACS.', detail: 'Resolution: 3888×2592, 8-bit RGB JPEG' },
  { id: 1, nm: 'Stage 0: Canonical flip', desc: 'Left eyes (OS) horizontally flipped to right-eye (OD) orientation. Optic disc consistently on the right side. Deterministic — not random augmentation.', detail: 'If OS detected → np.fliplr(). OD → passthrough.' },
  { id: 2, nm: 'Stage 1: OD-fovea rotation', desc: 'Detect optic disc (brightest region) and fovea (darkest in annular zone). Rotate so OD→fovea axis is horizontal. Normalizes retinal orientation across cameras.', detail: 'OD: Gaussian-blurred green ch, 97th percentile. Fovea: annular search 1.5–3.5× OD-radius. Fallback if low confidence.' },
  { id: 3, nm: 'Stage 2: FOV crop + isotropic resize', desc: 'Detect circular FOV boundary, crop and resize to 512×512 with zero-padding to preserve aspect ratio. Eliminates device-specific border artifacts.', detail: 'Green channel threshold → largest contour → bounding circle. Isotropic resize + zero-pad to 512×512 (V5 change from stretch-resize).' },
  { id: 4, nm: 'Stage 3: FOV mask generation', desc: 'Generate binary FOV mask (1=retinal pixels, 0=background). Used as the 4th input channel to the CNN — provides spatial boundary information.', detail: 'Binary mask from Stage 2 FOV detection. Appended to RGB → 4-channel (RGBM) tensor input.' },
  { id: 5, nm: 'Stage 4: Adaptive flat-field correction', desc: 'Remove illumination gradients using adaptive Gaussian σ = 0.07×D (D = FOV diameter). Preserves vessel and lesion detail while normalizing device-specific illumination.', detail: 'σ = 0.07 × FOV_diameter. V5 change from fixed σ=45 to adaptive σ proportional to FOV size.' },
  { id: 6, nm: 'Stage 5: CLAHE (dual-constraint)', desc: 'Adaptive histogram equalization on LAB L-channel. clip_limit = min(clip_factor×tile_area/256, global_threshold×tile_area). Stochastic 80% during training.', detail: 'Tile: 8×8. Parameters from Exp 2 sweep. Stochastic = regularization. Dual-constraint prevents OD over-enhancement.' },
  { id: 7, nm: 'Stage 6: Augmentation (train only)', desc: 'Integrated affine augmentation: 360° rotation (circular FOV), flips, adaptive PCA color jitter, brightness/contrast. Applied only during training, never at inference.', detail: '360° rotation valid because circular FOV. Rotation magnitude σ_θ adapted from Stage 1 OD-fovea detection confidence.' },
  { id: 8, nm: 'Stage 7: Dataset-specific normalize → 4ch', desc: 'Dataset-specific channel-wise normalization statistics (not fixed ImageNet stats). Stack RGB + FOV mask → 4-channel tensor input to CNN.', detail: 'V5 change: dataset-specific mean/std computed from EyePACS training set. Output: 4ch (RGBM) tensor at 512×512.' },
];

// Computational metrics
export const COMPUTE = [
  { metric: 'Parameters', resnet: '25.6M', effnet: '12.2M', unit: '' },
  { metric: 'Train time/epoch', resnet: '8.5', effnet: '12.3', unit: 'min' },
  { metric: 'Inference (baseline)', resnet: '18.2', effnet: '24.5', unit: 'ms/img' },
  { metric: 'Inference (+pipeline)', resnet: '45.3', effnet: '51.8', unit: 'ms/img' },
  { metric: 'Pipeline overhead', resnet: '27.1', effnet: '27.3', unit: 'ms/img' },
  { metric: 'GPU memory (train)', resnet: '4.2', effnet: '6.8', unit: 'GB' },
  { metric: 'Batch size', resnet: '32', effnet: '16', unit: 'images' },
];

// Statistical tests — 6 rows
export const STAT_TESTS = [
  { test: 'DeLong (ROC-AUC)', resnet: 'p=0.42', effnet: 'p=0.008 ✓' },
  { test: 'McNemar', resnet: 'p=0.38', effnet: 'p=0.012 ✓' },
  { test: 'Bootstrap 95% CI (ΔF1)', resnet: '[−1.8, +1.6]pp', effnet: '[+2.8, +7.8]pp ✓' },
  { test: 'Mixed-effects ANOVA', resnet: '—', effnet: 'interaction p=0.02 ✓' },
  { test: 'Holm-corrected p', resnet: 'p_adj=1.0', effnet: 'p_adj=0.024 ✓' },
  { test: 'Bonferroni-corrected p (Exp 2)', resnet: '—', effnet: 'p_adj=0.042 ✓' },
];

// Training-test gap
export const TRAIN_TEST_GAP = [
  { config: 'A', trainF1: 0.82, testF1: 0.762, gap: 5.8 },
  { config: 'B', trainF1: 0.83, testF1: 0.761, gap: 6.9 },
  { config: 'C', trainF1: 0.80, testF1: 0.727, gap: 7.3 },
  { config: 'D', trainF1: 0.85, testF1: 0.780, gap: 7.0 },
];

// Datasets — 7 entries (comprehensive)
export const DATASETS = [
  {
    name: 'EyePACS',
    tier: 'Training', tierColor: 'blue', status: 'active',
    size: '~35,126 labeled', sizeUsed: '~35,126 (100%)',
    camera: 'Canon CR-1', cameraType: 'Non-mydriatic', fov: '45°',
    resolution: '3888×2592 to 5184×3456', format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4)', taxonomyMapping: null,
    source: 'Kaggle', availability: 'Public',
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
      'Largest publicly available DR dataset with 5-class grading — provides sufficient statistical power for 5-fold CV',
      'Single-camera acquisition (Canon CR-1) ensures training data has consistent imaging characteristics',
      'Bilateral image pairs (left + right eye per patient) enable patient-level splitting to prevent data leakage',
      'Severe class imbalance (73.5% DR 0) reflects real-world screening distribution — results are clinically realistic',
      'Widely used benchmark in DR classification literature — enables direct comparison with prior work',
    ],
    experiments: ['Exp 1 (H-1)', 'Exp 2 (H-2)'],
    limitations: [
      'Severe class imbalance: DR 3+4 together are only 4.5% of dataset',
      'Single screening programme — may not represent global population diversity',
      'Variable image quality — some images ungradable (~19.9% per Voets et al., 2019)',
    ],
    splitStrategy: '5-fold patient-level stratified CV. Patient ID = numeric prefix before _left/_right in filename. Both eyes of same patient always in same fold.',
  },
  {
    name: 'APTOS 2019',
    tier: 'Transfer', tierColor: 'blue', status: 'active',
    size: '3,662', sizeUsed: '3,662 (full, zero-shot transfer)',
    camera: 'Various (unspecified)', cameraType: 'Mixed', fov: 'Various',
    resolution: 'Various', format: 'PNG',
    taxonomy: '5-class ICDR (DR 0–4)', taxonomyMapping: null,
    source: 'Kaggle', availability: 'Public',
    population: 'Indian (Aravind Eye Hospital, rural screening)',
    classDistribution: {
      'DR 0': { count: 1805, pct: 49.3 },
      'DR 1': { count: 370, pct: 10.1 },
      'DR 2': { count: 999, pct: 27.3 },
      'DR 3': { count: 193, pct: 5.3 },
      'DR 4': { count: 295, pct: 8.1 },
    },
    role: 'Cross-dataset transferability target for Experiment 3 (H-4). Zero-shot transfer from EyePACS-trained model. Generalization ratio G = F1_APTOS / F1_EyePACS must meet G ≥ 0.85 threshold.',
    whyChosen: [
      'Large, well-known benchmark with 5-class DR grading matching EyePACS taxonomy',
      'Indian population data provides demographic diversity from EyePACS (US screening)',
      'Mixed camera sources test cross-device generalization within same experiment',
    ],
    experiments: ['Exp 3 (H-4): Cross-dataset transferability'],
    limitations: [
      'Mixed camera sources — domain shift from EyePACS expected',
      'No pixel-level annotations — cannot be used for explainability evaluation',
    ],
    splitStrategy: 'Zero-shot transfer — no training on APTOS 2019. Evaluated directly using EyePACS-trained model.',
  },
  {
    name: 'IDRiD',
    tier: 'Clinical', tierColor: 'teal', status: 'active',
    size: '516 images', sizeUsed: '516 (full) + 81 with pixel-level lesion masks',
    camera: 'Kowa VX-10α', cameraType: 'Mydriatic digital fundus camera', fov: '50°',
    resolution: '4288×2848', format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4) + pixel-level lesion masks', taxonomyMapping: null,
    source: 'IEEE DataPort', availability: 'Public (CC-BY 4.0)',
    population: 'Indian (Sushrusha Hospital, Nanded, Maharashtra, 2009–2017)',
    classDistribution: null,
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
    tier: 'External', tierColor: 'purple', status: 'active',
    size: '1,748 images', sizeUsed: '1,748 (full)',
    camera: 'Topcon TRC NW6', cameraType: 'Non-mydriatic', fov: '45°',
    resolution: '1440×960 to 2240×1488', format: 'TIFF',
    taxonomy: 'Referable / Non-referable DR',
    taxonomyMapping: 'Messidor grade 0→DR 0, grade 1→DR 1, grade 2→DR 2. Grades 3–4 not directly available — binary referable/non-referable used for clinical screening evaluation.',
    source: 'ADCIS (upon registration)', availability: 'Public (registration required)',
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
      'Label mapping introduces approximation — Messidor grades 0–2 mapped to DR 0–2; grades 3–4 not directly available',
      'Registration-gated access limits perfect reproducibility',
    ],
    splitStrategy: 'Used entirely as external test set (no training on this data).',
  },
  {
    name: 'DDR',
    tier: 'Domain', tierColor: 'coral', status: 'active',
    size: '13,673 images', sizeUsed: '13,673 (full)',
    camera: 'Canon, Topcon (mixed)', cameraType: 'Various', fov: 'Various',
    resolution: 'Various', format: 'JPEG',
    taxonomy: '6-class DR (0–5) + lesion annotations',
    taxonomyMapping: 'DDR grade 5 (ungradable) excluded. Grades 0–4 map directly to ICDR 0–4.',
    source: 'GitHub (Li et al., 2019)', availability: 'Public',
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
    tier: 'Domain', tierColor: 'coral', status: 'active',
    size: '5,000 patients (bilateral)', sizeUsed: 'DR subset extracted via keyword mapping',
    camera: 'Canon, Zeiss (mixed)', cameraType: 'Various', fov: 'Various',
    resolution: 'Various', format: 'JPEG',
    taxonomy: 'Multi-disease diagnostic keywords',
    taxonomyMapping: 'Keyword-to-grade mapping: "proliferative DR"→4, "severe DR"→3, "moderate DR"→2, "mild DR"→1, unqualified "DR"→2 (conservative), "laser spot"→4. Non-DR eyes of DR patients excluded.',
    source: 'Peking University (ODIR competition)', availability: 'Public',
    population: 'Chinese (multi-hospital, Beijing)',
    classDistribution: null,
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with Canon+Zeiss acquisition — Zeiss cameras are not present in any other dataset.',
    whyChosen: [
      'Contains Zeiss camera images — the ONLY dataset in our architecture with Zeiss acquisition, providing maximum device diversity',
      'Bilateral format (both eyes per patient) provides patient-level evaluation consistency',
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
    tier: 'Domain', tierColor: 'coral', status: 'active',
    size: '3,200 images', sizeUsed: 'DR subset (binary: DR present / absent)',
    camera: 'Topcon, Kowa (mixed)', cameraType: 'Various', fov: 'Various',
    resolution: 'Various', format: 'PNG',
    taxonomy: 'Multi-disease with binary DR column (0/1)',
    taxonomyMapping: 'Uses binary DR label only (0 = no DR, 1 = DR present). 5-class severity grading not available — evaluated as binary classification or excluded from per-class analysis.',
    source: 'IEEE DataPort', availability: 'Public',
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

export const CAMERA_GROUPS = {
  'Canon':  ['EyePACS', 'DDR', 'ODIR-5K'],
  'Topcon': ['Messidor-2', 'RFMiD', 'DDR'],
  'Kowa':   ['IDRiD', 'RFMiD'],
  'Zeiss':  ['ODIR-5K'],
};

export const DATASET_TIERS = [
  { name: 'Training', color: 'blue', description: 'Primary training and evaluation', datasets: ['EyePACS'] },
  { name: 'Transfer', color: 'blue', description: 'Cross-dataset transferability (H-4)', datasets: ['APTOS 2019'] },
  { name: 'Clinical', color: 'teal', description: 'Lesion masks + parameter validation + small data', datasets: ['IDRiD'] },
  { name: 'Degradation', color: 'purple', description: 'Clinical degradation resistance (H-7)', datasets: ['Messidor-2'] },
  { name: 'Domain', color: 'coral', description: 'Device domain shift evaluation (H-6)', datasets: ['DDR', 'ODIR-5K', 'RFMiD'] },
];

// Hypotheses — 6 active
export const HYPOTHESES = [
  { id: 'H-1', name: 'Preprocessing Dominance', exp: 'Exp 1', status: '✓ Confirmed', detail: 'EfficientNet-B3: ΔF1=+5.3pp, ΔAUC=+4.4pp (p=0.008)' },
  { id: 'H-2', name: 'V5 Component Ablation + CLAHE/σ', exp: 'Exp 2', status: '✓ Confirmed', detail: 'Local optimum at clip_factor=2.5/2.0, threshold=0.03' },
  { id: 'H-4', name: 'Cross-Dataset Transfer (APTOS)', exp: 'Exp 3', status: 'Pending V5', detail: 'G ≥ 0.85 on APTOS 2019 target' },
  { id: 'H-5', name: 'Explainability (ALO)', exp: 'Exp 4', status: '✓ Confirmed', detail: 'ALO +31–61% across all lesion types' },
  { id: 'H-6', name: 'Device Domain Shift', exp: 'Exp 6', status: '✓ Confirmed', detail: 'Cross-device variance −46%' },
  { id: 'H-7', name: 'Clinical Degradation Resistance', exp: 'Exp 5', status: 'Pending V5', detail: 'V5 reduces cross-dataset performance drop vs baseline' },
];
