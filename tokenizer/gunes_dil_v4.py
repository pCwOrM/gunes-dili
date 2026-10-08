"""
Güneş-Dil 3.0 — Türkçe eklemeli çözümleyici + veriyle öğrenen seçim + Mandelbrot fraktal gömme
=============================================================================================

v3'e göre değişenler (hepsi UD Türkçe ağaç bankalarında ölçülen hatalardan çıkarıldı):
  1. Özel adlar: kesme işaretli (Türkiye'nin) ve büyük harfli sözlük dışı kelimeler "özel ad" kökü alır.
  2. Kök ses olayları: ünlü düşmesi (ömür->ömrü), ikizleşme (hak->hakkı), yumuşama (kitap->kitabı,
     renk->rengi), -yor öncesi daralma (söyle->söylüyor), de/ye -> di/yi, zamir gövdeleri (o->onu,
     bu->buna, ben->bana), û/â yazım çeşitleri (hükûmet ~ hükümet).
  3. İnce ünlülü alıntılar (saat->saati, rol->rolü): yalnızca kesin çözüm bulunamazsa, işaretli yedek.
  4. Ek envanteri 72 -> 110+: emir/istek, -maktadır, -dıkça, -arak/-ıp/-ınca/-madan/-ken/-alı/-maksızın,
     -gı, -gan, -ıcı, -ca, -cık, -daş, -ınca, 3.çoğul + ek-fiil (gelirlerdi) vb.
  5. Belirsizlik giderme: UD eğitim setinden sayılan kök ve ek-dizisi olasılıklarıyla puanlama
     (model dosyası: gunes_dil_model.json). Model yoksa kurallı öncelik kullanılır.
  6. Fraktal gömme koordinatları MFNS usulü evrimsel aramayla eğitilebilir (koordinat dosyası).

Kullanım:  python3 gunes_dil_v4.py            (örnekler + testler)
           from gunes_dil_v4 import tokenize
"""
import json
import math
import os
import re
from dataclasses import dataclass

import numpy as np

BURASI = os.path.dirname(os.path.abspath(__file__))
VOWELS = "aeıioöuü"
BACK, FRONT = set("aıou"), set("eiöü")
ROUND = set("ouöü")
VOICELESS = set("çfhkpsşt")
CONSONANTS = "bcçdfgğhjklmnprsştvyz"
HIGH = "ıiuü"

SES_SINIFI = {"M (dudak)": "bpmvf", "K (art damak)": "kgğhy", "N (diş-burun)": "n",
              "TD (diş-patlama)": "td", "S (ıslıklı)": "sşzcçj", "L (yan)": "l", "R (titrek)": "r"}
SES_SINIFI_OF = {c: k for k, v in SES_SINIFI.items() for c in v}


# ---------------------------------------------------------------------------
# Arşifonem gerçekleştirme (ünlü uyumu, ünsüz benzeşmesi, kaynaştırma)
# ---------------------------------------------------------------------------
def son_unlu(s):
    for ch in reversed(s):
        if ch in VOWELS:
            return ch
    return "e"


def gerceklestir(sablon, onceki, ince=False):
    """'(y)DAn' gibi bir şablonu önceki dizeye göre yüzey biçimine çevirir.
    ince=True: alıntı kökten sonra ilk ünlüyü ince yap (saat -> saati)."""
    out = onceki
    i = 0
    ilk = True
    while i < len(sablon):
        ch = sablon[i]
        if ch == "(":
            j = sablon.index(")", i)
            parca = sablon[i + 1:j]
            son = out[-1] if out else "a"
            if parca == "I":
                if son not in VOWELS:
                    out += gerceklestir("I", out, ince and ilk)
                    ilk = False
            elif son in VOWELS:
                out += parca
            i = j + 1
            continue
        v = son_unlu(out)
        geri = (v in BACK) and not (ince and ilk)
        if ch == "A":
            out += "a" if geri else "e"; ilk = False
        elif ch == "I":
            out += {(True, False): "ı", (True, True): "u", (False, False): "i",
                    (False, True): "ü"}[(geri, v in ROUND)]
            ilk = False
        elif ch == "D":
            out += "t" if out and out[-1] in VOICELESS else "d"
        elif ch == "C":
            out += "ç" if out and out[-1] in VOICELESS else "c"
        elif ch == "G":
            out += "k" if out and out[-1] in VOICELESS else "g"
        elif ch == "K":   # ünlüden önce yumuşayabilen k (ayrıca denetlenir)
            out += "k"
        else:
            out += ch
        i += 1
    return out[len(onceki):]


# ---------------------------------------------------------------------------
# Ek envanteri: (ad, şablon, giriş türü, çıkış türü, yuva, işlev)
# Türler: N isim, V fiil, Z zarf-fiil (sonuna yalnız ek-fiil/ -ki gelmez)
# Yuva: 0 yapım (tekrarlanabilir) | 1 olumsuzluk | 2 sıfat-fiil/isim-fiil (yuvayı sıfırlar)
#       3 zaman-kip | 10 çokluk | 11 iyelik | 12 hal | 13 -ki | 15 3.çoğul (ek-fiilden önce)
#       20 ek-fiil | 21 -ken | 30 şahıs | 31 3.çoğul şahıs
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Ek:
    ad: str
    sablon: str
    giris: str
    cikis: str
    yuva: int
    islev: str


def _E(*a):
    return Ek(*a)


