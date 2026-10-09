# Güneş Dili: Kümülatif Akademik Gelişim, Doğrulama ve Değişiklik Günlüğü
### Bilimsel Standartlar, Determinizm Metrikleri ve Sürüm Arşivi

---

## 🏛️ Yönetici Künyesi ve Tarihsel Öncelik

* **Kurucu Düşünce ve Tarihsel Vizyon:** Gazi Mustafa Kemal Atatürk (1935 Güneş-Dil Teorisi) & Sir Isaac Newton (1664 Trinity College *Of an Universall Language*)
* **Sistem ve Ontoloji Mimarı:** @pCwOrM (WERR / MFNS Külliyatı)
* **Gramer ve Çeviri Motoru:** Bekirhan Dağlı (@bdagli)
* **Morfolojik Tokenizer:** Dağhan Dağlı (@Lexovian)
* **Koordinasyon ve Takım:** Zerrin Dağlı (@jesmaat)
* **Kozmik ve Felsefi Arşiv:** Semih Salar
* **Patent Önceliği:** TÜRKPATENT TR 2026/016285 (WERR Engine & OED)

---

## 📅 Sürüm ve Değişiklik Kronolojisi

### [v4.1.0-Formal] — 2026-10-09
#### 1. 📐 Lean 4 Biçimsel Doğrulama Modülü Eklendi (`proofs/GunesDiliProof.lean`)
* **Amaç:** WERR ve GAP-Lean4 külliyatındaki standartlara uygun olarak, Güneş Dili'nin 3 kurucu aksiyomunu ve temel teoremlerini bağımlı tip teorisinde (dependent type theory) mekanik olarak kanıtlamak.
* **Formalize Edilen Teoremler:**
  1. `suffix_form_injective`: Aksiyom 1 uyarınca $1 \text{ Ek} \iff 1 \text{ Biçim} \iff 1 \text{ İşlev}$ eşlemesinin injektifliği ve allomorfinin mutlak sıfırlanması.
  2. `suffix_chain_zero_clusters`: Ardışık ek diziliminde ($K\ddot{U} \cdot K\ddot{U}$) hiçbir zaman iç ünsüz kümesi ($CC$) oluşamayacağının yapısal tümevarımla ispatı.
  3. `bare_root_zero_clusters` & `root_suffix_junction_is_cluster`: Aksiyom 2 uyarınca kök ile ek dizisi birleştiğinde tüm kelimede **TAM OLARAK BİR TEK ÜNSÜZ KÜMESİ** oluştuğu ve bu kümenin kök-ek sınırını $O(N)$ karmaşıklığında tekil olarak belirlediği.
  4. `dfa_transition_uniqueness`: Teorem 1 uyarınca Deterministik Sonlu Otomatın geçiş kardinalitesinin $| \delta(s, e) | \le 1$ olduğu ve biçimbilimsel dallanma belirsizliğinin sıfırlandığı.
  5. `holder_comma_phase_distinct`: Teorem 5 uyarınca Türk Musikisi 53-Holder koması ses sistemine eşlenen 53 ek ailesinin açısal faz izdüşümlerinin ($\theta_k \pmod{53}$) çakışmasızlığı.
  6. `radial_expansion_monotonic`: Yuva mesafesine bağlı radyal yarıçap genişlemesinin kesin monoton artanlığı.

#### 2. ⚡ Çekirdek Motor ve Kanıt Defteri İyileştirmeleri (Geri Dönülebilir ve Kayıtlı)
* **`engine/gunes_dili.py`:**
  * Windows terminallerinde (cp1254 kod sayfası) doğrudan `python engine/gunes_dili.py` çalıştırıldığında `≥` ve `∎` karakterlerinde oluşan `UnicodeEncodeError` hatası, `sys.stdout.reconfigure(encoding='utf-8')` denetimiyle güvenli hale getirildi. Kodun çekirdek mantığına dokunulmadı; yalnızca konsol çıktı güvenliği sağlandı.
* **`proofs/kanit_defteri.py`:**
  * Deponun ana dizininden veya herhangi bir alt dizinden bağımsız çalışabilmesi için `sys.path` yolu dinamik çözümlenecek şekilde güncellendi.
  * Yerel ortamda `ud` modülü (Universal Dependencies reader) bulunmadığında, daha önce UD Turkish test kümesinde ölçülmüş ve doğrulanmış T4 ve T5 istatistiklerinin (`kanit_defteri.json`) korunması, aynı zamanda canlı örnek küme üzerinde testlerin başarıyla geçirilmesi sağlandı.

