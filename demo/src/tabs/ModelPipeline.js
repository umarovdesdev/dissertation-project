import { useEffect, useState } from 'react';
import { C, PIPE } from '../data';
import { Sec, Note, DataTable, DiagramViewer, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

const DR_GRADES = [
  { id: 'dr00', label: 'DR 0', sub: 'No DR' },
  { id: 'dr01', label: 'DR 1', sub: 'Mild NPDR' },
  { id: 'dr02', label: 'DR 2', sub: 'Moderate NPDR' },
  { id: 'dr03', label: 'DR 3', sub: 'Severe NPDR' },
  { id: 'dr04', label: 'DR 4', sub: 'Proliferative DR' },
];

// Default pair-of-eyes file list. Override per-view when the folder uses min/max naming.
const PAIR = ['left.png', 'right.png'];

// Per-step views. Each step exposes one or more sub-views; views are buttons the user can click.
// `folder` is relative to /pipeline/<dr>/. `files` defaults to PAIR; for augmentation min/max
// folders we list the four files explicitly so the grid can render both extremes.
const STAGE_VIEWS = {
  0: [
    { id: 'main', label: 'Raw input', folder: 'input' },
  ],
  1: [
    { id: 'main', label: 'Result', folder: 'preprocessing/stage_0_canonical_flip' },
  ],
  2: [
    { id: 'main', label: 'Rotated', folder: 'preprocessing/stage_1_od_fovea_rotation' },
    { id: 'image', label: 'With landmarks', folder: 'preprocessing/stage_1_od_fovea_rotation/image' },
    { id: 'od', label: 'OD detection', folder: 'preprocessing/stage_1_od_fovea_rotation/od' },
    { id: 'fovea', label: 'Fovea search', folder: 'preprocessing/stage_1_od_fovea_rotation/fovea' },
    { id: 'midpoint', label: 'OD–fovea midpoint', folder: 'preprocessing/stage_1_od_fovea_rotation/midpoint' },
  ],
  3: [
    { id: 'main', label: 'Cropped 512×512', folder: 'preprocessing/stage_2_fov_crop_resize' },
  ],
  4: [
    { id: 'main', label: 'FOV mask', folder: 'preprocessing/stage_3_fov_mask' },
  ],
  5: [
    { id: 'main', label: 'Flat-fielded', folder: 'preprocessing/stage_4_flatfield' },
  ],
  6: [
    { id: 'main', label: 'Our CLAHE', folder: 'preprocessing/stage_5_clahe',
      note: 'Final dual-constraint CLAHE on the LAB L-channel.' },
    { id: 'cv2', label: 'OpenCV CLAHE', folder: 'preprocessing/stage_5_clahe/cv2',
      note: 'Baseline cv2.createCLAHE for comparison — note over-enhancement near the optic disc.' },
    { id: 'polar_1_vessels', label: '1. Vessel detection',
      folder: 'preprocessing/stage_5_clahe/polar/1_vessel_detection',
      note: 'Polar-adaptive CLAHE — step 1: vessel mask derived from green-channel response.' },
    { id: 'polar_2_density', label: '2. Vessel density',
      folder: 'preprocessing/stage_5_clahe/polar/2_vessel_density',
      note: 'Step 2: vessel-density map (smoothed local count of vessel pixels).' },
    { id: 'polar_3_grid', label: '3. Polar grid',
      folder: 'preprocessing/stage_5_clahe/polar/3_polar_grid_adaptive',
      note: 'Step 3: adaptive polar grid that follows the retinal radial geometry.' },
    { id: 'polar_4_density_grid', label: '4. Density grid',
      folder: 'preprocessing/stage_5_clahe/polar/4_density_grid_adaptive',
      note: 'Step 4: per-tile clip limit modulated by local vessel density.' },
    { id: 'polar_5_no_interp', label: '5. No interpolation',
      folder: 'preprocessing/stage_5_clahe/polar/5_clahe_no_interpolation',
      note: 'Step 5: tiles equalized but not yet interpolated — visible block boundaries.' },
    { id: 'polar', label: 'Polar adaptive (final)',
      folder: 'preprocessing/stage_5_clahe/polar',
      note: 'Final polar-adaptive CLAHE result after bilinear interpolation.' },
  ],
  7: [
    {
      id: 'rotation', label: 'Rotation',
      folder: 'preprocessing/stage_6_augmentation/1_rotation',
      note: 'Train-only. Random 360° rotation — circular FOV makes any angle valid.',
    },
    {
      id: 'scale', label: 'Scale',
      folder: 'preprocessing/stage_6_augmentation/2_scale',
      files: ['left_min.png', 'right_min.png', 'left_max.png', 'right_max.png'],
      labels: ['Left · min', 'Right · min', 'Left · max', 'Right · max'],
      note: 'Augmentation range — top row: minimum scale, bottom row: maximum scale.',
    },
    {
      id: 'shear', label: 'Shear',
      folder: 'preprocessing/stage_6_augmentation/3_shear',
      files: ['left_min.png', 'right_min.png', 'left_max.png', 'right_max.png'],
      labels: ['Left · min', 'Right · min', 'Left · max', 'Right · max'],
      note: 'Augmentation range — top row: minimum shear, bottom row: maximum shear.',
    },
    {
      id: 'pca_color', label: 'PCA color',
      folder: 'preprocessing/stage_6_augmentation/4_pca_color_jitter',
      files: ['left_min.png', 'right_min.png', 'left_max.png', 'right_max.png'],
      labels: ['Left · min', 'Right · min', 'Left · max', 'Right · max'],
      note: 'PCA colour jitter range (perturbation along principal colour axes).',
    },
    {
      id: 'brightness', label: 'Brightness',
      folder: 'preprocessing/stage_6_augmentation/5_brightness_contrast',
      files: ['left_min.png', 'right_min.png', 'left_max.png', 'right_max.png'],
      labels: ['Left · min', 'Right · min', 'Left · max', 'Right · max'],
      note: 'Brightness/contrast augmentation range.',
    },
  ],
  8: [
    { id: 'main', label: 'Normalized → 4ch', folder: 'preprocessing/stage_7_normalize' },
  ],
};

const STAGE_PANEL_HEIGHT = 380;

function ImageGrid({ folder, drId, files, labels }) {
  const cols = 2;
  const rows = Math.ceil(files.length / cols);
  return (
    <div style={{
      display: 'grid', gap: 6, height: '100%',
      gridTemplateColumns: `repeat(${cols}, 1fr)`,
      gridTemplateRows: `repeat(${rows}, 1fr)`,
    }}>
      {files.map((f, i) => (
        <div key={i} style={{
          position: 'relative', minWidth: 0, minHeight: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          background: 'var(--color-background-primary,#fff)', borderRadius: 6,
          border: '1px solid var(--color-border-tertiary,#eee)',
        }}>
          <img
            src={`${process.env.PUBLIC_URL}/pipeline/${drId}/${folder}/${f}`}
            alt={labels?.[i] || f}
            style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', display: 'block' }}
          />
          <span style={{
            position: 'absolute', bottom: 4, left: 4,
            fontSize: 9, fontWeight: 600, color: '#fff',
            background: 'rgba(0,0,0,0.55)', padding: '1px 6px', borderRadius: 3,
            pointerEvents: 'none',
          }}>
            {labels?.[i] || (f.startsWith('left') ? 'Left' : 'Right')}
          </span>
        </div>
      ))}
    </div>
  );
}

function StagePanel({ stepIndex, drId, viewId }) {
  const views = STAGE_VIEWS[stepIndex] || [];
  const view = views.find(v => v.id === viewId) || views[0];

  if (!view) {
    return (
      <div style={{ height: STAGE_PANEL_HEIGHT, marginBottom: 10 }} />
    );
  }

  const files = view.files || PAIR;
  return (
    <div style={{
      height: STAGE_PANEL_HEIGHT, marginBottom: 10, padding: 6,
      background: 'var(--color-background-secondary,#f7f7f5)',
      borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)',
      boxSizing: 'border-box',
    }}>
      <ImageGrid folder={view.folder} drId={drId} files={files} labels={view.labels} />
    </div>
  );
}

