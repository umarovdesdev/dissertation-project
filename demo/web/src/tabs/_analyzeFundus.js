// src/tabs/_analyzeFundus.js — client-side fundus image validation.
//
// Two pure-canvas heuristics, no network / no model:
//   1. Is this a fundus photograph?  (4 independent tests, ≥3 → fundus)
//   2. Which eye is it?  We localize the optic disc (the brightest compact
//      structure) and read laterality from which side of the FOV it sits on.
//      Project canonical convention (canonical_orientation.py): right eye =
//      optic disc on the RIGHT, macula on the LEFT; left eye = mirror image.
//      So OD centroid right of the FOV centre → right eye; left → left eye.
//
// Exported entry point:
//   analyzeFundus(dataUrl): Promise<{ isFundus, laterality, confidence }>
//     isFundus    — boolean  (false → show a non-blocking warning)
//     laterality  — 'left' | 'right' | null
//     confidence  — number 0..1 (laterality confidence)
//
// On any failure (decode error, empty image) we resolve with a permissive
// result (isFundus: true, no laterality) so the UI never blocks an upload.

// Downscale longest side to this before sampling — the heuristics are
// scale-invariant and a small canvas keeps the check well under a frame.
const MAX_DIM = 256;

function luma(d, k) {
  return 0.299 * d[k] + 0.587 * d[k + 1] + 0.114 * d[k + 2];
}

// Bounding box of non-black pixels (luma > 15) → the fundus disk region.
function detectRoi(imageData) {
  const { width, height, data } = imageData;
  let minX = width, minY = height, maxX = 0, maxY = 0, found = false;
  for (let j = 0; j < height; j++) {
    for (let i = 0; i < width; i++) {
      if (luma(data, (j * width + i) * 4) > 15) {
        found = true;
        if (i < minX) minX = i;
        if (i > maxX) maxX = i;
        if (j < minY) minY = j;
        if (j > maxY) maxY = j;
      }
    }
  }
  if (!found) return { x: 0, y: 0, w: width, h: height };
  return { x: minX, y: minY, w: maxX - minX + 1, h: maxY - minY + 1 };
}

// Mean luma across four corner patches (~5% of the short side each).
function cornerMeanLuma(imageData) {
  const { width, height, data } = imageData;
  const p = Math.max(2, Math.round(0.05 * Math.min(width, height)));
  const corners = [
    [0, 0], [width - p, 0], [0, height - p], [width - p, height - p],
  ];
  let sum = 0, count = 0;
  for (const [cx, cy] of corners) {
    for (let j = cy; j < cy + p && j < height; j++) {
      for (let i = cx; i < cx + p && i < width; i++) {
        sum += luma(data, (j * width + i) * 4);
        count++;
      }
    }
  }
  return count ? sum / count : 0;
}

// Four-test fundus classifier. Passes if ≥ 3 of 4 hold.
function checkIsFundus(imageData, roi) {
  const { width, data } = imageData;
  let total = 0, nonBlack = 0;
  let sumR = 0, sumG = 0, sumB = 0;
  let sumL = 0, sumL2 = 0;
  for (let j = roi.y; j < roi.y + roi.h; j++) {
    for (let i = roi.x; i < roi.x + roi.w; i++) {
      const k = (j * width + i) * 4;
      total++;
      const l = luma(data, k);
      if (l > 15) {
        nonBlack++;
        sumR += data[k]; sumG += data[k + 1]; sumB += data[k + 2];
        sumL += l; sumL2 += l * l;
      }
    }
  }
  const n = Math.max(nonBlack, 1);
  const fill = total ? nonBlack / total : 0;          // non-black fill in box
  const aspect = roi.h ? roi.w / roi.h : 0;
  const mR = sumR / n, mG = sumG / n, mB = sumB / n;
  const meanL = sumL / n;
  const std = Math.sqrt(Math.max(0, sumL2 / n - meanL * meanL));

  // 1. Circular ROI on a dark background.
  const t1 = aspect >= 0.8 && aspect <= 1.2 && fill > 0.6;
  // 2. Dark corners (vignette).
  const t2 = cornerMeanLuma(imageData) < 20;
  // 3. Red-orange dominance (rejects selfies, documents, screenshots).
  const t3 = mR > mG && mG > mB && (mB > 0 ? mR / mB : 99) > 1.8;
  // 4. Not flat (rejects single-color images).
  const t4 = std > 20;

  const passes = [t1, t2, t3, t4].filter(Boolean).length;
  return passes >= 3;
}

