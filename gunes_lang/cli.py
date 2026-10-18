"""
Güneş Dili Programlama Dili (Güneş-Lang) — Komut Satırı Arayüzü ve REPL (CLI)
=============================================================================
Dosya çalıştırma, etkileşimli REPL kabuğu ve WERR telemetri raporlama arayüzü.
"""

import sys
import argparse
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

if __package__ is None or __package__ == "":
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from gunes_lang.lexer import Lexer, LexerError
    from gunes_lang.parser import Parser, ParserError
    from gunes_lang.interpreter import Interpreter, RuntimeError
else:
    from .lexer import Lexer, LexerError
    from .parser import Parser, ParserError
    from .interpreter import Interpreter, RuntimeError


BANNER = r"""
================================================================================
   (*)  GUNES-LANG v1.0.0 — AKADEMIK LAB PROGRAMLAMA DILI
   Deterministik Morfo-Semantik Cekirdek & WERR 53-Holder Rezonans Motoru
   Newton 1664 & Ataturk 1935 Bilimsel Mirasi Uzerine Insa Edilmistir
================================================================================
"""


def execute_source(source: str, show_telemetry: bool = False, interpreter: Interpreter = None) -> Interpreter:
    if interpreter is None:
        interpreter = Interpreter()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        program = parser.parse()

        interpreter.interpret(program)

        if show_telemetry:
            print("\n" + interpreter.telemetry.summary())

    except (LexerError, ParserError, RuntimeError) as e:
        print(f"\n[!] {e}", file=sys.stderr)
    except Exception as e:
        print(f"\n[!] Beklenmeyen Hata: {e}", file=sys.stderr)

    return interpreter


def run_file(filepath: str, show_telemetry: bool = False) -> None:
    if not os.path.exists(filepath):
        print(f"HATA: Dosya bulunamadı: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    execute_source(source, show_telemetry=show_telemetry)


def start_repl() -> None:
    print(BANNER)
    print("Etkileşimli Güneş-Lang Kabuğu (REPL). Çıkmak için 'cikis' veya Ctrl+C yazınız.\n")

    interpreter = Interpreter()

    while True:
        try:
            line = input("güneş> ")
            if line.strip().lower() in ("cikis", "exit", "quit"):
                print("Güneş dili oturumu kapatıldı. Esen kalın.")
                break
            if not line.strip():
                continue

            # Eğer sonu noktalı virgül veya blok ile bitmiyorsa kolaylık sağlayalım
            code = line
            if not (code.endswith(";") or code.endswith("}")):
                code = f"werla ({code}) ;"

            execute_source(code, show_telemetry=False, interpreter=interpreter)

        except (KeyboardInterrupt, EOFError):
            print("\nGüneş dili kabuğundan çıkıldı.")
            break


def main():
    parser = argparse.ArgumentParser(description="Güneş-Lang: Akademik Deterministik Programlama Dili Yorumlayıcısı")
    parser.add_argument("file", nargs="?", help="Çalıştırılacak Güneş-Lang (.gns) kaynak kodu")
    parser.add_argument("-t", "--telemetry", action="store_true", help="WERR 53-Hölder rezonans telemetrisini ve frekans histogramını göster")
    parser.add_argument("-c", "--code", type=str, help="Doğrudan tek satırlık Güneş-Lang kodu çalıştır")

    args = parser.parse_args()

    if args.code:
        execute_source(args.code, show_telemetry=args.telemetry)
    elif args.file:
        run_file(args.file, show_telemetry=args.telemetry)
    else:
        start_repl()


if __name__ == "__main__":
    main()
