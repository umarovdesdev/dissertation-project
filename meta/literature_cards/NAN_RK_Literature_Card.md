# LITERATURE CARD

---

## I. SOURCE IDENTIFICATION

| Field | Value |
|---|---|
| **Unique ID** | LC-2025-Yesmukhamedov-01 |
| **Full Bibliographic Citation** | Yesmukhamedov, N. S., Sapakova, S., Al-Haddad, S. A. R., & Daniyarova, D. (2025). Development of an information system architecture for healthcare institutions using artificial intelligence. *News of the National Academy of Sciences of the Republic of Kazakhstan, Physico-Mathematical Series, 2*(354), 74–91. https://doi.org/10.32014/2025.2518-1726.345 |
| **Type of Publication** | Empirical study (with system architecture design and review components) |
| **Year** | 2025 |
| **Research Domain Classification** | Healthcare Information Systems > AI-Integrated Medical Imaging Architecture > Ophthalmological Diagnostic Systems |

---

## II. GLOBAL SOURCE ANALYSIS

### II.1 Central Thesis

The source argues that a modular and scalable AI-driven information system architecture — integrating medical imaging modules, cloud platforms, medical data repositories, and AI algorithms — can enhance diagnostic accuracy and efficiency in healthcare institutions while preserving the physician's central role in decision-making and complying with international data security and confidentiality standards. The paper further contends that this architecture, combined with telemedicine and portable diagnostic devices, is specifically adaptable to the ophthalmological care needs of Kazakhstan, particularly for addressing diabetic retinopathy screening in rural and underserved areas (pp. 74–75, 90).

### II.2 Research Problem Addressed

The source addresses the challenge of integrating AI technologies into real clinical practice for medical image processing (MRI, CT, X-ray, retinal imaging), while ensuring compatibility with electronic medical records (EMRs). The authors frame this as a dual problem: (1) the technical challenge of processing heterogeneous medical imaging data and linking it to patient records, and (2) the systemic challenge of deploying such systems in resource-limited healthcare environments, specifically in Kazakhstan, where only approximately 1,200 ophthalmologists serve the entire population and over 40% of residents live in rural areas with limited access to specialized care (pp. 74, 77, 86–87).

### II.3 Methodology

- **Theoretical framework:** The paper adopts a systems engineering and software architecture design approach, employing UML modeling (component diagrams, sequence diagrams, class diagrams, activity diagrams, ER diagrams) to formalize the proposed information system architecture. The authors frame AI as a decision-support tool within a physician-in-the-loop paradigm (pp. 77–79, 83–85).
- **Methods used:** (1) Comparative analysis of existing AI systems in ophthalmology (IDx-DR, Eyenuk, DeepMind, Retina-AI Health, Visulytix Pegasus, ZEISS VISUHEALTH, NVIDIA Clara AI, Orbis Cybersight AI, Heidelberg AI Tools); (2) System architecture design using UML diagrams; (3) Definition and specification of Data Management Platform (DMP) components; (4) Conceptual framework design for telemedicine integration (pp. 80–88).
- **Data sources:** No primary experimental dataset is used. The paper relies on published literature, specifications of existing AI systems, and Kazakhstan-specific epidemiological statistics (IDF Diabetes Atlas, 2021). Figures on diabetes prevalence (~8% of adult population) and rural population (~40%) are cited to justify the system's deployment context (pp. 86–87).
- **Analytical approach:** Qualitative comparative analysis of existing AI ophthalmology systems (Table 1, pp. 80–81); tabular decomposition of system components (Tables 2–4, pp. 82–86); conceptual benefit analysis (Table 5, p. 89). No quantitative experiments, statistical tests, or model training/evaluation are conducted in this paper.

### II.4 Conceptual Contributions

