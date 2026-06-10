# SUPERVISOR HANDOFF — Dissertation Autonomous Writing Pipeline

**Purpose of this file:** You are the **supervising instance** taking over the strategy/review/translation role in a two-instance workflow for writing a doctoral dissertation. This document is your complete operating brief. Read it fully before acting. Another Claude Code instance (the **executor**) does the file manipulation; you plan, review, verify, and translate. Nothing here overrides the project's own governance — when in doubt, the repo's `thesis/governance/` v6.0.0 is authoritative.

---

## 1. The two-instance architecture

- **Supervisor (you).** You converse with the candidate, who writes in **Russian**. You (a) turn his Russian ideas/questions into precise **English prompts** for the executor, (b) review and **verify** the executor's English output by reading the real files, and (c) explain results back to him **in Russian**. You decide *what* happens next; you do not write dissertation prose yourself.
- **Executor.** A separate Claude Code instance with full access to the monorepo. It runs the writing pipeline (briefs, drafts, verification, continuity notes) and edits files. It only acts on the prompts you hand the candidate to pass along.
- Both instances are Claude Code, in **different chats**. You are the one reading this file.

### Bilingual protocol (do not drop this)
- Candidate → you: Russian (raw, terse — he prefers direct, minimal filler).
- You → candidate: a ready-to-paste **English** prompt block for the executor, plus your Russian explanation/recommendation.
- Executor → you (via candidate): English. You translate the substance to Russian and give your assessment.

---

## 2. Core working principles (how this role has been performed — keep doing this)

1. **Verify, don't trust.** Always read the actual files before endorsing executor output. The executor's summaries have been accurate, but every consequential claim was independently checked (grep, reading the real card/draft/governance line). This caught real issues. Do the same.
2. **Stop-and-review gates.** Never let the executor run unbounded. The cadence is: one calibration unit → review → then scale. Specifically: §1.1.1 alone first (calibration), then the rest of Chapter 1 in one pass, then chapter-by-chapter (2 → 3 → 6 → §4.1). Do not authorize "write everything at once."
3. **Ground every edit in governance, verbatim.** When fixing or aligning anything, instruct the executor to pull exact wording/values from `thesis/governance/` (INVARIANTS, HYPOTHESIS, CONTRIBUTIONS, ARGUMENT_MAP, RESEARCH_ARCHITECTURE) — never paraphrase from memory, never invent numbers. If a value isn't explicit in governance, it gets a `[VERIFY]` flag, not a guess.
4. **Never fabricate data.** No metric, caption, or path may be invented. Demo-dashboard preview JSONs (placeholder numbers like APTOS G=0.890, exp3 G=0.812) are explicitly barred as results (CFC-2.x / SIR-1). A section that needs a ❌ MISSING resource stays blocked.
5. **Two-phase for any infra change.** For audits/edits to shared infrastructure (prompts, outline), require **Phase 1 REPORT (change nothing) → candidate approval → Phase 2 APPLY**. Ask the executor to quote stale lines so they can be verified.
6. **Calibrate before scaling.** The first unit of any new type is a calibration probe — check depth, tone, citation style, figure-placeholder format, word count, and whether the new brief fields (Argumentative Spine, Acceptance Criteria) are genuinely *used*, not just filled.
7. **One question at a time when a decision is needed**, with 2–4 concrete options. The candidate decides direction; you give a clear recommendation first.

---

## 3. What the project is (minimal orientation)

- Doctoral dissertation: **Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification.** Candidate: Yesmukhamedov N.S. (IITU, Almaty).
- Central thesis: `model = preprocessing + CNN`. The dissertation is written in **English**; final output is a single `.docx`. A Kazakh translation pipeline exists (Stage F).
- Monorepo layout: `thesis/` (the writing + governance + literature), `experiments/` (PyTorch, 7 experiments), `demo/` (React + FastAPI dashboard), `defense/` (slides), plus `council/` (defense-council regulatory docs, EN+RU). The executor has all of it; the supervisor reasons over `thesis/` primarily.
- **V5 pipeline:** 8 stages (0–7), 4-channel input (RGB + FOV mask), Focal Loss (γ=2), ResNet-50 + EfficientNet-B3 backbones, 7 experiments, datasets EyePACS (100%, ~35k), IDRiD, Messidor-2, APTOS 2019, clinical set. Hypotheses H-1, H-2, H-4, H-5, H-6, H-7 (H-3 dropped).
- **H-1 is "Integrated Pipeline Dominance"** with a *composite* independent variable (baseline⟹ImageNet pretrain vs V5⟹ophthalmology-specific SSL pretrain). **CFC-2.8 forbids attributing the effect to preprocessing alone.** This is the single most likely overclaim in the whole dissertation — guard it everywhere.
- **PC-0 / paradigm framing (P1/P2):** the "principal conceptual contribution." Gulshan et al. (2016) is the canonical P1 representative and may be described by *observed methodological practice only* (CFC-2.9 / SIR-9). Permitted: "treat preprocessing as ancillary data preparation," etc. Forbidden: "Gulshan claims preprocessing is unimportant," "Gulshan is our baseline," "we outperform Gulshan."

