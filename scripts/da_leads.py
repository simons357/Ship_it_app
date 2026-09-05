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
    lead("Kozono-Taniuchi", "BMO continuation", "B", "living",
         "Integrable BMO of vorticity continues a strong solution. Still an if. Not an a priori on X. BMO of omega is not bmo of xi.",
         "BMO continuation = bound on X"),
    lead("Neustupa-Penel", "one-component if", "B", "living",
         "Regularity of one velocity component regularizes a suitable weak solution. Still an if. One component is not the field.",
         "one component = bound on X"),
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
    lead("Lin", "CKN new proof", "B", "living",
         "A new proof of CKN still uses epsilon-regularity. Velocity L3, pressure L3/2. Small is not empty. Not no blowup.",
         "new proof = no blowup"),
    lead("Vasseur", "De Giorgi CKN", "B", "living",
         "De Giorgi iteration proves the same CKN partial regularity. H1 singular set small. Small is not empty. The 3/2 gap stays.",
         "De Giorgi = no blowup"),
    lead("Wolf", "local pressure / local energy", "B", "living",
         "A local pressure projection lets the same epsilon-regularity run without a global pressure. Still partial regularity. Small is not empty.",
         "local pressure = no blowup"),
    lead("Farwig", "very weak solutions", "B", "living",
         "Very weak solutions sit in Serrin's class without differentiability. They are not Leray-Hopf. Uniqueness in that class is not a bound on X. Sohr stays out.",
         "very weak = bound on X"),
    lead("Cheskidov", "energy equality / Onsager", "B", "living",
         "Energy equality in a weak-in-time Onsager class is still a condition. Leray already has the inequality. Equality is not a bound on X.",
         "energy equality = bound on X"),
    lead("Masmoudi", "critical uniqueness", "B", "living",
         "Uniqueness of mild solutions in C([0,T); L^N) is uniqueness, not regularity. It is not a bound on X.",
         "uniqueness = bound on X"),
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
    lead("Chae", "Triebel-Lizorkin geometric if", "B", "living",
         "Triebel-Lizorkin regularity of xi trades against integrability of |omega|. Still an if. It is not all-data A1.",
         "TL if = all-data alignment"),
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
    lead("Escauriaza", "ESS L3 endpoint", "B", "living",
         "L^infty_t L^3_x is the endpoint. A criterion is not an a priori. Bounded in L3 is not a bound on enstrophy.",
         "L3 endpoint = bound on X"),
    lead("Nadirashvili", "ancient Liouville / KNSS", "B", "living",
         "Bounded ancient mild solutions: 2D and axisymmetric no-swirl. 3D remains a door. A Liouville theorem is not an a priori. Gabriel Koch, not Herbert.",
         "KNSS Liouville = bound on X"),
    lead("Koch", "critical small data", "B", "living",
         "Small critical sits. Large data is the object.",
         "Koch-Tataru ⇒ large data"),
    lead("Chemin-Gallagher", "large Besov / nonlinear smallness", "B", "living",
         "Data may be large in the critical Besov space under a nonlinear smallness condition. Still a condition. Not all-data regularity.",
         "nonlinear smallness = all-data"),
    lead("Cannone-Planchon", "critical Besov mild / small self-similar", "B", "living",
         "Small critical Besov data gives self-similar mild solutions. Small is not all-data. Not Jia large-data existence.",
         "Besov mild = bound on X"),
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
    "Tao", "Sverak", "Seregin", "Escauriaza", "Nadirashvili", "Jia", "Guillod", "Koch", "Chemin-Gallagher", "Cannone-Planchon", "Tataru", "Grujic",
    "Miller", "Vicol", "Buckmaster", "Albritton", "Elgindi", "Hou", "Hou-Wang-Yang", "current math.AP",
    "Beirao-Berselli", "Chae", "Giga-Miura", "Lei-Ren-Tian", "CSTY", "Kozono-Taniuchi", "Neustupa-Penel", "Lin", "Vasseur", "Farwig", "Cheskidov", "Masmoudi", "Wolf",
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
    rec(
        "R24",
        "kozono_taniuchi_closes_X",
        "Kozono-Taniuchi BMO continuation closes X",
        "fail",
        "A continuation if is not an a priori. BMO of omega is not bmo of xi.",
    ),
    rec(
        "R25",
        "neustupa_penel_is_all_data",
        "Neustupa-Penel one-component if is all-data regularity",
        "fail",
        "One velocity component is still an if. One component is not the field.",
    ),
    rec(
        "R26",
        "ess_l3_closes_X",
        "Escauriaza-Seregin-Sverak L3 endpoint closes X",
        "fail",
        "A criterion is not an a priori. Bounded in L3 is not a bound on enstrophy.",
    ),
    rec(
        "R27",
        "knss_liouville_closes_X",
        "KNSS Liouville for bounded ancient solutions closes X",
        "fail",
        "3D remains a door. A Liouville theorem is not an a priori. Gabriel Koch, not Herbert.",
    ),
    rec(
        "R28",
        "chae_if_is_all_data_a1",
        "Chae Triebel-Lizorkin geometric if is all-data A1",
        "fail",
        "Direction plus magnitude is still an if. All-data A1 stays blank.",
    ),
    rec(
        "R29",
        "chemin_gallagher_is_all_data",
        "Chemin-Gallagher large Besov data is all-data regularity",
        "fail",
        "A nonlinear smallness condition is still a condition. Not all-data.",
    ),
    rec(
        "R30",
        "cannone_planchon_is_all_data",
        "Cannone-Planchon critical Besov mild solutions are all-data regularity",
        "fail",
        "Small data in a critical Besov space. Small is not all-data. Not Jia.",
    ),
    rec(
        "R31",
        "lin_ckn_is_no_blowup",
        "Lin's CKN proof is no blowup",
        "fail",
        "A new proof of a partial-regularity theorem is still partial regularity. Small is not empty.",
    ),
    rec(
        "R32",
        "vasseur_ckn_is_no_blowup",
        "Vasseur's CKN proof is no blowup",
        "fail",
        "De Giorgi on the same theorem. Small is not empty. The 3/2 gap is not a close.",
    ),
    rec(
        "R33",
        "farwig_very_weak_bounds_X",
        "Farwig very weak solutions bound X",
        "fail",
        "A different class is not Leray-Hopf and not a bound on classical X. Sohr stays out.",
    ),
    rec(
        "R34",
        "cheskidov_energy_equality_bounds_X",
        "Cheskidov energy equality bounds X",
        "fail",
        "Onsager-class energy equality is a condition. Equality is not regularity.",
    ),
    rec(
        "R35",
        "masmoudi_uniqueness_bounds_X",
        "Masmoudi uniqueness of mild solutions bounds X",
        "fail",
        "Uniqueness in L^N is uniqueness, not an a priori on X.",
    ),
    rec(
        "R36",
        "wolf_local_pressure_is_no_blowup",
        "Wolf local pressure is no blowup",
        "fail",
        "Local pressure is a tool for the same epsilon-regularity. Small is not empty.",
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
