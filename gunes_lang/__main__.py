"""
Güneş-Lang ana giriş noktası (__main__)
Hem 'python -m gunes_lang' hem de klasör içinden doğrudan çalıştırmayı destekler.
"""
import os
import sys

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from gunes_lang.cli import main
else:
    from .cli import main

if __name__ == "__main__":
    main()
