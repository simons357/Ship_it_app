import unittest
import numpy as np
from gaussian_gate_d import grid,diagnostics,step,project
from mask_policy import make_galerkin_mask
from signed_phi import witness,ordered_transfer
from signed_bridge import signed_diagnostics

class TestMaskRepair(unittest.TestCase):
 def test_mask_is_spherical_and_highpass_distinct(self):
  n=30;L=2*np.pi;N=6;K=2
  mask=make_galerkin_mask(n,L,N)
  self.assertTrue(mask[6,0,0]);self.assertFalse(mask[6,6,0]);self.assertTrue(mask[1,0,0]);self.assertTrue(K<N)
  ks=grid(n,L)[1];ks=(*ks[:4],mask)
  v=np.zeros((3,n,n,n),complex)
  for k,a in witness().items():v[:,k[0]%n,k[1]%n,k[2]%n]=a*n**3
  d=diagnostics(v,ks,L,200,.5,signed_K=1,signed_N=N)
  self.assertAlmostEqual(d['T_sc'],32*L**3,places=6)
  self.assertAlmostEqual(d['T_sc'],ordered_transfer(witness(),K=1,N=N)*L**3,places=6)
  self.assertAlmostEqual(d['G'],d['production']-d['Y']/200,places=8)
  self.assertAlmostEqual(d['D'],d['T_sc']-d['Y']/800,places=8)
 def test_step_preserves_one_mask(self):
  n=24;L=12.;N=5;xyz,ks=grid(n,L)
  mask=make_galerkin_mask(n,L,N);ks=(*ks[:4],mask)
  rng=np.random.default_rng(8)
  v=rng.normal(size=(3,n,n,n))
  vh=project(np.fft.fftn(v,axes=(1,2,3)),*ks[:4])*mask
  nxt=step(vh,ks,.0001,200)
  self.assertEqual(np.count_nonzero(nxt[:,~mask]),0)
  self.assertLess(np.max(np.abs(ks[0]*nxt[0]+ks[1]*nxt[1]+ks[2]*nxt[2])),1e-9)
 def test_threshold_rejected(self):
  ks=grid(24,12)[1]
  with self.assertRaises(ValueError):signed_diagnostics(np.zeros((3,24,24,24),complex),ks,12,K_index=1,N_index=5,threshold=1e-12)
 def test_resolution_rejected(self):
  with self.assertRaises(ValueError):make_galerkin_mask(24,12,8)

if __name__=='__main__':unittest.main()
