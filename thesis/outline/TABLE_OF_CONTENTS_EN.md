# TABLE OF CONTENTS

**Version:** 4.0 | **Binding Reference:** INVARIANTS.md v4.0

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
- 1.2.3 Device-Specific Variability in Fundus Imaging  

## 1.3 Deep Learning Approaches to Retinal Image Classification
- 1.3.1 Convolutional Neural Network Architectures for Medical Imaging  
- 1.3.2 Transfer Learning Strategies in Ophthalmic Diagnostics  
- 1.3.3 Explainability Methods in Medical Image Classification  

## 1.4 Critical Analysis of Existing Automated DR Screening Systems

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

## 2.5 Explainability in Deep Learning for Medical Imaging
- 2.5.1 Class Activation Mapping (CAM) and Grad-CAM Mathematical Formulation  
- 2.5.2 Interpretation of Attention Maps in Ophthalmic Context  
- 2.5.3 ALO and IoU as Quantitative Explainability Metrics

## 2.6 Image Quality Metrics for Preprocessing Evaluation

- Conclusions to Chapter 2  

---

# 3 METHODOLOGY OF INTEGRATED PREPROCESSING-CNN PIPELINE DESIGN

## 3.1 Formalization of the Unified Preprocessing Pipeline
- 3.1.1 Pipeline Stage Specification: V4 6-Stage System
- 3.1.2 Modified CLAHE Algorithm with Dual-Constraint Clip Limit
- 3.1.3 Augmentation Strategy for Class Imbalance Mitigation  
- 3.1.4 External Image Ingestion Protocol  

## 3.2 Design of CNN Architectures for DR Classification
- 3.2.1 ResNet-50 and EfficientNet-B3 as Primary Experimental Architectures  
- 3.2.2 Historical v1.0 Architectures (Reference Only)  

## 3.3 Transfer Learning Methodology
- 3.3.1 Architecture Adaptation for Five-Class DR Classification  
- 3.3.2 Two-Stage Fine-Tuning Protocol Design  
- 3.3.3 Weighted Loss Function Formulation for Ordinal Class Structure  

## 3.4 Evaluation Framework and Performance Metrics
- 3.4.1 Multi-Metric Assessment Framework  
- 3.4.2 Cross-Validation and Statistical Reliability Protocols  

- Conclusions to Chapter 3  

---

# 4 EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

## 4.1 Datasets and Experimental Configuration
- 4.1.1 Dataset Architecture V4
- 4.1.2 Class Distribution Analysis and Data Partitioning Strategy  
- 4.1.3 Hardware Specification and Reproducibility Protocol  

## 4.2 Experiment 1: Causal Improvement — Preprocessing vs. Architecture on EyePACS
- 4.2.1 Factorial Design (6 Configurations A–F)
- 4.2.2 Training Dynamics and Convergence Analysis  
- 4.2.3 Quantitative Comparison of Diagnostic Metrics  

## 4.3 Experiment 2: Preprocessing Component Ablation on EyePACS
- 4.3.1 V4 Ablation Design (Levels 0–4)
- 4.3.2 CLAHE Threshold Sensitivity Analysis (H-2 Sub-Analysis)  
- 4.3.3 Impact on Feature Preservation in Microaneurysms and Small Vessels  

## 4.4 Experiment 3: Cross-Dataset Generalization and Device Domain Shift
- 4.4.1 Cross-Database Transferability Without Retraining
- 4.4.2 Device Domain Shift — Cross-Camera Evaluation
- 4.4.3 Generalization Ratio and Cross-Device Performance Matrix

## 4.5 Experiment 4: Explainability Analysis via Grad-CAM
- 4.5.1 Grad-CAM Generation Protocol
- 4.5.2 Quantitative ALO and IoU with IDRiD Lesion Masks
- 4.5.3 Attention Consistency Across Datasets

- Conclusions to Chapter 4

---

# 5 RELIABILITY VALIDATION AND COMPARATIVE ANALYSIS

## 5.1 Explainability Results

## 5.2 Statistical Validation
- 5.2.1 Bootstrap Confidence Intervals and Mixed-Effects Model
- 5.2.2 Final Claim Strength Classifications

## 5.3 Comparative Analysis with Published Systems
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
- Appendix E — Grad-CAM Visualization Gallery  
- Appendix F — Device Domain Shift Supplementary Tables  