- **Modular AI-driven diagnostic architecture:** The paper proposes a multi-component system architecture consisting of: Image Capture, Image Processing, Recognition Model, Diagnosis, Reporting, User Interface, Data Storage, and Error Handling components (Fig. 1, p. 83). The architecture is designed as modular and scalable, adaptable to various clinical contexts.
- **Physician-in-the-loop paradigm:** The paper explicitly frames the doctor not merely as a consumer of AI outputs but as a "tuner" and auditor of AI systems, who must interpret results and adjust AI algorithms when necessary (p. 79).
- **Doctor-AI Feedback Loop:** Defined as a mechanism where, after receiving analysis results, the doctor can request further clarification or corrections from the AI model, enabling verification and adjustment (p. 85).
- **Sequential workflow for AI implementation in eye institutes:** A seven-stage process: Data Collection → Data Processing → Model Development → Model Testing → Integration → Training & Monitoring → Function Expansion → Effectiveness Evaluation (Fig. 4, p. 87).
- **Data Management Platform (DMP) taxonomy for healthcare:** Seven key concepts defined: Data Storage, Data Integration, Real-Time Processing, Scalability, Data Security, Interoperability, AI Integration, each mapped to specific technologies (Table 4, p. 86).
- **ER model for AI-driven telemedicine system:** Eight entities defined: Patient, Medical Record, Doctor, Appointment, Telemedicine Session, AI Model, Diagnostic Result, Device (Fig. 5, p. 88).

### II.5 Empirical Contributions

This paper does not present original empirical experiments, model training results, or quantitative validation data. The contributions are architectural and conceptual. However, the paper cites the following quantitative claims from external sources:

- AI algorithms (IDx-DR, EyeArt) have demonstrated sensitivity up to 96% and specificity of 93% in identifying referable DR cases (p. 87, citing external sources).
- UK telemedicine DR screening achieved 80% coverage among diabetic patients (p. 87).
- Portable diagnostic devices (e.g., Fundus on Phone) cost approximately $5,000 (p. 87).
- Remote monitoring could reduce in-person visits by 30–50% (p. 87).
- Potential outcomes for Kazakhstan: access for 4+ million rural residents; 20–30% reduction in late-stage DR complications; 15–20% healthcare cost reduction (p. 88).

These are projections and external benchmarks, not results of experiments conducted in this study.

### II.6 Limitations Acknowledged by the Author

The authors acknowledge the following limitations and challenges:
- Successful adoption of AI systems in Kazakhstan requires investments in diagnostic equipment and infrastructure (p. 81).
- Adaptation of algorithms to local data and conditions is necessary (p. 81).
- Development of national standards and specialist training is required (p. 81).
- The conclusion states that addressing infrastructure limitations and personnel training is essential for effective implementation (p. 90).
- Remote monitoring systems are dependent on internet connectivity (Table 1, p. 81, regarding Orbis Cybersight AI).

No limitations are acknowledged regarding the absence of empirical validation of the proposed architecture, the lack of quantitative testing, or the preliminary nature of the design.

### II.7 Implicit Assumptions

- **The proposed architecture can function effectively without primary experimental validation.** Justification: The paper presents a fully specified system architecture with detailed UML diagrams and component specifications but does not report any prototype implementation or testing. The benefits are stated as achievable outcomes rather than demonstrated results (pp. 85–90).
- **Kazakhstan's healthcare infrastructure can support cloud-based AI systems.** Justification: The architecture relies on cloud platforms, PACS servers, and internet connectivity (Fig. 3, p. 84), yet the paper acknowledges that infrastructure limitations exist without addressing how they would be specifically overcome.
- **Published performance metrics of existing AI systems (e.g., IDx-DR sensitivity of 96%) are transferable to the Kazakhstan context.** Justification: These figures are cited as evidence for the proposed system's potential without discussing dataset differences, population-specific validation, or regulatory approval requirements specific to Kazakhstan (p. 87).

---

## III. EXTRACTION BLOCKS

---

**[Extraction Block ID: EB-01]**

**Relevant to:**
- Dissertation Claim(s): DC-6, DC-7
- Dissertation Chapter/Section(s): Chapter 1, Section 1.4 (Critical Analysis of Existing Automated DR Screening Systems); Chapter 6, Section 6.1
- Concept(s) used: Comparative analysis of AI systems in ophthalmology
- Research question addressed: What are the strengths and limitations of existing AI-based DR screening systems?

**Function in Dissertation:**
- **Comparative benchmark** — Provides a structured comparison of nine existing AI systems in ophthalmology, documenting their primary focus, key features, strengths, and limitations.

