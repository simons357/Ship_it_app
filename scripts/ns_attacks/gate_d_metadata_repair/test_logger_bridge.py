import unittest
import numpy as np
from compare_cancellation import make_pair
from logger_bridge import diagnostic_record
class Tests(unittest.TestCase):
 def test_sparse(self):
  r=diagnostic_record(make_pair(52),L=2*np.pi,K=1,N=9,c=200,s=0)
  self.assertEqual(r["diagnostic_status"],"exact_represented_coefficients")
  self.assertFalse(r["crossing_certified"])
 def test_large_fail_closed(self):
  a=make_pair(52)
  # Add many valid, symmetric, solenoidal Fourier modes
  for j in range(1,7):
   for k in range(1,7):
    if j*j+k*k>81:continue
    a[2,j,k,0]=1j
    a[2,-j,-k,0]=-1j
  r=diagnostic_record(a,L=2*np.pi,K=1,N=9,c=200,s=0)
  self.assertEqual(r["diagnostic_status"],"sign_unverified")
  self.assertIsNone(r["T_sc"])
if __name__=="__main__":unittest.main()
