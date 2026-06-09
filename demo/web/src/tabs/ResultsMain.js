import { C, CONFIGS } from '../data';
import { Sec, DataTable, Hbar, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ResultsMain() {
  const { t } = useLang();
  const all4 = ['A', 'B', 'C', 'D'];

  return (
    <div>
      <Sec title={t('results.allConfigs')}>
        <DataTable
          headers={['Config', 'Preprocessing', 'CNN', 'W.F1 ± σ', 'ROC-AUC ± σ', 'κ ± σ', 'Acc']}
          rows={all4.map(k => {
            const v = CONFIGS[k];
            return [
              <span key={k} style={{ fontWeight: 700, color: k === 'D' ? C.teal : 'inherit' }}>{k}</span>,
              v.preprocessing, v.cnn,
              `${v.f1.toFixed(3)} ± ${v.f1s.toFixed(3)}`,
              `${v.auc.toFixed(3)} ± ${v.aucs.toFixed(3)}`,
              `${v.k.toFixed(3)} ± ${v.ks.toFixed(3)}`,
              v.acc.toFixed(3),
            ];
          })}
          highlightRow={(row, i) => i === 3}
        />
      </Sec>

      <Sec title="Weighted F1 — All 4 Configurations">
        <Hbar
          items={all4.map((k, i) => ({
            label: `${k}: ${CONFIGS[k].lbl}`,
            v: CONFIGS[k].f1,
            color: [C.gray, C.blue, C.gray, C.teal][i],
          }))}
          maxV={0.85}
        />
      </Sec>

      <Sec title="Summary Radar Chart">
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/11_summary_radar.png'}
          caption="Performance radar across 4 configurations (A–D) and all 6 hypotheses. Config D (Pipeline + EfficientNet-B3) is the best configuration."
          figNum={11}
          tooltip="tooltip.fig11"
        />
      </Sec>

      <Sec title="EH-3 Dominance Check">
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/12_eh3_dominance.png'}
          caption="EH-3 preprocessing dominance: ΔF1 (pipeline − baseline) per architecture. Both architectures exceed the 5pp threshold: EfficientNet-B3 (D−C = +5.3pp) and ResNet-50 (B−A = +5.2pp). H-1 confirmed for both."
          figNum={12}
          tooltip="tooltip.fig12"
        />
        <DataTable
          headers={['Criterion', 'ResNet-50 (B−A)', 'EfficientNet-B3 (D−C)', 'Threshold', 'Result']}
          rows={[
            ['ΔF1', `+${((CONFIGS.B.f1 - CONFIGS.A.f1) * 100).toFixed(1)}pp ✓`, `+${((CONFIGS.D.f1 - CONFIGS.C.f1) * 100).toFixed(1)}pp ✓`, '≥ 5pp', '✓ (both)'],
            ['ΔAUC', `+${((CONFIGS.B.auc - CONFIGS.A.auc) * 100).toFixed(1)}pp ✓`, `+${((CONFIGS.D.auc - CONFIGS.C.auc) * 100).toFixed(1)}pp ✓`, '≥ 2pp', '✓ (both)'],
            ['Δκ', `+${((CONFIGS.B.k - CONFIGS.A.k) * 100).toFixed(1)}pp ✓`, `+${((CONFIGS.D.k - CONFIGS.C.k) * 100).toFixed(1)}pp ✓`, '> 0', '✓ (both)'],
          ]}
        />
        <Note>
          Both architectures satisfy EH-3 dominance independently. The mixed-effects ANOVA shows a significant main
          effect of preprocessing (p&lt;0.001) with a non-significant interaction (p=0.23), confirming that the
          pipeline improves classification performance regardless of backbone architecture.
        </Note>
      </Sec>
    </div>
  );
}
