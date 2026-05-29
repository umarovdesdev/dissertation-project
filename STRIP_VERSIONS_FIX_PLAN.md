# STRIP_VERSIONS_FIX_PLAN.md — Claude Code Execution Plan (Fix-up)

**Supersedes:** Phase 2–4 of `STRIP_VERSIONS_PLAN.md`.
**Does NOT redo:** Phase 0 (policy files) and Phase 1 (git tags + `CHANGELOG.md`) — those are correct.
**Branch:** continue on the existing `chore/version-archaeology-and-strip` (already pushed; tags `v1.0.0..v5.3.0` are on the remote and stay).
**Mode:** autonomous. No per-action confirmation. Halt only on the explicit failure conditions.

---

## 1. Why this plan exists

The previous run produced `STRIP_VERSIONS_REPORT.md` claiming **0 strip-class markers outside `thesis/`**. That claim is **false**. Independent verification finds ≈250 strip-class matches across ≈50 files outside `thesis/`. The audit artifacts confirm a silent failure:

- `.strip-versions/raw-matches.txt` — empty.
- `.strip-versions/classified.tsv` — only the header row, no entries.
- `.strip-versions/post-strip-matches.txt` — empty.
- `.strip-versions/leakage.tsv` — only the header row.

Root cause in the original plan: Phase 2 §6.1 wrapped the `rg` invocation with `2>/dev/null || true`, so any tool failure was masked. The original Phase 4 verification then compared empty input to empty output and reported "success". This fix plan replaces that pipeline with multi-method scanning and explicit error checking.

---

## 2. Evidence — these matches MUST appear in the new inventory

If the new Phase 2 inventory does not contain every entry below classified as `STRIP`, the inventory is broken. Halt before Phase 3.

| File | Line | Excerpt (truncated) |
|---|---|---|
| `defense/paradigmatic_speech.md` | 4 | `**Version:** Generated under governance v5.3 ...` |
| `defense/paradigmatic_speech.md` | 6 | `INVARIANTS.md v5.3 SB-1.12, CFC-2.9, SIR-9; ...` |
| `defense/slide_plan.md` | 33 | `(v5.3 — қосылған)` |
| `defense/idea.md` | 6 | `Sources: thesis/governance/ v5.0 (...)` |
| `defense/slides/05a_PARADIGMATIC_POSITIONING.md` | 62 | `INVARIANTS.md v5.3 — SB-1.12, ...` |
| `defense/slides/09_ARCHITECTURE_COMPARISON.md` | 37 | `v5.1 / v5.2 шектеуі (CFC-2.8)` |
| `defense/slides/08_CNN_ARCHITECTURE.md` | 22 | `INVARIANTS.md v5.2, X бөлімі` |
| `demo/src/i18n.js` | 68 | `'... (INVARIANTS v5.3 SB-1.12); ...'` |
| `demo/src/tabs/ModelArchitecture.js` | 41 | `V5 arm (per governance v5.2): ...` |
| `experiments/src/explainability/iou.py` | 3 | `Two metrics are computed (per INVARIANTS v2.2 ...)` |
| `experiments/scripts/generate_report.py` | 452 | `f"... documented in INVARIANTS v2.2."` |

---

## 3. Phase 2 (redo) — Robust inventory

### 3.1 Branch and tree state
```bash
[ "$(git branch --show-current)" = "chore/version-archaeology-and-strip" ] || {
  echo "Wrong branch"; exit 1
}
git status --porcelain > .strip-versions/preflight-status.txt
```
Do NOT abort on dirty tree — the previous report flagged unrelated uncommitted edits in `demo/src/App.js`, `demo/src/i18n.js`, `demo/src/tabs/Demo.js`. Stash them so the fix run starts clean:
```bash
git stash push -u -m "fix-plan: stash unrelated work before inventory"
git stash list | head -1 > .strip-versions/stash-ref.txt
```
If `git stash` fails or there is nothing to stash, continue.