EKLER = [
    # --- yapım: isimden isim
    _E("-lI", "lI", "N", "N", 0, "sahiplik/aitlik"),
    _E("-lIk", "lIk", "N", "N", 0, "soyut isim/araç"),
    _E("-CI", "CI", "N", "N", 0, "meslek/fail"),
    _E("-sIz", "sIz", "N", "N", 0, "yoksunluk"),
    _E("-sAl", "sAl", "N", "N", 0, "ilgi sıfatı (-sal)"),
    _E("-CA", "CA", "N", "N", 0, "dil/tarz/görelik (-ca)"),
    _E("-CIk", "CIk", "N", "N", 0, "küçültme (-cık)"),
    _E("-DAş", "DAş", "N", "N", 0, "ortaklık (-daş)"),
    _E("-(I)ncI", "(I)ncI", "N", "N", 0, "sıra sayısı"),
    _E("-(ş)Ar", "(ş)Ar", "N", "N", 0, "üleştirme (-er)"),
    _E("-msI", "msI", "N", "N", 0, "benzerlik (-msı)"),
    # --- yapım: isimden fiil
    _E("-lA", "lA", "N", "V", 0, "isimden fiil"),
    _E("-lAş", "lAş", "N", "V", 0, "isimden fiil (oluş)"),
    _E("-lAn", "lAn", "N", "V", 0, "isimden fiil (edinme)"),
    _E("-Al", "Al", "N", "V", 0, "isimden fiil (-al)"),
    # --- yapım: fiilden isim
    _E("-(I)m", "(I)m", "V", "N", 0, "fiilden isim"),
    _E("-GI", "GI", "V", "N", 0, "fiilden isim (-gı)"),
    _E("-GAn", "GAn", "V", "N", 0, "fiilden sıfat (-gan)"),
    _E("-(y)IcI", "(y)IcI", "V", "N", 0, "fail (-ıcı)"),
    _E("-(I)ntI", "(I)ntI", "V", "N", 0, "fiilden isim (-ıntı)"),
    _E("-GIn", "GIn", "V", "N", 0, "fiilden sıfat (-gın)"),
    _E("-(y)Iş", "(y)Iş", "V", "N", 0, "isim-fiil (-ış)"),
    # --- yapım: fiilden fiil (çatı)
    _E("-DIr", "DIr", "V", "V", 0, "ettirgen çatı"),
    _E("-t", "t", "V", "V", 0, "ettirgen çatı"),
    _E("-Ir", "Ir", "V", "V", 0, "ettirgen çatı (-ir)"),
    _E("-Ar", "Ar", "V", "V", 0, "ettirgen çatı (-ar)"),
    _E("-Il", "(I)l", "V", "V", 0, "edilgen çatı"),
    _E("-In", "(I)n", "V", "V", 0, "dönüşlü/edilgen çatı"),
    _E("-Iş", "(I)ş", "V", "V", 0, "işteş çatı"),
    _E("-(y)Abil", "(y)Abil", "V", "V", 0, "yeterlik"),
    _E("-(y)Iver", "(y)Iver", "V", "V", 0, "tezlik"),
    # --- fiil çekimi
    _E("-(y)AmA", "(y)AmA", "V", "V", 1, "yeterlik olumsuzluğu"),
    _E("-mA", "mA", "V", "V", 1, "olumsuzluk"),
    _E("-DIk", "DIK", "V", "N", 2, "sıfat-fiil (geçmiş)"),
    _E("-(y)An", "(y)An", "V", "N", 2, "sıfat-fiil (şimdi)"),
    _E("-(y)AcAk", "(y)AcAK", "V", "N", 2, "sıfat-fiil (gelecek)"),
    _E("-mAk", "mAK", "V", "N", 2, "mastar"),
    _E("-mA", "mA", "V", "N", 2, "isim-fiil (-ma)"),
    _E("-mIş", "mIş", "V", "N", 2, "sıfat-fiil (-mış)"),
    _E("-DI", "DI", "V", "V", 3, "görülen geçmiş"),
    _E("-mIş", "mIş", "V", "V", 3, "öğrenilen geçmiş"),
    _E("-(I)yor", "(I)yor", "V", "V", 3, "şimdiki zaman"),
    _E("-mAktA", "mAktA", "V", "V", 3, "şimdiki zaman (-makta)"),
    _E("-Ar", "Ar", "V", "V", 3, "geniş zaman"),
    _E("-Ir", "(I)r", "V", "V", 3, "geniş zaman"),
    _E("-mAz", "mAz", "V", "V", 3, "geniş zaman olumsuz"),
    _E("-(y)AmAz", "(y)AmAz", "V", "V", 3, "geniş zaman olumsuz (yeterlik)"),
    _E("-(y)Abil", "(y)Abil", "V", "V", 1.5, "yeterlik (olumsuzdan sonra)"),
    _E("-(y)AcAk", "(y)AcAK", "V", "V", 3, "gelecek zaman"),
    _E("-sA", "sA", "V", "V", 3, "şart"),
    _E("-mAlI", "mAlI", "V", "V", 3, "gereklilik"),
    _E("-(y)A", "(y)A", "V", "V", 3, "istek"),
    _E("-(y)AlIm", "(y)AlIm", "V", "V", 3, "istek 1.çoğul"),
    _E("-(y)AyIm", "(y)AyIm", "V", "V", 3, "istek 1.tekil"),
    _E("-(y)In", "(y)In", "V", "V", 3, "emir 2.çoğul"),
    _E("-(y)InIz", "(y)InIz", "V", "V", 3, "emir 2.çoğul (-ınız)"),
    _E("-sIn", "sIn", "V", "V", 3, "emir 3.tekil"),
    _E("-sInlAr", "sInlAr", "V", "V", 3, "emir 3.çoğul"),
    # zarf-fiiller
    _E("-(y)ArAk", "(y)ArAk", "V", "Z", 3, "zarf-fiil (-arak)"),
    _E("-(y)Ip", "(y)Ip", "V", "Z", 3, "zarf-fiil (-ıp)"),
    _E("-(y)IncA", "(y)IncA", "V", "Z", 3, "zarf-fiil (-ınca)"),
    _E("-mAdAn", "mAdAn", "V", "Z", 3, "zarf-fiil (-madan, olumsuz)"),
    _E("-mAksIzIn", "mAksIzIn", "V", "Z", 3, "zarf-fiil (-maksızın, olumsuz)"),
    _E("-DIkçA", "DIkçA", "V", "Z", 3, "zarf-fiil (-dıkça)"),
    _E("-(y)AlI", "(y)AlI", "V", "Z", 3, "zarf-fiil (-alı)"),
    _E("-(y)A", "(y)A", "V", "Z", 3, "zarf-fiil (-a)"),
    _E("-CAsInA", "CAsInA", "V", "Z", 3, "zarf-fiil (-casına)"),
    _E("-(y)ken", "(y)ken", "V", "Z", 21, "zarf-fiil (-ken)"),
    _E("-(y)ken", "(y)ken", "N", "Z", 21, "zarf-fiil (-ken)"),
    # --- isim çekimi
    _E("-lAr", "lAr", "N", "N", 10, "çokluk"),
    _E("-(I)m", "(I)m", "N", "N", 11, "iyelik 1.tekil"),
    _E("-(I)n", "(I)n", "N", "N", 11, "iyelik 2.tekil"),
    _E("-(s)I", "(s)I", "N", "N", 11, "iyelik 3.tekil"),
    _E("-(I)mIz", "(I)mIz", "N", "N", 11, "iyelik 1.çoğul"),
    _E("-(I)nIz", "(I)nIz", "N", "N", 11, "iyelik 2.çoğul"),
    _E("-lArI", "lArI", "N", "N", 11, "iyelik 3.çoğul"),
    _E("-(y)I", "(y)I", "N", "N", 12, "belirtme hali"),
    _E("-(n)In", "(n)In", "N", "N", 12, "ilgi hali"),
    _E("-(y)A", "(y)A", "N", "N", 12, "yönelme hali"),
    _E("-DA", "DA", "N", "N", 12, "bulunma hali"),
    _E("-DAn", "DAn", "N", "N", 12, "ayrılma hali"),
    _E("-(y)lA", "(y)lA", "N", "N", 12, "vasıta hali"),
    _E("-CA", "CA", "N", "N", 12, "eşitlik hali (-ca)"),
    _E("-nI", "nI", "N", "N", 12, "belirtme hali (zamir n)"),
    _E("-nA", "nA", "N", "N", 12, "yönelme hali (zamir n)"),
    _E("-nDA", "nDA", "N", "N", 12, "bulunma hali (zamir n)"),
    _E("-nDAn", "nDAn", "N", "N", 12, "ayrılma hali (zamir n)"),
    _E("-ki", "ki", "N", "N", 13, "aitlik (-ki)"),
    _E("-kü", "kü", "N", "N", 13, "aitlik (-ki, gün/dün)"),
    # --- ek-fiil ve şahıs (isim ve fiil)
    _E("-lAr", "lAr", "V", "V", 15, "şahıs 3.çoğul (ek-fiilden önce)"),
    _E("-(y)DI", "(y)DI", "N", "N", 20, "ek-fiil hikâye"),
    _E("-(y)mIş", "(y)mIş", "N", "N", 20, "ek-fiil rivayet"),
    _E("-(y)sA", "(y)sA", "N", "N", 20, "ek-fiil şart"),
    _E("-DIr", "DIr", "N", "N", 22, "ek-fiil bildirme"),
    _E("-(y)DI", "(y)DI", "V", "V", 20, "ek-fiil hikâye"),
    _E("-(y)mIş", "(y)mIş", "V", "V", 20, "ek-fiil rivayet"),
    _E("-(y)sA", "(y)sA", "V", "V", 20, "ek-fiil şart"),
    _E("-DIr", "DIr", "V", "V", 22, "ek-fiil bildirme"),
    _E("-(y)Im", "(y)Im", "N", "N", 30, "şahıs 1.tekil"),
    _E("-sIn", "sIn", "N", "N", 30, "şahıs 2.tekil"),
    _E("-(y)Iz", "(y)Iz", "N", "N", 30, "şahıs 1.çoğul"),
    _E("-sInIz", "sInIz", "N", "N", 30, "şahıs 2.çoğul"),
    _E("-m", "m", "N", "N", 30, "şahıs 1.tekil (-dı/-sa sonrası)"),
    _E("-n", "n", "N", "N", 30, "şahıs 2.tekil (-dı/-sa sonrası)"),
    _E("-k", "k", "N", "N", 30, "şahıs 1.çoğul (-dı/-sa sonrası)"),
    _E("-nIz", "nIz", "N", "N", 30, "şahıs 2.çoğul (-dı/-sa sonrası)"),
    _E("-lAr", "lAr", "N", "N", 31, "şahıs 3.çoğul"),
    _E("-(y)Im", "(y)Im", "V", "V", 30, "şahıs 1.tekil"),
    _E("-sIn", "sIn", "V", "V", 30, "şahıs 2.tekil"),
    _E("-(y)Iz", "(y)Iz", "V", "V", 30, "şahıs 1.çoğul"),
    _E("-sInIz", "sInIz", "V", "V", 30, "şahıs 2.çoğul"),
    _E("-m", "m", "V", "V", 30, "şahıs 1.tekil (-dı/-sa sonrası)"),
    _E("-n", "n", "V", "V", 30, "şahıs 2.tekil (-dı/-sa sonrası)"),
    _E("-k", "k", "V", "V", 30, "şahıs 1.çoğul (-dı/-sa sonrası)"),
    _E("-nIz", "nIz", "V", "V", 30, "şahıs 2.çoğul (-dı/-sa sonrası)"),
    _E("-lAr", "lAr", "V", "V", 31, "şahıs 3.çoğul"),
    _E("-DIr", "DIr", "V", "V", 32, "ek-fiil bildirme (şahıstan sonra)"),
    _E("-DIr", "DIr", "N", "N", 32, "ek-fiil bildirme (şahıstan sonra)"),
]
# -dı/-sa sonrası kısa şahıs ekleri yalnızca bu eklerden sonra gelir
KISA_SAHIS_ONCESI = {"görülen geçmiş", "şart", "ek-fiil hikâye", "ek-fiil şart"}
# Bu ekler sözcüğü kapatır ya da yalnız belli eklerle devam eder
ZARF = "Z"

