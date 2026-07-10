# Dissertation Project

**Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification**

PhD dissertation — Yesmukhamedov N.S., IITU, Almaty, Kazakhstan.

## Structure

| Directory | Description |
|-----------|-------------|
| `experiments/` | Python/PyTorch ML pipeline, training, 6 experiments |
| `thesis/` | Dissertation text, governance docs, literature cards |
| `demo/` | Defense demo bundle: `web/` (React dashboard) + `server/` (FastAPI inference backend) |
| `defense/` | Slides and presentation materials |

See `CLAUDE.md` for detailed project documentation.

## Current status

- **Integrated-arm initialization (Exp-1 Configs B/D) resolved.** From-scratch in-domain
  self-supervised pretraining did not clear the linear-probe acceptance gate, so the
  integrated arm uses the sanctioned **ImageNet→continual-SSL** initialization (MoCo-v2,
  ResNet-50 + EfficientNet-B3). Both checkpoints pass the gate. Continual-SSL is a large
  in-domain win for ResNet-50 and neutral (≈ ImageNet) for EfficientNet-B3.
- A **supervised in-domain pretraining (SIP)** path is implemented and governance-admitted
  (v6.3.0) as an alternative, gate-selected initialization.
- **Experiment 1 (2×2 factorial, EyePACS) in progress**, starting with the integrated arm.
- Running notes and the one thing in flight live in `TASK.md`; durable decisions in
  `PROJECT_MEMORY/`; binding constraints in `thesis/governance/`.
