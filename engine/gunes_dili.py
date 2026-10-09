"""
GÜNEŞ DİLİ — kanıtlanabilir yapıda küresel eklemeli dil
======================================================

Tasarım ilkeleri ve dayanakları
-------------------------------
İ1  Ses envanteri dünyanın en yaygın seslerinden seçilir.
    Ünlüler: a e i o u   (WALS: 5 ünlülü sistem dünyada en yaygın; 564 dilin ~1/3'ü)
    Ünsüzler: m k n y s w p l b t g d f h r  (PHOIBLE: 913 dilde en sık 17 ünsüzün 15'i; /m/ %98,8)
İ2  Kök biçimi (K)Ü(KÜ)*K : kök ünsüzle biter, kök içinde ünsüz kümesi yoktur.
İ3  Ekler tam olarak KÜ (ünsüz+ünlü) biçimindedir; ek içinde ünsüz kümesi yoktur; ek biçimleri
    tektir (ünlü uyumu, benzeşme, kaynaştırma yok): 1 ek = 1 biçim = 1 işlev.
İ4  Ek ünsüzü işlev AİLESİNİ, ünlüsü ailedeki ÜYEYİ söyler. Aileler 1935 Güneş-Dil ek tablosunun
    (Tan, 15.11.1935) tutarlı hâle getirilmiş karşılığıdır: M = kendisi (1. kişi), N = bitişik
    (2. kişi), S = geniş saha (3. kişi), L = genellik (çokluk), T = yapıcılık (çatı), K = tamamlama
    (zaman), R = belli nokta (yer-yön halleri) ... Doğal dillerde bu eşleme kanıtlanamadı; Güneş
    Dili'nde ise TANIM GEREĞİ doğrudur.
İ5  Eklerin sırası kökten uzaklığa göredir (Tan 1935 Şekil 2'nin ego-merkez haritası):
    fiil:  KÖK · yapım* · çatı* · olumsuz · zaman · kip · ek-fiil · kişi · soru
    isim:  KÖK · yapım* · çokluk · iyelik · hal · aitlik · ek-fiil · kişi · soru
İ6  Güneş'in adı "ag"dır (1935'teki ilk kök). İ2'ye uyan geçerli bir köktür.

Teorem (tek çözümleme): Geçerli her Güneş Dili kelimesinin tam olarak bir kök+ek bölünmesi ve
tam olarak bir işlev dizisi vardır. Kanıt `teorem_kaniti()` içinde; ayrıca uzunluk sınırına kadar
kaba kuvvetle doğrulanır (`kaba_kuvvet_dogrulama`).
"""
import itertools
import json
import math
import os
import re
from dataclasses import dataclass

BURASI = os.path.dirname(os.path.abspath(__file__))
UNLU = "aeiou"
UNSUZ = "mknyswplbtgdfhr"

