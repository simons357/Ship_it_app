import unittest
import numpy as np
from signed_phi import witness
from fast_signed import fast_scalene
from vorticity_signed import vorticity_scalene
class Tests(unittest.TestCase):
 def test_witness(self):
  n=24; L=2*np.pi
  a=np.zeros((3,n,n,n),complex)
  for k,v in witness(2,1).items():a[(slice(None),)+tuple(np.array(k)%n)]=v*n**3
  self.assertAlmostEqual(vorticity_scalene(a,L,K=1,N=6),32*L**3,delta=1e-8)
 def test_dense(self):
  for n,N in ((18,4),(24,5),(30,7)):
   rng=np.random.default_rng(n)
   u=rng.normal(size=(3,n,n,n))
   h=np.fft.fftn(u,axes=(1,2,3))
   m=np.rint(np.fft.fftfreq(n)*n)
   k=np.array(np.meshgrid(m,m,m,indexing="ij"))
   r2=np.sum(k*k,axis=0)
   h-=k*np.sum(k*h,axis=0)[None,...]/np.where(r2==0,1,r2)[None,...]
   h*=((r2>0)&(r2<=N*N))[None,...]
   a=fast_scalene(h,2*np.pi,N=N)
   b=vorticity_scalene(h,2*np.pi,N=N)
   self.assertLess(abs(a-b),1e-8*max(1,abs(a)))
if __name__=="__main__":unittest.main()
