# 🛡️ ZENODO YÜKLEME REHBERİ (GÜNEŞ DİLİ PREPRINT & REPLICATION PACKAGE)

> [!IMPORTANT]
> **ÖNCELİK VE PATENT KORUMA DURUMU:**
> Güneş Dili yayını, WERR külliyatının halihazırda tescilli **çift ulusal patent önceliği** altına resmi olarak mühürlenmiştir:
> 1. **TÜRKPATENT TR 2026/016285** (Başvuru: 22 Eylül 2026, 04:52:16 UTC+3 - OED / MFNS / WERR Karar Motoru)
> 2. **TÜRKPATENT TR 2026/016633** (Başvuru: 27 Eylül 2026, 06:16:04 UTC+3 - Biyo-Sentetik Nöromorfik Drosophila Konnektom BCI)
> Bu sayede ayrı bir patent süreci beklenmeksizin Zenodo üzerinde açık bilim önbaskısı (preprint) olarak anında yayımlanabilir.

---

## 1. Hazırlanan ve Yüklenecek Dosyalar (`zenodo_package/`)

Zenodo arayüzünde **"Files"** bölümüne sürüklenecek ana dosyalar:

1. **`zenodo_bundle_gunes_dili_v1.0.zip`:**
   * Python motoru (`tokenizer/`, `engine/`), TDK sözlük ve model matrisleri (`gunes_dil_model.json`, `tdk_kokler.json`), Lean 4 makine teyitli kanıtları (`proofs/GunesDiliProof.lean`) ve LaTeX makale kaynaklarını içeren tam replikasyon paketi.
2. **`Gunes_Dili_WERR_Preprint.tex` & `references.bib`:**
   * Tam akademik LaTeX makale kaynağı ve BibTeX bibliyografyası.

---

## 2. Zenodo Web Arayüzü Alanları (Kopyala-Yapıştır Rehberi)

Zenodo'ya ([zenodo.org](https://zenodo.org)) giriş yapıp **"New Upload"** dedikten sonra alanları aşağıdaki gibi doldurunuz:

### A. Temel Bilgiler (Basic Information)
* **Resource Type:** `Publication` $\to$ `Preprint`
* **Title:**
  ```text
  Güneş Dili: Deterministic Morpho-Semantic Tokenization, Machine-Checked Lean 4 Verification, and Bio-Synthetic Neural Resonance in the WERR Corpus
  ```
* **Publication Date:** `2026-10-10`

---

### B. Yazarlar ve Kurumsal Künyeler (Authors / Creators)

Sıralama WERR külliyatı ve akademik protokol standartlarına uygundur:

1. **1. Yazar (First / Lead Author):**
   * **Family name:** `Dağlı` | **Given names:** `Dağhan`
   * **Affiliation:** `Toros Science High School, Mersin Education Foundation (Toros University) & ITouch Systems, Türkiye`
   * **ORCID:** `0009-0003-2492-8313`

2. **2. Yazar (Corresponding Author):**
   * **Family name:** `Dağlı` | **Given names:** `Volkan`
   * **Affiliation:** `Anadolu University & ITouch Systems, Çukurova Teknokent, Türkiye`
   * **ORCID:** `0009-0000-1587-8703`

3. **3. Yazar:**
   * **Family name:** `Dağlı` | **Given names:** `Bekirhan`
   * **Affiliation:** `ITouch Systems, Çukurova Teknokent, Türkiye`

4. **4. Yazar:**
   * **Family name:** `Salar` | **Given names:** `Semih`
   * **Affiliation:** `ITouch Systems, Çukurova Teknokent, Türkiye`

5. **5. Yazar:**
   * **Family name:** `Dağlı` | **Given names:** `Zerrin`
   * **Affiliation:** `Mersin University & Yusuf Kalkavan Anatolian High School, Türkiye`
   * **ORCID:** `0000-0001-9490-6425`

---

### C. Açıklama (Description)
*Klasördeki `zenodo_description.html` dosyasının içeriğini doğrudan kopyalayıp Zenodo "Description" editörüne yapıştırınız.*

---

### D. Anahtar Kelimeler (Keywords)
Aşağıdaki kelimeleri ekleyiniz:
```text
Güneş Dili, Deterministic Tokenization, Formal Morphology, Phonosemantics, Lean 4 Theorem Prover, Interactive Theorem Prover, WERR, Neuromorphic Computing, Drosophila Melanogaster Connectome, Bio-Synthetic BCI, Zero VRAM, Agglutinative Languages, Turkish NLP
```

---

### E. Lisans (License) & Erişim (Access Right)
* **Access Right:** `Open Access`
* **License:** `Creative Commons Attribution 4.0 International (CC-BY-4.0)`

---

### F. İlgili Tanımlayıcılar (Related Identifiers)
* `https://github.com/Lexovian/gunes-dili` $\to$ `isSupplementTo` (URL)
* `https://github.com/Lexovian/WerrSoma` $\to$ `isSupplementTo` (URL)
* `arXiv:2609.33066` $\to$ `isPreprintOf` (arXiv)
* `arXiv:2609.30115` $\to$ `isPreprintOf` (arXiv)
* `arXiv:2609.30719` $\to$ `isPreprintOf` (arXiv)
* `arXiv:2609.25498` $\to$ `isPreprintOf` (arXiv)
* `arXiv:2609.38492` $\to$ `isPreprintOf` (arXiv)
* `10.5281/zenodo.22939253` $\to$ `isSupplementTo` (DOI)
* `10.5281/zenodo.22983889` $\to$ `isSupplementTo` (DOI)

---

### G. Topluluklar (Communities)
* `zenodo`
* `computational-linguistics`
* `computer-science`

---

## 3. Yayım Sonrası Alınacaklar ve Repo Güncellemesi

1. "Publish" butonuna tıklandığında Zenodo otomatik olarak kalıcı bir DOI tahsis eder (Örn: `10.5281/zenodo.23xxxxx`).
2. Tahsis edilen bu DOI numarası `README.md` dosyasındaki Zenodo rozetine eklenir:
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23xxxxx.svg)](https://doi.org/10.5281/zenodo.23xxxxx)
   ```
3. İlgili DOI ve arXiv kayıtları külliyatın diğer repolarına çapraz referans (cross-reference) olarak eklenir.
