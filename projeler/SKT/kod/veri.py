import struct, glob, os, re, numpy as np
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','veri')
def read_rd(f):
    d=open(f,'rb').read()
    step,start,end=[struct.unpack_from('<d',d,o)[0] for o in (214,222,230)]
    raw=np.frombuffer(d[250:],dtype='<u2').astype(float)
    tt=start+step*np.arange(len(raw))
    return tt, raw**2/100.0, (start,end,step,len(raw))
def read_csv(f):
    rows=[]
    for ln in open(f,encoding='utf-8-sig',errors='ignore'):
        p=ln.strip().split(',')
        try: rows.append((float(p[0]),float(p[1])))
        except: pass
    a=np.array(rows); return a[:,0],a[:,1]
