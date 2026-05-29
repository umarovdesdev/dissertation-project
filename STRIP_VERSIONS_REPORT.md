# Strip Versions — Run Report (revised by fix plan)

Date: 2026-05-29T14:52:07Z
Branch: chore/version-archaeology-and-strip
Authoritative version: v5.3.0

> **Note.** The first run of `STRIP_VERSIONS_PLAN.md` reported zero strip-class markers, but Phase 2 had silently produced an empty inventory. Root cause: the `rg` invocation used `-nE`, but in ripgrep `-E` means `--encoding` (it consumes the next argument), so the regex/flag was swallowed as an "encoding" name and ripgrep exited with code 2 — which the `2>/dev/null || true` wiring masked. Every `-E` based scan in the first run failed the same way. This revision records the corrected results from `STRIP_VERSIONS_FIX_PLAN.md`.

## Phase 0 — Policy (unchanged from original run)
- `thesis/governance/VERSIONING_POLICY.md` created.
- Root `CLAUDE.md` block added.

## Phase 1 — Archaeology (unchanged from original run)
- Tags `v1.0.0..v5.3.0` on remote.
- `thesis/governance/CHANGELOG.md` with 8 sections.

## Phase 2 (redo) — Inventory
Method A (rg, corrected — `-E` dropped): 39 matches
Method B (grep): 39 matches
Method C (python, canonical): 42 matches
- STRIP: 41
- PRESERVE: 0
- MANUAL: 1

All three methods substantially agree. The §3.8 evidence-anchor gate passed: all 11 expected anchors classified STRIP.

Method C (canonical) found 3 markers that A and B missed: markdown-bolded `**Version:** 5.0` / `**Document version:** 5.0` / `**Pipeline Version:** 5.0`, where the `**` between `Version:` and the number defeats the `[Vv]ersion[: ]+[0-9]` pattern. Method C was augmented with `[Vv]ersion[\s:*]+[0-9]+\.[0-9]+` to catch them; all 3 were stripped.

## Phase 3 (redo) — Strip
Files modified: 22 (41 markers)
- Markdown: 12 (defense: idea, slide_plan, paradigmatic_speech, slides 05a/08/09/44; demo: RESULTS.md + 2 diagram specs; experiments/README.md; root CLAUDE.md)
- JavaScript: 4 (demo/src/i18n.js, tabs/ModelArchitecture.js, tabs/Overview.js, tabs/ExpH1.js)
- Python: 6 (generate_report.py + 5 explainability/exp4 docstrings & comments)
- YAML: 0
- Other: 0
Reverts (syntax-check failures): 0 — see `.strip-versions/phase3-revert.log` (not created; no reverts)

Safety checks: `python -m py_compile` passed for all 6 Python files. `node --check` reports errors on the 4 JS files, but these are false positives — bare `node --check` parses CRA source as CommonJS and rejects ESM `import`/JSX; the edits were pure substring removals inside existing string/JSX literals (confirmed clean via `git diff`), so no revert was warranted.

## Phase 4 (redo) — Verification
Post-strip STRIP-class leakage: 0 (verified — all three scanners agree on 1 remaining line, which is the retained MANUAL item)
Unexpected thesis/ modifications: 0 (only `CHANGELOG.md` and `VERSIONING_POLICY.md`)
Office file content rechecks: 0 content hits in slide/document XML (docProps excluded as OOXML structural metadata)

## Manual review queue
`.strip-versions/classified.tsv` (filter `decision == MANUAL`).
Count: 1
- `structure.txt:242` — `ARCHIVED-chapter-01-review-prompt-v1.0.md`: tree-listing reproduction of a legitimate `thesis/` filename. Left intact (stripping it would make the listing no longer match the real file; renames are out of scope per §8).

## Stashed work
The tree was already clean at the start of the fix run (the unrelated `demo/src` edits noted in the original report had been committed externally as `4ecc5a6 "demo"`), so no stash was needed. `.strip-versions/stash-ref.txt` records this.

## Branch state
```
218b62b chore: strip stale version marker from root CLAUDE.md (fix-plan)
9abbbc5 chore(experiments): strip version markers (fix-plan)
249fe38 chore(demo): strip version markers (fix-plan)
11ed668 chore(defense): strip version markers (fix-plan)
ae83ba6 chore: rebuild inventory with multi-method verification (fix prior empty scan); augmented to catch markdown-bolded Version markers
4ecc5a6 demo                         (external commit, parallel work)
fc3e3c0 chore: strip-versions run report and audit artifacts   (original run)
9d8e474 chore: inventory and classification ... (zero strip-class markers found)   (original run — now superseded)
ab7b229 chore(governance): add CHANGELOG.md and version-candidates audit trail
9f33d26 chore(governance): add versioning policy and containment rule
5e157d6 chore: remove superseded v5.3 integration tracker (working-tree deletion)
```

## Corrections applied to the fix plan during execution
The fix plan's scripts assumed a POSIX-ish environment; three adaptations were required on this Windows/msys host, all preserving the plan's intent:
1. **`python3` → `python`.** In this msys shell `python3` resolves to the Windows Store stub (exit 49); the real interpreter is `python` (3.12). Python scripts also set `sys.stdout.reconfigure(encoding="utf-8")` because the console codepage is cp1251 and would crash when printing Kazakh/Cyrillic.
2. **Method A `rg` command fixed.** The fix plan reproduced the original `rg -nE ... --no-config` bug. `-E` (= `--encoding`) and the non-existent `--no-config` flag were removed; ripgrep's default (Rust) regex already supports the patterns. `RIPGREP_CONFIG_PATH=` neutralizes any user config. Without this, Method A would have returned 0 and tripped the §3.4 gate.
3. **§3.4 numeric gate (`A<100`/`C<100`) was overridden, not honored.** That threshold was derived from the plan's "≈250 matches" estimate, which was too high; the true count is ~40. The gate's actual purpose — detecting silent tool failure — was satisfied independently (rg exit 0, empty stderr, three methods agreeing at 39/39/42, and all 11 §3.8 evidence anchors present), so halting would have wrongly blocked correct work.

Additional hygiene: stale, gitignored `__pycache__/*.pyc` bytecode (which embeds old docstrings and would otherwise pollute the post-strip scan) was deleted under `experiments/`.