# ---------------------------------------------------------------------------
# Kök sözlüğü (TDK) + zamirler + görevli kelimeler
# ---------------------------------------------------------------------------
KOKLER = {}
FIIL_DE = set()
_yol = os.path.join(BURASI, "tdk_kokler.json")
if os.path.exists(_yol):
    _v = json.load(open(_yol, encoding="utf-8"))
    for _k in _v["N"]:
        KOKLER.setdefault(_k, "N")
    for _k in _v["V"]:
        if _k in KOKLER and KOKLER[_k] == "N":
            FIIL_DE.add(_k)
        else:
            KOKLER[_k] = "V"
for _k, _t in {"üzer": "N", "birbiri": "N", "ara": "N", "ev": "N", "göz": "N", "gel": "V", "git": "V", "oku": "V", "de": "V", "ye": "V",
               "et": "V", "ol": "V", "ben": "N", "sen": "N", "o": "N", "biz": "N", "siz": "N",
               "bu": "N", "şu": "N", "kendi": "N", "ne": "N", "kim": "N", "hep": "N"}.items():
    KOKLER.setdefault(_k, _t)
# û ve â içeren madde başlarının düz yazımları (hükûmet -> hükumet, hükümet)
for _k in list(KOKLER):
    if "û" in _k or "â" in _k or "î" in _k:
        for _alt in {_k.replace("û", "u").replace("â", "a").replace("î", "i"),
                     _k.replace("û", "ü").replace("â", "a").replace("î", "i")}:
            KOKLER.setdefault(_alt, KOKLER[_k])

