"""Güneş Dili kanıt defteri: tüm testleri çalıştırır, sonuçları kanit_defteri.json'a yazar."""
import json, random, re, collections, time, statistics
import gunes_dili as G
import gunes_dil_v4 as M
import ud

KEL = re.compile(r"^[a-zçğıöşüâîûA-ZÇĞİÖŞÜÂÎÛ'’]+$")
S = {}

# T1 teorem + determinizm
ih, durum = G.fsa_determinizm()
S["T1_determinizm"] = {"taranan_durum": durum, "ek_sayisi": len(G.EK), "ihlal": len(ih)}

# T2 kaba kuvvet: gerçek köklerle tüm ek dizileri
random.seed(7)
kokler_N = [k for k, (t, tur) in G.SOZLUK.items() if tur == "N"]
kokler_V = [k for k, (t, tur) in G.SOZLUK.items() if tur == "V"]
t0 = time.time()
tp = gc = hata = 0
for k in ["ag", "ew", "gel"] + random.sample(kokler_N, 2) + random.sample(kokler_V, 2):
    a, b, c = G.kaba_kuvvet_dogrulama([k], max_ek=3)
    tp += a; gc += b; hata += c
for k in random.sample(kokler_N, 40) + random.sample(kokler_V, 40):
    a, b, c = G.kaba_kuvvet_dogrulama([k], max_ek=2)
    tp += a; gc += b; hata += c
S["T2_kaba_kuvvet"] = {"denenen_dizi": tp, "gecerli_kelime": gc, "tek_cozumleme_hatasi": hata,
                       "sure_sn": round(time.time() - t0, 1)}

# T3 rastgele harf dizileri: Güneş Dili alfabesiyle bile çoğu geçersiz (dil sınanabilir)
alf = G.UNLU + G.UNSUZ
rs = ["".join(random.choice(alf) for _ in range(random.randint(3, 10))) for _ in range(20000)]
S["T3_rastgele_gecerlilik"] = sum("hata" not in G.cozumle(w) for w in rs) / len(rs)

# T4 Türkçe -> Güneş Dili çevirisi (UD test, bağlamlı Türkçe çözümleme)
say = collections.Counter()
ornek, tr_allomorf, tr_belirsizlik, uzun_tr, uzun_gd, ek_tr, ek_gd = [], collections.defaultdict(set), [], [], [], [], []
for c in ud.oku("test"):
    idx = [i for i, t in enumerate(c) if KEL.match(t[0])]
    rs_ = M.cozumle_cumle([c[i][0] for i in idx])
    for i, r in zip(idx, rs_):
        form, lemma, upos, feats, mwt = c[i]
        if upos in ("PUNCT", "NUM", "SYM", "X"):
            continue
        say["kelime"] += 1
        if not r.get("tokenlar"):
            say["tr_cozumlenemedi"] += 1; continue
        if r["tokenlar"][0][1].islev == "soru":
            say["soru_eki"] += 1; continue
        for b, e in r["tokenlar"][1:]:
            tr_allomorf[e.islev.split(" (")[0]].add(b)
        tr_belirsizlik.append(r.get("alternatif", 1))
        g = G.turkceden(r, M)
        if not g:
            say["gd_uretilemedi"] += 1; continue
        geri = G.cozumle(g["kelime"])
        if "hata" in geri:
            say["gd_gecersiz"] += 1
            if len(ornek) < 30: ornek.append((form, g["kelime"], geri["hata"]))
            continue
        say["gd_gecerli"] += 1
        if [x[0] for x in geri["ekler"]] == g["ekler"] and geri["kok"] == g["kok"]:
            say["gidis_donus_ok"] += 1
        if G.SOZLUK.get(geri["kok"], (None,))[0] == g["tr_kok"]:
            say["kok_geri"] += 1
        uzun_tr.append(len(form)); uzun_gd.append(len(g["kelime"]))
        ek_tr.append(len(r["tokenlar"])); ek_gd.append(1 + len(g["ekler"]))
S["T4_ceviri"] = {k: v for k, v in say.items()}
S["T4_oranlar"] = {"gecerli/cevrilen": say["gd_gecerli"] / max(1, say["kelime"] - say["soru_eki"]),
                   "gidis_donus": say["gidis_donus_ok"] / max(1, say["gd_gecerli"]),
                   "kok_geri_kazanim": say["kok_geri"] / max(1, say["gd_gecerli"])}
S["T4_gecersiz_ornek"] = ornek[:15]

# T5 öğrenilebilirlik
S["T5_ogrenilebilirlik"] = {
    "turkce_islev_basina_ortalama_bicim": statistics.mean(len(v) for v in tr_allomorf.values()),
    "turkce_en_cok_bicimli": sorted(((k, len(v), sorted(v)[:12]) for k, v in tr_allomorf.items()),
                                    key=lambda x: -x[1])[:8],
    "gunes_dili_islev_basina_bicim": 1,
    "turkce_ortalama_aday_cozumleme": statistics.mean(tr_belirsizlik),
    "gunes_dili_aday_cozumleme": 1,
    "turkce_ses_kurali": ["2'li ünlü uyumu", "4'lü ünlü uyumu", "ünsüz benzeşmesi (d/t, c/ç)", "yumuşama (p/b, ç/c, t/d, k/ğ)",
                          "kaynaştırma (y, n, s)", "ünlü düşmesi", "ikizleşme", "daralma (-yor)", "zamir n'si", "ince ünlülü alıntılar"],
    "gunes_dili_ses_kurali": [],
    "ortalama_harf_tr": statistics.mean(uzun_tr), "ortalama_harf_gd": statistics.mean(uzun_gd),
    "ortalama_morfem_tr": statistics.mean(ek_tr), "ortalama_morfem_gd": statistics.mean(ek_gd),
}
json.dump(S, open("kanit_defteri.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=list)
print(json.dumps(S, ensure_ascii=False, indent=1, default=list)[:6000])
