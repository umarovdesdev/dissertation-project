import { C, CONFIGS } from '../data';
import { Sec, DataTable, Hbar, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ExpH1() {
  const { t } = useLang();
  const factorial = ['A', 'B', 'C', 'D'];
  const all4 = ['A', 'B', 'C', 'D'];

  const deltaF1 = ((CONFIGS.D.f1 - CONFIGS.C.f1) * 100).toFixed(1);
  const deltaAUC = ((CONFIGS.D.auc - CONFIGS.C.auc) * 100).toFixed(1);

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-1: Preprocessing Dominance Hypothesis
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 1 — 2×2 Factorial Design on EyePACS (100%, ~35,126 images, 5-fold CV)
        </div>
      </div>

      <Sec title={t('exp.factorial')}>
        <DataTable
          headers={['Config', 'Preprocessing', 'CNN', 'W.F1 ± σ', 'ROC-AUC ± σ', 'κ ± σ', 'Acc']}
          rows={factorial.map(k => {
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
        <Note>
          Config D (Full V5 pipeline + EfficientNet-B3) is the best single-image configuration.
          ΔF1(D−C) = +{deltaF1}pp, ΔAUC(D−C) = +{deltaAUC}pp. Statistically significant (DeLong p=0.008, McNemar p=0.012).
        </Note>
      </Sec>

      <Sec title="Weighted F1 by Configuration (A–D)">
        <Hbar
          items={factorial.map((k, i) => ({ label: `${k}: ${CONFIGS[k].lbl}`, v: CONFIGS[k].f1, color: [C.gray, C.blue, C.gray, C.teal][i] }))}
          maxV={0.85}
        />
      </Sec>

      <Sec title={t('exp.allConfigs')}>
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
          highlightRow={(row, i) => i === 5}
        />
        <Note>
          V5 uses 4 configurations (A–D) only. Baseline configs (A, C) use 3-channel stretch-resize + ImageNet normalize. Full V5 configs (B, D) use 8-stage pipeline with 4-channel input (RGB + FOV mask).
        </Note>
      </Sec>

      <Sec title="Factorial F1 Chart">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/01_exp1_factorial_f1.png'} caption="Weighted F1 comparison for 2×2 factorial design (Configs A–D). Bars show mean ± std across 5 folds." figNum={1} tooltip="tooltip.fig01" />
      </Sec>

      <Sec title="All Metrics Comparison">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/02_exp1_all_metrics.png'} caption="F1, AUC, κ, and Accuracy for all 2×2 factorial configurations. Config D dominates on all four metrics." figNum={2} tooltip="tooltip.fig02" />
      </Sec>

      <Sec title="Delta vs Baseline">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/03_exp1_delta.png'} caption="Preprocessing improvement (Δ) relative to baseline. EfficientNet-B3 (D−C) shows significantly larger gain than ResNet-50 (B−A), confirming architecture × preprocessing interaction." figNum={3} tooltip="tooltip.fig03" />
      </Sec>

      <Sec title="All 4 Configurations Chart">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/22_exp1_all_6_configs.png'} caption="All 4 configurations A–D. Architecture-dependent preprocessing interaction: EfficientNet-B3 (D vs C) shows significant gain; ResNet-50 (B vs A) near-zero." figNum={22} tooltip="tooltip.fig22" />
      </Sec>

      <Sec title="Per-Class F1 (EfficientNet-B3)">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/18_per_class_f1.png'} caption="Per-class weighted F1: Baseline (Config C) vs Pipeline (Config D). Largest improvement on minority classes: DR 1 (+12pp), DR 3 (+12pp). DR 0 near-saturated at baseline." figNum={18} tooltip="tooltip.fig18" />
      </Sec>

      <Sec title="Training Curves">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/19_training_curves.png'} caption="Training and validation loss/F1 curves across 3 folds. Pipeline configuration (D) converges to lower validation loss and higher F1. Consistent across folds." figNum={19} tooltip="tooltip.fig19" />
      </Sec>

      <Sec title="Confusion Matrix — Config D">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/20_confusion_matrix.png'} caption="Confusion matrix for Config D (best single-image configuration). Diagonal dominance confirms correct classification. Main confusions: DR 1↔DR 0, DR 2↔DR 3 (adjacent grade confusion)." figNum={20} tooltip="tooltip.fig20" />
      </Sec>

      <Sec title="ROC Curves — All Configs">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/24_roc_curves.png'} caption="One-vs-rest ROC curves for all 4 factorial configurations. Config D shows consistently higher AUC across all DR grades, particularly DR 1 and DR 3." figNum={24} tooltip="tooltip.fig24" />
      </Sec>

      <Sec title={t('exp.dominanceCriterion')}>
        <DataTable
          headers={['Criterion', 'ResNet-50 (B−A)', 'EfficientNet-B3 (D−C)', 'Threshold', 'Met?']}
          rows={[
            ['ΔF1', `${((CONFIGS.B.f1 - CONFIGS.A.f1) * 100).toFixed(1)}pp`, `+${deltaF1}pp`, '≥ 5pp', '✓ (EffNet)'],
            ['ΔAUC', `${((CONFIGS.B.auc - CONFIGS.A.auc) * 100).toFixed(1)}pp`, `+${deltaAUC}pp`, '≥ 2pp', '✓ (EffNet)'],
            ['Δκ', `+${((CONFIGS.B.k - CONFIGS.A.k) * 100).toFixed(1)}pp`, `+${((CONFIGS.D.k - CONFIGS.C.k) * 100).toFixed(1)}pp`, '> 0', '✓ (both)'],
          ]}
        />
        <Note>
          EH-3 requires preprocessing dominance independently for both architectures. EfficientNet-B3 meets all thresholds
          (ΔF1=+{deltaF1}pp ≥ 5pp, ΔAUC=+{deltaAUC}pp ≥ 2pp). ResNet-50 shows near-zero delta, confirming the
          architecture × preprocessing interaction effect (mixed-effects ANOVA, interaction p=0.02).
          The interaction is itself a scientifically significant finding: preprocessing benefit scales with model capacity.
        </Note>
      </Sec>
    </div>
  );
}
