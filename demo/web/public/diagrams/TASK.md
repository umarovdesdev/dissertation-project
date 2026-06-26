# TASK.md — Three Architecture Diagrams for Dissertation Defense

**Date:** 2026-04-26
**Candidate:** Yesmukhamedov N.S., IITU
**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification

---

## 1. Final understanding of the task

We need to produce **three separate diagrams** in `.svg` format (later converted to `.png` for the defense presentation).

### 1.1 Agreed parameters

| Parameter | Value |
|-----------|-------|
| Label language | English (only) |
| Style | Strict academic — thin lines, rectangles, no icons or illustrations |
| Background | White |
| Contrast | ≥ 4.5:1 on white (WCAG AA) |
| Format | SVG → later converted to PNG |
| Location | `demo/web/public/diagrams/` |

### 1.2 Conceptual structure of the three diagrams

| # | Abstraction level | What it reveals | What stays a "black box" |
|---|---|---|---|
| 1 | Highest — experimental design | 2×2 factorial: {Baseline, Pipeline} × {ResNet-50, EfficientNet-B3} → 4 configurations (Config A/B/C/D) → Results | Internals of preprocessing, internals of CNN, aggregation, explainability |
| 2 | System level — full end-to-end architecture | Input (eye pair) → preprocessing as a **single combined block** → output (processed image + FOV mask) → CNN → Patient-Level Aggregation Φ → Prediction → separate Grad-CAM branch | Internals of the 8 preprocessing stages (that is level №3) |
| 3 | Preprocessing level — detail of every stage | One large poster with 8 panels (one per Stage 0–7), parameters, formulas, tensor types | — (this is the deepest level of detail) |

**The "splitting" concept:** the existing `pipeline_diagram.svg` (the old monolith, which mixed the system and per-stage levels) is split into two:
- the system part → Diagram №2 (with Patient-Level Aggregation and Grad-CAM added)
- the per-stage part → Diagram №3 (poster with 8 panels)

---

## 2. Sources of truth

| File | What it provides |
|------|------------------|
| `CLAUDE.md` (root) | Central thesis: model = preprocessing + CNN |
| `thesis/governance/CENTRAL_THESIS.md` | Thesis statement in one paragraph |
| `demo/web/public/diagrams/system_architecture_specification.md` | Full architecture specification (Sections 1–14) |
| `demo/web/public/diagrams/pipeline_specification.md` | Detailed specification of the 8 preprocessing stages |
| `demo/web/public/diagrams/general.png` | User's reference for Diagram №1 |
| `demo/web/public/diagrams/pipeline_diagram.svg` | Existing monolith — conceptually split into №2 and №3 |

---

## 3. Diagram №1 — Maximally Abstract Architecture (2×2 Factorial)

**File:** `demo/web/public/diagrams/01_abstract_model_architecture.svg`

### 3.1 Structure (based on the reference `general.png`)

```
                            ┌─────────┐
                            │  Image  │
                            └────┬────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
        ┌───────────────┐                ┌───────────────┐
        │   Baseline    │                │   Pipeline    │
        │  preprocessing│                │  preprocessing│
        └───┬─────────┬─┘                └─┬─────────┬───┘
       Cfg A│         │Cfg C        Cfg B  │         │Cfg D
            │         └──────┐    ┌────────┘         │
            ▼                ▼    ▼                  ▼
     ┌────────────┐                          ┌──────────────────┐
     │ ResNet-50  │                          │ EfficientNet-B3  │
     └─────┬──────┘                          └────────┬─────────┘
           │                                          │
           └──────────────┬───────────────────────────┘
                          ▼
                    ┌──────────┐
                    │  Results │
                    └──────────┘
```

### 3.2 Block contents

- **Image** — Raw fundus photograph (a single generalized block).
- **Baseline preprocessing** — Stretch-resize 512×512 + ImageNet normalize (3 channels).
- **Pipeline preprocessing** — Full Pipeline (8 stages, 4 channels). Expanded in Diagrams №2 and №3.
- **ResNet-50** — CNN backbone, ImageNet-pretrained, 4-channel input adapted.
- **EfficientNet-B3** — CNN backbone, ImageNet-pretrained, 4-channel input adapted.
- **Results** — Aggregated metrics (F1 / AUC / κ / accuracy) for all 4 configurations.

### 3.3 Path labels

Each of the 4 edges (from preprocessing to backbone) carries a configuration label:
- Baseline → ResNet-50 = **Config A**
- Pipeline → ResNet-50 = **Config B**
- Baseline → EfficientNet-B3 = **Config C**
- Pipeline → EfficientNet-B3 = **Config D**

### 3.4 Visual features

- 6 rectangles + 4 path labels.
- Color coding:
  - Image — graphite gray.
  - Baseline preprocessing — slate gray (control branch).
  - Pipeline preprocessing — dark green (experimental branch).
  - CNN backbones — dark blue.
  - Results — wine red.
