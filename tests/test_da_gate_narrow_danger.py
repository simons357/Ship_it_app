"""Honesty locks for the 24 Sep narrow-danger-parameter gate."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_gate_narrow_danger import prove_all, prove_narrow_substitutions  # noqa: E402

PACKET = ROOT / "packets" / "DA-GATE-NARROW-DANGER-2026-09-24.md"
LOCK = ROOT / "data" / "da_gate_narrow_danger_2026-09-24.json"


class TestDaGateNarrowDanger(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.proofs = prove_all()

    def test_open_locks(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertEqual(self.lock["missing_unsigned_assembly_4"], "OPEN")
        self.assertEqual(self.lock["L1_both_signs"], "OPEN")
        self.assertFalse(self.lock["middle_region_payable"])
        self.assertEqual(self.lock["universal_threshold_kappa_r_1"], "KILLED")
        self.assertEqual(self.lock["promote_F_het_r_to_assembled"], "FORBIDDEN")
        self.assertFalse(self.lock["local_estimate_5_reproved_here"])
        self.assertIn("NS not solved", self.page)
        self.assertFalse(self.proofs["ns_solved"])
        self.assertFalse(self.proofs["middle_region_payable"])

    def test_does_not_ship_other_gates(self) -> None:
        self.assertFalse(
            (ROOT / "packets" / "DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md").exists()
        )
        self.assertFalse(
            (ROOT / "packets" / "FOURIER-TRIANGLES-AUDIT-2026-09-20.md").exists()
        )
        self.assertFalse(
            (ROOT / "packets" / "LEMMA-STAR-SHAPE-FORM-2026-09-10.md").exists()
        )

    def test_substitutions(self) -> None:
        s = prove_narrow_substitutions()
        self.assertTrue(s["Ds_sqrt_identity"])
        self.assertTrue(s["Y_sqrt_is_kappa_X_sqrt"])
        self.assertTrue(s["reaches_6"])
        self.assertTrue(s["reaches_7"])
        self.assertTrue(s["not_one_over_kappa_r"])
        self.assertTrue(s["X_sqrt_over_kappa_sqrt_is_Hdot_half"])

    def test_fork_and_gate_language(self) -> None:
        self.assertIn("need dynamic loss", self.lock["L1_fork"]["L1_nonzero"])
        self.assertIn("another radial power", self.lock["L1_fork"]["L1_zero"])
        self.assertIn("FORBIDDEN", self.page)
        self.assertIn("real gate", self.page)
        self.assertIn("KILLED", self.page)


if __name__ == "__main__":
    unittest.main()
