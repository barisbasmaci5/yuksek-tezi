---
description: Bir makaleyi (PDF, DOI veya yapıştırılmış metin) özetler, kaynakçaya ekler ve not dosyası oluşturur.
argument-hint: <PDF yolu | DOI | "metin">
---

Kaynak: $ARGUMENTS

1. Kaynağı oku. DOI verildiyse künyeyi doi.org / Crossref üzerinden doğrula. Doğrulayamazsan dur ve söyle, künye uydurma.
2. `kaynakca/kaynaklar.bib` dosyasına BibTeX kaydı ekle (anahtar: soyadYılKelime). Aynı kaynak zaten varsa ekleme.
3. `kaynakca/notlar/<anahtar>.md` dosyasını şu başlıklarla yaz (Türkçe, kısa):
   - **Künye**
   - **Amaç**
   - **Malzeme ve yöntem** (karışım oranları, kür koşulları, test standartları)
   - **Temel bulgular** (sayısal değerleriyle, sayfa/şekil/çizelge numarası belirterek)
   - **Tezimle ilişkisi** — `CLAUDE.md` içindeki araştırma sorularından hangisine nasıl katkı sağlıyor
   - **Atıf yapılabilecek ifadeler** (kendi cümlenle, sayfa numarasıyla)
4. Yeni terimleri `notlar/terimler.md` dosyasına ekle.
5. Sonunda 3-4 satırlık özet ver.
