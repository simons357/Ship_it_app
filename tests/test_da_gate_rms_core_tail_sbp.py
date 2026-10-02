"""RMS core/tail SBP gate: elementary facts sit; TG not run; NS not solved."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_rms_core_tail_sbp as gate  # noqa: E402


def test_elementary_phi_and_R_core():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["convention"] == "FROZEN_epoch"
    assert payload["do_not_mix_with_live_Lambda"] is True
    assert payload["sbp_identity_reconstructed_here"] is False
    assert payload["taylor_green_measured"] is False
    assert payload["all_elementary_ok"] is True
    assert abs(gate.phi(0.0, 2.0) - 16.0) < 1e-12
    assert abs(gate.R(2.0, 2.0, 2.0, 4.0) - 16.0) < 1e-12


def test_gate_page_is_identity_only():
    page = (ROOT / "packets" / "DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md").read_text()
    assert page.startswith("# DA gate — RMS core / tail / summation-by-parts")
    assert "stamped as an identity only" in page
    assert "FROZEN" in page
    assert "NS is solved" not in page
    assert "Those data are not on this tree" in page
    data = json.loads((ROOT / "results" / "da_gate_rms_core_tail_sbp.json").read_text())
    assert data["ns_solved"] is False
    assert data["taylor_green_measured"] is False
    assert data["all_elementary_ok"] is True