### 3.2 Wipe stale audit artifacts
```bash
rm -f .strip-versions/{raw-matches.txt,classified.tsv,post-strip-matches.txt,leakage.tsv,unhandled.tsv}
rm -f .strip-versions/method-{a,b,c}-*.txt
```
Keep `version-candidates.tsv` and `.gitignore`.

### 3.3 Run inventory with three independent methods

The three methods exist to catch silent tool failures. If they disagree wildly (§3.4), halt.

#### Method A — ripgrep (no error masking)
```bash
set +e
rg -nE --no-config --no-ignore-vcs \
   '\b[Vv][0-9]+\.[0-9]+(\.[0-9]+)?\b|\b[Vv]ersion[: ]+[0-9]+\.[0-9]+|\bper\s+v?[0-9]+\.[0-9]+' \
   --glob '!thesis/**' \
   --glob '!.git/**' \
   --glob '!**/node_modules/**' \
   --glob '!**/build/**' \
   --glob '!**/dist/**' \
   --glob '!.strip-versions/**' \
   --glob '!STRIP_VERSIONS_PLAN.md' \
   --glob '!STRIP_VERSIONS_FIX_PLAN.md' \
   --glob '!STRIP_VERSIONS_REPORT.md' \
   --glob '!**/~$*' \
   --glob '!**/*.{pdf,pptx,docx,png,jpg,jpeg,gif,ico,woff,woff2,ttf,zip,bin}' \
   . \
   > .strip-versions/method-a-rg.txt 2> .strip-versions/method-a-stderr.txt
rg_rc=$?
echo "rg exit code: $rg_rc" > .strip-versions/method-a-rc.txt
# exit 0 = matches, 1 = none, ≥2 = error
[ $rg_rc -ge 2 ] && {
  cp .strip-versions/method-a-stderr.txt STRIP_FIX_FAIL_PHASE_2.md
  echo "ripgrep failed with code $rg_rc"
  exit 1
}
set -e
```
Key differences from the original plan:
- `--no-ignore-vcs` — do not let `.gitignore` filter results
- Stderr captured, not silenced
- Exit code inspected explicitly (`|| true` removed)
- No reliance on shell glob expansion of `*.md`
- Office and binary extensions added to excludes

#### Method B — POSIX grep cross-check
```bash
set +e
grep -rnE \
  --include='*.md' --include='*.py' --include='*.js' --include='*.jsx' \
  --include='*.ts' --include='*.tsx' --include='*.yaml' --include='*.yml' \
  --include='*.txt' --include='*.json' \
  --exclude-dir=thesis --exclude-dir=.git --exclude-dir=node_modules \
  --exclude-dir=build --exclude-dir=dist --exclude-dir=.strip-versions \
  --exclude='STRIP_VERSIONS_*.md' \
  '\b[Vv][0-9]+\.[0-9]+([.][0-9]+)?\b' \
  . > .strip-versions/method-b-grep.txt 2> .strip-versions/method-b-stderr.txt
grep_rc=$?
echo "grep exit code: $grep_rc" > .strip-versions/method-b-rc.txt
[ $grep_rc -ge 2 ] && {
  cp .strip-versions/method-b-stderr.txt STRIP_FIX_FAIL_PHASE_2.md
  echo "grep failed with code $grep_rc"
  exit 1
}
set -e
```

#### Method C — python re (canonical)
```bash
python3 - << 'PY'
import re, os, sys
patterns = [
    re.compile(r"\b[Vv][0-9]+\.[0-9]+(\.[0-9]+)?\b"),
    re.compile(r"\b[Vv]ersion[: ]+[0-9]+\.[0-9]+"),
    re.compile(r"\bper\s+v?[0-9]+\.[0-9]+"),
]
skip_dirs = {".git", "node_modules", "build", "dist", "thesis", ".strip-versions"}
skip_exts = {".pdf", ".pptx", ".docx", ".png", ".jpg", ".jpeg", ".gif",
             ".ico", ".woff", ".woff2", ".ttf", ".zip", ".bin"}
skip_files = {"STRIP_VERSIONS_PLAN.md", "STRIP_VERSIONS_FIX_PLAN.md",
              "STRIP_VERSIONS_REPORT.md"}

out = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
    for f in files:
        if f.startswith("~$") or f in skip_files: continue
        if os.path.splitext(f)[1].lower() in skip_exts: continue
        path = os.path.join(root, f).replace("\\", "/")
        if path.startswith("./"): path = path[2:]
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh, 1):
                    for p in patterns:
                        if p.search(line):
                            out.append(f"{path}:{lineno}:{line.rstrip()}")
                            break
        except Exception as e:
            sys.stderr.write(f"skip {path}: {e}\n")

with open(".strip-versions/method-c-python.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + ("\n" if out else ""))
print(f"Method C: {len(out)} matches", file=sys.stderr)
PY
```

