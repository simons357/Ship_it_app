import unittest
import numpy as np
from signed_scalene import signed_scalene_reference
from gaussian_gate_d import grid, project, nonlinear

class SignedTests(unittest.TestCase):
    def test_no_scalene_on_one_shell(self):
        n=12; L=2*np.pi
        vh=np.zeros((3,n,n,n),complex)
        vh[1,1,0,0]=6; vh[1,-1,0,0]=6
        self.assertEqual(signed_scalene_reference(vh,L),0.)
    def test_direct_matches_pseudospectral_full_when_all_triads_scalene(self):
        n=24; L=2*np.pi
        xyz,ks=grid(n,L)
        vh=np.zeros((3,n,n,n),complex)
        # triad p=(1,0,0),q=(0,2,0),k=(1,2,0), all distinct radii 1,4,5
        rng=np.random.default_rng(11)
        for k in [(1,0,0),(0,2,0),(1,2,0)]:
            a=rng.normal(size=3)+1j*rng.normal(size=3)
            a=a-np.array(k)*np.dot(k,a)/np.dot(k,k)
            vh[(slice(None),*k)]=a*n**3
            vh[(slice(None),*(-i for i in k))]=np.conj(a)*n**3
        nh=nonlinear(vh,ks)
        k2=ks[3]
        total=(L**3/n**6)*np.sum(np.conj(vh)*k2[None,...]*nh).real
        direct=signed_scalene_reference(vh,L)
        self.assertAlmostEqual(direct,total,places=8)
if __name__=='__main__':unittest.main()