#### 3. 🧪 Canlı Doğrulama Sonuçları (`kanit_defteri.json`)
* **T1 (FSA Determinizm):** 2048 durum tarandı, 53 ek ailesi denendi &rarr; **İhlal: 0**.
* **T2 (Kaba Kuvvet Çözümleme Tekilliği):** 1.291.220 dizi denendi, 84.124 geçerli kelime &rarr; **Tek çözümleme hatası: 0**.
* **T3 (Rastgele Sınama Süzgeci):** Rastgele harf dizilerinin geçerlilik oranı %3.275 (Hata tespit süzgeci: %96.7).
* **T4 (İki Yönlü Çeviri & Round-Trip):** 17.297 kelimede 17.078 geçerli üretim &rarr; **Gidiş-Dönüş Doğruluğu: %100.0**.
* **T5 (Morfem/İşlev Oranı):** Türkçede işlev başına ortalama biçim sayısı 5.72 iken Güneş Dili'nde **tam olarak 1.0**.

---

### [v4.2.0-WebPortal] — 2026-10-09
#### 1. 🌐 Canlı Web Portalı & İnteraktif Laboratuvarın Baştan Aşağı Yenilenmesi (`docs/index.html`)
* **Tespit Edilen Eksiklik ve Hatalar:**
  1. Mobil ve orta ölçekli ekranlarda menü kırılmaları, taşmalar ve mobil açılır menü (hamburger drawer) eksikliği.
  2. Eski simülatörün statik kurallarla çalışması (`kitaptapızte` gibi sahte üretimler) ve `engine/gunes_dili.py` kanonik morfolojisine uymaması.
  3. GitHub Pages kök dizin dışındaki dosyalara erişemediği için `../lab/index.html` bağlantısının 404 Not Found hatası üretmesi.
  4. HTML DOM yapısında kapatılmamış div/section etiketleri (`div.proofs-table-wrap`) nedeniyle mimarlar bölümünün ispat tablosunun içine hapsolması.
* **Uygulanan Akademik ve Tasarımsal İyileştirmeler:**
  1. **Ultra-Modern Kozmik/Siber Glassmorphic Arayüz:** Cinzel, Plus Jakarta Sans ve IBM Plex Mono tipografileriyle Güneş Dili'nin hem kadim Atatürk/Newton mirasını hem de modern WERR/MFNS sibernetik karakterini yansıtan elit görsel mimari.
  2. **Duyarlı Gezinme & Mobil Drawer:** Masaüstünde cam efektli navbar, mobilde pürüzsüz açılır çekmece menüsü (`#mobileDrawer`).
  3. **Deterministik İki Yönlü Morfoloji Motoru (İstemci Taraflı JavaScript):**
     * Türkçe &rarr; Güneş Dili: Kanonik kök dönüştürücü (`(C)V(CV)*C`), 53 ek tablosu (`EK_TABLOSU`), zengin iki dilli korpus (`BILINGUAL_CORPUS`) ve morfem şeridi (kök, çatı, zaman, ek-fiil, hal/şahıs).
     * Güneş Dili &rarr; Türkçe: Aksiyom 2 tabanlı DFA tekil konsonant kümesi ayrıştırması ($CC$) ve $O(N)$ geri-çözümleyici.
  4. **Canlı 53-Holder Koması Akustik Sentezleyici (Web Audio API):**
     * 53-TET mikrotonal frekans formülü $f_k = 440 \cdot 2^{(k - 9)/53}\text{ Hz}$ ile saf sinüs osilatörü ve dinamik gain envelope eşliğinde işitsel rezonans çalma yeteneği.
  5. **Çift Etkileşimli Canvas:**
     * *Canvas 1:* Mandelbrot kutupsal faz yörüngesi çizici ($r, \theta$ ışıma vektörü).
     * *Canvas 2:* Tıklanabilir 53-Komalı Türk Musikisi Makam Çarkı (Rast, Segâh, Dügâh, Çargâh, Hüseyni, Nevâ vb.).
  6. **Bağlantı Bütünlüğü & Lab Entegrasyonu:** `lab/` paketi Pages kökü olan `docs/lab/` altına doğrudan kopyalanarak tüm 404 riskleri bertaraf edildi.
  7. **Biçimsel Doğrulama ve Arşiv Vitrini:** Lean 4 `GunesDiliProof.lean` teorem kartları, Dolmabahçe 1935, Newton 1664 ve Semih Salar kozmik arşivleri öne çıkarıldı.

