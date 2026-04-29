import { C } from '../data';
import { Sec, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

const codeStyle = {
  fontFamily: 'monospace',
  background: 'var(--color-background-secondary,#f5f5f3)',
  padding: '8px 12px', borderRadius: 6, fontSize: 11,
  lineHeight: 1.6, marginTop: 6, display: 'block',
};

const formulaStyle = {
  fontFamily: 'monospace',
  background: 'var(--color-background-secondary,#f5f5f3)',
  padding: '10px 16px', borderRadius: 6, fontSize: 12,
  textAlign: 'center', margin: '8px 0', display: 'block',
};

function StageTag({ label, color = 'teal' }) {
  return (
    <span style={{
      padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 700,
      background: C[color + 'Bg'] || C.tealBg, color: C[color + 'T'] || C.tealT,
      marginRight: 6,
    }}>
      {label}
    </span>
  );
}

// ── Section 1: Overview ───────────────────────────────────────────────────────
function Overview() {
  const { t } = useLang();
  return (
    <Sec title={t('methods.overview')}>
      <p style={{ fontSize: 12, lineHeight: 1.75, margin: '0 0 10px 0' }}>
        The preprocessing pipeline comprises <strong>8 ordered stages</strong>. Each stage uses a technique
        specifically adapted for retinal fundus image characteristics — circular FOV, radial illumination
        gradients, bilateral eye laterality, and the need to preserve microvascular features for DR
        classification.
      </p>
      <p style={{ fontSize: 12, lineHeight: 1.75, margin: 0 }}>
        Novel scientific contributions: canonical flip (Stage 0), OD-fovea rotation (Stage 1), isotropic resize
        (Stage 2), FOV mask (Stage 3), adaptive flat-field (Stage 4), dual-constraint CLAHE (Stage 5), and
        integrated augmentation (Stage 6). Stage 7 (dataset-specific normalize → 4ch tensor) is standard.
      </p>
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 12 }}>
        {[
          { label: 'Stage 0', name: 'Canonical Flip', color: 'teal', novel: true },
          { label: 'Stage 1', name: 'OD-Fovea Rotation', color: 'teal', novel: true },
          { label: 'Stage 2', name: 'FOV Crop + Isotropic Resize', color: 'teal', novel: true },
          { label: 'Stage 3', name: 'FOV Mask Generation', color: 'teal', novel: true },
          { label: 'Stage 4', name: 'Adaptive Flat-Field', color: 'teal', novel: true },
          { label: 'Stage 5', name: 'Dual-Constraint CLAHE', color: 'teal', novel: true },
          { label: 'Stage 6', name: 'Integrated Augmentation', color: 'teal', novel: true },
          { label: 'Stage 7', name: 'Dataset-Specific Normalize', color: 'gray', novel: false },
        ].map(s => (
          <div key={s.label} style={{
            padding: '6px 10px', borderRadius: 6, fontSize: 10,
            background: s.novel ? C.tealBg : C.grayBg,
            color: s.novel ? C.tealT : C.grayT,
            border: `1px solid ${s.novel ? C.teal : C.gray}30`,
          }}>
            <div style={{ fontWeight: 700 }}>{s.label}</div>
            <div style={{ marginTop: 1 }}>{s.name}</div>
            {s.novel && <div style={{ fontSize: 9, marginTop: 2, opacity: 0.75 }}>Novel</div>}
          </div>
        ))}
      </div>
    </Sec>
  );
}

