"""Five engineering checks for the connected signed-scalene diagnostic.

These checks use the packaged witness coefficients. They do not certify the
original Lemma 19 coefficients. The Navier–Stokes stepper is not modified,
and the frozen c=200 Gaussian experiment is not run.
"""
import unittest

import numpy as np

from driver import (
    STEPPER_PATH,
    WITNESS_VALUE,
    coeff_to_fft,
    diagnose,
    fft_to_coeff,
    five_checks,
    gauss,
    sha256,
    witness,
)


class ConnectedChecks(unittest.TestCase):
    def test_five_checks(self):
        checks = five_checks()
        # 1–2. Family, both the radius-block sum and the ordered convolution.
        for row in checks['family']:
            self.assertAlmostEqual(row['T_sc'], row['expected'])
            self.assertAlmostEqual(row['T_ordered'], row['expected'])
        # 3–4. Cutoff exclusions on the m=2, A=1 witness.
        self.assertEqual(checks['K2_is_zero'], 0)
        self.assertEqual(checks['N4_is_zero'], 0)
        # 5. The +32 witness, with the ordered convolution in agreement.
        self.assertAlmostEqual(checks['plus_32']['T_sc'], WITNESS_VALUE)
        self.assertAlmostEqual(checks['plus_32']['T_ordered'], WITNESS_VALUE)

    def test_roundtrip_and_D_uses_torus_Y(self):
        packed = coeff_to_fft(witness(2, 1), 16)
        back = fft_to_coeff(packed)
        self.assertEqual(set(back), set(witness(2, 1)))
        row = diagnose(packed, L=2 * np.pi, c=200, K=1, N=5)
        self.assertAlmostEqual(row['D'], row['T_sc'] - row['nu'] * row['Y_torus'] / 4)
        self.assertAlmostEqual(row['d'], row['D'] / row['X_torus'])
        # Same integer cutoff, two box lengths: physical edges differ by 2.
        wide = diagnose(packed, L=4 * np.pi, c=200, K=1, N=5)
        self.assertAlmostEqual(
            row['cutoff']['k_phys_at_K'],
            2 * wide['cutoff']['k_phys_at_K'],
        )
        self.assertAlmostEqual(row['T_sc'], wide['T_sc'])

    def test_stepper_source_and_one_witness_step(self):
        self.assertEqual(
            sha256(STEPPER_PATH),
            '0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56',
        )
        n, L, c = 16, 2 * np.pi, 200
        xyz, ks = gauss.grid(n, L)
        vh = coeff_to_fft(witness(2, 1), n)
        before = diagnose(vh, L, c, K=1, N=5)['T_sc']
        self.assertAlmostEqual(before, WITNESS_VALUE)
        advanced = gauss.step(vh, ks, h=1e-6, c=c)
        self.assertEqual(advanced.shape, vh.shape)
        self.assertTrue(np.isfinite(advanced).all())


if __name__ == '__main__':
    unittest.main()
