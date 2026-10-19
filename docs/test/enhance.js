/* ==========================================================================
   GÜNEŞ DİLİ — "Güneş Katmanı" (enhance.js)
   Orijinal sayfa betiklerine dokunmaz; yalnızca üstüne katman ekler.
   Her özellik kendi try/catch'i içindedir: biri patlarsa sayfa çalışmaya devam eder.
   ========================================================================== */
(() => {
  'use strict';
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FINE = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const page = (document.body && document.body.dataset.page) || 'home';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const safe = (name, fn) => { try { fn(); } catch (e) { console.warn('[güneş-katmanı]', name, e); } };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const store = { get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} } };

  document.documentElement.classList.add('sx');

  /* ---- ortak zamanlayıcı: sekme gizliyken durur ---- */
  const loops = new Set();
  let last = performance.now();
  const tick = (now) => {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!document.hidden) loops.forEach(fn => { try { fn(now / 1000, dt); } catch (e) { console.warn(e); } });
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);

  const pointer = { x: innerWidth / 2, y: innerHeight / 2, nx: 0, ny: 0 };
  addEventListener('pointermove', e => { pointer.x = e.clientX; pointer.y = e.clientY; pointer.nx = e.clientX / innerWidth - .5; pointer.ny = e.clientY / innerHeight - .5; }, { passive: true });

  /* =====================================================================
     1) İlerleme çubuğu + yukarı çık düğmesi
     ===================================================================== */
  safe('progress', () => {
    const bar = el('div'); bar.id = 'sx-progress'; document.body.appendChild(bar);
    let top = null;
    if (page === 'home' || page === 'wiki') {
      top = el('button', '', '<span>↑</span>'); top.id = 'sx-top'; top.setAttribute('aria-label', 'Yukarı çık');
      top.onclick = () => scrollTo({ top: 0, behavior: RM ? 'auto' : 'smooth' });
      document.body.appendChild(top);
    }
    let queued = false;
    const upd = () => {
      queued = false;
      const h = document.documentElement.scrollHeight - innerHeight;
      const p = h > 0 ? clamp(scrollY / h, 0, 1) : 0;
      bar.style.transform = `scaleX(${p})`;
      if (top) { top.style.setProperty('--p', p.toFixed(4)); top.classList.toggle('on', scrollY > 700); }
    };
    addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(upd); } }, { passive: true });
    addEventListener('resize', upd); upd();
  });

  /* =====================================================================
     2) Yıldız + kıvılcım alanı (arka plan)
     ===================================================================== */
  safe('stars', () => {
    if (page === 'ide' || page === 'paper') return;
    const cv = el('canvas'); cv.id = 'sx-stars'; document.body.prepend(cv);
    const ctx = cv.getContext('2d');
    let W = 0, H = 0, DPR = Math.min(devicePixelRatio || 1, 1.5);
    const stars = [], embers = [];
    const build = () => {
      W = cv.width = Math.floor(innerWidth * DPR); H = cv.height = Math.floor(innerHeight * DPR);
      stars.length = 0; embers.length = 0;
      const n = clamp(Math.round(innerWidth * innerHeight / 9000), 60, 190);
      for (let i = 0; i < n; i++) stars.push({ x: Math.random(), y: Math.random(), z: .2 + Math.random() * .8, tw: Math.random() * 6.28, sp: .6 + Math.random() * 1.8, hue: Math.random() < .12 ? 190 : 46 });
      for (let i = 0; i < 26; i++) embers.push({ x: Math.random(), y: Math.random(), r: .6 + Math.random() * 1.8, v: .01 + Math.random() * .03, ph: Math.random() * 6.28, a: .15 + Math.random() * .4 });
    };
    build(); addEventListener('resize', build);
    let sy = scrollY; addEventListener('scroll', () => { sy = scrollY; }, { passive: true });
    loops.add((t) => {
      ctx.clearRect(0, 0, W, H);
      const px = pointer.nx * 18, py = pointer.ny * 12;
      for (const s of stars) {
        const x = ((s.x * innerWidth + px * s.z * 2) % innerWidth + innerWidth) % innerWidth;
        const y = (((s.y * innerHeight - sy * .05 * s.z + py * s.z) % innerHeight) + innerHeight) % innerHeight;
        const a = (.25 + .75 * (.5 + .5 * Math.sin(t * s.sp + s.tw))) * s.z * .85;
        ctx.fillStyle = `hsla(${s.hue},90%,${s.hue > 100 ? 70 : 82}%,${a.toFixed(3)})`;
        ctx.beginPath(); ctx.arc(x * DPR, y * DPR, (.5 + s.z * 1.1) * DPR, 0, 6.283); ctx.fill();
      }
      for (const e of embers) {
        e.y -= e.v * .016; if (e.y < -.05) { e.y = 1.05; e.x = Math.random(); }
        const x = (e.x + Math.sin(t * .5 + e.ph) * .018) * innerWidth, y = e.y * innerHeight;
        const g = ctx.createRadialGradient(x * DPR, y * DPR, 0, x * DPR, y * DPR, e.r * 7 * DPR);
        g.addColorStop(0, `rgba(255,200,60,${e.a})`); g.addColorStop(1, 'rgba(255,140,0,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x * DPR, y * DPR, e.r * 7 * DPR, 0, 6.283); ctx.fill();
      }
    });
  });

  /* =====================================================================
     3) İmleç ışığı
     ===================================================================== */
  safe('cursor', () => {
    if (!FINE || RM || page === 'ide' || page === 'paper') return;
    const c = el('div'); c.id = 'sx-cursor'; document.body.appendChild(c);
    let x = pointer.x, y = pointer.y;
    addEventListener('pointermove', () => c.classList.add('on'), { once: true, passive: true });
    document.addEventListener('mouseleave', () => c.classList.remove('on'));
    loops.add(() => { x += (pointer.x - x) * .12; y += (pointer.y - y) * .12; c.style.transform = `translate(${x}px,${y}px)`; });
  });

  /* =====================================================================
     4) Açılış: gün doğumu (oturum başına bir kez)
     ===================================================================== */
  safe('intro', () => {
    if (page !== 'home' || RM || store.get('sx-intro')) return;
    store.set('sx-intro', '1');
    const logoSrc = ($('.brand img') && $('.brand img').getAttribute('src')) || 'assets/logo.svg';
    const o = el('div', '', `<div class="sky"></div><div class="horizon"></div><div class="mark"><img src="${logoSrc}" alt=""><b>GÜNEŞ DİLİ</b><small>1 EK · 1 BİÇİM · 1 İŞLEV</small></div>`);
    o.id = 'sx-intro'; document.body.appendChild(o);
    document.documentElement.style.overflow = 'hidden';
    const close = () => { if (o.classList.contains('out')) return; o.classList.add('out'); document.documentElement.style.overflow = ''; setTimeout(() => o.remove(), 1300); };
    o.addEventListener('click', close); setTimeout(close, 2600);
  });

  /* =====================================================================
     5) Hero: 53 ışınlı canlı güneş
     ===================================================================== */
  safe('sun', () => {
    const wrap = $('.hero-logo-wrap'); if (!wrap) return;
    const cv = el('canvas'); cv.id = 'sx-sun'; wrap.prepend(cv);
    cv.setAttribute('role', 'img'); cv.setAttribute('aria-label', 'Güneş Dili: 53 Holder koması ışınları. Bir ışına dokunarak sesini çalın.');
    const hint = el('div', 'sx-sun-hint', '☀ bir ışına dokun · 53 koma'); ($('.hero') || wrap).appendChild(hint);
    const ctx = cv.getContext('2d');
    const DPR = Math.min(devicePixelRatio || 1, 2);
    let S = 0;
    const fit = () => { const r = cv.getBoundingClientRect(); S = Math.round(r.width * DPR); cv.width = S; cv.height = S; };
    fit(); addEventListener('resize', fit);
    const N = 53; const rays = Array.from({ length: N }, () => ({ boost: 0 }));
    const ripples = [];
    let visible = true, rot = 0, hover = -1, fired = false;
    new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(wrap);

    const idxAt = (cx, cy) => {
      const r = cv.getBoundingClientRect();
      const x = cx - (r.left + r.width / 2), y = cy - (r.top + r.height / 2);
      const dist = Math.hypot(x, y) / (r.width / 2);
      let a = Math.atan2(y, x) - rot; a = ((a % 6.2832) + 6.2832) % 6.2832;
      return { i: Math.round(a / 6.2832 * N) % N, dist };
    };
    cv.addEventListener('pointermove', e => { const h = idxAt(e.clientX, e.clientY); hover = h.dist > .2 && h.dist < 1.05 ? h.i : -1; });
    cv.addEventListener('pointerleave', () => { hover = -1; });
    cv.addEventListener('click', e => {
      const { i, dist } = idxAt(e.clientX, e.clientY); if (dist < .16) return;
      rays[i].boost = 1; ripples.push({ i, t: 0 });
      try { if (typeof playCommaSound === 'function') playCommaSound(i); } catch (err) {}
      try { if (typeof currentKomaIndex !== 'undefined') { currentKomaIndex = i; updateCommaCard(i); drawWheel(); } } catch (err) {}
      hint.classList.remove('show'); fired = true;
    });
    new IntersectionObserver(es => { if (es[0].isIntersecting && !fired) setTimeout(() => hint.classList.add('show'), 2400); }, { threshold: .4 }).observe(wrap);

    loops.add((t, dt) => {
      if (!visible) return;
      rot += dt * .045;
      const c = S / 2, base = S * .19; // logo yarıçapının hemen dışı
      ctx.clearRect(0, 0, S, S);
      // çekirdek ışıma
      const pulse = .5 + .5 * Math.sin(t * 1.3);
      let g = ctx.createRadialGradient(c, c, base * .6, c, c, S * .5);
      g.addColorStop(0, `rgba(255,200,40,${.22 + pulse * .1})`); g.addColorStop(.35, 'rgba(255,140,0,.07)'); g.addColorStop(1, 'rgba(255,100,0,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
      ctx.lineCap = 'round';
      for (let i = 0; i < N; i++) {
        const r = rays[i];
        r.boost *= Math.pow(.02, dt); // sönümlenme
        const a = i / N * 6.2832 + rot;
        const wave = (Math.sin(t * 1.15 + i * .72) + Math.sin(t * .47 - i * .31) + 2) / 4; // 0..1
        const major = i % 9 === 0;
        const hv = hover === i ? 1 : (hover >= 0 && Math.min(Math.abs(hover - i), N - Math.abs(hover - i)) === 1 ? .35 : 0);
        const len = S * (.045 + wave * .075 + (major ? .035 : 0) + hv * .075 + r.boost * .1);
        const r0 = base + S * .012, r1 = r0 + len;
        const x0 = c + Math.cos(a) * r0, y0 = c + Math.sin(a) * r0, x1 = c + Math.cos(a) * r1, y1 = c + Math.sin(a) * r1;
        const lg = ctx.createLinearGradient(x0, y0, x1, y1);
        const cy = hv || r.boost > .05;
        lg.addColorStop(0, cy ? 'rgba(0,229,255,.95)' : major ? 'rgba(255,229,127,.95)' : 'rgba(255,196,40,.8)');
        lg.addColorStop(1, cy ? 'rgba(0,229,255,0)' : 'rgba(255,140,0,0)');
        ctx.strokeStyle = lg; ctx.lineWidth = (major ? 3 : 1.7) * DPR * (1 + hv * .8 + r.boost);
        ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
        // uç parıltısı
        if (major || hv || r.boost > .05) { ctx.fillStyle = cy ? '#00E5FF' : '#FFE57F'; ctx.beginPath(); ctx.arc(x1, y1, (major ? 2.4 : 2) * DPR * (1 + r.boost), 0, 6.283); ctx.fill(); }
      }
      // ters yönde dönen dış nokta halkası
      const orR = S * .445;
      for (let i = 0; i < N; i++) {
        const a = -i / N * 6.2832 - rot * 1.6 + t * .02;
        const tw = .35 + .65 * (.5 + .5 * Math.sin(t * 2 + i));
        ctx.fillStyle = `rgba(255,215,0,${(.12 + tw * .4).toFixed(3)})`;
        ctx.beginPath(); ctx.arc(c + Math.cos(a) * orR, c + Math.sin(a) * orR, (i % 9 === 0 ? 2.6 : 1.4) * DPR, 0, 6.283); ctx.fill();
      }
      // yörünge çizgisi
      ctx.strokeStyle = 'rgba(255,215,0,.07)'; ctx.lineWidth = DPR; ctx.beginPath(); ctx.arc(c, c, orR, 0, 6.283); ctx.stroke();
      ctx.beginPath(); ctx.arc(c, c, base + S * .21, 0, 6.283); ctx.setLineDash([2 * DPR, 9 * DPR]); ctx.stroke(); ctx.setLineDash([]);
      // üzerine gelinen ışının etiketi
      if (hover >= 0) {
        const a = hover / N * 6.2832 + rot, rr = base + S * .24, lx = c + Math.cos(a) * rr, ly = c + Math.sin(a) * rr;
        const txt = `#${hover} · ${(440 * Math.pow(2, hover / 53)).toFixed(1)} Hz`;
        ctx.font = `600 ${11 * DPR}px 'IBM Plex Mono', monospace`; ctx.textBaseline = 'middle';
        const tw = ctx.measureText(txt).width + 16 * DPR; const bx = clamp(lx - tw / 2, 4, S - tw - 4), by = clamp(ly - 12 * DPR, 4, S - 28 * DPR);
        ctx.fillStyle = 'rgba(5,7,11,.88)'; ctx.strokeStyle = 'rgba(0,229,255,.7)'; ctx.lineWidth = DPR;
        ctx.beginPath(); ctx.roundRect ? ctx.roundRect(bx, by, tw, 24 * DPR, 6 * DPR) : ctx.rect(bx, by, tw, 24 * DPR); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#00E5FF'; ctx.textAlign = 'center'; ctx.fillText(txt, bx + tw / 2, by + 12.5 * DPR); ctx.textAlign = 'start';
      }
      // dalgacıklar
      for (let k = ripples.length - 1; k >= 0; k--) {
        const rp = ripples[k]; rp.t += dt * .9; if (rp.t > 1) { ripples.splice(k, 1); continue; }
        const a = rp.i / N * 6.2832 + rot, rr = base + S * (.05 + rp.t * .34);
        ctx.strokeStyle = `rgba(0,229,255,${(1 - rp.t) * .75})`; ctx.lineWidth = 2.2 * DPR * (1 - rp.t);
        ctx.beginPath(); ctx.arc(c, c, rr, a - .55, a + .55); ctx.stroke();
        ctx.strokeStyle = `rgba(255,215,0,${(1 - rp.t) * .35})`; ctx.beginPath(); ctx.arc(c, c, rr, 0, 6.283); ctx.stroke();
      }
    });
  });

  /* =====================================================================
     6) Hero: Mandelbrot arka planı (yavaş yakınlaşma, ping-pong)
     ===================================================================== */
  safe('fractal', () => {
    const hero = $('.hero'); if (!hero || RM) return;
    const cv = el('canvas'); cv.id = 'sx-fractal'; hero.prepend(cv);
    const W = 224, Hh = 128; cv.width = W; cv.height = Hh;
    const ctx = cv.getContext('2d'); const img = ctx.createImageData(W, Hh); const d = img.data;
    // paleti önceden hesapla (altın → amber → camgöbeği)
    const PAL = new Uint8ClampedArray(256 * 3);
    for (let i = 0; i < 256; i++) {
      const u = i / 255, w = .5 + .5 * Math.sin(u * 6.2832 * 1.5 - 1.2);
      PAL[i * 3] = 255 * (.15 + .85 * w); PAL[i * 3 + 1] = 215 * (.1 + .75 * w * (.4 + .6 * u)); PAL[i * 3 + 2] = 255 * (.35 * (1 - w) * u + .05);
    }
    const CX = -0.7453, CY = 0.1127, MAXIT = 90, LN2 = Math.log(2);
    let vis = true, acc = 0;
    new IntersectionObserver(es => { vis = es[0].isIntersecting; }).observe(hero);
    loops.add((t, dt) => {
      if (!vis) return; acc += dt; if (acc < .07) return; acc = 0;
      const z = .5 - .5 * Math.cos(t * .11);              // 0..1 ping-pong
      const scale = 3.4 * Math.exp(-z * Math.log(95));      // 95× yakınlaşma
      const asp = W / Hh;
      for (let py = 0; py < Hh; py++) {
        const y0 = CY + (py / Hh - .5) * scale;
        for (let px = 0; px < W; px++) {
          const x0 = CX + (px / W - .5) * scale * asp;
          let x = 0, y = 0, x2 = 0, y2 = 0, i = 0;
          while (i < MAXIT && x2 + y2 < 256) { y = 2 * x * y + y0; x = x2 - y2 + x0; x2 = x * x; y2 = y * y; i++; }
          const o = (py * W + px) * 4;
          if (i >= MAXIT) { d[o + 3] = 0; continue; }
          const sm = i + 1 - Math.log(Math.log(x2 + y2) / 2) / LN2;
          const k = ((sm * 7 + t * 14) % 255 + 255) % 255 | 0;
          d[o] = PAL[k * 3]; d[o + 1] = PAL[k * 3 + 1]; d[o + 2] = PAL[k * 3 + 2]; d[o + 3] = 255;
        }
      }
      ctx.putImageData(img, 0, 0);
    });
  });

  /* =====================================================================
     7) Hero: yazı makinesi
     ===================================================================== */
  safe('ticker', () => {
    const lead = $('.hero p.lead'); if (!lead) return;
    const box = el('div', 'sx-ticker'); const txt = el('span'); const caret = el('i'); box.append(txt, caret);
    lead.insertAdjacentElement('afterend', box);
    const lines = ['1 Ek = 1 Biçim = 1 İşlev', 'O(N) · Deterministik Sonlu Otomat (DFA)', '53 Holder Koması · 53 Ek Ailesi', 'Lean 4 · 0 sorry', 'Atatürk 1935 × Newton 1664', 'Biçimbilimsel belirsizlik: 0.000'];
    if (RM) { txt.textContent = lines[0]; return; }
    let li = 0, ci = 0, del = false, wait = 0;
    const step = () => {
      const s = lines[li];
      if (wait > 0) { wait--; return setTimeout(step, 60); }
      if (!del) { ci++; txt.textContent = s.slice(0, ci); if (ci >= s.length) { del = true; wait = 28; } }
      else { ci -= 2; if (ci <= 0) { ci = 0; del = false; li = (li + 1) % lines.length; wait = 4; } txt.textContent = s.slice(0, Math.max(0, ci)); }
      setTimeout(step, del ? 22 : 48 + Math.random() * 40);
    };
    setTimeout(step, 1600);
  });

  /* =====================================================================
     8) Sayaçlar
     ===================================================================== */
  safe('counters', () => {
    const items = $$('.stat-num'); if (!items.length) return;
    const GL = 'ΑΒΓΔΞΨΩ0123456789#%&';
    const run = (n) => {
      const final = n.dataset.final; const dur = 1700; const t0 = performance.now();
      const m = final.match(/^([\d.]+)(.*)$/);
      const f = (now) => {
        const p = clamp((now - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 4);
        if (final === '0.000') n.textContent = (1 - e).toFixed(3);
        else if (m && /^\d+$/.test(m[1])) n.textContent = Math.round(+m[1] * e) + m[2];
        else if (m) n.textContent = (+m[1] * e).toFixed((m[1].split('.')[1] || '').length) + m[2];
        else { // "1:1", "Lean 4": karışık harf çözülmesi
          let s = ''; for (let i = 0; i < final.length; i++) s += (i < final.length * e || final[i] === ' ' || final[i] === ':') ? final[i] : GL[(Math.random() * GL.length) | 0];
          n.textContent = s;
        }
        if (p < 1) requestAnimationFrame(f); else { n.textContent = final; n.classList.add('sx-pop'); }
      };
      requestAnimationFrame(f);
    };
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io.unobserve(e.target); if (!RM) run(e.target); } }), { threshold: .6 });
    items.forEach(n => { n.dataset.final = n.textContent.trim(); if (!RM) n.textContent = n.dataset.final === '0.000' ? '1.000' : n.dataset.final.replace(/[0-9]/g, '0'); io.observe(n); });
  });

  /* =====================================================================
     9) Kaydırma ile belirme (kademeli)
     ===================================================================== */
  safe('reveal', () => {
    let roots;
    if (page === 'home') roots = $$('.container > section, .container > footer');
    else if (page === 'wiki') roots = $$('.wiki-content > *, .wiki-hero');
    else if (page === 'paper') roots = $$('.paper-container > *, .card-header');
    else return;
    const targets = new Set();
    roots.forEach(sec => {
      // doğrudan çocuklar
      Array.from(sec.children).forEach((c, i) => { c.style.setProperty('--d', Math.min(i, 4) * 90 + 'ms'); targets.add(c); });
      // ızgara çocukları (derinlik ≤ 3)
      sec.querySelectorAll(':scope > * , :scope > * > *, :scope > * > * > *').forEach(p => {
        if (p.children.length < 2 || p.children.length > 24) return;
        const cs = getComputedStyle(p); if (cs.display !== 'grid' && !(cs.display === 'flex' && cs.flexWrap === 'wrap')) return;
        Array.from(p.children).forEach((c, i) => { c.style.setProperty('--d', Math.min(i, 8) * 80 + 'ms'); targets.add(c); });
      });
    });
    const list = Array.from(targets).filter(t => !t.closest('header.navbar-wrap') && !t.matches('.hero > *') && !t.classList.contains('hero'));
    // iç içe hedeflerde yalnızca en dış olanı değil, her ikisini de canlandır (iç olan gecikmeli)
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return; io.unobserve(e.target);
      e.target.classList.add('sx-in');
      setTimeout(() => e.target.classList.add('sx-done'), 1800);
    }), { threshold: .04, rootMargin: '0px 0px -6% 0px' });
    list.forEach(t => { t.classList.add('sx-r'); io.observe(t); });
    // güvenlik ağı: 6 sn sonra hâlâ gizli kalan ne varsa göster
    setTimeout(() => list.forEach(t => { if (!t.classList.contains('sx-in')) t.classList.add('sx-in', 'sx-done'); }), 9000);
    // hash ile gelen bağlantılar için hemen göster
    if (location.hash) { const t = $(location.hash); if (t) $$('.sx-r', t).concat([t]).forEach(x => x.classList.add('sx-in', 'sx-done')); }
  });

  /* =====================================================================
     10) Kart ışıldağı + eğim
     ===================================================================== */
  safe('cards', () => {
    if (!FINE || RM) return;
    const sel = '.stat-card, .archive-card, .lean-code-card, .info-card, .guide-card, .doc-card, .team-card, .usecase-card, .use-case-card, .feature-card, .callout';
    const cards = $$(sel);
    cards.forEach(c => {
      if (getComputedStyle(c).position === 'static') c.style.position = 'relative';
      const s = el('i', 'sx-spot'); c.prepend(s); c.classList.add('sx-has-spot');
      c.addEventListener('pointermove', e => {
        const r = c.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top;
        c.style.setProperty('--mx', x + 'px'); c.style.setProperty('--my', y + 'px');
        if (c.classList.contains('stat-card')) c.style.transform = `perspective(700px) rotateX(${((.5 - y / r.height) * 9).toFixed(2)}deg) rotateY(${((x / r.width - .5) * 11).toFixed(2)}deg) translateY(-4px)`;
      });
      if (c.classList.contains('stat-card')) { c.classList.add('sx-tilt'); c.addEventListener('pointerleave', () => { c.style.transform = ''; }); }
    });
    // Mıknatıslı düğmeler
    $$('.hero-cta .btn').forEach(b => {
      b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${((e.clientX - r.left - r.width / 2) * .14).toFixed(1)}px,${((e.clientY - r.top - r.height / 2) * .22 - 2).toFixed(1)}px)`; });
      b.addEventListener('pointerleave', () => { b.style.transform = ''; });
    });
  });

  /* =====================================================================
     11) Bölüm rayı (sağ kenar)
     ===================================================================== */
  safe('rail', () => {
    if (page !== 'home') return;
    const map = [['simulator', 'Simülatör'], ['gunes-lang-ide', 'Güneş-Lang'], ['lab-tam-motor', 'Laboratuvar'], ['koma-cemberi', '53 Koma'], ['ispatlar', 'Lean 4'], ['arsiv', 'Arşiv'], ['telemetri', 'Telemetri'], ['dokumanlar', 'Belgeler'], ['kurucu-deha', 'Kurucu'], ['ekip', 'Ekip']];
    const rail = el('nav'); rail.id = 'sx-rail'; rail.setAttribute('aria-label', 'Bölümler');
    const secs = map.map(([id, lb]) => ({ sec: document.getElementById(id), lb, id })).filter(x => x.sec);
    secs.forEach(x => { const a = el('a', '', `<span>${x.lb}</span><i></i>`); a.href = '#' + x.id; x.a = a; rail.appendChild(a); });
    document.body.appendChild(rail);
    let q = false;
    const upd = () => { q = false; const mid = innerHeight * .4; let cur = null; secs.forEach(x => { const r = x.sec.getBoundingClientRect(); if (r.top < mid && r.bottom > mid) cur = x; }); secs.forEach(x => x.a.classList.toggle('on', x === cur)); };
    addEventListener('scroll', () => { if (!q) { q = true; requestAnimationFrame(upd); } }, { passive: true }); upd();
  });

  /* =====================================================================
     12) Koma çarkı: ilk görünüşte tarama animasyonu
     ===================================================================== */
  safe('wheel', () => {
    const cv = document.getElementById('wheelCanvas'); if (!cv || RM) return;
    let done = false;
    new IntersectionObserver((es, io) => {
      if (!es[0].isIntersecting || done) return; done = true; io.disconnect();
      let home; try { home = currentKomaIndex; } catch (e) { return; }
      let i = 0; const total = 53; const t0 = performance.now(); let touched = false;
      cv.addEventListener('pointerdown', () => { touched = true; }, { once: true });
      const f = (now) => {
        if (touched) return;
        const p = clamp((now - t0) / 2200, 0, 1); const e = 1 - Math.pow(1 - p, 3);
        i = Math.round(e * (total + home)) % total;
        try { currentKomaIndex = i; updateCommaCard(i); drawWheel(); } catch (err) { return; }
        if (p < 1) requestAnimationFrame(f); else { try { currentKomaIndex = home; updateCommaCard(home); drawWheel(); } catch (err) {} }
      };
      requestAnimationFrame(f);
    }, { threshold: .5 }).observe(cv);
  });

  /* =====================================================================
     13) Simülatör çıktısı yenilenince parlasın
     ===================================================================== */
  safe('flash', () => {
    const out = document.getElementById('gdOutput'); if (!out) return;
    const box = out.closest('.output-panel, .interactive-panel, .result-panel') || out.parentElement;
    let tm; new MutationObserver(() => { box.classList.remove('sx-flash'); void box.offsetWidth; box.classList.add('sx-flash'); clearTimeout(tm); tm = setTimeout(() => box.classList.remove('sx-flash'), 1000); })
      .observe(out, { childList: true, characterData: true, subtree: true });
  });

  /* =====================================================================
     14) Görsel büyütme
     ===================================================================== */
  safe('lightbox', () => {
    if (page !== 'home') return;
    const imgs = $$('#telemetri img, .archive-showcase img, #arsiv img').filter(i => !/logo/i.test(i.src));
    if (!imgs.length) return;
    const lb = el('div', '', '<img alt="">'); lb.id = 'sx-lightbox'; document.body.appendChild(lb);
    const big = $('img', lb);
    imgs.forEach(i => { i.classList.add('sx-zoomable'); i.addEventListener('click', () => { big.src = i.currentSrc || i.src; big.alt = i.alt || ''; lb.classList.add('on'); }); });
    const off = () => lb.classList.remove('on');
    lb.addEventListener('click', off); addEventListener('keydown', e => { if (e.key === 'Escape') off(); });
  });

  /* =====================================================================
     15) Wiki: kod kopyalama + kenar çubuğu takibi
     ===================================================================== */
  safe('wiki', () => {
    if (page !== 'wiki') return;
    $$('.code-snippet, pre').forEach(pre => {
      pre.classList.add('sx-copy-host');
      const b = el('button', 'sx-copy', 'KOPYALA'); b.type = 'button';
      b.onclick = async () => { try { await navigator.clipboard.writeText(pre.innerText.replace(/KOPYALA|KOPYALANDI ✓/g, '').trim()); b.textContent = 'KOPYALANDI ✓'; b.classList.add('ok'); setTimeout(() => { b.textContent = 'KOPYALA'; b.classList.remove('ok'); }, 1600); } catch (e) { b.textContent = 'HATA'; } };
      pre.appendChild(b);
    });
    const links = $$('.sidebar-nav a[href^="#"]'); const secs = links.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    let q = false; const upd = () => { q = false; let cur = secs[0]; secs.forEach(s => { if (s.getBoundingClientRect().top < innerHeight * .35) cur = s; }); links.forEach(a => a.classList.toggle('sx-on', a.getAttribute('href') === '#' + (cur && cur.id))); };
    addEventListener('scroll', () => { if (!q) { q = true; requestAnimationFrame(upd); } }, { passive: true }); upd();
  });
})();
