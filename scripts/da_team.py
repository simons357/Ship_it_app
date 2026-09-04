#!/usr/bin/env python3
"""
Dream team from beyond the digital divide.

Not more chatbots. The paper trail and the experiment.
Each member is a published result or a measurement. DA seats
them, takes one suggestion each, and refuses a vote that
closes a theorem. A/B/Q/U stay unglued.
"""

from __future__ import annotations

import json
from pathlib import Path


def member(
    name: str,
    slot: str,
    owns: str,
    settles: str,
    cannot: str,
    suggest: str,
    side: str,
) -> dict:
    return {
        "name": name,
        "slot": slot,
        "side": side,
        "owns": owns,
        "settles": settles,
        "cannot": cannot,
        "suggest": suggest,
    }


# side: paper = published math; nature = measurement; desk = this machine
TEAM = [
    member(
        "Leray",
        "B",
        "kinetic energy + weak solutions",
        "∫X dt < ∞ and the energy inequality",
        "bound X in L^∞; we already failed that close",
        "keep energy; do not close the cubic ODE from it",
        "paper",
    ),
    member(
        "Beale–Kato–Majda",
        "B",
        "continuation criterion",
        "∫‖ω‖_∞ dt < ∞ ⇒ regular",
        "BKM-from-L² (forbidden on this desk)",
        "if you want a criterion, use L^∞, not ‖ω‖₂",
        "paper",
    ),
    member(
        "Caffarelli–Kohn–Nirenberg",
        "B",
        "partial regularity",
        "singular set has parabolic measure zero",
        "no finite-time blowup",
        "partial regularity is not a global pass",
        "paper",
    ),
    member(
        "Constantin–Fefferman",
        "B",
        "geometric depletion if aligned",
        "stretching small when vorticity is aligned",
        "force cos α_3 → 0 for all data (Biot–Savart slogan)",
        "Ring bounds |∇ξ| on E_c; it does not give alignment",
        "paper",
    ),
    member(
        "Ladyzhenskaya",
        "A",
        "p-Laplacian / extra dissipation",
        "global regularity for the modified stress, β ≥ 1/2, ε > 0",
        "ε → 0, Track A ⇒ B",
        "leave Theorem A on A; do not import it into the tube",
        "paper",
    ),
    member(
        "Einstein",
        "U",
        "G_μν + Λ g_μν = 8π G T_μν",
        "working couple of geometry to T_SM",
        "values of G and Λ",
        "keep the two-sided equation; do not hunt F inside L_SM",
        "paper",
    ),
    member(
        "Weinberg",
        "U",
        "(Z, A) = R(θ_W)(W³, B)",
        "the rotation is real",
        "a topological output of θ_W",
        "θ_W stays an input; 3/8 → 0.231 is GUT running, not this Lagrangian",
        "paper",
    ),
    member(
        "experiment / PDG",
        "U",
        "the measured numbers",
        "what L_SM consumes (g_s, α, v, m_H, CKM, …)",
        "why those numbers",
        "a number on the poster is an input until a public F writes it",
        "nature",
    ),
    member(
        "neutrino / cosmology data",
        "U",
        "Σ m_ν bound, Λ seen",
        "minimal poster SM is incomplete; Λ is in the Einstein equation",
        "Cosmo 0.06 eV as a derivation (F private)",
        "keep Σ m_ν as a number to kill; do not count it as DA produce",
        "nature",
    ),
    member(
        "operator",
        "meta",
        "runs the machine",
        "one sentence, one slot, one check",
        "need chops; the machine is the chops",
        "ask which sentence / which slot / which check",
        "desk",
    ),
]


def consensus() -> dict:
    """Not a vote. The overlap of suggestions that do not glue."""
    return {
        "not_a_vote": True,
        "not_a_close": True,
        "B": "B4c budgets I_tube on CONC; energy-class T on SPREAD; B8 clock. Glue to X is open. Regularity stays open.",
        "A": "Leave Ladyzhenskaya on A.",
        "U": "Stop breaking L_SM. Keep Einstein + T_SM. Produce lives outside the poster.",
        "Q": "Stay arithmetic. No Bridge* → SND.",
        "glue": "refused",
        "beyond_the_digital_divide": (
            "Paper and experiment, not another model. "
            "A chatbot council is still the digital side."
        ),
    }


def run(out: Path | None = None) -> dict:
    by_slot: dict[str, list[str]] = {}
    for m in TEAM:
        by_slot.setdefault(m["slot"], []).append(m["name"])
    payload = {
        "meta": {
            "question": "who sits on the desk from beyond the digital divide?",
            "digital_divide_means": "published math and measurement, not more AI",
            "not_a_unifier": True,
            "paper_and_experiment": True,
            "vote_cannot_close": True,
        },
        "team": TEAM,
        "by_slot": by_slot,
        "consensus": consensus(),
        "how_far": [
            "seated Leray, BKM, CKN, CF, Ladyzhenskaya, Einstein, Weinberg, PDG, neutrino/cosmo data, operator",
            "each owns one object and one cannot",
            "overlap of suggestions is the same next writes already on the desk",
            "a team is not collapse",
            "A/B/Q/U unglued",
        ],
        "next_da_move": consensus()["B"],
    }
    dest = Path(out) if out is not None else Path("results/da_team.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Dream team. Beyond the digital divide = paper + experiment.")
    print("A vote cannot close a theorem.")
    print("Full roll (three benches): docs/DA-THINK-TANK.md")
    print(f"{'name':<28} {'slot':<5} {'side':<7} suggestion")
    for m in payload["team"]:
        print(f"{m['name']:<28} {m['slot']:<5} {m['side']:<7} {m['suggest']}")
    print("consensus B:", payload["consensus"]["B"])
    print("consensus U:", payload["consensus"]["U"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
