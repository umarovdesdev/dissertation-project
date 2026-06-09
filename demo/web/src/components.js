// src/components.js — Reusable UI components for DR Dashboard
import { useState } from 'react';
import { C } from './data';
import { useLang } from './i18n';

export function Card({ label, value, delta, color, sub }) {
  const bg = C[color + 'Bg'] || C.grayBg;
  const tx = C[color + 'T'] || C.grayT;
  return (
    <div style={{ background: bg, borderRadius: 10, padding: '11px 14px', flex: 1, minWidth: 110 }}>
      <div style={{ fontSize: 10, color: tx, opacity: 0.75 }}>{label}</div>
      <div style={{ fontSize: 20, fontWeight: 600, color: tx, marginTop: 2 }}>{value}</div>
      {delta && (
        <div style={{ fontSize: 10, color: (delta.includes('✓') || delta.includes('+')) ? C.green : C.red, marginTop: 1 }}>
          {delta}
        </div>
      )}
      {sub && <div style={{ fontSize: 9, color: tx, opacity: 0.5, marginTop: 1 }}>{sub}</div>}
    </div>
  );
}

export function Note({ children }) {
  return (
    <div style={{
      fontSize: 11, color: 'var(--color-text-secondary,#666)',
      padding: '8px 12px', background: 'var(--color-background-secondary,#f7f7f5)',
      borderRadius: 7, marginTop: 8, lineHeight: 1.6,
    }}>
      {children}
    </div>
  );
}

