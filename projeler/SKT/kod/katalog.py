# (ürün, yaş, ambalaj) -> dosya listesi. Yaş: 'K' kuru harç, 1, 7, 28
X='/xrd/'
XRD={
 ('Macunart','K','Ref'):['Macunart/9803-Macunart Ref KURU HARC.rd'],
 ('Macunart','K2','Ref'):['Macunart/9811-Macunart Ref Kuru Har#U00e7.rd'],
 ('Macunart','K','12'):['Macunart/9804-Macunart 12 mic KURU HARC.rd'],
 ('Macunart','K','20'):['Macunart/9805-Macunart 20 mic KURU HARC.rd'],
 ('Macunart','K','30'):['Macunart/98066-Macunart 30 mic KURU HARC.rd'],
 ('Macunart',1,'Ref'):['Macunart/9785-Macunart Ref 1 Gun.rd'],
 ('Macunart',1,'12'):['Macunart/9786-Macunart 12 1 Gun.rd'],
 ('Macunart',1,'20'):['Macunart/9787- Macunart 20 mic 1.g#U00fcn.rd'],
 ('Macunart',1,'30'):['Macunart/9788-Macunart 30 mic 1.g#U00fcn.rd'],
 ('Macunart',7,'Ref'):['Macunart/9864-Macunart Ref 7 Gun.rd'],
 ('Macunart',7,'12'):['Macunart/9795- Macunart 12 mic 7.g#U00fcn.rd'],
 ('Macunart',7,'20'):['Macunart/9794- Macunart 20 mic 7.g#U00fcn.rd'],
 ('Macunart',7,'30'):['Macunart/9798-Macunart 30 mic 7.g#U00fcn.rd'],
 ('Macunart',28,'12'):['Macunart/9827- Macunart 12 mic 28.g#U00fcn.rd'],
 ('Macunart',28,'30'):['Macunart/9858-Macunart 30 mic 28.g#U00fcn.rd'],
 ('İzolatex Plus','K','Ref'):['#U0130zolatex/9736-Izolatex 05.05.2026.rd'],
 ('İzolatex Plus','K','12'):['#U0130zolatex/9733-Izolatex Plus 12 Mic.rd'],
 ('İzolatex Plus','K','20'):['#U0130zolatex/9732-Izolatex Plus 20 Mic.rd'],
 ('İzolatex Plus','K','30'):['#U0130zolatex/9731-Izolatex Plus 30 Mic.rd'],
 ('İzolatex Plus',1,'Ref'):['#U0130zolatex/9725-Izolatex 05.05.2026 1.gun.rd'],
 ('İzolatex Plus',1,'12'):['#U0130zolatex/9725-Izolatex 05.05.2026 1.gun 12 Mikron.rd'],
 ('İzolatex Plus',1,'20'):['#U0130zolatex/9737-Izolatex plus 20 micron 1.gun.rd'],
 ('İzolatex Plus',1,'30'):['#U0130zolatex/9738-Izolatex plus 30micron 1.gun.rd'],
 ('İzolatex Plus',7,'Ref'):['#U0130zolatex/9752- Izolatex 05.05.2026 7.Gun.rd'],
 ('İzolatex Plus',7,'12'):['#U0130zolatex/9753- IzolatexPlus 12 mic 05.05.2026 7.Gun.rd'],
 ('İzolatex Plus',7,'20'):['#U0130zolatex/9765- IzolatexPlus 20 mic 7.Gun.rd'],
 ('İzolatex Plus',7,'30'):['#U0130zolatex/9766- IzolatexPlus 30 mic 7.Gun.rd'],
 ('İzolatex Plus',28,'30'):['#U0130zolatex/9844-Izolatex Plus 30 Mic 7.G#U00fcn.rd'],  # dosya adı '7.Gün'; ölçüm sırası ve değerler 28. günle uyumlu
 ('İzolatex Plus',28,'Ref'):['#U0130zolatex/9821-Izolatex 05.05.2026 28.gun.rd'],
 ('İzolatex Plus',28,'12'):['#U0130zolatex/9822-Izolatex Plus 12 Mic 05.05.2026 28.G#U00fcn.rd'],
 ('İzolatex Plus',28,'20'):['#U0130zolatex/9845-Izolatex Plus 20 Mic 28.gun.rd'],
 ('Technopool','K','Ref'):['Technopool/9744-Technopool Ref Kuru Har#U00e7.rd'],
 ('Technopool','K','12'):['Technopool/9708- Technopool 12 mic Kuru Harci 04.05.26.rd'],
 ('Technopool','K','20'):['Technopool/9709-Technopool 20 mic Kuru Harc.rd'],
 ('Technopool',1,'Ref'):['Technopool/9717-Technopool Ref 1 gun.rd'],
 ('Technopool',1,'12'):['Technopool/9712-Technopool 12 Micron 1.G#U00fcn.rd'],
 ('Technopool',1,'20'):['Technopool/9716- Technopool 20 mic 1.g#U00fcn.rd'],
 ('Technopool',7,'Ref'):['Technopool/9743-Technopool Ref 7 Gun.rd'],
 ('Technopool',7,'12'):['Technopool/9740-Technopool 12 Micron 7.G#U00fcn.rd'],
 ('Technopool',7,'20'):['Technopool/9742- Technopool 20 mic 7.g#U00fcn durdurulmus.rd'],
 ('Technopool','7nd','20'):['Technopool/9741- Technopool 20 mic 7.g#U00fcn durdurulmamis.rd'],
 ('Technopool',28,'Ref'):['Technopool/9812-Technopool Ref 28.g#U00fcn.rd'],
 ('Technopool',28,'12'):['Technopool/9819-Technopool 12 Micron 28.G#U00fcn.rd'],
 ('Technopool',28,'20'):['Technopool/9820- Technopool 20 mic 28.g#U00fcn durdurulmus.rd'],
}
import glob,os
_B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','veri','ftir')+'/'
def _f(no): return sorted(glob.glob(_B+no+'-*.csv'))
FTIR={
 ('Macunart','K','Ref'):_f('9843'),('Macunart','K','20'):_f('9844'),('Macunart','K','12'):_f('9845'),
 ('Macunart',1,'Ref'):_f('9865'),('Macunart',1,'12'):_f('9866'),('Macunart',1,'20'):_f('9867'),('Macunart',1,'30'):_f('9868'),
 ('Macunart',7,'Ref'):_f('9871'),('Macunart',7,'12'):_f('9839'),('Macunart',7,'20'):_f('9837'),('Macunart',7,'30'):_f('9840'),
 ('Macunart',28,'12'):_f('9873'),('Macunart',28,'20'):_f('9872'),
 ('İzolatex Plus',1,'Ref'):_f('9786'),('İzolatex Plus',1,'12'):_f('9787'),
 ('İzolatex Plus',7,'Ref'):_f('9806'),('İzolatex Plus',7,'12?'):_f('9807'),('İzolatex Plus',7,'30'):_f('9816'),('İzolatex Plus',28,'30'):_f('9880'),  # dosya adı '7.Gun'; ölçüm tarihi 05.06.2026 (28. gün ölçümleriyle aynı hafta)
 ('İzolatex Plus',28,'Ref'):_f('9860'),('İzolatex Plus',28,'12'):_f('9861'),
 ('Technopool',1,'Ref'):_f('9785'),('Technopool',1,'12'):_f('9783'),('Technopool',1,'20'):_f('9784'),
 ('Technopool',7,'Ref'):_f('9798'),('Technopool',7,'12'):_f('9793'),('Technopool',7,'20'):_f('9797'),
 ('Technopool',28,'12'):_f('9855'),
}
for k,v in FTIR.items(): assert v,k
