// src/tabs/_VisionWidget.js — "what the model sees" per-image widget (TASK-Demo D.2).
// Calls POST /api/visualize and shows: OD/fovea probability discs over the input,
// a confidence chip, an optional probability-heatmap layer, and a step-by-step
// preprocessing-stage view (which includes the FOV mask as its own slide). This
// is the visual core of
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
// For arbitrary uploads (no `gt`) the detector path renders the detection slide
// in the PRE-ROTATION (canonical-flip) frame: the base image is
// `detect_base_png_b64`, and the OD/fovea markers + probability heatmaps — all
// produced by the backend in that same flipped frame — overlay exactly with the
// OD–fovea axis at its true tilt. The detection slide only MARKS the discs; the
// Stage-1 rotation slide is what levels them. On the detector path the clinician
// can DRAG the OD and fovea centres to correct them; saving re-runs the whole
// pipeline server-side so the corrected centres redefine the rotation and every
// downstream stage (Phase 3 human-in-the-loop feedback).

import { useEffect, useRef, useState } from 'react';
import { C } from '../data';
import { visualizeImage, correctOdFovea } from './_apiPredict';

const BOX = 200; // fallback square box size (px) until the live width is measured

// Map an (x, y) in analysis space → pixel coords inside a `box`×`box` square,
// accounting for objectFit:contain letterboxing and the canonical left→right
// flip. `box` is the live, measured side length so markers stay aligned when the
// preview fills the block at any width.
function project(x, y, sw, sh, flipped, box) {
  const scale = Math.min(box / sw, box / sh);
  const offX = (box - sw * scale) / 2;
  const offY = (box - sh * scale) / 2;
  const dx = flipped ? sw - x : x;
  return [offX + dx * scale, offY + y * scale, scale];
}

// Inverse of `project`: a box pixel (e.g. a pointer position) → analysis-space
// (x, y). Used while dragging the OD/fovea markers.
function unproject(px, py, sw, sh, flipped, box) {
  const scale = Math.min(box / sw, box / sh);
  const offX = (box - sw * scale) / 2;
  const offY = (box - sh * scale) / 2;
  let x = (px - offX) / scale;
  const y = (py - offY) / scale;
  if (flipped) x = sw - x;
  return [Math.max(0, Math.min(sw, x)), Math.max(0, Math.min(sh, y))];
}

const LOW_CONF = 0.5; // confidence threshold mirroring the detector fallback gate

