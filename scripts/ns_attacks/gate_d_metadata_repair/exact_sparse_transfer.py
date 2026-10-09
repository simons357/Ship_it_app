"""Exact rational signed scalene transfer for small represented binary64 Fourier fields.
Normalized torus, integer Fourier wavevectors. No FFT operations or float accumulation.
"""
from fractions import Fraction as F
import numpy as np

def frac_complex(z):
    return F(float(z.real)),F(float(z.imag))
def cmul(a,b):
    return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def dot_real(k,v):
    return sum((int(k[i])*v[i][0] for i in range(3)),F(0)),sum((int(k[i])*v[i][1] for i in range(3)),F(0))
def dot_complex(u,v):
    return tuple(map(sum,zip(*(cmul(x,y) for x,y in zip(u,v)))))
def transfer_exact(vh,*,K=0,N=None,max_modes=64,max_pairs=4096):
    a=np.asarray(vh)
    if a.ndim!=4 or a.shape[0]!=3 or len(set(a.shape[1:]))!=1 or not np.isfinite(a).all():
        raise ValueError("invalid input")
    n=a.shape[1]; m=np.rint(np.fft.fftfreq(n)*n).astype(int)
    modes={}
    for ix in np.argwhere(np.any(a!=0,axis=0)):
        p=tuple(int(m[i]) for i in ix);r2=sum(x*x for x in p)
        if r2<=K*K or (N is not None and r2>N*N):continue
        modes[p]=[(F(float(a[c,*ix].real))/n**3,F(float(a[c,*ix].imag))/n**3) for c in range(3)]
    if len(modes)>max_modes or len(modes)**2>max_pairs:raise MemoryError("exact sparse transfer resource limit")
    result=F(0)
    for p,up in modes.items():
        for q,uq in modes.items():
            k=tuple(p[i]+q[i] for i in range(3))
            uk=modes.get(k)
            if uk is None:continue
            ap=sum(x*x for x in p);bq=sum(x*x for x in q);ck=sum(x*x for x in k)
            if len({ap,bq,ck})!=3:continue
            qdot=dot_real(q,up)
            inner=dot_complex(uq,[(z[0],-z[1]) for z in uk])
            product=cmul(qdot,inner)
            # -Re(i * ck * product) = ck * Im(product)
            result+=ck*product[1]
    return result
