import { useState } from 'react';
import { C, PIPE } from '../data';
import { Sec, Note, DataTable, DiagramViewer, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

// Per-step image mapping for the stepper
// null = no image for this step (Stage 5: train-only augmentation)
// false = image file not yet in public/fundus/ (Raw input)
const STAGE_IMAGES = [
  false,                                    // 0: Raw input — place 43199_right.jpeg in public/fundus/
  '/pipeline/method_canonical_flip.png',    // 1: Stage 0a
  '/pipeline/od_fovea_search_region.png',   // 2: Stage 0b
  '/pipeline/stage_1_cropped.png',          // 3: Stage 1
  '/pipeline/stage_2_flatfield.png',        // 4: Stage 2
  '/pipeline/stage_3_clahe.png',            // 5: Stage 3
  '/pipeline/stage_4_normalized.png',       // 6: Stage 4
  null,                                     // 7: Stage 5 — train only, shown as note
];

const imgStyle = {
  width: '100%', borderRadius: 8,
  border: '1px solid var(--color-border-tertiary,#eee)',
  display: 'block',
};

function StageImage({ stepIndex }) {
  const src = STAGE_IMAGES[stepIndex];

  if (src === null) {
    // Stage 5: augmentation is train-only — show informational note
    return (
      <div style={{
        padding: '20px', textAlign: 'center',
        background: C.purpleBg, borderRadius: 8, marginBottom: 10,
        border: `1px solid ${C.purple}30`,
      }}>
        <div style={{ fontSize: 14, color: C.purpleT, fontWeight: 600, marginBottom: 6 }}>
          Train only — not applied at inference
        </div>
        <div style={{ fontSize: 11, color: C.purpleT, lineHeight: 1.6 }}>
          Stage 5 augmentation is applied stochastically during training.<br />
          At inference, the image passes through Stages 0a–4 only.
        </div>
      </div>
    );
  }

  if (src === false) {
    // Fundus JPEG not yet copied to public/fundus/
    return (
      <div style={{
        padding: '20px', textAlign: 'center',
        background: C.amberBg, borderRadius: 8, marginBottom: 10,
        border: `1px solid ${C.amber}40`,
      }}>
        <div style={{ fontSize: 12, color: C.amberT, fontWeight: 600, marginBottom: 4 }}>
          Patient 43199, EyePACS, DR Grade 4 (Proliferative DR), Canon CR-1
        </div>
        <div style={{ fontSize: 11, color: C.amberT }}>
          Copy <code style={{ background: `${C.amber}20`, padding: '1px 4px', borderRadius: 3 }}>43199_right.jpeg</code> into{' '}
          <code style={{ background: `${C.amber}20`, padding: '1px 4px', borderRadius: 3 }}>public/fundus/</code> to display.
        </div>
      </div>
    );
  }

  return (
    <div style={{ marginBottom: 10 }}>
      <img src={src} alt={`Pipeline step ${stepIndex}`} style={imgStyle} />
    </div>
  );
}

export default function ModelPipeline() {
  const [stg, setStg] = useState(0);
  const { t } = useLang();

  return (
    <div>
      {/* Hero: complete pipeline grid */}
      <Sec title={t('pipeline.title')}>
        <ImageWithTooltip
          src="/pipeline/pipeline_stages_grid.png"
          alt="Complete V4 preprocessing pipeline stages"
          caption="2×3 grid: Raw fundus → Stage 0a (canonical flip) → Stage 1 (FOV crop, 512×512) → Stage 2 (flat-field) → Stage 3 (CLAHE) → Stage 4 (normalised). Patient 43199, EyePACS, Canon CR-1."
          tooltip="tooltip.pipeline_grid"
        />
      </Sec>

      {/* Pipeline flowchart SVG */}
      <Sec title={t('pipeline.diagram')}>
        <DiagramViewer
          src={process.env.PUBLIC_URL + '/diagrams/v4_preprocessing_pipeline_diagram.svg'}
          alt="V4 6-stage preprocessing pipeline"
          caption="V4 6-stage preprocessing pipeline flowchart. Five scientifically novel components (Stages 0a, 0b, 2, 3, 5) plus standard FOV crop/resize and ImageNet normalization."
          tooltip="tooltip.pipeline_svg"
        />
      </Sec>

      {/* Stage-by-stage stepper */}
      <Sec title={t('pipeline.walkthrough')}>
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
        </div>

        {/* Real stage image */}
        <StageImage stepIndex={stg} />

        {/* Description */}
        <div style={{ fontSize: 12, lineHeight: 1.65, marginBottom: 8 }}>
          {PIPE[stg].desc}
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

        {/* Navigation buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 14 }}>
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
          <span style={{ fontSize: 10, color: 'var(--color-text-secondary,#aaa)', alignSelf: 'center' }}>
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
      </Sec>

      {/* Bilateral pair section */}
      <Sec title={t('pipeline.bilateralPair')}>
        <ImageWithTooltip
          src="/pipeline/bilateral_pair.png"
          alt="Bilateral fundus pair — both eyes through the pipeline"
          caption="Patient 43199, DR Grade 4 (Proliferative DR), Canon CR-1. Top row: raw left-eye (OD on left) and raw right-eye (OD on right). Middle row: after canonical flip — both now OD on right. Bottom row: full V4 pipeline output."
          tooltip="tooltip.bilateral"
        />
      </Sec>

      {/* Before / after comparison */}
      <Sec title={t('pipeline.beforeAfter')}>
        <ImageWithTooltip
          src="/pipeline/before_after_pipeline.png"
          alt="Baseline vs full V4 pipeline comparison"
          caption="Left: baseline (crop + resize + ImageNet normalisation only). Right: full V4 pipeline (all 5 novel stages applied). The pipeline visibly improves vessel contrast and equalises illumination across the retinal field."
          tooltip="tooltip.before_after"
        />
      </Sec>

      {/* Pipeline configurations table */}
      <Sec title={t('pipeline.configurations')}>
        <DataTable
          headers={['Configuration', 'Stages Active', 'Novel Components', 'Used In']}
          rows={[
            ['Baseline', 'Stage 1 + Stage 4', '0', 'Configs A, C (Exp 1 control)'],
            ['Full V4 pipeline', 'All stages (0a, 0b, 1, 2, 3, 4, 5)', '5', 'Configs B, D (Exp 1 treatment)'],
            ['V4 + binocular', 'All stages + bilateral fusion', '5 + fusion', 'Configs E, F (Exp 1 extension)'],
            ['CLAHE sweep', 'Stage 3 parameter grid', '1', 'Exp 2 (IDRiD subset)'],
          ]}
        />
        <Note>
          "5-component pipeline" refers to the five scientifically novel contributions: canonical flip (0a),
          OD-fovea rotation (0b), flat-field correction (2), dual-constraint CLAHE (3), stochastic
          augmentation (5). Stages 1 and 4 are standard techniques present in both baseline and pipeline
          configurations.
        </Note>
      </Sec>
    </div>
  );
}
