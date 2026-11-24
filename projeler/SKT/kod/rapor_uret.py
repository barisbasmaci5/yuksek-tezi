#!/usr/bin/env python3
"""SKT proje raporu: Markdown üretir (pandoc ile .docx'e çevrilir).
Kullanım: python3 -I kod/rapor_uret.py  (projeler/SKT klasöründen)"""
import json, re, math, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
G = json.load(open('sekiller/gostergeler.json', encoding='utf8'))
X, F = G['xrd'], G['ftir']

def fs(v, d=0):
    s = ('%.' + str(d) + 'f') % v
    return s.replace('.', ',')

# ---------- eski rapor (Groutart Rapid, Mastar 10) ----------
ESKI_BASLIK = {
    1: 'Groutart Rapid – 1 günlük XRD difraktogramları (Referans/12/20/30 µm)',
    2: 'Groutart Rapid – 1 günlük FTIR spektrumları',
    3: 'Groutart Rapid – 7 günlük XRD difraktogramları',
    4: 'Groutart Rapid – 7 günlük FTIR spektrumları',
    5: 'Groutart Rapid – 28 günlük XRD difraktogramları',
    6: 'Groutart Rapid – 28 günlük FTIR spektrumları',
    7: 'Mastar 10 – 1 günlük XRD difraktogramları (12/20/30 µm)',
    8: 'Mastar 10 – 1 günlük FTIR spektrumları',
    9: 'Mastar 10 – 7 günlük XRD difraktogramları',
    10: 'Mastar 10 – 7 günlük FTIR spektrumları',
    11: 'Mastar 10 – 28 günlük XRD difraktogramları',
    12: 'Mastar 10 – 28 günlük FTIR spektrumları',
}
def eski_bolum():
    s = open('eski/eski.md', encoding='utf8').read()
    s = '\n'.join(l for l in s.splitlines() if not l.startswith('Şekil -'))
    def img(m):
        n = int(m.group(1))
        return '\n\n![Şekil %d. %s](eski/media/image%d.%s){width=15.5cm}\n\n' % (n, ESKI_BASLIK[n], n, m.group(2))
    s = re.sub(r'!\[\]\(\./media/image(\d+)\.(png|jpeg)\)\{[^}]*\}', img, s)
    s = s.replace('**Groutart Rapid Ürünü ile Gerçekleştirilen Çalışmalar**', '### 4.1. Groutart Rapid')
    s = s.replace('**Mastar-10 Ürünü ile Gerçekleştirilen Çalışmalar**', '### 4.2. Mastar 10')
    return s

# ---------- çizelgeler ----------
ETK = {'Ref': 'Referans', '12': '12 µm', '20': '20 µm', '30': '30 µm', '12?': '12 µm*'}
YAS = {'K': 'Kuru harç', '1': '1 gün', '7': '7 gün', '28': '28 gün', 'K2': 'Kuru harç? (adlandırma şüpheli)', '7b': '7 gün (tekrar)', '7nd': '7 gün (durdurulmamış)'}
def xrd_cizelge(urun, no, ek=()):
    satir = ['| Yaş | Ambalaj | Ölçüm no | Etrenjit (9,1°) | Portlandit (18,0°) | Alit (51,7°) | Kalsit (29,4°) |',
             '|---|---|---|--:|--:|--:|--:|']
    for yas in ['K', '1', '7', '28'] + list(ek):
        for amb in ['Ref', '12', '20', '30']:
            v = X.get('%s|%s|%s' % (urun, yas, amb))
            if v: satir.append('| %s | %s | %s | %d | %d | %d | %d |' % (YAS[yas], ETK[amb], v['no'], v['E'], v['P'], v['A'], v['Cc']))
    return '\n'.join(satir) + '\n\n: Çizelge %d. %s XRD net pik alanları (k.b.; doğrusal taban çizgisi üzerindeki alan, numune yüksekliği kayması düzeltilmiş)\n' % (no, urun)
def ftir_cizelge(urun, no, ek=()):
    satir = ['| Yaş | Ambalaj | Ölçüm no | n | Ca(OH)₂ 3640 cm⁻¹ (mAbs) | O–H bandı alanı (k.b.) | Si–O bandı minimumu (cm⁻¹) |',
             '|---|---|---|--:|--:|--:|--:|']
    for yas in ['K', '1', '7', '28'] + list(ek):
        for amb in ['Ref', '12', '12?', '20', '30']:
            v = F.get('%s|%s|%s' % (urun, yas, amb))
            if not v: continue
            def r(k, d=0):
                m, a, b = v[k]
                return fs(m, d) if v['n'] == 1 else '%s (%s–%s)' % (fs(m, d), fs(a, d), fs(b, d))
            satir.append('| %s | %s | %s | %d | %s | %s | %s |' % (YAS[yas], ETK[amb], v['no'], v['n'], r('OH3640', 1), r('H2O_alan'), r('SiO_min')))
    return '\n'.join(satir) + '\n\n: Çizelge %d. %s FTIR göstergeleri (tekrar ölçümlerin ortalaması; parantez içinde en küçük–en büyük değer)\n' % (no, urun)

def sek(no, dosya, baslik):
    return '\n![Şekil %d. %s](sekiller/%s){width=16cm}\n' % (no, baslik, dosya)

# oranlar (metinde kullanılan)
def x(u, y, a, k): return X['%s|%s|%s' % (u, y, a)][k]
def yuzde(a, b): return fs(100 * (a - b) / b, 0)

