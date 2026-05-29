# Paradigmatic Framing — Defense Speech and Anticipated Q&A
## Companion document to slide 05a_PARADIGMATIC_POSITIONING.md

**Date:** 2026-05-28
**Bindings:** INVARIANTS.md SB-1.12, CFC-2.9, SIR-9; CONTRIBUTIONS.md §Conceptual framing; ARGUMENT_MAP.md PC-0; gulshan-2016.md §15 Paradigmatic Role.

---

## 1. 60-Second Oral Fragment (Task 3.3.1)

To be delivered when introducing the conceptual framing of the work, ideally on slide 05a (Paradigmatic Positioning) or in the Discussion section (slide 40 / 41).

### English (primary)

> The conceptual foundation of this dissertation is a contrast between two paradigms for automated diabetic retinopathy diagnosis. Paradigm P1 — the end-to-end CNN paradigm — treats preprocessing as ancillary data preparation, not requiring methodological discussion. I designate Gulshan et al. 2016, JAMA, as the canonical representative of this paradigm — not on the basis of any theoretical statement by the authors, but on the basis of their observable methodological practice: preprocessing is deferred to supplementary material, and the main-text emphasis is on the Inception-v3 ensemble, the dataset of 128,175 images, and the multi-grader reference standard.
>
> Paradigm P2 — the integrated preprocessing-CNN paradigm — treats preprocessing as an integral component of the model itself, because it defines the feature space available to the network. The present work operationalises paradigm P2 in the form of an 8-stage preprocessing pipeline placed under controlled experimental contrast against the P1-instantiation baseline in Experiment 1. The A-versus-B and C-versus-D contrasts in the factorial are not a numerical comparison against Gulshan — such a comparison would be methodologically unsound given the differences in task, backbone, dataset partition, and validation protocol — but a matched-condition empirical contrast between the two paradigms within the dissertation's own experimental framework.

### Kazakh (secondary, for trilingual defense if required)

> Диссертациямның концептуалды негізі — диабеттік ретинопатияны автоматты диагностикалаудың екі парадигмасының қарама-қайшылығы. Парадигма P1 — end-to-end CNN парадигмасы — препроцессингті қосалқы деректерді дайындау сатысы ретінде қарастырады. Gulshan et al. 2016 *JAMA* еңбегі — осы парадигманың канондық өкілі: авторлардың теориялық тұжырымы негізінде емес, олардың әдіснамалық тәжірибесі негізінде (препроцессинг supplementary материалға шығарылған).
>
> Парадигма P2 — интегралды preprocessing-CNN парадигмасы — препроцессингті модельдің ажырамас компоненті ретінде қарастырады, өйткені ол CNN-ге қол жетімді feature space-ті анықтайды. Бұл диссертация — осы парадигманың 8-сатылы pipeline арқылы іске асырылуы; Эксперимент 1 — оның тең шарттардағы эмпирикалық тексерілуі. A vs B және C vs D салыстырулары Gulshan-нің сандық көрсеткіштерімен бетпе-бет қойылмайды — тапсырма, backbone, validation protocol айырмашылықтары мұндай салыстыруды әдіснамалық тұрғыдан болмайтын етеді.

---

## 2. Anticipated Committee Questions (Task 3.3.2)

### Q1. "Why did you not directly replicate Gulshan?"

**Answer.**
A direct replication of Gulshan et al. (2016) was deliberately not undertaken, for three reasons.

1. **Different classification endpoint.** Gulshan performs binary referable-DR detection (moderate-or-worse DR and/or referable DME vs. not). This dissertation performs five-class DR staging (DR 0–4). A replication would have required either downgrading the dissertation's endpoint to a binary task — losing the per-grade information that motivates this work — or upgrading Gulshan's setup to a five-class task, which would no longer be a replication.

2. **Different dataset access regime.** Gulshan's development set comprises 128,175 private images from EyePACS and three Indian hospitals, with reference labels supplied by 54 ophthalmologists, 3–7 reads per image, with majority voting. The dissertation operates on the public ~35,126-image Kaggle EyePACS partition with the single labels supplied at competition release. Replicating Gulshan's reference standard would have required private clinical access and grader recruitment beyond the scope and resources of a doctoral dissertation.

3. **Different conceptual goal.** A replication would have addressed the question "does Gulshan's result hold under reproduction?" — which is the question Voets et al. (2019) addressed. The present dissertation addresses a different question: "does formalising preprocessing as an integral model component (paradigm P2) yield measurable improvement over the same architecture under the unformalised-preprocessing paradigm (P1)?" This is a controlled within-study contrast, not a between-study replication.

