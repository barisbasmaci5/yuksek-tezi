#!/bin/bash
# projeler/SKT klasöründen çalıştırın: bash kod/word_uret.sh
set -e
cd "$(dirname "$0")/.."
python3 -I kod/rapor_uret.py
pandoc SKT_Proje_Raporu.md -o /tmp/skt_ham.docx --reference-doc=kod/referans.docx --resource-path=.
python3 -I kod/docx_duzelt.py /tmp/skt_ham.docx SKT_Proje_Raporu.docx
echo "SKT_Proje_Raporu.docx üretildi"
