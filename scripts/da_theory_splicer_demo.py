#!/usr/bin/env python3
"""End-to-end demo: Domain Architect theory splicer on NS then RH.

Saves artifacts to /opt/cursor/artifacts/da-theory-splicer/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running as script from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain_architect.theory_splicer import (
    cut,
    express,
    insert,
    screen,
    splice,
)

ARTIFACT_DIR = Path("/opt/cursor/artifacts/da-theory-splicer")


def _save(name: str, payload: dict) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACT_DIR / name
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return path


def run_ns_demo() -> dict:
    results: dict = {"section": "NS", "steps": []}

    # 1. Screen NS welds
    screen_report = screen("NS")
    results["steps"].append({"op": "SCREEN", "result": screen_report.to_dict()})
    _save("01-ns-screen.json", screen_report.to_dict())

    # 2. Cut Thm D Clay⇔SND
    cut_result = cut("SND-C", "THM-D-CLAY")
    results["steps"].append({"op": "CUT", "result": cut_result.to_dict()})
    _save("02-ns-cut-thm-d.json", cut_result.to_dict())

    # 3. Insert BOOT-M001 candidate
    insert_result = insert(
        "BOOT-M",
        "scale_response",
        "Lemma (Bootstrap-M): M=M(||u0||_{H^1}) with sup X(t)<=M on [0,T*)",
    )
    results["steps"].append({"op": "INSERT", "result": insert_result.to_dict()})
    _save("03-ns-insert-boot-m.json", insert_result.to_dict())

    # 4. Attempt illegal splice SFE→NS (must refuse)
    illegal = splice("SFE", "NS-B")
    results["steps"].append({"op": "SPLICE_ILLEGAL", "result": illegal.to_dict()})
    _save("04-ns-splice-sfe-refused.json", illegal.to_dict())
    if illegal.success:
        results["error"] = "Expected SFE→NS splice to be refused"
    else:
        results["sfe_refused"] = True

    # 5. Allowed splice BOOT-M ↔ SND-C
    allowed = splice("BOOT-M", "SND-C")
    results["steps"].append({"op": "SPLICE_ALLOWED", "result": allowed.to_dict()})
    _save("05-ns-splice-boot-sndc.json", allowed.to_dict())

    # 6. Express honest NS conditional book
    express_sndc = express("SND-C")
    express_nsb = express("NS-B")
    results["steps"].append({"op": "EXPRESS_SND-C", "result": express_sndc.to_dict()})
    results["steps"].append({"op": "EXPRESS_NS-B", "result": express_nsb.to_dict()})
    _save("06-ns-express-sndc.json", express_sndc.to_dict())
    _save("07-ns-express-nsb.json", express_nsb.to_dict())

    return results


def run_rh_demo() -> dict:
    results: dict = {"section": "RH", "steps": []}

    screen_report = screen("RH")
    results["steps"].append({"op": "SCREEN", "result": screen_report.to_dict()})
    _save("08-rh-screen.json", screen_report.to_dict())

    # Q6 vs RH Route C — what splice would require
    q6_rh = splice("Q6", "RH-ROUTE-C")
    results["steps"].append({"op": "SPLICE_Q6_RH", "result": q6_rh.to_dict()})
    _save("09-rh-splice-q6-route-c.json", q6_rh.to_dict())

    q6_ns = splice("Q6", "NS-B")
    results["steps"].append({"op": "SPLICE_Q6_NS_ILLEGAL", "result": q6_ns.to_dict()})
    _save("10-rh-splice-q6-ns-refused.json", q6_ns.to_dict())

    express_q6 = express("Q6")
    results["steps"].append({"op": "EXPRESS_Q6", "result": express_q6.to_dict()})
    _save("11-rh-express-q6.json", express_q6.to_dict())

    return results


def main() -> int:
    summary = {
        "title": "Domain Architect Theory Splicer Demo",
        "honesty": "DA does NOT prove Millennium problems — bullshit destruction only.",
        "ns": run_ns_demo(),
        "rh": run_rh_demo(),
    }
    _save("00-summary.json", summary)

    print("Domain Architect — Theory Splicer Demo")
    print("=" * 50)
    print(summary["honesty"])
    print()

    ns_screen = summary["ns"]["steps"][0]["result"]
    print(f"NS weld screen: {ns_screen['compatible_count']} COMPATIBLE, "
          f"{ns_screen['incompatible_count']} INCOMPATIBLE, "
          f"{ns_screen['open_count']} OPEN")
    print("Top incompatible NS welds:")
    incompatible = [w for w in ns_screen["welds"] if w.get("screen_verdict") == "INCOMPATIBLE"]
    for w in incompatible[:3]:
        print(f"  - {w['weld_id']}: {w['evidence'][:70]}...")
    print()

    rh_splice = summary["rh"]["steps"][1]["result"]
    print(f"RH/Q6 splice: success={rh_splice['success']}")
    print(f"  {rh_splice['message']}")
    if rh_splice.get("suggested_fix"):
        print(f"  requires: {rh_splice['suggested_fix']}")
    print()

    sfe = summary["ns"]["steps"][3]["result"]
    print(f"SFE→NS illegal splice refused: {not sfe['success']} "
          f"(bullshit_destroyed={sfe['bullshit_destroyed']})")
    print()
    print(f"Artifacts saved to {ARTIFACT_DIR}")

    ok = summary["ns"].get("sfe_refused", False) and not sfe["success"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
