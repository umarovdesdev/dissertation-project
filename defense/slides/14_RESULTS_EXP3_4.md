## 1. Тақырып

Нәтижелер: Exp 3 — Тасымалдаушылық (H-4), Exp 4 — Түсіндірмелілік (H-5)

---

## 2. Слайд мазмұны

**Exp 3: EyePACS -> APTOS 2019 (zero-shot)**

| Config | G ratio | G >= 0.85? |
|--------|---------|------------|
| A (baseline + ResNet) | 0.812 | Жоқ |
| B (V5 + ResNet) | **0.861** | **Иә** |
| C (baseline + EfficientNet) | 0.820 | Жоқ |
| D (V5 + EfficientNet) | **0.890** | **Иә** |

Pipeline configs: G >= 0.85 орындалды. Baseline configs: орындамады. **H-4 расталды.**

**Exp 4: Grad-CAM + IDRiD зақым маскалары**

| Зақым типі | ALO baseline | ALO pipeline | Δ |
|------------|-------------|-------------|---|
| Microaneurysms (MA) | 0.28 | **0.45** | **+61%** |
| Haemorrhages (HE) | 0.42 | **0.62** | **+48%** |
| Hard exudates (EX) | 0.55 | **0.72** | **+31%** |
| Soft exudates (SE) | 0.38 | **0.56** | **+47%** |

Attention consistency: 0.61 -> **0.81** (+33%). **H-5 расталды.**

---

## 3. Баяндаушы сөзі

Exp 3 — APTOS-та zero-shot transfer. Екі pipeline конфигурациясы G>=0.85 орындады, baseline-дар орындамады. Preprocessing domain gap-ін стандарттайды. H-4 расталды. Exp 4 — түсіндірмелілік. ALO метрикасы IDRiD-тің 4 зақым типінде 31-ден 61 пайызға дейін жақсарды. Preprocessing модельдің назарын зақым аймағына бағыттайды. Attention consistency датасеттер арасында 0.61-ден 0.81-ге көтерілді. H-5 расталды.
