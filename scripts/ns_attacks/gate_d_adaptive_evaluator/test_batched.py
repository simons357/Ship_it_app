import unittest
import numpy as np
from batched_signed import batched_scalene
from fast_signed import fast_scalene
from signed_phi import witness

class BatchTests(unittest.TestCase):
    def embed(self,coeff,n):
        a=np.zeros((3,n,n,n),complex)
        for k,v in coeff.items():a[(slice(None),)+tuple(np.array(k)%n)]=v*n**3
        return a
    def test_witness(self):
        a=self.embed(witness(2,1),24)
        for b in (1,2,4):
            self.assertAlmostEqual(batched_scalene(a,2*np.pi,K=1,N=6,batch_size=b),32*(2*np.pi)**3,places=7)
    def test_random_reference(self):
        rng=np.random.default_rng(121)
        for n,N in ((18,4),(24,5)):
            a=np.zeros((3,n,n,n),complex)
            for x in range(-N,N+1):
                for y in range(-N,N+1):
                    for z in range(-N,N+1):
                        k=(x,y,z); q=x*x+y*y+z*z
                        if q==0 or q>N*N or k<tuple(-t for t in k):continue
                        v=rng.normal(size=3)+1j*rng.normal(size=3)
                        v-=np.array(k)*np.dot(k,v)/q
                        a[(slice(None),)+tuple(t%n for t in k)]=v*n**3/100
                        a[(slice(None),)+tuple((-t)%n for t in k)]=v.conj()*n**3/100
            ref=fast_scalene(a,2*np.pi,N=N)
            for b in (1,3):
                got=batched_scalene(a,2*np.pi,N=N,batch_size=b)
                self.assertLessEqual(abs(got-ref),1e-9*max(1,abs(ref)))
    def test_resource_limit(self):
        a=self.embed(witness(2,1),24)
        with self.assertRaises(MemoryError):
            batched_scalene(a,2*np.pi,N=6,max_batch_bytes=1)
if __name__=="__main__":unittest.main()
