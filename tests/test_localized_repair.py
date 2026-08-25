#!/usr/bin/env python3
"""Localized reparation cuts diseased steps and grafts an OPEN hook.

It does not close Navier–Stokes and it does not call inverse design.
"""

from __future__ import annotations

import json
import unittest

from domain_architect.app import handle_api
from domain_architect.localized_repair import (
    DELTA_0,
    ETA_STAR_AUDIT,
    LOCAL_EXISTENCE_L1,
    PAPER2_CHAIN,
    cycle_localized_repair,
    localized_repair,
    simplex_concentration_diagnostic,
)
from domain_architect.pipeline import run_named_cycle
from domain_architect.schema import CorrespondenceKind, ValidationGate
from domain_architect.synthesize import inverse_design_architecture


class TestPaper2DefaultSurgery(unittest.TestCase):
    def test_keeps_lipschitz_and_weyl_cuts_t2(self):
        payload = localized_repair()
        self.assertEqual(payload["protocol"], "localized-reparation")
        self.assertEqual(payload["chain_name"], "paper2")
        self.assertFalse(payload["closed"])
        original_ids = [s["id"] for s in payload["original_chain"]]
        self.assertEqual(len(original_ids), 10)
        self.assertEqual(original_ids[1], "frozen-gap")
        excised = {s["id"] for s in payload["excised"]}
        self.assertIn("t2-closed", excised)
        self.assertIn("local-existence-as-target", excised)
        self.assertIn("lemma-6-1", excised)
        self.assertNotIn("lemma-3-1", excised)
        self.assertNotIn("theorem-4-1", excised)
        remaining = {s["id"] for s in payload["repaired_chain"]}
        self.assertIn("lemma-3-1", remaining)
        self.assertIn("theorem-4-1", remaining)
        self.assertIn("leray-setup", remaining)
        self.assertIn("continuation", remaining)
        self.assertNotIn("t2-closed", remaining)
        self.assertEqual(payload["chosen"]["id"], "independent-simplex-hypothesis")
        self.assertTrue(payload["chosen"]["accepted"])
        self.assertFalse(payload["chosen"]["closed"])
        self.assertEqual(payload["kind"], CorrespondenceKind.ANALOGY.value)
        self.assertIn("FIXED.tex", payload["june_fixed_tex"])
        self.assertIn("did not", payload["june_fixed_tex"])

    def test_proximal_and_distal_are_healthy_neighbors(self):
        payload = localized_repair()
        self.assertEqual(payload["proximal"]["id"], "product-arithmetic")
        self.assertEqual(payload["proximal"]["status"], "healthy")
        self.assertEqual(payload["distal"]["id"], "continuation")
        self.assertEqual(payload["distal"]["status"], "open")

    def test_local_existence_is_ranked_and_rejected(self):
        payload = localized_repair()
        by_id = {c["id"]: c for c in payload["candidates"]}
        loc = by_id["local-existence-bound-2"]
        self.assertEqual(loc["score"], 0.0)
        self.assertFalse(loc["accepted"])
        ratio = loc["computation"]["ratio"]
        self.assertGreater(ratio, 50)
        self.assertAlmostEqual(LOCAL_EXISTENCE_L1 / ETA_STAR_AUDIT, ratio)
        self.assertAlmostEqual(DELTA_0, 0.20)

    def test_glue_and_pd_are_refused(self):
        payload = localized_repair()
        by_id = {c["id"]: c for c in payload["candidates"]}
        self.assertEqual(by_id["ring-snd-glue"]["kind"], "refused")
        self.assertEqual(by_id["q6-hn-floor"]["kind"], "refused")
        self.assertEqual(by_id["pd-inverse-design"]["kind"], "refused")
        joined = " ".join(payload["refused"]).lower()
        self.assertIn("pd", joined)
        self.assertIn("clay", joined)
        self.assertIn("t2 closed", joined)


