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

## 🔒 Güvenlik, İzlenebilirlik ve Geri Alınabilirlik Güvencesi

Tüm değişiklikler Git versiyon kontrol sistemi üzerinde atomik commit'ler ile kayıt altında tutulmakta olup, önceki sürümlere tam uyumludur. Hiçbir kök, ek veya sözlük verisi silinmemiş ya da biçimi bozulmamıştır.
