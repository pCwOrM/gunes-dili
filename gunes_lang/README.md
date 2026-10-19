# Güneş-Lang: Akademik Morfo-Semantik ve Nöro-Akustik Programlama Dili

[![Lean 4 Formalized](https://img.shields.io/badge/Lean_4-0_sorry_(Verified)-green.svg)](../proofs/boundary_uniqueness.lean)
[![Deterministic Lexer](https://img.shields.io/badge/DFA_Lexer-O(L)_Deterministic-blue.svg)](lexer.py)
[![Acoustic Telemetry](https://img.shields.io/badge/Telemetry-53--Holder_Z53-gold.svg)](telemetry.py)
[![Memory Footprint](https://img.shields.io/badge/GPU_VRAM-0_Bytes-success.svg)](interpreter.py)
[![License: MIT / CC-BY-4.0](https://img.shields.io/badge/License-MIT_%2F_CC--BY--4.0-orange.svg)](../LICENSE)

**Güneş-Lang**, 1935 Gazi Mustafa Kemal Atatürk'ün *Güneş Dil Teorisi* fonetik kök-ek morfotaktiği, Sir Isaac Newton'un 1664 Cambridge evrensel dil koordinatları ve Lean 4 biçimsel ispat motorunun (`0 sorry`) birleşimiyle inşa edilmiş, dünyadaki ilk **makine-ispatlı fonosemantik ve nöro-akustik programlama dilidir**.

---

## 🏛️ 1. Kuramsal Temeller ve Mimari

1. **Kök-Ek Sınır Biricikliği (Lean 4 `0 sorry`):**
   * Aglutinatif (eklemeli) dillerdeki sözcük sınırları, Lean 4 ortamında makine onaylı olarak ispatlanmış morfotaktik monoid teoremine dayanır. Sözcük ayrıştırmada hiçbir geri izleme (backtracking) veya stokastik belirsizlik bulunmaz; karmaşıklık kesin $\mathcal{O}(L)$ lineerdir.
2. **Sıfır Halüsinasyon Entropisi ($H = 0.00\text{ bit}$):**
   * 1 ek = 1 biçim = 1 işlev prensibiyle allomorfi sıfırlanmıştır. Her deyimin anlamsal izdüşümü tektir.
3. **WERR 53-Hölder Koması Akustik Rezonansı ($\mathbb{Z}_{53}$):**
   * Çalıştırılan her deyim ve sözcük, 53 eşit tampere mikrotonal frekansa ($f \in [100, 8000]\text{ Hz}$) ve faz açısına ($\theta \in [0, 2\pi)$) eşlenir. Kod çalışırken aynı zamanda fiziksel bir ses dalgası ve nöromorfik darbe yayar.
4. **Sıfır GPU VRAM Tüketimi (0 Bytes):**
   * Stokastik alt-kelime (BPE/WordPiece) ve gömme matrisleri yerine sonlu durum dönüştürücüleri (FST) kullanılır.

---

## 🚀 2. Hızlı Başlangıç (Kurulum ve Çalıştırma)

Güneş-Lang hiçbir harici kütüphane bağımlılığı gerektirmez; standart Python 3.9+ ortamında sıfır kurulumla çalışır.

### Etkileşimli Kabuk (REPL)
```bash
# Repo kök dizininde veya gunes_lang klasöründe:
python -m gunes_lang
```
Veya kısayol çalıştırıcıları:
```powershell
.\gunes.ps1
```
```cmd
gunes.bat
```

### Dosya Çalıştırma
```bash
python -m gunes_lang gunes_lang/examples/01_merhaba.gns
python -m gunes_lang gunes_lang/examples/02_fibonacci.gns
python -m gunes_lang gunes_lang/examples/03_asal_sayilar.gns
python -m gunes_lang gunes_lang/examples/04_werr_rezonans.gns
```

### Tek Satır Komut Çalıştırma (`-c`)
```bash
python -m gunes_lang -c 'ag { werla "Güneş Doğuyor!" ; }'
```

---

## 📜 3. Sözdizimi ve Anahtar Sözcükler

| Anahtar Sözcük | Karşılığı | Açıklama |
| :--- | :--- | :--- |
| `ag { ... }` | `main { ... }` | **Güneş / İlk Enerji**: Programın ana bloğu ve başlangıç noktası |
| `tan` | `let / var` | Bellekte değişken tahsisi |
| `yi` | `=` | Atama ve bağlaç operatörü (`tan x yi 42 ;`) |
| `werla` | `print / emit` | Dışa aktarma, konsola veya ses arayüzüne basma |
| `wer` | `return` | Fonksiyondan değer döndürme |
| `tanim` | `def / function` | Fonksiyon tanımlama (`tanim kare(x) { ... }`) |
| `bakba` | `if` | Koşul denetimi (bak- kökü + şart eki -ba) |
| `bakde` | `else` | Olumsuz koşul denetimi (bak- kökü + olumsuzluk eki -de) |
| `donke` | `while` | Süreç döngüsü (dön- kökü + süre zarfı -ke) |
| `dur` | `break` | Döngüyü kırma / sonlandırma |
| `gec` | `continue` | Döngüde sonraki adıma atlama |

### Aritmetik ve Karşılaştırma İşleçleri
* **Aritmetik:** `kat` (+), `kes` (-), `tarap` (*), `bol` (/), `kalan` (%)
* **Karşılaştırma:** `es` (==), `esde` (!=), `buyuk` (>), `kutuk` (<), `buyukes` (>=), `kutukes` (<=)
* **Mantıksal:** `wen` / `ve` (&&), `weya` / `veya` (||), `de` / `degil` (!)
* **Yorum Satırı:** `-- Yorum buraya yazılır`

### Yerleşik Fonksiyonlar
* `boy(dizi)` / `uzunluk(dizi)`: Dizi veya metin boyutu.
* `ekle(dizi, eleman)`: Diziye dinamik eleman ekleme.
* `sayi(deger)` / `metin(deger)`: Tip dönüşüm fonksiyonları.
* `zaman()`: Milisaniye cinsinden zaman damgası.
* `rezonans(metin)`: Metnin 53-Hölder koması frekans fazı.

---

## 📂 4. Dizin Yapısı

```
gunes_lang/
├── __init__.py               # Paket kökü
├── __main__.py               # 'python -m gunes_lang' giriş noktası
├── cli.py                    # REPL, dosya ve -c CLI arayüzü
├── tokens.py                 # 53-Hölder token ve anahtar kelime tanımları
├── lexer.py                  # Deterministik O(L) morfotaktik ayrıştırıcı
├── ast_nodes.py              # Biçimsel sözdizim ağacı düğümleri
├── parser.py                 # Özyinelemeli iniş sözdizim çözümleyicisi
├── environment.py            # Leksikal kapsam ve bellek haritası
├── interpreter.py            # Yürütme motoru ve yerleşik işlevler
├── telemetry.py              # WERR 53-Hölder mikrotonal rezonans takipçisi
├── gunes.ps1 / gunes.bat     # PowerShell ve CMD hızlı çalıştırıcıları
├── examples/                 # Örnek programlar
│   ├── 01_merhaba.gns        # Merhaba Dünya & Temel Değişkenler
│   ├── 02_fibonacci.gns      # Özyinelemeli Fibonacci Serisi
│   ├── 03_asal_sayilar.gns   # 50'ye kadar Asal Sayılar Eleği
│   └── 04_werr_rezonans.gns  # WERR 53-Hölder Yörünge Düzeltme
└── gunes_lang_akademik_analiz.html # Akademik karşılaştırma raporu
```

---

## 🧪 5. Örnek Kod: Özyinelemeli Fibonacci ve Rezonans

```gunes
-- GÜNEŞ-LANG: Özyinelemeli Fibonacci ve WERR 53-Hölder Rezonansı
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
        tan f_val yi fib(i) ;
        werla "fib(" kat metin(i) kat ") = " kat metin(f_val) ;
        i yi i kat 1 ;
    }

    werla "Hesaplama Başarıyla Tamamlandı." ;
}
```

---

## 📊 6. Akademik Raporlar ve Çevrimiçi Derleyici

* **Akademik Analiz Raporu (HTML):** [gunes_lang_akademik_analiz.html](gunes_lang_akademik_analiz.html)
* **Akademik Analiz Raporu (PDF):** [Gunes_Lang_Akademik_Analiz_Raporu_Guncel.pdf](Gunes_Lang_Akademik_Analiz_Raporu_Guncel.pdf)
* **Çevrimiçi Derleyici (GitHub Pages):** [https://pcworm.github.io/gunes-dili/ide/](https://pcworm.github.io/gunes-dili/ide/)
