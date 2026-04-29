"""
Stage 5: Adaptive Polar CLAHE with vessel-density-driven non-uniform angular sectors.

Fovea-centered polar grid (coords.json). Log-spaced radial rings.
Angular sector widths proportional to local vessel density (72 fine bins → adaptive merge).
Dual-constraint clipping + polar bilinear interpolation.

Generates 5 substep visualizations + final result for all grades.
"""

import cv2
import numpy as np
import json
import os
import math
import sys

BASE = os.path.join(os.path.dirname(__file__), "..")
CLIP_FACTOR = 2.0
GLOBAL_THRESHOLD = 0.01
Nr_base = 8
N_FINE = 72
MIN_SECTOR_BINS = 2
MAX_SECTOR_BINS = 6
MIN_SECTOR_AREA_FRAC = 0.01   # each tile (ring x angular sector) must cover >= 1% of FOV area
GRADES = ["dr00", "dr01", "dr02", "dr03", "dr04"]


def transform_fovea_to_512(coords_entry, base_path, gr, side):
    c = coords_entry
    fovea = np.array(c["fovea"], dtype=np.float64)
    img_c = np.array(c["image"], dtype=np.float64)
    angle_rad = math.radians(c["angle_deg"])

    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    dx, dy = fovea[0] - img_c[0], fovea[1] - img_c[1]
    fovea_rot = np.array([
        cos_a * dx - sin_a * dy + img_c[0],
        sin_a * dx + cos_a * dy + img_c[1]
    ])

    rot_img = cv2.imread(os.path.join(
        base_path, gr, "preprocessing", "stage_1_od_fovea_rotation", "image", f"{side}.png"
    ))
    gray = cv2.cvtColor(rot_img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(binary > 0)
    x1, y1 = xs.min(), ys.min()
    x2, y2 = xs.max() + 1, ys.max() + 1
    cw, ch = x2 - x1, y2 - y1

    fovea_crop = fovea_rot - np.array([x1, y1])
    scale = 512 / max(ch, cw)
    new_w, new_h = int(cw * scale), int(ch * scale)
    x_off = (512 - new_w) // 2
    y_off = (512 - new_h) // 2

    return int(fovea_crop[0] * scale + x_off), int(fovea_crop[1] * scale + y_off)


def vessel_detection(L):
    L_float = L.astype(np.float32) / 255.0
    vessel_map = np.zeros_like(L_float)
    for sigma in [1.0, 1.5, 2.0, 3.0]:
        Lg = cv2.GaussianBlur(L_float, (0, 0), sigma)
        Lxx = cv2.Sobel(Lg, cv2.CV_32F, 2, 0)
        Lyy = cv2.Sobel(Lg, cv2.CV_32F, 0, 2)
        Lxy = cv2.Sobel(Lg, cv2.CV_32F, 1, 1)
        tmp = np.sqrt((Lxx - Lyy)**2 + 4 * Lxy**2)
        l1 = 0.5 * ((Lxx + Lyy) + tmp)
        l2 = 0.5 * ((Lxx + Lyy) - tmp)
        lmin = np.minimum(l1, l2)
        vesselness = np.where(lmin < 0, lmin**2, 0)
        vessel_map = np.maximum(vessel_map, vesselness * sigma**2)
    vessel_map = vessel_map / (vessel_map.max() + 1e-6)
    return vessel_map


def merge_small_sectors(boundaries, fine_pixels, min_pixels):
    while True:
        sector_pixels = []
        for k in range(len(boundaries) - 1):
            fi_lo = int(round(boundaries[k] / (2 * np.pi) * N_FINE))
            fi_hi = int(round(boundaries[k + 1] / (2 * np.pi) * N_FINE))
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


def compute_nonuniform_sectors(vessel_map, r, theta, r_boundaries, mask, image_area):
    sector_boundaries_per_ring = []
    min_sector_pixels = MIN_SECTOR_AREA_FRAC * image_area
    print(f"  min_sector_pixels = {min_sector_pixels:.0f}  "
          f"({MIN_SECTOR_AREA_FRAC * 100:.0f}% of FOV={image_area} px)")

    for ri in range(Nr_base):
        r_lo, r_hi = r_boundaries[ri], r_boundaries[ri + 1]
        ring_mask = (r >= r_lo) & (r < r_hi) & (mask > 0)
        ring_pixel_count = int(ring_mask.sum())

        if ring_pixel_count < min_sector_pixels:
            sector_boundaries_per_ring.append([0, 2 * np.pi])
            print(f"  ring {ri}: {ring_pixel_count} px < threshold -> 1 sector (full 360 deg)")
            continue

        fine_density = np.zeros(N_FINE)
        fine_pixels = np.zeros(N_FINE, dtype=int)
        for fi in range(N_FINE):
            t_lo = fi / N_FINE * 2 * np.pi
            t_hi = (fi + 1) / N_FINE * 2 * np.pi
            sec = ring_mask & (theta >= t_lo) & (theta < t_hi)
            cnt = int(sec.sum())
            fine_pixels[fi] = cnt
            if cnt > 0:
                fine_density[fi] = vessel_map[sec].mean()

        fine_smooth = np.convolve(
            np.tile(fine_density, 3),
            np.ones(5) / 5, mode="same"
        )[N_FINE:2 * N_FINE]

        thr_dens = np.median(fine_smooth[fine_smooth > 0]) if (fine_smooth > 0).any() else 0

        boundaries = [0]
        accum_bins = 0
        accum_pixels = 0
        for fi in range(N_FINE):
            accum_bins += 1
            accum_pixels += fine_pixels[fi]
            if fi == N_FINE - 1:
                boundaries.append(2 * np.pi)
            elif (fine_smooth[fi] > thr_dens
                  and accum_bins >= MIN_SECTOR_BINS
                  and accum_pixels >= min_sector_pixels):
                boundaries.append((fi + 1) / N_FINE * 2 * np.pi)
                accum_bins = 0
                accum_pixels = 0
            elif accum_bins >= MAX_SECTOR_BINS and accum_pixels >= min_sector_pixels:
                boundaries.append((fi + 1) / N_FINE * 2 * np.pi)
                accum_bins = 0
                accum_pixels = 0

        boundaries = merge_small_sectors(boundaries, fine_pixels, min_sector_pixels)
        sector_boundaries_per_ring.append(boundaries)
    return sector_boundaries_per_ring


def build_luts(L, r, theta, r_boundaries, sector_boundaries_per_ring, mask):
    LUTs = {}
    for ri in range(Nr_base):
        bounds = sector_boundaries_per_ring[ri]
        n_sec = len(bounds) - 1
        for ti in range(n_sec):
            sector = ((r >= r_boundaries[ri]) & (r < r_boundaries[ri + 1]) &
                      (theta >= bounds[ti]) & (theta < bounds[ti + 1]) & (mask > 0))
            pixels = L[sector]
            if len(pixels) < 10:
                LUTs[(ri, ti)] = np.arange(256, dtype=np.uint8)
                continue
            tile_area = len(pixels)
            cl = min(CLIP_FACTOR * tile_area / 256, GLOBAL_THRESHOLD * tile_area)
            hist, _ = np.histogram(pixels, bins=256, range=(0, 256))
            hist = hist.astype(np.float32)
            excess = np.maximum(hist - cl, 0.0)
            clipped = hist - excess
            clipped += excess.sum() / 256
            cdf = np.cumsum(clipped)
            cdf_norm = (cdf - cdf.min()) / (cdf.max() - cdf.min() + 1e-6)
            LUTs[(ri, ti)] = np.clip(cdf_norm * 255, 0, 255).astype(np.uint8)
    return LUTs


def interpolate_nonuniform(L, r, theta, r_boundaries, sector_boundaries_per_ring, LUTs, mask):
    L_out = np.zeros_like(L, dtype=np.float32)
    fundus_ys, fundus_xs = np.where(mask > 0)
    r_vals = r[fundus_ys, fundus_xs]
    t_vals = theta[fundus_ys, fundus_xs]
    l_vals = L[fundus_ys, fundus_xs]

    ri_arr = np.full(len(r_vals), Nr_base - 1, dtype=int)
    for i in range(Nr_base):
        within = r_vals < r_boundaries[i + 1]
        ri_arr = np.where((ri_arr == Nr_base - 1) & within, i, ri_arr)

    w_r = np.clip((r_vals - r_boundaries[ri_arr]) /
                  (r_boundaries[np.minimum(ri_arr + 1, Nr_base)] - r_boundaries[ri_arr] + 1e-6), 0, 1)
    ri_hi_arr = np.minimum(ri_arr + 1, Nr_base - 1)

    result = np.zeros(len(r_vals), dtype=np.float32)

    for r_weight, r_idx_arr in [(1 - w_r, ri_arr), (w_r, ri_hi_arr)]:
        ring_result = np.zeros(len(r_vals), dtype=np.float32)
        unique_ri = np.unique(r_idx_arr)

        for ri_val in unique_ri:
            px_mask = r_idx_arr == ri_val
            bounds = sector_boundaries_per_ring[ri_val]
            n_sec = len(bounds) - 1
            bounds_arr = np.array(bounds)
            t_px = t_vals[px_mask]
            l_px = l_vals[px_mask]

            ti_arr = np.searchsorted(bounds_arr, t_px, side='right') - 1
            ti_arr = np.clip(ti_arr, 0, n_sec - 1)

            w_t = np.clip((t_px - bounds_arr[ti_arr]) /
                          (bounds_arr[ti_arr + 1] - bounds_arr[ti_arr] + 1e-6), 0, 1)

            vals = np.zeros(len(t_px), dtype=np.float32)
            for ti in range(n_sec):
                ti_hi = (ti + 1) % n_sec
                sec_mask = ti_arr == ti
                if not sec_mask.any():
                    continue
                lut_lo = LUTs.get((ri_val, ti), np.arange(256, dtype=np.uint8))
                lut_hi = LUTs.get((ri_val, ti_hi), np.arange(256, dtype=np.uint8))
                lp = l_px[sec_mask]
                wt = w_t[sec_mask]
                vals[sec_mask] = (1 - wt) * lut_lo[lp].astype(np.float32) + wt * lut_hi[lp].astype(np.float32)

            full_indices = np.where(px_mask)[0]
            ring_result[full_indices] = vals

        result += r_weight * ring_result

    L_out[fundus_ys, fundus_xs] = result
    return np.clip(L_out, 0, 255).astype(np.uint8)


def process_grade(gr, all_coords):
    print(f"\n=== {gr} ===")

    for side in ["left", "right"]:
        fcx, fcy = transform_fovea_to_512(all_coords[gr][side], BASE, gr, side)
        print(f"  {side}: fovea on 512x512 = ({fcx}, {fcy})")

        img_bgr = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_4_flatfield", f"{side}.png"))
        mask = cv2.imread(os.path.join(BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"), cv2.IMREAD_GRAYSCALE)
        h, w = img_bgr.shape[:2]
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        L, A, B = cv2.split(lab)
        mask_3ch = np.expand_dims(mask > 0, axis=-1).astype(np.uint8)

        yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt((xx - fcx).astype(np.float32)**2 + (yy - fcy).astype(np.float32)**2)
        theta = np.arctan2((yy - fcy).astype(np.float32), (xx - fcx).astype(np.float32)) + np.pi
        r_max = r[mask > 0].max()

        r_boundaries = np.array([(i / Nr_base)**1.5 * r_max for i in range(Nr_base + 1)])

        vessel_map = vessel_detection(L)
        vessel_map[mask == 0] = 0

        image_area = int((mask > 0).sum())
        sector_boundaries_per_ring = compute_nonuniform_sectors(
            vessel_map, r, theta, r_boundaries, mask, image_area)
        n_sectors = [len(b) - 1 for b in sector_boundaries_per_ring]
        print(f"  sectors per ring: {n_sectors}")

        polar_base = os.path.join(BASE, gr, "preprocessing", "stage_5_clahe", "polar")

        # 1. Vessel detection
        vessel_vis = np.power(vessel_map, 0.3)
        vessel_vis = (vessel_vis * 255).astype(np.uint8)
        vessel_vis[mask == 0] = 0
        os.makedirs(os.path.join(polar_base, "1_vessel_detection"), exist_ok=True)
        cv2.imwrite(os.path.join(polar_base, "1_vessel_detection", f"{side}.png"), vessel_vis)

        # 2. Density heatmap
        density_smooth = cv2.GaussianBlur(vessel_map, (0, 0), 20)
        density_smooth = density_smooth / (density_smooth.max() + 1e-6)
        density_smooth[mask == 0] = 0
        density_color = cv2.applyColorMap((density_smooth * 255).astype(np.uint8), cv2.COLORMAP_JET)
        density_color[mask == 0] = 0
        os.makedirs(os.path.join(polar_base, "2_vessel_density"), exist_ok=True)
        cv2.imwrite(os.path.join(polar_base, "2_vessel_density", f"{side}.png"), density_color)

        # 3. Non-uniform polar grid
        grid_vis = img_bgr.copy()
        for ri in range(1, Nr_base):
            cv2.circle(grid_vis, (fcx, fcy), int(r_boundaries[ri]), (0, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(grid_vis, (fcx, fcy), int(r_max), (0, 255, 255), 1, cv2.LINE_AA)
        for ri in range(Nr_base):
            bounds = sector_boundaries_per_ring[ri]
            r_inner, r_outer = int(r_boundaries[ri]), int(r_boundaries[ri + 1])
            for angle in bounds[:-1]:
                a = angle - np.pi
                cv2.line(grid_vis,
                         (int(fcx + r_inner * np.cos(a)), int(fcy + r_inner * np.sin(a))),
                         (int(fcx + r_outer * np.cos(a)), int(fcy + r_outer * np.sin(a))),
                         (0, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(grid_vis, (fcx, fcy), 5, (149, 45, 255), -1)
        grid_vis[mask == 0] = 0
        os.makedirs(os.path.join(polar_base, "3_polar_grid_adaptive"), exist_ok=True)
        cv2.imwrite(os.path.join(polar_base, "3_polar_grid_adaptive", f"{side}.png"), grid_vis)

        # 4. Density + grid overlay
        overlay = cv2.addWeighted(img_bgr, 0.5, density_color, 0.5, 0)
        for ri in range(1, Nr_base):
            cv2.circle(overlay, (fcx, fcy), int(r_boundaries[ri]), (255, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(overlay, (fcx, fcy), int(r_max), (255, 255, 255), 1, cv2.LINE_AA)
        for ri in range(Nr_base):
            bounds = sector_boundaries_per_ring[ri]
            r_inner, r_outer = int(r_boundaries[ri]), int(r_boundaries[ri + 1])
            for angle in bounds[:-1]:
                a = angle - np.pi
                cv2.line(overlay,
                         (int(fcx + r_inner * np.cos(a)), int(fcy + r_inner * np.sin(a))),
                         (int(fcx + r_outer * np.cos(a)), int(fcy + r_outer * np.sin(a))),
                         (255, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(overlay, (fcx, fcy), 5, (149, 45, 255), -1)
        overlay[mask == 0] = 0
        os.makedirs(os.path.join(polar_base, "4_density_grid_adaptive"), exist_ok=True)
        cv2.imwrite(os.path.join(polar_base, "4_density_grid_adaptive", f"{side}.png"), overlay)

        # Build LUTs
        LUTs = build_luts(L, r, theta, r_boundaries, sector_boundaries_per_ring, mask)

        # 5. No interpolation
        L_no = np.zeros_like(L)
        for ri in range(Nr_base):
            bounds = sector_boundaries_per_ring[ri]
            for ti in range(len(bounds) - 1):
                sector = ((r >= r_boundaries[ri]) & (r < r_boundaries[ri + 1]) &
                          (theta >= bounds[ti]) & (theta < bounds[ti + 1]) & (mask > 0))
                L_no[sector] = LUTs.get((ri, ti), np.arange(256, dtype=np.uint8))[L[sector]]
        merged_no = cv2.merge((L_no, A, B))
        result_no = cv2.cvtColor(merged_no, cv2.COLOR_LAB2BGR) * mask_3ch
        os.makedirs(os.path.join(polar_base, "5_clahe_no_interpolation"), exist_ok=True)
        cv2.imwrite(os.path.join(polar_base, "5_clahe_no_interpolation", f"{side}.png"), result_no)

        # Final: polar bilinear interpolation
        L_out = interpolate_nonuniform(L, r, theta, r_boundaries, sector_boundaries_per_ring, LUTs, mask)
        merged = cv2.merge((L_out, A, B))
        result = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR) * mask_3ch
        cv2.imwrite(os.path.join(polar_base, f"{side}.png"), result)

        fundus = result[mask > 0]
        print(f"  final: mean={fundus.mean():.1f}, std={fundus.std():.1f}")


def run():
    with open(os.path.join(os.path.dirname(__file__), "coords.json")) as f:
        all_coords = json.load(f)

    grades = sys.argv[1:] if len(sys.argv) > 1 else GRADES
    for gr in grades:
        process_grade(gr, all_coords)


if __name__ == "__main__":
    run()