// ── Section 2: Stage 0 — Canonical Flip ─────────────────────────────────────
function Stage0a() {
  return (
    <Sec title="Stage 0 — Canonical Orientation Flip">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stage 0" /><StageTag label="Novel" color="green" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Left-eye (OS) images are horizontally flipped to right-eye (OD) orientation so the optic disc
        is consistently positioned on the right side of every image in the dataset.
      </p>
      <ImageWithTooltip
        src="/pipeline/dr04/preprocessing/stage_0_canonical_flip/left.png"
        caption="Left-eye image after canonical flip — optic disc now positioned on the right side, matching right-eye orientation. All training images are normalised to this canonical layout. (DR Grade 4 example)"
        tooltip="tooltip.method_flip"
      />
      <div style={{ display: 'flex', gap: 12, marginBottom: 10 }}>
        <div style={{ flex: 1, padding: '8px 10px', background: C.grayBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.grayT, marginBottom: 4 }}>Standard CV approach</div>
          <div style={{ fontSize: 11, color: C.grayT, lineHeight: 1.6 }}>
            Horizontal flip as <em>random augmentation</em> — applied probabilistically during training.
            No anatomical meaning.
          </div>
        </div>
        <div style={{ flex: 1, padding: '8px 10px', background: C.tealBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, marginBottom: 4 }}>Our adaptation</div>
          <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>
            <em>Deterministic</em> flip based on eye laterality metadata (<code>_left</code> / <code>_right</code> filename suffix in EyePACS). Applied once at load time, not during augmentation.
          </div>
        </div>
      </div>
      <Note>
        Without canonical flip, the CNN must learn separate feature detectors for OD-left and OD-right
        spatial configurations — effectively halving the training data per anatomical layout. Deterministic
        flip ensures all ~35,126 training images share the same retinal topology.
      </Note>
      <code style={codeStyle}>
        {`# Single operation — the decision logic is the contribution\nif eye_side == 'left':\n    image = cv2.flip(image, 1)  # horizontal flip`}
      </code>
    </Sec>
  );
}

// ── Section 3: Stage 1 — OD-Fovea Rotation ──────────────────────────────────
function Stage0b() {
  return (
    <Sec title="Stage 1 — OD-Fovea Rotation Normalization">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stage 1" /><StageTag label="Novel" color="green" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Detects the optic disc (brightest region) and fovea (darkest region within annular search zone),
        then rotates the image so the OD→fovea axis is horizontal. Normalises retinal orientation across
        different cameras and acquisition protocols.
      </p>

      <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
        <div style={{ flex: 1 }}>
          <ImageWithTooltip
            src="/pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/od/left.png"
            caption="Optic disc detection: green-channel Gaussian blur (σ=15) → 97th percentile threshold → morphological cleanup → centroid of largest component."
            tooltip="tooltip.method_odfovea"
          />
        </div>
        <div style={{ flex: 1 }}>
          <ImageWithTooltip
            src="/pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/fovea/left.png"
            caption="Fovea detection within annular search region (1.5–3.5 OD diameters from OD centroid). Fovea = darkest point within this region."
            tooltip="tooltip.method_search"
          />
        </div>
      </div>

      <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 6 }}>Algorithm — 5 steps</div>
      <ol style={{ fontSize: 11, lineHeight: 1.75, paddingLeft: 20, margin: '0 0 12px 0' }}>
        <li><strong>OD detection:</strong> Gaussian blur (σ=15) on green channel → 97th percentile threshold → morphological cleanup → centroid of largest component</li>
        <li><strong>Fovea detection:</strong> Gaussian blur (σ=25) → search in annular region 1.5–3.5 OD diameters from OD → darkest point</li>
        <li><strong>Rotation:</strong> <code>cv2.warpAffine</code> with <code>BORDER_REFLECT</code> to align OD→fovea axis horizontally</li>
        <li><strong>Confidence check:</strong> skip rotation if OD radius &lt; 10px or OD–fovea distance ratio outside [1.0, 5.0]; fall back to identity transform</li>
        <li><strong>Adaptive σ output:</strong> passes rotation uncertainty σ<sub>θ</sub> to Stage 6 augmentation</li>
      </ol>

      <code style={formulaStyle}>
        σ_θ = arctan(√(r_OD² + r_fovea²) / distance_OD_fovea)
      </code>

      <div style={{ display: 'flex', gap: 12 }}>
        <div style={{ flex: 1, padding: '8px 10px', background: C.grayBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.grayT, marginBottom: 4 }}>Standard approach</div>
          <div style={{ fontSize: 11, color: C.grayT, lineHeight: 1.6 }}>No rotation normalisation. Random ±15° augmentation used. Camera-to-camera orientation variation treated as noise.</div>
        </div>
        <div style={{ flex: 1, padding: '8px 10px', background: C.tealBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, marginBottom: 4 }}>Our adaptation</div>
          <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>Two-landmark detection with annular fovea search prior. Deterministic rotation to canonical axis. Adaptive σ passes uncertainty to augmentation stage.</div>
        </div>
      </div>
    </Sec>
  );
}

