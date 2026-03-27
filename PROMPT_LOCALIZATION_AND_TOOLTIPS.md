# Claude Code Task: Add EN/KZ Localization + Image Tooltips

## Context

You are working on `~/dissertation-demo` — a React (CRA) dashboard for PhD defense. Read `~/dissertation-demo/CLAUDE.md` first.

Two features:
1. **Bilingual UI (English / Kazakh)** — all dashboard text must switch between EN and KZ
2. **Image tooltips** — hovering over any chart/figure shows an explanatory popup

## Source Materials

- `~/dissertation-demo/GLOSSARY_KZ.md` — Official EN→KZ translation glossary (229 term pairs). **Read this file first** — it defines which terms stay in English and which get translated to Kazakh.

## PART 1: Localization System

### Architecture

Create a lightweight i18n system WITHOUT external libraries (no react-intl, no i18next). Use React Context + a JSON translations object.

#### Step 1: Create `src/i18n.js`

```jsx
import { createContext, useContext, useState } from 'react';

// Language context
const LangContext = createContext();

export function LangProvider({ children }) {
  const [lang, setLang] = useState('en'); // default English
  return (
    <LangContext.Provider value={{ lang, setLang, t: (key) => translations[lang]?.[key] || translations['en'][key] || key }}>
      {children}
    </LangContext.Provider>
  );
}

export function useLang() {
  return useContext(LangContext);
}

// All UI translations
const translations = { en: { /* ... */ }, kz: { /* ... */ } };
```

#### Step 2: Translation Keys

Build the `translations` object with ALL UI text. Structure it by section. Here are the key translations needed. **Follow the glossary rules strictly:**
- Technical terms (CNN, CLAHE, F1-Score, ROC-AUC, EyePACS, etc.) stay in English in BOTH languages
- Conceptual terms get Kazakh translations per GLOSSARY_KZ.md Section B

**Navigation items:**
```js
en: {
  // Navigation
  'nav.overview': 'Overview',
  'nav.model': 'Model',
  'nav.model.architecture': 'Architecture',
  'nav.model.pipeline': 'Pipeline',
  'nav.model.methods': 'Methods',
  'nav.model.explainability': 'Explainability',
  'nav.datasets': 'Datasets',
  'nav.experiments': 'Experiments',
  'nav.experiments.h1': 'H-1: Preprocessing',
  'nav.experiments.h2': 'H-2: CLAHE',
  'nav.experiments.h4': 'H-4: Transfer',
  'nav.experiments.h5': 'H-5: Explainability',
  'nav.experiments.h6': 'H-6: Robustness',
  'nav.results': 'Results',
  'nav.results.main': 'Main Metrics',
  'nav.results.bestConfig': 'Best Config (D)',
  'nav.results.statistical': 'Statistical Tests',
  'nav.validation': 'Validation',
  'nav.validation.clinical': 'Clinical',
  'nav.validation.quality': 'Image Quality',
  'nav.validation.compute': 'Computational',
},
kz: {
  'nav.overview': 'Шолу',
  'nav.model': 'Модель',
  'nav.model.architecture': 'Архитектура',
  'nav.model.pipeline': 'Pipeline',
  'nav.model.methods': 'Әдістер',
  'nav.model.explainability': 'Түсіндірмелілік',
  'nav.datasets': 'Деректер жиынтықтары',
  'nav.experiments': 'Эксперименттер',
  'nav.experiments.h1': 'H-1: Алдын ала өңдеу',
  'nav.experiments.h2': 'H-2: CLAHE',
  'nav.experiments.h4': 'H-4: Тасымалдау',
  'nav.experiments.h5': 'H-5: Түсіндірмелілік',
  'nav.experiments.h6': 'H-6: Төзімділік',
  'nav.results': 'Нәтижелер',
  'nav.results.main': 'Негізгі метрикалар',
  'nav.results.bestConfig': 'Үздік конфигурация (D)',
  'nav.results.statistical': 'Статистикалық тесттер',
  'nav.validation': 'Валидация',
  'nav.validation.clinical': 'Клиникалық',
  'nav.validation.quality': 'Кескін сапасы',
  'nav.validation.compute': 'Есептеу',
},
```

**Section titles and body text — follow this approach for EVERY tab:**

