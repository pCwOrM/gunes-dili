/**
 * Güneş-Lang Studio / IDE — Editör, Sözdizimi Renklendirici ve Arayüz Denetleyicisi
 * ==============================================================================
 * Bu dosya; senkronize satır numaralı renkli sözdizim vurgulayıcısını,
 * Web Audio API akustik rezonans sentezleyicisini, konsol terminalini ve
 * örnek program yükleyicisini yönetir.
 */

(function () {
  'use strict';

  // --- ÖRNEK PROGRAMLAR KÜTÜPHANESİ ---
  const EXAMPLES = {
    merhaba: `-- ☀️ GÜNEŞ-LANG: Merhaba Dünya ve Değişkenler
ag {
    werla "------------------------------------------------------------" ;
    werla "(*) GÜNEŞ-LANG v1.0 ÇALIŞTIRMA ORTAMI DEVREDE" ;
    werla "------------------------------------------------------------" ;

    -- Değişken Tanımlama (tan ... yi ...)
    tan kurucu yi "Gazi Mustafa Kemal Atatürk" ;
    tan yil yi 1935 ;
    tan teori yi "Güneş Dil Teorisi" ;
    tan holder_koma yi 53 ;

    werla "Tarihsel Bağlam : " kat kurucu kat " (" kat metin(yil) kat ")" ;
    werla "Kuram Adı       : " kat teori ;
    werla "Harmonik Koma   : " kat metin(holder_koma) kat "-TET Akustik Koma" ;

    -- Mantıksal ve Aritmetik İşlemler
    tan aktif yi dogru ;
    bakba (aktif es dogru) {
        werla "Durum           : Sistem Başarıyla Başlatıldı." ;
    }
}
`,

    fibonacci: `-- 🌀 GÜNEŞ-LANG: Özyinelemeli (Recursive) Fibonacci Serisi
ag {
    werla "==================================================" ;
    werla "   ÖZYİNELEMELİ FİBONACCİ REZONANS MOTORU         " ;
    werla "==================================================" ;

    tanim fib(n) {
        bakba (n kutukes 1) {
            wer n ;
        }
        wer fib(n kes 1) kat fib(n kes 2) ;
    }

    tan i yi 0 ;
    tan limit yi 10 ;

    donke (i kutukes limit) {
        tan f_val yi fib(i) ;
        werla "fib(" kat metin(i) kat ") = " kat metin(f_val) ;
        i yi i kat 1 ;
    }

    werla "--------------------------------------------------" ;
    werla "Hesaplama başarıyla tamamlandı (0 bellek kaybı)." ;
}
`,

    asal: `-- 🔢 GÜNEŞ-LANG: Asal Sayılar Eleği (Primes up to 40)
ag {
    werla "=== ASAL SAYILAR ELEĞİ VE SÜREÇ DÖNGÜSÜ ===" ;

    tanim asal_mi(sayi_val) {
        bakba (sayi_val kutuk 2) {
            wer yanlis ;
        }
        tan bolen yi 2 ;
        donke (bolen tarap bolen kutukes sayi_val) {
            bakba (sayi_val kalan bolen es 0) {
                wer yanlis ;
            }
            bolen yi bolen kat 1 ;
        }
        wer dogru ;
    }

    tan bulunan_asallar yi [] ;
    tan num yi 2 ;
    tan ust_sinir yi 40 ;

    donke (num kutukes ust_sinir) {
        bakba (asal_mi(num)) {
            ekle(bulunan_asallar, num) ;
        }
        num yi num kat 1 ;
    }

    werla "1 ile 40 arasındaki asallar:" ;
    werla bulunan_asallar ;
    werla "Toplam Bulunan Asal Adedi: " kat metin(boy(bulunan_asallar)) ;
}
`,

    werr_rezonans: `-- ⚡ GÜNEŞ-LANG: WERR 53-Hölder Akustik Rezonans & Yörünge Simülasyonu
ag {
    werla "=== WERR 53-HÖLDER AKUSTİK REZONANS MOTORU ===" ;

    tanim faz_hesapla(adim) {
        -- 53-TET koma fazı: (adım * 17) mod 53
        wer (adim tarap 17) kalan 53 ;
    }

    tan adim yi 1 ;
    tan hedef_koma yi 10 ;

    donke (adim kutukes hedef_koma) {
        tan koma_no yi faz_hesapla(adim) ;
        tan frekans yi 440 kat (koma_no tarap 8) ;
        
        werla "Adım " kat metin(adim) kat " -> Koma Fazı: " kat metin(koma_no) kat " / 53 (f ~ " kat metin(frekans) kat " Hz)" ;
        adim yi adim kat 1 ;
    }

    werla "Refleks Gecikmesi: < 0.1 ms (Nöromorfik BCI Eşzamanlı)" ;
}
`,

    diziler: `-- 📊 GÜNEŞ-LANG: Dinamik Dizi ve Metin Manipülasyonu
ag {
    werla "=== DİNAMİK DİZİ VE METİN İŞLEME ===" ;

    tan kokler yi ["ag", "tan", "yi", "wer", "donke"] ;
    werla "Başlangıç Kök Listesi: " kat metin(kokler) ;
    werla "Dizi Boyutu: " kat metin(boy(kokler)) ;

    -- Yeni kök ekleme
    ekle(kokler, "bakba") ;
    ekle(kokler, "werla") ;

    werla "Genişletilmiş Liste : " kat metin(kokler) ;
    werla "Yeni Boyut          : " kat metin(boy(kokler)) ;

    -- İndeks ile erişim
    werla "İlk Kök  (İndeks 0) : " kat kokler[0] ;
    werla "Üçüncü Kök (İndeks 2): " kat kokler[2] ;
    werla "Son Kök  (İndeks 6) : " kat kokler[6] ;
}
`
  };

  // --- SÖZDİZİMİ RENKLENDİRİCİSİ (SYNTAX HIGHLIGHTER) ---
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function highlightSyntax(code) {
    if (!code) return '';
    const tokenRegex = /(--[^\n]*)|("(?:\\[\s\S]|[^"])*"|'(?:\\[\s\S]|[^'])*')|(\b\d+(?:\.\d+)?\b)|(\b(?:ag|tan|yi|werla|wer|tanim|bakba|bakde|donke|dur|gec)\b)|(\b(?:dogru|yanlis)\b)|(\b(?:boy|uzunluk|ekle|zaman|sayi|metin|rezonans)\b)|(\b(?:kat|kes|tarap|bol|kalan|es|esde|buyuk|kutuk|buyukes|kutukes|wen|ve|weya|veya|de|degil)\b|[+\-*\/%=<>!&|]+)|([\{\}\[\]\(\)\;,])|([a-zA-Z_çğıöşüÇĞİÖŞÜ][a-zA-Z0-9_çğıöşüÇĞİÖŞÜ]*(?=\s*\())|([a-zA-Z_çğıöşüÇĞİÖŞÜ][a-zA-Z0-9_çğıöşüÇĞİÖŞÜ]*)|(\s+)|(.)/g;

    return code.replace(tokenRegex, (m, comment, str, num, kw, bool, builtin, op, punct, func, ident, ws, other) => {
      if (comment) return `<span class="token-comment">${escapeHtml(comment)}</span>`;
      if (str) return `<span class="token-string">${escapeHtml(str)}</span>`;
      if (num) return `<span class="token-number">${escapeHtml(num)}</span>`;
      if (kw) return `<span class="token-keyword">${escapeHtml(kw)}</span>`;
      if (bool) return `<span class="token-bool">${escapeHtml(bool)}</span>`;
      if (builtin) return `<span class="token-builtin">${escapeHtml(builtin)}</span>`;
      if (op) return `<span class="token-operator">${escapeHtml(op)}</span>`;
      if (punct) return `<span class="token-punct">${escapeHtml(punct)}</span>`;
      if (func) return `<span class="token-func">${escapeHtml(func)}</span>`;
      if (ident) return `<span class="token-ident">${escapeHtml(ident)}</span>`;
      if (ws) return ws;
      return escapeHtml(other);
    });
  }

  // --- WEB AUDIO API AKUSTİK REZONANS SENTEZLEYİCİSİ ---
  let audioCtx = null;
  let audioEnabled = false;

  function initAudio() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) audioCtx = new AudioContextClass();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  function playTone(freq, duration = 0.08) {
    if (!audioEnabled || !audioCtx) return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

      gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
      // Ses hatası sessizce geçilir
    }
  }

  // --- ARAYÜZ YÖNETİMİ ---
  document.addEventListener('DOMContentLoaded', () => {
    const codeInput = document.getElementById('codeInput');
    const highlightArea = document.getElementById('highlightArea');
    const lineNumbers = document.getElementById('lineNumbers');
    const runBtn = document.getElementById('runBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const exampleSelect = document.getElementById('exampleSelect');
    const audioToggle = document.getElementById('audioToggle');
    const consoleOutput = document.getElementById('consoleOutput');
    const statusText = document.getElementById('statusText');
    const statsTicks = document.getElementById('statsTicks');
    const statsDuration = document.getElementById('statsDuration');
    const statsKoma = document.getElementById('statsKoma');
    const statsFreq = document.getElementById('statsFreq');
    const dialSvg = document.getElementById('komaDialSvg');

    // 53-Hölder Koma Çarkını Çiz
    function drawKomaDial(activePhase = -1) {
      if (!dialSvg) return;
      dialSvg.innerHTML = '';
      const cx = 80;
      const cy = 80;
      const r = 68;

      // Merkez çember
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', cx);
      circle.setAttribute('cy', cy);
      circle.setAttribute('r', r);
      circle.setAttribute('fill', 'none');
      circle.setAttribute('stroke', 'rgba(255, 215, 0, 0.2)');
      circle.setAttribute('stroke-width', '1.5');
      dialSvg.appendChild(circle);

      // 53 Koma Noktası
      for (let k = 0; k < 53; k++) {
        const theta = (k / 53) * 2 * Math.PI - Math.PI / 2;
        const x = cx + r * Math.cos(theta);
        const y = cy + r * Math.sin(theta);

        const node = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        node.setAttribute('cx', x);
        node.setAttribute('cy', y);

        if (k === activePhase) {
          node.setAttribute('r', '4.5');
          node.setAttribute('fill', '#00E5FF');
          node.setAttribute('filter', 'drop-shadow(0 0 6px #00E5FF)');
        } else if (k % 9 === 0) {
          node.setAttribute('r', '2.8');
          node.setAttribute('fill', '#FFD700');
        } else {
          node.setAttribute('r', '1.5');
          node.setAttribute('fill', 'rgba(255, 215, 0, 0.45)');
        }
        dialSvg.appendChild(node);
      }

      // Merkez Göstergesi
      const centerDot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      centerDot.setAttribute('cx', cx);
      centerDot.setAttribute('cy', cy);
      centerDot.setAttribute('r', '14');
      centerDot.setAttribute('fill', 'rgba(10, 14, 24, 0.9)');
      centerDot.setAttribute('stroke', '#FFD700');
      centerDot.setAttribute('stroke-width', '1');
      dialSvg.appendChild(centerDot);

      const centerText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      centerText.setAttribute('x', cx);
      centerText.setAttribute('y', cy + 4);
      centerText.setAttribute('text-anchor', 'middle');
      centerText.setAttribute('fill', activePhase >= 0 ? '#00E5FF' : '#FFD700');
      centerText.setAttribute('font-size', '10px');
      centerText.setAttribute('font-family', 'IBM Plex Mono, monospace');
      centerText.setAttribute('font-weight', 'bold');
      centerText.textContent = activePhase >= 0 ? `K${activePhase}` : '53';
      dialSvg.appendChild(centerText);
    }

    drawKomaDial();

    // Senkronize Sözdizimi Renklendirme ve Satır Numaraları
    function updateEditor() {
      const code = codeInput.value;
      highlightArea.innerHTML = highlightSyntax(code) + '\n';

      const lineCount = code.split('\n').length;
      let linesHtml = '';
      for (let i = 1; i <= lineCount; i++) {
        linesHtml += `<div>${i}</div>`;
      }
      lineNumbers.innerHTML = linesHtml;

      // Scroll senkronizasyonu
      highlightArea.scrollTop = codeInput.scrollTop;
      highlightArea.scrollLeft = codeInput.scrollLeft;
      lineNumbers.scrollTop = codeInput.scrollTop;
    }

    codeInput.addEventListener('input', updateEditor);
    codeInput.addEventListener('scroll', () => {
      highlightArea.scrollTop = codeInput.scrollTop;
      highlightArea.scrollLeft = codeInput.scrollLeft;
      lineNumbers.scrollTop = codeInput.scrollTop;
    });

    // Tab Tuşu Desteği (4 Boşluk)
    codeInput.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const start = codeInput.selectionStart;
        const end = codeInput.selectionEnd;
        const value = codeInput.value;
        codeInput.value = value.substring(0, start) + '    ' + value.substring(end);
        codeInput.selectionStart = codeInput.selectionEnd = start + 4;
        updateEditor();
      } else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        // Ctrl + Enter ile Çalıştır
        e.preventDefault();
        runCode();
      }
    });

    // Örnek Yükleme
    function loadExample(key) {
      if (EXAMPLES[key]) {
        codeInput.value = EXAMPLES[key];
        updateEditor();
        clearConsole();
        logToConsole(`ℹ️ "${key}" örneği yüklendi. Çalıştırmak için 'Çalıştır (Ctrl+Enter)' butonuna basın.`, 'system');
      }
    }

    if (exampleSelect) {
      exampleSelect.addEventListener('change', (e) => {
        loadExample(e.target.value);
      });
    }

    // Konsol Yardımcıları
    function clearConsole() {
      consoleOutput.innerHTML = '';
    }

    function logToConsole(text, type = 'stdout') {
      const line = document.createElement('div');
      line.className = `console-line console-${type}`;
      line.textContent = text;
      consoleOutput.appendChild(line);
      consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }

    // Kod Çalıştırma Motoru
    function runCode() {
      initAudio();
      clearConsole();
      const code = codeInput.value.trim();

      if (!code) {
        logToConsole('UYARI: Çalıştırılacak kod bulunamadı.', 'error');
        return;
      }

      statusText.innerHTML = '<span class="status-running">● ÇALIŞTIRILIYOR...</span>';
      runBtn.disabled = true;

      // UI bloklanmaması için microtask ile yürüt
      setTimeout(() => {
        try {
          const result = GunesLang.run(code, {
            onOutput: (msg) => logToConsole(msg, 'stdout'),
            onAudio: (freq) => {
              if (audioEnabled) playTone(freq);
            },
            stepLimit: 150000,
            maxCallStack: 300
          });

          // Başarılı Sonuç
          statusText.innerHTML = '<span class="status-success">● BAŞARIYLA TAMAMLANDI</span>';
          statsTicks.textContent = result.totalTicks.toLocaleString();
          statsDuration.textContent = result.durationMs < 0.1 ? '< 0.1 ms' : `${result.durationMs.toFixed(2)} ms`;
          statsKoma.textContent = `${result.telemetry.activeNodes} / 53`;
          statsFreq.textContent = `${result.telemetry.dominantFreq.toFixed(1)} Hz`;

          drawKomaDial(result.telemetry.dominantPhase);

          logToConsole(`------------------------------------------------------------`, 'system');
          logToConsole(`[BİLGİ] Yürütme Tamamlandı | Süre: ${statsDuration.textContent} | Adım: ${result.totalTicks} ticks | VRAM: 0 Bytes`, 'system');
        } catch (err) {
          statusText.innerHTML = '<span class="status-error">● HATA</span>';
          logToConsole(err.message || String(err), 'error');
        } finally {
          runBtn.disabled = false;
        }
      }, 20);
    }

    runBtn.addEventListener('click', runCode);

    // Temizle Butonu
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        clearConsole();
        statusText.innerHTML = '<span class="status-idle">● HAZIR</span>';
        statsTicks.textContent = '0';
        statsDuration.textContent = '0.0 ms';
        statsKoma.textContent = '0 / 53';
        statsFreq.textContent = '440.0 Hz';
        drawKomaDial();
      });
    }

    // Kodu Kopyala
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(codeInput.value).then(() => {
          const original = copyBtn.innerHTML;
          copyBtn.innerHTML = '✓ Kopyalandı';
          setTimeout(() => { copyBtn.innerHTML = original; }, 1800);
        });
      });
    }

    // Kodu İndir (.gns)
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        const blob = new Blob([codeInput.value], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'program.gns';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    // Ses Aç/Kapat
    if (audioToggle) {
      audioToggle.addEventListener('click', () => {
        initAudio();
        audioEnabled = !audioEnabled;
        if (audioEnabled) {
          audioToggle.classList.add('active');
          audioToggle.innerHTML = '🎵 Akustik Sentez: <b>AÇIK</b>';
          playTone(440, 0.15); // Test tonu
        } else {
          audioToggle.classList.remove('active');
          audioToggle.innerHTML = '🎵 Akustik Sentez: <b>KAPALI</b>';
        }
      });
    }

    // URL Parametresi veya Varsayılan Örneği Yükle
    const hash = window.location.hash;
    if (hash && hash.startsWith('#code=')) {
      try {
        const decoded = decodeURIComponent(hash.substring(6));
        codeInput.value = decoded;
        updateEditor();
      } catch (e) {
        loadExample('merhaba');
      }
    } else {
      loadExample('merhaba');
    }
  });

})();
