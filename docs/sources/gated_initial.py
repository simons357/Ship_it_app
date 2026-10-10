from itertools import product
from math import sqrt
from collections import defaultdict
import json,sys,time

def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def add(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def neg(a): return (-a[0],-a[1],-a[2])
def n2(k): return dot(k,k)
def box(c,r): return [(c[0]+i,c[1]+j,c[2]+l) for i,j,l in product(range(-r,r+1),repeat=3)]
def pol(k,j):
    a=n2(k); return tuple(a*(i==j)-k[j]*k[i] for i in range(3))
def proj(k,v):
    kk=n2(k); kv=dot(k,v)
    return (v[0]-k[0]*kv/kk, v[1]-k[1]*kv/kk, v[2]-k[2]*kv/kk)

def packet(n):
    L=64*n; P=box((L,0,0),n); Q=box((0,3*L,0),n); R=box((L,3*L,0),2*n)
    a={}
    for modes,j in [(P,1),(Q,2),(R,2)]:
        for k in modes:
            v=pol(k,j); a[k]=v; a[neg(k)]=neg(v)
    E=sum(dot(v,v) for v in a.values()); alpha=1/sqrt(E)
    return {k:(alpha*v[0],alpha*v[1],alpha*v[2]) for k,v in a.items()}

def nonlinear(a,N2):
    ks=list(a); raw=defaultdict(lambda:[0.0,0.0,0.0])
    for p in ks:
        ap=a[p]
        for q in ks:
            k=add(p,q)
            if k==(0,0,0) or n2(k)>N2: continue
            s=dot(q,ap); aq=a[q]; rr=raw[k]
            rr[0]+=s*aq[0]; rr[1]+=s*aq[1]; rr[2]+=s*aq[2]
    out={}
    for k,v in raw.items(): out[k]=proj(k,v)
    return out

def scalene_mask(p,q,k,K2=1):
    a,b,c=n2(p),n2(q),n2(k)
    return a>K2 and b>K2 and c>K2 and a!=b and a!=c and b!=c

def transfer(a,K2=1):
    ks=list(a); T=0.0
    for p in ks:
        ap=a[p]
        for q in ks:
            k=add(p,q); ak=a.get(k)
            if ak is None or not scalene_mask(p,q,k,K2): continue
            T += n2(k)*dot(q,ap)*dot(a[q],ak)
    return T

def dT_nonlin(a,r,K2=1):
    # derivative of ordered transfer in direction r. Three slots separately, O(|S|^2) each.
    S=list(a); total=0.0
    # v in receiver k: p,q in S
    for p in S:
        ap=a[p]
        for q in S:
            k=add(p,q); rk=r.get(k)
            if rk is None or not scalene_mask(p,q,k,K2): continue
            total += n2(k)*dot(q,ap)*dot(a[q],rk)
    # v in p: q,k in S, p=k-q
    for q in S:
        aq=a[q]
        for k in S:
            p=sub(k,q); rp=r.get(p)
            if rp is None or not scalene_mask(p,q,k,K2): continue
            total += n2(k)*dot(q,rp)*dot(aq,a[k])
    # v in q: p,k in S, q=k-p
    for p in S:
        ap=a[p]
        for k in S:
            q=sub(k,p); rq=r.get(q)
            if rq is None or not scalene_mask(p,q,k,K2): continue
            total += n2(k)*dot(q,ap)*dot(rq,a[k])
    return total

def dT_visc(a,nu,K2=1):
    S=list(a); val=0.0
    for p in S:
        ap=a[p]; pa=n2(p)
        for q in S:
            k=add(p,q); ak=a.get(k)
            if ak is None or not scalene_mask(p,q,k,K2): continue
            qb=n2(q); kc=n2(k)
            term=kc*dot(q,ap)*dot(a[q],ak)
            val += -nu*(pa+qb+kc)*term
    return val

def run(n,nu=1e-5,cutmul=4):
    t=time.time(); a=packet(n); H=63*n; N=cutmul*H; N2=N*N
    E=sum(dot(v,v) for v in a.values()); X=sum(n2(k)*dot(v,v) for k,v in a.items()); Y=sum(n2(k)**2*dot(v,v) for k,v in a.items()); Z=sum(n2(k)**3*dot(v,v) for k,v in a.items())
    T=transfer(a); r=nonlinear(a,N2); Q=dT_nonlin(a,r); V=dT_visc(a,nu)
    U2=sum(n2(k)**2*dot(a[k],r.get(k,(0.,0.,0.))) for k in a)
    M=nu*nu/2*Z - nu/2*U2
    D=T-nu*Y/4; Dp=Q+V+M
    rec=dict(n=n,H=H,N=N,modes=len(a),generated=len(r),E=E,X=X,Y=Y,Z=Z,T=T,D=D,Q=Q,V=V,U2=U2,M=M,Dprime=Dp,D_over_X=D/X,tau_local=(D/Dp if Dp!=0 else None),scaled_tau=(D/Dp*H**2.5 if Dp!=0 else None),elapsed=time.time()-t)
    print(json.dumps(rec,indent=2)); return rec
if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 1; cm=int(sys.argv[2]) if len(sys.argv)>2 else 4; run(n,1e-5,cm)
