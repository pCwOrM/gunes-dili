"""
Güneş-Lang v1.0.0 — Kapsamlı Birim ve Entegrasyon Test Paketi
============================================================
Bu test paketi; sözcük birimleyici (Lexer), sözdizim ağacı (Parser),
çalışma zamanı (Interpreter), leksikal kapsam (Environment) ve
WERR 53-Hölder rezonans telemetrisini doğrular.
"""

import unittest
from gunes_lang.lexer import Lexer, LexerError
from gunes_lang.parser import Parser, ParserError
from gunes_lang.interpreter import Interpreter, RuntimeError
from gunes_lang.tokens import TokenType


class TestGunesLangLexer(unittest.TestCase):
    def test_keywords_and_operators(self):
        code = "ag tan yi werla wer tanim bakba bakde donke dur gec kat kes tarap bol kalan es"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [
            TokenType.AG, TokenType.TAN, TokenType.YI, TokenType.WERLA,
            TokenType.WER, TokenType.TANIM, TokenType.BAKBA, TokenType.BAKDE,
            TokenType.DONKE, TokenType.DUR, TokenType.GEC, TokenType.KAT,
            TokenType.KES, TokenType.TARAP, TokenType.BOL, TokenType.KALAN,
            TokenType.ES, TokenType.EOF
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_literals(self):
        code = '42 3.14 "merhaba gunes" \'tek tirnak\' dogru yanlis'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].literal, 42)
        self.assertEqual(tokens[1].literal, 3.14)
        self.assertEqual(tokens[2].literal, "merhaba gunes")
        self.assertEqual(tokens[3].literal, "tek tirnak")
        self.assertEqual(tokens[4].literal, True)
        self.assertEqual(tokens[5].literal, False)

    def test_comments(self):
        code = """
        -- Bu bir yorum satırıdır
        ag {
            tan x yi 10 ; -- satır içi yorum
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertNotIn(TokenType.KES, types)  # -- should not be parsed as minus
        self.assertIn(TokenType.AG, types)
        self.assertIn(TokenType.TAN, types)


class TestGunesLangInterpreter(unittest.TestCase):
    def _run(self, code: str):
        output = []
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter(output_callback=lambda s: output.append(s))
        interpreter.interpret(program)
        return output, interpreter

    def test_hello_world(self):
        code = """
        ag {
            werla "Merhaba Dünya" ;
        }
        """
        output, _ = self._run(code)
        self.assertEqual(output, ["Merhaba Dünya"])

    def test_arithmetic(self):
        code = """
        ag {
            tan a yi 10 kat 5 ;
            tan b yi 20 kes 8 ;
            tan c yi 4 tarap 3 ;
            tan d yi 15 bol 3 ;
            tan e yi 17 kalan 5 ;
            werla a ;
            werla b ;
            werla c ;
            werla d ;
            werla e ;
        }
        """
        output, _ = self._run(code)
        self.assertEqual(output, ["15", "12", "12", "5.0", "2"])

    def test_conditionals(self):
        code = """
        ag {
            tan x yi 10 ;
            bakba (x buyuk 5) {
                werla "buyuk" ;
            } bakde {
                werla "kucuk" ;
            }
        }
        """
        output, _ = self._run(code)
        self.assertEqual(output, ["buyuk"])

    def test_while_loop_and_scoping(self):
        code = """
        ag {
            tan sayac yi 0 ;
            tan toplam yi 0 ;
            donke (sayac kutuk 5) {
                toplam yi toplam kat sayac ;
                sayac yi sayac kat 1 ;
            }
            werla toplam ;
        }
        """
        output, _ = self._run(code)
        self.assertEqual(output, ["10"])  # 0+1+2+3+4 = 10

    def test_functions_and_recursion(self):
        code = """
        ag {
            tanim fib(n) {
                bakba (n kutukes 1) {
                    wer n ;
                }
                wer fib(n kes 1) kat fib(n kes 2) ;
            }
            werla fib(7) ;
        }
        """
        output, _ = self._run(code)
        self.assertEqual(output, ["13"])

    def test_arrays_and_builtins(self):
        code = """
        ag {
            tan dizi yi [10, 20, 30] ;
            ekle(dizi, 40) ;
            werla boy(dizi) ;
            werla dizi[1] ;
        }
        """
        output, _ = self._run(code)
        self.assertEqual(output, ["4", "20"])

    def test_telemetry(self):
        code = """
        ag {
            tan x yi 42 ;
            werla x ;
        }
        """
        _, interp = self._run(code)
        self.assertGreater(interp.telemetry.tick_count, 0)
        summary = interp.telemetry.summary()
        self.assertIn("GÜNEŞ DİLİ & WERR REZONANS TELEMETRİSİ", summary)
        self.assertIn("0 Bytes", summary)


if __name__ == "__main__":
    unittest.main()
