# TASK.md — Three Architecture Diagrams for Dissertation Defense

**Date:** 2026-04-26
**Candidate:** Yesmukhamedov N.S., IITU
**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification

---

## 1. Финальное понимание задачи

Нужно построить **три отдельные диаграммы** в формате `.svg` (с дальнейшей конвертацией в `.png` для презентации защиты).

### 1.1 Согласованные параметры

| Параметр | Значение |
|----------|----------|
| Язык подписей | English (только) |
| Стиль | Строгий академический — тонкие линии, прямоугольники, без иконок и иллюстраций |
| Фон | Белый |
| Контраст | ≥ 4.5:1 на белом (WCAG AA) |
| Формат | SVG → потом конвертация в PNG |
| Расположение | `demo/public/diagrams/` |

### 1.2 Концептуальная структура трёх диаграмм

| № | Уровень абстракции | Что раскрывает | Что остаётся «чёрным ящиком» |
|---|---|---|---|
| 1 | Самый высокий — экспериментальный дизайн | 2×2 факториал: {Baseline, Pipeline} × {ResNet-50, EfficientNet-B3} → 4 конфигурации (Config A/B/C/D) → Results | Внутренности препроцессинга, внутренности CNN, агрегация, объяснимость |
| 2 | Системный — полная end-to-end архитектура | Вход (пара глаз) → препроцессинг как **единый объединённый блок** → выход (обработанное изображение + FOV-маска) → CNN → Patient-Level Aggregation Φ → Prediction → отдельная ветка Grad-CAM | Внутренности 8 этапов препроцессинга (это уровень №3) |
| 3 | Уровень препроцессинга — детализация всех этапов | Один большой постер с 8 панелями (по одной на каждый Stage 0–7), параметры, формулы, типы тензоров | — (это самая глубокая детализация) |

**Концепт «разрезания»:** существующий `pipeline_diagram.svg` (старый монолит, который смешивал системный и этапный уровни) мы разделяем:
- системная часть → Диаграмма №2 (с добавлением Patient-Level Aggregation и Grad-CAM)
- этапная часть → Диаграмма №3 (постер с 8 панелями)

---

## 2. Источники истины

| Файл | Что даёт |
|------|----------|
| `CLAUDE.md` (корень) | Центральный тезис: model = preprocessing + CNN |
| `thesis/governance/CENTRAL_THESIS.md` | Тезис на одном абзаце |
| `demo/public/diagrams/system_architecture_specification.md` | Полная спецификация архитектуры (Sections 1–14) |
| `demo/public/diagrams/v5_pipeline_specification.md` | Подробная спецификация 8 этапов препроцессинга |
| `demo/public/diagrams/general.png` | Референс пользователя для Диаграммы №1 |
| `demo/public/diagrams/pipeline_diagram.svg` | Существующий монолит — концептуально разрезаем на №2 и №3 |

---

## 3. Диаграмма №1 — Maximally Abstract Architecture (2×2 Factorial)

**Файл:** `demo/public/diagrams/01_abstract_model_architecture.svg`

### 3.1 Структура (на основе референса `general.png`)

```
                            ┌─────────┐
                            │  Image  │
                            └────┬────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
        ┌───────────────┐                ┌───────────────┐
        │   Baseline    │                │   Pipeline    │
        │  preprocessing│                │  preprocessing│
        └───┬─────────┬─┘                └─┬─────────┬───┘
       Cfg A│         │Cfg C        Cfg B  │         │Cfg D
            │         └──────┐    ┌────────┘         │
            ▼                ▼    ▼                  ▼
     ┌────────────┐                          ┌──────────────────┐
     │ ResNet-50  │                          │ EfficientNet-B3  │
     └─────┬──────┘                          └────────┬─────────┘
           │                                          │
           └──────────────┬───────────────────────────┘
                          ▼
                    ┌──────────┐
                    │  Results │
                    └──────────┘
```

### 3.2 Содержание блоков

