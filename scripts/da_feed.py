#!/usr/bin/env python3
"""
Live experimental feed.

Ongoing scan of public test results: LIGO/Virgo/KAGRA,
LHC / INSPIRE, PDG, and the arXiv streams that already
touch this desk. A fetch miss is open, not a desk fail.
A new event does not write X and does not write F.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


UA = "Ship_it_app-DA-feed/0.1 (research notebook)"

ARXIV_QUERY = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:hep-ex+OR+cat:gr-qc+OR+cat:astro-ph.CO+OR+cat:math.AP"
    "&start=0&max_results=20&sortBy=submittedDate&sortOrder=descending"
)

ARXIV_CAT = {
    "arXiv_hep_ex": "hep-ex",
    "arXiv_gr_qc": "gr-qc",
    "arXiv_astro_ph_CO": "astro-ph.CO",
    "arXiv_math_AP": "math.AP",
}


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


SOURCES = [
    {
        "id": "S1",
        "name": "GWOSC_GWTC",
        "slot": "U",
        "kind": "catalog",
        "what": "LIGO–Virgo–KAGRA confirmed events",
        "url": "https://gwosc.org/eventapi/json/GWTC/",
        "can_kill": "a claim that compact binaries are not seen",
        "cannot": "Track B; inverse-GCD; F; nodes.json",
    },
    {
        "id": "S2",
        "name": "INSPIRE_LHC",
        "slot": "U",
        "kind": "catalog",
        "what": "latest ATLAS / CMS / LHCb literature",
        "url": (
            "https://inspirehep.net/api/literature"
            "?sort=mostrecent&size=5"
            "&q=collaboration:ATLAS%20or%20collaboration:CMS"
            "%20or%20collaboration:LHCb"
        ),
        "can_kill": "a poster number that the papers move",
        "cannot": "why those numbers; write F",
    },
    {
        "id": "S3",
        "name": "arXiv_hep_ex",
        "slot": "U",
        "kind": "preprint",
        "what": "accelerator / collider experimental preprints",
        "url": ARXIV_QUERY,
        "can_kill": "a stale experimental abstract",
        "cannot": "write F; close X",
    },
    {
        "id": "S4",
        "name": "arXiv_gr_qc",
        "slot": "U",
        "kind": "preprint",
        "what": "gravitational-wave and strong-field GR preprints",
        "url": ARXIV_QUERY,
        "can_kill": "a stale GW abstract",
        "cannot": "import strain into the tube",
    },
    {
        "id": "S5",
        "name": "arXiv_astro_ph_CO",
        "slot": "U",
        "kind": "preprint",
        "what": "cosmology / large-scale structure preprints",
        "url": ARXIV_QUERY,
        "can_kill": "a cosmology number outside the current tension box",
        "cannot": "write F; Cosmo 16 as a derivation",
    },
    {
        "id": "S6",
        "name": "arXiv_math_AP",
        "slot": "B",
        "kind": "preprint",
        "what": "analysis of PDEs / fluids preprints",
        "url": ARXIV_QUERY,
        "can_kill": "a B lemma whose identity fails on a named field",
        "cannot": "close domain B by announcement",
    },
    {
        "id": "S7",
        "name": "PDG",
        "slot": "U",
        "kind": "catalog",
        "what": "Review of Particle Physics landing page",
        "url": "https://pdg.lbl.gov/",
        "can_kill": "a poster number that drifts outside PDG error",
        "cannot": "why those numbers",
    },
]


STALE_AFTER_HOURS = 24
DEFAULT_FEED = Path(__file__).resolve().parents[1] / "results" / "da_feed.json"


def freshness(path: Path | None = None, now: datetime | None = None) -> dict:
    """Last scan age. No network. Missing or older than a day is stale."""
    dest = Path(path) if path is not None else DEFAULT_FEED
    clock = now or datetime.now(timezone.utc)
    out = {
        "path": str(dest),
        "exists": dest.is_file(),
        "fetched_at": None,
        "age_hours": None,
        "stale": True,
        "reason": "missing",
        "stale_after_hours": STALE_AFTER_HOURS,
        "network": False,
    }
    if not dest.is_file():
        return out
    try:
        data = json.loads(dest.read_text())
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        out["reason"] = "unreadable"
        return out
    meta = data.get("meta") if isinstance(data, dict) else None
    fetched = meta.get("fetched_at") if isinstance(meta, dict) else None
    if not fetched:
        out["reason"] = "no_timestamp"
        return out
    out["fetched_at"] = fetched
    try:
        ts = datetime.strptime(str(fetched), "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except (TypeError, ValueError):
        out["reason"] = "bad_timestamp"
        return out
    age = (clock - ts).total_seconds() / 3600.0
    out["age_hours"] = round(age, 3)
    if age < -1:
        out["reason"] = "future_timestamp"
        return out
    if age > STALE_AFTER_HOURS:
        out["reason"] = "older_than_24h"
        return out
    out["stale"] = False
    out["reason"] = "fresh"
    return out


def format_freshness(row: dict | None = None) -> str:
    fr = row if row is not None else freshness()
    stamp = fr.get("fetched_at") or "none"
    age = fr.get("age_hours")
    age_s = "none" if age is None else f"{age:.1f}h"
    flag = "STALE" if fr.get("stale") else "fresh"
    return f"feed {flag} ({fr.get('reason')}). last {stamp} age {age_s}"


CLAIMS = [
    rec(
        "F1",
        "feed_belongs",
        "An ongoing scan of public test results belongs on the desk",
        "pass",
        "LIGO, LHC, PDG, and arXiv already sit as pipes. A refresh command is the collection.",
    ),
    rec(
        "F2",
        "feed_is_omniscience",
        "The feed ingests all hard science as a constant stream",
        "fail",
        "Typed sources, a dated scan, optional live hits. Not omniscience.",
    ),
    rec(
        "F3",
        "ligo_closes_X",
        "A new LIGO event closes classical X",
        "fail",
        "Strain on interferometers is not 1/r^4 on T^3.",
    ),
    rec(
        "F4",
        "lhc_writes_F",
        "A new LHC paper writes F",
        "fail",
        "A catalog update refreshes consumed numbers. Produce still fails.",
    ),
    rec(
        "F5",
        "feed_is_leftover_B42",
        "The feed writes leftover-close B42",
        "fail",
        "Do not write leftover B42. A preprint is a proposal.",
    ),
    rec(
        "F6",
        "fetch_miss_is_desk_fail",
        "A fetch miss is a desk fail",
        "fail",
        "Network miss stays open. The source list still sits.",
    ),
    rec(
        "F7",
        "feed_retunes_nodes",
        "A GW or collider headline retunes nodes.json",
        "fail",
        "HB Experiment 01 is closed. Do not retune.",
    ),
    rec(
        "F8",
        "items_stay_in_slot",
        "Each scanned item stays in its slot",
        "pass",
        "GW and LHC on U. math.AP on B. LMFDB stays Q. Glue refused.",
    ),
    rec(
        "F9",
        "must_stay_current",
        "DA must stay current with the latest public data",
        "pass",
        "What the architect does is score against catalogs that move. A stale desk is a weaker device.",
    ),
    rec(
        "F10",
        "stale_is_weaker",
        "A missing or >24h feed is stale; stale DA is weaker",
        "pass",
        "status reports last-scan age. Re-run feed. Age is local.",
    ),
    rec(
        "F11",
        "status_hits_network",
        "status fetches the live catalogs",
        "fail",
        "status reads results/da_feed.json. No network on the check. feed is the fetch.",
    ),
]


def _http(url: str, timeout: float) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        ctype = resp.headers.get("Content-Type", "")
        return resp.read(), ctype


def _arxiv_items(raw: bytes, limit: int = 20) -> list[dict]:
    import xml.etree.ElementTree as ET

    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(raw)
    items = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
        title = " ".join(title.split())
        updated = (entry.findtext("a:updated", default="", namespaces=ns) or "")[:10]
        link = ""
        for el in entry.findall("a:link", ns):
            if el.get("type") == "text/html" or el.get("rel") == "alternate":
                link = el.get("href") or ""
                break
        cats = [el.get("term") or "" for el in entry.findall("a:category", ns)]
        items.append({"title": title, "date": updated, "url": link, "cats": cats})
        if len(items) >= limit:
            break
    return items


def _load_arxiv(timeout: float) -> tuple[list[dict] | None, str | None]:
    try:
        raw, _ = _http(ARXIV_QUERY, timeout=timeout)
        return _arxiv_items(raw), None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, Exception) as exc:
        return None, str(exc)


def fetch_source(
    src: dict,
    timeout: float = 8.0,
    arxiv: tuple[list[dict] | None, str | None] | None = None,
) -> dict:
    out = {
        "id": src["id"],
        "name": src["name"],
        "slot": src["slot"],
        "kind": src["kind"],
        "what": src["what"],
        "url": src["url"],
        "can_kill": src["can_kill"],
        "cannot": src["cannot"],
        "ok": False,
        "n": 0,
        "items": [],
        "error": None,
    }
    try:
        name = src["name"]
        if name.startswith("arXiv_"):
            raw, ctype = b"", ""
        else:
            raw, ctype = _http(src["url"], timeout=timeout)
        if name == "GWOSC_GWTC":
            data = json.loads(raw.decode("utf-8", errors="replace"))
            events = data.get("events") or {}
            rows = []
            for key, ev in events.items():
                if not isinstance(ev, dict):
                    continue
                rows.append(
                    {
                        "title": ev.get("commonName") or key,
                        "date": str(ev.get("GPS") or ""),
                        "url": ev.get("jsonurl") or ev.get("reference") or "",
                        "catalog": ev.get("catalog.shortName") or "",
                    }
                )
            rows.sort(key=lambda r: float(r["date"] or 0), reverse=True)
            out["items"] = rows[:5]
            out["ok"] = True
            out["n"] = len(out["items"])
            out["catalog_n"] = len(events)
        elif name == "INSPIRE_LHC":
            data = json.loads(raw.decode("utf-8", errors="replace"))
            hits = data.get("hits", {}).get("hits") or []
            items = []
            for hit in hits[:5]:
                meta = hit.get("metadata") or {}
                titles = meta.get("titles") or []
                title = titles[0].get("title") if titles else hit.get("id", "")
                date = meta.get("earliest_date") or ""
                rec_id = hit.get("id")
                url = f"https://inspirehep.net/literature/{rec_id}" if rec_id else ""
                items.append({"title": title, "date": date, "url": url})
            out["items"] = items
            out["ok"] = True
            out["n"] = len(items)
        elif name.startswith("arXiv_"):
            bundle, err = arxiv if arxiv is not None else _load_arxiv(timeout)
            if err:
                out["error"] = err
            else:
                want = ARXIV_CAT.get(name, "")
                picked = [item for item in (bundle or []) if want in (item.get("cats") or [])]
                out["items"] = picked[:5]
                out["ok"] = True
                out["n"] = len(out["items"])
            return out
        elif name == "PDG":
            out["ok"] = True
            out["n"] = 1
            out["items"] = [
                {
                    "title": "PDG landing page reachable",
                    "date": "",
                    "url": src["url"],
                    "content_type": ctype.split(";")[0],
                }
            ]
        else:
            out["error"] = "unknown source parser"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError, ValueError) as exc:
        out["error"] = str(exc)
    return out


def scan(timeout: float = 8.0) -> list[dict]:
    bundle = _load_arxiv(timeout)
    return [fetch_source(src, timeout=timeout, arxiv=bundle) for src in SOURCES]


def run(out: Path | None = None, fetch: bool = True, timeout: float = 8.0) -> dict:
    scanned = scan(timeout=timeout) if fetch else []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "meta": {
            "question": "scan latest public test results; keep each item in its slot",
            "writeup": "docs/DA-FEED.md",
            "wrote_at": now,
            "fetched_at": now if fetch else None,
            "fetched": fetch,
            "ongoing": True,
            "not_omniscience": True,
            "must_stay_current": True,
            "does_not_write_X": True,
            "does_not_write_F": True,
            "does_not_retune_nodes": True,
            "fetch_miss_is_open": True,
        },
        "sources": SOURCES,
        "scan": scanned,
        "claims": CLAIMS,
        "counts": {
            "sources": len(SOURCES),
            "scanned": len(scanned),
            "ok": sum(1 for s in scanned if s.get("ok")),
            "items": sum(int(s.get("n") or 0) for s in scanned),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "how_far": [
            "LIGO GWTC, LHC INSPIRE, PDG, hep-ex, gr-qc, astro-ph.CO, math.AP named",
            "re-run is the collection",
            "glue of strain or collisions onto X refused",
            "fetch miss is not a desk fail",
        ],
        "next_da_move": (
            "Re-run feed. Score a math.AP item only if it keeps 1/r^4 and names a check. "
            "Do not write leftover B42. Do not spawn n=64."
        ),
    }
    dest = Path(out) if out is not None else DEFAULT_FEED
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    payload["freshness"] = freshness(path=dest)
    return payload


def main() -> int:
    payload = run()
    print("DA feed. Public test results. Not omniscience. Not a close.")
    print("Full note: docs/DA-FEED.md")
    print(format_freshness(payload.get("freshness")))
    print("fetched", payload["meta"].get("fetched_at") or "none")
    for src in payload["scan"]:
        flag = "ok" if src.get("ok") else "miss"
        print(f"  [{flag}] {src['name']:<16} {src['slot']} n={src.get('n')}")
        for item in (src.get("items") or [])[:3]:
            title = (item.get("title") or "")[:72]
            print(f"      {item.get('date', '')} {title}")
        if src.get("error"):
            print(f"      error: {src['error']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
