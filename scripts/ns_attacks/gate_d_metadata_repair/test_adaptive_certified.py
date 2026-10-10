import unittest
import numpy as np
from compare_cancellation import make_pair
from adaptive_certified import evaluate
class Tests(unittest.TestCase):
 def test_near_cancellation(self):
  a=make_pair(52)
  r=evaluate(a,2*np.pi,1,9)
  self.assertEqual(r["sign"],"negative")
  self.assertEqual(r["status"],"exact_represented_coefficients")
  self.assertGreater(r["fast_discrepancy"],0)
 def test_exact_zero(self):
  r=evaluate(make_pair(54),2*np.pi,1,9)
  self.assertEqual(r["sign"],"zero")
 def test_fail_closed_large(self):
  r=evaluate(make_pair(52),2*np.pi,1,9,max_exact_modes=2)
  self.assertIsNone(r["T_sc"])
  self.assertEqual(r["status"],"sign_unverified")
if __name__=="__main__":unittest.main()