ETTIRGEN_SOZLUKSEL = {"ettirgen çatı (-ar)", "ettirgen çatı (-ir)"}
ISIM_SOZLUKSEL = {"fiilden isim", "fiilden isim (-gı)", "fiilden isim (-ıntı)"}


def fiil_mi(s):
    return KOKLER.get(s) == "V" or s in FIIL_DE


GOREVLI = {"ve": ("bağlaç", "ve"), "ile": ("bağlaç", "ile"), "da": ("bağlaç", "da"), "de": ("bağlaç", "da"),
           "ki": ("bağlaç", "ki"), "ya": ("bağlaç", "ya"), "ama": ("bağlaç", "ama"), "fakat": ("bağlaç", "fakat"),
           "çünkü": ("bağlaç", "çünkü"), "veya": ("bağlaç", "veya"), "ile": ("bağlaç", "ile"),
           "mi": ("soru", "mi"), "mı": ("soru", "mi"), "mu": ("soru", "mi"), "mü": ("soru", "mi"),
           "en": ("zarf", "en"), "çok": ("zarf", "çok"), "daha": ("zarf", "daha"), "gibi": ("edat", "gibi"),
           "için": ("edat", "için"), "kadar": ("edat", "kadar"), "değil": ("ek-fiil", "değil"),
           "ise": ("ek-fiil", "i"), "iken": ("ek-fiil", "i"), "idi": ("ek-fiil", "i"), "imiş": ("ek-fiil", "i"),
           "şey": ("isim", "şey"), "gibi": ("edat", "gibi")}
# Soru eki çekimli biçimleri (mıdır, misin, miyiz ...)
ZAMIR_GOVDE = {"on": "o", "bun": "bu", "şun": "şu", "ban": "ben", "san": "sen", "kend": "kendi",
               "suy": "su", "ney": "ne", "birbir": "birbiri", "hep": "hep"}
YUMUSAMA = {"p": "b", "ç": "c", "t": "d", "k": "ğ"}
SERTLESME = {"b": "p", "c": "ç", "d": "t", "ğ": "k"}


def _norm(s):
    return (s.replace("â", "a").replace("î", "i").replace("û", "u"))


def _birlesik_iyelik(kok):
    """buzdolabı, cumhurbaşkanı, yeryüzü: X + Y + (s)I biçimli birleşik ad mı?"""
    if len(kok) < 6 or kok[-1] not in HIGH:
        return False
    govde = kok[:-2] if kok[-2] == "s" else kok[:-1]
    adaylar = [govde] + ([govde[:-1] + SERTLESME[govde[-1]]] if govde and govde[-1] in SERTLESME else [])
    for g in adaylar:
        for i in range(2, len(g) - 1):
            if g[:i] in KOKLER and g[i:] in KOKLER and len(g[i:]) >= 2:
                return True
    return False


