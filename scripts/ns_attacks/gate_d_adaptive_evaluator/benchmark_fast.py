import time,json,resource
import numpy as np
from fast_signed import fast_scalene
from signed_bridge import signed_diagnostics
from gaussian_gate_d import grid
rows=[]
for n in (12,18,24):
    L=2*np.pi;K=0;N=3
    rng=np.random.default_rng(20261009)
    modes=np.rint(np.fft.fftfreq(n)*n).astype(int)
    x,y,z=np.meshgrid(modes,modes,modes,indexing='ij')
    k=np.array([x,y,z]);r2=x*x+y*y+z*z
    h=np.zeros((3,n,n,n),complex)
    # Real spatial field -> Hermitian Fourier coefficients
    v=rng.standard_normal((3,n,n,n));h=np.fft.fftn(v,axes=(1,2,3))
    div=np.einsum('ixyz,ixyz->xyz',k,h,optimize=True)
    h-=k*(div/np.where(r2==0,1,r2))[None,...]
    h*=((r2>0)&(r2<=N*N))[None,...]
    t=time.perf_counter();ref=signed_diagnostics(h,grid(n,L)[1],L,K_index=K,N_index=N);tr=time.perf_counter()-t
    t=time.perf_counter();fast=fast_scalene(h,L,K,N);tf=time.perf_counter()-t
    rows.append(dict(n=n,ref_seconds=tr,fft_seconds=tf,speedup=tr/tf,reference=ref,fast=fast,abs_error=abs(ref-fast),relative_error=abs(ref-fast)/max(1,abs(ref))))
print(json.dumps({'rows':rows,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
