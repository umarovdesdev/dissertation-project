## 1. Тақырып

Жүйе архитектурасы және деректер ағыны

---

## 2. Слайд мазмұны

**V5 Preprocessing Pipeline (P) — 8 кезең:**

| Кезең | Операция | Кілтті параметр | Шығыс |
|-------|----------|-----------------|-------|
| 0 | Canonical flip (left → right eye) | metadata laterality | RGB uint8 |
| 1 | OD-fovea ротациялық нормализация | OD/fovea detection | RGB uint8 |
| 2 | FOV crop + isotropic resize + zero-pad | 512 x 512 | RGB uint8 |
| 3 | FOV mask generation | threshold → binary | float32 mask |
| 4 | Adaptive flat-field correction | σ = 0.07 · D | RGB uint8 |
| 5 | Dual-constraint CLAHE (LAB L-channel) | clip=2.0, tile=8x8 | RGB uint8 |
| 6 | Augmentation (affine + PCA color) | **train only** | RGB uint8 |
| 7 | Normalize + FOV mask append | (μ, σ) dataset-specific | **4 x 512 x 512** |

**CNN Classifier (θ):**

|  | ResNet-50 | EfficientNet-B3 |
|--|-----------|-----------------|
| Conv1 кіріс | 4ch → 64, kernel 7x7 | 4ch → 40, kernel 3x3 |
| Feature dim | 2048 | 1536 |
| Spatial map | 2048 x 16 x 16 | 1536 x 16 x 16 |
| Mixed precision | ON | OFF (fp16 overflow) |

**Classification head:** GAP → Dropout(0.4) → Linear(d, 5) → Softmax → DR 0–4

**Patient-level aggregation (Φ):**

$$I'_L = \mathcal{P}(I_L, s_L), \quad I'_R = \mathcal{P}(I_R, s_R)$$

$$\hat{y}_L = \text{CNN}(I'_L), \quad \hat{y}_R = \text{CNN}(I'_R)$$

$$\hat{y}_{\text{patient}} = \max(\hat{y}_L,\; \hat{y}_R)$$

**Training:** Focal Loss (γ=2, α=inverse-freq) | Adam lr=1e-4 | batch 16 | 5-fold patient-level CV | early stop patience=5

E:\dissertation-project\defense\assets\11_architecture_diagram.svg

---

## 3. Баяндаушы сөзі

**Preprocessing pipeline** — 8 кезең. Raw fundus суреті қабылдап, CNN-ге дайын 4 каналды тензор қайтарады. 

Stage 0 — канондық flip: сол көзді оң көз бағдарына айналдырады, латералдық вариацияны жояды. 
Stage 1 — optic disc пен fovea арасындағы осьті горизонтальға туралайды, ротациялық вариацияны жояды. 
Stage 2 — FOV аймағын қиып, изотропты resize арқылы 512 x 512-ге келтіреді; baseline-дағы stretch-resize-дан айырмашылығы — fundus геометриясын бұзбайды, zero-padding қолданылады. 
Stage 3 — FOV масканы генерациялайды: нақты fundus пиксельдері фоннан ажыратылып 4-ші канал ретінде CNN-ге жіберіледі.
Stage 4 — адаптивті flat-field түзету. Кілтті параметр: σ = 0.07 · D, мұнда D — FOV диаметрі пиксельде. σ сурет геометриясына бейімделеді. 
Stage 5 — Upgrated CLAHE: бұл LAB түстер кеңістігінде L-каналының жергілікті контрастты арттырады, микроаневризмалар мен экссудаттарды(тамырлардан шыққан липидтер (майлар) мен ақуыздар) айқындайды. 
Stage 6 — аугментация: тек оқыту кезінде қосылады. Optic disc пен fovea кескіндерінің радиус өлшеміне тәуелді мәндермен жасалады.
Stage 7 — dataset-specific нормализация және FOV масканы 4-ші канал ретінде қосу; шығыс — float32 тензор, 4 x 512 x 512.

**CNN classifier.** 5 классқа жіктейді.

