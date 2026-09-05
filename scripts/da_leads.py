#!/usr/bin/env python3
"""
Full-roll lead sweep.

Ask every seated kingdom — fluids, program review, nature,
now-bench — for one lead. Kingdoms stay carved. A lead from
U or Q does not write X. A conversation is not a close.
"""

from __future__ import annotations

import json
from pathlib import Path


def rec(
    hid: str,
    name: str,
    statement: str,
    verdict: str,
    why: str,
    **extra,
) -> dict:
    row = {
        "id": hid,
        "name": name,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }
    row.update(extra)
    return row


def lead(
    who: str,
    specialty: str,
    slot: str,
    bench: str,
    line: str,
    cannot: str,
) -> dict:
    return {
        "who": who,
        "specialty": specialty,
        "slot": slot,
        "bench": bench,
        "lead": line,
        "cannot": cannot,
    }


# Every unique chair on the think-tank roll. One lead each.
LEADS = [
    lead("Leray", "weak solutions / energy", "B", "past",
         "Keep ∫X dt < ∞. Do not close the cubic ODE from my integral.",
         "X in L^∞ from energy"),
    lead("Beale", "continuation", "B", "past",
         "If you want a criterion, use ∫‖ω‖_∞. A leftover list is not the max.",
         "BKM from L²"),
    lead("Kato", "mild / continuation", "B", "past",
         "L² is not our theorem. We will sit for an a priori. We will not rename it.",
         "rename BKM into enstrophy"),
    lead("Majda", "continuation / class", "B", "past",
         "A leftover list is not a class. CONC stayed a spectrum.",
         "spectrum ⇒ geometric class"),
    lead("Caffarelli", "partial regularity", "B", "past",
         "The singular set is small. Small is not empty.",
         "no blowup"),
    lead("Kohn", "partial regularity", "B", "past",
         "Parabolic measure zero is not no blowup. A decaying box is not either.",
         "DNS-never-blew-up"),
    lead("Nirenberg", "partial regularity", "B", "past",
         "Keep us on the wall. Do not promote 1934–1982 to a global pass.",
         "energy + CKN = close"),
    lead("Constantin", "geometric depletion", "B", "past",
         "Stretching dies if aligned. CONC is not that if. The 1996 Euler if is a different equation.",
         "all-data alignment; Euler if = NS A1"),
    lead("Fefferman", "geometric depletion", "B", "past",
         "Do not glue Ring to Biot-Savart. Pretty-damn-close is that glue.",
         "the slogan"),
    lead("Beirao-Berselli", "geometric if / weaker than CF", "B", "living",
         "We weakened the Lipschitz if. The if remains an if. It is not all-data A1.",
         "weaker if = all-data alignment"),
    lead("Giga-Miura", "Type I / continuous direction", "B", "living",
         "Type I plus uniformly continuous direction prevents blow-up. Two ifs. It is not all-data A1.",
         "Type I + continuity = all-data alignment"),
    lead("Lei-Ren-Tian", "double-cone geometric if", "B", "living",
         "If vorticity stays in a double cone on high-magnitude sets, the solution is regular. Still an if. It is not all-data A1.",
         "double cone = all-data alignment"),
    lead("CSTY", "axisymmetric Type I", "B", "living",
         "Axisymmetric Type I is out. Symmetry plus a scale-invariant rate. Not an a priori on X.",
         "axisymmetric Type I = bound on X"),
    lead("Ladyzhenskaya", "extra dissipation", "A", "past",
         "Same weight, both sides, as a colleague. Epsilon stays on A.",
         "A ⇒ B"),
    lead("Einstein", "two-sided field equation", "U", "program",
         "Name the object. Keep the classical field. Do not change the PDE to look finished.",
         "values of G, Λ; the tube"),
    lead("Tesla", "apparatus", "U", "program",
         "Sit down on leftover knobs. A lead names a knob you can detune and a script that must move.",
         "SU(3); Einstein's equation; derive NS"),
    lead("Feynman", "missable number", "U", "program",
         "No new lead without a residual you can miss. Survival is not truth.",
         "a council without a number"),
    lead("Weyl", "gauge / compact groups", "U", "program",
         "Do not call the tube a gauge argument. Name G before you say gauge.",
         "SU(3) from a vortex"),
    lead("Wigner", "representations", "U", "program",
         "Type the object. Y_ℓm is not a vorticity direction. One object.",
         "a QNM as enstrophy"),
    lead("von Neumann", "Hilbert space + D", "U", "program",
         "The unknown is X on a divergence-free field. Write an estimate or store a residual. Do not open a slot on modes.",
         "modes as a slot"),
    lead("Weinberg", "electroweak mixing", "U", "past",
         "The W³–B rotation is real. It does not absorb I_tube. I sit this one out.",
         "θ_W from a vortex"),
    lead("experiment / PDG", "measured couplings", "U", "nature",
         "We brought numbers L consumes. They are not inputs to Jean's energy.",
         "why those numbers; fluids"),
    lead("neutrino / cosmology", "Σm_ν and Λ", "U", "nature",
         "Σm_ν is a bound. Λ is seen. Neither writes X.",
         "Cosmo 0.06 eV as F; the tube"),
    lead("Tao", "supercriticality", "B", "living",
         "Energy class is a derivative short. Where now: a residual. Not another leftover close.",
         "catalog closes X; averaged blowup ⇒ NS"),
    lead("Sverak", "Liouville / ancient / self-similar", "B", "living",
         "Honest doors: Liouville, ancient, self-similar. Ruled-out self-similar is not an a priori. Possible is not a theorem.",
         "those doors from a leftover list; exclusion = bound"),
    lead("Jia", "forward self-similar large data", "B", "living",
         "Forward self-similar solutions exist for large minus-one-homogeneous data. Existence is not an a priori on X.",
         "profile existence = bound"),
    lead("Guillod", "numerical non-uniqueness", "B", "living",
         "Numerics show a pitchfork for large scale-invariant data. Smooth profiles. Not an a priori. Not a singularity.",
         "numerics = bound; numerics = blowup"),
    lead("Seregin", "local regularity / ESS", "B", "living",
         "ESS endpoint sits as a criterion. It is not an a priori on X.",
         "criterion ⇒ bound"),
    lead("Koch", "critical small data", "B", "living",
         "Small critical sits. Large data is the object.",
         "Koch-Tataru ⇒ large data"),
    lead("Tataru", "critical small data", "B", "living",
         "The critical space is the wall. That is why leftover knobs died.",
         "scaling wall = estimate"),
    lead("Grujic", "sparseness / log-bmo if", "B", "living",
         "Sparseness can shrink the gap. The 2026 log-bmo if is still an if. Finite order does not make it vanish.",
         "log-bmo if = all-data A1"),
    lead("Miller", "strain / λ2+", "B", "living",
         "Enstrophy is −4∫det S. λ2+ is a different cut from the e3 cap. The identity is not an a priori. A strain model blows.",
         "rewrite in S closes X"),
    lead("Vicol", "wild weak solutions", "B", "living",
         "Non-uniqueness below the energy class is a different class.",
         "convex integration = smooth blowup"),
    lead("Albritton", "forced Leray non-uniqueness", "B", "living",
         "Non-uniqueness of forced Leray–Hopf is a different equation once f is on.",
         "forced ⇒ unforced X bound"),
    lead("Buckmaster", "wild weak solutions", "B", "living",
         "Do not cash us as a killing field for classical X.",
         "wild ⇒ smooth X blows"),
    lead("Elgindi", "Euler singularity", "B", "living",
         "Euler is a different equation. Viscosity is not a free limit.",
         "Euler ⇒ NS"),
    lead("Hou", "computation as probe", "B", "living",
         "A computed scenario is a probe. Do not spawn n=64.",
         "DNS is an a priori"),
    lead("Hou-Wang-Yang", "unforced Leray-Hopf / CAP", "B", "living",
         "Announced CAP of unforced Leray-Hopf non-uniqueness. Different class. Not a bound on classical X. Do not cash a CAP as regularity.",
         "unforced LH ⇒ bound on smooth X"),
    lead("current math.AP", "preprints", "B", "now",
         "An announcement is a proposal. Score one identity here or it stays a paragraph.",
         "close B by title"),
    lead("LVK", "GW strain / catalogs", "U", "now",
         "Four hundred compact binaries do not bound X. We will not update nodes.json.",
         "strain is enstrophy"),
    lead("EHT", "horizon-scale images", "U", "now",
         "A reconstructed ring is a form. It is not ω.",
         "nodes.json; HB"),
    lead("DESI", "BAO / Σm_ν", "U", "now",
         "Λ tension is live on U. It does not write F and it does not write X.",
         "F; the tube"),
    lead("IPTA / NANOGrav", "nHz pulsar timing", "U", "now",
         "A common-spectrum process is not a source name and not a fluids lemma.",
         "source = HB; NS"),
    lead("PDG + LHC", "poster refresh", "U", "now",
         "Refresh the consumed numbers. A PDG update is not a derivation.",
         "why; fluids"),
    lead("LMFDB / analytic NT", "L-functions / gaps", "Q", "now",
         "Keep Q arithmetic. A new gap paper is not ω·Sω.",
         "black holes; fluids"),
    lead("operator", "desk", "meta", "desk",
         "One sentence, one slot, one check. You never know — so you ask, then you refuse glue.",
         "needing chops; a vote"),
]