function GradeSelector({ value, onChange }) {
  return (
    <div style={{
      display: 'flex', gap: 4, marginBottom: 14, padding: 4,
      background: 'var(--color-background-secondary,#f1efe8)', borderRadius: 8,
    }}>
      {DR_GRADES.map(g => {
        const active = g.id === value;
        return (
          <button
            key={g.id}
            onClick={() => onChange(g.id)}
            style={{
              flex: 1, padding: '6px 4px',
              border: 'none', borderRadius: 6,
              background: active ? C.teal : 'transparent',
              color: active ? '#fff' : 'var(--color-text-primary,#444)',
              cursor: 'pointer', lineHeight: 1.2,
            }}
            title={g.sub}
          >
            <div style={{ fontSize: 11, fontWeight: 700 }}>{g.label}</div>
            <div style={{ fontSize: 9, opacity: active ? 0.85 : 0.6, marginTop: 1 }}>{g.sub}</div>
          </button>
        );
      })}
    </div>
  );
}

function ViewSelector({ views, value, onChange }) {
  if (views.length <= 1) return null;
  return (
    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 8 }}>
      {views.map(v => {
        const active = v.id === value;
        return (
          <button
            key={v.id}
            onClick={() => onChange(v.id)}
            style={{
              padding: '4px 10px', fontSize: 10, fontWeight: active ? 700 : 500,
              border: `1px solid ${active ? C.teal : 'var(--color-border-secondary,#ccc)'}`,
              borderRadius: 5,
              background: active ? C.tealBg : 'transparent',
              color: active ? C.tealT : 'var(--color-text-secondary,#555)',
              cursor: 'pointer',
            }}
          >
            {v.label}
          </button>
        );
      })}
    </div>
  );
}

