"""Exact fallback for small cancellation-sensitive fields; fail closed otherwise.
Certification applies only to arithmetic of represented Fourier coefficients.
"""
from fractions import Fraction
import numpy as np
from vorticity_signed import vorticity_scalene
from exact_sparse_transfer import transfer_exact

def evaluate(vh,L,K,N,*,max_exact_modes=64,max_exact_pairs=4096,
             cancellation_floor=1e-8):
    a=np.asarray(vh)
    if a.ndim!=4 or a.shape[0]!=3 or not np.isfinite(a).all():
        raise ValueError("Invalid Fourier array")
    n=a.shape[1]
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    k2=sum(x*x for x in np.meshgrid(modes,modes,modes,indexing="ij"))
    keep=(k2>K*K)&(k2<=N*N)
    count=int(np.count_nonzero(keep&np.any(a!=0,axis=0)))
    val,parts=vorticity_scalene(a,L,K,N,return_parts=True)
    scale=abs(parts["full"])+abs(parts["repeated"])
    # A magnitude-based heuristic alone misses internal cancellation.
    # Prefer exact evaluation whenever its explicit resource budget permits.
    if count<=max_exact_modes and count*count<=max_exact_pairs:
        exact=transfer_exact(a,K=K,N=N,max_modes=max_exact_modes,max_pairs=max_exact_pairs)
        factor=L**3*(2*np.pi/L)**3
        return dict(T_sc=float(exact)*factor,exact_normalized=str(exact),
                    status="exact_represented_coefficients",
                    sign="positive" if exact>0 else "negative" if exact<0 else "zero",
                    fast_value=val,fast_discrepancy=val-float(exact)*factor,
                    trajectory_certified=False)
    return dict(T_sc=None,fast_value=val,status="sign_unverified",
                sign="unknown",trajectory_certified=False,
                reason="Exact fallback exceeds mode/pair budget; no rigorous fast error bound")
