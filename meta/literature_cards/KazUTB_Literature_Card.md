# Literature Card

---

## I. SOURCE IDENTIFICATION

| Field | Content |
|-------|---------|
| **Unique ID** | `LC-Sapakova-2024-01` |
| **Full Bibliographic Citation** | **GOST R 7.0.5-2008:** Сапакова С.З., Данияррова Д.Р., Есмухамедов Н.С., Арманкызы Р., Ембердиева А.Б., Калдыбаева А.С. Mathematical Modeling of Laser Exposure on Fundus Tissues in the Treatment of Diabetic Retinopathy // Вестник КазУТБ. — 2024. — Т. 2, № 27-740. DOI: 10.58805/kazutb.v.2.27-740. **APA 7th (secondary):** Sapakova, S. Z., Daniyarova, D., Yesmukhamedov, N., Armankyzy, R., Emberdieva, A. B., & Kaldybaeva, A. (2024). Mathematical modeling of laser exposure on fundus tissues in the treatment of diabetic retinopathy. *Herald of KazUTB — Vestnik KazUTB*, *2*(27-740). https://doi.org/10.58805/kazutb.v.2.27-740 |
| **Publication Type** | Methodological paper. Justification: The source develops and presents mathematical models and numerical methods for simulating laser-tissue thermal interaction; it does not collect clinical data or test hypotheses on patient cohorts, nor does it review the literature systematically. |
| **Year** | 2024 |
| **Research Domain Classification** | Primary domain: Biomedical optics → Subdomain: Laser-tissue interaction modeling (thermal modeling of laser coagulation in ophthalmology) |

---

## II. GLOBAL SOURCE ANALYSIS

### II.1 Central Thesis

The authors argue that mathematical modeling of laser exposure on fundus tissues — specifically through differential equations describing thermal conductivity and laser radiation absorption — enables precise prediction of temperature distribution in eye tissue layers, which in turn allows optimization of laser parameters (power, pulse duration, spot diameter) to maximize therapeutic efficacy while minimizing damage to healthy tissues in the treatment of diabetic retinopathy. (Introduction, p. 1; Conclusion, p. 7)

### II.2 Research Problem Addressed

The source addresses the problem that effective laser coagulation therapy for diabetic retinopathy requires precise control of laser parameters, yet without mathematical modeling, there is insufficient ability to predict how laser energy distributes thermally across heterogeneous fundus tissue layers (cornea, choroid, retina), risking damage to healthy tissues. The authors frame this as a need to "construct a mathematical model describing laser coagulation effects on the retina" and to "study the impact of different laser parameters on effectiveness in treating diabetic retinopathy." (Introduction, p. 1–2)

### II.3 Methodology

- **Theoretical framework:** The work is grounded in classical heat conduction theory applied to biological tissues, specifically the Beer-Lambert law for laser radiation attenuation in tissue, the energy balance equation relating absorbed laser energy to temperature change, and the general heat conduction equation with spatially varying thermal properties. The Gaussian beam profile is assumed for initial laser intensity distribution. (Materials and Methods, p. 3–5, Equations 1–8)
- **Methods used:** Finite difference method (explicit scheme) for numerical solution of the heat conduction equation; Gaussian beam model for laser intensity profile; Beer's law for depth-dependent absorption; energy balance equation for thermal modeling. (Materials and Methods, p. 3–5; Results and Discussion, p. 6)
- **Data sources:** No clinical or experimental data were collected. The models use simulation parameters (laser power, spot radius, tissue absorption coefficients, thermal conductivity, volumetric heat capacity) without specifying their exact numerical values or sources in the text. The APTOS dataset or any fundus image dataset is not used; a fundus image is used only as a visual overlay for the heat map (Figure 1). (Results and Discussion, p. 6)
- **Analytical approach:** Numerical solution of the discretized heat conduction equation in Python using NumPy and SciPy libraries; visualization of temperature fields over time and depth using Matplotlib and Seaborn in a Jupyter Notebook environment. Results are presented as heat maps and temperature-depth/time graphs for three tissue layers (cornea, choroid, retina). (Results and Discussion, p. 6–7)

### II.4 Conceptual Contributions

The source does not introduce novel concepts or models. It applies and combines established physical models:

1. **Beer's Law for laser attenuation in tissue** (Equation 2, p. 4): Applied to describe exponential decrease of laser radiation intensity with depth, using an absorption coefficient β(r,z).
2. **Energy balance equation for laser-heated tissue** (Equation 3, p. 5): Applied to relate absorbed laser power to temperature change via volumetric heat capacity.
3. **Gaussian beam intensity profile** (Equation 7, p. 5): Applied to model initial laser intensity distribution as I₀(r) = (P/πa²)e^(−(r/a)²), where P is laser power and a is spot radius.
4. **General heat conduction equation with spatially varying properties** (Equation 8, p. 5): Applied in the form Coσ(x,y,z,T)∂T/∂t = div(k(x,y,z,T)·grad(T)), accounting for tissue inhomogeneity.
5. **Temperature change formulation** (Equations 4–6, p. 5): Applied to express temperature change as a function of initial intensity, absorption coefficient, volumetric heat capacity, and thermal conductivity.

The contribution lies in the integration of these models into a unified numerical simulation framework applied specifically to fundus tissues in the context of diabetic retinopathy laser coagulation.

### II.5 Empirical Contributions

Not applicable — theoretical/modeling study. No clinical or experimental data were collected. The authors present computational simulation results only:

- Temperature in surface tissue layers (cornea) rises significantly faster than in deeper layers (choroid, retina) (Figures 2–5, p. 6–7).
- Temperature stabilizes in deep layers after some time following laser exposure (Figure 4, p. 6).
- Temperature distribution is modeled over time intervals from 0 to 4.5 seconds across tissue depth (Figures 4–5, p. 6–7).

No specific numerical temperature values, thresholds, or error margins are reported in the text. Results are presented qualitatively through graphs and heat maps.

Validation claim: The authors state that "results of this study confirm the effectiveness of using laser therapy" and that their approach "allows precisely modeling heat exchange in fundus tissues, which can lead to improved clinical outcomes," but no quantitative validation against experimental or clinical data is provided. (Results and Discussion, p. 7)

### II.6 Limitations Acknowledged by the Author

- The authors state that "further research and experiments are required for effective application of laser exposure." (Abstract, p. 1)
- The Conclusion states: "Future research will be aimed at deeper study of laser energy effects on different tissues and evaluating long-term effects of multiple laser applications." (Conclusion, p. 7)

No other limitations are explicitly acknowledged. The authors do not discuss the absence of experimental validation, the lack of specified tissue parameter values, or the simplifications inherent in the 1D/2D modeling approach.

### II.7 Implicit Assumptions

1. **Tissue optical and thermal properties are static during laser exposure.** The model uses fixed absorption coefficients β(r,z) and thermal conductivity k(x,y,z,T) without accounting for dynamic changes due to coagulation-induced tissue property alteration. Evidence: Equations 2, 4, 8 (p. 4–5) treat these as given parameters without temperature-dependent modification beyond the general notation.

2. **The fundus can be modeled as a layered medium with homogeneous properties within each layer.** The graphs (Figures 3, 5, p. 6–7) present results for "cornea," "choroid," and "retina" as distinct layers with uniform behavior within each layer, despite the Introduction acknowledging tissue "inhomogeneity" (p. 1).

3. **Gaussian beam profile remains stable throughout the exposure.** Equation 7 (p. 5) assumes a fixed Gaussian distribution; no scattering or beam distortion effects are modeled.

4. **No blood perfusion term is included in the heat equation.** The heat conduction equation (Equation 8, p. 5) does not include a perfusion term (as would appear in the Pennes bioheat equation with blood flow), despite the Introduction referencing the Pennes bio-heat equation in the literature review (p. 3, reference [8]). The authors' own model omits this term.

5. **Boundary conditions are set at sufficient distance from the laser axis such that thermal energy does not reach them.** This is stated explicitly (p. 5) but constitutes an assumption that the computational domain is large enough that boundary effects are negligible, without verification.

---

## III. EXTRACTION BLOCKS

---

### [Extraction Block ID: EB-01]

**Relevant to:**
- Dissertation claim(s): C4 — Mathematical modeling of laser-tissue interaction informs diagnostic image feature interpretation and supports laser coagulation parameter optimization.
- Dissertation chapter/section: Chapter 2, Section on mathematical modeling of laser-tissue interaction.
- Concept(s) used: Heat conduction model for laser-irradiated fundus tissue; Beer's law for laser attenuation; energy balance equation; Gaussian beam profile.
- Research question addressed: How can mathematical models describe the thermal effects of laser coagulation on retinal tissue?