- Layout: symmetric "diamond".
- Font: sans-serif (Inter / Helvetica / Arial), 16pt for blocks, 12pt for path labels.

### 3.5 What we do NOT show

- Patient-Level Aggregation (that is level №2).
- Grad-CAM (that is level №2).
- Tensor dimensions (that is level №2 and №3).
- Preprocessing stages (those are levels №2 and №3).

---

## 4. Diagram №2 — Full System Architecture (End-to-End)

**File:** `demo/web/public/diagrams/02_system_architecture.svg`

### 4.1 Goal

Show the full end-to-end system architecture according to `system_architecture_specification.md` (Section 11 "Full Pipeline Flow"). Preprocessing here is a **single combined block** (its contents are expanded in Diagram №3).

### 4.2 Structure

```
                    Patient Record (bilateral pair)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │  I_left (BGR)   │             │  I_right (BGR)  │
     │  s_left         │             │  s_right        │
     └────────┬────────┘             └────────┬────────┘
              │                               │
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │  Preprocessing  │             │  Preprocessing  │
     │   𝒫 (all 8  │             │   𝒫 (all 8  │
     │     stages)     │             │     stages)     │
     └────────┬────────┘             └────────┬────────┘
              │                               │
       Processed image (RGB) +         Processed image (RGB) +
       FOV mask (4 channels,           FOV mask (4 channels,
       512×512, float32)                512×512, float32)
              │                               │
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │  CNN Backbone   │ ◄── shared ─►│  CNN Backbone   │
     │  (ResNet-50 or  │              │  (ResNet-50 or  │
     │  EfficientNet)  │              │  EfficientNet)  │
     └────────┬────────┘             └────────┬────────┘
              │                               │
        f_L ∈ ℝ^d                       f_R ∈ ℝ^d
              │                               │
              └───────────────┬───────────────┘
                              ▼
                  ┌───────────────────────┐
                  │  Patient-Level        │
                  │  Aggregation Φ        │
                  │  (max-grade)          │
                  └───────────┬───────────┘
                              ▼
                  ┌───────────────────────┐
                  │  Prediction Layer g   │
                  │  softmax → ŷ, p̂      │
                  └───────────┬───────────┘
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
            ┌─────────┐         ┌──────────────────┐
            │Diagnosis │         │ Grad-CAM         │
            │ ŷ ∈{0..4}│         │ Explainability   │
            │ ŷ_ref    │         │ → heatmap        │
            └─────────┘         │ → ALO, IoU       │
                                └──────────────────┘
```

### 4.3 What we show

- **Bilateral input:** pair of images (left/right eye) + laterality metadata.
- **Preprocessing 𝒫 as a single block** per eye. Label: "Pipeline (8 stages, see Diagram №3)".
- **Output of preprocessing:** processed RGB image + FOV mask = 4-channel tensor (4×512×512, float32).
- **CNN backbone:** shared weights for both eyes.
- **Per-eye feature vectors** f_L, f_R.
- **Patient-Level Aggregation Φ:** max-grade (the primary strategy).
- **Prediction layer g:** softmax → ŷ, p̂.
- **Diagnosis output:** DR grade + binary decision (referable DR).
- **Grad-CAM branch:** a separate branch from the prediction layer (or from feature maps), showing heatmap + ALO/IoU metrics.

### 4.4 Visual features

- Layout: vertical (top-down), symmetric about the center for the bilateral pair.
- Preprocessing — **a single rectangle** per eye (no expansion of the 8 stages).
- After preprocessing, the arrow carries a tensor-format label: `(4, 512, 512), float32`.
- Patient-Level Aggregation — a highlighted block at the center.
- Grad-CAM branch — dashed lines (post-hoc, not part of the main inference path).
- Color coding (consistent with №1 and №3):
  - Input — graphite.
  - Preprocessing block — dark green.
  - CNN backbones — dark blue.
  - Aggregation — amber.
  - Prediction — wine red.
  - Grad-CAM branch — slate-blue dashed.

### 4.5 What we do NOT show

- Internals of the 8 preprocessing stages (that is Diagram №3).
- Baseline vs Pipeline comparison (that is Diagram №1).
- Details of the MLP head PatientHead (Section 7.4) — it is not in the active design.
- Specific feature-dimension values d (2048 / 1536) — kept abstract as "d".

---

## 5. Diagram №3 — Detailed Per-Stage Preprocessing Diagram

**File:** `demo/web/public/diagrams/03_preprocessing_stages_detailed.svg` (one diagram, Variant A)

### 5.1 Goal

Open the "black box" of preprocessing 𝒫 from Diagram №2 — show all 8 stages with the details of each.

### 5.2 Format

**A single SVG poster**, divided into 8 panels arranged in a 4×2 grid (4 columns × 2 rows) or 2×4 (2 columns × 4 rows) — the choice is made at implementation time based on aspect ratio.

