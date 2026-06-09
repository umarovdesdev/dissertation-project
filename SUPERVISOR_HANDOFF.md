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

## 5. Exact current position

- **§1.1.1 (Pathophysiology and Clinical Grading Systems) is written, verified ✅ APPROVED, and reviewed by the supervisor.** Quality confirmed high: argumentative spine realized, all external statistics framed as third-party context (CFC-2.3 clean), SIR-2 limitation notes at first citation, low-reliability source #31 (Kesharwani) handled with explicit caveats, PART 3 checklist with verbatim quotes. This is the **quality bar** for every subsequent section.
- **In flight (just dispatched to the executor):** a single pass with two steps:
  - **Step 1 — corpus fix:** rename `thesis/literature/external/schmidt-erfurth-2018.md` → `kusuhara-2018.md` (its content is actually Kusuhara et al. 2018; "Schmidt-Erfurth" is only cited inside it), update `LITERATURE_INDEX.md` #32 and the §1.1.1 draft header, grep for zero stale refs, and flag any other filename↔content mismatches found.
  - **Step 2 — rest of Chapter 1:** run §1.1.2 → §1.2.1 → §1.2.2 → §1.2.3 → §1.3.1 → §1.3.2 → §1.3.3 → §1.4 → §1.5 → §1.C through the PLAN §10 loop. Calibration tweaks applied: **aim mid-band on word count** (§1.1.1 ran to the ceiling), keep the §1.1.1 standard exactly.
  - Executor instructed to **STOP at end of §1.C** and return a chapter-level summary (per-section word count, verdict, sources, coverage gaps) + the Step 1 confirmation.

**Your immediate next action when the executor reports back:** read the real files (don't just trust the summary), verify the corpus fix actually removed all stale `schmidt-erfurth-2018` refs, spot-check 2–3 of the new drafts against the §1.1.1 standard, confirm word counts came down mid-band, then report to the candidate in Russian and recommend whether to release Chapter 2.

---

## 6. The plan from here

- **Phase 1 (writable now), narrative order:** Chapter 1 → Chapter 2 → Chapter 3 (fully unblocked) → Chapter 6 (design-only) → §4.1. Release chapter-by-chapter with a review after each. After Chapter 1 proves the loop, larger blocks are fine.
- **Phase 2 (blocked, gated on experiment execution):** §4.2 (Exp 1) → §4.3–§4.8 (Exp 2–7) → Chapter 5 → Introduction (Ch 0) → Conclusion (Ch 7) → Appendices B/C/E/F. Each gate (G-1…G-19 in PLAN) names the exact MISSING Resource IDs that unblock it. **Do not let these be drafted until the real experiment results exist** — the uploaded `results/exp2…exp7` currently hold only preview PNGs and placeholder JSON, not real runs.
- **Phase 3 (last):** concatenate all drafts per outline → resolve every `[FIG/TAB-x.x]` placeholder to its real asset → convert to a single `.docx`. Only after Phase 2 is complete.

---

## 7. Open watch-items (track these; none is blocking)

1. **Latent ID inconsistency in governance.** `INVARIANTS.md` SIR-7/SIR-8 refer to self-works as `LC-Yesmukhamedov-2025-SELF` and `LC-2025-Yesmukhamedov-01`, while the literature cards' own §I Unique IDs use the `LC-SAPAKOVA-2025[-01]` form (Sapakova is first author). The prompts correctly quote INVARIANTS verbatim, so this is not a prompt bug — but it will bite at **bibliography assembly (Phase 3)** if not reconciled. Flag for a dedicated reconciliation pass before final citations.
2. **Misnamed literature card** (being fixed now in Step 1). After the executor reports, confirm the rename + index update are clean and that no other card has a filename↔content mismatch (the executor was asked to flag others without fixing them — decide what to do with any it finds).
3. **Word-count tendency to run high** — §1.1.1 hit the top of its band. Calibration instruction issued to aim mid-band; verify it took effect in the Chapter 1 batch.
4. **`§2.4.2`** (a leaf subsection of the laser/thermal-optical model) is not enumerated in the Section Map Key but doesn't conflict with it; left as-is intentionally. Revisit only if it causes a numbering question later.
5. **Deferred conceptual diagrams** (FIG-2.1/2.3/2.4/2.5, DIA-6.3 / UML): not experiment-gated. Prose for Ch 2/Ch 6 is writable now; these figures are queued as asset tasks and inserted as `TO BE CREATED` placeholders. Don't let a missing *conceptual* diagram block prose.
6. **Uncommitted work.** Earlier prompt-pipeline edits were left in the working tree on a branch named `feat/render-norm-polar-validation-fixes` (unrelated name). Suggest the candidate have the executor commit infra changes under clear messages so they don't get lost.

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