class TestExciseStepTwo(unittest.TestCase):
    def test_paper2_step_2_frozen_gap(self):
        payload = localized_repair(excise=2)
        excised = [s["id"] for s in payload["excised"]]
        self.assertEqual(excised, ["frozen-gap"])
        self.assertEqual(payload["proximal"]["id"], "leray-setup")
        self.assertEqual(payload["distal"]["id"], "lemma-3-1")
        self.assertEqual(payload["chosen"]["id"], "independent-frozen-gap-hypothesis")
        self.assertFalse(payload["chosen"]["closed"])
        remaining = {s["id"] for s in payload["repaired_chain"]}
        self.assertIn("lemma-3-1", remaining)
        self.assertIn("theorem-4-1", remaining)
        self.assertNotIn("frozen-gap", remaining)
        self.assertEqual(payload["operation"]["excise"], [2])
        self.assertEqual(payload["operation"]["reinsert"], 2)
        self.assertFalse(payload["operation"]["fix_is_a_proof"])
        self.assertTrue(payload["operation"]["order_preserved"])
        indices = [s["index"] for s in payload["repaired_chain"]]
        self.assertEqual(indices, list(range(1, 11)))
        self.assertTrue(payload["repaired_chain"][1]["id"].endswith("-graft"))
        self.assertEqual(payload["repaired_chain"][0]["id"], "leray-setup")
        self.assertEqual(payload["repaired_chain"][2]["id"], "lemma-3-1")
        self.assertIn("EXCISE", payload["board"]["text"])
        self.assertIn("GRAFT", payload["board"]["text"])
        self.assertIn("frozen-gap", payload["board"]["text"])
        self.assertIn("Yes.", payload["answer"])

    def test_toy_chain_excise_2(self):
        payload = localized_repair(chain="toy", excise=2)
        self.assertEqual(payload["chain_name"], "toy")
        self.assertEqual([s["id"] for s in payload["excised"]], ["toy-energy-implies-smallness"])
        self.assertEqual(payload["proximal"]["id"], "toy-energy")
        self.assertEqual(payload["distal"]["id"], "toy-continuation")
        self.assertEqual(payload["chosen"]["id"], "independent-smallness-hypothesis")
        self.assertFalse(payload["closed"])
        self.assertIn("energy-implies-smallness", {c["id"] for c in payload["candidates"]})

    def test_bad_index_raises(self):
        with self.assertRaises(ValueError):
            localized_repair(excise=99)


class TestSimplexDiagnostic(unittest.TestCase):
    def test_random_simplex_is_not_eta_star_close(self):
        diag = simplex_concentration_diagnostic()
        self.assertGreater(diag["mean_l1"], 0.2)
        self.assertGreater(diag["min_l1"], ETA_STAR_AUDIT)
        self.assertEqual(diag["fraction_within_eta_star"], 0.0)
        self.assertGreater(diag["local_existence_over_eta_star"], 50)
        payload = localized_repair()
        by_id = {c["id"]: c for c in payload["candidates"]}
        self.assertFalse(by_id["dirichlet-random-samples"]["accepted"])
        self.assertEqual(by_id["dirichlet-random-samples"]["computation"]["seed"], diag["seed"])


class TestCycleAndApi(unittest.TestCase):
    def test_cycle_does_not_emit_pd_loop(self):
        report = cycle_localized_repair()
        self.assertEqual(report.mode, "localized-repair")
        self.assertEqual(report.validation_gate, ValidationGate.MATHEMATICAL)
        self.assertEqual(report.candidate.name, "localized_reparation_open")
        blob = json.dumps(report.to_dict()).lower()
        self.assertNotIn("control u = k", blob)
        self.assertIn("localized-reparation", blob)
        self.assertIn("open", blob)
        self.assertEqual(report.translation.kind, CorrespondenceKind.ANALOGY)
        self.assertEqual(report.translation.mapping, {})
        self.assertFalse(report.prediction["closed"])

    def test_named_cycle_aliases(self):
        for name in ("localized-repair", "surgery", "paper2-surgery"):
            report = run_named_cycle(name)
            self.assertEqual(report.mode, "localized-repair")
            self.assertEqual(report.prediction["protocol"], "localized-reparation")

    def test_named_cycle_excise_two(self):
        report = run_named_cycle("excise-2")
        self.assertEqual(report.mode, "localized-repair")
        self.assertEqual(report.prediction["operation"]["excise"], [2])
        self.assertEqual(report.prediction["repaired_chain"][1]["index"], 2)
        self.assertTrue(report.prediction["repaired_chain"][1]["id"].endswith("-graft"))
        self.assertIn("Step 2", report.candidate.hypothesis)
        self.assertIn("Yes.", report.notes[0])

    def test_api_cycle_excise_two(self):
        status, body, _ = handle_api("/api/cycle", {"name": "excise-2"})
        self.assertEqual(status, 200)
        report = json.loads(body)
        self.assertEqual(report["prediction"]["operation"]["excise"], [2])

    def test_api_default_and_excise_two(self):
        status, body, _ = handle_api("/api/localized-repair", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["chosen"]["id"], "independent-simplex-hypothesis")
        status, body, _ = handle_api("/api/localized-repair", {"excise": 2})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["excised"][0]["id"], "frozen-gap")

    def test_inverse_design_of_ns_is_still_the_a13_hole(self):
        cand = inverse_design_architecture(
            "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl",
            ["classical NS"],
        )
        self.assertTrue(any("control u" in c for c in cand.components))

    def test_paper2_chain_step_two_is_frozen_gap(self):
        self.assertEqual(PAPER2_CHAIN[1].id, "frozen-gap")
        self.assertEqual(PAPER2_CHAIN[1].index, 2)
        self.assertEqual(PAPER2_CHAIN[5].id, "lemma-6-1")
        self.assertEqual(PAPER2_CHAIN[7].id, "t2-closed")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
