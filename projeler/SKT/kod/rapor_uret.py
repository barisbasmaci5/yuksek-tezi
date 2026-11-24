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
subtitle: "XRD ve FTIR Bulguları — Proje Raporu (Taslak)"
date: "Kasım 2026"
lang: tr-TR
---

`[DOĞRULANACAK]` ve `[VERİ GEREKLİ]` işaretli yerler proje ekibince tamamlanacaktır.

# 1. Amaç ve Kapsam

Çalışmada Kalekim ürünleri 12, 20 ve 30 µm iç film kalınlığındaki torbalara doldurulmuş ve hızlandırılmış iklim şartlandırmasına tabi tutulmuştur. Şartlandırma sonrasında kuru harç ile 1, 7 ve 28 günlük hidrate numuneler XRD ve FTIR ile incelenmiş, sonuçlar mevcut ambalajdaki referans ürünle karşılaştırılmıştır. Amaç, ambalaj değişikliğinin depolama sırasında ürüne nem girişini artırıp artırmadığını, dolayısıyla ön hidratasyona veya hidratasyonda gecikmeye yol açıp açmadığını belirlemektir.

Rapor Groutart Rapid, Mastar 10, Macunart, İzolatex Plus ve Technopool ürünlerini kapsamaktadır. Izoseal ve Izostop verileri henüz gelmemiştir [VERİ GEREKLİ].

# 2. Literatür

Çimento depolama sırasında nemle temas ederse tane yüzeyinde sınırlı bir hidratasyon başlar. Bu olaya ön hidratasyon denir. Whittaker ve diğerleri (2013), CEM I 42,5R çimentosunu ince tabaka hâlinde %60 ve %85 bağıl nemde bekletmiştir. %60 bağıl nemde dayanım kaybı ihmal edilebilir düzeyde kalmış, ancak işlenebilirlik azalmış ve priz süresi uzamıştır. %85 bağıl nemde ise basınç dayanımı, özellikle erken yaşta, belirgin biçimde düşmüştür.

Dubina ve diğerleri (2011), klinker fazlarının su buharı alımını ayrı ayrı ölçmüştür. En reaktif bileşenler serbest kireç (CaO) ve C₃A olmuştur. Ortorombik C₃A yaklaşık %55 bağıl nemde su bağlamaya başlamış, C₃S ve C₂S'de ise sorpsiyon ancak %74 bağıl nemde başlamış ve az kalmıştır. Kalsiyum sülfatlar suyu çoğunlukla fiziksel olarak tutmuştur. Buna göre ambalajın nem bariyeri en çok alüminat ve sülfat fazlarını etkileyecektir. Ambalaj tiplerini kuru harç raf ömrü açısından doğrudan karşılaştıran bir çalışma bulunamamıştır [KAYNAK GEREKLİ].

XRD'de etrenjit, portlandit ve AFm gibi kristalin hidratasyon ürünleri ile reaksiyona girmemiş alit ve belit izlenebilir. C-S-H amorf olduğu için yalnızca geniş bir zemin yükselmesi verir (Scrivener ve diğerleri, 2016). Hidratasyonu belirli bir yaşta durdurmak için RILEM TC-238 SCM, izopropanol ile solvent değişimini önermektedir (Snellings ve diğerleri, 2018).

FTIR'da C-S-H oluşumu 970–1100 cm⁻¹ aralığındaki banttan izlenir (Ylmén ve diğerleri, 2009). Sentetik C-S-H'de ana Si–O bantları 950–1100, 810–830 ve 660–670 cm⁻¹ aralığındadır ve konumları Ca/Si oranıyla kayar (Yu ve diğerleri, 1999). Bu raporda Si–O bandının anhidrit alitteki ~920 cm⁻¹ konumundan ~960–1000 cm⁻¹'e kayması hidratasyon göstergesi olarak kullanılmıştır.

# 3. Malzeme ve Yöntem

## 3.1. Ürünler ve ambalajlar

Torba tipleri Çizelge 1'de, ürün–ambalaj test matrisi Çizelge 2'de verilmiştir.

| Torba tipi | İç film kalınlığı | Numune kodu |
|---|---|---|
| Mapei Adesilex P7 torbası | 12 µm | 12 µm |
| Mapei boş torba | 20 µm | 20 µm |
| Weber torbası (weberfloor LVL 1040) | 30 µm | 30 µm |
| Ürünün mevcut Kalekim ambalajı [DOĞRULANACAK] | [VERİ GEREKLİ] | Referans |

