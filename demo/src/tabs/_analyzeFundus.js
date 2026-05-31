// src/tabs/_analyzeFundus.js — client-side fundus image validation.
//
// Two pure-canvas heuristics, no network / no model:
//   1. Is this a fundus photograph?  (4 independent tests, ≥3 → fundus)
//   2. Which eye is it?  Optic disc sits on the nasal side, so the brighter
//      half of the fundus ROI tells us the laterality.
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

// Laterality via half-luma comparison inside the ROI. The half holding the
// optic disc is brighter:  disc on left → right eye, disc on right → left eye.
function detectLaterality(imageData, roi) {
  const { x, y, w, h } = roi;
  let leftSum = 0, rightSum = 0, leftN = 0, rightN = 0;
  const mid = x + w / 2;
  const d = imageData.data;
  for (let j = y; j < y + h; j += 2) {
    for (let i = x; i < x + w; i += 2) {
      const k = (j * imageData.width + i) * 4;
      const l = 0.299 * d[k] + 0.587 * d[k + 1] + 0.114 * d[k + 2];
      if (l < 10) continue;             // outside the fundus disk
      if (i < mid) { leftSum += l; leftN++; }
      else         { rightSum += l; rightN++; }
    }
  }
  const L = leftSum / Math.max(leftN, 1);
  const R = rightSum / Math.max(rightN, 1);
  const ratio = (L - R) / ((L + R) / 2); // > 0 → disc on left → right eye
  if (Math.abs(ratio) < 0.03) return { guess: null, conf: 0 };
  return {
    guess: ratio > 0 ? 'right' : 'left',
    conf: Math.min(1, Math.abs(ratio) * 20),
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
