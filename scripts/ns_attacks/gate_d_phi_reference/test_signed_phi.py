import unittest
from signed_phi import phi_scalene,ordered_transfer,witness
class Tests(unittest.TestCase):
    def test_six_mode(self):
        for m in (1,2,3):
            for amp in (1,2):
                h=witness(m,amp)
                expected=4*m**3*amp**3
                self.assertAlmostEqual(phi_scalene(h),expected)
                self.assertAlmostEqual(ordered_transfer(h),expected)
    def test_cutoff_and_scaling(self):
        h=witness(2,1)
        self.assertEqual(phi_scalene(h,K=2),0)
        self.assertEqual(phi_scalene(h,N=4),0)
        self.assertAlmostEqual(phi_scalene(h,K=1,N=5),32)
if __name__=='__main__':unittest.main()