For the same three reasons, I do not claim to outperform Gulshan numerically. The dissertation's contribution is paradigmatic and methodological, not numerical, with respect to Gulshan 2016.

---

### Q2. "Why ResNet-50 / EfficientNet-B3 rather than Inception-v3?"

**Answer.**
Three reasons motivated the choice of ResNet-50 and EfficientNet-B3 over Inception-v3.

1. **Compatibility with the hardware constraint.** The experiments were run on a single NVIDIA RTX 3060 with 12 GB VRAM at image resolution 512×512 and batch size 16. ResNet-50 and EfficientNet-B3 fit this budget comfortably; Inception-v3 at the same resolution and batch size approaches the VRAM limit and does not leave headroom for the 4-channel V5 configuration (RGB + FOV mask).

2. **Factorial-design symmetry.** Experiment 1 is a 2×2 factorial in *(preprocessing × architecture)*. The dissertation's research question requires *two* architectures so that the preprocessing main effect can be tested for robustness across backbone families: a residual-connection backbone (ResNet-50) and a compound-scaling backbone (EfficientNet-B3). Inception-v3 alone would not have permitted this test.

3. **Backbone-family currency.** Inception-v3 was state-of-the-art in 2014–2016; by 2024–2026 the dominant backbone families for medical imaging are residual networks and the EfficientNet family. The dissertation's contribution is positioned relative to contemporary backbones, not to the 2016 backbone landscape.

---

### Q3. "What are the numerical differences between your results and Gulshan's?"

**Answer.**
I do not report a direct numerical comparison against Gulshan 2016, and the dissertation's governance documents explicitly forbid such a comparison (INVARIANTS SB-1.12, CFC-2.2). The reason is that the two studies are not commensurable:

- Gulshan reports binary referable-DR AUC = 0.991 on EyePACS-1 and 0.990 on Messidor-2.
- The dissertation reports five-class weighted F1, ROC-AUC (multi-class one-vs-rest), Cohen's Kappa with quadratic weights, and Accuracy on the EyePACS public partition.

A binary AUC and a five-class weighted F1 are not on the same scale; any "X > Y" statement comparing them would be methodologically meaningless. Furthermore, the backbone (Inception-v3 ensemble of 10 networks vs. single ResNet-50 / EfficientNet-B3), the pretraining source (ImageNet for both arms in Gulshan; ImageNet / RETFound CFP in the dissertation), and the reference standard (multi-grader majority vote vs. public competition labels) differ in ways that make the comparison unsound under any of these differences alone, and forbidden under their joint operation.

What the dissertation *does* report is its own internal contrast: configs B and D (P2 instantiation) versus configs A and C (P1 instantiation) under matched conditions on the same EyePACS partition. That contrast is the empirical evidence for the paradigmatic claim. Numerical figures from Gulshan are admitted into the dissertation only as historical / contextual reference (chapters 1.4 and 5.5), each accompanied by the methodological-differences caveat block.

---

## 3. Forbidden Phrasings in Live Speech

The following phrasings are forbidden during the live defense, in line with INVARIANTS:

- "Gulshan is our baseline" — conflicts with OD-3 and SB-1.12. The operational baseline is configs A/C, defined in OD-3; it is not Gulshan's system.
- "We outperform Gulshan" / "We beat Gulshan" — forbidden by CFC-2.2 in the absence of a direct controlled replication.
- "Gulshan claimed preprocessing is unimportant" — forbidden by CFC-2.9; no such statement appears in the cited paper.
- "Gulshan ignored preprocessing" — forbidden; the preprocessing is reported in the supplementary material, not absent.

## 4. Permitted Phrasings in Live Speech

- "Gulshan et al. (2016) is, in this dissertation, the canonical representative of paradigm P1."
- "The baseline configuration of Experiment 1 operationally instantiates the paradigm represented by Gulshan."
- "Direct numerical comparison with Gulshan is not performed due to differences in task, backbone, dataset partition, reference standard, and validation protocol."
- "The A-vs-B and C-vs-D contrasts are empirical comparisons between two paradigms under matched conditions, not against external figures."
- "The principal conceptual contribution of this dissertation is the P1 → P2 paradigm shift; the 8-stage V5 pipeline is its engineering operationalisation."
