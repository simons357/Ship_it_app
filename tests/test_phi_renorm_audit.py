"""Guardrails for the 22 Aug 2026 Phi-renorm swirl audit.

Checks the June 30 TeX face after the Hdot relabel:
- no residual energy-norm label \\dot H^{2.6}
- dual / energy sites use \\dot H^{1.3}
- lem:Phieq and op:gronwall remain present (barrier not softened)
"""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEX = ROOT / "docs" / "papers" / "swirl" / "Simons_PhiRenorm_Swirl_2026-06-30.tex"
AUDIT = ROOT / "docs" / "ns-review" / "PHI-RENORM-AUDIT-2026-08-22.md"
KEEP = ROOT / "docs" / "ns-review" / "PHI-RENORM-WHAT-IS-KEPT.md"

# Audit-listed sites (1-based) in the June 30 TeX face (no provenance header).
AUDIT_LINES = (408, 415, 426, 522, 561, 675, 768, 820, 821, 823, 907)
HEADER_OFFSET = 0


class TestPhiRenormAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tex = TEX.read_text(encoding="utf-8")
        cls.lines = cls.tex.splitlines()

    def test_sources_present(self) -> None:
        self.assertTrue(TEX.is_file(), f"missing {TEX}")
        self.assertTrue(AUDIT.is_file(), f"missing {AUDIT}")
        self.assertTrue(KEEP.is_file(), f"missing {KEEP}")

    def test_no_hdot_26_energy_label(self) -> None:
        self.assertNotIn(r"\dot H^{2.6}", self.tex)

    def test_hdot_13_present(self) -> None:
        self.assertGreaterEqual(self.tex.count(r"\dot H^{1.3}"), 11)

    def test_audit_sites_are_hdot_13(self) -> None:
        for n in AUDIT_LINES:
            idx = n + HEADER_OFFSET - 1
            line = self.lines[idx]
            self.assertIn(
                r"\dot H^{1.3}",
                line,
                msg=f"line {n} (file {idx+1}) expected Hdot 1.3, got: {line}",
            )
            self.assertNotIn(r"\dot H^{2.6}", line)

    def test_duality_pairing_line(self) -> None:
        # Original audit line 768 → file line 768+5
        line = self.lines[768 + HEADER_OFFSET - 1]
        self.assertIn(r"\norm{u_\e}_{\dot H^{1.3}}", line)
        self.assertIn(r"\norm{\phi}_{\dot H^{1.3}}", line)

    def test_open_barrier_intact(self) -> None:
        self.assertIn(r"\label{op:gronwall}", self.tex)
        self.assertIn(r"\label{lem:Phieq}", self.tex)
        self.assertIn(r"u_\e^r(t)/r", self.tex)
        # Must not claim Clay / unconditional GR in the open-problem block
        open_sec = self.tex.split(r"\section{Open Problems}", 1)[1]
        self.assertNotIn("Clay Millennium solved", open_sec)
        self.assertIn("Uniform Gronwall bound", open_sec)

    def test_audit_doc_states_barrier_open(self) -> None:
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("Barrier UNCHANGED", audit)
        self.assertIn("NOT** closed", audit)
        self.assertIn("op:gronwall", audit)


if __name__ == "__main__":
    unittest.main()
