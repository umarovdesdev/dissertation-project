import { C, STAT_TESTS, TRAIN_TEST_GAP } from '../data';
import { Sec, DataTable, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ResultsStatistical() {
  const { t } = useLang();
  return (
    <div>
      <Sec title={t('results.statTests')}>
        <DataTable
          headers={['Test', 'ResNet-50 (B vs A)', 'EfficientNet-B3 (D vs C)']}
          rows={STAT_TESTS.map(d => [d.test, d.resnet, d.effnet])}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/21_statistical_tests.png'}
          caption="Statistical test results visualized. Both architectures show statistically significant preprocessing improvement: ResNet-50 (B−A, DeLong p=0.006, McNemar p=0.009) and EfficientNet-B3 (D−C, DeLong p=0.008, McNemar p=0.012). Bootstrap CIs exclude zero for both."
          figNum={21}
          tooltip="tooltip.fig21"
        />
        <Note>
          Both architectures are statistically significant at α=0.05 across all tests after correction.
          ResNet-50: DeLong p=0.006, McNemar p=0.009, Holm-corrected p_adj=0.012.
          EfficientNet-B3: DeLong p=0.008, McNemar p=0.012, Holm-corrected p_adj=0.024.
          The mixed-effects ANOVA shows a non-significant interaction (p=0.23), confirming both architectures
          benefit comparably from the pipeline.
        </Note>
      </Sec>

      <Sec title="Mixed-Effects ANOVA Interpretation">
        <div style={{ fontSize: 12, lineHeight: 1.7, color: 'var(--color-text-primary,#333)' }}>
          <p style={{ margin: '0 0 10px 0' }}>
            A mixed-effects ANOVA was fitted with preprocessing (2 levels), architecture (2 levels), and their
            interaction as fixed effects, with fold as a random effect. Results:
          </p>
          <div style={{ background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 7, padding: '10px 14px', fontFamily: 'monospace', fontSize: 11, lineHeight: 1.8 }}>
            <div>Main effect (preprocessing): p&lt;0.001 ***</div>
            <div>Main effect (architecture): p=0.018 *</div>
            <div style={{ fontWeight: 700, color: C.gray }}>Interaction (preprocessing × architecture): p=0.23 (n.s.)</div>
          </div>
          <p style={{ margin: '10px 0 0 0' }}>
            The non-significant interaction (p=0.23) confirms that the preprocessing benefit is consistent across
            architectures — both ResNet-50 and EfficientNet-B3 improve comparably from the pipeline. The highly
            significant main effect of preprocessing (p&lt;0.001) establishes that the pipeline drives classification
            improvement regardless of backbone architecture.
          </p>
        </div>
      </Sec>

      <Sec title="Training-Test Gap Analysis">
        <DataTable
          headers={['Config', 'Train F1', 'Test F1', 'Gap (pp)']}
          rows={TRAIN_TEST_GAP.map(d => [
            d.config, d.trainF1.toFixed(3), d.testF1.toFixed(3), `${d.gap.toFixed(1)}pp`,
          ])}
        />
        <Note>
          Training-test gaps of 7.0–7.6pp are consistent with the class imbalance and dataset difficulty.
          All configurations show similar gap magnitude, indicating no systematic overfitting difference
          between baseline and pipeline configurations. Patient-level CV prevents data leakage.
        </Note>
      </Sec>
    </div>
  );
}
