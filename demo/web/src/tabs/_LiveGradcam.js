// src/tabs/_LiveGradcam.js — live Grad-CAM for the result panel (TASK-Demo D.3).
// Calls POST /api/gradcam per present eye and renders the returned heatmap +
// attention overlay in the same two-pane layout as the pre-rendered
// HeatmapPair, so the result section looks identical whether the source is the
// live checkpoint or a walkthrough's bundled assets.

import { useEffect, useState } from 'react';
import { C } from '../data';
import { Note } from '../components';
import { gradcamImage } from './_apiPredict';

function EyeGradcam({ eye, src, name, t }) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('loading'); // loading | done | error

  useEffect(() => {
    let alive = true;
    setStatus('loading'); setData(null);
    gradcamImage(src, eye, name)
      .then((d) => { if (alive) { setData(d); setStatus('done'); } })
      .catch(() => { if (alive) setStatus('error'); });
    return () => { alive = false; };
  }, [src, eye, name]);

  const label = t(eye === 'left' ? 'demo.leftEye' : 'demo.rightEye');

  if (status !== 'done') {
    return (
      <div style={{ flex: 1, minWidth: 220 }}>
        <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>{label}</div>
        <div style={{ fontSize: 10, color: status === 'error' ? C.amberT : C.gray }}>
          {status === 'error' ? t('demo.gradcam.error') : t('demo.gradcam.loading')}
        </div>
      </div>
    );
  }

  const overlay = `data:image/png;base64,${data.attention_overlay_png_b64}`;
  return (
    <div style={{ flex: 1, minWidth: 220 }}>
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>{label}</div>
      <figure style={{ margin: 0 }}>
        {/* The backend warps the overlay back into the original upload frame, so
            no client-side flip is needed — it already matches the snapshot. */}
        <img
          src={overlay}
          alt={`Attention overlay ${eye}`}
          style={{ width: '100%', display: 'block', borderRadius: 6, background: '#000' }}
        />
        <figcaption style={{ fontSize: 10, marginTop: 4, color: 'var(--color-text-secondary,#666)' }}>{t('demo.viz.overlay')}</figcaption>
      </figure>
      {/* Predicted-class rationale (TASK-Demo D.3) — backend-generated from CAM
          geometry (no LLM). English only, per the backend-copy scope note. */}
      {data.rationale && (
        <div style={{ marginTop: 8 }}>
          <div style={{ fontSize: 10, fontWeight: 600, color: 'var(--color-text-secondary,#666)' }}>
            {t('demo.viz.rationaleLabel')}
          </div>
          <div style={{ fontSize: 11, color: 'var(--color-text-primary,#333)', lineHeight: 1.5, marginTop: 2 }}>
            {data.rationale}
          </div>
        </div>
      )}
    </div>
  );
}

export default function LiveVisualizationBlock({ eyes, t }) {
  // Right eye (OD) first (shown on the left), matching the clinical convention
  // and the upload block order.
  const ordered = [...eyes].sort(
    (a, b) => (a.eye === 'right' ? 0 : 1) - (b.eye === 'right' ? 0 : 1)
  );
  return (
    <div style={{ marginTop: 14 }}>
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
        {t('demo.viz.title')}
      </div>
      <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
        {ordered.map((e) => (
          <EyeGradcam key={e.eye} eye={e.eye} src={e.src} name={e.name} t={t} />
        ))}
      </div>
      <Note>{t('demo.viz.liveDisclaimer')}</Note>
    </div>
  );
}