MUST_SIT = {
    "Leray", "Beale", "Kato", "Majda", "Caffarelli", "Kohn", "Nirenberg",
    "Constantin", "Fefferman", "Ladyzhenskaya",
    "Einstein", "Tesla", "Feynman", "Weyl", "Wigner", "von Neumann", "Weinberg",
    "experiment / PDG", "neutrino / cosmology",
    "Tao", "Sverak", "Seregin", "Jia", "Guillod", "Koch", "Tataru", "Grujic",
    "Miller", "Vicol", "Buckmaster", "Albritton", "Elgindi", "Hou", "Hou-Wang-Yang", "current math.AP",
    "Beirao-Berselli", "Giga-Miura", "Lei-Ren-Tian", "CSTY",
    "LVK", "EHT", "DESI", "IPTA / NANOGrav", "PDG + LHC",
    "LMFDB / analytic NT", "operator",
}


CLAIMS = [
    rec(
        "R1",
        "ask_every_chair",
        "Ask every seated kingdom for one lead",
        "pass",
        "A sweep is a process. You never know — so you ask.",
    ),
    rec(
        "R2",
        "kingdoms_stay",
        "Each lead stays in its slot",
        "pass",
        "Fluids on B. Olga on A. Arithmetic on Q. Program and nature on U.",
    ),
    rec(
        "R3",
        "u_lead_writes_X",
        "A U or Q lead writes a bound for classical X",
        "fail",
        "Wrong chair. Strain is not enstrophy. A gap table is not ω·Sω.",
    ),
    rec(
        "R4",
        "conversation_closes_X",
        "The full-roll conversation closes X",
        "fail",
        "Talk is not an estimate. Domain B stays open.",
    ),
    rec(
        "R5",
        "vote_of_specialties",
        "A vote across specialties writes the estimate",
        "fail",
        "A team is not a vote. More chairs do not collapse the waveform.",
    ),
    rec(
        "R6",
        "glue_across_slots",
        "Glue a U/Q/A lead onto B because you never know",
        "fail",
        "Asking is allowed. Glue is refused.",
    ),
    rec(
        "R7",
        "possible_to_close_X",
        "It is possible to close X",
        "open",
        "Unknown. That is regularity. Not a yes from a sweep.",
    ),
    rec(
        "R8",
        "impossible_to_close_X",
        "It is impossible to close X",
        "fail",
        "Impossibility is not a theorem. A sweep cannot write a no-go.",
    ),
    rec(
        "R9",
        "next_is_residual",
        "The fluids overlap is still a residual on B",
        "pass",
        "Closed estimate, killing field, or one preprint identity. Not leftover B42.",
    ),
    rec(
        "R10",
        "channeling",
        "Asking every chair means they endorse this desk",
        "fail",
        "Papers talk. Endorsement is a channel.",
    ),
    rec(
        "R11",
        "miller_identity_closes",
        "Miller's strain identity closes a bound for classical X",
        "fail",
        "A different cut is not an a priori. A strain model blows.",
    ),
    rec(
        "R12",
        "forced_leray_is_unforced",
        "Forced Leray-Hopf non-uniqueness writes unforced X",
        "fail",
        "Different equation once f is on.",
    ),
    rec(
        "R13",
        "beirao_if_is_all_data_a1",
        "Beirao-Berselli geometric if is all-data A1",
        "fail",
        "Weaker than CF is still an if. All-data A1 stays blank.",
    ),
    rec(
        "R14",
        "grujic_log_bmo_is_all_data_a1",
        "Grujic logarithmic bmo if is all-data A1",
        "fail",
        "arXiv 2607.08866 is an if on the vorticity direction. All-data A1 stays blank.",
    ),
    rec(
        "R15",
        "giga_miura_is_all_data_a1",
        "Giga-Miura Type I plus continuous direction is all-data A1",
        "fail",
        "Two ifs. All-data A1 stays blank.",
    ),
    rec(
        "R16",
        "cfm_euler_is_ns_a1",
        "Constantin-Fefferman-Majda Euler geometric if is classical NS A1",
        "fail",
        "Different equation. The 1996 if does not write NS A1.",
    ),
    rec(
        "R17",
        "self_similar_exclusion_closes_X",
        "Ruling out self-similar L3 and local-energy profiles closes X",
        "fail",
        "Exclusion of a profile class is not an a priori.",
    ),
    rec(
        "R18",
        "liouville_ancient_are_a_priori",
        "Liouville or ancient remaining doors are an a priori on X",
        "fail",
        "A remaining door is not a bound.",
    ),
    rec(
        "R19",
        "jia_forward_ss_closes_X",
        "Jia-Sverak forward self-similar large-data solutions close X",
        "fail",
        "Existence of a scale-invariant profile is not an a priori.",
    ),
    rec(
        "R20",
        "guillod_numerics_close_X",
        "Guillod-Sverak numerical pitchfork closes X",
        "fail",
        "Numerics on smooth profiles. Not an a priori. Not a singularity.",
    ),
    rec(
        "R21",
        "unforced_lh_closes_X",
        "Hou-Wang-Yang unforced Leray-Hopf non-uniqueness closes X",
        "fail",
        "Announced CAP. Different class. Not a bound on classical X.",
    ),
    rec(
        "R22",
        "lei_ren_tian_is_all_data_a1",
        "Lei-Ren-Tian double-cone if is all-data A1",
        "fail",
        "A double cone is still an if. All-data A1 stays blank.",
    ),
    rec(
        "R23",
        "csty_axisym_type_i_closes_X",
        "Chen-Strain-Tsai-Yau axisymmetric Type I exclusion closes X",
        "fail",
        "Axisymmetry plus Type I. Two restrictions. Not an a priori.",
    ),
]


