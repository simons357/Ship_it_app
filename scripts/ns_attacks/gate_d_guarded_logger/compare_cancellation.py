import json,sys,time
from fractions import Fraction as F
import numpy as np
from signed_phi import witness
from exact_sparse_transfer import transfer_exact
from fast_signed import fast_scalene
from vorticity_signed import vorticity_scalene
def make_pair(j,n=36):
    a=witness(2,1);b=witness(4,0.5)
    receiver=(4,8,0)
    # negative packet with tiny positive amplitude perturbation in receiver
    b[receiver]=-b[receiver]*(1+2.**(-j))
    b[tuple(-x for x in receiver)]=np.conj(b[receiver])
    a.update(b)
    vh=np.zeros((3,n,n,n),complex)
    for k,v in a.items():vh[(slice(None),)+tuple(x%n for x in k)]=v*n**3
    return vh
def main():
    rows=[]
    for j in [0,10,20,30,40,48,52,54]:
        a=make_pair(j)
        exact=transfer_exact(a,K=1,N=9,max_modes=64)
        fast,parts=fast_scalene(a,2*np.pi,K=1,N=9,return_parts=True)
        vort,parts2=vorticity_scalene(a,2*np.pi,K=1,N=9,return_parts=True)
        target=float(exact)*(2*np.pi)**3
        eps=np.finfo(float).eps
        scale=abs(parts['full'])+abs(parts['repeated'])
        bits=np.log2(scale/max(abs(fast),eps*scale)) if scale else 0
        rows.append(dict(j=j,exact_normalized=str(exact),exact_float=target,fast=fast,vorticity=vort,
            fast_error=fast-target,vorticity_error=vort-target,full=parts['full'],repeated=parts['repeated'],
            subtraction_lost_bits=float(bits)))
    print(json.dumps(rows,indent=2))
if __name__=="__main__":main()