---

## 4. What has been built in this chat (all complete and consistent at v6.0.0)

1. **Prompt pipeline upgraded to v6.0.0** (`thesis/prompts/`). It was stale at v1.0 and missing the entire v5.3 paradigm apparatus. Now:
   - `writing-session-system-prompt.md` — added binding rules 11–16: **CFC-2.8** (no preprocessing-alone attribution), **CFC-2.9 + SIR-9** (verbatim permitted/forbidden Gulshan phrasings), **SIR-2/7/8**, unsourced-claim→flag rule; **analytical-depth** directive; **PART 3 strengthened** to require a verbatim quote + location per constraint.
   - `verification-protocol.md` — §B extended (CFC-2.6/2.8/2.9, NC-14…17), §D extended (SIR-2/7/8/9), new **§F Scope & Paradigm** (SB-1.12, DGL-6, P1/P2), new **§G Evidence Thresholds** (EH-3: ≥5pp weighted-F1 AND ≥0.02 ROC-AUC AND no Kappa degradation; EH-4), claim-coverage check; VERDICT renumbered §H.
   - `section-brief-template.md` — added **Argumentative Spine**, **Acceptance Criteria**, **Counter-Argument & Inherited Limitations (SIR-2)**, **Paradigm positioning**, **Analytical-depth** directive; SC-namespace disambiguation (SC-x.y sub-claims vs SC-A…H contributions).
   - Created `translation-review.md` (Stage F template). 3 utility prompts kept; 0 deletions.
2. **`thesis/ASSET_INVENTORY.md`** — honest catalogue of every figure/table/result with stable Resource IDs (FIG-x.x, TAB-x.x, RES-*), real paths, and ✅ AVAILABLE / ⏳ PENDING / ❌ MISSING status + gap analysis.
3. **`thesis/PLAN.md`** — the master writing plan and live to-do board. Progress tracker (⬜/🟦/🟩/✅), data-readiness phasing, per-section task tables (word count, governance bindings, literature-card IDs, Resource IDs, ✅ writable / ⛔ blocked), the per-section execution loop (§10), final assembly (§11). **51 sections writable now, 42 blocked pending experiments.**
4. **`thesis/outline/MASTER_OUTLINE.md` re-synced to v6.0.0** — it had been a second, conflicting numbering source (v5.0 header, old Ch 5 numbering, 6-config/3-fold residue, H-1 "Preprocessing Dominance" wording, missing SSL sections, stale traceability matrix). Now: PLAN ↔ OUTLINE ↔ INVENTORY are consistent with **zero divergences**; the authoritative numbering is the `LITERATURE_INDEX.md` v6.0.0 Section Map Key.

---

## 5. Exact current position (updated 2026-06-10)

> This section was rewritten 2026-06-10 to match the real state of the files on disk. The prior version described the position as "end of §1.1.1"; that is obsolete. `thesis/PLAN.md`'s progress tracker is current and authoritative — cross-check against it.

