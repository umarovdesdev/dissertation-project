# STRIP_VERSIONS_PLAN.md — Claude Code Execution Plan

**Status:** Autonomous execution plan. No per-action confirmation. Claude Code executes all phases in order. On any phase failure, Claude Code writes a `STRIP_FAIL_PHASE_N.md` to the repo root and halts before pushing.

**Author of plan:** Claude (Cowork session, 2026-05-29)
**Executor:** Claude Code
**Reviewer:** human, after the branch is pushed

---

## 1. Purpose

Bring the `dissertation-project` repository into compliance with a single project-wide invariant:

> **Version markers exist only inside `thesis/`.** All other directories (`defense/`, `demo/`, `experiments/`) and root-level files reflect the current authoritative state of governance without explicit version references. `V5` (capital V, no decimal following) is preserved everywhere as the proper noun of the 8-stage preprocessing pipeline.

This plan accomplishes six things:

1. Codifies the versioning policy in `CLAUDE.md` and `thesis/governance/VERSIONING_POLICY.md`.
2. Reconstructs the full version history in git tags from `v1.0.0` through `v5.3.0`. Tags before `v2.0.0` are inferred and labeled as such.
3. Generates `thesis/governance/CHANGELOG.md` with one section per version.
4. Removes version markers from `defense/`, `demo/`, `experiments/`, and root files (except `CLAUDE.md` and `README.md`, which reference the policy).
5. Verifies zero strip-class markers remain outside `thesis/`.
6. Writes a run report. Pushes the branch. Stops before merge.

---

## 2. Working assumptions

- Working directory is the repo root (Windows host: `E:\dissertation-project`; under WSL2: `/mnt/e/dissertation-project`).
- Default branch is `main`.
- Tools available in the shell: `git`, `bash`, `python3`, `rg` (ripgrep). If `rg` is not installed, install it (`apt-get install -y ripgrep`) or fall back to `grep -E -rn`.
- The current authoritative version is the most recent header in `thesis/governance/VERSION_SYNC.md`. As of plan writing this is `v5.3` and the plan treats it as `v5.3.0`.

---

## 3. Detection patterns

These patterns are the single source of truth for what gets stripped and what is preserved. They are referenced from each phase below. They are also embedded in `VERSIONING_POLICY.md` (Phase 0).

### 3.1 STRIP (remove or rephrase outside `thesis/`)
ERE syntax:

- `P1`: `\bv[0-9]+\.[0-9]+(\.[0-9]+)?\b` — lowercase `v` + decimal (e.g., `v5.1`, `v5.3.0`).
- `P2`: `\bV[0-9]+\.[0-9]+(\.[0-9]+)?\b` — uppercase `V` + decimal (e.g., `V5.2`).
- `P3`: `\b[Vv]ersion[: ]+[0-9]+\.[0-9]+(\.[0-9]+)?\b` — `Version: 5.3`, `version 5.3`.
- `P4`: `\bper\s+v?[0-9]+\.[0-9]+\b` — `per v5.2`.
- `P5`: `\bv?[0-9]+\.[0-9]+\s+amendment\b` — `v5.3 amendment`.
- `P6`: `\(v?[0-9]+\.[0-9]+(?:/v?[0-9]+\.[0-9]+)*\)` — `(v5.1/v5.2)`.

### 3.2 PRESERVE (never touch)
- `Q1`: `\bV[0-9]+\b` NOT followed by `.` — `V5 arm`, `V5 pipeline`, `V5 model`. Proper noun.
- `Q2`: `\bStage\s+[0-9]+\b` — pipeline stage numbers.
- `Q3`: numerical literals (`1.0e-5`, `10^5`) and dataset sample IDs (`IDRiD_010`).

### 3.3 MANUAL (defer to human review)
- A match satisfying P1–P6 that sits inside a code identifier, a config key, an i18n key, or an import path.
- Standalone `V1`, `V2`, `V3`, `V4` (no decimal) in non-thesis files — ambiguous between historical version and incidental use. Log for human review.

---

## 4. Phase 0 — Pre-flight and policy creation

### 4.1 Git safety
```bash
cd <repo-root>
[ -z "$(git status --porcelain)" ] || { echo "Working tree not clean. Aborting."; exit 1; }
git fetch origin
git checkout main
git pull --ff-only
git checkout -b chore/version-archaeology-and-strip
```

### 4.2 Tool checks
```bash
command -v rg >/dev/null 2>&1 || sudo apt-get install -y ripgrep
command -v python3 >/dev/null 2>&1 || { echo "python3 missing"; exit 1; }
```