: Çizelge 1. Ambalaj tipleri (Ürün Listesi dosyası)

| Ürün | Referans | 12 µm | 20 µm | 30 µm |
|---|:-:|:-:|:-:|:-:|
| Groutart Rapid | ✓ | ✓ | ✓ | ✓ |
| Mastar 10 | – | ✓ | ✓ | ✓ |
| Macunart | ✓ | ✓ | ✓ | ✓ |
| İzolatex Plus (toz bileşen) | ✓ | ✓ | ✓ | ✓ |
| Technopool | ✓ | ✓ | ✓ | – |

: Çizelge 2. Ürün–ambalaj test matrisi

## 3.2. Şartlandırma

Kraft torbalar için iki döngü tanımlanmıştır (Çizelge 3). Soğuk döngü Moskova ve Fransa'nın soğuk bölgelerinin, sıcak döngü Nairobi, Duhok ve Trablus'un iklim verilerine göre hazırlanmıştır. Her döngü 24 saattir. 45 günlük uygulamanın 2 yıllık depolamaya karşılık geldiği kabul edilmiştir. Soğuk döngü 06.03.2026–21.04.2026 tarihleri arasında uygulanmıştır. Sıcak döngünün tarihleri ve hangi ürünün hangi döngüye girdiği dosyalarda yoktur [DOĞRULANACAK].

| Soğuk döngü adımı | Bağıl nem | Yağış | Süre (sa) | | Sıcak döngü adımı | Bağıl nem | Yağış | Süre (sa) |
|---|--:|---|--:|---|---|--:|---|--:|
| −15 °C | %90 | yok | 5 | | 0 °C | %65 | yok | 3 |
| −5 °C | %90 | yok | 5 | | 5 °C | %75 | yok | 4 |
| 0 °C | %85 | yok | 4 | | 15 °C | %75 | 70 mm | 4 |
| 10 °C | %80 | 70 mm | 5 | | 35 °C | %70 | yok | 5 |
| 20 °C | %75 | 90 mm | 5 | | 45 °C | %80 | yok | 4 |
| | | | | | 45 °C | %20 | yok | 4 |
| Toplam | | | 24 | | Toplam | | | 24 |

: Çizelge 3. Kraft torbalar için şartlandırma döngüleri (Şartlandırma Koşulları dosyası)

Jüt torbalar (Fayser Std., Foamplast, Technoplast Maxi Extra, Mastar 10, Groutart Rapid) için ayrıca 160 dakikalık klasik döngü kullanılmıştır. Bu döngü radyasyon (1120 W), −10, 23 ve 37 °C sıcaklık, nem ve yağış adımlarından oluşur. 6 aylık depolamaya ek 10, 20 ve 40 günlük uygulama, toplam 6, 12 ve 24 aylık yaşlanmaya karşılık gelir.

## 3.3. Numune hazırlama

Kuru harç numuneleri şartlandırmadan sonra torbadan alınıp doğrudan ölçülmüştür. Hidrate numuneler 1, 7 ve 28 gün kür edilmiş, ardından hidratasyonları durdurulmuştur [karışım oranları VERİ GEREKLİ; durdurma yöntemi ve çözücü DOĞRULANACAK]. Technopool 20 µm numunesi 7. günde hem durdurulmuş hem durdurulmamış olarak ölçülmüştür.

## 3.4. Ölçüm koşulları

XRD ölçümleri Cu Kα ışınımıyla (λ = 1,5406 Å), numune döndürücülü yansıma geometrisinde, 5–70° 2θ aralığında, 0,026° adımla alınmıştır. Bu bilgiler ham veri dosyalarının başlığından okunmuştur. FTIR spektrumları 4000–650 cm⁻¹ aralığında, 1 cm⁻¹ aralıkla, %T olarak kaydedilmiştir [cihaz ve ATR modu DOĞRULANACAK]. FTIR ölçümleri çoğunlukla iki, bazen üç ya da dört tekrarlıdır.

## 3.5. Veri işleme

Ham XRD (.rd) ve FTIR (.csv) dosyaları yeniden işlenmiş, tüm grafikler aynı ölçek ve renklerle çizilmiştir. Renkler: Referans siyah, 12 µm mavi, 20 µm turuncu, 30 µm yeşil.