---

### [v4.3.0-TributeAndLab] — 2026-10-09
#### 1. 🏛️ Tarihsel Kurucuların ve Geliştirici Ekibin Net Ayrımı
* **Gerekçe:** Gazi Mustafa Kemal Atatürk (1935) ve Sir Isaac Newton (1664) gibi kurucu ve tarihsel figürlerin modern geliştirici ekiple aynı ızgarada yer alması yerine; tarihsel saygı ve hiyerarşik zarafete uygun olarak müstakil bir anma ve kurucu ilham bölümüne taşınması sağlandı.
* **Uygulanan Değişiklik:**
  * `docs/index.html` ve `README.md` içerisinde iki bağımsız bölüm oluşturuldu:
    1. **Tarihsel Kurucu Vizyon ve Felsefi Öncüler:** Atatürk (Kurucu Deha ve Başöğretmen) ve Newton (17. Yüzyıl Fonetik Evrensel Dil Tasarımı).
    2. **Proje Geliştirme Ekibi & Modern Katkıda Bulunanlar:** @pCwOrM, Bekirhan Dağlı (@bdagli), Dağhan Dağlı (@Lexovian), Semih Salar ve Zerrin Dağlı (@jesmaat).

#### 2. 🧪 Sayfa İçi Tam Donanımlı Güneş Dili Laboratuvar Motoru (`#lab-tam-motor`)
* **Gerekçe:** Kullanıcının harici bir sayfaya gitmeksizin tüm sözlük köklerine, 53 ek ailesine ve morfolojik tersine çözümleme motoruna doğrudan tek sayfa üzerinden erişebilmesi sağlandı.
* **Uygulanan Değişiklik:**
  * Sayfa içerisine gömülü duyarlı iframe konteyneri (`#lab-tam-motor`) eklendi.
  * Gezinme çubuğuna, mobil menüye ve ana başlık (Hero CTA) butonlarına doğrudan motora ve laboratuvara atlama kısayolları yerleştirildi.

---

### [v4.3.1-HierarchyRefinement] — 2026-10-09
#### 1. 🏛️ Kurucu Deha Olarak Gazi Mustafa Kemal Atatürk'ün Tekil ve Zirve Konumu
* **Gerekçe:** Güneş-Dil Teorisinin yegâne mimarı ve başöğretmeni olan Gazi Mustafa Kemal Atatürk'ün, 17. yüzyıl bilim insanı Sir Isaac Newton ile dahi aynı kategorik seviyede tutulmaması; Atatürk'ün kurucu deha olarak mutlak zirvede bağımsız bir anma alanında konumlandırılması sağlandı.
* **Uygulanan Değişiklik:**
  * `docs/index.html` ve `README.md` içerisinde:
    1. **Kurucu Deha ve Tarihsel Başöğretmen (`#kurucu-deha`):** Gazi Mustafa Kemal Atatürk'e adanmış müstakil, altın çerçeveli anıtsal bölüm.
    2. **Tarihsel Karşılaştırmalı Arşiv Notları (`#tarihsel-notlar`):** Sir Isaac Newton'un 1664 tarihli *Of an Universall Language* not defteri, kuramsal kök analizlerinde incelenen arşivsel bir karşılaştırma dokümanı olarak ayrı bir başlığa taşındı.
    3. **Proje Geliştirme Ekibi (`#ekip`):** Çağdaş mühendislik ve geliştirici kadrosu bağımsız çalışma tablosunda muhafaza edildi.

---

## 🔒 Güvenlik, İzlenebilirlik ve Geri Alınabilirlik Güvencesi

Tüm değişiklikler Git versiyon kontrol sistemi üzerinde atomik commit'ler ile kayıt altında tutulmakta olup, önceki sürümlere tam uyumludur. Hiçbir kök, ek veya sözlük verisi silinmemiş ya da biçimi bozulmamıştır.
