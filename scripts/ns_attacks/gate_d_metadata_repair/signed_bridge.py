"""Research-only bridge. Integer torus lattice cutoffs; physical radius convention pending DA."""
import numpy as np
from signed_phi import phi_scalene

def signed_diagnostics(vh, ks, L, K_index=0, N_index=None, threshold=0.0):
    """Small-grid O(M^2) diagnostic, NOT suitable for N=128/160 production."""
    if threshold != 0: raise ValueError("Coefficient deletion is forbidden in reference evaluator")
    n=vh.shape[1]
    if N_index is not None and N_index >= n/3:
        raise ValueError("signed-N exceeds conservative fully represented 2/3 componentwise band; increase grid n")
    inds=np.rint(np.fft.fftfreq(n)*n).astype(int)
    kx,ky,kz,k2,mask=ks
    coeff={}
    for i in range(n):
        for j in range(n):
            for l in range(n):
                if not mask[i,j,l]: continue
                r2=int(inds[i]**2+inds[j]**2+inds[l]**2)
                if r2<=K_index*K_index or (N_index is not None and r2>N_index*N_index): continue
                v=vh[:,i,j,l]/n**3
                if np.any(v != 0):
                    coeff[(int(inds[i]),int(inds[j]),int(inds[l]))]=v
    # Phi uses integer wavevectors. On a box of side L, each derivative
    # contributes 2pi/L; the trilinear transfer has 3 derivatives total.
    # The L^3 factor converts normalized average to physical integral.
    return float(L**3*(2*np.pi/L)**3*phi_scalene(coeff,K=K_index,N=float('inf') if N_index is None else N_index))
