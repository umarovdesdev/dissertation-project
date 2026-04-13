## 1. Тақырып

Зерттеу нәтижелері — Exp 2–7: Қалған гипотезалар

---

## 2. Слайд мазмұны

| Exp | Гипотеза | Негізгі нәтиже | Күйі |
|-----|----------|-----------------|------|
| **2** | H-2: Ablation | Baseline 0.727 → Full V5 0.780 (+5.3pp). CLAHE: +1.4pp (ең ірі). σ=0.07·D оптимум | **Расталды** |
| **3** | H-4: Transfer | APTOS zero-shot: D G=0.890, B G=0.861 ≥ 0.85 | **Расталды** |
| **4** | H-5: Explainability | ALO: +31–61% (4 зақым типі). Attention consistency: 0.61→0.81 | **Расталды** |
| **5** | H-7: Degradation | IDRiD Δ: 11.9→9.0pp (−24%). Messidor-2 Δ: 10.2→8.0pp (−22%) | **Расталды** |
| **6** | H-6: Device shift | Cross-device σ²: 0.0052→0.0028 (−46%). DDR/ODIR/RFMiD: +8–9pp | **Расталды** |
| **7** | Small data | IDRiD→Clinical: baseline 0.515, pipeline 0.608 (+9.3pp) | *(Қосымша)* |

**6/6 гипотеза расталды.** Preprocessing classification-ды, тасымалдаушылықты, түсіндірмелілікті және құрылғы тұрақтылығын жақсартады.

E:\dissertation-project\demo\public\results\04_exp2_ablation.png
E:\dissertation-project\demo\public\results\09_exp5_G_ratio.png
E:\dissertation-project\demo\public\results\06_exp4_alo.png
E:\dissertation-project\demo\public\results\10_exp6_device_shift.png

---

## 3. Баяндаушы сөзі

Қалған эксперименттерді қысқаша баяндаймын.

**Exp 2 — компонент ablation.** Pipeline 7 кезеңі F1-ді 0.727-ден 0.780-ге арттырады. CLAHE ең ірі маржиналды үлес — +1.4pp. Flat-field σ=0.07·D оптимумы smooth response surface-те расталды. H-2 расталды.

**Exp 3 — APTOS тасымалдаушылық.** Zero-shot transfer. Екі pipeline конфигурациясы да G ≥ 0.85 шегін орындайды — baseline-дар орындамайды. Preprocessing domain gap-ін стандарттайды. H-4 расталды.

**Exp 4 — түсіндірмелілік.** ALO метрикасы 4 зақым типінде 31-ден 61 пайызға дейін жақсарды. Pipeline модельдің назарын зақым аймағына бағыттайды. H-5 расталды.

**Exp 5 — клиникалық деградация.** IDRiD-ке деградация 24 пайызға, Messidor-2-де 22 пайызға азайды. H-7 расталды.

**Exp 6 — құрылғы shift.** 4 камера өндірушісінде cross-device дисперсия 46 пайызға қысқарды. H-6 расталды.

**Exp 7 — шағын деректер.** Clinical датасетте pipeline +9.3pp жақсару — preprocessing шағын деректерде пропорционалды жоғары пайда береді.

Барлық алты гипотеза расталды.

---

## 4. Қосымша

- **Exp 2 Ablation** — Кезеңдер: canonical flip (+1.1), rotation (+1.0), isotropic resize+FOV mask (+0.4), flat-field (+0.6), CLAHE (+1.4), augmentation (+0.6), normalization (+0.2). CLAHE жеке қосқанда +2.3pp. Жеке қосындыларсі (5.5pp) > толық pipeline (5.3pp) — mild interaction.
- **CLAHE оптимумдары** — DR 1: clip=2.5, F1=0.47; DR 2: clip=2.0, F1=0.62. global_threshold=0.03.
- **Exp 3 G ratio** — A: G=0.812, B: G=0.861, C: G=0.820, D: G=0.890. Config D APTOS F1=0.694±0.024, AUC=0.842±0.014. DeLong p=0.015.
- **Exp 4 ALO** — MA: 0.28→0.45 (+61%), HE: 0.42→0.62 (+48%), Hard EX: 0.55→0.72 (+31%), Soft EX: 0.38→0.56 (+47%). IoU: +50–83%.
- **Exp 5 Degradation** — IDRiD: paired t-test p=0.031. Messidor-2: p=0.044. Baseline AUC→Pipeline AUC: IDRiD 0.780→0.830, Messidor-2 0.790→0.840.
- **Exp 6 Device shift** — DDR (Canon+Topcon): +8.0pp, ODIR-5K (Canon+Zeiss): +9.0pp, RFMiD (Topcon+Kowa): +9.0pp.
- **Exp 7 Small data** — IDRiD (516 сурет) → Clinical (60 сурет). Baseline: IDRiD F1=0.585, Clinical F1=0.515, AUC=0.742. Pipeline: IDRiD F1=0.652, Clinical F1=0.608, AUC=0.812. Δ=+9.3pp (vs Exp 1 +5.3pp).