For each piece of text currently in the dashboard, create an EN key and a KZ key. Examples:

```js
en: {
  // Overview
  'overview.title': 'Dissertation Dashboard',
  'overview.subtitle': 'Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification',
  'overview.candidate': 'Candidate: Yesmukhamedov N.S. (IITU)',
  'overview.centralThesis': 'Central thesis: model = preprocessing + CNN',
  'overview.bestConfig': 'Best Configuration — Config D',
  'overview.hypothesisStatus': 'Hypothesis Status',
  'overview.confirmed': 'Confirmed',

  // Common
  'common.baseline': 'Baseline',
  'common.pipeline': 'Full V4 Pipeline',
  'common.improvement': 'Improvement',
  'common.config': 'Configuration',
  'common.preprocessing': 'Preprocessing',
  'common.architecture': 'Architecture',
  'common.dataset': 'Dataset',
  'common.camera': 'Camera',
  'common.size': 'Size',
  'common.role': 'Role',
  'common.experiment': 'Experiment',
  'common.metric': 'Metric',
  'common.value': 'Value',
  'common.threshold': 'Threshold',
  'common.satisfied': 'Satisfied',
  'common.unit': 'Unit',

  // Datasets
  'datasets.title': 'Tiered Dataset Architecture',
  'datasets.summary': 'Dataset Summary',
  'datasets.cameraMatrix': 'Camera Coverage Matrix',
  'datasets.classDistribution': 'EyePACS Class Distribution',
  'datasets.whyChosen': 'Why chosen',
  'datasets.limitations': 'Limitations',
  'datasets.taxonomyMapping': 'Taxonomy mapping',
  'datasets.splitStrategy': 'Split strategy',
  'datasets.tier.training': 'Training',
  'datasets.tier.clinical': 'Clinical',
  'datasets.tier.external': 'External',
  'datasets.tier.domain': 'Domain Shift',
  'datasets.tier.dropped': 'Dropped',

  // Experiments
  'exp.factorial': '2×2 Factorial Design',
  'exp.ablation': 'Cumulative Ablation',
  'exp.perStage': 'Per-Stage Marginal Contribution',
  'exp.dominanceCriterion': 'EH-3 Dominance Criterion Check',
  'exp.crossDataset': 'Cross-Dataset Generalization',
  'exp.deviceShift': 'Cross-Device Performance',
  'exp.alo': 'Attention-Lesion Overlap (ALO)',
  'exp.iou': 'Intersection-over-Union (IoU)',

  // Clinical
  'clinical.referableDR': 'Referable DR Screening (Grade ≥ 2)',
  'clinical.sensitivity': 'Sensitivity',
  'clinical.specificity': 'Specificity',
  'clinical.calibration': 'Probability Calibration',
  'clinical.trainTestGap': 'Training-Test Gap',

  // Pipeline / Methods
  'pipeline.title': 'V4 6-Stage Preprocessing Pipeline',
  'pipeline.stageWalkthrough': 'Stage-by-Stage Walkthrough',
  'pipeline.bilateralPair': 'Bilateral Pair Demo',
  'pipeline.beforeAfter': 'Before / After',
  'methods.standardApproach': 'Standard Approach',
  'methods.ourAdaptation': 'Our V4 Adaptation',
  'methods.keyInnovation': 'Key Innovation',
},
kz: {
  'overview.title': 'Диссертация Dashboard',
  'overview.subtitle': 'Көз түбі кескінін жақсарту және CNN жіктеу арқылы диабеттік ретинопатияны автоматтандырылған диагностикалау',
  'overview.candidate': 'Кандидат: Есмұхамедов Н.С. (ХАТУ)',
  'overview.centralThesis': 'Негізгі тезис: модель = алдын ала өңдеу + CNN',
  'overview.bestConfig': 'Үздік конфигурация — Config D',
  'overview.hypothesisStatus': 'Гипотезалар күйі',
  'overview.confirmed': 'Расталды',

  'common.baseline': 'Baseline',
  'common.pipeline': 'Толық V4 Pipeline',
  'common.improvement': 'Жақсару',
  'common.config': 'Конфигурация',
  'common.preprocessing': 'Алдын ала өңдеу',
  'common.architecture': 'Архитектура',
  'common.dataset': 'Деректер жиынтығы',
  'common.camera': 'Камера',
  'common.size': 'Көлемі',
  'common.role': 'Рөлі',
  'common.experiment': 'Эксперимент',
  'common.metric': 'Метрика',
  'common.value': 'Мән',
  'common.threshold': 'Шектік мән',
  'common.satisfied': 'Қанағаттандырылды',
  'common.unit': 'Бірлік',

  'datasets.title': 'Деңгейлік деректер жиынтықтары архитектурасы',
  'datasets.summary': 'Деректер жиынтықтары қорытындысы',
  'datasets.cameraMatrix': 'Камера қамту матрицасы',
  'datasets.classDistribution': 'EyePACS класс үлестірімі',
  'datasets.whyChosen': 'Таңдау себебі',
  'datasets.limitations': 'Шектеулер',
  'datasets.taxonomyMapping': 'Таксономия сәйкестендіру',
  'datasets.splitStrategy': 'Бөлу стратегиясы',
  'datasets.tier.training': 'Оқыту',
  'datasets.tier.clinical': 'Клиникалық',
  'datasets.tier.external': 'Сыртқы',
  'datasets.tier.domain': 'Домен ығысуы',
  'datasets.tier.dropped': 'Алынып тасталған',

  'exp.factorial': '2×2 факторлық дизайн',
  'exp.ablation': 'Кумулятивтік абляция',
  'exp.perStage': 'Кезең бойынша маржиналды үлес',
  'exp.dominanceCriterion': 'EH-3 басымдық критерийін тексеру',
  'exp.crossDataset': 'Деректер жиынтықтары арасындағы жалпылау',
  'exp.deviceShift': 'Құрылғылар арасындағы өнімділік',
  'exp.alo': 'Назар-зақымдану қабаттасуы (ALO)',
  'exp.iou': 'Intersection-over-Union (IoU)',

  'clinical.referableDR': 'Жіберілетін DR скринингі (Grade ≥ 2)',
  'clinical.sensitivity': 'Сезімталдық',
  'clinical.specificity': 'Спецификалық',
  'clinical.calibration': 'Ықтималдық калибрлеу',
  'clinical.trainTestGap': 'Оқыту-тест алшақтығы',

  'pipeline.title': 'V4 6-кезеңді алдын ала өңдеу Pipeline',
  'pipeline.stageWalkthrough': 'Кезең бойынша шолу',
  'pipeline.bilateralPair': 'Екі жақты жұп көрсетілімі',
  'pipeline.beforeAfter': 'Дейін / Кейін',
  'methods.standardApproach': 'Стандартты тәсіл',
  'methods.ourAdaptation': 'Біздің V4 бейімделу',
  'methods.keyInnovation': 'Негізгі инновация',
},
```

