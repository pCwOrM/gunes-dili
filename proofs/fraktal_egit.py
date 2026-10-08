"""Güneş Dili eklerinin Mandelbrot koordinatlarını MFNS usulü evrimsel aramayla eğitir ve ölçer.

Hedef: her ekin 16 boyutlu fraktal ağırlık vektörü, en yakın komşusu kendi ailesinden olacak biçimde
ayrışsın (aile = işlev ailesi). Arama yalnızca koordinatları (cx, cy) değiştirir; ağırlık saklanmaz.
Dış test: kelime gömmesi (eklerin fraktal vektörlerinin toplamı) ile UD test setinde Türkçe hal/çokluk/
iyelik özelliklerini en yakın merkez yöntemiyle tahmin; tek-sıcak (one-hot) ve rastgele koordinatla karşılaştırma.
"""
import json, math, random, collections, re
import numpy as np
import gunes_dili as G

RES, ITER = 64, 70


def patch(cx, cy, zoom=G.ZOOM, res=RES):
    s = 1.0 / zoom
    x = np.linspace(cx - s, cx + s, res); y = np.linspace(cy - s, cy + s, res)
    C = x[None, :] + 1j * y[:, None]; Z = np.zeros_like(C); ic = np.ones(C.shape, bool)
    for _ in range(ITER):
        Z[ic] = Z[ic] ** 2 + C[ic]; ic &= np.abs(Z) <= 2.0
    t = res // 4
    return 6.0 * (np.array([ic[a*t:(a+1)*t, b*t:(b+1)*t].mean() for a in range(4) for b in range(4)]) - 0.5)


EKLER = list(G.EK)
AILE = [G.EK[e][0] for e in EKLER]


def nn_dogruluk(V, etiket):
    X = np.array(V, float); X = X - X.mean(0)
    X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    S = X @ X.T; np.fill_diagonal(S, -9)
    j = S.argmax(1)
    acc = np.mean([etiket[i] == etiket[j[i]] for i in range(len(X))])
    marj = []
    for i in range(len(X)):
        ayni = [S[i, k] for k in range(len(X)) if k != i and etiket[k] == etiket[i]]
        fark = [S[i, k] for k in range(len(X)) if etiket[k] != etiket[i]]
        if ayni: marj.append(max(ayni) - max(fark))
    return acc, float(np.mean(marj)) if marj else 0.0


def egit(tur=12, lam=8, tohum=1):
    rng = random.Random(tohum)
    koord = {e: G.ek_koordinat(e)[:2] for e in EKLER}
    V = {e: patch(*koord[e]) for e in EKLER}
    def amac():
        a, m = nn_dogruluk([V[e] for e in EKLER], AILE)
        X = np.array([V[e] for e in EKLER])
        D = np.linalg.norm(X[:, None] - X[None], axis=2); np.fill_diagonal(D, 9e9)
        kimlik = float(np.mean(np.minimum(D.min(1), 4.0))) / 4.0   # her ek diğerlerinden ne kadar ayrık
        return a + 0.2 * m + 0.5 * kimlik, a, m
    en, a0, m0 = amac()
    baslangic = (a0, m0)
    sigma = 0.004
    for t in range(tur):
        for e in EKLER:
            eski_k, eski_v = koord[e], V[e]
            en_aday = None
            for _ in range(lam):
                k = (eski_k[0] + rng.gauss(0, sigma), eski_k[1] + rng.gauss(0, sigma))
                V[e] = patch(*k)
                sk, _, _ = amac()
                if sk > en and (en_aday is None or sk > en_aday[0]):
                    en_aday = (sk, k, V[e])
            if en_aday:
                en, koord[e], V[e] = en_aday
            else:
                koord[e], V[e] = eski_k, eski_v
        sigma *= 0.85
        _, a, m = amac()
        print(f"tur {t+1}: NN aile doğruluğu {a:.3f}, marj {m:.3f}")
    return koord, baslangic, amac()[1:]


