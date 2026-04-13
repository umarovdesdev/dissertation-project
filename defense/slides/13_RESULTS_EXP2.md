## 1. Тақырып

Нәтижелер: Exp 2 — Компонент ablation (H-2)

---

## 2. Слайд мазмұны

**7-деңгейлі ablation** (baseline -> Full V5, EfficientNet-B3):

| Деңгей | Қосылған кезең | F1 | Маржиналды Δ |
|--------|----------------|-----|-------------|
| 0 | Baseline | 0.727 | — |
| 1 | +Canonical flip | 0.738 | +1.1pp |
| 2 | +OD-fovea rotation | 0.748 | +1.0pp |
| 3 | +Isotropic resize + FOV mask | 0.752 | +0.4pp |
| 4 | +Flat-field correction | 0.758 | +0.6pp |
| 5 | +CLAHE | **0.772** | **+1.4pp** |
| 6 | Full V5 (+ augmentation + norm) | **0.780** | +0.8pp |

**CLAHE — ең ірі маржиналды үлес: +1.4pp**

**Параметр sweep:** clip_factor=2.0-2.5 оптимум; flat-field sigma=0.07*D оптимум

**H-2 расталды.** Параметр-тәуелді sensitivity расталды.

---

## 3. Баяндаушы сөзі

Екінші эксперимент — pipeline компоненттерінің ablation-ы. Baseline 0.727-ден Full V5 0.780-ге дейін, кезең-кезеңмен қосылып, әр кезеңнің маржиналды үлесі анықталды. CLAHE ең ірі маржиналды үлес — +1.4pp. Flat-field +0.6pp, canonical flip +1.1pp, rotation +1.0pp. CLAHE параметрлері бойынша sweep жүргізілді — clip_factor 2.0-2.5 аймағында оптимум, flat-field sigma=0.07*FOV диаметрі оптимум. H-2 расталды — pipeline-ның компоненттері параметр-тәуелді sensitivity көрсетеді.