**CRITICAL GLOSSARY RULES (from GLOSSARY_KZ.md):**
- Terms that STAY in English in Kazakh text: CNN, CLAHE, ResNet-50, EfficientNet-B3, F1-Score, ROC-AUC, Cohen's Kappa, Accuracy, Precision, Recall, Grad-CAM, IoU, ALO, Pipeline, Baseline, Fine-Tuning, EyePACS, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD, ImageNet, FOV, SSIM, ECE, Bootstrap, Mixed-Effects Model, Dropout, Batch Normalization, Data Augmentation
- Terms that get translated: Diabetic Retinopathy → Диабеттік ретинопатия, Fundus Image → Көз түбі кескіні, Preprocessing → Алдын ала өңдеу, Image Quality → Кескін сапасы, Class Imbalance → Класс теңгерімсіздігі, Sensitivity → Сезімталдық, Specificity → Спецификалық, Overfitting → Артық үйрену, Generalization → Жалпылау қабілеті, Flat-Field Correction → Жарық өрісін түзету
- Hybrid terms (first use bilingual): "Конволюциялық нейрондық желі (CNN)" then "CNN" thereafter

#### Step 3: Language Switcher Component

Create a toggle button in the top-right corner of the dashboard (or in the sidebar header):

```jsx
function LangSwitcher() {
  const { lang, setLang } = useLang();
  return (
    <div style={{ display: 'flex', gap: 4, fontSize: 12 }}>
      <button
        onClick={() => setLang('en')}
        style={{
          padding: '3px 10px', borderRadius: 4, border: 'none', cursor: 'pointer',
          background: lang === 'en' ? '#1D9E75' : 'var(--color-background-secondary,#eee)',
          color: lang === 'en' ? 'white' : 'var(--color-text-secondary,#666)',
          fontWeight: lang === 'en' ? 600 : 400,
        }}
      >EN</button>
      <button
        onClick={() => setLang('kz')}
        style={{
          padding: '3px 10px', borderRadius: 4, border: 'none', cursor: 'pointer',
          background: lang === 'kz' ? '#1D9E75' : 'var(--color-background-secondary,#eee)',
          color: lang === 'kz' ? 'white' : 'var(--color-text-secondary,#666)',
          fontWeight: lang === 'kz' ? 600 : 400,
        }}
      >ҚАЗ</button>
    </div>
  );
}
```