### 3.4 Sanity gates
```bash
A=$(grep -c '' .strip-versions/method-a-rg.txt 2>/dev/null || echo 0)
B=$(grep -c '' .strip-versions/method-b-grep.txt 2>/dev/null || echo 0)
C=$(grep -c '' .strip-versions/method-c-python.txt 2>/dev/null || echo 0)
echo "A(rg)=$A  B(grep)=$B  C(python)=$C" | tee .strip-versions/method-counts.txt
```

**Halt and write `STRIP_FIX_FAIL_PHASE_2.md` if any of:**

- `A < 100` — repository has far more matches than this; an empty or near-empty scan signals tool failure.
- `C < 100` — same logic for python (the most reliable method).
- `|A - C| > 50` — methods disagree wildly; tool fault.
- `C == 0 && A > 0` or `A == 0 && C > 0` — clear silent failure on one side.

The diagnostic file must include all three counts, the first 30 lines of each output, and stderr from any method that returned non-zero exit.

### 3.5 Adopt Method C as canonical
```bash
cp .strip-versions/method-c-python.txt .strip-versions/raw-matches.txt
```

### 3.6 Classify

For each line in `raw-matches.txt` (format `path:lineno:text`), apply detection patterns from `thesis/governance/VERSIONING_POLICY.md §3` plus these rules. First match wins:

1. The matched token is `V[0-9]+` with no `.` following (proper noun, e.g., `V5 arm`): `PRESERVE`.
2. The matched token is `Stage [0-9]+` or part of a numeric literal (`1.0e-5`, `IDRiD_010`): `PRESERVE`.
3. The token is inside a Python identifier or a dict key used in logic (heuristic: the line matches `\[["']<token>["']\]` or `<token>\s*=` as left-hand assignment): `MANUAL`.
4. The line is a directory-tree listing in a plain text file that mentions an actual file path inside `thesis/` (e.g., `structure.txt` line referring to `ARCHIVED-chapter-01-review-prompt-v1.0.md`): `MANUAL` with reason "tree-listing reproduction of legitimate thesis/ filename".
5. The token is standalone `V1`/`V2`/`V3`/`V4` with no decimal: `MANUAL`.
6. The token matches any P1–P6 STRIP pattern: `STRIP`.
7. Otherwise: `MANUAL`.

Write `.strip-versions/classified.tsv` with header:
```
file<TAB>line<TAB>match<TAB>decision<TAB>reason
```

### 3.7 Summary preview
```bash
echo "=== Classification summary ==="
awk -F'\t' 'NR>1 {c[$4]++} END {for (k in c) print k": "c[k]}' .strip-versions/classified.tsv

echo "=== Per-directory STRIP counts ==="
awk -F'\t' 'NR>1 && $4=="STRIP" {
  split($1, parts, "/"); print parts[1]
}' .strip-versions/classified.tsv | sort | uniq -c

echo "=== First 10 STRIP rows ==="
awk -F'\t' 'NR>1 && $4=="STRIP"' .strip-versions/classified.tsv | head -10
```

### 3.8 Evidence-anchor gate