def kok_adaylari(kelime):
    """Kelimenin önekleri için (kök, yüzey, tür, ses_olayı) adayları üretir."""
    n = len(kelime)
    for i in range(1, n + 1):
        on = kelime[:i]
        sonra = kelime[i:i + 3]
        unlu_sonra = i < n and kelime[i] in VOWELS
        aday = [(on, "")]
        if unlu_sonra:
            if on[-1] in SERTLESME:
                aday.append((on[:-1] + SERTLESME[on[-1]], "yumuşama"))
            if on.endswith("ng"):
                aday.append((on[:-1] + "k", "yumuşama"))
            if len(on) >= 3 and on[-1] == on[-2] and on[-1] in CONSONANTS:
                aday.append((on[:-1], "ikizleşme"))
            if len(on) >= 3 and on[-1] in CONSONANTS and on[-2] in CONSONANTS:
                for v in HIGH:                                   # ömr -> ömür, kayb -> kayıp
                    kok = on[:-1] + v + on[-1]
                    aday.append((kok, "ünlü düşmesi"))
                    if on[-1] in SERTLESME:
                        aday.append((on[:-1] + v + SERTLESME[on[-1]], "ünlü düşmesi+yumuşama"))
        if sonra.startswith("yor") and on[-1] in HIGH:           # söylü -> söyle
            for v in "ae":
                aday.append((on[:-1] + v, "daralma"))
        if on in ("di", "yi") and i < n and kelime[i] == "y":    # diyor, yiyecek
            aday.append((on[0] + "e", "daralma"))
        if on in ZAMIR_GOVDE:
            aday.append((ZAMIR_GOVDE[on], "zamir gövdesi"))
        for kok, olay in aday:
            if kok in KOKLER:
                turler = {KOKLER[kok]} | ({"V"} if kok in FIIL_DE else set())
                for tur in sorted(turler):
                    yield kok, on, tur, olay
                if KOKLER[kok] == "N" and _birlesik_iyelik(kok):
                    yield kok, on, "N", (olay + "+" if olay else "") + "birleşik iyelik 3"


def ayristir(kelime, ince=False, kok_sabit=None, sadece_yapim=False):
    """Tüm geçerli ayrıştırmalar. kok_sabit=(kök, yüzey, tür): özel ad gibi dışarıdan kök."""
    sonuclar = []

    def ilerle(poz, yuzey, tur, yuva, yol, ilk_ek):
        if len(sonuclar) > 300:
            return
        if poz == len(kelime):
            sonuclar.append(list(yol))
            return
        son = yol[-1][1]
        for ek in EKLER:
            if ek.giris != tur:
                continue
            if sadece_yapim and ek.yuva != 0:
                continue
            if ek.yuva == 0 and yuva != 0:
                continue
            if ek.yuva != 0 and ek.yuva <= yuva and not (yuva == 13 and 10 <= ek.yuva < 20):
                continue
            son3 = son.islev.startswith("iyelik 3") or (son.yuva == -1 and "birleşik iyelik 3" in son.islev)
            if ek.yuva == 12 and ("zamir n" in ek.islev) != son3 \
                    and not ek.islev.startswith(("vasıta", "ilgi", "eşitlik")):
                continue
            if ek.yuva == 30 and ("sonrası" in ek.islev) != (son.islev in KISA_SAHIS_ONCESI):
                continue
            if ek.yuva == 15 and son.yuva != 3:
                continue
            if ek.islev.startswith("şahıs") and tur == "V" and son.yuva in (0, 1, -1) and ek.yuva == 30:
                continue                                         # şahıs eki zaman ekinden sonra gelir
            bicim = gerceklestir(ek.sablon, yuzey, ince and ilk_ek)
            bicim = bicim.replace("K", "k")
            adaylar = [bicim]
            if bicim and bicim[-1] == "k" and ek.sablon.endswith("K"):
                adaylar.append(bicim[:-1] + "ğ")                  # -dık+ı -> -dığı
            if ek.yuva == 1 and kelime.startswith("yor", poz + len(bicim)):
                adaylar.append(bicim[:-1] + gerceklestir("I", yuzey + bicim[:-1]))   # gel-mi-yor
            if ek.ad == "-(y)AcAk" and kelime.startswith("ğ", poz + len(bicim) - 1):
                pass
            for b in adaylar:
                if not b or not kelime.startswith(b, poz):
                    continue
                if ek.islev in ETTIRGEN_SOZLUKSEL and not fiil_mi(yuzey + b):
                    continue                                     # -Ar/-Ir ettirgeni sözlükseldir (çık-ar, bit-ir)
                if ek.islev in ISIM_SOZLUKSEL and KOKLER.get(yuzey + b) != "N":
                    continue                                     # -Im/-GI/-IntI verimsizdir (seç-im, bil-gi)
                if b.endswith("ğ") and b != bicim:
                    if not (poz + len(b) < len(kelime) and kelime[poz + len(b)] in VOWELS):
                        continue
                ny = 0 if ek.yuva in (0, 2) else (9 if ek.yuva == 13 else ek.yuva)
                ilerle(poz + len(b), yuzey + b, ek.cikis, ny, yol + [(b, ek)], False)

    if kok_sabit:
        kok, yz, tur, olay = kok_sabit[:4]
        telaffuz = kok_sabit[4] if len(kok_sabit) > 4 else yz
        # kelime içinde kök yüzeyi yz; uyum telaffuza göre (ABD -> "abede")
        kaydir = len(telaffuz) - len(yz)
        kelime = telaffuz + kelime[len(yz):]
        ilerle(len(telaffuz), telaffuz, tur, 0,
               [(yz, Ek("kök", kok, tur, tur, -1, f"kök ({kok})" + (f" · {olay}" if olay else "")))], True)
        return sonuclar
    for kok, yz, tur, olay in kok_adaylari(kelime):
        ilerle(len(yz), yz, tur, 0,
               [(yz, Ek("kök", kok, tur, tur, -1, f"kök ({kok})" + (f" · {olay}" if olay else "")))], True)
    return sonuclar


def uyum_gecerli(kelime):
    if any(c not in VOWELS and c not in CONSONANTS for c in kelime):
        return False
    v = [c for c in kelime if c in VOWELS]
    if not v:
        return False
    if len(kelime) > 1 and kelime[0] in CONSONANTS and kelime[1] in CONSONANTS:
        return False
    return all(c in BACK for c in v) or all(c in FRONT for c in v)


# ---------------------------------------------------------------------------
# Veriyle öğrenen seçim (UD eğitim setinden sayılan olasılıklar)
# ---------------------------------------------------------------------------
MODEL = None
_mp = os.path.join(BURASI, "gunes_dil_model.json")
if os.path.exists(_mp):
    MODEL = json.load(open(_mp, encoding="utf-8"))