#### Step 4: Apply to All Components

In every component, replace hardcoded English text with `t('key')`:

```jsx
// Before:
<h3>Hypothesis Status</h3>

// After:
const { t } = useLang();
<h3>{t('overview.hypothesisStatus')}</h3>
```

**For section notes and longer explanatory text:** Create translation keys for each note. If a note is complex, it's OK to have a long value:

```js
'exp1.note.factorial': 'Configs A/B/C/D: 3-fold CV on 40% EyePACS (~14,050 images). Config D: EfficientNet-B3 + full pipeline. Highlighted row = best configuration.',
// KZ:
'exp1.note.factorial': 'A/B/C/D конфигурациялары: 40% EyePACS-те (~14,050 кескін) 3-fold CV. D конфигурациясы: EfficientNet-B3 + толық pipeline. Ерекшеленген қатар = үздік конфигурация.',
```

**For data labels in tables (DR 0, DR 1, etc.):** These are clinical terms and stay the same in both languages. Column headers get translated.

#### Step 5: Wrap App in LangProvider

In `src/index.js` or `src/App.js`:
```jsx
<LangProvider>
  <App />
</LangProvider>
```

### Implementation Strategy — DO NOT Translate Everything at Once

This is a large codebase. Use this phased approach:

**Phase 1 (this task):** Set up the i18n infrastructure + translate:
- Navigation / sidebar labels
- Section titles (`<h3>`, `<Sec title=...>`)
- Table column headers
- Card labels
- Badge text
- Footer text
- Language switcher

**Phase 2 (can be deferred):** Translate:
- Long explanatory notes (the `note` props on `<Sec>`)
- Pipeline stage descriptions
- Methods page body text
- Dataset detail card text

For Phase 2 content, use a fallback: if a KZ translation doesn't exist for a key, fall back to the EN text. This way the app works immediately even with partial translations.

**The `t()` function already handles this:** `translations[lang]?.[key] || translations['en'][key] || key`

### IMPORTANT: Numerical Values Never Change

All numbers, metric values, percentages, p-values, confidence intervals etc. are language-independent. Only UI labels and descriptive text change.

---

## PART 2: Image Tooltips

### What It Does

When the user hovers over any chart image (`<img>`) or figure in the dashboard, a tooltip appears explaining what the image shows. On mobile, tap to show.

### Architecture

Create a reusable `ImageWithTooltip` component:

```jsx
function ImageWithTooltip({ src, alt, tooltip, figNum, caption, style }) {
  const [show, setShow] = useState(false);
  const { t } = useLang();
  
  // tooltip can be a translation key or direct string
  const tooltipText = typeof tooltip === 'string' && tooltip.startsWith('tooltip.')
    ? t(tooltip)
    : tooltip;
  
  return (
    <div
      style={{ position: 'relative', marginBottom: 16, ...style }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onClick={() => setShow(!show)} // mobile tap toggle
    >
      <img
        src={src}
        alt={alt || tooltipText}
        style={{
          width: '100%',
          borderRadius: 8,
          border: '1px solid var(--color-border-tertiary,#eee)',
          cursor: 'help',
        }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4 }}>
          {figNum && <strong>Fig. {figNum}. </strong>}{caption}
        </div>
      )}
      {show && tooltipText && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginBottom: 8,
          padding: '10px 14px',
          background: 'rgba(0,0,0,0.88)',
          color: 'white',
          borderRadius: 8,
          fontSize: 12,
          lineHeight: 1.5,
          maxWidth: 400,
          width: 'max-content',
          zIndex: 1000,
          pointerEvents: 'none',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        }}>
          {tooltipText}
          <div style={{
            position: 'absolute',
            top: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0, height: 0,
            borderLeft: '6px solid transparent',
            borderRight: '6px solid transparent',
            borderTop: '6px solid rgba(0,0,0,0.88)',
          }} />
        </div>
      )}
    </div>
  );
}
```

