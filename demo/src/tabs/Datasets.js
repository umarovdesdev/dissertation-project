import { useState } from 'react';
import { C, DATASETS, CAMERA_GROUPS, DATASET_TIERS, RESOLUTION_ANALYSIS, CAMERA_DISTRIBUTION } from '../data';
import { Sec, Note } from '../components';
import { useLang } from '../i18n';

// Tier colour helpers
function tierBg(color) { return C[color + 'Bg'] || C.grayBg; }
function tierT(color)  { return C[color + 'T']  || C.grayT;  }
function tierFg(color) { return C[color]         || C.gray;   }

// ── Section A: Tiered Architecture Overview ───────────────────────────────────
function TierOverview() {
  const { t } = useLang();
  const byTier = (tierName) => DATASETS.filter(d => d.tier === tierName);

  return (
    <Sec title={t('datasets.title')}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {DATASET_TIERS.map(tier => {
          const ds = byTier(tier.name);
          const isDropped = tier.name === 'Dropped';
          return (
            <div key={tier.name} style={{
              border: `1.5px solid ${tierFg(tier.color)}`,
              borderRadius: 8,
              overflow: 'hidden',
              opacity: isDropped ? 0.55 : 1,
            }}>
              {/* Tier header */}
              <div style={{
                background: tierBg(tier.color),
                padding: '5px 12px',
                display: 'flex', alignItems: 'center', gap: 10,
              }}>
                <span style={{ fontSize: 10, fontWeight: 700, color: tierT(tier.color), textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  {tier.name}{isDropped ? ' ✕' : ''}
                </span>
                <span style={{ fontSize: 10, color: tierT(tier.color), opacity: 0.7 }}>{tier.description}</span>
              </div>
              {/* Dataset cards inside tier */}
              <div style={{ display: 'flex', gap: 0, flexWrap: 'wrap', background: 'var(--color-background-primary,#fff)' }}>
                {ds.map((d, i) => (
                  <div key={d.name} style={{
                    flex: 1, minWidth: 140,
                    padding: '8px 12px',
                    borderLeft: i > 0 ? `1px solid ${tierFg(tier.color)}30` : 'none',
                  }}>
                    <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-text-primary,#333)' }}>{d.name}</div>
                    <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', marginTop: 2 }}>{d.size}</div>
                    <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 1 }}>{d.camera}</div>
                    {d.experiments && d.experiments.length > 0 && (
                      <div style={{ fontSize: 9, color: tierFg(tier.color), marginTop: 3, fontWeight: 500 }}>
                        {d.experiments.join(' · ')}
                      </div>
                    )}
                    {d.status === 'dropped' && (
                      <div style={{ fontSize: 9, color: C.gray, marginTop: 3, fontStyle: 'italic' }}>
                        {d.droppedReason}
                      </div>
                    )}
                    {d.name === 'IDRiD' && (
                      <div style={{ fontSize: 9, color: C.teal, marginTop: 3 }}>81 images with pixel-level lesion masks</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
      <Note>
        8 active datasets across 6 tiers. APTOS 2019 is the primary transfer target for Experiment 3 (H-4); Clinical KZ is the regional validation set for Experiment 7. Total labeled images across active datasets: ~63,589.
      </Note>
    </Sec>
  );
}

// ── Section B: Summary Table ──────────────────────────────────────────────────
function SummaryTable() {
  const { t } = useLang();
  const rows = DATASETS.map(d => ({
    name: d.name,
    status: d.status,
    tierColor: d.tierColor,
    size: d.size,
    camera: d.camera,
    taxonomy: d.taxonomy,
    mapping: d.taxonomyMapping ? 'Required' : 'None',
    experiments: d.experiments.length > 0 ? d.experiments.join(', ') : '—',
    source: d.source,
  }));

  return (
    <Sec title={t('datasets.summary')}>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)', background: 'var(--color-background-secondary,#f7f7f5)' }}>
              {['Dataset', 'Size', 'Camera', 'Taxonomy', 'Mapping', 'Experiments', 'Source'].map(h => (
                <th key={h} style={{ padding: '6px 8px', textAlign: 'left', fontWeight: 600, whiteSpace: 'nowrap' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={r.name} style={{
                borderBottom: '1px solid var(--color-border-tertiary,#eee)',
                opacity: r.status === 'dropped' ? 0.5 : 1,
                background: i % 2 === 0 ? 'transparent' : 'var(--color-background-secondary,#fafafa)',
              }}>
                <td style={{ padding: '5px 8px', fontWeight: 500, whiteSpace: 'nowrap' }}>
                  <span style={{
                    display: 'inline-block', width: 7, height: 7, borderRadius: '50%',
                    background: tierFg(r.tierColor), marginRight: 5, verticalAlign: 'middle',
                  }} />
                  {r.name}
                  {r.status === 'dropped' && <span style={{ fontSize: 9, color: C.gray, marginLeft: 4 }}>(dropped)</span>}
                </td>
                <td style={{ padding: '5px 8px', whiteSpace: 'nowrap' }}>{r.size}</td>
                <td style={{ padding: '5px 8px', whiteSpace: 'nowrap' }}>{r.camera}</td>
                <td style={{ padding: '5px 8px', fontSize: 10 }}>{r.taxonomy}</td>
                <td style={{ padding: '5px 8px', color: r.mapping === 'Required' ? C.coral : C.gray, fontWeight: r.mapping === 'Required' ? 600 : 400 }}>{r.mapping}</td>
                <td style={{ padding: '5px 8px', fontSize: 10 }}>{r.experiments}</td>
                <td style={{ padding: '5px 8px', fontSize: 10, color: 'var(--color-text-secondary,#888)' }}>{r.source}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Sec>
  );
}

// ── Section C: Camera Coverage Matrix ────────────────────────────────────────
function CameraMatrix() {
  const { t } = useLang();
  const cameras = Object.keys(CAMERA_GROUPS);
  const cols = [
    { label: 'Training', datasets: ['EyePACS'] },
    { label: 'Clinical / Transfer', datasets: ['IDRiD', 'Messidor-2'] },
    { label: 'Domain Shift', datasets: ['DDR', 'ODIR-5K', 'RFMiD'] },
  ];

  return (
    <Sec title={t('datasets.cameraMatrix')}
      note="The 4-manufacturer coverage (Canon, Topcon, Kowa, Zeiss) across 6 active datasets ensures Experiment 6 tests device shift across the maximum available range of imaging hardware.">
      <div style={{ overflowX: 'auto' }}>
        <table style={{ borderCollapse: 'collapse', fontSize: 11, width: '100%' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)' }}>
              <th style={{ padding: '6px 10px', textAlign: 'left', fontWeight: 600, minWidth: 70 }}>Camera</th>
              {cols.map(c => (
                <th key={c.label} style={{ padding: '6px 10px', textAlign: 'left', fontWeight: 600 }}>{c.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {cameras.map((cam, ri) => (
              <tr key={cam} style={{ borderBottom: '1px solid var(--color-border-tertiary,#eee)', background: ri % 2 === 0 ? 'transparent' : 'var(--color-background-secondary,#fafafa)' }}>
                <td style={{ padding: '6px 10px', fontWeight: 600 }}>{cam}</td>
                {cols.map(col => {
                  const hits = CAMERA_GROUPS[cam].filter(ds => col.datasets.includes(ds));
                  return (
                    <td key={col.label} style={{ padding: '6px 10px' }}>
                      {hits.length > 0
                        ? hits.map(ds => {
                            const d = DATASETS.find(x => x.name === ds);
                            return (
                              <span key={ds} style={{
                                display: 'inline-block', marginRight: 4, marginBottom: 2,
                                padding: '1px 6px', borderRadius: 4, fontSize: 10, fontWeight: 500,
                                background: tierBg(d.tierColor), color: tierT(d.tierColor),
                              }}>{ds}</span>
                            );
                          })
                        : <span style={{ color: 'var(--color-text-secondary,#ccc)', fontSize: 10 }}>—</span>}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Sec>
  );
}

// ── Section D: EyePACS Class Distribution ────────────────────────────────────
function ClassDistribution() {
  const { t } = useLang();
  const eyepacs = DATASETS.find(d => d.name === 'EyePACS');
  const dist = eyepacs.classDistribution;
  const grades = Object.keys(dist);
  const maxPct = Math.max(...grades.map(g => dist[g].pct));
  const colors = [C.blue, C.teal, C.amber, C.coral, C.purple];

  return (
    <Sec title={t('datasets.classDistribution')}
      note="Severe class imbalance (73.5% DR 0) reflects real-world population screening. Weighted cross-entropy loss is used during training to address imbalance. DR 1 (6.9%) and DR 3 (2.5%) are the most challenging classes — this directly explains their lower per-class F1 scores.">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 7 }}>
        {grades.map((grade, i) => {
          const { count, pct } = dist[grade];
          return (
            <div key={grade} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ fontSize: 11, fontWeight: 600, minWidth: 34, color: 'var(--color-text-primary,#333)' }}>{grade}</div>
              <div style={{ flex: 1, height: 22, background: 'var(--color-background-secondary,#eeede9)', borderRadius: 4, position: 'relative', overflow: 'hidden' }}>
                <div style={{
                  width: `${(pct / maxPct) * 100}%`, height: '100%',
                  background: colors[i], borderRadius: 4, opacity: 0.75,
                  transition: 'width 0.3s ease',
                }} />
                <span style={{ position: 'absolute', left: 8, top: '50%', transform: 'translateY(-50%)', fontSize: 10, fontWeight: 600, color: pct > 30 ? '#fff' : 'var(--color-text-primary,#333)' }}>
                  {pct}%
                </span>
              </div>
              <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', minWidth: 80, textAlign: 'right' }}>
                {count.toLocaleString()} images
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 10 }}>
        Total: ~35,126 labeled images. Exp 1 uses 100% (full dataset, ~35,126 images) with 5-fold patient-level stratified CV.
      </div>
    </Sec>
  );
}

// ── Section E: Individual Dataset Detail Cards ────────────────────────────────
function DatasetCard({ dataset: d }) {
  const [open, setOpen] = useState(false);
  const isDropped = d.status === 'dropped';

  return (
    <div style={{
      border: `1px solid ${tierFg(d.tierColor)}50`,
      borderLeft: `4px solid ${tierFg(d.tierColor)}`,
      borderRadius: 8, marginBottom: 10,
      opacity: isDropped ? 0.65 : 1,
      background: 'var(--color-background-primary,#fff)',
    }}>
      {/* Card header — always visible */}
      <div
        onClick={() => setOpen(o => !o)}
        style={{
          padding: '10px 14px', cursor: 'pointer',
          display: 'flex', alignItems: 'center', gap: 10,
        }}
      >
        <span style={{
          padding: '2px 8px', borderRadius: 5, fontSize: 10, fontWeight: 600,
          background: tierBg(d.tierColor), color: tierT(d.tierColor), whiteSpace: 'nowrap',
        }}>
          {d.tier}
        </span>
        <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-text-primary,#333)', flex: 1 }}>
          {d.name}
          {isDropped && <span style={{ fontSize: 10, color: C.gray, fontWeight: 400, marginLeft: 8 }}>Not active in current design</span>}
        </span>
        <div style={{ display: 'flex', gap: 12, fontSize: 10, color: 'var(--color-text-secondary,#888)' }}>
          <span>{d.size}</span>
          <span>{d.camera}</span>
        </div>
        <span style={{ fontSize: 11, color: 'var(--color-text-secondary,#aaa)', marginLeft: 4 }}>
          {open ? '▲' : '▼'}
        </span>
      </div>

      {/* Expanded content */}
      {open && (
        <div style={{ padding: '0 14px 14px 14px', borderTop: `1px solid ${tierFg(d.tierColor)}20` }}>
          {/* Quick specs row */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, padding: '10px 0 8px 0' }}>
            {[
              ['Camera', d.camera],
              ['Type', d.cameraType],
              ['FOV', d.fov],
              ['Resolution', d.resolution],
              ['Format', d.format],
              ['Population', d.population],
              ['Availability', d.availability],
            ].map(([label, val]) => (
              <div key={label} style={{ background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 5, padding: '3px 8px' }}>
                <span style={{ fontSize: 9, color: 'var(--color-text-secondary,#999)', marginRight: 4 }}>{label}:</span>
                <span style={{ fontSize: 10, fontWeight: 500 }}>{val}</span>
              </div>
            ))}
          </div>

          {/* Role */}
          <div style={{ marginBottom: 10 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--color-text-secondary,#666)', marginBottom: 3, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Role in dissertation</div>
            <div style={{ fontSize: 11, lineHeight: 1.6 }}>{d.role}</div>
          </div>

          {/* Experiments */}
          {d.experiments.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--color-text-secondary,#666)', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Experiments</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                {d.experiments.map(e => (
                  <span key={e} style={{ padding: '2px 8px', background: tierBg(d.tierColor), color: tierT(d.tierColor), borderRadius: 4, fontSize: 10, fontWeight: 500 }}>{e}</span>
                ))}
              </div>
            </div>
          )}

          {/* Why chosen */}
          {d.whyChosen && d.whyChosen.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--color-text-secondary,#666)', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Selection rationale</div>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: 11, lineHeight: 1.65 }}>
                {d.whyChosen.map((r, i) => <li key={i} style={{ marginBottom: 2 }}>{r}</li>)}
              </ul>
            </div>
          )}

          {/* Taxonomy mapping */}
          {d.taxonomyMapping && (
            <div style={{ marginBottom: 10, padding: '8px 10px', background: C.coralBg, borderRadius: 6 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.coralT, marginBottom: 3, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Taxonomy mapping required</div>
              <div style={{ fontSize: 11, color: C.coralT, lineHeight: 1.6 }}>{d.taxonomyMapping}</div>
            </div>
          )}

          {/* IDRiD lesion masks */}
          {d.lesionMasks && (
            <div style={{ marginBottom: 10, padding: '8px 10px', background: C.tealBg, borderRadius: 6 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Pixel-level lesion masks</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 4 }}>
                {d.lesionMasks.types.map(t => (
                  <span key={t} style={{ padding: '1px 6px', background: C.teal, color: '#fff', borderRadius: 3, fontSize: 9, fontWeight: 500 }}>{t}</span>
                ))}
              </div>
              <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>
                {d.lesionMasks.annotatedImages} images annotated · Tool: {d.lesionMasks.annotationTool} · {d.lesionMasks.validation}
              </div>
            </div>
          )}

          {/* Dropped reason */}
          {d.droppedReason && (
            <div style={{ marginBottom: 10, padding: '8px 10px', background: C.grayBg, borderRadius: 6 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.grayT, marginBottom: 3, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Why dropped</div>
              <div style={{ fontSize: 11, color: C.grayT, lineHeight: 1.6 }}>{d.droppedReason}</div>
            </div>
          )}

          {/* Limitations */}
          {d.limitations && d.limitations.length > 0 && (
            <div style={{ marginBottom: 8 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--color-text-secondary,#666)', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Limitations</div>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: 11, lineHeight: 1.65, color: 'var(--color-text-secondary,#555)' }}>
                {d.limitations.map((l, i) => <li key={i} style={{ marginBottom: 2 }}>{l}</li>)}
              </ul>
            </div>
          )}

          {/* Split strategy */}
          {d.splitStrategy && d.splitStrategy !== '—' && (
            <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', padding: '5px 8px', background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 5 }}>
              <strong>Split strategy: </strong>{d.splitStrategy}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function DatasetCards() {
  const { t } = useLang();
  return (
    <Sec title={t('datasets.individualDetail')} note="Click any dataset to expand full details including selection rationale, taxonomy mapping, and known limitations.">
      {DATASETS.map(d => <DatasetCard key={d.name} dataset={d} />)}
    </Sec>
  );
}

// ── Section F: Taxonomy Harmonization ────────────────────────────────────────
function TaxonomyHarmonization() {
  const { t } = useLang();
  const odir5kMapping = [
    { keyword: 'proliferative diabetic retinopathy', grade: '4', note: 'PDR = most severe' },
    { keyword: 'very severe (non proliferative)', grade: '4', note: '' },
    { keyword: 'severe non proliferative retinopathy', grade: '3', note: '' },
    { keyword: 'severe diabetic retinopathy', grade: '3', note: '' },
    { keyword: 'moderate non proliferative retinopathy', grade: '2', note: '' },
    { keyword: 'moderate diabetic retinopathy', grade: '2', note: '' },
    { keyword: 'mild non proliferative retinopathy', grade: '1', note: '' },
    { keyword: 'mild diabetic retinopathy', grade: '1', note: '' },
    { keyword: 'diabetic retinopathy (unqualified)', grade: '2', note: 'Conservative mapping' },
    { keyword: 'laser spot', grade: '4', note: 'Implies prior PDR treatment' },
    { keyword: 'non proliferative retinopathy', grade: '2', note: '' },
  ];

  return (
    <Sec title={t('datasets.harmonization')}
      note="All datasets are harmonized to 5-class ICDR grading (DR 0–4) for cross-dataset comparison. The mapping strategies below are applied consistently in the data loader (label_harmonization.py).">

      {/* Overview table */}
      <div style={{ overflowX: 'auto', marginBottom: 16 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)', background: 'var(--color-background-secondary,#f7f7f5)' }}>
              {['Dataset', 'Original Taxonomy', 'Mapping to 5-class ICDR', 'Complexity'].map(h => (
                <th key={h} style={{ padding: '6px 8px', textAlign: 'left', fontWeight: 600 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              { name: 'EyePACS', orig: '5-class ICDR (DR 0–4)', mapping: 'None required — native format', complexity: 'None', color: 'green' },
              { name: 'IDRiD', orig: '5-class ICDR (DR 0–4) + lesion masks', mapping: 'None required — native format', complexity: 'None', color: 'green' },
              { name: 'DDR', orig: '6-class (DR 0–5)', mapping: 'Exclude grade 5 (ungradable); grades 0–4 map directly', complexity: 'Minimal', color: 'teal' },
              { name: 'Messidor-2', orig: 'Referable / Non-referable', mapping: 'Grade 0→DR 0, grade 1→DR 1, grade 2→DR 2; no DR 3/4 available', complexity: 'Moderate', color: 'amber' },
              { name: 'ODIR-5K', orig: 'Multi-disease keyword strings', mapping: 'Priority keyword matching → DR grade (see table below)', complexity: 'High', color: 'coral' },
              { name: 'RFMiD', orig: 'Multi-disease, binary DR column', mapping: 'Binary only (0=no DR, 1=DR present); no severity grading', complexity: 'High (binary only)', color: 'coral' },
            ].map((r, i) => (
              <tr key={r.name} style={{ borderBottom: '1px solid var(--color-border-tertiary,#eee)', background: i % 2 === 0 ? 'transparent' : 'var(--color-background-secondary,#fafafa)' }}>
                <td style={{ padding: '5px 8px', fontWeight: 500 }}>{r.name}</td>
                <td style={{ padding: '5px 8px', fontSize: 10 }}>{r.orig}</td>
                <td style={{ padding: '5px 8px', fontSize: 10 }}>{r.mapping}</td>
                <td style={{ padding: '5px 8px' }}>
                  <span style={{ padding: '1px 6px', borderRadius: 4, fontSize: 10, fontWeight: 500, background: C[r.color + 'Bg'] || C.grayBg, color: C[r.color + 'T'] || C.grayT }}>
                    {r.complexity}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ODIR-5K keyword mapping */}
      <div style={{ marginTop: 8 }}>
        <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 6, color: 'var(--color-text-primary,#333)' }}>
          ODIR-5K Keyword-to-Grade Mapping
        </div>
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
          Priority-ordered keyword matching: earlier entries take precedence when multiple keywords match. Implemented in <code style={{ background: 'var(--color-background-secondary,#f0f0ee)', padding: '0 3px', borderRadius: 3 }}>label_harmonization.py</code>.
        </div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ borderCollapse: 'collapse', fontSize: 10 }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)', background: 'var(--color-background-secondary,#f7f7f5)' }}>
                {['Diagnostic Keyword', 'DR Grade', 'Note'].map(h => (
                  <th key={h} style={{ padding: '4px 8px', textAlign: 'left', fontWeight: 600 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {odir5kMapping.map((row, i) => (
                <tr key={i} style={{ borderBottom: '1px solid var(--color-border-tertiary,#eee)', background: i % 2 === 0 ? 'transparent' : 'var(--color-background-secondary,#fafafa)' }}>
                  <td style={{ padding: '4px 8px', fontStyle: 'italic' }}>&ldquo;{row.keyword}&rdquo;</td>
                  <td style={{ padding: '4px 8px', textAlign: 'center', fontWeight: 700, color: [C.green, C.teal, C.amber, C.coral, C.red][parseInt(row.grade)] }}>
                    DR {row.grade}
                  </td>
                  <td style={{ padding: '4px 8px', color: 'var(--color-text-secondary,#888)' }}>{row.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Sec>
  );
}

// ── Section G: Data Flow Diagram ──────────────────────────────────────────────
function DataFlowDiagram() {
  const { t } = useLang();
  const boxStyle = (color) => ({
    display: 'inline-block', padding: '5px 10px', borderRadius: 5, fontSize: 10, fontWeight: 600,
    background: C[color + 'Bg'] || C.grayBg, color: C[color + 'T'] || C.grayT,
    border: `1px solid ${C[color] || C.gray}40`,
  });
  const arrowStyle = { fontSize: 10, color: 'var(--color-text-secondary,#aaa)', margin: '0 4px' };
  const expStyle = (color) => ({
    display: 'inline-block', padding: '2px 7px', borderRadius: 4, fontSize: 9, fontWeight: 500,
    background: C[color + 'Bg'] || C.grayBg, color: C[color + 'T'] || C.grayT, margin: '0 2px',
  });
  const rowStyle = { display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 4, padding: '6px 0' };
  const branchStyle = { display: 'flex', flexDirection: 'column', gap: 3, paddingLeft: 16, borderLeft: `2px solid ${C.blueBg}`, marginLeft: 8 };

  return (
    <Sec title={t('datasets.dataFlow')}
      note="EyePACS is the sole training dataset. All other datasets serve as evaluation targets. No external dataset is used for training or fine-tuning.">
      <div style={{ fontSize: 11, lineHeight: 1.8, padding: '4px 0' }}>

        {/* EyePACS → Exp 1, Exp 2 */}
        <div style={rowStyle}>
          <span style={boxStyle('blue')}>EyePACS</span>
          <span style={arrowStyle}>→</span>
          <span style={expStyle('blue')}>Exp 1 (H-1): Factorial design — train + eval</span>
          <span style={expStyle('blue')}>Exp 2 (H-2): CLAHE ablation — partial eval</span>
        </div>

        {/* EyePACS → Transfer */}
        <div style={{ ...rowStyle, paddingBottom: 2 }}>
          <span style={boxStyle('blue')}>EyePACS</span>
          <span style={arrowStyle}>→ trained models →</span>
          <span style={arrowStyle}>cross-dataset evaluation</span>
        </div>
        <div style={branchStyle}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={boxStyle('purple')}>Messidor-2</span>
            <span style={arrowStyle}>→</span>
            <span style={expStyle('purple')}>Exp 5 (H-4): G=0.90 ≥ 0.85 ✓</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={boxStyle('teal')}>IDRiD</span>
            <span style={arrowStyle}>→</span>
            <span style={expStyle('teal')}>Exp 5 (H-4): G=0.88 ≥ 0.85 ✓</span>
          </div>
        </div>

        {/* EyePACS → Device shift */}
        <div style={{ ...rowStyle, paddingTop: 6, paddingBottom: 2 }}>
          <span style={boxStyle('blue')}>EyePACS</span>
          <span style={arrowStyle}>→ trained models →</span>
          <span style={arrowStyle}>device-shift evaluation</span>
        </div>
        <div style={branchStyle}>
          {[
            ['DDR', 'Canon+Topcon → Exp 6 (H-6)'],
            ['ODIR-5K', 'Canon+Zeiss → Exp 6 (H-6)'],
            ['RFMiD', 'Topcon+Kowa → Exp 6 (H-6)'],
          ].map(([name, label]) => (
            <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={boxStyle('coral')}>{name}</span>
              <span style={arrowStyle}>→</span>
              <span style={expStyle('coral')}>{label}</span>
            </div>
          ))}
        </div>

        {/* IDRiD multi-role */}
        <div style={{ ...rowStyle, paddingTop: 10 }}>
          <span style={boxStyle('teal')}>IDRiD</span>
          <span style={arrowStyle}>→</span>
          <span style={expStyle('teal')}>Exp 2 (H-2): CLAHE parameter sweep target</span>
          <span style={expStyle('teal')}>Exp 4 (H-5): Grad-CAM / ALO with lesion masks</span>
          <span style={expStyle('teal')}>Exp 5 (H-4): Transfer evaluation target</span>
        </div>
      </div>
    </Sec>
  );
}

// ── Section H: Split Strategy ─────────────────────────────────────────────────
function SplitStrategy() {
  const { t } = useLang();
  return (
    <Sec title={t('datasets.splitSection')}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {[
          {
            title: 'Patient-level stratified 5-fold CV',
            color: 'blue',
            content: 'Both eyes of the same patient are always assigned to the same fold. Patient ID is extracted from the filename prefix (e.g., "1234_left.jpeg" → patient 1234). This prevents data leakage through bilateral correlation — a key requirement for valid performance estimation.',
          },
          {
            title: 'Why 5-fold CV',
            color: 'teal',
            content: 'We use full EyePACS (100%, ~35,126 images) with 5-fold CV. 5-fold provides lower variance in performance estimates than 3-fold and is the standard for large-scale DR benchmarks. RTX 3060 (12 GB VRAM) with batch size 16, mixed precision disabled for EfficientNet.',
          },
          {
            title: 'Full EyePACS (100%, ~35,126 images)',
            color: 'amber',
            content: 'We use the complete EyePACS labeled set (~35,126 images). Using the full dataset increases statistical power for detecting preprocessing effects and provides more robust 5-class performance estimates across 5-fold CV.',
          },
          {
            title: 'External datasets — zero-shot evaluation',
            color: 'purple',
            content: 'IDRiD, Messidor-2, DDR, ODIR-5K, and RFMiD are used exclusively as external test sets. No training or fine-tuning is performed on any of these datasets. Best checkpoint from EyePACS CV is applied directly — this is the "zero-shot transfer" setting used to compute generalization ratio G.',
          },
        ].map(item => (
          <div key={item.title} style={{
            padding: '10px 12px',
            background: C[item.color + 'Bg'] || C.grayBg,
            borderRadius: 7, borderLeft: `3px solid ${C[item.color] || C.gray}`,
          }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: C[item.color + 'T'] || C.grayT, marginBottom: 4 }}>{item.title}</div>
            <div style={{ fontSize: 11, lineHeight: 1.65, color: C[item.color + 'T'] || C.grayT }}>{item.content}</div>
          </div>
        ))}
      </div>
    </Sec>
  );
}

// ── Section: Camera Distribution — Central Asia vs Training ──────────────────
const CAMERA_COLORS = { Canon: 'blue', Topcon: 'teal', Kowa: 'amber', Zeiss: 'purple', Other: 'gray' };

function DistributionRow({ data }) {
  const { label, ...shares } = data;
  const total = Object.values(shares).reduce((a, b) => a + b, 0);
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-primary,#333)', marginBottom: 5 }}>
        {label}
      </div>
      <div style={{ display: 'flex', height: 24, borderRadius: 5, overflow: 'hidden', border: '1px solid var(--color-border-tertiary,#eee)' }}>
        {Object.entries(shares).map(([brand, pct]) => {
          const colorKey = CAMERA_COLORS[brand] || 'gray';
          return (
            <div key={brand} style={{
              width: `${(pct / total) * 100}%`,
              background: C[colorKey] || C.gray,
              opacity: 0.85,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 9, fontWeight: 700, color: '#fff',
            }} title={`${brand}: ${pct}%`}>
              {pct >= 8 ? `${brand} ${pct}%` : pct >= 4 ? `${pct}%` : ''}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function CameraDistribution() {
  return (
    <Sec title="Camera Distribution — Central Asia vs Training Datasets"
      note="Topcon + Canon together cover 83% of regional Central Asia clinics and 73% of the training data — the training distribution thus fully covers the dominant deployment domain (slide 14, dissertation defense).">
      <DistributionRow data={CAMERA_DISTRIBUTION.centralAsia} />
      <DistributionRow data={CAMERA_DISTRIBUTION.training} />

      <div style={{ display: 'flex', gap: 8, marginTop: 6 }}>
        {[
          { ...CAMERA_DISTRIBUTION.coverage.centralAsia, color: 'teal' },
          { ...CAMERA_DISTRIBUTION.coverage.training,    color: 'blue' },
        ].map((c, i) => (
          <div key={i} style={{
            flex: 1, padding: '8px 12px',
            background: C[c.color + 'Bg'], borderLeft: `3px solid ${C[c.color]}`, borderRadius: 6,
          }}>
            <div style={{ fontSize: 10, color: C[c.color + 'T'], opacity: 0.8 }}>{c.label}</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: C[c.color + 'T'], marginTop: 2 }}>{c.value}%</div>
          </div>
        ))}
      </div>
    </Sec>
  );
}

// ── Section I: Resolution & Camera Analysis ─────────────────────────────────
function ResolutionAnalysis() {
  const { t } = useLang();
  const datasets = Object.entries(RESOLUTION_ANALYSIS);
  const maxUnique = Math.max(...datasets.map(([, d]) => d.uniqueResolutions));

  return (
    <Sec title={t('datasets.resolutionAnalysis') || 'Resolution & Camera Analysis'}
      note="EXIF metadata stripped from all datasets. Resolution grouping is the only per-image camera proxy available. Key finding: RFMiD 4288×2848 images match IDRiD Kowa VX-10α exactly (497 of 3,200 images).">

      {/* Resolution diversity bar chart */}
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-primary,#333)', marginBottom: 8 }}>
        Resolution diversity (unique resolutions per dataset)
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 5, marginBottom: 16 }}>
        {datasets
          .sort(([, a], [, b]) => b.uniqueResolutions - a.uniqueResolutions)
          .map(([name, d]) => (
            <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ fontSize: 10, minWidth: 90, textAlign: 'right', color: 'var(--color-text-secondary,#666)' }}>
                {name}
              </div>
              <div style={{ flex: 1, height: 18, background: 'var(--color-background-secondary,#eeede9)', borderRadius: 3, position: 'relative', overflow: 'hidden' }}>
                <div style={{
                  width: `${(d.uniqueResolutions / maxUnique) * 100}%`,
                  height: '100%',
                  background: d.uniqueResolutions > 50 ? C.coral : d.uniqueResolutions > 10 ? C.amber : d.uniqueResolutions > 1 ? C.teal : C.blue,
                  borderRadius: 3, opacity: 0.75,
                }} />
                <span style={{ position: 'absolute', left: 6, top: '50%', transform: 'translateY(-50%)', fontSize: 9, fontWeight: 600, color: d.uniqueResolutions > 20 ? '#fff' : 'var(--color-text-primary,#333)' }}>
                  {d.uniqueResolutions}
                </span>
              </div>
              <div style={{ fontSize: 9, color: 'var(--color-text-secondary,#888)', minWidth: 140 }}>
                {d.camera}
              </div>
            </div>
          ))}
      </div>

      {/* Resolution groups detail */}
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-primary,#333)', marginBottom: 8 }}>
        Top resolution groups per dataset
      </div>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 10 }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)', background: 'var(--color-background-secondary,#f7f7f5)' }}>
              {['Dataset', 'Resolution', 'Count', '%', 'Note'].map(h => (
                <th key={h} style={{ padding: '4px 8px', textAlign: 'left', fontWeight: 600 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {datasets.map(([name, d]) =>
              d.groups.slice(0, 3).map((g, gi) => (
                <tr key={`${name}-${gi}`} style={{
                  borderBottom: gi === Math.min(2, d.groups.length - 1) ? '2px solid var(--color-border-tertiary,#ddd)' : '1px solid var(--color-border-tertiary,#eee)',
                  background: gi === 0 ? 'transparent' : 'var(--color-background-secondary,#fafafa)',
                }}>
                  {gi === 0 ? (
                    <td rowSpan={Math.min(3, d.groups.length)} style={{ padding: '4px 8px', fontWeight: 600, verticalAlign: 'top', borderRight: '1px solid var(--color-border-tertiary,#eee)' }}>
                      {name}
                      <div style={{ fontSize: 9, fontWeight: 400, color: 'var(--color-text-secondary,#999)', marginTop: 2 }}>{d.camera}</div>
                    </td>
                  ) : null}
                  <td style={{ padding: '4px 8px', fontFamily: 'monospace', fontSize: 10 }}>{g.res}</td>
                  <td style={{ padding: '4px 8px', textAlign: 'right' }}>{g.count.toLocaleString()}</td>
                  <td style={{ padding: '4px 8px', textAlign: 'right' }}>{(g.pct || g.pctSampled || 0).toFixed(1)}%</td>
                  <td style={{ padding: '4px 8px', color: g.note ? C.teal : 'var(--color-text-secondary,#ccc)', fontStyle: g.note ? 'normal' : 'italic', fontSize: 9 }}>
                    {g.note || '—'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Key findings */}
      <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
        {[
          { color: 'teal', title: 'RFMiD camera split identified', text: '4288×2848 (497 imgs, 15.5%) = Kowa VX-10α (matches IDRiD). Remaining 84.5% = Topcon.' },
          { color: 'purple', title: 'Clinical = Messidor-2 camera', text: 'Identical 3-resolution profile. Almaty clinic uses same Topcon TRC NW6 or equivalent.' },
          { color: 'blue', title: 'DDR contains Canon CR-1', text: '677 images at 3888×2592 match EyePACS native resolution — partial training domain overlap.' },
          { color: 'amber', title: 'ODIR-5K Zeiss indicator', text: 'Square formats (1444×1444, 2976×2976) typical of Zeiss devices — unique to this dataset.' },
        ].map(f => (
          <div key={f.title} style={{
            flex: '1 1 220px', padding: '8px 10px', borderRadius: 6,
            background: C[f.color + 'Bg'], borderLeft: `3px solid ${C[f.color]}`,
          }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: C[f.color + 'T'], marginBottom: 3 }}>{f.title}</div>
            <div style={{ fontSize: 10, lineHeight: 1.5, color: C[f.color + 'T'] }}>{f.text}</div>
          </div>
        ))}
      </div>
    </Sec>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────
export default function Datasets() {
  return (
    <div>
      <TierOverview />
      <SummaryTable />
      <CameraMatrix />
      <CameraDistribution />
      <ResolutionAnalysis />
      <ClassDistribution />
      <DatasetCards />
      <TaxonomyHarmonization />
      <DataFlowDiagram />
      <SplitStrategy />
    </div>
  );
}