# ---------------------------------------------------------------------------
# Ek tablosu: aile ünsüzü -> (1935 anlamı, Güneş Dili işlevi, üyeler)
# ---------------------------------------------------------------------------
AILELER = {
    "m": ("kendisi", "1. kişi", {"mi": "1. tekil", "ma": "1. çoğul"}),
    "n": ("bitişik", "2. kişi", {"ni": "2. tekil", "na": "2. çoğul"}),
    "s": ("geniş saha", "3. kişi", {"si": "3. tekil", "sa": "3. çoğul"}),
    "l": ("uzak / genel", "çokluk", {"la": "çokluk"}),
    "t": ("yapıcılık", "çatı", {"ta": "ettirgen", "te": "edilgen", "ti": "dönüşlü", "to": "işteş", "tu": "yeterlik"}),
    "d": ("yapıcılık (olumsuz yön)", "olumsuzluk / soru", {"de": "olumsuz", "do": "soru"}),
    "k": ("tamamlama", "zaman", {"ka": "geçmiş", "ke": "şimdiki", "ki": "gelecek", "ko": "geniş", "ku": "duyulan geçmiş"}),
    "b": ("kendisi (dudak)", "kip", {"ba": "şart", "be": "istek", "bi": "emir", "bo": "gereklilik"}),
    "r": ("belli nokta", "yer-yön hali", {"ra": "bulunma", "re": "yönelme", "ro": "ayrılma", "ru": "belirtme", "ri": "ilgi"}),
    "w": ("tamamlama (dudak)", "ilişki hali / zarf", {"wi": "birliktelik", "wa": "eşitlik (gibi)", "wo": "amaç (için)",
                                                      "we": "zaman zarfı (-ınca)", "wu": "süre zarfı (-ken)"}),
    "g": ("tamamlama (art damak)", "tür değiştiren yapım", {"ga": "isimden fiil", "ge": "eylem adı", "gi": "yapan (fail)",
                                                             "go": "sahip (-li)", "gu": "soyut ad (-lik)"}),
    "p": ("kendisi (dudak)", "yapım / sıfat-fiil", {"pa": "yoksun (-siz)", "pe": "küçültme", "pi": "sıfat-fiil geçmiş",
                                                    "po": "sıfat-fiil şimdi", "pu": "bağ zarf-fiil (-arak)"}),
    "f": ("kendisi (dudak)", "yapım 2", {"fa": "sıra sayısı", "fe": "sıfat-fiil gelecek", "fi": "dil/tarz (-ca)",
                                         "fo": "ilgi sıfatı (-sal)", "fu": "üleştirme (-er)"}),
    "y": ("tamamlama (art damak)", "ek-fiil", {"ya": "hikâye (idi)", "ye": "rivayet (imiş)", "yi": "bildirme (-dir)"}),
    "h": ("tamamlama (art damak)", "aitlik / meslek", {"ha": "meslek, ilgili (-ci)", "hu": "aitlik (-ki)"}),
}
EK = {}
for c, (eski, aile, uyeler) in AILELER.items():
    for f, is_ in uyeler.items():
        EK[f] = (c, aile, is_)

# Yuva numaraları (kökten uzaklık). Tür geçişi: N isim, V fiil, Z zarf (kapanır)
YAPIM_TUR = {  # biçim: (giriş, çıkış)
    "ga": ("N", "V"), "ge": ("V", "N"), "gi": ("V", "N"), "go": ("N", "N"), "gu": ("N", "N"),
    "pa": ("N", "N"), "pe": ("N", "N"), "pi": ("V", "N"), "po": ("V", "N"), "pu": ("V", "Z"),
    "fa": ("N", "N"), "fe": ("V", "N"), "fi": ("N", "N"), "fo": ("N", "N"), "fu": ("N", "N"),
    "we": ("V", "Z"), "wu": ("V", "Z"), "ha": ("N", "N"),
}
Z_YAPIM = {"pu", "we", "wu"}      # zarf-fiiller zaman ekinden sonra da gelebilir (getir-ir-ken)
TEKRARLI = {"çatı"}               # çatı ekleri üst üste gelebilir (kural-laş-tır: ga-to-ta)
FIIL_YUVA = [("çatı", {"ta", "te", "ti", "to", "tu"}), ("olumsuz", {"de"}), ("zaman", {"ka", "ke", "ki", "ko", "ku"}),
             ("kip", {"ba", "be", "bi", "bo"}), ("ek-fiil", {"ya", "ye", "yi"}), ("kişi", {"mi", "ma", "ni", "na", "si", "sa"}),
             ("soru", {"do"})]
ISIM_YUVA = [("çokluk", {"la"}), ("iyelik", {"mi", "ma", "ni", "na", "si", "sa"}),
             ("hal", {"ra", "re", "ro", "ru", "ri", "wi", "wa", "wo"}), ("aitlik", {"hu"}),
             ("ek-fiil", {"ya", "ye", "yi", "ba"}), ("kişi", {"mi", "ma", "ni", "na", "si", "sa"}), ("soru", {"do"})]


# ---------------------------------------------------------------------------
# Biçim denetimleri
# ---------------------------------------------------------------------------
KOK_RE = re.compile(rf"^[{UNSUZ}]?[{UNLU}]([{UNSUZ}][{UNLU}])*[{UNSUZ}]$")


def kok_gecerli(k):
    return bool(KOK_RE.match(k))


def sinir_bul(w):
    """İ2+İ3: Kelimedeki tek ünsüz kümesi kök-ek sınırıdır. Döner: kök uzunluğu ya da None."""
    kumeler = [i for i in range(len(w) - 1) if w[i] in UNSUZ and w[i + 1] in UNSUZ]
    if not kumeler:
        return len(w) if w and w[-1] in UNSUZ else None
    if len(kumeler) > 1:
        return None
    return kumeler[0] + 1