def kelime_testi(koord_fn, adi):
    """UD'den Türkçe -> Güneş Dili; kelime gömmesi = ek vektörleri toplamı; en yakın merkezle özellik tahmini."""
    import ud, gunes_dil_v4 as M
    KEL = re.compile(r"^[a-zçğıöşüâîûA-ZÇĞİÖŞÜÂÎÛ'’]+$")
    cache = {}
    def vek(ekler):
        if koord_fn is None:                               # tek-sıcak torba (üst sınır)
            v = np.zeros(len(EKLER) + 1)
            for e in ekler: v[EKLER.index(e)] += 1
            return v
        YUV = ["yapım", "çatı", "olumsuz", "zaman", "kip", "çokluk", "iyelik", "hal", "aitlik", "ek-fiil", "kişi", "soru"]
        v = np.zeros(16 * len(YUV))
        f = G.fsa(ekler, "N") or G.fsa(ekler, "V") or [(e, "yapım") for e in ekler]
        for x in f:
            e, yv = x[0], x[1]
            if e not in cache: cache[e] = patch(*koord_fn(e))
            i = YUV.index(yv) if yv in YUV else 0
            v[16 * i:16 * i + 16] += cache[e]
        return v
    def veri(bolum, sinir):
        X, Y = [], []
        for c in ud.oku(bolum):
            for form, lemma, upos, feats, mwt in c:
                if mwt or upos not in ("NOUN",) or not KEL.match(form) or "Case" not in feats: continue
                r = M.tokenize(form)
                g = G.turkceden(r, M) if r.get("tokenlar") else None
                if not g: continue
                X.append(vek(g["ekler"])); Y.append((feats["Case"], feats.get("Number"), feats.get("Person[psor]")))
                if len(X) >= sinir: return X, Y
        return X, Y
    Xtr, Ytr = veri("train", 6000); Xte, Yte = veri("test", 3000)
    sonuc = {}
    for k, ad in enumerate(["hal", "çokluk", "iyelik"]):
        mer = collections.defaultdict(list)
        for x, y in zip(Xtr, Ytr): mer[y[k]].append(x)
        C = {lab: np.mean(v, 0) for lab, v in mer.items()}
        dog = np.mean([min(C, key=lambda l: np.linalg.norm(x - C[l])) == y[k] for x, y in zip(Xte, Yte)])
        cogunluk = collections.Counter(y[k] for y in Ytr).most_common(1)[0][0]
        taban = np.mean([y[k] == cogunluk for y in Yte])
        sonuc[ad] = (round(float(dog), 3), round(float(taban), 3))
    print(adi, sonuc)
    return sonuc


if __name__ == "__main__":
    koord, (a0, m0), (a1, m1) = egit()
    json.dump({e: [koord[e][0], koord[e][1], G.ZOOM] for e in EKLER}, open("gunes_dili_koordinat.json", "w"))
    # rastgele koordinat ablasyonu
    rng = random.Random(3)
    rast = {e: (G.MERKEZ.real + rng.uniform(-1, 1) * G.OLCEK, G.MERKEZ.imag + rng.uniform(-1, 1) * G.OLCEK) for e in EKLER}
    ar, mr = nn_dogruluk([patch(*rast[e]) for e in EKLER], AILE)
    sans = sum((c / len(AILE)) ** 2 for c in collections.Counter(AILE).values())
    s = {"nn_tasarim": [a0, m0], "nn_evrimsel": [a1, m1], "nn_rastgele": [ar, mr], "sans": sans}
    print(s)
    s["kelime_tasarim_egitilmis"] = kelime_testi(lambda e: koord[e], "eğitilmiş fraktal")
    s["kelime_rastgele"] = kelime_testi(lambda e: rast[e], "rastgele koordinat fraktal")
    s["kelime_tek_sicak"] = kelime_testi(None, "tek-sıcak (one-hot) üst sınır")
    json.dump(s, open("fraktal_sonuc.json", "w"), ensure_ascii=False, indent=1)
