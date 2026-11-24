import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from veri import read_rd, read_csv, BASE
from katalog import XRD, FTIR, X
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,
                 'axes.edgecolor':'#8a8984','axes.labelcolor':'#0b0b0b','xtick.color':'#52514e','ytick.color':'#52514e'})
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
REN={'Ref':'#3b3a37','12':'#2a78d6','20':'#eb6834','30':'#1baf7a','12?':'#2a78d6'}
ETK={'Ref':'Referans','12':'12 µm','20':'20 µm','30':'30 µm','12?':'12 µm*'}
SIRA=['Ref','12','12?','20','30']
YAS={'K':'Kuru harç',1:'1 günlük',7:'7 günlük',28:'28 günlük'}
def no(f): return os.path.basename(f).split('-')[0].strip()
# ---------------- XRD ----------------
FAZ=[  # (2θ, kısaltma)
 (9.09,'E'),(15.8,'E'),(11.6,'G'),(14.7,'Bs'),(18.05,'P'),(34.1,'P'),(47.1,'P'),
 (29.4,'Cc'),(39.4,'Cc'),(30.95,'D'),(41.1,'D'),(26.64,'Q'),(20.86,'Q'),(27.9,'F'),
 (32.2,'A'),(32.6,'Bl'),(51.7,'A')]
PEN={'E':(8.7,9.5),'P':(17.7,18.4),'Cc':(29.15,29.7),'A':(51.45,52.0),'G':(11.4,11.85),'B':(14.5,14.95),'K32':(31.9,32.85)}
def net_alan(tt,y,a,b):
    m=(tt>=a)&(tt<=b); x=tt[m]; v=y[m]
    k=3; bl=np.interp(x,[x[:k].mean(),x[-k:].mean()],[v[:k].mean(),v[-k:].mean()])
    return float(np.trapezoid(np.clip(v-bl,0,None),x))
xrd_tab={}; kayma={}
IC={'Macunart':30.94,'İzolatex Plus':26.64,'Technopool':26.64}
def hizala(urun,tt,y,n):
    # numune yüksekliği kaynaklı kaymayı iç standart pikle (dolomit 104 / kuvars 101) düzelt: Δ2θ = k·cosθ
    t0=IC[urun]; m=(tt>t0-0.9)&(tt<t0+0.9); i=np.argmax(y[m]); x=tt[m][i-3:i+4]; w=y[m][i-3:i+4]
    tp=float((x*w).sum()/w.sum()); k=(tp-t0)/np.cos(np.radians(t0/2))
    kayma[n]=round(tp-t0,3)
    return tt-k*np.cos(np.radians(tt/2))
