"""Exact Gaussian-rational Fourier checks; standard library only.

Not a numerical depletion study or a proof of a class estimate.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

class Q:
    def __init__(self, r=0, i=0): self.r,self.i=F(r),F(i)
    def __add__(self,o):
        o=q(o); return Q(self.r+o.r,self.i+o.i)
    __radd__=__add__
    def __neg__(self): return Q(-self.r,-self.i)
    def __sub__(self,o): return self+-q(o)
    def __mul__(self,o):
        o=q(o); return Q(self.r*o.r-self.i*o.i,self.r*o.i+self.i*o.r)
    __rmul__=__mul__
    def conj(self): return Q(self.r,-self.i)
    def __eq__(self,o):
        o=q(o); return self.r==o.r and self.i==o.i
    def out(self): return [str(self.r),str(self.i)]
def q(x): return x if isinstance(x,Q) else Q(x)
def dot(a,b): return sum((q(x)*q(y) for x,y in zip(a,b)),Q())
def cross(a,b): return [q(a[1])*q(b[2])-q(a[2])*q(b[1]),q(a[2])*q(b[0])-q(a[0])*q(b[2]),q(a[0])*q(b[1])-q(a[1])*q(b[0])]
def scale(a,s): return [q(x)*s for x in a]
def curl(k,a): return scale(cross(k,a),Q(0,1))
def field(entries):
    u={}
    for k,a in entries:
        u[k]=[q(x) for x in a]
        u[tuple(-t for t in k)]=[q(x).conj() for x in a]
    return u
def convolution_cross(u,w):
    out={}
    for p,r in product(u,w):
        k=tuple(p[i]+r[i] for i in range(3))
        out[k]=[a+b for a,b in zip(out.get(k,[Q()]*3),cross(u[p],w[r]))]
    return out
def check(u,phi,ell):
    U={k:scale(a,ell(k)) for k,a in u.items()}
    w={k:curl(k,a) for k,a in U.items()}
    X=convolution_cross(U,w)
    direct=Q();triple=Q();energy=Q();rows=[]
    for k,a in u.items():
        assert dot(k,a)==0
        v=scale(curl(k,a),phi(k))
        b=curl(k,X.get(k,[Q()]*3))
        direct+=dot([x.conj() for x in v],scale(b,phi(k)))
        test=scale(a,dot(k,k).r*phi(k)**2)
        triple+=dot([x.conj() for x in test],X.get(k,[Q()]*3))
        pair=dot([x.conj() for x in U[k]],X.get(k,[Q()]*3))
        energy+=pair
        rows.append({'k':k,'energy_pairing':pair.out()})
    assert direct==triple and energy==0
    return direct,rows
triad=field([((1,0,0),(0,1,1)),((0,1,0),(1,0,1)),((-1,-1,0),(Q(0,1),Q(0,-1),Q(0,1)))])
t,rows=check(triad,lambda k:F(1),lambda k:F(1))
assert t==4
soft,unused=check(triad,lambda k:F(1,2) if sum(x*x for x in k)==1 else F(3,4),lambda k:F(1))
assert soft==F(7,2)
shell=field([((1,0,0),(0,Q(0,-F(1,2)),0)),((0,1,0),(0,0,Q(0,-F(1,2)))),((0,0,1),(Q(0,-F(1,2)),0,0))])
s,unused=check(shell,lambda k:F(1),lambda k:F(1))
assert s==0
payload={'arithmetic':'exact Gaussian rationals','sharp_shell_triad_T':t.out(),'soft_multiplier_triad_T':soft.out(),'one_length_T':s.out(),'triad_rows':rows,'full_local_identity':'passed','energy_orthogonality':'passed','scope':'finite exact Fourier algebra; no class depletion conclusion'}
path=Path(__file__).with_name('C10-FULL-LOCAL-EXACT-CHECKS.json')
path.write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
