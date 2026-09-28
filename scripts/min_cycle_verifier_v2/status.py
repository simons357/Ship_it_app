"""Frozen status. The verifier does not arm itself.

Builder stage is closed. This package is the DA independent
reproduction, not a stamp of an unseen builder binary, and not
permission to run MIN-CYCLE on P2.
"""

from __future__ import annotations

# User-frozen builder-stage status. DA does not rewrite this line.
STATUS_FROZEN = "MIN-CYCLE v2: BUILT → SELF-TESTED → DISARMED → AWAITING DA REVIEW"

# DA conclusion after independent reproduction. Still not an arming.
DA_CONCLUSION = (
    "DA-AUDITED (independent reproduction) → STILL DISARMED → "
    "NEXT: γ=(Δ,σ) channel identity"
)

ARMED = False
P2_ARMED = False
FIRST_REAL_MIN_CYCLE_RUN_PERMITTED = False

# Bound on every enumerated result. Spec distinction, not a footnote.
COEFF_MAX_CAVEAT = (
    "coeff_max bounds coordinates in the chosen saturated basis, not ||c||_∞. "
    "A reported minimum from that enumeration is not automatically a global "
    "minimum over integer cycles. Use entry-bounded enumeration if exhaustive "
    "minimum-support certification depends on it."
)

RESEARCH_CHAIN = (
    "DA audit v2 → γ=(Δ,σ) channel identity → canonical M,b,labels → "
    "Jonathan GO → first real MIN-CYCLE run"
)

FORBIDDEN_LIVE_TOKENS = (
    "A live MIN-CYCLE run, a P2 evaluation, and any canonical (M, b, γ) "
    "labels are out of scope for this package."
)


def status_record() -> dict:
    return {
        "status_frozen": STATUS_FROZEN,
        "da_conclusion": DA_CONCLUSION,
        "armed": ARMED,
        "p2_armed": P2_ARMED,
        "first_real_min_cycle_run_permitted": FIRST_REAL_MIN_CYCLE_RUN_PERMITTED,
        "coeff_max_caveat": COEFF_MAX_CAVEAT,
        "research_chain": RESEARCH_CHAIN,
        "scope": FORBIDDEN_LIVE_TOKENS,
    }