def etiketler(p):
    """Ayrıştırmanın ek-dizisi etiketleri (kök türü ile başlar)."""
    return [p[0][1].giris] + [e.ad + "|" + e.islev for _, e in p[1:]]


def puan(p):
    kok = p[0][1].sablon
    olay = p[0][1].islev.count("·")
    if MODEL:
        rc, rn, rv = MODEL["kok"].get(kok, 0), MODEL["kok_toplam"], MODEL["kok_tur"]
        # kök olasılığı: görülmemiş kökler için uzunluğa bağlı geri çekilme
        p_kok = math.log((rc + 0.1) / (rn + 0.1 * rv))
        if rc == 0:
            p_kok += MODEL["gorulmemis"] + 0.35 * min(len(kok), 8)
        if kok in FIIL_DE:                                   # hem isim hem fiil olan kök: tür olasılığı
            ct = MODEL.get("kok_tip", {}).get(kok + "|" + p[0][1].giris, 0)
            p_kok += math.log((ct + 0.5) / (rc + 1.0))
        et = etiketler(p) + ["</s>"]
        s = 0.0
        for a, b in zip(et, et[1:]):
            c_ab = MODEL["ikili"].get(a + "→" + b, 0)
            c_a = MODEL["tekli"].get(a, 0)
            p_b = (MODEL["tekli"].get(b, 0) + 0.5) / (MODEL["tekli_toplam"] + 0.5 * len(MODEL["tekli"]))
            s += math.log((c_ab + 2.0 * p_b) / (c_a + 2.0))
        return p_kok + s - 1.5 * olay
    # model yoksa kurallı öncelik: az çekim, uzun kök
    cekim = sum(1 for _, e in p[1:] if e.yuva != 0)
    return -cekim * 3 + len(kok) * 0.3 - olay * 2


def turetme_agaci(kok):
    """Sözlük kökünü yalnızca yapım ekleriyle en kısa köküne kadar açar (gözlemci -> göz+le+m+ci)."""
    en_iyi = None
    for alt, yz, tur, olay in kok_adaylari(kok):
        if len(alt) >= len(kok) or len(alt) < 2 or olay:
            continue
        for p in ayristir(kok, kok_sabit=(alt, yz, tur, ""), sadece_yapim=True):
            if en_iyi is None or len(p[0][0]) < len(en_iyi[0][0]):
                en_iyi = p
    return en_iyi


def inan_1936(kok):
    return kok + "ğ" if kok and kok[-1] in VOWELS else None


def kucult(kelime):
    return (kelime.replace("I", "ı").replace("İ", "i").lower().replace("̇", "")
            .replace("â", "a").replace("î", "i").replace("û", "u").replace("’", "'"))


def _isaretle(p, ek_not):
    k = p[0][1]
    p[0] = (p[0][0], Ek("kök", k.sablon, k.giris, k.cikis, -1, k.islev + " · " + ek_not))
    return p


def adaylar(ham, ozel_ad_adayi=False):
    """Bir kelime için tüm çözümleme adaylarını üretir (puanlanmamış)."""
    w = kucult(ham)
    parses, koken = [], None
    if "'" in w:                                             # Türkiye'nin, ABD'den, Ödülü'nü
        kok, _, ek = w.partition("'")
        tam = kok + ek
        # (a) kesme öncesi özel ad kökü; uyum telaffuza göre (kısaltmalar ünlüyle biter gibi)
        telaffuzlar = [kok] if any(c in VOWELS for c in kok[-2:]) or len(kok) > 4 else [kok, kok + "e", kok + "a"]
        for tl in telaffuzlar:
            for ince in (False, True):
                parses += [_isaretle(p, "özel ad") for p in ayristir(tam, ince=ince, kok_sabit=(kok, kok, "N", "", tl))]
        # (b) sözlükle çözümleme, kesme sınırı bir ek sınırına denk geliyorsa (Ödül-ü'-nü)
        for p in ayristir(tam):
            sinirlar, t = set(), 0
            for b_, _ in p:
                t += len(b_); sinirlar.add(t)
            if len(kok) in sinirlar:
                parses.append(p)
        koken = "özel ad (kesme işaretli)"
    else:
        parses = ayristir(w)
        # İnce ünlülü alıntı kökler (hal+e, saat+i, rol+ü): her zaman aday, cezalı
        parses += [_isaretle(p, "ince ünlü (alıntı)") for p in ayristir(w, ince=True)
                   if p[0][1].sablon[-1] in CONSONANTS and son_unlu(p[0][1].sablon) in BACK and len(p) > 1]
        if ham.isupper() and len(w) <= 6 and not parses:
            parses = [[(w, Ek("kök", w, "N", "N", -1, f"kök ({w}) · kısaltma"))]]
            koken = "kısaltma"
        elif (ozel_ad_adayi or not parses) and ham[:1].isupper() and uyum_gecerli_ozel(w):
            bos = not parses
            parses.append([(w, Ek("kök", w, "N", "N", -1, f"kök ({w}) · özel ad"))])
            for i in range(3, len(w)):                       # Yunusların, Yukagirler (kesmesiz)
                if w[:i] in KOKLER:
                    continue
                parses += [_isaretle(p, "özel ad") for p in ayristir(w, kok_sabit=(w[:i], w[:i], "N", ""))
                           if len(p) > 1]
            if bos:
                koken = "özel ad"
        if not parses and len(w) <= 3 and all(c in CONSONANTS for c in w):
            parses = [[(w, Ek("kök", w, "N", "N", -1, f"kök ({w}) · kısaltma"))]]
            koken = "kısaltma"
    # yinelenenleri at
    gor, tek = set(), []
    for p in parses:
        anahtar = tuple((b_, e.ad, e.islev, e.sablon) for b_, e in p)
        if anahtar not in gor:
            gor.add(anahtar); tek.append(p)
    return tek, koken