The 11 rows from §2 of this plan MUST each appear in `classified.tsv` with `decision == STRIP`. Implement as a tiny check script:
```bash
python3 - << 'PY'
import csv
expected = [
    ("defense/paradigmatic_speech.md", "4"),
    ("defense/paradigmatic_speech.md", "6"),
    ("defense/slide_plan.md", "33"),
    ("defense/idea.md", "6"),
    ("defense/slides/05a_PARADIGMATIC_POSITIONING.md", "62"),
    ("defense/slides/09_ARCHITECTURE_COMPARISON.md", "37"),
    ("defense/slides/08_CNN_ARCHITECTURE.md", "22"),
    ("demo/src/i18n.js", "68"),
    ("demo/src/tabs/ModelArchitecture.js", "41"),
    ("experiments/src/explainability/iou.py", "3"),
    ("experiments/scripts/generate_report.py", "452"),
]
found = set()
with open(".strip-versions/classified.tsv", encoding="utf-8") as fh:
    rdr = csv.reader(fh, delimiter="\t")
    next(rdr, None)
    for row in rdr:
        if len(row) < 4: continue
        if row[3] == "STRIP":
            found.add((row[0], row[1]))

missing = [e for e in expected if e not in found]
if missing:
    with open("STRIP_FIX_FAIL_PHASE_2.md", "w") as fh:
        fh.write("# Phase 2 evidence gate failed\n\n")
        fh.write("These expected STRIP matches are missing from classified.tsv:\n\n")
        for m in missing:
            fh.write(f"- {m[0]}:{m[1]}\n")
    import sys; sys.exit(1)
print(f"Evidence gate passed: all {len(expected)} anchors found")
PY
```

### 3.9 Commit
```bash
git add .strip-versions/
git commit -m "chore: rebuild inventory with multi-method verification (fix prior empty scan)"
```

---

## 4. Phase 3 (redo) — Strip

### 4.1 Apply edits

For each row in `.strip-versions/classified.tsv` where `decision == STRIP`, group by file and apply edits with the Edit tool (open file once, apply all changes in it).

### 4.2 Replacement table

| Match shape | Replacement |
|---|---|
| `**Version:** ... vN.M ...` as a full line | Delete the entire line. |
| `(vN.M ...)` parenthetical | Delete with parentheses. |
| `(governance vN.M)` parenthetical | Delete with parentheses. |
| `INVARIANTS.md vN.M`, `INVARIANTS vN.M`, `HYPOTHESIS.md vN.M`, `ARGUMENT_MAP.md vN.M`, `CONTRIBUTIONS.md vN.M`, `CENTRAL_THESIS.md vN.M` | Drop the version suffix; keep the file/section name. |
| `per governance vN.M`, `per INVARIANTS vN.M`, `per vN.M` | Replace with `per current governance` / `per INVARIANTS` / `per current`. |
| `vN.M / vN.M шектеуі`, `vN.M / vN.M constraint`, `vN.M / vN.M limitation` | Drop the version prefix entirely; keep the noun. |
| `Sources: thesis/governance/ vN.M (...)` | Replace with `Sources: thesis/governance/ (...)`. |
| `V5 arm (per governance vN.M)` | Replace with `V5 arm`. |
| `(per governance vN.M)` | Delete with parentheses. |
| `(H-1 гипотезасы — vN.M)`, `(... — vN.M)` em-dash form | Delete the version trailing part `— vN.M` and the surrounding parens if they now hold nothing meaningful. |
| Bare `vN.M` in inline prose | Delete and reflow whitespace; if removal leaves dangling punctuation, repair the sentence. |
| `Generated under governance vN.M` | Delete the entire phrase. |

When in doubt, delete with minimal collateral. Do not invent replacement text beyond the patterns above.

### 4.3 Per-file-type safety checks

- **`.py`**: after editing a file, run `python3 -m py_compile <file>`. On failure: revert with `git checkout -- <file>`, log to `.strip-versions/phase3-revert.log`, continue.
- **`.js` / `.jsx`** (`demo/`): after editing, run `node --check <file>` if `node` is available. On failure: revert and log.
- **`.yaml` / `.yml`**: after editing, run `python3 -c "import yaml,sys; yaml.safe_load(open('<file>'))"`. On failure: revert and log.
- **`.md`, `.txt`, `.json`**: no syntax check; edits are free-form text.

