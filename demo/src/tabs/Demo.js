// src/tabs/Demo.js — Live inference demo page.
// Lets the user supply up to two fundus images (left + right eye) of one
// patient, runs a simulated Config-D-style prediction in the browser, and lets
// the user confirm or reject the result. Confirmed / corrected cases are
// appended to a local relabeling buffer that can be exported as JSONL for
// further training.

import { useMemo, useRef, useState } from 'react';
import { C, CONFIGS } from '../data';
import { Sec, Note } from '../components';
import { useLang } from '../i18n';

// ---------------------------------------------------------------------------
// Sample pool — one or two images from each DR grade in public/datasets.
// `path` is relative to PUBLIC_URL.
// ---------------------------------------------------------------------------
const SAMPLE_POOL = [
  { id: 'dr0a', grade: 0, left: 'datasets/eyepacs/samples/dr0/41832_left.jpeg', right: 'datasets/eyepacs/samples/dr0/36215_right.jpeg' },
  { id: 'dr0b', grade: 0, left: 'datasets/eyepacs/samples/dr0/6287_left.jpeg',  right: 'datasets/eyepacs/samples/dr0/1356_right.jpeg'  },
  { id: 'dr1',  grade: 1, left: 'datasets/eyepacs/samples/dr1/15835_left.jpeg', right: 'datasets/eyepacs/samples/dr1/17348_right.jpeg' },
  { id: 'dr2',  grade: 2, left: 'datasets/eyepacs/samples/dr2/40249_left.jpeg', right: 'datasets/eyepacs/samples/dr2/5795_right.jpeg'  },
  { id: 'dr3',  grade: 3, left: 'datasets/eyepacs/samples/dr3/1420_left.jpeg',  right: 'datasets/eyepacs/samples/dr3/22502_right.jpeg' },
  { id: 'dr4',  grade: 4, left: 'datasets/eyepacs/samples/dr4/33283_left.jpeg', right: 'datasets/eyepacs/samples/dr4/14844_right.jpeg' },
];

