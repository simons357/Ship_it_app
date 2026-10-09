"""Single fixed Galerkin mask, with distinct diagnostic high-pass."""
import numpy as np

def make_galerkin_mask(n, L, N):
    if N is None or N <= 0: raise ValueError('Explicit positive integer Galerkin N required')
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    x,y,z=np.meshgrid(modes,modes,modes,indexing='ij')
    base=(np.abs(x)<n/3)&(np.abs(y)<n/3)&(np.abs(z)<n/3)
    radial=x*x+y*y+z*z<=N*N
    # A spherical cutoff requires the full sphere to lie in the 2/3 retained cube.
    if N>=n/3: raise ValueError('Need N < n/3 for complete spherical Galerkin cutoff')
    return base & radial

def check_highpass(K,N):
    if K is None or not (0<=K<N): raise ValueError('Require 0 <= K < N')