**Function in dissertation:**
- [x] Theoretical grounding — This source provides the mathematical framework (Equations 1–8) that underpins the dissertation's Chapter 2 treatment of laser-tissue interaction modeling.
- [x] Methodological precedent — The finite difference numerical solution approach serves as methodological precedent for the dissertation's computational modeling component.

**Extracted Content (Strict Extraction Only):**
- Beer's law for laser intensity attenuation: I(r,z) = I₀(r)e^(−∫₀ᶻ β(r,ξ)dξ), where β(r,z) is the absorption coefficient. (Equation 2, p. 4)
- Energy balance equation: ΔV · Co(x,y,z) · ΔT(x,y,z) = W(…) · Δt, relating elementary volume, volumetric heat capacity, temperature change, laser power, and time interval. (Equation 3, p. 5)
- Temperature change formula: ΔT(x,y,z) = [I₀(…)e^(−∫₀ᶻ β(x,y,ξ)dξ) · β(x,y,z)Δt] / [Co(x,y,z)σ(x,y,z)]. (Equation 4, p. 5)
- Gaussian beam intensity: I₀(r) = (P/πa²)e^(−(r/a)²), where a = spot radius, P = laser power. (Equation 7, p. 5)
- General heat conduction equation: Coσ(x,y,z,T)∂T/∂t = div(k(x,y,z,T)·grad(T)), with initial condition T|ₜ₌₀ = ΔT(x,y,z) + Tᶜ(x,y,z). (Equation 8, p. 5)
- Simplification for slowly varying absorption coefficient: 1 − e^(−∫ᶻᶻ⁺ᐩᶻ β(r,ξ)ds) ≈ β(r,z)Δz. (Equation 5, p. 5)
- Numerical solution was obtained using the explicit finite difference method in Python. (Results and Discussion, p. 6)

**Strength of Relevance:** **Core.** This source is co-authored by the dissertation candidate and directly provides the mathematical modeling content that constitutes the laser-tissue interaction component of Chapter 2. Removing it would eliminate the primary published basis for the dissertation's thermal modeling framework.

---

### [Extraction Block ID: EB-02]

**Relevant to:**
- Dissertation claim(s): C4 — Mathematical modeling of laser-tissue interaction supports laser coagulation parameter optimization.
- Dissertation chapter/section: Chapter 4 or Chapter 5, sections discussing simulation results and parameter sensitivity.
- Concept(s) used: Temperature distribution in layered fundus tissues; laser parameter optimization.
- Research question addressed: How do laser parameters (power, pulse duration, spot size) affect temperature distribution across fundus tissue layers?

**Function in dissertation:**
- [x] Empirical support — The simulation results (Figures 1–5) provide computational evidence for the claim that laser parameter adjustment affects tissue temperature distribution differentially across layers.

**Extracted Content (Strict Extraction Only):**
- "Temperature in surface tissue layers rises significantly faster and spreads slowly in deeper layers, confirming the importance of precise laser exposure control." (Abstract, p. 1)
- Cornea: "temperature rises quickly due to high laser energy absorption." Choroid: "temperature change is slow and stable." Retina: "temperature remains relatively stable with depth." (Figure 3 description, p. 6)
- "Tissue surface temperature rises immediately after laser exposure, then spreads to depth and begins to stabilize as time passes." (Figure 4 description, p. 6)
- Temperature distribution modeled over 0 to 4.5 seconds across tissue depth. (Figures 4–5, p. 6–7)
- "Optimizing laser parameters increases laser exposure precision and effectiveness without damaging healthy tissues." (Conclusion, p. 7)

**Strength of Relevance:** **Supporting.** The simulation results reinforce claim C4 but are qualitative (no reported numerical temperature values), so they add conceptual support rather than quantitative evidence.

---

### [Extraction Block ID: EB-03]

**Relevant to:**
- Dissertation claim(s): C5 — The system is deployable in resource-limited telemedicine environments.
- Dissertation chapter/section: Chapter 6, Section on AI processing module and system architecture.
- Concept(s) used: Software implementation using open-source tools (Python, NumPy, SciPy, Matplotlib, Jupyter Notebook).
- Research question addressed: Can the computational modeling component be implemented using accessible, open-source tools suitable for resource-limited settings?

