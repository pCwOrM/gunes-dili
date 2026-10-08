# Güneş Dili (Sun Language) Ekosistemi
### Matematiksel, Fonetik ve Fraktal Temelli Evrensel Dil Mimarisi

![Repo Status: Private](https://img.shields.io/badge/Repo%20Status-Private%20%2F%20Confidential-red.svg)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![UD Turkish Validated](https://img.shields.io/badge/UD%20Turkish-Validated-success.svg)](https://universaldependencies.org/)
[![Mandelbrot Fractal Trajectory](https://img.shields.io/badge/Fractal-Mandelbrot%20MFNS-orange.svg)](https://doi.org/10.5281/zenodo.22802921)

---

## ☀️ Proje Manifestosu

**Güneş Dili Ekosistemi**; Mustafa Kemal Atatürk'ün 1935 yılında başlattığı tarihsel **Güneş-Dil Teorisi**'ni, çağdaş **biçimsel diller teorisi (formal language theory)**, **hesaplamalı morfoloji**, **Mandelbrot fraktal geometrisi** ve **53 eşit parçalı harmonik ses sistemi (Holder koma çemberi)** ile birleştirerek matematiksel olarak kanıtlanabilir, deterministik ve evrensel bir sentetik dil motoruna dönüştüren açık kaynaklı bir monorepodur.

Doğal dillerdeki morfolojik belirsizlikler (allomorfi, ünlü uyumu istisnaları, ek çakışmaları), Güneş Dili mimarisinde **1 Ek = 1 Biçim = 1 İşlev** aksiyomuyla sıfırlanmıştır.

---

## 🏛️ Mimari ve Çekirdek Bileşenler

```
gunes-dili/
├── archive/         # Atatürk 1935 Nöbet Defteri, Newton 1664 Notları ve Tarihsel Belgeler
├── tokenizer/       # Işıma ve Rezonans Tabanlı Morfolojik Tokenizer (gunes_dil_v4)
├── engine/          # Deterministik Güneş Dili Gramer ve Çeviri Motoru (gunes_dili)
├── lab/             # İnteraktif Web Tabanlı Çeviri ve Ayrıştırma Laboratuvarı
└── proofs/          # T1-T5 Matematiksel Kanıt Defteri ve Fraktal Sinir Ağı Modelleri
```

---

## 🔬 Matematiksel ve Fiziksel İlkeler: Işıma ve Rezonans

Güneş Dili Tokenizer'ı ve Motoru, dili salt bir sembol dizisi olarak değil; **Güneş'ten dışa doğru ışıyarak yayılan ve belirli frekanslarda rezonansa giren dinamik bir faz yörüngesi** olarak modeller.

### 1. Işıma (Radyal Yayılım — $r$)
* Merkezde kök odağı yer alır ($r = 0$, `MERKEZ = -0.7453 + 0.1127i`).
* Ekler ardışık olarak eklendikçe merkezden dışarıya doğru radyal ışınım katmanları ($r$) oluşturur:
  $$r = (0.05 + 0.095 	imes \text{SIRA}[\text{ek.yuva}]) \times \text{ÖLÇEK}$$
* İçten dışa doğru: **Kök $\to$ Yapım $\to$ Çatı $\to$ Zaman/Kip $\to$ Hal/Şahıs**.

### 2. Rezonans (Açısal Faz ve Frekans — $\theta$)
* Her işlev ailesi, kutupsal çember üzerinde belirli bir harmonik faza ($	heta$) kilitlenmiştir:
  $$\theta = \frac{\text{İşlev Ailesi İndeksi}}{|\text{İşlev Aileleri}|} \times 2\pi$$
* **53'lük Ses Çemberi Uyumu:** 53 morfolojik ek ailesi, Türk Musikisindeki 53 eşit tampere ses sistemindeki (Holder koması) rezonans aralıklarına karşılık gelir.
* Fonetik rezonans (ünlü ve ünsüz harmonisi), bu faz açıları üzerinden denetlenir.

### 3. Mandelbrot Fraktal Gömme Formülü
Kelimeler karmaşık sayılar düzleminde tekil koordinatlara ve faz yörüngelerine dönüştürülür:
$$C = \text{MERKEZ} + r \times e^{i \cdot \theta}$$
$$Z_{n+1} = Z_n^2 + C$$

---

## ⚡ Hızlı Başlangıç

### Gereksinimler
* Python 3.9 veya üzeri
* `numpy`

### 1. Tokenizer ile Türkçe Ayrıştırma
```python
import sys
sys.path.append("./tokenizer")
from gunes_dil_v4 import tokenize, cozumle_cumle

# Tek kelime morfolojik ayrıştırma
res = tokenize("kitaplarımızdan")
print("Durum:", res["durum"])  # KABUL
for parca, ek in res["tokenlar"]:
    print(f"  {parca:10} -> {ek.islev}")
# Çıktı:
#   kitap      -> kök (kitap)
#   lar        -> çokluk
#   ımız       -> iyelik 1.çoğul
#   dan        -> ayrılma hali
```

### 2. Güneş Dili Çevirisi ve Ayrıştırma
```python
import sys
sys.path.append("./tokenizer")
sys.path.append("./engine")
import gunes_dil_v4 as M
import gunes_dili as G

kelime = "gidiyorlardı"
tok = M.tokenize(kelime)
gd = G.turkceden(tok, M)

print(f"{kelime} -> {gd['kelime']}")
# Çıktı: gidiyorlardı -> gitkeyasa

# Güneş Dili kelimesini deterministik çözme
cozum = G.cozumle(gd["kelime"])
print(cozum["kok"], cozum["ekler"])
# Çıktı: git [('ke', 'zaman', 'şimdiki', 'V'), ('ya', 'ek-fiil', 'hikâye (idi)', 'V'), ('sa', 'kişi', 'kişi 3. çoğul', 'V')]
```

---

## 📐 Kanıt Defteri Bulguları (`proofs/kanit_defteri.json`)

| Teorem | Test Edilen Hacim | Başarı Oranı | Anlamı |
| :--- | :--- | :--- | :--- |
| **T1 (DFA Determinizmi)** | 2.048 durum, 53 ek | **%100 (0 ihlal)** | Biçimbilimsel otomat tekil ve deterministiktir. |
| **T2 (Kaba Kuvvet Doğrulama)** | 1.291.220 ek dizisi | **%100 (0 hata)** | Geçerli her kelimenin tam olarak 1 çözümü vardır. |
| **T3 (Sınanabilirlik)** | 20.000 rastgele dizi | **%3.27 kabul** | Rastgele harf yığınları elenir; kurallar katıdır. |
| **T4 (Universal Dependencies)** | BOUN & IMST Test Setleri | **%100 gidiş-dönüş** | Türkçeden Güneş Dili'ne kayıpsız çeviri ve geri-alım. |
| **T5 (Fraktal Yapay Zeka)** | Mandelbrot Gömme Modeli | **%94.3 doğruluk** | Sinir ağı fraktal uzayda morfemleri sınıflandırabilir. |

---

## 📂 Arşiv ve Tarihsel Miras (`archive/`)

Bu repoda kuramın dayandığı orijinal el yazması ve tarihi tahliller tam set olarak muhafaza edilmektedir:
1. **Atatürk'ün Son Nöbet Defteri / Güneş-Dil Teorisi (1-53):** 1935 Ulus tefrikaları, Afet İnan mektupları ve Atatürk'ün fonetik analizleri (PDF ve 31 sayfa yüksek çözünürlüklü tarama).
2. **Isaac Newton (1664–1665):** Trinity College not defterindeki *Of an Universall Language* evrensel dil tasarımı (23 sayfa tarama).
3. **53'lük Müzik ve Ses Çemberi:** Safiyüddin Urmevi, Kantemiroğlu ve Arel-Ezgi-Uzdilek 53 Holder koması ses çemberi ile 53 Güneş Dili ek ailesi harmoni tahlilleri.
4. **Kozmik İşletim Sistemi & Kuantum Palimpsest:** Dil-evren-fraktal ontolojisi.

---

## 🧪 İnteraktif Web Laboratuvarı (`lab/`)

`lab/index.html` dosyasını doğrudan herhangi bir web tarayıcısında açarak:
* Türkçe $\to$ Güneş Dili çeviri motorunu çalıştırabilir,
* Kelimelerin Mandelbrot fraktal koordinat haritasını inceleyebilir,
* Tersine ayrıştırıcı (reverse parser) ile Güneş Dili metinlerini çözümleyebilirsiniz.

---

## 🔒 Gizlilik ve Telif Hakları

Bu depo ve içerisindeki Güneş Dili motoru, tokenizer'ı, matematiksel kanıtları ve tarihsel arşiv tahlilleri **ÖZEL VE GİZLİ (PRIVATE & CONFIDENTIAL)** araştırma niteliğindedir. İzinsiz çoğaltılamaz, kamuya açık paylaşılamaz veya üçüncü taraflara dağıtılamaz. Tüm hakları saklıdır (All Rights Reserved).
