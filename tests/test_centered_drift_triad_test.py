"""First adversarial triad test: exact finite-triad rejection checkpoint.

Not a closure theorem. NS not solved.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_test as cdt  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def test_near_scale_triad_matches_note():
    rec = cdt.record(cdt.near_scale_triad())
    assert rec["div_free"] and rec["real"]
    assert rec["X"] == 10
    assert rec["Y"] == 14
    assert rec["Z"] == 22
    assert abs(rec["Lambda"] - 7 / 5) < 1e-12
    assert abs(rec["D_s"] - 12 / 5) < 1e-12
    assert rec["tau"][(1, 0, 0)] == 0
    assert rec["tau"][(-1, 0, 0)] == 0
    assert rec["tau"][(0, 1, 0)] == -1
    assert rec["tau"][(0, -1, 0)] == -1
    assert rec["tau"][(1, 1, 0)] == 1
    assert rec["tau"][(-1, -1, 0)] == 1
    assert rec["N"] == 2
    assert rec["M"] == 6
    assert abs(rec["T_c"] - 16 / 5) < 1e-12
    assert abs(rec["T_c_direct"] - 16 / 5) < 1e-12
    assert abs(rec["T_c"] / rec["D_s"] - 4 / 3) < 1e-12
    assert rec["ns_solved"] is False


def test_sign_flips_and_amplitude_kills_pure_absorption():
    field = cdt.near_scale_triad()
    plus = cdt.record(field)
    minus = cdt.record(field.scale(-1))
    assert abs(minus["T_c"] + plus["T_c"]) < 1e-12
    assert abs(minus["D_s"] - plus["D_s"]) < 1e-12
    twice = cdt.record(field.scale(2))
    assert abs(twice["T_c"] / twice["D_s"] - 2 * (4 / 3)) < 1e-12


def test_spectral_gap_identity_and_triad_reconstruction():
    Lambda = 7 / 5
    assert abs(cdt.spectral_gap_factor(1, 2, Lambda) - (cdt.f_lambda(1, Lambda) - cdt.f_lambda(2, Lambda))) < 1e-15
    # Two conjugate pairs: (f(1)-f(2)) τ_q with τ_q=-1 each pair.
    piece = (cdt.f_lambda(1, Lambda) - cdt.f_lambda(2, Lambda)) * (-1)
    assert abs(2 * piece - 16 / 5) < 1e-12


def test_exact_shell_vanishes():
    field = core.Field()
    field.set_mode((1, 0, 0), [0.0, 1.0, 0.0])
    field.set_mode((0, 1, 0), [1.0, 0.0, 0.0])
    rec = cdt.record(field)
    assert abs(rec["Lambda"] - 1) < 1e-12
    assert abs(rec["D_s"]) < 1e-12
    assert abs(rec["T_c"]) < 1e-12


def test_separated_family_tracks_note_asymptotic():
    rows = []
    for L in (4, 8, 16):
        rec = cdt.record(cdt.separated_triad(L))
        rows.append((L, rec["T_c"], rec["D_s"]))
        assert rec["T_c"] > 0
        assert rec["D_s"] > 0
        assert rec["T_c"] / rec["D_s"] < 2.0 / L
    L, Tc, Ds = rows[-1]
    assert abs(Tc / L**3 - 2 * math.sqrt(2)) < 0.01
    assert abs(Ds / L**4 - 2) < 0.02
    assert abs((Tc / Ds) * L - math.sqrt(2)) < 0.03
    # Suppression with separation: not the primary obstruction.
    assert rows[-1][1] / rows[-1][2] < rows[0][1] / rows[0][2]


def test_note_does_not_claim_ns_solved():
    page = Path(__file__).resolve().parents[1] / "docs" / "ns-recovery" / "CENTERED-DRIFT-TRIAD-TEST.md"
    text = page.read_text()
    assert text.startswith("# Centered drift: first adversarial triad test")
    assert "not a closure theorem" in text.lower() or "Not a closure theorem" in text
    assert r"T_c=\frac{16}{5}" in text or r"T_c=\dfrac{16}{5}" in text or "16/5" in text
    assert "NS is solved" not in text
    assert "Clay is solved" not in text
    assert "Do not put" in text or "not independently reviewed" in text.lower()
