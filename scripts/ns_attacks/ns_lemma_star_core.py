"""Shim. Canonical standalone evaluator: scripts/ns_lemma_star_core.py.

Does not import Stokes. Does not replace stokes_moments.py.
Lemma★ is still open. NS is not solved.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_lemma_star_core import *  # noqa: E402,F401,F403
from ns_lemma_star_core import (  # noqa: E402
    B_hat_at,
    D_s_direct_form,
    D_s_double_sum,
    D_s_moment_form,
    Field,
    K_of_w,
    ModeKey,
    R_star,
    T_c_direct,
    T_c_from_MN,
    T_k_map,
    build_closing_direction,
    dilate,
    from_mode_dict,
    lam,
    moments,
    project_perp,
    random_shell_field,
    shell_wavevectors,
    sum_Tk,
    to_mode_dict,
)
