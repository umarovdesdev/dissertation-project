## 1. Тақырып

V5 Preprocessing Pipeline — 8 кезең

---

## 2. Слайд мазмұны

| Кезең | Операция | Кілтті параметр | Режим |
|-------|----------|-----------------|-------|
| 0 | Canonical flip (left -> right) | metadata laterality | always |
| 1 | OD-fovea ротациялық нормализация | OD/fovea detection | always |
| 2 | FOV crop + isotropic resize + zero-pad | 512 x 512 | always |
| 3 | FOV mask generation | threshold -> binary | always |
| 4 | Adaptive flat-field correction | sigma = 0.07 * D | always |
| 5 | Dual-constraint CLAHE (LAB L-channel) | clip=2.0, tile=8x8 | always |
| 6 | Augmentation (affine + PCA color) | train only | train |
| 7 | Normalize + FOV mask append | dataset-specific mu, sigma | always |

**Кіріс:** raw fundus RGB uint8 --> **Шығыс:** 4 x 512 x 512 float32

**Baseline:** stretch-resize 512x512 + ImageNet normalize --> 3 x 512 x 512

E:\dissertation-project\defense\assets\11_architecture_diagram.svg

---

## 3. Баяндаушы сөзі

V5 pipeline 8 кезеңнен тұрады. Stage 0 — сол көзді оң көз бағдарына айналдырады. Stage 1 — optic disc пен fovea арасындағы осьті горизонтальға туралайды. Stage 2 — FOV аймағын қиып, изотропты resize 512x512-ге келтіреді, zero-padding қолданады. Stage 3 — FOV масканы генерациялайды, 4-ші канал ретінде қосылады. Stage 4 — адаптивті flat-field түзету, sigma FOV диаметріне пропорционал. Stage 5 — dual-constraint CLAHE, LAB L-каналында жергілікті контрастты арттырады. Stage 6 — аугментация, тек оқыту кезінде. Stage 7 — dataset-specific нормализация. Шығыс — 4 каналды тензор. Baseline тек stretch-resize және ImageNet нормализация қолданады.
