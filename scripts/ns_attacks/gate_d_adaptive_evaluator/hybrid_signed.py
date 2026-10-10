"""Adaptive signed scalene diagnostic. No coefficient magnitude threshold."""
import numpy as np
from fast_signed import fast_scalene

def hybrid_scalene(vh,L,K=0,N=None,*,max_pairs=150000,return_meta=False):
    a=np.asarray(vh)
    if a.ndim!=4 or a.shape[0]!=3 or len(set(a.shape[1:]))!=1:
        raise ValueError('Expected Fourier array (3,n,n,n)')
    n=a.shape[1]
    if N is not None and N>=n/3: raise ValueError('N must be < n/3')
    m=np.rint(np.fft.fftfreq(n)*n).astype(int)
    mx,my,mz=np.meshgrid(m,m,m,indexing='ij')
    r2=mx*mx+my*my+mz*mz
    mask=r2>K*K
    if N is not None: mask &= r2<=N*N
    idx=np.argwhere(mask & np.any(a!=0,axis=0))
    count=len(idx)
    if count*count>max_pairs:
        val=fast_scalene(a,L,K,N)
        return (val,{'method':'fft_shell','occupied_modes':count}) if return_meta else val
    coeff={tuple(int(m[i]) for i in ix):a[:,ix[0],ix[1],ix[2]]/n**3 for ix in idx}
    alpha=2*np.pi/L
    transfer=0.
    for p,up in coeff.items():
        for q,uq in coeff.items():
            k=tuple(p[i]+q[i] for i in range(3))
            uk=coeff.get(k)
            if uk is None:continue
            ap=sum(x*x for x in p); bq=sum(x*x for x in q); ck=sum(x*x for x in k)
            if len({ap,bq,ck})!=3:continue
            transfer+=-np.real(1j*alpha**3*ck*np.dot(q,up)*np.dot(uq,np.conj(uk)))
    val=float(L**3*transfer)
    return (val,{'method':'sparse_ordered','occupied_modes':count}) if return_meta else val
