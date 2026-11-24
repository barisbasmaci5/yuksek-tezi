# SKT Çalışması — Ambalaj tipinin raf ömrüne etkisi (Kalekim)

> Bu klasör tezden bağımsız bir iş projesidir. Tez kuralları (`CLAUDE.md`) burada geçerli değildir; yalnızca veri/kaynak dürüstlüğü kuralları uygulanır.

| Yol | İçerik |
|---|---|
| `SKT_Proje_Raporu.docx` | Proje raporu (taslak) |
| `SKT_Proje_Raporu.md` | Raporun Markdown kaynağı (`kod/rapor_uret.py` üretir) |
| `sekiller/` | XRD/FTIR grafikleri ve `gostergeler.json` (net pik alanları, FTIR göstergeleri) |
| `veri/xrd/`, `veri/ftir/` | Ham XRD (.rd) ve FTIR (.csv) dosyaları |
| `veri/kaynak/` | Önceki GR/M10 raporu, şartlandırma koşulları ve ürün listesi |
| `eski/` | Önceki raporun Markdown dönüşümü ve görselleri |
| `kod/` | `katalog.py` (numune–dosya eşlemesi), `analiz.py` (grafik+gösterge), `ozet.py`, `rapor_uret.py`, `word_uret.sh` |

Yeniden üretmek için (projeler/SKT içinden):

    python3 -I kod/analiz.py sekiller && python3 -I kod/ozet.py sekiller/gostergeler.json sekiller/OZET_XRD.png && bash kod/word_uret.sh
