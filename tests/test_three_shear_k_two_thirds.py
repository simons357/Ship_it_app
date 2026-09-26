"""Three-shear K_{1,2}=2/3. Floor, not the 16/9 ceiling.

NS not solved. Not a singular NSE solution.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import three_shear_k_two_thirds as ts  # noqa: E402


def test_hand_floor_is_two_thirds():
    rec = ts.record()
    assert rec["div_free"] and rec["real_valued"]
    assert rec["exact_shell_alpha_1"]
    assert rec["n_modes"] == 6
    assert rec["n_outputs"] == 12
    assert rec["all_outputs_one_sixteenth"]
    assert abs(rec["E"] - 1.5) < 1e-12
    assert abs(rec["PiB_L2_sq"] - 0.75) < 1e-12
    assert rec["K_matches_two_thirds"]
    assert rec["K_is_C0"] is False
    assert rec["ns_solved"] is False
    assert rec["exact_shell_16_over_9"] == "CLAIMED_not_stamped"
