import unittest
import numpy as np
from hybrid_signed import hybrid_scalene
from fast_signed import fast_scalene
from signed_phi import witness
class HybridTest(unittest.TestCase):
 def test_witness(self):
  n=24; a=np.zeros((3,n,n,n),complex)
  for k,v in witness(2,1).items():a[(slice(None),)+tuple(x%n for x in k)]=v*n**3
  for maxpairs in (1,10000):
   x=hybrid_scalene(a,2*np.pi,K=1,N=6,max_pairs=maxpairs)
   self.assertAlmostEqual(x,32*(2*np.pi)**3,places=7)
 def test_random(self):
  rng=np.random.default_rng(17);n=18;N=4;a=np.zeros((3,n,n,n),complex)
  for x in range(-N,N+1):
   for y in range(-N,N+1):
    for z in range(-N,N+1):
     k=(x,y,z);q=x*x+y*y+z*z
     if q==0 or q>N*N or k<tuple(-t for t in k):continue
     v=rng.normal(size=3)+1j*rng.normal(size=3)
     v-=np.array(k)*np.dot(k,v)/q
     a[(slice(None),)+tuple(t%n for t in k)]=v*n**3/100
     a[(slice(None),)+tuple(-t%n for t in k)]=v.conj()*n**3/100
  reference=fast_scalene(a,2*np.pi,N=N)
  for maxpairs in (1,1000000):
   got=hybrid_scalene(a,2*np.pi,N=N,max_pairs=maxpairs)
   self.assertLess(abs(got-reference),1e-8*max(1,abs(reference)))
if __name__=='__main__':unittest.main()