def run(out: Path | None = None) -> dict:
    names = [row["who"] for row in LEADS]
    missing = sorted(MUST_SIT.difference(names))
    slots = sorted({row["slot"] for row in LEADS})
    payload = {
        "meta": {
            "question": "ask every seated kingdom for one lead",
            "writeup": "docs/DA-LEADS.md",
            "not_a_vote": True,
            "not_a_close": True,
            "not_channeling": True,
            "papers_not_persons": True,
            "glue_refused": True,
            "regularity_after": "open",
            "possible_to_close_X": "open",
            "missing_chairs": missing,
            "next_write": (
                "A residual on B. Closed estimate, killing field, "
                "or one preprint identity. Regularity stays open. "
                "Do not spawn n=64. Do not write leftover B42."
            ),
        },
        "leads": LEADS,
        "claims": CLAIMS,
        "counts": {
            "asked": len(LEADS),
            "unique": len(set(names)),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
            "slots": slots,
        },
        "how_far": [
            "every seated kingdom was asked",
            "kingdoms stayed carved",
            "U/Q/A leads refused as a write of X",
            "fluids overlap is still a residual",
            "possible_to_close_X stays open",
            "domain B still open",
        ],
        "next_da_move": (
            "You asked every chair. The fluids lead is a residual. "
            "The other specialties said not here. Possible to close X "
            "stays open. Regularity stays open. Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_leads.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA leads. Every chair asked. Not a vote. Not a close.")
    print("Full roll: docs/DA-LEADS.md")
    print(f"{'who':<24} {'slot':<5} lead")
    for row in payload["leads"]:
        print(f"  {row['who']:<22} {row['slot']:<5} {row['lead']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print("regularity:", payload["meta"]["regularity_after"])
    print("possible_to_close_X:", payload["meta"]["possible_to_close_X"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