- **Image** — Raw fundus photograph (один обобщённый блок).
- **Baseline preprocessing** — Stretch-resize 512×512 + ImageNet normalize (3 channels).
- **Pipeline preprocessing** — Full V5 (8 stages, 4 channels). Раскрывается в Диаграммах №2 и №3.
- **ResNet-50** — CNN backbone, ImageNet-pretrained, 4-channel input adapted.
- **EfficientNet-B3** — CNN backbone, ImageNet-pretrained, 4-channel input adapted.
- **Results** — Aggregated metrics (F1 / AUC / κ / accuracy) для всех 4 конфигураций.

### 3.3 Подписи путей

На каждой из 4 рёбер (от препроцессинга к бэкбону) подпись конфигурации:
- Baseline → ResNet-50 = **Config A**
- Pipeline → ResNet-50 = **Config B**
- Baseline → EfficientNet-B3 = **Config C**
- Pipeline → EfficientNet-B3 = **Config D**

### 3.4 Визуальные особенности

- 6 прямоугольников + 4 подписи путей.
- Цветовое кодирование:
  - Image — графит-серый.
  - Baseline preprocessing — сланцево-серый (контрольная ветка).
  - Pipeline preprocessing — тёмно-зелёный (экспериментальная ветка).
  - CNN backbones — тёмно-синий.
  - Results — винно-красный.
- Layout: симметричный «diamond».
- Шрифт: sans-serif (Inter / Helvetica / Arial), 16pt для блоков, 12pt для подписей путей.

### 3.5 Что НЕ показываем

- Patient-Level Aggregation (это уровень №2).
- Grad-CAM (это уровень №2).
- Размерности тензоров (это уровень №2 и №3).
- Этапы препроцессинга (это уровни №2 и №3).

---

## 4. Диаграмма №2 — Full System Architecture (End-to-End)

**Файл:** `demo/public/diagrams/02_system_architecture.svg`

### 4.1 Цель

Показать полную end-to-end архитектуру системы согласно `system_architecture_specification.md` (Section 11 «Full Pipeline Flow»). Препроцессинг здесь — **единый объединённый блок** (содержание раскрывается в Диаграмме №3).

### 4.2 Структура

```
                    Patient Record (bilateral pair)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │  I_left (BGR)   │             │  I_right (BGR)  │
     │  s_left         │             │  s_right        │
     └────────┬────────┘             └────────┬────────┘
              │                               │
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │  Preprocessing  │             │  Preprocessing  │
     │   𝒫 (V5, all 8  │             │   𝒫 (V5, all 8  │
     │     stages)     │             │     stages)     │
     └────────┬────────┘             └────────┬────────┘
              │                               │
       Processed image (RGB) +         Processed image (RGB) +
       FOV mask (4 channels,           FOV mask (4 channels,
       512×512, float32)                512×512, float32)
              │                               │
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │  CNN Backbone   │ ◄── shared ─►│  CNN Backbone   │
     │  (ResNet-50 or  │              │  (ResNet-50 or  │
     │  EfficientNet)  │              │  EfficientNet)  │
     └────────┬────────┘             └────────┬────────┘
              │                               │
        f_L ∈ ℝ^d                       f_R ∈ ℝ^d
              │                               │
              └───────────────┬───────────────┘
                              ▼
                  ┌───────────────────────┐
                  │  Patient-Level        │
                  │  Aggregation Φ        │
                  │  (max-grade)          │
                  └───────────┬───────────┘
                              ▼
                  ┌───────────────────────┐
                  │  Prediction Layer g   │
                  │  softmax → ŷ, p̂      │
                  └───────────┬───────────┘
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
            ┌─────────┐         ┌──────────────────┐
            │Diagnosis │         │ Grad-CAM         │
            │ ŷ ∈{0..4}│         │ Explainability   │
            │ ŷ_ref    │         │ → heatmap        │
            └─────────┘         │ → ALO, IoU       │
                                └──────────────────┘
```

### 4.3 Что показываем