**Completed and verified ✅ APPROVED (drafts + briefs + continuity + reviews on disk):**
- **Chapter 1 — Problem Domain: COMPLETE.** All 11 sections (§1.1.1 → §1.C) verified 2026-06-09. §1.1.1 remains the **quality bar** (argumentative spine realized, external stats framed as third-party context per CFC-2.3, SIR-2 limitation notes at first citation, low-reliability #31 Kesharwani caveated, PART 3 with verbatim quotes). Corpus fix from the earlier pass landed: `schmidt-erfurth-2018.md` → `kusuhara-2018.md` renamed, `LITERATURE_INDEX.md` #32 + draft header updated, zero stale refs.
- **Chapter 2 — Theoretical Foundations: COMPLETE except deferred §2.3.3.** 14 sections verified 2026-06-09. **§2.3.3 (In-Domain SSL for Retinal Imaging) is intentionally DEFERRED** (candidate directive) until in-domain SSL cards (DINO/BYOL/SimCLR/MoCo-on-fundus) are acquired — #73 is a general survey only. It is named-only in §2.3.1/§2.3.2. FIG-2.1/2.3/2.4/2.5 inserted as `TO BE CREATED` placeholders (deferred assets, not blockers).
- **Chapter 3 — Methodology: COMPLETE.** All 13 sections (§3.1.1 → §3.C) verified 2026-06-09. Fully unblocked chapter; every asset real and on disk.
- **Chapter 6 — System Architecture: COMPLETE.** All 9 sections (§6.1.1 → §6.C) APPROVED on disk; committed in `4b6898f` (§6.1.1+§6.1.2) and `04fa027` (§6.2.1–§6.C + tracker sync). §6.1.2 carries the deferred DIA-6.3 UML as a `TO BE CREATED` placeholder (not a blocker).
- **§4.1 — Datasets & Configuration: COMPLETE.** All 3 sections (§4.1.1 ~1,200 w, §4.1.2 ~1,000 w, §4.1.3 ~720 w) APPROVED 2026-06-10, verified on disk; design/setup only, no experiment metrics, per-grade counts deferred to FIG-4.1 not fabricated (SIR-1 clean). #47/#48/#49/#50/#51 cited at index-level only with missing-card status flagged; #41 cited for EyePACS scale only (its AUC/accuracy excluded). **NOT YET COMMITTED** — 12 §4.1 files + modified PLAN.md are uncommitted in the working tree on `main`.

- **Appendix A (preprocessing source code) + Appendix D (certificates & publications): COMPLETE.** Both APPROVED 2026-06-10, saved under `thesis/chapters/08-appendices/`, verified on disk. App A reproduces real on-disk pipeline source (flat_field.py byte-for-byte verified against `experiments/src/preprocessing/`; stage→module map Table A.1). App D = 5 card-backed co-authored publications + the 6 real confirmation PNGs in `defense/presentation/assets/publications/`; self-works identified (SIR-4), no fabricated entries. **NOT YET COMMITTED** — `thesis/chapters/08-appendices/` (untracked) + modified PLAN.md.

**▶ PHASE 1 IS COMPLETE.** All 51 writable-now sections + App A + App D are drafted and APPROVED. The only Phase-1 prose still parked is **deferred §2.3.3** (in-domain SSL — held by candidate directive until DINO/BYOL/SimCLR/MoCo-on-fundus cards are acquired; not a normal blocker).

**Next action is NOT drafting — everything remaining is Phase 2, hard-blocked on experiment results.** Do NOT let §4.2–§4.8, Ch 5, Ch 0 (except the 🟨 content-writable-now front-matter items, at candidate's discretion), Ch 7, or App B/C/E/F be drafted until the real experiment artifacts exist (RES-EXP1 full, TAB-4.x, FIG-4.x — currently ❌ MISSING; demo preview JSONs are barred as results per CFC-2.x/SIR-1). App C is unblocked only by the DIA-6.3 UML asset (drawing task, not an experiment). The supervisor's job now shifts to: commit App A/D, optionally pull forward the writable-now Ch 0 front-matter (§0.FM1–3, §0.1–0.7, §0.9–0.12), and otherwise **wait on experiments**.

**⚠️ State drifts in real time.** The executor writes files in a parallel chat faster than `PLAN.md`'s tracker and this handoff get updated. As of 2026-06-10 the `PLAN.md` tracker still shows Chapter 6 as mostly ⬜ even though all 9 sections are APPROVED on disk. **Trust the real files (drafts/ + reviews/ verdict), not the tracker checkboxes.** Before dispatching anything, re-glob `thesis/chapters/*/drafts/` and `reviews/` to confirm the true frontier.

**Your immediate next action:** (1) ask the executor to **sync the `PLAN.md` tracker** (mark §6.1.2…§6.C ✅) and **commit** the Chapter 6 + §6.1.1 outputs under a clear message so nothing is lost; (2) spot-check 2–3 Chapter 6 drafts against the §1.1.1 standard (design-only framing held? NFR/architecture grounded in #22, not invented? word counts — several ran high, e.g. §6.1.1≈2.4k, §6.1.2≈2.6k including tables/PART2-3); (3) then dispatch §4.1.1 → §4.1.3 through the PLAN §10 loop, STOP at §4.1.3, review, then App A + App D. Aim mid-band on word count.

---

## 6. The plan from here

- **Phase 1 (writable now): ✅ COMPLETE** — Chapter 1 ✅ → Chapter 2 ✅ → Chapter 3 ✅ → Chapter 6 ✅ → §4.1 ✅ → App A + App D ✅. Deferred §2.3.3 is the only Phase-1 prose still parked (candidate directive). **Next supervisor action: commit App A/D, then either pull forward writable-now Ch 0 front-matter or wait on experiments.**
- **Phase 2 (blocked, gated on experiment execution):** §4.2 (Exp 1) → §4.3–§4.8 (Exp 2–7) → Chapter 5 → Introduction (Ch 0) → Conclusion (Ch 7) → Appendices B/C/E/F. Each gate (G-1…G-19 in PLAN) names the exact MISSING Resource IDs that unblock it. **Do not let these be drafted until the real experiment results exist** — the uploaded `results/exp2…exp7` currently hold only preview PNGs and placeholder JSON, not real runs.
- **Phase 3 (last):** concatenate all drafts per outline → resolve every `[FIG/TAB-x.x]` placeholder to its real asset → convert to a single `.docx`. Only after Phase 2 is complete.

---

## 7. Open watch-items (track these; none is blocking)

1. **Latent ID inconsistency in governance.** `INVARIANTS.md` SIR-7/SIR-8 refer to self-works as `LC-Yesmukhamedov-2025-SELF` and `LC-2025-Yesmukhamedov-01`, while the literature cards' own §I Unique IDs use the `LC-SAPAKOVA-2025[-01]` form (Sapakova is first author). The prompts correctly quote INVARIANTS verbatim, so this is not a prompt bug — but it will bite at **bibliography assembly (Phase 3)** if not reconciled. Flag for a dedicated reconciliation pass before final citations.
2. **Literature corpus integrity (partially resolved).** The `kusuhara-2018.md` rename is done. Still OPEN per drafting flags: cards #47/#49/#50/#51 are index-only (no card files; #51 unconfirmed), a `scopus-q2.md` ID mismatch (`LC-AlTimemy-2021` vs the EEJET citation), and #46 (Selvaraju, Grad-CAM) is index-only/absent. None blocks current prose but all bite at Phase-3 bibliography assembly. Reconcile before final citations.
3. **Word-count tendency to run high** — calibration to aim mid-band was issued and held across Chapters 1–3. Keep enforcing it for Chapter 6 and §4.1.
4. **`§2.4.2`** (a leaf subsection of the laser/thermal-optical model) is not enumerated in the Section Map Key but doesn't conflict with it; left as-is intentionally. Revisit only if it causes a numbering question later.
5. **Deferred conceptual diagrams** (FIG-2.1/2.3/2.4/2.5, DIA-6.3 / UML): not experiment-gated. Prose for Ch 2/Ch 6 is writable now; these figures are queued as asset tasks and inserted as `TO BE CREATED` placeholders. Don't let a missing *conceptual* diagram block prose.
6. **Uncommitted work.** The §6.1.1 outputs (`thesis/chapters/06-system-architecture/{briefs,drafts,continuity,reviews}/6.1.1-*.md`) plus a modified `thesis/PLAN.md` are currently **untracked/unstaged in the working tree on `main`**. Have the executor commit each completed chapter/section under a clear message so drafts don't get lost. (Earlier prompt-pipeline infra edits were similarly left on `feat/render-norm-polar-validation-fixes`.)

---

## 8. The per-section execution loop the executor runs (PLAN §10)

For each writable section, in order: (a) generate Section Brief from `section-brief-template.md` v6.0.0 — fill **all** fields incl. Argumentative Spine, Acceptance Criteria, Paradigm positioning; (b) self-review brief against governance, flag coverage gaps; (c) gate pre-check (every referenced resource ✅ AVAILABLE or literature-derived, no ❌ MISSING); (d) draft via `writing-session-system-prompt.md` v6.0.0 — prose + tables in Markdown, figures referenced as `[FIG/TAB-x.x: caption — real path]` placeholders, **not embedded**; include PART 3 compliance checklist with verbatim quote per constraint; (e) verify via `verification-protocol.md` v6.0.0 → APPROVED or REVISE (revise until APPROVED); (f) write continuity-note for the next section, save draft to the chapter's `drafts/`, update PLAN tracker.

---

## 9. Quick reference — authoritative files

- Numbering authority: `thesis/literature/LITERATURE_INDEX.md` (v6.0.0 Section Map Key).
- Content/governance authority: `thesis/governance/` (INVARIANTS, HYPOTHESIS, ARGUMENT_MAP, CONTRIBUTIONS, RESEARCH_ARCHITECTURE, CENTRAL_THESIS) — all v6.0.0.
- Plan & status: `thesis/PLAN.md`. Resources: `thesis/ASSET_INVENTORY.md`. Section spec: `thesis/outline/MASTER_OUTLINE.md`.
- Pipeline prompts: `thesis/prompts/` (all v6.0.0).
- Per-chapter outputs: `thesis/chapters/<n>-<name>/{briefs,drafts,reviews,continuity}/`.
- Glossaries: `thesis/glossary/GLOSSARY_EN.md`, `GLOSSARY_KZ.md`.

---

## 10. First message to send the candidate (suggested, in Russian)

> Контекст принят — я продолжаю как сопровождающий: перевожу твои идеи в промпты для исполнителя, проверяю его вывод по реальным файлам и объясняю результат. Сейчас на исполнении: фикс карточки Kusuhara + остаток главы 1 (до §1.C). Как пришлёт результат — проверю и доложу. Присылай его отчёт сюда.

(Then, when the executor's Chapter 1 report arrives: verify against real files per §5, report in Russian, recommend next step.)
