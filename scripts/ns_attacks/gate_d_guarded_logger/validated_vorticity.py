"""Validated research wrapper for the unchanged vorticity signed-transfer evaluator.
Error indicators are NOT rigorous forward bounds or production authorization.
"""
import numpy as np
from vorticity_signed import vorticity_scalene

def evaluate_checked(vh, L, K, N, *, max_work_bytes=512*1024**2,
                     symmetry_rtol=1e-11, divergence_rtol=1e-11,
                     cancellation_limit=1e10):
    a=np.asarray(vh)
    if a.ndim != 4 or a.shape[0] != 3 or len(set(a.shape[1:])) != 1:
        raise ValueError("Expected complex Fourier coefficients (3,n,n,n)")
    n=a.shape[1]
    if not np.issubdtype(a.dtype,np.complexfloating):
        raise ValueError("Expected complex Fourier coefficients")
    if not np.isfinite(a).all():
        raise ValueError("Nonfinite Fourier coefficients")
    if not (np.isfinite(L) and L>0 and isinstance(N,(int,np.integer)) and
            isinstance(K,(int,np.integer)) and 0<=K<N<n/3):
        raise ValueError("Require L>0 and integer 0<=K<N<n/3")
    # Conservative working-set *estimate*, not a hard bound on FFT library allocation.
    estimated=320*n**3
    if estimated>max_work_bytes:
        raise MemoryError(f"Estimated working set {estimated} exceeds cap {max_work_bytes}")
    idx=(-np.arange(n))%n
    partner=np.conj(a[:,idx[:,None,None],idx[None,:,None],idx[None,None,:]])
    scale=max(1.,float(np.max(np.abs(a))))
    hermitian_residual=float(np.max(np.abs(a-partner)))/scale
    if hermitian_residual>symmetry_rtol:
        raise ValueError(f"Hermitian symmetry residual {hermitian_residual}")
    modes=np.rint(np.fft.fftfreq(n)*n)
    mx,my,mz=np.meshgrid(modes,modes,modes,indexing="ij")
    div=mx*a[0]+my*a[1]+mz*a[2]
    div_residual=float(np.max(np.abs(div)))/(max(1.,N)*scale)
    if div_residual>divergence_rtol:
        raise ValueError(f"Divergence residual {div_residual}")
    mask=(mx*mx+my*my+mz*mz)<=N*N
    outside=float(np.max(np.abs(a[:,~mask]))) if np.any(~mask) else 0.
    if outside>symmetry_rtol*scale:
        raise ValueError("Nonzero coefficients outside spherical Galerkin mask")
    val,parts=vorticity_scalene(a,L,K,N,return_parts=True)
    denom=max(abs(val),np.finfo(float).tiny)
    ratio=(abs(parts["full"])+abs(parts["repeated"]))/denom
    parts.update(hermitian_residual=hermitian_residual,
                 divergence_residual=div_residual,
                 estimated_work_bytes=estimated,
                 cancellation_ratio=ratio,
                 error_certificate=False,
                 sign_certified=False,
                 cancellation_warning=ratio>cancellation_limit)
    return val,parts
