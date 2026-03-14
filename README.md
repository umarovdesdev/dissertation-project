# Dissertation Repository

**Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification**

Candidate: Yesmukhamedov N.S. | IITU Doctoral Programme

---

## Directory Map

| Directory | Purpose |
|-----------|---------| 
| `governance/` | Epistemic constraint system — thesis, hypothesis, invariants, argument map, contributions |
| `methods/` | Methodology specifications — preprocessing pipeline, implementation details |
| `outline/` | Table of contents (EN + KZ) and master structural outline |
| `glossary/` | Terminological resources — English glossary and EN→KZ translation control |
| `literature/` | Source corpus — external cards, self-citation cards, and the master index |
| `literature/external/` | Third-party literature cards (`author-year[-qualifier].md`) |
| `literature/self/` | Own publications (`yesmukhamedov-venue.md`) |
| `chapters/` | Dissertation chapter drafts, one subdirectory per chapter |
| `experiments/` | Experimental protocol and design documents |
| `prompts/` | AI pipeline templates — section briefs, writing prompts, verification, translation, revision (see `prompts/README.md`) |
| `assets/` | Figures, diagrams, exported images |

## Governance Files

| File | Purpose |
|------|---------|
| `governance/INVARIANTS.md` | Master constraint document (v2.2) — immutable thesis, hypotheses, operational definitions |
| `governance/CENTRAL_THESIS.md` | Single-paragraph thesis formulation with model=preprocessing+CNN framing |
| `governance/HYPOTHESIS.md` | Central hypothesis + H-1 through H-6 decomposition + argument structure |
| `governance/ARGUMENT_MAP.md` | Formal claim-evidence-dependency structure (PC-1 through PC-9) |
| `governance/RESEARCH_ARCHITECTURE.md` | Methodological blueprint (v2.2) |
| `governance/CORE_OBJECTIVE.md` | Research objective formulation |
| `governance/CONTRIBUTIONS.md` | Scientific contributions register (3 primary + 3 supporting) |

## Methods Files

| File | Purpose |
|------|---------|
| `methods/preprocessing-pipeline.md` | 5-component pipeline specification with design principle and pipeline-as-model assertion |
| `methods/implementation.md` | Software stack, hardware config, training config, model definition, Grad-CAM with ALO |

## Naming Conventions

- **Literature cards**: `author-year[-qualifier].md` → `gulshan-2016.md`, `porwal-2018-idrid-dataset.md`
- **Self-citations**: `yesmukhamedov-venue.md` → `yesmukhamedov-scopus-q2.md`
- **All filenames**: lowercase, hyphens only, no spaces, no version suffixes (use git)
- **Governance files**: UPPER_CASE permitted (they act as project constants)

## Writing Pipeline

The dissertation uses a section-level AI-assisted writing pipeline (V3.0):

1. **Section Brief** (planning) → compact instruction per section with governance bindings and source mappings
2. **Writing Session** (generation) → section text + Continuity Note + Compliance Checklist
3. **Verification** (review) → governance compliance audit
4. **Revision** (if needed) → targeted fixes with continuity preservation
5. **Translation** (EN→KZ) → controlled translation per GLOSSARY_KZ.md
6. **Translation Review** → terminology and register verification

Templates are in `prompts/`. Assembly script: `scripts/assemble-session-input.py`.

## Known Issues

- `ting-2017-duplicate.md` — RESOLVED: duplicate removed; `ting-2017.md` is canonical
- `wikipedia-clahe.md` location — RESOLVED: moved to `literature/non-peer-reviewed/`
