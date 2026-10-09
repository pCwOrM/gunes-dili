// Güneş Dili motoru: Türkçe çözümleyici (gunes_dil_v4.py'nin birebir JS karşılığı) + Güneş Dili dilbilgisi
// Tarayıcıda ve Node'da çalışır. VERI: motor_veri.js
(function (kok_) {
const VERI = (typeof module !== "undefined" && typeof require !== "undefined") ? require("./motor_veri.js") : kok_.VERI;

// ------------------------------------------------------------------ Türkçe
const VOWELS = "aeıioöuü", BACK = new Set("aıou"), FRONT = new Set("eiöü"), ROUND = new Set("ouöü");
const VOICELESS = new Set("çfhkpsşt"), CONS = "bcçdfgğhjklmnprsştvyz", HIGH = "ıiuü";
const isV = c => c !== undefined && VOWELS.includes(c), isC = c => c !== undefined && CONS.includes(c);
const Ek = (ad, sablon, giris, cikis, yuva, islev) => ({ ad, sablon, giris, cikis, yuva, islev });
const EKLER = VERI.EKLER.map(x => Ek(...x));
const KOKLER = new Map();
{ const ks = VERI.KOK_SIRA.split(" "), ts = VERI.KOK_TUR; for (let i = 0; i < ks.length; i++) KOKLER.set(ks[i], ts[i]); }
const FIIL_DE = new Set(VERI.FIIL_DE.split(" "));
const GOREVLI = VERI.GOREVLI, ZAMIR_GOVDE = VERI.ZAMIR_GOVDE, KISA = new Set(VERI.KISA);
const MODEL = VERI.MODEL;
let BAGLAM_AGIRLIK = VERI.BAGLAM_AGIRLIK;
const SERT = { b: "p", c: "ç", d: "t", ğ: "k" };

function sonUnlu(s) { for (let i = s.length - 1; i >= 0; i--) if (isV(s[i])) return s[i]; return "e"; }
function gercek(sablon, onceki, ince = false) {
  let out = onceki, i = 0, ilk = true;
  while (i < sablon.length) {
    const ch = sablon[i];
    if (ch === "(") {
      const j = sablon.indexOf(")", i), parca = sablon.slice(i + 1, j), son = out.length ? out[out.length - 1] : "a";
      if (parca === "I") { if (!isV(son)) { out += gercek("I", out, ince && ilk); ilk = false; } }
      else if (isV(son)) out += parca;
      i = j + 1; continue;
    }
    const v = sonUnlu(out), geri = BACK.has(v) && !(ince && ilk);
    if (ch === "A") { out += geri ? "a" : "e"; ilk = false; }
    else if (ch === "I") { out += geri ? (ROUND.has(v) ? "u" : "ı") : (ROUND.has(v) ? "ü" : "i"); ilk = false; }
    else if (ch === "D") out += (out && VOICELESS.has(out[out.length - 1])) ? "t" : "d";
    else if (ch === "C") out += (out && VOICELESS.has(out[out.length - 1])) ? "ç" : "c";
    else if (ch === "G") out += (out && VOICELESS.has(out[out.length - 1])) ? "k" : "g";
    else if (ch === "K") out += "k";
    else out += ch;
    i++;
  }
  return out.slice(onceki.length);
}
function birlesikIyelik(kok) {
  if (kok.length < 6 || !HIGH.includes(kok[kok.length - 1])) return false;
  const govde = kok[kok.length - 2] === "s" ? kok.slice(0, -2) : kok.slice(0, -1);
  const ad = [govde]; if (govde && SERT[govde[govde.length - 1]]) ad.push(govde.slice(0, -1) + SERT[govde[govde.length - 1]]);
  for (const g of ad) for (let i = 2; i < g.length - 1; i++) if (KOKLER.has(g.slice(0, i)) && KOKLER.has(g.slice(i)) && g.slice(i).length >= 2) return true;
  return false;
}
function kokAdaylari(w) {
  const out = [], n = w.length;
  for (let i = 1; i <= n; i++) {
    const on = w.slice(0, i), sonra = w.slice(i, i + 3), us = i < n && isV(w[i]);
    const aday = [[on, ""]];
    if (us) {
      if (SERT[on[on.length - 1]]) aday.push([on.slice(0, -1) + SERT[on[on.length - 1]], "yumuşama"]);
      if (on.endsWith("ng")) aday.push([on.slice(0, -1) + "k", "yumuşama"]);
      if (on.length >= 3 && on[on.length - 1] === on[on.length - 2] && isC(on[on.length - 1])) aday.push([on.slice(0, -1), "ikizleşme"]);
      if (on.length >= 3 && isC(on[on.length - 1]) && isC(on[on.length - 2]))
        for (const v of HIGH) {
          aday.push([on.slice(0, -1) + v + on[on.length - 1], "ünlü düşmesi"]);
          if (SERT[on[on.length - 1]]) aday.push([on.slice(0, -1) + v + SERT[on[on.length - 1]], "ünlü düşmesi+yumuşama"]);
        }
    }
    if (sonra.startsWith("yor") && HIGH.includes(on[on.length - 1])) for (const v of "ae") aday.push([on.slice(0, -1) + v, "daralma"]);
    if ((on === "di" || on === "yi") && i < n && w[i] === "y") aday.push([on[0] + "e", "daralma"]);
    if (Object.prototype.hasOwnProperty.call(ZAMIR_GOVDE, on)) aday.push([ZAMIR_GOVDE[on], "zamir gövdesi"]);
    for (const [kok, olay] of aday) {
      if (!KOKLER.has(kok)) continue;
      const tl = new Set([KOKLER.get(kok)]); if (FIIL_DE.has(kok)) tl.add("V");
      for (const t of [...tl].sort()) out.push([kok, on, t, olay]);
      if (KOKLER.get(kok) === "N" && birlesikIyelik(kok)) out.push([kok, on, "N", (olay ? olay + "+" : "") + "birleşik iyelik 3"]);
    }
  }
  return out;
}
function ayristir(kelime, ince = false, kokSabit = null, sadeceYapim = false) {
  const sonuc = [];
  function ilerle(poz, yuzey, tur, yuva, yol, ilkEk) {
    if (sonuc.length > 300) return;
    if (poz === kelime.length) { sonuc.push(yol.slice()); return; }
    const son = yol[yol.length - 1][1];
    for (const ek of EKLER) {
      if (ek.giris !== tur) continue;
      if (sadeceYapim && ek.yuva !== 0) continue;
      if (ek.yuva === 0 && yuva !== 0) continue;
      if (ek.yuva !== 0 && ek.yuva <= yuva && !(yuva === 13 && ek.yuva >= 10 && ek.yuva < 20)) continue;
      const son3 = son.islev.startsWith("iyelik 3") || (son.yuva === -1 && son.islev.includes("birleşik iyelik 3"));
      if (ek.yuva === 12 && ek.islev.includes("zamir n") !== son3 &&
          !(ek.islev.startsWith("vasıta") || ek.islev.startsWith("ilgi") || ek.islev.startsWith("eşitlik"))) continue;
      if (ek.yuva === 30 && ek.islev.includes("sonrası") !== KISA.has(son.islev)) continue;
      if (ek.yuva === 15 && son.yuva !== 3) continue;
      if (ek.islev.startsWith("şahıs") && tur === "V" && (son.yuva === 0 || son.yuva === 1 || son.yuva === -1) && ek.yuva === 30) continue;
      let bicim = gercek(ek.sablon, yuzey, ince && ilkEk).replace(/K/g, "k");
      const ad = [bicim];
      if (bicim && bicim[bicim.length - 1] === "k" && ek.sablon.endsWith("K")) ad.push(bicim.slice(0, -1) + "ğ");
      if (ek.yuva === 1 && kelime.startsWith("yor", poz + bicim.length)) ad.push(bicim.slice(0, -1) + gercek("I", yuzey + bicim.slice(0, -1)));
      for (const b of ad) {
        if (!b || !kelime.startsWith(b, poz)) continue;
        if ((ek.islev === "ettirgen çatı (-ar)" || ek.islev === "ettirgen çatı (-ir)") && !(KOKLER.get(yuzey + b) === "V" || FIIL_DE.has(yuzey + b))) continue;
        if ((ek.islev === "fiilden isim" || ek.islev === "fiilden isim (-gı)" || ek.islev === "fiilden isim (-ıntı)") && KOKLER.get(yuzey + b) !== "N") continue;
        if (b.endsWith("ğ") && b !== bicim && !(poz + b.length < kelime.length && isV(kelime[poz + b.length]))) continue;
        const ny = (ek.yuva === 0 || ek.yuva === 2) ? 0 : (ek.yuva === 13 ? 9 : ek.yuva);
        yol.push([b, ek]); ilerle(poz + b.length, yuzey + b, ek.cikis, ny, yol, false); yol.pop();
      }
    }
  }
  if (kokSabit) {
    const [kok, yz, tur, olay] = kokSabit, tel = kokSabit.length > 4 ? kokSabit[4] : yz;
    kelime = tel + kelime.slice(yz.length);
    ilerle(tel.length, tel, tur, 0, [[yz, Ek("kök", kok, tur, tur, -1, `kök (${kok})` + (olay ? ` · ${olay}` : ""))]], true);
    return sonuc;
  }
  for (const [kok, yz, tur, olay] of kokAdaylari(kelime))
    ilerle(yz.length, yz, tur, 0, [[yz, Ek("kök", kok, tur, tur, -1, `kök (${kok})` + (olay ? ` · ${olay}` : ""))]], true);
  return sonuc;
}
function uyum(w) {
  for (const c of w) if (!isV(c) && !isC(c)) return false;
  const v = [...w].filter(isV); if (!v.length) return false;
  if (w.length > 1 && isC(w[0]) && isC(w[1])) return false;
  return v.every(c => BACK.has(c)) || v.every(c => FRONT.has(c));
}
function uyumOzel(w) { return [...w].every(c => isV(c) || isC(c) || "qwx".includes(c)) && [...w].some(isV); }
const etiketler = p => [p[0][1].giris].concat(p.slice(1).map(([, e]) => e.ad + "|" + e.islev));
const get = (o, k) => (Object.prototype.hasOwnProperty.call(o, k) ? o[k] : 0);
const NTEKLI = Object.keys(MODEL.tekli).length;
function puan(p) {
  const kok = p[0][1].sablon, olay = (p[0][1].islev.match(/·/g) || []).length;
  const rc = get(MODEL.kok, kok), rn = MODEL.kok_toplam, rv = MODEL.kok_tur;
  let pk = Math.log((rc + 0.1) / (rn + 0.1 * rv));
  if (rc === 0) pk += MODEL.gorulmemis + 0.35 * Math.min([...kok].length, 8);
  if (FIIL_DE.has(kok)) pk += Math.log((get(MODEL.kok_tip || {}, kok + "|" + p[0][1].giris) + 0.5) / (rc + 1.0));
  const et = etiketler(p).concat(["</s>"]);
  let s = 0;
  for (let i = 0; i + 1 < et.length; i++) {
    const a = et[i], b = et[i + 1];
    const cab = get(MODEL.ikili, a + "→" + b), ca = get(MODEL.tekli, a);
    const pb = (get(MODEL.tekli, b) + 0.5) / (MODEL.tekli_toplam + 0.5 * NTEKLI);
    s += Math.log((cab + 2.0 * pb) / (ca + 2.0));
  }
  return pk + s - 1.5 * olay;
}
const turCache = new Map();
function turetmeAgaci(kok) {
  if (turCache.has(kok)) return turCache.get(kok);
  let en = null;
  for (const [alt, yz, tur, olay] of kokAdaylari(kok)) {
    if (alt.length >= kok.length || alt.length < 2 || olay) continue;
    for (const p of ayristir(kok, false, [alt, yz, tur, ""], true))
      if (en === null || p[0][0].length < en[0][0].length) en = p;
  }
  turCache.set(kok, en);
  return en;
}
function kucult(k) {
  return k.replace(/I/g, "ı").replace(/İ/g, "i").toLowerCase().replace(/̇/g, "")
    .replace(/â/g, "a").replace(/î/g, "i").replace(/û/g, "u").replace(/’/g, "'");
}
function isaretle(p, not) { const k = p[0][1]; p[0] = [p[0][0], Ek("kök", k.sablon, k.giris, k.cikis, -1, k.islev + " · " + not)]; return p; }
const buyukMu = s => s.length > 0 && s === s.toUpperCase() && s !== s.toLowerCase();
const ilkBuyuk = s => s.length > 0 && s[0] === s[0].toUpperCase() && s[0] !== s[0].toLowerCase();
function adaylar(ham, ozelAdAdayi = false) {
  const w = kucult(ham);
  let ps = [], koken = null;
  if (w.includes("'")) {
    const i = w.indexOf("'"), kok = w.slice(0, i), ek = w.slice(i + 1), tam = kok + ek;
    const tels = ([...kok.slice(-2)].some(isV) || kok.length > 4) ? [kok] : [kok, kok + "e", kok + "a"];
    for (const tl of tels) for (const ince of [false, true])
      for (const p of ayristir(tam, ince, [kok, kok, "N", "", tl])) ps.push(isaretle(p, "özel ad"));
    for (const p of ayristir(tam)) {
      let t = 0; const sin = new Set();
      for (const [b] of p) { t += b.length; sin.add(t); }
      if (sin.has(kok.length)) ps.push(p);
    }
    koken = "özel ad (kesme işaretli)";
  } else {
    ps = ayristir(w);
    for (const p of ayristir(w, true)) {
      const s = p[0][1].sablon;
      if (isC(s[s.length - 1]) && BACK.has(sonUnlu(s)) && p.length > 1) ps.push(isaretle(p, "ince ünlü (alıntı)"));
    }
    if (buyukMu(ham) && w.length <= 6 && !ps.length) { ps = [[[w, Ek("kök", w, "N", "N", -1, `kök (${w}) · kısaltma`)]]]; koken = "kısaltma"; }
    else if ((ozelAdAdayi || !ps.length) && ilkBuyuk(ham) && uyumOzel(w)) {
      const bos = !ps.length;
      ps.push([[w, Ek("kök", w, "N", "N", -1, `kök (${w}) · özel ad`)]]);
      for (let i = 3; i < w.length; i++) {
        if (KOKLER.has(w.slice(0, i))) continue;
        for (const p of ayristir(w, false, [w.slice(0, i), w.slice(0, i), "N", ""])) if (p.length > 1) ps.push(isaretle(p, "özel ad"));
      }
      if (bos) koken = "özel ad";
    }
    if (!ps.length && w.length <= 3 && [...w].every(isC)) { ps = [[[w, Ek("kök", w, "N", "N", -1, `kök (${w}) · kısaltma`)]]]; koken = "kısaltma"; }
  }
  const gor = new Set(), tek = [];
  for (const p of ps) {
    const a = JSON.stringify(p.map(([b, e]) => [b, e.ad, e.islev, e.sablon]));
    if (!gor.has(a)) { gor.add(a); tek.push(p); }
  }
  return [tek, koken];
}
function inan(kok) { return kok && isV(kok[kok.length - 1]) ? kok + "ğ" : null; }
function sonucYap(w, ps, koken, k) {
  const en = ps[0], kok = en[0][1].sablon, isl = en[0][1].islev;
  const ozel = isl.includes("özel ad") || isl.includes("kısaltma");
  return { durum: "KABUL", tokenlar: en, alternatif: ps.length, alternatifler: ps.slice(1, k),
    turetme: ozel ? null : turetmeAgaci(kok),
    koken: isl.includes("özel ad") ? "özel ad" : isl.includes("kısaltma") ? "kısaltma" : (uyum(kok) ? "yerli yapı" : "alıntı kök (ünlü uyumu dışı)"),
    inan: ozel ? null : inan(kok) };
}
const SORU_RE = /^m[ıiuü](y?d[ıiuü]r|s[ıiuü]n(ız|iz|uz|üz)?|y[ıiuü]m|y[ıiuü]z|yd[ıiuü].*|ym[ıi]ş.*)$/;
function gorevli(w) {
  if (Object.prototype.hasOwnProperty.call(GOREVLI, w)) { const [t, l] = GOREVLI[w]; return [[w, Ek(t, l, "X", "X", -1, t)]]; }
  if (SORU_RE.test(w)) return [[w.slice(0, 2), Ek("soru", "mi", "X", "X", -1, "soru")], [w.slice(2), Ek("-ek-fiil", w.slice(2), "X", "X", 30, "soru eki çekimi")]];
  return null;
}
function red(w) {
  if (kokAdaylari(w).length) return { durum: "RED: ek sırası/biçimi Türkçe şablona aykırı", tokenlar: [], alternatif: 0 };
  if (uyum(w)) return { durum: "BİLİNMEYEN KÖK (uyumlu, sözlük dışı)", tokenlar: [], alternatif: 0 };
  return { durum: "RED: yerli kök ölçütü sağlanmıyor -> alıntı/yabancı", tokenlar: [], alternatif: 0 };
}
const sirala = (ps, f) => ps.map((p, i) => [f(p), i, p]).sort((a, b) => (b[0] - a[0]) || (a[1] - b[1])).map(x => x[2]);
function tokenize(kelime, k = 3, ozel = false) {
  const ham = kelime.trim(), w = kucult(ham);
  if (!w) return { durum: "Boş giriş", tokenlar: [], alternatif: 0 };
  const g = gorevli(w);
  if (g) return { durum: "KABUL", tokenlar: g, alternatif: 1, alternatifler: [], turetme: null, koken: "görevli kelime", inan: null };
  let [ps, koken] = adaylar(ham, ozel);
  if (!ps.length) return red(w);
  ps = sirala(ps, puan);
  return sonucYap(w, ps, koken, k);
}
const HAL_KISA = [["belirtme", "Acc"], ["ilgi", "Gen"], ["yönelme", "Dat"], ["bulunma", "Loc"], ["ayrılma", "Abl"], ["vasıta", "Ins"], ["eşitlik", "Equ"]];
function ozet(p) {
  let hal = "Nom", iye = "-", cok = 0, neg = 0;
  for (const [, e] of p.slice(1)) {
    for (const [k, v] of HAL_KISA) if (e.islev.startsWith(k)) hal = v;
    if (e.islev.startsWith("iyelik")) iye = e.islev.split(" ")[1][0];
    if (e.islev === "çokluk") cok = 1;
    if (e.islev.includes("olumsuz")) neg = 1;
  }
  const son = p[p.length - 1][1], tur = son.yuva !== -1 ? son.cikis : son.giris;
  return `${tur}|${hal}|${iye}|${cok}|${neg}|${p[0][1].islev.includes("özel ad") ? 1 : 0}`;
}
function baglam(onc, snr, buyukIc) {
  let pg = 0;
  if (onc) { const oz = ozet(onc).split("|"); pg = oz[1] === "Gen" ? 1 : ((oz[0] === "N" && oz[1] === "Nom" && oz[2] === "-") ? 2 : 0); }
  let sv = 0;
  if (snr) { const son = snr[snr.length - 1][1]; sv = (son.cikis === "V" && son.yuva >= 3) ? 1 : 0; }
  return `${pg}${sv}${buyukIc ? 1 : 0}`;
}
function baglamPuani(p, ctx) {
  const B = MODEL.baglam; if (!B) return 0;
  const o = ozet(p), K = 50.0;
  return BAGLAM_AGIRLIK * (Math.log((get(B.oc, o + "#" + ctx) + 1) / (get(B.c, ctx) + K)) - Math.log((get(B.o, o) + 1) / (B.n + K)));
}
function cozumleCumle(kelimeler, k = 3) {
  const ham = kelimeler.map(w => w.trim()), al = [], kk = [];
  ham.forEach((h, i) => {
    const w = kucult(h), g = w ? gorevli(w) : null;
    if (g || !w) { al.push(["G", g]); kk.push(null); return; }
    let [ps, ko] = adaylar(h, i > 0 && ilkBuyuk(h));
    ps = sirala(ps, puan);
    al.push(["P", ps]); kk.push(ko);
  });
  const enler = al.map(a => (a[0] === "P" && a[1].length) ? a[1][0] : null);
  return al.map(([tip, ps], i) => {
    const w = kucult(ham[i]);
    if (tip === "G") return ps ? { durum: "KABUL", tokenlar: ps, alternatif: 1, alternatifler: [], turetme: null, koken: "görevli kelime", inan: null } : { durum: "Boş giriş", tokenlar: [] };
    if (!ps.length) return red(w);
    const ctx = baglam(i > 0 ? enler[i - 1] : null, i + 1 < enler.length ? enler[i + 1] : null, i > 0 && ilkBuyuk(ham[i]));
    return sonucYap(w, sirala(ps, p => puan(p) + baglamPuani(p, ctx)), kk[i], k);
  });
}

// ------------------------------------------------------------------ Güneş Dili
const UNLU = "aeiou", UNSUZ = "mknyswplbtgdfhr";
const AILELER = VERI.AILELER, YAPIM_TUR = VERI.YAPIM_TUR, Z_YAPIM = new Set(VERI.Z_YAPIM), TEKRARLI = new Set(VERI.TEKRARLI);
const FIIL_YUVA = VERI.FIIL_YUVA.map(([a, k]) => [a, new Set(k)]), ISIM_YUVA = VERI.ISIM_YUVA.map(([a, k]) => [a, new Set(k)]);
const EK = {};
for (const [c, [eski, aile, uyeler]] of Object.entries(AILELER)) for (const [f, is] of Object.entries(uyeler)) EK[f] = [c, aile, is];
const GSOZ = new Map(), TR2GD = new Map();
for (const [gd, tr, tur] of VERI.GD_SOZLUK) { GSOZ.set(gd, [tr, tur]); TR2GD.set(tr + "|" + tur, gd); }
const KOK_RE = new RegExp(`^[${UNSUZ}]?[${UNLU}]([${UNSUZ}][${UNLU}])*[${UNSUZ}]$`);
const kokGecerli = k => KOK_RE.test(k);
const gU = c => UNLU.includes(c), gK = c => UNSUZ.includes(c);
function sinirBul(w) {
  const k = []; for (let i = 0; i < w.length - 1; i++) if (gK(w[i]) && gK(w[i + 1])) k.push(i);
  if (!k.length) return (w && gK(w[w.length - 1])) ? w.length : null;
  if (k.length > 1) return null;
  return k[0] + 1;
}
function kurallar(e, tur, yuva, gecmis) {
  const k = [];
  if (YAPIM_TUR[e] && YAPIM_TUR[e][0] === tur && (yuva === -1 || (tur === "V" && yuva <= 1) || (tur === "V" && Z_YAPIM.has(e) && yuva <= 2))) k.push(["yapım", null]);
  const yv = tur === "V" ? FIIL_YUVA : ISIM_YUVA;
  for (let i = 0; i < yv.length; i++) {
    const [ad, kume] = yv[i];
    if ((i < yuva || (i === yuva && !TEKRARLI.has(ad))) || !kume.has(e)) continue;
    if (ad === "kişi") {
      if (tur === "N" && !gecmis.has("ek-fiil")) continue;
      if (tur === "V" && !(gecmis.has("zaman") || gecmis.has("kip") || gecmis.has("ek-fiil"))) continue;
    }
    if (ad === "iyelik" && gecmis.has("ek-fiil")) continue;
    k.push([ad, i]); break;
  }
  return k;
}
function fsa(ekler, tur) {
  const s = []; let yuva = -1, gecmis = new Set();
  for (const e of ekler) {
    if (!EK[e] || tur === "Z") return null;
    const k = kurallar(e, tur, yuva, gecmis);
    if (!k.length) return null;
    const [ad, i] = k[0];
    if (ad === "yapım") { tur = YAPIM_TUR[e][1]; yuva = -1; gecmis = new Set(); s.push([e, "yapım", EK[e][2], tur]); }
    else { yuva = i; gecmis.add(ad); s.push([e, ad, (ad === "iyelik" || ad === "kişi") ? `${ad} ${EK[e][2]}` : EK[e][2], tur]); }
  }
  return s;
}
function gdCozumle(w) {
  w = w.trim().toLowerCase();
  if (!w || [...w].some(c => !gU(c) && !gK(c))) return { hata: `Güneş Dili alfabesi dışı harf (alfabe: ${UNLU} + ${UNSUZ})` };
  const s = sinirBul(w);
  if (s === null) return { hata: "Kök-ek sınırı bulunamadı: kelimede birden fazla ünsüz kümesi var ya da kök ünsüzle bitmiyor" };
  const kok = w.slice(0, s), kalan = w.slice(s);
  if (!kokGecerli(kok)) return { hata: `'${kok}' geçerli bir kök biçimi değil ((K)Ü(KÜ)*K olmalı)` };
  if (kalan.length % 2) return { hata: "Ek bölümü ünsüz+ünlü çiftlerine bölünemiyor" };
  const ekler = []; for (let i = 0; i < kalan.length; i += 2) ekler.push(kalan.slice(i, i + 2));
  const tl = GSOZ.has(kok) ? [...GSOZ.get(kok)[1]] : [];
  for (const t of ["N", "V"]) if (!tl.includes(t)) tl.push(t);
  for (const t of tl) { const f = fsa(ekler, t); if (f) return { kok, tur: t, ekler: f, turkce: GSOZ.has(kok) ? GSOZ.get(kok)[0] : null }; }
  return { hata: "Ek sırası Güneş Dili şablonuna aykırı", kok, ekler_ham: ekler };
}
const HARF = VERI.HARF;
function uyarla(tr) {
  let s = [...tr.toLowerCase()].map(c => HARF[c] !== undefined ? HARF[c] : c).join("");
  s = [...s].filter(c => gU(c) || gK(c)).join("");
  if (!s) return null;
  const out = [];
  for (const c of s) {
    if (out.length) {
      const p = out[out.length - 1];
      if (gK(p) && gK(c)) { let v = [...out].reverse().find(gU); if (v === undefined) v = [...s].find(gU) || "a"; out.push(v); }
      else if (gU(p) && gU(c)) out.push("y");
    }
    out.push(c);
  }
  if (gU(out[out.length - 1])) out.push("n");
  const k = out.join("");
  return kokGecerli(k) ? k : null;
}
const ESLEME = VERI.ISLEV_ESLEME;
function islevGd(islev, ad = "") {
  const s = islev.replace("şimdiki zaman (-makta)", "şimdiki zaman");
  if (s.startsWith("fail") || ad === "-(y)IcI") return ["gi"];
  for (const [on, ekler] of ESLEME) if (s.startsWith(on)) return ekler;
  if (s.includes("ettirgen")) return ["ta"]; if (s.includes("edilgen")) return ["te"]; if (s.includes("işteş")) return ["to"];
  if (s.includes("sahiplik")) return ["go"]; if (s.includes("soyut")) return ["gu"];
  return null;
}
function turkceden(r) {
  const tok = r.tokenlar || []; if (!tok.length) return null;
  const ke = tok[0][1]; let trKok = ke.sablon, tur = ke.giris === "X" ? "N" : ke.giris;
  let zincir = [];
  const t = r.turetme;
  if (t && t[t.length - 1][1].cikis === tur) {
    let seq = [], ok = true;
    for (const [, e] of t.slice(1)) { const g = islevGd(e.islev, e.ad); if (g === null) { ok = false; break; } seq = seq.concat(g); }
    if (ok && TR2GD.has(t[0][1].sablon + "|" + t[0][1].giris)) { trKok = t[0][1].sablon; zincir = zincir.concat(seq); }
  }
  const gdKok = TR2GD.get(trKok + "|" + tur) || TR2GD.get(trKok + "|" + (tur === "V" ? "N" : "V")) || uyarla(trKok);
  if (!gdKok) return null;
  const atlanan = []; let govde = [], kisi = [], cur = tur;
  for (const [, e] of tok.slice(1)) {
    let g = islevGd(e.islev, e.ad);
    if (g === null) { atlanan.push(e.islev); continue; }
    if (cur === "V" && g.length === 1 && (g[0] === "ya" || g[0] === "ye") && !govde.some(x => "kb".includes(x[0]))) g = g[0] === "ya" ? ["ka"] : ["ku"];
    if (e.islev.startsWith("şahıs")) { kisi = kisi.concat(g); continue; }
    govde = govde.concat(g); cur = e.cikis;
  }
  if (kisi.length && !govde.some(x => ["ya", "ye", "yi", "ba"].includes(x)) && cur === "N") govde.push("yi");
  zincir = zincir.concat(govde, kisi);
  return { kelime: gdKok + zincir.join(""), kok: gdKok, ekler: zincir, atlanan, trKok };
}
function mfns(cx, cy, zoom, res = 128, maxIter = 70, izgara = 4) {
  const s = 1 / zoom, t = res / izgara, cnt = new Float64Array(izgara * izgara);
  for (let j = 0; j < res; j++) { const y = cy - s + 2 * s * j / (res - 1);
    for (let i = 0; i < res; i++) { const x = cx - s + 2 * s * i / (res - 1);
      let zx = 0, zy = 0, k = 0;
      for (; k < maxIter; k++) { const nx = zx * zx - zy * zy + x; zy = 2 * zx * zy + y; zx = nx; if (zx * zx + zy * zy > 4) break; }
      if (k === maxIter) cnt[Math.floor(j / t) * izgara + Math.floor(i / t)]++; } }
  return Array.from(cnt, v => 6 * (v / (t * t) - 0.5));
}
const MOTOR = { tokenize, cozumleCumle, adaylar, puan, turetmeAgaci, kucult, gdCozumle, fsa, sinirBul, kokGecerli, uyarla,
  turkceden, mfns, EK, AILELER, GSOZ, TR2GD, KOORD: VERI.GD_KOORD, FIIL_YUVA, ISIM_YUVA, UNLU, UNSUZ,
  setBaglam: w => { BAGLAM_AGIRLIK = w; } };
if (typeof module !== "undefined") module.exports = MOTOR; else kok_.MOTOR = MOTOR;
})(typeof window !== "undefined" ? window : globalThis);
