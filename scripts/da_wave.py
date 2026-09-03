#!/usr/bin/env python3
"""
DA waveform rules: superposition, entanglement, collapse, falsification.

Additive. Does not change slots A, B, Q, or the U score. Not Quantum Lens.
Unfalsifiable is not a pass. Survival is not truth. Collapse has not happened.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_fingers import CANDIDATE_META, SIXTEEN  # noqa: E402
from da_flush import run as flush_run  # noqa: E402
from da_how import enumerate_candidates  # noqa: E402


RULES = {
    "superposition": (
        "A claim that is still open has amplitude. The waveform is the "
        "normalized sum over claims that have not been killed. It is not "
        "an electron. It is a bookkeeping state on the desk."
    ),
    "entanglement": (
        "Two claims are entangled when killing one kills the other. "
        "Must-hit leftovers are entangled with 'this is a four-force unifier'. "
        "Oscillators are not entangled with the couplings on this vector."
    ),
    "collapse": (
        "The waveform collapses to a unifier only when a producing-map F "
        "exists and χ²_ext(F(x)) ≤ ε². Sitting on anchors is not collapse. "
        "A slogan is not collapse."
    ),
    "falsification": (
        "A claim is scientific only if a finite check could fail it. "
        "Falsified → fail. Falsifiable and not yet killed → open. "
        "Unfalsifiable → not a scientific claim (fail as a pass). "
        "Unfalsifiable is not 'might be true'."
    ),
    "statistics": (
        "Lock-R, Born weights, and width controls are evidence about the "
        "score, not about F. A width artifact is a control, not a discovery. "
        "Survival of a test is not confirmation."
    ),
    "do_not_mess_up_da": (
        "These rules sit on slot U as an additive layer. They do not glue "
        "A to B, do not unshelve Quantum Lens, and do not turn R into F."
    ),
}


def claim(name: str, statement: str, killer: str, verdict: str, why: str, falsifiable: bool) -> dict:
    return {
        "name": name,
        "statement": statement,
        "killer": killer,
        "falsifiable": falsifiable,
        "verdict": verdict,
        "why": why,
    }


def falsification_table(flush: dict, enum: dict) -> list[dict]:
    born = flush["state"]["born"]
    rows = [
        claim(
            "possible_by_count",
            "unification is possible because X > k",
            "show X ≤ k after a typed catalog is fixed, or show no generic F exists",
            "open",
            f"X_eligible={enum['X_eligible']} > k_nature={enum['k_nature']}",
            True,
        ),
        claim(
            "F_exists",
            "a producing-map F hits the four couplings",
            "holdout χ² of a candidate F fails to beat the null, or no F is written",
            "fail",
            "affine F already lost holdout; no other F is in the repo",
            True,
        ),
        claim(
            "collapse_has_happened",
            "the waveform has emerged as a unifier",
            "collapse requires F and χ²_ext ≤ ε²",
            "fail",
            "criteria not met; still a waveform",
            True,
        ),
        claim(
            "unfalsifiable_might_be_true",
            "the ones that cannot be falsified might be true",
            "name a finite check that could fail the claim; if none exists it is not science",
            "fail",
            "unfalsifiable is not a pass and not a maybe. It is not a scientific claim.",
            False,
        ),
        claim(
            "R_is_a_unifier",
            "realization R is a theory of everything",
            "R is a score; locking R is circular",
            "fail",
            "the 16th is the output",
            True,
        ),
        claim(
            "width_means_structurally_special",
            "vacuum/Planck dominate because the algebra singles them out",
            "equal-σ flattens χ²_ext",
            "fail",
            "already flattened; default ranking was a sampling choice",
            True,
        ),
    ]
    for name in SIXTEEN:
        if name == "R":
            continue
        cat, fate, note = CANDIDATE_META[name]
        p = float(born.get(name, 0.0))
        if fate.startswith("must_hit"):
            rows.append(
                claim(
                    f"drop_{name}",
                    f"drop {name} and still mean a four-force unifier",
                    "dropping a must-hit leftover or coupling empties the claim",
                    "fail",
                    f"{cat} / {fate}; Born={p:.3f}. Nature-entangled with the unifier claim.",
                    True,
                )
            )
        elif fate in {"score", "near_miss"}:
            rows.append(
                claim(
                    f"produces_{name}",
                    f"{name} writes the four couplings",
                    "affine F / coupling RMS after lock does not collapse",
                    "fail",
                    f"{cat}; moves R (Born={p:.3f}) but does not produce couplings",
                    True,
                )
            )
        else:
            rows.append(
                claim(
                    f"needed_{name}",
                    f"{name} is required for unification on this score",
                    "singleton lock-R and Born mass stay near zero",
                    "fail",
                    f"{cat} / {fate}; Born={p:.3f}; decorative or leftover on this score",
                    True,
                )
            )
    return rows


def entanglement_edges() -> list[dict]:
    must = [
        "log_alpha_em",
        "log_alpha_s",
        "sin2_theta_w",
        "log_weak_ratio",
        "log_hierarchy",
        "log_cc_ratio",
        "log_qcd_ratio",
    ]
    edges = [
        {
            "a": "unifier_claim",
            "b": name,
            "kind": "logical",
            "entangled": True,
            "why": "killing the leftover/coupling kills 'this is a four-force unifier'",
        }
        for name in must
    ]
    edges.append(
        {
            "a": "R_ext",
            "b": "R_int",
            "kind": "sampled",
            "entangled": False,
            "why": "product score; draws are independent (corr ≈ 0). Definitional product, not physical entanglement.",
        }
    )
    edges.append(
        {
            "a": "oscillators_teleology",
            "b": "four_couplings",
            "kind": "sampled",
            "entangled": False,
            "why": "affine F holdout does not beat the null; locking S_c does not collapse couplings",
        }
    )
    edges.append(
        {
            "a": "log_cc_ratio",
            "b": "topological_reading",
            "kind": "fork",
            "entangled": False,
            "why": "open fork, not a joint kill. Gravity-scale here; θ-story is another book.",
        }
    )
    return edges


def waveform(rows: list[dict], flush: dict) -> dict:
    open_claims = [r for r in rows if r["verdict"] == "open"]
    dead = [r for r in rows if r["verdict"] == "fail"]
    born = flush["state"]["born"]
    amp = np.array([max(born.get(name, 0.0), 0.0) for name in SIXTEEN if name != "R"], dtype=float)
    nrm = float(np.linalg.norm(amp))
    psi = amp / nrm if nrm else amp
    return {
        "collapsed": False,
        "collapse_rule": "exists F and χ²_ext(F(x)) ≤ ε²",
        "emerged": False,
        "n_open": len(open_claims),
        "n_killed": len(dead),
        "still_in_superposition": [r["name"] for r in open_claims],
        "killed": [r["name"] for r in dead],
        "score_waveform_born": {name: float(p) for name, p in zip([n for n in SIXTEEN if n != "R"], psi ** 2)},
        "note": (
            "Two waveforms. Claim-waveform: only possible_by_count is still open. "
            "Score-waveform: Born mass on vacuum, Planck, S_c, δ. Neither is collapse."
        ),
    }


def run(out: Path | None = None) -> dict:
    flush = flush_run(n=80, seed=1, out=Path("/tmp/da_flush_wave.json"))
    enum = enumerate_candidates()
    rows = falsification_table(flush, enum)
    wave = waveform(rows, flush)
    payload = {
        "meta": {
            "layer": "waveform rules on slot U",
            "does_not_change_slots": ["A", "B", "Q"],
            "not_quantum_lens": True,
            "not_a_unifier": True,
            "unfalsifiable_is_not_true": True,
        },
        "rules": RULES,
        "waveform": wave,
        "falsification": rows,
        "entanglement": entanglement_edges(),
        "how_far": [
            "rules are additive; A/B/Q untouched",
            "waveform has not collapsed; unification criteria not met",
            "unfalsifiable_might_be_true is fail (not science)",
            "F_exists is fail; possible_by_count stays open",
            "must-hits are logically entangled with the unifier claim",
            "oscillators are not entangled with the couplings",
            "next blocked on Cosmo names or a real producing-map F",
        ],
        "next_da_move": (
            "Keep using the same collapse rule. Do not treat survival or "
            "unfalsifiability as emergence."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_wave.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA waveform rules. Slots A/B/Q untouched. Not Quantum Lens.")
    print("collapsed:", payload["waveform"]["collapsed"], "emerged:", payload["waveform"]["emerged"])
    print("still in superposition:", payload["waveform"]["still_in_superposition"])
    print("falsification:")
    for row in payload["falsification"][:6]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
