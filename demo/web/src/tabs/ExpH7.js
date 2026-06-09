import { C, SMALL_DATA } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';

export default function ExpH7() {
  const baseline = SMALL_DATA[0];
  const pipeline = SMALL_DATA[1];
  const idridDelta = ((pipeline.idrid_f1 - baseline.idrid_f1) * 100).toFixed(1);
  const clinDelta = ((pipeline.clinical_f1 - baseline.clinical_f1) * 100).toFixed(1);
  const aucDelta = ((pipeline.clinical_auc - baseline.clinical_auc) * 100).toFixed(1);

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          Experiment 7 — Small-Data Clinical Training
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          IDRiD (516 images) → Clinical test set (60 images, Almaty medical centre). 5-fold CV on IDRiD; clinical held out.
        </div>
      </div>

      <Sec title="Headline — Pipeline Lift in Low-Data Regime">
        <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
          <Card
            label="IDRiD CV F1 (pipeline)"
            value={pipeline.idrid_f1.toFixed(3)}
            delta={`+${idridDelta}pp vs baseline`}
            color="teal"
            sub={`Baseline ${baseline.idrid_f1.toFixed(3)}`}
          />
          <Card
            label="Clinical Test F1 (pipeline)"
            value={pipeline.clinical_f1.toFixed(3)}
            delta={`+${clinDelta}pp vs baseline`}
            color="blue"
            sub={`Baseline ${baseline.clinical_f1.toFixed(3)}`}
          />
          <Card
            label="Clinical Test AUC (pipeline)"
            value={pipeline.clinical_auc.toFixed(3)}
            delta={`+${aucDelta}pp vs baseline`}
            color="purple"
            sub={`Baseline ${baseline.clinical_auc.toFixed(3)}`}
          />
        </div>
        <Note>
          Pipeline (4ch) yields larger gains in the small-data regime (Δ +6.7pp on IDRiD CV, +9.3pp on Clinical test)
          than in the full-data regime (Exp 1: Δ +5.3pp on EyePACS). This indicates preprocessing acts as a strong
          inductive prior when training data is scarce — feature normalization compensates for limited statistical
          coverage.
        </Note>
      </Sec>

      <Sec title="IDRiD CV vs Clinical Test — F1">
        <Paired
          items={[
            { label: 'IDRiD (5-fold CV)', a: baseline.idrid_f1, b: pipeline.idrid_f1 },
            { label: 'Clinical (held-out test)', a: baseline.clinical_f1, b: pipeline.clinical_f1 },
          ]}
          c1={C.gray}
          c2={C.teal}
          l1="Baseline (3ch)"
          l2="Pipeline (4ch)"
        />
        <DataTable
          headers={['Condition', 'IDRiD F1', 'IDRiD std', 'Clinical F1', 'Clinical AUC']}
          rows={SMALL_DATA.map(d => [
            d.condition,
            d.idrid_f1.toFixed(3),
            `±${d.idrid_std.toFixed(3)}`,
            d.clinical_f1.toFixed(3),
            d.clinical_auc.toFixed(3),
          ])}
          highlightRow={(_, i) => i === 1}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/exp7/30_exp7_small_data.png'}
          caption="Small-data training: IDRiD 5-fold CV → Clinical test set. Pipeline shows largest absolute gains in the small-data regime, supporting the hypothesis that preprocessing functions as an inductive prior."
          figNum={30}
        />
      </Sec>

      <Sec title="Protocol">
        <DataTable
          headers={['Property', 'Value']}
          rows={[
            ['Training dataset', 'IDRiD (516 images, Kowa VX-10α)'],
            ['Evaluation dataset', 'Clinical (60 images, Almaty medical centre — Topcon-class camera)'],
            ['Cross-validation', '5-fold patient-level stratified on IDRiD'],
            ['Test protocol', 'Clinical held out — never seen during training or validation'],
            ['Bootstrap resamples (CI)', '1,000'],
          ]}
        />
        <Note>
          Experiment 7 is the only experiment in the dissertation that trains on a non-EyePACS dataset.
          It tests whether the pipeline retains its advantage when the training pool is two orders of magnitude
          smaller than EyePACS (516 vs ~35,126 images).
        </Note>
      </Sec>
    </div>
  );
}
