# REFACTORING — Dissertation monorepo audit & plan

**What this is.** A progressive, checkpoint-based audit of `E:\dissertation-project\`
with an actionable refactoring strategy. Goals: better structure, removal of
intermediate / obsolete / duplicated / temporary files, retirement of artifacts from
completed work, easier navigation, and stronger reproducibility + long-term
maintainability.

**How this document is built.** Work proceeds in checkpoints (~25k tokens of analysis
each). After each checkpoint the findings are appended here, then work STOPS and asks
permission before continuing. Nothing destructive is executed without it being recorded
here first.

**Conventions in this doc**
- 🔴 delete/remove · 🟠 move/relocate · 🟡 consolidate/dedupe · 🟢 keep (noted for context)
- "history rewrite" = removing a blob from all past commits (BFG / git-filter-repo), not
  just `git rm` (which leaves the bytes in `.git`).

---

## Checkpoint log

| # | Scope | Status | Date |
|---|-------|--------|------|
| 1 | Repo-wide inventory, size/bloat analysis, root-level & top-level structure | ✅ done | 2026-06-12 |
| 2 | `demo/` deep audit (web public assets, server, build artifacts) | ⬜ pending | — |
| 3 | `experiments/` deep audit (outputs, logs, src, colab/kaggle) | ⬜ pending | — |
| 4 | `defense/` + `council/` deep audit (pptx, figures, docs) | ⬜ pending | — |
| 5 | `thesis/` deep audit (chapters, literature, governance, output) | ⬜ pending | — |
| 6 | Git history rewrite plan + `.gitignore` hardening + execution sequencing | ⬜ pending | — |

> Checkpoint boundaries may shift as findings dictate; the table is updated each round.

---

## Checkpoint 1 — Inventory & top-level audit  ✅ 2026-06-12

### 1.1 Repository at a glance

- **Branch:** `main` (tracks `origin/main`). Working tree clean except
  `.claude/settings.local.json` (local, expected).
- **Tracked files:** 2,364.
- **On-disk size by top dir** (includes untracked/ignored content):

  | Dir | On-disk | Tracked files | Note |
  |-----|--------:|--------------:|------|
  | `demo` | **2,262 MB** | 1,474 | `web/node_modules` + `web/build` (untracked) + ~1 GB tracked images |
  | `experiments` | **869 MB** | 109 | almost all in `outputs/` (gitignored checkpoints/backups) |
  | `defense` | 142 MB | 305 | pptx decks + figures |
  | `server` | 124 MB | 19 | `checkpoints/` holds a model artifact (gitignored `.pth`?) |
  | `thesis` | 3.5 MB | 383 | text + literature cards (healthy) |
  | `council` | 0.2 MB | ~50 | governance reference docs |
  | `.claude` | 0.1 MB | 4 | skills |
  | `PROJECT_MEMORY` | ~0 | 12 | portable memory store (see Appendix A) |
  | **`.git`** | **927 MB** | — | ⚠️ history bloat — see §1.2 |

### 1.2 The headline problem: binary bloat in git (927 MB `.git`)

The repository's single biggest maintainability/reproducibility liability is **~1 GB of
binary blobs living in git** — both in the current tree and, worse, multiplied across
history.

**Largest blobs in history** (`git rev-list --objects --all`):

| Size | Path | Issue |
|-----:|------|-------|
| 48 / 48 / 40 MB | `defense/presentation/seminar-ready.pptx` (3 revisions) | same deck re-committed → ~136 MB of history for one file |
| 40 MB | `defense/presentation/presentation.pptx` | current deck |
| 31 MB | `defense/presentation/archive/presentation.pptx` | explicit *archive* of an old deck — pure dead weight |
| 8–9 MB ×~16 | `demo/web/public/images/pipeline/dr04/preprocessing/stage_*/...png` | full-res preprocessing-stage PNGs incl. debug overlays (`od/`, `fovea/`, `midpoint/`, `image/`) |
| 6–7 MB ×many | `demo/web/public/datasets/*/samples/*.png` | full-res fundus sample thumbnails |

**Type totals in current HEAD:** images ≈ **1,002 MB**, pptx ≈ **69 MB**, docx/pdf ≈ 2 MB,
other ≈ 10 MB. History adds repeated pptx revisions (~200 MB) on top.

**Implications**
- Every `clone`/`fetch` transfers ~1 GB; the candidate moves this repo across three
  machines on an external drive *and* via `origin` — both are penalised.
- The pptx files change often and never compress (binary OOXML), so each save bloats
  history by tens of MB. Three machines × git history = the dominant cost.

**Direction (to be detailed in Checkpoint 6):**
1. Decide what binary assets *belong in git at all*. Candidate: demo sample/pipeline
   PNGs and pptx decks are **derived/presentational**, regenerable or archivable outside
   git. Options: (a) Git LFS, (b) keep web images but downscale + strip debug overlays,
   (c) move pptx + large source images out of the repo onto the E: drive (untracked,
   travels physically) with a manifest.
2. **History rewrite** (git-filter-repo) to evict already-committed large pptx revisions
   and the `archive/` deck — the only way to shrink `.git` from 927 MB.
3. Harden `.gitignore` so binaries can't silently re-enter.

> ⚠️ History rewrite is the one irreversible action in this whole plan. It is deliberately
> deferred to the final checkpoint, gated behind explicit approval, and will be preceded
> by a full `.git` backup (bundle).

### 1.3 Root-level files — inventory & disposition

```
E:\dissertation-project\
├── CLAUDE.md              🟢 keep (project instructions; recently updated)
├── README.md             🟢 keep (622 B, thin — could grow a nav section)
├── .gitignore            🟢 keep (audit/extend in CP6)
├── PROJECT_MEMORY.md      🟢 keep (portable-memory index — Appendix A)
├── PROJECT_MEMORY/        🟢 keep (12 memory facts)
├── REFACTORING.md        🟢 keep (this file)
├── TASK.md               🟠/🟡 28 KB operational task log (Config-D + demo launch),
│                              "Updated 2026-06-02"; itself a consolidation of two older
│                              task docs. Operational handoff, not dissertation content.
│                              → audit for completed items, relocate under a docs/ or
│                                ops/ area or archive once Config-D run closes.
├── SUPERVISOR_HANDOFF.md 🟠 18 KB two-instance-workflow operating brief. Process doc,
│                              not deliverable. → relocate to a docs/ or .claude/ area;
│                              verify it isn't stale vs current workflow.
└── download_dc.sh        🔴/🟠 one-off bash helper to scrape council docs from the IITU
                               site; hardcoded absolute paths (`E:/dissertation_council`,
                               Cyrillic dirs), violates the repo's "no hardcoded paths"
                               rule. Likely already-run scaffolding. → confirm obsolete,
                               then remove or move to council/scripts/ with a header.
```

**Root clutter assessment.** The root mixes three concerns: (a) genuine project entry
points (`CLAUDE.md`, `README.md`, governance/memory), (b) **operational/process handoff
docs** (`TASK.md`, `SUPERVISOR_HANDOFF.md`), and (c) a **stray utility script**
(`download_dc.sh`). Recommendation (decide in a later CP): introduce a single `docs/` or
`ops/` home for (b)+(c) so the root presents only entry points. This is low-risk and high
navigability payoff.

### 1.4 Top-level structure observations (to deep-dive in CP2–5)

- **`demo/` vs root `server/` split.** CLAUDE.md describes the demo as `web/` + `server/`,
  but there are **two** server trees: `demo/server/` (19 tracked files) *and* a top-level
  `server/` (19 tracked files, 124 MB incl. a checkpoint). Strong duplication smell —
  one is likely the live copy and the other a stale fork/mirror. **Flag for CP2** to
  diff them and collapse to one.
- **`experiments/outputs/`** holds `backup_exp1_abc_40pct_20260324/`, `backup_exp1_full/`,
  `checkpoints/`, `kaggle_config_d/`, `kaggle_config_d_v2/`, `validation/` — dated backups
  and v1/v2 duplicates (869 MB). Gitignored, so not a *git* problem, but a disk/clarity
  problem and a reproducibility-hygiene question. **CP3.**
- **`experiments/logs/` is tracked** and contains `*.log` and **`*.pid`** files
  (`exp1_D_fold2.pid`, `exp1_remaining.pid`, …). PIDs are meaningless across machines and
  logs are run residue — **🔴 these should not be in git.** Quick win, scheduled for CP3.
- **`defense/presentation/archive/`** — an in-repo archive folder of superseded decks
  (31 MB pptx). Archetypal "completed-stage artifact". **🔴 CP4.**
- **`council/ru/…`** filenames are URL-escaped Cyrillic; fine functionally but worth a
  glance for encoding/portability in CP4.
- **`demo/web/{node_modules,build}`** present on disk (~1.1 GB, untracked/ignored).
  Expected; just confirm both are ignored and document a clean-rebuild step (CP2).

### 1.5 Quick wins identified (low-risk, high-value — staged for their CPs)

1. 🔴 Untrack `experiments/logs/*.log` + `*.pid` and ignore the pattern. *(CP3)*
2. 🔴 Remove `defense/presentation/archive/presentation.pptx` (31 MB) from tree + history. *(CP4/CP6)*
3. 🟡 Resolve the `demo/server/` ↔ root `server/` duplication. *(CP2)*
4. 🟠 Give `TASK.md` / `SUPERVISOR_HANDOFF.md` / `download_dc.sh` a non-root home. *(later)*
5. 🔴 Plan history rewrite for pptx + oversized PNGs to reclaim most of the 927 MB `.git`. *(CP6)*

### 1.6 Method notes (for reproducibility of this audit)

- Sizes from `git ls-tree -r -l HEAD` (tracked) and PowerShell recursive `Length` sums
  (on-disk). History blobs from
  `git rev-list --objects --all | git cat-file --batch-check`.
- No files changed in this checkpoint — inventory only.

---

> **Checkpoint 1 complete.** Continue to the next checkpoint?

---
---

# Appendix A — COMPLETED: Relocate dissertation memory onto drive E:

> This was the previous occupant of REFACTORING.md and is retained as a record. It is a
> finished task (memory migration), not part of the active structural refactor above.

**Status:** ✅ EXECUTED 2026-06-12 (per §7 recommendations: visible `PROJECT_MEMORY/`,
git-tracked, no symlink, C: memory stubbed-with-redirect). 14 memory facts → 12 files on E:
+ index; CLAUDE.md wired; `council/PEOPLE.md` + `demo/RUNBOOK.md` added; C: store retired.
**Created:** 2026-06-12

## A.1 Problem

Persistent project knowledge ("memory") that Claude has been saving lived at
`C:\Users\yesmu\.claude\projects\E--dissertation-project\memory\` — a **machine-local**
path. The candidate works across **three machines** (work PC, home laptop, university)
carrying the project on an **external drive (E:)**; the C: memory does not travel, so that
knowledge was missing/stale elsewhere. **Goal:** every persistent dissertation fact lives
under `E:\dissertation-project\` (travels + git-tracked), read/written there, not on C:.

## A.2 Principle implemented

1. Single portable store `PROJECT_MEMORY\` + `PROJECT_MEMORY.md` index on E: (git-tracked).
2. Auto-loaded via root `CLAUDE.md` so it is in context on every machine.
3. Domain facts also surfaced in their natural home (`demo/RUNBOOK.md`,
   `experiments/...`, `council/PEOPLE.md`) for humans.
4. C: harness memory retired to redirect stubs so future writes don't land back on C:.

## A.3 Result

14 source memory files were migrated/consolidated into 12 files under `PROJECT_MEMORY/`
(`#3+#4` → `thesis-writing-status.md`; `#11+#12` → `preprocessing-od-fovea-polar.md`),
indexed by `PROJECT_MEMORY.md`. The C: store and its `MEMORY.md` were reduced to redirect
pointers. CLAUDE.md gained a "Project memory — ON DRIVE E:" section.

## A.4 V5 leak fix (version markers escaping `thesis/`) — 2026-06-12

**Rule (binding):** version markers stay **inside `thesis/` only**, and this includes the
token **`V5`** (it denotes the fifth pipeline version). Outside `thesis/` the pipeline is
"the preprocessing pipeline" / "the 8-stage pipeline" / "конвейер" / "pipeline".

**Problem:** the council-docs skill rendered `thesis/output/*.md` (where `V5` is allowed)
verbatim into `defense/docs/*.docx`+`.pdf`, leaking `V5` outside `thesis/`.

**Fix:** added `strip_version_markers()` to
`.claude/skills/council-docs/scripts/md2gost.py`, called in `convert(...)`
(`strip_versions=True`). Removes `(V5)` parentheticals, bare tokens (`V5`, `v5.2`, `V4`,
`V3`), and word forms (`version 5.x`, `версия 5`, `нұсқа 5`). Source `thesis/output/*.md`
left unchanged; all 5 deliverables rebuilt and verified to contain zero `V[345]` markers.

**Going forward:** any new export pathway out of `thesis/` must apply the same scrub;
grep the destination for `[Vv][345]` before committing.
