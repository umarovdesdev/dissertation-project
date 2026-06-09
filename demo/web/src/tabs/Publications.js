import { C, PUBLICATIONS } from '../data';
import { Sec, Note } from '../components';
import { useLang } from '../i18n';

function tierBg(color) { return C[color + 'Bg'] || C.grayBg; }
function tierT(color)  { return C[color + 'T']  || C.grayT;  }
function tierFg(color) { return C[color]         || C.gray;   }

export default function Publications() {
  const { t } = useLang();
  const grouped = PUBLICATIONS.reduce((acc, p) => {
    (acc[p.tier] ||= []).push(p);
    return acc;
  }, {});
  const tierOrder = ['Scopus Q3', 'Scopus Conf.', 'KZ VAK'];

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          {t('publications.title') || 'Publications'}
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          {t('publications.subtitle') || 'Dissertation results published in 5 venues — 1 Scopus Q3 journal, 1 Scopus-indexed conference, 3 KZ VAK journals.'}
        </div>
      </div>

      <Sec title={t('publications.summary') || 'Publication Tier Summary'}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 8 }}>
          {tierOrder.map(tier => {
            const items = grouped[tier] || [];
            const color = items[0]?.tierColor || 'gray';
            return (
              <div key={tier} style={{
                flex: 1, minWidth: 140,
                padding: '10px 12px',
                background: tierBg(color),
                borderLeft: `3px solid ${tierFg(color)}`,
                borderRadius: 6,
              }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: tierT(color), letterSpacing: '0.04em', textTransform: 'uppercase' }}>
                  {tier}
                </div>
                <div style={{ fontSize: 22, fontWeight: 700, color: tierT(color), marginTop: 3 }}>
                  {items.length}
                </div>
                <div style={{ fontSize: 10, color: tierT(color), opacity: 0.7 }}>
                  {items.length === 1 ? 'publication' : 'publications'}
                </div>
              </div>
            );
          })}
        </div>
      </Sec>

      {tierOrder.map(tier => {
        const items = grouped[tier] || [];
        if (items.length === 0) return null;
        const color = items[0].tierColor;
        return (
          <Sec key={tier} title={`${tier} (${items.length})`}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {items.map((p, i) => (
                <div key={i} style={{
                  padding: '10px 14px',
                  background: 'var(--color-background-primary,#fff)',
                  border: `1px solid ${tierFg(color)}40`,
                  borderLeft: `3px solid ${tierFg(color)}`,
                  borderRadius: 6,
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, flexWrap: 'wrap' }}>
                    <span style={{
                      padding: '2px 8px', borderRadius: 4, fontSize: 9, fontWeight: 700,
                      background: tierBg(color), color: tierT(color), letterSpacing: '0.04em', textTransform: 'uppercase',
                    }}>
                      {p.type}
                    </span>
                    <span style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)' }}>{p.year}</span>
                  </div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-text-primary,#222)', lineHeight: 1.4, marginBottom: 3 }}>
                    {p.title}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--color-text-secondary,#555)', marginBottom: 2 }}>
                    {p.authors}
                  </div>
                  <div style={{ fontSize: 11, color: tierT(color), fontStyle: 'italic' }}>
                    {p.venue}{p.details ? `. ${p.details}` : ''}
                  </div>
                </div>
              ))}
            </div>
          </Sec>
        );
      })}

      <Note>
        {t('publications.note') || 'Total: 5 publications. Two indexed by Scopus (one Q3 journal, one conference proceedings); three in journals recommended by the Committee for Quality Assurance in the Sphere of Education and Science of the Republic of Kazakhstan (KZ VAK).'}
      </Note>
    </div>
  );
}
