import unittest
import numpy as np
from gaussian_gate_d import grid,diagnostics,project
from signed_bridge import signed_diagnostics
from signed_phi import witness,ordered_transfer

def as_fft(coeff,n):
    a=np.zeros((3,n,n,n),dtype=complex)
    for k,v in coeff.items():a[:,k[0]%n,k[1]%n,k[2]%n]=v*n**3
    return a

class ConnectedTests(unittest.TestCase):
    def test_witness_physical_scaling_and_independent_convolution(self):
        for L in (2*np.pi,4*np.pi,8*np.pi):
            n=24;ks=grid(n,L)[1];v=as_fft(witness(),n)
            a=signed_diagnostics(v,ks,L,K_index=1,N_index=6,threshold=0)
            alpha=2*np.pi/L
            expected=L**3*alpha**3*32
            self.assertAlmostEqual(a,expected,places=7)
            self.assertAlmostEqual(a,L**3*alpha**3*ordered_transfer(witness(),K=1,N=6),places=7)
            self.assertEqual(signed_diagnostics(v,ks,L,K_index=2,N_index=6,threshold=0),0.)
    def test_connected_X_Y_D_and_mask(self):
        n=24;L=2*np.pi;ks=grid(n,L)[1];v=as_fft(witness(),n)
        d=diagnostics(v,ks,L,200.,.5,signed_K=1,signed_N=6)
        vol=L**3
        self.assertAlmostEqual(d['X'],20*4*vol,places=6)
        self.assertAlmostEqual(d['Y'],84*16*vol,places=6)
        self.assertAlmostEqual(d['T_sc'],32*vol,places=6)
        self.assertAlmostEqual(d['D'],vol*(32-84*16/800),places=6)
        self.assertAlmostEqual(d['d_over_X'],d['D']/d['X'])
        self.assertAlmostEqual(d['G'],d['production']-d['Y']/200.)
        self.assertIsNone(diagnostics(v,ks,L,200.,.5)['D'])
    def test_reject_unresolved_N(self):
        ks=grid(24,12)[1]
        with self.assertRaises(ValueError):signed_diagnostics(np.zeros((3,24,24,24),complex),ks,12,K_index=1,N_index=128)

if __name__=='__main__':unittest.main()
