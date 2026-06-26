---
name: eyepacs-local-dataset
description: Local EyePACS on E:\datasets is the FULL 88,702-image set; test labels added 2026-06-26 (testLabels15.csv)
metadata:
  type: project
---

`E:\datasets\EyePACS` already holds the **complete** Kaggle Diabetic Retinopathy
Detection set, not just the 35k train split:

- `train/` — 35,126 .jpeg, labeled by `trainLabels.csv` (cols `image,level`)
- `test/`  — 53,576 .jpeg (53.8 GB), all valid (0 zero-byte) — **= 88,702 total**
- `sample/` — 10 .jpeg

The "only 35k" impression comes from labels, not images: the competition ships
`trainLabels.csv` (35,126 rows) only. The test images were always present but unlabeled.

**2026-06-26:** added `E:\datasets\EyePACS\testLabels15.csv` — the official 2015 test
labels (53,576 rows; cols `image,level,Usage`; `Usage` = Public 10,906 / Private 42,670).
Verified 1:1 against `test/` basenames (0 mismatches). Level dist: 0=39533, 1=3762,
2=7861, 3=1214, 4=1206. Source: Kaggle dataset
`benjaminwarner/resized-2015-2019-blindness-detection-images`, file `labels/testLabels15.csv`
(its `trainLabels15.csv` is byte-identical, 465317 B, to our `trainLabels.csv` — confirms
canonical competition labels). The competition's own file list has NO test-labels file.

Leftover redundant split-zip parts (`train.zip.002-005`, `test.zip.002-007`, 10 files
~66.6 GB) remain on disk — already extracted, and incomplete anyway (no `.001` parts),
so re-extraction is impossible. Candidate for deletion to reclaim space; left in place
(user opted to download labels only). Governance still scopes Exp 1 to EyePACS ~35,126
(train) — see [[config-d-kaggle-source]].
