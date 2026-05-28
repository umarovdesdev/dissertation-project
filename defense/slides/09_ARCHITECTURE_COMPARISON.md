## 1. Тақырып

Архитектураларды салыстыру: ResNet-50 vs EfficientNet-B3

---

## 2. Слайд мазмұны

![Абстрактты модель архитектурасы: ResNet-50 vs EfficientNet-B3](../assets/architecture/08_comparison/01_abstract_model_architecture.png)

**Факторлық дизайн (Эксперимент 1, H-1 гипотезасы — v5.2)**

| Config | Препроцессинг | Pretraining source | Backbone | Каналдар |
|--------|---------------|---------------------|----------|----------|
| **A**  | Baseline (stretch-resize + ImageNet norm) | **ImageNet** | ResNet-50 | 3 |
| **C**  | Baseline (stretch-resize + ImageNet norm) | **ImageNet** | EfficientNet-B3 | 3 |
| **B′** | Full V5 Pipeline (8 кезең + FOV mask) | **RETFound** (CFP-checkpoint, multi-modal corpus: ~904K CFP + ~736K OCT) | AOQ-1 шешіміне сай (ViT-Large / CNN-үйлесімді) | 4 |

**Factor 1 — Препроцессинг:** Baseline (stretch-resize 512×512 + ImageNet normalize, 3 канал) vs V5 Pipeline (8 кезең + 4-каналды RGB + FOV mask + dataset-specific normalize).

**Factor 2 — Pretraining source:** ImageNet (табиғи кескіндер, кросс-домендік) vs RETFound (ретиналды foundation model, Zhou et al., 2023 — MAE мульти-модальді ретиналды корпуста: ≈904K CFP + ≈736K OCT; диссертацияда CFP-checkpoint жүктеледі).

> Ескерту (v5.1 / v5.2): тәуелсіз айнымалы композициялық — *(препроцессинг × pretraining source)*. Әсерді тек препроцессингке немесе тек pretrain-ге бөлу CFC-2.8 бойынша **тыйым салынған**. Dominance шарты: Performance(B′) > max(Performance(A), Performance(C)), EH-3 критерийлерімен (ΔF1 ≥ 5pp, ΔAUC ≥ 0.02, Kappa нашарламайды). v5.0 конфигурациялары B (V5 + ResNet-50 + ImageNet) және D (V5 + EfficientNet-B3 + ImageNet) v5.1-де ретирленген.

**Шығыс:** 5 класс DR саты + explainable attention map (Grad-CAM).

---

## 3. Баяндаушы сөзі

Диаграммада бірінші эксперименттің дизайны көрсетілген — бұл интегралды pipeline-ның (V5 препроцессинг + RETFound pretrain) baseline-нен (stretch-resize + ImageNet pretrain) басымдылығын тексеретін негізгі эксперимент.

v5.2 редакциясында тәуелсіз айнымалы композициялық: *(препроцессинг × pretraining source)*. Бір жағынан препроцессинг өзгереді (baseline vs V5), екінші жағынан pretrain көзі өзгереді (ImageNet vs RETFound). Сондықтан конфигурациялар A, C (baseline + ImageNet) мен B′ (V5 + RETFound) арасында салыстырылады; әрқайсысы EyePACS датасетінде 5-fold кросс-валидациямен оқытылады.

Baseline — ретинопатияны диагностикалаудағы стандартты шешімдер жинағы; негіз ретінде осы бағыттағы ең көп сілтеме алған жұмыстардың бірі — Google-дың 2016 жылғы зерттеу жұмысының архитектурасы алынды (жұмыс ескі болғанымен өзінен кейінгі барлық зерттеу жұмыстары үшін ортақ стандартты бекіткен). V5 тармағында pretrain көзі ретінде **RETFound** қолданылады — ретиналды foundation model, Zhou et al. (2023, Nature) ұсынған, мульти-модальді ретиналды корпуста (≈904K CFP + ≈736K OCT) MAE арқылы алдын ала оқытылған; диссертацияда фундус-тапсырмаға арналған CFP-checkpoint жүктеледі. Pipeline зерттеуде ұсынылған архитектура.

> v5.1 / v5.2 шектеуі (CFC-2.8): нәтиже препроцессингке немесе pretrain-ге жеке тиесілі деп тұжырымдауға болмайды — тек интегралды pipeline-ның (V5 + RETFound) baseline-нен (ImageNet) басымдылығы туралы тұжырым шығаруға рұқсат.