**Extracted Content:**
- IDx-DR: FDA-approved, analyzes retinal images for diabetic retinopathy detection; high accuracy with no specialist required; limited to diabetic retinopathy only (Table 1, p. 80).
- Eyenuk: AI for diabetic retinopathy, macular edema, and AMD; comprehensive multi-disease analysis; requires high-quality imaging data (Table 1, p. 80).
- DeepMind: Analyzes OCT scans for glaucoma and macular degeneration; accurate and widely validated; requires advanced imaging equipment (Table 1, p. 81).
- Visulytix Pegasus: Multi-disease detection (glaucoma, DR, AMD) in a single platform; limited adoption in non-English-speaking regions (Table 1, p. 81).
- NVIDIA Clara AI: Customizable tools for building institutional AI solutions for ophthalmology; requires technical expertise (Table 1, p. 81).
- Orbis Cybersight AI: Cloud-based screening for underserved regions; enables accessibility in low-resource settings; dependent on internet connectivity (Table 1, p. 81).
- Heidelberg AI Tools: Ultra-high-resolution imaging focus; excellent for research; expensive and not suited for general clinical use (Table 1, p. 81).

**Strength of Relevance:** **Supporting** — This comparative table provides contextual benchmarks for the dissertation's own system but does not include quantitative performance comparison data from primary experiments.

---

**[Extraction Block ID: EB-02]**

**Relevant to:**
- Dissertation Claim(s): DC-7, DC-10
- Dissertation Chapter/Section(s): Chapter 6, Sections 6.1 and 6.2; Chapter 1, Section 1.4
- Concept(s) used: Modular AI-driven diagnostic architecture; information system components
- Research question addressed: How should an AI-integrated healthcare information system be architecturally structured?

**Function in Dissertation:**
- **Technical specification reference** — Defines the component architecture of the proposed medical image recognition and diagnostic system.

**Extracted Content:**
- The system architecture comprises the following components: Medical Equipment, Medical Database, AI Image Recognition Models, Image Processing (Image Processor), Recognition Algorithms, Report Generation System, User Interface (UI), Security System, and Doctor (Table 2, p. 82).
- Extended component specifications include: Scanners (CT, MRI, X-ray, Ultrasound), PACS, Cloud Services, EHR, AI Models (Deep Learning), Image Processing Algorithms, Clinical Decision Support Systems (CDSS), Security Systems, User Interface, and Data Analytics and Reporting Tools (Table 3, pp. 82–83).
- AI Models use neural networks, convolutional layers (CNNs), and other machine learning techniques (Table 3, p. 83).
- CDSS uses patient data and medical history to provide clinical recommendations (Table 3, p. 83).
- Security systems include encryption, user authentication, and secure communication protocols for HIPAA compliance (Table 3, p. 83).
- The general system structure is represented as a UML component diagram with flows: Image Capture → Image Processing → Recognition Model → Diagnosis → Reporting → User Interface, with parallel Data Storage and Error Handling components (Fig. 1, p. 83).

**Strength of Relevance:** **Core** — This directly provides the architectural foundation described in Chapter 6 of the dissertation. Since this is the dissertant's own publication, this material constitutes the primary architectural contribution referenced in the dissertation.

---

**[Extraction Block ID: EB-03]**

**Relevant to:**
- Dissertation Claim(s): DC-8, DC-7
- Dissertation Chapter/Section(s): Chapter 6, Section 6.3 (Clinical Workflow Integration, Telemedicine and Portable Device Support)
- Concept(s) used: Telemedicine; portable diagnostic devices; rural healthcare accessibility
- Research question addressed: How can AI-driven diagnostic systems be deployed in rural/underserved areas?

**Function in Dissertation:**
- **Empirical support** (indirect, based on external data) — Provides quantitative projections for telemedicine and portable device deployment in Kazakhstan.