**Patient-level aggregation.** Диабеттік ретинопатия — билатералды ауру: бір пациенттің екі көзі ортақ жүйелік тәуекел факторларын бөліседі, бірақ жергілікті патология әртүрлі болуы мүмкін. Клиникалық практикада скрининг шешімі пациент деңгейінде қабылданады. 

Ұсынылған әдістің көздер арасындағы өзара қатынасын CNN ішінде модельдеу тәсілдерінен айырмашылығы тәуелділікті айқын әрі жеке әзірлеуге болады.

Мұндай тәсіл көздер арасындағы тәуелділікті айқын бақылауға және классификация процесіне априорлық медициналық білімді енгізуге мүмкіндік береді.

**Training конфигурациясы:** Focal Loss — класс теңгерімсіздігіне қарсы. 5-fold patient-level cross-validation — бір пациенттің барлық суреттері (сол + оң көз) бір fold-та, data leakage болмайды. Early stopping — артық оқудың алдын алу.

---

## 4. Қосымша

- **Isotropic resize** — кескіннің пропорциясын сақтай отырып масштабтау + zero-padding. Stretch-resize (baseline) кескін геометриясын бұзады, isotropic resize fundus шеңберінің пішінін сақтайды.
- **FOV (Field of View) mask** — бинарлық кеңістіктік маска: 1.0 = fundus пиксельдері, 0.0 = zero-padding. CNN-ге нақты деректер мен фон арасын ажыратуға мүмкіндік береді.
- **Flat-field correction** — кескін бетіндегі біркелкі емес жарықтандыруды (vignetting, жарық градиенттері) жоятын әдіс. Формуласы: I' = I − GaussianBlur(I, σ) + 128. Адаптивті σ = 0.07·D — FOV диаметріне пропорционал.
- **Dual-constraint CLAHE** — стандартты CLAHE-дан айырмашылығы: clip limit екі шектеумен бақыланады — clip_factor (жергілікті) және global_threshold (жаһандық). Бұл over-enhancement artifact-тарының алдын алады.
- **LAB L-channel** — жарықтық каналында ғана CLAHE қолданылады, түс ақпараты (A, B каналдары) бұзылмайды.
- **Conv1 модификациясы** — стандартты 3ch conv қабат 4ch-ға кеңейтіледі. RGB салмақтары ImageNet pretrained-тен көшіріледі, 4-ші канал (mask) RGB салмақтарының ортасымен инициализацияланады.
- **GAP (Global Average Pooling)** — spatial feature map-ты (d x 16 x 16) feature vector-ға (d) қысқартады; әр каналдың кеңістіктік ортасы алынады.
- **Focal Loss** — FL = −α(1−p_t)^γ · log(p_t). γ=2 кезінде оңай мысалдардың (p_t ≈ 0.9) градиент үлесі 100× азаяды. α = inverse-frequency class weights — сирек класстарға (DR 1, 3, 4) жоғары салмақ.
- **Patient-level CV** — бір пациенттің барлық суреттері (сол + оң көз) бір fold-та. PatientLevelKFold splitter max DR grade бойынша стратификация жасайды. Data leakage болмайды.
- **Mixed precision** — ResNet-50 үшін ON (жад үнемделеді, жылдамдық артады), EfficientNet-B3 үшін OFF (fp16 overflow мәселесіне байланысты).
- **Patient-level aggregation (Φ)** — пациенттің екі көзін жеке жіктеп, нәтижесін біріктіру стратегиясы. V5-те Max-Grade қолданылады.
- **Max-Grade стратегиясы** — ŷ_patient = max(ŷ_L, ŷ_R). Қосымша оқытылатын параметрлер жоқ. Клиникалық практикаға сәйкес: скрининг шешімін ауыр көз анықтайды.
- **Shared weights** — екі көздің суреттері бір CNN backbone арқылы өңделеді (параметрлер ортақ). Бұл билатералды симметрияны қамтамасыз етеді.
- **Bilateral disease** — DR екі көзде де дамиды, бірақ асимметриялы: бір көз DR 3 болса, екіншісі DR 1 болуы мүмкін. Пациент деңгейіндегі шешім осыны ескереді.