MD = []
A = MD.append
A('''---
title: "Ambalaj Tipinin Kalekim Ürünlerinin Raf Ömrüne (SKT) Etkisi"
subtitle: "XRD ve FTIR Bulgularına Dayalı Proje Raporu — TASLAK"
date: "Kasım 2026"
lang: tr-TR
---

> **Taslak notu.** `[DOĞRULANACAK]` ve `[VERİ GEREKLİ]` ile işaretli yerler proje ekibince tamamlanmalıdır. Bulgular bölümündeki yorumlar veriye dayalı önerilerdir; nihai değerlendirme proje sorumlusuna aittir.

# 1. Amaç ve Kapsam

Bu çalışmada, Kalekim çimento esaslı kuru karışım ürünlerinin farklı film kalınlığına sahip ambalajlara aktarılmasının ürünün raf ömrü (son kullanma tarihi, SKT) üzerindeki etkisi incelenmiştir. Ürünler 12 µm, 20 µm ve 30 µm iç film kalınlığına sahip üç farklı torba tipine doldurulmuş, hızlandırılmış iklim şartlandırmasına tabi tutulmuş ve şartlandırma sonrasında kuru harç ile 1, 7 ve 28 günlük hidrate numuneler XRD ve FTIR yöntemleriyle karakterize edilmiştir. Mevcut (referans) ambalajdaki ürün karşılaştırma numunesi olarak kullanılmıştır.

Çalışmanın temel sorusu, ambalaj değişikliğinin depolama süresince ürüne nem girişini artırıp artırmadığı ve bunun sonucunda bağlayıcı fazlarda ön hidratasyon (prehidratasyon) ve hidratasyon kinetiğinde gecikme oluşup oluşmadığıdır. Bu rapor Groutart Rapid, Mastar 10, Macunart, İzolatex Plus ve Technopool ürünlerine ait mineralojik bulguları kapsamaktadır. Izoseal ve Izostop ürünlerine ait veri bu rapora ulaşmamıştır [VERİ GEREKLİ].

# 2. Literatür Özeti

**Ön hidratasyon ve depolama nemi.** Portland çimentosu depolama sırasında ortam nemiyle temas ettiğinde yüzeyde sınırlı bir hidratasyon (ön hidratasyon) gerçekleşir. Whittaker ve diğerleri (2013), ince tabakalar hâlinde %60 ve %85 bağıl nemde bekletilen CEM I 42,5R çimentosunda %60 bağıl nemin dayanım gelişimini ihmal edilebilir düzeyde etkilediğini, ancak işlenebilirliği azaltıp priz süresini uzattığını bildirmiştir. Aynı çalışmada %85 bağıl nemde basınç dayanımının, özellikle erken yaşta, belirgin biçimde düştüğü ve işlenebilirlik kaybının arttığı rapor edilmiştir.

**Fazların nem duyarlılığı.** Dubina ve diğerleri (2011), su buharı sorpsiyon terazisiyle klinker fazlarını ayrı ayrı incelemiş ve serbest kireç (CaO) ile C₃A'nın su buharına karşı en reaktif bileşenler olduğunu göstermiştir. Ortorombik C₃A'nın yaklaşık %55 bağıl nemden itibaren önemli miktarda su bağladığı, C₃S ve C₂S'de sorpsiyonun ancak yaklaşık %74 bağıl nemde başladığı ve miktarının düşük kaldığı, kalsiyum sülfatların ise suyu ağırlıklı olarak fiziksel yolla tuttuğu bildirilmiştir. Bu bulgular, ambalajın nem bariyeri özelliğinin özellikle alüminat ve sülfat fazlarının korunmasında belirleyici olabileceğine işaret etmektedir. Ambalaj tiplerini kuru harç raf ömrü açısından doğrudan karşılaştıran kontrollü bir çalışmaya bu literatür taramasında ulaşılamamıştır [KAYNAK GEREKLİ].

**XRD ile hidratasyonun izlenmesi.** Toz XRD ile kristalin hidratasyon ürünleri (etrenjit, portlandit, AFm fazları) ve reaksiyona girmemiş klinker fazları (alit, belit) izlenebilir; C-S-H jeli amorf olduğundan XRD'de yalnızca geniş bir zemin yükselmesi olarak görülür (Scrivener ve diğerleri, 2016). Hidratasyonun belirli bir yaşta durdurulması için RILEM TC-238 SCM önerisi, izopropanol ile solvent değişimini hidrat fazlarını en iyi koruyan yöntem olarak belirlemiştir (Snellings ve diğerleri, 2018).

**FTIR ile hidratasyonun izlenmesi.** Ylmén ve diğerleri (2009), FTIR spektroskopisiyle erken yaş hidratasyonunda sülfat bantlarının ilk saniyelerde yeniden düzenlendiğini, yaklaşık 60 dakikadan sonra silikat polimerleşmesine ait işaretlerin ortaya çıktığını ve 970–1100 cm⁻¹ aralığındaki yükselmenin C-S-H oluşumunu gösterdiğini bildirmiştir. Yu ve diğerleri (1999), sentetik C-S-H'nin ana Si–O bantlarını 950–1100, 810–830 ve 660–670 cm⁻¹ aralıklarında tanımlamış ve bant konumlarının Ca/Si oranıyla sistematik olarak kaydığını göstermiştir. Bu nedenle Si–O gerilme bandının anhidrit alite özgü ~920 cm⁻¹ konumundan ~960–1000 cm⁻¹'e kayması hidratasyonun ilerlemesinin göstergesi olarak kullanılmıştır.

# 3. Malzeme ve Yöntem

## 3.1. Ürünler ve ambalajlar

Çalışmada kullanılan torba tipleri ve ürün–ambalaj eşleşmeleri Çizelge 1'de verilmiştir.

| Torba tipi | İç film kalınlığı | Numune kodu |
|---|---|---|
| Mapei Adesilex P7 torbası | 12 µm | 12 µm |
| Mapei boş torba | 20 µm | 20 µm |
| Weber torbası (weberfloor LVL 1040) | 30 µm | 30 µm |
| Ürünün mevcut Kalekim ambalajı [DOĞRULANACAK] | [VERİ GEREKLİ] | Referans |

: Çizelge 1. Kullanılan ambalaj tipleri (Ürün Listesi dosyasına göre)

| Ürün | Referans | 12 µm | 20 µm | 30 µm |
|---|:-:|:-:|:-:|:-:|
| Groutart Rapid | ✓ | ✓ | ✓ | ✓ |
| Mastar 10 | – | ✓ | ✓ | ✓ |
| Macunart | ✓ | ✓ | ✓ | ✓ |
| İzolatex Plus (toz bileşen) | ✓ | ✓ | ✓ | ✓ |
| Technopool | ✓ | ✓ | ✓ | – |

: Çizelge 2. Ürün–ambalaj test matrisi

## 3.2. Şartlandırma

Kraft torbalardaki ürünler için soğuk ve sıcak iklim şartlandırma döngüleri tanımlanmıştır (Çizelge 3). Her iki döngü de 24 saatlik bir programdan oluşmakta olup 45 günlük döngü uygulamasının 2 yıllık depolamaya karşılık geldiği kabul edilmiştir. Soğuk döngü Moskova (Rusya) ve Fransa'nın soğuk bölgeleri, sıcak döngü ise Nairobi (Kenya), Duhok (Irak) ve Trablus (Libya) iklim verileri esas alınarak oluşturulmuştur. Ürün Listesi dosyasına göre soğuk döngü (kraft) 06.03.2026–21.04.2026 tarihleri arasında uygulanmıştır. Sıcak döngünün uygulama tarihleri ve hangi ürünlerin hangi döngüye tabi tutulduğu dosyalarda yer almamaktadır [DOĞRULANACAK].

| Soğuk döngü adımı | Bağıl nem | Yağış | Süre (sa) | | Sıcak döngü adımı | Bağıl nem | Yağış | Süre (sa) |
|---|--:|---|--:|---|---|--:|---|--:|
| −15 °C | %90 | yok | 5 | | 0 °C | %65 | yok | 3 |
| −5 °C | %90 | yok | 5 | | 5 °C | %75 | yok | 4 |
| 0 °C | %85 | yok | 4 | | 15 °C | %75 | 70 mm | 4 |
| 10 °C | %80 | 70 mm | 5 | | 35 °C | %70 | yok | 5 |
| 20 °C | %75 | 90 mm | 5 | | 45 °C | %80 | yok | 4 |
| | | | | | 45 °C | %20 | yok | 4 |
| **Toplam** | | | **24** | | **Toplam** | | | **24** |

: Çizelge 3. Kraft torbalar için soğuk ve sıcak şartlandırma döngüleri (Şartlandırma Koşulları dosyası)

Jüt torbalardaki ürünler (Fayser Std., Foamplast, Technoplast Maxi Extra, Mastar 10, Groutart Rapid) için ayrıca 160 dakikalık radyasyon (1120 W), sıcaklık (−10/23/37 °C), nem ve yağış adımlarından oluşan klasik döngü tanımlanmıştır. Bu döngüde 6 aylık depolamaya ek olarak 10, 20 ve 40 günlük uygulamaların sırasıyla toplam 6, 12 ve 24 aylık yaşlanmaya karşılık geldiği kabul edilmiştir.

## 3.3. Numune hazırlama ve hidratasyonun durdurulması

Şartlandırma sonrasında her ambalajdan alınan kuru harç doğrudan analiz edilmiştir. Hidrate numuneler ürünün karışım oranına göre hazırlanmış [karışım suyu/sıvı oranları VERİ GEREKLİ], 1, 7 ve 28 gün kür edilmiş ve ilgili yaşta hidratasyon durdurulmuştur [durdurma yöntemi ve kullanılan çözücü DOĞRULANACAK]. Technopool 20 µm numunesinin 7 günlük yaşında durdurma işlemi uygulanmış ve uygulanmamış iki numune karşılaştırmalı olarak ölçülmüştür.

## 3.4. Ölçüm koşulları

XRD ölçümleri Cu Kα ışınımıyla (λ = 1,5406 Å), numune döndürücülü yansıma geometrisinde, 5,0–70,0° 2θ aralığında ve 0,026° adım aralığıyla alınmıştır (ham veri dosyası başlık bilgilerine göre). FTIR spektrumları 4000–650 cm⁻¹ aralığında 1 cm⁻¹ veri aralığıyla geçirgenlik (%T) olarak kaydedilmiştir [cihaz ve ölçüm modu (ATR) DOĞRULANACAK]. FTIR ölçümlerinin çoğu iki, bazıları üç veya dört tekrar olarak alınmıştır.

## 3.5. Veri işleme

Ham XRD (.rd) ve FTIR (.csv) dosyaları bu rapor için yeniden işlenmiş ve tüm grafikler aynı ölçek ve renk kodlamasıyla çizilmiştir (Referans: siyah, 12 µm: mavi, 20 µm: turuncu, 30 µm: yeşil). Veri işlemede aşağıdaki adımlar izlenmiştir:

- **Numune yüksekliği kayması düzeltmesi.** Özellikle polimer modifiyeli İzolatex Plus numunelerinde pikler 0,1–0,7° 2θ kadar yüksek açıya kaymıştır. Bu kayma, iç standart olarak kuvars (101, 26,64°) ya da dolomit (104, 30,94°) piki kullanılarak Δ2θ = k·cos θ bağıntısıyla düzeltilmiştir. Diğer ürünlerde kayma 0,08°'in altındadır.
- **XRD net pik alanları.** Etrenjit (8,7–9,5°), portlandit (17,7–18,4°), alit (51,45–52,0°) ve kalsit (29,15–29,7°) pencerelerinde doğrusal taban çizgisi üzerindeki net alan hesaplanmıştır. Bu değerler yarı niceldir ve yalnızca aynı ürün içindeki göreli karşılaştırma için kullanılmalıdır. Rietveld analizi yapılmamıştır.
- **FTIR göstergeleri.** Tekrar spektrumlarının ortalaması alınmış, absorbansa (A = −log T) çevrilmiştir. Portlandit O–H bandı (3640 cm⁻¹) yerel taban çizgisine göre yükseklik olarak, yapısal su O–H bandı 3750–2700 cm⁻¹ aralığında alan olarak, Si–O gerilme bandının konumu ise 900–1060 cm⁻¹ aralığındaki en düşük geçirgenlik noktası olarak belirlenmiştir.

**Ölçüm belirsizliğine ilişkin not.** Aynı numunenin FTIR tekrarları arasında 650 cm⁻¹'deki geçirgenlik %5–9'a, O–H bandı alanı %25–30'a varan farklılık göstermektedir (örneğin Çizelge 5'te Macunart 28 gün 12 µm). Bu fark, numuneler arasındaki farklarla aynı büyüklüktedir. Bu nedenle FTIR bant şiddetlerine dayalı sıralamalar, tekrar aralıkları örtüşüyorsa "fark yok" olarak değerlendirilmiştir. XRD ölçümleri tekrarsızdır; kum içeren ürünlerde (Technopool, İzolatex Plus) iri tanelerden kaynaklanan tane istatistiği sorunu kuvars, feldispat ve kalsit pik şiddetlerini numuneden numuneye değiştirmektedir.

# 4. Bulgular ve Değerlendirme

Groutart Rapid ve Mastar 10 ürünlerine ait bulgular, proje ekibinin önceki değerlendirme raporundan (GR ve M10 SKT, son hâl) olduğu gibi aktarılmıştır (Bölüm 4.1 ve 4.2). Macunart, İzolatex Plus ve Technopool bulguları bu rapor kapsamında ham veriden yeniden işlenerek değerlendirilmiştir (Bölüm 4.3–4.5).
''')
A(eski_bolum())

