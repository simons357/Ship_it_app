
"""Fail-closed integration for stored Fourier arrays; stepper not modified.
Exact arithmetic for sparse arrays; unverified for dense arrays.
"""
from fractions import Fraction
import math
import numpy as np
from fail_closed import preflight
from exact_sparse_transfer import transfer_exact
from exact_discrete_y import exact_Y
from validated_vorticity import evaluate_checked

def assess(vh,L,K,N,nu=1/200,*,limit_bytes=2*1024**3,
           max_exact_modes=64,max_exact_pairs=4096):
    a=np.asarray(vh)
    if a.ndim!=4 or a.shape[0]!=3 or len(set(a.shape[1:]))!=1:
        raise ValueError("Invalid Fourier array shape")
    n=a.shape[1]
    preflight(n,N,limit_bytes)
    if not math.isfinite(L) or L<=0 or not isinstance(K,int) or not 0<=K<N:
        raise ValueError("Invalid L or K")
    if not math.isfinite(nu) or nu<=0: raise ValueError("Invalid viscosity")
    if not np.issubdtype(a.dtype,np.complexfloating) or not np.isfinite(a).all():
        raise ValueError("Nonfinite or noncomplex Fourier array")
    m=np.rint(np.fft.fftfreq(n)*n).astype(int)
    k=np.array(np.meshgrid(m,m,m,indexing="ij"))
    r2=np.sum(k*k,axis=0)
    scale=max(1.,float(np.max(np.abs(a))))
    neg=(-np.arange(n))%n
    conj_partner=np.conj(a[:,neg[:,None,None],neg[None,:,None],neg[None,None,:]])
    if np.max(np.abs(a-conj_partner))>1e-11*scale:
        raise ValueError("Hermitian symmetry violation")
    if np.max(np.abs(np.sum(k*a,axis=0)))>1e-11*N*scale:
        raise ValueError("Divergence violation")
    if np.any(a[:,r2>N*N]!=0):
        raise ValueError("Nonzero coefficient outside Galerkin sphere")
    count=int(np.count_nonzero(np.any(a!=0,axis=0)&(r2>K*K)))
    # IMPORTANT: do not run the unverified fast evaluator before the exact path.
    if count<=max_exact_modes and count**2<=max_exact_pairs:
        t=transfer_exact(a,K=K,N=N,max_modes=max_exact_modes,max_pairs=max_exact_pairs)
        y=exact_Y(a,max_nonzero=max_exact_modes)
        # At L=2pi the common volume factor cancels in the sign of D.
        # At other L the physical Y factor differs; do not certify D there.
        if L==2*math.pi:
            nu_r=Fraction(float(nu))
            d=t-nu_r*y/4
            d_sign='positive' if d>0 else 'negative' if d<0 else 'zero'
            return {'status':'exact_represented_coefficients',
                    'T_sc_normalized_exact':str(t),'Y_normalized_exact':str(y),
                    'D_normalized_exact':str(d),'D_sign':d_sign,
                    'T_sc':float(t)*(2*math.pi)**3,
                    'sign_certified_for_stored_coefficients':True,
                    'trajectory_certified':False}
        return {'status':'physical_box_sign_unverified',
                'T_sc_normalized_exact':str(t),'Y_normalized_exact':str(y),
                'D_sign':'unknown','sign_certified_for_stored_coefficients':False,
                'trajectory_certified':False}
    # Never silently promote a fast sign when exact reference is infeasible.
    return {'status':'sign_unverified','T_sc':None,'D_sign':'unknown',
            'occupied_high_modes':count,
            'sign_certified_for_stored_coefficients':False,
            'trajectory_certified':False}
