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
    return '\n'.join(satir) + '\n\n: Tablo %d. %s XRD net pik alanları (k.b.; doğrusal taban çizgisi üzerindeki alan, numune yüksekliği kayması düzeltilmiş)\n' % (no, urun)
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
    return '\n'.join(satir) + '\n\n: Tablo %d. %s FTIR göstergeleri (tekrar ölçümlerin ortalaması; parantez içinde en küçük–en büyük değer)\n' % (no, urun)

def sek(no, dosya, baslik):
    return '\n![Şekil %d. %s](sekiller/%s){width=16cm}\n' % (no, baslik, dosya)

# oranlar (metinde kullanılan)
def x(u, y, a, k): return X['%s|%s|%s' % (u, y, a)][k]
def yuzde(a, b): return fs(100 * (a - b) / b, 0)


# Türkçe ek: sayının okunuşuna göre -dIr / -tIr
_SON = {1:('i',0),2:('i',0),3:('ü',1),4:('ü',1),5:('i',1),6:('ı',0),7:('i',0),8:('i',0),9:('u',0),
        10:('u',0),20:('i',0),30:('u',0),40:('ı',1),50:('i',0),60:('ı',1),70:('i',1),80:('i',0),90:('ı',0),
        100:('ü',0),1000:('i',0)}
def _son(n):
    n = abs(int(n))
    if n == 0: return ('ı', 0)
    if n % 10: return _SON[n % 10]
    if n % 100: return _SON[n % 100]
    if n % 1000: return _SON[100]
    return _SON[1000]
def nd(n):
    """sayı + ek: 959'dur, 263'tür, 1010'dur"""
    v, sert = _son(n)
    return "%s'%s%s" % (bs(n), 't' if sert else 'd', {'i':'ir','ı':'ır','u':'ur','ü':'ür'}[v])
def bs(n):
    """binlik ayırıcı: 20 199"""
    s = '%d' % round(n)
    return s if len(s) < 5 else s[:-3] + ' ' + s[-3:]


# ---------- kaynaklar: metinde {c:anahtar} ya da {c:a,b}; numara ilk geçiş sırasına göre ----------
KAYNAK = {
 'kalekim2025': 'Kalekim Ar-Ge. (2025). *Tekli, İkili ve Üçlü Bağlayıcı Sistemlere Sahip Ürünlerin Raf Ömürlerinin Performans Özelliklerine Etkilerinin İncelenmesi – 2025 Çalışmaları Raporu*. Kurum içi rapor (Hizmete Özel).',
 'taylor': 'Taylor, H. F. W. (1997). *Cement chemistry* (2nd ed.). London: Thomas Telford. ISBN 0-7277-2592-0.',
 'lamberet': 'Lamberet, S. (2004). *Durability of ternary binders based on Portland cement, calcium aluminate cement and calcium sulfate* (Doktora tezi No. 3151). École Polytechnique Fédérale de Lausanne.',
 'whittaker': 'Whittaker, M., Dubina, E., Al-Mutawa, F., vd. (2013). The effect of prehydration on the engineering properties of CEM I Portland cement. *Advances in Cement Research, 25*(1), 12–20. https://doi.org/10.1680/adcr.12.00030',
 'dubina': 'Dubina, E., Wadsö, L., & Plank, J. (2011). A sorption balance study of water vapour sorption on anhydrous cement minerals and cement constituents. *Cement and Concrete Research, 41*(11), 1196–1204. https://doi.org/10.1016/j.cemconres.2011.07.009',
 'astmf1249': 'ASTM International. (2020). *ASTM F1249-20: Standard test method for water vapor transmission rate through plastic film and sheeting using a modulated infrared sensor*. West Conshohocken, PA. [yürürlükteki baskı DOĞRULANACAK]',
 'astmf1980': 'ASTM International. (2021). *ASTM F1980-21: Standard guide for accelerated aging of sterile barrier systems and medical devices*. West Conshohocken, PA.',
 'scrivener2016': 'Scrivener, K., Snellings, R., & Lothenbach, B. (Eds.). (2016). *A practical guide to microstructural analysis of cementitious materials*. Boca Raton: CRC Press. ISBN 978-1-4987-3865-1.',
 'scrivener2004': 'Scrivener, K. L., Füllmann, T., Gallucci, E., Walenta, G., & Bermejo, E. (2004). Quantitative study of Portland cement hydration by X-ray diffraction/Rietveld analysis and independent methods. *Cement and Concrete Research, 34*(9), 1541–1547. https://doi.org/10.1016/j.cemconres.2004.04.014',
 'lothenbach': 'Lothenbach, B., Le Saout, G., Gallucci, E., & Scrivener, K. (2008). Influence of limestone on the hydration of Portland cements. *Cement and Concrete Research, 38*(6), 848–860. https://doi.org/10.1016/j.cemconres.2008.01.002',
 'matschei': 'Matschei, T., Lothenbach, B., & Glasser, F. P. (2007). The AFm phase in Portland cement. *Cement and Concrete Research, 37*(2), 118–130. https://doi.org/10.1016/j.cemconres.2006.10.010',
 'snellings': 'Snellings, R., vd. (2018). RILEM TC-238 SCM recommendation on hydration stoppage by solvent exchange for the study of hydrate assemblages. *Materials and Structures, 51*(6), 172. https://doi.org/10.1617/s11527-018-1298-5 [yazar listesi DOĞRULANACAK]',
 'ylmen': 'Ylmén, R., Jäglid, U., Steenari, B.-M., & Panas, I. (2009). Early hydration and setting of Portland cement monitored by IR, SEM and Vicat techniques. *Cement and Concrete Research, 39*(5), 433–439. https://doi.org/10.1016/j.cemconres.2009.01.017',
 'yu': 'Yu, P., Kirkpatrick, R. J., Poe, B., McMillan, P. F., & Cong, X. (1999). Structure of calcium silicate hydrate (C-S-H): Near-, mid-, and far-infrared spectroscopy. *Journal of the American Ceramic Society, 82*(3), 742–748. https://doi.org/10.1111/j.1151-2916.1999.tb01826.x',
 'trezza': 'Trezza, M. A., & Lavat, A. E. (2001). Analysis of the system 3CaO·Al₂O₃–CaSO₄·2H₂O–CaCO₃–H₂O by FT-IR spectroscopy. *Cement and Concrete Research, 31*(6), 869–872. https://doi.org/10.1016/S0008-8846(01)00502-6',
}