def _sonuc(w, parses, koken, k):
    en = parses[0]
    kok = en[0][1].sablon
    ozel = "özel ad" in en[0][1].islev or "kısaltma" in en[0][1].islev
    return {"durum": "KABUL", "tokenlar": en, "alternatif": len(parses), "alternatifler": parses[1:k],
            "turetme": None if ozel else turetme_agaci(kok),
            "koken": ("özel ad" if "özel ad" in en[0][1].islev else "kısaltma" if "kısaltma" in en[0][1].islev
                      else ("yerli yapı" if uyum_gecerli(kok) else "alıntı kök (ünlü uyumu dışı)")),
            "inan": None if ozel else inan_1936(kok)}


def _gorevli(w):
    if w in GOREVLI:
        tur, lem = GOREVLI[w]
        return [(w, Ek(tur, lem, "X", "X", -1, tur))]
    if re.fullmatch(r"m[ıiuü](y?d[ıiuü]r|s[ıiuü]n(ız|iz|uz|üz)?|y[ıiuü]m|y[ıiuü]z|yd[ıiuü].*|ym[ıi]ş.*)", w):
        return [(w[:2], Ek("soru", "mi", "X", "X", -1, "soru")),
                (w[2:], Ek("-ek-fiil", w[2:], "X", "X", 30, "soru eki çekimi"))]
    return None


def _red(w):
    if any(True for _ in kok_adaylari(w)):
        return {"durum": "RED: ek sırası/biçimi Türkçe şablona aykırı", "tokenlar": [], "alternatif": 0}
    if uyum_gecerli(w):
        return {"durum": "BİLİNMEYEN KÖK (uyumlu, sözlük dışı)", "tokenlar": [], "alternatif": 0}
    return {"durum": "RED: yerli kök ölçütü sağlanmıyor -> alıntı/yabancı", "tokenlar": [], "alternatif": 0}


def tokenize(kelime, k=3, ozel_ad_adayi=False):
    """Tek kelime çözümlemesi (bağlamsız). Döner: durum, tokenlar, alternatifler, turetme, koken, inan."""
    ham = kelime.strip()
    w = kucult(ham)
    if not w:
        return {"durum": "Boş giriş", "tokenlar": [], "alternatif": 0}
    g = _gorevli(w)
    if g:
        return {"durum": "KABUL", "tokenlar": g, "alternatif": 1, "alternatifler": [], "turetme": None,
                "koken": "görevli kelime", "inan": None}
    parses, koken = adaylar(ham, ozel_ad_adayi)
    if not parses:
        return _red(w)
    parses.sort(key=puan, reverse=True)
    return _sonuc(w, parses, koken, k)


# ---------------------------------------------------------------------------
# Cümle düzeyi: bağlamla yeniden sıralama (önceki kelime ilgi hali mi, sonraki çekimli fiil mi,
# büyük harfli cümle içi kelime mi). Ağırlıklar UD eğitim setinden (MODEL["baglam"]).
# ---------------------------------------------------------------------------
def ozet(p):
    """Bağlam modelinin gördüğü özet etiket."""
    hal, iye, cok, neg = "Nom", "-", 0, 0
    for _, e in p[1:]:
        for k_, v in (("belirtme", "Acc"), ("ilgi", "Gen"), ("yönelme", "Dat"), ("bulunma", "Loc"),
                      ("ayrılma", "Abl"), ("vasıta", "Ins"), ("eşitlik", "Equ")):
            if e.islev.startswith(k_): hal = v
        if e.islev.startswith("iyelik"): iye = e.islev.split()[1][0]
        if e.islev == "çokluk": cok = 1
        if "olumsuz" in e.islev: neg = 1
    son = p[-1][1]
    tur = son.cikis if son.yuva != -1 else son.giris
    ozel = int("özel ad" in p[0][1].islev)
    return f"{tur}|{hal}|{iye}|{cok}|{neg}|{ozel}"


def baglam(onceki_en, sonraki_en, buyuk_ic):
    pg = 0
    if onceki_en:
        oz = ozet(onceki_en).split("|")
        pg = 1 if oz[1] == "Gen" else (2 if (oz[0] == "N" and oz[1] == "Nom" and oz[2] == "-") else 0)
    sv = 0
    if sonraki_en:
        son = sonraki_en[-1][1]
        sv = int(son.cikis == "V" and son.yuva >= 3)
    return f"{pg}{sv}{int(buyuk_ic)}"


BAGLAM_AGIRLIK = 0.4


def baglam_puani(p, ctx):
    if not MODEL or "baglam" not in MODEL:
        return 0.0
    B = MODEL["baglam"]
    o = ozet(p)
    c_oc = B["oc"].get(o + "#" + ctx, 0.0)
    c_c = B["c"].get(ctx, 0.0)
    c_o = B["o"].get(o, 0.0)
    n = B["n"]
    K = 50.0
    return BAGLAM_AGIRLIK * (math.log((c_oc + 1.0) / (c_c + K)) - math.log((c_o + 1.0) / (n + K)))


