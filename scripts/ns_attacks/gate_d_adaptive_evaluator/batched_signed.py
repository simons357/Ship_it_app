"""Batched repeated-radius FFT evaluator, preserving full-minus-repeated identity.
Explicit memory cap; no coefficient pruning. Research candidate, not production certified.
"""
import numpy as np
from fast_signed import fast_scalene

def batched_scalene(vh,L,K=0,N=None,*,batch_size=4,max_batch_bytes=256*1024**2,return_parts=False):
    vh=np.asarray(vh)
    if vh.ndim!=4 or vh.shape[0]!=3 or len(set(vh.shape[1:]))!=1:
        raise ValueError("vh must be (3,n,n,n)")
    n=vh.shape[1]
    if N is not None and N>=n/3: raise ValueError("N must be < n/3")
    if batch_size<1 or max_batch_bytes<=0: raise ValueError("invalid resource limits")
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    mx,my,mz=np.meshgrid(modes,modes,modes,indexing="ij")
    r2=mx*mx+my*my+mz*mz
    keep=r2>K*K
    if N is not None: keep &= r2<=N*N
    h=np.where(keep[None,...],vh,0)
    alpha=2*np.pi/L
    k=np.array([mx,my,mz])*alpha
    k2=r2*alpha**2
    norm=L**3/n**6
    def nonlinear(a):
        ax=np.fft.ifftn(a,axes=(-3,-2,-1))
        grad=np.fft.ifftn(1j*k[None,:,None,...]*a[:,None,...],axes=(-3,-2,-1))
        conv=np.einsum("bjxyz,bjixyz->bixyz",ax,grad,optimize=True)
        out=np.fft.fftn(conv,axes=(-3,-2,-1))
        dot=np.einsum("ixyz,bixyz->bxyz",k,out,optimize=True)
        out-=k[None,...]*dot[:,None,...]/np.where(k2==0,1,k2)[None,None,...]
        out[:,:,0,0,0]=0
        return -out
    full_rhs=nonlinear(h[None,...])[0]
    full=norm*np.vdot(full_rhs,k2[None,...]*h).real
    shells=np.unique(r2[keep])
    # Conservative estimate for stacked complex arrays incl. gradients and temporaries.
    bytes_per_shell=32*3*n**3*16
    if max_batch_bytes<bytes_per_shell:
        raise MemoryError(f"cap {max_batch_bytes} below estimated one-shell requirement {bytes_per_shell}")
    bsize=min(batch_size,max(1,max_batch_bytes//bytes_per_shell))
    repeated=0.
    for start in range(0,len(shells),bsize):
        chunk=shells[start:start+bsize]
        a=np.where((r2[None,None,...]==chunk[:,None,None,None,None]),h[None,...],0)
        rhs=nonlinear(a)
        weights=(k2[None,...]-alpha**2*chunk[:,None,None,None])
        repeated+=norm*np.einsum("bixyz,bixyz->",rhs.conj(),weights[:,None,...]*h[None,...],optimize=True).real
    val=float(full-repeated)
    if return_parts:
        return val,dict(full=float(full),repeated=float(repeated),shell_count=len(shells),batch_size=int(bsize),estimated_batch_bytes=int(bsize*bytes_per_shell))
    return val
