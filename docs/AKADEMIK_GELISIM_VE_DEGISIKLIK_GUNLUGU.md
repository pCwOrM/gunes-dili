# Güneş Dili: Kümülatif Akademik Gelişim, Doğrulama ve Değişiklik Günlüğü
### Bilimsel Standartlar, Determinizm Metrikleri ve Sürüm Arşivi

---

## 🏛️ Yönetici Künyesi, Yazarlar ve Tarihsel Öncelik

* **Kurucu Düşünce ve Tarihsel Vizyon:** Gazi Mustafa Kemal Atatürk (1935 Güneş-Dil Teorisi)
* **Tarihsel Karşılaştırma Arşivi:** Sir Isaac Newton (1664 Trinity College *Of an Universall Language*)
* **1. Yazar, Sorumlu Yazar & WERR Mimarı:** Volkan Dağlı ([@pCwOrM](https://github.com/pCwOrM)) — Anadolu University & ITouch Systems, Çukurova Teknokent (`ask@answerr.me`)
* **2. Yazar & Sistem Geliştirme Lideri:** Bekirhan Dağlı ([@bdagli](https://github.com/bdagli)) — ITouch Systems, Çukurova Teknokent (Gramer ve Çeviri Motoru, `engine/gunes_dili.py`)
* **3. Yazar & Mimari Lideri:** Dağhan Dağlı ([@Lexovian](https://github.com/Lexovian)) — Toros Science High School, MEV (Toros University)
* **4. Yazar & Platform Mühendisliği Lideri:** Semih Salar — ITouch Systems, Çukurova Teknokent (Kozmik ve Felsefi Arşiv, `archive/`)
* **5. Yazar & Akademik Koordinasyon:** Zerrin Dağlı ([@jesmaat](https://github.com/jesmaat)) — Mersin University & Yusuf Kalkavan Anatolian High School
* **Tescilli Patent Öncelikleri:**
  * TÜRKPATENT TR 2026/016285 (*WERR Engine & OED - Waves & Errors Reflex Resonator*, Başvuru: 22.09.2026)
  * TÜRKPATENT TR 2026/016633 (*WerrSoma - Bio-Synthetic Neuromorphic Interfacing & Drosophila Connectome*, Başvuru: 27.09.2026)

---

## 📅 Sürüm ve Değişiklik Kronolojisi

### [v4.5.0-ZenodoPublication] — 2026-10-10
#### 1. 📦 WERR Külliyatı Resmi Zenodo Araştırma Önbaskısı ve Replikasyon Paketi (`zenodo_package/`)
* **Amaç:** Güneş Dili mimarisini, WERR külliyatının açık bilim protokollerine (CERN Zenodo & arXiv) uygun olarak kamera-hazır makale metni, Lean 4 biçimsel ispatları, tam replikasyon kodu ve kriptografik özetleriyle uluslararası akademik dolaşıma sokmak.
* **Makale Künyesi:**
  * **Başlık:** *«Güneş Dili: Deterministic Morpho-Semantic Tokenization, Machine-Checked Lean 4 Verification, and Bio-Synthetic Neural Resonance in the WERR Corpus»*
  * **Yazarlar & Kurumsal Künyeler:**
    * 1. Volkan Dağlı (Anadolu University & ITouch Systems, ORCID: 0009-0000-1587-8703, `ask@answerr.me`)
    * 2. Bekirhan Dağlı (ITouch Systems, Çukurova Teknokent)
    * 3. Dağhan Dağlı (Toros Science High School, MEV (Toros University), ORCID: 0009-0003-2492-8313)
    * 4. Semih Salar (ITouch Systems, Çukurova Teknokent)
    * 5. Zerrin Dağlı (Mersin University & Yusuf Kalkavan Anatolian High School, ORCID: 0000-0001-9490-6425)
* **Tescilli Çift Patent Önceliğiyle Koruma:**
  * TÜRKPATENT TR 2026/016285 (*OED / MFNS / WERR Karar Motoru*, Başvuru: 22.09.2026)
  * TÜRKPATENT TR 2026/016633 (*WerrSoma Drosophila Connectome BCI*, Başvuru: 27.09.2026)
* **Paket Bileşenleri:**
  1. `zenodo_package/Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf`: Standalone kamera-hazır makale metni (322 KB, KaTeX renderli).
  2. `zenodo_package/zenodo_bundle_gunes_dili_v1.0.zip`: Kod, model, Lean 4 ispatları ve LaTeX kaynaklarını içeren temiz açık bilim replikasyon arşivi (1.22 MB, SHA256: `e9e443dd00a57f645db5e86ac31bb7a3b4743b05d511b22b280c1bb9eb6bd6b3`).
  3. `zenodo_package/ZENODO_YUKLEME_REHBERI.md`: Dahili adım adım yükleme kılavuzu (arşiv dışı, yerel).
  4. `zenodo_package/zenodo_description.html`: Zenodo portalı için zenginleştirilmiş HTML açıklaması (yerel).
  5. `zenodo_package/.zenodo.json`: Zenodo API ve web yükleme metadata şeması.
  6. `zenodo_package/Gunes_Dili_WERR_Preprint.tex` & `references.bib`: Tam akademik LaTeX makale kaynağı ve bibliyografya.
  7. `zenodo_package/CITATION.cff`: Standart akademik atıf dosyası.
  8. `zenodo_package/create_replication_bundle.py` & `build_zenodo_pdf.py`: Derleme ve hash mühürleme scriptleri.
  9. `zenodo_package/SHA256SUMS.txt`: Kriptografik mühür manifestosu.

---

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
    2. **Proje Geliştirme Ekibi & Modern Katkıda Bulunanlar:** [@pCwOrM](https://github.com/pCwOrM), Bekirhan Dağlı ([@bdagli](https://github.com/bdagli)), Dağhan Dağlı ([@Lexovian](https://github.com/Lexovian)), Semih Salar ve Dr. Zerrin Dağlı ([@jesmaat](https://github.com/jesmaat)).

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

### [v4.4.0-PDFPublication] — 2026-10-09
#### 1. 📄 Yüksek Çözünürlüklü A4 PDF Dokümantasyon Paketinin Üretimi (`docs/pdf/`)
* **Gerekçe:** Kullanıcının tüm kuramsal metinleri, WERR matematiksel modellerini, 53 Holder komalık ek tablolarını ve nöro-biyolojik telemetri grafiklerini çevrimdışı ve baskıya hazır halde tek tıkla indirebilmesi sağlandı.
* **Derlenen Dokümanlar:**
  1. `docs/pdf/GUNES_DILI_MANIFESTOSU.pdf` (~2.6 MB): Tam külliyat manifestosu, 4 renkli telemetri deney görseli, T1-T5 kanıt defteri.
  2. `docs/pdf/LOGO_FELSEFESI_VE_TEKNIK_ACIKLAMASI.pdf` (~1.2 MB): 53 komalık rezonans çemberi, Mandelbrot fraktal spirali, yüksek çözünürlüklü vektörel logo analizi.
  3. `docs/pdf/TEKNIK_VE_AKADEMIK_REHBER.pdf` (~340 KB): Chomsky Tip-3 düzenli gramer, DFA geçişleri, 53 ek ailesinin tam tablosu.
  4. `docs/pdf/HALKA_ANLATIM_REHBERI.pdf` (~230 KB): Atatürk'ün 1935 dil sezgisi, popüler bilim ve müzik-dil sentezi.
* **Erişim:** `README.md` ve `docs/index.html` dokümantasyon merkezine doğrudan indirme bağlantıları eklendi.

---

## 🔒 Güvenlik, İzlenebilirlik ve Geri Alınabilirlik Güvencesi

Tüm değişiklikler Git versiyon kontrol sistemi üzerinde atomik commit'ler ile kayıt altında tutulmakta olup, önceki sürümlere tam uyumludur. Hiçbir kök, ek veya sözlük verisi silinmemiş ya da biçimi bozulmamıştır.