**Extracted Content:**
- Telemedicine: The UK's DR screening initiative achieved 80% screening coverage among diabetic patients and reduced blindness rates in the working-age population for the first time in 50 years (p. 87).
- Kazakhstan could screen up to 2 million individuals annually in rural and underserved areas through mobile diagnostic units with fundus cameras (p. 87).
- AI algorithms (IDx-DR, EyeArt) demonstrated sensitivity up to 96% and specificity of 93% for referable DR (p. 87).
- Only about 1,200 ophthalmologists serve Kazakhstan's entire population (p. 87).
- Portable retinal cameras such as Fundus on Phone cost approximately $5,000 and could replace traditional tabletop setups (p. 87).
- Approximately 70% of rural Kazakhstan residents have limited access to eye care (p. 87).
- Home-based monitoring (OCT devices) could reduce in-person visits by 30–50% (p. 87).
- Projected outcomes: access to retinal care for 4+ million rural residents; 20–30% reduction in late-stage DR complications; 15–20% healthcare cost reduction (p. 88).

**Strength of Relevance:** **Supporting** — Provides contextual and statistical justification for the deployment scenario described in Chapter 6, though these are projections rather than results from the dissertation's own experiments.

---

**[Extraction Block ID: EB-04]**

**Relevant to:**
- Dissertation Claim(s): DC-9
- Dissertation Chapter/Section(s): Chapter 6, Section 6.4 (Data Security and Regulatory Compliance Framework)
- Concept(s) used: Data security; GDPR; HIPAA; patient data confidentiality
- Research question addressed: What data security and regulatory compliance considerations apply to AI healthcare systems?

**Function in Dissertation:**
- **Technical specification reference** — Establishes the compliance framework requirements for the proposed system.

**Extracted Content:**
- The system meets international standards for data security and confidentiality (p. 74).
- Security systems include encryption, user authentication, and secure communication protocols to comply with regulations like HIPAA (Table 3, p. 83).
- Data security is defined as ensuring compliance with data protection regulations and safeguarding patient data, using encryption and anonymization tools (Table 4, p. 86).
- The Security Gateway ensures secure data transfer between system components (p. 85, Fig. 3, p. 84).
- The conclusion states the system is GDPR and HIPAA-compliant (p. 90).

**Strength of Relevance:** **Supporting** — Provides the regulatory compliance framing for Chapter 6 but at a conceptual level without implementation details or compliance testing.

---

**[Extraction Block ID: EB-05]**

**Relevant to:**
- Dissertation Claim(s): DC-6, DC-7
- Dissertation Chapter/Section(s): Chapter 1, Sections 1.3, 1.4; Chapter 6, Section 6.2
- Concept(s) used: AI in medical imaging; physician-AI collaboration; clinical decision support
- Research question addressed: What is the current state of AI integration in medical diagnostic systems?

**Function in Dissertation:**
- **Theoretical grounding** — Provides a literature-based overview of AI applications in healthcare and frames the physician-in-the-loop paradigm.

**Extracted Content:**
- AI does not replace the physician but serves as a powerful tool to assist in their work (p. 78).
- With the development of AI technologies, a new role for doctors is emerging as "tuner" and auditor of AI systems; the doctor must not only interpret results but also adjust AI algorithms (p. 79).
- The Doctor-AI Feedback Loop allows the doctor to request further clarification or corrections from the AI model after receiving analysis results (p. 85).
- AI adoption faces challenges including data privacy concerns, algorithmic biases, and the need for interpretability and regulatory compliance (p. 78, citing Beronius et al., 2022).
- Most AI systems in healthcare support decision-making rather than act autonomously (p. 79, citing Sharma et al., 2022).
- AI's significance in medical imaging was especially evident during COVID-19, accelerating responses to medical challenges (p. 79, citing Pallavi et al., 2022).

**Strength of Relevance:** **Peripheral** — Provides background context and conceptual framing for the dissertation's literature review, but the claims are synthesized from secondary sources rather than original analysis.

---

**[Extraction Block ID: EB-06]**

**Relevant to:**
- Dissertation Claim(s): DC-10
- Dissertation Chapter/Section(s): Chapter 6, Section 6.1.2 (Modular Architecture with PACS and EHR Integration)
- Concept(s) used: Data Management Platforms; interoperability; FHIR/HL7 standards
- Research question addressed: What data management infrastructure supports AI-driven healthcare systems?

**Function in Dissertation:**
- **Technical specification reference** — Defines the DMP taxonomy and associated technologies for the proposed system.

