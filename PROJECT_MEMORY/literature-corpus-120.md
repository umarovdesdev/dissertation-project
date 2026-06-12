---
name: literature-corpus-120
description: "Literature corpus expanded to 120 active sources (LITERATURE_INDEX v6.1.0, 2026-06-12)"
metadata:
  type: project
---

On 2026-06-12 the literature corpus was expanded from **81 → 120 active sources** (LITERATURE_INDEX
bumped v6.0.0 → **v6.1.0**). Two work-streams:

**(a) Missing-card fills from the candidate's `litres` PDF batch** (`C:\Users\yesmu\Downloads\litres`).
Five PDFs were checked against LITERATURE_INDEX: three matched existing index entries that lacked card
files and were written — **#46 Grad-CAM (Selvaraju 2017, ICCV), #47 EyePACS (Cuadros & Bresnick 2009,
J Diabetes Sci Technol 3(3):509–516), #48 Messidor (Decencière 2014, Image Anal Stereol 33(3):231–234)**.
One PDF was a genuinely relevant DR paper but NOT a missing index entry → added as new **#83 FGADR
(Zhou et al. 2020, IEEE TMI)**. One PDF (`2003.10792v1.pdf`) was **off-topic** (Sumpter & Van Loo,
astrophysics/MNRAS) — rejected, no card.

**(b) 38 web-sourced additions (#84–#121)** targeting the index's flagged gaps/THIN sections, all
verified via web search before carding:
- Ophthalmology/medical SSL & foundation models (resolves §2.3.3 + §3.3.2 gaps): #84 RETFound,
  #85 MICLe, #86 SimCLR, #87 MoCo, #88 BYOL, #89 DINO, #90 MAE (RETFound's pretraining basis),
  #91 SimSiam, #92 Shurrab medical-SSL survey.
- Image degradation/quality (resolves §1.2.1 gap; upgrades §2.6): #93 Shen cofe-Net, #94 Zago RIQA,
  #95 Zuiderveld CLAHE (canonical, replaces Wikipedia #25).
- Loss/optim/regularization/augmentation: #96 **Lin Focal Loss (the dissertation's training loss, γ=2)**,
  #97 Cui class-balanced, #98 Buda imbalance, #99 Adam, #100 BatchNorm, #101 Dropout, #102 mixup,
  #103 Shorten aug-survey, #104 RandAugment.
- Architectures: #105 VGG, #106 GoogLeNet, #107 Inception-v3 (backbone of Gulshan #12 + Esteva #121),
  #108 Swin.
- Surveys: #109 Pan & Yang transfer-learning, #110 Litjens medical-DL.
- DR/ophthalmology clinical & empirical: #111 Quellec deep-image-mining, #112 Gargeya & Leng,
  #113 Krause grader-variability, #114 Son multi-finding, #115 Bellemo Africa, #116 Dai DeepDR,
  #117 De Fauw device-independent OCT, #118 Ting review, #119 Beede human-centered, #120 Burlina AMD,
  #121 Esteva skin-cancer (cited as the **P1 end-to-end paradigm foil** to V5).

All cards follow the 18-section format in `thesis/prompts/literature-card-review.md`, in
`thesis/literature/external/`. Index Source Index, Coverage Matrix, Gaps section, and a new
Epistemic-Tier table (#83–#121) were all updated. **Still TODO:** cards for #49 RFMiD, #50 DDR,
#51 ODIR-5K (not in litres). See [[literature-integrity-flags]].