def _kurallar(e, tur, yuva, gecmis):
    """(tür, yuva, geçmiş) durumunda e ekine uygulanabilen TÜM kurallar (determinizm denetimi için)."""
    k = []
    olumsuz_i = 1
    zaman_i = 2
    if e in YAPIM_TUR and YAPIM_TUR[e][0] == tur and (
            yuva == -1 or (tur == "V" and yuva <= olumsuz_i) or (tur == "V" and e in Z_YAPIM and yuva <= zaman_i)):
        k.append(("yapım", None))
    yuvalar = FIIL_YUVA if tur == "V" else ISIM_YUVA
    for i, (ad, kume) in enumerate(yuvalar):
        if (i < yuva or (i == yuva and ad not in TEKRARLI)) or e not in kume:
            continue
        if ad == "kişi":
            if tur == "N" and "ek-fiil" not in gecmis:
                continue
            if tur == "V" and not ({"zaman", "kip", "ek-fiil"} & gecmis):
                continue
        if ad == "iyelik" and "ek-fiil" in gecmis:
            continue
        k.append((ad, i))
        break                                          # sıra monotondur: ilk uygun yuva
    return k


def fsa(ekler, tur):
    """İ5 durum makinesi: ek dizisine işlev atar ya da None (geçersiz)."""
    sonuc = []
    yuva = -1
    gecmis = set()
    for e in ekler:
        if e not in EK or tur == "Z":
            return None
        k = _kurallar(e, tur, yuva, gecmis)
        if not k:
            return None
        ad, i = k[0]
        if ad == "yapım":
            tur = YAPIM_TUR[e][1]
            yuva = -1
            gecmis = set()
            sonuc.append((e, "yapım", EK[e][2], tur))
        else:
            yuva = i
            gecmis.add(ad)
            sonuc.append((e, ad, EK[e][2] if ad not in ("iyelik", "kişi") else f"{ad} {EK[e][2]}", tur))
    return sonuc


SOZLUK = {}          # Güneş Dili kökü -> (Türkçe kök, tür)
TR2GD = {}           # (Türkçe kök, tür) -> Güneş Dili kökü
_sp = os.path.join(BURASI, "gunes_dili_sozluk.json")
if os.path.exists(_sp):
    _d = json.load(open(_sp, encoding="utf-8"))
    for gd, (tr, tur) in _d.items():
        SOZLUK[gd] = (tr, tur)
        TR2GD[(tr, tur)] = gd


def cozumle(w):
    """Güneş Dili kelimesi -> {kok, tur, ekler:[(biçim, yuva, işlev, tür)]} ya da hata."""
    w = w.strip().lower()
    if not w or any(c not in UNLU + UNSUZ for c in w):
        return {"hata": "Güneş Dili alfabesi dışı harf (alfabe: " + UNLU + " + " + UNSUZ + ")"}
    s = sinir_bul(w)
    if s is None:
        return {"hata": "Kök-ek sınırı bulunamadı: kelimede birden fazla ünsüz kümesi var ya da kök ünsüzle bitmiyor"}
    kok, kalan = w[:s], w[s:]
    if not kok_gecerli(kok):
        return {"hata": f"'{kok}' geçerli bir kök biçimi değil ((K)Ü(KÜ)*K olmalı)"}
    if len(kalan) % 2:
        return {"hata": "Ek bölümü ünsüz+ünlü çiftlerine bölünemiyor"}
    ekler = [kalan[i:i + 2] for i in range(0, len(kalan), 2)]
    turler = list(SOZLUK[kok][1]) if kok in SOZLUK else []
    turler += [t for t in ("N", "V") if t not in turler]
    for tur in turler:
        f = fsa(ekler, tur)
        if f is not None:
            return {"kok": kok, "tur": tur, "ekler": f, "turkce": SOZLUK.get(kok, (None,))[0]}
    return {"hata": "Ek sırası Güneş Dili şablonuna aykırı", "kok": kok, "ekler_ham": ekler}


def uret(kok, ekler):
    return kok + "".join(ekler)


