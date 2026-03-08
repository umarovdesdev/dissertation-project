You are a doctoral-level research indexer working on a PhD dissertation about automated diabetic retinopathy diagnosis via fundus image enhancement and CNN classification.

Your task is to read ALL Literature Cards provided below and produce a single `LITERATURE_INDEX.md` file — a compact navigation table covering the entire external source corpus.

---

## STRICT RULES

1. Extract information ONLY from the provided Literature Cards. Do NOT invent, infer, or assume.
2. Each Literature Card maps to exactly ONE row in the index table.
3. Row numbering (`#`) must follow the Literature Card file numbering (01, 02, 03, ...).
4. Every field must be filled. If a field cannot be determined from the card, write `[TBD]`.
5. Keep entries maximally compressed — no full sentences, only key phrases.
6. Do NOT rewrite or reinterpret authors' findings — use the card's own terminology.

---

## OUTPUT FORMAT

Produce a single Markdown file with the following structure:

```markdown
# LITERATURE INDEX
## External Source Corpus — Navigation Table

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Generated from:** Literature Cards in /LITERATURE/
**Total sources indexed:** [N]

---

### Section Map Key

| Code | Dissertation Section |
|------|---------------------|
| §1.1.1 | Pathophysiology and Clinical Grading Systems |
| §1.1.2 | Screening Requirements in Resource-Limited Healthcare Settings |
| §1.2.1 | Sources of Image Degradation in Clinical Practice |
| §1.2.2 | Impact of Image Quality on Diagnostic Model Performance |
| §1.3.1 | CNN Architectures for Medical Imaging |
| §1.3.2 | Transfer Learning Strategies in Ophthalmic Diagnostics |
| §1.4   | Critical Analysis of Existing Automated DR Screening Systems |
| §1.5   | Formulation of Research Problem |
| §2.1.1 | Histogram Equalization and Adaptive Contrast Enhancement |
| §2.1.2 | Formalization of CLAHE with Controllable Threshold Parameters |
| §2.1.3 | Spatial Filtering and Noise Reduction Methods |
| §2.2.1 | Convolution, Pooling, and Feature Extraction Operations |
| §2.2.2 | Loss Functions and Optimization for Imbalanced Medical Datasets |
| §2.2.3 | Regularization Techniques: Dropout, Batch Normalization, Data Augmentation |
| §2.3.1 | Feature Transferability Across Visual Domains |
| §2.3.2 | Frozen-Layer versus Progressive Fine-Tuning Strategies |
| §2.4.1 | Coupled Thermal-Optical Model of Fundus Tissue Response |
| §3.1   | Formalization of the Unified Preprocessing Pipeline |
| §3.2   | Design of Baseline and Enhanced CNN Architectures |
| §3.3   | Transfer Learning Methodology Using EfficientNetB0 and ResNet50 |
| §3.4   | Evaluation Framework and Performance Metrics |
| §4.1   | Datasets and Experimental Configuration |
| §4.2   | Experiment 1: Baseline vs Enhanced CNN |
| §4.3   | Experiment 2: CLAHE Threshold Optimization |
| §4.4   | Experiment 3: Transfer Learning Strategy Comparison |
| §5.1   | Cross-Database Generalization Testing |
| §5.2   | Statistical Validation of Preprocessing Dominance |
| §5.3   | Comparative Analysis with Existing DR Systems |
| §6.1   | System Requirements and Design Principles |
| §6.3   | Clinical Workflow Integration |
| INTRO  | Introduction (contextual framing) |

---

### Source Index

| # | Source | Type | Key Result | Dataset | Maps to |
|---|--------|------|------------|---------|---------|
| 01 | Pratt et al. (2016) | CNN classification | 75% acc, 5-class, Kaggle DR | EyePACS/Kaggle | §1.3.1 |
| 02 | Saxena et al. (2020) | Cross-dataset validation | Binary DR, InceptionResNetV2, AUC 0.97 | EyePACS, Messidor-1/2 | §1.3.2, §1.4 |
| ... | ... | ... | ... | ... | ... |

---

### Coverage Matrix

| Dissertation Section | Sources Covering It |
|---------------------|---------------------|
| §1.1.1 | #XX, #XX |
| §1.1.2 | #XX, #XX |
| §1.2.1 | #XX |
| ... | ... |

**Gaps identified:** [List any dissertation sections with 0 or 1 source]
```

