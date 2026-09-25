"""Young occupation keeps nu. Envelope and occupation stay unproved.

Locked gates are not altered. Missing source files stay absent. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_young_occupation_nu as gate  # noqa: E402


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md",
    "packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md",
    "packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md",
)


def test_young_keeps_nu_and_does_not_prove_occupation():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["envelope_proved"] is False
    assert payload["occupation_proved"] is False
    assert payload["nu_dropped"] is False
    assert payload["covers_samples"] is True
    assert payload["all_identities_ok"] is True
    assert "/ nu" in payload["occupation_condition"]
    assert "2 nu" in payload["remainder_over_Y"]
    assert payload["equality"]["equality_ok"] is True
    assert payload["a8r_scaling"]["identity_ok"] is True
    assert abs(payload["a8r_critical_ratio"]["T_c_over_nu_D_s"] - 2.0) < 1e-12
    assert payload["a8r_construction_on_this_tree"] is False
    assert payload["a8r_leading_coefficient_proved"] is False
    assert payload["i3_weighted_proved_internally"] is False
    assert payload["kkl_regrouping_proved_internally"] is False
    assert payload["fiber_verdict_separated"] == "NEUTRAL"
    assert payload["comparable_KKK"] == "OPEN"
    assert payload["q4_0_executed"] is False
    assert payload["missing_sources"]["all_named_sources_absent"] is True
    assert payload["gate_altered"] == {
        "sbp": False,
        "phi_vs_d": False,
        "low_tail_snapshot": False,
        "sign_realizability": False,
        "s_pq": False,
    }


def test_page_keeps_nu_and_does_not_claim_ns():
    page = (ROOT / "packets" / "DA-GATE-YOUNG-OCCUPATION-NU-2026-09-25.md").read_text()
    assert page.startswith("# DA gate — Young occupation keeps")
    assert r"\frac{\alpha^2\chi^2\kappa X}{\nu}" in page
    assert r"\tfrac12\nu D_s" in page
    assert "not prove" in page.lower() or "does **not** prove" in page
    assert "NS is solved" not in page
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "Young occupation keeps" not in text
        assert "NS is solved" not in text
    out = ROOT / "results" / "da_gate_young_occupation_nu.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["nu_dropped"] is False
    assert data["all_identities_ok"] is True