- **Bilateral input:** пара изображений (левый/правый глаз) + метаданные laterality.
- **Preprocessing 𝒫 как единый блок** для каждого глаза. Подпись: «V5 (8 stages, see Diagram №3)».
- **Output of preprocessing:** обработанное RGB-изображение + FOV-маска = 4-канальный тензор (4×512×512, float32).
- **CNN backbone:** общие веса для обоих глаз (shared weights).
- **Per-eye feature vectors** f_L, f_R.
- **Patient-Level Aggregation Φ:** max-grade (основная стратегия).
- **Prediction layer g:** softmax → ŷ, p̂.
- **Diagnosis output:** DR grade + бинарное решение (referable DR).
- **Grad-CAM ветка:** отдельная ветка, отходящая от prediction layer (или от feature maps), показывает heatmap + метрики ALO/IoU.

### 4.4 Визуальные особенности

- Layout: вертикальный (top-down), симметричный по центру для bilateral pair.
- Препроцессинг — **единый прямоугольник** на каждый глаз (без раскрытия 8 этапов).
- На стрелках после препроцессинга — подпись формата тензора `(4, 512, 512), float32`.
- Patient-Level Aggregation — выделенный блок в центре.
- Grad-CAM ветка — пунктирные линии (post-hoc, не часть основного inference потока).
- Цветовое кодирование (согласовано с №1 и №3):
  - Input — графит.
  - Preprocessing блок — тёмно-зелёный.
  - CNN backbones — тёмно-синий.
  - Aggregation — янтарный.
  - Prediction — винно-красный.
  - Grad-CAM ветка — серо-голубой пунктир.

### 4.5 Что НЕ показываем

- Внутренности 8 этапов препроцессинга (это Диаграмма №3).
- Сравнение Baseline vs Pipeline (это Диаграмма №1).
- Детали MLP-головы PatientHead (Section 7.4) — она не в активном дизайне.
- Конкретные размерности feature dimension d (2048 / 1536) — оставляем абстрактно «d».

---

## 5. Диаграмма №3 — Detailed Per-Stage Preprocessing Diagram

**Файл:** `demo/public/diagrams/03_preprocessing_stages_detailed.svg` (одна диаграмма, Вариант A)

### 5.1 Цель

Раскрыть «чёрный ящик» препроцессинга 𝒫 из Диаграммы №2 — показать все 8 этапов V5 с подробностями каждого.

### 5.2 Формат

**Один SVG-постер**, разбитый на 8 панелей в grid 4×2 (4 колонки × 2 строки) или 2×4 (2 колонки × 4 строки) — выберу по соотношению сторон при реализации.

### 5.3 Содержание каждой панели

| Элемент | Описание |
|---------|----------|
| Header | `Stage N — Name` |
| Input | Формат и размерность тензора (например, `RGB uint8, H×W×3`) |
| Internal operations | 2–4 шага операции (например, для Stage 1: OD detection → Fovea detection → Compute angle θ → Rotate by −θ) |
| Output | Формат и размерность тензора |
| Key parameters | Значения по умолчанию (σ = 0.07·D; clip_factor = 2.0; tile_grid = 8×8; и т.д.) |
| Mode | always-on / train-only / stochastic |

### 5.4 Восемь панелей

- **Stage 0** — Canonical Flip (always-on)
- **Stage 1** — OD-Fovea Rotation Normalization (always-on, conditional)
- **Stage 2** — FOV Crop + Isotropic Resize → 512×512 (always-on)
- **Stage 3** — FOV Mask Generation (always-on, side branch для 4-го канала)
- **Stage 4** — Adaptive Flat-Field Correction, σ = 0.07·D (always-on)
- **Stage 5** — Dual-Constraint CLAHE, LAB L-channel (always-on, stochastic при train)
- **Stage 6** — Augmentation, affine + PCA color (train only)
- **Stage 7** — Dataset-Specific Normalize + FOV Mask Append (always-on)

### 5.5 Визуальные особенности

