"""B★ attack: families first; not a seated close; star stays killed."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from bstar_attack import (  # noqa: E402
    score,
    separated_triad,
    shear_field,
    one_shell_field,
)
from stokes_moments import high_triad_field, scale_field  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

PAGE = ROOT / "docs" / "BSTAR.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
PATH = ROOT / "docs" / "PATH-TO-CLOSE.md"
DRIFT = ROOT / "docs" / "CENTERED-DRIFT.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class BStarArithmeticTests(unittest.TestCase):
    def test_vn_kills_star_not_bstar(self):
        a = score(growing_layer_field(1), "v1")
        b = score(growing_layer_field(4), "v4")
        self.assertGreater(b["R_star"], a["R_star"])
        self.assertLess(b["R_B"], a["R_B"])
        self.assertGreater(a["R_B"], 0.0)

    def test_amplitude_matches_cubic(self):
        base = high_triad_field(amp=1.0)
        r1 = score(scale_field(base, 1.0), "A1")
        r3 = score(scale_field(base, 3.0), "A3")
        self.assertAlmostEqual(r1["R_B"], r3["R_B"], places=8)

    def test_shear_and_one_shell_vacuous(self):
        sh = score(shear_field(), "shear")
        one = score(one_shell_field(2), "one")
        self.assertAlmostEqual(sh["Tc"], 0.0, places=8)
        self.assertAlmostEqual(one["Ds"], 0.0, places=8)
        self.assertAlmostEqual(one["Tc"], 0.0, places=8)

    def test_separation_shrinks_ratio(self):
        close = score(separated_triad(1), "m1")
        far = score(separated_triad(8), "m8")
        self.assertGreater(close["R_B"], far["R_B"])
        self.assertLess(close["R_B"], 1.0)


class BStarPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not seated", raw)
        self.assertIn("Does not kill", raw)
        self.assertIn("useful", text)
        self.assertIn("OPEN", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)

    def test_pointers(self):
        for path in (STATUS, TAPE, TINY, LATEST, ISSUES, PLAN, PATH, DRIFT):
            self.assertIn("BSTAR.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
