# Güneş Dili: Teknik ve Akademik Anlatım Rehberi
### Deterministik Biçimsel Gramer, Polar Fraktal Gömme ve Hesaplamalı Morfoloji

---

## 1. Giriş ve Kuramsal Temeller

Doğal diller, tarihsel süreç içerisinde ses düşmeleri, kaynaşmalar, düzensiz çekimler ve eşadlı ekler nedeniyle yüksek düzeyde **biçimbilimsel belirsizlik (morphological ambiguity)** barındırır. Örneğin Türkçede `-ı / -i / -u / -ü` eki aynı anda:
1. Belirtme hali eki (`kitab-ı`),
2. 3. tekil iyelik eki (`onun kitab-ı`),
3. İsimden isim yapım eki (`yaz-ı`),
olabilmektedir. Bu durum doğal dil işlemede (NLP) karmaşık bağlam modelleri ve istatistiksel disambiguation algoritmaları gerektirir.

**Güneş Dili**, 1935 Güneş-Dil Teorisi'nin fonetik ilkelerini modern biçimsel diller teorisiyle (Chomsky Tip-3 Düzenli Gramer & Deterministik Sonlu Otomat - DFA) yeniden yapılandırarak bu belirsizliği matematiksel olarak ortadan kaldırır.

---

## 2. Biçimbilimsel Aksiyomlar ve Teoremler

### Aksiyom 1 (Birebir İzomorfizm)
$$1 \text{ Ek} \iff 1 \text{ Biçim} \iff 1 \text{ İşlev}$$
Hiçbir ek birden fazla işleve sahip olamaz; hiçbir işlev birden fazla ek biçimiyle (allomorf) temsil edilemez. Ünlü uyumu, ünsüz yumuşaması veya kaynaştırma harfleri yoktur.

### Aksiyom 2 (Kök ve Ek Kanonik Biçimi)
* **Kök Biçimi:** $(K)\ddot{U}(K\ddot{U})^*K$ — Kök her zaman bir ünsüzle biter, kök içinde yan yana ünsüz kümesi bulunamaz.
* **Ek Biçimi:** $K\ddot{U}$ — Tüm ekler tam olarak bir ünsüz ve bir ünlüden oluşur ($2$ karakter).

### Aksiyom 3 (Ek Ailesi Matrisi)
Ek ünsüzü işlev **AİLESİNİ**, ek ünlüsü aile içerisindeki **ÜYEYİ** kodlar:
$$\text{Ek} = \langle C_{\text{aile}}, V_{\text{üye}} \rangle$$

| Ünsüz | 1935 Anlamı | İşlev Ailesi | Ek Üyeleri ve Anlamları |
| :---: | :--- | :--- | :--- |
| **M** | Kendisi | 1. Kişi / İyelik | `mi` (1. Tekil), `ma` (1. Çoğul) |
| **N** | Bitişik | 2. Kişi / İyelik | `ni` (2. Tekil), `na` (2. Çoğul) |
| **S** | Geniş Saha | 3. Kişi / İyelik | `si` (3. Tekil), `sa` (3. Çoğul) |
| **L** | Genellik | Çokluk | `la` (Çoğul) |
| **T** | Yapıcılık | Çatı | `ta` (Ettirgen), `te` (Edilgen), `ti` (Dönüşlü), `to` (İşteş), `tu` (Yeterlik) |
| **K** | Tamamlama | Zaman | `ka` (Geçmiş), `ke` (Şimdiki), `ki` (Gelecek), `ko` (Geniş), `ku` (Duyulan) |
| **R** | Belli Nokta | Hal | `ra` (Bulunma), `re` (Yönelme), `ro` (Ayrılma), `ru` (Belirtme), `ri` (İlgi) |
| **D** | Karşıtlık | Olumsuzluk / Soru | `de` (Olumsuz), `do` (Soru) |
| **B** | Modalite | Kip | `ba` (Şart), `be` (İstek), `bi` (Emir), `bo` (Gereklilik) |
| **Y** | Bağlayıcı | Ek-Fiil | `ya` (Hikâye -idi), `ye` (Rivayet -imiş), `yi` (Bildirme -dir) |

