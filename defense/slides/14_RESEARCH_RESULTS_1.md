## 1. Тақырып

Зерттеу нәтижелері — Exp 1: Preprocessing доминанттылығы (H-1)

---

## 2. Слайд мазмұны

**2×2 факторлық нәтижелер** *(EyePACS 100%, ~35 126 сурет, 5-fold patient-level CV)*

|  | Baseline (3ch) | Full V5 (4ch) | ΔF1 | ΔAUC | Δκ |
|--|----------------|---------------|-----|------|----|
| **ResNet-50** | A: 0.724±0.011 | B: 0.776±0.009 | **+5.2pp** | **+3.3pp** | **+8.0pp** |
| **EfficientNet-B3** | C: 0.727±0.033 | D: 0.780±0.022 | **+5.3pp** | **+4.4pp** | **+8.0pp** |

**EH-3 доминанттылық критерийі:**

| Критерий | Шек | ResNet-50 (B−A) | EfficientNet-B3 (D−C) |
|----------|-----|-----------------|------------------------|
| ΔF1 ≥ 5pp | 5pp | **+5.2pp ✓** | **+5.3pp ✓** |
| ΔAUC ≥ 2pp | 2pp | **+3.3pp ✓** | **+4.4pp ✓** |
| Δκ > 0 | 0 | **+8.0pp ✓** | **+8.0pp ✓** |
| **EH-3** | 3/3 | **ИӘ** (3/3) | **ИӘ** (3/3) |

**ANOVA:** preprocessing main effect p<0.001 | interaction p=0.23 (n.s.)
**DeLong:** ResNet p=0.006, EfficientNet p=0.008
**Bootstrap 95% CI:** ResNet [+2.5, +7.9]pp, EfficientNet [+2.8, +7.8]pp

E:\dissertation-project\defense\assets\14_exp1_factorial_results.svg
E:\dissertation-project\demo\public\results\01_exp1_factorial_f1.png
E:\dissertation-project\demo\public\results\12_eh3_dominance.png

---

## 3. Баяндаушы сөзі

Зерттеу нәтижелерін ұсынамын. Бірінші эксперимент — preprocessing доминанттылығы. EyePACS-тың 35 мың суретінде 2 мал 2 факторлық дизайн жүргізілді.

Нәтиже: **екі архитектурада да** EH-3 доминанттылық критерийі орындалды. ResNet-50-де ΔF1=+5.2pp, EfficientNet-B3-те +5.3pp. ANOVA preprocessing main effect p<0.001, ал interaction p=0.23 — маңызды емес. Бұл preprocessing-тің пайдасы архитектурадан тәуелсіз, robust main effect екенін дәлелдейді.

Config D — EfficientNet-B3 + V5 — ең жоғары абсолютті нәтиже: F1=0.780. Бірақ Config B — ResNet-50 + V5 — де ұқсас деңгейде: F1=0.776. DeLong тесті екі архитектурада да маңызды: p=0.006 және p=0.008. Bootstrap сенімділік интервалдары нөлді қамтымайды. H-1 расталды.

---

## 4. Қосымша

- **2×2 факторлық дизайн** — A (baseline+ResNet), B (V5+ResNet), C (baseline+EfficientNet), D (V5+EfficientNet). Main effect пен interaction effect бөлуге мүмкіндік береді.
- **EH-3 критерийі** — ΔF1 ≥ 5pp ∧ ΔAUC ≥ 2pp ∧ Δκ > 0. Екі архитектурада да орындалды.
- **ANOVA** — preprocessing main effect p<0.001, interaction p=0.23 (n.s.). Preprocessing-тің пайдасы архитектурадан тәуелсіз.
- **DeLong тесті** — ResNet: p=0.006, EfficientNet: p=0.008. McNemar: ResNet p=0.009, EfficientNet p=0.012. Holm-corrected: ResNet p_adj=0.012, EfficientNet p_adj=0.024.
- **Bootstrap 95% CI** — ResNet: [+2.5, +7.9]pp, EfficientNet: [+2.8, +7.8]pp — нөлді қамтымайды.
- **Training–test gap** — A=7.6pp, B=7.4pp, C=7.3pp, D=7.0pp — барлығы 15pp шегінен төмен. Overfitting жоқ.
