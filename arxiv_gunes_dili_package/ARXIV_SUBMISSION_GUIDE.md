# Güneş Dili: arXiv Adım Adım Makale Gönderim Rehberi
## Deterministic Morpho-Semantic Tokenization, Machine-Checked Lean 4 Verification, and Bio-Synthetic Neural Resonance in the WERR Corpus

**Hedef Portal:** [arXiv.org Submission Portal](https://arxiv.org/submit)  
**Tarih:** 11 Ekim 2026  
**Zenodo DOI:** `10.5281/zenodo.23273006` (Konsept DOI: `10.5281/zenodo.23273005`)  
**TÜRKPATENT Öncelikleri:** `TR 2026/016285` & `TR 2026/016633`  
**Yerel Paket Dizini:** `c:\Users\maat\Documents\antigravity\gunes-dili\arxiv_gunes_dili_package\`

---

## 📦 Hazırlanan Yükleme Dosyaları

arXiv sistemine yüklenecek paket `arxiv_gunes_dili_package` klasöründe hazırdır:

| Dosya | Boyut | Açıklama |
| :--- | :--- | :--- |
| **`arxiv_bundle.tar.gz`** | ~11.4 KB | **(ÖNERİLEN)** arXiv'in tercih ettiği sıkıştırılmış kaynak kod arşivi |
| **`arxiv_bundle.zip`** | ~14.5 KB | Alternatif ZIP arşivi |
| `Gunes_Dili_WERR_Preprint.tex` | ~23 KB | Bağımsız, `\begin{thebibliography}` ve Lean 4 renklendirmesi gömülü ana LaTeX dosyası |
| `Gunes_Dili_WERR_Preprint.bbl` | ~3.8 KB | Önceden derlenmiş bibliyografya dosyası (arXiv BibTeX çalıştırmaz, bu dosya garantidir) |
| `references.bib` | ~6.0 KB | Orijinal BibTeX kaynakçası |
| `Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf` | ~342 KB | Yerel referans PDF'i *(arXiv'e yüklenmez, arXiv sunucuları TeX'ten kendisi derler)* |

> [!IMPORTANT]
> **arXiv Kuralı:** arXiv'e LaTeX kaynağı yüklenirken paket içine **asla PDF konulmaz**. Hazırladığımız `arxiv_bundle.tar.gz` sadece `.tex`, `.bbl` ve `.bib` dosyalarını içerir; bu sayede arXiv AutoTeX motoru sıfır hata ile tek seferde derleme yapar.

---

## 🚀 ADIM 1: arXiv Girişi ve Yeni Gönderim (Start Submission)

1. Tarayıcınızda [https://arxiv.org/submit](https://arxiv.org/submit) adresine gidin.
2. Hesabınıza giriş yapın.
3. **"START NEW SUBMISSION"** (veya **"Submit"**) butonuna tıklayın.

---

## 📜 ADIM 2: Lisans Seçimi (Verify / License Agreement)

* **License:**  
  Seçeneklerden **`Creative Commons Attribution (CC BY 4.0)`** seçin.  
  *(Zenodo kaydımız ve açık erişim standartlarımızla %100 uyumludur; alternatif olarak "arXiv.org perpetual, non-exclusive license" da seçilebilir).*

---

## 🏷️ ADIM 3: Kategori Seçimi (Subject Classification)

* **Primary Category (Ana Kategori):**  
  $$\mathbf{cs.CL\ -\ Computation\ and\ Language}$$  
  *(Hesaplamalı Dilbilim, NLP, Biçimbilim, Tokenizer)*

* **Cross-Lists / Secondary Categories (İkincil / Çapraz Kategoriler):**  
  * **`cs.FL - Formal Languages and Automata Theory`** *(Chomsky Tip-3 Gramer, DFA)*
  * **`cs.LO - Logic in Computer Science`** *(Lean 4 Makine İspatları, Formal Doğrulama)*
  * **`q-bio.NC - Neurons and Cognition`** *(Drosophila Konnektomu, Biyo-Sentetik Nöral Rezonans)*

---

## 📁 ADIM 4: Dosya Yükleme (Upload Files)

1. arXiv yükleme alanına şu dosyayı sürükleyip bırakın (veya "Browse" ile seçin):
   ```text
   c:\Users\maat\Documents\antigravity\gunes-dili\arxiv_gunes_dili_package\arxiv_bundle.tar.gz
   ```
2. **"Upload file"** butonuna basın.
3. arXiv arşivi açıp `Gunes_Dili_WERR_Preprint.tex` ve `Gunes_Dili_WERR_Preprint.bbl` dosyalarını listeleyecektir.
4. Sağ alttaki **"Continue: Process Files"** butonuna basarak derlemeyi başlatın.
5. arXiv derleme motoru (AutoTeX) çalışacak ve başarıyla derlendikten sonra yeşil **"View PDF"** butonu çıkacaktır. PDF'i açıp makaleyi kontrol edin.

---

## ✍️ ADIM 5: Üstveri Alanlarını Doldurma (Metadata)

Aşağıdaki kutuları doğrudan kopyalayıp arXiv formundaki ilgili alanlara yapıştırın:

### 1. Title (Başlık)
```text
Güneş Dili: Deterministic Morpho-Semantic Tokenization, Machine-Checked Lean 4 Verification, and Bio-Synthetic Neural Resonance in the WERR Corpus
```

### 2. Authors (Yazarlar)
```text
Volkan Dağlı, Bekirhan Dağlı, Dağhan Dağlı, Semih Salar, Zerrin Dağlı
```

### 3. Abstract (Özet - arXiv Form Kutusu İçin)
```text
Contemporary Natural Language Processing (NLP) models universally depend on stochastic subword tokenization heuristics (e.g., Byte-Pair Encoding, WordPiece, Unigram). While computationally pragmatic for dense Transformer representations, stochastic tokenizers introduce linguistic fragmentation, out-of-vocabulary hallucinations, high GPU VRAM overhead, and an absence of formal semantic compositionality. In this paper, we formulate, implement, and empirically validate Güneş Dili: an exact, deterministic morpho-semantic tokenization architecture grounded in atomic phonosemantic coordinates, formally verified in the Lean 4 interactive theorem prover, and integrated into the bio-synthetic neural resonance substrates of the Waves & Errors Reflex Resonator (WERR) corpus. Re-evaluating the 1935 Güneş Dil Teorisi through the lens of formal language theory and algebraic topology, we model every phoneme as an invariant vector endowed with an articulatory coordinate, an acoustic frequency, and an optical photonic carrier mapping (\lambda \in [380, 750] nm). Agglutinative morphotactics is modeled as a non-backtracking deterministic finite-state transducer operating over an invariant root monoid. Güneş Dili achieves 100.0% morphological parse fidelity on standard lexicons with strict linear time complexity O(L), sustaining single-thread CPU throughputs exceeding 1,200,000 tokens/second with exactly 0 Bytes VRAM overhead and 0-bit hallucination entropy. All core computational properties—including deterministic parsing uniqueness, terminating length-decreasing reduction, topological semantic kernel invariance, and vowel harmony soundness—are formally proved in Lean 4 without non-standard axioms. Finally, anchored under the dual patent priority umbrellas of the WERR reflex coprocessor (TÜRKPATENT TR 2026/016285) and the WerrSoma whole-brain connectome interface (TÜRKPATENT TR 2026/016633), we demonstrate real-time linguistic projection into the Ellipsoid Body (EB) and Mushroom Body (MB) neuropils of the 158,262-neuron Drosophila melanogaster connectome, achieving sub-millisecond linguistic reflex latencies (< 0.5 ms).
```

### 4. Comments (Açıklamalar / Notlar)
```text
8 pages, 1 figure, 1 table. Lean 4 formal verification proofs, interactive web simulator, and historical primary manuscripts openly available at Zenodo: https://doi.org/10.5281/zenodo.23273006 and GitHub: https://github.com/pCwOrM/gunes-dili
```

### 5. Report-no / External Identifier (Rapor No / Dış Tanımlayıcı)
```text
Zenodo: 10.5281/zenodo.23273006
```

### 6. ACM Class (ACM Sınıflandırması)
```text
I.2.7; F.4.3; F.3.1; J.3
```

### 7. MSC Class (Matematik Konu Sınıflandırması)
```text
68T50, 68Q45, 68V15, 92B20
```

---

## 🔍 ADIM 6: Önizleme ve Onay (Preview & Submit)

1. **"Preview and Submit"** aşamasında derlenen PDF'i son kez gözden geçirin.
2. Metadata özetini kontrol edin (Başlık, yazarlar, kategori: `cs.CL`).
3. **"Submit Paper"** butonuna basarak başvuruyu tamamlayın.
4. arXiv size bir takip numarası (`submit/XXXXXXX`) verecektir. Makale bir sonraki duyuru döngüsünde kalıcı bir `arXiv:2610.XXXXX` kimliğiyle dünya çapında yayına girecektir.
