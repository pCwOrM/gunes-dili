"""
Güneş Dili Programlama Dili (Güneş-Lang) — Token Tanımları
===========================================================
Güneş Dili'nin kök-ek morfolojisinden türetilmiş deterministik sözcük birimleri.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # Değişmezler (Literals)
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()

    # Çekirdek Güneş Dili Anahtar Kelimeleri (Keywords)
    AG = auto()         # ag: Başlangıç / Ana Fonksiyon Girişi (Güneş / İlk Enerji)
    TAN = auto()        # tan: Tanımlama / Bellek tahsisi (let / var)
    YI = auto()         # yi: Ek-fiil atama operatörü (= / is)
    WERLA = auto()      # werla: Dışa aktarma / Ekrana basma (print / emit)
    WER = auto()        # wer: Değer döndürme (return / yield)
    TANIM = auto()      # tanim: İşlev tanımlama (function / def)
    BAKBA = auto()      # bakba: Koşul denetimi (if: bak- şart eki -ba ile)
    BAKDE = auto()      # bakde: Olumsuz koşul (else: bak- olumsuz eki -de ile)
    DONKE = auto()      # donke: Süreç döngüsü (while: dön- süre zarfı -ke/-ken ile)
    DUR = auto()        # dur: Döngü kesme (break / halt)
    GEC = auto()        # gec: Döngü atlama (continue / step)

    # İşleçler (Operators) — Hem fonotaktik kök hem sembolik destek
    KAT = auto()        # kat (+) : Toplama / Ekleme
    KES = auto()        # kes (-) : Çıkarma / Kesme
    TARAP = auto()      # tarap (*) : Çarpma (çarp- kökü)
    BOL = auto()        # bol (/) : Bölme
    KALAN = auto()      # kalan (%) : Modülo / Kalan
    
    ES = auto()         # es (==) : Eşitlik
    ESDE = auto()       # esde (!=) : Eşit değil (es- olumsuz -de ile)
    BUYUK = auto()      # buyuk (>) : Büyüktür
    KUTUK = auto()      # kutuk (<) : Küçüktür
    BUYUKES = auto()    # buyukes (>=) : Büyük veya eşit
    KUTUKES = auto()    # kutukes (<=) : Küçük veya eşit

    VE = auto()         # wen / ve (&&) : Mantıksal VE
    VEYA = auto()       # weya / veya (||) : Mantıksal VEYA
    DEGIL = auto()      # de / degil (!) : Mantıksal DEĞİL

    # Ayraçlar (Delimiters)
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    SEMICOLON = auto()  # ;
    COMMA = auto()      # ,
    ARROW = auto()      # ->

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int
    column: int

    def __repr__(self) -> str:
        if self.literal is not None:
            return f"Token({self.type.name}, '{self.lexeme}', {self.literal}, L{self.line}:{self.column})"
        return f"Token({self.type.name}, '{self.lexeme}', L{self.line}:{self.column})"


# Güneş Dili Anahtar Kelime Haritası (Kök + Ek Çözümlemesi)
KEYWORDS = {
    # Anahtar sözcükler
    "ag": TokenType.AG,
    "tan": TokenType.TAN,
    "yi": TokenType.YI,
    "werla": TokenType.WERLA,
    "wer": TokenType.WER,
    "tanim": TokenType.TANIM,
    "bakba": TokenType.BAKBA,
    "bakde": TokenType.BAKDE,
    "donke": TokenType.DONKE,
    "dur": TokenType.DUR,
    "gec": TokenType.GEC,

    # Boole değerleri
    "dogru": TokenType.BOOLEAN,
    "yanlis": TokenType.BOOLEAN,

    # Aritmetik sözcük işleçleri
    "kat": TokenType.KAT,
    "kes": TokenType.KES,
    "tarap": TokenType.TARAP,
    "bol": TokenType.BOL,
    "kalan": TokenType.KALAN,

    # Karşılaştırma sözcük işleçleri
    "es": TokenType.ES,
    "esde": TokenType.ESDE,
    "buyuk": TokenType.BUYUK,
    "kutuk": TokenType.KUTUK,
    "buyukes": TokenType.BUYUKES,
    "kutukes": TokenType.KUTUKES,

    # Mantık işleçleri
    "wen": TokenType.VE,
    "ve": TokenType.VE,
    "weya": TokenType.VEYA,
    "veya": TokenType.VEYA,
    "de": TokenType.DEGIL,
    "degil": TokenType.DEGIL,
}
