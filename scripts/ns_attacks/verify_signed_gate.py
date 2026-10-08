"""Exact coherent signed-packet check. Standard library only.

Variant of the Sept. 20 separated-packet source with second center 3L e2,
so the entire field is in H <= |k| <= 4H, H=63n. All decisive assertions
use integers/Fractions. Displayed diagnostic ratios use square roots.
"""
from itertools import product
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
import json

dot=lambda a,b:sum(x*y for x,y in zip(a,b))
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
neg=lambda a:tuple(-x for x in a)
norm2=lambda p:dot(p,p)


def box(center,r):
    return [add(center,d) for d in product(range(-r,r+1),repeat=3)]


def polarization(k,j):
    a=norm2(k)
    return tuple(a*(i==j)-k[j]*k[i] for i in range(3))


def packet(n):
    L=64*n
    P=box((L,0,0),n);Q=box((0,3*L,0),n);R=box((L,3*L,0),2*n)
    w={}
    for modes,j in [(P,1),(Q,2),(R,2)]:
        for k in modes:
            assert k not in w and neg(k) not in w
            v=polarization(k,j)
            w[k]=v;w[neg(k)]=neg(v)
    # Fourier coefficients are i*w[k], so these assertions give reality
    # and exact incompressibility.
    assert all(dot(k,v)==0 and w[neg(k)]==neg(v) for k,v in w.items())
    H=63*n
    assert all(H*H<=norm2(k)<=16*H*H for k in w)
    E=sum(dot(v,v) for v in w.values())
    X=sum(norm2(k)*dot(v,v) for k,v in w.items())
    Y=sum(norm2(k)**2*dot(v,v) for k,v in w.items())
    T=0;pairs=0
    for p in P:
        a=norm2(p);wp=w[p]
        for q in Q:
            k=add(p,q);b=norm2(q);c=norm2(k)
            assert k in w and a<b<c and c>=4*a
            wq,wk=w[q],w[k]
            kernel=(c-b)*dot(q,wp)*dot(wq,wk)+(c-a)*dot(k,wq)*dot(wk,wp)+(b-a)*dot(p,wk)*dot(wp,wq)
            assert kernel>2*L**3*a*b*c
            T+=2*kernel;pairs+=1
    assert pairs==(2*n+1)**6
    # Independent full ordered Fourier evaluation, including all receivers
    # and both input orderings. No projection is omitted from the mathematics:
    # P_k drops from its pairing with w_k because k dot w_k is exactly zero.
    ordered=None
    if n==1:
        ordered=0;rep=0;nonsep=0
        for p,wp in w.items():
            for q,wq in w.items():
                k=add(p,q)
                if k not in w:continue
                a,b,c=norm2(p),norm2(q),norm2(k)
                term=c*dot(q,wp)*dot(wq,w[k])
                ordered+=term
                if len({a,b,c})<3:rep+=term
                if max(a,b,c)<4*min(a,b,c):nonsep+=term
        assert ordered==T and rep==0 and nonsep==0
    return {'n':n,'H':H,'modes':len(w),'positive_pairs':pairs,
            'E':str(E),'X':str(X),'Y':str(Y),'T_scalene':str(T),
            'ordered_full_transfer':None if ordered is None else str(ordered),
            'T_over_sqrtE_Y_diagnostic':T/(sqrt(E)*Y)}


def main():
    e=F(1,64)
    signed_lower=(1-10*e-5*e*e)*(3-9*e)*(1-2*e-e*e)-672*e*e
    assert signed_lower==F(2329130643,1073741824)>2
    assert 66**2+194**2+2**2<252**2
    # Check the center relations independently; offsets total at most 6n,
    # smaller than L, so nonzero center sums cannot produce hidden triads.
    centers=[(1,0,0),(0,3,0),(1,3,0),(-1,0,0),(0,-3,0),(-1,-3,0)]
    patterns=set()
    for p,q,r in product(centers,repeat=3):
        if add(add(p,q),r)==(0,0,0):patterns.add(tuple(sorted((p,q,r))))
    assert len(patterns)==2
    rec={'status':'PASS: exact signed finite checks; analytical all-scale proof in companion note.',
         'signed_kernel_uniform_lower':str(signed_lower),
         'sharp_uniform_band_exponent':'1/2',
         'upper_bound_constant':1728,
         'scope':'Actual instantaneous signed scalene transfer in H<=|k|<=4H.',
         'checks':[packet(n) for n in (1,2,3)]}
    Path(__file__).with_name('Signed-Gate-Checks.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2))


if __name__=='__main__':main()
