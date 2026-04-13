## 1. Тақырып

Зерттеудің негізгі қорытындылары

---

## 2. Слайд мазмұны

**Орталық тезис расталды:**
> Model = Preprocessing + CNN. 8-кезеңді preprocessing pipeline, CNN-ге қолжетімді feature кеңістігін анықтап тәуелсіз — robust main effect (ANOVA p<0.001, interaction p=0.23 n.s.).

**6 гипотезаның расталу нәтижесі:**

| Гипотеза | Не тексерілді | Негізгі дәлелдеме | Күйі |
|----------|---------------|-------------------|------|
| **H-1** | Preprocessing доминанттылығы | EH-3: ResNet +5.2/+3.3/+8.0; EfficientNet +5.3/+4.4/+8.0 — екеуінде де расталды | **Расталды** |
| **H-2** | Компонент ablation + CLAHE оптимумы | CLAHE +1.4pp маржиналды; clip=2.0–2.5, σ=0.07·D | **Расталды** |
| **H-4** | Cross-dataset тасымалдаушылық | Config D: G=0.890, Config B: G=0.861 — екеуі де ≥ 0.85 | **Расталды** |
| **H-5** | Түсіндірмелілік (ALO) | ALO +31–61%, IoU +50–83% (4 зақым типі) | **Расталды** |
| **H-6** | Құрылғы domain shift | Cross-device variance −46% (4 камера) | **Расталды** |
| **H-7** | Клиникалық деградация | Δ: IDRiD −24%, Messidor-2 −22% | **Расталды** |

**Ғылыми үлес (3 негізгі + 6 қосымша):**

| # | Үлес | Дәлелдеме |
|---|------|-----------|
| **C-1** | Cross-device нормализация pipeline (V5, 8 кезең, 4-канал) | Exp 1, 2, 6 |
| **C-2** | Cross-dataset жалпылау дәлелдемесі (G ≥ 0.85) | Exp 3 |
| **C-3** | Зақым feature-ларын сақтау талдамасы (ALO метрикасы) | Exp 4 |

**Қосымша:** SC-A — Adaptive CLAHE (dual-constraint), SC-B — CLAHE sensitivity сипаттамасы, SC-C — Cross-device тұрақтылық бағалауы, SC-D — Adaptive flat-field (σ=0.07·D), SC-E — FOV mask 4-канал, SC-F — OD-fovea rotation

---

## 3. Баяндаушы сөзі

Зерттеудің негізгі қорытындыларын тұжырымдаймын.

**Орталық тезис расталды.** "Model = preprocessing + CNN" — бұл зерттеудің фундаменталды тұжырымы. 7 эксперимент, 8 датасет және 62 мыңнан астам fundus суреті бойынша жүргізілген зерттеу көрсетті: preprocessing — модельдің сыртқы деректер дайындау қадамы емес, CNN-ге қолжетімді feature кеңістігін анықтайтын интегралды компонент.

Ең маңызды табыс — preprocessing-тің **архитектурадан тәуелсіз** robust main effect екені. ANOVA preprocessing main effect p<0.001, ал interaction term p=0.23 — маңызды емес. Бұл ResNet-50 де, EfficientNet-B3 де preprocessing-тен бірдей деңгейде пайда алатынын дәлелдейді. V5 pipeline — архитектура-агностикалық шешім.

**Барлық алты гипотеза расталды.**

H-1 — preprocessing доминанттылығы. **Екі архитектурада да** EH-3 доминанттылық критерийі орындалды. ResNet-50: ΔF1=+5.2 пайыздық пункт, ΔAUC=+3.3 пункт, Δκ=+8.0 пункт. DeLong p=0.006, McNemar p=0.009. EfficientNet-B3: ΔF1=+5.3 пункт, ΔAUC=+4.4 пункт, Δκ=+8.0 пункт. DeLong p=0.008, McNemar p=0.012. Config D ең жоғары абсолютті нәтижеге жетті — F1=0.780.

