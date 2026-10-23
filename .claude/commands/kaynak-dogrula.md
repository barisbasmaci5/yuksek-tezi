---
description: Bir kaynak listesini kaynak doğrulayıcı ajanına doğrulatır ve doğrulananları kaynaklar.bib dosyasına ekletir.
argument-hint: <dosya yolu veya kaynak listesi> (boşsa kaynaklar.bib)
---

`kaynak-dogrulayici` ajanını çalıştır. Girdi: $ARGUMENTS (boşsa `kaynakca/kaynaklar.bib` dosyasındaki DOI'si eksik kayıtlar).

Liste 10 kaynaktan uzunsa ikiye bölüp iki ajanı paralel çalıştır; her biri `kaynaklar.bib` dosyasına yalnızca kendi kaynaklarını eklesin.

Bitince: sonuç tablosunu öğrenciye aktar, `kaynaklar.bib` dosyasındaki değişikliği kontrol et (`git diff kaynakca/kaynaklar.bib`) ve ❌ ile atıf-iddia uyumsuzluğu olanları `notlar/ilerleme.md` dosyasındaki açık işlere ekle.