### 4.4 Commit per area
```bash
# Group commits by major area to keep diffs reviewable:
git add defense/ && git commit -m "chore(defense): strip version markers (fix-plan)"
git add demo/    && git commit -m "chore(demo): strip version markers (fix-plan)"
git add experiments/ && git commit -m "chore(experiments): strip version markers (fix-plan)"
# any root-level .txt/.json:
git add structure.txt 2>/dev/null && git commit -m "chore: strip version markers from root text files (fix-plan)" || true
```

If `.strip-versions/phase3-revert.log` has entries: continue, but include them in the run report as "Phase 3 reverts".

---

## 5. Phase 4 (redo) — Strict verification

### 5.1 Re-run all three scans

Repeat §3.3 (A/B/C) producing `.strip-versions/post-strip-method-{a,b,c}.txt`.

### 5.2 Reclassify and detect leakage
```bash
python3 - << 'PY'
import re
patterns_strip = [
    re.compile(r"\bv[0-9]+\.[0-9]+(\.[0-9]+)?\b"),
    re.compile(r"\bV[0-9]+\.[0-9]+(\.[0-9]+)?\b"),
    re.compile(r"\b[Vv]ersion[: ]+[0-9]+\.[0-9]+(\.[0-9]+)?\b"),
    re.compile(r"\bper\s+v?[0-9]+\.[0-9]+\b"),
]
preserve_proper_noun = re.compile(r"\bV[0-9]+(?![0-9\.])")

leakage = []
with open(".strip-versions/post-strip-method-c.txt", encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if not line: continue
        # crude: a STRIP-class hit is any match for a decimal-bearing pattern
        for p in patterns_strip:
            if p.search(line):
                # exclude pure proper-noun lines (no decimal)
                if not any(c.isdigit() and "." in line[max(0,line.find(c)-2):line.find(c)+4]
                           for c in line):
                    continue
                leakage.append(line)
                break

with open(".strip-versions/leakage.tsv", "w", encoding="utf-8") as fh:
    fh.write("post_strip_line\n")
    for l in leakage:
        fh.write(l + "\n")

print(f"Leakage count: {len(leakage)}")
if leakage:
    with open("STRIP_FIX_FAIL_PHASE_4.md", "w", encoding="utf-8") as fh:
        fh.write("# Phase 4 leakage\n\n")
        fh.write(f"{len(leakage)} STRIP-class lines remain outside thesis/.\n\n")
        fh.write("First 50:\n\n```\n")
        for l in leakage[:50]:
            fh.write(l + "\n")
        fh.write("```\n")
    import sys; sys.exit(1)
PY
```
Halt and do not push if `STRIP_FIX_FAIL_PHASE_4.md` is written.

### 5.3 thesis/ integrity check
```bash
git diff --name-only main..HEAD | grep '^thesis/' \
  | grep -vE '^thesis/governance/(CHANGELOG\.md|VERSIONING_POLICY\.md)$' \
  > .strip-versions/thesis-leaks.txt || true
if [ -s .strip-versions/thesis-leaks.txt ]; then
  cp .strip-versions/thesis-leaks.txt STRIP_FIX_FAIL_PHASE_4.md
  exit 1
fi
```

### 5.4 Office file content recheck

Tracked Office documents — `defense/presentation.pptx`, `defense/seminar-ready.pptx`, `defense/999.docx` — re-extract XML and grep:
```bash
mkdir -p .strip-versions/office-recheck
for f in defense/presentation.pptx defense/seminar-ready.pptx defense/999.docx; do
  base=$(basename "$f" | tr '.' '_')
  outdir=".strip-versions/office-recheck/$base"
  rm -rf "$outdir"; mkdir -p "$outdir"
  python3 -c "import zipfile,sys; zipfile.ZipFile('$f').extractall('$outdir')" 2>/dev/null || continue
  grep -rnE '\b[Vv][0-9]+\.[0-9]+|\b[Vv]ersion[: ]+[0-9]+\.[0-9]+' \
    --include='*.xml' \
    --exclude-dir='docProps' \
    "$outdir" > "$outdir/_content-hits.txt" 2>/dev/null || true