**Extracted Content:**
- Key DMP functions in healthcare: Data Storage, Data Integration, Real-Time Data Processing, Scalability (pp. 85–86).
- Data Integration involves unifying disparate sources such as HIS, wearable devices, and telemedicine platforms (p. 86).
- Interoperability is defined as facilitating seamless data exchange using standards like FHIR and HL7 (Table 4, p. 86).
- Key technologies: NoSQL, Hadoop, Relational Databases (storage); ETL Tools, Apache Kafka, MuleSoft (integration); Apache Spark, Stream Processing Frameworks (real-time); TensorFlow, PyTorch, Pre-Trained Models (AI integration) (Table 4, p. 86).
- The ER model defines eight entities: Patient, Medical Record, Doctor, Appointment, Telemedicine Session, AI Model, Diagnostic Result, Device (Fig. 5, p. 88).

**Strength of Relevance:** **Core** — Directly provides the data management and integration specifications referenced in Chapter 6, Sections 6.1–6.2. As the dissertant's own publication, this is a primary source for the system design chapter.

---

## IV. RELATIONAL POSITIONING

### IV.1 Supports Which Dissertation Claims

- **DC-6:** Partially supports. The comparative analysis (Table 1) documents limitations of existing systems (IDx-DR limited to DR only; DeepMind requires advanced equipment; Orbis dependent on connectivity), providing evidence that existing systems have addressable gaps. However, the source does not demonstrate how the dissertant's proposed preprocessing-CNN pipeline specifically addresses these gaps.
- **DC-7:** Directly supports. The entire paper is dedicated to proposing and specifying an AI-driven information system architecture tailored to Kazakhstan's healthcare infrastructure, including ophthalmological screening.
- **DC-8:** Directly supports. Provides data on telemedicine efficacy, portable device costs, and rural healthcare gaps in Kazakhstan to justify the deployment of DR screening in underserved areas.
- **DC-9:** Supports. Establishes GDPR/HIPAA compliance as a design requirement and includes security components (encryption, authentication, security gateway) in the architecture.
- **DC-10:** Directly supports. The modular, scalable architecture design is the central contribution of this paper, demonstrable through the component diagrams, ER model, and DMP specifications.

### IV.2 Contradicts Which Dissertation Claims

No contradictions identified. However, there is a notable **gap**: the paper does not provide any empirical validation of the proposed architecture (no prototype, no testing metrics), which means it cannot serve as evidence for claims requiring experimental demonstration (DC-1 through DC-4).

### IV.3 Extends Which Conceptual Axis

This source extends the **system architecture and clinical deployment axis** of the dissertation (primarily Chapter 6). It provides the information system design layer that complements the CNN diagnostic pipeline (Chapters 2–5) by specifying how the diagnostic model would operate within a full healthcare IT ecosystem including PACS, EHR, cloud storage, telemedicine, and security infrastructure.

### IV.4 Overlaps With Which Other Sources

Based on the source's own reference list:
- Pallavi et al. (2022) — AI applications in healthcare, clinical decision support
- Sharma et al. (2022) — AI implementation in healthcare, decision-making support
- Beronius et al. (2022) — AI challenges (data privacy, bias, interpretability)
- Jiang et al. (2017) — AI in healthcare past/present/future
- Quazi et al. (2022) — AI applications, ML and NLP in healthcare
- Chernobrivtseva & Misyurin (2022) — Machine learning in medical imaging for cancer diagnosis
- Matsuo et al. (2024) — Point-of-Care Diagnostics

The IDx-DR, Eyenuk, and DeepMind system descriptions overlap with content likely present in other dissertation sources covering automated DR screening systems (relevant to Section 1.4 and Chapter 5, Section 5.3).

---

## V. REUSABILITY CONTROL

### V.1 What Can Be Reused in Dissertation Drafting

- Comparative table of AI systems in ophthalmology (Table 1, pp. 80–81) — reusable with proper self-citation in Section 1.4.
- System component specifications (Tables 2–4, pp. 82–86) — reusable as the basis for Chapter 6 architecture description.
- UML diagrams (Figs. 1–5) — reusable or adaptable for Chapter 6 with proper cross-referencing.
- ER model entities and relationships (Fig. 5, p. 88) — directly reusable in Section 6.1.
- Kazakhstan-specific statistics (ophthalmologist count, rural population percentage, diabetes prevalence) — reusable as contextual data in Sections 1.1.2 and 6.3.1.
- DMP taxonomy and technology mappings (Table 4, p. 86) — reusable in Section 6.1.

