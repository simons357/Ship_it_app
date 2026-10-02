"""Gate lineage: recovered algebra sits; definitions stay missing.

NS not solved. Roadmap not reopened.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import gate5_recovered_algebra as g5  # noqa: E402


def test_d_plus_is_minus_discriminant_and_vertex_identity():
    u, m = Fraction(1), Fraction(2)
    c0, c1, c2 = g5.C0(u, m), g5.C1(u, m), g5.C2(u, m)
    assert g5.D_plus(u, m) == 4 * c0 * c2 - c1 * c1
    assert g5.D_plus(u, m) == -(c1 * c1 - 4 * c0 * c2)
    zs = g5.z_star(u, m)
    assert zs == -c1 / (2 * c2)
    assert g5.P0(u, m, zs) == g5.D_plus(u, m) / (4 * c2)
    payload = g5.run()
    assert payload["ns_solved"] is False
    assert payload["reopened"] is False
    assert payload["chamber_search"] is False
    assert payload["all_vertex_identities"] is True
    assert payload["definitions_of_u_m_d"] == "missing"


def test_page_is_lineage_and_does_not_overwrite_the_board():
    page = (ROOT / "docs" / "ns-recovery" / "GATE-ROADMAP-LINEAGE.md").read_text()
    assert page.startswith("# Gate roadmap — recoverable lineage")
    assert "Does not overwrite the live board" in page
    assert "REOPEN = recompute only" in page
    assert r"D_+(u,m)=4C_0C_2-C_1^2" in page
    assert "MISSING" in page
    assert "NS is solved" not in page
    assert "Clay is solved" not in page
    data = json.loads((ROOT / "results" / "gate5_recovered_algebra.json").read_text())
    assert data["ns_solved"] is False
    assert data["reopened"] is False
    assert data["definitions_of_u_m_d"] == "missing"
    assert data["chamber_search"] is False
