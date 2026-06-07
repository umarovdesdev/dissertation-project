// src/tabs/_VisionWidget.js — "what the model sees" per-image widget (TASK-Demo D.2).
// Calls POST /api/visualize and shows: OD/fovea markers over the input, a
// confidence chip, an expandable 6-panel preprocessing strip, and a FOV-mask
// toggle. This is the visual core of contributions C-1, SC-E, SC-F and works on
// arbitrary uploads (visualize is preprocessing-only — no trained checkpoint
// needed), so it lights up as soon as the backend is reachable.
//
// When a `gt` payload is supplied (IDRiD localization samples), the markers and
// FOV mask are taken from GROUND-TRUTH instead of the detector. IDRiD markups
// are in the displayed image's own frame, so they project by simple scaling
// (no canonical flip / rotation / crop) and therefore align exactly. GT samples
// render even when the backend is offline; the preprocessing strip still needs
// the backend.
//
// For arbitrary uploads (no `gt`) the detector path renders in ANALYSIS space:
// the base image shown is `fov_base_png_b64` (the oriented/cropped 512² RGB),
// not the raw upload, so the FOV mask and OD/fovea markers — both produced in
// that same flipped/rotated/cropped frame by the backend — overlay exactly
// (TASK-fix #1, Option A). The mask is composited as a translucent teal tint on
// top of the base rather than swapped in as a separate image.

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

export default function VisionWidget({ src, eye, name, enabled, gt, t }) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | loading | done | error
  const [showStages, setShowStages] = useState(false);
  const [showMask, setShowMask] = useState(false);

  useEffect(() => {
    // Backend visualize is best-effort: needed for the preprocessing strip and
    // for detector markers on non-GT images. GT samples don't depend on it.
    if (!enabled || !src) { setData(null); setStatus('idle'); return; }
    let alive = true;
    setStatus('loading'); setData(null); setShowStages(false); setShowMask(false);
    visualizeImage(src, eye, name)
      .then((d) => { if (alive) { setData(d); setStatus('done'); } })
      .catch(() => { if (alive) { setStatus('error'); } });
    return () => { alive = false; };
  }, [src, eye, name, enabled]);

  // Nothing to show: no backend and no ground truth.
  if (!enabled && !gt) return null;
  // Backend-only image still waiting on / failing the visualize call.
  if (!gt && status === 'loading') {
    return <div style={{ fontSize: 10, color: C.gray, marginTop: 6 }}>{t('demo.vision.loading')}</div>;
  }
  if (!gt && (status === 'error' || !data)) {
    return <div style={{ fontSize: 10, color: C.amberT, marginTop: 6 }}>{t('demo.vision.unavailable')}</div>;
  }

  // --- Resolve markers + mask from either ground truth or the detector. ---
  let markers = null;   // { odx, ody, odR, fvx, fvy, fvR }
  let maskSrc = null;
  if (gt) {
    const sw = gt.width || BOX, sh = gt.height || BOX;
    const [odx, ody, scale] = project(gt.odCenter[0], gt.odCenter[1], sw, sh, false);
    const [fvx, fvy] = project(gt.foveaCenter[0], gt.foveaCenter[1], sw, sh, false);
    markers = {
      odx, ody, fvx, fvy,
      odR: Math.max((gt.odRadius || 0) * scale, 4),
      fvR: Math.max((gt.odRadius || 0) * scale * 0.4, 3),
    };
    maskSrc = gt.maskSrc;
  } else {
    const od = data.od_fovea || {};
    const sw = od.space_w || BOX, sh = od.space_h || BOX, flipped = !!od.flipped;
    if (od.confident) {
      const [odx, ody, scale] = project(od.od_center[0], od.od_center[1], sw, sh, flipped);
      const [fvx, fvy] = project(od.fovea_center[0], od.fovea_center[1], sw, sh, flipped);
      markers = {
        odx, ody, fvx, fvy,
        odR: Math.max((od.od_radius || 0) * scale, 4),
        fvR: Math.max((od.fovea_radius || 0) * scale, 3),
      };
    }
    maskSrc = data ? `data:image/png;base64,${data.fov_mask_png_b64}` : null;
  }

  // Base image the mask + markers are aligned to. For GT it is the displayed
  // sample (markups live in its frame). For the detector path it is the
  // analysis-space RGB (`fov_base_png_b64`) so the analysis-space mask/markers
  // coincide; fall back to the raw upload only if the backend omitted it.
  const baseSrc = gt
    ? src
    : (data && data.fov_base_png_b64 ? `data:image/png;base64,${data.fov_base_png_b64}` : src);

  const stripSrc = data ? `data:image/png;base64,${data.preview_png_b64}` : null;
  const od = !gt && data ? (data.od_fovea || {}) : {};

  return (
    <div style={{ marginTop: 8 }}>
      {/* Preview with OD/fovea overlay (or FOV mask) */}
      <div style={{ position: 'relative', width: BOX, height: BOX, background: '#000', borderRadius: 8, overflow: 'hidden' }}>
        <img
          src={baseSrc}
          alt={showMask ? 'FOV mask overlay' : 'analysis-space input'}
          style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
        />
        {/* FOV mask as a translucent teal tint, masked to the white (FOV) region.
            Base + mask are both 512²/display-frame and contain-fit identically,
            so the tint lands exactly on the field of view. */}
        {showMask && maskSrc && (
          <div
            aria-label="FOV mask"
            style={{
              position: 'absolute', inset: 0, background: C.teal, opacity: 0.4,
              pointerEvents: 'none',
              WebkitMaskImage: `url(${maskSrc})`, maskImage: `url(${maskSrc})`,
              WebkitMaskMode: 'luminance', maskMode: 'luminance',
              WebkitMaskRepeat: 'no-repeat', maskRepeat: 'no-repeat',
              WebkitMaskPosition: 'center', maskPosition: 'center',
              WebkitMaskSize: 'contain', maskSize: 'contain',
            }}
          />
        )}
        {!showMask && markers && (
          <svg width={BOX} height={BOX} style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
            <line x1={markers.odx} y1={markers.ody} x2={markers.fvx} y2={markers.fvy} stroke={C.amber} strokeWidth="1.5" strokeDasharray="3 2" />
            <circle cx={markers.odx} cy={markers.ody} r={markers.odR} fill="none" stroke={C.teal} strokeWidth="2" />
            <circle cx={markers.fvx} cy={markers.fvy} r={markers.fvR} fill="none" stroke={C.coral} strokeWidth="2" />
          </svg>
        )}
      </div>

      {/* OD–fovea chip */}
      <div style={{ marginTop: 6, fontSize: 10, color: 'var(--color-text-secondary,#666)' }}>
        {gt ? (
          <span>
            <span style={{ color: C.teal, fontWeight: 700 }}>OD</span>
            {' · '}
            <span style={{ color: C.coral, fontWeight: 700 }}>{t('demo.vision.fovea')}</span>
          </span>
        ) : od.confident ? (
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
        {stripSrc && (
          <button onClick={() => setShowStages(v => !v)} style={chipBtn}>
            {showStages ? t('demo.vision.hideStages') : t('demo.vision.showStages')}
          </button>
        )}
        {maskSrc && (
          <button onClick={() => setShowMask(v => !v)} style={chipBtn}>
            {showMask ? t('demo.vision.hideMask') : t('demo.vision.showMask')}
          </button>
        )}
      </div>

      {/* stage strip */}
      {showStages && stripSrc && (
        <div style={{ marginTop: 8, overflowX: 'auto' }}>
          <img src={stripSrc} alt="stages" style={{ height: 120, display: 'block', borderRadius: 6 }} />
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
