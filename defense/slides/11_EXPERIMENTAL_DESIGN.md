## 1. Тақырып

Эксперименттік дизайн және метрикалар

---

## 2. Слайд мазмұны

**7 эксперимент — 6 гипотеза:**

| Exp | Дизайн | Оқыту -> Тест | Критерий |
|-----|--------|---------------|----------|
| 1 | 2x2 факторлық (A/B/C/D) | EyePACS 5-fold CV | EH-3: ΔF1>=5pp, ΔAUC>=0.02, Δκ>=0 |
| 2 | 7-деңгейлі ablation + sweep | EyePACS 5-fold CV | Әр класс бойынша F1, CNR/VVI |
| 3 | Zero-shot transfer | EyePACS -> APTOS | G >= 0.85 |
| 4 | Grad-CAM + ALO/IoU | IDRiD + Clinical | ALO_V5 > ALO_baseline |
| 5 | Деградация салыстыру | EyePACS -> IDRiD, Messidor-2 | Δ_V5 < Δ_baseline |
| 6 | Cross-camera zero-shot | EyePACS -> DDR, ODIR, RFMiD | F1 stable across cameras |
| 7 | Small data | IDRiD 5-fold -> Clinical | Weighted F1, κ |

**Метрикалар:** Weighted F1 > ROC-AUC > Cohen κ > Accuracy

**Статистика:** McNemar, DeLong, Bootstrap CI (1000+), ANOVA, Holm-Bonferroni

---

## 3. Баяндаушы сөзі

Эксперименттік бағдарлама 7 эксперименттен тұрады. Бірінші эксперимент — зерттеудің негізі: 2x2 факторлық дизайн. Екінші — pipeline компоненттерінің ablation-ы. Үшінші — APTOS-та zero-shot transfer. Төртінші — Grad-CAM арқылы түсіндірілгіштік. Бесінші — клиникалық деградация. Алтыншы — құрылғы domain shift. Жетінші — шағын деректерде оқыту. Негізгі метрика — Weighted F1; қосымша ROC-AUC, Cohen kappa, Accuracy. Статистикалық валидация McNemar, DeLong тесттері, bootstrap сенімділік интервалдары арқылы жүргізілді, көп салыстыру Holm-Bonferroni түзетуімен бақыланды.
