# Prompts Directory

## Active Pipeline Templates (governance v6.0.0)

| Template | Purpose | Used In |
|----------|---------|---------|
| `section-brief-template.md` | Template for Section Briefs — the primary planning artifact | Stage A (Planning) |
| `writing-session-system-prompt.md` | Fixed system prompt for all writing sessions | Stage D (Generation) |
| `revision-session-template.md` | Template for revision sessions | Stage C (Revision) |
| `translation-directive.md` | Instructions for EN→KZ translation | Stage E (Translation) |
| `translation-review.md` | Back-check of Kazakh translation against GLOSSARY_KZ + governance codes | Stage F (Translation Review) |
| `verification-protocol.md` | Post-generation compliance checklist | Stage B (Review) |
| `continuity-note-template.md` | Structure for inter-section continuity | Stage D output |

## Pipeline Architecture
A. Section Planning (Claude Opus) → Section Brief
B. Quality Review (Claude Opus)   → Approved draft or revision notes
C. Revision Control (if needed)   → Revised draft
D. Text Generation (fresh session) → Section draft + Continuity Note
E. Translation (separate session)  → Kazakh draft
F. Translation Review (Claude Opus) → Verified Kazakh text

## Utility Prompts

| Template | Purpose |
|----------|---------|
| `glossary-update.md` | Controlled glossary expansion protocol |
| `literature-card-review.md` | Direct literature card creation from articles |
| `literature-index-update.md` | Literature index regeneration protocol |
| `article-evaluation.md` | Structured article evaluation protocol |
| `citation-assembly.md` | Stage G — convert draft author-year citations to GOST `[N]` + build "List of references used" (run once on the assembled manuscript) |
