"""16 Sep handoff: four buckets; C10 not seated; no H repair; no 9D claim."""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_drift import (  # noqa: E402
    identity_matches_log_derivative,
    lambda_prime_ceiling,
    spectral_cauchy,
    tautological_k,
    two_mode_moments,
    y_remainder_log_ceiling,
)
from snd_instrument import (  # noqa: E402
    diagnose,
    equal_shell_masses,
    envelope_gamma,
    high_tail_one_peak,
    migrate,
    packet_shear_masses,
    shear_flux_is_zero,
)

STATUS = ROOT / "docs" / "NS-STATUS.md"
DRIFT = ROOT / "docs" / "CENTERED-DRIFT.md"
INSTR = ROOT / "docs" / "SND-INSTRUMENT.md"
C10 = ROOT / "docs" / "C10-CHAIN.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
PLAN = ROOT / "docs" / "UNAUGMENTED-R4-VORTICITY-PLAN.md"
CHAIN = ROOT / "docs" / "UNAUGMENTED-NS-CHAIN.md"
NINE = ROOT / "docs" / "ATTACK-9D-FULL-SUPPORT-BOUND.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class CenteredDriftArithmeticTests(unittest.TestCase):
    def test_identities(self):
        self.assertTrue(spectral_cauchy(Fraction(4), Fraction(2), Fraction(1)))
        self.assertFalse(spectral_cauchy(Fraction(1), Fraction(2), Fraction(1)))
        self.assertEqual(lambda_prime_ceiling(Fraction(3)), 6)
        self.assertEqual(y_remainder_log_ceiling(Fraction(5, 2)), 5)
        self.assertEqual(tautological_k(Fraction(5), Fraction(1), Fraction(2)), 2)
        self.assertEqual(tautological_k(Fraction(1), Fraction(4), Fraction(2)), 0)
        self.assertTrue(identity_matches_log_derivative())
        m = two_mode_moments()
        self.assertAlmostEqual(m["D_s"], m["D_s_fact"])

    def test_drift_page_does_not_restore_star(self):
        text = _plain(DRIFT)
        self.assertIn("Unrestricted", text)
        self.assertIn("KILLED", DRIFT.read_text())
        self.assertIn("tautolog", text.lower())
        self.assertIn("Do not restore", text)
        self.assertIn("NEW CLAIM", text)
        self.assertIn("Lambda'<=2K", text.replace(" ", ""))
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())


class SndInstrumentArithmeticTests(unittest.TestCase):
    def test_packet_shear(self):
        masses = packet_shear_masses()
        d = diagnose(masses)
        self.assertEqual(d["j_star"], 0)
        self.assertEqual(d["rho"], Fraction(2, 22))
        self.assertGreater(d["tail_mass"], 0)
        self.assertEqual(sum(shear_flux_is_zero(masses).values()), 0)
        self.assertEqual(d["outside"], 1 - d["rho"])

    def test_equal_shells_have_no_universal_floor(self):
        d = diagnose(equal_shell_masses(11))
        self.assertEqual(d["rho"], Fraction(1, 11))
        self.assertEqual(d["j_star"], 0)

    def test_high_tail_rho_does_not_control_location(self):
        d = diagnose(high_tail_one_peak(2, 40, Fraction(9, 10)))
        self.assertEqual(d["rho"], Fraction(9, 10))
        self.assertEqual(d["j_star"], 2)
        self.assertEqual(d["tail_mass"], Fraction(1, 10))
        self.assertGreater(d["gamma"], 0)
        # Peak plus far mass: rho large, tail frequency arbitrary.
        # The same leftover mass farther out forces a smaller gamma.
        other = diagnose(high_tail_one_peak(2, 80, Fraction(9, 10)))
        self.assertEqual(other["rho"], d["rho"])
        self.assertLess(other["gamma"], d["gamma"])
        self.assertGreater(max(high_tail_one_peak(2, 80, Fraction(9, 10))), 40)

    def test_envelope_and_migration(self):
        decaying = {0: Fraction(4), 1: Fraction(2), 2: Fraction(1)}
        g = envelope_gamma(decaying, 0, Fraction(4))
        self.assertEqual(g, 1)
        before = diagnose({0: Fraction(3), 1: Fraction(1)})
        after = diagnose({0: Fraction(1), 3: Fraction(3)})
        mig = migrate(before, after)
        self.assertEqual(mig["delta_j_star"], 3)


class StatusPageTests(unittest.TestCase):
    def test_four_buckets_and_failed_arrows(self):
        text = _plain(STATUS)
        raw = STATUS.read_text()
        for needle in (
            "PROVED",
            "CLAIMED",
            "OPEN",
            "DEAD",
            "which implication failed",
            "not survive as seated",
            "Do not repair old Theorem H",
            "instrument first",
            "Do not write",
            "Catalog B open stays 1",
        ):
            self.assertIn(needle, text)
        self.assertIn("K\\le 16/9", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("Exact-shell 9D — claimed", raw)
        self.assertNotIn("9D bound CLAIMED", raw)
        self.assertIn("Do not write", raw)

    def test_instrument_page_refuses_persistence(self):
        text = _plain(INSTR)
        self.assertIn("No persistence", text)
        self.assertIn("does not assert", text)
        self.assertIn("Frozen partition", text)
        self.assertNotIn("NS is solved", text)

    def test_pointers(self):
        for path in (TAPE, TINY, LATEST, ISSUES, PLAN, CHAIN, C10):
            body = path.read_text()
            self.assertIn("NS-STATUS.md", body, msg=str(path))
        self.assertIn("CENTERED-DRIFT.md", C10.read_text())
        self.assertIn("SND-INSTRUMENT.md", TINY.read_text())
        nine = NINE.read_text()
        self.assertIn("Freeze", nine)
        self.assertIn("CLAIMED", nine)
        tape = _plain(TAPE)
        self.assertIn("C10 is not a theorem", tape)


if __name__ == "__main__":
    unittest.main()
