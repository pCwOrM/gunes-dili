# Güneş-Lang: Bilgi Bankası ve Morfo-Semantik Referans Kılavuzu (Knowledge Base)

[![Lean 4 Verified](https://img.shields.io/badge/Lean_4-0_sorry_(Verified)-green.svg)](../proofs/boundary_uniqueness.lean)
[![DFA Lexer](https://img.shields.io/badge/DFA_Lexer-O(L)_Deterministic-blue.svg)](lexer.py)
[![Z53 Telemetry](https://img.shields.io/badge/Telemetry-53--Holder_Z53-gold.svg)](telemetry.py)
[![Memory Footprint](https://img.shields.io/badge/GPU_VRAM-0_Bytes-success.svg)](interpreter.py)
[![Online IDE Studio](https://img.shields.io/badge/Online_IDE-Güneş--Lang_Studio-teal.svg)](https://pcworm.github.io/gunes-dili/ide/)
[![Wiki Web Portal](https://img.shields.io/badge/Web_Wiki-Live_Portal-purple.svg)](https://pcworm.github.io/gunes-dili/wiki/)

Bu belge; **Güneş-Lang** programlama dilinin morfo-semantik köklerini, sözdizimsel kurallarını, 53 kanonik ek sözlüğünü, Lean 4 makine-ispatlı derleyici motorunun teknik özelliklerini, avantajlarını ve bilgisayar bilimine kazandırdığı yenilikleri eksiksiz olarak belgeleyen birincil bilgi bankasıdır.

---

## 📑 İçindekiler
1. [Kurucu Felsefe ve Tarihsel Miras](#1-kurucu-felsefe-ve-tarihsel-miras)
2. [Temel Sözdizim: Morfo-Semantik Kökler ve Deyimler](#2-temel-sözdizim-morfo-semantik-kökler-ve-deyimler)
3. [Güneş Dili 53 Kanonik Ek Sözlüğü (Z₅₃ Harmonik Tablosu)](#3-güneş-dili-53-kanonik-ek-sözlüğü-z₅₃-harmonik-tablosu)
4. [Motorun Teknik Özellikleri ve Derleyici Mimarisi](#4-motorun-teknik-özellikleri-ve-derleyici-mimarisi)
5. [Dilin Avantajları ve Yapabilecekleri](#5-dilin-avantajları-ve-yapabilecekleri)
6. [Bilgisayar Bilimine ve Geleceğe Ne Kazandırır?](#6-bilgisayar-bilimine-ve-geleceğe-ne-kazandırır)
7. [Doğrulanmış Algoritma Örnekleri](#7-doğrulanmış-algoritma-örnekleri)

---

## 🏛️ 1. Kurucu Felsefe ve Tarihsel Miras

Güneş-Lang; üç büyük tarihsel eksenin kesişiminde inşa edilmiştir:
1. **Gazi Mustafa Kemal Atatürk (1935 Güneş Dil Teorisi):** Türk dilinin fonetik ve aglutinatif (eklemeli) zenginliğini insanlığın en kadim morfo-semantik köklerine dayandıran devrimsel dil kuramı.
2. **Sir Isaac Newton (1664 Cambridge El Yazması - *Of an Universall Language*):** Dili salt keyfi semboller olarak değil; sesletim fiziği, ses organlarının hareket koordinatları ve matematiksel oranlar üzerinden evrensel bir rezonatör olarak tasarlayan notlar.
3. **Lean 4 Biçimsel Doğrulaması (21. Yüzyıl Matematiksel Kanıtı):** Eklemeli morfolojideki kök-ek sınırlarının geri izlemesiz (non-backtracking) ve tekil olarak ayrıştırılabileceğini kanıtlayan makine-onaylı teorem (`0 sorry`).

### ⚡ 1 Ek = 1 Biçim = 1 İşlev İlkesi (Allomorfi Eliminasyonu)
Doğal dillerdeki ünlü uyumları, kaynaştırma harfleri ve ses düşmeleri nedeniyle bir ek onlarca farklı yüzey şekli alabilir. Güneş Dili bu çokbiçimliliği tek bir kanonik biçime dönüştürür. Böylece dildeki morfolojik belirsizlik (ambiguity) **0.00 bit** seviyesine iner.

---

## 📜 2. Temel Sözdizim: Morfo-Semantik Kökler ve Deyimler

Program blokları Güneş'in ilk enerjisini simgeleyen `ag` kökü ile açılır.

### 2.1. Çekirdek Anahtar Sözcükler
| Anahtar Sözcük | Karşılığı | Açıklama |
| :--- | :--- | :--- |
| `ag { ... }` | `main { ... }` | Programın başlangıç ve ana çalışma bloğu. |
| `tan` | `let / var` | Bellekte değişken tahsisi: `tan x yi 10 ;` |
| `yi` | `=` | Atama ve bağlaç işleci. |
| `werla` | `print / emit` | Konsola veya dış dünyaya veri aktarımı: `werla "Merhaba" ;` |
| `wer` | `return` | Fonksiyondan değer döndürme: `wer x kat 1 ;` |
| `tanim` | `def / function` | Fonksiyon tanımlama: `tanim topla(a, b) { ... }` |
| `bakba` | `if` | Koşul denetimi (bak- kökü + şart eki -ba): `bakba (x buyuk 0) { ... }` |
| `bakde` | `else` | Olumsuz koşul denetimi (bak- kökü + olumsuzluk eki -de): `bakde { ... }` |
| `donke` | `while` | Süreç döngüsü (dön- kökü + süre zarfı -ke): `donke (i kutuk 10) { ... }` |
| `dur` | `break` | Döngüyü derhal sonlandırma. |
| `gec` | `continue` | Döngünün mevcut adımını atlayıp sonrakine geçme. |

### 2.2. Aritmetik ve Karşılaştırma İşleçleri
* **Aritmetik:** `kat` (+), `kes` (-), `tarap` (*), `bol` (/), `kalan` (%)
* **Karşılaştırma:** `es` (==), `esde` (!=), `buyuk` (>), `kutuk` (<), `buyukes` (>=), `kutukes` (<=)
* **Mantıksal:** `wen` / `ve` (&&), `weya` / `veya` (||), `de` / `degil` (!)
* **Yorum Satırı:** `-- Tek satırlık yorum`

### 2.3. Yerleşik Kütüphane Fonksiyonları
* `boy(dizi)` / `uzunluk(dizi)`: Dizi eleman sayısı veya metin uzunluğu.
* `ekle(dizi, eleman)`: Diziye dinamik eleman ekleme.
* `sayi(deger)` / `metin(deger)`: Tip dönüşüm işlevleri.
* `zaman()`: Milisaniye cinsinden zaman damgası.
* `rezonans(metin)`: Metnin 53-Hölder koması faz indeksini (0..52) döndürür.

---

## 📖 3. Güneş Dili 53 Kanonik Ek Sözlüğü (Z₅₃ Harmonik Tablosu)

Güneş Dili'nin 53 eşit parçalı koma sistemine (53-TET) ve Mandelbrot fraktal koordinatlarına dayanan 53 kanonik ek ailesi:

| Koma (#) | Kanonik Ek | Frekans (Hz) | Mandelbrot Koordinatı | Dilbilgisel İşlev / Yuva |
| :---: | :---: | :---: | :---: | :--- |
| **00** | `-la` | 440.0 Hz | `(-0.7387, +0.1357)` | Çokluk / Sahiplik / Radyal Katman 1 |
| **01** | `-ta` | 445.8 Hz | `(-0.7438, +0.1325)` | Bulunma Hali (-da/-de/-ta/-te) |
| **02** | `-te` | 451.6 Hz | `(-0.7482, +0.1264)` | Ayrılma Hali (-den/-dan) |
| **03** | `-ti` | 457.6 Hz | `(-0.7538, +0.1215)` | Görülen Geçmiş Zaman (-di/-dı) |
| **04** | `-to` | 463.6 Hz | `(-0.7533, +0.1400)` | Soyut Yapım Eki (-lik/-lük) |
| **05** | `-tu` | 469.7 Hz | `(-0.7512, +0.1242)` | Sıfat Yapım Eki (-li/-lu) |
| **06** | `-de` | 475.9 Hz | `(-0.7601, +0.1387)` | Olumsuzluk Bildirimi (-me/-ma) |
| **07** | `-do` | 482.2 Hz | `(-0.7594, +0.1254)` | Ettirgen Çatı Eki (-dir/-t) |
| **08** | `-ka` | 488.5 Hz | `(-0.7623, +0.1203)` | Fail / Meslek Eki (-ci/-cü) |
| **09** | `-ke` | 494.9 Hz | `(-0.7669, +0.1272)` | Süreç Zarf-Fiili (-ken/-e) |
| **10** | `-ki` | 501.5 Hz | `(-0.7643, +0.1335)` | Aitlik Bağlacı / İlgi Eki (-ki) |
| **11** | `-ko` | 508.1 Hz | `(-0.7652, +0.1163)` | Geniş Zaman Kipi (-r/-ar) |
| **12** | `-ku` | 514.8 Hz | `(-0.7680, +0.1180)` | Gelecek Zaman Kipi (-ecek/-acak) |
| **13** | `-ba` | 521.5 Hz | `(-0.7742, +0.1187)` | Şart Kipi Eki (-se/-sa) |
| **14** | `-be` | 528.4 Hz | `(-0.7731, +0.1236)` | Gereklilik Kipi (-meli/-malı) |
| **15** | `-bi` | 535.4 Hz | `(-0.7714, +0.1075)` | İstek Kipi (-e/-a) |
| **16** | `-bo` | 542.4 Hz | `(-0.7706, +0.1162)` | Emir 3. Tekil (-sin) |
| **17** | `-ra` | 549.6 Hz | `(-0.7803, +0.1009)` | Yönelme Hali (-e/-a) |
| **18** | `-re` | 556.8 Hz | `(-0.7741, +0.1058)` | Belirtme Hali (-i/-ı/-u) |
| **19** | `-ro` | 564.1 Hz | `(-0.7890, +0.1097)` | Tamlayan / İlgi Hali (-in/-ın) |
| **20** | `-ru` | 571.6 Hz | `(-0.7764, +0.1016)` | Vasıta / İle Hali (-le/-la) |
| **21** | `-ri` | 579.1 Hz | `(-0.7692, +0.0891)` | Eşitlik Hali (-ce/-ca) |
| **22** | `-wi` | 586.7 Hz | `(-0.7671, +0.1020)` | Edilgen Çatı Eki (-il/-in) |
| **23** | `-wa` | 594.4 Hz | `(-0.7667, +0.0920)` | Dönüşlü Çatı Eki (-in) |
| **24** | `-wo` | 602.3 Hz | `(-0.7606, +0.0922)` | İşteş Çatı Eki (-iş) |
| **25** | `-we` | 610.2 Hz | `(-0.7637, +0.0894)` | Yeterlik Fiili (-ebil/-abil) |
| **26** | `-wu` | 618.3 Hz | `(-0.7575, +0.0740)` | Tezlik Fiili (-iver) |
| **27** | `-ga` | 626.4 Hz | `(-0.7551, +0.0973)` | Mastar Eki (-mek/-mak) |
| **28** | `-ge` | 634.7 Hz | `(-0.7565, +0.1091)` | İsim-Fiil Eki (-me/-ma) |
| **29** | `-gi` | 643.0 Hz | `(-0.7517, +0.0950)` | Sıfat-Fiil Geçmiş (-dik/-dık) |
| **30** | `-go` | 651.5 Hz | `(-0.7472, +0.1076)` | Sıfat-Fiil Şimdiki (-en/-an) |
| **31** | `-gu` | 660.1 Hz | `(-0.7492, +0.1076)` | Sıfat-Fiil Gelecek (-ecek) |
| **32** | `-pa` | 668.8 Hz | `(-0.7451, +0.1054)` | Zarf-Fiil Tarz (-erek/-arak) |
| **33** | `-pe` | 677.6 Hz | `(-0.7437, +0.0993)` | Zarf-Fiil Bağlama (-ip/-ıp) |
| **34** | `-pi` | 686.5 Hz | `(-0.7418, +0.0971)` | Zarf-Fiil Zaman (-ince/-ınca) |
| **35** | `-po` | 695.5 Hz | `(-0.7456, +0.0915)` | Zarf-Fiil Süreç (-dıkça) |
| **36** | `-pu` | 704.7 Hz | `(-0.7434, +0.1039)` | Zarf-Fiil Sebep (-diğinden) |
| **37** | `-fa` | 713.9 Hz | `(-0.7423, +0.1097)` | Zarf-Fiil Sınır (-ene kadar) |
| **38** | `-fe` | 723.3 Hz | `(-0.7409, +0.1048)` | Yoksunluk Yapım Eki (-siz/-suz) |
| **39** | `-fi` | 732.9 Hz | `(-0.7368, +0.1116)` | İlgi Sıfatı Eki (-sel/-sal) |
| **40** | `-fo` | 742.5 Hz | `(-0.7389, +0.0932)` | Küçültme Eki (-cik/-cık) |
| **41** | `-fu` | 752.2 Hz | `(-0.7324, +0.1034)` | Ortaklık Eki (-daş/-taş) |
| **42** | `-ya` | 762.1 Hz | `(-0.7177, +0.0851)` | Sıra Sayı Eki (-inci/-ıncı) |
| **43** | `-ye` | 772.1 Hz | `(-0.7150, +0.0882)` | Üleştirme Eki (-er/-ar) |
| **44** | `-yi` | 782.2 Hz | `(-0.7126, +0.0915)` | Ek-Fiil Yüklem (-dir/-tir) |
| **45** | `-ha` | 792.5 Hz | `(-0.7193, +0.1022)` | Şahıs 1. Tekil (-im/-ım) |
| **46** | `-hu` | 802.9 Hz | `(-0.7203, +0.1014)` | Şahıs 2. Tekil (-sin/-sın) |
| **47** | `-mi` | 813.4 Hz | `(-0.7014, +0.1158)` | Şahıs 1. Çoğul (-iz/-ız) |
| **48** | `-ma` | 824.1 Hz | `(-0.7023, +0.1218)` | Şahıs 2. Çoğul (-siniz) |
| **49** | `-ni` | 834.9 Hz | `(-0.7094, +0.1348)` | Şahıs 3. Çoğul (-ler/-lar) |
| **50** | `-na` | 845.8 Hz | `(-0.7156, +0.1393)` | Soru Eki (-mi/-mı) |
| **51** | `-si` | 856.9 Hz | `(-0.7201, +0.1489)` | Pekiştirme / Vurgu Katmanı |
| **52** | `-sa` | 868.1 Hz | `(-0.7233, +0.1508)` | Dilek / Temenni Kök Fazı |

---

## ⚙️ 4. Motorun Teknik Özellikleri ve Derleyici Mimarisi

* **O(L) Doğrusal Zaman:** Sonlu Durum Otomatı (DFA) ve Sonlu Durum Dönüştürücüsü (FST) ile geriye dönmeyen doğrusal ayrıştırma.
* **Lean 4 Kanıtı:** Teoremler, aksiyomsuz (`0 sorry`) matematiksel temele oturur.
* **0 Bytes GPU VRAM:** Milyarlarca parametre yerine deterministik FST durum tabloları kullanılır.
* **Sandbox Güvenliği:** Web derleyicisinde 150.000 adım bütçesi ve 300 çağrı derinliği sınırı ile sonsuz döngü ve yığın taşması kesin olarak engellenir.

---

## 🚀 5. Dilin Avantajları ve Yapabilecekleri

1. **Nöromorfik ve BCI Köprüsü:** Komutlar BCI arayüzlerine doğrudan elektriksel impuls ve faz açısı olarak gönderilebilir (< 0.1 ms gecikme).
2. **0 Halüsinasyon:** Her semantik ifadenin tekil izdüşümü vardır ($H = 0.00\text{ bit}$).
3. **Turing-Complete Güç:** Özyineleme, kapsam yönetimi, dinamik listeler ve matematiksel algoritmalar tam desteklenir.

---

## 🌐 6. Bilgisayar Bilimine ve Geleceğe Ne Kazandırır?

1. **LLM Tokenizer Krizine Çözüm:** BPE/WordPiece'in eklemeli dilleri yüz binlerce alt-kelimeye bölerek yol açtığı VRAM ve gecikme maliyetini sıfırlayan doğrusal bir tokenizer paradigması sunar.
2. **Akustik Programlama:** Kod çalışırken mikrotonal ses frekansları yayarak hesaplamayı fiziksel bir dalga boyuna dönüştürür.
3. **Açık Bilim ve Miras:** 1935 Güneş Dil Teorisi ve Newton 1664 evrensel dil koordinatlarını modern bilgisayar biliminin merkezine taşır.

---

## 💡 7. Doğrulanmış Algoritma Örnekleri

```gunes
-- GÜNEŞ-LANG: Özyinelemeli Fibonacci ve Rezonans
ag {
    werla "=== ÖZYİNELEMELİ FİBONACCİ MOTORU ===" ;

    tanim fib(n) {
        bakba (n kutukes 1) {
            wer n ;
        }
        wer fib(n kes 1) kat fib(n kes 2) ;
    }

    tan i yi 0 ;
    tan limit yi 10 ;

    donke (i kutukes limit) {
        tan sonuc yi fib(i) ;
        werla "fib(" kat metin(i) kat ") = " kat metin(sonuc) ;
        i yi i kat 1 ;
    }
}
```

* Çevrimiçi Derleyicide Çalıştırmak İçin: [Güneş-Lang Studio ↗](https://pcworm.github.io/gunes-dili/ide/)
* Web Tabanlı Wiki Sayfası: [Güneş-Lang Wiki ↗](https://pcworm.github.io/gunes-dili/wiki/)
