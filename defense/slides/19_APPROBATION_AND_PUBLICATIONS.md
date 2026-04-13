## 1. Тақырып

Апробация және жарияланымдар

---

## 2. Слайд мазмұны

**Жалпы жарияланымдар саны: 5**

**Ғылыми мақалалар:**

**Scopus (Q3) журналында — 1 мақала:**
- Sapakova S., Yesmukhamedov N., Sapakov A. Development of an Image Quality Enhancement Approach for Diabetic Retinopathy Diagnosis // *Eastern-European Journal of Enterprise Technologies*. — 2025. — Vol. 4, No. 9(136). — P. 79–88. DOI: 10.15587/1729-4061.2025.335570

**ҚР БҒСБК (ВАК) тізіміндегі журналдарда — 3 мақала:**
- Yesmukhamedov N.S., Sapakova S.Z., Kozhamkulova Zh.Zh., Daniyarova D.R., Armankyzy R. Methods for Preprocessing and Analysis of Fundus Images for Diabetic Retinopathy Detection // *Herald of KBTU*. — 2025. — No. 4(75). — P. 119–130. DOI: 10.55452/1998-6688-2025-22-4-119-130
- Yesmukhamedov N.S., Sapakova S., Al-Haddad S.A.R., Daniyarova D. Development of an Information System Architecture for Healthcare Institutions Using Artificial Intelligence // *News of NAN RK, Phys.-Math. Series*. — 2025. — No. 2(354). — P. 74–91. DOI: 10.32014/2025.2518-1726.345
- Сапакова С.З., Данияррова Д.Р., Есмухамедов Н.С., Арманкызы Р., Ембердиева А.Б., Калдыбаева А.С. Mathematical Modeling of Laser Exposure on Fundus Tissues in the Treatment of Diabetic Retinopathy // *Вестник КазУТБ*. — 2024. — Т. 2, No. 27-740. DOI: 10.58805/kazutb.v.2.27-740

**Халықаралық конференциялар:**

**Scopus индекстелетін конференция материалдарында — 1 баяндама:**
- Sapakova S., Yesmukhamedov N., Sapakov A., Yemberdiyeva A., Kozhamkulova Zh. Methods for Pre-processing and Analysis of Fund Images for Detection of Diabetic Retinopathy // *Procedia Computer Science* (Elsevier). — 2025. — Vol. 272. — P. 496–501. DOI: 10.1016/j.procs.2025.10.237. (DS-2025, Istanbul)

---

## 3. Баяндаушы сөзі

Зерттеу жұмысының нәтижелері ғылыми қауымдастықта апробациядан өтті. Жалпы жарияланымдар саны — бесеу.

**Scopus журналында** бір мақала жарияланды. Eastern-European Journal of Enterprise Technologies — Scopus Q3 деңгейіндегі журнал. Мақалада V5 preprocessing pipeline-ның алғашқы нұсқасы мен CNN интеграциясының тиімділігі сипатталған. Preprocessing-тің validation accuracy-ді 71%-дан 86%-ға дейін арттырғаны көрсетілді.

**ВАК журналдарында** үш мақала жарияланды.

Біріншісі — Қазақстан-Британ техникалық университетінің хабаршысы. Мақалада EfficientNetB0 архитектурасымен transfer learning стратегиялары салыстырылған: frozen vs fine-tuning. Fine-tuning test F1-ді 0.62-ден 0.74-ке арттырды.

Екіншісі — ҚР Ұлттық ғылым академиясының хабарлары. Мақалада AI-интеграцияланған денсаулық сақтау ақпараттық жүйесінің архитектурасы ұсынылған — PACS, EHR, телемедицина модульдерімен.

Үшіншісі — Қазақ технология және бизнес университетінің хабаршысы, 2024 жылы жарияланған. Мақала диабеттік ретинопатияны емдеуде лазерлік әсердің математикалық модельдеуіне арналған — жылу өткізгіштік теңдеуі мен Бир заңы арқылы.

