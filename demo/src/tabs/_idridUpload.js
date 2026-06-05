// src/tabs/_idridUpload.js — match a MANUAL upload to IDRiD ground truth.
//
// When the user picks a file from the IDRiD Localization TRAINING set (named
// IDRiD_NNN.jpg, 3-digit), we look up its ground-truth OD + fovea centres from
// the bundled `_idridGtLookup.js` and build the same `gt` payload the random
// button produces — so the preprocessing/centre overlay renders for it too.
//
// Coordinates in the lookup are in ORIGINAL-image pixels; the uploaded image is
// shown at its natural size, so they project directly. The FOV mask is produced
// client-side from the uploaded pixels (canvas threshold), mirroring the
// server-side mask for the toggle.
//
// 2-digit names like "IDRiD_21" (the Segmentation sub-challenge — a DIFFERENT
// image set with different numbering) deliberately do NOT match, so they can't
// be overlaid with the wrong coordinates.

import { IDRID_GT } from './_idridGtLookup';

// Extract a 3-digit Localization id (IDRiD_NNN) from a filename, or null.
function normId(name) {
  if (!name) return null;
  const m = String(name).match(/IDRiD[_-]?(\d{3})(?!\d)/i);
  return m ? `IDRiD_${m[1]}` : null;
}

// Build a display-frame FOV mask (white field on black) from a loaded image via
// a downscaled canvas threshold. Same aspect ratio as the source, so it lines
// up under objectFit:contain.
function fovMaskDataUrl(img, maxSide = 512) {
  const scale = Math.min(1, maxSide / Math.max(img.naturalWidth, img.naturalHeight));
  const w = Math.max(1, Math.round(img.naturalWidth * scale));
  const h = Math.max(1, Math.round(img.naturalHeight * scale));
  const canvas = document.createElement('canvas');
  canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, w, h);
  const data = ctx.getImageData(0, 0, w, h);
  const px = data.data;
  for (let i = 0; i < px.length; i += 4) {
    const gray = 0.299 * px[i] + 0.587 * px[i + 1] + 0.114 * px[i + 2];
    const v = gray > 15 ? 255 : 0;
    px[i] = px[i + 1] = px[i + 2] = v; px[i + 3] = 255;
  }
  ctx.putImageData(data, 0, 0);
  return canvas.toDataURL('image/png');
}

// Resolve to a `gt` payload if `name` matches a bundled IDRiD localization id,
// else null. Never rejects.
export function matchIdridUpload(name, src) {
  const id = normId(name);
  if (!id) return Promise.resolve(null);
  const g = IDRID_GT[id];
  if (!g) return Promise.resolve(null);
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const width = img.naturalWidth, height = img.naturalHeight;
      const side = g.fovea[0] > g.od[0] ? 'left' : 'right';
      let maskSrc = null;
      try { maskSrc = fovMaskDataUrl(img); } catch { maskSrc = null; }
      resolve({
        source: 'IDRiD-upload',
        id,
        side,
        odCenter: g.od,
        foveaCenter: g.fovea,
        odRadius: width / 18,
        width,
        height,
        maskSrc,
      });
    };
    img.onerror = () => resolve(null);
    img.src = src;
  });
}
