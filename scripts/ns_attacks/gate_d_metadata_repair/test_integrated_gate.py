
import unittest
import numpy as np
from signed_phi import witness
from compare_cancellation import make_pair
from integrated_gate import assess
class Tests(unittest.TestCase):
 def test_negative_near_cancellation(self):
  r=assess(make_pair(52),2*np.pi,1,9)
  self.assertEqual(r['status'],'exact_represented_coefficients')
  self.assertEqual(r['T_sc_normalized_exact'],'-1/200385994162176')
 def test_zero_near_cancellation(self):
  r=assess(make_pair(54),2*np.pi,1,9)
  self.assertEqual(r['T_sc_normalized_exact'],'0')
 def test_dense_fails_closed(self):
  r=assess(make_pair(52),2*np.pi,1,9,max_exact_modes=2)
  self.assertEqual(r['status'],'sign_unverified')
 def test_outside_mask_rejected(self):
  a=make_pair(52)
  a[0,10,0,0]=1
  with self.assertRaises(ValueError):assess(a,2*np.pi,1,9)
 def test_other_box_uncertified(self):
  r=assess(make_pair(52),4*np.pi,1,9)
  self.assertFalse(r['sign_certified_for_stored_coefficients'])
if __name__=='__main__':unittest.main()
