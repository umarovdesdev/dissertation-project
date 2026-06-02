# Versioning Policy

**Status:** Binding governance constraint.
**Created:** 2026-05-29.
**Authority:** Project-wide. Supersedes ad-hoc version conventions.

## 1. Containment

Version markers exist **only inside `thesis/`**. The following directories and files MUST NOT contain version markers:

- `defense/`
- `demo/`
- `experiments/`
- Repository root, except `CLAUDE.md` and `README.md`, which may reference this policy.

A "version marker" is any string matching the STRIP patterns in §3.

**Rationale.** `thesis/` is the living working journal of the dissertation, where iterative governance is documented and version history matters. Everything outside `thesis/` is a delivered artifact and represents the current authoritative state. Version archaeology of artifacts is recoverable via git tags (§5).

## 2. Proper noun exception

`V5` (uppercase V, no decimal following) is the proper noun for the 8-stage preprocessing pipeline defined in the root `CLAUDE.md`. It is NOT a version marker and is preserved in all locations.

Preserved:
- "V5 preprocessing pipeline"
- "V5 arm"
- "V5 model"
- "the V5 baseline"

Not preserved (these are version markers):
- "V5.2", "V5.3"
- "v5", "v5.2"
- "version 5.3"

## 3. Detection patterns

### STRIP (must be removed outside `thesis/`)
- `\bv[0-9]+\.[0-9]+(\.[0-9]+)?\b`
- `\bV[0-9]+\.[0-9]+(\.[0-9]+)?\b`
- `\b[Vv]ersion[: ]+[0-9]+\.[0-9]+(\.[0-9]+)?\b`
- `\bper\s+v?[0-9]+\.[0-9]+\b`
- `\bv?[0-9]+\.[0-9]+\s+amendment\b`
- `\(v?[0-9]+\.[0-9]+(?:/v?[0-9]+\.[0-9]+)*\)`

### PRESERVE
- `\bV[0-9]+\b` NOT followed by `.`
- `\bStage\s+[0-9]+\b`
- Numerical literals (`1.0e-5`, dataset IDs).

### MANUAL
- Matches inside code identifiers, config keys, i18n keys, or import paths.
- Standalone `V1`/`V2`/`V3`/`V4` (no decimal) in non-thesis files.

## 4. Version scheme (MAJOR.MINOR.PATCH)

### MAJOR (X → X+1)
A binding constraint in `INVARIANTS.md` is reversed; a hypothesis is reformulated incompatibly with prior version; the paradigmatic framing changes.
Example: `5.3.x → 6.0.0`.

### MINOR (Y → Y+1)
A new substantive entity is added — a new clause (e.g., SB-N, CFC-N), a new hypothesis, a new chapter, a new experimental arm — that does NOT reverse any prior binding.
Test: *"Can I point at the new thing and reference it by number?"* If yes → MINOR.
Example: `5.3.x → 5.4.0`.

### PATCH (Z → Z+1)
Clarification, continuation, or refinement of an existing entity. No new reference-able entity, no scope change.
Example: `5.3.0 → 5.3.1`.

### Tie-break
When in doubt, bump higher. Over-bumping has no cost; under-bumping misrepresents the change.

### Historical mapping
Versions before this policy used a 2-component scheme (`v5.0`, `v5.1`, `v5.2`, `v5.3`). These are mapped to the 3-component scheme by appending `.0`:
- `v5.0 → v5.0.0`
- `v5.1 → v5.1.0`
- `v5.2 → v5.2.0`
- `v5.3 → v5.3.0`

Pre-V2 history is tagged `v1.0.0` (inferred — predates explicit versioning).

## 5. Workflow when bumping version

1. Update affected governance files with the new version in their header.
2. Update `VERSION_SYNC.md`: amendment scope block + dependent-file sync status.
3. Add a section to `CHANGELOG.md` (date, scope summary, at most two paragraphs).
4. Commit with message `chore(governance): bump to vX.Y.Z`.
5. Tag the commit: `git tag -a vX.Y.Z -m "Governance vX.Y.Z"`.
6. Push commit and tag.
7. Bring dependent files (literature, chapters) to the new version. Re-commit; do not re-tag.
8. Once governance is stable at the new version, run the version-marker scan (§6) and remove any STRIP-class markers that have appeared in `defense/`, `demo/`, `experiments/`.

## 6. Enforcement

Enforcement of §1 is the version-marker scan below — run as a pre-push or CI hook. It fails if any STRIP-class marker remains outside `thesis/`:
```bash
rg -nE '\b[Vv][0-9]+\.[0-9]+|\bversion\s+[0-9]+\.[0-9]+' \
  --glob '!thesis/**' \
  --glob '!.git/**' \
  --glob '!**/node_modules/**' \
  --glob '!**/build/**' \
  .
```
If this command returns non-empty output, reject the push or commit.