MD = []
A = MD.append
A('''---
title: "Farklı İklim Koşulları İçin Ambalaj Yapısının Optimizasyonu ve Raf Ömrüne (SKT) Etkisi"
subtitle: "Ara Rapor: Yaşlandırma Sonrası Mikroyapı İncelemeleri (XRD ve FTIR) — Taslak"
date: "Kasım 2026"
lang: tr-TR
---

Metindeki [DOĞRULANACAK] ve [VERİ GEREKLİ] işaretli yerler proje ekibince tamamlanacaktır.

# 1. Amaç

Çimento esaslı yapı kimyasalları; Portland çimentosu (OPC) ve kalsiyum alüminat çimentosu (CAC) gibi mineral bağlayıcılar, kalsiyum sülfat türleri, kum, kalsit ve dolomit gibi dolgular ile polimer ve kimyasal katkılardan oluşan toz karışımlardır. Bu ürünlerin raf ömrü, içerdikleri ham maddelerin raf ömrü esas alınarak belirlenmektedir. Ancak ürün nemli ya da sıcak ortamda depolandığında veya ambalaj nemi yeterince tutmadığında bağlayıcılar havadaki nemle tepkimeye girebilir (ön hidratasyon). Bunun sonucunda ürünün bağlayıcılığı ve dayanımı düşer, uygulamada beklenen performansa ulaşılamaz. Bu durum hem kalite kaybına hem de gereksiz malzeme, enerji ve maliyet kullanımına yol açmaktadır.

Ekibin 2025 yılında yürüttüğü raf ömrü çalışmasında, orijinal ambalajında işletme koşullarında bekletilen ürünlerde raf süresi uzadıkça hidratasyon veriminin ve performansın düştüğü, CAC içeren bazı ürünlerde 6–12. aylarda taşlaşma ve topaklanma görüldüğü bildirilmiştir {c:kalekim2025}. Aynı çalışmada nem bariyeri artırılmış ambalajlara geçilmesi ya da ambalaj film kalınlığının artırılması önerilmiştir {c:kalekim2025}.

Bu proje, söz konusu öneriden hareketle, farklı iklim koşullarında ürün stabilitesini artırmak ve raf ömrünü uzatmak için ambalaj yapısının optimize edilmesini amaçlamaktadır. Sıcak ve soğuk iklim senaryolarını temsil eden, sıcaklık, nem ve yağış adımlarından oluşan iklim profilleri hazırlanmış ve farklı içerikteki ürünler bu profiller altında hızlandırılmış yaşlandırmaya tabi tutulmuştur. Yaşlandırmadan sonra ürünlerin performansı ve mikroyapısı incelenerek ambalaj yapıları karşılaştırılmakta, gerekli görülen ürünlerde ambalajın bariyer özelliklerinin ve yapısının revize edilmesi öngörülmektedir.

Projeden beklenen çıktılar, farklı coğrafi pazarlarda ürün dayanıklılığının artırılması, kalite kayıplarının azaltılması ve daha uzun raf ömrüne sahip ürünlerin geliştirilmesidir. Bu çıktıların çevresel ve ekonomik sürdürülebilirlik hedeflerine de katkı sağlaması beklenmektedir. Sonuçların performansa göre ticarileştirilmesi ve akademik yayına dönüştürülmesi planlanmaktadır.

Bu rapor projenin mikroyapı ayağına ait ara rapordur ve Groutart Rapid, Mastar 10, Macunart, İzolatex Plus ve Technopool ürünlerini kapsamaktadır. Raporun sorusu, ambalaj tipinin depolama sırasında ürüne nem girişini değiştirip değiştirmediği ve buna bağlı olarak ön hidratasyon ya da hidratasyonda gecikme oluşup oluşmadığıdır. Performans test sonuçları ile Izoseal ve Izostop verileri bu rapora dahil değildir [VERİ GEREKLİ].

# 2. Literatür Özeti

## 2.1. Portland çimentosu ve hidratasyon reaksiyonları

Portland çimentosu, klinkerin uygun oranda alçı taşı ile öğütülmesiyle elde edilir. Klinkerin ana fazları trikalsiyum silikat (C₃S, alit), dikalsiyum silikat (C₂S, belit), trikalsiyum alüminat (C₃A) ve tetrakalsiyum alüminoferrittir (C₄AF) {c:taylor}. Bu raporda kullanılan faz adları ve kısaltmaları Tablo 1'de verilmiştir.

| Faz | Formül | Kısaltma | XRD'deki adı |
|---|---|---|---|
| Trikalsiyum silikat | 3CaO·SiO₂ | C₃S | Alit / hatrurit |
| Dikalsiyum silikat | 2CaO·SiO₂ | C₂S | Belit / larnit |
| Trikalsiyum alüminat | 3CaO·Al₂O₃ | C₃A | – |
| Tetrakalsiyum alüminoferrit | 4CaO·Al₂O₃·Fe₂O₃ | C₄AF | Brovnmillerit |
| Kalsiyum silikat hidrat | değişken | C-S-H | amorf |
| Kalsiyum hidroksit | Ca(OH)₂ | CH | Portlandit |
| Etrenjit | 3CaO·Al₂O₃·3CaSO₄·32H₂O | AFt | Etrenjit |
| Monosülfat / monokarbonat | – | AFm | – |
| Alçı taşı | CaSO₄·2H₂O | CS̄H₂ | Jips |

: Tablo 1. Çimento fazları ve hidratasyon ürünlerinin gösterimi {c:taylor}

Çimento su ile karıştırıldığında C₃S ve C₂S, amorf C-S-H jeli ile kristalin portlanditi (CH) oluşturur. C-S-H, sertleşmiş çimento hamurunun dayanımını sağlayan ana üründür. C₃S erken yaş dayanımını, C₂S ise ileri yaş dayanımını belirler. C₃A, ortamdaki alçı taşı ile önce etrenjiti (AFt), sülfat tükendikten sonra ise monosülfat gibi AFm fazlarını oluşturur {c:taylor}. Ortamda kalsit bulunduğunda monosülfat yerine monokarbonat kararlı hâle gelir ve etrenjit de daha kararlı kalır {c:lothenbach,matschei}.

## 2.2. Kalsiyum alüminat çimentosu ve ikili/üçlü bağlayıcı sistemler

CAC'nin ana reaktif fazı monokalsiyum alüminattır (CA) {c:taylor}. CAC hızlı priz ve erken dayanım gerektiren tesviye şapları, hızlı tamir harçları ve teknik yapıştırıcılarda OPC ve kalsiyum sülfat ile birlikte ikili ya da üçlü bağlayıcı sistem olarak kullanılır {c:kalekim2025,lamberet}. OPC–CAC–kalsiyum sülfat üçlü sistemlerinde CAC ve sülfatça zengin karışımlar ağırlıklı olarak etrenjit ve alüminyum hidroksit (AH₃) oluşturur {c:lamberet}. Bu çalışmadaki ürünlerden Mastar 10, OPC, CAC ve anhidrit içeren üçlü bir sistemdir {c:kalekim2025}. Diğer ürünlerin bağlayıcı sistemleri Tablo 3'te verilmiştir.

## 2.3. Ön hidratasyon ve depolama nemi

Çimento depolama sırasında nemle temas ettiğinde tane yüzeyinde sınırlı bir hidratasyon (ön hidratasyon) başlar. Whittaker ve diğerleri, ince tabaka hâlinde %60 ve %85 bağıl nemde bekletilen CEM I 42,5R çimentosunda %60 bağıl nemin dayanımı ihmal edilebilir düzeyde etkilediğini, ancak işlenebilirliği azalttığını ve priz süresini uzattığını bildirmiştir {c:whittaker}. %85 bağıl nemde ise basınç dayanımı, özellikle erken yaşta, büyük ölçüde düşmüştür {c:whittaker}.

Dubina ve diğerleri, klinker fazlarının su buharı alımını ayrı ayrı ölçmüş ve en reaktif bileşenlerin serbest kireç (CaO) ile C₃A olduğunu göstermiştir {c:dubina}. Ortorombik C₃A yaklaşık %55 bağıl nemde su bağlamaya başlarken C₃S ve C₂S'de sorpsiyon ancak %74 bağıl nemde başlamış ve düşük kalmıştır. Kalsiyum sülfatlar suyu çoğunlukla fiziksel olarak tutmuştur {c:dubina}. Torbaya nem girdiğinde ilk etkilenecek fazların alüminat ve sülfat fazları olması beklenir.

Ekibin 2025 çalışmasında da benzer bir tablo görülmüştür. Mastar 10'un 12. ay numunelerinde 24 saatlik kuruma gerçekleşmemiş ve bu durum CAC'nin rafta ön hidratasyona girmesine bağlanmıştır. CAC içeren ikili sistemlerde (Rapitech, Ultratech) 6–12. aylarda taşlaşma görülmüş, yalnız OPC içeren ürünlerde ise raf süresi uzadıkça hidratasyon verimi ve performans düşmüştür {c:kalekim2025}.

## 2.4. Ambalajın nem bariyeri ve hızlandırılmış yaşlandırma

Bir ambalaj filminin nem bariyeri su buharı geçirgenliği (WVTR) ile tanımlanır. ASTM F1249, plastik film ve levhaların WVTR, su buharı geçirgenliği ve homojen malzemeler için geçirgenlik katsayısının belirlenmesini tanımlar ve WVTR'yi paketlenmiş ürünün raf ömrü ve stabilitesiyle ilişkilendirir {c:astmf1249}. Aynı standart, WVTR'nin film kalınlığıyla ters orantılı olduğu varsayımının her zaman geçerli olmadığını da belirtir {c:astmf1249}. Bu nedenle torbaların bariyer performansı yalnızca film kalınlığından çıkarılamaz.

Hızlandırılmış yaşlandırma, bozulma tepkimelerinin sıcaklıkla Arrhenius bağıntısına göre hızlandığı varsayımına dayanır. Tıbbi ambalajlar için hazırlanmış olan ASTM F1980, hızlandırılmış yaşlandırma çalışmalarının gerçek zamanlı yaşlandırma çalışmalarıyla birlikte yürütülmesini öngörmektedir {c:astmf1980}. Bu projede kullanılan "45 günlük döngü = 2 yıl" eşdeğerliği de gerçek zamanlı depolama verisiyle doğrulanmalıdır.

## 2.5. Hidratasyonun XRD ve FTIR ile izlenmesi

XRD ile etrenjit, portlandit ve AFm gibi kristalin hidratasyon ürünleri ile reaksiyona girmemiş alit ve belit izlenebilir; amorf C-S-H ise yalnızca geniş bir zemin yükselmesi verir {c:scrivener2016}. Rietveld analiziyle bulunan faz miktarlarının görüntü analizi ve TGA ile uyumlu olduğu gösterilmiştir {c:scrivener2004}. Hidratasyonu belirli bir yaşta durdurmak için RILEM TC-238 SCM, izopropanol ile solvent değişimini önermektedir {c:snellings}.

FTIR'da C-S-H oluşumu 970–1100 cm⁻¹ aralığındaki banttan izlenir {c:ylmen}. Sentetik C-S-H'nin ana Si–O bantları 950–1100, 810–830 ve 660–670 cm⁻¹ aralığındadır ve konumları Ca/Si oranına göre kayar {c:yu}. Etrenjit ve alçı taşının sülfat bantları ile 1600–1700 cm⁻¹ aralığındaki H–O–H bükülme bandı, C₃A–alçı taşı–kalsit sisteminde hidratasyonun izlenmesinde kullanılmıştır {c:trezza}. Bu raporda Si–O bandının anhidrit alitteki ~920 cm⁻¹ konumundan ~960–1000 cm⁻¹'e kayması hidratasyon göstergesi olarak kullanılmıştır.

# 3. Deneysel Çalışmalar

## 3.1. Numune hazırlanışı

### 3.1.1. Ambalaj seçimi

Çalışmada üç farklı torba tipi kullanılmış ve ürünün mevcut ambalajı referans alınmıştır (Tablo 2).

| Torba tipi | İç film kalınlığı | Numune kodu |
|---|---|---|
| Mapei Adesilex P7 torbası | 12 µm | 12 µm |
| Mapei boş torba | 20 µm | 20 µm |
| Weber torbası (weberfloor LVL 1040) | 30 µm | 30 µm |
| Ürünün mevcut Kalekim ambalajı [DOĞRULANACAK] | [VERİ GEREKLİ] | Referans |

: Tablo 2. Ambalaj tipleri (Ürün Listesi dosyası)

### 3.1.2. Ürün seçimi

Farklı bağlayıcı sistemlerini ve kullanım alanlarını temsil eden beş ürün seçilmiştir (Tablo 3). Ürün–ambalaj eşleşmeleri de aynı tabloda verilmiştir.

| Ürün | Bağlayıcı sistemi | Referans | 12 µm | 20 µm | 30 µm |
|---|---|:-:|:-:|:-:|:-:|
| Groutart Rapid | [DOĞRULANACAK] | ✓ | ✓ | ✓ | ✓ |
| Mastar 10 | Üçlü (OPC + CAC + anhidrit) {c:kalekim2025} | – | ✓ | ✓ | ✓ |
| Macunart | [DOĞRULANACAK] | ✓ | ✓ | ✓ | ✓ |
| İzolatex Plus (toz bileşen) | [DOĞRULANACAK] | ✓ | ✓ | ✓ | ✓ |
| Technopool | [DOĞRULANACAK] | ✓ | ✓ | ✓ | – |

: Tablo 3. Ürünler, bağlayıcı sistemleri ve test edilen ambalajlar

## 3.2. Deney planı

Kraft torbalar için sıcak ve soğuk iklim senaryolarını temsil eden 24 saatlik iki iklim profili tanımlanmıştır (Tablo 4). Soğuk profil Moskova ve Fransa'nın soğuk bölgelerinin, sıcak profil ise Nairobi, Duhok ve Trablus'un iklim verilerine göre hazırlanmıştır. 45 günlük uygulamanın 2 yıllık depolamaya karşılık geldiği kabul edilmiştir. Soğuk profil 06.03.2026–21.04.2026 tarihleri arasında uygulanmıştır. Sıcak profilin tarihleri ve hangi ürünün hangi profile girdiği dosyalarda yer almamaktadır [DOĞRULANACAK]. Sonuçların iklim profiline göre yorumlanabilmesi için bu bilgi gereklidir.

| Soğuk profil adımı | Bağıl nem | Yağış | Süre (sa) | | Sıcak profil adımı | Bağıl nem | Yağış | Süre (sa) |
|---|--:|---|--:|---|---|--:|---|--:|
| −15 °C | %90 | yok | 5 | | 0 °C | %65 | yok | 3 |
| −5 °C | %90 | yok | 5 | | 5 °C | %75 | yok | 4 |
| 0 °C | %85 | yok | 4 | | 15 °C | %75 | 70 mm | 4 |
| 10 °C | %80 | 70 mm | 5 | | 35 °C | %70 | yok | 5 |
| 20 °C | %75 | 90 mm | 5 | | 45 °C | %80 | yok | 4 |
| | | | | | 45 °C | %20 | yok | 4 |
| Toplam | | | 24 | | Toplam | | | 24 |

: Tablo 4. Kraft torbalar için soğuk ve sıcak iklim profilleri (Şartlandırma Koşulları dosyası)

Jüt torbalarda (Fayser Std., Foamplast, Technoplast Maxi Extra, Mastar 10, Groutart Rapid) radyasyon (1120 W), −10/23/37 °C sıcaklık, nem ve yağış adımlarından oluşan 160 dakikalık klasik döngü kullanılmıştır. 6 aylık depolamaya ek olarak 10, 20 ve 40 günlük uygulama sırasıyla 6, 12 ve 24 aylık yaşlanmaya karşılık gelmektedir.

Yaşlandırmadan sonra her ambalajdan alınan kuru harç doğrudan analiz edilmiş, hidrate numuneler ise 1, 7 ve 28 gün kür edildikten sonra incelenmiştir [karışım oranları VERİ GEREKLİ].

## 3.3. Reaksiyon takibi

### 3.3.1. Reaksiyon durdurma

2025 raf ömrü çalışmasında hidratasyon, AG_YK_TL_0397 numaralı "Çözücü Değişim Metodu ile Çimento Hidratasyonu Durdurma" talimatına göre durdurulmuştur: numuneler havanda dövülmüş, 100 ml aseton ve 50 ml dietil eter ile yıkanmış ve mavi bant filtre kâğıdından süzülmüştür {c:kalekim2025}. Bu çalışmada da aynı talimatın uygulandığı varsayılmıştır [DOĞRULANACAK]. Technopool 20 µm numunesi 7. günde hem durdurulmuş hem durdurulmamış olarak ölçülmüştür.

### 3.3.2. XRD ölçümleri

Ham veri dosyalarının başlık bilgilerine göre XRD ölçümleri Cu Kα ışınımıyla (λ = 1,5406 Å), numune döndürücülü yansıma (reflection) geometrisinde, 2θ = 5–70° aralığında ve 0,026° adımla alınmıştır.

### 3.3.3. FTIR ölçümleri

FTIR spektrumları 4000–650 cm⁻¹ aralığında 1 cm⁻¹ aralıkla %T olarak kaydedilmiş, numunelerin çoğu iki, bazıları üç ya da dört tekrar ölçülmüştür. 2025 çalışmasında FTIR ölçümleri transmisyon modunda alınmıştır {c:kalekim2025}; bu çalışmadaki ölçüm modu [DOĞRULANACAK].

### 3.3.4. Veri işleme

Ham XRD (.rd) ve FTIR (.csv) dosyaları yeniden işlenmiş ve tüm grafikler aynı ölçek ve renklerle çizilmiştir (Referans siyah, 12 µm mavi, 20 µm turuncu, 30 µm yeşil).

İzolatex Plus hidrate numunelerinde pikler 0,1–0,7° 2θ kadar yüksek açıya kaymıştır; diğer ürünlerde kayma 0,08°'in altındadır. Kayma, kuvars (26,64°) ya da dolomit (30,94°) piki iç standart alınarak Δ2θ = k·cos θ bağıntısıyla düzeltilmiştir.

Her numunede etrenjit (8,7–9,5°), portlandit (17,7–18,4°), alit (51,45–52,0°) ve kalsit (29,15–29,7°) pencerelerinde doğrusal taban çizgisi üzerindeki net pik alanı hesaplanmıştır. Bu değerler yarı nicel olup yalnızca aynı ürünün numuneleri arasında karşılaştırma için kullanılmıştır. Rietveld analizi yapılmamıştır.

FTIR tekrarlarının ortalaması alınarak absorbansa (A = −log T) çevrilmiştir. 3640 cm⁻¹ portlandit bandının yüksekliği, 3750–2700 cm⁻¹ O–H bandının alanı ve 900–1060 cm⁻¹ aralığındaki Si–O bandının konumu gösterge olarak kullanılmıştır.

Aynı numunenin FTIR tekrarları arasında O–H bandı alanı %25–30'a kadar değişmektedir (Tablo 7, Macunart 28 gün 12 µm). Bu fark numuneler arasındaki farkla aynı büyüklükte olduğundan tekrar aralıkları örtüşen FTIR sonuçları "fark yok" olarak değerlendirilmiştir. XRD ölçümleri tekrarsızdır. Kum içeren ürünlerde (Technopool, İzolatex Plus) iri taneler nedeniyle kuvars, feldispat ve kalsit pik şiddetleri numuneden numuneye değişmektedir.

## 3.4. Performans testleri

Ürünlere uygulanacak performans testleri Ürün Listesi dosyasındaki Testler sayfasında tanımlanmıştır (Tablo 5). Testler referans ambalajla karşılaştırmalı yapılacak ve ürünlerin kalite kontrol planlarındaki limit değerlerle değerlendirilecektir. 2025 çalışmasında Mastar 10 için TS EN 13813, TS EN 13888, TS EN 196-3 ve TS EN 196-10 standartları uygulanmıştır {c:kalekim2025}. Diğer ürünler için uygulanacak standartlar ve kalite kontrol planı kodları [DOĞRULANACAK].

| Ürün | Testler |
|---|---|
| Macunart | Ambalaj ve ürün görünüşü, işlenebilirlik ve kat kuruma, kap ömrü, zımpara sonrası yüzey görünüşü, tiksotropi, basınç dayanımı, betona yapışma |
| Groutart Rapid | Ambalaj ve ürün görünüşü, kap ömrü, tiksotropi, kapiler su emme, basınç dayanımı (1 saat, 1 gün, 7 gün), betona yapışma |
| İzolatex Plus | Toz ve sıvı bileşen görünüşü, sıvı bileşen katı madde miktarı, işlenebilirlik, viskozite, su geçirimsizlik (pozitif ve negatif basınç), kuru ve ıslak çekme dayanımı, 23 °C'de çatlak köprüleme, su emme, kap ömrü, yapışma |
| Technopool | Ambalaj ve ürün görünüşü, işlenebilirlik, viskozite, seramik düzeltilebilme süresi, kayma, kuru/ıslak/sıcak yapışma, açık bekletme süresi, esneklik, kabuklaşma |
| Mastar 10 | Ambalaj ve ürün görünüşü, kürlenmiş yüzey görünüşü, işlenebilirlik, yayılma çapı (0 ve 15 dk), viskozite, eğilme ve basınç dayanımı (24 saat, 28 gün), ilk ve son priz, aşınma |

: Tablo 5. Ürünlere uygulanacak performans testleri (Ürün Listesi – Testler sayfası)

# 4. Bulgular ve Tartışma

Groutart Rapid ve Mastar 10 bölümleri ekibin önceki raporundan (GR ve M10 SKT, son hâl) değiştirilmeden alınmıştır. Macunart, İzolatex Plus ve Technopool bölümleri bu rapor için ham veriden hazırlanmıştır.
''')
A(eski_bolum())
# ---------------- MACUNART ----------------
u = 'Macunart'
A('''
### 4.3. Macunart

Macunart'ta baskın faz dolomittir (30,9° ve 41,1°); kalsit (29,4°), alit (32,2° ve 51,7°) ve belit (32,6°) de bulunmaktadır. XRD göstergeleri Tablo 6'da, FTIR göstergeleri Tablo 7'de verilmiştir.

#### Kuru harç

Dört numunenin difraktogramları birbirine çok yakındır (Şekil 13). Etrenjit (15–30) ve portlandit (18–45) gürültü düzeyinde, alit 225–254 aralığındadır. FTIR spektrumları üst üste çakışmakta, 3640 cm⁻¹ bandı görülmemekte ve Si–O bandı anhidrit alitin konumunda (~925 cm⁻¹) bulunmaktadır (Şekil 14). Hiçbir ambalajda ön hidratasyon saptanmamıştır.

"Macunart Ref Kuru Harç" adıyla kaydedilen ikinci XRD ölçümünde (9811) ise etrenjit 121, portlandit 718 olup alit neredeyse kalmamıştır (13). Bu desen sertleşmiş bir numuneye aittir. 28 günlük referans ölçümü de eksik olduğundan numunenin yanlış adlandırılmış olabileceği düşünülmektedir [DOĞRULANACAK]. Bu ölçüm değerlendirmeye alınmamıştır.
''')
A(sek(13, 'MA_XRD_K.png', 'Macunart – kuru harç XRD difraktogramları'))
A(sek(14, 'MA_FTIR_K.png', 'Macunart – kuru harç FTIR spektrumları (30 µm kuru harç FTIR ölçümü yoktur)'))
A('''
#### 1 gün

1. günde tüm numunelerde etrenjit ve portlandit oluşmuş, alit kuru harçtaki değerin yaklaşık dörtte birine inmiştir (Şekil 15). Portlandit Referansta %d, 12 µm'de %s; 20 µm (%d) ve 30 µm (%d) numunelerinde ise bunun yaklaşık yarısıdır. Etrenjit 30 µm'de %d, diğer numunelerde 145–154 aralığındadır. Kalan alit tüm numunelerde birbirine yakın olduğundan (43–60) fark klinker tüketiminde değil portlandit pikindedir.

FTIR'da 3640 cm⁻¹ bandı ve O–H alanı tekrar aralığı içinde kalmaktadır (Şekil 16). Si–O bandı Referansta 960 cm⁻¹, ambalaj numunelerinde 966–971 cm⁻¹ konumundadır.

1 günlük XRD sonuçlarına göre sıralama şöyledir:

12 µm ≈ Referans > 20 µm > 30 µm
''' % (x(u,'1','Ref','P'), nd(x(u,'1','12','P')), x(u,'1','20','P'), x(u,'1','30','P'), x(u,'1','30','E')))
A(sek(15, 'MA_XRD_1.png', 'Macunart – 1 günlük XRD difraktogramları'))
A(sek(16, 'MA_FTIR_1.png', 'Macunart – 1 günlük FTIR spektrumları'))
A('''
#### 7 gün

7. günde alit tüm numunelerde tükenmiştir (1–5; Şekil 17). Ambalaj numunelerinde etrenjit 145–147, portlandit 425–715 aralığında olup en yüksek portlandit 12 µm'dedir. Referansta ise etrenjit %d, portlandit %s; bu değerler hem ambalaj numunelerinin hem de Referansın 1 günlük değerinin altındadır. Referansın XRD (9864) ve FTIR (9871) ölçümleri diğer 7 günlük numunelerden çok sonra alındığı için ayrı bir karışımdan hazırlanmış olabilir [DOĞRULANACAK]. Bu nedenle Referans 7. günde karşılaştırmaya alınmamıştır.

FTIR'da 3640 cm⁻¹ bandı en belirgin 12 µm'de görülmekte, diğer göstergeler tekrar aralığında kalmaktadır (Şekil 18). Ambalaj numuneleri arasındaki fark küçüktür:

12 µm ≥ 30 µm ≈ 20 µm
''' % (x(u,'7','Ref','E'), nd(x(u,'7','Ref','P'))))
A(sek(17, 'MA_XRD_7.png', 'Macunart – 7 günlük XRD difraktogramları'))
A(sek(18, 'MA_FTIR_7.png', 'Macunart – 7 günlük FTIR spektrumları'))
A('''
#### 28 gün

28 günlük yaşta yalnızca 12 ve 30 µm'nin XRD (Şekil 19), 12 ve 20 µm'nin FTIR (Şekil 20) ölçümü bulunmaktadır. 12 ve 30 µm'de etrenjit 105 ve 98, portlandit 496 ve 435 olarak birbirine yakındır. 12 ve 20 µm'nin FTIR göstergeleri de tekrar aralığı içinde örtüşmektedir. Referans ve 20 µm XRD ile Referans ve 30 µm FTIR ölçümleri eksiktir [VERİ GEREKLİ].

Macunart kuru harcında ön hidratasyon izine rastlanmamıştır. 20 ve 30 µm'de 1. günde görülen portlandit farkı 7. günde kapanmış, 12 µm ise her yaşta Referansla aynı ya da daha yüksek değer vermiştir.
''')
A(sek(19, 'MA_XRD_28.png', 'Macunart – 28 günlük XRD difraktogramları'))
A(sek(20, 'MA_FTIR_28.png', 'Macunart – 28 günlük FTIR spektrumları'))
A(xrd_cizelge(u, 6, ek=('K2',)))
A(ftir_cizelge(u, 7))

