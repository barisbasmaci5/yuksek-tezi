#!/usr/bin/env bash
# bolumler/*.md dosyalarını sırasıyla birleştirip cikti/tez.docx üretir.
# Enstitü şablonu sablon/referans.docx olarak konursa stiller oradan alınır.
set -euo pipefail

KOK="$(cd "$(dirname "$0")/.." && pwd)"
cd "$KOK"
mkdir -p cikti

ARGS=(metadata.yaml bolumler/*.md --citeproc --resource-path=.:sekiller -o cikti/tez.docx)
if [ -f sablon/referans.docx ]; then
  ARGS+=(--reference-doc=sablon/referans.docx)
fi

pandoc "${ARGS[@]}"
echo "Oluşturuldu: cikti/tez.docx"