**Халықаралық конференцияда** бір баяндама жасалды. DS-2025 конференциясы, Стамбул — Procedia Computer Science (Elsevier), Scopus индекстелетін. Баяндамада fundus суреттерін preprocessing пен талдау әдістері баяндалған.

Барлық жарияланымдар диссертациялық зерттеудің әр түрлі аспектілерін қамтиды: preprocessing pipeline, CNN classification, жүйе архитектурасы, лазерлік модельдеу және transfer learning.

---

## 4. Қосымша

- **Scopus Q3 мақала (Eastern-European J. of Enterprise Technologies, 2025)** — диссертацияның preprocessing + CNN интеграциясы тезисін алғаш жариялаған жұмыс. APTOS 2019 датасетінде baseline CNN (256×256, preprocessing-сіз) мен enhanced CNN (512×512, CLAHE + augmentation) салыстырылған. Enhanced модель: accuracy 91%, ROC-AUC 0.9638. Бұл мақала диссертацияның C-1 үлесінің (cross-device pipeline) алдын ала нұсқасын сипаттайды. CC BY лицензиясы бойынша жарияланған.
- **Scopus конференция (Procedia Computer Science, DS-2025, Istanbul)** — EfficientNetB0-мен transfer learning зерттеуі. Frozen layers (Method 1): Test F1=0.62, Fine-tuning (Method 2): Test F1=0.74, Δ=+12pp. APTOS 2019 + жеке клиникалық деректер, барлығы 35 126 оқыту суреті. Класс теңгерімсіздігі мәселесі қаралған: DR 0 = 73.5%, DR 3 = 2.5%.
- **ВАК — Herald of KBTU, No. 4(75), 2025** — Scopus конференция мақаласымен ұқсас тақырып, бірақ қазақ тілінде кеңейтілген нұсқа. EfficientNetB0 fine-tuning стратегиясы, cross-validation нәтижелері, Cohen's Kappa (quadratic weights) метрикасы қолданылған.
- **ВАК — News of NAN RK, Phys.-Math. Series, No. 2(354), 2025** — AI-негізді денсаулық сақтау ақпараттық жүйесінің архитектурасы. UML диаграммалары, PACS, EHR, CDSS компоненттері, DMP таксономиясы. Қазақстанда ~1200 офтальмолог, тұрғындардың 40%+ ауылды аймақтарда тұрады — бұл контекст жүйенің қажеттілігін негіздейді. Эмпирикалық эксперимент жоқ — архитектуралық жоба.
- **ВАК — Вестник КазУТБ, 2024** — лазерлік коагуляцияның математикалық модельдеуі. Бір заңы (Beer's law), жылу өткізгіштік теңдеуі, Gaussian beam профилі. Explicit finite difference әдісі Python-да іске асырылған. Бұл мақала диссертацияның DR емдеу контекстін кеңейтеді, бірақ preprocessing + CNN classification тақырыбына тікелей қатысы жоқ.
- **Жарияланымдардың диссертациямен байланысы** — 5 жарияланым диссертацияның келесі бөлімдерін қамтиды: (1) Preprocessing pipeline мен CNN интеграциясы → Scopus Q3 мақала; (2) Transfer learning стратегиялары → Scopus конф. + KBTU; (3) Жүйе архитектурасы → NAN RK; (4) Лазерлік модельдеу → КазУТБ. Барлығы 2024–2025 жылдары жарияланған, диссертация жазылу кезеңінде.
- **yesmukhamedov-scopus-q2.md файлы** — бұл файл yesmukhamedov-scopus-q3.md-мен бірдей библиографиялық сілтемені қамтиды (Eastern-European J. of Enterprise Technologies), бірақ Unique ID-сі `LC-AlTimemy-2021` деп қате белгіленген. Бұл бөлек Q2 жарияланым емес — дубликат/қате белгіленген файл. Нақты жарияланымдар саны: 5.