### 4.3 Create `thesis/governance/VERSIONING_POLICY.md`
Write the file with exactly the following content:

````markdown
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
8. Once governance is stable at the new version, run `STRIP_VERSIONS_PLAN.md` to bring `defense/`, `demo/`, `experiments/` into compliance.

## 6. Enforcement

`STRIP_VERSIONS_PLAN.md` (repo root) is the automated enforcement of §1. Its verification phase fails if any STRIP-class marker remains outside `thesis/`.

Recommended additional enforcement — a pre-push or CI hook:
```bash
rg -nE '\b[Vv][0-9]+\.[0-9]+|\bversion\s+[0-9]+\.[0-9]+' \
  --glob '!thesis/**' \
  --glob '!.git/**' \
  --glob '!**/node_modules/**' \
  --glob '!**/build/**' \
  .
```
If this command returns non-empty output, reject the push or commit.
````

### 4.4 Update root `CLAUDE.md`
Append the following section at the end of `CLAUDE.md`:

```markdown

## Versioning policy

Version markers (`v5.X`, `V5.X`, `version 5.X`, etc.) appear **only inside `thesis/`**. `defense/`, `demo/`, `experiments/`, and root-level files reflect the current authoritative state of `thesis/` without explicit version references.

`V5` (uppercase, no decimal) is the proper noun for the 8-stage preprocessing pipeline and is preserved everywhere.

Version bumps follow semantic versioning: `MAJOR.MINOR.PATCH`. See `thesis/governance/VERSIONING_POLICY.md` for the full scheme, detection regexes, and workflow. `STRIP_VERSIONS_PLAN.md` (repo root) is the automated enforcement.
```

### 4.5 Commit
```bash
git add CLAUDE.md thesis/governance/VERSIONING_POLICY.md
git commit -m "chore(governance): add versioning policy and containment rule"
```

### 4.6 Halt conditions
- Pre-flight 4.1 fails (dirty tree, branch creation error): write `STRIP_FAIL_PHASE_0.md` with `git status` output. Exit.
- `VERSIONING_POLICY.md` already exists with different content: write `STRIP_FAIL_PHASE_0.md` describing the conflict. Exit.

---

## 5. Phase 1 — Version archaeology

Goal: identify and tag historical commits for every version. Generate `thesis/governance/CHANGELOG.md`.

### 5.1 Identify commits for each version

Target tag set: `v1.0.0`, `v2.0.0`, `v3.0.0`, `v4.0.0`, `v5.0.0`, `v5.1.0`, `v5.2.0`, `v5.3.0`.

#### Strategy for v2.0.0 through v5.3.0
For each version `vN.M`, find the commit that finalized it. Two methods, applied in order:

**Method A — VERSION_SYNC.md headers.** Scan the history of `thesis/governance/VERSION_SYNC.md`:
```bash
git log --reverse --format='%H %ai' -- thesis/governance/VERSION_SYNC.md \
  | while read sha date_time tz; do
    header=$(git show "$sha:thesis/governance/VERSION_SYNC.md" 2>/dev/null | grep -m1 -E '^\*\*Version:\*\*' | sed -E 's/.*Version:\*\* ([0-9]+\.[0-9]+).*/\1/')
    echo "$sha $date_time $header"
  done > /tmp/version-sync-headers.txt
```
For each target version, take the **last commit** whose header equals that version (i.e., the commit immediately before the next bump in the history of this file).

**Method B — INVARIANTS.md headers.** If `VERSION_SYNC.md` did not exist for an early version, repeat Method A against `thesis/governance/INVARIANTS.md`.

**Method C — commit message search.** If neither A nor B yields a candidate for a target version:
```bash
git log --all --format='%H %ai %s' --grep="v?$N\.$M" -E
```
Take the most recent matching commit.

If a target version cannot be located by A, B, or C: mark it `INFERRED` and use the latest commit predating the next version that was located.

#### Strategy for v1.0.0
This tag marks the pre-versioning baseline.
```bash
v2_sha=$(awk -v target="2.0" '$3==target {print $1}' /tmp/version-sync-headers.txt | head -1)
v1_sha=$(git rev-list --reverse HEAD | head -1)   # first commit on main, or:
v1_sha=$(git log --format='%H' "$v2_sha^" | head -1)   # parent of first v2 commit, if exists
```
Prefer the parent of the first `v2.0.0` commit when available. Fall back to the very first commit in the repo. Always label v1.0.0 as `INFERRED`.