export function Hbar({ items, maxV, height = 20 }) {
  const mx = maxV || Math.max(...items.map(i => i.v)) * 1.1;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      {items.map((it, i) => (
        <div key={i} className="hbar-row" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div className="hbar-label" style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', minWidth: 150, textAlign: 'right', lineHeight: 1.2 }}>
            {it.label}
          </div>
          <div style={{ flex: 1, height, background: 'var(--color-background-secondary,#eeede9)', borderRadius: 3, position: 'relative', overflow: 'hidden' }}>
            <div style={{ width: `${(it.v / mx) * 100}%`, height: '100%', background: it.color || C.blue, borderRadius: 3, opacity: 0.8 }} />
            <span style={{ position: 'absolute', right: 5, top: '50%', transform: 'translateY(-50%)', fontSize: 9, fontWeight: 500 }}>
              {it.v.toFixed ? it.v.toFixed(3) : it.v}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export function Paired({ items, c1 = C.gray, c2 = C.teal, l1 = 'Baseline', l2 = 'Pipeline' }) {
  const mx = Math.max(...items.flatMap(i => [i.a, i.b])) * 1.12;
  return (
    <div>
      <div style={{ display: 'flex', gap: 14, fontSize: 10, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <span style={{ width: 8, height: 8, borderRadius: 2, background: c1, display: 'inline-block' }} />{l1}
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <span style={{ width: 8, height: 8, borderRadius: 2, background: c2, display: 'inline-block' }} />{l2}
        </span>
      </div>
      {items.map((it, i) => (
        <div key={i} style={{ marginBottom: 8 }}>
          <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', marginBottom: 2 }}>{it.label}</div>
          {[{ v: it.a, c: c1 }, { v: it.b, c: c2 }].map((b, bi) => (
            <div key={bi} style={{ display: 'flex', alignItems: 'center', gap: 4, marginBottom: 1 }}>
              <div style={{ flex: 1, height: 16, background: 'var(--color-background-secondary,#eeede9)', borderRadius: 3, position: 'relative', overflow: 'hidden' }}>
                <div style={{ width: `${(b.v / mx) * 100}%`, height: '100%', background: b.c, borderRadius: 3, opacity: 0.8 }} />
                <span style={{ position: 'absolute', right: 4, top: '50%', transform: 'translateY(-50%)', fontSize: 9, fontWeight: 500 }}>
                  {b.v.toFixed(3)}
                </span>
              </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export function Sec({ title, note, children }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, margin: 0, color: 'var(--color-text-primary,#333)' }}>{title}</h3>
      </div>
      {children}
      {note && <Note>{note}</Note>}
    </div>
  );
}

export function DataTable({ headers, rows, highlightRow }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
        <thead>
          <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)' }}>
            {headers.map((h, i) => (
              <th key={i} style={{ padding: '5px 8px', textAlign: i === 0 ? 'left' : 'center', fontWeight: 600, color: 'var(--color-text-primary,#333)' }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} style={{
              borderBottom: '1px solid var(--color-border-tertiary,#eee)',
              background: highlightRow && highlightRow(row, i) ? C.amberBg : 'transparent',
            }}>
              {row.map((cell, j) => (
                <td key={j} style={{
                  padding: '5px 8px',
                  textAlign: j === 0 ? 'left' : 'center',
                  fontWeight: j === 0 ? 500 : 400,
                  color: typeof cell === 'string' && cell.includes('✓') ? C.teal : 'inherit',
                }}>
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function ImageFigure({ src, caption, figNum }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <img
        src={src}
        alt={caption || ''}
        style={{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)', display: 'block' }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4 }}>
          {figNum && <strong>Fig. {figNum}. </strong>}{caption}
        </div>
      )}
    </div>
  );
}

export function DiagramViewer({ src, alt, caption, tooltip }) {
  const [show, setShow] = useState(false);
  const { t } = useLang();
  const tooltipText = tooltip && tooltip.startsWith('tooltip.') ? t(tooltip) : tooltip;
  return (
    <div
      style={{ marginBottom: 16, position: 'relative' }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onClick={() => setShow(s => !s)}
    >
      <img
        src={src}
        alt={alt || caption || ''}
        style={{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)', display: 'block', background: '#fff', cursor: tooltipText ? 'help' : 'default' }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4, textAlign: 'center' }}>
          {caption}
        </div>
      )}
      {show && tooltipText && (
        <div className="tooltip-bubble" style={{
          position: 'absolute', bottom: '100%', left: '50%',
          transform: 'translateX(-50%)', marginBottom: 8,
          padding: '10px 14px', background: 'rgba(0,0,0,0.88)', color: 'white',
          borderRadius: 8, fontSize: 12, lineHeight: 1.5,
          maxWidth: 380, width: 'max-content', zIndex: 1000,
          pointerEvents: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        }}>
          {tooltipText}
          <div style={{
            position: 'absolute', top: '100%', left: '50%',
            transform: 'translateX(-50%)',
            width: 0, height: 0,
            borderLeft: '6px solid transparent', borderRight: '6px solid transparent',
            borderTop: '6px solid rgba(0,0,0,0.88)',
          }} />
        </div>
      )}
    </div>
  );
}

export function ImageWithTooltip({ src, alt, tooltip, figNum, caption, style }) {
  const [show, setShow] = useState(false);
  const { t } = useLang();
  const tooltipText = tooltip && tooltip.startsWith('tooltip.') ? t(tooltip) : tooltip;
  return (
    <div
      style={{ position: 'relative', marginBottom: 16, ...(style || {}) }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onClick={() => setShow(s => !s)}
    >
      <img
        src={src}
        alt={alt || caption || ''}
        style={{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)', cursor: 'help', display: 'block' }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4, lineHeight: 1.4 }}>
          {figNum && <strong>Fig. {figNum}. </strong>}{caption}
        </div>
      )}
      {show && tooltipText && (
        <div className="tooltip-bubble" style={{
          position: 'absolute', bottom: '100%', left: '50%',
          transform: 'translateX(-50%)', marginBottom: 8,
          padding: '10px 14px', background: 'rgba(0,0,0,0.88)', color: 'white',
          borderRadius: 8, fontSize: 12, lineHeight: 1.5,
          maxWidth: 380, width: 'max-content', zIndex: 1000,
          pointerEvents: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        }}>
          {tooltipText}
          <div style={{
            position: 'absolute', top: '100%', left: '50%',
            transform: 'translateX(-50%)',
            width: 0, height: 0,
            borderLeft: '6px solid transparent', borderRight: '6px solid transparent',
            borderTop: '6px solid rgba(0,0,0,0.88)',
          }} />
        </div>
      )}
    </div>
  );
}

export function LangSwitcher() {
  const { lang, setLang } = useLang();
  const label = lang === 'en' ? 'EN' : 'ҚАЗ';
  const next = lang === 'en' ? 'kz' : 'en';
  return (
    <button
      type="button"
      className="chip-toggle"
      onClick={() => setLang(next)}
      title={`Language: ${label} (click to switch)`}
      aria-label={`Language: ${label}, click to switch`}
    >
      <span aria-hidden="true">🌐</span>
      <span>{label}</span>
    </button>
  );
}

export function ModeSwitcher({ mode, setMode }) {
  const isLite = mode === 'lite';
  const icon = isLite ? '⚡' : '📚';
  const label = isLite ? 'Lite' : 'Full';
  const next = isLite ? 'full' : 'lite';
  return (
    <button
      type="button"
      className="chip-toggle"
      onClick={() => setMode(next)}
      title={`Mode: ${label} (click to switch)`}
      aria-label={`Mode: ${label}, click to switch`}
    >
      <span aria-hidden="true">{icon}</span>
      <span>{label}</span>
    </button>
  );
}
