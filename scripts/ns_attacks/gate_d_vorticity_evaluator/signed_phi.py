"""September 20 exact-radius signed scalene trilinear diagnostic.
Fourier coefficients normalized so physical Parseval sum is sum |u_hat|^2.
Only integer lattice torus modes; NOT a periodic-L Gaussian certification.
"""
import numpy as np

def phi_scalene(coeff, K=0, N=float('inf')):
    """coeff: dict[(int,int,int)] -> complex 3-vector. Includes negative modes.
    Implements September 20 Phi_abc, with no extra Hermitian factor.
    """
    keys=set(coeff)
    out=0.
    for p in keys:
        a=sum(t*t for t in p)
        if a<=K*K or a>N*N: continue
        vp=np.asarray(coeff[p],dtype=complex)
        for q in keys:
            b=sum(t*t for t in q)
            if not a<b or b>N*N:continue
            r=tuple(-p[i]-q[i] for i in range(3))
            if r not in keys:continue
            c=sum(t*t for t in r)
            if not b<c or c>N*N:continue
            wq=np.asarray(coeff[q],dtype=complex);zr=np.asarray(coeff[r],dtype=complex)
            p0=np.asarray(p);q0=np.asarray(q);r0=np.asarray(r)
            term=(c-b)*np.dot(q0,vp)*np.dot(wq,zr)+(a-c)*np.dot(r0,wq)*np.dot(zr,vp)+(b-a)*np.dot(p0,zr)*np.dot(vp,wq)
            out+=term.imag
    return float(out)

def ordered_transfer(coeff,K=0,N=float('inf'),scalene=True):
    """Independent ordered receiver convolution; physical Fourier convention."""
    total=0.
    for p,up in coeff.items():
        ap=sum(v*v for v in p)
        for q,uq in coeff.items():
            bq=sum(v*v for v in q)
            k=tuple(p[i]+q[i] for i in range(3))
            if k not in coeff:continue
            ck=sum(v*v for v in k)
            if min(ap,bq,ck)<=K*K or max(ap,bq,ck)>N*N:continue
            if scalene and len({ap,bq,ck})!=3:continue
            uk=np.asarray(coeff[k]);up=np.asarray(up);uq=np.asarray(uq)
            total+=(-1j*ck*np.dot(np.asarray(q),up)*np.dot(uq,np.conj(uk))).real
    return float(total)

def witness(m=2,A=1):
    p=(m,0,0);q=(0,2*m,0);k=(m,2*m,0)
    out={p:1j*A*np.array([0,1,0]),q:1j*A*np.array([0,0,1]),k:1j*A*np.array([0,0,1])}
    for key,value in list(out.items()):out[tuple(-x for x in key)]=np.conj(value)
    return out