İzolatex Plus hidrate numunelerinde pikler 0,1–0,7° 2θ yüksek açıya kaymıştır. Diğer ürünlerde kayma 0,08°'in altındadır. Kayma, kuvars (26,64°) ya da dolomit (30,94°) piki iç standart alınarak Δ2θ = k·cos θ bağıntısıyla düzeltilmiştir.

Her numunede şu pencerelerde doğrusal taban çizgisi üzerindeki net pik alanı hesaplanmıştır: etrenjit 8,7–9,5°, portlandit 17,7–18,4°, alit 51,45–52,0°, kalsit 29,15–29,7°. Bu değerler yarı niceldir. Yalnızca aynı ürünün numuneleri arasında karşılaştırma için kullanılmalıdır. Rietveld analizi yapılmamıştır.

FTIR tekrarlarının ortalaması alınıp absorbansa (A = −log T) çevrilmiştir. Üç gösterge kullanılmıştır: 3640 cm⁻¹ portlandit bandının yüksekliği, 3750–2700 cm⁻¹ O–H bandının alanı ve 900–1060 cm⁻¹ aralığındaki Si–O bandının konumu.

Aynı numunenin FTIR tekrarları arasında O–H bandı alanı %25–30'a kadar değişmektedir (örnek: Çizelge 5, Macunart 28 gün 12 µm). Bu, numuneler arasındaki farkla aynı büyüklüktedir. Bu nedenle tekrar aralıkları örtüşen FTIR sonuçları "fark yok" olarak okunmuştur. XRD ölçümleri tekrarsızdır. Kum içeren ürünlerde (Technopool, İzolatex Plus) iri taneler kuvars, feldispat ve kalsit pik şiddetlerini numuneden numuneye değiştirmektedir.

# 4. Bulgular

Groutart Rapid ve Mastar 10 bölümleri ekibin önceki raporundan (GR ve M10 SKT, son hâl) değiştirilmeden alınmıştır. Macunart, İzolatex Plus ve Technopool bölümleri bu rapor için ham veriden hazırlanmıştır.
''')
A(eski_bolum())

# ---------------- MACUNART ----------------
u = 'Macunart'
A('''
### 4.3. Macunart

Macunart'ta baskın faz dolomittir (30,9° ve 41,1°). Kalsit (29,4°), alit (32,2° ve 51,7°) ve belit (32,6°) de bulunmaktadır. XRD göstergeleri Çizelge 4'te, FTIR göstergeleri Çizelge 5'te verilmiştir.

#### Kuru harç

Dört numunenin difraktogramları birbirine çok yakındır (Şekil 13). Etrenjit (15–30) ve portlandit (18–45) gürültü düzeyindedir. Alit 225–254 aralığındadır. FTIR spektrumları üst üste çakışmaktadır (Şekil 14). 3640 cm⁻¹ bandı yoktur ve Si–O bandı anhidrit alitin konumundadır (~925 cm⁻¹). Hiçbir ambalajda ön hidratasyon saptanmamıştır.

"Macunart Ref Kuru Harç" adıyla kaydedilen ikinci XRD ölçümü (9811) bu tabloya uymamaktadır. Bu numunede etrenjit 121, portlandit 718'dir ve alit neredeyse kalmamıştır (13). Desen sertleşmiş bir numuneye aittir. 28 günlük referans ölçümünün eksik olması nedeniyle numunenin yanlış adlandırılmış olabileceği düşünülmektedir [DOĞRULANACAK]. Bu ölçüm değerlendirmeye alınmamıştır.
''')
A(sek(13, 'MA_XRD_K.png', 'Macunart – kuru harç XRD difraktogramları'))
A(sek(14, 'MA_FTIR_K.png', 'Macunart – kuru harç FTIR spektrumları (30 µm kuru harç FTIR ölçümü yoktur)'))
A('''
#### 1 gün

Tüm numunelerde etrenjit ve portlandit oluşmuş, alit kuru harçtaki değerin yaklaşık dörtte birine inmiştir (Şekil 15). Portlandit Referansta %d, 12 µm'de %d'dir. 20 µm (%d) ve 30 µm (%d) numunelerinde bunun yaklaşık yarısıdır. Etrenjit 30 µm'de %d, diğerlerinde 145–154'tür. Kalan alit tüm numunelerde birbirine yakındır (43–60), yani fark klinker tüketiminde değil portlandit pikindedir.

FTIR'da 3640 cm⁻¹ bandı ve O–H alanı tekrar aralığı içindedir (Şekil 16). Si–O bandı Referansta 960 cm⁻¹, ambalaj numunelerinde 966–971 cm⁻¹'dir.