### Tooltip Content — All 28 Result Chart Images

Add tooltip translation keys for every chart. These are bilingual (EN and KZ). Each tooltip is 1-3 sentences explaining what the figure shows.

```js
en: {
  // Result chart tooltips
  'tooltip.fig01': 'Weighted F1-score for the 4 factorial configurations (A-D). Config D (EfficientNet-B3 + full pipeline) achieves the highest F1 of 0.780. Error bars show ±1 standard deviation across 3 folds.',
  'tooltip.fig02': 'All four primary metrics (F1, AUC, κ, Accuracy) side by side. Config D outperforms all others on every metric.',
  'tooltip.fig03': 'Preprocessing improvement delta: ResNet-50 shows near-zero effect, EfficientNet-B3 shows +5.3pp F1. Red line = EH-3 threshold.',
  'tooltip.fig04': 'Cumulative ablation: each pipeline stage added sequentially. Monotonic increase confirms every stage contributes positively.',
  'tooltip.fig05': 'Per-stage marginal contribution. CLAHE (Stage 3) contributes the most: +1.4pp F1.',
  'tooltip.fig06': 'ALO (Attention-Lesion Overlap) by lesion type. Pipeline improves attention to all lesion types by 31-61%.',
  'tooltip.fig07': 'IoU by lesion type. Secondary metric — lower values than ALO because IoU penalizes excessive activation.',
  'tooltip.fig08': 'Cross-dataset F1 and AUC. Performance drop on external datasets is reduced by preprocessing.',
  'tooltip.fig09': 'Generalization ratio G = F1_external / F1_EyePACS. Pipeline achieves G ≥ 0.85 on both datasets (H-4 threshold).',
  'tooltip.fig10': 'F1 across 6 camera groups. Pipeline consistently improves performance; largest gains on most distant cameras.',
  'tooltip.fig11': 'Radar chart: pipeline (teal) uniformly encloses baseline (gray) on all 6 dimensions.',
  'tooltip.fig12': 'EH-3 check: EfficientNet-B3 exceeds all thresholds. ResNet-50 shows near-zero deltas — architecture-dependent effect.',
  'tooltip.fig13': 'CLAHE parameter sensitivity heatmap. DR1 optimal at clip_factor=2.5, DR2 at 2.0. Both at global_threshold=0.03.',
  'tooltip.fig14': 'Clinical screening metrics for referable DR. Pipeline improves sensitivity from 0.82 to 0.90 (+8pp).',
  'tooltip.fig15': 'Calibration: ECE reduced by 45%, Brier Score by 23%. Pipeline curve follows the diagonal more closely.',
  'tooltip.fig16': 'Image quality metrics. CNR improves by 81%, vessel visibility by 51%.',
  'tooltip.fig17': 'Computational comparison. EfficientNet-B3 has fewer parameters but longer training due to compound scaling.',
  'tooltip.fig18': 'Per-class F1. Largest improvements on minority classes: DR1 +12pp, DR3 +12pp.',
  'tooltip.fig19': 'Training curves. Config D converges faster and achieves higher plateau than Config C.',
  'tooltip.fig20': 'Confusion matrices. Pipeline reduces off-diagonal confusion, especially between adjacent DR grades.',
  'tooltip.fig21': 'Statistical tests. EfficientNet-B3: DeLong p=0.008, McNemar p=0.012 — both significant at α=0.05.',
  'tooltip.fig22': 'All 6 configs including binocular (E, F). Binocular adds ~+1pp over single-image pipeline configs.',
  'tooltip.fig23': 'Individual ablation: each stage added independently. CLAHE alone adds +2.3pp (largest individual effect).',
  'tooltip.fig24': 'Per-class ROC curves. Pipeline shifts all curves upward. DR1 shows largest AUC improvement (0.72→0.81).',
  'tooltip.fig25': 'Real fundus image (patient 43199, DR4) through all V4 pipeline stages.',
  'tooltip.fig26': 'Bilateral pair showing both eyes. After canonical flip, both have OD on right side.',
  'tooltip.fig27': 'Grad-CAM overlays. Baseline: diffuse attention. Pipeline: focused on hemorrhages and exudates.',
  'tooltip.fig28': 'Attention consistency: cosine similarity of Grad-CAM across datasets. Pipeline mean 0.81 vs. baseline 0.61.',

  // Pipeline stage image tooltips
  'tooltip.pipeline_grid': 'Complete V4 pipeline: Raw → Canonical Flip → FOV Crop 512×512 → Flat-Field (σ=45) → CLAHE (dual-constraint) → ImageNet Normalization. Patient 43199, Canon CR-1, DR4.',
  'tooltip.bilateral': 'Both eyes of patient 43199 (DR4). Left eye flipped to match right-eye orientation. After full pipeline, lesions become clearly visible.',
  'tooltip.stage_raw': 'Raw EyePACS fundus photograph. Variable illumination, black borders, 2000×1333 JPEG from Canon CR-1.',
  'tooltip.stage_0a': 'Stage 0a: Left eye horizontally flipped so optic disc is on the right (canonical orientation).',
  'tooltip.stage_1': 'Stage 1: Black borders removed, fundus centered and resized to 512×512 using PIL LANCZOS resampling.',
  'tooltip.stage_2': 'Stage 2: Flat-field correction removes illumination gradient. Formula: corrected = image − blur(σ=45) + 128.',
  'tooltip.stage_3': 'Stage 3: Upgraded CLAHE with dual-constraint clip limit dramatically enhances vessel and lesion contrast.',
  'tooltip.stage_4': 'Stage 4: ImageNet channel-wise normalization. Visual appearance similar to CLAHE output.',

  // Methods image tooltips
  'tooltip.method_flip': 'Canonical flip comparison: left eye (OD on left) → flipped (OD on right) → right eye (already correct).',
  'tooltip.method_flatfield': 'Flat-field: input → estimated illumination envelope (blur σ=45) → corrected (uniform brightness).',
  'tooltip.method_clahe_cmp': 'Standard CLAHE (cv2, clip=2.0) vs. Upgraded CLAHE (dual-constraint). Green border = our method.',
  'tooltip.method_clahe_sens': 'CLAHE clip_factor sweep from 0.5 to 4.0. Optimal range 2.0-3.0. Over-enhancement at >3.5 amplifies noise.',
  'tooltip.method_fov': 'FOV detection: PIL foreground sampling detects fundus boundary. Removes black borders that waste CNN capacity.',
  'tooltip.method_augment': '8 augmentation examples. 360° rotation is valid because circular FOV makes corner pixels empty.',
  'tooltip.method_odfovea': 'OD-fovea detection in 4 steps: green channel → OD mask (97th percentile) → annular fovea search → axis angle.',
  'tooltip.method_search': 'Annular search region: fovea is always 1.5-3.5 OD diameters from the optic disc (anatomical prior).',
  'tooltip.baseline_vs_pipe': 'Baseline (crop+resize only) vs. full pipeline. Difference map (×3) highlights regions most affected.',
  'tooltip.before_after': 'Before: original image after basic crop. After: full V4 pipeline. Vessels and lesions dramatically clearer.',
},
kz: {
  'tooltip.fig01': 'A-D конфигурациялары үшін weighted F1-score. D конфигурациясы (EfficientNet-B3 + толық pipeline) ең жоғары F1=0.780 көрсетеді.',
  'tooltip.fig02': 'Төрт негізгі метрика (F1, AUC, κ, Accuracy) қатар. D конфигурациясы барлық метрикалар бойынша үздік.',
  'tooltip.fig03': 'Алдын ала өңдеу жақсаруы: ResNet-50 нөлге жуық, EfficientNet-B3 +5.3пп F1. Қызыл сызық = EH-3 шегі.',
  'tooltip.fig04': 'Кумулятивтік абляция: әрбір pipeline кезеңі кезекпен қосылады. Монотонды өсу әрбір кезеңнің үлесін растайды.',
  'tooltip.fig05': 'Кезең бойынша маржиналды үлес. CLAHE (3-кезең) ең көп үлес қосады: +1.4пп F1.',
  'tooltip.fig06': 'Зақымдану түрі бойынша ALO. Pipeline барлық зақымдану түрлеріне назарды 31-61% жақсартады.',
  'tooltip.fig09': 'Жалпылау коэффициенті G = F1_external / F1_EyePACS. Pipeline екі деректер жиынтығында G ≥ 0.85 (H-4 шегі).',
  'tooltip.fig11': 'Радар диаграммасы: pipeline (көк-жасыл) барлық 6 өлшемде baseline-ді (сұр) қамтиды.',
  'tooltip.fig12': 'EH-3 тексерісі: EfficientNet-B3 барлық шектерден асады. ResNet-50 нөлге жуық — архитектураға тәуелді әсер.',
  'tooltip.fig14': 'Клиникалық скрининг метрикалары. Pipeline сезімталдықты 0.82-ден 0.90-ға жақсартады (+8пп).',
  'tooltip.fig18': 'Класс бойынша F1. Ең үлкен жақсару азшылық кластарда: DR1 +12пп, DR3 +12пп.',
  'tooltip.pipeline_grid': 'Толық V4 pipeline: Raw → Canonical Flip → FOV Crop 512×512 → Flat-Field (σ=45) → CLAHE → ImageNet Normalization. Науқас 43199, Canon CR-1, DR4.',
  'tooltip.bilateral': 'Науқас 43199 (DR4) екі көзі. Сол көз оң көз бағдарына сәйкес айналдырылған. Толық pipeline кейін зақымданулар анық көрінеді.',
  'tooltip.stage_3': '3-кезең: Қос шектеулі CLAHE тамыр мен зақымдану контрастын күрт жақсартады.',
  // ... remaining KZ tooltips follow the same pattern
  // For tooltips without explicit KZ translation, the EN fallback is used automatically
},
```