# ---------------- İZOLATEX ----------------
u = 'İzolatex Plus'
A('''
### 4.4. İzolatex Plus

İzolatex Plus iki bileşenli bir ürün olup ambalaj değişikliği toz bileşeni kapsamaktadır. Kuru harçta kuvars (26,6° ve 20,9°) ile kalsit (29,4°) baskındır; alit ve belit de bulunmaktadır.

Hidrate numunelerin FTIR spektrumlarındaki 2950, 1730, 1160 ve 700 cm⁻¹ bantları sıvı bileşenin polimerine aittir ve stiren-akrilik bir dispersiyonla uyumludur [DOĞRULANACAK]. Bu bantlar 900–1200 cm⁻¹ Si–O bölgesiyle örtüştüğünden İzolatex Plus'ta C-S-H FTIR ile değerlendirilememiştir. Hidrate numunelerdeki 0,1–0,7°'lik kayma düzeltilmiştir (Bölüm 3.5); ancak esnek membran numuneleri düz bir yüzey oluşturmadığı için pik şiddetleri de etkilenmektedir. Göstergeler Tablo 8 ve 9'da verilmiştir.

"İzolatex 05.05.2026" adlı numuneler Referans olarak alınmıştır. 9725 numarası hem "1.gün" hem "1.gün 12 Mikron" dosyasında kullanıldığından ikincisi 12 µm sayılmıştır. 7 günlük 9807 FTIR numunesinde film kalınlığı yazmadığı için 12 µm varsayılmıştır (tabloda 12 µm*) [DOĞRULANACAK].

#### Kuru harç

Etrenjit (15–58) ve portlandit (10–45) tüm ambalajlarda gürültü düzeyindedir (Şekil 21). Alit Referansta %d, ambalaj numunelerinde %d–%d aralığındadır. Ancak 31,9–32,8° bölgesinin toplam alanı ambalaj numunelerinde düşük olmadığından alit farkı tane istatistiğine bağlanmıştır.

11,6°'deki alçı taşı piki ambalaj numunelerinde 41–68, Referansta 13'tür. Bu fark hemihidratın nemle alçı taşına dönüşmesinden ya da parti farkından kaynaklanabilir; mevcut verilerle ikisi ayırt edilememektedir [DOĞRULANACAK: Referansın üretim tarihi ve partisi]. Kuru harç FTIR ölçümü yoktur.
''' % (x(u,'K','Ref','A'), min(x(u,'K',a,'A') for a in ['12','20','30']), max(x(u,'K',a,'A') for a in ['12','20','30'])))
A(sek(21, 'IZ_XRD_K.png', 'İzolatex Plus – kuru harç XRD difraktogramları'))
A('''
#### 1 gün

1. günde hiçbir numunede belirgin etrenjit ya da portlandit oluşmamış (5–31), alit pikleri korunmuştur (Şekil 22). Polimer modifiyeli bu sistemde ilk gün az miktarda kristalin hidratasyon ürünü oluşmaktadır. 30 µm numunesinin zemini ile kalsit ve alit değerleri diğerlerinden yüksektir; bunun numune hazırlamadan kaynaklandığı düşünülmektedir. FTIR ölçümü yalnızca Referans ve 12 µm için vardır ve polimer bantları dışında fark görülmemektedir (Şekil 23).
''')
A(sek(22, 'IZ_XRD_1.png', 'İzolatex Plus – 1 günlük XRD difraktogramları'))
A(sek(23, 'IZ_FTIR_1.png', 'İzolatex Plus – 1 günlük FTIR spektrumları'))
A('''
#### 7 gün

7. günde portlandit oluşmaya başlamış, ancak değerler çok dağınık çıkmıştır: 12 µm %d, Referans %d, 20 µm %d, 30 µm %d (Şekil 24). Aynı 30 µm numunesinin ikinci ölçümünde (9844) portlandit %d, etrenjit %d bulunmuştur. Aynı ambalaj ve yaşta yaklaşık 10 katlık bu fark nedeniyle 7 günlük XRD sonuçları ambalaj sıralamasında kullanılmamıştır. FTIR'da 3640 cm⁻¹ bandı 12 µm* numunesinde %s, 30 µm ikinci ölçümde %s, Referansta %s mAbs olup tekrar aralıkları geniştir (Şekil 25).
''' % (x(u,'7','12','P'), x(u,'7','Ref','P'), x(u,'7','20','P'), x(u,'7','30','P'), x(u,'7b','30','P'), x(u,'7b','30','E'),
       fs(F[u+'|7|12?']['OH3640'][0],1), fs(F[u+'|7b|30']['OH3640'][0],1), fs(F[u+'|7|Ref']['OH3640'][0],1)))