// ── Section 4: Stages 2–3 — FOV Crop + Isotropic Resize + FOV Mask ──────────
function Stage1() {
  return (
    <Sec title="Stages 2–3 — FOV Crop + Isotropic Resize + FOV Mask">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stages 2–3" /><StageTag label="Novel" color="green" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Detects the circular FOV boundary, removes black border regions, and resizes to 512×512. Eliminates
        device-specific border artifacts that vary substantially between camera models.
      </p>
      <ImageWithTooltip
        src="/pipeline/dr04/preprocessing/stage_2_fov_crop_resize/left.png"
        caption="After FOV detection, isotropic resize to 512×512, and centred zero-padding. Black border regions removed; aspect ratio preserved so border pixels no longer consume the CNN receptive field."
        tooltip="tooltip.method_fov"
      />
      <div style={{ display: 'flex', gap: 12, marginBottom: 10 }}>
        <div style={{ flex: 1, padding: '8px 10px', background: C.grayBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.grayT, marginBottom: 4 }}>Standard method</div>
          <div style={{ fontSize: 11, color: C.grayT, lineHeight: 1.6 }}>Hough circle detection. Sensitive to image quality, fails on non-circular FOV or partial occlusions.</div>
        </div>
        <div style={{ flex: 1, padding: '8px 10px', background: C.tealBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, marginBottom: 4 }}>Our adaptation</div>
          <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>PIL foreground edge sampling: samples edge columns, thresholds at <code>max_background + 10</code>. Fallback: centre-square crop. Robust to non-circular FOV.</div>
        </div>
      </div>
      <Note>
        Target resolution 512×512: balances microaneurysm detection detail (diameter ~5–15px at this resolution)
        against GPU memory (RTX 3060, 12 GB) at batch size 16.
      </Note>
    </Sec>
  );
}

// ── Section 5: Stage 4 — Flat-Field Correction ──────────────────────────────
function Stage2() {
  return (
    <Sec title="Stage 4 — Flat-Field Correction">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stage 4" /><StageTag label="Novel" color="green" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Removes low-frequency illumination gradients (brighter centre, darker periphery) introduced by the
        fundus camera optics. Preserves all vessel and lesion detail.
      </p>
      <ImageWithTooltip
        src="/pipeline/dr04/preprocessing/stage_4_flatfield/left.png"
        caption="After flat-field correction (adaptive σ = 0.07·D). Radial illumination gradient removed; vessel and lesion structures preserved with uniform illumination across the field."
        tooltip="tooltip.method_flatfield"
      />
      <code style={formulaStyle}>
        corrected = image − GaussianBlur(image, σ=0.07×D) + 128  {'  '}(D = FOV diameter)
      </code>
      <div style={{ display: 'flex', gap: 12, marginBottom: 10 }}>
        <div style={{ flex: 1, padding: '8px 10px', background: C.grayBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.grayT, marginBottom: 4 }}>Standard approach</div>
          <div style={{ fontSize: 11, color: C.grayT, lineHeight: 1.6 }}>Most DR pipelines skip illumination correction entirely. Some use global histogram normalisation (loses spatial gradient info).</div>
        </div>
        <div style={{ flex: 1, padding: '8px 10px', background: C.tealBg, borderRadius: 6 }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, marginBottom: 4 }}>Our adaptation</div>
          <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>Adaptive σ = 0.07×D (D = FOV diameter). Scale-invariant adaptive σ (replaces fixed σ=45). Captures illumination envelope for any FOV size while preserving vessels (~5–15px) and lesions (&lt;30px).</div>
        </div>
      </div>
      <Note>
        Adaptive σ = 0.07×D selection: σ is proportional to FOV diameter D, making it scale-invariant
        across camera models. At D=512px (typical after resize), σ≈36px. This captures the illumination
        envelope while fully preserving diagnostic structures. The +128 offset re-centres the output to [0,255] range.
      </Note>
    </Sec>
  );
}