# ---------------------------------------------------------------------------
# Türkçe kökü Güneş Dili köküne uyarlama (ödünçleme kuralı)
# ---------------------------------------------------------------------------
HARF = {"ı": "i", "ö": "o", "ü": "u", "ç": "t", "c": "d", "ş": "s", "j": "s", "z": "s", "v": "w", "ğ": "g",
        "â": "a", "î": "i", "û": "u", "q": "k", "x": "ks"}


def uyarla(tr):
    """Türkçe kök -> İ2 biçimli Güneş Dili kökü (henüz çakışma çözülmemiş)."""
    s = "".join(HARF.get(c, c) for c in tr.lower())
    s = "".join(c for c in s if c in UNLU + UNSUZ)
    if not s:
        return None
    out = []
    for c in s:
        if out:
            p = out[-1]
            if p in UNSUZ and c in UNSUZ:                  # ünsüz kümesi: önceki ünlünün kopyası araya
                v = next((x for x in reversed(out) if x in UNLU), None)
                if v is None:
                    v = next((x for x in s if x in UNLU), "a")
                out.append(v)
            elif p in UNLU and c in UNLU:                  # ünlü yan yana: araya y
                out.append("y")
        out.append(c)
    if out[-1] in UNLU:                                    # kök ünsüzle biter: Türkçedeki zamir n'si gibi
        out.append("n")
    k = "".join(out)
    return k if kok_gecerli(k) else None


def sozluk_kur(tr_kokler, siklik, ozel=None):
    """Türkçe kökleri sıklık sırasıyla uyarlayıp çakışmasız (birebir) sözlük kurar."""
    ozel = ozel or {}
    sozluk, ters, cakisma = {}, {}, 0
    for (tr, tur), gd in ozel.items():
        sozluk[gd] = (tr, tur); ters[(tr, tur)] = gd
    sirali = sorted(tr_kokler, key=lambda x: (-siklik.get(x[0], 0), x[0], x[1]))
    for tr, tur in sirali:
        if (tr, tur) in ters:
            continue
        gd = uyarla(tr)
        if gd is None:
            continue
        # aynı Türkçe kök isim ve fiil olarak ayrı girerse aynı Güneş Dili kökünü paylaşsın
        diger = (tr, "V" if tur == "N" else "N")
        if diger in ters and sozluk.get(ters[diger], (None,))[0] == tr:
            ters[(tr, tur)] = ters[diger]
            sozluk[ters[diger]] = (tr, "NV")
            continue
        taban = gd
        n = 0
        while gd in sozluk:                                 # çakışma: ünlü kopyası + n eklenir
            cakisma += 1 if n == 0 else 0
            n += 1
            v = next(x for x in reversed(taban) if x in UNLU)
            gd = taban + (v + "n") * n
        sozluk[gd] = (tr, tur); ters[(tr, tur)] = gd
    return sozluk, ters, cakisma


