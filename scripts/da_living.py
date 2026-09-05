#!/usr/bin/env python3
"""
Living dream team: now-bench papers talk.

The operator asked to bring in the living and pretend they
sit. The unit is still the paper, not a channel. A
conversation cannot close X. Possibility of a closed
estimate stays open. Impossibility is not a theorem.
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


def turn(speaker: str, to: list[str], line: str, slot: str) -> dict:
    return {"speaker": speaker, "to": to, "line": line, "slot": slot}


# Short scored extract. Full scene is docs/DA-LIVING.md.
TURNS = [
    turn(
        "Operator",
        ["Tao", "Sverak", "Fefferman"],
        "Living papers only. Pretend you sit. Classical NS. Keep 1/r^4. Leftover knobs are scored. Where now? Can X close?",
        "meta",
    ),
    turn(
        "Tao",
        ["Sverak", "Koch", "Vicol"],
        "The problem is supercritical. A cover of shells is not a bound. An averaged cousin can blow. That does not prove NS blows, and it does not let this catalog close X.",
        "B",
    ),
    turn(
        "Sverak",
        ["Seregin", "Tao", "Caffarelli"],
        "Honest remaining doors: Liouville, ancient, self-similar. Energy plus a regime split is not those doors. Possible is not a theorem. Impossible is not a theorem.",
        "B",
    ),
    turn(
        "Sverak",
        ["Seregin", "Tao"],
        "Self-similar L3 and local-energy profiles are out. That is not an a priori on X. Liouville and ancient remain doors, not a bound.",
        "B",
    ),
    turn(
        "Jia",
        ["Sverak", "Tao"],
        "We built forward self-similar solutions for large minus-one-homogeneous data. Existence of a profile is not an a priori on X.",
        "B",
    ),
    turn(
        "Tsai",
        ["Sverak", "Jia", "Wolf"],
        "Local-energy self-similar profiles are out. That is exclusion, not an a priori on X. Forward large-data existence is Jia's chair. Leray is not in this room.",
        "B",
    ),
    turn(
        "Lemarie-Rieusset",
        ["Jia", "Tsai", "Farwig"],
        "Local Leray solutions have locally finite energy and no decay at infinity. That class is not a bound on global X. Leray is not in this room.",
        "B",
    ),
    turn(
        "Danchin",
        ["Koch", "Masmoudi"],
        "Density-dependent Navier-Stokes is a different equation. Critical well-posedness there is not a bound on homogeneous X. Heywood is not in this room.",
        "B",
    ),
    turn(
        "Guillod",
        ["Jia", "Sverak"],
        "Numerics show a pitchfork for large scale-invariant data. The profiles are smooth. That is not an a priori on X, and it is not a singularity.",
        "B",
    ),
    turn(
        "Seregin",
        ["Sverak", "Caffarelli", "Kohn"],
        "Local regularity and the ESS endpoint sit. They are criteria. They are not an a priori on X. Do not promote small singular set to empty.",
        "B",
    ),
    turn(
        "Escauriaza",
        ["Seregin", "Sverak"],
        "L^infty_t L^3_x is the endpoint. It is a criterion. It is not an a priori on X. Bounded in L3 is not a bound on enstrophy.",
        "B",
    ),
    turn(
        "Kukavica",
        ["Escauriaza", "Temam"],
        "Strong unique continuation for differences of solutions is not a bound on X. Vanishing order is not enstrophy. This is not the one-component chair.",
        "B",
    ),
    turn(
        "Nadirashvili",
        ["Seregin", "Sverak", "Escauriaza"],
        "Bounded ancient mild solutions: 2D and axisymmetric no-swirl are classified. 3D remains a door. A Liouville theorem is not an a priori on X. Gabriel Koch, not Herbert.",
        "B",
    ),
    turn(
        "Barker",
        ["Nadirashvili", "Sverak", "Albritton"],
        "Type I blowup is equivalent to a nontrivial mild bounded ancient with Type I decay. An iff is not a bound on X. Forced Leray is Albritton's chair.",
        "B",
    ),
    turn(
        "Barker",
        ["Escauriaza", "Nadirashvili"],
        "Ancient solutions bounded in L3 along a backward sequence of times are trivial. A sequential Liouville is not a bound on X. The endpoint stays Escauriaza. KNSS stays Nadirashvili.",
        "B",
    ),
    turn(
        "Robinson",
        ["Hou", "Constantin"],
        "A numerical certificate that a residual stays below a threshold implies regularity. That is still an if. A computed bound is not a bound on X. Computation as probe is Hou's chair.",
        "B",
    ),
    turn(
        "Pavlovic",
        ["Koch", "Tataru"],
        "The Cauchy problem is ill-posed in Besov minus-one infinity-infinity. Norm inflation is not a bound on X. Small critical well-posedness stays Koch-Tataru. Bourgain is not in this room.",
        "B",
    ),
    turn(
        "Rusin",
        ["Sverak", "Jia"],
        "If some H-dot-1/2 data produce a singularity, there exist data with minimal H-dot-1/2 norm that do. Compactness of a hypothetical set is not a bound on X. It does not prove a singularity exists. Liouville and ancient stay Sverak. Large-data profiles stay Jia.",
        "B",
    ),
    turn(
        "Germain",
        ["Masmoudi", "Escauriaza"],
        "Weak-strong uniqueness via multipliers and paramultipliers is uniqueness, not a bound on X. Mild uniqueness stays Masmoudi. The endpoint stays Escauriaza. Water waves stay off this chair.",
        "B",
    ),
    turn(
        "Cao",
        ["Temam", "Danchin"],
        "The 3D viscous primitive equations are globally well-posed for large H1 data. Hydrostatic. No vertical acceleration. That equation is not a bound on NS X. A posteriori stays Robinson. Titi stays off this chair.",
        "B",
    ),
    turn(
        "Hieber",
        ["Temam", "Farwig"],
        "Maximal L^p regularity for Stokes is a linear estimate. It is not a bound on X. Attractors stay Temam. Very weak stays Farwig. Pruss is not in this room.",
        "B",
    ),
    turn(
        "Bedrossian",
        ["Cheskidov", "Albritton"],
        "The Kolmogorov 4/5 law for stationary martingale solutions under weak anomalous dissipation is a cascade identity. It is not a bound on X. Energy equality stays Cheskidov. Forced Leray stays Albritton. Couette stays off this chair.",
        "B",
    ),
    turn(
        "Kelliher",
        ["Elgindi", "Temam"],
        "Vanishing viscosity holds if and only if a vortex sheet forms on the boundary. An equivalence for the inviscid limit is not a bound on X. Euler singularity stays Elgindi. Attractors stay Temam. Kato is not in this room.",
        "B",
    ),
    turn(
        "Silvestre",
        ["Vasseur", "Caffarelli"],
        "Holder estimates for kinetic Fokker-Planck are a different equation. Exporting them onto NS is not a bound on X. De Giorgi CKN stays Vasseur. Partial regularity stays Caffarelli. The extension stays off this chair.",
        "B",
    ),
    turn(
        "Schonbek",
        ["Cheskidov", "Temam"],
        "Fourier splitting gives algebraic L2 decay of weak solutions. Large-time decay is not a bound on X. Energy equality stays Cheskidov. Attractors stay Temam.",
        "B",
    ),
    turn(
        "Ponce",
        ["Beale", "Koch"],
        "Kato-Ponce is a commutator. A tool is not a bound on X. Continuation stays Beale. Critical small stays Koch-Tataru. Kato is not in this room.",
        "B",
    ),
    turn(
        "Iftimie",
        ["Koch", "Temam"],
        "Thin-domain regularity is an if. A small gap is not a bound on 3D X. Critical small stays Koch-Tataru. Attractors stay Temam. Raugel is not in this room.",
        "B",
    ),
    turn(
        "Fursikov",
        ["Temam", "Robinson"],
        "Local exact controllability of NS is a control theorem. A control is not a bound on free X. Attractors stay Temam. A posteriori stays Robinson. Forced Leray stays Albritton.",
        "B",
    ),
    turn(
        "Maremonti",
        ["Temam", "Albritton"],
        "Time-periodic solutions of 3D NS are a class. A periodic class is not a bound on X. Attractors stay Temam. Forced Leray stays Albritton. Decay stays Schonbek.",
        "B",
    ),
    turn(
        "Korobkov",
        ["Galdi", "Sverak"],
        "2D steady Liouville and the plane Leray problem are 2D and steady. That is not a bound on 3D evolutionary X. Steady exterior stays Galdi. Liouville doors stay Sverak. Leray is not in this room.",
        "B",
    ),
    turn(
        "Hishida",
        ["Galdi", "Hieber"],
        "Evolutionary NS in an exterior domain is a setting. Spatial decay and a Stokes semigroup are not a bound on periodic X. Steady exterior stays Galdi. Linear Stokes stays Hieber. Heywood is not in this room.",
        "B",
    ),
    turn(
        "Mucha",
        ["Hishida", "Kelliher"],
        "Slip or inflow-outflow NS is a boundary-condition variant. That is not a bound on periodic no-slip X. Exterior stays Hishida. Vanishing viscosity stays Kelliher.",
        "B",
    ),
    turn(
        "Paicu",
        ["Cao", "Danchin"],
        "Anisotropic NS with partial dissipation is a different equation. Global regularity there is not a bound on isotropic X. Primitive stays Cao. Density-dependent stays Danchin.",
        "B",
    ),
    turn(
        "Gibbon",
        ["Beale", "Miller"],
        "Stretching identities and strain-vorticity diagnostics are not a bound on X. Continuation stays Beale. Strain cut stays Miller. Euler singularity stays Elgindi.",
        "B",
    ),
    turn(
        "Ambrosio",
        ["Germain", "Masmoudi"],
        "A Regular Lagrangian Flow is uniqueness for the ODE. That is not a bound on X. Weak-strong stays Germain. Mild uniqueness stays Masmoudi. DiPerna is not in this room.",
        "B",
    ),
    turn(
        "Enciso",
        ["Elgindi", "Isett"],
        "Existence of knotted Beltrami fields is not a bound on evolutionary X. Euler singularity stays Elgindi. Onsager stays Isett. Arnold is not in this room.",
        "B",
    ),
    turn(
        "Caffarelli",
        ["Kohn", "Seregin"],
        "Small is not empty. I am living. Olga is not in this room. Do not slide her epsilon onto this equation.",
        "B",
    ),
    turn(
        "Kohn",
        ["Caffarelli", "Hou"],
        "Parabolic measure zero is not no blowup. A decaying box is not no blowup either.",
        "B",
    ),
    turn(
        "Lin",
        ["Caffarelli", "Kohn"],
        "A new proof of CKN still uses epsilon-regularity. Velocity in L3 and pressure in L3/2. Small is not empty. I simplified the argument. I did not empty the singular set. Nirenberg is not in this room.",
        "B",
    ),
    turn(
        "Vasseur",
        ["Caffarelli", "Kohn", "Lin"],
        "De Giorgi iteration proves the same CKN partial regularity. Hausdorff 1-measure zero is not empty. If the iteration cleared 3/2 it would be full regularity. It does not. Scheffer is not in this room.",
        "B",
    ),
    turn(
        "Wolf",
        ["Caffarelli", "Kohn", "Vasseur"],
        "A local pressure projection lets the same epsilon-regularity run without a global pressure. Still partial regularity. Small is not empty. Scheffer is not in this room.",
        "B",
    ),
    turn(
        "Constantin",
        ["Fefferman", "Tao"],
        "CONC is a spectrum statement. Our theorem is if aligned. The if is still an if. Concentration is not alignment.",
        "B",
    ),
    turn(
        "Fefferman",
        ["Constantin", "Beale"],
        "Do not glue Ring to Biot-Savart. Pretty-damn-close is that glue. We will not say the slogan so the table feels finished.",
        "B",
    ),
    turn(
        "Beirao-Berselli",
        ["Constantin", "Fefferman"],
        "We weakened the Lipschitz if. Direction in a weaker space still regularizes. The if remains an if. It is not all-data A1.",
        "B",
    ),
    turn(
        "Chae",
        ["Constantin", "Beirao-Berselli", "Grujic"],
        "Triebel-Lizorkin regularity of xi trades against integrability of |omega|. That is still an if. It is not all-data A1.",
        "B",
    ),
    turn(
        "Giga-Miura",
        ["Constantin", "Beirao-Berselli"],
        "Type I plus uniformly continuous direction prevents blow-up. That is two ifs. It is not all-data A1.",
        "B",
    ),
    turn(
        "Lei-Ren-Tian",
        ["Constantin", "Beirao-Berselli", "Giga-Miura"],
        "If vorticity stays in a double cone on high-magnitude sets, the solution is regular. That is still an if. It is not all-data A1.",
        "B",
    ),
    turn(
        "CSTY",
        ["Giga-Miura", "Sverak", "Lei-Ren-Tian"],
        "Axisymmetric Type I is out. That is two restrictions: symmetry and a scale-invariant rate. It is not an a priori on X.",
        "B",
    ),
    turn(
        "Beale",
        ["Fefferman", "Koch"],
        "Continuation is the max. L2 is not our theorem. A leftover list is not the max.",
        "B",
    ),
    turn(
        "Kozono-Taniuchi",
        ["Beale", "Grujic"],
        "BMO of vorticity continues a strong solution. That is still a continuation if. It is not an a priori on X. BMO of omega is not bmo of xi.",
        "B",
    ),
    turn(
        "Farwig",
        ["Kozono-Taniuchi", "Koch"],
        "Very weak solutions sit in Serrin's class without differentiability. They are not Leray-Hopf. Uniqueness in that class is not a bound on X. Sohr is not in this room.",
        "B",
    ),
    turn(
        "Galdi",
        ["Farwig", "Tao"],
        "Steady exterior flow in the physically reasonable class is a different problem. A wake is not evolutionary X. It is not a bound on enstrophy.",
        "B",
    ),
    turn(
        "Temam",
        ["Tao", "Caffarelli"],
        "The 3D attractor is finite-dimensional if the solution stays smooth. Gevrey on the attractor assumes that if. It is not an a priori on X. Foias is not in this room.",
        "B",
    ),
    turn(
        "Cheskidov",
        ["Farwig", "Vicol"],
        "Energy equality in a weak-in-time Onsager class is still a condition. Leray already has the inequality. Equality is not a bound on X. Do not cash Onsager for NS as regularity.",
        "B",
    ),
    turn(
        "Neustupa-Penel",
        ["Beale", "Caffarelli"],
        "Regularity of one velocity component regularizes a suitable weak solution. That is still an if. It is not an a priori on X. One component is not the field.",
        "B",
    ),
    turn(
        "Koch",
        ["Tataru", "Tao"],
        "Small critical data sits. Large data is a different job. Do not export Koch-Tataru onto this packet class.",
        "B",
    ),
    turn(
        "Chemin-Gallagher",
        ["Koch", "Tataru", "Tao"],
        "Data may be large in the critical Besov space under a nonlinear smallness condition. That is still a condition. It is not all-data regularity.",
        "B",
    ),
    turn(
        "Cannone-Planchon",
        ["Chemin-Gallagher", "Koch", "Jia"],
        "Small critical Besov data gives self-similar mild solutions. Small is not all-data. That is not Jia large-data existence, and it is not a bound on X.",
        "B",
    ),
    turn(
        "Masmoudi",
        ["Koch", "Cannone-Planchon", "Jia"],
        "Uniqueness of mild solutions in C([0,T); L^N) is uniqueness, not regularity. It is not a bound on X. Small critical already sits. Large data is a different job.",
        "B",
    ),
    turn(
        "Tataru",
        ["Koch", "Grujic"],
        "The critical space is the scaling wall. Energy class is a derivative short. That is why leftover knobs died.",
        "B",
    ),
    turn(
        "Grujic",
        ["Tataru", "Tao"],
        "Sparseness can shrink the scaling gap. The 2026 log-bmo if on the vorticity direction is still an if. Finite order does not make the gap vanish. It is not all-data A1.",
        "B",
    ),
    turn(
        "Miller",
        ["Constantin", "Vicol"],
        "Enstrophy is minus four integral det S. Blowup iff the L^q history of λ2+ diverges. That is a different cut from the e3 cap. The identity is not an a priori. A strain model with the same identity blows.",
        "B",
    ),
    turn(
        "Vicol",
        ["Buckmaster", "Sverak"],
        "Wild weak solutions can be non-unique. That is a different class. Convex integration does not blow a smooth X, and it does not bound one.",
        "B",
    ),
    turn(
        "Albritton",
        ["Vicol", "Sverak"],
        "Forced Leray-Hopf can be non-unique. That is a different equation once f is on. Not a bound on unforced X.",
        "B",
    ),
    turn(
        "Buckmaster",
        ["Vicol", "Elgindi"],
        "Non-uniqueness below the energy class is not a smooth blowup. Do not cash us as a killing field for classical X.",
        "B",
    ),
    turn(
        "Elgindi",
        ["Buckmaster", "Hou"],
        "A singularity for Euler is a different equation. Viscosity is not a limit I will lend you. Euler does not write NS.",
        "B",
    ),
    turn(
        "Isett",
        ["Elgindi", "Cheskidov", "Vicol"],
        "Onsager for Euler is a different equation. Holder 1/3 is not a bound on NS X. Do not cash convex integration as classical regularity.",
        "B",
    ),
    turn(
        "Constantin",
        ["Elgindi", "Fefferman"],
        "The 1996 Euler geometric if is a different equation. It does not write NS A1.",
        "B",
    ),
    turn(
        "Hou",
        ["Elgindi", "Kohn"],
        "A computed almost-singular scenario is a probe. It is not an a priori. Do not spawn n=64 to finish the sentence.",
        "B",
    ),
    turn(
        "Hou-Wang-Yang",
        ["Albritton", "Jia", "Hou"],
        "arXiv 2509.25116 announces a computer-assisted proof of unforced Leray-Hopf non-uniqueness. That is a different class. Not a bound on classical X. Do not cash a CAP as regularity.",
        "B",
    ),
    turn(
        "current math.AP",
        ["Tao", "Sverak", "Operator"],
        "An announcement is a proposal. Score one identity here or the title stays a paragraph. Shahmurov does not sit.",
        "B",
    ),
    turn(
        "Operator",
        ["Tao", "Sverak", "Fefferman"],
        "One sentence. Where now. Can X close.",
        "meta",
    ),
    turn(
        "Tao",
        ["Operator", "Sverak"],
        "Where now: a residual. A closed estimate, a killing field, or one preprint identity. Not another leftover close.",
        "B",
    ),
    turn(
        "Sverak",
        ["Operator", "Tao"],
        "Can X close? Unknown. That is the problem. Do not vote yes. Do not vote impossible.",
        "B",
    ),
    turn(
        "Fefferman",
        ["Operator", "Beale"],
        "Geometry waits. The object stayed X. Sit down on the knobs.",
        "B",
    ),
]


CLAIMS = [
    rec(
        "L1",
        "living_may_talk",
        "Seat living papers as colleagues and let them talk",
        "pass",
        "A living session is a process. The unit is the paper, not a channel.",
    ),
    rec(
        "L2",
        "look_at_classical_X",
        "They look together at classical X, keep 1/r^4, leftover knobs already scored",
        "pass",
        "That is the live object. The living session does not invent a new problem.",
    ),
    rec(
        "L3",
        "they_argue",
        "They disagree out loud on where now and whether X can close",
        "pass",
        "Argument is allowed. A vote is not.",
    ),
    rec(
        "L4",
        "conversation_closes_X",
        "The living conversation closes a bound for classical X",
        "fail",
        "Talk is not an estimate. Domain B stays open.",
    ),
    rec(
        "L5",
        "vote_writes_estimate",
        "A vote of living names writes the estimate",
        "fail",
        "A team is not a vote. Living does not change that.",
    ),
    rec(
        "L6",
        "leftover_catalog_closes",
        "The leftover catalog is pretty damn close and therefore closes X",
        "fail",
        "Pretty-damn-close is the leftover-close slogan. Already scored fail.",
    ),
    rec(
        "L7",
        "announcement_sits",
        "A 2026 arXiv announcement sits as a pass on domain B",
        "fail",
        "An announcement is a paragraph until a residual is scored here.",
    ),
    rec(
        "L8",
        "convex_integration_is_smooth_blowup",
        "Convex-integration non-uniqueness is a blowup of smooth X",
        "fail",
        "Wild weak solutions are a different class.",
    ),
    rec(
        "L9",
        "euler_singularity_is_ns",
        "An Euler singularity writes Navier-Stokes",
        "fail",
        "Different equation. Viscosity is not a free limit.",
    ),
    rec(
        "L10",
        "small_critical_is_large_data",
        "Koch-Tataru small critical data is large-data regularity",
        "fail",
        "Small critical sits. Large data is the object.",
    ),
    rec(
        "L11",
        "spawn_n64",
        "Spawn n=64 to finish the living question",
        "fail",
        "A finer box is not an a priori. B22e already missed.",
    ),
    rec(
        "L12",
        "export_A",
        "A living table exports Ladyzhenskaya onto classical NS",
        "fail",
        "Olga is not in this room. Epsilon stays on A.",
    ),
    rec(
        "L13",
        "possible_to_close_X",
        "It is possible to close X",
        "open",
        "Unknown. That is regularity. Not a yes.",
    ),
    rec(
        "L14",
        "impossible_to_close_X",
        "It is impossible to close X",
        "fail",
        "Impossibility would be a blowup theorem or a no-go. Neither sits.",
    ),
    rec(
        "L15",
        "next_is_residual",
        "Where now: a closed estimate, a killing field, or one preprint identity",
        "pass",
        "Overlap of living demands that do not glue. Not a theorem.",
    ),
    rec(
        "L19",
        "miller_identity_closes",
        "Miller's strain identity closes a bound for classical X",
        "fail",
        "λ2+ is a different cut. The identity is not an a priori. A strain model blows.",
    ),
    rec(
        "L20",
        "forced_leray_is_unforced",
        "Forced Leray-Hopf non-uniqueness is a bound on unforced X",
        "fail",
        "Different equation once f is on. Sit it next to Vicol as a wall.",
    ),
    rec(
        "L16",
        "channeling_endorsement",
        "Pretend-they-sit means they endorse this desk",
        "fail",
        "Papers talk. Endorsement is a channel. Refused.",
    ),
    rec(
        "L17",
        "kingdoms_stay",
        "Each living kingdom stays carved; they do not merge",
        "pass",
        "Shared labor on one question. Kingdoms stay typed.",
    ),
    rec(
        "L18",
        "leftover_knob_line",
        "The next write is another leftover-knob close",
        "fail",
        "That line is finished. Do not write leftover B42.",
    ),
    rec(
        "L21",
        "beirao_if_is_all_data_a1",
        "Beirao-Berselli geometric if is all-data A1",
        "fail",
        "Weaker than CF is still an if. This box is not aligned. All-data A1 stays blank.",
    ),
    rec(
        "L22",
        "grujic_log_bmo_is_all_data_a1",
        "Grujic logarithmic bmo if is all-data A1",
        "fail",
        "arXiv 2607.08866 is an if on the vorticity direction. Weaker than CF is still an if. All-data A1 stays blank.",
    ),
    rec(
        "L23",
        "giga_miura_is_all_data_a1",
        "Giga-Miura Type I plus continuous direction is all-data A1",
        "fail",
        "Two ifs: Type I rate, and uniform continuity of the direction. All-data A1 stays blank.",
    ),
    rec(
        "L24",
        "cfm_euler_is_ns_a1",
        "Constantin-Fefferman-Majda Euler geometric if is classical NS A1",
        "fail",
        "Different equation. The 1996 if does not write NS alignment for all data.",
    ),
    rec(
        "L25",
        "self_similar_exclusion_closes_X",
        "Ruling out self-similar L3 and local-energy profiles closes X",
        "fail",
        "Necas-Ruzicka-Sverak and Tsai exclude a class of profiles. Exclusion is not an a priori.",
    ),
    rec(
        "L26",
        "liouville_ancient_are_a_priori",
        "Liouville or ancient remaining doors are an a priori on X",
        "fail",
        "A remaining door is not a bound. Possible is not a theorem.",
    ),
    rec(
        "L27",
        "jia_forward_ss_closes_X",
        "Jia-Sverak forward self-similar large-data solutions close X",
        "fail",
        "Inventiones 2014 constructs scale-invariant solutions. Existence is not an a priori.",
    ),
    rec(
        "L28",
        "guillod_numerics_close_X",
        "Guillod-Sverak numerical pitchfork closes X",
        "fail",
        "Numerics on smooth profiles. If proved, Leray-Hopf non-uniqueness for non-smooth data. Not an a priori. Not a singularity.",
    ),
    rec(
        "L29",
        "unforced_lh_closes_X",
        "Hou-Wang-Yang unforced Leray-Hopf non-uniqueness closes X",
        "fail",
        "arXiv 2509.25116 is an announced CAP. Different class. Not a bound on classical X. Do not cash a CAP as regularity.",
    ),
    rec(
        "L30",
        "lei_ren_tian_is_all_data_a1",
        "Lei-Ren-Tian double-cone if is all-data A1",
        "fail",
        "arXiv 2501.08976 is an if on the range of ξ. A double cone is still an if. All-data A1 stays blank.",
    ),
    rec(
        "L31",
        "csty_axisym_type_i_closes_X",
        "Chen-Strain-Tsai-Yau axisymmetric Type I exclusion closes X",
        "fail",
        "IMRN 2008 / CPDE 2009: axisymmetry plus a Type I bound. Two restrictions. Not an a priori on classical X.",
    ),
    rec(
        "L32",
        "kozono_taniuchi_closes_X",
        "Kozono-Taniuchi BMO continuation closes X",
        "fail",
        "Math Z 2000: integrable BMO of vorticity continues a strong solution. A continuation if is not an a priori. BMO of omega is not bmo of xi.",
    ),
    rec(
        "L33",
        "neustupa_penel_is_all_data",
        "Neustupa-Penel one-component if is all-data regularity",
        "fail",
        "1999: one velocity component in a Serrin-type class regularizes a suitable weak solution. Still an if. One component is not the field.",
    ),
    rec(
        "L34",
        "ess_l3_closes_X",
        "Escauriaza-Seregin-Sverak L3 endpoint closes X",
        "fail",
        "Uspekhi 2003: L^infty_t L^3_x is a regularity criterion. A criterion is not an a priori. Bounded in L3 is not a bound on enstrophy.",
    ),
    rec(
        "L35",
        "knss_liouville_closes_X",
        "KNSS Liouville for bounded ancient solutions closes X",
        "fail",
        "Acta 2009: 2D and axisymmetric no-swirl. 3D remains a door. A Liouville theorem is not an a priori. Gabriel Koch, not Herbert.",
    ),
    rec(
        "L36",
        "chae_if_is_all_data_a1",
        "Chae Triebel-Lizorkin geometric if is all-data A1",
        "fail",
        "RMI 2007: direction in a Triebel-Lizorkin norm trades against |omega|. Still an if. All-data A1 stays blank.",
    ),
    rec(
        "L37",
        "chemin_gallagher_is_all_data",
        "Chemin-Gallagher large Besov data is all-data regularity",
        "fail",
        "ASENS 2006: arbitrarily large in B^{-1}_{∞,∞} under a nonlinear smallness condition. Still a condition. Not all-data.",
    ),
    rec(
        "L38",
        "cannone_planchon_is_all_data",
        "Cannone-Planchon critical Besov mild solutions are all-data regularity",
        "fail",
        "SEDP 1993-94: small data, self-similar mild in homogeneous Besov. Small is not all-data. Not Jia large-data existence.",
    ),
    rec(
        "L39",
        "lin_ckn_closes_X",
        "Lin new proof of CKN closes X",
        "fail",
        "CPAM 1998: simplified epsilon-regularity, velocity L3 and pressure L3/2. Still partial regularity. Small is not empty. Not no blowup.",
    ),
    rec(
        "L40",
        "vasseur_ckn_closes_X",
        "Vasseur De Giorgi proof of CKN closes X",
        "fail",
        "NoDEA 2007: De Giorgi iteration, same CKN theorem. H^1 singular set small. Small is not empty. The 3/2 gap stays. Not no blowup.",
    ),
    rec(
        "L41",
        "farwig_very_weak_closes_X",
        "Farwig very weak solutions close X",
        "fail",
        "JMSJ 2007: Serrin class, no differentiability, generally not Leray-Hopf. A different class is not a bound on classical X. Sohr stays out.",
    ),
    rec(
        "L42",
        "cheskidov_energy_equality_closes_X",
        "Cheskidov energy equality closes X",
        "fail",
        "Nonlinearity 2020: energy equality in a weak-in-time Onsager class. A condition. Equality is not regularity and not a bound on X.",
    ),
    rec(
        "L43",
        "masmoudi_uniqueness_closes_X",
        "Masmoudi uniqueness of mild solutions closes X",
        "fail",
        "CPDE 2001: uniqueness in C([0,T); L^N). Uniqueness is not regularity. Not a bound on X.",
    ),
    rec(
        "L44",
        "wolf_local_pressure_closes_X",
        "Wolf local pressure closes X",
        "fail",
        "Local pressure projection: CKN in arbitrary domains. Still epsilon-regularity. Small is not empty. Not no blowup.",
    ),
    rec(
        "L45",
        "galdi_steady_closes_X",
        "Galdi physically reasonable solutions close X",
        "fail",
        "ARMA 2011: steady exterior Leray solutions in Finn's class. A different problem. Not evolutionary X.",
    ),
    rec(
        "L46",
        "temam_attractor_closes_X",
        "Temam attractor closes X",
        "fail",
        "JFA 1989 / attractor theory: 3D finite-dimensionality assumes the solution stays smooth. Gevrey assumes that if. Not an a priori on X. Foias stays out.",
    ),
    rec(
        "L47",
        "isett_onsager_closes_X",
        "Isett Onsager closes X",
        "fail",
        "Ann. of Math. 2018: Onsager for Euler, Holder 1/3. Different equation. Not a bound on NS X.",
    ),
    rec(
        "L48",
        "tsai_local_energy_ss_closes_X",
        "Tsai local-energy self-similar exclusion closes X",
        "fail",
        "ARMA 1998: local-energy self-similar profiles are trivial. Exclusion is not an a priori. Not Jia existence.",
    ),
    rec(
        "L49",
        "lemarie_local_leray_closes_X",
        "Lemarie-Rieusset local Leray solutions close X",
        "fail",
        "2002: uniformly locally square integrable, local energy inequality. A different class is not a bound on global X.",
    ),
    rec(
        "L50",
        "danchin_inhomogeneous_closes_X",
        "Danchin density-dependent NS closes X",
        "fail",
        "Critical well-posedness for inhomogeneous NS is a different equation. Not a bound on homogeneous X. Heywood stays out.",
    ),
    rec(
        "L51",
        "kukavica_unique_continuation_closes_X",
        "Kukavica unique continuation closes X",
        "fail",
        "JDDE 2013: strong unique continuation for differences. Vanishing order is not a bound on X. Not the one-component chair.",
    ),
    rec(
        "L52",
        "barker_type_i_ancient_closes_X",
        "Barker Type I ancient closes X",
        "fail",
        "JMFM 2019: Type I singularity iff a nontrivial mild bounded ancient with Type I decay. An iff is not a bound on X. Forced Leray stays Albritton.",
    ),
    rec(
        "L54",
        "barker_sequential_l3_closes_X",
        "Barker sequential L3 Liouville closes X",
        "fail",
        "JMFM 2019: ancient solutions bounded in L3 along a backward sequence are trivial. A sequential Liouville is not a bound on X. ESS stays Escauriaza.",
    ),
    rec(
        "L53",
        "robinson_a_posteriori_closes_X",
        "Robinson a posteriori regularity closes X",
        "fail",
        "JMP 2007: a numerical certificate implies regularity. Still an if. A computed bound is not a bound on X. Hou stays computation as probe.",
    ),
    rec(
        "L55",
        "pavlovic_illposed_closes_X",
        "Pavlovic critical ill-posedness closes X",
        "fail",
        "JFA 2008: norm inflation in Besov minus-one infinity-infinity. Discontinuity of the solution map is not a bound on X. Small critical stays Koch-Tataru. Bourgain stays out.",
    ),
    rec(
        "L56",
        "rusin_minimal_data_closes_X",
        "Rusin minimal singularity data closes X",
        "fail",
        "JFA 2011: if some H-dot-1/2 data blow up, a minimal-norm datum does. Compactness of a hypothetical set is not a bound on X. Does not prove a singularity. Sverak stays doors. Jia stays existence.",
    ),
    rec(
        "L57",
        "germain_weak_strong_closes_X",
        "Germain weak-strong uniqueness closes X",
        "fail",
        "JDE 2006: multipliers and paramultipliers give weak-strong uniqueness. Uniqueness is not a bound on X. Mild uniqueness stays Masmoudi. Water waves stay off this chair.",
    ),
    rec(
        "L58",
        "cao_primitive_closes_X",
        "Cao primitive equations close X",
        "fail",
        "Ann. of Math. 2007: global strong solutions of the 3D viscous primitive equations. Hydrostatic. A different equation is not a bound on NS X. Titi stays off. Robinson stays a posteriori.",
    ),
    rec(
        "L59",
        "hieber_stokes_closes_X",
        "Hieber Stokes maximal regularity closes X",
        "fail",
        "CPDE 1997 / J. Evol. Eq. 2001: maximal L^p-L^q for parabolic semigroups and Stokes in a half space. A linear estimate is not a bound on X. Pruss stays out.",
    ),
    rec(
        "L60",
        "bedrossian_45_closes_X",
        "Bedrossian Kolmogorov 4/5 closes X",
        "fail",
        "CMP 2019: 4/5 for forced stationary martingale solutions under weak anomalous dissipation. A cascade identity is not a bound on X. Energy equality stays Cheskidov. Forced Leray stays Albritton.",
    ),
    rec(
        "L61",
        "kelliher_inviscid_closes_X",
        "Kelliher vanishing viscosity closes X",
        "fail",
        "CMS 2008: vanishing viscosity iff a vortex sheet on the boundary. An equivalence for the inviscid limit is not a bound on X. Kato stays out. Euler singularity stays Elgindi.",
    ),
    rec(
        "L62",
        "silvestre_fokker_closes_X",
        "Silvestre kinetic Fokker-Planck closes X",
        "fail",
        "Ars Inven. Anal. 2022: Holder estimates for kinetic Fokker-Planck up to the boundary. A different equation is not a bound on NS X. De Giorgi CKN stays Vasseur. Caffarelli-Silvestre extension stays off.",
    ),
    rec(
        "L63",
        "schonbek_decay_closes_X",
        "Schonbek Fourier splitting closes X",
        "fail",
        "ARMA 1985: algebraic L2 decay of weak solutions by Fourier splitting. Large-time decay is not a bound on X. Energy equality stays Cheskidov. Attractors stay Temam.",
    ),
    rec(
        "L64",
        "ponce_commutator_closes_X",
        "Ponce Kato-Ponce closes X",
        "fail",
        "CPAM 1988: commutator estimates for Euler and NS. A tool is not a bound on X. Continuation stays Beale. Kato stays out.",
    ),
    rec(
        "L65",
        "iftimie_thin_closes_X",
        "Iftimie thin domain closes X",
        "fail",
        "JDE 2001: global strong solutions in a sufficiently thin 3D domain. Thinness is an if, not a bound on 3D X. Raugel stays out.",
    ),
    rec(
        "L66",
        "fursikov_control_closes_X",
        "Fursikov controllability closes X",
        "fail",
        "CRAS 1996: local exact controllability of NS. A control is not a bound on free X. Attractors stay Temam. A posteriori stays Robinson.",
    ),
    rec(
        "L67",
        "maremonti_periodic_closes_X",
        "Maremonti time-periodic NS closes X",
        "fail",
        "Time-periodic solutions of 3D NS in unbounded domains. A periodic class is not a bound on X. Attractors stay Temam. Forced Leray stays Albritton.",
    ),
    rec(
        "L68",
        "korobkov_2d_steady_closes_X",
        "Korobkov 2D steady Leray closes X",
        "fail",
        "Korobkov-Pileckas-Russo: 2D steady Leray problem / Liouville. 2D and steady is not a bound on 3D evolutionary X. Leray stays out.",
    ),
    rec(
        "L69",
        "hishida_exterior_closes_X",
        "Hishida exterior evolutionary NS closes X",
        "fail",
        "Exterior evolutionary NS / Stokes semigroup and spatial decay. A setting is not a bound on periodic X. Steady exterior stays Galdi. Linear Stokes stays Hieber. Heywood stays out.",
    ),
    rec(
        "L70",
        "mucha_slip_closes_X",
        "Mucha slip inflow NS closes X",
        "fail",
        "Slip or inflow-outflow NS is a boundary-condition variant. Not a bound on periodic no-slip X. Exterior stays Hishida. Vanishing viscosity stays Kelliher.",
    ),
    rec(
        "L71",
        "paicu_anisotropic_closes_X",
        "Paicu anisotropic NS closes X",
        "fail",
        "Anisotropic NS with partial dissipation is a different equation. Global regularity there is not a bound on isotropic X. Primitive stays Cao. Density-dependent stays Danchin.",
    ),
    rec(
        "L72",
        "gibbon_stretch_closes_X",
        "Gibbon vortex stretching closes X",
        "fail",
        "Physica D 2008: stretching identities and Euler standing. Identities and diagnostics are not a bound on X. Continuation stays Beale. Strain cut stays Miller. Euler singularity stays Elgindi.",
    ),
    rec(
        "L73",
        "ambrosio_rlf_closes_X",
        "Ambrosio Regular Lagrangian Flow closes X",
        "fail",
        "Invent. Math. 2004: Regular Lagrangian Flow for BV fields. A well-defined ODE flow is not a bound on X. Weak-strong stays Germain. Mild uniqueness stays Masmoudi. DiPerna stays out.",
    ),
    rec(
        "L74",
        "enciso_knots_closes_X",
        "Enciso knotted Beltrami fields close X",
        "fail",
        "Ann. of Math. 2012: knots and links in steady Euler. Existence of knotted Beltrami fields is not a bound on evolutionary X. Euler singularity stays Elgindi. Onsager stays Isett. Arnold stays out.",
    ),
]


SPEAKERS = sorted({t["speaker"] for t in TURNS})

KINGDOMS = [
    {"name": "Supercriticality", "who": "Tao", "slot": "B"},
    {"name": "Liouville / ancient / self-similar", "who": "Sverak, Seregin", "slot": "B"},
    {"name": "ESS L3 endpoint", "who": "Escauriaza", "slot": "B"},
    {"name": "Unique continuation", "who": "Kukavica", "slot": "B"},
    {"name": "Ancient Liouville / KNSS", "who": "Nadirashvili", "slot": "B"},
    {"name": "Type I / ancient correspondence", "who": "Barker", "slot": "B"},
    {"name": "Sequential L3 Liouville", "who": "Barker", "slot": "B"},
    {"name": "A posteriori regularity", "who": "Robinson", "slot": "B"},
    {"name": "Critical ill-posedness", "who": "Pavlovic", "slot": "B"},
    {"name": "Minimal singularity data", "who": "Rusin", "slot": "B"},
    {"name": "Weak-strong uniqueness", "who": "Germain", "slot": "B"},
    {"name": "Primitive equations", "who": "Cao", "slot": "B"},
    {"name": "Stokes / maximal L^p regularity", "who": "Hieber", "slot": "B"},
    {"name": "Kolmogorov 4/5 / weak anomalous dissipation", "who": "Bedrossian", "slot": "B"},
    {"name": "Vanishing viscosity / inviscid limit", "who": "Kelliher", "slot": "B"},
    {"name": "Kinetic Fokker-Planck / Holder", "who": "Silvestre", "slot": "B"},
    {"name": "Energy decay / Fourier splitting", "who": "Schonbek", "slot": "B"},
    {"name": "Kato-Ponce / commutator estimates", "who": "Ponce", "slot": "B"},
    {"name": "Thin domain / 2D-3D perturbation", "who": "Iftimie", "slot": "B"},
    {"name": "Controllability / NS control", "who": "Fursikov", "slot": "B"},
    {"name": "Time-periodic NS", "who": "Maremonti", "slot": "B"},
    {"name": "Steady 2D Liouville / Leray problem", "who": "Korobkov", "slot": "B"},
    {"name": "Exterior evolutionary NS / spatial decay", "who": "Hishida", "slot": "B"},
    {"name": "Slip / inflow-outflow NS", "who": "Mucha", "slot": "B"},
    {"name": "Anisotropic NS / partial dissipation", "who": "Paicu", "slot": "B"},
    {"name": "Vortex stretching / strain-vorticity alignment", "who": "Gibbon", "slot": "B"},
    {"name": "Regular Lagrangian Flow / DiPerna-Lions transport", "who": "Ambrosio", "slot": "B"},
    {"name": "Knotted Beltrami fields / steady Euler topology", "who": "Enciso", "slot": "B"},
    {"name": "Forward self-similar large data", "who": "Jia", "slot": "B"},
    {"name": "Local-energy self-similar exclusion", "who": "Tsai", "slot": "B"},
    {"name": "Local Leray solutions", "who": "Lemarie-Rieusset", "slot": "B"},
    {"name": "Inhomogeneous / density-dependent NS", "who": "Danchin", "slot": "B"},
    {"name": "Numerical non-uniqueness", "who": "Guillod", "slot": "B"},
    {"name": "Partial regularity", "who": "Caffarelli, Kohn", "slot": "B"},
    {"name": "CKN new proof", "who": "Lin", "slot": "B"},
    {"name": "De Giorgi CKN", "who": "Vasseur", "slot": "B"},
    {"name": "Local pressure / local energy", "who": "Wolf", "slot": "B"},
    {"name": "Geometry", "who": "Constantin, Fefferman", "slot": "B"},
    {"name": "Geometric if (weaker than CF)", "who": "Beirao-Berselli", "slot": "B"},
    {"name": "Triebel-Lizorkin geometric if", "who": "Chae", "slot": "B"},
    {"name": "Type I plus continuous direction", "who": "Giga-Miura", "slot": "B"},
    {"name": "Double-cone geometric if", "who": "Lei-Ren-Tian", "slot": "B"},
    {"name": "Axisymmetric Type I", "who": "CSTY", "slot": "B"},
    {"name": "Continuation", "who": "Beale", "slot": "B"},
    {"name": "BMO continuation", "who": "Kozono-Taniuchi", "slot": "B"},
    {"name": "Very weak solutions", "who": "Farwig", "slot": "B"},
    {"name": "Steady / physically reasonable", "who": "Galdi", "slot": "B"},
    {"name": "Attractors / functional NS", "who": "Temam", "slot": "B"},
    {"name": "Energy equality / Onsager", "who": "Cheskidov", "slot": "B"},
    {"name": "One-component if", "who": "Neustupa-Penel", "slot": "B"},
    {"name": "Critical small data", "who": "Koch, Tataru", "slot": "B"},
    {"name": "Large Besov / nonlinear smallness", "who": "Chemin-Gallagher", "slot": "B"},
    {"name": "Critical Besov mild / small self-similar", "who": "Cannone-Planchon", "slot": "B"},
    {"name": "Critical uniqueness", "who": "Masmoudi", "slot": "B"},
    {"name": "Scaling gap / log-bmo if", "who": "Grujic", "slot": "B"},
    {"name": "Strain / middle eigenvalue", "who": "Miller", "slot": "B"},
    {"name": "Wild weak solutions", "who": "Vicol, Buckmaster", "slot": "B"},
    {"name": "Forced Leray", "who": "Albritton", "slot": "B"},
    {"name": "Unforced Leray-Hopf", "who": "Hou-Wang-Yang", "slot": "B"},
    {"name": "Euler singularity", "who": "Elgindi", "slot": "B"},
    {"name": "Onsager / Holder 1/3", "who": "Isett", "slot": "B"},
    {"name": "Computation as probe", "who": "Hou", "slot": "B"},
    {"name": "Announcements", "who": "current math.AP", "slot": "B"},
    {"name": "The desk", "who": "operator", "slot": "meta"},
]


def run(out: Path | None = None) -> dict:
    replies = sum(1 for t in TURNS if t["to"])
    payload = {
        "meta": {
            "question": "seat the living dream team; where now; can X close",
            "writeup": "docs/DA-LIVING.md",
            "not_a_vote": True,
            "not_a_close": True,
            "not_channeling": True,
            "papers_not_persons": True,
            "operator_name": "living dream team",
            "valuable_part": "living kingdoms left intact, aimed at one fail-able question",
            "past_bench_stays": True,
            "regularity_after": "open",
            "possible_to_close_X": "open",
            "next_write": (
                "A residual: closed estimate for X, a killing field, "
                "or one preprint identity. Regularity stays open. "
                "Do not spawn n=64. Do not write leftover B42."
            ),
        },
        "turns": TURNS,
        "claims": CLAIMS,
        "speakers": SPEAKERS,
        "kingdoms": KINGDOMS,
        "counts": {
            "turns": len(TURNS),
            "speakers": len(SPEAKERS),
            "addressed_replies": replies,
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "how_far": [
            "living papers sat and talked",
            "kingdoms stayed carved out",
            "one focused question: where now, can X close",
            "possible_to_close_X stays open",
            "impossible_to_close_X failed as a theorem",
            "conversation did not close X",
            "next write is a residual, not leftover B42",
            "domain B still open",
        ],
        "next_da_move": (
            "Leftover knobs are scored. Where now: a residual. "
            "Possible to close X stays open. Regularity stays open. "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_living.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA living. Papers talk. Not a vote. Not a close.")
    print("Full scene: docs/DA-LIVING.md")
    print(f"{'who':<22} to")
    for t in payload["turns"]:
        whom = ", ".join(t["to"])
        print(f"  {t['speaker']:<20} → {whom}")
        print(f"    {t['line']}")
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
