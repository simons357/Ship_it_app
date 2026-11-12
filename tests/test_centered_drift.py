"""Centered drift: identities sit, remainder open, NS not solved."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "ns_attacks"))

import centered_drift as cd  # noqa: E402

DOCS = ROOT / "docs" / "ns-review"
EQ_PAGE = DOCS / "CENTERED-EQUATION.md"
DRIFT_PAGE = DOCS / "CENTERED-DRIFT.md"
PACKET = ROOT / "packets" / "DA-GATE-CENTERED-DRIFT-2026-11-12.md"
JSON_PATH = ROOT / "results" / "centered_drift.json"


class TestCenteredEquationPage(unittest.TestCase):
    def test_equation_is_the_identity(self) -> None:
        text = EQ_PAGE.read_text(encoding="utf-8")
        self.assertIn(r"\Lambda'", text)
        self.assertIn(r"-\frac{2\nu}{X}D_s", text)
        self.assertIn(r"+\frac{2}{X}T_c", text)
        self.assertIn("That is the centered equation.", text)
        self.assertIn("This is not (4).", text)
        self.assertIn("This is not Young.", text)
        self.assertIn("This is not Need★.", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)


class TestCenteredDriftPage(unittest.TestCase):
    def test_inventory_locks_and_open_remainder(self) -> None:
        text = DRIFT_PAGE.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Centered spectral drift"))
        self.assertIn(r"T_c=M-\Lambda N", text)
        self.assertIn("The centered equation", text)
        self.assertIn(r"T_c=\frac{16}{5}", text)
        self.assertIn("OPEN", text)
        self.assertIn("Ordinary unaugmented 3-D", text)
        self.assertIn("Navier–Stokes is not solved", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertIn(r"Do not put \(K(t)\)", text)
        self.assertIn("in the PDE.", text)
        self.assertIn("Need★", text)
        self.assertIn("MISSING", text)

    def test_packet_refuses_a_close(self) -> None:
        text = PACKET.read_text(encoding="utf-8")
        self.assertIn("OPEN", text)
        self.assertIn("ns_solved", text)
        self.assertIn("false", text)
        self.assertIn("NS is not solved", text)


class TestNoteTriad(unittest.TestCase):
    def test_near_scale_triad_matches_note(self) -> None:
        rec = cd.record(cd.near_scale_triad())
        self.assertTrue(rec["div_free"] and rec["real"])
        self.assertEqual(rec["X"], 10)
        self.assertEqual(rec["Y"], 14)
        self.assertEqual(rec["Z"], 22)
        self.assertAlmostEqual(rec["Lambda"], 7 / 5)
        self.assertAlmostEqual(rec["D_s"], 12 / 5)
        self.assertEqual(rec["tau"]["(1, 0, 0)"], 0)
        self.assertEqual(rec["tau"]["(-1, 0, 0)"], 0)
        self.assertEqual(rec["tau"]["(0, 1, 0)"], -1)
        self.assertEqual(rec["tau"]["(0, -1, 0)"], -1)
        self.assertEqual(rec["tau"]["(1, 1, 0)"], 1)
        self.assertEqual(rec["tau"]["(-1, -1, 0)"], 1)
        self.assertEqual(rec["N"], 2)
        self.assertEqual(rec["M"], 6)
        self.assertAlmostEqual(rec["T_c"], 16 / 5)
        self.assertAlmostEqual(rec["T_c_direct"], 16 / 5)
        self.assertAlmostEqual(rec["T_c"] / rec["D_s"], 4 / 3)
        self.assertFalse(rec["ns_solved"])
        self.assertTrue(rec["remainder_open"])

    def test_two_writings_of_Ds_and_Tc_agree(self) -> None:
        rec = cd.record(cd.near_scale_triad())
        self.assertAlmostEqual(rec["D_s"], rec["D_s_direct"], places=12)
        self.assertAlmostEqual(rec["T_c"], rec["T_c_direct"], places=12)

    def test_barycenter_rewrite(self) -> None:
        rec = cd.record(cd.near_scale_triad())
        bary = rec["barycenter"]
        self.assertAlmostEqual(bary["mean_lambda"], rec["Lambda"], places=12)
        self.assertAlmostEqual(bary["D_s_from_var"], rec["D_s"], places=12)
        self.assertAlmostEqual(bary["T_c_from_cov"], rec["T_c"], places=12)
        self.assertAlmostEqual(bary["D_s_check"], 0.0, places=12)
        self.assertAlmostEqual(bary["T_c_check"], 0.0, places=12)

    def test_algebraic_centered_equation(self) -> None:
        rec = cd.record(cd.near_scale_triad())
        for nu in (0.0, 0.1, 1.0, 7.0):
            alg = cd.algebraic_identity(nu, rec["X"], rec["Y"], rec["Z"], rec["N"], rec["M"])
            self.assertAlmostEqual(alg["residual"], 0.0, places=12)


class TestKilledAndVacuous(unittest.TestCase):
    def test_sign_flips_and_amplitude_kills_pure_absorption(self) -> None:
        field = cd.near_scale_triad()
        plus = cd.record(field)
        minus = cd.record(field.scale(-1))
        self.assertAlmostEqual(minus["T_c"] + plus["T_c"], 0.0, places=12)
        self.assertAlmostEqual(minus["D_s"], plus["D_s"], places=12)
        twice = cd.record(field.scale(2))
        self.assertAlmostEqual(twice["T_c"] / twice["D_s"], 2 * (4 / 3), places=12)
        kill = cd.amplitude_kill(field)
        self.assertEqual(kill["pure_absorption_T_c_le_C_nu_Ds"], "KILLED")
        for value in kill["ratio_over_a_constant"]:
            self.assertAlmostEqual(value, 4 / 3, places=12)

    def test_exact_shell_vanishes(self) -> None:
        rec = cd.record(cd.single_shell_field())
        self.assertAlmostEqual(rec["Lambda"], 1.0, places=12)
        self.assertAlmostEqual(rec["D_s"], 0.0, places=12)
        self.assertAlmostEqual(rec["T_c"], 0.0, places=12)

    def test_two_shell_closed_form(self) -> None:
        rec = cd.record(cd.two_shell_field())
        closed = rec["two_shell"]
        self.assertIsNotNone(closed)
        self.assertAlmostEqual(closed["D_s_closed"], rec["D_s"], places=12)
        self.assertGreater(rec["D_s"], 0.0)

    def test_near_shell_ratio_blows(self) -> None:
        scan = cd.near_shell_scan()
        rows = scan["rows"]
        ratios = [row["T_c_over_D_s"] for row in rows]
        for earlier, later in zip(ratios, ratios[1:]):
            self.assertGreater(later, earlier)
        self.assertGreater(ratios[-1], 10.0)
        # Linearization is asymptotic: T_c/eps and D_s/eps^2 settle as eps -> 0.
        self.assertAlmostEqual(rows[-1]["T_c_over_eps"], rows[-2]["T_c_over_eps"], places=1)
        self.assertAlmostEqual(rows[-1]["D_s_over_eps2"], rows[-2]["D_s_over_eps2"], places=1)
        self.assertAlmostEqual(rows[-1]["T_c_over_D_s"] * rows[-1]["eps"], 1.0, places=1)


class TestPackageFlags(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cd.main()
        cls.payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    def test_json_refuses_a_close(self) -> None:
        self.assertFalse(self.payload["ns_solved"])
        self.assertFalse(self.payload["lemma_star_proved"])
        self.assertTrue(self.payload["remainder_open"])
        self.assertEqual(self.payload["identity"], "EXACT")
        self.assertEqual(self.payload["drift_estimate"], "OPEN")
        self.assertEqual(self.payload["uniform_remainder"], "KILLED")
        self.assertEqual(self.payload["need_star"], "MISSING")
        self.assertTrue(self.payload["do_not_put_K_in_the_PDE"])

    def test_locked_note_numbers_in_json(self) -> None:
        locked = self.payload["note_triad"]["locked"]
        rec = self.payload["note_triad"]
        self.assertAlmostEqual(rec["T_c"], locked["T_c"])
        self.assertAlmostEqual(rec["D_s"], locked["D_s"])
        self.assertAlmostEqual(rec["T_c_over_D_s"], locked["T_c_over_D_s"])
        self.assertAlmostEqual(rec["algebra"]["residual"], 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