### V.2 What Must Be Reformulated

- Literature review content (pp. 77–80) synthesizing external sources (Jiang et al., Shaheen, Rich & Winston, etc.) must be independently re-engaged with original sources rather than cited through this paper.
- Projected outcomes for Kazakhstan (pp. 87–88) should be presented as projections, not established results.
- The claim that the system "meets international standards" (p. 74) must be qualified in the dissertation, as no compliance testing or certification is documented.
- Benefit claims (Table 5, p. 89) must be reformulated as design goals rather than validated outcomes.

### V.3 Risk of Self-Plagiarism

**⚠️ HIGH RISK — This is the dissertant's own publication (Yesmukhamedov N.S. is the first author).**

Specific overlap areas requiring careful demarcation:

1. **Chapter 6 (Architecture of an Automated DR Screening System):** The system architecture presented in this paper (Figs. 1–5, Tables 2–5) constitutes the primary content that will also appear in Chapter 6 of the dissertation. The dissertant must:
   - Clearly cite this publication as the source of the architecture.
   - Expand and deepen the architectural description in the dissertation beyond what is presented in this 18-page paper.
   - Add implementation details, prototype results, or validation data not present in this paper to demonstrate that the dissertation contribution goes beyond the published work.

2. **Section 1.4 (Critical Analysis of Existing Automated DR Screening Systems):** The comparative analysis (Table 1) will likely appear in a similar form. The dissertation should extend this comparison with additional systems and/or deeper analysis.

3. **Section 6.3 (Clinical Workflow Integration):** The telemedicine and portable device discussion (pp. 87–88) overlaps with Section 6.3. The dissertation should incorporate primary data or more detailed implementation specifications.

4. **Literature review content (pp. 77–80):** The secondary source synthesis overlaps with Chapter 1 literature review. The dissertation must independently engage with original sources.

**Recommendation:** The dissertant should include an explicit statement in the dissertation that this paper represents a preliminary publication of the system architecture developed during the doctoral research, and should clearly delineate which elements are expanded, refined, or newly contributed in the dissertation text versus the published paper.

---

## VI. TERMINOLOGY INDEX

| Term | Definition/Usage in Source | Page Reference | Stability Note |
|---|---|---|---|
| PACS (Picture Archiving and Communication System) | System for storing, retrieving, and sharing medical images within a healthcare network | p. 78, Table 3 (p. 82) | Standard term; used consistently in medical imaging literature. Must be consistent across dissertation. |
| EHR (Electronic Health Records) | Stores comprehensive patient medical information including images, diagnoses, and treatment history | p. 78, Table 3 (p. 82) | Standard term. Note: the paper uses both "EHR" and "EMR" (Electronic Medical Records) — the dissertation should standardize on one. |
| EMR (Electronic Medical Records) | Used in the abstract; appears to be used interchangeably with EHR | p. 74 | **Terminological conflict:** EMR and EHR have distinct meanings in some frameworks (EMR = facility-level; EHR = cross-institutional). The dissertation should define and distinguish. |
| DMP (Data Management Platform) | Backbone infrastructure enabling storage, retrieval, and processing of healthcare data | pp. 85–86 | Not a universally standard healthcare IT term; the dissertation should define it explicitly if adopted. |
| CDSS (Clinical Decision Support Systems) | AI-driven suggestions based on medical data and analysis to improve decision-making | Table 3, p. 83 | Standard term in health informatics. |
| Doctor-AI Feedback Loop | Mechanism where the doctor requests clarification/corrections from the AI model after analysis | p. 85 | Coined/defined in this paper. Since this is the dissertant's own term, it should be used consistently and defined once in the dissertation. |
| FHIR (Fast Healthcare Interoperability Resources) | Standard facilitating seamless data exchange between different healthcare systems | Table 4, p. 86 | International standard (HL7). Must be consistent. |
| Interoperability | Facilitating seamless data exchange between different systems using standards like FHIR | Table 4, p. 86 | Standard health informatics concept. |
| Modular architecture | System design allowing adaptation to various clinical contexts through independent, replaceable components | pp. 74–75, 90 | Core concept of this paper and the dissertation's Chapter 6. |