#### Write candidates table
Output `.strip-versions/version-candidates.tsv`:
```
version<TAB>commit-sha<TAB>commit-date<TAB>inferred<TAB>method<TAB>evidence
```

### 5.2 Create tags
```bash
while IFS=$'\t' read -r version sha date inferred method evidence; do
  [ "$version" = "version" ] && continue   # skip header
  msg="Governance $version"
  [ "$inferred" = "yes" ] && msg="$msg (inferred — predates explicit versioning convention)"
  git tag -a "$version" "$sha" -m "$msg"
done < .strip-versions/version-candidates.tsv
```

Verify the tag set:
```bash
expected="v1.0.0 v2.0.0 v3.0.0 v4.0.0 v5.0.0 v5.1.0 v5.2.0 v5.3.0"
actual=$(git tag -l 'v*' | sort -V | tr '\n' ' ' | xargs)
[ "$actual" = "$(echo $expected | tr -s ' ')" ] || {
  echo "Tag set mismatch."
  echo "Expected: $expected"
  echo "Actual:   $actual"
  exit 1
}
```

### 5.3 Generate `thesis/governance/CHANGELOG.md`

Create the file with this skeleton, then populate each version section:

```markdown
# Governance Changelog

This file is the human-readable history of governance versions. Each entry corresponds to a git tag. To recover the exact state at any version, run `git checkout <tag>`.

The versioning scheme is defined in [VERSIONING_POLICY.md](VERSIONING_POLICY.md).

---

## v5.3.0 — <date>
<scope text>

## v5.2.0 — <date>
<scope text>

## v5.1.0 — <date>
<scope text>

## v5.0.0 — <date>
<scope text>

## v4.0.0 — <date>
<scope text>

## v3.0.0 — <date>
<scope text>

## v2.0.0 — <date>
<scope text>

## v1.0.0 — <date> (inferred)
Pre-versioning baseline. The repository state captured by this tag predates the explicit governance versioning convention. See git tag `v1.0.0` for the complete state.
```

Population rules:

- **For v5.1.0, v5.2.0, v5.3.0:** copy the corresponding `## vN.M Amendment Scope` block verbatim from current `thesis/governance/VERSION_SYNC.md`. Strip the `## vN.M Amendment Scope` heading (already in the section header) and keep the prose.
- **For v5.0.0, v4.0.0, v3.0.0, v2.0.0:** derive a 2–4 sentence summary from commit messages between the previous tag and this tag:
  ```bash
  git log v<prev>..v<this> --oneline --no-decorate
  ```
  Borrow phrasing from current governance files that describe these earlier versions where available.
- **For v1.0.0:** use the fallback paragraph as shown.

### 5.4 Commit
```bash
git add thesis/governance/CHANGELOG.md .strip-versions/version-candidates.tsv
git commit -m "chore(governance): add CHANGELOG.md and version-candidates audit trail"
git push origin --tags
```

### 5.5 Halt conditions
- Section 5.2 tag verification fails: write `STRIP_FAIL_PHASE_1.md` listing missing or unexpected tags. Exit.
- `CHANGELOG.md` has fewer than 8 version sections after population: write `STRIP_FAIL_PHASE_1.md`. Exit.

---

## 6. Phase 2 — Inventory version markers outside `thesis/`

### 6.1 Run ripgrep
```bash
mkdir -p .strip-versions
rg -nE '\b[Vv][0-9]+(\.[0-9]+){1,2}\b|\b[Vv]ersion[: ]+[0-9]+\.[0-9]+|\bper\s+v?[0-9]+\.[0-9]+' \
   --glob '!thesis/**' \
   --glob '!.git/**' \
   --glob '!**/node_modules/**' \
   --glob '!**/build/**' \
   --glob '!**/dist/**' \
   --glob '!.strip-versions/**' \
   --glob '!STRIP_VERSIONS_PLAN.md' \
   --glob '!STRIP_VERSIONS_REPORT.md' \
   defense/ demo/ experiments/ *.md \
   > .strip-versions/raw-matches.txt 2>/dev/null || true
```

### 6.2 Classify each match

For each line in `raw-matches.txt` (format: `file:line:text`):