# ---------------------------------------------------------------------------
# Türkçe çözümlemesinden Güneş Dili'ne çeviri (Türkçe çözümleyici: gunes_dil_v4)
# ---------------------------------------------------------------------------
ISLEV_ESLEME = [  # (Türkçe işlev öneki, Güneş Dili ek dizisi)
    ("çokluk", ["la"]), ("iyelik 1.tekil", ["mi"]), ("iyelik 2.tekil", ["ni"]), ("iyelik 3.tekil", ["si"]),
    ("iyelik 1.çoğul", ["ma"]), ("iyelik 2.çoğul", ["na"]), ("iyelik 3.çoğul", ["sa"]),
    ("belirtme", ["ru"]), ("ilgi hali", ["ri"]), ("yönelme", ["re"]), ("bulunma", ["ra"]), ("ayrılma", ["ro"]),
    ("vasıta", ["wi"]), ("eşitlik", ["wa"]), ("aitlik", ["hu"]),
    ("ek-fiil hikâye", ["ya"]), ("ek-fiil rivayet", ["ye"]), ("ek-fiil bildirme", ["yi"]), ("ek-fiil şart", ["ba"]),
    ("şahıs 1.tekil", ["mi"]), ("şahıs 2.tekil", ["ni"]), ("şahıs 1.çoğul", ["ma"]), ("şahıs 2.çoğul", ["na"]),
    ("şahıs 3.çoğul", ["sa"]),
    ("görülen geçmiş", ["ka"]), ("öğrenilen geçmiş", ["ku"]), ("şimdiki zaman", ["ke"]), ("gelecek zaman", ["ki"]),
    ("geniş zaman olumsuz (yeterlik)", ["tu", "de", "ko"]), ("geniş zaman olumsuz", ["de", "ko"]),
    ("geniş zaman", ["ko"]), ("şart", ["ba"]), ("gereklilik", ["bo"]),
    ("istek 1.çoğul", ["be", "ma"]), ("istek 1.tekil", ["be", "mi"]), ("istek", ["be"]),
    ("emir 2.çoğul", ["bi", "na"]), ("emir 3.tekil", ["bi", "si"]), ("emir 3.çoğul", ["bi", "sa"]),
    ("yeterlik olumsuzluğu", ["tu", "de"]), ("olumsuzluk", ["de"]),
    ("ettirgen", ["ta"]), ("edilgen", ["te"]), ("dönüşlü/edilgen", ["te"]), ("işteş", ["to"]), ("yeterlik", ["tu"]),
    ("tezlik", []),
    ("isimden fiil", ["ga"]), ("fiilden isim", ["ge"]), ("isim-fiil", ["ge"]), ("mastar", ["ge"]),
    ("fail", ["gi"]), ("meslek/fail", ["ha"]), ("sahiplik", ["go"]), ("soyut isim", ["gu"]), ("yoksunluk", ["pa"]),
    ("küçültme", ["pe"]), ("sıfat-fiil (geçmiş)", ["pi"]), ("sıfat-fiil (-mış)", ["pi"]), ("sıfat-fiil (şimdi)", ["po"]),
    ("sıfat-fiil (gelecek)", ["fe"]), ("sıra sayısı", ["fa"]), ("dil/tarz", ["fi"]), ("ilgi sıfatı", ["fo"]),
    ("üleştirme", ["fu"]), ("fiilden sıfat", ["go"]), ("fiilden isim (-gı)", ["ge"]), ("fiilden isim (-ıntı)", ["ge"]),
    ("benzerlik", ["wa"]),
    ("zarf-fiil (-madan", ["de", "pu"]), ("zarf-fiil (-maksızın", ["de", "pu"]), ("zarf-fiil (-ınca)", ["we"]),
    ("zarf-fiil (-alı)", ["we"]), ("zarf-fiil (-ken)", ["wu"]), ("zarf-fiil (-dıkça)", ["wu"]),
    ("zarf-fiil (-casına)", ["pu"]), ("zarf-fiil", ["pu"]),
]


def islev_gd(islev, ad=""):
    s = islev.replace("şimdiki zaman (-makta)", "şimdiki zaman")
    if s.startswith("fail") or ad == "-(y)IcI":
        return ["gi"]
    for on, ekler in ISLEV_ESLEME:
        if s.startswith(on) or (on in ("ettirgen", "edilgen", "işteş", "yeterlik") and s.startswith(on)):
            return ekler
    if "ettirgen" in s: return ["ta"]
    if "edilgen" in s: return ["te"]
    if "işteş" in s: return ["to"]
    if "sahiplik" in s: return ["go"]
    if "soyut" in s: return ["gu"]
    return None


KISI = {"mi", "ma", "ni", "na", "si", "sa"}


