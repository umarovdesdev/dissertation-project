# Dissertation Project — Monorepo

PhD dissertation: "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
Candidate: Yesmukhamedov N.S., IITU (Almaty, Kazakhstan)

## Project memory — ON DRIVE E: (not C: harness memory)

Persistent project facts live in `PROJECT_MEMORY/` on this drive, indexed by
`PROJECT_MEMORY.md`. **READ `PROJECT_MEMORY.md` at session start, and WRITE new durable
facts there** (one file per fact, `[[name]]` cross-links) — never into the machine-local
`~/.claude/.../memory/` store. The candidate works across a work PC, a home laptop, and a
university machine, carrying the project on an external drive (E:); only what lives under
`E:\dissertation-project\` travels. See `REFACTORING.md` for the migration rationale.

## Monorepo Structure

```
dissertation-project/
├── experiments/   Python/PyTorch — ML pipeline, training, 7 experiments
├── thesis/        Dissertation text, governance docs, literature cards
├── demo/          Defense demo bundle: web/ (React dashboard) + server/ (FastAPI inference backend)
├── defense/       Slides (pptx/docx) and presentation materials
├── CLAUDE.md      ← you are here
└── README.md
```

Each sub-directory has its own CLAUDE.md with detailed context.

## Central Thesis

model = preprocessing + CNN. The 8-stage preprocessing pipeline is an integral model component, not ancillary data preparation. It defines the feature space available to the CNN.

## Governance — Single Source of Truth

All governance documents live in `thesis/governance/`. These are the authoritative versions:
- INVARIANTS.md — scope boundaries, forbidden claims, binding constraints
- HYPOTHESIS.md — H-1 through H-7 formal definitions
- ARGUMENT_MAP.md — claim-evidence dependency structure
- CENTRAL_THESIS.md — one-paragraph thesis statement
- CONTRIBUTIONS.md — 4 primary + supporting contributions
- RESEARCH_ARCHITECTURE.md — full experimental design
- VERSION_SYNC.md — cross-file version register

`experiments/docs/` contains only `experimental_protocol.md` (quick-start guide for running experiments). All other governance references point to `thesis/governance/`.

## Preprocessing Pipeline (8 stages)

Stage 0: Canonical flip (left→right eye) — always on
Stage 1: OD-fovea rotation normalization — always on
Stage 2: FOV crop + isotropic resize to 512×512 — always on
Stage 3: FOV mask generation (binary mask → 4th channel) — always on
Stage 4: Flat-field correction (adaptive σ=0.07·D) — always on
Stage 5: CLAHE (dual-constraint, LAB L-channel, stochastic at train) — always on
Stage 6: Augmentation (unified affine + PCA color + brightness/contrast) — train only
Stage 7: Dataset-specific normalize → tensor — always last

Baseline (Exp 1 A/C) = stretch-resize 512×512 + ImageNet normalize (3 channels).
Full pipeline (Exp 1 B/D) = all 8 stages (4 channels: RGB + FOV mask).

## Experiments

| Exp | Hypothesis | Dataset | What |
|-----|-----------|---------|------|
| 1   | H-1       | EyePACS (100%, ~35,126) | 2×2 factorial: ResNet-50 vs EfficientNet-B3 × baseline(3ch) vs pipeline(4ch). Configs A–D. |
| 2   | H-2       | EyePACS | pipeline stage ablation (7 levels) + CLAHE sweep + flat-field σ sweep |
| 3   | H-4       | EyePACS → APTOS 2019 | Cross-dataset transfer (G ≥ 0.85) |
| 4   | H-5       | EyePACS → IDRiD + Clinical | Explainability: IDRiD quantitative (ALO/IoU), Clinical qualitative (Grad-CAM) |
| 5   | H-7       | EyePACS → IDRiD + Messidor-2 | Clinical degradation resistance |
| 6   | H-6       | EyePACS → DDR + ODIR-5K + RFMiD | Device domain shift (DR labels only) |
| 7   | —         | IDRiD → Clinical | Small data training (5-fold CV on IDRiD) |

## Hardware

- GPU: NVIDIA RTX 3060 12GB VRAM
- OS: WSL2 Ubuntu on Windows
- Conda env: `dr-classifier`
- Datasets: `E:/datasets/` (external, not in git)
- batch_size=16, image_size=512×512, input_channels=4 (RGB + FOV mask)
- Cross-validation: 5-fold patient-level stratified
- Loss: Focal Loss (γ=2, α=inverse-frequency)
- Mixed precision: enabled for ResNet-50, DISABLED for EfficientNet (fp16 overflow)

## Working Conventions

- All code in English. Dissertation text in English, with Kazakh translations.
- Governance docs are binding — any code change must be consistent with INVARIANTS.md.
- Claude's role for `experiments/`: plan each stage, review completed work, approve or request fixes. Implementation done via ChatGPT between sessions.
- Type hints on all Python function signatures. Docstrings with Args/Returns.
- No hardcoded paths — all paths from config YAML. Use pathlib.Path.

## Quick Commands

```bash
cd experiments
conda activate dr-classifier
python run_experiment.py exp1 --config configs/default.yaml
python run_experiment.py exp2 --config configs/default.yaml
```

```bash
cd demo
npm start     # localhost:3000
npm run build # production build
```

## Versioning policy

Version markers (`v5.X`, `V5.X`, `version 5.X`, etc.) appear **only inside `thesis/`**. `defense/`, `demo/`, `experiments/`, and root-level files reflect the current authoritative state of `thesis/` without explicit version references.

`V5` is a version marker (the fifth pipeline version), **not** a proper noun, and must not appear as a name anywhere. Outside `thesis/` it is removed entirely; inside `thesis/` only bare version references are kept (never as a name). The pipeline is named descriptively — "preprocessing pipeline" / "full pipeline"; the full-pipeline experimental arm is the "integrated arm" (vs. the "baseline arm"). See `thesis/governance/VERSIONING_POLICY.md` §2.

Version bumps follow semantic versioning: `MAJOR.MINOR.PATCH`. See `thesis/governance/VERSIONING_POLICY.md` for the full scheme, detection regexes, and workflow. Containment outside `thesis/` is enforced by the version-marker scan in §6 of that policy.