1. Extract the matched token and its surrounding 80 characters of context.
2. Apply patterns in this order — first match wins:
   - If token matches **Q1, Q2, or Q3** (PRESERVE patterns): decision = `PRESERVE`.
   - Else if the token sits inside an identifier or config key (surrounded by `[A-Za-z_0-9]` on both sides without a word break): decision = `MANUAL`.
   - Else if the token is standalone `V1`/`V2`/`V3`/`V4` without a decimal: decision = `MANUAL`.
   - Else if token matches any **P1–P6** (STRIP patterns): decision = `STRIP`.
   - Else: decision = `MANUAL`.
3. Output to `.strip-versions/classified.tsv`:
   ```
   file<TAB>line<TAB>match<TAB>decision<TAB>reason
   ```

### 6.3 Commit
```bash
git add .strip-versions/
git commit -m "chore: inventory and classification of version markers outside thesis/"
```

### 6.4 Halt conditions
None. Proceed regardless of MANUAL count — those are reported in Phase 4 for human review.

---

## 7. Phase 3 — Strip

For each row in `.strip-versions/classified.tsv` with `decision = STRIP`, apply the per-extension handler. Use the Edit tool for targeted line edits; do not run global `sed -i` across the tree.

### 7.1 Markdown (`.md`)

Apply per match:

| Match shape | Action |
|---|---|
| `Version: N.M` or `**Version:** N.M` alone on a line | Delete the entire line. If inside a pipe-table row, replace the cell with an empty cell. |
| `(vN.M)` inline | Delete with one surrounding space. |
| `vN.M amendment` | Replace with `amendment`. |
| `per vN.M` | Replace with `per current governance`. |
| Bare `vN.M` in prose | Delete with adjacent whitespace; if removal leaves a dangling fragment ("at vN.M:" → "at :"), rephrase the surrounding clause. |

After all `.md` edits:
```bash
git add <touched-md-files>
git commit -m "chore(<area>): strip version markers from markdown"
```
Repeat the commit per affected area (`defense`, `demo`, `experiments`, root) if convenient.

### 7.2 JavaScript / TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`)
Restrict edits to:
- `//` line comments.
- `/* ... */` block comments.
- JSX text nodes (between tags).
- String literals that are UI text, identified by one of:
  - Passed to `t(...)` (i18n call).
  - Used as a JSX child.
  - Assigned to property names in `{ title, description, label, name }`.
  - In `demo/src/i18n.js`, the right-hand side of any key.

Do NOT touch:
- Identifiers (variable / function / class names).
- Object property keys.
- Import paths.

Commit:
```bash
git add <touched-js-files>
git commit -m "chore(demo): strip version markers from JavaScript"
```

### 7.3 Python (`.py`)
Restrict edits to docstrings and `#` comments. Do NOT touch identifiers, function names, dictionary keys, or string literals used in logic.

Commit:
```bash
git add <touched-py-files>
git commit -m "chore(experiments): strip version markers from Python docstrings and comments"
```

### 7.4 YAML (`.yaml`, `.yml`)
Restrict edits to `#` comments. Do NOT touch keys or values.

Commit:
```bash
git add <touched-yaml-files>
git commit -m "chore(experiments): strip version markers from YAML comments"
```

### 7.5 PowerPoint (`.pptx`)
For each `.pptx` listed in classified.tsv:

```bash
SKILLS=<path-to-pptx-skill-scripts>   # e.g., /sessions/.../skills/pptx/scripts
mkdir -p .strip-versions/pptx-work
basename=$(basename "$file" .pptx)
python3 "$SKILLS/office/unpack.py" "$file" ".strip-versions/pptx-work/$basename/"
```

Edit XML in `.strip-versions/pptx-work/$basename/ppt/slides/*.xml`. Apply the same replacement table as §7.1 but on the slide text runs (`<a:t>...</a:t>`).

Also clean document properties — open and edit:
- `docProps/core.xml`: remove `<cp:revision>`, `<cp:version>`, and any custom property containing a STRIP-pattern match.
- `docProps/app.xml`: remove the same.

Repack:
```bash
python3 "$SKILLS/office/pack.py" ".strip-versions/pptx-work/$basename/" "$file" --original "$file"
```

Commit:
```bash
git add defense/
git commit -m "chore(defense): strip version markers from .pptx (slides + properties)"
```

### 7.6 Word (`.docx`)
Same procedure as §7.5 with the `docx` skill scripts. Additionally:

- Accept all tracked changes before edit:
  ```bash
  python3 "$SKILLS_DOCX/accept_changes.py" "$file" "$file"
  ```
- Remove all comments via XML editing of `word/comments.xml` (delete file and remove the relationship + content-type entry).