H-2 — компонент ablation. Pipeline-ның 7 кезеңі бір-бірлеп F1-ді baseline 0.727-ден толық V5 0.780-ге дейін арттырады. CLAHE — ең ірі маржиналды үлес, 1.4 пайыздық пункт. CLAHE мен flat-field параметр sweep нәтижесінде тривиальсыз sensitivity surface табылды — clip_factor=2.0-2.5 аймағында жергілікті оптимум, σ=0.07 мал FOV диаметрі оптимум.

H-4 — cross-dataset тасымалдаушылық. EyePACS-те оқытылған модельдер APTOS 2019-да zero-shot режимде тексерілді. **Екі pipeline конфигурациясы да** H-4 шегін орындады: Config D G=0.890, Config B G=0.861 — екеуі де 0.85-тен жоғары. Baseline конфигурациялар (A: G=0.812, C: G=0.820) орындамады. Preprocessing domain gap-ін стандарттайды.

H-5 — түсіндірмелілік. Grad-CAM мен IDRiD зақым маскалары бойынша ALO метрикасы 4 зақым типінде 31 пайыздан 61 пайызға дейін жақсарды. Preprocessing модельдің назарын клиникалық маңызды зақым аймағына бағыттайды. Attention consistency датасеттер арасында 0.61-ден 0.81-ге көтерілді.

H-6 — құрылғы domain shift. Canon, Topcon, Kowa және Zeiss камераларын қамтитын 3 сыртқы датасетте cross-device F1 дисперсиясы 46 пайызға қысқарды. Pipeline камера өндірушісіне тәуелсіз тұрақты нәтиже береді.

H-7 — клиникалық деградация. EyePACS-тен IDRiD-ке ауысқанда деградация 11.9 пайыздық пункттен 9.0-ға азайды — 24 пайызға. Messidor-2-де 10.2-ден 8.0-ге — 22 пайызға. Pipeline сыртқы датасеттерде нашарлауды азайтады.

**Ғылыми үлес тұрғысынан** зерттеу үш негізгі және алты қосымша үлес қосады.

Бірінші негізгі үлес — C-1 — cross-device нормализация pipeline-ның жобалануы, іске асырылуы және эксперименттік валидациясы. V5 pipeline бес жаңалық енгізеді: изотропты resize, FOV mask 4-канал ретінде, adaptive flat-field σ, dataset-specific нормализация, және OD-fovea rotation.

Екінші — C-2 — cross-dataset жалпылау дәлелдемесі. G ≥ 0.85 шегімен алдын ала тіркелген тасымалдаушылық критерийі тәуелсіз APTOS 2019 датасетінде екі pipeline конфигурациясында да расталды.

Үшінші — C-3 — зақым feature-ларын сақтау талдамасы. ALO метрикасы арқылы preprocessing-тің CNN назарын зақым аймағына бағыттайтыны сандық дәлелденді. Бұл — preprocessing-тің "неліктен жұмыс істейтінін" түсіндіретін дәлелдеме.

Қосымша үлестер: adaptive CLAHE dual-constraint формулациясы, CLAHE sensitivity сипаттамасы, cross-device тұрақтылық бағалауы, adaptive flat-field нормализациясы, FOV mask pipeline компоненті ретінде, және OD-fovea rotation нормализациясы.

---

## 4. Қосымша

