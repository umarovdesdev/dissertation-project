# TRANSLATION DIRECTIVE

**Version:** 1.0 | **Date:** 2026-03-14
**Usage:** Use this prompt when translating an approved English section into academic Kazakh. Attach the English section text and the full GLOSSARY_KZ.md.

---

You are translating a doctoral dissertation section from English to academic Kazakh for defense at IITU (International Information Technology University).

## BINDING REFERENCE

GLOSSARY_KZ.md (attached) is the authoritative translation control document. All terminology decisions are governed by it.

## TRANSLATION POLICY

1. **Technical terms REMAIN IN ENGLISH** — do not translate: CNN, CLAHE, ResNet-50, EfficientNet-B3, EfficientNet-B4, ROC-AUC, F1-Score, Grad-CAM, IoU, ALO, Transfer Learning, Fine-Tuning, Dropout, Batch Normalization, Data Augmentation, Loss Function, Adam Optimizer, Early Stopping, Softmax, ReLU, and all other terms listed in GLOSSARY_KZ Section A.
2. **Conceptual terms are translated** to academic Kazakh per GLOSSARY_KZ Part B translation table.
3. **First use of a translated term** must be bilingual: қазақша (English). Subsequent uses may be Kazakh only.
4. **Globally standardized AI terminology** is not over-translated.
5. **Terminology must be consistent** across all chapters and defense materials.

## STRUCTURAL PRESERVATION RULES

1. Preserve all section headings — translate the text but keep numbering identical (§X.Y.Z).
2. Preserve all table structures — translate headers and text content; keep data values, metrics, and numbers unchanged.
3. Preserve all equation numbering and mathematical notation unchanged.
4. Preserve all citation references ([Author, Year] or Literature Card IDs) unchanged.
5. Preserve all governance reference codes (PC-1, SIR-4, H-1, CFC-2.2, etc.) unchanged — these are internal codes and must not be translated.

## REGISTER

Academic Kazakh appropriate for a doctoral dissertation defense. Formal register throughout. No colloquialisms, no Russian loan words where a Kazakh academic equivalent exists per GLOSSARY_KZ.

## OUTPUT

Produce exactly two parts:

### PART 1: TRANSLATED SECTION TEXT
The complete Kazakh translation of the section.

### PART 2: TERM USAGE REPORT
A table listing every term from GLOSSARY_KZ used in this section:

| English Term | Kazakh Form Used | GLOSSARY_KZ Reference | First Use Location |
|-------------|-----------------|----------------------|-------------------|
| ... | ... | ... | §X.Y.Z, paragraph N |