# ---------------- MACUNART ----------------
u = 'Macunart'
A('''
### 4.3. Macunart

Macunart numunelerinin difraktogramlarında baskın faz dolomittir (30,9° ve 41,1°). Bunun yanında kalsit (29,4°), alit (32,2° ve 51,7°) ve belit (32,6°) pikleri bulunmaktadır. Hesaplanan XRD göstergeleri Çizelge 4'te, FTIR göstergeleri Çizelge 5'te verilmiştir.

**Kuru harç.** Şekil 13'te verilen kuru harç difraktogramlarında referans ve üç ambalaj tipine ait desenler birbirine çok yakındır. Etrenjit ve portlandit bölgelerindeki net alanlar tüm numunelerde gürültü düzeyindedir (etrenjit 15–30, portlandit 18–45). Alit piki de benzer büyüklüktedir (225–254). Şekil 14'teki FTIR spektrumları neredeyse üst üste çakışmaktadır. 3640 cm⁻¹ portlandit bandı görülmemekte, Si–O bandı tüm numunelerde anhidrit alite özgü ~925 cm⁻¹ konumunda bulunmaktadır. Bu bulgular, şartlandırma sonrasında hiçbir ambalaj tipinde XRD ve FTIR ile saptanabilir düzeyde ön hidratasyon oluşmadığını göstermektedir.

> **Uyarı.** "Macunart Ref Kuru Harç" adıyla kaydedilen ikinci ölçüm (9811) belirgin etrenjit (121) ve portlandit (718) pikleri içermekte, alit piki ise neredeyse kaybolmuş durumdadır (13). Bu desen kuru harçtan çok sertleşmiş bir numuneye benzemektedir ve 28 günlük referans ölçümünün eksik olması dikkat çekicidir. Numune adlandırmasının kontrol edilmesi önerilir [DOĞRULANACAK]. Bu ölçüm değerlendirmeye alınmamıştır.
''')
A(sek(13, 'MA_XRD_K.png', 'Macunart – kuru harç XRD difraktogramları'))
A(sek(14, 'MA_FTIR_K.png', 'Macunart – kuru harç FTIR spektrumları (30 µm kuru harç FTIR ölçümü yoktur)'))
A('''
**1 gün.** Şekil 15'te 1 günlük difraktogramlar verilmiştir. Tüm numunelerde etrenjit ve portlandit oluşmuş, alit piki kuru harca göre yaklaşık dörtte birine inmiştir. Portlandit net alanı Referans (%d) ve 12 µm (%d) numunelerinde birbirine yakın, 20 µm (%d) ve 30 µm (%d) numunelerinde ise yaklaşık yarısı düzeyindedir. Etrenjit 30 µm numunesinde (%d) diğerlerine (145–154) göre daha düşüktür. Kalan alit miktarları birbirine yakın olduğundan (43–60), bu farkın klinker tüketiminden çok portlandit kristallenmesindeki farklılıktan kaynaklanabileceği düşünülmektedir. Şekil 16'daki FTIR spektrumlarında 3640 cm⁻¹ bandı ve O–H bandı alanı numuneler arasında tekrar aralığı içinde kalmaktadır. Si–O bandı Referansta 960 cm⁻¹, ambalaj numunelerinde 966–971 cm⁻¹ konumundadır.

1 günlük XRD verilerine göre erken hidratasyon ürünü gelişimi: **12 µm ≈ Referans > 20 µm > 30 µm** şeklinde sıralanabilir.
''' % (x(u,'1','Ref','P'), x(u,'1','12','P'), x(u,'1','20','P'), x(u,'1','30','P'), x(u,'1','30','E')))
A(sek(15, 'MA_XRD_1.png', 'Macunart – 1 günlük XRD difraktogramları'))
A(sek(16, 'MA_FTIR_1.png', 'Macunart – 1 günlük FTIR spektrumları'))
A('''
**7 gün.** Şekil 17'de alit pikinin tüm numunelerde neredeyse tamamen tükendiği görülmektedir (1–5). Ambalaj numunelerinde etrenjit (145–147) ve portlandit (425–715) birbirine yakındır. En yüksek portlandit 12 µm numunesindedir. Referans numunesinde (9864) ise hem etrenjit (%d) hem portlandit (%d), ambalaj numunelerinin ve aynı numunenin 1 günlük değerinin altında kalmıştır. Referans numunesinin XRD ve FTIR ölçümlerinin diğer 7 günlük numunelerden belirgin biçimde sonra alınmış olması (ölçüm no 9864 ve 9871), bu numunenin ayrı bir karışımdan hazırlanmış olabileceğini düşündürmektedir [DOĞRULANACAK]. Şekil 18'deki FTIR spektrumlarında 3640 cm⁻¹ bandı en belirgin 12 µm numunesindedir. Diğer göstergeler tekrar aralığı içindedir.

7 günlük sonuçlara göre ambalaj numuneleri arasında anlamlı bir fark görülmemekte, sıralama **12 µm ≥ 30 µm ≈ 20 µm** şeklindedir. Referans numunesi bu yaşta güvenilir bir karşılaştırma noktası olarak kabul edilmemiştir.
''' % (x(u,'7','Ref','E'), x(u,'7','Ref','P')))
A(sek(17, 'MA_XRD_7.png', 'Macunart – 7 günlük XRD difraktogramları'))
A(sek(18, 'MA_FTIR_7.png', 'Macunart – 7 günlük FTIR spektrumları'))
A('''
**28 gün.** 28 günlük yaşta XRD ölçümü yalnızca 12 µm ve 30 µm (Şekil 19), FTIR ölçümü yalnızca 12 µm ve 20 µm numunelerinde (Şekil 20) mevcuttur. 12 µm ve 30 µm numunelerinin etrenjit (105 ve 98) ve portlandit (496 ve 435) değerleri birbirine yakındır. FTIR'da 12 µm ve 20 µm numunelerinin tüm göstergeleri tekrar aralığı içinde örtüşmektedir. Referans ve 20 µm XRD ile Referans ve 30 µm FTIR ölçümleri eksiktir [VERİ GEREKLİ].

**Macunart için genel değerlendirme.** Kuru harçta ön hidratasyon bulgusu yoktur. 1 günlük yaşta 20 µm ve 30 µm numunelerinde portlandit gelişimi bir miktar geride kalmış, ancak bu fark 7 ve 28 günlük yaşlarda kapanmıştır. 12 µm ambalaj, tüm yaşlarda Referans ile aynı ya da daha yüksek hidratasyon ürünü göstermiştir.
''')
A(sek(19, 'MA_XRD_28.png', 'Macunart – 28 günlük XRD difraktogramları'))
A(sek(20, 'MA_FTIR_28.png', 'Macunart – 28 günlük FTIR spektrumları'))
A(xrd_cizelge(u, 4, ek=('K2',)))
A(ftir_cizelge(u, 5))