XRD'ye göre 1 günlük sıralama: **12 µm ≈ Referans > 20 µm > 30 µm**.
''' % (x(u,'1','Ref','P'), x(u,'1','12','P'), x(u,'1','20','P'), x(u,'1','30','P'), x(u,'1','30','E')))
A(sek(15, 'MA_XRD_1.png', 'Macunart – 1 günlük XRD difraktogramları'))
A(sek(16, 'MA_FTIR_1.png', 'Macunart – 1 günlük FTIR spektrumları'))
A('''
#### 7 gün

Alit tüm numunelerde tükenmiştir (1–5; Şekil 17). Ambalaj numunelerinde etrenjit 145–147, portlandit 425–715'tir. En yüksek portlandit 12 µm'dedir. Referansta etrenjit %d, portlandit %d'dir. Bu değerler hem ambalaj numunelerinin hem de Referansın kendi 1 günlük değerinin altındadır. Referansın XRD (9864) ve FTIR (9871) ölçümleri diğer 7 günlük numunelerden çok sonra alınmıştır. Numune ayrı bir karışımdan hazırlanmış olabilir [DOĞRULANACAK]. Bu nedenle Referans 7. günde karşılaştırmaya alınmamıştır.

FTIR'da 3640 cm⁻¹ bandı en belirgin 12 µm'dedir (Şekil 18). Diğer göstergeler tekrar aralığı içindedir.

7 günlük sıralama: **12 µm ≥ 30 µm ≈ 20 µm**. Fark küçüktür.
''' % (x(u,'7','Ref','E'), x(u,'7','Ref','P')))
A(sek(17, 'MA_XRD_7.png', 'Macunart – 7 günlük XRD difraktogramları'))
A(sek(18, 'MA_FTIR_7.png', 'Macunart – 7 günlük FTIR spektrumları'))
A('''
#### 28 gün

28 günlük yaşta yalnızca 12 ve 30 µm'nin XRD (Şekil 19), 12 ve 20 µm'nin FTIR (Şekil 20) ölçümü vardır. 12 ve 30 µm'de etrenjit 105 ve 98, portlandit 496 ve 435'tir. 12 ve 20 µm'nin FTIR göstergeleri tekrar aralığı içinde örtüşmektedir. Referans ve 20 µm XRD ile Referans ve 30 µm FTIR ölçümleri eksiktir [VERİ GEREKLİ].

Sonuç olarak Macunart'ta ön hidratasyon görülmemiştir. 20 ve 30 µm'de 1. gündeki portlandit gerilemesi 7. günde kapanmıştır. 12 µm her yaşta Referansla aynı ya da daha yüksek değer vermiştir.
''')
A(sek(19, 'MA_XRD_28.png', 'Macunart – 28 günlük XRD difraktogramları'))
A(sek(20, 'MA_FTIR_28.png', 'Macunart – 28 günlük FTIR spektrumları'))
A(xrd_cizelge(u, 4, ek=('K2',)))
A(ftir_cizelge(u, 5))

# ---------------- İZOLATEX ----------------
u = 'İzolatex Plus'
A('''
### 4.4. İzolatex Plus

İzolatex Plus iki bileşenlidir ve ambalaj değişikliği toz bileşeni kapsamaktadır. Kuru harçta kuvars (26,6° ve 20,9°) ile kalsit (29,4°) baskındır, alit ve belit de bulunmaktadır.

Hidrate numunelerin FTIR spektrumlarında 2950, 1730, 1160 ve 700 cm⁻¹'de sıvı bileşenin polimerine ait bantlar vardır. Bant seti stiren-akrilik bir dispersiyonla uyumludur [DOĞRULANACAK]. Bu bantlar Si–O bölgesiyle (900–1200 cm⁻¹) örtüştüğü için C-S-H bu üründe FTIR ile değerlendirilememiştir. Hidrate numunelerde 0,1–0,7°'lik kayma düzeltilmiştir (Bölüm 3.5). Esnek membran numuneleri düz bir yüzey oluşturmadığından pik şiddetleri de etkilenmiştir. Göstergeler Çizelge 6 ve 7'dedir.

"İzolatex 05.05.2026" adlı numuneler Referans kabul edilmiştir. 9725 numarası hem "1.gün" hem "1.gün 12 Mikron" dosyasında kullanılmıştır; ikincisi 12 µm sayılmıştır. 7 günlük 9807 FTIR numunesinde film kalınlığı yazmamaktadır; 12 µm varsayılmıştır (12 µm*) [DOĞRULANACAK].

