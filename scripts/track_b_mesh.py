#!/usr/bin/env python3
"""
Finer DNS as an a priori: a finer mesh is not continuation.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B23: decaying n=32 DNS is not a bound. B22e: a finer
box is not a saving climb. This write asks whether
n>32 makes the DNS run an a priori. It does not.
Do not spawn n=64.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb_law import C_SAVE
from track_b_dns import T_LONG, lemma_dns_not_a_priori, lemma_dns_readable, lemma_no_blow_not_bounded
from track_b_finer import lemma_finer_priori_readable
from track_b_lemmas import rec
from track_b_longer import T_ROOM


def lemma_mesh_priori_readable() -> dict:
    dns = lemma_dns_readable()
    not_ap = lemma_dns_not_a_priori()
    noblow = lemma_no_blow_not_bounded()
    finer = lemma_finer_priori_readable()
    ok = (
        dns["verdict"] == "pass"
        and not_ap["verdict"] == "fail"
        and noblow["verdict"] == "fail"
        and finer["verdict"] == "pass"
        and T_LONG > T_ROOM
        and finer["c_inc_max"] < C_SAVE
    )
    return rec(
        "B34_mesh_readable",
        "n=32 DNS miss, refused no-blow, and the finer-box miss are readable together",
        "pass" if ok else "fail",
        "B23 already refused DNS-never-blew-up. B33 already refused a finer climb. Same box. Typed c is not written into the PDE.",
        T_long=T_LONG,
        t_room=T_ROOM,
        c_inc_max=finer["c_inc_max"],
        c_save=C_SAVE,
    )


def lemma_mesh_not_a_priori() -> dict:
    return rec(
        "B34a_mesh_not_a_priori",
        "a finer box (n>32) makes the DNS run a closed a priori bound for classical X",
        "fail",
        "Same knob as B22e. A finer DNS run is not continuation. n is a knob on the box. Do not spawn n=64.",
    )


def lemma_mesh_not_continuation() -> dict:
    return rec(
        "B34b_mesh_not_continuation",
        "cashing n=64 DNS after a decaying n=32 path is continuation for classical X",
        "fail",
        "Continuation is an estimate, not a finer mesh. B23b already refused a longer interval. A finer grid is the same slogan.",
        T_long=T_LONG,
        t_room=T_ROOM,
    )


def lemma_finer_dns_not_ns() -> dict:
    return rec(
        "B34c_finer_dns_not_ns",
        "an unrun finer DNS box is still an NS a priori",
        "fail",
        "The field on this box decayed. A box you did not run is not the packet. Do not sit n=64 as the estimate.",
    )


def lemma_mesh_not_integral_max() -> dict:
    return rec(
        "B34d_mesh_not_integral_max",
        "a finer DNS run is an integral bound on the max vorticity",
        "fail",
        "A mesh is not ∫‖ω‖_∞. DNS-never-blew-up at a finer n is the same refused slogan as B23d.",
    )


def lemma_regularity_leftover() -> dict:
    return rec(
        "B34e_regularity_leftover",
        "a leftover close writes a bound for classical X",
        "fail",
        "Scored as B35. A leftover close is a knob on the check. It does not write X. Regularity stays open. Do not spawn n=64.",
    )


def lemma_mesh_priori_not_a_retune() -> dict:
    return rec(
        "B34f_not_a_pde_retune",
        "scoring finer DNS as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. n is a knob on the box. No Q1. No ε. Do not type c=8 into the equation. Do not spawn n=64.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_mesh_priori_readable(),
        lemma_mesh_not_a_priori(),
        lemma_mesh_not_continuation(),
        lemma_finer_dns_not_ns(),
        lemma_mesh_not_integral_max(),
        lemma_regularity_leftover(),
        lemma_mesh_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "finer DNS as an a priori",
            "tuning_the_pde": False,
            "n": 32,
            "spawned_n64": False,
            "tesla": (
                "exacting, not a jerk. A finer DNS run is not continuation. "
                "Same knob as B22e. Do not spawn n=64."
            ),
            "domain_verdict": "open",
            "c_save": C_SAVE,
            "t_room": T_ROOM,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). "
            "NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). "
            "Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). "
            "Leftover close is not an a priori (B34e). Regularity stays open. Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_mesh.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Finer DNS as an a priori. A finer mesh is not continuation.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
