# REVIEW-MODE WRITING PROMPT
## Chapter 1: PROBLEM DOMAIN ANALYSIS AND CURRENT STATE OF AUTOMATED DIABETIC RETINOPATHY DIAGNOSIS

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification
**Candidate:** Yesmukhamedov N.S.
**Prompt Type:** Structured Literature Review Writing Prompt (Review Mode)
**Binding References:** DISSERTATION_INVARIANTS.md v.1.0 | ARGUMENT_MAP.md | GLOSSARY_v1_0.md | LITERATURE_INDEX.md | MASTER_OUTLINE.md

---

# A. REVIEW OBJECTIVE BLOCK

## A.1 Analytical Purpose

The analytical purpose of Chapter 1 is fourfold:

1. **Landscape mapping:** Establish the clinical, epidemiological, and technical research landscape surrounding automated diabetic retinopathy diagnosis, covering medical context, image acquisition challenges, deep learning architectures, and existing screening systems.
2. **Conceptual framing:** Position the dissertation's integrated preprocessing-CNN approach within the broader spectrum of DR classification methodologies — from pure architecture-scaling to pure preprocessing to hybrid pipelines.
3. **Gap identification:** Through critical analysis of existing approaches, identify the specific methodological gaps that the dissertation addresses: the underrepresentation of preprocessing as a primary performance driver, confounded ablation designs, and the absence of unified preprocessing-classification frameworks optimized for resource-limited environments.
4. **Methodological comparison:** Compare evaluation practices, dataset usage, and validation protocols across the reviewed literature to expose inconsistencies and justify the dissertation's own multi-metric evaluation framework.

## A.2 Relationship to Central Thesis

The review must prepare the evidential and contextual ground for the Central Thesis (INVARIANTS IT-1):

> An integrated preprocessing-CNN pipeline [...] produces statistically measurable improvement in five-class diabetic retinopathy classification performance relative to a baseline CNN trained without preprocessing, under constrained computational conditions.

The review achieves this by:
- Demonstrating that existing literature predominantly focuses on architectural innovations while underrepresenting preprocessing contributions.
- Showing that evaluation inconsistencies across the field (metric variation, dataset heterogeneity, binary vs. multi-class tasks) make direct performance comparisons unreliable.
- Establishing that resource-limited deployment contexts impose constraints not adequately addressed by existing approaches.

**The review must NOT assert the Central Thesis as established.** It must only demonstrate that the research question is well-motivated by the current state of the field.

## A.3 Prohibitions