// Separable box blur of a single-channel float grid (in place via a scratch
// buffer). A few passes approximate a Gaussian — enough to suppress thin dark
// vessels and small specular highlights so the optic disc survives as the
// dominant bright blob. `radius` is in grid pixels.
function boxBlur(src, w, h, radius) {
  const tmp = new Float32Array(w * h);
  const r = Math.max(1, radius | 0);
  const norm = 1 / (2 * r + 1);
  // Horizontal pass: src → tmp.
  for (let j = 0; j < h; j++) {
    const row = j * w;
    let acc = 0;
    for (let i = -r; i <= r; i++) acc += src[row + Math.min(w - 1, Math.max(0, i))];
    for (let i = 0; i < w; i++) {
      tmp[row + i] = acc * norm;
      const iOut = Math.max(0, i - r);
      const iIn = Math.min(w - 1, i + r + 1);
      acc += src[row + iIn] - src[row + iOut];
    }
  }
  // Vertical pass: tmp → src.
  for (let i = 0; i < w; i++) {
    let acc = 0;
    for (let j = -r; j <= r; j++) acc += tmp[Math.min(h - 1, Math.max(0, j)) * w + i];
    for (let j = 0; j < h; j++) {
      src[j * w + i] = acc * norm;
      const jOut = Math.max(0, j - r);
      const jIn = Math.min(h - 1, j + r + 1);
      acc += tmp[jIn * w + i] - tmp[jOut * w + i];
    }
  }
  return src;
}

// Laterality via optic-disc localization. We blur the luma inside the FOV to
// suppress vessels, find the optic disc as the centroid of the brightest pixels
// (top percentile of the blurred map, FOV-masked), and read laterality from its
// horizontal position relative to the FOV centre.
//   OD right of centre → right eye  |  OD left of centre → left eye
// (matches the project canonical convention: right eye = disc on the right).
function detectLaterality(imageData, roi) {
  const { x, y, w, h } = roi;
  const W = imageData.width;
  const d = imageData.data;

  // Luma grid over the ROI, with a FOV mask (luma > 15 = inside the disk).
  const grid = new Float32Array(w * h);
  const fov = new Uint8Array(w * h);
  let fovN = 0;
  for (let j = 0; j < h; j++) {
    for (let i = 0; i < w; i++) {
      const l = luma(d, ((y + j) * W + (x + i)) * 4);
      grid[j * w + i] = l;
      if (l > 15) { fov[j * w + i] = 1; fovN++; }
    }
  }
  if (fovN < 16) return { guess: null, conf: 0 };

  // Blur radius ~6% of the short side suppresses vessels but keeps the disc.
  boxBlur(grid, w, h, Math.max(2, Math.round(0.06 * Math.min(w, h))));

  // Peak blurred intensity inside the FOV → disc threshold at 92% of the peak.
  let peak = 0;
  for (let p = 0; p < grid.length; p++) if (fov[p] && grid[p] > peak) peak = grid[p];
  if (peak <= 0) return { guess: null, conf: 0 };
  const thr = 0.92 * peak;

  // Centroid of the brightest blob (the optic disc).
  let sx = 0, n = 0;
  for (let j = 0; j < h; j++) {
    for (let i = 0; i < w; i++) {
      const p = j * w + i;
      if (fov[p] && grid[p] >= thr) { sx += i; n++; }
    }
  }
  if (n === 0) return { guess: null, conf: 0 };
  const odx = sx / n;

  // Offset of the disc from the FOV centre, normalized to the half-width.
  const half = w / 2;
  const offset = (odx - half) / half; // >0 → disc on the right → right eye
  if (Math.abs(offset) < 0.05) return { guess: null, conf: 0 };
  return {
    guess: offset > 0 ? 'right' : 'left',
    conf: Math.min(1, Math.abs(offset) * 2.5),
  };
}

export function analyzeFundus(dataUrl) {
  return new Promise((resolve) => {
    const permissive = { isFundus: true, laterality: null, confidence: 0 };
    if (!dataUrl) { resolve(permissive); return; }

    const img = new Image();
    img.onerror = () => resolve(permissive);
    img.onload = () => {
      try {
        const longest = Math.max(img.naturalWidth, img.naturalHeight);
        const scale = longest > 0 ? Math.min(1, MAX_DIM / longest) : 1;
        const w = Math.max(1, Math.round(img.naturalWidth * scale));
        const h = Math.max(1, Math.round(img.naturalHeight * scale));

        const canvas = document.createElement('canvas');
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        ctx.drawImage(img, 0, 0, w, h);
        const imageData = ctx.getImageData(0, 0, w, h);

        const roi = detectRoi(imageData);
        const isFundus = checkIsFundus(imageData, roi);
        const lat = detectLaterality(imageData, roi);
        resolve({ isFundus, laterality: lat.guess, confidence: lat.conf });
      } catch (e) {
        resolve(permissive);
      }
    };
    img.src = dataUrl;
  });
}
