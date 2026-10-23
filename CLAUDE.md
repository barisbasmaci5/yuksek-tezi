# Yüksek Lisans Tezi — Çalışma Kuralları

Bu repo bir yüksek lisans tezinin yazım ortamıdır (Malzeme / Kimya, Türkçe).
Her oturumun başında bu dosyayı ve `notlar/ilerleme.md` dosyasını oku.

## Tez bilgileri

> `[DOLDURULACAK]` yazan yerler öğrenciyle birlikte doldurulur. Boş alanı tahminle doldurma, sor.

> Kaynak: `belgeler/BAP-proje-basvurusu.docx` (YTÜ BAP Yüksek Lisans projesi).

- **Başlık (çalışma başlığı, BAP):** Atık Yumurta Kabuğundan Kalsiyum Silikat Hidrat Sentezi ve Uygulama Alanının İncelenmesi
- **Öğrenci:** Barış BASMACI
- **Danışman:** Prof. Dr. Müge SARI YILMAZ
- **Üniversite / Enstitü / Anabilim Dalı:** Yıldız Teknik Üniversitesi, Fen Bilimleri Enstitüsü, Kimya Mühendisliği Anabilim Dalı
- **Konu:** Yumurta kabuğu atığından kalsinasyonla (950 °C) CaO elde edilir; sodyum metasilikat pentahidrat ile hidrotermal (otoklav) yöntemle C-S-H sentezlenir. En uygun C-S-H, CEM I 42,5N çimento harçlarında tohumlama (seeding) katkısı olarak denenir.
- **Araştırma soruları / hipotezler:**
  1. Yumurta kabuğundan elde edilen CaO ile yüksek C-S-H içerikli ürün sentezlenebilir mi? Ca/Si oranı (0,8–1,6), otoklav sıcaklığı (140–180 °C) ve süresi (24–72 sa) ürünü nasıl etkiler?
  2. Bu C-S-H, çimento hidratasyonunu hızlandırarak erken yaş dayanımını artırır mı? (BAP başarı ölçütü: referansa göre ≥ %10 dayanım artışı)
  3. Optimum katkı oranı nedir (%1–5)?
- **Kullanılan malzemeler:** Yumurta kabuğu (evsel atık), sodyum metasilikat pentahidrat, CEM I 42,5N, PCE dispersan (çimentonun kütlece %0,1'i), su/çimento = 0,35.
- **Kullanılan yöntemler:** Kalsinasyon, hidrotermal sentez; XRD-Rietveld, FTIR, TG/DTA (SEM-EDS ve izotermal kalorimetre BAP özetinde geçiyor, yapılıp yapılmadığı öğrenciye sorulmalı); TS EN 197-1'e göre 2, 7, 28 gün eğilme/basınç dayanımı; asetonla hidratasyon durdurma (2, 7, 14, 28 gün).
- **Kaynak gösterme stili:** APA 7 (`sablon/apa.csl`) — enstitü numaralı stil isterse `sablon/ieee.csl` kullanılır.
- **Enstitü şablonu:** `sablon/YTU_Tez_Sablon.docx` (YTÜ FBE, 24.02.2026). Şablonda **Üretken Yapay Zekâ (ÜYZ) kullanım beyanı** sayfası var; bu ortam kullanıldığı için "ÜYZ kullanılmışsa" beyanı seçilmeli.
- **Literatür:** BAP başvurusunda 20 kaynak var (henüz `kaynaklar.bib` içine aktarılmadı, DOI doğrulaması gerekli). Drive'da Elicit C-S-H literatür listesi (xlsx) mevcut.

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
- Maliyet önemli (sınırlı kredi). Gereksiz dosya okuma; kısa ve odaklı çalış.
- Teze özel komutlar `.claude/commands/` içindedir: `/kaynak-ozetle`, `/bolum-yaz`, `/dil-kontrol`, `/atif-kontrol`, `/tutarlilik`, `/word-cikti`, `/kaydet`, `/hakem-incele`, `/kaynak-dogrula`.

## Ajanlar

Yalnızca iki ajan vardır (`.claude/agents/`) ve yalnızca öğrenci istediğinde ya da ilgili komut çalıştırıldığında başlatılır. Başka alt ajan (ECC ajanları dahil) başlatma.

| Ajan | Model | Ne zaman |
|------|-------|----------|
| `hakem` | sonnet | Bir metin (özet, bildiri, bölüm) bittiğinde bağımsız değerlendirme için — `/hakem-incele` |
| `kaynak-dogrulayici` | haiku | Yeni kaynak listesi geldiğinde DOI doğrulaması ve `kaynaklar.bib` girişi için — `/kaynak-dogrula` |

Hakeme bu konuşmadaki bağlamı ya da kendi görüşünü verme; yalnızca dosya yolunu ve metin türünü ver.
