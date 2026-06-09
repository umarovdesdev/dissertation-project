"""
Stage 5 (polar variant): Adaptive Polar CLAHE.

Fovea-centred polar grid with log-spaced radial rings and vessel-density-driven
non-uniform angular sectors, dual-constraint histogram clipping, and polar
bilinear interpolation. This is the algorithm the dissertation describes for
Stage 5 and the one the static demo images under
``demo/public/.../stage_5_clahe/polar/`` are generated with; this module is the
framework-clean production port of ``demo/public/pipeline/helpers/s5_polar_adaptive.py``.

Contract mirrors :func:`upgraded_clahe.apply_upgraded_clahe`: input and output
are RGB uint8 arrays, enhancement runs on the LAB L-channel, and pixels outside
the FOV mask are left unchanged.

Pivot centre (important — see TASK-fix #4)
------------------------------------------
The polar grid is centred on the fovea. The Stage 1 OD/fovea detector, validated
against IDRiD ground-truth (``scripts/validate_od_fovea_idrid.py``), localizes
the fovea poorly at native resolution (median ≈5 OD-radii error, ~0% within 2
OD-radii) and its ``confident`` flag does not gate the failures. Pivoting on that
centre would be unreliable, so the **default pivot is the FOV-mask centroid** —
deterministic, robust, and ≈ the central retina in a centred FOV crop. A caller
may pass an explicit ``fovea_xy`` (e.g. a trustworthy/annotated centre); it is
used only when it falls inside the FOV, otherwise the centroid is used.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

@dataclass
class PolarClaheParams:
    """Parameters for the adaptive polar CLAHE algorithm.

    Args:
        clip_factor: Per-tile clip-limit scale (``clip_factor × tile_area / 256``).
        global_threshold: Additional global clip limit (``global_threshold × tile_area``).
        radial_rings: Number of log-spaced radial rings (``Nr_base``).
        radial_exponent: Exponent of the radial spacing law ``r ∝ (i/N)^exp``.
        fine_bins: Number of fine angular bins merged into adaptive sectors.
        min_sector_bins: Minimum fine bins per merged angular sector.
        max_sector_bins: Maximum fine bins per merged angular sector.
        min_sector_area_frac: Each ring/sector tile must cover at least this
            fraction of the FOV area, else it is merged / the ring is left whole.
        vessel_sigmas: Gaussian σ scales for multi-scale vesselness.
    """

    clip_factor: float = 2.0
    global_threshold: float = 0.01
    radial_rings: int = 8
    radial_exponent: float = 1.5
    fine_bins: int = 72
    min_sector_bins: int = 2
    max_sector_bins: int = 6
    min_sector_area_frac: float = 0.01
    vessel_sigmas: tuple[float, ...] = (1.0, 1.5, 2.0, 3.0)


# ---------------------------------------------------------------------------
# Vessel detection (multi-scale Hessian vesselness)
# ---------------------------------------------------------------------------

def _vessel_detection(
    l_channel: np.ndarray,
    sigmas: tuple[float, ...],
) -> np.ndarray:
    """Multi-scale Hessian vesselness map normalised to [0, 1].

    Args:
        l_channel: uint8 L-channel.
        sigmas: Gaussian scales to combine (max over scales).

    Returns:
        float32 vesselness map of the same shape, in [0, 1].
    """
    l_float = l_channel.astype(np.float32) / 255.0
    vessel_map = np.zeros_like(l_float)
    for sigma in sigmas:
        lg = cv2.GaussianBlur(l_float, (0, 0), sigma)
        lxx = cv2.Sobel(lg, cv2.CV_32F, 2, 0)
        lyy = cv2.Sobel(lg, cv2.CV_32F, 0, 2)
        lxy = cv2.Sobel(lg, cv2.CV_32F, 1, 1)
        tmp = np.sqrt((lxx - lyy) ** 2 + 4 * lxy ** 2)
        l1 = 0.5 * ((lxx + lyy) + tmp)
        l2 = 0.5 * ((lxx + lyy) - tmp)
        lmin = np.minimum(l1, l2)
        vesselness = np.where(lmin < 0, lmin ** 2, 0)
        vessel_map = np.maximum(vessel_map, vesselness * sigma ** 2)
    return vessel_map / (vessel_map.max() + 1e-6)


# ---------------------------------------------------------------------------
# Adaptive angular sectors
# ---------------------------------------------------------------------------

def _merge_small_sectors(
    boundaries: list[float],
    fine_pixels: np.ndarray,
    min_pixels: float,
    fine_bins: int,
) -> list[float]:
    """Merge angular sectors that fall below ``min_pixels`` until none remain."""
    while True:
        sector_pixels = []
        for k in range(len(boundaries) - 1):
            fi_lo = int(round(boundaries[k] / (2 * np.pi) * fine_bins))
            fi_hi = int(round(boundaries[k + 1] / (2 * np.pi) * fine_bins))
            sector_pixels.append(int(fine_pixels[fi_lo:fi_hi].sum()))
        if not sector_pixels or len(boundaries) <= 2:
            break
        if min(sector_pixels) >= min_pixels:
            break
        small_idx = int(np.argmin(sector_pixels))
        if small_idx == 0:
            boundaries.pop(1)
        elif small_idx == len(sector_pixels) - 1:
            boundaries.pop(-2)
        else:
            left = sector_pixels[small_idx - 1]
            right = sector_pixels[small_idx + 1]
            boundaries.pop(small_idx if left <= right else small_idx + 1)
    return boundaries


def _compute_nonuniform_sectors(
    vessel_map: np.ndarray,
    r: np.ndarray,
    theta: np.ndarray,
    r_boundaries: np.ndarray,
    mask: np.ndarray,
    image_area: int,
    params: PolarClaheParams,
) -> list[list[float]]:
    """Compute vessel-density-driven angular sector boundaries per radial ring.

    Args:
        vessel_map: Normalised vesselness map.
        r: Radial distance from the pivot per pixel.
        theta: Angle in [0, 2π) per pixel.
        r_boundaries: Radial ring boundaries (length ``radial_rings + 1``).
        mask: Boolean/float FOV mask (>0 inside).
        image_area: FOV pixel count (for the min-sector-area threshold).
        params: :class:`PolarClaheParams`.

    Returns:
        List (per ring) of angular boundary lists in radians.
    """
    n_fine = params.fine_bins
    sector_boundaries_per_ring: list[list[float]] = []
    min_sector_pixels = params.min_sector_area_frac * image_area

    for ri in range(params.radial_rings):
        r_lo, r_hi = r_boundaries[ri], r_boundaries[ri + 1]
        ring_mask = (r >= r_lo) & (r < r_hi) & (mask > 0)
        if int(ring_mask.sum()) < min_sector_pixels:
            sector_boundaries_per_ring.append([0, 2 * np.pi])
            continue

        fine_density = np.zeros(n_fine)
        fine_pixels = np.zeros(n_fine, dtype=int)
        for fi in range(n_fine):
            t_lo = fi / n_fine * 2 * np.pi
            t_hi = (fi + 1) / n_fine * 2 * np.pi
            sec = ring_mask & (theta >= t_lo) & (theta < t_hi)
            cnt = int(sec.sum())
            fine_pixels[fi] = cnt
            if cnt > 0:
                fine_density[fi] = vessel_map[sec].mean()

        fine_smooth = np.convolve(
            np.tile(fine_density, 3), np.ones(5) / 5, mode="same"
        )[n_fine:2 * n_fine]
        thr_dens = (np.median(fine_smooth[fine_smooth > 0])
                    if (fine_smooth > 0).any() else 0)

        boundaries = [0]
        accum_bins = 0
        accum_pixels = 0
        for fi in range(n_fine):
            accum_bins += 1
            accum_pixels += fine_pixels[fi]
            if fi == n_fine - 1:
                boundaries.append(2 * np.pi)
            elif (fine_smooth[fi] > thr_dens
                  and accum_bins >= params.min_sector_bins
                  and accum_pixels >= min_sector_pixels):
                boundaries.append((fi + 1) / n_fine * 2 * np.pi)
                accum_bins = 0
                accum_pixels = 0
            elif accum_bins >= params.max_sector_bins and accum_pixels >= min_sector_pixels:
                boundaries.append((fi + 1) / n_fine * 2 * np.pi)
                accum_bins = 0
                accum_pixels = 0

        boundaries = _merge_small_sectors(
            boundaries, fine_pixels, min_sector_pixels, n_fine
        )
        sector_boundaries_per_ring.append(boundaries)
    return sector_boundaries_per_ring


# ---------------------------------------------------------------------------
# LUT construction + polar bilinear interpolation
# ---------------------------------------------------------------------------

def _build_luts(
    l_channel: np.ndarray,
    r: np.ndarray,
    theta: np.ndarray,
    r_boundaries: np.ndarray,
    sector_boundaries_per_ring: list[list[float]],
    mask: np.ndarray,
    params: PolarClaheParams,
) -> dict[tuple[int, int], np.ndarray]:
    """Build a dual-constraint-clipped equalisation LUT per (ring, sector) tile."""
    luts: dict[tuple[int, int], np.ndarray] = {}
    for ri in range(params.radial_rings):
        bounds = sector_boundaries_per_ring[ri]
        for ti in range(len(bounds) - 1):
            sector = ((r >= r_boundaries[ri]) & (r < r_boundaries[ri + 1]) &
                      (theta >= bounds[ti]) & (theta < bounds[ti + 1]) & (mask > 0))
            pixels = l_channel[sector]
            if len(pixels) < 10:
                luts[(ri, ti)] = np.arange(256, dtype=np.uint8)
                continue
            tile_area = len(pixels)
            cl = min(params.clip_factor * tile_area / 256,
                     params.global_threshold * tile_area)
            hist, _ = np.histogram(pixels, bins=256, range=(0, 256))
            hist = hist.astype(np.float32)
            excess = np.maximum(hist - cl, 0.0)
            clipped = hist - excess
            clipped += excess.sum() / 256
            cdf = np.cumsum(clipped)
            cdf_norm = (cdf - cdf.min()) / (cdf.max() - cdf.min() + 1e-6)
            luts[(ri, ti)] = np.clip(cdf_norm * 255, 0, 255).astype(np.uint8)
    return luts


def _interpolate_nonuniform(
    l_channel: np.ndarray,
    r: np.ndarray,
    theta: np.ndarray,
    r_boundaries: np.ndarray,
    sector_boundaries_per_ring: list[list[float]],
    luts: dict[tuple[int, int], np.ndarray],
    mask: np.ndarray,
    params: PolarClaheParams,
) -> np.ndarray:
    """Apply the per-tile LUTs with polar bilinear interpolation (radial + angular).

    Returns:
        uint8 L-channel; pixels outside the FOV mask keep their input value.
    """
    n_rings = params.radial_rings
    l_out = l_channel.astype(np.float32).copy()
    fundus_ys, fundus_xs = np.where(mask > 0)
    r_vals = r[fundus_ys, fundus_xs]
    t_vals = theta[fundus_ys, fundus_xs]
    l_vals = l_channel[fundus_ys, fundus_xs]

    ri_arr = np.full(len(r_vals), n_rings - 1, dtype=int)
    for i in range(n_rings):
        within = r_vals < r_boundaries[i + 1]
        ri_arr = np.where((ri_arr == n_rings - 1) & within, i, ri_arr)

    w_r = np.clip(
        (r_vals - r_boundaries[ri_arr]) /
        (r_boundaries[np.minimum(ri_arr + 1, n_rings)] - r_boundaries[ri_arr] + 1e-6),
        0, 1,
    )
    ri_hi_arr = np.minimum(ri_arr + 1, n_rings - 1)

    result = np.zeros(len(r_vals), dtype=np.float32)
    for r_weight, r_idx_arr in [(1 - w_r, ri_arr), (w_r, ri_hi_arr)]:
        ring_result = np.zeros(len(r_vals), dtype=np.float32)
        for ri_val in np.unique(r_idx_arr):
            px_mask = r_idx_arr == ri_val
            bounds = sector_boundaries_per_ring[ri_val]
            n_sec = len(bounds) - 1
            bounds_arr = np.array(bounds)
            t_px = t_vals[px_mask]
            l_px = l_vals[px_mask]

            ti_arr = np.searchsorted(bounds_arr, t_px, side="right") - 1
            ti_arr = np.clip(ti_arr, 0, n_sec - 1)
            w_t = np.clip(
                (t_px - bounds_arr[ti_arr]) /
                (bounds_arr[ti_arr + 1] - bounds_arr[ti_arr] + 1e-6), 0, 1,
            )

            vals = np.zeros(len(t_px), dtype=np.float32)
            for ti in range(n_sec):
                ti_hi = (ti + 1) % n_sec
                sec_mask = ti_arr == ti
                if not sec_mask.any():
                    continue
                lut_lo = luts.get((ri_val, ti), np.arange(256, dtype=np.uint8))
                lut_hi = luts.get((ri_val, ti_hi), np.arange(256, dtype=np.uint8))
                lp = l_px[sec_mask]
                wt = w_t[sec_mask]
                vals[sec_mask] = ((1 - wt) * lut_lo[lp].astype(np.float32)
                                  + wt * lut_hi[lp].astype(np.float32))

            ring_result[np.where(px_mask)[0]] = vals
        result += r_weight * ring_result

    l_out[fundus_ys, fundus_xs] = result
    return np.clip(l_out, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Pivot resolution
# ---------------------------------------------------------------------------

def resolve_pivot(
    fov_mask: np.ndarray,
    fovea_xy: tuple[float, float] | None,
) -> tuple[float, float]:
    """Resolve the polar-grid pivot: a valid in-FOV ``fovea_xy`` else FOV centroid.

    Args:
        fov_mask: float/bool FOV mask (>0 inside the field of view).
        fovea_xy: Optional ``(x, y)`` fovea centre in image pixels. Used only
            when it lands inside the FOV; otherwise the centroid is used (see the
            module docstring on detector unreliability, TASK-fix #4).

    Returns:
        ``(cx, cy)`` pivot coordinates in pixels.
    """
    ys, xs = np.where(fov_mask > 0)
    if xs.size == 0:
        h, w = fov_mask.shape[:2]
        return (w / 2.0, h / 2.0)
    cx_centroid, cy_centroid = float(xs.mean()), float(ys.mean())

    if fovea_xy is not None:
        fx, fy = float(fovea_xy[0]), float(fovea_xy[1])
        ix, iy = int(round(fx)), int(round(fy))
        if (0 <= iy < fov_mask.shape[0] and 0 <= ix < fov_mask.shape[1]
                and fov_mask[iy, ix] > 0):
            return fx, fy
    return cx_centroid, cy_centroid


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def apply_polar_clahe(
    image_rgb: np.ndarray,
    fov_mask: np.ndarray,
    params: PolarClaheParams | None = None,
    fovea_xy: tuple[float, float] | None = None,
) -> np.ndarray:
    """Apply adaptive polar CLAHE to the L-channel of an RGB image.

    Builds a fovea-centred (or FOV-centroid) polar grid with log-spaced radial
    rings and vessel-density-driven angular sectors, equalises each tile with the
    dual-constraint clip, and recombines via polar bilinear interpolation.

    Args:
        image_rgb: RGB uint8 array of shape ``(H, W, 3)`` (Stage-4 output).
        fov_mask: float32 ``(H, W)`` binary FOV mask (1.0 inside, 0.0 padding).
        params: :class:`PolarClaheParams`; defaults used when ``None``.
        fovea_xy: Optional fovea pivot in pixels (see :func:`resolve_pivot`).

    Returns:
        Enhanced RGB uint8 array of shape ``(H, W, 3)``; padding (mask 0) is
        left unchanged.
    """
    if params is None:
        params = PolarClaheParams()

    mask = fov_mask > 0
    if not mask.any():
        return image_rgb

    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)

    h, w = l_ch.shape
    cx, cy = resolve_pivot(fov_mask, fovea_xy)

    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt((xx - cx).astype(np.float32) ** 2 + (yy - cy).astype(np.float32) ** 2)
    theta = np.arctan2((yy - cy).astype(np.float32), (xx - cx).astype(np.float32)) + np.pi
    r_max = float(r[mask].max())
    if r_max <= 0:
        return image_rgb

    n_rings = params.radial_rings
    r_boundaries = np.array(
        [(i / n_rings) ** params.radial_exponent * r_max for i in range(n_rings + 1)]
    )

    vessel_map = _vessel_detection(l_ch, params.vessel_sigmas)
    vessel_map[~mask] = 0
    image_area = int(mask.sum())

    sectors = _compute_nonuniform_sectors(
        vessel_map, r, theta, r_boundaries, fov_mask, image_area, params
    )
    luts = _build_luts(l_ch, r, theta, r_boundaries, sectors, fov_mask, params)
    l_out = _interpolate_nonuniform(
        l_ch, r, theta, r_boundaries, sectors, luts, fov_mask, params
    )

    merged = cv2.merge((l_out, a_ch, b_ch))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)


def maybe_apply_polar_clahe(
    image_rgb: np.ndarray,
    fov_mask: np.ndarray,
    params: PolarClaheParams | None = None,
    is_training: bool = True,
    train_prob: float = 0.8,
    fovea_xy: tuple[float, float] | None = None,
) -> np.ndarray:
    """Apply polar CLAHE with stochastic skip during training.

    Mirrors :func:`upgraded_clahe.maybe_apply_clahe`: always applied at
    inference; applied with probability ``train_prob`` during training.

    Args:
        image_rgb: RGB uint8 array ``(H, W, 3)``.
        fov_mask: float32 binary FOV mask.
        params: :class:`PolarClaheParams`; defaults used when ``None``.
        is_training: ``True`` during training, ``False`` at inference.
        train_prob: Probability of applying CLAHE at train time.
        fovea_xy: Optional fovea pivot (see :func:`resolve_pivot`).

    Returns:
        Processed (or unchanged) RGB uint8 array.
    """
    if is_training and np.random.rand() > train_prob:
        return image_rgb
    return apply_polar_clahe(image_rgb, fov_mask, params, fovea_xy)
