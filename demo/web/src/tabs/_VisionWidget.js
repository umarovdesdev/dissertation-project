// src/tabs/_VisionWidget.js — "what the model sees" per-image widget (TASK-Demo D.2).
// Calls POST /api/visualize and shows: OD/fovea probability discs over the input,
// a confidence chip, an optional probability-heatmap layer, an expandable 6-panel
// preprocessing strip, and a FOV-mask toggle. This is the visual core of
// contributions C-1, SC-E, SC-F and works on arbitrary uploads (visualize is
// preprocessing-only — no trained checkpoint needed), so it lights up as soon as
// the backend is reachable.
//
// When a `gt` payload is supplied (IDRiD localization samples), the markers and
// FOV mask are taken from GROUND-TRUTH instead of the detector. IDRiD markups
// are in the displayed image's own frame, so they project by simple scaling
// (no canonical flip / rotation / crop) and therefore align exactly. GT samples
// render even when the backend is offline; the preprocessing strip still needs
// the backend. GT samples are not editable (they are the reference, not a guess).
//
// For arbitrary uploads (no `gt`) the detector path renders in ANALYSIS space:
// the base image shown is `fov_base_png_b64` (the oriented/cropped 512² RGB),
// not the raw upload, so the FOV mask, OD/fovea markers and probability heatmaps
// — all produced in that same flipped/rotated/cropped frame by the backend —
// overlay exactly (TASK-fix #1, Option A). On the detector path the clinician can
// DRAG the OD and fovea centres to correct them and save the correction back to
// the server (Phase 3 human-in-the-loop feedback).

import { useEffect, useRef, useState } from 'react';
import { C } from '../data';
import { visualizeImage, correctOdFovea } from './_apiPredict';

const BOX = 200; // square preview box (px)
const LOW_CONF = 0.5; // confidence threshold mirroring the detector fallback gate

// Map an (x, y) in analysis space → pixel coords inside the BOX, accounting for
// objectFit:contain letterboxing and the canonical left→right flip.
function project(x, y, sw, sh, flipped) {
  const scale = Math.min(BOX / sw, BOX / sh);
  const offX = (BOX - sw * scale) / 2;
  const offY = (BOX - sh * scale) / 2;
  const dx = flipped ? sw - x : x;
  return [offX + dx * scale, offY + y * scale, scale];
}

// Inverse of `project`: a BOX pixel (e.g. a pointer position) → analysis-space
// (x, y). Used while dragging the OD/fovea markers.
function unproject(px, py, sw, sh, flipped) {
  const scale = Math.min(BOX / sw, BOX / sh);
  const offX = (BOX - sw * scale) / 2;
  const offY = (BOX - sh * scale) / 2;
  let x = (px - offX) / scale;
  const y = (py - offY) / scale;
  if (flipped) x = sw - x;
  return [Math.max(0, Math.min(sw, x)), Math.max(0, Math.min(sh, y))];
}