#### Kuru harç

Etrenjit (15–58) ve portlandit (10–45) tüm ambalajlarda gürültü düzeyindedir (Şekil 21). Alit Referansta %d, ambalaj numunelerinde %d–%d'dir. Ancak 31,9–32,8° bölgesinin toplam alanı ambalaj numunelerinde düşük değildir. Bu nedenle alit farkı tane istatistiğine bağlanmıştır.

11,6°'deki alçı taşı piki ambalaj numunelerinde 41–68, Referansta 13'tür. Bu fark hemihidratın nemle alçı taşına dönüşmesinden de, parti farkından da kaynaklanabilir. Mevcut verilerle ikisi ayırt edilememektedir [DOĞRULANACAK: Referansın üretim tarihi ve partisi]. Kuru harç FTIR ölçümü yoktur.
''' % (x(u,'K','Ref','A'), min(x(u,'K',a,'A') for a in ['12','20','30']), max(x(u,'K',a,'A') for a in ['12','20','30'])))
A(sek(21, 'IZ_XRD_K.png', 'İzolatex Plus – kuru harç XRD difraktogramları'))
A('''
#### 1 gün

Hiçbir numunede belirgin etrenjit ya da portlandit yoktur (5–31; Şekil 22). Alit pikleri hâlâ belirgindir. Polimer modifiyeli sistemde ilk gün kristalin hidratasyon ürünü az oluşmaktadır. 30 µm numunesinin zemini, kalsit ve alit değerleri diğerlerinden yüksektir. Bunun numune hazırlamadan kaynaklandığı düşünülmektedir. FTIR yalnızca Referans ve 12 µm için vardır ve polimer bantları dışında fark görülmemektedir (Şekil 23).
''')
A(sek(22, 'IZ_XRD_1.png', 'İzolatex Plus – 1 günlük XRD difraktogramları'))
A(sek(23, 'IZ_FTIR_1.png', 'İzolatex Plus – 1 günlük FTIR spektrumları'))
A('''
#### 7 gün

Portlandit oluşmaya başlamıştır, ancak değerler çok dağınıktır: 12 µm %d, Referans %d, 20 µm %d, 30 µm %d (Şekil 24). Aynı 30 µm numunesinin ikinci ölçümünde (9844) portlandit %d, etrenjit %d çıkmıştır. Aynı ambalaj ve yaşta yaklaşık 10 kat fark vardır. Bu yüzden 7 günlük XRD ambalaj sıralaması için kullanılmamıştır. FTIR'da 3640 cm⁻¹ bandı 12 µm*'da %s, 30 µm ikinci ölçümde %s, Referansta %s mAbs'dir (Şekil 25). Tekrar aralıkları geniştir.
''' % (x(u,'7','12','P'), x(u,'7','Ref','P'), x(u,'7','20','P'), x(u,'7','30','P'), x(u,'7b','30','P'), x(u,'7b','30','E'),
       fs(F[u+'|7|12?']['OH3640'][0],1), fs(F[u+'|7b|30']['OH3640'][0],1), fs(F[u+'|7|Ref']['OH3640'][0],1)))
A(sek(24, 'IZ_XRD_7.png', 'İzolatex Plus – 7 günlük XRD difraktogramları (30 µm için 9766 ölçümü gösterilmiştir)'))
A(sek(25, 'IZ_FTIR_7.png', 'İzolatex Plus – 7 günlük FTIR spektrumları'))
A('''
#### 28 gün

Tüm numunelerde etrenjit ve portlandit oluşmuştur (Şekil 26). Portlandit: 20 µm %d, 12 µm %d, Referans %d. Etrenjit: 20 µm %d, Referans %d, 12 µm %d. Kalan alit birbirine yakındır (30–48). FTIR'da Referans ve 12 µm neredeyse çakışmaktadır: 3640 cm⁻¹ bandı %s ve %s mAbs, Si–O bandı 963 ve 962 cm⁻¹ (Şekil 27). 30 µm'nin 28 günlük ölçümü yoktur [VERİ GEREKLİ].

Sonuç olarak İzolatex Plus'ta ön hidratasyon görülmemiştir. Alçı taşı farkı ayrıca izlenmelidir. 28. günde 12 ve 20 µm Referansla aynı ya da daha yüksek değer vermiştir. 1 ve 7 günlük veriler numune geometrisi ve tekrarlanabilirlik sorunları nedeniyle karar için kullanılmamalıdır.
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

