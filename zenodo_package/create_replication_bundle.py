#!/usr/bin/env python3
"""
Güneş Dili Zenodo Replication Bundle Packager & Checksum Verifier
Generates zenodo_bundle_gunes_dili_v1.0.zip and SHA256SUMS.txt
"""

import os
import hashlib
import zipfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZENODO_DIR = os.path.abspath(os.path.dirname(__file__))

BUNDLE_NAME = "zenodo_bundle_gunes_dili_v1.0.zip"
BUNDLE_PATH = os.path.join(ZENODO_DIR, BUNDLE_NAME)

FILES_TO_PACK = [
    # Package metadata & sources
    (os.path.join(ZENODO_DIR, "Gunes_Dili_WERR_Preprint.tex"), "Gunes_Dili_WERR_Preprint.tex"),
    (os.path.join(ZENODO_DIR, "references.bib"), "references.bib"),
    (os.path.join(ZENODO_DIR, ".zenodo.json"), ".zenodo.json"),
    (os.path.join(ZENODO_DIR, "CITATION.cff"), "CITATION.cff"),
    (os.path.join(ZENODO_DIR, "ZENODO_YUKLEME_REHBERI.md"), "ZENODO_YUKLEME_REHBERI.md"),
    (os.path.join(ZENODO_DIR, "zenodo_description.html"), "zenodo_description.html"),
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
    print(f"[+] Bundle created successfully: {bundle_size} bytes")
    print(f"[+] SHA256: {bundle_hash}")

    # Generate SHA256SUMS.txt
    sums_file = os.path.join(ZENODO_DIR, "SHA256SUMS.txt")
    with open(sums_file, "w", encoding="utf-8") as f:
        f.write(f"{bundle_hash}  {BUNDLE_NAME}\n")
        for abs_path, rel_path in FILES_TO_PACK:
            if os.path.exists(abs_path):
                f.write(f"{sha256_file(abs_path)}  {os.path.basename(abs_path)}\n")
    print(f"[+] Written {sums_file}")

if __name__ == "__main__":
    build_bundle()
