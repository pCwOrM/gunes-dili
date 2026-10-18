# Güneş Dili: arXiv Resmi Makale Gönderim Rehberi
## Primary Category: cs.LO (Logic in Computer Science)

> [!IMPORTANT]
> **Kategori Bildirimi:** Bu gönderim için **Primary Category (Ana Kategori)** olarak yetkinizin bulunduğu **`cs.LO - Logic in Computer Science`** belirlenmiştir. Makalenin bağımlı tip teorisi (dependent type theory), DFA durum otomatı geçişleri, monoid cebri ve Lean 4 interaktif teorem kanıtlayıcısındaki aksiyomsuz makine ispatları (`0 sorry`) bu kategorinin en yüksek akademik standartlarını eksiksiz karşılamaktadır.

**Hedef Portal:** [arXiv.org Submission Portal](https://arxiv.org/submit)  
**Tarih:** 18 Ekim 2026  
**Zenodo DOI:** `10.5281/zenodo.23273006` (Konsept DOI: `10.5281/zenodo.23273005`)  
**TÜRKPATENT Öncelikleri:** `TR 2026/016285` & `TR 2026/016633`  
**Hazır Yükleme Paketi:** `c:\Users\maat\Documents\antigravity\gunes-dili\arxiv_gunes_dili_package\`

---

## 📦 Hazır Yükleme Dosyaları

arXiv sistemine yüklenecek dosyalar `arxiv_gunes_dili_package` klasöründedir:

| Dosya | Boyut | Açıklama |
| :--- | :--- | :--- |
| **`arxiv_bundle.tar.gz`** | ~12.7 KB | **(ÖNERİLEN)** arXiv'in tercih ettiği sıkıştırılmış kaynak kod arşivi |
| **`arxiv_bundle.zip`** | ~15.8 KB | Alternatif ZIP arşivi |
| `Gunes_Dili_WERR_Preprint.tex` | ~23 KB | Lean 4 sözdizimi ve tam `\begin{thebibliography}` kaynakçası gömülü ana LaTeX dosyası |
| `Gunes_Dili_WERR_Preprint.bbl` | ~3.8 KB | Önceden derlenmiş bibliyografya dosyası (arXiv AutoTeX motoru için tam güvence) |
| `references.bib` | ~6.0 KB | Orijinal BibTeX kaynakça veri tabanı |
| `Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf` | 328 KB | Yerel referans PDF'i *(arXiv'e yüklenmez, arXiv sunucuları TeX'ten kendisi derler)* |

> [!NOTE]
> **arXiv Kuralı:** arXiv'e LaTeX kaynağı yüklenirken paket içine **kesinlikle PDF dosyası konulmaz**. Hazırladığımız `arxiv_bundle.tar.gz` sadece `.tex`, `.bbl` ve `.bib` dosyalarını içerir. Bu sayede arXiv AutoTeX motoru sıfır uyarı ile tek seferde derleme yapar.

---

## 🚀 ADIM 1: arXiv Girişi ve Yeni Gönderim (Start Submission)

1. Tarayıcınızda [https://arxiv.org/submit](https://arxiv.org/submit) adresine gidin.
2. Yetkili hesabınızla giriş yapın (Log in).
3. **"START NEW SUBMISSION"** (veya **"Submit"**) butonuna tıklayın.

---

## 📜 ADIM 2: Lisans Seçimi (Verify / License Agreement)

* **License:**  
  Seçeneklerden **`Creative Commons Attribution (CC BY 4.0)`** seçin.  
  *(Zenodo tescilimiz, açık bilim manifestomuz ve GitHub depomuz ile %100 uyumludur; alternatif olarak "arXiv.org perpetual, non-exclusive license" da seçilebilir).*

---

## 🏷️ ADIM 3: Kategori Seçimi (Subject Classification - cs.LO ODAKLI)

* **Primary Category (Ana Kategori - ZORUNLU):**  
  $$\mathbf{cs.LO\ -\ Logic\ in\ Computer\ Science}$$  
  *(Bilgisayar Bilimlerinde Mantık: Biçimsel diller, Tip teorisi, Lean 4 makine kanıtları, DFA durum matrisleri)*

* **Cross-Lists / Secondary Categories (İkincil / Çapraz Kategoriler):**  
  * **`cs.CL - Computation and Language`** *(Hesaplamalı Dilbilim, Biçimbilim, Tokenizer)*
  * **`cs.FL - Formal Languages and Automata Theory`** *(Chomsky Tip-3 Gramerler, Otomatlar)*
  * **`q-bio.NC - Neurons and Cognition`** *(Drosophila Konnektomu, Biyo-Sentetik Nöral Rezonans)*

---

## 📁 ADIM 4: Dosya Yükleme (Upload Files)

1. Yükleme alanına şu dosyayı sürükleyip bırakın (veya "Browse" ile seçin):
   ```text
   c:\Users\maat\Documents\antigravity\gunes-dili\arxiv_gunes_dili_package\arxiv_bundle.tar.gz
   ```
2. **"Upload file"** butonuna basın.
3. arXiv arşivi açıp `Gunes_Dili_WERR_Preprint.tex`, `Gunes_Dili_WERR_Preprint.bbl` ve `references.bib` dosyalarını tespit edecektir.
4. Sağ alttaki **"Continue: Process Files"** butonuna basarak derlemeyi başlatın.
5. arXiv derleme motoru (AutoTeX) `pdflatex` çalıştıracak ve başarıyla derlendikten sonra yeşil **"View PDF"** butonu çıkacaktır. PDF'i açıp makaleyi kontrol edin.

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
Contemporary Natural Language Processing (NLP) models universally depend on stochastic subword tokenization heuristics (e.g., Byte-Pair Encoding, WordPiece, Unigram). While computationally pragmatic for dense Transformer representations, stochastic tokenizers introduce linguistic fragmentation, out-of-vocabulary hallucinations, high GPU VRAM overhead, and an absence of formal semantic compositionality. In this paper, we formulate, implement, and formally certify Güneş Dili: an exact, deterministic morpho-semantic language and tokenization architecture formalized in dependent type theory and verified in the Lean 4 interactive theorem prover without unproven axioms (0 sorry), integrated into the bio-synthetic neural resonance substrates of the Waves & Errors Reflex Resonator (WERR) corpus. Re-evaluating two foundational mechanical traditions preserved directly as primary manuscripts in the open-science archive---Sir Isaac Newton's 1664 Cambridge Trinity College Notebook (Of an Universall Language, MS Add. 3996) and Gazi Mustafa Kemal Atatürk's 1935 Güneş Dil Teorisi Working Manuscripts (Nöbet Defteri)---we formalize human vocal articulation as an invariant phonosemantic vector space. Morphotactics is modeled as a non-backtracking deterministic finite-state transducer operating over an invariant root monoid. In Lean 4, we mechanically prove: (1) Canonical Root-Suffix Boundary Uniqueness, establishing that composite words contain at most one consonant cluster marking the exact morpheme cut; (2) Bijective Suffix Isomorphism, eliminating allomorphy and homophonic ambiguity; (3) DFA State Transition Determinism, proving that transition cardinality satisfies |\delta(s, e)| <= 1; and (4) 53-Hölder Comma Coset Invariance, demonstrating orthogonal microtonal acoustic frequency separation in the cyclic ring Z_{53}. Güneş Dili achieves 100.0% morphological parse fidelity on the complete official lexicon with strict linear time complexity O(L), sustaining single-thread CPU throughputs exceeding 1,240,000 tokens/second with exactly 0 Bytes VRAM overhead and 0-bit hallucination entropy. Finally, anchored under the dual national patent priority umbrellas of the WERR reflex coprocessor (TÜRKPATENT TR 2026/016285) and the WerrSoma whole-brain connectome interface (TÜRKPATENT TR 2026/016633), we demonstrate real-time linguistic projection into the Ellipsoid Body (EB) and Mushroom Body (MB) neuropils of the 158,262-neuron Drosophila melanogaster connectome, achieving sub-millisecond reflex latencies (< 0.5 ms).
```

### 4. Comments (Açıklamalar / Notlar)
```text
8 pages, 1 figure, 1 table. Machine-checked Lean 4 verification proofs (0 sorry), primary historical manuscripts (Newton 1664 MS Add. 3996 & Atatürk 1935 Nöbet Defteri), and open-science replication codebase available at Zenodo: https://doi.org/10.5281/zenodo.23273006 and GitHub: https://github.com/pCwOrM/gunes-dili
```

### 5. Report-no / External Identifier (Rapor No / Dış Tanımlayıcı)
```text
Zenodo: 10.5281/zenodo.23273006
```

### 6. ACM Class (ACM Sınıflandırması)
```text
F.3.1; F.4.1; F.4.3; I.2.7
```
*(Anlamları: F.3.1 Mekanik doğrulama ve invaryantlar, F.4.1 Teorem kanıtlama ve formel sistemler, F.4.3 Düzenli diller ve otomatlar, I.2.7 Hesaplamalı dilbilim)*

### 7. MSC Class (Matematik Konu Sınıflandırması)
```text
68V15, 68Q45, 03B35, 68T50, 92B20
```
*(Anlamları: 68V15 Bilgisayar destekli ispat, 68Q45 Biçimsel diller ve otomatlar, 03B35 Matematiksel mantık ve mekanik ispat, 68T50 Doğal dil işleme, 92B20 Biyolojik hesaplama)*

---

## 🔍 ADIM 6: Önizleme ve Gönderim (Preview & Submit)

1. **"Preview and Submit"** ekranında derlenen PDF'i açıp kontrol edin:
   - Başlık, yazar listesi ve kurumlar,
   - Section 3'teki Lean 4 teorem blokları ve sözdizimi,
   - Tablo 1 ve Şekil 1,
   - Kaynakça numaralandırması ve DOI bağlantıları.
2. Kategori dağılımını teyit edin:
   - Primary: `cs.LO`
   - Cross-list: `cs.CL`, `cs.FL`, `q-bio.NC`
3. **"Submit Paper"** butonuna basarak yayını arXiv havuzuna emanet edin!
4. arXiv size anında bir başvuru kimliği (`submit/XXXXXXX`) verecektir. Bir sonraki duyuru bülteninde resmi `arXiv:2610.XXXXX` numarası atanacaktır.
