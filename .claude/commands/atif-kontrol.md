---
description: Metindeki atıflarla kaynakçayı karşılaştırır, eksik, fazla veya hatalı kaynakları bulur.
argument-hint: [bölüm dosyası — boşsa tüm tez]
---

Kapsam: $ARGUMENTS (boşsa `bolumler/` içindeki tüm dosyalar)

1. Metindeki tüm `[@anahtar]` atıflarını topla ve `kaynakca/kaynaklar.bib` ile karşılaştır:
   - Metinde olup kaynakçada olmayanlar (hata)
   - Kaynakçada olup metinde hiç atıf yapılmayanlar
   - DOI'si veya zorunlu alanları (yazar, yıl, başlık, dergi, cilt, sayfa) eksik kayıtlar
2. Tüm `[KAYNAK GEREKLİ]` işaretlerini dosya ve satırıyla listele.
3. Atıf yapılmadan verilmiş gibi görünen olgusal iddiaları (sayısal değer, "literatürde ... gösterilmiştir" gibi) işaretle.
4. Sonuçları tablo halinde ver. Kaynakçaya künye uydurarak ekleme yapma.
