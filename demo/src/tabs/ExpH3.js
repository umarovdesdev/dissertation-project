import { C, APTOS, CONFIGS } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';

export default function ExpH3() {
  const configs = ['A', 'B', 'C', 'D'];

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-4: APTOS 2019 Cross-Dataset Transferability
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 3 — Zero-shot transfer of EyePACS-trained models to APTOS 2019 (Indian population, mixed cameras)
        </div>
      </div>

      <Sec title="Generalization Ratio G — APTOS 2019">
        <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
          <Card
            label="G (Config A — Baseline ResNet-50)"
            value={APTOS.A.G.toFixed(2)}
            delta={APTOS.A.G >= APTOS.threshold ? `≥ ${APTOS.threshold} ✓` : `< ${APTOS.threshold} ✗`}
            color={APTOS.A.G >= APTOS.threshold ? 'green' : 'red'}
            sub={`F1: ${APTOS.A.f1.toFixed(3)}`}
          />
          <Card
            label="G (Config B — Pipeline ResNet-50)"
            value={APTOS.B.G.toFixed(2)}
            delta={APTOS.B.G >= APTOS.threshold ? `≥ ${APTOS.threshold} ✓` : `< ${APTOS.threshold} ✗`}
            color={APTOS.B.G >= APTOS.threshold ? 'green' : 'red'}
            sub={`F1: ${APTOS.B.f1.toFixed(3)}`}
          />
          <Card
            label="G (Config C — Baseline EffNet-B3)"
            value={APTOS.C.G.toFixed(2)}
            delta={APTOS.C.G >= APTOS.threshold ? `≥ ${APTOS.threshold} ✓` : `< ${APTOS.threshold} ✗`}
            color={APTOS.C.G >= APTOS.threshold ? 'green' : 'red'}
            sub={`F1: ${APTOS.C.f1.toFixed(3)}`}
          />
          <Card
            label="G (Config D — Pipeline EffNet-B3)"
            value={APTOS.D.G.toFixed(2)}
            delta={APTOS.D.G >= APTOS.threshold ? `≥ ${APTOS.threshold} ✓` : `< ${APTOS.threshold} ✗`}
            color={APTOS.D.G >= APTOS.threshold ? 'green' : 'red'}
            sub={`F1: ${APTOS.D.f1.toFixed(3)}`}
          />
        </div>
        <Note>
          H-4 criterion: G = F1<sub>APTOS</sub> / F1<sub>EyePACS</sub> ≥ 0.85.
          Both pipeline configurations (B, D) exceed the threshold (G=0.86, 0.89);
          both baselines fall below (G=0.81, 0.82). Preprocessing is the deciding factor for cross-dataset transfer.
          DeLong test on Config D AUC: p=0.015 (significant). Bootstrap 95% CI for ΔG: [+0.04, +0.11].
        </Note>
      </Sec>

      <Sec title="EyePACS (in-domain) vs APTOS 2019 (transfer) — F1">
        <Paired
          items={configs.map(k => ({
            label: `Config ${k}`,
            v1: CONFIGS[k].f1,
            v2: APTOS[k].f1,
          }))}
          c1={C.blue}
          c2={C.coral}
          l1="EyePACS (in-domain)"
          l2="APTOS 2019 (zero-shot)"
        />
        <DataTable
          headers={['Config', 'EyePACS F1', 'APTOS F1', 'APTOS F1 std', 'G', 'H-4']}
          rows={configs.map(k => [
            `${k} — ${CONFIGS[k].lbl}`,
            CONFIGS[k].f1.toFixed(3),
            APTOS[k].f1.toFixed(3),
            `±${APTOS[k].f1s.toFixed(3)}`,
            APTOS[k].G.toFixed(3),
            APTOS[k].G >= APTOS.threshold ? '✓' : '✗',
          ])}
          highlightRow={(_, i) => configs[i] === 'D'}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/exp3/29_exp3_aptos_transfer.png'}
          caption="APTOS 2019 zero-shot transfer. Configs B and D (pipeline) exceed the H-4 generalization threshold G ≥ 0.85; baselines fall short despite comparable EyePACS F1."
          figNum={29}
        />
      </Sec>

      <Sec title="Best-Config Detail (D) — Full APTOS Metrics">
        <DataTable
          headers={['Metric', 'Value', 'Std']}
          rows={[
            ['F1 (weighted)', APTOS.D.f1.toFixed(3), `±${APTOS.D.f1s.toFixed(3)}`],
            ['ROC-AUC', APTOS.D.auc.toFixed(3), `±${APTOS.D.aucs.toFixed(3)}`],
            ["Cohen's κ", APTOS.D.k.toFixed(3), `±${APTOS.D.ks.toFixed(3)}`],
            ['Accuracy', APTOS.D.acc.toFixed(3), '—'],
            ['G (transfer ratio)', APTOS.D.G.toFixed(3), '—'],
          ]}
        />
        <Note>
          Training set: EyePACS (~35,126 images, Canon CR-1). Evaluation set: APTOS 2019 (3,662 images,
          mixed cameras, Indian population). Protocol: zero-shot — no retraining or fine-tuning on APTOS.
          5-fold patient-level stratified CV on EyePACS; best checkpoint per fold evaluated on APTOS.
        </Note>
      </Sec>
    </div>
  );
}