### Step 6: Replace All `<img>` Tags

Find every `<img>` tag in the codebase and wrap it with `ImageWithTooltip`:

```jsx
// Before:
<img src="/results/01_exp1_factorial_f1.png" style={{ width: '100%' }} />

// After:
<ImageWithTooltip
  src="/results/01_exp1_factorial_f1.png"
  tooltip="tooltip.fig01"
  figNum={1}
  caption={t('fig01.caption')}  // optional
/>
```

For pipeline stage images in the stepper:
```jsx
<ImageWithTooltip
  src="/pipeline/stage_3_clahe.png"
  tooltip="tooltip.stage_3"
/>
```

### Step 7: Export Components

Export `ImageWithTooltip` and `LangSwitcher` from `src/components.js` (or wherever shared components live) so all tabs can use them.

---

## Critical Rules

1. **ALL Kazakh text must follow GLOSSARY_KZ.md** — read it before writing translations
2. **Technical terms stay in English** in Kazakh mode (CNN, CLAHE, F1-Score, etc.)
3. **Numbers never change** between languages
4. **Fallback to English** if a KZ translation key doesn't exist
5. **No external i18n libraries** — pure React Context + JSON object
6. **Tooltips on ALL images** — no image without a tooltip
7. **Tooltip bilingual** — tooltip content switches with language
8. **No "synthesized", "projected" labels** in any language
9. **Mobile-friendly** — tooltips should work on tap (not just hover)

## Verification Checklist

```bash
cd ~/dissertation-demo && npm start
```

- [ ] Language switcher visible (top-right or sidebar header)
- [ ] Clicking EN/ҚАЗ switches ALL visible text
- [ ] Navigation labels change language
- [ ] Section titles change language
- [ ] Table column headers change language
- [ ] Technical terms (CNN, CLAHE, F1, etc.) stay English in KZ mode
- [ ] Numbers and metric values unchanged in both languages
- [ ] Tooltips appear on hover for ALL images
- [ ] Tooltip text switches with language
- [ ] Tooltips position correctly (above image, not clipped)
- [ ] Tooltips work on mobile (tap to show/hide)
- [ ] No console errors about missing translation keys
- [ ] App doesn't crash when switching languages rapidly