Technopool'da kuvars (26,6°) ve feldispat (27,6–28,0°) baskındır. Kalsit, alit ve belit de bulunmaktadır. 30 µm ambalaj test edilmemiştir. Göstergeler Çizelge 8 ve 9'dadır. Kum içeriği nedeniyle FTIR'da Si–O bölgesi kuvarsın ~1080 cm⁻¹ bandıyla örtüşmektedir.

#### Kuru harç

Etrenjit (33–44) ve portlandit (11–26) üç numunede de gürültü düzeyindedir (Şekil 28). Alit ambalaj numunelerinde Referanstan düşük değildir: Referans %d, 12 µm %d, 20 µm %d. Ön hidratasyon saptanmamıştır. Kuru harç FTIR ölçümü yoktur.
''' % (x(u,'K','Ref','A'), x(u,'K','12','A'), x(u,'K','20','A')))
A(sek(28, 'TP_XRD_K.png', 'Technopool – kuru harç XRD difraktogramları'))
A('''
#### 1 gün

Referansın portlandit değeri (%d) 12 µm (%d) ve 20 µm'nin (%d) yaklaşık iki katıdır (Şekil 29). Etrenjit de aynı sıradadır: %d, %d, %d. 12 µm'de kalan alit (%d) Referanstan (%d) yüksektir, yani bu numunede silikat hidratasyonu biraz geridedir.

FTIR'da O–H alanı ambalaj numunelerinde yüksek görünmektedir (Şekil 30). Ancak Si–O bandı kuvarsla örtüşmekte ve tekrarlar arasında geniş aralıkta değişmektedir (12 µm'de 944–987 cm⁻¹). Bu nedenle FTIR'dan sıralama yapılmamıştır.

XRD'ye göre 1 günlük sıralama: **Referans > 12 µm ≥ 20 µm**.
''' % (x(u,'1','Ref','P'), x(u,'1','12','P'), x(u,'1','20','P'), x(u,'1','Ref','E'), x(u,'1','12','E'), x(u,'1','20','E'), x(u,'1','12','A'), x(u,'1','Ref','A')))
A(sek(29, 'TP_XRD_1.png', 'Technopool – 1 günlük XRD difraktogramları'))
A(sek(30, 'TP_FTIR_1.png', 'Technopool – 1 günlük FTIR spektrumları'))
A('''
#### 7 gün

Alit büyük ölçüde tükenmiştir (Şekil 31). Portlandit Referansta %d, 12 µm'de %d, 20 µm'de %d'dir. Referans ambalaj numunelerinden yaklaşık %%%s yüksektir. Etrenjit de aynı sırayı izlemektedir (%d, %d, %d). FTIR'da O–H alanı Referansta %s, 12 µm'de %s, 20 µm'de %s'tür (Şekil 32). Bu da XRD sonucuyla uyumludur.

7 günlük 20 µm numunesinin durdurulmamış ölçümünde (9741) portlandit %d, etrenjit %d'dir. Durdurulmuş numunede (9742) bu değerler %d ve %d'dir. Durdurma yapılmayınca portlandit yaklaşık %%%s, etrenjit %%%s yüksek çıkmıştır. Hidratasyon numune alındıktan sonra da sürmektedir. Bu yüzden durdurma işlemi tüm yaşlarda aynı şekilde uygulanmalıdır.
''' % (x(u,'7','Ref','P'), x(u,'7','12','P'), x(u,'7','20','P'), yuzde(x(u,'7','Ref','P'), (x(u,'7','12','P')+x(u,'7','20','P'))/2),
       x(u,'7','Ref','E'), x(u,'7','12','E'), x(u,'7','20','E'),
       fs(F[u+'|7|Ref']['H2O_alan'][0]), fs(F[u+'|7|12']['H2O_alan'][0]), fs(F[u+'|7|20']['H2O_alan'][0]),
       x(u,'7nd','20','P'), x(u,'7nd','20','E'), x(u,'7','20','P'), x(u,'7','20','E'),
       yuzde(x(u,'7nd','20','P'), x(u,'7','20','P')), yuzde(x(u,'7nd','20','E'), x(u,'7','20','E'))))
A(sek(31, 'TP_XRD_7.png', 'Technopool – 7 günlük XRD difraktogramları (20 µm: durdurulmuş numune)'))
A(sek(32, 'TP_FTIR_7.png', 'Technopool – 7 günlük FTIR spektrumları'))
A('''
#### 28 gün

