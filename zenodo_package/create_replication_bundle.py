#!/usr/bin/env python3
"""
Güneş Dili Zenodo Replication Bundle Packager & Checksum Verifier
Generates zenodo_bundle_gunes_dili_v1.0.zip and SHA256SUMS.txt
Excludes internal upload guides (.zenodo.json, ZENODO_YUKLEME_REHBERI.md, zenodo_description.html)
Includes the research paper PDF and full reproduction codebase.
"""

import os
import hashlib
import zipfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZENODO_DIR = os.path.abspath(os.path.dirname(__file__))

BUNDLE_NAME = "zenodo_bundle_gunes_dili_v1.0.zip"
BUNDLE_PATH = os.path.join(ZENODO_DIR, BUNDLE_NAME)

PDF_NAME = "Gunes_Dili_Deterministic_Morphology_Lean4_WERR_Preprint.pdf"
PDF_PATH = os.path.join(ZENODO_DIR, PDF_NAME)

FILES_TO_PACK = [
    # Academic research paper manuscript & sources
    (PDF_PATH, PDF_NAME),
    (os.path.join(ZENODO_DIR, "Gunes_Dili_WERR_Preprint.tex"), "Gunes_Dili_WERR_Preprint.tex"),
    (os.path.join(ZENODO_DIR, "references.bib"), "references.bib"),
    (os.path.join(ZENODO_DIR, "CITATION.cff"), "CITATION.cff"),
    (os.path.join(ZENODO_DIR, "gunes_dili_preprint_summary.md"), "gunes_dili_preprint_summary.md"),
    # Core Repo Components
    (os.path.join(BASE_DIR, "README.md"), "README.md"),
    (os.path.join(BASE_DIR, "LICENSE"), "LICENSE"),
    (os.path.join(BASE_DIR, "proofs", "GunesDiliProof.lean"), "proofs/GunesDiliProof.lean"),
    (os.path.join(BASE_DIR, "proofs", "kanit_defteri.json"), "proofs/kanit_defteri.json"),
    (os.path.join(BASE_DIR, "proofs", "fraktal_sonuc.json"), "proofs/fraktal_sonuc.json"),
    (os.path.join(BASE_DIR, "tokenizer", "gunes_dil_v4.py"), "tokenizer/gunes_dil_v4.py"),
    (os.path.join(BASE_DIR, "tokenizer", "gunes_dil_model.json"), "tokenizer/gunes_dil_model.json"),
    (os.path.join(BASE_DIR, "tokenizer", "tdk_kokler.json"), "tokenizer/tdk_kokler.json"),
    (os.path.join(BASE_DIR, "engine", "gunes_dili.py"), "engine/gunes_dili.py"),
    (os.path.join(BASE_DIR, "engine", "gunes_dili_koordinat.json"), "engine/gunes_dili_koordinat.json"),
    (os.path.join(BASE_DIR, "engine", "gunes_dili_sozluk.json"), "engine/gunes_dili_sozluk.json"),
]

def sha256_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def build_bundle():
    print(f"[*] Packaging Güneş Dili Zenodo bundle: {BUNDLE_PATH}")
    with zipfile.ZipFile(BUNDLE_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for abs_path, rel_path in FILES_TO_PACK:
            if os.path.exists(abs_path):
                print(f"  + Adding {rel_path} ({os.path.getsize(abs_path)} bytes)")
                zipf.write(abs_path, arcname=rel_path)
            else:
                print(f"  ! Warning: {abs_path} not found!")

    bundle_hash = sha256_file(BUNDLE_PATH)
    bundle_size = os.path.getsize(BUNDLE_PATH)
    pdf_hash = sha256_file(PDF_PATH) if os.path.exists(PDF_PATH) else "N/A"
    print(f"[+] Bundle created successfully: {bundle_size} bytes")
    print(f"[+] Bundle SHA256: {bundle_hash}")
    print(f"[+] PDF SHA256: {pdf_hash}")

    # Generate SHA256SUMS.txt for all public deposit artifacts
    sums_file = os.path.join(ZENODO_DIR, "SHA256SUMS.txt")
    with open(sums_file, "w", encoding="utf-8") as f:
        f.write(f"{pdf_hash}  {PDF_NAME}\n")
        f.write(f"{bundle_hash}  {BUNDLE_NAME}\n")
        for abs_path, rel_path in FILES_TO_PACK:
            if os.path.exists(abs_path) and abs_path != PDF_PATH:
                f.write(f"{sha256_file(abs_path)}  {os.path.basename(abs_path)}\n")
    print(f"[+] Written {sums_file}")

if __name__ == "__main__":
    build_bundle()
