"""Independent DA audit of the Gate B trilinear / CS chain."""

from __future__ import annotations

import unittest

from domain_architect.cli import main as da_main
from domain_architect.trilinear_audit import audit_gate_b_trilinear


class TestTrilinearDAAudit(unittest.TestCase):
    def setUp(self):
        self.audit = audit_gate_b_trilinear()
        self.by_id = {s.step_id: s for s in self.audit.steps}

    def test_every_cs_use_is_named(self):
        for sid in ("CS-1", "CS-2", "CS-3"):
            self.assertIn(sid, self.by_id)
            self.assertIsNotNone(self.by_id[sid].cauchy_schwarz)

    def test_distinct_shell_hypothesis_fails(self):
        self.assertEqual(self.by_id["H-shell"].verdict, "fail")
        self.assertIn("linear independence", self.by_id["H-shell"].reason.lower())

    def test_counting_does_not_imply_trilinear_bound(self):
        self.assertEqual(self.by_id["CS-3"].verdict, "fail")
        self.assertEqual(self.by_id["G2"].verdict, "fail")
        self.assertIn("Gap", self.audit.board["Full multiplicity / trilinear inequality"])

    def test_cs1_and_g1_and_lb_pass(self):
        self.assertEqual(self.by_id["G1"].verdict, "pass")
        self.assertEqual(self.by_id["CS-1"].verdict, "pass")
        self.assertEqual(self.by_id["LB"].verdict, "pass")
        self.assertIn("θ ≥ 1/2", self.audit.board["Gate B lower bound (nonnegative Q)"])

    def test_promotion_is_split_not_a_new_upper_bound(self):
        step = self.by_id["PROMOTE"]
        self.assertEqual(step.verdict, "split")
        self.assertIn("Do not promote a new all-radii", step.reason)
        self.assertFalse(self.audit.theorem_17_proved)
        self.assertFalse(self.audit.ns_solved)

    def test_cs2_is_a_different_object(self):
        self.assertEqual(
            self.by_id["CS-2"].verdict, "pass_as_upper_bound_on_a_different_object"
        )

    def test_cli_trilinear_ns(self):
        rc = da_main(["--trilinear-ns"])
        self.assertEqual(rc, 0)

    def test_no_clay_language_in_narrative(self):
        text = self.audit.narrative().lower()
        self.assertNotIn("millennium prize", text)
        self.assertIn("ns is not solved", text)


if __name__ == "__main__":
    unittest.main()
