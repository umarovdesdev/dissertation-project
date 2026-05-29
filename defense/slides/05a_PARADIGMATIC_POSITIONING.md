## 1. Тақырып

**Парадигмалық позиционирование: P1 vs P2**
(Paradigmatic Positioning: P1 vs P2)

---

## 2. Слайд мазмұны

**Екі парадигма / Two paradigms**

| | **Парадигма P1** | **Парадигма P2** |
|---|---|---|
| **Тұжырымдама** | end-to-end CNN | model = preprocessing + CNN |
| **Препроцессинг** | қосалқы дайындау (ancillary data preparation) | модельдің ажырамас компоненті (integral model component) |
| **Канондық өкіл / Canonical representative** | Gulshan et al. (2016, *JAMA*) | Бұл диссертация / This dissertation |
| **Тәжірибеші өкілдер** | Pratt 2016, Rakhlin 2017, Saxena 2020, Ting 2017, Voets 2019 | V5 8-сатылы pipeline |
| **Әдіснамалық тәжірибе** | препроцессинг supplement-ке шығарылады | 8 кезең OD-3-те формализацияланған |
| **Іске асырылу (Exp 1)** | A/C конфигурациялары (3-канал, stretch-resize + ImageNet normalize) | B/D конфигурациялары (4-канал, толық V5 pipeline) |

**Эксперименттік тексеру / Experimental test**

```
        P1 instantiation (A/C)            P2 instantiation (B/D)
                  │                                  │
                  └──────► Эксперимент 1 ◄──────────┘
                         (matched conditions,
                          paradigmatic contrast)
```

---

## 3. Баяндаушы сөзі

Диссертациямыздың концептуалды негізі — диабеттік ретинопатияны автоматты диагностикалаудың екі парадигмасының қарама-қайшылығы.

**Парадигма P1** — end-to-end CNN парадигмасы — препроцессингті модельден тыс, қосалқы деректерді дайындау сатысы ретінде қарастырады. Бұл парадигманың канондық өкілі — Gulshan et al. (2016, *JAMA*) еңбегі. Pratt 2016, Rakhlin 2017, Saxena 2020, Ting 2017 және Voets 2019 еңбектері де осы тәсілде орналасқан.

**Парадигма P2** — интегралды preprocessing-CNN парадигмасы — препроцессингті модельдің ажырамас компоненті ретінде қарастырады, өйткені ол CNN-ге қол жетімді feature space-ті анықтайды. Бұл диссертация — осы парадигманың тәжірибелік іске асырылуы.

Назар аударыңыз: Gulshan авторлары "препроцессинг маңызды емес" деген тұжырымды нақты айтпаған. Біз олардың әдіснамалық *тәжірибесін* парадигма P1 деп жіктеп жатырмыз — препроцессинг supplementary материалға шығарылған, негізгі мәтін архитектура мен деректер ауқымына шоғырланған.

Эксперимент 1-дегі A/C және B/D конфигурацияларының салыстыруы — нақты сандық сан мәндерімен Gulshan-мен бетпе-бет салыстыру емес, тең шарттардағы екі парадигманың эмпирикалық контрасты.

---

## 4. Қосымша — Әдіснамалық ескертулер (Methodological notes)

**Тікелей сандық салыстыру жоқ / No direct numerical comparison.** Gulshan 2016 — бинарлық referable-DR, Inception-v3 ансамблі, жеке композиттік деректер жинағы; біздің диссертация — 5-кластық DR 0–4, ResNet-50 / EfficientNet-B3, EyePACS-тің ашық бөлімі. Бұл айырмашылықтар бетпе-бет сандық салыстыруды әдіснамалық тұрғыдан болмайтын етеді (INVARIANTS SB-1.12, CFC-2.2).

**Базалық конфигурация ≠ Gulshan жүйесі.** Эксперимент 1-дегі базалық конфигурация (configs A/C) — OD-3-те анықталған *операционды конструкт* (stretch-resize + ImageNet normalize, 3-канал). Ол Gulshan ұсынған парадигманы операционализациялайды, бірақ Gulshan-ның жүйесі емес. "Gulshan — біздің baseline" деген тұжырым тыйым салынған (CFC-2.9).

**Терминология / Terminology.**
- "P1-instantiation baseline" — конфигурация A/C (Exp 1 ішкі құрылымы).
- "Canonical representative of P1" — Gulshan 2016 (әдебиет, тарихи / canonical).
- Бұл екі мағынаны араластыруға болмайды.

---

## 5. Қосымша — Дереккөздер (Source references)

- `thesis/governance/INVARIANTS.md` — SB-1.12, CFC-2.9, SIR-9
- `thesis/governance/CENTRAL_THESIS.md` — Paradigmatic framing paragraph
- `thesis/governance/CONTRIBUTIONS.md` — Conceptual framing of primary contributions
- `thesis/governance/ARGUMENT_MAP.md` — PC-0 (Paradigmatic Framing Claim)
- `thesis/literature/external/gulshan-2016.md` §15 (Paradigmatic Role) + §18 (Paradigmatic Synthesis)
- `thesis/literature/LITERATURE_INDEX.md` — Paradigm column
- `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` — integration tracker