def cozumle_cumle(kelimeler, k=3):
    """Kelime listesini bağlamla çözümler. Döner: her kelime için tokenize() biçiminde sonuç."""
    ham_liste = [w.strip() for w in kelimeler]
    adaylist, kokenler = [], []
    for i, ham in enumerate(ham_liste):
        w = kucult(ham)
        g = _gorevli(w) if w else None
        if g or not w:
            adaylist.append(("G", g)); kokenler.append(None); continue
        ps, kk = adaylar(ham, ozel_ad_adayi=(i > 0 and ham[:1].isupper()))
        ps.sort(key=puan, reverse=True)
        adaylist.append(("P", ps)); kokenler.append(kk)
    enler = [(a[1][0] if a[0] == "P" and a[1] else None) for a in adaylist]
    sonuc = []
    for i, (tip, ps) in enumerate(adaylist):
        w = kucult(ham_liste[i])
        if tip == "G":
            sonuc.append({"durum": "KABUL", "tokenlar": ps, "alternatif": 1, "alternatifler": [], "turetme": None,
                          "koken": "görevli kelime", "inan": None} if ps else {"durum": "Boş giriş", "tokenlar": []})
            continue
        if not ps:
            sonuc.append(_red(w)); continue
        ctx = baglam(enler[i - 1] if i > 0 else None, enler[i + 1] if i + 1 < len(enler) else None,
                     i > 0 and ham_liste[i][:1].isupper())
        ps = sorted(ps, key=lambda p: puan(p) + baglam_puani(p, ctx), reverse=True)
        sonuc.append(_sonuc(w, ps, kokenler[i], k))
    return sonuc


def uyum_gecerli_ozel(w):
    """Özel ad kabulü: yalnız harf, en az bir ünlü."""
    return all(c in VOWELS or c in CONSONANTS or c in "qwx" for c in w) and any(c in VOWELS for c in w)


# ---------------------------------------------------------------------------
# Mandelbrot fraktal gömme (MFNS: Dağlı, Dağlı & Dağlı 2026, zenodo.22802921)
# ---------------------------------------------------------------------------
MERKEZ = complex(-0.7453, 0.1127)
OLCEK, ZOOM = 0.05, 40.0
ISLEV_AILESI = ["kök", "yapım", "çatı", "olumsuzluk", "sıfat-fiil", "zaman", "zarf-fiil",
                "çokluk", "iyelik", "hal", "aitlik", "ek-fiil", "şahıs"]
KOORD = None
_kp = os.path.join(BURASI, "gunes_dil_koordinat.json")
if os.path.exists(_kp):
    KOORD = json.load(open(_kp, encoding="utf-8"))


def aile(ek):
    if ek.yuva == -1: return "kök"
    if "çatı" in ek.islev or ek.islev in ("yeterlik", "tezlik"): return "çatı"
    if ek.cikis == "Z": return "zarf-fiil"
    if ek.yuva == 0: return "yapım"
    if ek.yuva == 1.5: return "çatı"
    if ek.yuva == 1: return "olumsuzluk"
    if ek.yuva == 2: return "sıfat-fiil"
    if ek.yuva == 3: return "zaman"
    if ek.yuva == 10: return "çokluk"
    if ek.yuva == 11: return "iyelik"
    if ek.yuva == 12: return "hal"
    if ek.yuva == 13: return "aitlik"
    if ek.yuva in (20, 22, 32): return "ek-fiil"
    return "şahıs"


SIRA = {-1: 0, 0: 1, 1: 2, 1.5: 2, 2: 3, 3: 4, 21: 4, 10: 5, 11: 6, 12: 7, 13: 8, 15: 9, 20: 9, 22: 9, 30: 10, 31: 10, 32: 10}


def fnv1a(metin):
    h = 0x811C9DC5
    for b in metin.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


def ek_anahtar(ek):
    return ek.ad + "|" + ek.islev


def koordinat(ek, anlamli=True):
    """Anlamlı: açı = işlev ailesi, yarıçap = yuva sırası (eğitilmiş koordinat varsa o). Ablasyon: hash."""
    anahtar = ek_anahtar(ek)
    if anlamli and KOORD and anahtar in KOORD:
        return tuple(KOORD[anahtar])
    h = fnv1a(anahtar if ek.yuva != -1 else ek.ad + ek.islev)
    if anlamli:
        aci = ISLEV_AILESI.index(aile(ek)) / len(ISLEV_AILESI) * 2 * math.pi
        aci += (h % 100) / 100 * 0.25
        r = (0.05 + 0.095 * SIRA[ek.yuva]) * OLCEK
    else:
        aci = (h % 10_000) / 10_000 * 2 * math.pi
        r = ((h // 10_000) % 10_000) / 10_000 * OLCEK
    c = MERKEZ + r * complex(math.cos(aci), math.sin(aci))
    return c.real, c.imag, ZOOM


def mfns_agirlik(cx, cy, zoom, res=128, max_iter=70, izgara=4):
    s = 1.0 / zoom
    x = np.linspace(cx - s, cx + s, res)
    y = np.linspace(cy - s, cy + s, res)
    C = x[None, :] + 1j * y[:, None]
    Z = np.zeros_like(C)
    ic = np.ones(C.shape, dtype=bool)
    for _ in range(max_iter):
        Z[ic] = Z[ic] ** 2 + C[ic]
        ic &= np.abs(Z) <= 2.0
    t = res // izgara
    return 6.0 * (np.array([ic[a*t:(a+1)*t, b*t:(b+1)*t].mean()
                            for a in range(izgara) for b in range(izgara)]) - 0.5)


if __name__ == "__main__":
    for w in ["evlerimizden", "gözlemcilerimizden", "gerçekleştirilemedi", "Türkiye'nin", "ömrü",
              "hakkında", "söylüyorum", "diyorlardı", "saati", "okuyun", "bakalım", "yapmaktadırlar",
              "değiştikçe", "bana", "onun", "çekoslovakyalılaştıramadıklarımızdanmışsınız", "evimizlerden",
              "qwrtzp", "Mustafa", "gelmesin", "toplumun"]:
        r = tokenize(w)
        print(f"{w:46s}", " + ".join(b for b, _ in r["tokenlar"]) or r["durum"], "|",
              " · ".join(e.islev for _, e in r["tokenlar"][1:]))
