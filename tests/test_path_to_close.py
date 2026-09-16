"""Path to a close is a path, not a close. Route A is pairing, not L^inf."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from route_a_write import (  # noqa: E402
    amplitude_powers,
    embedding_a_plus_is_bkm,
    energy_linear_fails_amplitude,
    pairing_le_a_plus_z,
    tautological_k,
    tjj_e_false_t_over_d_sq,
)

PATH = ROOT / "docs" / "PATH-TO-CLOSE.md"
ROUTE = ROOT / "docs" / "ROUTE-A-WRITE.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
CLOSE = ROOT / "docs" / "NS-CLOSE-REPORT.md"
C10 = ROOT / "docs" / "C10-CHAIN.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class RouteAArithmeticTests(unittest.TestCase):
    def test_pairing_matches_a_plus_z_and_beats_energy(self):
        self.assertTrue(pairing_le_a_plus_z(5, 7))
        p = amplitude_powers(5)
        self.assertEqual(p["pairing"], p["a_plus_Z"])
        self.assertLess(p["energy"], p["pairing"])
        self.assertTrue(energy_linear_fails_amplitude(2, 6))

    def test_e_false_and_locks(self):
        self.assertEqual(tjj_e_false_t_over_d_sq(16), 16)
        self.assertTrue(embedding_a_plus_is_bkm())
        self.assertEqual(tautological_k(12, 0, 4), 3)


class PathToCloseTests(unittest.TestCase):
    def test_path_does_not_close(self):
        raw = PATH.read_text()
        text = _plain(PATH)
        self.assertIn("Not a close", raw)
        self.assertIn("seated inequality", text)
        self.assertIn("G1", raw)
        self.assertIn("G5", raw)
        self.assertIn("A-pair", raw)
        self.assertIn("Route B", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("A is not B", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_route_a_is_pairing_not_linf(self):
        raw = ROUTE.read_text()
        text = _plain(ROUTE)
        self.assertIn("A-pair", raw)
        self.assertIn("Write or kill", raw)
        self.assertIn("BKM", raw)
        self.assertIn("tautological", text)
        self.assertIn("three shapes remain", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_pointers(self):
        for path in (STATUS, TAPE, TINY, LATEST, ISSUES, PLAN, CLOSE, C10):
            body = path.read_text()
            self.assertIn("PATH-TO-CLOSE.md", body, msg=str(path))
            self.assertIn("ROUTE-A-WRITE.md", body, msg=str(path))


if __name__ == "__main__":
    unittest.main()
