## 1. Тақырып

Модель

---

## 2. Слайд мазмұны

**Орталық тұжырым:**

$$\text{model} = \mathcal{P}(\text{preprocessing}) + \text{CNN}_\theta$$

**Қолданыстағы тәсіл** — preprocessing модельден тыс, тек деректер дайындау сатысы:

$$\text{data} = \text{prep}(I) \quad \rightarrow \quad \hat{y} = \text{CNN}(\text{data})$$

**Ұсынылған тәсіл** — preprocessing модельдің ажырамас компоненті, feature space-ті анықтайды:

$$\hat{y} = \text{CNN}_\theta(\;\mathcal{P}(I,\; s)\;)$$

**2 x 2 факторлық эксперимент (Exp 1):**

|  | Baseline (3ch) | Fullline (4ch) |
|--|----------------|----------------|
| **ResNet-50** | A | B |
| **EfficientNet-B3** | C | D |

**Доминанттылық критерийі (EH-3):** ΔF1 ≥ 5pp, ΔAUC ≥ 0.02, κ деградациясыз

E:\dissertation-project\defense\assets\07_model_diagram.svg

---

## 3. Баяндаушы сөзі

Ұсынылған модельдің тұжырымдамалық негізі — preprocessing пен CNN-ді біртұтас модель ретінде қарастыру.

Қолданыстағы зерттеулерде preprocessing тек деректер дайындау сатысы ретінде қарастырылады — resize, нормализация жасалып, нәтиже CNN-ге жіберіледі. Бұл тәсілде preprocessing модельден тыс, оның CNN-нің feature кеңістігіне әсері бақылаусыз қалады.

Зерттеуде ұсынылған тәсілде preprocessing модельдің ажырамас компоненті: pipeline fundus суреттің геометриясын, жарықтандыруын және контрастын стандарттайды әрі CNN-ге қолжетімді белгілер кеңістігін анықтайды. Pipeline-сыз CNN қарапайым feature space-те жұмыс істейді — бұл базалық модель.

Тұжырымды тексеру үшін 2 x 2 факторлық дизайн құрылды: екі preprocessing деңгейі — Baseline және Fullline, екі CNN архитектурасы — ResNet-50 және EfficientNet-B3. Нәтижесінде 4 конфигурация: A, B, C, D. Доминанттылық критерийі — үш шарт бір мезгілде орындалуы тиіс: F1-ге 5 пайыздық пункттен артық өсім, AUC-қа 2 пункт өсім, және Cohen kappa деградациясыз.

---

## 4. Қосымша

- **model = P + CNN** — зерттеудің орталық тұжырымы: preprocessing модельдің ажырамас компоненті, жеке қарастырылатын деректер дайындау сатысы емес.
- **P (V5 pipeline)** — 8 кезеңді алдын ала өңдеу pipeline-ы; кіріс: raw fundus (RGB uint8), шығыс: 4-каналды тензор (4 x 512 x 512, float32).
- **Feature space** — CNN-нің «көретін» белгілер кеңістігі. Pipeline feature space-ті анықтайды: сол суретті әртүрлі pipeline-мен өңдесең — CNN әртүрлі белгілер көреді.
- **2 x 2 факторлық дизайн** — екі тәуелсіз фактор (preprocessing, CNN) бір мезгілде тексеріледі; бұл main effect пен interaction effect-ті бөлуге мүмкіндік береді.
- **Baseline (3ch)** — stretch-resize 512 x 512 + ImageNet нормализация; 3 RGB канал. Салыстыру үшін контроль жағдай.
- **Fullline (4ch)** — 8 кезеңді pipeline; 4 канал: RGB + FOV mask. Эксперименттік жағдай.
- **Доминанттылық критерийі (EH-3)** — ΔF1 ≥ 5 percentage points, ΔAUC ≥ 0.02, no κ degradation. Үш шарт бір мезгілде орындалуы тиіс — бір метриканың жоғары болуы жеткіліксіз.
- **ResNet-50** — 50 қабатты residual network; skip connection арқылы терең желілерді оқытуға мүмкіндік береді; feature dim = 2048.
- **EfficientNet-B3** — compound scaling (тереңдік + ені + рұқсат); MBConv + SE attention; feature dim = 1536.
