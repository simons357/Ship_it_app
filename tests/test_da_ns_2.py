"""DA-NS-2: identities sit, occupation tautology locked, integral OPEN."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "ns_attacks"))

import da_ns_2 as dn  # noqa: E402
from domain_architect.cli import main as da_main  # noqa: E402
from domain_architect.da_ns_2 import (  # noqa: E402
    CLAIM,
    STATUS,
    classify_last_line,
    express_as_proved,
    looks_like_da_ns_2,
    navigate_da_ns_2,
    refuse_proved,
)

DOCS = ROOT / "docs" / "ns-review"
PAGE = DOCS / "DA-NS-2.md"
PACKET = ROOT / "packets" / "DA-NS-2-2026-11-12.md"
JSON_PATH = ROOT / "results" / "da_ns_2.json"


class TestDANS2Page(unittest.TestCase):
    def test_page_locks_the_hole_and_refuses_a_close(self) -> None:
        text = PAGE.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# DA-NS-2"))
        self.assertIn(r"K_{\min,\theta}^{(n)}", text)
        self.assertIn(r"\sup_n\int_0^T", text)
        self.assertIn("The integral is the hole", text)
        self.assertIn("OPEN", text)
        self.assertIn("Y-cousin", text)
        self.assertIn("Joint Gap–Charge Epoch Budget", text)
        self.assertIn("Ordinary unaugmented", text)
        self.assertIn("Navier–Stokes is not solved", text)
        self.assertIn(r"Do not put \(K(t)\)", text)
        self.assertIn("in the PDE.", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertIn("KILLED", text)

    def test_packet_refuses_a_close(self) -> None:
        text = PACKET.read_text(encoding="utf-8")
        self.assertIn("OPEN", text)
        self.assertIn("ns_solved", text)
        self.assertIn("false", text)
        self.assertIn("NS is not solved", text)


class TestNoteTriadOccupation(unittest.TestCase):
    def test_near_scale_triad_matches_note(self) -> None:
        rec = dn.record(dn.near_scale_triad())
        self.assertEqual(rec["X"], 10)
        self.assertEqual(rec["Y"], 14)
        self.assertEqual(rec["Z"], 22)
        self.assertAlmostEqual(rec["Lambda"], 7 / 5)
        self.assertAlmostEqual(rec["D_s"], 12 / 5)
        self.assertEqual(rec["N"], 2)
        self.assertEqual(rec["M"], 6)
        self.assertAlmostEqual(rec["T_c"], 16 / 5)
        self.assertAlmostEqual(rec["T_c_direct"], 16 / 5)
        self.assertEqual(rec["da_ns_2"], "OPEN")
        self.assertFalse(rec["ns_solved"])

    def test_locked_k_min_at_nu_one(self) -> None:
        rec = dn.record(dn.near_scale_triad())
        k0 = dn.occupation(rec["T_c"], rec["D_s"], rec["Y"], 1.0, 0.0)
        kh = dn.occupation(rec["T_c"], rec["D_s"], rec["Y"], 1.0, 0.5)
        self.assertAlmostEqual(k0, 8 / 35)
        self.assertAlmostEqual(kh, 1 / 7)

    def test_tautology_is_an_identity(self) -> None:
        rec = dn.record(dn.near_scale_triad())
        for theta in (0.0, 0.5, 0.99):
            ident = dn.tautology_identity(rec, 1.0, theta)
            self.assertAlmostEqual(ident["residual"], 0.0, places=12)
            self.assertTrue(ident["is_identity_not_theorem"])

    def test_x_cousin_is_lambda_times_k_min(self) -> None:
        rec = dn.record(dn.near_scale_triad())
        row = dn.k_min_row(rec, 1.0, 0.5)
        self.assertAlmostEqual(row["K_X"], rec["Lambda"] * row["K_min"], places=12)

    def test_log_lambda_prime_bounded_by_two_k_min(self) -> None:
        rec = dn.record(dn.near_scale_triad())
        for theta in (0.0, 0.5, 0.99):
            bound = dn.algebraic_log_bound(rec, 1.0, theta)
            self.assertTrue(bound["log_Lambda_prime_le_2_K_min"])
            self.assertAlmostEqual(bound["rewrite_residual"], 0.0, places=12)
            self.assertGreater(bound["frozen_theta_leftover"], 0.0)


class TestKilledCloses(unittest.TestCase):
    def test_amplitude_kills_pure_absorption(self) -> None:
        field = dn.near_scale_triad()
        twice = dn.record(field.scale(2))
        once = dn.record(field)
        self.assertAlmostEqual(twice["T_c"] / twice["D_s"], 2 * (4 / 3), places=12)
        kill = dn.amplitude_occupation(field)
        self.assertEqual(kill["pure_absorption_T_c_le_theta_nu_Ds"], "KILLED")
        # Y scales as a^2, T_c as a^3, so K_min(theta=0) scales as |a|.
        k1 = dn.occupation(once["T_c"], once["D_s"], once["Y"], 1.0, 0.0)
        k2 = dn.occupation(twice["T_c"], twice["D_s"], twice["Y"], 1.0, 0.0)
        self.assertAlmostEqual(k2 / k1, 2.0, places=12)

    def test_phase_twins_hide_the_sign(self) -> None:
        twin = dn.phase_twin_occupation()
        self.assertTrue(twin["same_Y"] and twin["same_D_s"])
        self.assertAlmostEqual(twin["T_c_plus"] + twin["T_c_minus"], 0.0, places=12)
        self.assertGreater(twin["K_min_plus"], 0.0)
        self.assertEqual(twin["K_min_minus"], 0.0)
        self.assertFalse(twin["quadratic_moments_see_the_sign"])

    def test_exact_shell_vanishes(self) -> None:
        rec = dn.record(dn.single_shell_field())
        self.assertAlmostEqual(rec["D_s"], 0.0, places=12)
        self.assertAlmostEqual(rec["T_c"], 0.0, places=12)
        self.assertEqual(dn.occupation(rec["T_c"], rec["D_s"], rec["Y"], 1.0, 0.5), 0.0)

    def test_near_shell_ratio_blows_but_snapshot_k_min_does_not_close(self) -> None:
        scan = dn.near_shell_occupation()
        ratios = [row["T_c_over_D_s"] for row in scan["rows"]]
        for earlier, later in zip(ratios, ratios[1:]):
            self.assertGreater(later, earlier)
        self.assertGreater(ratios[-1], 10.0)
        self.assertTrue(scan["not_a_C_geom_theorem"])


class TestLastLineGate(unittest.TestCase):
    def test_forbidden_last_lines_rejected(self) -> None:
        for line in ("int D_s/Y", "sup Lambda", "Serrin", "BKM", "int Y"):
            hit = classify_last_line(line)
            self.assertEqual(hit["status"], "REJECTED", msg=line)
            self.assertEqual(hit["da_ns_2"], "OPEN")

    def test_jgc_language_is_spec_only(self) -> None:
        hit = classify_last_line(
            "Joint Gap-Charge Epoch Budget: charge, radial covariance, "
            "moving-barycenter error, homochiral drift, cross-band flux, "
            "phase/far terms, one-use dissipation, summable resets"
        )
        self.assertEqual(hit["status"], "SPEC_ONLY")
        self.assertEqual(hit["da_ns_2"], "OPEN")
        self.assertGreaterEqual(len(hit["jgc_hits"]), 6)


class TestDomainArchitectCard(unittest.TestCase):
    def test_navigate_stays_open(self) -> None:
        card = navigate_da_ns_2()
        self.assertEqual(card.status, "OPEN")
        self.assertFalse(card.ns_solved)
        self.assertFalse(card.lemma_star_proved)
        self.assertEqual(card.integral_bound, "OPEN")
        self.assertEqual(card.jgc_epoch_budget, "NOT_SEATED")
        self.assertTrue(card.do_not_put_K_in_the_PDE)
        self.assertEqual(STATUS, "OPEN")
        self.assertIn("int_0^T", CLAIM)
        self.assertIn("Y^(n)", CLAIM)

    def test_refuse_proved(self) -> None:
        refusal = refuse_proved()
        self.assertFalse(refusal["accepted"])
        self.assertTrue(refusal["forbidden"])
        self.assertFalse(express_as_proved()["accepted"])

    def test_recognition(self) -> None:
        self.assertTrue(looks_like_da_ns_2("DA-NS-2"))
        self.assertTrue(looks_like_da_ns_2("the Y-cousin occupation bound"))
        self.assertTrue(looks_like_da_ns_2("K_min,theta"))
        self.assertFalse(looks_like_da_ns_2("nabla^2 Phi = 4 pi G rho"))

    def test_cli_da_ns_2(self) -> None:
        self.assertEqual(da_main(["--da-ns-2"]), 0)
        self.assertEqual(da_main(["--navigate", "DA-NS-2"]), 0)
        self.assertEqual(da_main(["DA-NS-2"]), 0)

    def test_registry_books_the_leftover(self) -> None:
        from domain_architect.registry import EquationRegistry

        registry = EquationRegistry.load_default()
        rec = registry.equations["NS-H001"]
        self.assertEqual(rec.audit_disposition, "UNRESOLVED")
        self.assertIn("K_min", rec.original_expression)
        self.assertTrue(any(c.left_id == "NS-H001" for c in registry.conflicts))
        self.assertTrue(any(n.null_id == "NULL-DA-NS-2-TAUTOLOGY" for n in registry.nulls))


class TestPackageFlags(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        dn.main()
        cls.payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    def test_json_refuses_a_close(self) -> None:
        self.assertFalse(self.payload["ns_solved"])
        self.assertFalse(self.payload["lemma_star_proved"])
        self.assertEqual(self.payload["status"], "OPEN")
        self.assertEqual(self.payload["integral_bound"], "OPEN")
        self.assertEqual(self.payload["jgc_epoch_budget"], "NOT_SEATED")
        self.assertTrue(self.payload["do_not_put_K_in_the_PDE"])
        self.assertEqual(
            self.payload["amplitude_kill"]["pure_absorption_T_c_le_theta_nu_Ds"],
            "KILLED",
        )
        self.assertEqual(
            self.payload["inherited_kills"]["charge_only_net_coercivity"],
            "KILLED",
        )

    def test_locked_note_numbers_in_json(self) -> None:
        rec = self.payload["note_triad"]
        locked = rec["locked"]
        self.assertAlmostEqual(rec["T_c"], locked["T_c"])
        self.assertAlmostEqual(rec["Y"], locked["Y"])
        self.assertAlmostEqual(rec["K_min_nu1"]["theta_0"], rec["K_min_nu1"]["locked_theta_0"])
        self.assertAlmostEqual(rec["tautology"]["residual"], 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
