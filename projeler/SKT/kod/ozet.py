import json,sys,numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#8a8984','xtick.color':'#52514e','ytick.color':'#52514e'})
d=json.load(open(sys.argv[1]))['xrd']
REN={'Ref':'#3b3a37','12':'#2a78d6','20':'#eb6834','30':'#1baf7a'}; ETK={'Ref':'Referans','12':'12 µm','20':'20 µm','30':'30 µm'}
MRK={'Ref':'s','12':'o','20':'^','30':'D'}
Y=['K','1','7','28']; YL=['Kuru\nharç','1 gün','7 gün','28 gün']
fig,axs=plt.subplots(3,3,figsize=(7.4,7.2),dpi=200,sharex=True)
for i,u in enumerate(['Macunart','İzolatex Plus','Technopool']):
    for j,(p,ad) in enumerate([('P','Portlandit (18,0°)'),('E','Etrenjit (9,1°)'),('A','Alit (51,7°)')]):
        ax=axs[i,j]
        for amb in ['Ref','12','20','30']:
            xs=[];ys=[]
            for k,yas in enumerate(Y):
                v=d.get('%s|%s|%s'%(u,yas,amb))
                if v: xs.append(k); ys.append(v[p])
            if xs: ax.plot(xs,ys,color=REN[amb],lw=1.6,marker=MRK[amb],ms=5,mec='white',mew=0.8,label=ETK[amb])
        ax.set_xticks(range(4)); ax.set_xticklabels(YL); ax.grid(axis='y',color='#e6e5e0',lw=0.6); ax.set_ylim(bottom=0)
        if i==0: ax.set_title(ad,fontsize=9,color='#0b0b0b')
        if j==0: ax.set_ylabel(u+'\nnet pik alanı (k.b.)',fontsize=8.5)
axs[0,2].legend(frameon=False,fontsize=7.5,loc='upper right')
fig.tight_layout(); fig.savefig(sys.argv[2],bbox_inches='tight')