// ── Section 6: Stage 5 — Upgraded CLAHE ─────────────────────────────────────
function Stage3() {
  return (
    <Sec title="Stage 5 — Upgraded CLAHE (Dual-Constraint)">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stage 5" /><StageTag label="Novel" color="green" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Adaptive histogram equalisation on the LAB L-channel with a dual-constraint clip limit and
        stochastic application during training. Three key differences from standard OpenCV CLAHE.
      </p>

      <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
        <div style={{ flex: 1 }}>
          <ImageWithTooltip
            src="/pipeline/dr04/preprocessing/stage_5_clahe/left.png"
            caption="After dual-constraint CLAHE on the LAB L-channel. Local contrast enhanced uniformly without over-enhancement near the optic disc."
            tooltip="tooltip.method_clahe_cmp"
          />
        </div>
        <div style={{ flex: 1 }}>
          <ImageWithTooltip
            src={process.env.PUBLIC_URL + '/results/exp2/13_exp2_clahe_sensitivity.png'}
            caption="CLAHE parameter sensitivity on IDRiD. X-axis: global threshold. Y-axis: clip factor. ★ marks optimal parameter pair for DR grade 1 (clip_factor=2.5, gt=0.03)."
            tooltip="tooltip.method_clahe_sens"
          />
        </div>
      </div>

      <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 6 }}>Three key innovations</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 12 }}>
        {[
          {
            n: '1', title: 'Dual-constraint clip limit',
            body: 'Standard CLAHE uses a single clip limit. Our implementation uses:',
            formula: 'CL = min(clip_factor × tile_area / 256,  global_threshold × tile_area)',
            note: 'The global_threshold cap prevents over-enhancement near the optic disc (bright, large area). The clip_factor term controls local contrast. Both constraints must be satisfied.',
            color: 'teal',
          },
          {
            n: '2', title: 'Custom tile-by-tile implementation with bilinear interpolation',
            body: 'Full control over redistribution algorithm. Enables the dual-constraint logic that cv2.createCLAHE does not support.',
            color: 'blue',
          },
          {
            n: '3', title: 'Stochastic application — 80% probability during training',
            body: 'Applied to 80% of training batches, never at inference. Acts as a data augmentation / regularisation mechanism, preventing over-reliance on CLAHE-specific features.',
            color: 'purple',
          },
        ].map(item => (
          <div key={item.n} style={{ padding: '8px 12px', background: C[item.color + 'Bg'], borderRadius: 6, borderLeft: `3px solid ${C[item.color]}` }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: C[item.color + 'T'], marginBottom: 3 }}>{item.n}. {item.title}</div>
            <div style={{ fontSize: 11, color: C[item.color + 'T'], lineHeight: 1.6 }}>{item.body}</div>
            {item.formula && <code style={{ ...codeStyle, background: `${C[item.color]}15`, color: C[item.color + 'T'], marginTop: 4 }}>{item.formula}</code>}
            {item.note && <div style={{ fontSize: 10, color: C[item.color + 'T'], marginTop: 4, opacity: 0.8 }}>{item.note}</div>}
          </div>
        ))}
      </div>

      <div style={{ fontSize: 11, fontWeight: 600, marginBottom: 4 }}>Optimal parameters (Exp 2 sweep on IDRiD)</div>
      <div style={{ display: 'flex', gap: 8 }}>
        {[
          { grade: 'DR Grade 1', cf: '2.5', gt: '0.03', note: 'Mild NPDR — subtle microaneurysms benefit from stronger enhancement' },
          { grade: 'DR Grade 2', cf: '2.0', gt: '0.03', note: 'Moderate NPDR — more visible features, lower clip needed' },
        ].map(p => (
          <div key={p.grade} style={{ flex: 1, padding: '8px 10px', background: C.amberBg, borderRadius: 6 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: C.amberT, marginBottom: 4 }}>{p.grade}</div>
            <div style={{ fontSize: 11, color: C.amberT }}>clip_factor = <strong>{p.cf}</strong>, global_threshold = <strong>{p.gt}</strong></div>
            <div style={{ fontSize: 10, color: C.amberT, marginTop: 3, opacity: 0.8 }}>{p.note}</div>
          </div>
        ))}
      </div>
    </Sec>
  );
}

