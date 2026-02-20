# TABLE OF CONTENT

- NORMATIVE REFERENCES  
- DEFINITIONS  
- DESIGNATIONS AND ABBREVIATIONS  

# INTRODUCTION

- Relevance of the Research  
- Scientific Novelty  
- Research Goal  
- Research Objectives  
- Object and Subject of Research  
- Research Hypothesis  
- Methodological Basis  
- Provisions Submitted for Defense  
- Theoretical Significance  
- Practical Significance  
- Approbation of Research Results  
- Publications  

---

# 1 PROBLEM DOMAIN ANALYSIS AND CURRENT STATE OF AUTOMATED DIABETIC RETINOPATHY DIAGNOSIS

## 1.1 Medical and Epidemiological Context of Diabetic Retinopathy
- 1.1.1 Pathophysiology and Clinical Grading Systems  
- 1.1.2 Screening Requirements in Resource-Limited Healthcare Settings  

## 1.2 Fundus Image Acquisition and Quality Variability
- 1.2.1 Sources of Image Degradation in Clinical Practice  
- 1.2.2 Impact of Image Quality on Diagnostic Model Performance  

## 1.3 Deep Learning Approaches to Retinal Image Classification
- 1.3.1 Convolutional Neural Network Architectures for Medical Imaging  
- 1.3.2 Transformer and Hybrid Architectures  
- 1.3.3 Transfer Learning Strategies in Ophthalmic Diagnostics  
- 1.3.4 Global Benchmarking and Clinical-Scale Validation  

## 1.4 Evidence Synthesis and Critical Analysis of Existing Automated DR Screening Systems
- 1.4.1 Comparative Performance Across Datasets and Model Families  
- 1.4.2 Meta-Analytic Evidence on Diagnostic Accuracy and Generalization  
- 1.4.3 Methodological Gaps: Preprocessing Underrepresentation and Confounded Ablation  

## 1.5 Formulation of the Research Problem and Justification of Research Direction  

- Conclusions to Chapter 1  

---

# 2 THEORETICAL FOUNDATIONS OF IMAGE PREPROCESSING AND DEEP LEARNING FOR FUNDUS IMAGE ANALYSIS

## 2.1 Mathematical Foundations of Image Enhancement Techniques
- 2.1.1 Histogram Equalization and Adaptive Contrast Enhancement  
- 2.1.2 Formalization of CLAHE with Controllable Threshold Parameters  
- 2.1.3 Spatial Filtering and Noise Reduction Methods  

## 2.2 Theoretical Framework of Convolutional Neural Networks
- 2.2.1 Convolution, Pooling, and Feature Extraction Operations  
- 2.2.2 Loss Functions and Optimization for Imbalanced Medical Datasets  
- 2.2.3 Regularization Techniques: Dropout, Batch Normalization, and Data Augmentation  

## 2.3 Transfer Learning Theory and Domain Adaptation
- 2.3.1 Feature Transferability Across Visual Domains  
- 2.3.2 Frozen-Layer versus Progressive Fine-Tuning Strategies  

## 2.4 Mathematical Modeling of Laser-Tissue Interaction in Retinal Therapy
- 2.4.1 Coupled Thermal-Optical Model of Fundus Tissue Response  
- 2.4.2 Implications for Diagnostic Image Feature Interpretation  

- Conclusions to Chapter 2  

---

# 3 METHODOLOGY OF INTEGRATED PREPROCESSING-CNN PIPELINE DESIGN

## 3.1 Formalization of the Unified Preprocessing Pipeline
- 3.1.1 Pipeline Stage Specification: Resizing, Normalization, Enhancement, Augmentation  
- 3.1.2 Modified CLAHE Algorithm with Simplified Threshold Control  
- 3.1.3 Augmentation Strategy for Class Imbalance Mitigation  

## 3.2 Design of Baseline and Enhanced CNN Architectures
- 3.2.1 Shallow Baseline CNN for Preprocessing Quality Validation  
- 3.2.2 Enhanced Multi-Block CNN with Regularization Layers  