def xrd_fig(urun,yas,anahtarlar,dosya,baslik):
    seri=[]
    for amb in SIRA:
        k=(urun,yas,amb)
        if k in anahtarlar:
            f=BASE+X+XRD[k][0]; tt,y,_=read_rd(f); tt=hizala(urun,tt,y,no(f)); seri.append((amb,no(f),tt,y))
    if not seri: return None
    fig=plt.figure(figsize=(7.2,5.6),dpi=200)
    gs=fig.add_gridspec(2,3,height_ratios=[2.3,1],hspace=0.38,wspace=0.28)
    ax=fig.add_subplot(gs[0,:])
    ymax=max(np.percentile(s[3],99.7) for s in seri); off=0.55*ymax
    for i,(amb,n,tt,y) in enumerate(seri):
        ax.plot(tt,y+i*off,color=REN[amb],lw=0.6)
        ax.text(65.6,np.median(y[-80:])+i*off,'%s (%s)'%(ETK[amb],n),color='#0b0b0b',fontsize=7.5,va='center')
    top=(len(seri)-1)*off+ymax*1.02
    ax.set_ylim(0,top); ax.set_xlim(5,65)
    for j,(t,l) in enumerate(sorted(FAZ)):
        ax.axvline(t,color='#c3c2b7',lw=0.4,ls=':',zorder=0)
        ax.text(t,1.005+0.035*(j%2),l,fontsize=6,ha='center',va='bottom',color='#52514e',transform=ax.get_xaxis_transform())
    ax.set_xlabel('2θ (°, Cu Kα; numune yüksekliği kayması düzeltilmiş)'); ax.set_ylabel('Şiddet (k.b., kaydırılmış)'); ax.set_yticks([])
    ax.set_title(baslik,fontsize=10,loc='left',color='#0b0b0b',pad=18)
    for j,(a,b,ad) in enumerate([(8.2,12.2,'Etrenjit / AFm / alçı'),(17.4,18.7,'Portlandit (001)'),(31.6,33.0,'Alit / belit')]):
        az=fig.add_subplot(gs[1,j])
        for amb,n,tt,y in seri:
            m=(tt>=a)&(tt<=b); az.plot(tt[m],y[m],color=REN[amb],lw=1.0,label=ETK[amb])
        az.set_title(ad,fontsize=8,color='#52514e'); az.set_yticks([]); az.tick_params(labelsize=7)
        if j==2: az.legend(fontsize=6.5,frameon=False,loc='upper left',bbox_to_anchor=(1.0,1.0))
    fig.text(0.01,0.005,'E: etrenjit, G: alçı taşı, Bs: basanit, P: portlandit, Cc: kalsit, D: dolomit, Q: kuvars, F: feldispat, A: alit (C₃S), Bl: belit (C₂S)',fontsize=6,color='#52514e')
    fig.savefig(dosya,bbox_inches='tight'); plt.close(fig)
    for amb,n,tt,y in seri:
        xrd_tab[(urun,str(yas),amb)]={'no':n,**{p:round(net_alan(tt,y,*w)) for p,w in PEN.items()}}
    return [s[1] for s in seri]
# ---------------- FTIR ----------------
def absorb(T): return -np.log10(np.clip(T,1,None)/100)
def hb(x,A,a,b,c):  # c civarındaki yüksekliği [a,b] doğrusal taban çizgisine göre
    ia,ib=np.argmin(abs(x-a)),np.argmin(abs(x-b)); ic=(x<=max(c+6,c-6))&(x>=c-6)
    bl=np.interp(x[ic],[x[ib],x[ia]],[A[ib],A[ia]]) if x[ib]<x[ia] else np.interp(x[ic],[x[ia],x[ib]],[A[ia],A[ib]])
    return float((A[ic]-bl).max())
def alan(x,A,a,b):
    m=(x>=min(a,b))&(x<=max(a,b)); xx=x[m][::-1]; AA=A[m][::-1]
    bl=np.interp(xx,[xx[0],xx[-1]],[AA[0],AA[-1]]); return float(np.trapezoid(np.clip(AA-bl,0,None),xx))
def silo_min(x,T,a=900,b=1060):
    m=(x>=a)&(x<=b); return float(x[m][np.argmin(T[m])])
DOLGU={'Macunart':(745,705,728),'İzolatex Plus':(820,760,778),'Technopool':(820,760,778)}
ftir_tab={}
def ftir_gosterge(urun,x,T):
    A=absorb(T); ref=1/1000.0  # mAbs
    return {'OH3640':hb(x,A,3660,3620,3642)/ref,'H2O_alan':alan(x,A,3750,2700)/ref,'HOH1640':hb(x,A,1700,1580,1640)/ref,
            'SO4_1110':hb(x,A,1160,1060,1110)/ref if urun=='Macunart' else float('nan'),
            'SiO_min':silo_min(x,T),'CO3_1420':hb(x,A,1560,1300,1420)/ref,'ref':ref}