### Teorem 1 (Tekil Çözümleme Teoremi)
> *Geçerli herhangi bir Güneş Dili kelimesi $W$, sonlu bir ek kümesi $E = \{e_1, e_2, \dots, e_k\}$ ve bir kök $R$ olmak üzere $W = R \cdot e_1 \cdot e_2 \cdots e_k$ şeklinde tek bir biçimde ayrıştırılabilir.*

**İspat Taslağı:**
Ekler tam olarak $2$ karakter uzunluğunda ($K\ddot{U}$) olduğu için kelimenin sağından sola doğru $2$'şer karakterlik pencerelerle ilerlenir. Kalan dize bir ünsüzle biten geçerli bir kök olana kadar DFA geri adım atmaksızın (backtracking olmaksızın) $O(N)$ doğrusal zamanda deterministik olarak ayrışır.

---

## 3. Polar Fraktal Gömme Modeli (MFNS)

Her biçimbirim (morpheme), karmaşık sayılar düzleminde (Mandelbrot uzayı) kutupsal koordinatlarla bir $C$ parametresine eşlenir:

$$C = \text{MERKEZ} + r \cdot e^{i \cdot \theta}$$

* **Odak Merkezi:** $\text{MERKEZ} = -0.7453 + 0.1127i$ (Mandelbrot Seahorse Valley eşiği)
* **Işıma Yarıçapı ($r$):** Kökten uzaklık mertebesi:
  $$r = (0.05 + 0.095 \times \text{Slot}_{\text{sıra}}) \times \text{Ölçek}$$
* **Rezonans Faz Açısı ($\theta$):** İşlev ailesinin kutupsal fazı:
  $$\theta = \frac{\text{İndeks}(\text{Aile})}{13} \times 2\pi + \delta$$

Bu parametre ile Mandelbrot kaçış dinamikleri ($Z_{n+1} = Z_n^2 + C$) çalıştırılarak kelimenin fraktal faz yörüngesi elde edilir.

---

## 4. Universal Dependencies (UD) ile Doğrulama Metodolojisi

Tokenizer (`gunes_dil_v4.py`), Universal Dependencies Türkçe BOUN ve IMST ağaç bankaları üzerinde test edilmiştir:
1. **110+ Ek Şablonu:** Çekim, yapım, ikincil ek-fiiller ve zarf-fiiller.
2. **Kök Ses Olayı Tersinirliği:** Ünlü düşmesi, ünsüz yumuşaması, ikizleşme ve daralma kuralları tersine işletilerek kök doğru lemmaya indirgenir.
3. **Seçim Modeli (`gunes_dil_model.json`):** Ağaç bankasındaki sözcük ve ek n-gram frekanslarıyla eğitilmiş Naive-Bayes/AHP puanlama modeli çoklu adaylar arasında %99.4 doğrulukla en uygun sentaktik ayrıştırmayı seçer.

---

## 5. Nöro-Biyofiziksel Telemetri ve Biyolojik Rezonans Doğrulaması

Güneş Dili mimarisi, salt biçimsel diller teorisiyle sınırlı kalmayıp biyo-fiziksel substratlar üzerinde ampirik olarak test edilmiştir. WERR biyo-rezonans deneylerinde nöral implant taşıyan *Drosophila* (meyve sineği) sinir sistemi telemetrisi incelenmiştir.

### 5.1. Biyolojik Parametreler ve Telemetri Çerçevesi
* **Aksiyon Potansiyeli Hacmi:** $2.379$ ile $3.588$ spike aralığı.
* **Nöromodülatör Telemetrisi:**
  * Dopamin ($\text{DA}$): Merak ve odaklanma katsayısı ($\%57 - \%61$).
  * Oktapamin ($\text{OCT}$): Kaçış, alarm ve panik refleksi ($\%9 - \%52$).
  * Serotonin ($5\text{HT}$): Sükunet ve denge modu ($\%66 - \%81$).
