# Dissertation Project — Monorepo

PhD dissertation: "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
Candidate: Yesmukhamedov N.S., IITU (Almaty, Kazakhstan)

## Monorepo Structure

```
dissertation-project/
├── experiments/   Python/PyTorch — ML pipeline, training, 6 experiments
├── thesis/        Dissertation text, governance docs, literature cards
├── demo/          React dashboard for defense presentation
├── defense/       Slides (pptx/docx) and presentation materials
├── CLAUDE.md      ← you are here
└── README.md
```

Each sub-directory has its own CLAUDE.md with detailed context.

## Central Thesis

model = preprocessing + CNN. The 6-stage V4 preprocessing pipeline is an integral model component, not ancillary data preparation. It defines the feature space available to the CNN.

## Governance — Single Source of Truth

All governance documents live in `thesis/governance/` (v4.1). These are the authoritative versions:
- INVARIANTS.md — scope boundaries, forbidden claims, binding constraints
- HYPOTHESIS.md — H-1 through H-6 formal definitions
- ARGUMENT_MAP.md — claim-evidence dependency structure
- CENTRAL_THESIS.md — one-paragraph thesis statement
- CONTRIBUTIONS.md — 4 primary + supporting contributions
- RESEARCH_ARCHITECTURE.md — full experimental design
- VERSION_SYNC.md — cross-file version register

`experiments/docs/` contains only `experimental_protocol.md` (quick-start guide for running experiments). All other governance references point to `thesis/governance/`.

## V4 Preprocessing Pipeline (6 stages)

Stage 0a: Canonical flip (left→right eye) — toggleable
Stage 0b: OD-fovea rotation normalization — toggleable
Stage 1:  FOV crop + isotropic resize to 512×512 — always on
Stage 2:  Flat-field correction (Gaussian σ=45) — toggleable
Stage 3:  Upgraded CLAHE (dual-constraint, LAB L-channel, stochastic at train) — toggleable
Stage 5:  Augmentation (unified affine + PCA color + brightness/contrast) — train only
Stage 4:  ImageNet normalize → tensor — always last

Baseline = Stages 1 + 4 only (crop + resize + ImageNet normalize).

## Experiments

| Exp | Hypothesis | Dataset | What |
|-----|-----------|---------|------|
| 1   | H-1       | EyePACS (40% subset, ~14,050) | 2×2 factorial: ResNet-50 vs EfficientNet-B3 × baseline vs full V4. Configs A–F. |
| 2   | H-2       | EyePACS + IDRiD | Component ablation (V4 levels 0–4) + CLAHE sweep |
| 3   | —         | DROPPED (APTOS robustness removed in V3) |
| 4   | H-5       | IDRiD | Grad-CAM explainability (ALO primary, IoU secondary) |
| 5   | H-4       | Messidor/Messidor-2/IDRiD | Cross-dataset generalization (G ≥ 0.85) |
| 6   | H-6       | RFMiD/DDR/ODIR-5K | Device domain shift (Canon, Topcon, Kowa, Zeiss) |

Experiment 1 is COMPLETED. Config D (EfficientNet-B3 + full V4) achieved best results (F1=0.780, AUC=0.865, κ=0.700).

## Hardware

- GPU: NVIDIA RTX 3060 12GB VRAM
- OS: WSL2 Ubuntu on Windows
- Conda env: `dr-classifier`
- Datasets: `/mnt/d/datasets/` (external, not in git)
- batch_size=16, image_size=512×512, input_channels=4 (RGB + FOV mask)
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
python run_experiment.py exp1 --config configs/default.yaml --configs D
python run_experiment.py exp2 --config configs/default.yaml
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml  # 1% smoke test
```

```bash
cd demo
npm start     # localhost:3000
npm run build # production build
```
