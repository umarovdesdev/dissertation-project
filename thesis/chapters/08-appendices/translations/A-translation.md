# А қосымшасы — Алдын ала өңдеу pipeline-нің бастапқы коды

> Қазақ тіліндегі аударма. Бастапқы мәтін: `drafts/A-draft.md` (writing-session-system-prompt v6.0.0, INVARIANTS.md v6.0.0 негізінде жасалған). Аудару бақылауы: `glossary/GLOSSARY_KZ.md`. Дереккөз: нақты дискідегі ағаш `experiments/src/preprocessing/` (+ `experiments/src/`), `experiments/CLAUDE.md`-да каталогталған; шежіре #19/#21/#23/#24 🔹SELF. **Код-каталог қосымшасы — ешбір эксперименттік нәтиже келтірмейді; әр жол мен үзінді дискіден алынған, ешбірі ойдан шығарылмаған. Бастапқы код ағылшын тілінде қалдырылады (аудармаға жатпайды).**

---

## 1-БӨЛІК: БӨЛІМ МӘТІНІ

§4.1.3 preprocessing pipeline мен оқыту кодын нұсқа бақылауына міндеттеп, оларды осында қайта беруге уәде берді, сонда әр кескінге қолданылған түрлендіру тек прозада сипатталудан гөрі бастапқы код ретінде қалпына келтірілетін болады. Бұл қосымша сол уәдені орындайды. Оны қосу — кездейсоқ құжаттама емес: осы жұмыстың орталық тезисі бойынша — модель preprocessing мен конволюциялық желінің құрамы, сегіз кезеңді pipeline қосалқы деректерді дайындау емес, интегралды модель компоненті — preprocessing бастапқы коды модель сипаттамасының *бөлігі*. Оны қайта беру — сол тезисті жай бекітілгеннен гөрі аудитталатын ететін нәрсе.

Код `experiments/src/` астында Python пакеті ретінде ұйымдастырылған. Preprocessing стегі канондық пакет `experiments/src/preprocessing/`-те орналасқан, оның жария интерфейсі `experiments/src/preprocessing/__init__.py`-дан экспортталады, ал оның оркестраторы, `experiments/src/preprocessing/pipeline.py`-дағы `PreprocessingPipeline`, сегіз кезеңді 3-тарауда көрсетілген тіркелген ретпен тізбектейді. Эксперименттерді қайта беруге қажетті қалған аппарат `experiments/src/`-тің бауырлас ішкі-пакеттері бойынша таратылған: `data/` (деректер жиынтығы жүктеуіштері, пациент-деңгейлі стратификацияланған k-fold бөлгіш, біртұтас augmentation және таңба гармонизациясы), `models/` (ResNet-50 және EfficientNet фабрикалары мен екі кезеңді fine-tuning утилитасы), `training/` (оқыту циклі, кері-жиілік салмақтары бар focal loss және checkpoint басқару), `evaluation/` (метрикалар, калибрлеу және статистикалық тесттер), `explainability/` (Grad-CAM, IoU/ALO және жабын рендерлеу), `experiments/` (жеті эксперимент драйвері) және `utils/` (YAML конфигурациясын өңдеу, қайта жаңғыртылушылық seed утилитасы және кескін-сапасы метрикалары). Төмендегі каталог осы жұмысты ажырататын модель компонентін жүзеге асыратын preprocessing пакетімен шектелген; кеңірек ағаш мұнда тек қайта беру толық локализацияланатын болуы үшін аталады.

A.1-кесте 3-тараудың әр pipeline кезеңін оны жүзеге асыратын модульге салыстырады. Әр жол репозиторий түбіріне қатысты беріледі әрі нұсқаланған бастапқы ағашта бар файлға сәйкес келеді.

**A.1-кесте. Pipeline кезеңі → жүзеге асырушы модуль (`experiments/src/preprocessing/`).**

| Кезең | Сипаттама (3-тар.) | Жүзеге асырушы модуль |
|-------|--------------------|---------------------|
| 0 | Канондық аудару (сол→оң көз бағдары) | `canonical_flip.py`, `canonical_orientation.py` |
| 1 | OD–фовеа айналу нормализациясы | `od_fovea_detect.py`, `canonical_orientation.py` |
| 2 | FOV қию + изотропты 512×512-ге өлшем өзгерту (ортаға нөл-padding) | `crop_resize.py` |
| 3 | FOV маска генерациясы (бинарлық → 4-ші арна) | `crop_resize.py` (маска өлшемі өзгертілген кескінмен қайтарылады) |
| 4 | Жарық-өрісін түзету (адаптивті σ = 0,07·D, маска ішінде) | `flat_field.py` |
| 5 | Қос шектеулі CLAHE (LAB L-арна; оқытуда стохастикалық) | `upgraded_clahe.py`, `polar_clahe.py`, `clahe.py` |
| 6 | Augmentation (біртұтас аффинді + жарықтылық/контраст + PCA түс; тек оқыту) | `experiments/src/data/augmentation_unified.py` |
| 7 | Деректер жиынтығына тән нормалау → tensor (әрқашан соңғы) | `imagenet_normalize.py` |
| — | Конфигурация беті (базалық пен толық-pipeline пресеттері) | `config.py` (`PreprocessingConfig`, `PIPELINE_PRESETS`) |
| — | Кезең оркестрациясы (тіркелген орындау реті) | `pipeline.py` (`PreprocessingPipeline`) |