export default function VisionWidget({ src, eye, name, enabled, gt, t }) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | loading | done | error
  const [showStages, setShowStages] = useState(false);
  const [showMask, setShowMask] = useState(false);
  const [showHeat, setShowHeat] = useState(false);
  // Detector-path correction state (analysis coords): null until a confident
  // detection loads; { od:[x,y], fovea:[x,y] } once editable.
  const [edit, setEdit] = useState(null);
  const [drag, setDrag] = useState(null);          // null | 'od' | 'fovea'
  const [saveStatus, setSaveStatus] = useState('idle'); // idle|saving|saved|error
  const boxRef = useRef(null);

  useEffect(() => {
    // Backend visualize is best-effort: needed for the preprocessing strip and
    // for detector markers on non-GT images. GT samples don't depend on it.
    if (!enabled || !src) { setData(null); setStatus('idle'); return; }
    let alive = true;
    setStatus('loading'); setData(null);
    setShowStages(false); setShowMask(false); setShowHeat(false);
    setEdit(null); setDrag(null); setSaveStatus('idle');
    visualizeImage(src, eye, name)
      .then((d) => { if (alive) { setData(d); setStatus('done'); } })
      .catch(() => { if (alive) { setStatus('error'); } });
    return () => { alive = false; };
  }, [src, eye, name, enabled]);

  // Seed the editable centres from the detector payload once it lands.
  useEffect(() => {
    if (gt || !data) { setEdit(null); return; }
    const od = data.od_fovea || {};
    if (od.confident && od.od_center && od.fovea_center) {
      setEdit({ od: [...od.od_center], fovea: [...od.fovea_center] });
    } else {
      setEdit(null);
    }
    // Note: saveStatus is reset on new-image load by the visualize effect, not
    // here — so the "saved" confirmation survives the data update a save triggers.
  }, [data, gt]);

  // Nothing to show: no backend and no ground truth.
  if (!enabled && !gt) return null;
  // Backend-only image still waiting on / failing the visualize call.
  if (!gt && status === 'loading') {
    return <div style={{ fontSize: 10, color: C.gray, marginTop: 6 }}>{t('demo.vision.loading')}</div>;
  }
  if (!gt && (status === 'error' || !data)) {
    return <div style={{ fontSize: 10, color: C.amberT, marginTop: 6 }}>{t('demo.vision.unavailable')}</div>;
  }

  const od = !gt && data ? (data.od_fovea || {}) : {};
  const editable = !gt && !!edit;       // detector path with a confident detection
  const sw = od.space_w || BOX, sh = od.space_h || BOX, flipped = !!od.flipped;

  // --- Resolve markers + mask from either ground truth or the detector. ---
  let markers = null;   // { odx, ody, odR, fvx, fvy, fvR }
  let maskSrc = null;
  if (gt) {
    const gsw = gt.width || BOX, gsh = gt.height || BOX;
    const [odx, ody, scale] = project(gt.odCenter[0], gt.odCenter[1], gsw, gsh, false);
    const [fvx, fvy] = project(gt.foveaCenter[0], gt.foveaCenter[1], gsw, gsh, false);
    markers = {
      odx, ody, fvx, fvy,
      odR: Math.max((gt.odRadius || 0) * scale, 4),
      fvR: Math.max((gt.odRadius || 0) * scale * 0.4, 3),
    };
    maskSrc = gt.maskSrc;
  } else if (editable || od.confident) {
    // Prefer the (possibly dragged) editable centres over the raw payload.
    const odC = edit ? edit.od : od.od_center;
    const fvC = edit ? edit.fovea : od.fovea_center;
    const [odx, ody, scale] = project(odC[0], odC[1], sw, sh, flipped);
    const [fvx, fvy] = project(fvC[0], fvC[1], sw, sh, flipped);
    markers = {
      odx, ody, fvx, fvy,
      odR: Math.max((od.od_radius || 0) * scale, 4),
      fvR: Math.max((od.fovea_radius || 0) * scale, 3),
    };
    maskSrc = data ? `data:image/png;base64,${data.fov_mask_png_b64}` : null;
  }

  // Base image the mask + markers are aligned to. For GT it is the displayed
  // sample (markups live in its frame). For the detector path it is the
  // analysis-space RGB (`fov_base_png_b64`).
  const baseSrc = gt
    ? src
    : (data && data.fov_base_png_b64 ? `data:image/png;base64,${data.fov_base_png_b64}` : src);

  const stripSrc = data ? `data:image/png;base64,${data.preview_png_b64}` : null;
  const odHeat = od.od_heatmap_png_b64 ? `data:image/png;base64,${od.od_heatmap_png_b64}` : null;
  const fvHeat = od.fovea_heatmap_png_b64 ? `data:image/png;base64,${od.fovea_heatmap_png_b64}` : null;
  const hasHeat = !gt && (odHeat || fvHeat);
  const odConf = od.od_confidence != null ? od.od_confidence : 0;
  const fvConf = od.fovea_confidence != null ? od.fovea_confidence : 0;
  const lowConf = !gt && od.confident && (odConf < LOW_CONF || fvConf < LOW_CONF);
  // Disc fill opacity tracks confidence so a diffuse/uncertain detection looks
  // visibly fainter than a sharp one.
  const odFill = Math.max(0.12, Math.min(0.4, odConf * 0.4));
  const fvFill = Math.max(0.12, Math.min(0.4, fvConf * 0.4));

  // --- Drag handling (detector path only). ---
  function boxXY(e) {
    const r = boxRef.current.getBoundingClientRect();
    return [e.clientX - r.left, e.clientY - r.top];
  }
  function onPointerDownMarker(which) {
    return (e) => {
      if (!editable) return;
      e.preventDefault();
      setDrag(which);
      setSaveStatus('idle');
    };
  }
  function onPointerMove(e) {
    if (!drag || !editable) return;
    const [px, py] = boxXY(e);
    const [ax, ay] = unproject(px, py, sw, sh, flipped);
    setEdit((prev) => ({ ...prev, [drag]: [ax, ay] }));
  }
  function onPointerUp() { if (drag) setDrag(null); }

  function dirty() {
    if (!editable) return false;
    const o = od.od_center || [0, 0], f = od.fovea_center || [0, 0];
    return (
      Math.abs(edit.od[0] - o[0]) > 0.5 || Math.abs(edit.od[1] - o[1]) > 0.5 ||
      Math.abs(edit.fovea[0] - f[0]) > 0.5 || Math.abs(edit.fovea[1] - f[1]) > 0.5
    );
  }
  async function saveCorrection() {
    if (!editable) return;
    setSaveStatus('saving');
    try {
      const resp = await correctOdFovea(src, eye, name, edit.od, edit.fovea, {
        od: odConf, fovea: fvConf,
      });
      // Re-render with the server's recomputed overlay (angle/radii updated).
      setData((prev) => ({ ...prev, od_fovea: resp.od_fovea }));
      setEdit({ od: [...resp.od_fovea.od_center], fovea: [...resp.od_fovea.fovea_center] });
      setSaveStatus('saved');
    } catch {
      setSaveStatus('error');
    }
  }

  return (
    <div style={{ marginTop: 8 }}>
      {/* Preview with OD/fovea overlay (or FOV mask / heatmap) */}
      <div
        ref={boxRef}
        style={{ position: 'relative', width: BOX, height: BOX, background: '#000', borderRadius: 8, overflow: 'hidden', touchAction: 'none' }}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerLeave={onPointerUp}
      >
        <img
          src={baseSrc}
          alt={showMask ? 'FOV mask overlay' : 'analysis-space input'}
          style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
        />
        {/* Probability heatmap layer (detector path). RGBA PNGs are already
            analysis-aligned and carry their own alpha, so they overlay directly. */}
        {!showMask && showHeat && odHeat && (
          <img src={odHeat} alt="OD probability heatmap" style={heatLayer} />
        )}
        {!showMask && showHeat && fvHeat && (
          <img src={fvHeat} alt="fovea probability heatmap" style={heatLayer} />
        )}
        {/* FOV mask as a translucent teal tint, masked to the white (FOV) region. */}
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
            {/* Probability discs: filled (opacity ∝ confidence) + outline. */}
            <circle cx={markers.odx} cy={markers.ody} r={markers.odR} fill={C.teal} fillOpacity={gt ? 0 : odFill} stroke={C.teal} strokeWidth="2" />
            <circle cx={markers.fvx} cy={markers.fvy} r={markers.fvR} fill={C.coral} fillOpacity={gt ? 0 : fvFill} stroke={C.coral} strokeWidth="2" />
            {/* Draggable handles (detector path only). */}
            {editable && (
              <g>
                <circle cx={markers.odx} cy={markers.ody} r={9} fill={C.teal} fillOpacity={drag === 'od' ? 0.9 : 0.6}
                  stroke="#fff" strokeWidth="2" style={{ cursor: 'grab', pointerEvents: 'all' }}
                  onPointerDown={onPointerDownMarker('od')} />
                <circle cx={markers.fvx} cy={markers.fvy} r={9} fill={C.coral} fillOpacity={drag === 'fovea' ? 0.9 : 0.6}
                  stroke="#fff" strokeWidth="2" style={{ cursor: 'grab', pointerEvents: 'all' }}
                  onPointerDown={onPointerDownMarker('fovea')} />
              </g>
            )}
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
            {' '}<span style={{ color: C.gray }}>{(odConf * 100).toFixed(0)}%</span>
            {' · '}
            <span style={{ color: C.coral, fontWeight: 700 }}>{t('demo.vision.fovea')}</span>
            {' '}<span style={{ color: C.gray }}>{(fvConf * 100).toFixed(0)}%</span>
            {' · '}{t('demo.vision.angle')}: <strong>{(od.angle_deg).toFixed(1)}°</strong>
            {' · σ: '}<strong>{(od.rotation_sigma_deg).toFixed(1)}°</strong>
            {lowConf
              ? <span style={{ color: C.amberT }}>{' · ⚠ '}{t('demo.vision.verify')}</span>
              : <span style={{ color: C.greenT }}>{' · ✓ '}{t('demo.vision.confident')}</span>}
          </span>
        ) : (
          <span style={{ color: C.amberT }}>⚠ {t('demo.vision.lowConfidence')}</span>
        )}
      </div>

      {/* Edit hint + Save (detector path with a confident detection). */}
      {editable && (
        <div style={{ marginTop: 5, fontSize: 10, color: 'var(--color-text-secondary,#666)' }}>
          <span style={{ color: C.gray }}>{t('demo.vision.dragHint')}</span>
          <div style={{ display: 'flex', gap: 6, marginTop: 4, alignItems: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={saveCorrection}
              disabled={!dirty() || saveStatus === 'saving'}
              style={{
                ...chipBtn,
                cursor: (!dirty() || saveStatus === 'saving') ? 'not-allowed' : 'pointer',
                background: dirty() ? C.tealBg : 'transparent',
                color: dirty() ? C.teal : 'var(--color-text-secondary,#999)',
                borderColor: dirty() ? C.teal : 'var(--color-border-secondary,#ccc)',
              }}
            >
              {saveStatus === 'saving' ? t('demo.vision.saving') : t('demo.vision.saveCorrection')}
            </button>
            {saveStatus === 'saved' && <span style={{ color: C.greenT }}>✓ {t('demo.vision.saved')}</span>}
            {saveStatus === 'error' && <span style={{ color: C.red }}>{t('demo.vision.saveError')}</span>}
          </div>
        </div>
      )}

      {/* Toggles */}
      <div style={{ display: 'flex', gap: 6, marginTop: 6, flexWrap: 'wrap' }}>
        {stripSrc && (
          <button onClick={() => setShowStages(v => !v)} style={chipBtn}>
            {showStages ? t('demo.vision.hideStages') : t('demo.vision.showStages')}
          </button>
        )}
        {hasHeat && (
          <button onClick={() => { setShowHeat(v => !v); if (!showHeat) setShowMask(false); }} style={chipBtn}>
            {showHeat ? t('demo.vision.hideHeat') : t('demo.vision.showHeat')}
          </button>
        )}
        {maskSrc && (
          <button onClick={() => { setShowMask(v => !v); if (!showMask) setShowHeat(false); }} style={chipBtn}>
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

const heatLayer = {
  position: 'absolute', inset: 0, width: '100%', height: '100%',
  objectFit: 'contain', pointerEvents: 'none', opacity: 0.85,
};
