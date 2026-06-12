---
name: literature-integrity-flags
description: "Known mismatches/gaps in thesis/literature corpus found during Ch1 drafting (2026-06-09)"
metadata:
  type: project
---

Corpus-integrity issues found while drafting Chapter 1 (2026-06-09), flagged not fixed:

1. **FIXED:** `external/schmidt-erfurth-2018.md` actually contained Kusuhara et al. (2018) "Pathophysiology of DR" (DMJ, DOI 10.4093/dmj.2018.0182) — Schmidt-Erfurth was only a paper cited inside it. Renamed → `kusuhara-2018.md`; updated 1.1.1 draft + brief; LITERATURE_INDEX #32 already read "Kusuhara et al. (2018)" so no index edit needed. Zero stale `schmidt-erfurth-2018` refs remain.

2. **OPEN — missing card files:** Dataset-descriptor sources **#47 (EyePACS/Cuadros), #48 (Messidor/Decencière), #49 (RFMiD/Pachade), #50 (DDR/Li-2019), #51 (ODIR-5K)** are LITERATURE_INDEX entries with **no card files** in `external/`. §1.2.3 cited their camera-model facts at index/dataset-attribute level only. #51 ODIR-5K is additionally index-flagged "TO BE IDENTIFIED" (descriptor unconfirmed). Cards should be written before these are cited at full depth (e.g. §4.1, §4.7).

3. **OPEN — self-card ID anomaly:** `self/yesmukhamedov-scopus-q2.md` carries Unique ID `LC-AlTimemy-2021` but its bibliographic-citation line shows the Sapakova/Yesmukhamedov/Sapakov (2025) EEJET paper (DOI 10.15587/1729-4061.2025.335570) — same paper as `scopus-q3.md` (`LC-SAPAKOVA-2025-01`, the real #24). INVARIANTS treats LC-AlTimemy-2021 as a *distinct* STARE/T-80 CLAHE study (100% acc, sensitivity-formula anomaly). Possible mislabel: scopus-q2 may be the AlTimemy card with a wrong citation line, or a duplicate. Verify which paper scopus-q2 actually analyses before citing #23 vs the AlTimemy STARE study in Ch 2/3. See [[strip-version-markers]].

Source-number map confirmed during drafting: #24 = `scopus-q3.md` (LC-SAPAKOVA-2025-01, val-acc 71%→86%, ROC-AUC 0.9638); #22 = `nan-rk.md` (LC-2025-Yesmukhamedov-01, system architecture).
