// src/tabs/_apiPredict.js — thin client for the FastAPI inference backend.
// Keeps the network details out of Demo.js. The backend contract is defined in
// server/app/schemas.py (PatientPredictionResponse).

const API = process.env.REACT_APP_API_URL || '';

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
  const t0 = performance.now();
  const res = await fetch(`${API}/api/predict`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  const json = await res.json();
  json.client_latency_ms = Math.round(performance.now() - t0);
  return json;
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