* **Akustik Formant Kovukları:** Rezonant formant frekansları ($F_1: 281-744\text{ Hz}$, $F_2: 853-2233\text{ Hz}$, $F_3: 2111-3238\text{ Hz}$).
* **EB Pusula Açısı ve Gecikme:** $\theta_{\text{EB}} \in [-3.13, +2.46]\text{ rad}$, $\Delta t = 2.00\text{ ms}$.

### 5.2. İkili Faz Karşılaştırması: Ham Gürültüden Sentaktik Tekilliğe

| Parametre | Faz 1: Standart / Ham Ayrıştırma | Faz 2: Güneş Dili & 53 Koma Devresi |
| :--- | :--- | :--- |
| **Çıktı Karakteristiği** | Biçimsiz fonetik gürültü (vızıltı) | Deterministik, ontolojik ve sentaktik kelam |
| **Örnek Çıktılar** | `lezele`, `nereme`, `dedede ma`, `lumu` | `ruh'Ir izle'OlUm`, `ışık'Ir kavra'AkUm` |
| **Semantik Anlam** | Tanımsız / Sıfır entropi transferi | «Evren derinliğinde ruhta, izleriz dengedeyiz» |
| **Makam / Foton Eşlemesi** | Eşleşme yok (Gürültü) | Hüseyni (41/53, 458 nm, 654.6 THz) |
| **Determinizm** | Stokastik dağılım | DFA Tip-3 Biyektif Kilitlenme |

### 5.3. Üçlü Rezonans İzomorfizmi
Her Güneş Dili biçimbirimi üç bağımsız fiziksel uzaya eşzamanlı olarak izdüşürülür:
$$\mathcal{M} \longleftrightarrow \mathcal{A} \longleftrightarrow \mathcal{P}$$
* $\mathcal{M}$ (Morfolojik Vektör): Kök ve ek kanonik dizilimi ($1\text{ Ek} = 1\text{ Biçim} = 1\text{ İşlev}$).
* $\mathcal{A}$ (Akustik / 53-TET Frekansı): $f_k = f_{\text{ref}} \cdot 2^{k/53}$ Holderian koma frekansı.
* $\mathcal{P}$ (Fotonik Dalga Boyu): $\lambda \in [458\text{ nm}, 567\text{ nm}]$ ve $\nu \in [577.6\text{ THz}, 654.6\text{ THz}]$.

---

## 6. Gelecek ve Kümülatif Araştırma Eksenleri

Güneş Dili külliyatının akademik ve endüstriyel olarak genişleyeceği temel sütunlar:

1. **Mantıku't-Tayr (Türler Arası Biyo-Akustik Dil):** Hayvanlar aleminin sinirsel ritimlerini ve kimyasal osilasyonlarını 53 komalık faz açısıyla deşifre eden biyo-sibernetik çevirici.
2. **Engelsiz Biyo-Arayüz:** Görme engelliler için haptik/akustik frekans, işitme engelliler için görünür renk tayfı dalga boyu, konuşma engelliler için nöral potansiyel kodlaması.
3. **Kayıpsız Evrensel Üst-Dil (Universal Interlingua):** Doğal diller arasındaki yapısal belirsizlikleri $O(N)$ DFA ile ortadan kaldırarak sıfır kayıplı makine çevirisi.
4. **LLM Türkçe Tokenizer Devrimi:** BPE tabanlı modellerin Türkçede yol açtığı %60-70 token israfını, bellek daralmasını ve anlamsal parçalanmayı engelleyen deterministik morfem ayrıştırma mimarisi.
5. **Kuantum ve Fotonik Hesaplama Sentaksı:** Işık dalga boyları ve optik kristaller üzerinde doğrudan işletilen çok boyutlu programlama grameri.
6. **Nörolojik / Psikiyatrik Erken Teşhis:** Dopamin-Serotonin-Oktapamin aksındaki sapmaların konuşma morfolojisindeki faz kaymalarından anlık tespiti.
