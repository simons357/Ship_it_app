#!/usr/bin/env python3
"""Localized reparation cuts diseased steps and grafts an OPEN hook.

It does not close Navier–Stokes and it does not call inverse design.
Default dataset: classical unaugmented 9-step chain. Leftover cut is 7–8.
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


class TestClassicalDefaultChain(unittest.TestCase):
    def test_nine_program_steps_step_two_is_proved_ring_lemma(self):
        self.assertEqual(len(PAPER2_CHAIN), 9)
        self.assertEqual(PAPER2_CHAIN[1].id, "ring-lemma-ns6")
        self.assertIn("ring-lemma", PAPER2_CHAIN[1].id)
        self.assertEqual(PAPER2_CHAIN[1].index, 2)
        self.assertEqual(PAPER2_CHAIN[1].status, "healthy")
        self.assertIn("PROVED", PAPER2_CHAIN[1].notes)
        self.assertEqual(PAPER2_CHAIN[3].id, "frozen-gap-route-j")
        self.assertEqual(PAPER2_CHAIN[3].index, 4)
        self.assertEqual(PAPER2_CHAIN[3].status, "open")
        self.assertIn("NUMERICAL", PAPER2_CHAIN[3].notes)
        self.assertEqual(PAPER2_CHAIN[6].id, "lemma-6-1-simplex")
        self.assertEqual(PAPER2_CHAIN[7].id, "dynamic-snd-ns10")
        self.assertEqual(PAPER2_CHAIN[8].id, "continuation")
        self.assertNotIn("not_claimed", {s.status for s in PAPER2_CHAIN})


class TestPaper2DefaultSurgery(unittest.TestCase):
    def test_keeps_proved_steps_cuts_leftover_7_and_8(self):
        payload = localized_repair()
        self.assertEqual(payload["protocol"], "localized-reparation")
        self.assertEqual(payload["chain_name"], "paper2")
        self.assertFalse(payload["closed"])
        original_ids = [s["id"] for s in payload["original_chain"]]
        self.assertEqual(len(original_ids), 9)
        self.assertEqual(original_ids[1], "ring-lemma-ns6")
        self.assertIn("ring-lemma", original_ids[1])
        excised = {s["id"] for s in payload["excised"]}
        self.assertIn("lemma-6-1-simplex", excised)
        self.assertIn("dynamic-snd-ns10", excised)
        self.assertTrue(any("lemma-6-1" in i for i in excised))
        self.assertTrue(any("dynamic-snd" in i for i in excised))
        self.assertNotIn("ring-lemma-ns6", excised)
        self.assertFalse(any("ring-lemma" in i for i in excised))
        remaining = {s["id"] for s in payload["repaired_chain"]}
        self.assertIn("ring-lemma-ns6", remaining)
        self.assertIn("lemma-3-1-continuity", remaining)
        self.assertIn("weyl-master", remaining)
        self.assertIn("conditional-h1", remaining)
        self.assertIn("leray-energy", remaining)
        self.assertIn("continuation", remaining)
        self.assertNotIn("lemma-6-1-simplex", remaining)
        self.assertNotIn("dynamic-snd-ns10", remaining)
        self.assertEqual(payload["chosen"]["id"], "independent-simplex-hypothesis")
        self.assertTrue(payload["chosen"]["accepted"])
        self.assertFalse(payload["chosen"]["closed"])
        self.assertEqual(payload["kind"], CorrespondenceKind.ANALOGY.value)
        self.assertNotIn("TRANSFORMABLE", payload["kind"].upper())
        self.assertIn("not the June FIXED PDF compile", payload["not_june_fixed_compile"])
        self.assertIn("Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex", payload["controlling_face"])
        self.assertEqual(payload["not_claimed"][0]["id"], "classical-ns-11")
        self.assertEqual(payload["not_claimed"][0]["status"], "not_claimed")

    def test_proximal_and_distal_are_healthy_neighbors(self):
        payload = localized_repair()
        self.assertEqual(payload["proximal"]["id"], "conditional-h1")
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
        blob = json.dumps(payload).lower()
        self.assertNotIn("control u = k", blob)
        self.assertIn("transformable", joined)
        self.assertIn("no TRANSFORMABLE stamp", " ".join(payload["refused"]))


class TestExciseK(unittest.TestCase):
    def _assert_graft_at(self, payload, k, excised_id, proximal_id, distal_id):
        self.assertEqual([s["id"] for s in payload["excised"]], [excised_id])
        self.assertEqual(payload["proximal"]["id"], proximal_id)
        self.assertEqual(payload["distal"]["id"], distal_id)
        self.assertEqual(payload["operation"]["excise"], [k])
        self.assertEqual(payload["operation"]["reinsert"], k)
        self.assertFalse(payload["operation"]["fix_is_a_proof"])
        self.assertTrue(payload["operation"]["order_preserved"])
        self.assertFalse(payload["closed"])
        original = {s["index"]: s["id"] for s in payload["original_chain"]}
        for step in payload["repaired_chain"]:
            if step["index"] == k:
                self.assertTrue(step["id"].endswith("-graft"))
                self.assertEqual(step["status"], "open")
            else:
                self.assertEqual(step["id"], original[step["index"]])
        indices = [s["index"] for s in payload["repaired_chain"]]
        self.assertEqual(indices, sorted(indices))
        self.assertIn(k, indices)

    def test_paper2_excise_2_still_works_as_generic_k(self):
        payload = localized_repair(excise=2)
        self._assert_graft_at(
            payload, 2, "ring-lemma-ns6", "leray-energy", "lemma-3-1-continuity"
        )
        self.assertEqual(payload["chosen"]["id"], "independent-ring-geometry-hypothesis")
        self.assertFalse(payload["chosen"]["closed"])
        remaining = {s["id"] for s in payload["repaired_chain"]}
        self.assertIn("lemma-3-1-continuity", remaining)
        self.assertIn("weyl-master", remaining)
        self.assertNotIn("ring-lemma-ns6", remaining)
        self.assertEqual([s["index"] for s in payload["repaired_chain"]], list(range(1, 10)))
        self.assertIn("EXCISE", payload["board"]["text"])
        self.assertIn("GRAFT", payload["board"]["text"])
        self.assertIn("ring-lemma-ns6", payload["board"]["text"])
        self.assertIn("Yes.", payload["answer"])
        blob = json.dumps(payload).lower()
        self.assertIn("does not prove clay", blob)
        by_id = {c["id"]: c for c in payload["candidates"]}
        self.assertEqual(by_id["clay-from-ring-lemma"]["kind"], "refused")

    def test_excise_8_cuts_dynamic_snd(self):
        payload = localized_repair(excise=8)
        self._assert_graft_at(
            payload, 8, "dynamic-snd-ns10", "lemma-6-1-simplex", "continuation"
        )
        self.assertNotIn("dynamic-snd-ns10", {s["id"] for s in payload["repaired_chain"]})
        self.assertTrue(payload["repaired_chain"][7]["id"].endswith("-graft"))
        self.assertEqual(payload["repaired_chain"][6]["id"], "lemma-6-1-simplex")
        self.assertEqual(payload["repaired_chain"][8]["id"], "continuation")

    def test_excise_7_cuts_lemma_6_1(self):
        payload = localized_repair(excise=7)
        self._assert_graft_at(
            payload, 7, "lemma-6-1-simplex", "conditional-h1", "dynamic-snd-ns10"
        )
        self.assertEqual(payload["chosen"]["id"], "independent-simplex-hypothesis")
        self.assertNotIn("lemma-6-1-simplex", {s["id"] for s in payload["repaired_chain"]})

    def test_toy_chain_excise_2(self):
        payload = localized_repair(chain="toy", excise=2)
        self.assertEqual(payload["chain_name"], "toy")
        self._assert_graft_at(
            payload, 2, "toy-energy-implies-smallness", "toy-energy", "toy-continuation"
        )
        self.assertEqual(payload["chosen"]["id"], "independent-smallness-hypothesis")
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
        self.assertEqual(report.translation.kind, CorrespondenceKind.ANALOGY)

    def test_named_cycle_aliases(self):
        for name in ("localized-repair", "surgery", "paper2-surgery"):
            report = run_named_cycle(name)
            self.assertEqual(report.mode, "localized-repair")
            self.assertEqual(report.prediction["protocol"], "localized-reparation")
            excised = {s["id"] for s in report.prediction["excised"]}
            self.assertIn("lemma-6-1-simplex", excised)
            self.assertIn("dynamic-snd-ns10", excised)
            self.assertNotIn("ring-lemma-ns6", excised)

    def test_named_cycle_excise_k_and_hidden_alias(self):
        report = run_named_cycle("localized-repair", excise=8)
        self.assertEqual(report.mode, "localized-repair")
        self.assertEqual(report.prediction["operation"]["excise"], [8])
        self.assertTrue(report.prediction["repaired_chain"][7]["id"].endswith("-graft"))
        self.assertIn("Step 8", report.candidate.hypothesis)
        self.assertFalse(report.prediction["closed"])

        report = run_named_cycle("excise-2")  # hidden/test alias
        self.assertEqual(report.mode, "localized-repair")
        self.assertEqual(report.prediction["operation"]["excise"], [2])
        self.assertEqual(report.prediction["repaired_chain"][1]["index"], 2)
        self.assertTrue(report.prediction["repaired_chain"][1]["id"].endswith("-graft"))
        self.assertEqual(report.prediction["excised"][0]["id"], "ring-lemma-ns6")
        self.assertIn("Step 2", report.candidate.hypothesis)
        self.assertIn("Yes.", report.notes[0])

    def test_api_cycle_hidden_alias_excise_two(self):
        status, body, _ = handle_api("/api/cycle", {"name": "excise-2"})
        self.assertEqual(status, 200)
        report = json.loads(body)
        self.assertEqual(report["prediction"]["operation"]["excise"], [2])

    def test_api_default_and_excise_k(self):
        status, body, _ = handle_api("/api/localized-repair", {})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["chosen"]["id"], "independent-simplex-hypothesis")
        self.assertFalse(payload["closed"])
        excised = {s["id"] for s in payload["excised"]}
        self.assertIn("lemma-6-1-simplex", excised)
        self.assertIn("dynamic-snd-ns10", excised)
        self.assertNotIn("ring-lemma-ns6", excised)
        status, body, _ = handle_api("/api/localized-repair", {"excise": 2})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["excised"][0]["id"], "ring-lemma-ns6")
        self.assertEqual(payload["proximal"]["id"], "leray-energy")
        self.assertEqual(payload["distal"]["id"], "lemma-3-1-continuity")
        self.assertFalse(payload["closed"])
        status, body, _ = handle_api("/api/localized-repair", {"excise": 8})
        self.assertEqual(status, 200)
        payload = json.loads(body)
        self.assertEqual(payload["excised"][0]["id"], "dynamic-snd-ns10")
        self.assertTrue(payload["repaired_chain"][7]["id"].endswith("-graft"))
        self.assertEqual(payload["operation"]["reinsert"], 8)

    def test_cli_help_advertises_excise_k_not_excise_2(self):
        import io
        from contextlib import redirect_stderr, redirect_stdout

        from domain_architect.cli import main

        buf = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(buf), redirect_stderr(buf):
                main(["cycle", "--help"])
        text = buf.getvalue()
        self.assertIn("--excise", text)
        self.assertIn("localized-repair", text)
        self.assertNotIn("excise-2", text)

    def test_inverse_design_of_ns_fail_closes_a13(self):
        cand = inverse_design_architecture(
            "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl",
            ["classical NS"],
        )
        self.assertEqual(cand.name, "inverse_design[refused]")
        self.assertFalse(any("control u" in c for c in cand.components))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