done
cat .strip-versions/office-recheck/*/_content-hits.txt > .strip-versions/office-content-hits.txt
```

`docProps/*.xml` is excluded because `cp:revision`, `<AppVersion>` etc. are OOXML structural metadata, not content. If `office-content-hits.txt` is non-empty: this is a known gap — these files need Office-aware unpack/repack. Log to MANUAL queue (do NOT halt — log and proceed).

### 5.5 Update the report

Overwrite `STRIP_VERSIONS_REPORT.md`:

```markdown
# Strip Versions — Run Report (revised by fix plan)

Date: <ISO timestamp>
Branch: chore/version-archaeology-and-strip
Authoritative version: v5.3.0

> **Note.** The first run of `STRIP_VERSIONS_PLAN.md` reported zero strip-class markers, but Phase 2 had silently produced an empty inventory due to error-masking shell wiring. This revision records the corrected results from `STRIP_VERSIONS_FIX_PLAN.md`.

## Phase 0 — Policy (unchanged from original run)
- `thesis/governance/VERSIONING_POLICY.md` created.
- Root `CLAUDE.md` block added.

## Phase 1 — Archaeology (unchanged from original run)
- Tags `v1.0.0..v5.3.0` on remote.
- `thesis/governance/CHANGELOG.md` with 8 sections.

## Phase 2 (redo) — Inventory
Method A (rg) matches: <N>
Method B (grep) matches: <N>
Method C (python, canonical) matches: <N>
- STRIP: <a>
- PRESERVE: <b>
- MANUAL: <c>

## Phase 3 (redo) — Strip
Files modified:
- Markdown: <count>
- JavaScript: <count>
- Python: <count>
- YAML: <count>
- Other: <count>
Reverts (syntax-check failures): <count> — see `.strip-versions/phase3-revert.log`

## Phase 4 (redo) — Verification
Post-strip STRIP-class leakage: 0 (verified)
Unexpected thesis/ modifications: 0
Office file content rechecks: <none | listed in MANUAL queue>

## Manual review queue
`.strip-versions/classified.tsv` (filter `decision == MANUAL`).
Count: <c>

## Stashed work
The fix plan stashed unrelated working-tree edits before starting.
Stash ref: `.strip-versions/stash-ref.txt`
Recover with `git stash list` and `git stash pop`.

## Branch state
<git log main..HEAD --oneline output>
```

### 5.6 Commit and push
```bash
git add STRIP_VERSIONS_REPORT.md STRIP_VERSIONS_FIX_PLAN.md .strip-versions/
git commit -m "chore: revised report after strip-plan fix-up"
git push origin chore/version-archaeology-and-strip
```

### 5.7 Stop
Do not merge to `main`. The user reviews the updated branch.

---

## 6. After Phase 4: restoring stashed work

```bash
git stash list                                 # find the fix-plan stash
git stash pop "stash@{<N>}"                    # apply
```
If `git stash pop` conflicts in `demo/src/i18n.js` (because Phase 3 modified that file): resolve manually, preferring the stashed UI changes and re-applying the Phase 3 strips after.

---

## 7. Failure protocol

If any `STRIP_FIX_FAIL_PHASE_N.md` exists at the end of execution:
1. Do not push.
2. Do not delete the failure file.
3. Exit cleanly. The user reviews the diagnostic.

---

## 8. Out of scope (still)

- Renaming files whose names contain version markers (`augmentation_v4.py`, `smoke_test_v4.py`). Renames break imports; tracked in MANUAL queue.
- `demo/public/diagrams/v5_pipeline_specification.md` filename — `v5` is the proper noun (pipeline name). Filename stays; content is treated by the normal STRIP/PRESERVE rules.
- Office file content edits if §5.4 finds content hits — those go to MANUAL for a separate pass with proper pptx/docx unpack/repack tooling.
- Squashing the new fix commits with the original four — keep history visible.