- Каждая панель — прямоугольник с border, внутри — структурированный layout (Header / Input / Operations / Output / Params).
- Между панелями — стрелки, обозначающие порядок исполнения (если grid позволяет — линия с номерами 0→1→2→…→7).
- Stage 6 (train-only) — выделен пунктирной обводкой.
- Stage 3 (mask side branch) — выделен другим цветом (бирюзовый), с пунктирной стрелкой к Stage 7 (показать что mask append'ится в конце).
- Цветовое кодирование (согласовано с №2):
  - Geometry stages (0–3) — бирюзовый.
  - Photometric stages (4–5) — оранжевый.
  - Train-only (6) — фиолетовый, пунктир.
  - Normalization (7) — винно-красный.
- Внизу — компактная легенда (always-on / train-only / stochastic / data flow).

---

## 6. Унифицированная цветовая палитра

| Назначение | HEX | Контраст на белом |
|------------|-----|-------------------|
| Input (`Image`, raw tensor) — графит | `#1f2937` | 14.7:1 |
| Baseline preprocessing — сланцево-серый | `#475569` | 8.6:1 |
| Pipeline (V5) preprocessing — тёмно-зелёный | `#166534` | 8.4:1 |
| Geometry stages (0–3) — бирюзовый | `#0d9488` | 4.7:1 |
| Photometric stages (4–5) — оранжевый | `#c2410c` | 5.6:1 |
| Train-only / stochastic (6) — фиолетовый | `#6d28d9` | 7.4:1 |
| Normalization (7) / Results / Prediction — винно-красный | `#9f1239` | 8.5:1 |
| CNN backbones (ResNet-50, EfficientNet-B3) — тёмно-синий | `#1e3a8a` | 11.2:1 |
| Patient-Level Aggregation — янтарный | `#b45309` | 5.0:1 |
| Grad-CAM ветка — серо-голубой пунктир | `#475569` | 8.6:1 |
| Текст подписей | `#111827` | 17.3:1 |
| Стрелки | `#000000` | 21:1 |
| Заливка блоков | соответствующий цвет с alpha 12–18% | — |

Все цвета имеют контраст ≥ 4.5:1 на белом фоне (WCAG AA).

---

## 7. Технические детали

- **Формат:** чистый SVG (XML вручную), без зависимостей от внешних шрифтов (sans-serif fallback).
- **viewBox:**
  - №1: 1600×900 (16:9 для слайда).
  - №2: 1200×1600 (вертикальный — bilateral pair требует высоты).
  - №3: 1920×1080 для grid 4×2 ИЛИ 1080×1920 для grid 2×4.
- **Toolchain:** SVG пишется руками, без зависимости от Inkscape/Figma.
- **Конвертация в PNG:** позднее, через ImageMagick / Inkscape CLI / онлайн при экспорте 2× DPI.

---

## 8. Согласованные решения

Все вопросы из предыдущей итерации решены:

| Вопрос | Решение |
|--------|---------|
| Язык подписей | English |
| Стиль | Строгий академический |
| Диаграмма №1: Config A/B/C/D на путях | Да, показываем |
| Диаграмма №3: Вариант A или B | Вариант A (одна диаграмма-постер) |
| Patient-Level Aggregation в №1 | НЕТ — переносим в №2 |
| Grad-CAM в №1 | НЕТ — переносим в №2 |
| Препроцессинг в №2 | Единый блок, без раскрытия этапов |
| Выход препроцессинга в №2 | Обработанное RGB + FOV-маска (4-канальный тензор) |

---

## 9. План работ

1. ✅ Согласовать TASK.md (текущая версия — финальная).
2. ⏳ Создать Диаграмму №1 (`01_abstract_model_architecture.svg`).
3. ⏳ Создать Диаграмму №2 (`02_system_architecture.svg`).
4. ⏳ Создать Диаграмму №3 (`03_preprocessing_stages_detailed.svg`).
5. ⏳ Визуальная проверка каждой диаграммы.
6. ⏳ Конвертация SVG → PNG для экспорта.

---

*End of TASK.md*
