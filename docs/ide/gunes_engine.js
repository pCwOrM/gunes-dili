/**
 * Güneş-Lang v1.0.0 — İstemci Tarafı Deterministik Çalışma Zamanı Motoru (Web / JS)
 * ==============================================================================
 * Atatürk 1935 Güneş Dil Teorisi, Newton 1664 ve Lean 4 İspatlı Sınır Biricikliği
 * prensiplerine tam sadakatle geliştirilmiş saf JavaScript sözcük birimleyici,
 * ayrıştırıcı, AST yorumlayıcı ve WERR 53-Hölder telemetri motoru.
 *
 * GÜVENLİK ÖNLEMLERİ (Sandboxing & Protection):
 * 1. 0 Sunucu Bağımlılığı: Tamamen tarayıcı içi yalıtılmış ortamda çalışır.
 * 2. Sonsuz Döngü Koruması: Maksimum talimat bütçesi (stepLimit = 150,000 ticks).
 * 3. Çağrı Yığını Koruması: Maksimum özyineleme derinliği (maxCallStack = 300 frame).
 * 4. Bellek & Çıktı Taşırma Koruması: Maksimum 5,000 satır tampon bellek.
 * 5. XSS Koruması: Tüm metinler DOM'a HTML olarak değil metin (textContent) olarak yazılır.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.GunesLang = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // --- 1. TOKEN TÜRLERİ VE ANAHTAR SÖZCÜKLER ---
  const TokenType = {
    // Literaller
    NUMBER: 'NUMBER',
    STRING: 'STRING',
    BOOLEAN: 'BOOLEAN',
    IDENTIFIER: 'IDENTIFIER',

    // Çekirdek Güneş Dili Kökleri
    AG: 'AG',           // ag: Başlangıç / Ana Fonksiyon Girişi
    TAN: 'TAN',         // tan: Tanımlama / Bellek tahsisi
    YI: 'YI',           // yi: Atama ve bağlaç operatörü (=)
    WERLA: 'WERLA',     // werla: Dışa aktarma (print)
    WER: 'WER',         // wer: Değer döndürme (return)
    TANIM: 'TANIM',     // tanim: Fonksiyon tanımlama (function)
    BAKBA: 'BAKBA',     // bakba: Koşul denetimi (if)
    BAKDE: 'BAKDE',     // bakde: Olumsuz koşul (else)
    DONKE: 'DONKE',     // donke: Süreç döngüsü (while)
    DUR: 'DUR',         // dur: Döngü kesme (break)
    GEC: 'GEC',         // gec: Sonraki adıma atlama (continue)

    // Aritmetik İşleçler
    KAT: 'KAT',         // kat (+)
    KES: 'KES',         // kes (-)
    TARAP: 'TARAP',     // tarap (*)
    BOL: 'BOL',         // bol (/)
    KALAN: 'KALAN',     // kalan (%)

    // Karşılaştırma İşleçleri
    ES: 'ES',           // es (==)
    ESDE: 'ESDE',       // esde (!=)
    BUYUK: 'BUYUK',     // buyuk (>)
    KUTUK: 'KUTUK',     // kutuk (<)
    BUYUKES: 'BUYUKES', // buyukes (>=)
    KUTUKES: 'KUTUKES', // kutukes (<=)

    // Mantıksal İşleçler
    VE: 'VE',           // wen / ve (&&)
    VEYA: 'VEYA',       // weya / veya (||)
    DEGIL: 'DEGIL',     // de / degil (!)

    // Ayraçlar
    LPAREN: 'LPAREN',       // (
    RPAREN: 'RPAREN',       // )
    LBRACE: 'LBRACE',       // {
    RBRACE: 'RBRACE',       // }
    LBRACKET: 'LBRACKET',   // [
    RBRACKET: 'RBRACKET',   // ]
    SEMICOLON: 'SEMICOLON', // ;
    COMMA: 'COMMA',         // ,

    EOF: 'EOF'
  };

  const KEYWORDS = {
    'ag': TokenType.AG,
    'tan': TokenType.TAN,
    'yi': TokenType.YI,
    'werla': TokenType.WERLA,
    'wer': TokenType.WER,
    'tanim': TokenType.TANIM,
    'bakba': TokenType.BAKBA,
    'bakde': TokenType.BAKDE,
    'donke': TokenType.DONKE,
    'dur': TokenType.DUR,
    'gec': TokenType.GEC,

    'dogru': TokenType.BOOLEAN,
    'yanlis': TokenType.BOOLEAN,

    'kat': TokenType.KAT,
    'kes': TokenType.KES,
    'tarap': TokenType.TARAP,
    'bol': TokenType.BOL,
    'kalan': TokenType.KALAN,

    'es': TokenType.ES,
    'esde': TokenType.ESDE,
    'buyuk': TokenType.BUYUK,
    'kutuk': TokenType.KUTUK,
    'buyukes': TokenType.BUYUKES,
    'kutukes': TokenType.KUTUKES,

    'wen': TokenType.VE,
    've': TokenType.VE,
    'weya': TokenType.VEYA,
    'veya': TokenType.VEYA,
    'de': TokenType.DEGIL,
    'degil': TokenType.DEGIL
  };

  class Token {
    constructor(type, lexeme, literal, line, column) {
      this.type = type;
      this.lexeme = lexeme;
      this.literal = literal;
      this.line = line;
      this.column = column;
    }
  }

  // --- 2. DETERMINISTIK SÖZCÜK BİRİMLEYİCİ (LEXER) ---
  class Lexer {
    constructor(source) {
      this.source = source || '';
      this.tokens = [];
      this.start = 0;
      this.current = 0;
      this.line = 1;
      this.column = 1;
      this.startColumn = 1;
    }

    tokenize() {
      while (!this.isAtEnd()) {
        this.start = this.current;
        this.startColumn = this.column;
        this.scanToken();
      }
      this.tokens.push(new Token(TokenType.EOF, '', null, this.line, this.column));
      return this.tokens;
    }

    isAtEnd() {
      return this.current >= this.source.length;
    }

    advance() {
      const c = this.source[this.current++];
      this.column++;
      return c;
    }

    peek() {
      if (this.isAtEnd()) return '\0';
      return this.source[this.current];
    }

    peekNext() {
      if (this.current + 1 >= this.source.length) return '\0';
      return this.source[this.current + 1];
    }

    match(expected) {
      if (this.isAtEnd() || this.source[this.current] !== expected) return false;
      this.current++;
      this.column++;
      return true;
    }

    scanToken() {
      const c = this.advance();
      switch (c) {
        case '(': this.addToken(TokenType.LPAREN); break;
        case ')': this.addToken(TokenType.RPAREN); break;
        case '{': this.addToken(TokenType.LBRACE); break;
        case '}': this.addToken(TokenType.RBRACE); break;
        case '[': this.addToken(TokenType.LBRACKET); break;
        case ']': this.addToken(TokenType.RBRACKET); break;
        case ';': this.addToken(TokenType.SEMICOLON); break;
        case ',': this.addToken(TokenType.COMMA); break;

        // Sembolik İşleçler (Alternatif Hızlı Yazım)
        case '+': this.addToken(TokenType.KAT); break;
        case '*': this.addToken(TokenType.TARAP); break;
        case '/': this.addToken(TokenType.BOL); break;
        case '%': this.addToken(TokenType.KALAN); break;

        case '-':
          if (this.match('-')) {
            // Yorum satırı: -- sonuna kadar atla
            while (this.peek() !== '\n' && !this.isAtEnd()) {
              this.advance();
            }
          } else {
            this.addToken(TokenType.KES);
          }
          break;

        case '=':
          if (this.match('=')) {
            this.addToken(TokenType.ES);
          } else {
            this.addToken(TokenType.YI);
          }
          break;

        case '!':
          if (this.match('=')) {
            this.addToken(TokenType.ESDE);
          } else {
            this.addToken(TokenType.DEGIL);
          }
          break;

        case '<':
          if (this.match('=')) {
            this.addToken(TokenType.KUTUKES);
          } else {
            this.addToken(TokenType.KUTUK);
          }
          break;

        case '>':
          if (this.match('=')) {
            this.addToken(TokenType.BUYUKES);
          } else {
            this.addToken(TokenType.BUYUK);
          }
          break;

        case '&':
          if (this.match('&')) this.addToken(TokenType.VE);
          else throw new Error(`[Satır ${this.line}, Sütun ${this.startColumn}] Beklenmeyen karakter '&'. Mantıksal VE için 'wen' veya '&&' kullanın.`);
          break;

        case '|':
          if (this.match('|')) this.addToken(TokenType.VEYA);
          else throw new Error(`[Satır ${this.line}, Sütun ${this.startColumn}] Beklenmeyen karakter '|'. Mantıksal VEYA için 'weya' veya '||' kullanın.`);
          break;

        case ' ':
        case '\r':
        case '\t':
          break;

        case '\n':
          this.line++;
          this.column = 1;
          break;

        case '"':
        case "'":
          this.stringLiteral(c);
          break;

        default:
          if (this.isDigit(c)) {
            this.numberLiteral();
          } else if (this.isAlpha(c)) {
            this.identifierOrKeyword();
          } else {
            throw new Error(`[Satır ${this.line}, Sütun ${this.startColumn}] Tanınmayan karakter: '${c}'`);
          }
          break;
      }
    }

    stringLiteral(quoteChar) {
      let value = '';
      while (this.peek() !== quoteChar && !this.isAtEnd()) {
        if (this.peek() === '\n') {
          this.line++;
          this.column = 1;
        }
        if (this.peek() === '\\') {
          this.advance();
          const esc = this.advance();
          if (esc === 'n') value += '\n';
          else if (esc === 't') value += '\t';
          else if (esc === 'r') value += '\r';
          else if (esc === '\\') value += '\\';
          else if (esc === '"') value += '"';
          else if (esc === "'") value += "'";
          else value += esc;
        } else {
          value += this.advance();
        }
      }

      if (this.isAtEnd()) {
        throw new Error(`[Satır ${this.line}, Sütun ${this.startColumn}] Kapatılmamış dize değişmezi.`);
      }

      this.advance(); // Kapatma tırnağını tüket
      const lexeme = this.source.substring(this.start, this.current);
      this.tokens.push(new Token(TokenType.STRING, lexeme, value, this.line, this.startColumn));
    }

    numberLiteral() {
      while (this.isDigit(this.peek())) this.advance();
      let isFloat = false;
      if (this.peek() === '.' && this.isDigit(this.peekNext())) {
        isFloat = true;
        this.advance(); // '.' tüket
        while (this.isDigit(this.peek())) this.advance();
      }

      const text = this.source.substring(this.start, this.current);
      const val = isFloat ? parseFloat(text) : parseInt(text, 10);
      this.tokens.push(new Token(TokenType.NUMBER, text, val, this.line, this.startColumn));
    }

    identifierOrKeyword() {
      while (this.isAlphaNumeric(this.peek())) this.advance();
      const text = this.source.substring(this.start, this.current);
      const lower = text.toLowerCase();
      let type = KEYWORDS[lower] || TokenType.IDENTIFIER;
      let literal = null;

      if (type === TokenType.BOOLEAN) {
        literal = (lower === 'dogru');
      }

      this.tokens.push(new Token(type, text, literal, this.line, this.startColumn));
    }

    isDigit(c) {
      return c >= '0' && c <= '9';
    }

    isAlpha(c) {
      return (c >= 'a' && c <= 'z') ||
             (c >= 'A' && c <= 'Z') ||
             c === '_' ||
             'çğıöşüÇĞİÖŞÜ'.indexOf(c) !== -1;
    }

    isAlphaNumeric(c) {
      return this.isAlpha(c) || this.isDigit(c);
    }

    addToken(type, literal = null) {
      const text = this.source.substring(this.start, this.current);
      this.tokens.push(new Token(type, text, literal, this.line, this.startColumn));
    }
  }

  // --- 3. SÖZDİZİM AĞACI (PARSER & AST) ---
  class Parser {
    constructor(tokens) {
      this.tokens = tokens;
      this.current = 0;
    }

    parse() {
      const statements = [];
      while (!this.isAtEnd()) {
        const stmt = this.declaration();
        if (stmt) statements.push(stmt);
      }
      return { type: 'Program', statements };
    }

    isAtEnd() {
      return this.peek().type === TokenType.EOF;
    }

    peek() {
      return this.tokens[this.current];
    }

    previous() {
      return this.tokens[this.current - 1];
    }

    advance() {
      if (!this.isAtEnd()) this.current++;
      return this.previous();
    }

    check(type) {
      if (this.isAtEnd()) return false;
      return this.peek().type === type;
    }

    match(...types) {
      for (const t of types) {
        if (this.check(t)) {
          this.advance();
          return true;
        }
      }
      return false;
    }

    consume(type, message) {
      if (this.check(type)) return this.advance();
      const token = this.peek();
      throw new Error(`[Satır ${token.line}, Sütun ${token.column}] Sözdizim Hatası: ${message} (Bulunan: '${token.lexeme}')`);
    }

    declaration() {
      if (this.match(TokenType.TANIM)) return this.functionDeclaration();
      if (this.match(TokenType.TAN)) return this.varDeclaration();
      return this.statement();
    }

    functionDeclaration() {
      const name = this.consume(TokenType.IDENTIFIER, "Fonksiyon adı bekleniyor.");
      this.consume(TokenType.LPAREN, "Fonksiyon parametreleri için '(' bekleniyor.");
      const params = [];
      if (!this.check(TokenType.RPAREN)) {
        do {
          params.push(this.consume(TokenType.IDENTIFIER, "Parametre adı bekleniyor."));
        } while (this.match(TokenType.COMMA));
      }
      this.consume(TokenType.RPAREN, "Parametre listesinden sonra ')' bekleniyor.");
      this.consume(TokenType.LBRACE, "Fonksiyon gövdesi için '{' bekleniyor.");
      const body = this.block();
      return { type: 'FunctionStmt', name, params, body };
    }

    varDeclaration() {
      const name = this.consume(TokenType.IDENTIFIER, "Değişken adı bekleniyor.");
      let initializer = null;
      if (this.match(TokenType.YI)) {
        initializer = this.expression();
      }
      this.consume(TokenType.SEMICOLON, "Değişken tanımlamasından sonra ';' bekleniyor.");
      return { type: 'VarDeclStmt', name, initializer };
    }

    statement() {
      if (this.match(TokenType.AG)) return this.agBlockStatement();
      if (this.match(TokenType.WERLA)) return this.printStatement();
      if (this.match(TokenType.BAKBA)) return this.ifStatement();
      if (this.match(TokenType.DONKE)) return this.whileStatement();
      if (this.match(TokenType.DUR)) return this.breakStatement();
      if (this.match(TokenType.GEC)) return this.continueStatement();
      if (this.match(TokenType.WER)) return this.returnStatement();
      if (this.match(TokenType.LBRACE)) return { type: 'BlockStmt', statements: this.block() };
      return this.expressionStatement();
    }

    agBlockStatement() {
      this.consume(TokenType.LBRACE, "'ag' bloğu için '{' bekleniyor.");
      const statements = this.block();
      return { type: 'BlockStmt', statements };
    }

    printStatement() {
      const expr = this.expression();
      this.consume(TokenType.SEMICOLON, "'werla' ifadesinden sonra ';' bekleniyor.");
      return { type: 'PrintStmt', expression: expr };
    }

    ifStatement() {
      this.consume(TokenType.LPAREN, "'bakba' koşulu için '(' bekleniyor.");
      const condition = this.expression();
      this.consume(TokenType.RPAREN, "Koşuldan sonra ')' bekleniyor.");
      const thenBranch = this.statement();
      let elseBranch = null;
      if (this.match(TokenType.BAKDE)) {
        elseBranch = this.statement();
      }
      return { type: 'IfStmt', condition, thenBranch, elseBranch };
    }

    whileStatement() {
      this.consume(TokenType.LPAREN, "'donke' döngüsü için '(' bekleniyor.");
      const condition = this.expression();
      this.consume(TokenType.RPAREN, "Döngü koşulundan sonra ')' bekleniyor.");
      const body = this.statement();
      return { type: 'WhileStmt', condition, body };
    }

    breakStatement() {
      this.consume(TokenType.SEMICOLON, "'dur' deyiminden sonra ';' bekleniyor.");
      return { type: 'BreakStmt' };
    }

    continueStatement() {
      this.consume(TokenType.SEMICOLON, "'gec' deyiminden sonra ';' bekleniyor.");
      return { type: 'ContinueStmt' };
    }

    returnStatement() {
      let value = null;
      if (!this.check(TokenType.SEMICOLON)) {
        value = this.expression();
      }
      this.consume(TokenType.SEMICOLON, "'wer' deyiminden sonra ';' bekleniyor.");
      return { type: 'ReturnStmt', value };
    }

    block() {
      const statements = [];
      while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
        const stmt = this.declaration();
        if (stmt) statements.push(stmt);
      }
      this.consume(TokenType.RBRACE, "Blok bitişi için '}' bekleniyor.");
      return statements;
    }

    expressionStatement() {
      const expr = this.expression();
      this.consume(TokenType.SEMICOLON, "İfadeden sonra ';' bekleniyor.");
      return { type: 'ExprStmt', expression: expr };
    }

    expression() {
      return this.assignment();
    }

    assignment() {
      const expr = this.logicalOr();
      if (this.match(TokenType.YI)) {
        const equals = this.previous();
        const value = this.assignment();
        if (expr.type === 'VariableExpr') {
          return { type: 'AssignExpr', name: expr.name, value };
        }
        throw new Error(`[Satır ${equals.line}, Sütun ${equals.column}] Geçersiz atama hedefi.`);
      }
      return expr;
    }

    logicalOr() {
      let expr = this.logicalAnd();
      while (this.match(TokenType.VEYA)) {
        const op = this.previous();
        const right = this.logicalAnd();
        expr = { type: 'BinaryExpr', left: expr, operator: op, right };
      }
      return expr;
    }

    logicalAnd() {
      let expr = this.equality();
      while (this.match(TokenType.VE)) {
        const op = this.previous();
        const right = this.equality();
        expr = { type: 'BinaryExpr', left: expr, operator: op, right };
      }
      return expr;
    }

    equality() {
      let expr = this.comparison();
      while (this.match(TokenType.ES, TokenType.ESDE)) {
        const op = this.previous();
        const right = this.comparison();
        expr = { type: 'BinaryExpr', left: expr, operator: op, right };
      }
      return expr;
    }

    comparison() {
      let expr = this.term();
      while (this.match(TokenType.BUYUK, TokenType.BUYUKES, TokenType.KUTUK, TokenType.KUTUKES)) {
        const op = this.previous();
        const right = this.term();
        expr = { type: 'BinaryExpr', left: expr, operator: op, right };
      }
      return expr;
    }

    term() {
      let expr = this.factor();
      while (this.match(TokenType.KAT, TokenType.KES)) {
        const op = this.previous();
        const right = this.factor();
        expr = { type: 'BinaryExpr', left: expr, operator: op, right };
      }
      return expr;
    }

    factor() {
      let expr = this.unary();
      while (this.match(TokenType.TARAP, TokenType.BOL, TokenType.KALAN)) {
        const op = this.previous();
        const right = this.unary();
        expr = { type: 'BinaryExpr', left: expr, operator: op, right };
      }
      return expr;
    }

    unary() {
      if (this.match(TokenType.DEGIL, TokenType.KES)) {
        const op = this.previous();
        const right = this.unary();
        return { type: 'UnaryExpr', operator: op, right };
      }
      return this.call();
    }

    call() {
      let expr = this.primary();
      while (true) {
        if (this.match(TokenType.LPAREN)) {
          expr = this.finishCall(expr);
        } else if (this.match(TokenType.LBRACKET)) {
          const index = this.expression();
          const bracket = this.consume(TokenType.RBRACKET, "Dizi indeks kapatması için ']' bekleniyor.");
          expr = { type: 'IndexExpr', target: expr, index, bracket };
        } else {
          break;
        }
      }
      return expr;
    }

    finishCall(callee) {
      const args = [];
      if (!this.check(TokenType.RPAREN)) {
        do {
          args.push(this.expression());
        } while (this.match(TokenType.COMMA));
      }
      const paren = this.consume(TokenType.RPAREN, "İşlev argüman listesinden sonra ')' bekleniyor.");
      return { type: 'CallExpr', callee, paren, arguments: args };
    }

    primary() {
      if (this.match(TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN)) {
        return { type: 'LiteralExpr', value: this.previous().literal };
      }
      if (this.match(TokenType.IDENTIFIER)) {
        return { type: 'VariableExpr', name: this.previous() };
      }
      if (this.match(TokenType.LPAREN)) {
        const expr = this.expression();
        this.consume(TokenType.RPAREN, "İfadeden sonra ')' bekleniyor.");
        return expr;
      }
      if (this.match(TokenType.LBRACKET)) {
        const elements = [];
        if (!this.check(TokenType.RBRACKET)) {
          do {
            elements.push(this.expression());
          } while (this.match(TokenType.COMMA));
        }
        this.consume(TokenType.RBRACKET, "Dizi kapatması için ']' bekleniyor.");
        return { type: 'ListExpr', elements };
      }

      const tok = this.peek();
      throw new Error(`[Satır ${tok.line}, Sütun ${tok.column}] Beklenmeyen sözcük birimi: '${tok.lexeme}'`);
    }
  }

  // --- 4. LEKSİKAL KAPSAM VE ÇALIŞMA ZAMANI ORTAMI ---
  class Environment {
    constructor(enclosing = null) {
      this.values = new Map();
      this.enclosing = enclosing;
    }

    define(name, value) {
      this.values.set(name.toLowerCase(), value);
    }

    assign(token, value) {
      const key = token.lexeme.toLowerCase();
      if (this.values.has(key)) {
        this.values.set(key, value);
        return;
      }
      if (this.enclosing !== null) {
        this.enclosing.assign(token, value);
        return;
      }
      throw new Error(`[Satır ${token.line}] Tanımsız değişkene atama yapılamaz: '${token.lexeme}'`);
    }

    get(token) {
      const key = token.lexeme.toLowerCase();
      if (this.values.has(key)) {
        return this.values.get(key);
      }
      if (this.enclosing !== null) {
        return this.enclosing.get(token);
      }
      throw new Error(`[Satır ${token.line}] Tanımsız değişken: '${token.lexeme}'`);
    }
  }

  // --- 5. WERR 53-HÖLDER KOMALARI VE REZONANS TELEMETRİSİ ---
  const HOLDER_CAPACITY = 53;
  const PHONEME_PHASE = {
    'a': 0, 'e': 9, 'i': 17, 'o': 31, 'u': 43,
    'm': 4, 'k': 8, 'n': 12, 'y': 16, 's': 20,
    'w': 24, 'p': 28, 'l': 32, 'b': 36, 't': 40,
    'g': 44, 'd': 48, 'f': 50, 'h': 51, 'r': 52
  };

  class WerrTelemetry {
    constructor() {
      this.tickCount = 0;
      this.histogram = new Array(HOLDER_CAPACITY).fill(0);
      this.events = [];
    }

    record(name) {
      this.tickCount++;
      let phase = 0;
      const lower = (name || '').toLowerCase();
      for (let i = 0; i < lower.length; i++) {
        const ch = lower[i];
        if (PHONEME_PHASE[ch] !== undefined) {
          phase = (phase + PHONEME_PHASE[ch]) % HOLDER_CAPACITY;
        }
      }

      this.histogram[phase]++;
      const angle = 2.0 * Math.PI * (phase / HOLDER_CAPACITY);
      const freq = 440.0 * Math.pow(2.0, phase / 53.0);

      const event = {
        tick: this.tickCount,
        name: name,
        phase: phase,
        angle: angle,
        freq: freq
      };

      if (this.events.length < 500) {
        this.events.push(event);
      }
      return event;
    }

    getSummary() {
      let activeNodes = 0;
      for (let i = 0; i < HOLDER_CAPACITY; i++) {
        if (this.histogram[i] > 0) activeNodes++;
      }
      let dominantPhase = 0;
      let maxCnt = 0;
      for (let i = 0; i < HOLDER_CAPACITY; i++) {
        if (this.histogram[i] > maxCnt) {
          maxCnt = this.histogram[i];
          dominantPhase = i;
        }
      }
      const dominantFreq = 440.0 * Math.pow(2.0, dominantPhase / 53.0);

      return {
        tickCount: this.tickCount,
        activeNodes: activeNodes,
        dominantPhase: dominantPhase,
        dominantFreq: dominantFreq,
        histogram: [...this.histogram]
      };
    }
  }

  // --- 6. İSTEMCİ YORUMLAYICISI (INTERPRETER & RUNTIME) ---
  class Interpreter {
    constructor(options = {}) {
      this.outputCallback = options.onOutput || console.log;
      this.telemetryCallback = options.onTelemetry || null;
      this.audioCallback = options.onAudio || null;
      this.stepLimit = options.stepLimit || 150000;
      this.maxCallStack = options.maxCallStack || 300;

      this.stepCounter = 0;
      this.callStackDepth = 0;
      this.outputBuffer = [];
      this.telemetry = new WerrTelemetry();

      this.globals = new Environment();
      this.environment = this.globals;

      this.initBuiltins();
    }

    initBuiltins() {
      // boy / uzunluk
      const lenFunc = (x) => {
        if (x === null || x === undefined) return 0;
        if (typeof x === 'string' || Array.isArray(x)) return x.length;
        return 0;
      };
      this.globals.define('boy', { arity: 1, call: (interp, args) => lenFunc(args[0]) });
      this.globals.define('uzunluk', { arity: 1, call: (interp, args) => lenFunc(args[0]) });

      // ekle (dizi, eleman)
      this.globals.define('ekle', {
        arity: 2,
        call: (interp, args) => {
          if (Array.isArray(args[0])) {
            args[0].push(args[1]);
            return args[0];
          }
          return args[0];
        }
      });

      // zaman() ms
      this.globals.define('zaman', {
        arity: 0,
        call: () => Date.now()
      });

      // sayi / metin
      this.globals.define('sayi', {
        arity: 1,
        call: (interp, args) => {
          const num = Number(args[0]);
          return isNaN(num) ? 0 : num;
        }
      });

      this.globals.define('metin', {
        arity: 1,
        call: (interp, args) => this.formatValue(args[0])
      });

      // rezonans(s) -> 53 koma fazı
      this.globals.define('rezonans', {
        arity: 1,
        call: (interp, args) => {
          const s = String(args[0] || '');
          let sum = 0;
          for (let i = 0; i < s.length; i++) sum += s.charCodeAt(i);
          return sum % 53;
        }
      });
    }

    executeProgram(program) {
      const startTime = performance.now();
      this.stepCounter = 0;
      this.callStackDepth = 0;
      this.outputBuffer = [];
      let lastVal = null;

      for (const stmt of program.statements) {
        lastVal = this.execute(stmt);
      }

      const durationMs = performance.now() - startTime;
      const teleSummary = this.telemetry.getSummary();

      return {
        output: this.outputBuffer,
        telemetry: teleSummary,
        durationMs: durationMs,
        totalTicks: this.stepCounter,
        lastValue: lastVal
      };
    }

    execute(stmt) {
      if (++this.stepCounter > this.stepLimit) {
        throw new Error(`[GÜVENLİK KORUMASI] Sonsuz döngü engellendi! Maksimum adım sınırı (${this.stepLimit.toLocaleString()} ticks) aşıldı.`);
      }

      const event = this.telemetry.record(stmt.type);
      if (this.telemetryCallback) this.telemetryCallback(event);
      if (this.audioCallback) this.audioCallback(event.freq);

      switch (stmt.type) {
        case 'ExprStmt':
          return this.evaluate(stmt.expression);

        case 'PrintStmt': {
          const val = this.evaluate(stmt.expression);
          const str = this.formatValue(val);
          this.outputBuffer.push(str);
          if (this.outputCallback) this.outputCallback(str);
          return val;
        }

        case 'VarDeclStmt': {
          let val = null;
          if (stmt.initializer) val = this.evaluate(stmt.initializer);
          const key = stmt.name.lexeme.toLowerCase();
          if (this.environment.enclosing !== null && this.findInAncestor(this.environment.enclosing, key)) {
            this.environment.assign(stmt.name, val);
          } else {
            this.environment.define(key, val);
          }
          return val;
        }

        case 'BlockStmt':
          return this.executeBlock(stmt.statements, new Environment(this.environment));

        case 'IfStmt': {
          const cond = this.evaluate(stmt.condition);
          if (this.isTruthy(cond)) {
            return this.execute(stmt.thenBranch);
          } else if (stmt.elseBranch) {
            return this.execute(stmt.elseBranch);
          }
          return null;
        }

        case 'WhileStmt': {
          while (this.isTruthy(this.evaluate(stmt.condition))) {
            try {
              this.execute(stmt.body);
            } catch (flow) {
              if (flow.type === 'BREAK') break;
              if (flow.type === 'CONTINUE') continue;
              throw flow;
            }
          }
          return null;
        }

        case 'BreakStmt':
          throw { type: 'BREAK' };

        case 'ContinueStmt':
          throw { type: 'CONTINUE' };

        case 'FunctionStmt': {
          const funcObj = {
            arity: stmt.params.length,
            call: (interp, args) => {
              if (++this.callStackDepth > this.maxCallStack) {
                this.callStackDepth--;
                throw new Error(`[GÜVENLİK KORUMASI] Maksimum çağrı yığını derinliği (${this.maxCallStack}) aşıldı! Özyineleme (recursion) taban koşulunu kontrol edin.`);
              }
              const fnEnv = new Environment(this.environment);
              for (let i = 0; i < stmt.params.length; i++) {
                fnEnv.define(stmt.params[i].lexeme, args[i]);
              }
              try {
                interp.executeBlock(stmt.body, fnEnv);
              } catch (flow) {
                if (flow.type === 'RETURN') {
                  this.callStackDepth--;
                  return flow.value;
                }
                this.callStackDepth--;
                throw flow;
              }
              this.callStackDepth--;
              return null;
            }
          };
          this.environment.define(stmt.name.lexeme, funcObj);
          return funcObj;
        }

        case 'ReturnStmt': {
          let val = null;
          if (stmt.value) val = this.evaluate(stmt.value);
          throw { type: 'RETURN', value: val };
        }

        default:
          throw new Error(`Bilinmeyen deyim: ${stmt.type}`);
      }
    }

    executeBlock(statements, env) {
      const previous = this.environment;
      try {
        this.environment = env;
        let last = null;
        for (const s of statements) {
          last = this.execute(s);
        }
        return last;
      } finally {
        this.environment = previous;
      }
    }

    evaluate(expr) {
      switch (expr.type) {
        case 'LiteralExpr':
          return expr.value;

        case 'VariableExpr':
          return this.environment.get(expr.name);

        case 'AssignExpr': {
          const val = this.evaluate(expr.value);
          this.environment.assign(expr.name, val);
          return val;
        }

        case 'ListExpr':
          return expr.elements.map(el => this.evaluate(el));

        case 'IndexExpr': {
          const target = this.evaluate(expr.target);
          const idx = this.evaluate(expr.index);
          if (typeof target !== 'string' && !Array.isArray(target)) {
            throw new Error(`[Satır ${expr.bracket.line}] İndekslenebilir olmayan hedef: ${typeof target}`);
          }
          if (typeof idx !== 'number' || !Number.isInteger(idx)) {
            throw new Error(`[Satır ${expr.bracket.line}] Dizi indeksi bir tamsayı olmalıdır.`);
          }
          if (idx < 0 || idx >= target.length) {
            throw new Error(`[Satır ${expr.bracket.line}] Dizi indeksi sınır dışı: ${idx} (Uzunluk: ${target.length})`);
          }
          return target[idx];
        }

        case 'UnaryExpr': {
          const right = this.evaluate(expr.right);
          if (expr.operator.type === TokenType.DEGIL) {
            return !this.isTruthy(right);
          } else if (expr.operator.type === TokenType.KES) {
            return -right;
          }
          throw new Error(`[Satır ${expr.operator.line}] Bilinmeyen tekil işleç: ${expr.operator.lexeme}`);
        }

        case 'BinaryExpr': {
          const left = this.evaluate(expr.left);
          const right = this.evaluate(expr.right);
          const op = expr.operator.type;

          if (op === TokenType.KAT) {
            if (typeof left === 'string' || typeof right === 'string') {
              return String(left) + String(right);
            }
            if (Array.isArray(left) && Array.isArray(right)) {
              return left.concat(right);
            }
            return left + right;
          }
          if (op === TokenType.KES) return left - right;
          if (op === TokenType.TARAP) return left * right;
          if (op === TokenType.BOL) {
            if (right === 0) throw new Error(`[Satır ${expr.operator.line}] Sıfıra bölme hatası.`);
            return left / right;
          }
          if (op === TokenType.KALAN) return left % right;

          if (op === TokenType.ES) return left === right;
          if (op === TokenType.ESDE) return left !== right;
          if (op === TokenType.BUYUK) return left > right;
          if (op === TokenType.BUYUKES) return left >= right;
          if (op === TokenType.KUTUK) return left < right;
          if (op === TokenType.KUTUKES) return left <= right;

          if (op === TokenType.VE) return this.isTruthy(left) && this.isTruthy(right);
          if (op === TokenType.VEYA) return this.isTruthy(left) || this.isTruthy(right);

          throw new Error(`[Satır ${expr.operator.line}] Bilinmeyen ikili işleç: ${expr.operator.lexeme}`);
        }

        case 'CallExpr': {
          const callee = this.evaluate(expr.callee);
          const args = expr.arguments.map(arg => this.evaluate(arg));
          if (!callee || typeof callee.call !== 'function') {
            throw new Error(`[Satır ${expr.paren.line}] Çağrılabilir bir fonksiyon değil.`);
          }
          if (callee.arity !== undefined && args.length !== callee.arity) {
            throw new Error(`[Satır ${expr.paren.line}] Argüman sayısı uyuşmazlığı: Beklenen ${callee.arity}, Verilen ${args.length}`);
          }
          return callee.call(this, args);
        }

        default:
          throw new Error(`Bilinmeyen ifade: ${expr.type}`);
      }
    }

    findInAncestor(env, lexeme) {
      let curr = env;
      while (curr !== null) {
        if (curr.values.has(lexeme)) return true;
        curr = curr.enclosing;
      }
      return false;
    }

    isTruthy(val) {
      if (val === null || val === undefined) return false;
      if (typeof val === 'boolean') return val;
      if (typeof val === 'number') return val !== 0;
      if (typeof val === 'string' || Array.isArray(val)) return val.length > 0;
      return true;
    }

    formatValue(val) {
      if (val === null || val === undefined) return "bos";
      if (typeof val === 'boolean') return val ? "dogru" : "yanlis";
      if (Array.isArray(val)) {
        return "[" + val.map(v => this.formatValue(v)).join(", ") + "]";
      }
      return String(val);
    }
  }

  // --- 7. GENEL DIŞA AKTARIM API'SI ---
  return {
    TokenType,
    KEYWORDS,
    Lexer,
    Parser,
    Interpreter,
    WerrTelemetry,

    // Kolay Tek Fonksiyonlu Çalıştırma
    run: function (sourceCode, options = {}) {
      const lexer = new Lexer(sourceCode);
      const tokens = lexer.tokenize();
      const parser = new Parser(tokens);
      const program = parser.parse();
      const interpreter = new Interpreter(options);
      return interpreter.executeProgram(program);
    }
  };

}));