A(sek(24, 'IZ_XRD_7.png', 'İzolatex Plus – 7 günlük XRD difraktogramları (30 µm için 9766 ölçümü gösterilmiştir)'))
A(sek(25, 'IZ_FTIR_7.png', 'İzolatex Plus – 7 günlük FTIR spektrumları'))
A('''
#### 28 gün

28. günde tüm numunelerde etrenjit ve portlandit oluşmuştur (Şekil 26). Portlandit 20 µm'de %d, 12 µm'de %d, Referansta %s; etrenjit ise 20 µm'de %d, Referansta %d, 12 µm'de %s. Kalan alit birbirine yakındır (30–48). FTIR'da Referans ve 12 µm neredeyse çakışmaktadır (3640 cm⁻¹: %s ve %s mAbs; Si–O: 963 ve 962 cm⁻¹; Şekil 27). 30 µm'nin 28 günlük ölçümü yoktur [VERİ GEREKLİ].

İzolatex Plus kuru harcında da ön hidratasyon izi bulunmamakla birlikte alçı taşı farkının ayrıca izlenmesi gerekir. 28. günde 12 ve 20 µm Referansla aynı ya da daha yüksek değer vermiştir. 1 ve 7 günlük veriler numune geometrisi ve tekrarlanabilirlik sorunları nedeniyle karar için kullanılmamalıdır.
''' % (x(u,'28','20','P'), x(u,'28','12','P'), nd(x(u,'28','Ref','P')), x(u,'28','20','E'), x(u,'28','Ref','E'), nd(x(u,'28','12','E')),
       fs(F[u+'|28|Ref']['OH3640'][0],1), fs(F[u+'|28|12']['OH3640'][0],1)))
