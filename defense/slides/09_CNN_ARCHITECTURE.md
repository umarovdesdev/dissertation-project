## 1. Тақырып

CNN архитектурасы және оқыту конфигурациясы

---

## 2. Слайд мазмұны

**CNN Classifier:**

|  | ResNet-50 | EfficientNet-B3 |
|--|-----------|-----------------|
| Conv1 кіріс | 4ch -> 64 (7x7) | 4ch -> 40 (3x3) |
| Feature dim | 2048 | 1536 |
| Параметрлер | 25.6M | 12.2M |
| Mixed precision | ON | OFF (fp16 overflow) |

**Classification head:** GAP -> Dropout(0.4) -> Linear(d, 5) -> Softmax -> DR 0-4

**Training конфигурациясы:**
- Focal Loss (gamma=2, alpha=inverse-frequency)
- Adam lr=1e-4, batch=16, max epochs=20
- Early stopping patience=5
- 5-fold patient-level stratified CV (data leakage жоқ)
- seed=42, deterministic=true

**Patient-level aggregation:** y_patient = max(y_left, y_right)

---

## 3. Баяндаушы сөзі

CNN classifier екі архитектура: ResNet-50 және EfficientNet-B3. Екеуінде де Conv1 қабат 3 каналдан 4 каналға кеңейтілді — FOV mask 4-ші канал. ImageNet pretrained салмақтар сақталады, 4-ші канал RGB орташасымен инициализацияланады. EfficientNet параметрлер бойынша 2 есе тиімді, бірақ fp16 overflow мәселесіне байланысты mixed precision өшірілді. Focal Loss класс теңгерімсіздігіне қарсы — сирек класстарға фокусталады. 5-fold patient-level CV бір пациенттің барлық суреттерін бір fold-та ұстайды. Patient-level aggregation max-grade стратегиясы — клиникалық практикаға сәйкес.
