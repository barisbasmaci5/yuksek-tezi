# Yüksek Lisans Tezi — Çalışma Kuralları

Bu repo bir yüksek lisans tezinin yazım ortamıdır (Malzeme / Kimya, Türkçe).
Her oturumun başında bu dosyayı ve `notlar/ilerleme.md` dosyasını oku.

## Tez bilgileri

> `[DOLDURULACAK]` yazan yerler öğrenciyle birlikte doldurulur. Boş alanı tahminle doldurma, sor.

- **Başlık:** [DOLDURULACAK]
- **Öğrenci:** [DOLDURULACAK]
- **Danışman:** [DOLDURULACAK]
- **Üniversite / Enstitü / Anabilim Dalı:** [DOLDURULACAK]
- **Konu (2-3 cümle):** [DOLDURULACAK]
- **Araştırma soruları / hipotezler:**
  1. [DOLDURULACAK]
- **Kullanılan malzemeler:** [DOLDURULACAK]
- **Kullanılan yöntemler:** [DOLDURULACAK — örn. XRD (Rietveld), FTIR, SEM-EDS, TGA/DTA, basınç/eğilme dayanımı]
- **Kaynak gösterme stili:** APA 7 (`sablon/apa.csl`) — enstitü numaralı stil isterse `sablon/ieee.csl` kullanılır.
- **Enstitü yazım kılavuzu:** [DOLDURULACAK — kılavuz `sablon/` içine konunca buraya özetle]

## Repo düzeni

| Yol | İçerik |
|-----|--------|
| `bolumler/` | Tez metni, bölüm başına bir Markdown dosyası. Dosya adındaki numara sırayı belirler. |
| `kaynakca/kaynaklar.bib` | Tek kaynakça (BibTeX). Metinde `[@anahtar]` ile atıf yapılır. |
| `kaynakca/notlar/` | Okunan her makale için özet notu (`anahtar.md`). |
| `veriler/` | Ham ve işlenmiş deney verileri (XRD, FTIR, mekanik test vb.). |
| `sekiller/` | Şekiller (PNG/SVG). |
| `sablon/` | Enstitü Word şablonu (`referans.docx`), yazım kılavuzu, CSL dosyaları. |
| `notlar/ilerleme.md` | Yapılanlar, açık işler, kararlar. Oturumlar arası hafıza. |
| `notlar/terimler.md` | Terim sözlüğü — tez boyunca aynı terim aynı şekilde yazılır. |
| `scripts/word-uret.sh` | Tüm bölümlerden `cikti/tez.docx` üretir. |

## Akademik dürüstlük (kesin kurallar)

1. **Kaynak uydurma.** Yalnızca `kaynaklar.bib` içinde olan ve DOI / yayıncı sayfasıyla doğrulanmış kaynaklara atıf yap. Bir iddiaya kaynak bulamazsan metne `[KAYNAK GEREKLİ]` yaz ve öğrenciye bildir.
2. **Veri uydurma.** Sayısal sonuç, tablo veya grafik yalnızca `veriler/` içindeki gerçek verilerden üretilir. Veri yoksa `[VERİ GEREKLİ: ...]` yaz.
3. **Bulgu yorumu öğrencinindir.** Bulgular ve Tartışma bölümünde yorum önerebilirsin, ama öneri olduğunu belirt. Son karar öğrencinin.
4. **İntihal yok.** Kaynaklardan uzun alıntıyı yeniden yazarak gizleme. Kendi cümlenle anlat ve atıf yap. Doğrudan alıntı tırnak içinde ve sayfa numarasıyla verilir.
5. **Yapay zekâ kullanımı** enstitünün politikasına göre beyan edilir. Bu öğrencinin sorumluluğudur, gerekiyorsa hatırlat.

## Yazım kuralları

- **Dil:** Türkçe akademik dil, edilgen ya da "bu çalışmada" yapısı. "Ben/biz" kullanılmaz.
- **Zaman:** Literatür için geniş/geçmiş zaman ("... bildirmiştir"), yapılan deneyler için geçmiş zaman ("... hazırlanmıştır").
- **Sayılar:** Ondalık ayırıcı **virgül** (12,5 MPa). Sayı ile birim arasında boşluk (25 °C, 28 gün). SI birimleri.
- **Kimyasal gösterim:** Çimento kimyası kısaltmaları ilk kullanımda açılır (C₃S, C-S-H, CH vb.) ve `notlar/terimler.md` dosyasına eklenir.
- **Tablolar "Çizelge"** olarak adlandırılır (enstitü aksini söylemezse). Şekil ve çizelgelere metinde mutlaka atıf yapılır.
- **Terim tutarlılığı:** Yeni terim kullanmadan önce `notlar/terimler.md` dosyasına bak. Yoksa ekle.
- Paragraf başına tek fikir. Çok uzun cümleleri böl.

## Çalışma şekli

- Öğrenci düz metin, not ya da madde işaretiyle gelebilir. Görev bunu akademik metne çevirmek ve geliştirmek. Anlamı değiştirme.
- Bir bölümde değişiklik yapınca sadece o bölümü düzenle. Tüm dosyayı baştan yazma.
- Her oturum sonunda `notlar/ilerleme.md` güncellenir, değişiklikler commit edilip push edilir.
- Maliyet önemli (sınırlı kredi). Alt ajan başlatma, gereksiz dosya okuma. Kısa ve odaklı çalış.
- Teze özel komutlar `.claude/commands/` içindedir: `/kaynak-ozetle`, `/bolum-yaz`, `/dil-kontrol`, `/atif-kontrol`, `/tutarlilik`, `/word-cikti`, `/kaydet`.