---

## FIELD EXTRACTION RULES

For each Literature Card, extract the following fields:

### `#` (Index Number)
- Use the Literature Card file number: 01.md → 01, 02.md → 02, etc.

### `Source`
- Format: `Last_name et al. (Year)` or `Last_name & Last_name (Year)` for two authors.
- Extract from **Section 1: Bibliographic Metadata**.

### `Type`
- Compress the study type into a short label (2–4 words max).
- Extract from **Section 2: Study Type Classification**.
- Use standardized labels from this list when applicable:
  - `CNN classification` — trains/evaluates CNN for DR grading
  - `Transfer learning` — primary focus on pretrained model adaptation
  - `Preprocessing study` — primary focus on image enhancement methods
  - `Cross-dataset validation` — tests generalization across datasets
  - `System architecture` — proposes screening/deployment system design
  - `Clinical validation` — prospective or retrospective clinical trial
  - `Review / Survey` — literature review or systematic survey
  - `Segmentation` — lesion or vessel segmentation focus
  - `Ensemble / Hybrid` — combines multiple models or approaches
  - `CLAHE / Enhancement` — specific focus on contrast enhancement
  - `Mathematical modeling` — theoretical/computational modeling
  - If none fit, create a concise custom label.

### `Key Result`
- The single most important quantitative finding OR qualitative conclusion.
- Max 15 words. Include metric values where available.
- Extract from **Section 8: Performance Metrics** or **Section 9: Authors' Claims**.
- Format: `[metric] [value], [context]` — e.g., `AUC 0.97, binary DR, EyePACS`

### `Dataset`
- Primary dataset(s) used. Short names only.
- Extract from **Section 4: Datasets Used**.
- Use standardized names: `APTOS 2019`, `EyePACS/Kaggle`, `Messidor-1`, `Messidor-2`, `STARE`, `DRIVE`, `IDRiD`, `Messidor-2`, etc.

### `Maps to`
- Which dissertation section(s) this source is most relevant to.
- Use section codes from the Section Map Key above.
- Extract from **Section 15: Relevance to My Dissertation**.
- If Section 15 does not exist or is unclear, infer from the source's topic:
  - Pathophysiology/grading → §1.1.1
  - Epidemiology/screening burden → §1.1.2
  - Image quality/degradation → §1.2.1, §1.2.2
  - CNN architectures for DR → §1.3.1
  - Transfer learning for DR → §1.3.2
  - Existing systems (IDx-DR, EyeNuk, etc.) → §1.4
  - CLAHE/histogram equalization → §2.1.1, §2.1.2
  - Preprocessing pipelines → §3.1
  - Class imbalance handling → §2.2.2, §2.2.3
  - Cross-dataset generalization → §5.1
  - System design/deployment → §6.1, §6.3
- A source may map to multiple sections (comma-separated).

---

## COVERAGE MATRIX RULES

After completing the Source Index table:
1. For each dissertation section in the Section Map Key, list which source numbers (`#XX`) cover it.
2. If a section has 0 sources, mark it as **⚠️ GAP**.
3. If a section has only 1 source, mark it as **⚡ THIN**.
4. Sections with 3+ sources need no marker.
5. Add a `Gaps identified` summary listing all ⚠️ GAP and ⚡ THIN sections.

---

## INPUT

Below are all Literature Cards to index. Process each one and produce the complete LITERATURE_INDEX.md.

[PASTE ALL LITERATURE CARDS HERE]
