"""Exact signed two-sphere assembly and initial scalene regeneration.
Standard-library Gaussian rational arithmetic; no floating-point sampling.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

# Reuse just the arithmetic definitions, without running earlier checks.
src=Path('c10_full_local_exact_checks.py').read_text()
exec(src[:src.index('triad=field(')])
def radius(k): return sum(t*t for t in k)
def addk(p,q): return tuple(a+b for a,b in zip(p,q))
def conj(v): return [z.conj() for z in v]
def B(u):
    out={}
    for p,r in product(u,u):
        k=addk(p,r)
        if radius(k)==0: continue
        z=scale(u[r],Q(0,1)*dot(r,u[p]))
        out[k]=[a+b for a,b in zip(out.get(k,[Q()]*3),z)]
    for k,z in out.items():
        out[k]=[a-b for a,b in zip(z,scale(k,dot(k,z)*F(1,radius(k))))]
    return {k:z for k,z in out.items() if any(a!=0 for a in z)}
def transfer(u, scalene=False):
    s=F(0)
    for p,r in product(u,u):
        k=addk(p,r)
        if k not in u: continue
        if scalene and len({radius(p),radius(r),radius(k)})!=3: continue
        s+=radius(k)*(dot(r,u[p])*dot(u[r],conj(u[k]))).i
    return s
u=field([((1,0,0),(0,1,1)),((0,1,0),(1,0,1)),((-1,-1,0),(Q(0,1),Q(0,-1),Q(0,1)))])
b=B(u)
f={k:scale(z,-1) for k,z in b.items()}
assert all(dot(k,z)==0 for k,z in f.items())
modal={k:-dot(z,conj(u[k])).r for k,z in b.items() if k in u}
J=sum(t for k,t in modal.items() if radius(k)==2)
assert sum(modal.values())==0 and J==4 and transfer(u)==4 and transfer(u,True)==0
assert b[(2,1,0)]==[Q(F(1,5)),Q(F(-2,5)),Q(2)]
# Derivative of the complete cubic signed scalene sum. Viscosity contributes
# nothing here: all three old radii are drawn from {1,2}.
keys=set(u)|set(f)
z=[Q()]*3
s=F(0)
for p,r in product(keys,keys):
    k=addk(p,r)
    if k not in keys or len({radius(p),radius(r),radius(k)})!=3: continue
    up,ur,uk=u.get(p,z),u.get(r,z),u.get(k,z)
    fp,fr,fk=f.get(p,z),f.get(r,z),f.get(k,z)
    deriv=dot(r,fp)*dot(ur,conj(uk))+dot(r,up)*dot(fr,conj(uk))+dot(r,up)*dot(ur,conj(fk))
    s+=radius(k)*deriv.i
# Independent exact polynomial recovery of the cubic coefficient.
def blend(t): return {k:[a+t*c for a,c in zip(u.get(k,z),f.get(k,z))] for k in keys}
p1,m1=transfer(blend(F(1)),True),transfer(blend(F(-1)),True)
p2,m2=transfer(blend(F(2)),True),transfer(blend(F(-2)),True)
s2=(8*(p1-m1)-(p2-m2))/12
assert s==s2
# Filters: exact single sphere and arbitrary unidirectional shear.
sphere=field([((1,0,0),(0,Q(0,-F(1,2)),0)),((0,1,0),(0,0,Q(0,-F(1,2)))),((0,0,1),(Q(0,-F(1,2)),0,0))])
assert transfer(sphere)==0 and B(sphere)
shear=field([((0,3,0),(1,0,Q(0,2))),((0,7,0),(Q(0,3),0,2))])
assert B(shear)=={} and transfer(shear)==0 and transfer(shear,True)==0
assert transfer({k:scale(v,-1) for k,v in u.items()})==-4
payload={'normalization':'T3, normalized volume; Fourier exponent exp(i k.x)', 'E':str(sum(dot(a,conj(a)).r for a in u.values())), 'X':str(sum(radius(k)*dot(a,conj(a)).r for k,a in u.items())), 'Y':str(sum(radius(k)**2*dot(a,conj(a)).r for k,a in u.items())), 'modal_transfers':[{ 'k':k,'tau':str(t)} for k,t in sorted(modal.items())], 'J_radius_2':str(J),'T':str(transfer(u)),'initial_T_scalene':str(transfer(u,True)), 'B_at_2_1_0':[a.out() for a in b[(2,1,0)]], 'generated_radii_squared':sorted({radius(k) for k in f if k not in u}), 'initial_derivative_T_scalene':str(s),'independent_cubic_recovery':'passed','divergence_free':'passed','one_exact_sphere_signed_T':str(transfer(sphere)),'one_exact_sphere_B_nonzero':bool(B(sphere)),'shear_B_zero':B(shear)=={},'sign_reversal':'passed'}
Path('TWO-SHELL-REGENERATION-CHECKS.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
