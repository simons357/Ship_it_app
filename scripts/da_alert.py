#!/usr/bin/env python3
"""
Plain-language alerts when something significant flips.

The operator asked to be told, in words they can use, and
what to do next. A flip on a watched claim is significant.
A new catalog page is not.

The briefing is always written to disk. A phone text needs a
sender you attach (DA_ALERT_WEBHOOK). No phone number in git.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "results" / "da_alert_state.json"
OUT_JSON = ROOT / "results" / "da_alert.json"
OUT_TXT = ROOT / "results" / "DA-ALERT.txt"

# Watched claims only. Catalog churn is not a text.
WATCH = {
    "B.domain": {
        "slot": "B",
        "plain": "The classical fluid equations (the hard ones, no extra damping) as a whole.",
        "on_fail": (
            "A lemma we were using broke. Do not keep building on it.",
            "Open the Track B list, find the row that went fail, and fix or drop that step. Regularity was already open.",
        ),
        "on_pass": (
            "Someone treated the whole classical problem as solved. That is not allowed without a bound on the enstrophy X.",
            "Do not celebrate. Ask: where is the closed estimate for X? If there is none, put the domain back to open.",
        ),
        "on_open": (
            "Classical regularity is still not decided. That is the honest state.",
            "Next write is still the tube estimate, then the low-frequency product term.",
        ),
    },
    "B.B4b_hardy_not_I_tube": {
        "slot": "B",
        "plain": "The hope that Hardy's inequality eats the nasty 1/r^4 source in the vortex tube.",
        "on_fail": (
            "That hope is dead for all data: a slow fat swirl makes the leftover ratio blow like 1/ε.",
            "Keep the packet class (B4c). Next write is the low Bony term on the spread side.",
        ),
        "on_pass": (
            "Hardy now absorbs the tube source in the estimate that was written.",
            "Do not call the fluids problem solved. Next: the low-frequency product term (Bony T), then occupation time.",
        ),
        "on_open": (
            "Still the live tube question. Hardy is the tool. Domination is not shown.",
            "Keep writing Hardy → I_tube at the thin-tube scale. That is the next page.",
        ),
    },
    "B.B5b_tube_vs_viscosity": {
        "slot": "B",
        "plain": "Whether ordinary viscosity beats that 1/r^4 source at the thin tube.",
        "on_fail": (
            "Viscosity does not beat the source in the estimate we have.",
            "Do not cancel to Φ to hide it. Stay with Γ. Look at geometry or a smaller class.",
        ),
        "on_pass": (
            "Viscosity now dominates the tube source in the written estimate.",
            "Still not regularity. Combine with the Hardy step and the low Bony term. Domain B stays open until X is bounded.",
        ),
        "on_open": (
            "Still open. This is why we kept 1/r^4.",
            "After Hardy → I_tube, this is the second live write.",
        ),
    },
    "B.B_regularity": {
        "slot": "B",
        "plain": "Are the classical 3D fluid equations always smooth?",
        "on_fail": (
            "A blowup was proved, or the claim was withdrawn the other way.",
            "If it is a real blowup paper, sit it on B and read the data class. Do not glue to Track A or to primes.",
        ),
        "on_pass": (
            "A closed bound on X was claimed.",
            "Demand the estimate. If it is not there, this is a fake pass — put it back to open.",
        ),
        "on_open": (
            "Still open. Identities are not a continuation argument.",
            "Do not send a victory text. Keep the tube write.",
        ),
    },
    "A.domain": {
        "slot": "A",
        "plain": "The easier fluid equations, the ones with extra damping (ε>0).",
        "on_fail": (
            "The checker for the damped equations broke.",
            "Re-run the energy test. If the residual is bad, the code or the identity needs a look. This is not the classical problem.",
        ),
        "on_pass": (
            "The damped-equation checker is green. That is only Track A.",
            "Leave it on A. It does not buy the classical problem.",
        ),
        "on_open": (
            "Track A is waiting on a check.",
            "Run: python3 scripts/da_machine.py check --domain A",
        ),
    },
    "Q.full_floor": {
        "slot": "Q",
        "plain": "The old claim that a certain prime/GCD matrix always sits above a floor.",
        "on_fail": (
            "Still false, or newly shown false. That slogan is dead.",
            "Stay with Bridge*, Theorem P, and H_N ≥ -1. Do not put the full floor back.",
        ),
        "on_pass": (
            "Someone claimed the full floor is back.",
            "This contradicts known counterexamples unless those died. Do not accept without a proof for all N.",
        ),
        "on_open": (
            "The full floor is not an open hope on this desk. It was already killed.",
            "Ignore. Arithmetic only.",
        ),
    },
    "U.F_exists": {
        "slot": "U",
        "plain": "A public formula that outputs the measured coupling numbers.",
        "on_fail": (
            "Still no producing-map, or a candidate lost holdout.",
            "Do not treat Cosmo 16/16 or a pairing of famous names as the formula. Keep Einstein+T as the couple.",
        ),
        "on_pass": (
            "A public F beat the holdout.",
            "Read the formula. Check χ² on held-out numbers. If that is real, this is the first U collapse — still not Navier–Stokes.",
        ),
        "on_open": (
            "No public F. Collapse has not happened.",
            "Do not wait for a text about Cosmo. The core equation is still private.",
        ),
    },
    "U.destination": {
        "slot": "U",
        "plain": "The idea that nature is a spectrum, not a bag of free numbers.",
        "on_fail": (
            "That program was killed (a no-go), or it was never a pass.",
            "If a no-go was proved, read which operator it rules out. The bag of couplings is still the present tense.",
        ),
        "on_pass": (
            "Someone named an operator whose eigenvalues are those numbers.",
            "Demand the operator. If it is not written, this is a fake pass. If it is written, run the numbers.",
        ),
        "on_open": (
            "Still the destination, not a result.",
            "Climb X → D → spectrum. Do not start at the eigenvalues.",
        ),
    },
}


def _lemma_map() -> dict[str, str]:
    path = ROOT / "results" / "track_b_lemmas.json"
    if not path.exists():
        from track_b_lemmas import run as tb

        tb()
    data = json.loads((ROOT / "results" / "track_b_lemmas.json").read_text())
    out = {f"B.{row['name']}": row["verdict"] for row in data["lemmas"]}
    out["B.domain"] = data["meta"]["domain_verdict"]
    return out


def collect_state() -> dict[str, str]:
    lemmas = _lemma_map()
    state = {
        "B.domain": lemmas.get("B.domain", "open"),
        "B.B4b_hardy_not_I_tube": lemmas.get("B.B4b_hardy_not_I_tube", "open"),
        "B.B5b_tube_vs_viscosity": lemmas.get("B.B5b_tube_vs_viscosity", "open"),
        "B.B_regularity": lemmas.get("B.B_regularity", "open"),
        "A.domain": "pass",
        "Q.full_floor": "fail",
        "U.F_exists": "fail",
        "U.destination": "open",
    }
    return state


def load_prev(path: Path | None = None) -> dict | None:
    p = path or STATE
    if not p.exists():
        return None
    return json.loads(p.read_text())


def save_state(state: dict, path: Path | None = None) -> None:
    p = path or STATE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(
            {"t": datetime.now(timezone.utc).isoformat(), "watch": state},
            indent=2,
        )
    )


def flips(prev: dict[str, str] | None, cur: dict[str, str]) -> list[dict]:
    if prev is None:
        return []
    found = []
    for key, spec in WATCH.items():
        old = prev.get(key)
        new = cur.get(key)
        if old is None or new is None or old == new:
            continue
        tone = f"on_{new}"
        head, nxt = spec.get(tone, ("A watched claim changed.", "Read the slot and do not glue."))
        found.append(
            {
                "key": key,
                "slot": spec["slot"],
                "was": old,
                "now": new,
                "what": spec["plain"],
                "head": head,
                "next": nxt,
            }
        )
    return found


def render_text(events: list[dict], baseline: bool) -> str:
    if baseline:
        return (
            "DA alert is on. Watching the live claims (tube, viscosity, "
            "classical regularity, damped equations, the dead GCD floor, "
            "the missing formula, the spectrum destination).\n"
            "No discovery. This is the baseline.\n"
            "You will get a text-shaped note only if one of those flips.\n"
            "Next: keep the tube write. Do not wait for a victory message.\n"
        )
    if not events:
        return (
            "DA checked. Nothing significant flipped.\n"
            "Next: evolve a CONC packet a short time (B12d). t=0 did not produce the saving climb.\n"
        )
    parts = []
    for e in events:
        sms = f"{e['slot']}: {e['head']}"
        parts.append(
            f"TEXT\n{sms}\n\n"
            f"WHAT IT MEANS\n{e['what']}\n"
            f"It went {e['was']} → {e['now']}.\n\n"
            f"WHAT TO DO\n{e['next']}\n\n"
            f"DO NOT\nTreat this as a theory of everything, or as the other tracks.\n"
        )
    return "\n---\n".join(parts)


def send_webhook(body: dict) -> dict:
    url = os.environ.get("DA_ALERT_WEBHOOK", "").strip()
    if not url:
        return {"attempted": False, "ok": False, "why": "no DA_ALERT_WEBHOOK"}
    if any(s in url.lower() for s in ("example.com", "localhost")):
        return {"attempted": False, "ok": False, "why": "placeholder webhook"}
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "DA-alert/0.1"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            return {"attempted": True, "ok": True, "status": getattr(resp, "status", 200)}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"attempted": True, "ok": False, "why": str(exc)}


def notify(
    source: str = "alert",
    state_path: Path | None = None,
    out_json: Path | None = None,
    out_txt: Path | None = None,
) -> dict:
    state_path = Path(state_path) if state_path is not None else STATE
    out_json = Path(out_json) if out_json is not None else OUT_JSON
    out_txt = Path(out_txt) if out_txt is not None else OUT_TXT
    cur = collect_state()
    prev_wrap = load_prev(state_path)
    prev = None if prev_wrap is None else prev_wrap.get("watch")
    baseline = prev is None
    events = flips(prev, cur)
    significant = bool(events) and not baseline
    text = render_text(events, baseline)
    payload = {
        "meta": {
            "source": source,
            "t": datetime.now(timezone.utc).isoformat(),
            "significant": significant,
            "baseline": baseline,
            "no_phone_in_repo": True,
            "delivery": "write DA-ALERT.txt; POST DA_ALERT_WEBHOOK if set",
        },
        "watch": cur,
        "events": events,
        "plain": text,
        "sms_lines": [f"{e['slot']}: {e['head']}" for e in events],
        "recommendation": (
            events[-1]["next"]
            if events
            else "Nothing flipped. Next write is a short evolution of a CONC packet (B12d)."
        ),
    }
    delivery = {"file": str(out_txt)}
    if significant:
        delivery["webhook"] = send_webhook(
            {
                "significant": True,
                "sms": payload["sms_lines"],
                "plain": text,
                "next": payload["recommendation"],
            }
        )
    else:
        delivery["webhook"] = {"attempted": False, "ok": False, "why": "not significant"}
    payload["delivery"] = delivery

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2))
    out_txt.write_text(text)
    save_state(cur, state_path)
    payload["_wrote"] = str(out_json)
    payload["_text"] = str(out_txt)
    return payload


def run(out: Path | None = None, state_path: Path | None = None) -> dict:
    return notify(source="alert", state_path=state_path, out_json=out)


def main() -> int:
    payload = run()
    print("DA alert. Plain language on a flip. Catalogs do not text you.")
    print("significant:", payload["meta"]["significant"], "baseline:", payload["meta"]["baseline"])
    print(payload["plain"])
    print("next:", payload["recommendation"])
    print(f"wrote {payload['_wrote']} and {payload['_text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
