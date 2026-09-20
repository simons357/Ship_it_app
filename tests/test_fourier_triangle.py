"""Fourier-triangle: identities sit; first missing arrow named; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fourier_triangle import (  # noqa: E402
    isosceles_hh_l,
    one_shell_field,
    record,
    three_shell_unequal,
    two_shell_reduction,
)
from ns_lemma_star_core import T_c_direct, moments, sum_Tk  # noqa: E402

PAGE = ROOT / "docs" / "FOURIER-TRIANGLE.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
PATH = ROOT / "docs" / "PATH-TO-CLOSE.md"
DRIFT = ROOT / "docs" / "CENTERED-DRIFT.md"
BSTAR = ROOT / "docs" / "BSTAR.md"
PROOF = ROOT / "docs" / "BSTAR-PROOF.md"
CLOSE = ROOT / "docs" / "NS-CLOSE-REPORT.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class FourierTriangleIdentityTests(unittest.TestCase):
    def test_energy_sum_and_leray_idle(self):
        row = record()
        self.assertLess(abs(row["identities"]["energy_sum_iso"]), 1e-12)
        self.assertLess(abs(row["identities"]["energy_sum_uneq"]), 1e-12)
        self.assertLess(row["identities"]["leray_idle_max_abs"], 1e-12)
        self.assertAlmostEqual(row["identities"]["one_shell_Tc"], 0.0, places=12)
        self.assertAlmostEqual(row["identities"]["one_shell_Ds"], 0.0, places=12)
        self.assertAlmostEqual(row["identities"]["idle_z_pol_I3_im"], 0.0, places=12)

    def test_two_shell_gap_cancel(self):
        red = two_shell_reduction(isosceles_hh_l())
        self.assertTrue(red["two_shell"])
        self.assertAlmostEqual(red["T_a_plus_T_b"], 0.0, places=12)
        self.assertAlmostEqual(red["Tc"], red["pred_from_Ta"], places=10)
        self.assertAlmostEqual(red["Tc"], red["pred_from_Tb"], places=10)
        self.assertAlmostEqual(red["Ds_two_shell"], red["Ds_moment"], places=10)
        self.assertGreater(abs(red["Tc"]), 1.0)

    def test_unequal_length_defect(self):
        row = record()
        uneq = row["identities"]["uneq_three_shell"]
        self.assertEqual(uneq["n_shells"], 3)
        self.assertFalse(uneq["reducible_to_one_gap"])
        ratios = list(uneq["Tc_over_T_shell"].values())
        self.assertGreater(max(ratios) - min(ratios), 100.0)

    def test_phase_changes_sign(self):
        row = record()
        iso = row["numerical"]["iso_phase_scan"]
        uneq = row["numerical"]["uneq_phase_scan"]
        self.assertTrue(iso["changes_sign"])
        self.assertTrue(uneq["changes_sign"])
        self.assertGreater(iso["max"], 1.0)
        self.assertLess(iso["min"], -1.0)

    def test_one_shell_vacuous_on_core(self):
        f = one_shell_field()
        self.assertLess(abs(sum_Tk(f)), 1e-12)
        _E, _X, _Y, _Z, Lam = moments(f)
        self.assertAlmostEqual(T_c_direct(f, Lam), 0.0, places=12)
        u = three_shell_unequal()
        self.assertEqual(len({k: None for k in u.support()}), 6)


class FourierTrianglePageTests(unittest.TestCase):
    def test_page_separates_and_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("Exact identities", raw)
        self.assertIn("Numerical observations", raw)
        self.assertIn("Illustrative motion", raw)
        self.assertIn("Leray idle", raw)
        self.assertIn("Equal-length", raw)
        self.assertIn("Unequal-length", raw)
        self.assertIn("phase", text.lower())
        self.assertIn("I_3", raw)
        self.assertIn("Not prime", raw)
        self.assertIn("First missing", raw)
        self.assertIn("useful", text)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("stays killed", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)

    def test_i3_is_not_leftover_three(self):
        text = _plain(PAGE)
        self.assertIn("not leftover 3", text.lower())
        self.assertIn("not the Q-matrix", text)

    def test_pointers(self):
        for path in (
            STATUS,
            TAPE,
            TINY,
            LATEST,
            ISSUES,
            PLAN,
            PATH,
            DRIFT,
            BSTAR,
            PROOF,
            CLOSE,
        ):
            body = path.read_text()
            self.assertIn("FOURIER-TRIANGLE.md", body, msg=str(path))


if __name__ == "__main__":
    unittest.main()
