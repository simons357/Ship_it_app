#!/usr/bin/env python3
"""
DA tick: roster + feed inside the machine.

The operator asked whether a living roster and a live
feed make DA an agent. The shape is an agent: propose,
scan, score, alert. Genius is not a slot. Latest data
belongs here. A tick does not write X and does not
replace the checker.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_feed import SOURCES, format_freshness, freshness, run as feed_run  # noqa: E402
from da_now import WATCH, collaborations, seated_living  # noqa: E402


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


CLAIMS = [
    rec(
        "G1",
        "roster_feed_strengthen",
        "Fitting the living roster and the live feed into DA makes the process stronger",
        "pass",
        "A machine that names who sits and refreshes public catalogs is a better anti-bullshit device.",
    ),
    rec(
        "G2",
        "agent_shaped",
        "That shape is an agent: propose, scan, score, alert",
        "pass",
        "Ordinary AI proposes. The feed scans. Scripts score. Alert speaks on a watched flip. The operator still runs the command.",
    ),
    rec(
        "G3",
        "agent_closes_X",
        "The DA agent closes classical X",
        "fail",
        "A tick is not an estimate. Domain B stays open.",
    ),
    rec(
        "G4",
        "agent_writes_F",
        "The DA agent writes F",
        "fail",
        "Latest PDG or LHC numbers refresh inputs. Produce still fails.",
    ),
    rec(
        "G5",
        "agent_replaces_checker",
        "The agent replaces the checker",
        "fail",
        "No chops means the script still verdicts. Autopilot is not a pass.",
    ),
    rec(
        "G6",
        "latest_data_writes_X",
        "Latest LIGO or LHC data writes a bound on X",
        "fail",
        "Up to date is a U duty. Strain and collisions are not 1/r^4.",
    ),
    rec(
        "G7",
        "latest_data_belongs",
        "DA must be able to refresh the latest public data",
        "pass",
        "A process machine that cannot re-read GWTC or LHC is stale. Re-run feed.",
    ),
    rec(
        "G8",
        "cosmo_superagent_sits",
        "Cosmo Superagent sits as this agent",
        "fail",
        "Already refused. This tick is roster plus feed plus score, not a ToE app.",
    ),
    rec(
        "G9",
        "agent_unshelves",
        "The agent unshelves SFE or retunes nodes.json",
        "fail",
        "Architecture is U. The shelf stays.",
    ),
    rec(
        "G10",
        "more_sources_later",
        "More feed sources and watch chairs may be added",
        "open",
        "The collection is ongoing. A name is not a seat until a wall is scored.",
    ),
    rec(
        "G11",
        "status_reports_freshness",
        "status reports last-scan age without a fetch",
        "pass",
        "A process machine that cannot say how old its catalogs are is already stale. Age is local.",
    ),
]


def run(out: Path | None = None, fetch: bool = False) -> dict:
    seated = seated_living()
    feed = feed_run(out=Path(out).parent / "da_feed_tick.json", fetch=fetch) if out else feed_run(fetch=fetch)
    payload = {
        "meta": {
            "question": "fit roster and feed into DA; is that an agent",
            "writeup": "docs/DA-AGENT.md",
            "agent_shaped": True,
            "not_a_closer": True,
            "not_a_unifier": True,
            "does_not_replace_checker": True,
            "latest_data_belongs": True,
            "does_not_write_X": True,
        },
        "tick": {
            "seated_living": seated,
            "watch": [row["name"] for row in WATCH],
            "collaborations": [row["name"] for row in collaborations()],
            "feed_sources": [s["name"] for s in SOURCES],
            "feed_ok": feed["counts"].get("ok", 0),
            "feed_items": feed["counts"].get("items", 0),
            "fetched": fetch,
            "freshness": freshness(),
        },
        "claims": CLAIMS,
        "counts": {
            "seated_living": len(seated),
            "watch": len(WATCH),
            "collaborations": len(collaborations()),
            "feed_sources": len(SOURCES),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "how_far": [
            "now and feed sit inside the DA tick",
            "agent-shaped process passed",
            "agent-as-closer failed",
            "latest data belongs; stale feed is weaker; status reports age",
        ],
        "next_da_move": (
            "Re-run feed. Score one watch paper before seating it. "
            "Do not write leftover B42. Do not spawn n=64. "
            "Track A stays this PDE only."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_agent.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run(fetch=True)
    print("DA agent. Propose, scan, score, alert.")
    print("Full note: docs/DA-AGENT.md")
    tick = payload["tick"]
    print("seated", len(tick["seated_living"]), "watch", len(tick["watch"]))
    print("feed", "ok" if tick["fetched"] else "offline", "items", tick["feed_items"])
    print(format_freshness(tick.get("freshness")))
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
