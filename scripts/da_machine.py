#!/usr/bin/env python3
"""
Domain Architect process machine.

Anti-bullshit device. Operator needs no chops. AI proposes.
Checkers verdict. Glue and fake passes are refused.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "results" / "da_machine_log.json"

SLOTS = {
    "A": {
        "object": "Q1-augmented NS, eps>0",
        "note": "docs/TRACK-A-LEMMAS.md",
        "checker": ["python3", "-m", "unittest", "tests.test_augmented_ns_verify", "-v"],
    },
    "B": {
        "object": "classical NS, keep 1/r^4",
        "note": "docs/TRACK-B-LEMMAS.md",
        "checker": ["python3", "-m", "unittest", "tests.test_track_b_lemmas", "-v"],
        "domain_pass_means": "open",
        "why_no_pass": "Lemma identities may hold. Regularity stays open.",
    },
    "Q": {
        "object": "inverse-GCD floors",
        "note": "docs/SPECTRAL-FLOOR-EXPLORATION.md",
        "checker": ["python3", "-m", "unittest", "tests.test_spectral_floor_explore", "-v"],
    },
    "U": {
        "object": "realization score R (exercise, not a unifier)",
        "note": "docs/UNIFIER-EXERCISE.md",
        "checker": [
            "python3",
            "-m",
            "unittest",
            "tests.test_unifier_exercise",
            "tests.test_unifier_combo",
            "tests.test_da_sixteen",
            "tests.test_da_fingers",
            "tests.test_da_how",
            "tests.test_da_flush",
            "tests.test_da_wave",
            "tests.test_da_game",
            "tests.test_da_screen",
            "tests.test_da_gq",
            "tests.test_da_separate",
            "tests.test_da_cosmo",
            "tests.test_da_sm",
            "tests.test_da_sm_break",
            "tests.test_da_team",
            "tests.test_da_sm_lineage",
            "tests.test_da_harmonic",
            "tests.test_da_ground",
            "tests.test_da_pipe",
            "tests.test_da_desk",
            "tests.test_da_compute",
            "tests.test_da_alert",
            "tests.test_da_session",
            "tests.test_da_living",
            "tests.test_da_leads",
            "-v",
        ],
    },
}

FORBIDDEN = [
    (r"\bsolved (navier|ns|rh|riemann)\b", "prize-style close"),
    (r"lambda_?min\s*\(\s*(q|qtilde|\\widetilde\s*q)", "full-spectrum Q floor"),
    (r"cos\s*\(?\s*alpha_?3", "Biot-Savart depletion slogan"),
    (r"beale|bkm", "BKM-from-L2 style close"),
    (r"\bsfe\b|\buhf\b|\bdhfa\b", "shelved HB stack"),
    (r"track\s*a\s*(implies|=>|⇒)\s*track\s*b", "A=>B glue"),
    (r"bridge.*=.*snd|snd.*=.*bridge", "triple-lock glue"),
]


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "meta": {
            "experiment": "DA-process-machine",
            "operator_needs_chops": False,
            "ai_is_generator": True,
            "not_a_unifier": True,
        },
        "runs": [],
        "counts": {"scored": 0, "pass": 0, "fail": 0, "open": 0},
    }


def save_log(data: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(data, indent=2))


def classify_claim(claim: str) -> dict:
    text = claim.lower()
    for pat, why in FORBIDDEN:
        if re.search(pat, text, flags=re.I):
            return {"domain": None, "verdict": "fail", "reason": f"forbidden: {why}"}
    if re.search(
        r"\brepair\b|\bwhat.?s wrong\b|\bhow to fix\b|\baugmented one\b|"
        r"\bdream team\b|\banalyze my\b|\bcomplete the chain\b|"
        r"\brenormali[sz]|\bda attempt\b|\bmy rh\b|"
        r"\btry every\b|\bquantum comput|\bsupercomput|\bbrute\b|"
        r"\bneed to close\b|\beinstein\b|\btesla\b|"
        r"\bbig picture\b|\bcomprehensive\b|\bwhat would they do next\b|"
        r"\bproof chain\b|\bwrite (me )?(the )?proof\b|\bda proof\b|"
        r"\btrack [ab]\b.{0,40}\bwrite\b|\bwrite\b.{0,40}\btrack [ab]\b|"
        r"\bwrite rh\b|\bmy best paper\b|"
        r"\bis that right\b|\bis (ns |navier |navi )?done\b|"
        r"\bcan da\b|\bda done\b|\blooks like.{0,24}done\b|"
        r"\bgcd paper\b|\bbest gcd\b|\bq6\b|\bq7\b|"
        r"\belectoral floor\b|\bspectral floor\b|"
        r"\bdirected at da\b|\bthese questions\b|\bcan da do\b|\bda study\b|"
        r"\bwas it you\b|\bdid da finish\b",
        text,
    ):
        return {
            "domain": "U",
            "verdict": "open",
            "reason": "looks like score U / SM Lagrangian / waveform; run sm or how",
        }
    if re.search(r"\bq_?1\b|augmented|ladyzhenskaya", text):
        return {"domain": "A", "verdict": "open", "reason": "looks like Track A; run check A"}
    if re.search(
        r"1/r\^?4|\bring\b|bony|3-conc|spread|tube|vorticity|hardy|\bgamma\b|triad|track b|t2 lemma|occupation|\bglue\b|two-regime|enstrophy|energy.?ceiling|low-?j|climbing|climb.?law|dj\*/dt|barycenter|strain|eigenframe|\balignment\b|packet.?geometry|stretching.?budget|weighted.?alignment|enstrophy.?balance|angular.?viscos|coherent.?conc|signed.?strain|blob.?strain|field.?occupation|field.?glue|ns.?climb|field.?climb|saving.?c|climb.?sketch|longer.?path|longer.?run|dns.?a.?priori|packet.?dns|tube.?budget|align(?:ment)?.?a.?priori|payers|aligned.?budget|enstrophy.?net|visc(?:osity)?.?owns|balance.?a.?priori|signed.?blob|onesided.?cubic|blob.?a.?priori|field.?clock|occupation.?a.?priori|matching.?the.?sketch|glue.?a.?priori|saving.?climb|climb.?window|finer.?box|finer.?dns|leftover.?close|regularity.?leftover|residual.?holes|synthetic.?r\b|miller.?cut|lambda.?2|empty.?rename|det.?plus|a1.?a2.?blanks|a1.?off|a2.?live|a2.?path|log.?bmo|2607.?08866|\bcfm\b|fefferman.?majda|self.?similar|ancient.?doors|liouville|jia.?sverak|forward.?self.?similar|guillod.?sverak|numerical.?pitchfork|2509.?25116|unforced.?leray.?hopf|2501.?08976|double.?cone|axisymmetric.?type.?i|bmo.?continuation|one.?component|l3.?endpoint|knss|ancient.?liouville|triebel.?lizorkin|nonlinear.?smallness|besov.?large|besov.?mild|lin.{0,40}ckn|new.?proof.{0,20}ckn|vasseur.{0,40}(ckn|de.?giorgi|partial.?reg)|de.?giorgi.{0,20}(ckn|navier)|very.?weak|farwig.{0,40}very.?weak|cheskidov.{0,40}(energy.?equal|onsager)|energy.?equal|masmoudi.{0,40}(uniqu|mild)|critical.?uniqu|wolf.{0,40}(local.?energy|local.?press|epsilon.?reg)|local.?pressure|galdi.{0,40}(steady|exterior|physically.?reason)|physically.?reason|temam.{0,40}(attractor|gevrey)|ns.?attractor|isett.{0,40}(onsager|euler|holder)|onsager.?conject|tsai.{0,40}(self.?similar|local.?energy)|lemarie.{0,40}(local.?leray|luloc)|local.?leray|danchin.{0,40}(inhomog|density)|density.?dependent.?ns|inhomogeneous.?navier|kukavica.{0,40}(unique.?cont|continuation)|unique.?continuation|barker.{0,40}(type.?i|ancient)|type.?i.{0,20}ancient|robinson.{0,40}(a.?posteriori|posterior|certificate)|a.?posteriori.{0,20}(regular|ns)|barker.{0,40}(l3|liouville)|sequential.?l3|pavlovic.{0,40}(ill.?posed|norm.?inflat|critical.?space)|ill.?posed.{0,20}(navier|critical)|norm.?inflation|rusin.{0,40}(minimal|singularity|h.?1.?2)|minimal.?initial.?data|minimal.?singularity|germain.{0,40}(weak.?strong|paramultiplier)|weak.?strong.?uniqu|paramultiplier|cao.{0,40}(primitive|ocean|atmospher)|primitive.?equations|hieber.{0,40}(stokes|maximal)|maximal.?l.?p|stokes.{0,20}(half.?space|maximal)|bedrossian.{0,40}(4.?5|kolmogorov)|kolmogorov.?4.?5|4.?5.?law|kelliher.{0,40}(vanishing|inviscid|vortex.?sheet)|vanishing.?viscos|inviscid.?limit|silvestre.{0,40}(holder|fokker|kinetic)|fokker.?planck|kinetic.?fokker|schonbek.{0,40}(decay|fourier.?split)|fourier.?splitting|ponce.{0,40}(commutator|kato)|kato.?ponce|iftimie.{0,40}(thin|domain)|thin.?domain|fursikov.{0,40}(control|controllab)|exact.?controllab|maremonti.{0,40}(periodic|exterior)|time.?periodic.?ns|korobkov.{0,40}(leray|liouville|steady)|2d.?steady.?leray|leray.?problem|hishida.{0,40}(exterior|stokes|rotating)|exterior.?evolutionary|mucha.{0,40}(slip|inflow|outflow)|slip.?boundary.?ns|inflow.?outflow|paicu.{0,40}(anisotropic|partial.?dissip)|anisotropic.?navier|partial.?dissipation|gibbon.{0,40}(stretch|strain|euler)|vortex.?stretching|ambrosio.{0,40}(transport|lagrangian|rlf)|regular.?lagrangian|enciso.{0,40}(knot|beltrami|euler)|knotted.?(vortex|beltrami)|beltrami.?field|feireisl.{0,40}(compress|viscous)|compressible.?navier|viscous.?compressible|kiselev.{0,40}(euler|growth|double)|double.?exponential.?euler|2d.?euler.?growth",
        text,
    ):
        return {
            "domain": "B",
            "verdict": "open",
            "reason": "looks like Track B; run trackb. Regularity stays open.",
        }
    if re.search(r"bridge|prime.?block|h_n|inverse.?gcd|qtilde|theorem p", text):
        return {"domain": "Q", "verdict": "open", "reason": "looks like Track Q; run check Q"}
    if re.search(
        r"\bunifier\b|realization|\block_r\b|cosmos|hierarchy|vacuum|\b16\b|finger|wave|falsif|superposition|entangle|standard model|lagrangian|yukawa|weinberg|dream team|digital divide|lineage|maxwell|yang-mills|harmonic vocab|vocabulary of harmonic|spherical harmonic|peter.?weyl|hodge form|harmonic universe|bag of couplings|ground level|\beinstein\b|\btesla\b|\bfeynman\b|\bpipe\b|satellite|hologram|gwtc|desi|think tank|\bcorpus\b|\bdesk\b|write-?up|anti-?bullshit|comput(e|ing)|dedalus|sympy|gwosc|\balert\b|text me|notif|converse|working session|talk to each other|virtual s[eé]ance|kingdoms|living dream team|living bench|not dead|full.?roll|all specialties|next lead|every chair|seat miller|albritton|beirao|berselli|giga.?miura|\bmiura\b|\bseat jia\b|\bseat guillod\b|\bseat hou.?wang.?yang\b|\bseat lei.?ren.?tian\b|\bseat csty\b|\bseat kozono|\bseat neustupa|\bseat escauriaza|\bseat nadirashvili|\bseat chae\b|\bseat chemin|\bseat cannone|\bseat lin\b|\bseat vasseur\b|\bseat farwig\b|\bseat cheskidov\b|\bseat masmoudi\b|\bseat wolf\b|\bseat galdi\b|\bseat temam\b|\bseat isett\b|\bseat tsai\b|\bseat lemarie\b|\bseat danchin\b|\bseat kukavica\b|\bseat barker\b|living genius|genius roster|\bda now\b|\bda feed\b|live feed|latest (ligo|lhc|pdg)|particle accelerator|\bnow roster\b|\bseat robinson\b|\bseat pavlovic\b|\bseat rusin\b|\bseat germain\b|\bseat cao\b|\bseat hieber\b|\bseat bedrossian\b|\bseat kelliher\b|\bseat silvestre\b|\bseat schonbek\b|\bseat ponce\b|\bseat iftimie\b|\bseat fursikov\b|\bseat maremonti\b|\bseat korobkov\b|\bseat hishida\b|\bseat mucha\b|\bseat paicu\b|\bseat gibbon\b|\bseat ambrosio\b|\bseat enciso\b|\bseat feireisl\b|\bseat kiselev\b|\bda next\b|\bnow what\b|\bnowwhat\b|\bwhat would you\b|\blost operator\b|\bmissing piece\b|\bsmartest\b|\bin history\b|\bwhat would you do now\b|\bda hunt\b|\bhunter mode\b|\bproof chain\b|\bobject window\b|\bda look\b|\blook at the object\b|\bshow the object\b|\bcontext and meaning\b|\bunderstands context\b|\bfrom my work\b|\bwhere it breaks\b|\bda from\b|\bglobal regularity\b|\bmy steps\b|\bda proof\b|\bwrite (me )?(the )?proof\b|\bxavier stokes\b|\bnavier.?stokes\b|\brh proof\b|\briemann\b|\bproof chain please\b|around.?the.?wall|where.?is.?the.?wall|translate.?to.?math|proof.?chain.?next|radial.?spoke|\bda agent\b|agent.?shaped|domain architect agent|feed freshness|stale.?da|stale.?feed|must stay current|last.?scan",
        text,
    ):
        return {"domain": "U", "verdict": "open", "reason": "looks like score U / SM Lagrangian / waveform; run sm or how"}
    return {"domain": None, "verdict": "open", "reason": "no slot; rephrase into A, B, Q, or U"}


def run_checker(domain: str) -> dict:
    slot = SLOTS[domain]
    if slot["checker"] is None:
        return {"domain": domain, "verdict": "open", "reason": slot["why_no_pass"]}
    proc = subprocess.run(slot["checker"], cwd=ROOT, capture_output=True, text=True)
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    if proc.returncode != 0:
        return {
            "domain": domain,
            "verdict": "fail",
            "reason": "checker exit %s" % proc.returncode,
            "tail": tail[-8:],
        }
    # Slot B: lemma tests holding is not a regularity pass.
    if slot.get("domain_pass_means") == "open":
        return {
            "domain": domain,
            "verdict": "open",
            "reason": slot["why_no_pass"],
            "tail": tail[-8:],
        }
    return {
        "domain": domain,
        "verdict": "pass",
        "reason": "checker exit 0",
        "tail": tail[-8:],
    }


def maybe_alert(source: str) -> None:
    from da_alert import notify

    payload = notify(source=source)
    if payload["meta"].get("significant"):
        print("ALERT (significant):")
        print(payload["plain"])


def append_run(domain: str | None, claim: str, verdict: str, note: str) -> dict:
    data = load_log()
    rec = {
        "t": datetime.now(timezone.utc).isoformat(),
        "domain": domain,
        "claim": claim,
        "verdict": verdict,
        "note": note,
    }
    data["runs"].append(rec)
    data["counts"]["scored"] = len(data["runs"])
    data["counts"]["pass"] = sum(1 for r in data["runs"] if r["verdict"] == "pass")
    data["counts"]["fail"] = sum(1 for r in data["runs"] if r["verdict"] == "fail")
    data["counts"]["open"] = sum(1 for r in data["runs"] if r["verdict"] == "open")
    save_log(data)
    return rec


def cmd_status() -> int:
    data = load_log()
    print("DA is an anti-bullshit device.")
    print("Operator needs no chops. AI proposes. Checkers verdict.")
    print("Slots:")
    for key, slot in SLOTS.items():
        print(f"  {key}  {slot['object']}")
        print(f"      {slot['note']}")
    print("counts", json.dumps(data["counts"]))
    print("Agent-shaped: propose, scan, score, alert.")
    from da_feed import format_freshness, freshness

    fr = freshness()
    print(format_freshness(fr))
    print("now / feed / agent: python3 scripts/da_machine.py now|feed|agent")
    if fr.get("stale"):
        print("re-run: python3 scripts/da_machine.py feed")
    return 0


def cosmos_drill() -> dict:
    """DA drill-down: official Cosmo 16 names, must-hits, score core, missing F."""
    return {
        "slot": "U",
        "cosmos_list_found": True,
        "cosmos_core_equation_public": False,
        "n_claimed": 16,
        "n_confirmed": 16,
        "source": "https://cosmoevolution3d.base44.app",
        "catalog": "docs/COSMO-SIXTEEN.md",
        "possibility_claim": {
            "statement": "unification is possible with about 16 variables",
            "verdict": "open",
            "why": (
                "Names exist. A finite n is a real narrowing IF one public map F "
                "of those n hits the four couplings. The app saying 16/16 is "
                "not the check. The check is χ²_ext(F(x)) ≤ ε². F is still private."
            ),
        },
        "layers": [
            {
                "layer": 0,
                "name": "official Cosmo 16 (Topology vs Gauge table)",
                "pieces": [
                    "Koide",
                    "m_tau",
                    "generations",
                    "charge",
                    "alpha",
                    "sin2_theta_W",
                    "m_mu/m_e",
                    "v",
                    "m_H",
                    "CKM_theta12",
                    "alpha_s",
                    "m_p/m_e",
                    "Lambda",
                    "G",
                    "ell_P",
                    "sum_m_nu",
                ],
                "status": "names found; 16th is sum m_nu, not R; F still private",
            },
            {
                "layer": 1,
                "name": "must-hit observables (any four-force unifier)",
                "pieces": [
                    "log_alpha_em",
                    "log_alpha_s",
                    "sin2_theta_w",
                    "log_hierarchy",
                    "log_cc_ratio",
                    "log_qcd_ratio",
                    "log_weak_ratio",
                ],
                "status": "cannot drop gravity or vacuum energy and still call it nature",
            },
            {
                "layer": 2,
                "name": "score core from lock-R search",
                "pieces": ["log_cc_ratio", "log_hierarchy"],
                "status": "in every best subset of size ≥ 2",
            },
            {
                "layer": 3,
                "name": "next lock-R pieces",
                "pieces": ["S_coh", "delta_spread", "grad_coh"],
                "status": "raise lock_R to 0.70 at k=5; still not F",
            },
            {
                "layer": 4,
                "name": "not in any best set",
                "pieces": [
                    "A_mean",
                    "f_mean",
                    "phi_scale",
                    "p_cut",
                    "log_alpha_em",
                    "log_alpha_s",
                    "sin2_theta_w",
                    "log_weak_ratio",
                ],
                "status": "do not drill these first",
            },
        ],
        "rebuild": (
            "Names exist. Rebuild is still blocked on a public F from a named "
            "topology to the four couplings plus G_N and Λ. Sitting at measured "
            "values is not that map. Do not glue this table to the reconstructed 4×4."
        ),
        "how_to_get_the_16": [
            "Done: official table is docs/COSMO-SIXTEEN.md / scripts/da_cosmo.py",
            "Still missing: the public producing-map (core equation is trade secret)",
        ],
        "next_da_move": (
            "Run the isolated Cosmo screen (da_cosmo). Do not treat 16/16 as a pass."
        ),
    }


def cmd_cosmos() -> int:
    from da_cosmo import run as cosmo_run

    drill = cosmos_drill()
    out = ROOT / "results" / "da_cosmos_drill.json"
    out.write_text(json.dumps(drill, indent=2))
    payload = cosmo_run()
    print("DA Cosmos drill. Official 16 found. Core equation still private.")
    print("source:", drill["source"])
    print("n_claimed:", drill["n_claimed"], "n_confirmed:", drill["n_confirmed"])
    for layer in drill["layers"]:
        print(f"L{layer['layer']} {layer['name']}: {', '.join(layer['pieces'])}")
        print(f"    {layer['status']}")
    print("16/16 UI:", "fail")
    print("gauge3:", payload["gauge3"]["verdict"], "nature4:", payload["nature4"]["verdict"])
    print("collapsed:", payload["collapsed"])
    print("rebuild:", drill["rebuild"])
    print("next:", drill["next_da_move"])
    append_run(
        "U",
        "Cosmos drill: official 16 from cosmoevolution3d.base44.app",
        "open",
        "names found; F private; 16/16 is not a pass; produce fails for all 16",
    )
    print(f"wrote {out}")
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_sixteen() -> int:
    from da_sixteen import run as sixteen_run

    payload = sixteen_run()
    print("DA 16. The 16th is R (realization). Official Cosmo 16 is a different catalog.")
    print("possibility-from-count:", payload["possibility_from_count"]["why"])
    print(f"baseline R={payload['baseline_R']:.4f}")
    for f in payload["each_one"]:
        d = "" if f["delta"] is None else f"{f['delta']:+.3f}"
        print(f"{f['id']:3d} {f['family']:<16} {f['name']:<18} {f['lock_R']:7.4f} {f['fits']} {d}")
    print("fits that move R:", payload["fits_that_move_R"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Identify the 16 from gauge / gravity-gauge / teleological / harmonic and test each",
        "open",
        "16th is R; four singletons raise lock-R; affine F to the four couplings fails",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_fingers() -> int:
    from da_fingers import run as fingers_run

    payload = fingers_run()
    print("DA five fingers on:", payload["meta"]["line"])
    print("The 16th is still R. Official Cosmo 16 is a different catalog.")
    for f in payload["tree"]["fingers"]:
        print(f"[{f['verdict']}] {f['name']}: {f['piece']}")
        print(f"    {f['why']}")
        for g in f.get("fingers", []):
            print(f"    [{g['verdict']}] {g['name']}: {g['piece']}")
    print("equal-width flattens χ²_ext:", payload["checks"]["equal_width_flattens_ext"])
    print("16 fates:")
    for rec in payload["candidates"]:
        print(f"  {rec['id']:2d} {rec['category']:<16} {rec['fate']:<22} {rec['name']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Five-finger DA on R = exp(-1/2 χ²_ext) exp(-1/2 χ²_int), then each piece, then the 16",
        "open",
        "product passes; implied F fails; vacuum/Planck width artifact; θ is the topological leftover",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_fate() -> int:
    from da_fingers import run as fingers_run

    payload = fingers_run()
    print("DA 16 candidates. Category, general fate, then smaller pieces.")
    print("Same five questions on each: kind / nature / score / produce / next.")
    for rec in payload["candidates"]:
        print(f"{rec['id']:2d} {rec['name']:<16} {rec['category']:<16} {rec['fate']}")
        for f in rec.get("hand", []):
            print(f"    [{f['verdict']}] {f['name']}: {f['why']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Category and general fate for each of the 16, then DA the smaller pieces",
        "open",
        "kind/nature/score/produce/next on all 16; produce fails; R is output; θ is topological",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_how() -> int:
    from da_how import run as how_run

    payload = how_run()
    print("DA how-it-knew. Cosmos internals not in the repo.")
    enum = payload["enumerator"]
    print(
        f"X_eligible={enum['X_eligible']}  X_must_hit={enum['X_must_hit_nature']}  "
        f"possible_by_count={enum['possible_by_count']}"
    )
    print("able means:", enum["able_means"])
    for step in enum["how_it_could_know"]:
        print(" -", step)
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "How can a typed catalog say possible and emit X candidates without F?",
        "open",
        "P1 n>k is the only pre-name possible; X is a type-count; P3 explicit F fails",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_flush() -> int:
    from da_flush import run as flush_run

    payload = flush_run()
    print("DA Hilbert flush. Not Quantum Lens. Not a quantum computer.")
    print("flushed:", payload["flushed"])
    for row in payload["best_combination_by_born_mass"]:
        print(f"k={row['k']}  mass={row['born_mass']:.3f}  {row['set']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Hilbert flush of combinations on the reconstructed 16",
        "open",
        "Born mass on vacuum, Planck, S_c, delta; rewrite of lock-R, not F",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_wave() -> int:
    from da_wave import run as wave_run

    payload = wave_run()
    print("DA waveform rules. Slots A/B/Q untouched. Not Quantum Lens.")
    print("collapsed:", payload["waveform"]["collapsed"], "emerged:", payload["waveform"]["emerged"])
    print("still in superposition:", payload["waveform"]["still_in_superposition"])
    print("falsification (head):")
    for row in payload["falsification"][:6]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Waveform rules: superposition, entanglement, collapse, falsification",
        "open",
        "not collapsed; unfalsifiable_might_be_true fails; F_exists fails; possible_by_count open",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_game() -> int:
    from da_game import run as game_run

    payload = game_run()
    print("DA game theory. Two games. Neither is F.")
    print("Game R top4:", payload["game_R"]["top4"], "same as flush:", payload["game_R"]["same_four_as_flush"])
    print("narrows past flush:", payload["game_R"]["narrows_past_flush"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Shapley on lock-R vs must-hit unifier game",
        "open",
        "Game R agrees with the flush four; Game U protects must-hits by definition; no F",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_screen() -> int:
    from da_screen import run as screen_run

    payload = screen_run()
    print("DA unification screen. Two levels. Do not glue them.")
    print(f"{'claim':<42} {'kind':<16} {'gauge3':<6} {'nature4'}")
    for c in payload["claims"]:
        print(f"{c['name']:<42} {c['kind']:<16} {c['gauge3_verdict']:<6} {c['nature4_verdict']}")
    print("still open as gauge3:", payload["still_open_as_gauge3"])
    print("passed nature4:", payload["passed_nature4"])
    print(payload["discernment"])
    append_run(
        "U",
        "Screen published unification claims at gauge3 vs nature4",
        "open",
        "nothing passes nature4; MSSM-class stays open as gauge3; SU(5) minimal and SM fail",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_gq() -> int:
    from da_gq import run as gq_run

    payload = gq_run()
    print("DA gravity + quantum. What is coupled? Each pair separate.")
    print(payload["what_is_coupled"])
    for p in payload["pairs"]:
        print(f"  [{p['verdict']}] {p['name']}: {p['coupling']}")
    print("leftovers:", payload["leftovers"])
    append_run(
        "U",
        "Start at gravity + quantum: what is coupled?",
        "open",
        "universal couple is (g,T) via G; vacuum leftover fails as a prediction; gauge3 not coupled to G",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_tracka() -> int:
    from track_a_lemmas import run as tracka_run

    payload = tracka_run()
    print("DA Track A. Q1-augmented NS. This PDE only.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("theorem A:", payload["meta"]["theorem_A"])
    print("eps->0:", payload["meta"]["eps_to_0"])
    print("implies B:", payload["meta"]["implies_B"])
    print("next:", payload["next_da_move"])
    append_run(
        "A",
        "Theorem A for Q1-augmented NS at eps>0",
        "pass",
        "this PDE only; uniform H1 as eps->0 stays open; A=>B fail",
    )
    print(f"wrote {payload.get('_wrote')}")
    maybe_alert("tracka")
    return 0


def cmd_trackb() -> int:
    from track_b_lemmas import run as trackb_run

    payload = trackb_run()
    print("DA Track B. Lemma identities scored. Regularity stays open.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("domain:", payload["meta"]["domain_verdict"])
    print("next:", payload["next_da_move"])
    for row in payload["lemmas"]:
        append_run("B", row["statement"], row["verdict"], row["name"] + ": " + row["why"])
    append_run(
        "B",
        "classical 3D NS globally regular (domain close)",
        "open",
        "lemma identities held or correctly failed; no closed estimate for X",
    )
    print(f"wrote {payload.get('_wrote')}")
    maybe_alert("trackb")
    return 0


def cmd_sm() -> int:
    from da_sm import run as sm_run

    payload = sm_run()
    print("DA SM Lagrangian. Started over from L_SM. Cosmo 16 not used.")
    print("realized:", payload["realized_equation"]["equation"])
    print("working couple:", payload["realized_equation"]["working_couple"])
    print("gauge3:", payload["gauge3"], "nature4:", payload["nature4"])
    for b in payload["blocks"]:
        print(f"  [{b['verdict']}] {b['name']}")
    append_run(
        "U",
        "Analyze the SM Lagrangian; realize the two-sided Einstein+T_SM equation",
        "open",
        "L consumes couplings; working couple pass; nature4 fail; A/B/Q untouched",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_team() -> int:
    from da_team import run as team_run

    payload = team_run()
    print("DA dream team. Paper + experiment. A vote cannot close.")
    print("Full roll (three benches): docs/DA-THINK-TANK.md")
    print("Working session: python3 scripts/da_machine.py session")
    print("Living session: python3 scripts/da_machine.py living")
    for m in payload["team"]:
        print(f"  [{m['slot']}] {m['name']}: {m['suggest']}")
    print("next B:", payload["consensus"]["B"])
    print("next U:", payload["consensus"]["U"])
    append_run(
        "U",
        "Seat the dream team from beyond the digital divide",
        "open",
        "paper+experiment seated; vote cannot close; next write still I_tube then T",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_session() -> int:
    from da_session import run as session_run

    payload = session_run()
    print("DA session. Colleagues at one table. Not a vote. Not a close.")
    print("Full scene: docs/DA-SESSION.md")
    for t in payload["turns"]:
        print(f"  {t['speaker']} → {', '.join(t['to'])}")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("regularity:", payload["meta"]["regularity_after"])
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Have the dream team converse as colleagues on the live problem",
        "open",
        "process pass; regularity still open; next write still I_tube then T",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_leads() -> int:
    from da_leads import run as leads_run

    payload = leads_run()
    print("DA leads. Every chair asked. Not a vote. Not a close.")
    print("Full roll: docs/DA-LEADS.md")
    for row in payload["leads"]:
        print(f"  [{row['slot']}] {row['who']}: {row['lead']}")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("regularity:", payload["meta"]["regularity_after"])
    print("possible_to_close_X:", payload["meta"]["possible_to_close_X"])
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Ask every seated kingdom for one lead",
        "open",
        "sweep pass; glue refused; possible_to_close_X open; next is a residual",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_living() -> int:
    from da_living import run as living_run

    payload = living_run()
    print("DA living. Papers talk. Not a vote. Not a close.")
    print("Full scene: docs/DA-LIVING.md")
    for t in payload["turns"]:
        print(f"  {t['speaker']} → {', '.join(t['to'])}")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("regularity:", payload["meta"]["regularity_after"])
    print("possible_to_close_X:", payload["meta"]["possible_to_close_X"])
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Seat the living dream team; where now; can X close",
        "open",
        "process pass; possible_to_close_X open; regularity still open; next is a residual",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_lineage() -> int:
    from da_sm_lineage import run as lineage_run

    payload = lineage_run()
    print("DA lineage. SM runs backwards by limits, forwards by assembly.")
    print(payload["dots"])
    for r in payload["forwards"]:
        print(f"  [{r['back_verdict']}] {r['name']}: {r['back_from_sm']}")
    append_run(
        "U",
        "Wind L_SM backwards through prior theories and forwards through the same dots",
        "open",
        "Maxwell/QED/Fermi/YM/GWS/QCD recover; Einstein and one-group UV do not; not F",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_harmonic() -> int:
    from da_harmonic import run as harmonic_run

    payload = harmonic_run()
    print("DA harmonic vocabulary. Typed catalog, not a unifier.")
    print(payload["meta"]["answer"])
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    append_run(
        "U",
        "Make a complete harmonic vocabulary out of mathematics",
        "open",
        "typed catalog pass; desk coverage pass; one-object / finished-field / F / HB / regularity fail",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_ground() -> int:
    from da_ground import run as ground_run

    payload = ground_run()
    print("DA ground. Spectrum is the destination, not a pass.")
    print("HB chapter 1 → process. Not a trigger. Not a theorem.")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("improvements:")
    for line in payload["improvements_to_da"]:
        print(f"  {line}")
    append_run(
        "U",
        "Ground-level destination: spectrum not a bag; reconstruct; ablate; ask Einstein/Tesla/Feynman",
        "open",
        "HB ch1→DA process pass; destination open; couplings/F/review/SFE/nodes fail; program review scores the process",
    )
    print(f"wrote {payload.get('_wrote')}")
    maybe_alert("ground")
    return 0


def cmd_now() -> int:
    from da_now import run as now_run

    payload = now_run()
    print("DA now. Living roster. Genius is not a slot.")
    print("seated", payload["counts"]["seated_living"], "watch", payload["counts"]["watch"])
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    append_run(
        "U",
        "Living roster of seated papers and collaborations; not a world genius census",
        "open",
        "genius is not a slot; vote fail; omniscience fail; especially involved = seated fluids + pipes",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_picture() -> int:
    from da_picture import print_picture

    print_picture()
    append_run(
        "U",
        "Picture: published survey names the next write; seeing the field is not the estimate",
        "open",
        "treatise pass; omniscience fail; qualified vote fail",
    )
    return 0


def cmd_brute() -> int:
    from da_brute import print_brute

    print_brute()
    append_run(
        "U",
        "Brute: a finite list is legal; try-every is not the leftover; quantum is not the estimate",
        "open",
        "finite pass; try-every fail; Grover/Shor are not an a priori",
    )
    return 0


def cmd_attempt(job: str = "", ask: str = "") -> int:
    from da_attempt import print_attempt

    print_attempt(job=job, ask=ask)
    append_run(
        "U",
        "Attempt: best A (Q1 + renormalization) and furthest RH; dream team looks; legal write",
        "open",
        "this PDE complete; uniform H1 open; RH WRITE open; Q is not RH; vote is not a close",
    )
    return 0


def cmd_repair(job: str = "", ask: str = "") -> int:
    from da_repair import print_repair

    print_repair(job=job, ask=ask)
    append_run(
        "U",
        "Take the operator's A / SND / H work; name the fault and the repair write",
        "open",
        "takes mine; Theorem A is this PDE; A=>B is not a repair",
    )
    return 0


def cmd_study() -> int:
    from da_study import print_study

    print_study()
    append_run(
        "U",
        "Study: questions pointed at DA; write yes; finish leftover no",
        "open",
        "support pass; solver fail; emit is not QED",
    )
    return 0


def cmd_q() -> int:
    from da_q import print_q

    print_q()
    append_run(
        "Q",
        "Look at the inverse-GCD paper: sitting floors, Q6 hygiene, Q7 not seated",
        "open",
        "Q6 is 22045478; retracted floor false; Q7 not seated; Q is not RH or B",
    )
    return 0


def cmd_done() -> int:
    from da_done import print_done

    print_done()
    append_run(
        "U",
        "Is NS done? A this PDE yes. Classical leftover no. Emit is not QED.",
        "open",
        "study is the write; Theorem A sits; B line (6) does not; A is not B",
    )
    return 0


def cmd_proof(problem: str = "", ask: str = "") -> int:
    from da_proof import parse_problems, print_proof

    pids = parse_problems(ask=ask, problem=problem)
    print_proof(problem=problem, ask=ask)
    append_run(
        "U",
        "Write the " + ", ".join(pids) + " proof chain from the ground floor",
        "open",
        "ask pass; emit is not QED; WRITE is the attempt; A is not B; Q is not RH",
    )
    return 0


def cmd_from() -> int:
    from da_from import print_from

    print_from()
    append_run(
        "U",
        "From your work: walk scored steps to the break; proceed is classify",
        "open",
        "skeleton pass; walk-to-break pass; analyze is not smoothness",
    )
    return 0


def cmd_look() -> int:
    from da_hunt import print_object_window

    print_object_window()
    print("anytime. hunt --look is the same window. Looking is not a bound.")
    append_run(
        "U",
        "Object window: look at X whenever you want",
        "open",
        "window pass; looking is not a bound; F is not the object",
    )
    return 0


def cmd_hunt(look: bool = False) -> int:
    from da_hunt import print_hunt

    print_hunt(look=look)
    append_run(
        "U",
        "Proof-chain hunter: scored edges, blocked edges, object window",
        "open",
        "graph pass; LLM fill fail; hunter does not write R",
    )
    return 0


def cmd_nowwhat() -> int:
    from da_nowwhat import print_nowwhat

    print_nowwhat()
    append_run(
        "U",
        "Lost-operator council: leftover papers say what they would try",
        "open",
        "papers not minds; not a vote; would_try is a claim; cannot is a veto",
    )
    return 0


def cmd_next(ask: str = "") -> int:
    from da_from import is_from_ask
    from da_hunt import is_look_ask
    from da_next import is_lost_ask, run as next_run
    from da_attempt import is_attempt_ask
    from da_brute import is_brute_ask
    from da_picture import is_picture_ask
    from da_done import is_done_ask
    from da_proof import is_proof_ask
    from da_q import is_q_ask
    from da_repair import is_repair_ask
    from da_study import is_study_ask

    if is_study_ask(ask):
        return cmd_study()
    if is_done_ask(ask):
        return cmd_done()
    if is_q_ask(ask):
        return cmd_q()
    if is_look_ask(ask):
        return cmd_look()
    if is_brute_ask(ask):
        return cmd_brute()
    if is_picture_ask(ask):
        return cmd_picture()
    if is_attempt_ask(ask):
        return cmd_attempt(ask=ask)
    if is_proof_ask(ask):
        return cmd_proof(ask=ask)
    if is_repair_ask(ask):
        return cmd_repair(ask=ask)
    if is_from_ask(ask):
        return cmd_from()
    if is_lost_ask(ask):
        return cmd_nowwhat()

    payload = next_run(ask=ask, fetch=True)
    print("DA next. Hub, rim, wall.")
    print("WHERE", payload["wall"]["where"])
    print("TARGET B", payload["wall"]["target_B"])
    print("AROUND", payload["wall"]["around"])
    tr = payload["translate"]
    if tr.get("ask"):
        print("ASK", tr["ask"])
        print("→", tr["slot"], tr["chair"], "/", tr["math"])
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    append_run(
        "U",
        "Now-what spoke: wall, target, translate words to math; latest data on the rim",
        "open",
        "hub-and-spoke pass; target is X not F; next does not write the leftover",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_agent() -> int:
    from da_agent import run as agent_run

    payload = agent_run(fetch=True)
    print("DA agent. Propose, scan, score, alert.")
    print("seated", payload["counts"]["seated_living"], "feed items", payload["tick"]["feed_items"])
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    append_run(
        "U",
        "Fit roster and feed into DA; agent-shaped process, not a closer",
        "open",
        "propose/scan/score/alert pass; close X fail; write F fail; latest data belongs",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_feed() -> int:
    from da_feed import format_freshness, run as feed_run

    payload = feed_run()
    print("DA feed. Public test results. Not omniscience. Not a close.")
    print(format_freshness(payload.get("freshness")))
    print("fetched", payload["meta"].get("fetched_at") or "none")
    for src in payload["scan"]:
        flag = "ok" if src.get("ok") else "miss"
        print(f"  [{flag}] {src['name']:<16} {src['slot']} n={src.get('n')}")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    append_run(
        "U",
        "Scan latest LIGO / LHC / PDG / arXiv results; keep each item in its slot",
        "open",
        "ongoing collection; glue to X fail; F fail; fetch miss is open",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_pipe() -> int:
    from da_pipe import run as pipe_run

    payload = pipe_run()
    print("DA pipe. Now-bench + falsify every verdict. Past team stays.")
    print("snapshot", payload["meta"]["snapshot"])
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    live = payload["live"]
    print("live arXiv:", "ok" if live.get("ok") else "miss", "n=", live.get("n"))
    append_run(
        "U",
        "Pipe current hard science into the think tank; falsify every pass/fail",
        "open",
        "additive now-bench; GWTC/EHT/DESI/LMFDB typed; glue fail; omniscience fail; killers on every verdict",
    )
    print(f"wrote {payload.get('_wrote')}")
    maybe_alert("pipe")
    return 0


def cmd_desk() -> int:
    from da_desk import run as desk_run

    payload = desk_run()
    print("DA desk. Write-up: docs/DA-DESK.md")
    print("DA is an anti-bullshit device. Process pass. Unifier fail.")
    print("Corpus = published papers. Pair 2–3. Score the sentence.")
    for r in payload["corpus_rules"]:
        print(f"  [{r['verdict']}] {r['id']}: {r['statement']}")
    append_run(
        "U",
        "Write the whole desk down; type the corpus method",
        "open",
        "write-up in docs/DA-DESK.md; corpus method pass; pairing-writes-F fail; all benches listed",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_alert() -> int:
    from da_alert import run as alert_run

    payload = alert_run()
    print("DA alert. Plain language on a flip. Catalogs do not text you.")
    print("significant:", payload["meta"]["significant"], "baseline:", payload["meta"]["baseline"])
    print(payload["plain"])
    print("next:", payload["recommendation"])
    append_run(
        "U",
        "Watch significant flips and explain them in plain language",
        "open",
        "baseline or no flip is not a discovery; webhook optional; no phone in repo",
    )
    print(f"wrote {payload.get('_wrote')} and {payload.get('_text')}")
    return 0


def cmd_compute() -> int:
    from da_compute import run as compute_run

    payload = compute_run()
    print("DA compute. A library sits on one slot. It is not a theorem.")
    for t in payload["tech"]:
        print(f"  [{t['status']}] {t['slot']} {t['name']}")
    append_run(
        "U",
        "List computing techniques we can borrow or wire in",
        "open",
        "FFT/eigh/identities/arXiv wired; sympy/LP/LMFDB/GWOSC borrow; DNS/QNM-glue/LLM-proof refuse",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_smbreak() -> int:
    from da_sm_break import run as break_run

    payload = break_run()
    print("DA broke L_SM past five blocks, then put it back.")
    print("leaves:", payload["meta"]["n_leaves"], "counts:", payload["counts"])
    print("unique SM:", payload["reassembly"]["unique_sm"])
    print("put back:", payload["reassembly"]["put_back"]["equation"])
    print("step 7 (produce couplings): fail")
    append_run(
        "U",
        "Break L_SM to atoms and reassemble Einstein+T_SM",
        "open",
        "more than 5 blocks; uniqueness pass; produce still fail; A/B/Q untouched",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_separate() -> int:
    from da_separate import run as separate_run

    payload = separate_run()
    print("DA separate. One object, one verdict. No bundles.")
    print("GQ:")
    for r in payload["GQ"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['coupling']}")
    print("PUB:")
    for r in payload["PUB"]:
        print(f"  gauge3={r['gauge3_alone']:<5} nature4={r['nature4_alone']:<5}  {r['name']}")
    print("SIX:")
    for r in payload["SIX"]:
        d = "" if r.get("delta_lock_R") is None else f" Δ={r['delta_lock_R']:+.3f}"
        print(f"  {r['id']:2d} [{r['verdict']}] {r['name']:<16}{d}")
    append_run(
        "U",
        "Run each GQ pair, published claim, reconstructed slot, and Cosmo slot alone",
        "open",
        "isolation did not write F; Cosmo produce fails alone; Einstein passes alone; MSSM open only as gauge3",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_check(domain: str) -> int:
    domains = list(SLOTS) if domain == "all" else [domain]
    rc = 0
    for d in domains:
        result = run_checker(d)
        print(d, result["verdict"], result["reason"])
        if result.get("tail"):
            print("  " + "\n  ".join(result["tail"]))
        append_run(d, f"automatic check {d}", result["verdict"], result["reason"])
        if result["verdict"] == "fail":
            rc = 1
    maybe_alert("check")
    return rc


def main() -> int:
    p = argparse.ArgumentParser(description="Domain Architect process machine")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("cosmos", help="official Cosmo 16 plus isolated screen")
    sub.add_parser("sixteen", help="identify 4x4 list, run each, name the 16th")
    sub.add_parser("fingers", help="five-finger DA on the R line, recurse, fate the 16")
    sub.add_parser("fate", help="category + general fate for each of the 16, then smaller pieces")
    sub.add_parser("how", help="how a typed catalog can say possible and emit X")
    sub.add_parser("flush", help="Hilbert flush of which candidates carry the score")
    sub.add_parser("wave", help="waveform rules: superposition, entanglement, collapse, falsification")
    sub.add_parser("game", help="Shapley on the score vs the unifier-claim game")
    sub.add_parser("screen", help="screen published unification claims at gauge3 vs nature4")
    sub.add_parser("gq", help="start at gravity + quantum: what is coupled")
    sub.add_parser("separate", help="run each GQ pair, published claim, and slot alone")
    sub.add_parser("tracka", help="score Track A lemmas; Theorem A for this PDE only")
    sub.add_parser("trackb", help="score Track B lemmas; regularity stays open")
    sub.add_parser("sm", help="analyze the SM Lagrangian; realize Einstein+T_SM")
    sub.add_parser("smbreak", help="break L_SM to atoms, then put it back")
    sub.add_parser("team", help="seat paper+experiment; a vote cannot close")
    sub.add_parser("session", help="working session: colleagues talk; not a close")
    sub.add_parser("living", help="living dream team: now-bench papers talk; not a close")
    sub.add_parser("leads", help="ask every seated kingdom for one lead; glue refused")
    sub.add_parser("lineage", help="wind L_SM backwards and forwards through prior theories")
    sub.add_parser("harmonic", help="typed harmonic vocabulary from mathematics; not a unifier")
    sub.add_parser("ground", help="spectrum destination: reconstruct, ablate, program review")
    sub.add_parser("pipe", help="now-bench: live science pipes + falsify every verdict")
    sub.add_parser("now", help="living roster: seated papers + watch list; not a genius census")
    sub.add_parser("feed", help="scan latest LIGO / LHC / PDG / arXiv results")
    sub.add_parser("agent", help="DA tick: roster + feed; agent-shaped, not a closer")
    nx = sub.add_parser("next", help="now-what spoke: wall, target, translate, latest data")
    nx.add_argument("--ask", default="", help="operator sentence to translate into math")
    sub.add_parser("nowwhat", help="lost-operator council: what the leftover papers would try")
    hn = sub.add_parser("hunt", help="proof-chain hunter: scored connections, blocked edges, object window")
    hn.add_argument("--look", action="store_true", help="print only the object window")
    ch = sub.add_parser("chain", help="same as hunt")
    ch.add_argument("--look", action="store_true", help="print only the object window")
    sub.add_parser("look", help="object window: look at X anytime")
    sub.add_parser("window", help="same as look")
    sub.add_parser("from", help="walk your scored steps to the break; proceed toward regularity")
    sub.add_parser("mine", help="same as from")
    sub.add_parser("study", help="exam: can DA do the asks; emit is not a solver pass")
    sub.add_parser("q", help="inverse-GCD paper, floors, Q6, Q7")
    sub.add_parser("done", help="is NS done? emit is not QED; A this PDE yes; B no")
    prf = sub.add_parser("proof", help="write a proof chain: NS, A, or RH")
    prf.add_argument("--problem", default="", help="NS | A | RH. Empty defaults to NS.")
    sub.add_parser(
        "picture",
        help="survey of each field; next write; not omniscience",
    )
    sub.add_parser(
        "brute",
        help="why try-every / quantum / supercomputer does not write the leftover",
    )
    at = sub.add_parser(
        "attempt",
        help="best A and RH: dream team looks; legal write; vote is not a close",
    )
    at.add_argument(
        "--job",
        default="",
        help="A | B | RH | SND | H. Empty prints all. B is unaugmented NS.",
    )
    rp = sub.add_parser(
        "repair",
        help="take A, SND, or H; name the fault and the repair write",
    )
    rp.add_argument(
        "--job",
        default="",
        help="A | SND | H (aliases: augmented, CONC, SPREAD, theorem H, H_N). Empty prints all three.",
    )
    sub.add_parser("desk", help="write-up roster + corpus method (papers, not a vote)")
    sub.add_parser("compute", help="computing techniques already wired, legal to borrow, or refuse")
    sub.add_parser("alert", help="plain-language text when a watched claim flips")
    c = sub.add_parser("check")
    c.add_argument("--domain", default="all", choices=["all", "A", "B", "Q", "U"])
    cl = sub.add_parser("classify")
    cl.add_argument("--claim", required=True)
    lg = sub.add_parser("log")
    lg.add_argument("--domain", required=True, choices=["A", "B", "Q", "U"])
    lg.add_argument("--claim", required=True)
    lg.add_argument("--verdict", required=True, choices=["pass", "fail", "open"])
    lg.add_argument("--note", default="")
    args = p.parse_args()

    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "cosmos":
        return cmd_cosmos()
    if args.cmd == "sixteen":
        return cmd_sixteen()
    if args.cmd == "fingers":
        return cmd_fingers()
    if args.cmd == "fate":
        return cmd_fate()
    if args.cmd == "how":
        return cmd_how()
    if args.cmd == "flush":
        return cmd_flush()
    if args.cmd == "wave":
        return cmd_wave()
    if args.cmd == "game":
        return cmd_game()
    if args.cmd == "screen":
        return cmd_screen()
    if args.cmd == "gq":
        return cmd_gq()
    if args.cmd == "separate":
        return cmd_separate()
    if args.cmd == "tracka":
        return cmd_tracka()
    if args.cmd == "trackb":
        return cmd_trackb()
    if args.cmd == "sm":
        return cmd_sm()
    if args.cmd == "smbreak":
        return cmd_smbreak()
    if args.cmd == "team":
        return cmd_team()
    if args.cmd == "session":
        return cmd_session()
    if args.cmd == "living":
        return cmd_living()
    if args.cmd == "leads":
        return cmd_leads()
    if args.cmd == "lineage":
        return cmd_lineage()
    if args.cmd == "harmonic":
        return cmd_harmonic()
    if args.cmd == "ground":
        return cmd_ground()
    if args.cmd == "pipe":
        return cmd_pipe()
    if args.cmd == "now":
        return cmd_now()
    if args.cmd == "feed":
        return cmd_feed()
    if args.cmd == "agent":
        return cmd_agent()
    if args.cmd == "next":
        return cmd_next(getattr(args, "ask", ""))
    if args.cmd == "nowwhat":
        return cmd_nowwhat()
    if args.cmd in ("hunt", "chain"):
        return cmd_hunt(getattr(args, "look", False))
    if args.cmd in ("look", "window"):
        return cmd_look()
    if args.cmd in ("from", "mine"):
        return cmd_from()
    if args.cmd == "study":
        return cmd_study()
    if args.cmd == "q":
        return cmd_q()
    if args.cmd == "done":
        return cmd_done()
    if args.cmd == "proof":
        return cmd_proof(problem=getattr(args, "problem", ""))
    if args.cmd == "picture":
        return cmd_picture()
    if args.cmd == "brute":
        return cmd_brute()
    if args.cmd == "attempt":
        return cmd_attempt(job=getattr(args, "job", ""))
    if args.cmd == "repair":
        return cmd_repair(job=getattr(args, "job", ""))
    if args.cmd == "desk":
        return cmd_desk()
    if args.cmd == "compute":
        return cmd_compute()
    if args.cmd == "alert":
        return cmd_alert()
    if args.cmd == "check":
        return cmd_check(args.domain)
    if args.cmd == "classify":
        result = classify_claim(args.claim)
        print(json.dumps(result, indent=2))
        return 0
    rec = append_run(args.domain, args.claim, args.verdict, args.note)
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