Portlandit Referansta %d, 12 µm'de %d, 20 µm'de %d'dir (Şekil 33). Etrenjit Referansta %d, 12 ve 20 µm'de %d'dir. Tüm numunelerde 11,7° civarında bir AFm piki (muhtemelen monokarbonat) oluşmuştur. 28 günlük FTIR yalnızca 12 µm için vardır (Şekil 34) [VERİ GEREKLİ: Referans ve 20 µm].

Sonuç olarak Technopool'da da ön hidratasyon görülmemiştir. Buna karşın Referans 1, 7 ve 28. günde en yüksek portlandit ve etrenjit değerlerini vermiştir. 12 µm 28. günde Referansa yaklaşmış, 20 µm geride kalmıştır. Bu farkın nedeni mevcut verilerle belirlenememektedir. XRD'de görünmeyen amorf ya da yüzeysel bir ön hidratasyon olabileceği gibi parti veya numune farkı da olabilir. Technopool için yapışma dayanımı ve açık bekletme süresi sonuçlarına bakılmalıdır.
''' % (x(u,'28','Ref','P'), x(u,'28','12','P'), x(u,'28','20','P'), x(u,'28','Ref','E'), x(u,'28','12','E')))
A(sek(33, 'TP_XRD_28.png', 'Technopool – 28 günlük XRD difraktogramları'))
A(sek(34, 'TP_FTIR_28.png', 'Technopool – 28 günlük FTIR spektrumu (yalnızca 12 µm)'))
A(xrd_cizelge(u, 8, ek=('7nd',)))
A(ftir_cizelge(u, 9))

# ---------------- GENEL ----------------
A('''
# 5. Genel Değerlendirme

Üç ürünün XRD göstergeleri Şekil 35'te, beş ürünün özeti Çizelge 10'da verilmiştir.
''')
A(sek(35, 'OZET_XRD.png', 'XRD göstergelerinin (net pik alanı) yaşa ve ambalaj tipine göre değişimi'))
A('''
| Ürün | Kuru harçta ön hidratasyon | 1–7 gün | 28 gün | Sonuç |
|---|---|---|---|---|
| Groutart Rapid* | – | 1 g: 12 µm (kristalin), 20 µm (C-S-H); 7 g: 20 µm (XRD), 30 µm (FTIR) | 12 µm (kristalin), 20 µm (C-S-H) | En dengeli: 20 µm |
| Mastar 10* | – | 30 µm önde | 30 µm önde; 12 ≈ 20 µm | En dengeli: 30 µm |
| Macunart | Yok | 1 g: 12 µm ≈ Ref > 20 > 30 µm; 7 g: ambalajlar yakın | 12 ≈ 30 µm (XRD), 12 ≈ 20 µm (FTIR) | Olumsuz etki yok |
| İzolatex Plus | Yok (alçı taşı farkı izlenmeli) | Veri tekrarlanabilir değil | 20 > 12 µm ≈ Ref | Olumsuz etki yok |
| Technopool | Yok | Ref > 12 ≥ 20 µm | Ref ≈ 12 > 20 µm | Ref önde, 20 µm geride |

: Çizelge 10. Ürün bazında özet (*önceki rapordan; bu ürünlerin kuru harç ölçümü raporda yoktur)

Macunart, İzolatex Plus ve Technopool kuru harçlarında hiçbir ambalajda etrenjit ya da portlandit oluşmamış, alit korunmuştur. Macunart'ın FTIR verisi de bunu doğrulamaktadır. Ancak XRD kristalin fazları genellikle yaklaşık %1'in üzerinde saptayabilir. Nemden en çok etkilenen C₃A ve serbest kireçteki yüzeysel değişimler (Dubina ve diğerleri, 2011) ve amorf ön hidratasyon ürünleri bu yöntemle görülmeyebilir.

Ambalajın hidratasyona etkisi ürüne göre değişmiştir. Bütün ürünlerde kötü sonuç veren tek bir ambalaj yoktur. Film kalınlığı arttıkça sonuçların iyileştiği bir eğilim de görülmemiştir. Bu nedenle numuneler arasındaki farkların bir kısmı numune hazırlama ve ölçüm değişkenliğinden gelebilir.

