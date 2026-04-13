## 1. Тақырып

Нәтижелер: Exp 1 — Preprocessing доминанттылығы (H-1)

---

## 2. Слайд мазмұны

**2x2 факторлық нәтижелер** *(EyePACS, ~35 126 сурет, 5-fold CV)*

|  | Baseline (3ch) | Full V5 (4ch) | ΔF1 | ΔAUC | Δκ |
|--|----------------|---------------|-----|------|----|
| **ResNet-50** | A: 0.724+-0.011 | B: 0.776+-0.009 | **+5.2pp** | **+3.3pp** | **+8.0pp** |
| **EfficientNet-B3** | C: 0.727+-0.033 | D: 0.780+-0.022 | **+5.3pp** | **+4.4pp** | **+8.0pp** |

**EH-3 доминанттылық:** екі архитектурада да 3/3 критерий орындалды

**ANOVA:** preprocessing main effect p<0.001 | interaction p=0.23 (n.s.)
**DeLong:** ResNet p=0.006, EfficientNet p=0.008
**Bootstrap 95% CI:** [+2.5, +7.9]pp, [+2.8, +7.8]pp — нөлді қамтымайды

**H-1 расталды.** Preprocessing — архитектура-агностикалық robust main effect.

E:\dissertation-project\defense\assets\14_exp1_factorial_results.svg

---

## 3. Баяндаушы сөзі

Бірінші эксперимент — preprocessing доминанттылығы. EyePACS-тың 35 мың суретінде 2x2 факторлық дизайн жүргізілді. Нәтиже: екі архитектурада да EH-3 доминанттылық критерийі орындалды. ResNet-50-де ΔF1=+5.2pp, EfficientNet-B3-те +5.3pp. ANOVA preprocessing main effect p<0.001, interaction p=0.23 — маңызды емес. Бұл preprocessing-тің пайдасы архитектурадан тәуелсіз екенін дәлелдейді. DeLong тесті екі архитектурада да маңызды, bootstrap интервалдары нөлді қамтымайды. Config D ең жоғары абсолютті F1=0.780 нәтижеге жетті. H-1 расталды.