// ---------------------------------------------------------------------------
// Simulated inference.
// Strategy: derive a deterministic pseudo-random seed from the image source
// (file name or sample URL). Match Config D's accuracy profile — pick the
// "true" class for samples (from /drN/ in the URL), or a uniform random class
// for arbitrary uploads. Add per-class softmax-like probabilities.
// ---------------------------------------------------------------------------
function hashStr(s) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h >>> 0;
}
function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6D2B79F5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function gradeFromUrl(url) {
  const m = url && url.match(/\/dr([0-4])\//i);
  return m ? parseInt(m[1], 10) : null;
}

// Per-eye prediction. Mirrors Config-D: ~78% correct, ~17% off-by-one,
// ~5% off-by-two. Returns { pred, probs[5], confidence, trueGrade }.
function predictEye(src, key) {
  const seed = hashStr((src || '') + '|' + (key || ''));
  const rand = rng(seed);
  const truth = gradeFromUrl(src);
  // Use truth when available (sample image), else pick a class biased toward
  // lower grades (real-world prevalence-ish).
  const reference = truth !== null
    ? truth
    : [0, 0, 1, 2, 3, 4][Math.floor(rand() * 6)];

  // Decide outcome based on Config D weighted F1 (0.78).
  const r = rand();
  let pred;
  if (r < 0.78)       pred = reference;
  else if (r < 0.95)  pred = Math.max(0, Math.min(4, reference + (rand() < 0.5 ? -1 : 1)));
  else                pred = Math.max(0, Math.min(4, reference + (rand() < 0.5 ? -2 : 2)));

  // Build softmax-ish probabilities centered on `pred`.
  const raw = [0, 1, 2, 3, 4].map(c => {
    const dist = Math.abs(c - pred);
    return Math.exp(-1.4 * dist + (rand() - 0.5) * 0.4);
  });
  const sum = raw.reduce((a, b) => a + b, 0);
  const probs = raw.map(v => v / sum);
  return {
    pred,
    probs,
    confidence: probs[pred],
    trueGrade: truth,
    latencyMs: Math.round(180 + rand() * 220),
  };
}

// Patient-level result = worst eye (clinical convention for screening).
function patientPrediction(eyes) {
  // eyes: array of { eye, src } excluding empties
  const perEye = eyes.map(e => ({ ...e, result: predictEye(e.src, e.eye) }));
  if (perEye.length === 0) return null;
  const worst = perEye.reduce((a, b) => (b.result.pred > a.result.pred ? b : a));
  const probs = [0, 1, 2, 3, 4].map(c =>
    perEye.reduce((acc, p) => Math.max(acc, p.result.probs[c]), 0)
  );
  const sum = probs.reduce((a, b) => a + b, 0);
  const norm = probs.map(p => p / sum);
  return {
    perEye,
    pred: worst.result.pred,
    confidence: norm[worst.result.pred],
    probs: norm,
    latencyMs: Math.max(...perEye.map(p => p.result.latencyMs)),
  };
}

// ---------------------------------------------------------------------------
// UI sub-components
// ---------------------------------------------------------------------------
function EyeSlot({ label, eye, image, onPick, onClear, t }) {
  const inputRef = useRef(null);
  const onChange = (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => onPick({ src: ev.target.result, name: file.name, fromUpload: true });
    reader.readAsDataURL(file);
  };
  const onDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => onPick({ src: ev.target.result, name: file.name, fromUpload: true });
    reader.readAsDataURL(file);
  };
  return (
    <div style={{ flex: 1, minWidth: 220 }}>
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
        {label}
      </div>
      <div
        onClick={() => inputRef.current && inputRef.current.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        style={{
          aspectRatio: '1 / 1', width: '100%',
          border: `1px dashed ${image ? C.teal : 'var(--color-border-secondary,#ccc)'}`,
          borderRadius: 10, background: image ? '#000' : 'var(--color-background-secondary,#f7f7f5)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          cursor: 'pointer', overflow: 'hidden', position: 'relative',
        }}
      >
        {image ? (
          <img src={image.src} alt={label} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        ) : (
          <div style={{ textAlign: 'center', color: 'var(--color-text-secondary,#888)', padding: 12 }}>
            <div style={{ fontSize: 11, fontWeight: 600 }}>{t('demo.dropHere')}</div>
            <div style={{ fontSize: 9, marginTop: 4 }}>{t('demo.formats')}</div>
          </div>
        )}
        <input ref={inputRef} type="file" accept="image/*" onChange={onChange} style={{ display: 'none' }} />
      </div>
      {image && (
        <button onClick={onClear} style={{
          marginTop: 6, fontSize: 10, padding: '3px 8px', background: 'transparent',
          color: C.red, border: `1px solid ${C.red}`, borderRadius: 4, cursor: 'pointer',
        }}>
          {t('demo.clear')}
        </button>
      )}
    </div>
  );
}

function ProbabilityBar({ idx, p, isPred, t }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
      <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', minWidth: 36, fontWeight: isPred ? 700 : 400 }}>
        {t('demo.gradeShort.' + idx)}
      </div>
      <div style={{ flex: 1, height: 16, background: 'var(--color-background-secondary,#eeede9)', borderRadius: 3, position: 'relative', overflow: 'hidden' }}>
        <div style={{ width: `${p * 100}%`, height: '100%', background: isPred ? C.teal : C.gray, opacity: isPred ? 0.85 : 0.45 }} />
        <span style={{ position: 'absolute', right: 5, top: '50%', transform: 'translateY(-50%)', fontSize: 9, fontWeight: isPred ? 700 : 500, color: 'var(--color-text-primary,#333)' }}>
          {(p * 100).toFixed(1)}%
        </span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------
export default function Demo() {
  const { t } = useLang();
  const [leftImg, setLeftImg] = useState(null);
  const [rightImg, setRightImg] = useState(null);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [feedbackMode, setFeedbackMode] = useState(null); // 'confirm' | 'reject' | null
  const [correctedGrade, setCorrectedGrade] = useState(0);
  const [toast, setToast] = useState('');
  const [history, setHistory] = useState([]);

  const D = CONFIGS.D;

  const eyes = useMemo(() => {
    const list = [];
    if (leftImg)  list.push({ eye: 'left',  src: leftImg.src,  name: leftImg.name  || 'left'  });
    if (rightImg) list.push({ eye: 'right', src: rightImg.src, name: rightImg.name || 'right' });
    return list;
  }, [leftImg, rightImg]);

  const reset = (keepHistory = true) => {
    setLeftImg(null);
    setRightImg(null);
    setResult(null);
    setFeedbackMode(null);
    setCorrectedGrade(0);
    if (!keepHistory) setHistory([]);
  };

  const handleRun = () => {
    if (eyes.length === 0) return;
    setRunning(true);
    setResult(null);
    setFeedbackMode(null);
    // Simulate latency so the UI feels realistic.
    const minLatency = 700;
    setTimeout(() => {
      const r = patientPrediction(eyes);
      setResult(r);
      setRunning(false);
    }, minLatency);
  };

  const useSample = (sample) => {
    setLeftImg({  src: process.env.PUBLIC_URL + '/' + sample.left,  name: sample.left,  fromUpload: false });
    setRightImg({ src: process.env.PUBLIC_URL + '/' + sample.right, name: sample.right, fromUpload: false });
    setResult(null);
    setFeedbackMode(null);
  };

  const submitFeedback = (verdict) => {
    if (!result) return;
    const entry = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      images: eyes.map(e => ({ eye: e.eye, source: e.name })),
      predicted: result.pred,
      confidence: Number(result.confidence.toFixed(4)),
      probs: result.probs.map(p => Number(p.toFixed(4))),
      verdict,
      corrected_grade: verdict === 'confirmed' ? result.pred : correctedGrade,
      latency_ms: result.latencyMs,
      model: 'config-D (pipeline + EfficientNet-B3)',
    };
    setHistory(h => [entry, ...h]);
    setToast(t('demo.thanks'));
    setTimeout(() => setToast(''), 2500);
    setFeedbackMode(null);
  };

  const exportJsonl = () => {
    if (history.length === 0) return;
    const jsonl = history.map(h => JSON.stringify(h)).join('\n');
    const blob = new Blob([jsonl], { type: 'application/x-ndjson' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dr-relabel-${new Date().toISOString().replace(/[:.]/g, '-')}.jsonl`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, color: 'var(--color-text-primary,#222)', margin: '0 0 4px 0' }}>
          {t('demo.title')}
        </h2>
        <p style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)', margin: '0 0 8px 0', lineHeight: 1.55 }}>
          {t('demo.subtitle')}
        </p>
        <div style={{ fontSize: 10, color: C.amberT, background: C.amberBg, padding: '6px 10px', borderRadius: 6, display: 'inline-block' }}>
          ⚠ {t('demo.disclaimer')}
        </div>
      </div>

      {/* Upload section */}
      <Sec title={t('demo.uploadSection')}>
        <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
          <EyeSlot
            label={t('demo.leftEye')}
            eye="left"
            image={leftImg}
            onPick={setLeftImg}
            onClear={() => { setLeftImg(null); setResult(null); setFeedbackMode(null); }}
            t={t}
          />
          <EyeSlot
            label={t('demo.rightEye')}
            eye="right"
            image={rightImg}
            onPick={setRightImg}
            onClear={() => { setRightImg(null); setResult(null); setFeedbackMode(null); }}
            t={t}
          />
        </div>

        <div style={{ marginTop: 14 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
            {t('demo.useSample')}
          </div>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {SAMPLE_POOL.map(s => (
              <button key={s.id} onClick={() => useSample(s)} style={{
                padding: '4px 10px', fontSize: 10, fontWeight: 600,
                background: C.tealBg, color: C.tealT,
                border: `1px solid ${C.teal}`, borderRadius: 4, cursor: 'pointer',
              }}>
                {t('demo.gradeShort.' + s.grade)} pair
              </button>
            ))}
          </div>
          <Note>{t('demo.sampleHint')}</Note>
        </div>
      </Sec>

      {/* Run section */}
      <Sec title={t('demo.runSection')}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
          <button
            onClick={handleRun}
            disabled={running || eyes.length === 0}
            style={{
              padding: '8px 18px', fontSize: 12, fontWeight: 600,
              background: (running || eyes.length === 0) ? C.gray : C.teal,
              color: 'white', border: 'none', borderRadius: 6,
              cursor: (running || eyes.length === 0) ? 'not-allowed' : 'pointer',
            }}
          >
            {running ? t('demo.running') : t('demo.runButton')}
          </button>
          {eyes.length === 0 && (
            <span style={{ fontSize: 11, color: C.red }}>{t('demo.needAtLeastOne')}</span>
          )}
          {eyes.length > 0 && !running && (
            <span style={{ fontSize: 11, color: 'var(--color-text-secondary,#666)' }}>
              {eyes.length} {eyes.length === 1 ? 'image' : 'images'} · {t('demo.modelVersion')}: Config D
            </span>
          )}
        </div>
      </Sec>

      {/* Result section */}
      {result && (
        <Sec title={t('demo.resultSection')}>
          <div style={{
            display: 'flex', gap: 12, flexWrap: 'wrap',
            padding: 14, borderRadius: 10,
            background: result.pred >= 2 ? C.coralBg : C.tealBg,
            border: `1px solid ${result.pred >= 2 ? C.coral : C.teal}`,
          }}>
            <div style={{ flex: 1, minWidth: 180 }}>
              <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', color: result.pred >= 2 ? C.coralT : C.tealT, opacity: 0.8 }}>
                {t('demo.predictedGrade')}
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, color: result.pred >= 2 ? C.coralT : C.tealT, marginTop: 2 }}>
                {t('demo.grade.' + result.pred)}
              </div>
              <div style={{ fontSize: 11, color: 'var(--color-text-secondary,#555)', marginTop: 6 }}>
                {t('demo.confidence')}: <strong>{(result.confidence * 100).toFixed(1)}%</strong>
                {' · '}
                {t('demo.referable')}: <strong>{result.pred >= 2 ? t('demo.yes') : t('demo.no')}</strong>
                {' · '}
                {t('demo.latency')}: <strong>{result.latencyMs} ms</strong>
              </div>
            </div>
            <div style={{ flex: 1, minWidth: 220 }}>
              <div style={{ fontSize: 10, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 4 }}>
                {t('demo.classProbs')}
              </div>
              {result.probs.map((p, i) => (
                <ProbabilityBar key={i} idx={i} p={p} isPred={i === result.pred} t={t} />
              ))}
            </div>
          </div>

          {/* Per-eye breakdown */}
          {result.perEye.length > 1 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
                {t('demo.perEye')}
              </div>
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                {result.perEye.map((eye, i) => (
                  <div key={i} style={{
                    flex: 1, minWidth: 200, padding: '8px 12px',
                    background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 8,
                    borderLeft: `3px solid ${eye.result.pred >= 2 ? C.coral : C.teal}`,
                  }}>
                    <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', fontWeight: 600 }}>
                      {t(eye.eye === 'left' ? 'demo.leftEye' : 'demo.rightEye')}
                    </div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-text-primary,#222)' }}>
                      {t('demo.grade.' + eye.result.pred)}
                    </div>
                    <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', marginTop: 2 }}>
                      {(eye.result.confidence * 100).toFixed(1)}% · {eye.result.latencyMs} ms
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </Sec>
      )}

      {/* Feedback section */}
      {result && (
        <Sec title={t('demo.feedbackSection')} note={t('demo.feedbackHint')}>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'center' }}>
            <button
              onClick={() => { setFeedbackMode('confirm'); submitFeedback('confirmed'); }}
              style={{
                padding: '8px 16px', fontSize: 12, fontWeight: 600,
                background: C.green, color: 'white', border: 'none',
                borderRadius: 6, cursor: 'pointer',
              }}
            >
              ✓ {t('demo.confirm')}
            </button>
            <button
              onClick={() => setFeedbackMode('reject')}
              style={{
                padding: '8px 16px', fontSize: 12, fontWeight: 600,
                background: 'white', color: C.red,
                border: `1px solid ${C.red}`, borderRadius: 6, cursor: 'pointer',
              }}
            >
              ✕ {t('demo.reject')}
            </button>
          </div>
          {feedbackMode === 'reject' && (
            <div style={{
              marginTop: 12, padding: 12, borderRadius: 8,
              background: C.redBg, border: `1px solid ${C.red}`,
              display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap',
            }}>
              <label style={{ fontSize: 11, fontWeight: 600, color: C.redT }}>
                {t('demo.correctGrade')}:
              </label>
              <select
                value={correctedGrade}
                onChange={(e) => setCorrectedGrade(parseInt(e.target.value, 10))}
                style={{ padding: '4px 8px', fontSize: 11, border: '1px solid var(--color-border-secondary,#ccc)', borderRadius: 4 }}
              >
                {[0, 1, 2, 3, 4].map(g => (
                  <option key={g} value={g}>{t('demo.grade.' + g)}</option>
                ))}
              </select>
              <button
                onClick={() => submitFeedback('rejected')}
                style={{
                  padding: '6px 14px', fontSize: 11, fontWeight: 600,
                  background: C.red, color: 'white', border: 'none',
                  borderRadius: 4, cursor: 'pointer',
                }}
              >
                {t('demo.submit')}
              </button>
            </div>
          )}
          {toast && (
            <div style={{
              marginTop: 10, padding: '8px 12px', borderRadius: 6,
              background: C.greenBg, color: C.greenT, fontSize: 11, fontWeight: 600,
            }}>
              ✓ {toast}
            </div>
          )}
        </Sec>
      )}

      {/* History / relabeling buffer */}
      <Sec title={`${t('demo.historyTitle')} (${history.length})`}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 10 }}>
          <button
            onClick={exportJsonl}
            disabled={history.length === 0}
            style={{
              padding: '6px 12px', fontSize: 11, fontWeight: 600,
              background: history.length === 0 ? C.gray : C.blue,
              color: 'white', border: 'none', borderRadius: 4,
              cursor: history.length === 0 ? 'not-allowed' : 'pointer',
            }}
          >
            ⬇ {t('demo.export')}
          </button>
          <button
            onClick={() => setHistory([])}
            disabled={history.length === 0}
            style={{
              padding: '6px 12px', fontSize: 11,
              background: 'white', color: history.length === 0 ? C.gray : C.red,
              border: `1px solid ${history.length === 0 ? C.gray : C.red}`,
              borderRadius: 4, cursor: history.length === 0 ? 'not-allowed' : 'pointer',
            }}
          >
            {t('demo.clearAll')}
          </button>
        </div>
        {history.length === 0 ? (
          <Note>{t('demo.historyEmpty')}</Note>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)' }}>
                  <th style={{ padding: '5px 8px', textAlign: 'left', fontWeight: 600 }}>{t('demo.col.time')}</th>
                  <th style={{ padding: '5px 8px', textAlign: 'center', fontWeight: 600 }}>{t('demo.col.images')}</th>
                  <th style={{ padding: '5px 8px', textAlign: 'center', fontWeight: 600 }}>{t('demo.col.predicted')}</th>
                  <th style={{ padding: '5px 8px', textAlign: 'center', fontWeight: 600 }}>{t('demo.col.verdict')}</th>
                  <th style={{ padding: '5px 8px', textAlign: 'center', fontWeight: 600 }}>{t('demo.col.corrected')}</th>
                </tr>
              </thead>
              <tbody>
                {history.map(h => (
                  <tr key={h.id} style={{ borderBottom: '1px solid var(--color-border-tertiary,#eee)' }}>
                    <td style={{ padding: '5px 8px', fontFamily: 'monospace', fontSize: 10, color: 'var(--color-text-secondary,#666)' }}>
                      {new Date(h.timestamp).toLocaleTimeString()}
                    </td>
                    <td style={{ padding: '5px 8px', textAlign: 'center' }}>{h.images.length}</td>
                    <td style={{ padding: '5px 8px', textAlign: 'center', fontWeight: 600 }}>
                      {t('demo.gradeShort.' + h.predicted)} ({(h.confidence * 100).toFixed(0)}%)
                    </td>
                    <td style={{ padding: '5px 8px', textAlign: 'center' }}>
                      <span style={{
                        padding: '2px 6px', borderRadius: 3, fontSize: 10, fontWeight: 600,
                        background: h.verdict === 'confirmed' ? C.greenBg : C.redBg,
                        color: h.verdict === 'confirmed' ? C.greenT : C.redT,
                      }}>
                        {t('demo.verdict.' + h.verdict)}
                      </span>
                    </td>
                    <td style={{ padding: '5px 8px', textAlign: 'center', fontWeight: 600 }}>
                      {t('demo.gradeShort.' + h.corrected_grade)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Sec>

      {/* Footer caveat */}
      <Note>
        Predicted via simulated Config D (Pipeline + EfficientNet-B3).
        Reported reference metrics on held-out EyePACS: F1={D.f1.toFixed(3)}, AUC={D.auc.toFixed(3)}, κ={D.k.toFixed(3)}.
      </Note>

      <div style={{ marginTop: 14 }}>
        <button onClick={() => reset(true)} style={{
          fontSize: 10, padding: '4px 10px', background: 'transparent',
          color: 'var(--color-text-secondary,#666)',
          border: '1px solid var(--color-border-secondary,#ccc)',
          borderRadius: 4, cursor: 'pointer',
        }}>
          ↺ Reset case
        </button>
      </div>
    </div>
  );
}
