"""Exact rational Y for finite binary64 Fourier coefficients on normalized torus.
Certifies only arithmetic on the represented coefficients, not PDE/FFT errors.
"""
from fractions import Fraction
import numpy as np

def exact_Y(vh, *, max_nonzero=5000):
    a=np.asarray(vh)
    if a.ndim!=4 or a.shape[0]!=3 or len(set(a.shape[1:]))!=1:
        raise ValueError("Expected (3,n,n,n) complex Fourier array")
    if not np.isfinite(a).all():raise ValueError("Nonfinite input")
    n=a.shape[1]
    nonzero=np.argwhere(np.any(a!=0,axis=0))
    if len(nonzero)>max_nonzero:raise MemoryError("exact arithmetic mode count limit")
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    total=Fraction(0)
    for i,j,k in nonzero:
        r2=int(modes[i]**2+modes[j]**2+modes[k]**2)
        if r2==0:continue
        for c in range(3):
            z=a[c,i,j,k]
            re=Fraction(float(z.real)); im=Fraction(float(z.imag))
            total+=r2*r2*(re*re+im*im)
    return total/Fraction(n**6)

def certified_float_enclosure(exact):
    """Return adjacent binary64 floats enclosing exact rational value."""
    import math
    if exact<0:raise ValueError("Y must be nonnegative")
    nearest=float(exact)
    if not math.isfinite(nearest):raise OverflowError("Y outside finite float range")
    represented=Fraction(nearest)
    lo=math.nextafter(nearest,-math.inf) if represented>exact else nearest
    hi=math.nextafter(nearest,math.inf) if represented<exact else nearest
    return (lo,hi)
