"""S_pq equation (1) sits; audit report does not invent 432 or BOTH-SIGNS.

NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import fourier_triangle_s_pq as spq  # noqa: E402


def test_boxed_identities_sit():
    payload = spq.run()
    assert payload["ns_solved"] is False
    assert payload["seats_G1_1"] is True
    assert payload["alpha_98_432_invented"] is False
    assert payload["both_signs_invented"] is False
    assert payload["all_identities_ok"] is True
    rec = spq.check_identity()
    assert rec["identity_1"] is True
    assert rec["identity_4"] is True
    eq = spq.check_equal_length()
    assert eq["identity_3"] is True
    assert eq["in_plane_cancels"] is True


def test_pages_do_not_invent_or_claim_ns():
    packet = (ROOT / "packets" / "FOURIER-TRIANGLES-S-PQ-2026-09-20.md").read_text()
    assert packet.startswith("# Fourier triangles — pair vector")
    assert r"\tag{1}" in packet
    assert "432" in packet and "Not computed" in (ROOT / "docs" / "ns-recovery" / "AUDIT-BOARD-2026-09-24.md").read_text()
    board = (ROOT / "docs" / "ns-recovery" / "AUDIT-BOARD-2026-09-24.md").read_text()
    assert "REPORTED" in board
    assert "not on this tree" in board
    assert "NS is solved" not in packet
    assert "NS is solved" not in board
    data = json.loads((ROOT / "results" / "fourier_triangle_s_pq.json").read_text())
    assert data["all_identities_ok"] is True
    assert data["alpha_98_432_invented"] is False
