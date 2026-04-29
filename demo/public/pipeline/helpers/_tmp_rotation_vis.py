import cv2, numpy as np, json, math, os

BASE = os.path.join(os.path.dirname(__file__), "..")
gr = "dr03"

with open(os.path.join(os.path.dirname(__file__), "coords.json")) as f:
    all_coords = json.load(f)


def transform_point_to_512(point, coords_entry, base_path, gr, side):
    c = coords_entry
    pt = np.array(point, dtype=np.float64)
    img_c = np.array(c["image"], dtype=np.float64)
    angle_rad = math.radians(c["angle_deg"])
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    dx, dy = pt[0] - img_c[0], pt[1] - img_c[1]
    pt_rot = np.array([
        cos_a * dx + sin_a * dy + img_c[0],
        -sin_a * dx + cos_a * dy + img_c[1]
    ])
    rot_img = cv2.imread(os.path.join(
        base_path, gr, "preprocessing", "stage_1_od_fovea_rotation", "image", f"{side}.png"
    ))
    gray_r = cv2.cvtColor(rot_img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_r, 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    ys, xs = np.where(binary > 0)
    x1, y1 = xs.min(), ys.min()
    x2, y2 = xs.max() + 1, ys.max() + 1
    cw, ch = x2 - x1, y2 - y1
    pt_crop = pt_rot - np.array([x1, y1])
    scale = 512 / max(ch, cw)
    new_w, new_h = int(cw * scale), int(ch * scale)
    x_off = (512 - new_w) // 2
    y_off = (512 - new_h) // 2
    return int(pt_crop[0] * scale + x_off), int(pt_crop[1] * scale + y_off)


def smooth_contour(cnt, n_points=120, smooth_window=11):
    """Resample to uniform spacing, then circular moving average.
    Result: organic curve between raw polygon and perfect ellipse."""
    pts = cnt.reshape(-1, 2).astype(np.float64)
    if len(pts) < 5:
        return cnt

    pts_closed = np.vstack([pts, pts[0:1]])
    diffs = np.diff(pts_closed, axis=0)
    dists = np.sqrt((diffs ** 2).sum(axis=1))
    cum = np.concatenate([[0], np.cumsum(dists)])
    total = cum[-1]
    if total < 1:
        return cnt

    targets = np.linspace(0, total, n_points, endpoint=False)
    resampled = np.zeros((n_points, 2))
    for d in range(2):
        resampled[:, d] = np.interp(targets, cum, pts_closed[:, d])

    half = smooth_window // 2
    pad = np.vstack([resampled[-half:], resampled, resampled[:half]])
    smoothed = np.zeros_like(resampled)
    for i in range(n_points):
        smoothed[i] = pad[i:i + smooth_window].mean(axis=0)

    return smoothed.astype(np.int32).reshape(-1, 1, 2)


def find_smooth_contours(gray_ch, center, fov_mask, n_levels=4, is_bright=True,
                         blur_sigma=10, max_radius=60):
    h, w = gray_ch.shape
    cx, cy = int(center[0]), int(center[1])
    cx, cy = max(0, min(cx, w - 1)), max(0, min(cy, h - 1))

    blurred = cv2.GaussianBlur(gray_ch, (0, 0), blur_sigma)

    roi = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(roi, (cx, cy), max_radius, 255, -1)
    roi = cv2.bitwise_and(roi, fov_mask)

    center_val = float(blurred[cy, cx])
    ring = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(ring, (cx, cy), max_radius, 255, -1)
    cv2.circle(ring, (cx, cy), int(max_radius * 0.7), 0, -1)
    ring = cv2.bitwise_and(ring, fov_mask)
    bg_pix = blurred[ring > 0]
    bg_val = float(np.mean(bg_pix)) if len(bg_pix) > 0 else 128.0
    diff = abs(center_val - bg_val)

    label = 'OD' if is_bright else 'Fovea'
    print(f"    {label}: center={center_val:.0f}, bg={bg_val:.0f}, diff={diff:.0f}")

    contours_out = []
    for i in range(1, n_levels + 1):
        if is_bright:
            frac = 1.0 - i / (n_levels + 1)
            thresh = int(bg_val + frac * (center_val - bg_val))
            _, bw = cv2.threshold(blurred, thresh, 255, cv2.THRESH_BINARY)
        else:
            frac = i / (n_levels + 1)
            thresh = int(center_val + frac * (bg_val - center_val))
            _, bw = cv2.threshold(blurred, thresh, 255, cv2.THRESH_BINARY_INV)

        bw = cv2.bitwise_and(bw, roi)
        # Slight blur on binary mask to soften edges before contour extraction
        bw = cv2.GaussianBlur(bw, (5, 5), 1.5)
        _, bw = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)

        cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        best, best_area = None, float('inf')
        for cnt in cnts:
            if cv2.pointPolygonTest(cnt, (float(cx), float(cy)), False) >= 0:
                a = cv2.contourArea(cnt)
                if 30 < a < best_area:
                    best, best_area = cnt, a

        if best is not None:
            smoothed = smooth_contour(best, n_points=120, smooth_window=11)
            contours_out.append(smoothed)
            r_approx = math.sqrt(best_area / math.pi)
            print(f"      level {i}: thresh={thresh}, area={best_area:.0f}, ~r={r_approx:.0f}")

    return contours_out, diff