The review must NOT:
- Present experimental results from Chapters 4–5 of this dissertation.
- Claim that the preprocessing dominance hypothesis (H-1) has been confirmed.
- Assert superiority of the dissertation's pipeline over named commercial systems (CFC-2.2; NC-2).
- Reproduce projected deployment outcomes (20–30% DR complication reduction; 15–20% cost reduction) as dissertation findings (SIR-8; NC-3).
- Claim that the proposed system achieves clinical-grade diagnostic accuracy (CFC-2.4; NC-4).
- Aggregate performance metrics across incompatible datasets without explicit contextual separation.
- Introduce self-publication results (Sources #19–#24) as independent confirmatory evidence where they share identical experimental data (SIR-5).

---

# B. FIELD STRUCTURE ARCHITECTURE

Organize the reviewed literature under the following taxonomy. Each category must contain only cited sources; no unreferenced generalizations are permitted.

## B.1 Conceptual Paradigms

Structure the field into the following paradigms, identifying which sources belong to each and highlighting differences in their foundational assumptions:

| Paradigm | Description | Key Sources |
|----------|-------------|-------------|
| **Architecture-scaling paradigm** | Performance gains primarily through deeper/wider networks or novel architectures | #01 (Pratt 2016), #04 (Arrieta 2022), #09 (Xu 2024), #12 (Gulshan 2016), #16 (Goh 2024), #18 (González-Díaz 2024), #37 (Geetha & Hema 2026), #41 (Sharma 2025) |
| **Preprocessing-as-driver paradigm** | Preprocessing quality is primary determinant of downstream performance | #26 (Shaout & Han 2025), #27 (Hayati 2023), #23/24 🔹SELF (Sapakova et al. 2025a/b) |
| **Hybrid pipeline paradigm** | Integrated preprocessing + architecture co-optimization | #02 (Saxena 2020), #09 (Xu 2024), #15 (Liu 2022) |
| **Clinical deployment paradigm** | Focus on screening system validation and real-world performance | #03 (Sánchez-Gutiérrez 2022), #07 (Baget-Bernaldiz 2021), #11/#13 (Ting 2017), #44 (Zhang 2022), #45 (Ruamviboonsuk 2022) |
| **External validation paradigm** | Emphasis on cross-dataset generalization and reproducibility | #05 (Rakhlin 2017), #17 (Voets 2019), #38 (Khosravi 2025), #44 (Zhang 2022) |

**Critical instruction:** For each paradigm, identify its foundational assumption about what drives performance, and note where assumptions conflict across paradigms (e.g., architecture-scaling assumes model capacity is the bottleneck; preprocessing-as-driver assumes input quality is the bottleneck).

## B.2 Methodological Families

| Family | Core Method | Key Sources |
|--------|-------------|-------------|
| **Supervised CNN classification** | End-to-end supervised training on labeled fundus images | #01, #05, #12, #42 |
| **Transfer learning (frozen/fine-tuned)** | Pre-trained ImageNet weights adapted to fundus domain | #02, #04, #09, #12, #19 🔹SELF, #21 🔹SELF, #42 |
| **Transformer / hybrid architectures** | Vision Transformers, ViT-CNN hybrids | #09, #16, #18, #37, #38, #41 |
| **Semi-supervised / label-efficient** | Training with limited labels | #04 |
| **Segmentation-based** | Lesion segmentation as intermediate step | #08 |
| **Ensemble methods** | Multi-model combination | #09, #12, #44 |
| **Meta-analysis / systematic review** | Evidence synthesis across studies | #14, #39, #40 |

## B.3 Model Architectures

Map architectures referenced across the corpus:

| Architecture | Sources Using It | Dataset Context | Key Performance |
|-------------|-----------------|-----------------|-----------------|
| Custom CNN (baseline/enhanced) | #01, #24 🔹SELF | EyePACS/Kaggle, APTOS 2019 | 75% acc (#01); 71%→86% val acc (#24) |
| EfficientNet family | #09, #15, #19 🔹SELF, #21 🔹SELF, #27, #42 | APTOS 2019, DeepDRiD, Kaggle | F1 0.74 fine-tuned (#19); 97.83% acc EfficientNetB4 (#27); 0.8653 avg acc (#42) |
| ResNet family | #23 🔹SELF, #38, #43 | STARE, multi-country, OCTA | 100% acc (#23 — **flag metric anomaly SIR-3**); AUC 0.9626 (#38) |
| Inception family | #02, #12, #44 | EyePACS, Messidor, multicentre | AUC 0.991 (#12); AUROC 0.9931 (#44) |
| VGG family | #05 | EyePACS/Kaggle, Messidor-2 | AUC 0.967 Messidor-2 (#05) |
| Vision Transformers (ViT/Swin) | #09, #16, #18, #37, #38, #41 | Various | SWIN AUC 95.7% (#16); Acc 0.97 hybrid (#09) |
| ViT-CapsNet | #41 | EyePACS | 94% acc, **AUC 0.44–0.56 per class — CRITICAL INCONSISTENCY** |

**Instruction:** When tabulating architectures, always note the dataset, task (binary vs. multi-class), and any metric formula deviations. Flag Source #41 (Sharma et al., 2025) for internal metric inconsistency (AUC values fundamentally incompatible with claimed accuracy). Flag Source #23 🔹SELF for sensitivity formula anomaly (SIR-3).

## B.4 Preprocessing Strategies

| Strategy | Sources | Implementation Details | Impact |
|----------|---------|----------------------|--------|
| CLAHE (standard) | #24 🔹SELF, #27 | clip limit 2.0, grid 8×8 | Improved 3/4 CNNs (#27); val acc 71%→86% (#24) |
| CLAHE (upgraded, T/80) | #23 🔹SELF | T/80 threshold formulation | 100% acc on STARE (**flag SIR-3**) |
| Fuzzy + CLAHE | #26 | FCE+CLAHE blending | 59% preference, 88% combined |
| Rescaling only | #30 | Best of 4 techniques for OCT | No numerical metrics (**low epistemic weight**) |
| Not reported / minimal | #01, #04, #12, #16, #44, #45 | Preprocessing details absent or minimal | N/A |

**Critical instruction:** Explicitly note that many high-performing studies (#12 Gulshan, #44 Zhang, #45 Ruamviboonsuk) do not report preprocessing details — this is the core of the "preprocessing underrepresentation" gap that motivates the dissertation.

## B.5 Evaluation Protocols

| Protocol Element | Variation Observed | Sources Exemplifying |
|-----------------|-------------------|---------------------|
| **Metric selection** | Accuracy only vs. multi-metric (AUC, F1, κ) | #01 (acc only), #27 (acc only), #12 (AUC), #15 (κ + acc), #44 (AUROC + κ) |
| **Task definition** | Binary (referable/non-referable) vs. 5-class grading | #02, #03, #07, #12 (binary); #01, #09, #15, #16, #19 🔹SELF (multi-class) |
| **Validation strategy** | Internal hold-out vs. external dataset vs. prospective clinical | #01 (internal), #17 (external reproduction), #44 (multicentre external), #45 (prospective clinical) |
| **Statistical testing** | Presence/absence of CI, p-values, statistical significance | #45 (p=0.024), #14 (pooled SROC); most sources lack formal testing |
| **Class imbalance handling** | Addressed vs. ignored | #19 🔹SELF (weighted loss), #40 (systematic review of CSL); #01, #42 (limited handling) |

**Instruction:** Synthesize across sources to demonstrate that evaluation protocol heterogeneity is a systemic problem in the field, not merely an observation about individual studies.

## B.6 Clinical Deployment Contexts

| Context | Sources | Validation Level | Key Limitations |
|---------|---------|-----------------|-----------------|
| **Commercial systems (FDA-approved)** | #03 (RetCAD), #11/#13 (DLS Singapore) | Clinical validation, external datasets | Proprietary; limited architecture transparency |
| **Research prototypes** | #01, #04, #09, #12, #16 | Internal validation only | No clinical deployment |
| **National screening programs** | #45 (Thailand), #11/#13 (Singapore), #22 🔹SELF (Kazakhstan design) | Prospective (#45), multiethnic external (#11), design only (#22) | Country-specific; limited portability |
| **Resource-limited environments** | #22 🔹SELF | Design specification only | No prototype or field testing (SB-4.1) |

---

# C. SYNTHESIS RULES

The following synthesis rules are **mandatory** for every subsection of Chapter 1.

## C.1 Comparative Analysis Requirement

Every subsection must contain cross-source synthesis. **No single-source summarization blocks are permitted.** Each paragraph must reference at least two sources, comparing, contrasting, or synthesizing their findings.

**Acceptable pattern:**
> While Gulshan et al. (2016) achieved AUC 0.991 using an Inception-v3 ensemble on EyePACS, Voets et al. (2019) attempted to reproduce these results and obtained AUC 0.951 on the same dataset, suggesting that reported performance may be sensitive to implementation specifics not captured in published methodology.

**Forbidden pattern:**
> Gulshan et al. (2016) achieved AUC 0.991 using an Inception-v3 ensemble. The study used EyePACS data and binary classification. [single-source block]

## C.2 Explicit Identification Requirements

For every thematic cluster, the writer must explicitly identify:

1. **Agreements:** Where do multiple sources converge on the same finding? (e.g., transfer learning improves DR classification: #02, #04, #12, #19 🔹SELF)
2. **Disagreements:** Where do sources produce contradictory findings? (e.g., CLAHE improves most CNNs (#27 Hayati: 3/4 architectures) but degrades ResNet34 by −12.02% (#27 Hayati) — complicating universal preprocessing dominance claims)
3. **Methodological trade-offs:** What design choices produce different strengths/weaknesses? (e.g., binary classification achieves higher AUC but obscures clinically important inter-grade distinctions)
4. **Dataset differences:** When comparing performance figures, always note: dataset name, size, class taxonomy, public vs. private (e.g., #12 Gulshan's EyePACS is private; #01 Pratt's Kaggle EyePACS is public — these are not identical)
5. **Metric inconsistencies:** Flag any differences in metric definitions (e.g., Source #23 🔹SELF sensitivity formula anomaly per SIR-3; Source #41 internal AUC-accuracy incompatibility)

## C.3 Separation Between Evidence Types

Maintain strict separation between:

| Type | Definition | Example |
|------|-----------|---------|
| **Empirical finding** | A reported experimental result with dataset, metric, and value | "AUC 0.991 on EyePACS-1" (#12) |
| **Theoretical argument** | A conceptual claim about why something should work | "Features learned on ImageNet retain utility for fundus classification" (INVARIANTS DGL-6) |
| **Implementation-specific claim** | A finding that depends on specific technical choices | "EfficientNetB4 achieved 97.83% accuracy with CLAHE on APTOS 2019" (#27) |

Never conflate a theoretical argument with an empirical finding. Never present an implementation-specific result as a general conclusion.

---

# D. GAP IDENTIFICATION FRAMEWORK

## D.1 Required Gap Identifications

The review must identify and document the following gaps. Each gap must be derived from cited sources, not asserted a priori.

### Gap 1: Preprocessing Underrepresentation

**Nature:** Genuine research gap.
**Evidence:**
- Many high-performing DR classification studies do not report preprocessing details (#12 Gulshan 2016, #44 Zhang 2022, #45 Ruamviboonsuk 2022).
- Systematic reviews (#14 Wewetzer 2021, #39 Senapati 2024) identify class imbalance and overfitting as key challenges but do not systematically address preprocessing as a performance variable.
- Hayati et al. (#27) is among the few studies that explicitly evaluates CLAHE impact across architectures — and finds it is not universally beneficial (ResNet34 degradation).
- The field-mapping survey by Senapati et al. (#39) identifies overfitting and class imbalance as key gaps but does not identify preprocessing underrepresentation as a systematic issue.

**Instruction:** Derive this gap by synthesizing the absence of preprocessing analysis across multiple sources, not by asserting it as self-evident.

### Gap 2: Confounded Ablation Designs

**Nature:** Unresolved methodological issue.
**Evidence:**
- In Source #24 🔹SELF, preprocessing and architectural complexity changes are applied simultaneously — the isolated effect of preprocessing is not independently measured (ARGUMENT_MAP CA-1.1).
- Most architecture-focused studies (#01, #04, #09, #12) do not include ablation of preprocessing components.
- The cost-sensitive learning review (#40 Araf 2024) reveals that only 2 of 173 studies were validation research — suggesting systematic underinvestment in rigorous experimental design.

### Gap 3: Evaluation Protocol Heterogeneity

**Nature:** Inconsistent evaluation practices.
**Evidence:**
- Binary vs. multi-class task definitions vary across studies (#02, #07 use binary; #01, #09, #15, #16 use multi-class).
- Metric selection is inconsistent: some report accuracy only (#01, #27), others report AUC (#12), others use comprehensive multi-metric profiles (#15, #44).
- Statistical testing is absent from most studies; only #45 (Ruamviboonsuk) reports p-values for comparison with specialists.
- Cross-dataset validation is rare; #17 (Voets 2019) demonstrates reproducibility challenges.

### Gap 4: Resource-Limited Deployment Context

**Nature:** Underexplored optimization area.
**Evidence:**
- Most high-performing systems (#03, #11, #12, #44, #45) are validated in well-resourced clinical or research settings.
- Resource-limited deployment as defined in INVARIANTS OD-6 (no GPU, <16 GB RAM, connectivity limitations) is not systematically addressed in the reviewed literature.
- Kazakhstan-specific context (~1,200 ophthalmologists, >40% rural population) provides clinical framing but does not constitute experimental evidence (MASTER_OUTLINE, §1.1.2).

### Gap 5: Image Quality Variability

**Nature:** Dataset-specific limitation with cross-study implications.
**Evidence:**
- Liu et al. (#15) reports only 0.70 image quality accuracy on DeepDRiD, demonstrating that quality assessment itself is a challenging task.
- Rakhlin (#05) and Voets (#17) both document performance degradation under cross-dataset conditions, partially attributable to image quality differences.
- Section §1.2.1 currently has **ZERO sources** (LITERATURE_INDEX Coverage Matrix: ⚠️ GAP). The writer must **explicitly flag** that sources specifically addressing image degradation mechanisms in clinical fundus photography are absent from the current corpus and must be acquired.

## D.2 Distinction Requirements

For each gap, explicitly classify it as:

| Classification | Meaning | Gap Examples |
|---------------|---------|--------------|
| **Genuine research gap** | No adequate investigation exists in the literature | Gap 1 (preprocessing underrepresentation) |
| **Underexplored optimization area** | Investigations exist but are insufficient or non-systematic | Gap 4 (resource-limited deployment) |
| **Dataset-specific limitation** | The problem exists due to characteristics of available data | Gap 5 (image quality variability) |
| **Unresolved methodological issue** | The field lacks consensus on proper methodology | Gap 2 (confounded ablation), Gap 3 (evaluation heterogeneity) |

## D.3 Dissertation Response Statement

For each identified gap, state how the dissertation addresses it — without restating experimental results:

- **Gap 1** → The dissertation proposes an integrated preprocessing-CNN framework that makes preprocessing an explicit, controllable experimental variable (§3.1).
- **Gap 2** → The dissertation includes an ablation study design (§5.2) to isolate preprocessing effects from architectural complexity changes.
- **Gap 3** → The dissertation adopts a multi-metric evaluation framework (EH-1: weighted F1, ROC-AUC, Cohen's Kappa, Accuracy) with explicit empirical dominance criteria (EH-3).
- **Gap 4** → The dissertation frames its experimental conditions within resource-limited constraints (OD-6) and proposes a system architecture (Chapter 6) targeting such environments.
- **Gap 5** → The dissertation uses CLAHE-based preprocessing specifically to address contrast and visibility of microvascular features under variable image quality conditions.

---

# E. TERMINOLOGICAL DISCIPLINE

## E.1 Mandatory Glossary Compliance

All terms must conform to GLOSSARY_v1_0.md definitions. The following terms carry specific operational definitions that must not be diluted:

| Term | Canonical Definition | Chapter 1 Usage Rule |
|------|---------------------|---------------------|
| **Image quality** | OD-1: assessed through downstream classification metrics, not subjective scores | In §1.2, introduce the physical/visual characterization of image degradation (acceptable in introductory context per GLOSSARY §5, Invariants Deviation Report), but explicitly transition to the operational definition (OD-1) by §1.2.2 |
| **Preprocessing pipeline** | OD-3: four-stage ordered sequence (resizing → normalization → CLAHE → augmentation) | In §1.3–1.4, when comparing with other approaches, note that most studies do not implement the full four-stage pipeline as defined in OD-3 |
| **Generalization** | OD-4: two distinct definitions (training-test gap; cross-database ratio) | Always qualify: "training generalization" or "cross-database generalization." Never use unqualified |
| **Resource-limited environment** | OD-6: computational definition (no GPU, <16 GB RAM, connectivity constraints) | In §1.1.2, provide clinical framing (Kazakhstan context) but clarify that the operational definition is computational |
| **Diagnostic effectiveness** | OD-5: joint profile on four metrics with specific thresholds | Do not use informally; reserve for explicit metric-based assessment in experimental chapters |

## E.2 Disambiguation Requirements

| Overloaded Term | Meaning A | Meaning B | Sources Using Each | Resolution |
|----------------|-----------|-----------|-------------------|------------|
| **Feature extraction** | CNN operation (hierarchical spatial representation learning) | Transfer learning strategy (frozen base, no adaptation) | #12, #19 🔹SELF, #21 🔹SELF | Use "feature extraction layers" for (A) and "frozen-base strategy" for (B) per GLOSSARY §6 Priority 1 Item 2 |
| **Robustness** | Training stability | Cross-database consistency | #02, #19 🔹SELF | Define explicitly at each point of use per GLOSSARY §6 Priority 3 Item 11 |
| **Fine-tuning** | General: any weight update from pre-trained state | Specific: Stage 2 of two-stage protocol | #02, #04, #12, #19 🔹SELF | Standardize: "progressive fine-tuning" for the specific protocol per GLOSSARY §6 Priority 1 Item 1 |
| **Accuracy** | Overall accuracy | Per-class accuracy | #01, #12, #27, #42 | Always specify "overall accuracy" or "per-class accuracy." Note EH-1 position: accuracy is reported but not sufficient alone under class imbalance |

## E.3 Metric Definition Consistency

When citing performance metrics from different sources, explicitly note if:
- The metric formula differs (e.g., Source #23 🔹SELF sensitivity anomaly: Sen = TP/(TP+TN) vs. standard Sen = TP/(TP+FN) — SIR-3)
- The task differs (binary vs. 5-class; different class taxonomies — e.g., STARE uses BDR/CRVO/CNV/PDR/Normal ≠ DR 0–4)
- The evaluation partition differs (internal validation vs. external hold-out vs. prospective clinical)
- Class imbalance is present but unaccounted for (making accuracy a potentially misleading metric — EH-1)

---

# F. POSITIONING PROTOCOL

## F.1 Dissertation Positioning

Position the dissertation relative to the three major paradigms identified in B.1:

| Paradigm | Dissertation Relationship | Language |
|----------|--------------------------|----------|
| **Architecture-scaling** | The dissertation does not compete on architectural novelty; it uses established architectures (EfficientNetB0, ResNet50, custom CNN) as fixed classifiers | "employs established architectures as classification backbones" |
| **Preprocessing-as-driver** | The dissertation extends this paradigm by formalizing preprocessing as a controllable experimental variable with explicit parameter sensitivity analysis | "extends prior preprocessing investigations by formalizing..." |
| **Hybrid pipeline** | The dissertation proposes an integrated preprocessing-CNN framework — neither pure preprocessing nor pure architecture scaling | "systematically integrates preprocessing and classification within a unified pipeline" |

## F.2 Language Requirements

**Required neutral positioning language:**
- "extends"
- "systematically integrates"
- "addresses variability in"
- "formalizes"
- "proposes to evaluate"
- "complements existing approaches by"

**Forbidden positioning language:**
- "outperforms" (CFC-2.2 — no controlled comparison against named systems)
- "superior to"
- "dominates" (when used informally — the term "preprocessing dominance" has a precise operational definition in EH-3)
- "state-of-the-art" (unless citing a specific benchmark with specific metric)
- "best" / "optimal" (INVARIANTS SB-3.1 — no claim of architectural optimality)
- "revolutionary" / "breakthrough" / "novel solution" (inflated language)

## F.3 Self-Publication Positioning

When referencing self-publications (#19–#24 🔹SELF):
- Explicitly identify as prior own work at point of citation (SIR-4).
- Frame as "previously published results" that the dissertation extends.
- Sources #19 and #21 share identical experimental data and must not be cited as independent evidence (SIR-5).
- Sources #23 and #24 are duplicate entries for the same article; cite as a single source.
- State what the dissertation adds beyond these publications.

---

# G. SOURCE HANDLING RULES

## G.1 Non-Amplification

Do not attribute to any source conclusions stronger than explicitly stated in that source (SIR-1). Examples:

| Source States | Forbidden Amplification | Correct Attribution |
|--------------|------------------------|---------------------|
| Hayati (#27): "CLAHE improved accuracy for 3 of 4 architectures" | "CLAHE universally improves CNN performance" | "Hayati et al. found CLAHE improved accuracy for three of four tested architectures, while degrading ResNet34 performance by 12 percentage points" |
| Gulshan (#12): AUC 0.991 on EyePACS | "Deep learning has solved DR diagnosis" | "Gulshan et al. reported AUC 0.991 on EyePACS using an Inception-v3 ensemble with binary classification" |
| Senapati (#39): identifies overfitting and class imbalance as gaps | "The field universally acknowledges preprocessing as neglected" | "Senapati et al. identified overfitting and class imbalance as persistent challenges, though preprocessing quality was not explicitly analyzed as a variable" |

## G.2 Dataset Context Separation

Never aggregate metrics across different datasets without explicit contextual separation:

| Forbidden | Correct |
|-----------|---------|
| "DR classification systems achieve AUC of 0.85–0.99" | "Reported AUC values range from 0.853 (Voets 2019, Messidor-2 reproduction) to 0.991 (Gulshan 2016, private EyePACS), reflecting differences in dataset size, image quality, and evaluation protocol" |

## G.3 Mandatory Contextual Notations

For each source cited, note at first citation:
- Dataset name and size
- Task type (binary / multi-class; specific class taxonomy)
- Public vs. private dataset status
- Any metric formula deviations

## G.4 Source Quality Flags

The following sources carry explicit quality concerns that must be noted when cited:

| Source | Flag | Implication |
|--------|------|-------------|
| #23 🔹SELF | Sensitivity formula anomaly (SIR-3): Sen = TP/(TP+TN) | Do not cite 100% sensitivity at face value |
| #26 (Shaout & Han) | arXiv preprint; 10-person subjective survey | Low epistemic weight |
| #30 (Chakka) | High school journal; no numerical metrics | Do not cite as evidence; contextual reference only |
| #31 (Kesharwani) | Citation errors; questionable journal practices | Use #32 (Kusuhara) instead for pathophysiology |
| #37 (Geetha & Hema) | No dataset names; no external validation; no AUC/CI | Architectural reference only |
| #41 (Sharma) | AUC 0.44–0.56 incompatible with 94% accuracy | Do not cite AUC values without explicit disclaimer |
| #42 (Arora) | CI bounds identical (likely artifact); 11-point training-test gap | Note overfitting concern |

## G.5 Self-Publication Handling

| Source | Handling Rule |
|--------|--------------|
| #19 (CONF) and #21 (KBTU) | Treat as single experimental thread; cite both but note overlap (SIR-5) |
| #23 and #24 (SQOPUS) | Duplicate entries for same article; consolidate citation |
| #20 (KazUTB) | Unique contribution (laser modeling); not relevant to Chapter 1 |
| #22 (NAN_RK) | Relevant for §1.1.2 (Kazakhstan screening context) and §1.4 (system architecture comparison) |

---

# H. STRUCTURAL TEMPLATE FOR THE CHAPTER

## H.1 Section-by-Section Breakdown

---

### §1.1 Medical and Epidemiological Context of Diabetic Retinopathy

**Estimated allocation:** 4–5 pages (10–12 paragraphs)

#### §1.1.1 Pathophysiology and Clinical Grading Systems
**Analytical focus:** Establish the five-stage clinical grading system (DR 0–4); describe microvascular pathology (microaneurysms, hemorrhages, exudates, neovascularization); explain why automated detection is clinically motivated.
**Sources:** #31 (Kesharwani — use cautiously, prefer #32), #32 (Kusuhara 2018), #33 (Gettinger 2025), #34 (Morya 2024), #35 (Wang & Lo 2018)
**Synthesis requirement:** Cross-reference at least three sources on the pathophysiological progression; note where #33 (Gettinger) and #35 (Wang & Lo) reinforce the neurodegeneration-preceding-microvasculopathy model.
**Cross-reference to experimental chapters:** §4.1.2 (class distribution mirrors DR severity stages)
**Estimated paragraphs:** 4–5

#### §1.1.2 Screening Requirements in Resource-Limited Healthcare Settings
**Analytical focus:** Global screening burden; WHO recommendations; Kazakhstan-specific context (~1,200 ophthalmologists, >40% rural; INVARIANTS OD-6).
**Sources:** #06/#10 (Porwal — IDRiD; Indian population context), #22 🔹SELF (Kazakhstan framing), #34 (Morya — 35–55% screening compliance data)
**Synthesis requirement:** Compare screening contexts across settings (India #06, Singapore #11, Kazakhstan #22, Thailand #45). Note that #22 is a self-publication providing design specifications, not deployment outcomes (SIR-8; SB-4.1).
**Boundary:** Projected deployment benefits are contextual framing, not dissertation findings (NC-3; SIR-8).
**Cross-reference to experimental chapters:** §6.1 (system requirements for resource-limited settings)
**Estimated paragraphs:** 4–5
**Table placement:** Consider a comparison table of screening contexts (country, ophthalmologist ratio, key challenges, AI screening status).

---

### §1.2 Fundus Image Acquisition and Quality Variability

**Estimated allocation:** 3–4 pages (7–9 paragraphs)

#### §1.2.1 Sources of Image Degradation in Clinical Practice
**Analytical focus:** Illumination inconsistencies, motion artifacts, camera-specific noise, patient-related factors.
**Sources:** **⚠️ COVERAGE GAP — ZERO SOURCES in current corpus.** The writer must:
  1. Flag this gap explicitly in the text.
  2. Derive limited context from related sources (#05 Rakhlin, #15 Liu, #17 Voets) which document performance sensitivity to image quality without explicitly cataloging degradation sources.
  3. Recommend acquisition of additional literature on fundus image quality assessment (e.g., from medical imaging or ophthalmology journals).
**Operational definition:** Transition to OD-1 (image quality as downstream classification performance) by end of this section.
**Estimated paragraphs:** 3–4

#### §1.2.2 Impact of Image Quality on Diagnostic Model Performance
**Analytical focus:** Evidence that image quality variability degrades model performance; motivation for preprocessing.
**Sources:** #05 (Rakhlin — AUC drop cross-dataset), #15 (Liu — 0.70 quality accuracy on DeepDRiD), #17 (Voets — reproduction failure), #24 🔹SELF (val acc 71% without preprocessing)
**Synthesis requirement:** Cross-reference #05, #15, and #17 to demonstrate that performance degradation is a cross-study phenomenon. Use #24 🔹SELF as a data point (identified as self-publication per SIR-4) showing baseline performance without preprocessing.
**Cross-reference to experimental chapters:** §4.2 (Experiment 1), §5.1 (cross-database generalization)
**Estimated paragraphs:** 4–5

---

### §1.3 Deep Learning Approaches to Retinal Image Classification

**Estimated allocation:** 8–10 pages (20–25 paragraphs)

#### §1.3.1 Convolutional Neural Network Architectures for Medical Imaging
**Analytical focus:** Survey of CNN architectures applied to DR classification; performance landscape; evolution from shallow to deep architectures.
**Sources:** #01 (Pratt — custom CNN), #04 (Arrieta — semi-supervised), #05 (Rakhlin — VGG), #08 (Wan — segmentation), #09 (Xu — EfficientNet+Swin), #12 (Gulshan — Inception), #15 (Liu — EfficientNet benchmark), #16 (Goh — ViT vs. CNN), #18 (González-Díaz — ViT for AMD), #37 (Geetha — ViT hybrid), #38 (Khosravi — FastViT vs. ResNet), #41 (Sharma — ViT-CapsNet), #42 (Arora — EfficientNetB0), #43 (Ryu — OCTA ResNet101)
**Synthesis requirement:** This is the most source-rich section. Organize by architectural generation: (1) custom/shallow CNNs → (2) deep pre-trained CNNs → (3) Vision Transformers and hybrids. For each generation, synthesize performance trends across multiple sources. Explicitly compare CNN vs. ViT performance claims (#16 Goh: ViT > CNN; #38 Khosravi: FastViT > ResNet18; but #09 Xu: hybrid achieves highest performance).
**Table placement:** Comparative table of CNN architectures (Architecture | Source | Dataset | Task | Key Metric | Preprocessing Reported?) — see Section I.
**Cross-reference to experimental chapters:** §3.2 (baseline/enhanced CNN design), §3.3 (EfficientNetB0/ResNet50 selection)
**Estimated paragraphs:** 8–10

#### §1.3.2 Transformer and Hybrid Architectures
**Analytical focus:** Emergence of ViT-based approaches; comparison with CNN performance; hybrid architectures.
**Sources:** #09 (Xu — EfficientNet+Swin hybrid, Acc 0.97), #16 (Goh — SWIN AUC 95.7%, ViT > CNN), #18 (González-Díaz — ViT for AMD, limited sample), #37 (Geetha — ViT-BFF-HGS, 98.4% acc but no validation), #38 (Khosravi — FastViT AUC 0.9811), #41 (Sharma — ViT-CapsNet, metric inconsistency)
**Synthesis requirement:** Critically analyze whether ViT superiority claims hold across settings. Note: #16 shows ViT advantage on large datasets; #18 has only 305 images; #37 lacks external validation; #41 has internal metric inconsistency. Conclude that ViT shows promise but evidence is heterogeneous and often methodologically limited.
**Boundary:** Dissertation evaluates EfficientNetB0 and ResNet50 only; no claim of architectural optimality (SB-3.1; NC-6).
**Estimated paragraphs:** 5–6

#### §1.3.3 Transfer Learning Strategies in Ophthalmic Diagnostics
**Analytical focus:** ImageNet pre-training for medical imaging; domain gap; frozen vs. fine-tuned strategies.
**Sources:** #02 (Saxena — InceptionResNetV2 cross-dataset), #09 (Xu — hybrid transfer), #12 (Gulshan — Inception-v3 transfer)
**Synthesis requirement:** Compare transfer learning approaches across sources. Note that #02 achieves AUC 0.958 with cross-dataset validation, while #12 achieves AUC 0.991 but on a private dataset. Discuss domain gap (INVARIANTS DGL-6) as a theoretical concern motivating the fine-tuning protocol.
**Cross-reference to experimental chapters:** §2.3 (theoretical framework), §4.4 (Experiment 3)
**Estimated paragraphs:** 4–5

#### §1.3.4 Global Benchmarking and Clinical-Scale Validation
**Analytical focus:** Large-scale validation studies; clinical-grade performance claims; methodological standards for clinical validation.
**Sources:** #11/#13 (Ting — 10 multiethnic datasets, AUC 0.936), #44 (Zhang — multicentre 83,465 images, AUROC 0.9931), #45 (Ruamviboonsuk — prospective 7,651 patients, outperformed specialists)
**Synthesis requirement:** This subsection establishes the performance ceiling and methodological gold standard. Compare validation scales and protocols across #11, #44, and #45. Note that #44 and #45 represent the strongest external validation evidence but are geographically specific (China, Thailand) and do not report preprocessing details.
**Estimated paragraphs:** 4–5

---

### §1.4 Evidence Synthesis and Critical Analysis of Existing Automated DR Screening Systems

**Estimated allocation:** 6–8 pages (15–20 paragraphs)

#### §1.4.1 Comparative Performance Across Datasets and Model Families
**Analytical focus:** Systematic comparison of reported performance across datasets (APTOS, EyePACS, Messidor, IDRiD, private datasets) and model families (CNN, ViT, hybrid, ensemble).
**Sources:** #02, #03, #05, #07, #09, #12, #15, #16, #22 🔹SELF, #39, #43, #44, #45
**Synthesis requirement:** Do NOT simply list source results. Organize by dataset and show how performance varies across architectures on the same dataset, and how the same architecture performs across datasets. This is the core analytical contribution of Chapter 1.
**Table placement:** Comparative performance table organized by dataset (see Section I).
**Estimated paragraphs:** 6–7

#### §1.4.2 Meta-Analytic Evidence on Diagnostic Accuracy and Generalization
**Analytical focus:** Evidence from systematic reviews and meta-analyses; pooled performance estimates; generalization challenges.
**Sources:** #14 (Wewetzer — pooled sens 87%, spec 90%, SROC AUC 0.9543), #39 (Senapati — PRISMA review, gap identification), #40 (Araf — cost-sensitive learning review, only 2/173 validation studies)
**Synthesis requirement:** Synthesize across the three reviews to show: (1) overall field performance level (#14), (2) persistent methodological gaps (#39), and (3) severe underinvestment in rigorous validation (#40). This triad of evidence motivates the dissertation's emphasis on evaluation rigor.
**Estimated paragraphs:** 4–5

#### §1.4.3 Methodological Gaps: Preprocessing Underrepresentation and Confounded Ablation
**Analytical focus:** This is the critical gap-identification subsection. Derive the following gaps from the reviewed literature:
  1. Preprocessing is not treated as an independent experimental variable in most studies.
  2. Ablation designs that confound preprocessing with architecture changes.
  3. Metric inconsistency across the field.
  4. Limited cross-dataset validation.
**Sources:** #17 (Voets — reproducibility), #27 (Hayati — CLAHE not universally beneficial), #39 (Senapati — gap survey), #40 (Araf — validation gap), plus synthesis across §1.3 and §1.4.1–1.4.2.
**Synthesis requirement:** This subsection must explicitly derive the research gap from evidence, not assert it. The logical chain should be: (1) preprocessing is rarely reported → (2) when it is reported, it shows variable effects → (3) ablation studies isolating preprocessing are absent → (4) therefore, the contribution of preprocessing to classification performance is an open question.
**Estimated paragraphs:** 5–6

---

### §1.5 Formulation of the Research Problem and Justification of Research Direction

**Estimated allocation:** 2–3 pages (5–7 paragraphs)

**Analytical focus:** Synthesize all gaps from §1.1–1.4 into a formal research problem statement. Justify the specific research direction aligned with CORE_OBJECTIVE.md.
**Sources:** #17 (Voets — reproducibility gap), #39 (Senapati — field landscape gaps)
**Synthesis requirement:** The research problem must emerge as a logical consequence of the gaps identified. It must not be asserted independently. Link each element of the Core Objective to a specific gap:
  - "integrated fundus image enhancement and CNN-based classification framework" → Gap 1 (preprocessing underrepresentation) + Gap 2 (confounded ablation)
  - "contrast-adaptive preprocessing" → Gap 5 (image quality variability)
  - "variable image quality and constrained computational conditions" → Gap 4 (resource-limited deployment)
  - "multi-stage diabetic retinopathy diagnosis" → Gap 3 (evaluation heterogeneity — binary vs. multi-class)
**Cross-reference:** Connect to CORE_OBJECTIVE.md (verbatim), HYPOTHESIS.md (H-1, H-2, H-3).
**Estimated paragraphs:** 5–7

---

### Conclusions to Chapter 1

**Estimated allocation:** 1–1.5 pages (3–4 paragraphs)

**Content:** Summarize the state of the art; enumerate the specific gaps identified; state the research problem formally. Do NOT preview experimental results.

---

## H.2 Total Chapter Estimate

| Section | Pages | Paragraphs |
|---------|-------|------------|
| §1.1 | 4–5 | 10–12 |
| §1.2 | 3–4 | 7–9 |
| §1.3 | 8–10 | 20–25 |
| §1.4 | 6–8 | 15–20 |
| §1.5 | 2–3 | 5–7 |
| Conclusions | 1–1.5 | 3–4 |
| **TOTAL** | **24–31** | **60–77** |

---

# I. ANALYTICAL TABLE REQUIREMENT

The following tables are **mandatory** for Chapter 1. Each table must include source reference, dataset, metric definition, and key performance indicator without reinterpretation.

## Table 1.1: Comparative Table of CNN and ViT Architectures for DR Classification

| Architecture | Source | Year | Dataset | Size | Task | Key Metric | Value | Preprocessing Reported? |
|-------------|--------|------|---------|------|------|------------|-------|------------------------|
| Custom CNN | Pratt #01 | 2016 | Kaggle EyePACS | — | 5-class | Accuracy | 75% | Not specified |
| InceptionResNetV2 | Saxena #02 | 2020 | EyePACS → Messidor-1/2 | — | Binary | AUC | 0.958/0.92 | Not specified |
| Inception-v3 ensemble | Gulshan #12 | 2016 | EyePACS (private) | 128,175 | Binary | AUC | 0.991 | Not specified |
| Modified VGGNet | Rakhlin #05 | 2017 | Kaggle → Messidor-2 | — | Binary | AUC | 0.923/0.967 | Not specified |
| EfficientNet+Swin V2 | Xu #09 | 2024 | APTOS 2019 | — | 5-class | Acc/AUC | 0.97/0.97 | Not specified |
| EfficientNetB4 | Hayati #27 | 2023 | APTOS 2019 | 3,662 | Binary | Accuracy | 97.83% | CLAHE (studied) |
| EfficientNetB0 | Arora #42 | 2024 | Kaggle DR (undersampled) | 3,704 | 5-class | Accuracy | 86.53% | Not specified |
| SWIN Transformer | Goh #16 | 2024 | Kaggle/SEED/Messidor-1 | — | Multi-class | AUC | 95.7%/97.3%/96.3% | Not specified |
| FastViT | Khosravi #38 | 2025 | Multi-country | 2,661 ext. | Binary | AUC | 0.9811 | Not specified |
| Ensemble (Inc-V3/Xc/Inc-RN) | Zhang #44 | 2022 | Multicentre (4 centres) | 83,465 | Binary | AUROC | 0.9931 | Not reported |
| DL system | Ruamviboonsuk #45 | 2022 | Thai prospective (9 sites) | 7,651 pts | Binary | Accuracy | 94.7% | Not reported |

**Column "Preprocessing Reported?"** is critical — it visually demonstrates that preprocessing is underreported in the field.

## Table 1.2: Comparative Table of Preprocessing Strategies in DR Classification

| Strategy | Source | Year | Dataset | CNN Used | Impact on Performance | Parameters Specified? |
|----------|--------|------|---------|----------|----------------------|----------------------|
| CLAHE | Sapakova #24 🔹SELF | 2025 | APTOS 2019 + private | Custom 4-block | Val acc 71%→86% | clip=2.0, grid=8×8 |
| Upgraded CLAHE (T/80) | Sapakova #23 🔹SELF | 2025 | STARE | ResNet50 | 100% acc (⚠️ SIR-3) | T/80 formulation |
| CLAHE (multi-arch) | Hayati #27 | 2023 | APTOS 2019 | 4 architectures | +3/4 improved; ResNet34 −12% | Not fully specified |
| FCE+CLAHE | Shaout #26 | 2025 | DRIVE | — | 59%/88% preference | clipLimit=2.0, 8×8 |
| Rescaling | Chakka #30 | 2023 | Kaggle OCT | ResNet50 | "Best of 4" (no metrics) | Not specified |
| Not reported | Gulshan #12 | 2016 | EyePACS | Inception-v3 | AUC 0.991 | N/A |
| Not reported | Zhang #44 | 2022 | Multicentre | Ensemble | AUROC 0.9931 | N/A |

## Table 1.3: Evaluation Metrics and Datasets Across DR Classification Studies

| Source | Dataset | Public? | Size | Task | Metrics Reported | Statistical Testing |
|--------|---------|---------|------|------|-----------------|-------------------|
| Pratt #01 | EyePACS/Kaggle | Public | ~35K | 5-class | Acc, Sens, Spec | No |
| Gulshan #12 | EyePACS (private) | Private | 128,175 | Binary | AUC | No |
| Liu #15 | DeepDRiD | Public | — | Multi | κ, Acc | No |
| Voets #17 | EyePACS/Kaggle, Messidor-2 | Public | — | Binary | AUC | No |
| Wewetzer #14 | Multiple (pooled) | Mixed | — | Binary | Pooled Sens/Spec, SROC | Meta-analytic |
| Zhang #44 | Multicentre (4 centres) | Private | 83,465 | Binary | AUROC, κ | Expert comparison |
| Ruamviboonsuk #45 | Thai prospective | Private | 7,651 pts | Binary | Acc, Sens, Spec | p=0.024 |
| Sapakova #24 🔹SELF | APTOS 2019 + private | Mixed | ~25,000 | 5-class | Acc, F1, ROC-AUC | No |

---

# J. QUALITY CONTROL CHECKLIST

Before finalizing Chapter 1, verify each item:

- [ ] **No single-source narrative blocks without synthesis.** Every paragraph references ≥2 sources in comparative mode.
- [ ] **No unreferenced general statements.** Every claim about the field is backed by at least one cited source.
- [ ] **No superiority or dominance claims.** The dissertation's approach is positioned using neutral language (extends, integrates, formalizes).
- [ ] **No metric aggregation across incompatible datasets.** Performance comparisons always note dataset, task, and evaluation protocol differences.
- [ ] **All terminology matches Glossary.** Image quality → OD-1; preprocessing pipeline → OD-3; generalization → OD-4 (qualified); resource-limited → OD-6.
- [ ] **Identified gaps are logically derived from cited sources.** Each gap follows from documented evidence, not a priori assertion.
- [ ] **Positioning language is neutral and precise.** No "outperforms," "superior," "best," "revolutionary."
- [ ] **No experimental results from dissertation are pre-claimed.** Chapter 1 describes the state of the art and gaps; it does not preview findings.
- [ ] **Self-publications identified as prior own work at first citation (SIR-4).** Sources #19–#24 flagged as 🔹SELF.
- [ ] **Non-independent sources not cited as independent confirmation (SIR-5).** #19/#21 overlap acknowledged; #23/#24 consolidated.
- [ ] **Sensitivity formula anomaly noted (SIR-3).** Source #23 flagged when sensitivity/accuracy figures are cited.
- [ ] **Source quality flags applied.** #26, #30, #31, #37, #41, #42 cited with explicit epistemic weight qualifications.
- [ ] **§1.2.1 coverage gap explicitly flagged.** Writer acknowledges absence of dedicated image degradation sources and recommends literature acquisition.
- [ ] **Projected deployment outcomes not attributed to dissertation (SIR-8; NC-3).** Kazakhstan statistics framed as contextual, not as results.
- [ ] **Tables 1.1, 1.2, and 1.3 included** with complete source references, dataset context, and metric definitions.
- [ ] **Conclusions do not preview experimental results.** They summarize the state of the art and formally state the research problem.

---

# K. CRITICAL RULES

1. **Do not write the Literature Review chapter.** This document is the structured writing prompt only.
2. **The writing prompt is now complete and reusable.** It can be provided to a fresh conversation alongside the full Literature Cards and governing documents to generate Chapter 1.
3. **Synthesis instructions are exhaustive.** Every subsection has specified sources, analytical focus, synthesis requirements, and estimated paragraph allocation.
4. **Insufficient source coverage flagged.** §1.2.1 (Sources of Image Degradation) has ZERO sources and requires literature acquisition. §1.5 has only 2 sources (#17, #39) — adequate but thin.
5. **No external knowledge beyond provided materials has been introduced.** All source references correspond to entries in LITERATURE_INDEX.md.

---

# APPENDIX: SOURCE QUICK-REFERENCE FOR CHAPTER 1

| # | Short Citation | Ch.1 Sections |
|---|---------------|---------------|
| 01 | Pratt et al. (2016) | §1.3.1, INTRO |
| 02 | Saxena et al. (2020) | §1.3.2, §1.4 |
| 03 | Sánchez-Gutiérrez et al. (2022) | §1.4 |
| 04 | Arrieta et al. (2022) | §1.3.1 |
| 05 | Rakhlin (2017) | §1.2.2, §1.3.1 |
| 06/10 | Porwal et al. (2018) — DUPLICATE | §1.1.2 |
| 07 | Baget-Bernaldiz et al. (2021) | §1.4 |
| 08 | Wan et al. (2021) | §1.3.1 |
| 09 | Xu et al. (2024) | §1.3.1, §1.3.2 |
| 11/13 | Ting et al. (2017) — DUPLICATE | §1.4, §1.3.4 |
| 12 | Gulshan et al. (2016) | §1.3.1, §1.3.2, §1.4, INTRO |
| 14 | Wewetzer et al. (2021) | §1.4.2, INTRO |
| 15 | Liu et al. (2022) | §1.2.2, §1.3.1 |
| 16 | Goh et al. (2024) | §1.3.1, §1.3.2 |
| 17 | Voets et al. (2019) | §1.2.2, §1.5 |
| 18 | González-Díaz et al. (2024) | §1.3.1 (AMD — peripheral) |
| 22 🔹SELF | Yesmukhamedov et al. (2025b) | §1.1.2, §1.4 |
| 24 🔹SELF | Sapakova et al. (2025b) | §1.2.2 |
| 27 | Hayati et al. (2023) | §1.4.3 |
| 31 | Kesharwani et al. (2021) | §1.1.1 (⚠️ caution) |
| 32 | Kusuhara et al. (2018) | §1.1.1 |
| 33 | Gettinger et al. (2025) | §1.1.1, INTRO |
| 34 | Morya et al. (2024) | §1.1.1, §1.1.2 |
| 35 | Wang & Lo (2018) | §1.1.1, INTRO |
| 37 | Geetha & Hema (2026) | §1.3.1 (arch. reference only) |
| 38 | Khosravi et al. (2025) | §1.3.1 |
| 39 | Senapati et al. (2024) | §1.4.2, §1.5 |
| 40 | Araf et al. (2024) | §1.4.2 |
| 41 | Sharma et al. (2025) | §1.3.1 (⚠️ metric issue) |
| 42 | Arora et al. (2024) | §1.3.1 |
| 43 | Ryu et al. (2021) | §1.3.1, §1.4 |
| 44 | Zhang et al. (2022) | §1.4.1, §1.3.4 |
| 45 | Ruamviboonsuk et al. (2022) | §1.4.1, §1.3.4 |

**Total sources mapped to Chapter 1:** ~35 (out of 45 in corpus)
**Sources NOT used in Chapter 1:** #20 (laser modeling — Ch. 2), #23 🔹SELF (CLAHE formalization — Ch. 2/3), #19/#21 🔹SELF (transfer learning experiments — Ch. 2/3/4), #25 (Wikipedia — not citable), #26 (FCE+CLAHE — Ch. 2/3), #28/#29 (peripheral FHIR), #30 (OCT preprocessing — Ch. 2), #36 (FHIR interop — Ch. 6)

---

*End of Chapter 1 Review-Mode Writing Prompt*
*Bound to: DISSERTATION_INVARIANTS.md v.1.0 | ARGUMENT_MAP.md | GLOSSARY_v1_0.md*
*Generated per: REVIEW_MODE_META_PROMPT.md specifications (Sections A–K)*
