"""Domain Architect process-machine smoke tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_machine import classify_claim, cosmos_drill, run_checker  # noqa: E402
from da_sixteen import SIXTEEN  # noqa: E402


class DaMachineTests(unittest.TestCase):
    def test_forbidden_close_fails(self):
        r = classify_claim("I solved NS and RH last May")
        self.assertEqual(r["verdict"], "fail")

    def test_theorem_p_lands_in_q(self):
        r = classify_claim("Theorem P: the prime block of Q-tilde sits above -1/4")
        self.assertEqual(r["domain"], "Q")
        self.assertEqual(r["verdict"], "open")

    def test_unassigned_stays_open(self):
        r = classify_claim("hello there")
        self.assertIsNone(r["domain"])
        self.assertEqual(r["verdict"], "open")

    def test_cosmos_drill_names_found_f_still_private(self):
        d = cosmos_drill()
        self.assertTrue(d["cosmos_list_found"])
        self.assertFalse(d["cosmos_core_equation_public"])
        self.assertEqual(d["n_confirmed"], 16)
        self.assertEqual(d["possibility_claim"]["verdict"], "open")
        self.assertEqual(len(d["layers"][0]["pieces"]), 16)
        self.assertEqual(d["layers"][2]["pieces"], ["log_cc_ratio", "log_hierarchy"])

    def test_sixteen_command_list_is_wired(self):
        self.assertEqual(len(SIXTEEN), 16)
        self.assertEqual(SIXTEEN[-1], "R")

    def test_fingers_claim_lands_in_u(self):
        r = classify_claim("five finger DA on the realization line")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_wave_claim_lands_in_u(self):
        r = classify_claim("can we use superposition and falsification on the waveform")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_sm_lagrangian_lands_in_u(self):
        r = classify_claim("analyze the Standard Model Lagrangian and the Weinberg rotation")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_dream_team_lands_in_u(self):
        r = classify_claim("bring in the dream team from beyond the digital divide")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_session_converse_lands_in_u(self):
        r = classify_claim("have the dream team converse and talk to each other")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")
        r2 = classify_claim("a virtual seance of carved-out kingdoms on one problem")
        self.assertEqual(r2["domain"], "U")
        self.assertEqual(r2["verdict"], "open")

    def test_harmonic_vocab_lands_in_u(self):
        r = classify_claim("can DA make a complete harmonic vocabulary out of mathematics")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_ground_destination_lands_in_u(self):
        r = classify_claim("harmonic universe as a spectrum not a bag of couplings; ask Feynman")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_pipe_think_tank_lands_in_u(self):
        r = classify_claim("pipe satellite and hologram data into the think tank")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_desk_writeup_lands_in_u(self):
        r = classify_claim("write up the whole desk and the corpus method")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_compute_techniques_land_in_u(self):
        r = classify_claim("computing techniques we can borrow: sympy and Dedalus")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_alert_lands_in_u(self):
        r = classify_claim("text me a plain language alert when something significant flips")
        self.assertEqual(r["domain"], "U")
        self.assertEqual(r["verdict"], "open")

    def test_tube_hardy_lands_in_b_and_solved_ns_fails(self):
        r = classify_claim("localized tube Hardy for Gamma, keep 1/r^4")
        self.assertEqual(r["domain"], "B")
        self.assertEqual(r["verdict"], "open")
        occ = classify_claim("occupation time of 3-CONC vs SPREAD")
        self.assertEqual(occ["domain"], "B")
        self.assertEqual(occ["verdict"], "open")
        glue = classify_claim("two-regime glue of B4c CONC to energy-class T")
        self.assertEqual(glue["domain"], "B")
        self.assertEqual(glue["verdict"], "open")
        ceil = classify_claim("energy ceiling on a frozen low-j packet")
        self.assertEqual(ceil["domain"], "B")
        self.assertEqual(ceil["verdict"], "open")
        climb = classify_claim("climbing CONC with a climb law for dj*/dt")
        self.assertEqual(climb["domain"], "B")
        self.assertEqual(climb["verdict"], "open")
        field = classify_claim("barycenter climb law from the vorticity field")
        self.assertEqual(field["domain"], "B")
        self.assertEqual(field["verdict"], "open")
        geo = classify_claim("strain eigenframe alignment on a vorticity packet")
        self.assertEqual(geo["domain"], "B")
        self.assertEqual(geo["verdict"], "open")
        stretch = classify_claim("stretching budget and weighted alignment on a vorticity packet")
        self.assertEqual(stretch["domain"], "B")
        self.assertEqual(stretch["verdict"], "open")
        bal = classify_claim("enstrophy balance production versus dissipation on a vorticity packet")
        self.assertEqual(bal["domain"], "B")
        self.assertEqual(bal["verdict"], "open")
        ang = classify_claim("angular viscosity versus I_tube on a swirl packet")
        self.assertEqual(ang["domain"], "B")
        self.assertEqual(ang["verdict"], "open")
        coh = classify_claim("signed strain blob on a coherent CONC vorticity packet")
        self.assertEqual(coh["domain"], "B")
        self.assertEqual(coh["verdict"], "open")
        focc = classify_claim("field occupation of 3-CONC along a vorticity path")
        self.assertEqual(focc["domain"], "B")
        self.assertEqual(focc["verdict"], "open")
        fgl = classify_claim("field glue of the two-regime sketch against vorticity Ẋ")
        self.assertEqual(fgl["domain"], "B")
        self.assertEqual(fgl["verdict"], "open")
        nsc = classify_claim("NS climb of j_bar on a vorticity blob")
        self.assertEqual(nsc["domain"], "B")
        self.assertEqual(nsc["verdict"], "open")
        csk = classify_claim("climb sketch of prescribed c against a vorticity window")
        self.assertEqual(csk["domain"], "B")
        self.assertEqual(csk["verdict"], "open")
        lng = classify_claim("longer path of a vorticity packet past the climb room time")
        self.assertEqual(lng["domain"], "B")
        self.assertEqual(lng["verdict"], "open")
        dns = classify_claim("packet DNS as an a priori bound for vorticity")
        self.assertEqual(dns["domain"], "B")
        self.assertEqual(dns["verdict"], "open")
        tb = classify_claim("tube budget of vorticity as an a priori")
        self.assertEqual(tb["domain"], "B")
        self.assertEqual(tb["verdict"], "open")
        aln = classify_claim("alignment as an a priori bound for vorticity")
        self.assertEqual(aln["domain"], "B")
        self.assertEqual(aln["verdict"], "open")
        pay = classify_claim("aligned stretching payers on a vorticity packet")
        self.assertEqual(pay["domain"], "B")
        self.assertEqual(pay["verdict"], "open")
        net = classify_claim("enstrophy net as an a priori bound for vorticity")
        self.assertEqual(net["domain"], "B")
        self.assertEqual(net["verdict"], "open")
        blob = classify_claim("signed blob as an a priori bound for vorticity")
        self.assertEqual(blob["domain"], "B")
        self.assertEqual(blob["verdict"], "open")
        clock = classify_claim("field clock as an a priori bound for vorticity")
        self.assertEqual(clock["domain"], "B")
        self.assertEqual(clock["verdict"], "open")
        match = classify_claim("matching the sketch as an a priori bound for vorticity")
        self.assertEqual(match["domain"], "B")
        self.assertEqual(match["verdict"], "open")
        bad = classify_claim("I solved NS last May")
        self.assertEqual(bad["verdict"], "fail")

    def test_check_b_stays_open_when_lemmas_hold(self):
        result = run_checker("B")
        self.assertEqual(result["verdict"], "open")
        self.assertIn("Regularity stays open", result["reason"])


if __name__ == "__main__":
    unittest.main()
