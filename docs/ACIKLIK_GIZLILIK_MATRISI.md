# Güneş Dili Ekosistemi: Açıklık ve Gizlilik (Public vs. Private) Matrisi

Bu belge; Güneş Dili deposunda yer alan dosyaların, modellerin ve tarihsel arşivlerin hangilerinin gelecekte **Kamuya Açık (Public / Open-Source)** yapılabileceğini, hangilerinin ise **Özel ve Mülki (Private / Sovereign Vault)** olarak korunması gerektiğini belirleyen stratejik güvenlik ve fikri mülkiyet matrisidir.

---

## 📊 1. Dosya Sınıflandırma Matrisi

| Dosya / Dizin | Mevcut Durum | Önerilen Statü | Gerekçe ve Stratejik Neden |
| :--- | :---: | :---: | :--- |
| **`tokenizer/gunes_dil_v4.py`** | Private | 🟢 **PUBLIC** (Açılabilir) | Türkçe doğal dil işleme (NLP) ekosistemine kazandırılacak en güçlü açık kaynak tokenizer. Akademik atıf ve kabul üretir. |
| **`tokenizer/gunes_dil_model.json`** | Private | 🟢 **PUBLIC** (Açılabilir) | UD ağaç bankası istatistiksel modeli. Topluluğun doğrulaması için gereklidir. |
| **`tokenizer/tdk_kokler.json`** | Private | 🟢 **PUBLIC** (Açılabilir) | TDK kamuya açık kök listesi türevidir. Açılmasında risk yoktur. |
| **`engine/gunes_dili.py`** | Private | 🟢 **PUBLIC** (Açılabilir) | Dilin temel dilbilgisi kuralları ve tersine ayrıştırıcısı. Ekosistemin standartlaşması için açık olmalıdır. |
| **`engine/gunes_dili_koordinat.json`** | Private | 🟡 **RESTRICTED / YARI-AÇIK** | 53 ekin Mandelbrot koordinat haritası. Temel koordinatlar açılabilir, hassas eğitim ağırlıkları gizlenebilir. |
| **`lab/index.html` & `motor.js`** | Private | 🟢 **PUBLIC** (Açılabilir) | Web tarayıcısında çalışan interaktif tanıtım ve eğitim arayüzü. Topluluk etkileşimi için harika bir vitrindir. |
| **`proofs/kanit_defteri.py` & `.json`** | Private | 🟢 **PUBLIC** (Açılabilir) | Teoremlerin matematiksel ispatları. Hakemli dergiler ve akademik itibar için açık kanıt teşkil eder. |
| **`archive/ataturk_1935_gunes_dil/`** | Private | 🔴 **PRIVATE / SOVEREIGN** | Atatürk'ün el yazması notları ve 1-53 Nöbet Defteri yüksek çözünürlüklü taramaları. Milli ve manevi mülkiyet olarak özel kasada saklanmalıdır. |
| **`archive/newton_1664_universal_language/`** | Private | 🔴 **PRIVATE / SOVEREIGN** | Newton'un Trinity College defteri yüksek çözünürlüklü dijital arşivleri. Telif ve araştırma önceliği açısından özel tutulmalıdır. |
| **`archive/kozmik_ve_kuantum/`** | Private | 🔴 **PRIVATE / SOVEREIGN** | Henüz yayınlanmamış kozmik işletim sistemi ve kuantum palimpsest araştırma notları. Fikri mülkiyet önceliği nedeniyle gizli kalmalıdır. |
| **`archive/muzik_ve_53_ses_cemberi/`** | Private | 🟡 **RESTRICTED / ÖZEL** | 53 ses çemberinin ham analiz notları. Patent ve kurumsal yayın sonrasına kadar koruma altında tutulmalıdır. |

---

## 🛡️ 2. Kademeli Açılma (Phased Rollout) Stratejisi

1. **Aşama 1 (Mevcut Durum - Tamamen Private):**
   * Repo bütünüyle `pCwOrM/gunes-dili` altında gizli tutulur. Çekirdek ekip (`Lexovian`, `jesmaat`, `Bekirhan`) incelemelerini onay mekanizması altında sürdürür.
2. **Aşama 2 (Akademik Preprint & Ön Sürüm):**
   * Zenodo veya arXiv üzerinde teknik rapor yayınlandığında; sadece `tokenizer/`, `engine/` ve `lab/` modüllerinden oluşan hafif bir açık kaynak sürüm (`gunes-dili-core`) public repoya çıkarılır.
3. **Aşama 3 (Kasa ve Arşiv Ayrımı):**
   * Yüksek çözünürlüklü tarihi taramalar, patent taslakları ve nöbet defteri belgeleri (`archive/`) daima özel ve yetkilendirilmiş araştırma kasasında kalır.

---

## 👥 Katılımcı (Collaborator) Erişim Politikası

Depoya dahil edilen yetkili katılımcılar (**Lexovian**, **jesmaat**, **Bekirhan**):

1. **Özel ve Akademik Dizinlere Tam Erişim:**
   * Tier-2 (Akademik & Kanıtlar - `proofs/`, `engine/`, `tokenizer/`) ve Tier-3 (Tarihsel Kasa & Arşiv - `archive/`, `docs/`) dahil olmak üzere tüm dizinleri doğrudan klonlama, okuma ve yerel ortamlarında çalıştırma hakkına sahiptir.
2. **Dal Koruma ve Onay Mekanizması:**
   * Doğrudan `main` dalına push yetkisi kısıtlanmıştır; değişiklikler dal (branch) açılıp Pull Request (PR) üzerinden sunulur.
   * `.github/CODEOWNERS` yapılandırması uyarınca, akademik ve arşiv dizinlerindeki PR incelemelerinde katılımcılar otomatik incelemeci (reviewer) atanır; nihai birleştirme (merge) `@pCwOrM` onayıyla yürütülür.

