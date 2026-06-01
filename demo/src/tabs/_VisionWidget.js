// src/tabs/_VisionWidget.js — "what the model sees" per-image widget (TASK-Demo D.2).
// Calls POST /api/visualize and shows: OD/fovea markers over the input, a
// confidence chip, an expandable 6-panel V5 preprocessing strip, and a FOV-mask
// toggle. This is the visual core of contributions C-1, SC-E, SC-F and works on
// arbitrary uploads (visualize is preprocessing-only — no trained checkpoint
// needed), so it lights up as soon as the backend is reachable.

import { useEffect, useState } from 'react';
import { C } from '../data';
import { visualizeImage } from './_apiPredict';

const BOX = 200; // square preview box (px)

// Map an (x, y) in analysis space → pixel coords inside the BOX, accounting for
// objectFit:contain letterboxing and the canonical left→right flip.
function project(x, y, sw, sh, flipped) {
  const scale = Math.min(BOX / sw, BOX / sh);
  const offX = (BOX - sw * scale) / 2;
  const offY = (BOX - sh * scale) / 2;
  const dx = flipped ? sw - x : x;
  return [offX + dx * scale, offY + y * scale, scale];
}

export default function VisionWidget({ src, eye, name, enabled, t }) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | loading | done | error
  const [showStages, setShowStages] = useState(false);
  const [showMask, setShowMask] = useState(false);

  useEffect(() => {
    if (!enabled || !src) { setData(null); setStatus('idle'); return; }
    let alive = true;
    setStatus('loading'); setData(null); setShowStages(false); setShowMask(false);
    visualizeImage(src, eye, name)
      .then((d) => { if (alive) { setData(d); setStatus('done'); } })
      .catch(() => { if (alive) { setStatus('error'); } });
    return () => { alive = false; };
  }, [src, eye, name, enabled]);

  if (!enabled) return null;
  if (status === 'loading') {
    return <div style={{ fontSize: 10, color: C.gray, marginTop: 6 }}>{t('demo.vision.loading')}</div>;
  }
  if (status === 'error' || !data) {
    return <div style={{ fontSize: 10, color: C.amberT, marginTop: 6 }}>{t('demo.vision.unavailable')}</div>;
  }

  const od = data.od_fovea || {};
  const sw = od.space_w || BOX, sh = od.space_h || BOX, flipped = !!od.flipped;
  const [odx, ody, scale] = od.confident ? project(od.od_center[0], od.od_center[1], sw, sh, flipped) : [0, 0, 1];
  const [fvx, fvy] = od.confident ? project(od.fovea_center[0], od.fovea_center[1], sw, sh, flipped) : [0, 0];
  const odR = (od.od_radius || 0) * scale;
  const fvR = (od.fovea_radius || 0) * scale;

  const maskSrc = `data:image/png;base64,${data.fov_mask_png_b64}`;
  const stripSrc = `data:image/png;base64,${data.v5_preview_png_b64}`;

  return (
    <div style={{ marginTop: 8 }}>
      {/* Preview with OD/fovea overlay (or FOV mask) */}
      <div style={{ position: 'relative', width: BOX, height: BOX, background: '#000', borderRadius: 8, overflow: 'hidden' }}>
        <img
          src={showMask ? maskSrc : src}
          alt={showMask ? 'FOV mask' : 'input'}
          style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
        />
        {!showMask && od.confident && (
          <svg width={BOX} height={BOX} style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
            <line x1={odx} y1={ody} x2={fvx} y2={fvy} stroke={C.amber} strokeWidth="1.5" strokeDasharray="3 2" />
            <circle cx={odx} cy={ody} r={Math.max(odR, 4)} fill="none" stroke={C.teal} strokeWidth="2" />
            <circle cx={fvx} cy={fvy} r={Math.max(fvR, 3)} fill="none" stroke={C.coral} strokeWidth="2" />
          </svg>
        )}
      </div>

      {/* OD–fovea chip */}
      <div style={{ marginTop: 6, fontSize: 10, color: 'var(--color-text-secondary,#666)' }}>
        {od.confident ? (
          <span>
            <span style={{ color: C.teal, fontWeight: 700 }}>OD</span>
            {' · '}
            <span style={{ color: C.coral, fontWeight: 700 }}>{t('demo.vision.fovea')}</span>
            {' · '}{t('demo.vision.angle')}: <strong>{(od.angle_deg).toFixed(1)}°</strong>
            {' · σ: '}<strong>{(od.rotation_sigma_deg).toFixed(1)}°</strong>
            {' · '}<span style={{ color: C.greenT }}>✓ {t('demo.vision.confident')}</span>
          </span>
        ) : (
          <span style={{ color: C.amberT }}>⚠ {t('demo.vision.lowConfidence')}</span>
        )}
      </div>

      {/* Toggles */}
      <div style={{ display: 'flex', gap: 6, marginTop: 6, flexWrap: 'wrap' }}>
        <button onClick={() => setShowStages(v => !v)} style={chipBtn}>
          {showStages ? t('demo.vision.hideStages') : t('demo.vision.showStages')}
        </button>
        <button onClick={() => setShowMask(v => !v)} style={chipBtn}>
          {showMask ? t('demo.vision.hideMask') : t('demo.vision.showMask')}
        </button>
      </div>

      {/* V5 stage strip */}
      {showStages && (
        <div style={{ marginTop: 8, overflowX: 'auto' }}>
          <img src={stripSrc} alt="V5 stages" style={{ height: 120, display: 'block', borderRadius: 6 }} />
          <div style={{ fontSize: 9, color: C.gray, marginTop: 3 }}>{t('demo.vision.stripCaption')}</div>
        </div>
      )}
    </div>
  );
}

const chipBtn = {
  padding: '3px 8px', fontSize: 10, fontWeight: 600,
  background: 'transparent', color: 'var(--color-text-secondary,#666)',
  border: '1px solid var(--color-border-secondary,#ccc)', borderRadius: 4, cursor: 'pointer',
};
