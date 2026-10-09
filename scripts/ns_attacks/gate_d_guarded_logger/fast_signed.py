"""FFT shell-subtraction signed scalene transfer; diagnostic only.

T_sc = T_full - T_rep, where
T_rep = -Re sum_a < B(h_a,h_a), (A-a)h >.
This identity groups all receiver orientations for repeated squared radii.
FFT uses unnormalized forward, 1/n^3 inverse; physical volume L^3.
The full field supplied is already Galerkin-masked; high-pass only here.
"""
import numpy as np

def fast_scalene(vh, L, K=0, N=None, *, return_parts=False):
    vh=np.asarray(vh)
    if vh.ndim!=4 or vh.shape[0]!=3 or len(set(vh.shape[1:]))!=1:
        raise ValueError('vh must be (3,n,n,n)')
    n=vh.shape[1]
    if N is not None and N>=n/3: raise ValueError('N must be < n/3')
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    mx,my,mz=np.meshgrid(modes,modes,modes,indexing='ij')
    r2=mx*mx+my*my+mz*mz
    keep=(r2>K*K)
    if N is not None: keep &= r2<=N*N
    h=np.where(keep[None,...],vh,0)
    m=np.array([mx,my,mz]); k=(2*np.pi/L)*m
    k2=(2*np.pi/L)**2*r2
    norm=n**3
    def inner_hat(a,b):
        return (L**3/norm**2)*np.vdot(a,b).real
    def nonlinear(a,b):
        # -P[(a dot grad)b] in Fourier; project in receiver wavevector.
        ax=np.fft.ifftn(a,axes=(1,2,3))
        grad=np.fft.ifftn(1j*k[:,None,...]*b[None,...],axes=(2,3,4))
        conv=np.einsum('jxyz,jixyz->ixyz',ax,grad,optimize=True)
        out=np.fft.fftn(conv,axes=(1,2,3))
        dot=np.einsum('ixyz,ixyz->xyz',k,out,optimize=True)
        safe=np.where(k2==0,1,k2)
        out-=k*dot[None,...]/safe[None,...]
        out[:,0,0,0]=0
        return -out
    # Full enstrophy production, h-only (not full-solution G).
    full=inner_hat(nonlinear(h,h),k2[None,...]*h)
    repeated=0.
    shells=np.unique(r2[keep])
    for a in shells:
        ha=np.where((r2==a)[None,...],h,0)
        rhs=nonlinear(ha,ha)
        # (A - a_phys) h includes all receiver shells.
        repeated+=inner_hat(rhs,(k2-(2*np.pi/L)**2*a)[None,...]*h)
    val=full-repeated
    return (float(val),{'full':float(full),'repeated':float(repeated),'shell_count':len(shells)}) if return_parts else float(val)
