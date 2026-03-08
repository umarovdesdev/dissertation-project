# Dissertation Repository

**Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification**

Candidate: Yesmukhamedov N.S. | IITU Doctoral Programme

---

## Directory Map

| Directory | Purpose |
|-----------|---------|
| `governance/` | Epistemic constraint system — thesis, hypothesis, invariants, argument map |
| `outline/` | Table of contents (EN + KZ) and master structural outline |
| `glossary/` | Terminological resources — English glossary and EN→KZ translation control |
| `literature/` | Source corpus — external cards, self-citation cards, and the master index |
| `literature/external/` | Third-party literature cards (`author-year[-qualifier].md`) |
| `literature/self/` | Own publications (`yesmukhamedov-venue.md`) |
| `chapters/` | Dissertation chapter drafts, one subdirectory per chapter |
| `experiments/` | Experimental protocol and design documents |
| `prompts/` | LLM meta-prompts for chapter writing, card generation, review, etc. |
| `assets/` | Figures, diagrams, exported images |

## Naming Conventions

- **Literature cards**: `author-year[-qualifier].md` → `gulshan-2016.md`, `porwal-2018-idrid-dataset.md`
- **Self-citations**: `yesmukhamedov-venue.md` → `yesmukhamedov-scopus-q2.md`
- **All filenames**: lowercase, hyphens only, no spaces, no version suffixes (use git)
- **Governance files**: UPPER_CASE permitted (they act as project constants)

## Known Issues

- `literature/external/ting-2017-duplicate.md` is a duplicate of `ting-2017.md` (same paper, two cards) — review and merge or remove
- `literature/external/wikipedia-clahe.md` is not a peer-reviewed source — consider moving to a `references/` directory or flagging in the index
