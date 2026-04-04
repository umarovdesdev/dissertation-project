# Scientific Novelty — Defense Slide

**Purpose:** One slide in the defense presentation.
**Two deliverables below:** (A) exact text for the slide, (B) presenter script.

---

## A. SLIDE TEXT (what goes on the slide)

**Slide title:** Scientific Novelty

---

**1. Preprocessing as an optimizable model component**

The 6-stage V4 pipeline is formalized as a parameterized transformation P(θ). A 2×2 factorial experiment (6 configs, 2 CNN architectures) demonstrates that optimization over P(θ) dominates architectural choice (ΔF1 ≥ 5 pp, ΔAUC ≥ 0.02) — establishing preprocessing as the primary performance driver.

**2. Per-patient binocular fusion (PatientHead)**

A dual-branch architecture fuses left- and right-eye CNN features via Φ(f_L, f_R) = [f_L ‖ f_R ‖ |f_L − f_R|], elevating inference from single-image to patient-level. Canonical orientation (Stage 0) is a prerequisite for anatomically meaningful bilateral comparison.

**3. ALO — quantitative explainability metric**

Attention–Lesion Overlap (ALO = area(GradCAM ∩ lesion) / area(lesion)) replaces qualitative saliency maps with a per-lesion-type quantitative metric. Cross-condition analysis links ALO to classification performance, positioning it as a functional predictor of diagnostic quality.

**4. Multi-device cross-dataset transferability**

Zero-shot evaluation on 5 external datasets (Messidor-2, IDRiD, RFMiD, DDR, ODIR-5K), 4 camera manufacturers (Canon, Topcon, Kowa, Zeiss), with pre-registered threshold G = F1_ext / F1_train ≥ 0.85.

---

## B. PRESENTER SCRIPT (what you say out loud)

**Estimated speaking time: 2–2.5 minutes.**

---

### Opening (10 sec)

> This slide summarizes the four elements of scientific novelty. I will go through each briefly.

---

### Point 1 — Preprocessing dominance (~40 sec)

> The central novelty of the work is how we treat preprocessing. Most papers in DR classification apply CLAHE or normalization as a data preparation step and then focus entirely on the neural network architecture. We take the opposite position.
>
> We formalize the preprocessing pipeline as a parameterized transformation P(θ) — where θ includes CLAHE clip parameters, flat-field sigma, augmentation distributions, and so on — and we show experimentally that optimizing over this space produces greater gains than switching between ResNet-50 and EfficientNet-B3.
>
> The evidence comes from Experiment 1: a 2×2 factorial design with six configurations. The dominance criteria — delta F1 at least 5 percentage points, delta AUC at least 0.02 — are pre-registered and tested independently for both architectures.
>
> This reframes preprocessing from an engineering detail into the primary lever for diagnostic improvement.

---

### Point 2 — Binocular fusion (~30 sec)

> The second element is the PatientHead architecture. In clinical practice, an ophthalmologist always looks at both eyes. But almost every automated DR system classifies each image independently — left and right eyes are treated as unrelated samples.
>
> We introduce a binocular fusion head that takes feature vectors from both eyes and combines them via concatenation plus element-wise absolute difference. The absolute difference is the key — it captures inter-ocular asymmetry, which is clinically known to correlate with disease progression.
>
> Importantly, this only works because Stage 0 of our pipeline flips all left-eye images to a canonical right-eye orientation. Without this step, the optic disc and fovea are mirrored, and direct feature comparison is meaningless.

---

### Point 3 — ALO metric (~30 sec)

> Third: explainability. Existing DR papers that use Grad-CAM show attention maps qualitatively — a heatmap on a fundus image, and a sentence saying "the model attends to lesions." There is no number attached.
>
> We introduce ALO — Attention–Lesion Overlap — defined as the fraction of the lesion mask that is covered by the Grad-CAM activation. This directly answers the clinical question: does the model actually look at the lesion?
>
> We compute ALO per lesion type — microaneurysms, hemorrhages, hard exudates, soft exudates — using IDRiD pixel-level masks. And through cross-condition analysis across our ablation experiments, we show that ALO covaries with classification performance: preprocessing configurations that increase ALO also increase F1. This transforms ALO from a visualization tool into a functional quality indicator.

---

### Point 4 — Cross-device transferability (~20 sec)

> Finally, transferability. We train on EyePACS — Canon cameras — and evaluate in zero-shot mode on five external datasets acquired with four different camera manufacturers. We use a pre-registered generalization ratio: F1 on the external set divided by F1 on EyePACS, with a threshold of 0.85.
>
> No prior preprocessing study in DR classification has reported this kind of systematic multi-device validation with quantitative thresholds.

---

### Closing (10 sec)

> These four elements — preprocessing as an optimization problem, binocular fusion, quantitative explainability, and multi-device transferability — together constitute the scientific novelty of the work.

---

## C. DESIGN NOTES FOR SLIDE LAYOUT

- Use **numbered bold headings** (1–4) as visual anchors — the audience reads the heading, you fill in the detail verbally
- Keep each point to **2–3 lines maximum** on the slide — the text above is already at the density limit
- Consider a **thin vertical accent line** or **icon** next to each point for visual separation
- Font size: headings 20–22pt, body 16–18pt
- Do **not** add diagrams or formulas beyond what's in the text — one slide means text density wins over illustration
- If you want to add one visual element: the P(θ) formula or the ALO formula in a small callout box in the margin
