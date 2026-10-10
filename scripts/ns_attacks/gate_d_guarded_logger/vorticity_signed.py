"""Vorticity-form signed transfer: eliminates per-shell forward FFTs and Leray projection.
Assumes divergence-free Hermitian Fourier input, validates by reference comparison.
No coefficient deletion; no production error certificate.
"""
import numpy as np
def vorticity_scalene(vh,L,K=0,N=None,*,return_parts=False):
    a=np.asarray(vh)
    if a.ndim!=4 or a.shape[0]!=3 or len(set(a.shape[1:]))!=1:raise ValueError("expected (3,n,n,n)")
    n=a.shape[1]
    if N is not None and N>=n/3:raise ValueError("N must be < n/3")
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    mx,my,mz=np.meshgrid(modes,modes,modes,indexing="ij")
    r2=mx*mx+my*my+mz*mz
    keep=r2>K*K
    if N is not None:keep &= r2<=N*N
    h=np.where(keep[None,...],a,0)
    alpha=2*np.pi/L
    kx,ky,kz=(alpha*mx,alpha*my,alpha*mz)
    def curl_hat(v):
        return np.stack((1j*(ky*v[2]-kz*v[1]),1j*(kz*v[0]-kx*v[2]),1j*(kx*v[1]-ky*v[0])))
    def physical(v):return np.fft.ifftn(v,axes=(-3,-2,-1)).real
    u=physical(h)
    ah=physical((alpha**2*r2)[None,...]*h)
    def cross_integral(v,omega,receiver):
        return float(L**3*np.mean(np.sum(np.cross(v,omega,axisa=0,axisb=0,axisc=0)*receiver,axis=0)))
    full=cross_integral(u,physical(curl_hat(h)),ah)
    repeated=0.
    for shell in np.unique(r2[keep]):
        hs=np.where((r2==shell)[None,...],h,0)
        vs=physical(hs)
        ws=physical(curl_hat(hs))
        repeated+=cross_integral(vs,ws,ah-alpha**2*shell*u)
    out=full-repeated
    return (float(out),dict(full=full,repeated=repeated,shell_count=len(np.unique(r2[keep])))) if return_parts else float(out)