A(sek(26, 'IZ_XRD_28.png', 'İzolatex Plus – 28 günlük XRD difraktogramları'))
A(sek(27, 'IZ_FTIR_28.png', 'İzolatex Plus – 28 günlük FTIR spektrumları'))
A(xrd_cizelge(u, 8, ek=('7b',)))
A(ftir_cizelge(u, 9, ek=('7b',)))

# ---------------- TECHNOPOOL ----------------
u = 'Technopool'
A('''
### 4.5. Technopool

Technopool'da kuvars (26,6°) ve feldispat (27,6–28,0°) baskın olup kalsit, alit ve belit de bulunmaktadır. Bu üründe 30 µm ambalaj test edilmemiştir. Kum içeriği nedeniyle FTIR'daki Si–O bölgesi kuvarsın ~1080 cm⁻¹ bandıyla örtüşmektedir. Göstergeler Tablo 10 ve 11'de verilmiştir.

#### Kuru harç

Etrenjit (33–44) ve portlandit (11–26) üç numunede de gürültü düzeyindedir (Şekil 28). Alit ambalaj numunelerinde Referanstan düşük değildir (Referans %d, 12 µm %d, 20 µm %d). Ön hidratasyon saptanmamıştır. Kuru harç FTIR ölçümü yoktur.
''' % (x(u,'K','Ref','A'), x(u,'K','12','A'), x(u,'K','20','A')))
A(sek(28, 'TP_XRD_K.png', 'Technopool – kuru harç XRD difraktogramları'))
A('''
#### 1 gün

1. günde Referansın portlandit değeri (%d), 12 µm (%d) ve 20 µm (%d) numunelerinin yaklaşık iki katıdır (Şekil 29). Etrenjit de aynı sırayı izlemektedir (%d, %d ve %d). 12 µm'de kalan alitin (%d) Referanstan (%d) yüksek olması, bu numunede silikat hidratasyonunun bir miktar geride olduğunu göstermektedir.

FTIR'da O–H alanı ambalaj numunelerinde daha yüksek görünmektedir (Şekil 30). Ancak Si–O bandı kuvarsla örtüştüğü ve tekrarlar arasında geniş aralıkta değiştiği için (12 µm'de 944–987 cm⁻¹) FTIR'dan sıralama yapılmamıştır. XRD sonuçlarına göre sıralama şöyledir:

Referans > 12 µm ≥ 20 µm
''' % (x(u,'1','Ref','P'), x(u,'1','12','P'), x(u,'1','20','P'), x(u,'1','Ref','E'), x(u,'1','12','E'), x(u,'1','20','E'), x(u,'1','12','A'), x(u,'1','Ref','A')))
A(sek(29, 'TP_XRD_1.png', 'Technopool – 1 günlük XRD difraktogramları'))
A(sek(30, 'TP_FTIR_1.png', 'Technopool – 1 günlük FTIR spektrumları'))
A('''
#### 7 gün

7. günde alit büyük ölçüde tükenmiştir (Şekil 31). Portlandit Referansta %d, 12 µm'de %d, 20 µm'de %s; Referans ambalaj numunelerinden yaklaşık %%%s yüksektir. Etrenjit de aynı sıradadır (%d, %d ve %d). FTIR'daki O–H alanı da Referansta (%s) 12 µm (%s) ve 20 µm (%s) numunelerinden yüksek olup XRD sonucuyla uyumludur (Şekil 32).

20 µm numunesinin 7 günlük durdurulmamış ölçümünde (9741) portlandit %d, etrenjit %d; durdurulmuş ölçümünde (9742) ise %d ve %s. Durdurma yapılmayan numunede portlandit yaklaşık %%%s, etrenjit %%%s daha yüksektir; yani hidratasyon numune alındıktan sonra da sürmektedir. Durdurma işleminin tüm yaşlarda aynı şekilde uygulanması gerekir.
''' % (x(u,'7','Ref','P'), x(u,'7','12','P'), nd(x(u,'7','20','P')), yuzde(x(u,'7','Ref','P'), (x(u,'7','12','P')+x(u,'7','20','P'))/2),
       x(u,'7','Ref','E'), x(u,'7','12','E'), x(u,'7','20','E'),
       bs(F[u+'|7|Ref']['H2O_alan'][0]), bs(F[u+'|7|12']['H2O_alan'][0]), bs(F[u+'|7|20']['H2O_alan'][0]),
       x(u,'7nd','20','P'), x(u,'7nd','20','E'), x(u,'7','20','P'), nd(x(u,'7','20','E')),
       yuzde(x(u,'7nd','20','P'), x(u,'7','20','P')), yuzde(x(u,'7nd','20','E'), x(u,'7','20','E'))))
