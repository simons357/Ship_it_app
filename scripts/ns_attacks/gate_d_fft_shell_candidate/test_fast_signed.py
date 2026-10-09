import unittest
import numpy as np
from fast_signed import fast_scalene
from signed_bridge import signed_diagnostics
from signed_phi import witness
from gaussian_gate_d import grid

class TestFastSigned(unittest.TestCase):
    def embed(self,coeff,n):
        a=np.zeros((3,n,n,n),complex)
        for k,v in coeff.items():a[(slice(None),)+tuple(np.array(k)%n)] = v*n**3
        return a
    def test_witness(self):
        n=24; L=2*np.pi
        vh=self.embed(witness(2,1),n)
        self.assertAlmostEqual(fast_scalene(vh,L,K=1,N=6),32*L**3,delta=1e-8)
    def test_random_fields(self):
        n=24;L=2*np.pi
        rng=np.random.default_rng(42)
        modes=[(i,j,k) for i in range(-4,5) for j in range(-4,5) for k in range(-4,5) if 0<i*i+j*j+k*k<=22]
        coeff={}
        for p in modes:
            if p in coeff or tuple(-v for v in p) in coeff:continue
            v=rng.normal(size=3)+1j*rng.normal(size=3)
            pv=np.array(p,dtype=float);v-=pv*np.dot(pv,v)/np.dot(pv,pv)
            coeff[p]=v/100;coeff[tuple(-v for v in p)]=np.conj(v)/100
        vh=self.embed(coeff,n)
        for K in (0,1,2):
            ref=signed_diagnostics(vh,grid(n,L)[1],L,K_index=K,N_index=5)
            fast=fast_scalene(vh,L,K=K,N=5)
            self.assertAlmostEqual(fast,ref,delta=1e-9*max(1,abs(ref)))
if __name__=='__main__':unittest.main()