### 5.3 Contents of each panel

| Element | Description |
|---------|-------------|
| Header | `Stage N — Name` |
| Input | Tensor format and dimensions (e.g., `RGB uint8, H×W×3`) |
| Internal operations | 2–4 operation steps (e.g., for Stage 1: OD detection → Fovea detection → Compute angle θ → Rotate by −θ) |
| Output | Tensor format and dimensions |
| Key parameters | Default values (σ = 0.07·D; clip_factor = 2.0; tile_grid = 8×8; etc.) |
| Mode | always-on / train-only / stochastic |

### 5.4 The eight panels

- **Stage 0** — Canonical Flip (always-on)
- **Stage 1** — OD-Fovea Rotation Normalization (always-on, conditional)
- **Stage 2** — FOV Crop + Isotropic Resize → 512×512 (always-on)
- **Stage 3** — FOV Mask Generation (always-on, side branch for the 4th channel)
- **Stage 4** — Adaptive Flat-Field Correction, σ = 0.07·D (always-on)
- **Stage 5** — Dual-Constraint CLAHE, LAB L-channel (always-on, stochastic at train)
- **Stage 6** — Augmentation, affine + ColorJitter + noise/JPEG (train only)
- **Stage 7** — Dataset-Specific Normalize + FOV Mask Append (always-on)

### 5.5 Visual features

- Each panel — a bordered rectangle, with a structured internal layout (Header / Input / Operations / Output / Params).
- Between panels — arrows indicating execution order (if the grid allows, a numbered line 0→1→2→…→7).
- Stage 6 (train-only) — outlined with a dashed border.
- Stage 3 (mask side branch) — drawn in a different color (teal), with a dashed arrow to Stage 7 (showing that the mask is appended at the end).
- Color coding (consistent with №2):
  - Geometry stages (0–3) — teal.
  - Photometric stages (4–5) — orange.
  - Train-only (6) — purple, dashed.
  - Normalization (7) — wine red.
- Below — a compact legend (always-on / train-only / stochastic / data flow).

---

## 6. Unified color palette

| Purpose | HEX | Contrast on white |
|---------|-----|-------------------|
| Input (`Image`, raw tensor) — graphite | `#1f2937` | 14.7:1 |
| Baseline preprocessing — slate gray | `#475569` | 8.6:1 |
| Pipeline preprocessing — dark green | `#166534` | 8.4:1 |
| Geometry stages (0–3) — teal | `#0d9488` | 4.7:1 |
| Photometric stages (4–5) — orange | `#c2410c` | 5.6:1 |
| Train-only / stochastic (6) — purple | `#6d28d9` | 7.4:1 |
| Normalization (7) / Results / Prediction — wine red | `#9f1239` | 8.5:1 |
| CNN backbones (ResNet-50, EfficientNet-B3) — dark blue | `#1e3a8a` | 11.2:1 |
| Patient-Level Aggregation — amber | `#b45309` | 5.0:1 |
| Grad-CAM branch — slate-blue dashed | `#475569` | 8.6:1 |
| Label text | `#111827` | 17.3:1 |
| Arrows | `#000000` | 21:1 |
| Block fills | corresponding color at 12–18% alpha | — |

All colors meet contrast ≥ 4.5:1 on white background (WCAG AA).

---

## 7. Technical details

- **Format:** plain SVG (XML written by hand), no dependency on external fonts (sans-serif fallback).
- **viewBox:**
  - №1: 1600×900 (16:9 for a slide).
  - №2: 1200×1600 (vertical — the bilateral pair requires height).
  - №3: 1920×1080 for a 4×2 grid OR 1080×1920 for a 2×4 grid.
- **Toolchain:** SVG is written by hand, with no dependency on Inkscape/Figma.
- **PNG conversion:** later, via ImageMagick / Inkscape CLI / online, exporting at 2× DPI.

---

## 8. Agreed decisions

All questions from the previous iteration have been resolved:

| Question | Decision |
|----------|----------|
| Label language | English |
| Style | Strict academic |
| Diagram №1: Config A/B/C/D on paths | Yes, shown |
| Diagram №3: Variant A or B | Variant A (one poster diagram) |
| Patient-Level Aggregation in №1 | NO — moved to №2 |
| Grad-CAM in №1 | NO — moved to №2 |
| Preprocessing in №2 | Single block, no stage expansion |
| Output of preprocessing in №2 | Processed RGB + FOV mask (4-channel tensor) |

---

## 9. Work plan

1. ✅ Agree on TASK.md (current version — final).
2. ⏳ Create Diagram №1 (`01_abstract_model_architecture.svg`).
3. ⏳ Create Diagram №2 (`02_system_architecture.svg`).
4. ⏳ Create Diagram №3 (`03_preprocessing_stages_detailed.svg`).
5. ⏳ Visual check of each diagram.
6. ⏳ Convert SVG → PNG for export.

---

*End of TASK.md*
