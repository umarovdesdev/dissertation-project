# Strip Versions — Run Report

Date: 2026-05-29T12:53:06Z
Branch: chore/version-archaeology-and-strip
Authoritative version: v5.3.0

## Phase 0 — Policy

- Created `thesis/governance/VERSIONING_POLICY.md` (binding containment + semver scheme).
- Appended a "Versioning policy" section to root `CLAUDE.md`.
- Pre-existing working-tree deletion of `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` (the superseded v5.3 integration tracker) was committed separately so subsequent phases ran on a clean tree.

## Phase 1 — Archaeology

Tags created: v1.0.0, v2.0.0, v3.0.0, v4.0.0, v5.0.0, v5.1.0, v5.2.0, v5.3.0
Inferred tags: v1.0.0 (predates the explicit versioning convention; anchored at commit `015436c` "feat meat V1").
CHANGELOG.md sections: 8

Anchor evidence is recorded in `.strip-versions/version-candidates.tsv`. v5.0–v5.3 anchors derive from `VERSION_SYNC.md` header history; v1–v4 anchors derive from explicit `V1`/`V2`/`V3.0`/`V4` commit messages (the three sub-projects were separate repos until the 2026-04-01 monorepo subtree merge, so governance-file history does not reach below v5.0).

## Phase 2 — Inventory

Total raw matches (decimal version markers / "version N.M" outside `thesis/`): 0
- STRIP: 0
- PRESERVE: 0
- MANUAL: 0

The repository was already compliant with the containment invariant. Numerous `V5`/`v5` tokens exist outside `thesis/` (e.g. "V5 pipeline", "Full V5 (4ch)", config keys like `preprocessing_v5`, `pipeline_version: "v5"`), but all are the preserved proper noun or bare tokens with no decimal — none match the STRIP patterns. Supplementary scans confirmed zero decimal markers (text files, with and without `.gitignore`), zero standalone `V1`–`V4`, and zero version-marker content inside the tracked Office files (`defense/999.docx`, `defense/presentation.pptx`, `defense/seminar-ready.pptx`). The `version`/`AppVersion`/`cp:revision` strings in those Office files are OOXML structural metadata, not content markers, and were left untouched.

## Phase 3 — Strip

Files modified by type (no STRIP-decision rows existed):
- Markdown: 0
- JavaScript: 0
- Python: 0
- YAML: 0
- PowerPoint: 0
- Word: 0
- Unhandled (deferred): 0

## Phase 4 — Verification

Post-strip STRIP-class matches: 0 (expected)
Leakage rows: 0 (expected)
Unexpected thesis/ modifications: 0 (expected — only `CHANGELOG.md` and `VERSIONING_POLICY.md` added)

## Manual review queue

File: `.strip-versions/classified.tsv` (filter where `decision == MANUAL`).
Count: 0
Plus unhandled file types: `.strip-versions/unhandled.tsv` (0).

## Branch state

Commits on this branch:
```
9d8e474 chore: inventory and classification of version markers outside thesis/ (zero strip-class markers found)
ab7b229 chore(governance): add CHANGELOG.md and version-candidates audit trail
9f33d26 chore(governance): add versioning policy and containment rule
5e157d6 chore: remove superseded v5.3 integration tracker (working-tree deletion)
```

(A subsequent commit adds this report and audit artifacts.)

## Notes for the reviewer

- Tags are created locally but **not yet pushed**, and the branch is **not merged**. All pushes were deferred to a single final step so that no artifacts reached the remote unless the full run succeeded.
- The v1–v4 tag anchors are heuristic (commit-message based) and labeled with evidence in `version-candidates.tsv`; v1.0.0 is explicitly inferred. Adjust before relying on them for archaeology if a more precise boundary is known.
- Office lock files (`~$*.pptx`, `~$*.docx`) were present, suggesting the documents may be open in Office; they were not touched. Since no Office file contained a strip-class marker, none were repacked.