A(sek(31, 'TP_XRD_7.png', 'Technopool – 7 günlük XRD difraktogramları (20 µm: durdurulmuş numune)'))
A(sek(32, 'TP_FTIR_7.png', 'Technopool – 7 günlük FTIR spektrumları'))
A('''
#### 28 gün

28. günde portlandit Referansta %d, 12 µm'de %d, 20 µm'de %s; etrenjit Referansta %d, 12 ve 20 µm'de %s (Şekil 33). Tüm numunelerde 11,7° civarında bir AFm piki (muhtemelen monokarbonat) oluşmuştur. 28 günlük FTIR ölçümü yalnızca 12 µm için bulunmaktadır (Şekil 34) [VERİ GEREKLİ: Referans ve 20 µm].

Technopool kuru harcında ön hidratasyon izi görülmemesine karşın Referans 1, 7 ve 28. günlerin tamamında en yüksek portlandit ve etrenjit değerlerini vermiştir. 12 µm 28. günde Referansa yaklaşmış, 20 µm ise geride kalmıştır. Bu farkın XRD'de görünmeyen amorf ya da yüzeysel bir ön hidratasyondan mı, yoksa parti veya numune farkından mı kaynaklandığı mevcut verilerle belirlenememektedir. Bu nedenle Technopool'da yapışma dayanımı ve açık bekletme süresi sonuçlarına bakılması gerekir.
''' % (x(u,'28','Ref','P'), x(u,'28','12','P'), nd(x(u,'28','20','P')), x(u,'28','Ref','E'), nd(x(u,'28','12','E'))))
A(sek(33, 'TP_XRD_28.png', 'Technopool – 28 günlük XRD difraktogramları'))
A(sek(34, 'TP_FTIR_28.png', 'Technopool – 28 günlük FTIR spektrumu (yalnızca 12 µm)'))
A(xrd_cizelge(u, 10, ek=('7nd',)))
A(ftir_cizelge(u, 11))


