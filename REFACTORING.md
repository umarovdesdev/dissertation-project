# REFACTORING — Relocate all dissertation knowledge onto drive E:

**Status:** ✅ EXECUTED 2026-06-12 (per §7 recommendations: visible `PROJECT_MEMORY/`,
git-tracked, no symlink, C: memory stubbed-with-redirect). 14 memory facts → 12 files on E:
+ index; CLAUDE.md wired; `council/PEOPLE.md` + `demo/RUNBOOK.md` added; C: store retired.
**Created:** 2026-06-12

---

## 1. Problem

Persistent project knowledge ("memory") that Claude has been saving lives at:

```
C:\Users\yesmu\.claude\projects\E--dissertation-project\memory\   ← MACHINE-LOCAL
```

This path is inside the **per-user, per-machine** Windows profile. The candidate
works across **three machines** (work PC, home laptop, university) and carries the
project on an **external drive mounted as E:**. The C: memory directory does **not**
travel with the E: drive, so on every other machine that knowledge is missing or
stale. Anything dissertation-related must therefore live under `E:\dissertation-project\`.

**Goal:** every persistent fact about the dissertation is stored on E: (travels with
the drive, and is git-tracked), and Claude reads/writes it there — not in C: memory.

## 2. Principle (the decision this plan implements)

1. **Single portable store on E:.** Create `E:\dissertation-project\PROJECT_MEMORY\`
   (folder) + `PROJECT_MEMORY.md` (root index) — a 1:1 replacement for the harness
   memory, but on the drive. It is git-tracked and travels physically with E:.
2. **Auto-load via CLAUDE.md.** The root `CLAUDE.md` points Claude at this store so it
   is in context on every machine, regardless of Windows username or C: path.
3. **Domain facts also surfaced in their natural home** (demo runbook, experiments
   docs, council people file) so humans — not just Claude — find them.
4. **C: harness memory is retired** for this project: emptied down to a stub pointer
   that redirects to the E: store, so no future writes silently land back on C:.

> Why not just symlink the C: memory dir to E:? It would have to be re-created on each
> machine (different `C:\Users\<name>\` per box), it is not version-controlled, and a
> broken link fails silently. The in-repo store is portable and auditable. Symlinking is
> listed as a fallback in §7 only.

## 3. Inventory — 14 memory files to migrate

Source: `C:\Users\yesmu\.claude\projects\E--dissertation-project\memory\`

| # | Memory file | Topic | Natural domain home on E: |
|---|-------------|-------|---------------------------|
| 1 | `dissertation-people-names.md` | Candidate/supervisor/consultant names, programme code 8D06104, supervisor regalia | `council/PEOPLE.md` |
| 2 | `council-docs-skill.md` | MD→GOST docx/pdf skill | already self-documented in `.claude/skills/council-docs/SKILL.md` (on E:) — pointer only |
| 3 | `phase1-writing-complete.md` | Writing phase-1 done, what's gated | `thesis/PLAN.md` / `SUPERVISOR_HANDOFF.md` (already track this) |
| 4 | `chapter3-methodology-drafted.md` | Ch3 drafted & approved | `thesis/PLAN.md` |
| 5 | `literature-corpus-integrity-flags.md` | Missing/мismatched lit cards | `thesis/literature/INTEGRITY_FLAGS.md` |
| 6 | `config-d-shipped-retfound-deferred.md` | Pretraining axis RETFound→SSL, demo divergence | `experiments/docs/` |
| 7 | `kaggle-eyepacs-source-and-adapter-fix.md` | Kaggle EyePACS source + adapter fix | `experiments/colab/` notes |
| 8 | `colab-config-d-runner.md` | Colab Config-D runner two-mode | `experiments/colab/README.md` |
| 9 | `v5-preprocessing-throughput-bottleneck.md` | GPU-starve fix, precompute cache | `experiments/docs/` |
| 10 | `config-d-cache-mirror-handoff.md` | Cache work handoff, repo mirror task | `experiments/docs/` |
| 11 | `od-fovea-detector-unreliable-polar-centroid.md` | OD/fovea detector unreliable; polar pivots on centroid | `experiments/` preprocessing notes / `thesis/methods/` |
| 12 | `polar-clahe-now-default-retrain.md` | Stage 5 polar default → retrain | `experiments/` preprocessing notes |
| 13 | `strip-version-markers-outside-thesis.md` | Version-marker strip directive | `thesis/governance/VERSIONING_POLICY.md` note |
| 14 | `demo-local-stack-end-to-end.md` | Launch backend+frontend, Cloudflare tunnel | `demo/RUNBOOK.md` |

Plus the index `MEMORY.md` → becomes `PROJECT_MEMORY.md` on E:.

## 4. Target layout on E:

```
E:\dissertation-project\
├── PROJECT_MEMORY.md              ← index (was MEMORY.md); one line per fact
├── PROJECT_MEMORY\                ← portable store (the 14 facts, same frontmatter format)
│   ├── people-and-identifiers.md
│   ├── council-docs-skill.md
│   ├── thesis-writing-status.md   (consolidates #3 + #4)
│   ├── literature-integrity-flags.md
│   ├── config-d-pretraining.md
│   ├── config-d-kaggle-source.md
│   ├── colab-config-d-runner.md
│   ├── v5-cache-throughput.md
│   ├── config-d-cache-handoff.md
│   ├── preprocessing-od-fovea-polar.md   (consolidates #11 + #12)
│   ├── strip-version-markers.md
│   └── demo-runbook-pointer.md
├── council\PEOPLE.md              ← human-facing copy of identities (Track B)
├── demo\RUNBOOK.md                ← human-facing demo launch steps (Track B)
└── CLAUDE.md                      ← updated to load PROJECT_MEMORY (see §5)
```

## 5. Wiring into CLAUDE.md (so it loads on every machine)

Add to root `E:\dissertation-project\CLAUDE.md`:

```markdown
## Project memory — ON DRIVE E: (not C: harness memory)

Persistent project facts live in `PROJECT_MEMORY/` on this drive, indexed by
`PROJECT_MEMORY.md`. READ the index at session start and WRITE new durable facts
there — never into the machine-local `~/.claude/.../memory/` store (it does not
travel across the candidate's work PC / home laptop / university machines).
```

This makes the store first-class context regardless of Windows user or C: path.

## 6. Execution phases (checklist)

- [ ] **P0 — Snapshot.** Copy the 14 C: memory files into a temp staging area on E:
      (`PROJECT_MEMORY/_incoming/`) so nothing is lost mid-migration.
- [ ] **P1 — Create store.** Make `PROJECT_MEMORY\` + `PROJECT_MEMORY.md`; move each
      fact in, consolidating #3+#4 and #11+#12; keep the YAML frontmatter format.
- [ ] **P2 — Wire CLAUDE.md.** Add the §5 block to root `CLAUDE.md`.
- [ ] **P3 — Track B domain copies.** Create `council/PEOPLE.md`, `demo/RUNBOOK.md`;
      fold experiment facts into `experiments/docs/` and `experiments/colab/README.md`.
      Cross-link each to its `PROJECT_MEMORY/` entry.
- [ ] **P4 — Retire C: memory.** Replace every C: memory file with a one-line stub
      "MOVED → E:\dissertation-project\PROJECT_MEMORY\…"; reduce `MEMORY.md` (C:) to a
      single pointer line. (Do NOT delete blindly — leave the redirect.)
- [ ] **P5 — Commit.** `git add PROJECT_MEMORY PROJECT_MEMORY.md CLAUDE.md council/PEOPLE.md demo/RUNBOOK.md …`
      and commit so the store also syncs via git, not only the physical drive.
- [ ] **P6 — Verify portability.** Confirm no remaining dissertation fact is C:-only;
      `_incoming/` staging removed after parity check.

## 7. Open decisions (resolve before P1)

1. **Store name/visibility.** `PROJECT_MEMORY/` (visible, recommended) vs `.memory/`
   (hidden dotfolder). Recommend visible.
2. **Git-track the store?** Recommend YES (history + sync). If the candidate prefers the
   store to be drive-only and not in git, add it to `.gitignore` — it still travels on E:.
3. **Symlink fallback?** Only if a true single physical copy is wanted: per machine,
   `mklink /D "%USERPROFILE%\.claude\projects\E--dissertation-project\memory" "E:\dissertation-project\PROJECT_MEMORY"`.
   Not recommended as primary (per-machine setup, no version history).
4. **Delete vs stub C: memory.** Recommend stub-with-redirect (P4), not delete.

## 8. Going-forward convention (after migration)

- New durable dissertation fact → write to `E:\dissertation-project\PROJECT_MEMORY\`
  and add its index line to `PROJECT_MEMORY.md`. Never to C: harness memory.
- Operational facts (how to launch demo, run a Colab job, who signs a doc) → also
  update the human-facing domain doc (`demo/RUNBOOK.md`, `experiments/...`, `council/PEOPLE.md`).
- Commit the store with the related work so all three machines converge via git + drive.