def turkceden(r, M):
    """Türkçe çözümleme sonucu (gunes_dil_v4.tokenize çıktısı) -> Güneş Dili kelimesi + açıklama."""
    tok = r.get("tokenlar") or []
    if not tok:
        return None
    kok_ek = tok[0][1]
    tr_kok, tur = kok_ek.sablon, kok_ek.giris
    if tur == "X":
        tur = "N"
    zincir = []
    # kökü türetme ağacıyla aç (yapım ekleri eşlenebiliyor ve tür tutarlıysa)
    t = r.get("turetme")
    if t and t[-1][1].cikis == tur:
        ek_seq, ok = [], True
        for b, e in t[1:]:
            g = islev_gd(e.islev, e.ad)
            if g is None:
                ok = False; break
            ek_seq += g
        if ok and ((t[0][1].sablon, t[0][1].giris) in TR2GD):
            tr_kok = t[0][1].sablon
            zincir += ek_seq
    gd_kok = TR2GD.get((tr_kok, tur)) or TR2GD.get((tr_kok, "N" if tur == "V" else "V")) or uyarla(tr_kok)
    if gd_kok is None:
        return None
    atlanan = []
    # ekleri tür bilgisiyle ekle; Türkçe sıra farklarını Güneş Dili şablonuna uydur
    govde, kisi, soru = [], [], []
    cur = tur
    for b, e in tok[1:]:
        g = islev_gd(e.islev, e.ad)
        if g is None:
            atlanan.append(e.islev); continue
        # fiilde zaman ekinden önce gelen -dı/-mış ek-fiili Güneş Dili'nde zaman ekidir (edil-miş-tir)
        if cur == "V" and g in (["ya"], ["ye"]) and not any(x[0] in "kb" for x in govde):
            g = ["ka"] if g == ["ya"] else ["ku"]
        if e.islev.startswith("şahıs") and not e.islev.startswith("şahıs 3.çoğul (ek-fiil"):
            kisi += g; continue
        if e.islev.startswith("şahıs 3.çoğul"):
            kisi += g; continue
        govde += g
        cur = e.cikis
    # isim yüklemde kişi eki: Güneş Dili'nde ek-fiil (yi) zorunlu (öğretmen-yi-ma: öğretmeniz)
    if kisi and not any(x in ("ya", "ye", "yi", "ba") for x in govde) and cur == "N":
        govde.append("yi")
    zincir += govde + kisi + soru
    w = uret(gd_kok, zincir)
    return {"kelime": w, "kok": gd_kok, "ekler": zincir, "atlanan": atlanan, "tr_kok": tr_kok}


# ---------------------------------------------------------------------------
# Mandelbrot haritası (MFNS: Dağlı, Dağlı & Dağlı 2026) — aile = açı, yuva = yarıçap
# ---------------------------------------------------------------------------
MERKEZ = complex(-0.7453, 0.1127)
OLCEK, ZOOM = 0.05, 40.0
AILE_SIRA = list(AILELER.keys())
YUVA_UZAKLIK = {"yapım": 1, "çatı": 2, "olumsuz": 3, "zaman": 4, "kip": 5, "çokluk": 3, "iyelik": 4, "hal": 5,
                "aitlik": 6, "ek-fiil": 7, "kişi": 8, "soru": 9}


def ek_koordinat(bicim, yuva=None):
    c = bicim[0]
    ai = AILE_SIRA.index(c)
    uyeler = list(AILELER[c][2].keys())
    aci = (ai + (uyeler.index(bicim) + 0.5) / (len(uyeler) + 1)) / len(AILE_SIRA) * 2 * math.pi
    if yuva is None:
        yuva = {"h": "aitlik", "m": "kişi", "n": "kişi", "s": "kişi", "l": "çokluk", "t": "çatı", "d": "olumsuz", "k": "zaman",
                "b": "kip", "r": "hal", "w": "hal", "g": "yapım", "p": "yapım", "f": "yapım", "y": "ek-fiil"}[c]
    r = (0.08 + 0.1 * YUVA_UZAKLIK[yuva]) * OLCEK
    z = MERKEZ + r * complex(math.cos(aci), math.sin(aci))
    return z.real, z.imag, ZOOM


