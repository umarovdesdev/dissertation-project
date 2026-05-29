# Қорғау презентациясы — Слайд жоспары

**Диссертация:** Компьютерлік өңдеу жүйесі және көз түбі деректерін талдаумен диабеттік ретинопатияны емдеу кезіндегі лазерлік коагуляцияны қолдау
**Ізденуші:** Есмұхамедов Н.С.

---

## Слайдтар тізімі (47 слайд)

### I. Титул (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 01 | 01_TITLE.md | Титул |

### II. Өзектілік және ғылыми мәселе (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 02 | 02_RELEVANCE.md | Зерттеудің өзектілігі және ғылыми мәселе |

### III. Мақсат, міндеттер, гипотезалар (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 03 | 03_AIM_OBJECTIVES.md | Мақсат, міндеттер, гипотезалар |

### IV. Әдебиет шолуы және теориялық негіз (2 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 04 | 04_LITERATURE_REVIEW.md | Әдебиет шолуы және теориялық негіздеме |
| 04a | 05a_PARADIGMATIC_POSITIONING.md | **Парадигмалық позиционирование: P1 vs P2** (қосылған) |

### V. Әдіснама (Methodology) (21 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 05 | 05_SECTION_METHODOLOGY.md | **Әдіснама (Methodology)** |
| 06 | 06_SYSTEM_ARCHITECTURE.md | Жүйенің жалпы архитектурасы |
| 07 | 07_CNN_ARCHITECTURE.md | CNN моделінің архитектурасы |
| 08 | 08_ARCHITECTURE_COMPARISON.md | Архитектураларды салыстыру: ResNet-50 vs EfficientNet-B3 |
| 09 | 09_TRAINING_PARAMS.md | Оқыту параметрлері: Focal Loss, optimizer, 5-fold CV |
| 10 | 10_PREPROCESS_INPUT.md | Препроцессинг кезеңдері: Input |
| 11 | 11_PREPROCESS_CANONICAL_FLIP.md | Каноникалық айналым (canonical flip) |
| 12 | 12_PREPROCESS_FOVEA_OD_ROTATION.md | Fovea және OD арқылы бұру (rotation by midpoint) |
| 13 | 13_PREPROCESS_CROP_RESIZE.md | Кесу және өлшемге келтіру (crop & resize) |
| 14 | 14_PREPROCESS_FOV_MASK.md | Көру өрісі маскасы (FOV mask) |
| 15 | 15_PREPROCESS_FLATFIELD.md | Жарықтандыруды теңестіру (flat-field correction) |
| 16 | 16_PREPROCESS_CLAHE_VESSEL.md | CLAHE — қан тамыр негіздемесі (vessel) |
| 17 | 17_PREPROCESS_CLAHE_POLAR.md | CLAHE — полярлық координаттар (polar) |
| 18 | 18_PREPROCESS_CLAHE_SV2.md | CLAHE — SV2 нұсқасы |
| 19 | 19_PREPROCESS_AUG_ROTATION.md | Аугментация: айналдыру (rotation) |
| 20 | 20_PREPROCESS_AUG_TRANSLATION.md | Аугментация: жылжыту (translation) |
| 21 | 21_PREPROCESS_AUG_SCALE.md | Аугментация: масштабтау (scale) |
| 22 | 22_PREPROCESS_AUG_SHEAR.md | Аугментация: ығыстыру (shear) |
| 23 | 23_PREPROCESS_AUG_PCA_COLOR.md | Аугментация: PCA түс jitter |
| 24 | 24_PREPROCESS_AUG_BRIGHTNESS_CONTRAST.md | Аугментация: жарықтық және контраст |
| 25 | 25_PREPROCESS_NORMALIZATION.md | Деректер жиынына сәйкес нормализация (dataset-specific normalization) |

### VI. Деректер (Data) (4 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 26 | 26_SECTION_DATA.md | **Деректер (Data)** |
| 27 | 27_DATASETS.md | Деректер жиындары |
| 28 | 28_DATASETS_EXPERIMENTS.md | Эксперименттер бойынша деректер жиындары |
| 29 | 29_CAMERAS_DISTRIBUTION.md | Камералар бойынша таралым |

### VII. Нәтижелер (Results) (9 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 30 | 30_SECTION_RESULTS.md | **Нәтижелер (Results)** |
| 31 | 31_METRICS.md | Метрикалар: F1, AUC, Cohen's κ, Generalization gap (G), ALO |
| 32 | 32_RESULTS_EXP1.md | 1-эксперимент: H-1 — Препроцессингтің доминанттылығы |
| 33 | 33_RESULTS_EXP2.md | 2-эксперимент: H-2 — V5 компоненттерінің абляциясы |
| 34 | 34_RESULTS_EXP3.md | 3-эксперимент: H-4 — Cross-dataset жалпылау |
| 35 | 35_RESULTS_EXP4.md | 4-эксперимент: H-5 — Түсіндірмелілік (ALO/IoU + Grad-CAM) |
| 36 | 36_RESULTS_EXP5.md | 5-эксперимент: H-7 — Сапа төмендеуіне төзімділік |
| 37 | 37_RESULTS_EXP6.md | 6-эксперимент: H-6 — Камера домен ауысуы |
| 38 | 38_RESULTS_EXP7.md | 7-эксперимент: Кіші деректермен оқыту |

### VIII. Талқылау (Discussion) (4 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 39 | 39_SECTION_DISCUSSION.md | **Талқылау (Discussion)** |
| 40 | 40_DISCUSSION_SYNTHESIS.md | Зерттеу синтезі: препроцессинг — модель компоненті |
| 41 | 41_DISCUSSION_SOTA.md | Клиникалық дайындық және SOTA позициясы |
| 42 | 42_DISCUSSION_LIMITATIONS.md | Зерттеудің шектеулері |

### IX. Ғылыми жаңалық және үлес (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 43 | 43_NOVELTY.md | Ғылыми жаңалық және үлес |

### X. Практикалық маңыздылығы (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 44 | 44_PRACTICAL_SIGNIFICANCE.md | Практикалық маңыздылығы |

### XI. Қорытындылар (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 45 | 45_CONCLUSIONS.md | Қорытындылар |

### XII. Жарияланымдар (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 46 | 46_PUBLICATIONS.md | Жарияланымдар |

### XIII. Қорытынды слайд (1 слайд)

| # | Файл | Тақырып |
|---|------|---------|
| 47 | 47_FINAL.md | Назарларыңызға рахмет! Сұрақтар |