# ---------------- İZOLATEX ----------------
u = 'İzolatex Plus'
A('''
### 4.4. İzolatex Plus

İzolatex Plus iki bileşenli bir üründür. Ambalaj değişikliği toz bileşeni kapsamaktadır. Kuru harç difraktogramlarında kuvars (26,6° ve 20,9°) ve kalsit (29,4°) baskın olup alit ve belit pikleri bulunmaktadır. Hidrate numunelerin FTIR spektrumlarında 2950, 1730, 1160 ve 700 cm⁻¹ civarındaki bantlar sıvı bileşenden gelen polimere aittir (C–H, C=O, C–O ve aromatik halka titreşimleri; stiren-akrilik tipte bir dispersiyonla uyumlu [DOĞRULANACAK]). Bu bantlar 900–1200 cm⁻¹ Si–O bölgesiyle örtüştüğünden İzolatex Plus için FTIR'da C-S-H değerlendirmesi sınırlıdır. Ayrıca hidrate numunelerde 0,1–0,7° 2θ'lik numune yüksekliği kayması saptanmış ve düzeltilmiştir (Bölüm 3.5). Esnek membran numunelerinin düz bir yüzey oluşturmaması, numuneler arasında pik şiddetlerini de etkilemektedir. Göstergeler Çizelge 6 ve Çizelge 7'de verilmiştir.

> **Not.** "İzolatex 05.05.2026" adlı numuneler Referans olarak değerlendirilmiştir. Aynı ölçüm numarası (9725) hem "1.gün" hem "1.gün 12 Mikron" dosyalarında kullanılmıştır. İkincisi 12 µm kabul edilmiştir. 7 günlük "Izolatex Plus 05.05.2026" FTIR numunesinde (9807) film kalınlığı belirtilmemiştir ve 12 µm olarak varsayılmıştır (12 µm*) [DOĞRULANACAK].

**Kuru harç.** Şekil 21'deki difraktogramlarda tüm ambalaj tiplerinde etrenjit (15–58) ve portlandit (10–45) gürültü düzeyindedir. Alit piki Referansta %d, ambalaj numunelerinde %d–%d aralığındadır. Ancak 31,9–32,8° bölgesinin toplam alanı ambalaj numunelerinde daha düşük değildir. Bu nedenle alit farkı tane istatistiğine bağlanmış, ön hidratasyon göstergesi olarak kabul edilmemiştir. 11,6° alçı taşı piki ambalaj numunelerinde (41–68) Referansa (13) göre daha belirgindir. Bu farkın hemihidratın nemle alçı taşına dönüşmesinden mi yoksa üretim partisi farkından mı kaynaklandığı mevcut verilerle ayırt edilememektedir [DOĞRULANACAK: referans numunenin üretim tarihi/partisi]. Kuru harç FTIR ölçümü yoktur.
''' % (x(u,'K','Ref','A'), min(x(u,'K',a,'A') for a in ['12','20','30']), max(x(u,'K',a,'A') for a in ['12','20','30'])))
A(sek(21, 'IZ_XRD_K.png', 'İzolatex Plus – kuru harç XRD difraktogramları'))
A('''
**1 gün.** Şekil 22'de 1 günlük yaşta hiçbir numunede belirgin etrenjit veya portlandit piki oluşmadığı görülmektedir (net alanlar 5–31). Alit pikleri hâlâ belirgindir. Bu durum, polimer modifiyeli sistemde erken yaşta kristalin hidratasyon ürünlerinin sınırlı kaldığını göstermektedir. 30 µm numunesinin deseni (yüksek zemin ve daha yüksek kalsit ile alit) diğerlerinden farklıdır ve numune hazırlamadan kaynaklanabilir. Şekil 23'teki FTIR spektrumları yalnızca Referans ve 12 µm numunelerini içermektedir ve polimer bantları dışında belirgin bir fark görülmemektedir.
''')
A(sek(22, 'IZ_XRD_1.png', 'İzolatex Plus – 1 günlük XRD difraktogramları'))
A(sek(23, 'IZ_FTIR_1.png', 'İzolatex Plus – 1 günlük FTIR spektrumları'))
A('''
**7 gün.** Şekil 24'teki 7 günlük difraktogramlarda portlandit oluşumu başlamıştır. Ancak değerler numuneden numuneye çok değişkendir: 12 µm %d, Referans %d, 20 µm %d, 30 µm %d. Aynı 7 günlük 30 µm numunesinin ikinci ölçümünde (9844) portlandit %d ve etrenjit %d bulunmuştur. Bu, aynı ambalaj ve yaş için ölçümler arasında yaklaşık 10 katlık bir fark anlamına gelir. Bu tekrarlanabilirlik düzeyinde 7 günlük XRD verileri ambalaj sıralaması için yeterli görülmemektedir. Şekil 25'teki FTIR spektrumlarında 3640 cm⁻¹ bandı 12 µm* (%s) ve 30 µm ikinci ölçümünde (%s) Referansa (%s) göre biraz daha belirgindir, ancak tekrar aralıkları geniştir.
''' % (x(u,'7','12','P'), x(u,'7','Ref','P'), x(u,'7','20','P'), x(u,'7','30','P'), x(u,'7b','30','P'), x(u,'7b','30','E'),
       fs(F[u+'|7|12?']['OH3640'][0],1), fs(F[u+'|7b|30']['OH3640'][0],1), fs(F[u+'|7|Ref']['OH3640'][0],1)))