def kok_koordinat(kok):
    h = 0x811C9DC5
    for b in kok.encode():
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    aci = (h % 10000) / 10000 * 2 * math.pi
    r = (0.02 + 0.05 * ((h // 10000) % 1000) / 1000) * OLCEK
    z = MERKEZ + r * complex(math.cos(aci), math.sin(aci))
    return z.real, z.imag, ZOOM


# ---------------------------------------------------------------------------
# Kanıtlar
# ---------------------------------------------------------------------------
def teorem_kaniti():
    return """TEOREM. Geçerli her Güneş Dili kelimesi w = K·E1·E2·…·En (K kök, Ei ek) için bu bölünme tektir.
KANIT. (1) İ2'ye göre K = (k)ü(kü)*k biçimindedir: içinde iki ünsüz yan yana gelmez ve K ünsüzle biter.
(2) İ3'e göre her Ei = kü'dür: içinde ünsüz kümesi yoktur, ünsüzle başlar, ünlüyle biter; dolayısıyla
    Ei·Ei+1 birleşiminde de küme oluşmaz (ünlü + ünsüz).
(3) n = 0 ise w ünsüzle biter ve hiç ünsüz kümesi içermez. n ≥ 1 ise w ünlüyle biter ve K'nın son
    ünsüzü ile E1'in ilk ünsüzü yan yana gelir: w'de TAM OLARAK BİR ünsüz kümesi vardır.
(4) Dolayısıyla kök, bu tek kümenin ilk ünsüzünde biter (küme yoksa w'nin tamamıdır). Kalan kısım sabit
    uzunluklu (2 harf) parçalara tek biçimde bölünür.
(5) İşlev ataması: her ek biçimi tektir (İ3) ve İ5 durum makinesi her (durum, ek) çifti için en fazla bir
    geçişe sahiptir (deterministik); bu `fsa_determinizm()` ile tüm durum-ek çiftleri taranarak doğrulanır.
Bu nedenle bölünme de işlev dizisi de tektir. ∎"""


def fsa_determinizm():
    """Tüm (tür, yuva, geçmiş) durumları ve tüm ekler için birden fazla kural uygulanıp uygulanamadığını tarar.
    Yapım kuralı ile yuva kuralı aynı eke uygulanamaz (yapım biçimleri hiçbir yuva kümesinde yok);
    aynı biçimin iki yuvası (mi: iyelik / kişi) birbirini dışlayan koşullara bağlıdır."""
    ihlal, durum = [], 0
    for tur in ("N", "V"):
        yuvalar = FIIL_YUVA if tur == "V" else ISIM_YUVA
        adlar = [a for a, _ in yuvalar]
        for yuva in range(-1, len(yuvalar)):
            for r in range(0, len(adlar) + 1):
                for gecmis in itertools.combinations(adlar, r):
                    g = set(gecmis)
                    durum += 1
                    for e in EK:
                        # yapım ve yuva kurallarını ayrı ayrı say
                        yap = e in YAPIM_TUR and YAPIM_TUR[e][0] == tur and (
                            yuva == -1 or (tur == "V" and yuva <= 1) or (tur == "V" and e in Z_YAPIM and yuva <= 2))
                        yuv = 0
                        for i, (ad, kume) in enumerate(yuvalar):
                            if (i < yuva or (i == yuva and ad not in TEKRARLI)) or e not in kume: continue
                            if ad == "kişi" and ((tur == "N" and "ek-fiil" not in g) or
                                                 (tur == "V" and not ({"zaman", "kip", "ek-fiil"} & g))): continue
                            if ad == "iyelik" and "ek-fiil" in g: continue
                            yuv += 1
                        # mi/ni/si: isimde iyelik (ek-fiil yokken) ve kişi (ek-fiil varken) aynı anda uygulanamaz
                        if yap + min(yuv, 1) > 1 or (yuv > 1 and not (e in {"mi", "ma", "ni", "na", "si", "sa"} and tur == "N")):
                            ihlal.append((tur, yuva, gecmis, e))
                        if e in {"mi", "ma", "ni", "na", "si", "sa"} and tur == "N" and yuv > 1:
                            ihlal.append((tur, yuva, gecmis, e))
    return ihlal, durum


def kaba_kuvvet_dogrulama(kokler, max_ek=3):
    """Verilen köklerle en fazla max_ek ekli TÜM dizileri üretip, geçerli olanların tek bölünmesini
    ve üretilen işlevlerin geri okunduğunu doğrular."""
    ekler = list(EK)
    toplam = gecerli = hata = 0
    for k in kokler:
        tur = SOZLUK.get(k, (None, "N"))[1][0]
        for n in range(0, max_ek + 1):
            for seq in itertools.product(ekler, repeat=n):
                toplam += 1
                f = fsa(list(seq), tur)
                if f is None:
                    continue
                gecerli += 1
                w = uret(k, list(seq))
                r = cozumle(w)
                if "hata" in r or r["kok"] != k or [x[0] for x in r["ekler"]] != list(seq) or \
                        [x[1] for x in r["ekler"]] != [x[1] for x in f]:
                    hata += 1
    return toplam, gecerli, hata


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(teorem_kaniti())
    ih, d = fsa_determinizm()
    print("FSA determinizm:", d, "durum tarandı, ihlal:", len(ih), ih[:5])