- **Орталық тезис формулациясы** — "Model = preprocessing + CNN" — preprocessing модельдің ажырамас бөлігі, CNN-ге қолжетімді feature кеңістігін анықтайды. Бұл тұжырым 7 эксперимент, 8 датасет, 5 камера өндірушісінде расталды. Preprocessing robust main effect ретінде расталды (ANOVA p<0.001, interaction p=0.23 n.s.) — preprocessing-тің пайдасы архитектурадан тәуелсіз.
- **EH-3 доминанттылық критерийі** — ΔF1 ≥ 5pp ∧ ΔAUC ≥ 0.02 ∧ Δκ > 0. Үш шарт бір мезгілде. ResNet-50: +5.2pp, +3.3pp, +8.0pp — орындалды. EfficientNet-B3: +5.3pp, +4.4pp, +8.0pp — орындалды. Екі архитектурада да EH-3 расталуы preprocessing-тің universal benefit екенін көрсетеді.
- **H-3 тағдыры** — H-3 гипотезасы V3 нұсқасында алынып тасталды. Қалған гипотезалар: H-1, H-2, H-4, H-5, H-6, H-7.
- **ANOVA нәтижелері** — Mixed-effects ANOVA (fold = random effect): preprocessing main effect p<0.001 (маңызды), architecture main effect (маңызды — EfficientNet абсолютті F1-де ResNet-тен жоғары), preprocessing × architecture interaction p=0.23 (маңызды емес). Interaction маңызды еместігі: preprocessing пайдасы архитектура бойынша айтарлықтай ерекшеленбейді. EfficientNet-B3 +5.3pp vs ResNet-50 +5.2pp — тек 0.1pp айырмашылық.
- **Config D vs Config B** — Config D (EfficientNet-B3 + V5): F1=0.780, AUC=0.865, κ=0.700. Config B (ResNet-50 + V5): F1=0.776, AUC=0.863, κ=0.698. Абсолютті айырмашылық аз — F1-де 0.4pp, AUC-де 0.2pp. Бірақ EfficientNet-B3 параметрлер бойынша 2× тиімді (12.2M vs 25.6M), GPU жадында 6.9GB vs 4.3GB.
- **C-1 жаңалықтары (5 пункт)** — (a) isotropic resize centered zero-padding: fundus шеңберінің геометриясын сақтайды, stretch-resize сияқты деформация болмайды; (b) FOV mask 4-канал: CNN-ге жарамды пиксел аймағы туралы ақпарат береді, padding артефактілерін оқымауды қамтамасыз етеді; (c) adaptive flat-field σ=0.07·D: FOV диаметріне пропорционал, әр суреттің геометриясына бейімделеді; (d) dataset-specific нормализация: ImageNet статистикасы орнына training set mask=1.0 пиксельдерінен есептелген mean/std; (e) OD-fovea rotation: ретиналды бағдарды стандарттайды, detection confidence-ке бейімделетін augmentation σ.
- **C-2 алдын ала тіркелген шек** — G ≥ 0.85 шегі RESEARCH_ARCHITECTURE-да эксперименттер жүргізілмес бұрын анықталған. Post-hoc таңдалған шек емес — бұл зерттеу дизайнының бөлігі. Екі pipeline config те (B: G=0.861, D: G=0.890) осы шекті орындады.
- **C-3 ALO метрикасы** — ALO = |GradCAM ∩ lesion| / |lesion|. Асимметриялық метрика — зақым жағынан бағалайды. IoU-дан айырмашылығы: ALO GradCAM-ның зақымнан тыс кеңейгенін ескермейді, тек зақымның қамтылуын өлшейді. Бұл клиникалық контекстте маңызды: дәрігерді зақымды жіберіп алу қауіпі қызықтырады.
- **SC-A Dual-constraint CLAHE** — clip_limit = min(clip_factor × tile_area/256, global_threshold × tile_area). Екі шектеу: (1) стандартты clip_factor × tile_area/256, (2) глобалды шек global_threshold × tile_area. Minimum алынады — OD (optic disc) аймағында over-enhancement-тің алдын алады. Stochastic p=0.8: оқыту кезінде 80% ықтималдықпен қолданылады — регуляризация эффектісі.
- **SC-D Adaptive flat-field** — corrected = image − GaussianBlur(image, σ) + 128, мұнда σ = 0.07 × FOV_diameter. Fixed σ=45 (V4) орнына FOV диаметріне пропорционал σ (V5). Тек FOV mask=1.0 аймағында қолданылады — padding артефактілерін болдырмайды.
- **Қайта өндірілу** — seed=42, deterministic=true, тұрақты аугментация, patient-level CV. Код мен конфигурация GitHub-та қолжетімді. Барлық эксперименттер бір GPU-да (RTX 3060 12GB) жүргізілді — нәтижелер қайта өндірілуі қамтамасыз етілген.
- **8 датасет рөлдері** — EyePACS: оқыту (Exp 1-6); APTOS: zero-shot transfer (Exp 3); IDRiD: ALO + оқыту (Exp 4, 5, 7); Messidor-2: degradation (Exp 5); DDR/ODIR/RFMiD: device shift (Exp 6); Clinical: жергілікті валидация (Exp 4, 5, 7).
