## 1. Тақырып

Зерттеу нәтижелерін талқылау (2): Cross-domain, клиникалық маңыздылық, есептеу тиімділігі

---

## 2. Слайд мазмұны

**1. Cross-domain стандарттау**

| Аспект | Baseline | Pipeline | Жақсару |
|--------|----------|----------|---------|
| APTOS transfer G (Config D) | 0.820 | **0.890** | +7.0pp |
| Device variance σ² | 0.0052 | **0.0028** | **−46%** |
| Attention consistency | 0.61 | **0.81** | **+33%** |
| Degradation (IDRiD) | 11.9pp | **9.0pp** | **−24%** |

→ Pipeline камераға тәуелсіз feature кеңістігін жасайды.

**2. Клиникалық маңыздылық**

| Метрика | Baseline | Pipeline | WHO шегі |
|---------|----------|----------|----------|
| Sensitivity | 0.82 | **0.90** | ≥ 0.80 ✓ |
| Specificity | 0.88 | **0.91** | — |
| NPV | 0.92 | **0.96** | — |
| ECE | 0.082 | **0.045** | −45% |

→ Sensitivity 0.90 — WHO скрининг шегінен +10pp жоғары.

**3. Есептеу тиімділігі**

| Метрика | ResNet-50 | EfficientNet-B3 |
|---------|-----------|-----------------|
| Параметрлер | 25.6M | **12.2M** |
| Inference (pipeline) | 45.3 ms | 51.8 ms |
| Pipeline overhead | ~27 ms | ~27 ms |
| GPU жады | 4.3 GB | 6.9 GB |

→ RTX 3060 (12GB) жеткілікті. Секундына ~19 сурет өңдеуге мүмкін.

E:\dissertation-project\demo\public\results\08_exp5_generalization.png
E:\dissertation-project\demo\public\results\14_clinical_metrics.png
E:\dissertation-project\demo\public\results\17_computational.png
E:\dissertation-project\demo\public\results\28_attention_consistency.png

---

## 3. Баяндаушы сөзі

Талқылаудың қалған үш аспектісін баяндаймын.

**Cross-domain стандарттау.** Pipeline тек classification-ды ғана емес, тасымалдаушылықты да жақсартады. Екі pipeline config H-4 шегін орындайды. Cross-device дисперсия 46 пайызға азайды. Attention consistency — 0.61-ден 0.81-ге. Pipeline модельді камераға тәуелсіз feature-ларға назар аударуға мәжбүр етеді — Canon-мен оқытылған модель Topcon, Kowa, Zeiss камераларында да бірдей ретиналды құрылымдарға қарайды.

**Клиникалық маңыздылық.** Sensitivity 0.90 — WHO 0.80 шегінен жоғары. NPV 0.96 — модель "DR жоқ" десе, 96 пайыз дұрыс. ECE 45 пайызға азайды — модельдің confidence бағалаулары сенімдірек, дәрігер оларға сене алады.

**Есептеу тиімділігі.** Pipeline overhead суретке 27 миллисекунд. 4-канал кіріс GPU жадын тек 2 пайызға арттырады. Барлығы RTX 3060-та орындалды — бұл consumer-grade карта, клиникалық ортада қолжетімді.

---

## 4. Қосымша

- **Generalization ratio G** — G = F1_external / F1_EyePACS. Pipeline configs B: G=0.861, D: G=0.890. Baseline A: G=0.812, C: G=0.820. Domain gap стандарттау: EyePACS (Canon, АҚШ) мен APTOS (аралас камералар, Үндістан).
- **Attention consistency** — Grad-CAM distribution-дардың cosine similarity. 3 датасет жұбы: EyePACS-IDRiD 0.58→0.78, EyePACS-Messidor 0.62→0.82, IDRiD-Messidor 0.64→0.84. Орташа: 0.61→0.81 (+33%).
- **Sensitivity 0.90** — referable DR (Grade ≥ 2). 1000 пациенттен 900-і дұрыс анықталады (vs baseline 820). PPV 0.76→0.82.
- **NPV 0.96** — жалған теріс нәтижелер аз, пациент қауіпсіздігі.
- **ECE** — 0.082→0.045 (−45%). Preprocessing модельді "дәлірек сенімді" етеді — confidence = actual accuracy.
- **Pipeline overhead** — ~27 ms/сурет: flat-field, CLAHE, FOV detection, rotation. Inference: 24.5→51.8 ms (EfficientNet). Секундына 19 сурет.
- **GPU жады** — 4ch: EfficientNet 6.9GB, ResNet 4.3GB — RTX 3060 12GB шегінде. Тек 1-conv қабат өзгереді (+0.1K parametr).
- **Brier Score** — 0.185→0.142 (−23%). ECE-мен бірге калибрлеу жақсаруын растайды.