A(sek(24, 'IZ_XRD_7.png', 'İzolatex Plus – 7 günlük XRD difraktogramları (30 µm için 9766 ölçümü gösterilmiştir)'))
A(sek(25, 'IZ_FTIR_7.png', 'İzolatex Plus – 7 günlük FTIR spektrumları'))
A('''
**28 gün.** Şekil 26'da 28 günlük yaşta tüm numunelerde etrenjit ve portlandit belirginleşmiştir. Portlandit 20 µm (%d) > 12 µm (%d) ≈ Referans (%d), etrenjit 20 µm (%d) > Referans (%d) ≈ 12 µm (%d) sıralamasındadır. Kalan alit miktarları birbirine yakındır (30–48). Şekil 27'deki FTIR spektrumlarında Referans ve 12 µm numuneleri neredeyse çakışmaktadır (3640 cm⁻¹: %s ve %s mAbs; Si–O: 963 ve 962 cm⁻¹). 30 µm numunesinin 28 günlük ölçümü yoktur [VERİ GEREKLİ].

**İzolatex Plus için genel değerlendirme.** Kuru harçta ön hidratasyon bulgusu yoktur. Alçı taşı pikindeki fark izlenmelidir. 28 günlük yaşta 12 µm ve 20 µm ambalajlar Referans ile aynı ya da daha yüksek hidratasyon ürünü göstermiştir. Erken yaş (1 ve 7 gün) verileri numune geometrisi ve tekrarlanabilirlik sorunları nedeniyle karar için kullanılmamalıdır.
''' % (x(u,'28','20','P'), x(u,'28','12','P'), x(u,'28','Ref','P'), x(u,'28','20','E'), x(u,'28','Ref','E'), x(u,'28','12','E'),
       fs(F[u+'|28|Ref']['OH3640'][0],1), fs(F[u+'|28|12']['OH3640'][0],1)))