# ---------------- SONUÇLAR ----------------
A('''
# 5. Sonuçlar

Macunart, İzolatex Plus ve Technopool'un XRD göstergeleri Şekil 35'te, beş ürünün özeti Tablo 12'de verilmiştir.
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

: Tablo 12. Ürün bazında özet (*önceki rapordan; bu ürünlerin kuru harç ölçümü raporda yoktur)

Macunart, İzolatex Plus ve Technopool kuru harçlarının hiçbirinde etrenjit ya da portlandit oluşmamış ve alit korunmuştur; Macunart'ta FTIR sonuçları da aynı yöndedir. Bununla birlikte XRD kristalin fazları genellikle yaklaşık %1'in üzerinde saptayabildiğinden, nemden en çok etkilenen C₃A ve serbest kireçteki yüzeysel değişimler {c:dubina} ile amorf ön hidratasyon ürünleri bu yöntemle görülmeyebilir.

Ambalajın hidratasyona etkisi ürüne göre değişmektedir. Bütün ürünlerde kötü sonuç veren tek bir ambalaj tipi olmadığı gibi film kalınlığı arttıkça sonuçların iyileştiği bir eğilim de görülmemiştir. Bu sonuç, WVTR'nin film kalınlığıyla her zaman ters orantılı olmadığı bilgisiyle {c:astmf1249} birlikte, torbaların bariyer performansının kalınlık yerine ölçülmüş WVTR değerleriyle karşılaştırılması gerektiğini göstermektedir. Numuneler arasındaki farkların bir kısmı numune hazırlama ve ölçüm değişkenliğinden de kaynaklanıyor olabilir.

Referansın her yaşta önde olduğu tek ürün Technopool'dur ve bu üründe 20 µm 28. günde de geride kalmıştır.

Projenin hedefi açısından ara bulgular şöyledir. Macunart ve İzolatex Plus'ta 12 ve 20 µm ambalajların, 2 yıllık depolamaya karşılık kabul edilen yaşlandırmadan sonra ön hidratasyona yol açtığını gösteren mineralojik bir bulgu yoktur; bu iki üründe mikroyapı verileri ambalaj bariyerinin revize edilmesini gerektirmemektedir. Technopool ise ambalaj bariyerinin yeniden değerlendirilmesi gerekebilecek tek üründür ve bu üründe karar performans testlerine göre verilmelidir. 2025 çalışmasında neme en duyarlı ürünlerin CAC içeren ikili ve üçlü sistemler olduğu görülmüştür {c:kalekim2025}. Bu nedenle bariyer revizyonu değerlendirmesinde öncelik CAC içeren ürünlere verilmelidir.

Sonuçlar henüz iklim profiline göre ayrıştırılamamaktadır. Numunelerin hangi profile tabi tutulduğu kayıtlarda yer almamakta ve bu raporda her ürün için tek bir yaşlandırma süresi bulunmaktadır. Farklı pazarlar için SKT önerisi verebilmek amacıyla her ürünün sıcak ve soğuk profillerde ayrı ayrı ve birden fazla yaşlandırma süresinde test edilmesi gerekir. SKT kararı ayrıca Tablo 5'teki performans testlerinin Referansla karşılaştırmalı sonuçlarına dayanmalıdır [VERİ GEREKLİ].

# 6. Öneriler ve Gelecek Çalışmalar

- Her numunenin hangi iklim profiline tabi tutulduğu kayda geçirilmeli; sıcak ve soğuk profiller aynı ürün ve ambalajda ayrı ayrı uygulanmalıdır.
- SKT'nin süreye bağlı değişimini görebilmek için ara yaşlandırma süreleri (örneğin 6 ve 12 ay eşdeğeri) eklenmeli ve "45 gün = 2 yıl" eşdeğerliği gerçek zamanlı depolanan numunelerle doğrulanmalıdır {c:astmf1980}.
- Ambalaj bariyer revizyonuna temel oluşturmak için Referans ambalajın yapısı belirlenmeli ve tüm torbaların WVTR değerleri ölçülmelidir {c:astmf1249}.
- Eksik ölçümler tamamlanmalıdır: Macunart 28 gün Referans ve 20 µm XRD; Technopool 28 gün Referans ve 20 µm FTIR; İzolatex Plus 28 gün 30 µm XRD ve FTIR; İzolatex Plus ve Technopool kuru harç FTIR.
- Kuru harçlarda 40–200 °C (bağlı su) ve 400–500 °C (portlandit) kütle kayıpları TGA ile Referansla karşılaştırmalı ölçülmelidir. TGA, XRD'de görünmeyen amorf ön hidratasyonu da yansıtır {c:scrivener2016}.
- Neme en duyarlı fazlar olan C₃A (kübik ve ortorombik), alçı taşı, basanit ve anhidrit kuru harçlarda Rietveld analiziyle belirlenmelidir {c:dubina,scrivener2004}.
- XRD en az iki bağımsız numuneyle tekrarlanmalı, agregalı ürünlerde numune 63 µm altına öğütülmeli ya da elenmeli, İzolatex Plus gibi esnek numunelerde yüzey tutucu seviyesine getirilmelidir.
- Tüm yaşlarda aynı durdurma talimatı (AG_YK_TL_0397) uygulanmalıdır. RILEM önerisindeki izopropanol ile solvent değişimi {c:snellings} talimatla karşılaştırmalı olarak denenebilir.

# Kaynakça
''')

