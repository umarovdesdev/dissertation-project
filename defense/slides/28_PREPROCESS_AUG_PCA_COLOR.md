## 1. Тақырып

Аугментация: PCA түс jitter

---

## 2. Слайд мазмұны

![Stage 6: Аугментация — PCA түс jitter](../assets/preprocessing/23_aug_pca_color/stage6_augmentation.png)

![Min PCA color jitter](../assets/preprocessing/23_aug_pca_color/left_min.png)
![Max PCA color jitter](../assets/preprocessing/23_aug_pca_color/left_max.png)

![PCA jitter таралымы](../assets/preprocessing/23_aug_pca_color/distribution.png)

---

## 3. Баяндаушы сөзі

Бұл аугментацияда кескіннің түс каналдары кездейсоқ аздап өзгертіліп беріледі. Әр камера түсті сәл өзгеше жеткізетіндіктен, осы вариация арқылы модель түске емес, тор қабықтың құрылымдық белгілеріне сүйеніп шешім қабылдауға үйренеді. 

Жарық суретке түсірудегі ең ойналмалы фактор болғандықтан аугментация кезінде де ең агрессивті кезең.
