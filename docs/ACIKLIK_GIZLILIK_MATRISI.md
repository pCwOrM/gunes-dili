# Güneş Dili Ekosistemi: Açık Bilim (Public Open Science) ve Fikri Mülkiyet Stratejisi

Bu belge; Güneş Dili monoreposunun (**`https://github.com/pCwOrM/gunes-dili`**) açık bilim, akademik yayın ve kamuya açılma (Public Open Science) mimarisini, patent öncelikleriyle uyumunu ve dizin standartlarını tanımlayan resmi strateji belgesidir.

---

## 🏛️ 1. Stratejik Temel: Patent Güvencesi ve Tam Açıklık İlkesi

Önceki taslaklarda yer alan *"belirli arşivlerin veya dosyaların özel kasada saklanması"* yaklaşımı, patent başvuruları öncesi koruma tedbirlerine dayanan geçici bir varsayımdı. 

Güncel durumda:
1. **Resmi Patent Tescil Süreçleri:** TÜRKPATENT nezdinde **TR 2026/016285** *(Yörüngesel Hata Dinamikleri ve Sıfır Bellekli Fraktal Sinirsel Sentez Yöntemi)* ve **TR 2026/016633** *(Biyo-Sentetik Nöromorfik Arayüzleme: Drosophila Connectome & BCI Entegrasyonu)* başvuruları resmi olarak yapılmıştır.
2. **Paris Sözleşmesi Rüçhan Koruması:** Patent başvuruları yapıldığı andan itibaren 12 aylık uluslararası rüçhan (priority) koruması devreye girmiştir.
3. **Açık Bilim & Öncelik Hakkı (Prior Art):** Zenodo önbaskısı ve GitHub deposunun kamuya açılması (**Public** yapılması), patent haklarına halel getirmediği gibi; yazarların adını, külliyatın tarihsel köklerini ve buluş önceliğini küresel düzeyde geri dönülemez biçimde tescilleyen en güçlü akademik savunma kalkanıdır.

Bu doğrultuda; **Güneş Dili reposunun tüm bileşenleri 100% Açık Bilim (Public Open Science) standardında kamuya açılacak şekilde kurgulanmıştır.**

---

## 📊 2. Depo Mimarisi ve Açıklık Sınıflandırma Tablosu

| Dizin / Dosya | Statü | Standart ve Kapsam | Açıklama ve Gerekçe |
| :--- | :---: | :--- | :--- |
| **`tokenizer/`** | 🟢 **PUBLIC** | Algoritmik Çekirdek | `gunes_dil_v4.py`, Universal Dependencies modeli (`gunes_dil_model.json`) ve TDK kök sözlüğü. Türkçe NLP topluluğu için deterministik O(N) morfolojik ayrıştırıcı. |
| **`engine/`** | 🟢 **PUBLIC** | Gramer & Çeviri Motoru | `gunes_dili.py` ve 53 ekin Mandelbrot faz koordinatları (`gunes_dili_koordinat.json`). Fonetik uyum ve tersine ayrıştırma standardı. |
| **`proofs/`** | 🟢 **PUBLIC** | Biçimsel Doğrulama | `GunesDiliProof.lean` (Lean 4 teorem kanıtları) ve `kanit_defteri.py`. T1-T5 morfolojik teklik teoremleri hakemli açık inceleme için tam şeffaftır. |
| **`archive/`** | 🟢 **PUBLIC** | Tarihsel & Kültürel Miras | Atatürk 1935 Nöbet Defteri, Newton 1664 elyazmaları, Kozmik/Kuantum metinleri ve 53 Ses Çemberi. İnsanlığın ortak mirası ve kültürel açık erişim olarak sunulmaktadır. |
| **`lab/`** | 🟢 **PUBLIC** | İnteraktif Web Simülatörü | Tarayıcı üzerinde istemci taraflı (client-side) çalışan interaktif görsel ayrıştırıcı ve 53 koma çarkı. |
| **`docs/`** | 🟢 **PUBLIC** | Canlı Portal ve Kılavuzlar | GitHub Pages canlı portalı (`docs/index.html`), teknik rehberler, akademik günlük ve lisans metinleri. |
| **`zenodo_package/`** | 🟢 **PUBLIC** | Akademik Önbaskı & Replikasyon | LaTeX kaynakları (`.tex`, `.bib`), kamera-hazır PDF, `.zenodo.json`, `CITATION.cff` ve bağımsız replikasyon arşivi. |
| **Yerel Geçici Dosyalar** | 🔒 **IGNORED** | `.gitignore` Koruması | Yalnızca Python derleme kalıntıları (`__pycache__/`, `*.pyc`), sanal ortamlar (`.venv/`) ve yerel `scratch/` dizini gizlenir; repoya dahil edilmez. |

---

## 🚀 3. Halka Arz (Public Rollout) ve Yayın İş Akışı

1. **Zenodo Önbaskı Kaydı:**
   - Resmi önbaskı PDF (`Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf`) ve replikasyon paketi (`zenodo_bundle_gunes_dili_v1.0.zip`) Zenodo platformuna yüklenir.
   - Kalıcı DOI (Digital Object Identifier) alınarak WERR külliyatı zincirine bağlanır.

2. **GitHub Deposunun Public Yapılması:**
   - `https://github.com/pCwOrM/gunes-dili` deposunun görünürlüğü GitHub ayarlarından `Private` durumundan `Public` durumuna geçirilir.
   - GitHub Pages yayını (`https://pcworm.github.io/gunes-dili/`) otomatik olarak küresel erişime açılır.

3. **Lisanslama ve Koruma:**
   - Açık kaynak kodları ve metinler **BBL v1.0 (Barış, Bilim, Liyakat & Beerware/Çay)** lisansı ve patent öncelik referanslarıyla birlikte korunur.