A(sek(26, 'IZ_XRD_28.png', 'İzolatex Plus – 28 günlük XRD difraktogramları'))
A(sek(27, 'IZ_FTIR_28.png', 'İzolatex Plus – 28 günlük FTIR spektrumları'))
A(xrd_cizelge(u, 6, ek=('7b',)))
A(ftir_cizelge(u, 7, ek=('7b',)))

# ---------------- TECHNOPOOL ----------------
u = 'Technopool'
A('''
### 4.5. Technopool

Technopool difraktogramlarında kuvars (26,6°) ve feldispat (27,6–28,0°) agrega fazları baskındır. Kalsit, alit ve belit pikleri bulunmaktadır. Technopool için 30 µm ambalaj test edilmemiştir. Göstergeler Çizelge 8 ve Çizelge 9'da verilmiştir. Kum içeriği nedeniyle 900–1200 cm⁻¹ FTIR bölgesi kuvarsın ~1080 cm⁻¹ bandıyla örtüşmektedir.

**Kuru harç.** Şekil 28'de üç numunede de etrenjit (33–44) ve portlandit (11–26) gürültü düzeyindedir. Alit piki ambalaj numunelerinde Referansa göre daha düşük değildir (Referans %d; 12 µm %d; 20 µm %d). Kuru harçta ön hidratasyon bulgusu yoktur. Kuru harç FTIR ölçümü yoktur.
''' % (x(u,'K','Ref','A'), x(u,'K','12','A'), x(u,'K','20','A')))
A(sek(28, 'TP_XRD_K.png', 'Technopool – kuru harç XRD difraktogramları'))
A('''
**1 gün.** Şekil 29'da Referans numunesinin portlandit piki (%d) 12 µm (%d) ve 20 µm (%d) numunelerinin yaklaşık iki katıdır. Etrenjit de Referans (%d) > 12 µm (%d) > 20 µm (%d) sırasındadır. Kalan alit 12 µm numunesinde (%d) Referanstan (%d) yüksektir. Bu durum 12 µm numunesinde silikat hidratasyonunun bir miktar geride olduğunu düşündürmektedir. Şekil 30'daki FTIR spektrumlarında O–H bandı alanı ambalaj numunelerinde daha yüksek görünmektedir. Ancak Si–O ve kuvars bantlarının örtüşmesi ve tekrarlar arasındaki geniş fark (12 µm Si–O minimumu 944–987 cm⁻¹) nedeniyle FTIR'dan bir sıralama çıkarılamamaktadır.

1 günlük XRD verilerine göre sıralama: **Referans > 12 µm ≥ 20 µm.**
''' % (x(u,'1','Ref','P'), x(u,'1','12','P'), x(u,'1','20','P'), x(u,'1','Ref','E'), x(u,'1','12','E'), x(u,'1','20','E'), x(u,'1','12','A'), x(u,'1','Ref','A')))
A(sek(29, 'TP_XRD_1.png', 'Technopool – 1 günlük XRD difraktogramları'))
A(sek(30, 'TP_FTIR_1.png', 'Technopool – 1 günlük FTIR spektrumları'))
A('''
**7 gün.** Şekil 31'de alitin büyük ölçüde tükendiği görülmektedir. Portlandit Referansta (%d), 12 µm (%d) ve 20 µm (%d) numunelerine göre yaklaşık %%%s daha yüksektir. Etrenjit de aynı eğilimi izlemektedir (%d, %d, %d). Şekil 32'deki FTIR spektrumlarında O–H bandı alanı Referansta (%s) 12 µm (%s) ve 20 µm (%s) numunelerinden yüksektir. Bu sonuç XRD bulgusuyla uyumludur.

**Hidratasyon durdurmanın etkisi.** 7 günlük 20 µm numunesinin durdurulmamış ölçümünde (9741) portlandit (%d) ve etrenjit (%d), durdurulmuş numuneye (9742; %d ve %d) göre sırasıyla yaklaşık %%%s ve %%%s yüksektir. Bu sonuç, durdurma yapılmadığında hidratasyonun numune alındıktan sonra da sürdüğünü göstermekte ve tüm yaşlarda durdurma işleminin standart uygulanmasının önemini ortaya koymaktadır.
''' % (x(u,'7','Ref','P'), x(u,'7','12','P'), x(u,'7','20','P'), yuzde(x(u,'7','Ref','P'), (x(u,'7','12','P')+x(u,'7','20','P'))/2),
       x(u,'7','Ref','E'), x(u,'7','12','E'), x(u,'7','20','E'),
       fs(F[u+'|7|Ref']['H2O_alan'][0]), fs(F[u+'|7|12']['H2O_alan'][0]), fs(F[u+'|7|20']['H2O_alan'][0]),
       x(u,'7nd','20','P'), x(u,'7nd','20','E'), x(u,'7','20','P'), x(u,'7','20','E'),
       yuzde(x(u,'7nd','20','P'), x(u,'7','20','P')), yuzde(x(u,'7nd','20','E'), x(u,'7','20','E'))))
