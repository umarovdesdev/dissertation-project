// src/tabs/_apiPredict.js — thin client for the FastAPI inference backend.
// Keeps the network details out of Demo.js. The backend contract is defined in
// server/app/schemas.py (PatientPredictionResponse).

const API = process.env.REACT_APP_API_URL || '';
const PW_KEY = 'demo_password';

// Shared-password helpers. The password (when the backend requires one) is held
// in sessionStorage and attached to every protected request. When the backend
// runs with no DEMO_PASSWORD the gate is open and this is simply absent.
export function getPassword() {
  try { return sessionStorage.getItem(PW_KEY) || ''; } catch { return ''; }
}
export function setPassword(pw) {
  try { sessionStorage.setItem(PW_KEY, pw || ''); } catch { /* ignore */ }
}
function appendPassword(fd) {
  const pw = getPassword();
  if (pw) fd.append('password', pw);
  return fd;
}

async function srcToBlob(src) {
  // Works for both data: URLs (uploads) and public asset paths (samples):
  // fetch resolves both, and through CRA's dev server the proxy/CORS apply.
  const r = await fetch(src);
  if (!r.ok) throw new Error(`could not load image (${r.status})`);
  return await r.blob();
}

// eyes: [{ eye: 'left'|'right', src: dataURL|publicPath, name }]
// Returns the raw backend PatientPredictionResponse (snake_case) plus
// client_latency_ms. Demo.js normalizes it into the simulator's shape.
export async function predictPatient(eyes) {
  if (!API) throw new Error('REACT_APP_API_URL is not set');
  const fd = new FormData();
  for (const e of eyes) {
    const blob = await srcToBlob(e.src);
    fd.append(e.eye, blob, e.name || `${e.eye}.png`);
  }
  appendPassword(fd);
  const t0 = performance.now();
  const res = await fetch(`${API}/api/predict`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  const json = await res.json();
  json.client_latency_ms = Math.round(performance.now() - t0);
  return json;
}

// POST /api/visualize → { fov_mask_png_b64, v5_preview_png_b64, od_fovea }.
export async function visualizeImage(src, eye, name) {
  if (!API) throw new Error('REACT_APP_API_URL is not set');
  const fd = new FormData();
  fd.append('image', await srcToBlob(src), name || `${eye}.png`);
  fd.append('eye', eye);
  appendPassword(fd);
  const res = await fetch(`${API}/api/visualize`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return await res.json();
}

// POST /api/gradcam → { gradcam_png_b64, attention_overlay_png_b64, target_class }.
export async function gradcamImage(src, eye, name) {
  if (!API) throw new Error('REACT_APP_API_URL is not set');
  const fd = new FormData();
  fd.append('image', await srcToBlob(src), name || `${eye}.png`);
  fd.append('eye', eye);
  appendPassword(fd);
  const res = await fetch(`${API}/api/gradcam`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return await res.json();
}

// Resolves to the /api/health payload object when the backend is up and the
// checkpoint is loaded, or null otherwise (never throws).
export async function getHealth() {
  if (!API) return null;
  try {
    const r = await fetch(`${API}/api/health`, { method: 'GET' });
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  }
}
