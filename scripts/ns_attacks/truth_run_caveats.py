"""Truth-run on caveats: (P1) skeleton, jet threshold, shape double-charge.

Not a proof of (17). Standard library only.
"""
from fractions import Fraction as F
from math import isqrt, sqrt
from pathlib import Path
import json
from itertools import combinations


def radius(k):
    return sum(t * t for t in k)


def lattice_shell(r2, rmax=None):
    R = isqrt(r2) + 1
    out = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if x * x + y * y + z * z == r2:
                    out.append((x, y, z))
    return out


def scalene_shapes(rmax=40):
    """Distinct unordered triples a<b<c of squared radii that admit p+q+r=0."""
    shells = {r: lattice_shell(r) for r in range(1, rmax + 1)}
    shapes = []
    for a, b, c in combinations(range(1, rmax + 1), 3):
        # triangle inequality on lengths: |√a-√b| ≤ √c ≤ √a+√b etc — necessary
        sa, sb, sc = sqrt(a), sqrt(b), sqrt(c)
        if not (abs(sa - sb) <= sc <= sa + sb):
            continue
        if not (abs(sa - sc) <= sb <= sa + sc):
            continue
        if not (abs(sb - sc) <= sa <= sb + sc):
            continue
        # existence of integer triangle
        found = False
        for p in shells[a]:
            for q in shells[b]:
                r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
                if radius(r) == c:
                    found = True
                    break
            if found:
                break
        if found:
            shapes.append((a, b, c))
    return shapes


# --- (P1) constant consistency from Duhamel skeleton ---
# ∫|T| ≤ |T0|/(38ν) + (1/(38ν)) ∫|Q|
# If ∫|Q| ≤ K E0²/ν, then second term = K/(38) E0²/ν²
# Author face: 0.275533 E0²/ν² ⇒ K = 0.275533 * 38
c_p1 = 0.275533
K_implied = c_p1 * 38

# (P2)-(P3): |T+|+|T×| ≤ α √E0 / n * Y_S4
# Viscous allowance: compare α √E0 / n * Y  vs  ν * (rates?) * something
# Author: both fit below viscous allowance once n ≥ β √E0 / ν
# Check α * β ≈ ?  If allowance is ν Y (or similar), need α √E0 / n ≤ ν ⇒ n ≥ α √E0 / ν
# So β should equal α if allowance is exactly ν Y_S4
alpha = 0.375329
beta = 1.501315
# If threshold is n ≥ α/ν_factor * √E0/ν with ν_factor from rate mixing...
ratio = beta / alpha  # ~4 if comparing to νY/4?

# --- Jet threshold: T_sc(h2) = (15084/1625) t^6 + O(t^7), E=14,X=20,Y=32 ---
c_t6 = F(15084, 1625)
Y0 = 32
# νY/4 at t=0
# [c t^6 - ν Y0/4]_+ > 0 iff t^6 > (ν Y0/4)/c = 8ν / c
# For any ν>0 there is t_*(ν)>0 below which integrand vanishes

def t_star(nu):
    return float((8 * nu / c_t6) ** (F(1, 6)))


# --- Shape census / double-charge ---
shapes = scalene_shapes(30)
# How many shapes touch each shell?
from collections import Counter

touch = Counter()
for a, b, c in shapes:
    touch[a] += 1
    touch[b] += 1
    touch[c] += 1

# Naive sum of per-shape constants: if each shape had the SAME C as (P1)'s 0.275533,
# total charge multiplier = N_shapes * C — and shell 5 appears in touch[5] shapes
shell5_shapes = touch.get(5, 0)
shell_max = touch.most_common(5)

payload = {
    "P1_duhamel_skeleton": {
        "identity": "T'=Q-38νT ⇒ ∫|T|≤|T0|/(38ν)+(1/(38ν))∫|Q|",
        "author_second_coefficient": c_p1,
        "implied_∫|Q|_coefficient_K_if_form_K_E0²/ν": K_implied,
        "first_unjustified_step_without_packet": (
            "Bound ∫|Q_5825| dt by a multiple of E0²/ν using only energy "
            "(and possibly shell structure), including outside inputs — "
            "this is where the analytic packet must be checked"
        ),
        "status": "Duhamel reduction STANDARD; Q-integral bound NOT independently verified here",
    },
    "P2_P3_consistency": {
        "alpha_face": alpha,
        "beta_face": beta,
        "beta_over_alpha": beta / alpha,
        "interpretation": (
            "If |T_sum|≤α√E0/n Y_S4 and viscous allowance were ν Y_S4, "
            "threshold would be n≥α√E0/ν. Observed β/α≈4 suggests allowance "
            "νY/4 (budget viscosity share) or a rate/normalization factor ~4. "
            "Not a proof — consistency probe only."
        ),
        "status": "NUMERICAL consistency probe; proofs not verified",
    },
    "jet_threshold_K2_witness": {
        "E0": 14,
        "X0": 20,
        "Y0": Y0,
        "T_sc_h2_leading": str(c_t6),
        "nuY0_over_4": "8 ν",
        "t_star_nu_1": t_star(1.0),
        "t_star_nu_0_1": t_star(0.1),
        "conclusion": (
            "For every ν>0, T_sc(h2)=O(t^6) starts below νY/4 near t=0. "
            "So (P1) on T_5825 does NOT by itself turn on the budget integrand "
            "[T_sc(h)-νY/4]_+/X. Distinct objects — EXACT qualitative separation."
        ),
        "status": "EXACT qualitative on the named jet (using filed t^6 coefficient)",
    },
    "all_shape_double_charge": {
        "rmax": 30,
        "scalene_shape_count": len(shapes),
        "shapes_touching_shell_5": shell5_shapes,
        "most_shared_shells": shell_max,
        "naive_sum_risk": (
            "If each shape used a (P1)-style bound charging E0 (or shared shell "
            "energies) once per shape, total constant grows with #shapes and "
            "overcounts shells that participate in many triples. "
            "Sample: shell 5 sits in many shapes already at rmax=30."
        ),
        "failed_scheme": (
            "SCHEME A (FAILED as a path to (17)): sum_shapes ∫|T_abc| ≤ "
            "(#shapes)*C E0²/ν². #shapes→∞ as rmax→∞, so no uniform bound."
        ),
        "open_scheme_need": (
            "Need a pot that charges each shell energy at most once "
            "(or a convergent weight), not once per scalene multiset."
        ),
        "status": "EXACT census obstruction to naive summation; (17) still OPEN",
    },
}

Path(__file__).with_name("TRUTH-RUN-CAVEATS.json").write_text(
    json.dumps(payload, indent=2) + "\n"
)
print(json.dumps(payload, indent=2))