// ── Section 7: Stage 7 — Dataset-Specific Normalization ─────────────────────
function Stage7() {
  return (
    <Sec title="Stage 7 — Dataset-Specific Normalization → 4ch Tensor">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stage 7" color="gray" /><StageTag label="Standard (in both configs)" color="gray" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Channel-wise normalisation using dataset-specific statistics (not fixed ImageNet). Stack RGB + FOV mask
        → 4-channel (RGBM) tensor. Required for pre-trained ResNet-50 and EfficientNet-B3/B4 weight initialisation.
      </p>
      <code style={formulaStyle}>
        pixel_norm = (pixel − mean_dataset) / std_dataset<br />
        channels: R, G, B, FOV_mask  (4ch)<br />
        mean/std: computed from EyePACS training split
      </code>
      <Note>
        Stage 7 is always the final stage. Dataset-specific statistics (not fixed ImageNet) and
        4-channel output (RGB + FOV mask). Baseline uses 3ch with ImageNet statistics. Present in both
        Baseline and Pipeline configurations — it is not a novel contribution.
      </Note>
    </Sec>
  );
}

// ── Section 8: Stage 6 — Augmentation ────────────────────────────────────────
function Stage5() {
  return (
    <Sec title="Stage 6 — Integrated Augmentation (Train Only)">
      <div style={{ marginBottom: 10 }}>
        <StageTag label="Stage 6" /><StageTag label="Novel" color="green" />
      </div>
      <p style={{ fontSize: 12, lineHeight: 1.7, margin: '0 0 10px 0' }}>
        Applied only during training — never at inference. Key differences from standard augmentation
        pipelines for natural images.
      </p>
      <ImageWithTooltip
        src="/pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_variant_A.png"
        caption="Augmentation example — 360° rotation applied (only valid because circular FOV has no black corners). Stage 6 also applies scale, shear, PCA colour jitter, and brightness/contrast — all composed into a single affine pass."
        tooltip="tooltip.method_augment"
      />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 10 }}>
        {[
          { aspect: '360° rotation', standard: '±15° (avoids black corners)', ours: 'Full 360° — circular FOV means any rotation is valid. No black corners appear.' },
          { aspect: 'Rotation magnitude', standard: 'Fixed ±15°', ours: 'Adaptive: σ_θ from Stage 1 confidence. Higher OD/fovea detection uncertainty → larger rotation range.' },
          { aspect: 'Colour jitter', standard: 'Random brightness/contrast/saturation', ours: 'PCA colour jitter (à la AlexNet): perturbation along principal colour axes preserves colour correlations.' },
          { aspect: 'Transform pipeline', standard: 'Sequential (multiple interpolations)', ours: 'Composed into single affine matrix — single bilinear interpolation pass. Reduces cumulative resampling artefacts.' },
        ].map((r, i) => (
          <div key={i} style={{ display: 'flex', gap: 0, borderRadius: 5, overflow: 'hidden', border: '1px solid var(--color-border-tertiary,#eee)' }}>
            <div style={{ width: 140, minWidth: 140, padding: '6px 8px', background: 'var(--color-background-secondary,#f7f7f5)', fontSize: 10, fontWeight: 600 }}>{r.aspect}</div>
            <div style={{ flex: 1, padding: '6px 8px', fontSize: 11, borderLeft: '1px solid var(--color-border-tertiary,#eee)' }}><span style={{ color: C.gray }}>Standard: </span>{r.standard}</div>
            <div style={{ flex: 1, padding: '6px 8px', fontSize: 11, background: '#E6F9F1', borderLeft: '1px solid var(--color-border-tertiary,#eee)' }}><span style={{ color: C.teal, fontWeight: 600 }}>Ours: </span>{r.ours}</div>
          </div>
        ))}
      </div>
    </Sec>
  );
}

