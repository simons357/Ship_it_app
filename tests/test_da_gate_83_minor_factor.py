"""Gate 83 specimen-1 minor. Data verdict M ≢ 0. NS not solved."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_83_minor_factor as gate  # noqa: E402
import sympy as sp


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
)


def test_specimen_1_exact_minor_is_nonzero():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["specimen_1_exact_rank"] == 9
    assert payload["pivot"]["rows"] == [0, 1, 2, 3, 4, 6, 7, 8]
    assert payload["pivot"]["drop_var"] == "z0"
    assert payload["pivot"]["exact_det"] == (
        "-1800283866071764628484124381981399482114048"
    )
    assert payload["boxed"] == r"M \not\equiv 0"
    assert payload["factorization_landed"] is False
    assert payload["all_checks_ok"] is True
    # recompute the pivot det from the stored integer matrix
    J = sp.Matrix(payload["J_specimen_1"])
    M = J[payload["pivot"]["rows"], payload["pivot"]["cols"]]
    assert sp.det(M) == sp.Integer(payload["pivot"]["exact_det"])


def test_pages_are_data_and_do_not_claim_ns():
    proof = (ROOT / "docs" / "ns-recovery" / "GATE-83-MINOR-FACTOR.md").read_text()
    card = (ROOT / "packets" / "DA-GATE-83-MINOR-FACTOR-2026-09-27.md").read_text()
    assert proof.startswith("# Gate 83")
    assert r"M\not\equiv 0" in proof
    assert "NS is solved" not in proof
    assert "NS is solved" not in card
    assert "did not land" in proof
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "specimen-1" not in text
        assert "NS is solved" not in text
    out = ROOT / "results" / "da_gate_83_minor_factor.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["boxed"] == r"M \not\equiv 0"
    assert data["ns_solved"] is False