Commit:
```bash
git add <touched-docx-files>
git commit -m "chore: strip version markers from .docx (text + properties + comments)"
```

### 7.7 Unsupported file types
If a STRIP match falls in an extension not handled by §7.1–§7.6: log to `.strip-versions/unhandled.tsv`. These join the MANUAL queue and are reported in Phase 4. Do not modify.

---

## 8. Phase 4 — Verification and report

### 8.1 Re-run inventory
Run the same ripgrep as §6.1. Output to `.strip-versions/post-strip-matches.txt`.

### 8.2 Diff against classification
Every line in `post-strip-matches.txt` must classify (using the §6.2 rules) as `PRESERVE` or `MANUAL`. Any line classifying as `STRIP` is a failure.

```bash
# pseudo-code; implement as a small python or bash script
python3 - <<'PY'
import csv
# load classified.tsv, build {file:line -> decision}
# load post-strip-matches.txt
# for each post-strip line, classify (re-apply rules) — if STRIP, append to .strip-versions/leakage.tsv
PY

if [ -s .strip-versions/leakage.tsv ]; then
  cp .strip-versions/leakage.tsv STRIP_FAIL_PHASE_4.md
  echo "STRIP-class markers leaked past Phase 3. See STRIP_FAIL_PHASE_4.md."
  exit 1
fi
```

### 8.3 `thesis/` integrity check
Only the two new files in `thesis/` are permitted in the diff:

```bash
unexpected=$(git diff --name-only main..HEAD \
  | grep '^thesis/' \
  | grep -v -E '^thesis/governance/(CHANGELOG\.md|VERSIONING_POLICY\.md)$' || true)
if [ -n "$unexpected" ]; then
  echo "Unexpected thesis/ modifications:" > STRIP_FAIL_PHASE_4.md
  echo "$unexpected" >> STRIP_FAIL_PHASE_4.md
  exit 1
fi
```

### 8.4 Write the run report
Create `STRIP_VERSIONS_REPORT.md` in the repo root with this template:

```markdown
# Strip Versions — Run Report

Date: <ISO timestamp>
Branch: chore/version-archaeology-and-strip
Authoritative version: v5.3.0

## Phase 1 — Archaeology
Tags created: <comma-separated list>
Inferred tags: <list of tags labeled INFERRED>
CHANGELOG.md sections: <count>

## Phase 2 — Inventory
Total raw matches: <N>
- STRIP: <a>
- PRESERVE: <b>
- MANUAL: <c>

## Phase 3 — Strip
Files modified by type:
- Markdown: <count>
- JavaScript: <count>
- Python: <count>
- YAML: <count>
- PowerPoint: <count>
- Word: <count>
- Unhandled (deferred): <count>

## Phase 4 — Verification
Post-strip STRIP-class matches: 0 (expected)
Unexpected thesis/ modifications: 0 (expected)

## Manual review queue
File: `.strip-versions/classified.tsv` (filter where `decision == MANUAL`).
Count: <c>
Plus unhandled file types: `.strip-versions/unhandled.tsv` (<count>).

## Branch state
Commits on this branch:
<git log main..HEAD --oneline output>
```

### 8.5 Commit and push
```bash
git add STRIP_VERSIONS_REPORT.md .strip-versions/
git commit -m "chore: strip-versions run report and audit artifacts"
git push -u origin chore/version-archaeology-and-strip
git push origin --tags
```

### 8.6 Stop
**Do NOT merge to main.** The user reviews the branch.

---

## 9. Failure protocol

If any `STRIP_FAIL_PHASE_N.md` is present at the end of execution:

1. Do not push the branch.
2. Do not delete the failure file.
3. The file's contents are the diagnostic for human review.
4. Exit cleanly.

The human can then either fix the issue manually and re-run from the failed phase, or discuss with the planning agent (Claude) to amend this plan and re-run from scratch on a fresh branch.

---

## 10. What is intentionally out of scope

- Rewriting git history (e.g., squashing or rebasing earlier commits to remove version markers from old commit messages). Old history is preserved untouched.
- Modifying `thesis/` content beyond creating `CHANGELOG.md` and `VERSIONING_POLICY.md`. Governance content stays as is.
- Resolving MANUAL items automatically. These are reported for human decision.
- Merging the resulting branch. Human review and merge.
- Adding the recommended pre-push / CI enforcement hook from `VERSIONING_POLICY.md` §6. That is a separate follow-up task.