5-кезең бірден көп модульмен жүзеге асырылады, өйткені pipeline өзінің қазіргі әдепкісі ретінде қос шектеулі CLAHE-нің полярлық нұсқасымен (`polar_clahe.py`), түзусызықты тайлға-негізделген формуляциямен (`upgraded_clahe.py`) қатар жеткізіледі; екеуі де нұсқаланған бастапқы кодта бар әрі каталогталғандай қайта беріледі. 0–5 және 7-кезеңдер оқыту мен inference-те бірдей қолданылады, тек 5-кезең контрастты күшейту оқыту кезінде стохастикалық; 6-кезең augmentation тек оқыту кезінде қолданылады әрі `uint8` кескіндерде жұмыс істеуі үшін 7-кезең нормализациясының алдына енгізіледі. Базалық конфигурация (A және C конфигурациялары) 0–6 кезеңдерді айналып өтіп, орнына қарапайым 512×512-ге созыла-өлшем өзгертуді, содан кейін үш арнада ImageNet нормализациясын pipeline-ді өңдеуден гөрі конфигурация пресеті арқылы таңдай отырып қолданады; толық pipeline (B және D конфигурациялары) сегіз кезеңнің бәрін орындап, төрт арна (RGB плюс FOV маскасы) шығарады.

Бұл каталог оны парафраздаудан гөрі нақты бастапқы кодты қайта беретінін орнықтыру үшін 4-кезең жарық-өрісі модулі `experiments/src/preprocessing/flat_field.py`-дан сөзбе-сөз қайта беріледі:

```python
"""
Stage 4: Flat-Field Correction.

Reduces uneven illumination by subtracting a heavily blurred version of the
image and re-centering at 128:

    corrected = image − GaussianBlur(image, σ) + 128

A large σ captures only the low-frequency illumination gradient, so the
subtraction removes broad brightness variation while preserving local vessel
and lesion detail.

σ is computed adaptively as σ = 0.07 × FOV_diameter.  Correction
is applied only inside the FOV mask (padding pixels are left at zero).

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import cv2
import numpy as np


def apply_flat_field(
    image: np.ndarray,
    sigma: float = 45.0,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    Apply flat-field correction to reduce uneven illumination.

    Algorithm::

        blur      = GaussianBlur(image, σ)
        corrected = image − blur + 128

    When *mask* is provided, correction is applied only inside the mask
    (``mask > 0``). Padding areas (``mask == 0``) are left at zero.

    Kernel size is derived automatically from *sigma* (passed as ``(0, 0)``
    to :func:`cv2.GaussianBlur`).

    Args:
        image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
        sigma: Gaussian blur σ controlling the spatial scale of the
            illumination estimate.
        mask: Optional binary mask of shape ``(H, W)`` (float32 or uint8).
            When provided, only pixels where ``mask > 0`` are corrected;
            padding regions remain zero.

    Returns:
        Corrected RGB uint8 NumPy array of shape ``(H, W, 3)``.
    """
    blur = cv2.GaussianBlur(image, (0, 0), sigma)
    corrected = image.astype(np.float32) - blur.astype(np.float32) + 128.0
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)
    if mask is not None:
        mask_3ch = np.expand_dims(mask > 0, axis=-1).astype(np.uint8)
        corrected = corrected * mask_3ch  # zero out padding
    return corrected
```

Қалған модульдер код базасы үшін орнықтырылған сол конвенцияларды ұстанады — тип-белгіленген қолтаңбалар, `Args`/`Returns` docstring-тері, қатты-кодталудан гөрі конфигурациядан шешілген жолдар және тұтасымен `pathlib.Path` — әрі жинақталған құжатта сол пакеттен толық қайта беріледі. Pipeline шежіресі кандидаттың жаңартылған CLAHE мен preprocessing–жіктеу интеграциясы бойынша бұрын жарияланған жұмысынан тарайды (`yesmukhamedov-scopus-q2.md`/`yesmukhamedov-scopus-q3.md`, `yesmukhamedov-kbtu.md` және конференция мақаласы, 🔹бұрынғы өз жұмысы; SIR-4); осында қайта берілген бастапқы код сол желіні 3-тарауда көрсетілген жалғыз нұсқаланған сегіз кезеңді жүйеге формализациялайды әрі шоғырландырады. §4.1.3-те айтылған аппаратқа-тән қайта жаңғыртылушылық шегімен үйлесімді, бастапқы код баламалы аппаратта қайта жаңғыртылады, бірақ ол көрсететін есептеу-тиімділігі сипаттары құжатталған орнатуға тән болып қалады (DGL-2); оны қайта беру арқылы ешбір өнімділік, дәлдік немесе орналастыру дайындығы тұжырымы жасалмайды. Бастапқы код каталогталып, репрезентативті модуль нақты, дискідегі жүзеге асыру екені көрсетілген соң, §4.1.3-те ашылған қайта жаңғыртылушылық циклі жабылады: тіркелген конфигурация (4.2-кесте), құжатталған аппарат және осы нұсқаланған код бірге эксперименттік pipeline-ді қалпына келтірілетін етеді.

---

### Аудармашы ескертуі

Бастапқы черновиктегі **«PART 3: COMPLIANCE CHECKLIST»** (APP-A AVAILABLE, no-invention rule, CENTRAL_THESIS, reproducibility loop, SIR-4, SIR-1, DGL-2, CFC-2.2/2.4/2.5 және т.б. governance кодтарының аудиті) ағылшын тіліндегі мәтіннен алынған дәйексөздерге (verbatim quotes) сүйенеді, сондықтан аудит-артефакт ретінде ағылшын тіліндегі бастапқы файлда (`drafts/A-draft.md`) сақталады және осы аудармада қайталанбайды. Аударма негізгі мәтінді (1-бөлік) және A.1-кестені қамтиды; бастапқы код блогы (`flat_field.py`) дискідегі түпнұсқа ретінде ағылшын тілінде өзгеріссіз сақталады.
