"""October 7 signed-scalene convention, direct O(m^2) reference evaluator.
Not yet reconciled with September 20 Gate D high-pass definition.
"""
import numpy as np

def signed_scalene_reference(vh, L, cutoff=None):
    """Compute -Re <P(v·grad v),-Delta v> restricted to distinct |k|².
    vh is unnormalized numpy FFT, shape (3,n,n,n). Normalized torus
    integral = average; physical cube integral = L**3 times average.
    cutoff optionally restricts all three Fourier legs to |k|>cutoff.
    Only use on small test fields (quadratic pair enumeration).
    """
    n=vh.shape[1]
    indices=np.argwhere(np.max(np.abs(vh),axis=0)>1e-9)
    ks=np.rint(np.fft.fftfreq(n)*n).astype(int)
    modes={tuple(ks[i] for i in idx):vh[(slice(None),*idx)]/n**3 for idx in indices}
    factor=2*np.pi/L
    result=0j
    for p,a in modes.items():
        ap=sum(i*i for i in p)
        if cutoff is not None and factor*np.sqrt(ap)<=cutoff:continue
        for q,b in modes.items():
            bq=sum(i*i for i in q)
            k=tuple(p[j]+q[j] for j in range(3))
            ck=sum(i*i for i in k)
            if len({ap,bq,ck})!=3:continue
            if cutoff is not None and (factor*np.sqrt(bq)<=cutoff or factor*np.sqrt(ck)<=cutoff):continue
            h=modes.get(k)
            if h is None:continue
            result+=-1j*(factor**3)*ck*np.dot(np.array(q),a)*np.vdot(h,b)
    return float(result.real*L**3)
