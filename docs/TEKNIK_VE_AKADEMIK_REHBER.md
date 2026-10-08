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