Referansın her yaşta önde olduğu tek ürün Technopool'dur. Bu üründe 20 µm 28. günde de geride kalmıştır. Technopool'da ambalaj kararı performans testlerine göre verilmelidir.

SKT açısından, 2 yıllık depolamaya karşılık kabul edilen şartlandırma sonunda Macunart ve İzolatex Plus'ta 12 ve 20 µm ambalajların ön hidratasyona yol açtığına dair mineralojik bir bulgu yoktur. SKT kararı için XRD ve FTIR yeterli değildir. Referansla karşılaştırmalı performans testleri (Ürün Listesi – Testler sayfası: kıvam, priz, yapışma, basınç ve eğilme dayanımı, kap ömrü vb.) gereklidir [VERİ GEREKLİ].

# 6. Öneriler

- Eksik ölçümler tamamlanmalıdır: Macunart 28 gün Referans ve 20 µm XRD; Technopool 28 gün Referans ve 20 µm FTIR; İzolatex Plus 28 gün 30 µm XRD ve FTIR; İzolatex Plus ve Technopool kuru harç FTIR.
- Kuru harçlarda TGA ile 40–200 °C (bağlı su) ve 400–500 °C (portlandit) kütle kayıpları Referansla karşılaştırmalı ölçülmelidir. TGA, XRD'de görünmeyen amorf ön hidratasyonu da gösterir.
- Kuru harçlarda C₃A (kübik ve ortorombik), alçı taşı, basanit ve anhidrit oranları Rietveld analiziyle belirlenmelidir. Neme en duyarlı fazlar bunlardır.
- XRD en az iki bağımsız numuneyle tekrarlanmalıdır. Agregalı ürünlerde numune 63 µm altına öğütülmeli ya da elenmelidir. İzolatex Plus gibi esnek numunelerde yüzey tutucu seviyesine getirilmelidir.
- Tüm yaşlarda aynı durdurma işlemi uygulanmalıdır. RILEM önerisi izopropanol ile solvent değişimidir (Snellings ve diğerleri, 2018).
- Referans ambalajın yapısı ve torbaların su buharı geçirgenliği (WVTR) rapora eklenmelidir. Nem bariyerini film kalınlığı tek başına belirlemez.

# Kaynaklar

Dubina, E., Wadsö, L., & Plank, J. (2011). A sorption balance study of water vapour sorption on anhydrous cement minerals and cement constituents. *Cement and Concrete Research, 41*(11), 1196–1204. https://doi.org/10.1016/j.cemconres.2011.07.009

Scrivener, K., Snellings, R., & Lothenbach, B. (Eds.). (2016). *A practical guide to microstructural analysis of cementitious materials*. CRC Press. ISBN 978-1-4987-3865-1

Snellings, R., vd. (2018). RILEM TC-238 SCM recommendation on hydration stoppage by solvent exchange for the study of hydrate assemblages. *Materials and Structures, 51*(6), 172. https://doi.org/10.1617/s11527-018-1298-5 [yazar listesi DOI sayfasından DOĞRULANACAK]

Whittaker, M., Dubina, E., Al-Mutawa, F., vd. (2013). The effect of prehydration on the engineering properties of CEM I Portland cement. *Advances in Cement Research, 25*(1), 12–20. https://doi.org/10.1680/adcr.12.00030

Ylmén, R., Jäglid, U., Steenari, B.-M., & Panas, I. (2009). Early hydration and setting of Portland cement monitored by IR, SEM and Vicat techniques. *Cement and Concrete Research, 39*(5), 433–439. https://doi.org/10.1016/j.cemconres.2009.01.017

Yu, P., Kirkpatrick, R. J., Poe, B., McMillan, P. F., & Cong, X. (1999). Structure of calcium silicate hydrate (C-S-H): Near-, mid-, and far-infrared spectroscopy. *Journal of the American Ceramic Society, 82*(3), 742–748. https://doi.org/10.1111/j.1151-2916.1999.tb01826.x

# Ek A. Veri Dosyaları

Ham veriler `veri/xrd/` ve `veri/ftir/` klasörlerinde, hesaplanan göstergeler `sekiller/gostergeler.json` dosyasındadır. Grafikleri ve çizelgeleri üreten kodlar `kod/` klasöründedir. Ölçüm numaraları Çizelge 4–9'da verilmiştir. XRD ve FTIR ölçüm numaraları birbirinden bağımsızdır.
''')

open('SKT_Proje_Raporu.md', 'w', encoding='utf8').write('\n'.join(MD))
print('ok')