## 3.3 Transfer Learning Methodology Using EfficientNetB0 and ResNet50
- 3.3.1 Architecture Adaptation for Five-Class DR Classification  
- 3.3.2 Two-Stage Fine-Tuning Protocol Design  
- 3.3.3 Weighted Loss Function Formulation for Ordinal Class Structure  

## 3.4 Evaluation Framework and Performance Metrics
- 3.4.1 Multi-Metric Assessment: Accuracy, F1-Score, ROC-AUC, Cohen’s Kappa  
- 3.4.2 Cross-Validation and Statistical Reliability Protocols  

- Conclusions to Chapter 3  

---

# 4 EXPERIMENTAL RESEARCH: PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

## 4.1 Datasets and Experimental Configuration
- 4.1.1 APTOS 2019, STARE, and Supplementary Clinical Image Corpora  
- 4.1.2 Class Distribution Analysis and Data Partitioning Strategy  
- 4.1.3 Hardware Constraints and Computational Resource Limitations  

## 4.2 Experiment 1: Baseline CNN without Preprocessing versus Enhanced CNN
- 4.2.1 Training Dynamics and Convergence Analysis  
- 4.2.2 Quantitative Comparison of Diagnostic Metrics  

## 4.3 Experiment 2: Modified CLAHE Threshold Optimization on Small Datasets
- 4.3.1 Threshold Parameter Sensitivity Analysis  
- 4.3.2 Impact on Feature Preservation in Microaneurysms and Small Vessels  

## 4.4 Experiment 3: Transfer Learning Strategy Comparison
- 4.4.1 EfficientNetB0: Frozen versus Progressive Fine-Tuning  
- 4.4.2 ResNet50: Feature Extraction versus End-to-End Fine-Tuning  
- 4.4.3 Per-Class Performance Analysis under Severe Class Imbalance  

- Conclusions to Chapter 4  

---

# 5 RELIABILITY VALIDATION AND COMPARATIVE ANALYSIS

## 5.1 Cross-Database Generalization Testing
- 5.1.1 Model Transferability Across Heterogeneous Image Sources  
- 5.1.2 Stability Assessment under Varying Image Quality Conditions  

## 5.2 Statistical Validation of Preprocessing Dominance Hypothesis
- 5.2.1 Ablation Study: Preprocessing Components versus Architectural Complexity  
- 5.2.2 Quantitative Evidence for Image Quality as Primary Performance Driver  

## 5.3 Comparative Analysis with Existing DR Diagnostic Systems
- 5.3.1 Benchmarking Against Published Results: IDx-DR, EyeNuk, DeepMind  
- 5.3.2 Performance-Complexity Trade-Off Analysis  

## 5.4 Limitations and Boundary Conditions of the Proposed Approach  

- Conclusions to Chapter 5  

---

# 6 ARCHITECTURE OF AN AUTOMATED DR SCREENING SYSTEM FOR RESOURCE-LIMITED ENVIRONMENTS

## 6.1 System Requirements and Design Principles
- 6.1.1 Functional and Non-Functional Requirements Specification  
- 6.1.2 Modular Architecture with PACS and EHR Integration  

## 6.2 AI Processing Module Design
- 6.2.1 Preprocessing Engine with Configurable Pipeline Parameters  
- 6.2.2 Inference Module with Model Selection Logic  

## 6.3 Clinical Workflow Integration
- 6.3.1 Telemedicine and Portable Device Support for Rural Deployment  
  - 6.3.1.1 Deployment in distributed telemedicine systems  
  - 6.3.1.2 Integration with national eHealth platforms  
  - 6.3.1.3 Real-time remote DR screening in low-resource regions  
- 6.3.2 Physician-in-the-Loop Decision Support Interface  

## 6.4 Data Security and Regulatory Compliance Framework
- 6.4.1 GDPR/HIPAA-Aligned Data Management Protocols  
- 6.4.2 Applicability to Kazakhstan Healthcare Infrastructure  

- Conclusions to Chapter 6  

---

# CONCLUSION  

# REFERENCES  

# APPENDICES

- Appendix A — Source Code of the Preprocessing Pipeline  
- Appendix B — Supplementary Experimental Results and Confusion Matrices  
- Appendix C — System Architecture UML Diagrams  
- Appendix D — Certificates of Implementation and Approbation Acts  