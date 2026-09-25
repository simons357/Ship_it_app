#!/usr/bin/env python3
"""Atlas closed shortcuts and Taylor–Green cleanup sweep."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from domain_architect.atlas import TAYLOR_GREEN_SHORTCUT, default_atlas
from domain_architect.errata import (
    LIVE_R_SQUARED,
    LIVE_TC_OVER_NU_DS,
    LIVE_TAYLOR_GREEN,
    WITHDRAWN_TAYLOR_GREEN,
    classify_hit,
    sweep_paths,
    sweep_repository,
)
from domain_architect.process_console import ProcessConsole
from domain_architect.q4_runs import CLOSED_SHORTCUT


class TestAtlasShortcut(unittest.TestCase):
    def test_taylor_green_negative_result_is_prominent(self):
        atlas = default_atlas()
        shortcuts = atlas.prominent_shortcuts()
        self.assertEqual(len(shortcuts), 1)
        shortcut = shortcuts[0]
        self.assertEqual(shortcut.statement, CLOSED_SHORTCUT)
        self.assertIn(r"\not\Rightarrow", shortcut.boxed)
        self.assertIn("Broad spectral state", shortcut.statement)
        self.assertIn("pointwise viscous payment", shortcut.statement)
        self.assertFalse(atlas.ns_solved)
        self.assertEqual(shortcut.shortcut_id, TAYLOR_GREEN_SHORTCUT.shortcut_id)

    def test_console_html_boxes_the_shortcut(self):
        html = ProcessConsole().render_html()
        self.assertIn("Atlas", html)
        self.assertIn("Closed shortcut", html)
        self.assertIn("Broad spectral state", html)
        self.assertIn("pointwise viscous payment", html)
        self.assertIn(r"\not\Rightarrow", html)


class TestTaylorGreenCleanup(unittest.TestCase):
    def test_live_values(self):
        self.assertEqual(LIVE_R_SQUARED, 2.2291)
        self.assertEqual(LIVE_TC_OVER_NU_DS, 1.2259)
        self.assertEqual(LIVE_TAYLOR_GREEN["status"], "live")
        self.assertEqual(WITHDRAWN_TAYLOR_GREEN["status"], "WITHDRAWN")
        self.assertTrue(WITHDRAWN_TAYLOR_GREEN["do_not_cite_as_evidence"])
        html = ProcessConsole().render_html()
        self.assertIn("2.2291", html)
        self.assertIn("1.2259", html)
        self.assertIn("WITHDRAWN", html)
        self.assertIn("3915/663", html)

    def test_withdrawn_on_same_record_is_provenance(self):
        self.assertEqual(
            classify_hit("old fraction 3915/663 WITHDRAWN"),
            "historical_withdrawn",
        )
        self.assertEqual(
            classify_hit("the ratio 3915/663 is the answer"),
            "live_unmarked_withdrawn",
        )

    def test_repo_sweep_has_no_live_unmarked_fraction(self):
        root = Path(__file__).resolve().parent.parent
        report = sweep_repository(root)
        violations = [
            h for h in report.hits if h.classification == "live_unmarked_withdrawn"
        ]
        self.assertEqual(
            violations,
            [],
            msg=f"unmarked withdrawn TG fraction still live: {violations}",
        )

    def test_sweep_flags_unmarked_temp_file(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer_note.md"
            path.write_text(
                "Taylor–Green fraction 3915/663 remains the desk value.\n",
                encoding="utf-8",
            )
            report = sweep_paths([path], root=Path(tmp))
        self.assertEqual(report.hits[0].classification, "live_unmarked_withdrawn")


if __name__ == "__main__":
    unittest.main()