A(sek(31, 'TP_XRD_7.png', 'Technopool – 7 günlük XRD difraktogramları (20 µm: durdurulmuş numune)'))
A(sek(32, 'TP_FTIR_7.png', 'Technopool – 7 günlük FTIR spektrumları'))
A('''
**28 gün.** Şekil 33'te portlandit Referans (%d) ≈ 12 µm (%d) > 20 µm (%d), etrenjit Referans (%d) > 12 µm (%d) = 20 µm (%d) sırasındadır. 11,7° civarında tüm numunelerde AFm fazına (muhtemelen monokarbonat) ait bir pik gelişmiştir. 28 günlük FTIR ölçümü yalnızca 12 µm numunesinde mevcuttur (Şekil 34). Bu nedenle FTIR karşılaştırması yapılamamıştır [VERİ GEREKLİ: Referans ve 20 µm 28 gün FTIR].

**Technopool için genel değerlendirme.** Kuru harçta ön hidratasyon bulgusu olmamasına karşın, Referans numunesi 1, 7 ve 28 günlük yaşların tamamında en yüksek portlandit ve etrenjit değerlerini vermiştir. 12 µm ambalaj 28 günde Referansa yaklaşmış, 20 µm ambalaj ise 28 günde de geride kalmıştır. Bu eğilimin ambalaj kaynaklı, XRD'de saptanamayan amorf ya da yüzeysel bir ön hidratasyondan mı yoksa parti ve numune farkından mı kaynaklandığı mevcut verilerle ayırt edilememektedir. Technopool için performans testlerinin (yapışma dayanımı, açık bekletme süresi) sonuçlarıyla birlikte değerlendirilmesi önerilir.
''' % (x(u,'28','Ref','P'), x(u,'28','12','P'), x(u,'28','20','P'), x(u,'28','Ref','E'), x(u,'28','12','E'), x(u,'28','20','E')))
A(sek(33, 'TP_XRD_28.png', 'Technopool – 28 günlük XRD difraktogramları'))
A(sek(34, 'TP_FTIR_28.png', 'Technopool – 28 günlük FTIR spektrumu (yalnızca 12 µm)'))
A(xrd_cizelge(u, 8, ek=('7nd',)))
A(ftir_cizelge(u, 9))