def ftir_fig(urun,yas,anahtarlar,dosya,baslik):
    seri=[]
    for amb in SIRA:
        k=(urun,yas,amb)
        if k in anahtarlar:
            ys=[];g=[]
            for f in FTIR[k]:
                x,T=read_csv(f); ys.append(T); g.append(ftir_gosterge(urun,x,T))
            seri.append((amb,no(FTIR[k][0]),x,np.mean(ys,0),g))
    if not seri: return None
    fig,axs=plt.subplots(1,2,figsize=(7.2,3.4),dpi=200,gridspec_kw={'width_ratios':[1.6,1],'wspace':0.18})
    for amb,n,x,T,g in seri:
        lab='%s (%s, n=%d)'%(ETK[amb],n,len(g))
        axs[0].plot(x,T,color=REN[amb],lw=0.9,label=lab); m=(x<=1300)
        axs[1].plot(x[m],T[m],color=REN[amb],lw=1.0)
        ftir_tab[(urun,str(yas),amb)]={'no':n,'n':len(g),**{k:[float(np.mean([gg[k] for gg in g])),float(np.min([gg[k] for gg in g])),float(np.max([gg[k] for gg in g]))] for k in g[0]}}
    for ax in axs: ax.invert_xaxis(); ax.set_xlabel('Dalga sayısı (cm⁻¹)')
    axs[0].set_xlim(4000,650); axs[1].set_xlim(1300,650); axs[0].set_ylabel('Geçirgenlik (%T)')
    yl=axs[0].get_ylim()
    for c,l in [(3640,'Ca(OH)₂'),(3400,'O–H'),(1640,'H–O–H'),(1420,'CO₃²⁻'),(1110,'SO₄²⁻'),(970,'Si–O')]:
        axs[0].axvline(c,color='#c3c2b7',lw=0.5,ls=':',zorder=0); axs[0].text(c,1.01,l,fontsize=6,rotation=90,va='bottom',ha='center',color='#52514e',transform=axs[0].get_xaxis_transform())
    for c,l in [(1110,'SO₄²⁻ (Et)'),(970,'Si–O (C-S-H)'),(920,'Si–O (alit)'),(875,'CO₃²⁻'),(797,'Q'),(728,'D')]:
        axs[1].axvline(c,color='#c3c2b7',lw=0.5,ls=':',zorder=0); axs[1].text(c,1.01,l,fontsize=5.5,rotation=90,va='bottom',ha='center',color='#52514e',transform=axs[1].get_xaxis_transform())
    axs[0].legend(fontsize=6.5,frameon=False,loc='lower left'); 
    fig.suptitle(baslik,fontsize=10,x=0.01,y=1.13,ha='left',color='#0b0b0b')
    fig.savefig(dosya,bbox_inches='tight'); plt.close(fig)
    return [s[1] for s in seri]
sekil=[]
for urun,kod in [('Macunart','MA'),('İzolatex Plus','IZ'),('Technopool','TP')]:
    for yas in ['K',1,7,28]:
        r=xrd_fig(urun,yas,XRD,f'{OUT}/{kod}_XRD_{yas}.png',f'{urun} – {YAS[yas]} XRD difraktogramları')
        if r: sekil.append(('XRD',urun,yas,f'{kod}_XRD_{yas}.png',r))
        r=ftir_fig(urun,yas,FTIR,f'{OUT}/{kod}_FTIR_{yas}.png',f'{urun} – {YAS[yas]} FTIR spektrumları')
        if r: sekil.append(('FTIR',urun,yas,f'{kod}_FTIR_{yas}.png',r))
# ek numuneler (tablo için)
for k in [('Macunart','K2','Ref'),('İzolatex Plus','7b','30'),('Technopool','7nd','20')]:
    tt,y,_=read_rd(BASE+X+XRD[k][0]); tt=hizala(k[0],tt,y,no(XRD[k][0])); xrd_tab[(k[0],str(k[1]),k[2])]={'no':no(XRD[k][0]),**{p:round(net_alan(tt,y,*w)) for p,w in PEN.items()}}
x,T=None,None
g=[ftir_gosterge('İzolatex Plus',*read_csv(f)) for f in FTIR[('İzolatex Plus','7b','30')]]
ftir_tab[('İzolatex Plus','7b','30')]={'no':'9880','n':len(g),**{k:[float(np.mean([gg[k] for gg in g])),float(min(gg[k] for gg in g)),float(max(gg[k] for gg in g))] for k in g[0]}}
json.dump({'sekil':sekil,'xrd':{'|'.join(k):v for k,v in xrd_tab.items()},'ftir':{'|'.join(k):v for k,v in ftir_tab.items()},'kayma':kayma},open(f'{OUT}/gostergeler.json','w'),ensure_ascii=False,indent=1)
print(len(sekil),'şekil')