def make_fallback_contours(center, base_radius, multipliers, elongation=1.1):
    """Smooth pseudo-ellipses as fallback when contrast is too low."""
    cx, cy = center
    contours = []
    for m in multipliers:
        r = max(4, base_radius * m)
        n_pts = 100
        angles = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
        rx, ry = r * elongation, r
        # Add subtle smooth perturbation for organic look
        np.random.seed(int(r * 100))
        perturb = 1.0 + 0.03 * np.sin(angles * 3) + 0.02 * np.sin(angles * 5 + 1.0)
        pts = np.column_stack([
            cx + rx * np.cos(angles) * perturb,
            cy + ry * np.sin(angles) * perturb
        ]).astype(np.int32).reshape(-1, 1, 2)
        contours.append(pts)
    return contours


for side in ["left", "right"]:
    c = all_coords[gr][side]
    od_512 = transform_point_to_512(c["od"], c, BASE, gr, side)
    fov_512 = transform_point_to_512(c["fovea"], c, BASE, gr, side)
    mid_512 = transform_point_to_512(c["midpoint"], c, BASE, gr, side)

    img = cv2.imread(os.path.join(
        BASE, gr, "preprocessing", "stage_5_clahe", "polar", f"{side}.png"))
    mask = cv2.imread(os.path.join(
        BASE, gr, "preprocessing", "stage_3_fov_mask", f"{side}.png"), cv2.IMREAD_GRAYSCALE)
    s2_img = cv2.imread(os.path.join(
        BASE, gr, "preprocessing", "stage_2_fov_crop_resize", f"{side}.png"))
    green_ch = s2_img[:, :, 1]

    print(f"\n=== {side} ===")
    print(f"  OD={od_512}, Fov={fov_512}, Mid={mid_512}")

    dist = np.linalg.norm(np.array(od_512, dtype=float) - np.array(fov_512, dtype=float))
    r_od = dist / 7.0
    r_fovea = r_od * 0.5

    # OD: 5 levels, generous radius
    od_contours, od_diff = find_smooth_contours(
        green_ch, od_512, mask, n_levels=5, is_bright=True,
        blur_sigma=10, max_radius=int(r_od * 2.5))

    # Fovea: 4 levels, tighter radius
    fov_contours, fov_diff = find_smooth_contours(
        green_ch, fov_512, mask, n_levels=4, is_bright=False,
        blur_sigma=5, max_radius=int(r_fovea * 3))

    if fov_diff < 5:
        print("    retrying Fovea with grayscale...")
        fov_contours, fov_diff = find_smooth_contours(
            cv2.cvtColor(s2_img, cv2.COLOR_BGR2GRAY), fov_512, mask,
            n_levels=4, is_bright=False, blur_sigma=5, max_radius=int(r_fovea * 3))
    if fov_diff < 5:
        print("    retrying Fovea with LAB L...")
        lab = cv2.cvtColor(s2_img, cv2.COLOR_BGR2LAB)
        fov_contours, fov_diff = find_smooth_contours(
            lab[:, :, 0], fov_512, mask,
            n_levels=4, is_bright=False, blur_sigma=5, max_radius=int(r_fovea * 3))

    if fov_diff < 5:
        print(f"    Fovea fallback: organic pseudo-ellipses")
        fov_contours = make_fallback_contours(fov_512, r_fovea,
                                               [0.7, 1.2, 1.8, 2.3], elongation=1.1)
    if od_diff < 5:
        od_contours = make_fallback_contours(od_512, r_od,
                                              [0.5, 0.9, 1.3, 1.8, 2.2], elongation=1.15)

    print(f"  dist={dist:.1f}, r_od={r_od:.1f}, r_fov={r_fovea:.1f}")
    print(f"  OD: {len(od_contours)} rings, Fov: {len(fov_contours)} rings")

    vis = img.copy()

    od_color = (130, 165, 130)
    fov_color = (145, 145, 145)

    for cnt in od_contours:
        cv2.drawContours(vis, [cnt], -1, od_color, 1, cv2.LINE_AA)
    for cnt in fov_contours:
        cv2.drawContours(vis, [cnt], -1, fov_color, 1, cv2.LINE_AA)

    cv2.circle(vis, fov_512, 3, (0, 0, 220), -1, cv2.LINE_AA)
    cv2.circle(vis, od_512, 3, (0, 220, 0), -1, cv2.LINE_AA)
    cv2.circle(vis, mid_512, 2, (0, 200, 0), -1, cv2.LINE_AA)

    vis[mask == 0] = 0

    out_dir = os.path.join(BASE, gr, "preprocessing", "stage_6_augmentation", "1_rotation")
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, f"{side}_contours_v2.png"), vis)
    print(f"  -> saved {side}_contours_v2.png")