**Function in dissertation:**
- [x] Methodological precedent — The implementation stack (Python, NumPy, SciPy, Matplotlib, Jupyter Notebook) demonstrates feasibility of the modeling component using freely available tools.

**Extracted Content (Strict Extraction Only):**
- "The modeling process was built on the basis of the Python programming language, and NumPy and SciPy libraries were used for computational and numerical analysis purposes." (Results and Discussion, p. 7)
- "Matplotlib and Seaborn tools were used to visually display temperature field and laser parameter distribution in space." (Results and Discussion, p. 7)
- "The study was conducted in the Jupyter Notebook interactive environment, which allowed modularizing the structure of scientific calculations, ensuring result accuracy, and making the research process reproducible." (Results and Discussion, p. 7)

**Strength of Relevance:** **Peripheral.** This information provides useful context for the dissertation's argument about resource-limited deployability but does not directly substantiate C5 regarding the full screening system.

---

### [Extraction Block ID: EB-04]

**Relevant to:**
- Dissertation claim(s): C2 — Integration of image enhancement methods with CNN as a unified pipeline yields clinically reliable automated DR diagnosis (indirectly, via the broader system concept).
- Dissertation chapter/section: Chapter 1, Section on problem domain analysis and current state of automated DR diagnosis; Chapter 2, literature review on laser-tissue interaction.
- Concept(s) used: Literature review of laser-tissue interaction modeling in ophthalmology.
- Research question addressed: What is the current state of mathematical modeling for laser-tissue interaction in the treatment of diabetic retinopathy?

**Function in dissertation:**
- [x] Theoretical grounding — The literature review in the Introduction (p. 2–3) surveys existing models (Pennes bio-heat equation, Monte Carlo method, Arrhenius integral, MPC method, 3D FEM) that contextualize the dissertation's modeling approach within the broader field.

**Extracted Content (Strict Extraction Only):**
- Reference to 3D fundus structure restoration via OCT and algorithms for retinal segmentation and laser exposure modeling, with root mean square deviation decreasing by 1.7–5.9 times when intervals doubled [ref. 1]. (Introduction, p. 2)
- MILI model used for calculating optimal laser radiation parameters, energy absorption, and heat distribution [ref. 2]. (Introduction, p. 2)
- Multilayer Monte Carlo method for modeling laser beam propagation and energy absorption in multilayer homogeneous medium [ref. 3]. (Introduction, p. 3)
- Computer models at cellular level showed 31% deviation from experimental data for retinal thermal damage thresholds [ref. 4]. (Introduction, p. 3)
- Arrhenius first-order rate constant and integral used for predicting thermal damage threshold [ref. 5]. (Introduction, p. 3)
- Model Predictive Control (MPC) method for solving laser radiation heat equation [ref. 6]. (Introduction, p. 3)
- Pennes bio-heat equation for studying laser radiation-tissue interaction [ref. 8]. (Introduction, p. 3)
- 3D extension of 2D thermal model using finite element method with Galerkin-Bubnov procedure [ref. 11]. (Introduction, p. 3)

**Strength of Relevance:** **Supporting.** The literature survey provides secondary references and contextual framing for the dissertation's own literature review but does not contribute original analysis.

---

## IV. RELATIONAL POSITIONING

| Relation Type | Details |
|---------------|---------|
| **Supports which dissertation claims** | **C4** (theoretical and methodological support): Provides the mathematical framework for laser-tissue interaction modeling, including equations for thermal conductivity, Beer's law attenuation, energy balance, and Gaussian beam profile. Simulation results qualitatively demonstrate differential temperature distribution across fundus layers, supporting the claim that mathematical modeling informs laser coagulation parameter optimization. **C5** (peripheral methodological support): Demonstrates implementation feasibility using open-source Python tools. |
| **Contradicts which claims (if any)** | No contradictions identified. |
| **Extends which conceptual axis** | Thermal modeling of laser-tissue interaction. This source extends the dissertation's mathematical modeling thread by providing a published, peer-reviewed implementation of the heat conduction framework applied specifically to fundus tissues in the DR treatment context. |
| **Overlaps with which other sources** | Overlaps with references cited within the source itself: Shirokanev et al. (2021) [ref. 1] on fundus laser exposure modeling; Cvetković et al. (2008, 2010) [refs. 5, 11] on thermal modeling of the human eye; Welch et al. (1979) [ref. 12] on experimental validation of thermal retinal models. Cross-referencing with other dissertation sources pending. |

---

