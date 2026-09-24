"""Centered spectral barycenter: identities sit; slope is not a bound.

NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import centered_drift_triad_test as cdt  # noqa: E402
import centered_spectral_barycenter as bary  # noqa: E402


def test_identities_and_note_slope():
    rec = bary.barycenter(cdt.near_scale_triad())
    assert rec["identities_ok"] is True
    assert abs(rec["slope"] - 4 / 3) < 1e-12
    assert abs(rec["X"] * rec["Var_p_lambda"] - rec["D_s"]) < 1e-12
    assert abs(rec["X"] * rec["Cov_p_lambda_t"] - rec["T_c"]) < 1e-12
    assert rec["absorbed_at_theta"] is False
    assert rec["band_Ds_frac"] == 1.0
    amp2 = bary.barycenter(cdt.near_scale_triad().scale(2.0))
    assert abs(amp2["slope"] / rec["slope"] - 2.0) < 1e-12
    assert abs(amp2["Var_p_lambda"] - rec["Var_p_lambda"]) < 1e-12


def test_v_n_is_fat_and_near_shell_collapses():
    payload = bary.run()
    assert payload["ns_solved"] is False
    assert payload["K_formula_proved"] is None
    assert payload["all_identities_ok"] is True
    assert payload["v_n_slope_decreases"] is True
    assert payload["v_n_absorbed_at_theta"] is True
    assert payload["v_n_rel_width_bounded"] is True
    assert payload["near_shell_slope_grows"] is True
    assert payload["near_shell_var_shrinks"] is True
    vn = {row["n"]: row for row in payload["growing_layer"]}
    assert abs(vn[1]["mean_t"]) < 1e-12
    assert abs(vn[8]["mean_t"]) < 1e-12
    assert 0.26 < vn[8]["rel_width"] < 0.28
    assert vn[8]["corr"] < 0.4
    assert payload["near_shell"][-1]["corr"] > 0.99


def test_page_and_json_do_not_claim_a_K_or_ns():
    page = (ROOT / "docs" / "ns-recovery" / "CENTERED-SPECTRAL-BARYCENTER.md").read_text()
    assert page.startswith("# Centered spectral barycenter")
    assert "Not a closure theorem" in page
    assert "No new estimate is claimed" in page
    assert "NS is solved" not in page
    assert "Clay is solved" not in page
    data = json.loads((ROOT / "results" / "centered_spectral_barycenter.json").read_text())
    assert data["ns_solved"] is False
    assert data["K_formula_proved"] is None
    assert data["K_formula"] == "not written"
    assert data["all_identities_ok"] is True