// ── Section 9: Comparison Table ───────────────────────────────────────────────
function ComparisonTable() {
  const { t } = useLang();
  const rows = [
    { stage: 'S0: Canonical Flip', standard: 'Random H-flip (augmentation)', ours: 'Deterministic flip by eye metadata', innovation: 'Anatomical consistency' },
    { stage: 'S1: OD-Fovea Rotation', standard: 'None or random rotation', ours: 'Two-landmark detection + rotate to canonical axis', innovation: 'Annular fovea search prior' },
    { stage: 'S2: FOV Crop + Isotropic Resize', standard: 'Stretch-resize to target size', ours: 'PIL foreground edge sampling + isotropic resize + zero-pad', innovation: 'Preserves aspect ratio' },
    { stage: 'S3: FOV Mask', standard: 'None (discarded after crop)', ours: 'Binary FOV mask → 4th input channel', innovation: 'Spatial boundary for CNN (novel)' },
    { stage: 'S4: Flat-Field', standard: 'None (most pipelines skip)', ours: 'Blur subtraction, adaptive σ=0.07·D, per-channel', innovation: 'Scale-invariant σ (novel)' },
    { stage: 'S5: CLAHE', standard: 'cv2.createCLAHE (fixed clip limit)', ours: 'Dual-constraint + stochastic 80%', innovation: 'Global cap + regularisation' },
    { stage: 'S6: Augmentation', standard: 'Separate transforms, ±15° rotation', ours: 'Integrated affine, 360°, adaptive σ, PCA jitter', innovation: 'Circular FOV enables full rotation' },
    { stage: 'S7: Normalization', standard: 'ImageNet channel-wise (μ, σ), 3ch', ours: 'Dataset-specific μ/σ, 4ch (RGB + FOV mask)', innovation: 'Dataset-specific stats + 4ch input' },
  ];

  return (
    <Sec title={t('methods.comparison')}>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--color-border-secondary,#ccc)' }}>
              <th style={{ padding: '6px 8px', textAlign: 'left', fontWeight: 600, minWidth: 110 }}>Stage</th>
              <th style={{ padding: '6px 8px', textAlign: 'left', fontWeight: 600, background: C.grayBg }}>Standard Approach</th>
              <th style={{ padding: '6px 8px', textAlign: 'left', fontWeight: 600, background: '#E6F9F1' }}>Our Adaptation</th>
              <th style={{ padding: '6px 8px', textAlign: 'left', fontWeight: 600, background: '#FFF8E6' }}>Key Innovation</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} style={{ borderBottom: '1px solid var(--color-border-tertiary,#eee)' }}>
                <td style={{ padding: '6px 8px', fontWeight: 500, whiteSpace: 'nowrap' }}>{r.stage}</td>
                <td style={{ padding: '6px 8px', background: i % 2 === 0 ? C.grayBg : `${C.grayBg}80` }}>{r.standard}</td>
                <td style={{ padding: '6px 8px', background: i % 2 === 0 ? '#E6F9F1' : '#F0FAF6', color: C.tealT }}>{r.ours}</td>
                <td style={{ padding: '6px 8px', background: i % 2 === 0 ? '#FFF8E6' : '#FFFBF0', color: C.amberT, fontWeight: 500 }}>{r.innovation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Note>
        Stages S0, S1, S2, S3, S4, S5, and S6 constitute the seven novel scientific contributions of the
        8-stage pipeline. Stage S7 (dataset-specific normalize + 4ch) is standard and present in both
        baseline and full pipeline configurations.
      </Note>
    </Sec>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────
export default function ModelMethods() {
  return (
    <div>
      <Overview />
      <Stage0a />
      <Stage0b />
      <Stage1 />
      <Stage2 />
      <Stage3 />
      <Stage7 />
      <Stage5 />
      <ComparisonTable />
    </div>
  );
}