## V. REUSABILITY CONTROL

| Aspect | Assessment |
|--------|------------|
| **What can be reused in dissertation drafting** | Equations 1–8 (with proper citation) as the mathematical framework for Chapter 2's laser-tissue interaction modeling section. The literature review references (refs. 1–12) as secondary entry points to the broader modeling literature. The general finding that surface layers absorb more laser energy than deep layers, with appropriate citation. The Python/NumPy/SciPy implementation approach as precedent for the dissertation's computational methodology. |
| **What must be reformulated** | All prose descriptions of the models, results, and conclusions must be fully rewritten to avoid verbatim overlap. The Introduction's literature review framing must be independently restructured. Figure descriptions and result interpretations must be presented in the candidate's own words with new analysis. The discussion comparing results to prior work (p. 7) must be independently composed. |
| **Risk of self-plagiarism** | **HIGH — Yesmukhamedov N. is a co-author of this source.** This publication is explicitly referenced in the seminar presentation as "a laser-tissue interaction modeling component (published in Vestnik KazUTB)." Precautions required: (1) This prior publication must be explicitly cited in the dissertation introduction and in every chapter section where its content is used. (2) No verbatim text may be reused from this publication in the dissertation. (3) All equations must be re-derived or presented with independent notation and commentary, with citation to this source. (4) Figures must be regenerated, not reproduced. (5) The dissertation must clearly state the relationship between this publication and the dissertation research (e.g., "Preliminary results of this modeling work were published in [self-citation]"). |

---

## VI. TERMINOLOGY INDEX

| Term | Author's Definition/Usage | Page/Section | Dissertation Equivalent (if different) |
|------|--------------------------|--------------|---------------------------------------|
| Diabetic retinopathy | "A retinal disease of the eye that develops due to the prolonged course of diabetes mellitus," causing blood vessel damage, vision deterioration, and potential blindness. | Introduction, p. 1 | Same |
| Laser coagulation | Laser radiation affecting the retina causing "protein coagulation and destruction of abnormal vessels" to stop disease progression. | Introduction, p. 1 | Same |
| Beer's law (laser attenuation) | Describes exponential decrease of laser radiation intensity with tissue depth: I(r,z) = I₀(r)e^(−∫₀ᶻ β(r,ξ)dξ). | Equation 2, p. 4 | Same (Beer-Lambert law) |
| Absorption coefficient β(r,z) | Coefficient governing the rate of laser radiation absorption as a function of position in cylindrical coordinates. | Equation 2, p. 4 | Same |
| Volumetric heat capacity Co(x,y,z) | Thermal property of tissue representing heat energy stored per unit volume per degree temperature change. | Equation 3, p. 5 | Same |
| Thermal conductivity k(x,y,z,T) | Coefficient at point (x,y,z) at temperature T governing rate of heat conduction through tissue. | Equation 8, p. 5 | Same |
| Gaussian beam profile | Initial laser intensity distribution: I₀(r) = (P/πa²)e^(−(r/a)²), where a = spot radius, P = laser power. | Equation 7, p. 5 | Same |
| Spot radius (a) | Radius of the laser beam spot on tissue surface; does not change during laser coagulation. | Equation 7, p. 5 | Same |
| Heat conduction equation | General form: Coσ(x,y,z,T)∂T/∂t = div(k(x,y,z,T)·grad(T)), describing temperature evolution in tissue after laser exposure. | Equation 8, p. 5 | Same |
| Finite difference method | Explicit numerical method used to discretize and solve the heat conduction equation over a grid in time and space. | Results and Discussion, p. 6 | Same |
| Heat map | Visual representation of temperature distribution in fundus tissues overlaid on a fundus image. | Figure 1, p. 6 | Same |
| Laser parameters | Collective term for power, pulse duration, spot diameter, wavelength, and intensity — the controllable variables in laser therapy. | Introduction, p. 1; throughout | Same |
| Fundus | The interior surface of the eye including the retina; the target tissue for laser therapy in DR treatment. | Title; throughout | Same |
| Pennes bio-heat equation | Referenced in literature review as a model for studying laser radiation-tissue interaction; not used in the authors' own model. | Introduction, p. 3 (ref. [8]) | Same |
| Arrhenius integral | Referenced in literature review for predicting thermal damage threshold from laser radiation; not applied in the authors' own model. | Introduction, p. 3 (ref. [5]) | Same |
