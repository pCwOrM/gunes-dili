#!/usr/bin/env python3
"""
Compile Güneş Dili Camera-Ready Research Paper PDF using Playwright & KaTeX
Outputs: Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf
"""

import os
import sys
from playwright.sync_api import sync_playwright

ZENODO_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(ZENODO_DIR, "gunes_dili_paper_template.html")
OUTPUT_PDF = os.path.join(ZENODO_DIR, "Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf")

def build_pdf():
    print(f"[*] Compiling camera-ready preprint PDF from: {HTML_PATH}")
    if not os.path.exists(HTML_PATH):
        print(f"[!] Error: {HTML_PATH} does not exist.")
        sys.exit(1)

    file_uri = "file:///" + HTML_PATH.replace("\\", "/")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_uri, wait_until="networkidle")
        
        # Wait for KaTeX to finish rendering
        try:
            page.wait_for_function("() => window.katexDone === true", timeout=15000)
            print("[+] KaTeX math rendering verified.")
        except Exception as e:
            print(f"[!] Note on KaTeX wait: {e}")
        
        page.wait_for_timeout(1000)

        print(f"[*] Printing A4 PDF to: {OUTPUT_PDF}")
        page.pdf(
            path=OUTPUT_PDF,
            format="A4",
            print_background=True,
            margin={
                "top": "12mm",
                "bottom": "14mm",
                "left": "14mm",
                "right": "14mm"
            },
            display_header_footer=True,
            header_template="<div></div>",
            footer_template='<div style="font-size: 7.5pt; font-family: -apple-system, sans-serif; width: 100%; text-align: center; color: #64748b;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
        )
        browser.close()

    if os.path.exists(OUTPUT_PDF):
        size_kb = os.path.getsize(OUTPUT_PDF) / 1024
        print(f"[+] Successfully generated: {os.path.basename(OUTPUT_PDF)} ({size_kb:.1f} KB)")
        return True
    else:
        print("[!] PDF generation failed.")
        return False

if __name__ == "__main__":
    build_pdf()