# ---------------- GENEL ----------------
A('''
# 5. Genel Değerlendirme

Macunart, İzolatex Plus ve Technopool için XRD hidratasyon göstergelerinin yaşa göre değişimi Şekil 35'te topluca verilmiştir. Ürün bazındaki bulgular Çizelge 10'da özetlenmiştir.
''')
A(sek(35, 'OZET_XRD.png', 'XRD hidratasyon göstergelerinin (net pik alanı) yaşa ve ambalaj tipine göre değişimi'))
A('''
| Ürün | Kuru harçta ön hidratasyon | Erken yaş (1–7 gün) | 28 gün | Öne çıkan / geride kalan ambalaj |
|---|---|---|---|---|
| Groutart Rapid* | – | 1 g: 12 µm (kristalin), 20 µm (C-S-H); 7 g: 20 µm (XRD), 30 µm (FTIR) | 12 µm (kristalin), 20 µm (C-S-H) | En dengeli: 20 µm |
| Mastar 10* | – | 30 µm önde | 30 µm dengeli; 12 ≈ 20 µm | En dengeli: 30 µm |
| Macunart | Saptanmadı | 1 g: 12 µm ≈ Ref > 20 > 30 µm; 7 g: ambalajlar benzer | 12 ≈ 30 µm (XRD), 12 ≈ 20 µm (FTIR) | Belirgin olumsuz etki yok; 12 µm Ref ile eşdeğer |
| İzolatex Plus | Saptanmadı (alçı taşı farkı izlenmeli) | Tekrarlanabilirlik yetersiz | 20 > 12 µm ≈ Ref | Belirgin olumsuz etki yok |
| Technopool | Saptanmadı | Ref > 12 ≥ 20 µm | Ref ≈ 12 > 20 µm | Ref önde; 20 µm geride |

: Çizelge 10. Ürün bazında bulguların özeti (*önceki rapordan; kuru harç ölçümü bu raporda bulunmamaktadır)

Bu bulgulara göre aşağıdaki değerlendirmeler önerilmektedir:

1. **Ön hidratasyon.** Uygulanan şartlandırma sonrasında Macunart, İzolatex Plus ve Technopool kuru harçlarında hiçbir ambalaj tipinde XRD ile saptanabilir kristalin hidratasyon ürünü (etrenjit, portlandit) oluşmamış, alit korunmuştur. Macunart FTIR verileri de bunu desteklemektedir. Ancak XRD'nin kristalin fazlar için algılama sınırı genellikle yaklaşık %1 düzeyindedir. Literatürde nem duyarlılığı en yüksek olduğu bildirilen C₃A ve serbest kireçteki yüzeysel değişimler ile amorf ön hidratasyon ürünleri bu yöntemle saptanamayabilir (Dubina ve diğerleri, 2011).
2. **Hidratasyon kinetiği.** Ambalaj tipinin etkisi ürüne göre değişmektedir. Bütün ürünlerde tutarlı biçimde olumsuz sonuç veren tek bir ambalaj tipi görülmemiştir. Film kalınlığı ile hidratasyon göstergeleri arasında da sistematik bir ilişki (kalınlık arttıkça daha iyi koruma) gözlenmemiştir. Bu nedenle numuneler arası farkların bir bölümü numune hazırlama ve ölçüm değişkenliğinden kaynaklanıyor olabilir.
3. **Technopool.** Referans ambalajın tüm yaşlarda önde olduğu tek üründür. 20 µm ambalaj 28 günde de geride kalmıştır. Bu ürün için ambalaj değişikliği kararı performans testleriyle desteklenmelidir.
4. **SKT açısından.** Mineralojik veriler, 2 yıllık depolamaya karşılık kabul edilen şartlandırma sonunda 12 µm ve 20 µm ambalajların Macunart ve İzolatex Plus için raf ömrünü kısaltacak bir ön hidratasyona yol açtığını göstermemektedir. SKT kararı için XRD ve FTIR tek başına yeterli değildir. Ürün standartlarındaki performans testlerinin (Ürün Listesi – Testler sayfası: kıvam, priz, yapışma, basınç/eğilme dayanımı, kap ömrü vb.) Referans ile karşılaştırmalı sonuçları gereklidir [VERİ GEREKLİ].

# 6. Öneriler

- **Eksik ölçümlerin tamamlanması.** Macunart 28 gün Referans ve 20 µm XRD; Technopool 28 gün Referans ve 20 µm FTIR; İzolatex Plus 28 gün 30 µm XRD/FTIR; İzolatex Plus ve Technopool kuru harç FTIR ölçümleri.
- **Ön hidratasyonun daha duyarlı ölçülmesi.** Kuru harçlarda TGA ile 40–200 °C (bağlı su) ve 400–500 °C (portlandit) kütle kayıpları, Referans ile karşılaştırmalı olarak ölçülmelidir. TGA, XRD'de görünmeyen amorf ön hidratasyon ürünlerini de yansıtır.
- **Nicel faz analizi.** Kuru harçlarda C₃A (kübik/ortorombik), alçı taşı, basanit ve anhidrit oranlarının Rietveld analiziyle belirlenmesi. Nem girişine en duyarlı fazlar bunlardır.
- **Tekrarlanabilirlik.** XRD ölçümlerinin en az iki bağımsız numune hazırlamasıyla tekrarlanması ve agrega içeren ürünlerde numunenin 63 µm altına öğütülmesi ya da elenmesi. İzolatex Plus gibi esnek numunelerde yüzeyin tutucuyla aynı seviyeye getirilmesi.
- **Hidratasyon durdurma.** Tüm yaşlarda aynı durdurma prosedürünün uygulanması. RILEM önerisine göre izopropanol ile solvent değişimi tercih edilebilir (Snellings ve diğerleri, 2018).
- **Ambalaj verileri.** Referans ambalajın yapısı ve torbaların su buharı geçirgenliği (WVTR) değerlerinin rapora eklenmesi. Film kalınlığı tek başına nem bariyerini tanımlamaz.

# Kaynaklar

Dubina, E., Wadsö, L., & Plank, J. (2011). A sorption balance study of water vapour sorption on anhydrous cement minerals and cement constituents. *Cement and Concrete Research, 41*(11), 1196–1204. https://doi.org/10.1016/j.cemconres.2011.07.009

Scrivener, K., Snellings, R., & Lothenbach, B. (Eds.). (2016). *A practical guide to microstructural analysis of cementitious materials*. CRC Press. ISBN 978-1-4987-3865-1

Snellings, R., vd. (2018). RILEM TC-238 SCM recommendation on hydration stoppage by solvent exchange for the study of hydrate assemblages. *Materials and Structures, 51*(6), 172. https://doi.org/10.1617/s11527-018-1298-5 [yazar listesi DOI sayfasından DOĞRULANACAK]

Whittaker, M., Dubina, E., Al-Mutawa, F., vd. (2013). The effect of prehydration on the engineering properties of CEM I Portland cement. *Advances in Cement Research, 25*(1), 12–20. https://doi.org/10.1680/adcr.12.00030

Ylmén, R., Jäglid, U., Steenari, B.-M., & Panas, I. (2009). Early hydration and setting of Portland cement monitored by IR, SEM and Vicat techniques. *Cement and Concrete Research, 39*(5), 433–439. https://doi.org/10.1016/j.cemconres.2009.01.017

Yu, P., Kirkpatrick, R. J., Poe, B., McMillan, P. F., & Cong, X. (1999). Structure of calcium silicate hydrate (C-S-H): Near-, mid-, and far-infrared spectroscopy. *Journal of the American Ceramic Society, 82*(3), 742–748. https://doi.org/10.1111/j.1151-2916.1999.tb01826.x

# Ek A. Ölçüm Listesi ve Veri Dosyaları

Ham veriler `veri/xrd/` ve `veri/ftir/` klasörlerinde, işlenmiş göstergeler `sekiller/gostergeler.json` dosyasında, grafikleri ve çizelgeleri üreten kodlar `kod/` klasöründe bulunmaktadır. Ölçüm numaraları Çizelge 4–9'da verilmiştir. XRD ve FTIR ölçüm numaraları birbirinden bağımsızdır.
''')

open('SKT_Proje_Raporu.md', 'w', encoding='utf8').write('\n'.join(MD))
print('ok')