export default function ModelPipeline() {
  const [stg, setStg] = useState(0);
  const [drId, setDrId] = useState('dr04');
  const [viewId, setViewId] = useState('main');
  const { t } = useLang();

  const views = STAGE_VIEWS[stg] || [];
  const currentView = views.find(v => v.id === viewId) || views[0];

  // Reset sub-view when changing stages — the previous view id may not exist.
  useEffect(() => {
    const valid = views.some(v => v.id === viewId);
    if (!valid && views.length > 0) setViewId(views[0].id);
  }, [stg]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div>
      {/* Hero: complete pipeline grid */}
      <Sec title={t('pipeline.title')}>
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/25_pipeline_stages_real.png'}
          alt="Complete preprocessing pipeline stages"
          caption="Pipeline: Raw → Stage 0 (canonical flip) → Stage 1 (OD-fovea rotation) → Stage 2 (FOV crop + isotropic resize) → Stage 3 (FOV mask) → Stage 4 (adaptive flat-field) → Stage 5 (CLAHE) → Stage 6 (aug, train only) → Stage 7 (dataset-specific normalize + 4ch)."
          tooltip="tooltip.pipeline_grid"
        />
      </Sec>

      {/* Pipeline flowchart SVG */}
      <Sec title={t('pipeline.diagram')}>
        <DiagramViewer
          src={process.env.PUBLIC_URL + '/diagrams/04_preprocessing_pipeline_vertical.svg'}
          alt="8-stage preprocessing pipeline"
          caption="8-stage preprocessing pipeline flowchart. Novel components: canonical flip (S0), OD-fovea rotation (S1), isotropic resize (S2), FOV mask (S3), adaptive flat-field (S4), CLAHE (S5), integrated augmentation (S6), dataset-specific normalize + 4ch (S7)."
          tooltip="tooltip.pipeline_svg"
        />
      </Sec>

      {/* Stage-by-stage stepper */}
      <Sec title={t('pipeline.walkthrough')}>
        {/* DR grade selector */}
        <GradeSelector value={drId} onChange={setDrId} />

        {/* Navigation buttons — directly under DR selector for quick stepping */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
          <button
            onClick={() => setStg(Math.max(0, stg - 1))}
            disabled={stg === 0}
            style={{
              padding: '5px 14px', fontSize: 11,
              border: '1px solid var(--color-border-secondary,#ccc)',
              borderRadius: 5, background: 'transparent',
              cursor: stg === 0 ? 'default' : 'pointer', opacity: stg === 0 ? 0.3 : 1,
            }}
          >
            ← Previous
          </button>
          <span style={{ fontSize: 10, color: 'var(--color-text-secondary,#aaa)' }}>
            {stg + 1} / {PIPE.length}
          </span>
          <button
            onClick={() => setStg(Math.min(PIPE.length - 1, stg + 1))}
            disabled={stg === PIPE.length - 1}
            style={{
              padding: '5px 14px', fontSize: 11, border: 'none', borderRadius: 5,
              background: stg === PIPE.length - 1 ? 'transparent' : C.tealBg,
              color: C.tealT, fontWeight: 500,
              cursor: stg === PIPE.length - 1 ? 'default' : 'pointer',
              opacity: stg === PIPE.length - 1 ? 0.3 : 1,
            }}
          >
            Next →
          </button>
        </div>

        {/* Progress bar */}
        <div style={{ display: 'flex', gap: 3, marginBottom: 14 }}>
          {PIPE.map((s, i) => (
            <button key={i} onClick={() => setStg(i)} style={{
              flex: 1, height: 6, border: 'none', borderRadius: 3, cursor: 'pointer',
              background: i <= stg ? C.teal : 'var(--color-background-secondary,#e5e5e3)',
              opacity: i === stg ? 1 : 0.55,
            }} title={s.nm} />
          ))}
        </div>

        {/* Stage label */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
          <span style={{
            background: stg === 0 ? C.grayBg : C.tealBg,
            color: stg === 0 ? C.grayT : C.tealT,
            padding: '3px 10px', borderRadius: 5, fontSize: 11, fontWeight: 600,
          }}>
            {stg === 0 ? 'INPUT' : `Stage ${stg}/${PIPE.length - 1}`}
          </span>
          <span style={{ fontSize: 14, fontWeight: 600 }}>{PIPE[stg].nm}</span>
          <span style={{ marginLeft: 'auto', fontSize: 10, color: 'var(--color-text-secondary,#888)' }}>
            {DR_GRADES.find(g => g.id === drId)?.label} · both eyes
          </span>
        </div>

        {/* Sub-view selector — only shown when stage has multiple views */}
        <ViewSelector views={views} value={viewId} onChange={setViewId} />

        {/* Image grid (left + right eye side by side; 2×2 for min/max augmentation) */}
        <StagePanel stepIndex={stg} drId={drId} viewId={viewId} />

        {/* Description (stage-level) + sub-view note when present */}
        <div style={{ fontSize: 12, lineHeight: 1.65, marginBottom: 8 }}>
          {PIPE[stg].desc}
          {currentView?.note && (
            <div style={{ fontSize: 11, color: C.tealT, background: C.tealBg, padding: '6px 10px', borderRadius: 5, marginTop: 6 }}>
              {currentView.note}
            </div>
          )}
        </div>

        {/* Technical details */}
        <details style={{ fontSize: 11, color: 'var(--color-text-secondary,#666)' }}>
          <summary style={{ cursor: 'pointer', fontWeight: 500 }}>Technical details</summary>
          <div style={{
            padding: '6px 10px', marginTop: 4, borderRadius: 5,
            background: 'var(--color-background-secondary,#f7f7f5)',
            fontFamily: 'monospace', fontSize: 10, lineHeight: 1.5,
          }}>
            {PIPE[stg].detail}
          </div>
        </details>
      </Sec>

      {/* Bilateral pair section */}
      <Sec title={t('pipeline.bilateralPair')}>
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/26_bilateral_pair.png'}
          alt="Bilateral fundus pair — both eyes through the pipeline"
          caption="Bilateral fundus pair (left and right eye of the same patient) processed through the full pipeline. Canonical flip ensures both eyes share the same OD-on-right orientation; subsequent stages are applied identically and independently to each eye."
          tooltip="tooltip.bilateral"
        />
      </Sec>

      {/* Pipeline configurations table */}
      <Sec title={t('pipeline.configurations')}>
        <DataTable
          headers={['Configuration', 'Stages Active', 'Novel Components', 'Used In']}
          rows={[
            ['Baseline', 'Stages 2+7 only (3ch stretch-resize + ImageNet norm)', '0', 'Configs A, C (Exp 1 control)'],
            ['Full pipeline', 'All stages 0–7 (4ch: RGB + FOV mask)', '7', 'Configs B, D (Exp 1 treatment)'],
            ['CLAHE sweep', 'Stage 5 parameter grid (clip_factor × global_threshold)', '1', 'Exp 2 (IDRiD)'],
            ['Ablation (levels 0–6)', 'Progressive stage addition', 'N', 'Exp 2 (H-2) component contribution'],
          ]}
        />
        <Note>
          Pipeline has 7 novel contributions: canonical flip (S0), OD-fovea rotation (S1),
          isotropic resize + zero-padding (S2), FOV mask generation (S3), adaptive flat-field σ=0.07·D (S4),
          dual-constraint CLAHE (S5), integrated augmentation (S6). Stage 7 (dataset-specific normalize → 4ch)
          is standard. Baseline uses 3ch stretch-resize + ImageNet normalize only.
        </Note>
      </Sec>
    </div>
  );
}