export default function VisionWidget({ src, eye, name, enabled, gt, t }) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | loading | done | error
  // Index of the currently shown preprocessing-stage slide (step-by-step view).
  const [stageIdx, setStageIdx] = useState(0);
  const [retryNonce, setRetryNonce] = useState(0); // bump to force a re-fetch
  const [showHeat, setShowHeat] = useState(false);
  // Detector-path correction state (analysis coords): null until a confident
  // detection loads; { od:[x,y], fovea:[x,y] } once editable.
  const [edit, setEdit] = useState(null);
  const [drag, setDrag] = useState(null);          // null | 'od' | 'fovea'
  const [saveStatus, setSaveStatus] = useState('idle'); // idle|saving|saved|error
  // Live side length of the (square) preview box. The box stretches to 100% of
  // the Additional-info block, so its pixel size is measured at runtime and used
  // to keep the SVG overlay + marker projection aligned at any width.
  const [boxSize, setBoxSize] = useState(BOX);
  const boxRef = useRef(null);        // detection box (pointer math; mounted on its slide only)
  const frameRef = useRef(null);      // always-mounted slide frame; measured for boxSize

  // Track the rendered slide width so markers/overlay scale with the block.
  useEffect(() => {
    const el = frameRef.current;
    if (!el || typeof ResizeObserver === 'undefined') return undefined;
    const ro = new ResizeObserver((entries) => {
      for (const e of entries) {
        const w = e.contentRect.width;
        if (w > 0) setBoxSize(w);
      }
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, [status, gt, data]);

  useEffect(() => {
    // Backend visualize is best-effort: needed for the preprocessing strip and
    // for detector markers on non-GT images. GT samples don't depend on it.
    if (!enabled || !src) { setData(null); setStatus('idle'); return; }
    let alive = true;
    let timer = null;
    setStatus('loading'); setData(null);
    setStageIdx(0);
    setShowHeat(false);
    setEdit(null); setDrag(null); setSaveStatus('idle');

    // The visualize call is best-effort and can hit a transient blip (backend
    // mid-restart, momentary network drop). Retry a few times with linear
    // backoff before surfacing "unavailable", so a brief hiccup self-heals
    // instead of pinning the widget to the error state.
    const MAX_ATTEMPTS = 5;
    const attempt = (n) => {
      visualizeImage(src, eye, name)
        .then((d) => { if (alive) { setData(d); setStatus('done'); } })
        .catch(() => {
          if (!alive) return;
          if (n < MAX_ATTEMPTS) {
            timer = setTimeout(() => attempt(n + 1), Math.min(800 * n, 4000));
          } else {
            setStatus('error');
          }
        });
    };
    attempt(1);
    return () => { alive = false; if (timer) clearTimeout(timer); };
  }, [src, eye, name, enabled, retryNonce]);

  // Seed the editable centres from the detector payload once it lands.
  useEffect(() => {
    if (gt || !data) { setEdit(null); return; }
    const od = data.od_fovea || {};
    // Seed editable centres for ANY detection — confident or not — so the
    // clinician can drag-correct a low-confidence best guess. The backend
    // projects real centres for both cases now; only the all-zero sentinel
    // (no detection at all) is skipped.
    const hasCenters =
      Array.isArray(od.od_center) && Array.isArray(od.fovea_center) &&
      !(od.od_center[0] === 0 && od.od_center[1] === 0 &&
        od.fovea_center[0] === 0 && od.fovea_center[1] === 0);
    if (hasCenters) {
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
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
        <span style={{ fontSize: 10, color: C.amberT }}>{t('demo.vision.unavailable')}</span>
        <button onClick={() => setRetryNonce((n) => n + 1)} style={chipBtn}>
          {t('demo.vision.retry')}
        </button>
      </div>
    );
  }

  const od = !gt && data ? (data.od_fovea || {}) : {};
  const editable = !gt && !!edit;       // detector path with any seeded detection
  const sw = od.space_w || BOX, sh = od.space_h || BOX, flipped = !!od.flipped;

  // --- Resolve markers + mask from either ground truth or the detector. ---
  let markers = null;   // { odx, ody, odR, fvx, fvy, fvR }
  if (gt) {
    const gsw = gt.width || BOX, gsh = gt.height || BOX;
    const [odx, ody, scale] = project(gt.odCenter[0], gt.odCenter[1], gsw, gsh, false, boxSize);
    const [fvx, fvy] = project(gt.foveaCenter[0], gt.foveaCenter[1], gsw, gsh, false, boxSize);
    markers = {
      odx, ody, fvx, fvy,
      odR: Math.max((gt.odRadius || 0) * scale, 4),
      fvR: Math.max((gt.odRadius || 0) * scale * 0.4, 3),
    };
  } else if (editable || od.confident) {
    // Prefer the (possibly dragged) editable centres over the raw payload.
    const odC = edit ? edit.od : od.od_center;
    const fvC = edit ? edit.fovea : od.fovea_center;
    const [odx, ody, scale] = project(odC[0], odC[1], sw, sh, flipped, boxSize);
    const [fvx, fvy] = project(fvC[0], fvC[1], sw, sh, flipped, boxSize);
    markers = {
      odx, ody, fvx, fvy,
      odR: Math.max((od.od_radius || 0) * scale, 4),
      fvR: Math.max((od.fovea_radius || 0) * scale, 3),
    };
  }

  // Per-stage slides for the step-by-step view (one image per preprocessing
  // stage). Available for any image once the backend has returned them (GT
  // samples included, when the backend is reachable).
  const stages = data && Array.isArray(data.stages) ? data.stages : [];

  // Base image the OD/fovea markers are aligned to. For GT it is the displayed
  // sample (markups live in its frame). For the detector path it is the image
  // AFTER Canonical flip (the `canonical_flip` stage) — the detector runs in
  // that frame, so for a left eye the detection must show the flipped image, not
  // the raw upload. Falls back to `detect_base_png_b64` (identical), then to the
  // raw upload only if no stages are available at all.
  const flipStage = stages.find((s) => s.key === 'canonical_flip');
  const baseSrc = gt
    ? src
    : (flipStage
        ? `data:image/png;base64,${flipStage.png_b64}`
        : (data && data.detect_base_png_b64
            ? `data:image/png;base64,${data.detect_base_png_b64}`
            : src));
  // Unified step-by-step slides: the interactive OD/fovea detection view is
  // inserted as its own slide immediately BEFORE the Stage-1 rotation slide
  // (detection is what drives the rotation). Falls back to the front when the
  // rotation stage isn't present (e.g. backend offline on a GT sample).
  const slides = stages.map((s) => ({ ...s, kind: 'image' }));
  if (markers) {
    const detect = { key: '__detection', kind: 'detection', caption: t('demo.vision.detectionSlide') };
    const rotIdx = slides.findIndex((s) => s.key === 'od_fovea_rotation');
    slides.splice(rotIdx >= 0 ? rotIdx : 0, 0, detect);
  }
  const stageI = Math.min(stageIdx, Math.max(0, slides.length - 1));
  const curSlide = slides[stageI];
  // The confidence chip, drag/Save controls, and heatmap toggle belong to the
  // detection step, so they only show while the detection slide is on screen.
  const onDetection = !!curSlide && curSlide.kind === 'detection';
  // The R/G/B/FOV channel decomposition of the CURRENT stage, shown at the very
  // bottom — stepping through stages reveals how each method reshapes the
  // channels. Empty for the detection slide and the standalone FOV-mask slide.
  const stageChannels = curSlide && Array.isArray(curSlide.channels) ? curSlide.channels : [];
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
    const [ax, ay] = unproject(px, py, sw, sh, flipped, boxSize);
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
      // The correction redefines the rotation, so the server returns a FULL
      // re-run: swap in the recomputed overlay AND every downstream stage so the
      // whole step-by-step view (rotation, crop, flat-field, CLAHE, FOV mask)
      // reflects the corrected geometry.
      setData((prev) => ({
        ...prev,
        od_fovea: resp.od_fovea,
        stages: resp.stages && resp.stages.length ? resp.stages : prev.stages,
        detect_base_png_b64: resp.detect_base_png_b64 || prev.detect_base_png_b64,
        fov_mask_png_b64: resp.fov_mask_png_b64 || prev.fov_mask_png_b64,
        fov_base_png_b64: resp.fov_base_png_b64 || prev.fov_base_png_b64,
      }));
      setEdit({ od: [...resp.od_fovea.od_center], fovea: [...resp.od_fovea.fovea_center] });
      setSaveStatus('saved');
    } catch {
      setSaveStatus('error');
    }
  }

  // The interactive OD/fovea detection box, rendered as the detection slide.
  const detectionBox = (
    <div
      ref={boxRef}
      style={{ position: 'relative', width: '100%', aspectRatio: '1 / 1', background: '#000', borderRadius: 6, overflow: 'hidden', touchAction: 'none' }}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerLeave={onPointerUp}
    >
      <img
        src={baseSrc}
        alt="analysis-space input"
        style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
      />
      {/* Probability heatmap layer (detector path). RGBA PNGs are already
          analysis-aligned and carry their own alpha, so they overlay directly. */}
      {showHeat && odHeat && (
        <img src={odHeat} alt="OD probability heatmap" style={heatLayer} />
      )}
      {showHeat && fvHeat && (
        <img src={fvHeat} alt="fovea probability heatmap" style={heatLayer} />
      )}
      {markers && (
        <svg width={boxSize} height={boxSize} style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
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
  );

  return (
    <div style={{ marginTop: 8 }}>
      {/* Step-by-step view: the OD/fovea detection preview is one interactive
          slide (inserted just before the rotation stage); the rest are the
          per-stage preprocessing images. Detection/confidence controls sit
          BELOW the slider. */}
      {slides.length > 0 && (
        <div>
          <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
            {t('demo.vision.stagesHeading')}
          </div>
          {/* Navigation */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6, width: '100%' }}>
            <button
              onClick={() => setStageIdx(i => Math.max(0, i - 1))}
              disabled={stageI === 0}
              style={{ ...chipBtn, opacity: stageI === 0 ? 0.3 : 1, cursor: stageI === 0 ? 'default' : 'pointer' }}
            >
              ←
            </button>
            <span style={{ fontSize: 10, color: C.gray }}>{stageI + 1} / {slides.length}</span>
            <button
              onClick={() => setStageIdx(i => Math.min(slides.length - 1, i + 1))}
              disabled={stageI === slides.length - 1}
              style={{ ...chipBtn, opacity: stageI === slides.length - 1 ? 0.3 : 1, cursor: stageI === slides.length - 1 ? 'default' : 'pointer' }}
            >
              →
            </button>
          </div>
          {/* Progress segments — click to jump to a slide. */}
          <div style={{ display: 'flex', gap: 3, marginBottom: 8, width: '100%' }}>
            {slides.map((s, i) => (
              <button
                key={s.key}
                onClick={() => setStageIdx(i)}
                title={s.caption}
                style={{
                  flex: 1, height: 5, border: 'none', borderRadius: 3, cursor: 'pointer',
                  background: i <= stageI ? C.teal : 'var(--color-background-secondary,#e5e5e3)',
                  opacity: i === stageI ? 1 : 0.55,
                }}
              />
            ))}
          </div>
          {/* Current slide: caption + frame (detection box or stage image). */}
          <div style={{ fontSize: 11, fontWeight: 600, marginBottom: 4 }}>{curSlide.caption}</div>
          <div ref={frameRef} style={{ width: '100%' }}>
            {curSlide.kind === 'detection' ? detectionBox : (
              <img
                src={`data:image/png;base64,${curSlide.png_b64}`}
                alt={curSlide.caption}
                style={{ width: '100%', aspectRatio: '1 / 1', objectFit: 'contain', display: 'block', borderRadius: 6, background: '#000' }}
              />
            )}
          </div>
        </div>
      )}

      {/* OD–fovea chip — only on the detection slide */}
      {onDetection && (
      <div style={{ marginTop: 12, fontSize: 10, color: 'var(--color-text-secondary,#666)' }}>
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
          <span style={{ color: C.amberT }}>
            ⚠ {t('demo.vision.lowConfidence')}
            {' · '}<span style={{ color: C.teal, fontWeight: 700 }}>OD</span>
            {' '}<span style={{ color: C.gray }}>{(odConf * 100).toFixed(0)}%</span>
            {' · '}<span style={{ color: C.coral, fontWeight: 700 }}>{t('demo.vision.fovea')}</span>
            {' '}<span style={{ color: C.gray }}>{(fvConf * 100).toFixed(0)}%</span>
            {editable && <span style={{ color: C.gray }}>{' · '}{t('demo.vision.bestGuess')}</span>}
          </span>
        )}
      </div>
      )}

      {/* Edit hint + Save (detector path with any seeded detection, incl. low
          confidence — the clinician corrects the best guess) — detection slide only. */}
      {onDetection && editable && (
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

      {/* Heatmap toggle — detection slide only (it overlays that slide) */}
      {onDetection && hasHeat && (
        <div style={{ display: 'flex', gap: 6, marginTop: 6, flexWrap: 'wrap' }}>
          <button onClick={() => setShowHeat(v => !v)} style={chipBtn}>
            {showHeat ? t('demo.vision.hideHeat') : t('demo.vision.showHeat')}
          </button>
        </div>
      )}

      {/* Per-stage channel decomposition (R/G/B/FOV) — the "how preprocessing
          helps" panel: it tracks the current stage so stepping through the
          slider shows each method's effect on the individual channels. The final
          CLAHE stage's channels are the CNN input tensor itself. */}
      {stageChannels.length > 0 && (
        <div style={{ marginTop: 14 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
            {t('demo.vision.stageChannels')}
            {curSlide.key === 'clahe' && (
              <span style={{ fontWeight: 400, color: C.gray }}>{' '}· {t('demo.vision.cnnInputNote')}</span>
            )}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 6, width: '100%' }}>
            {stageChannels.map((ch) => (
              <div key={ch.key}>
                <img
                  src={`data:image/png;base64,${ch.png_b64}`}
                  alt={ch.caption}
                  style={{ width: '100%', aspectRatio: '1 / 1', objectFit: 'contain', display: 'block', borderRadius: 4, background: '#000' }}
                />
                <div style={{ fontSize: 9, color: C.gray, marginTop: 3, textAlign: 'center' }}>{ch.caption}</div>
              </div>
            ))}
          </div>
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