# ---------- atıfları numaralandır ----------
_t = '\n'.join(MD)
_sira = []
def _num(m):
    out = []
    for k in m.group(1).split(','):
        k = k.strip()
        if k not in _sira: _sira.append(k)
        out.append(_sira.index(k) + 1)
    return '[' + ', '.join(map(str, sorted(out))) + ']'
_t = re.sub(r'\{c:([^}]+)\}', _num, _t)
_t += '\n' + '\n\n'.join('[%d] %s' % (i + 1, KAYNAK[k]) for i, k in enumerate(_sira)) + '\n'
_t += '''
# Ek A. Veri Dosyaları

Ham veriler `veri/xrd/` ve `veri/ftir/` klasörlerinde, hesaplanan göstergeler `sekiller/gostergeler.json` dosyasında, grafikleri ve tabloları üreten kodlar `kod/` klasöründe bulunmaktadır. Ölçüm numaraları Tablo 6–11'de verilmiştir; XRD ve FTIR ölçüm numaraları birbirinden bağımsızdır.
'''
kullanilmayan = set(KAYNAK) - set(_sira)
assert not kullanilmayan, kullanilmayan
_t = re.sub(r'(?m)^(\d+)\. (?=[a-zçğıöşü])', r'\1\\. ', _t)  # "7. günde" liste sanılmasın
open('SKT_Proje_Raporu.md', 'w', encoding='utf8').write(_t)
print('ok', len(_sira), 'kaynak')
