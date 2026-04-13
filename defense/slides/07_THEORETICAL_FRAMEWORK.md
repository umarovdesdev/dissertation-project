## 1. Тақырып

Теориялық негіздеме: model = preprocessing + CNN

---

## 2. Слайд мазмұны

**Қолданыстағы тәсіл** — preprocessing модельден тыс:

$$\text{data} = \text{prep}(I) \;\rightarrow\; \hat{y} = \text{CNN}(\text{data})$$

**Ұсынылған тәсіл** — preprocessing модельдің компоненті:

$$\hat{y} = \text{CNN}_\theta(\;\mathcal{P}(I,\; s)\;)$$

**Себептік тізбек:**

V5 preprocessing --> микроваскулярлы feature көрінуі --> CNN feature extraction тұрақтылығы --> DR classification жақсаруы

**2x2 факторлық дизайн** — main effect пен interaction бөлу:

|  | Baseline (3ch) | Full V5 (4ch) |
|--|----------------|---------------|
| **ResNet-50** | A | B |
| **EfficientNet-B3** | C | D |

E:\dissertation-project\defense\assets\07_model_diagram.svg

---

## 3. Баяндаушы сөзі

Зерттеудің теориялық негізі — preprocessing пен CNN-ді біртұтас модель ретінде қарастыру. Қолданыстағы тәсілде preprocessing модельден тыс, тек деректерді дайындау. Біздің тәсілде preprocessing CNN-нің feature space-ін анықтайды. Себептік тізбек: preprocessing микроваскулярлы зақымдардың көрінуін арттырады, бұл CNN feature extraction-ды тұрақтандырады, нәтижесінде classification жақсарады. Тұжырымды тексеру үшін 2x2 факторлық дизайн құрылды — екі preprocessing деңгейі мен екі CNN архитектурасы. Бұл main effect пен interaction effect бөлуге мүмкіндік береді.
