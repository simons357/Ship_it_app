#!/usr/bin/env python3
"""Acceptance tests for Process Console v5.

The console must represent Q4-1 v1 as INCONCLUSIVE, expose the failed
consistency check, and refuse promotion — independently of any
scientific outcome written on the record.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from domain_architect.process_console import ProcessConsole
from domain_architect.process_schema import ProcessRun, SchemaError, parse_stamp_kind
from domain_architect.q4_runs import Q4_1_V1_ID, Q4_1_V2_ID, q4_1_v1_historical
from domain_architect.schema import SCHEMA_VERSION, ProcessStatus, StampKind
from domain_architect.stamps import relabel_stamp


class TestSchemaV5Stamps(unittest.TestCase):
    def test_stamp_kinds_are_schema_not_prose(self):
        self.assertEqual(
            {k.value for k in StampKind},
            {"proved", "reproduced", "consistency_check"},
        )
        self.assertIn("independently checked", StampKind.PROVED.label)
        self.assertIn("independent computation matched", StampKind.REPRODUCED.label)
        self.assertIn("stipulated formula", StampKind.CONSISTENCY_CHECK.label)

    def test_opaque_da_stamped_is_not_a_kind(self):
        with self.assertRaises(SchemaError):
            parse_stamp_kind("DA-STAMPED")
        refused = relabel_stamp("DA-STAMPED")
        self.assertFalse(refused.accepted)
        relabeled = relabel_stamp("DA-STAMPED", intended_kind="consistency_check")
        self.assertTrue(relabeled.accepted)
        self.assertEqual(relabeled.kind, StampKind.CONSISTENCY_CHECK)


class TestQ41V1Inconclusive(unittest.TestCase):
    def test_console_displays_inconclusive(self):
        snap = ProcessConsole().snapshot()
        view = snap.view_for(Q4_1_V1_ID)
        self.assertEqual(view.process_status, ProcessStatus.INCONCLUSIVE)
        html = ProcessConsole().render_html()
        self.assertIn("INCONCLUSIVE", html)
        self.assertIn(Q4_1_V1_ID, html)
        self.assertIn('data-process-status="inconclusive"', html)

    def test_failed_consistency_check_is_exposed(self):
        view = ProcessConsole().snapshot().view_for(Q4_1_V1_ID)
        self.assertTrue(view.failed_checks)
        failed = view.failed_checks[0]
        self.assertFalse(failed["passed"])
        self.assertIn("D_s", failed["stipulated_formula"])
        self.assertIn("3915/663", failed["implementation"])
        html = ProcessConsole().render_html()
        self.assertIn("Failed consistency check", html)
        self.assertIn("3915/663", html)

    def test_promotion_to_evidence_is_prohibited(self):
        console = ProcessConsole()
        result = console.promote(Q4_1_V1_ID)
        self.assertFalse(result["allowed"])
        self.assertEqual(result["decision"], "prohibited")
        self.assertIn("INCONCLUSIVE", result["reason"])
        html = console.render_html()
        v1 = html.split('id="Q4-1-v1"', 1)[1]
        self.assertIn("disabled", v1.split("</article>", 1)[0])

    def test_verdict_ignores_scientific_outcome(self):
        run = q4_1_v1_historical()
        run.scientific_outcome = "CONFIRMED — dangerous term paid"
        view = ProcessConsole([run]).render_run(run)
        self.assertEqual(view.process_status, ProcessStatus.INCONCLUSIVE)
        self.assertEqual(view.promotion.value, "prohibited")
        self.assertIn("CONFIRMED", view.to_dict()["scientific_outcome"])
        self.assertTrue(
            view.to_dict()["console"]["scientific_outcome_ignored_for_verdict"]
        )


class TestQ41V2Preregistration(unittest.TestCase):
    def test_v2_is_preregistered_direct_ds(self):
        view = ProcessConsole().snapshot().view_for(Q4_1_V2_ID)
        self.assertEqual(view.process_status, ProcessStatus.PREREGISTERED)
        self.assertFalse(view.run.executed)
        self.assertTrue(view.run.preregistered)
        self.assertIn("D_s = Z - ΛY", view.run.diagnostics["D_s_form"])
        self.assertIn("scale-aware", view.run.diagnostics["residual"])
        self.assertTrue(view.run.protocol_hash)
        self.assertTrue(view.run.code_hashes)
        self.assertFalse(view.run.diagnostics["inherits_3915_663"])
        self.assertEqual(view.run.inherited_evidence_ids, [])
        self.assertEqual(
            view.run.decision_window.window_id,
            "Q4-DECISION-WINDOW-2026-09-25",
        )
        self.assertFalse(view.run.decision_window.changed_by_da)
        self.assertEqual(view.promotion.value, "prohibited")

    def test_v2_does_not_inherit_v1_imbalance_as_evidence(self):
        v1 = ProcessConsole().snapshot().view_for(Q4_1_V1_ID)
        v2 = ProcessConsole().snapshot().view_for(Q4_1_V2_ID)
        self.assertIn("withdrawn_imbalance", v1.run.diagnostics)
        self.assertNotIn("withdrawn_imbalance", v2.run.diagnostics)
        self.assertFalse(v2.run.diagnostics["inherits_3915_663"])


class TestConsoleWritesAndSchema(unittest.TestCase):
    def test_schema_version_is_v5(self):
        self.assertEqual(SCHEMA_VERSION, "v5")
        snap = ProcessConsole().snapshot()
        self.assertEqual(snap.schema_version, "v5")

    def test_write_static_roundtrip(self):
        console = ProcessConsole()
        with TemporaryDirectory() as tmp:
            dest = Path(tmp)
            paths = console.write_static(dest)
            html = paths["html"].read_text(encoding="utf-8")
            ledger = json.loads(paths["ledger"].read_text(encoding="utf-8"))
        self.assertIn("Process Console", html)
        self.assertEqual(ledger["schema_version"], "v5")
        ids = {run["run_id"] for run in ledger["runs"]}
        self.assertEqual(ids, {Q4_1_V1_ID, Q4_1_V2_ID})

    def test_from_dict_rejects_foreign_schema(self):
        payload = q4_1_v1_historical().to_dict()
        payload["schema_version"] = "v4"
        with self.assertRaises(SchemaError):
            ProcessRun.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
