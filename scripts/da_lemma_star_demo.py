#!/usr/bin/env python3
"""Demo: Lemma★ / DA-NS-1 energy-budget packaging in Domain Architect.

Saves artifacts to /opt/cursor/artifacts/da-lemma-star/
Honesty: Lemma★ is HYPOTHESIS — broken at PRODUCT-BLOCK; refuse PROVED claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain_architect.lemma_star import (
    analyze_lemma_star,
    compare_lemma_star_shapes,
    express_lemma_star_as_proved,
    insert_product_block_candidate,
    navigate_lemma_star,
    product_block_incompleteness,
    refuse_proved_lemma_star,
    screen_lemma_star,
)
from domain_architect.theory_splicer import express, screen

ARTIFACT_DIR = Path("/opt/cursor/artifacts/da-lemma-star")


def _save(name: str, payload: dict) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACT_DIR / name
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return path


def main() -> int:
    summary: dict = {
        "title": "Domain Architect — Lemma★ / DA-NS-1 Demo",
        "honesty": (
            "Lemma★ packages Clay B correctly in this framing. "
            "Status HYPOTHESIS. Broken at PRODUCT-BLOCK. "
            "DA will not green as PROVED."
        ),
        "steps": [],
        "errors": [],
    }

    # 1. Analyze Lemma★
    analysis = analyze_lemma_star()
    summary["steps"].append({"op": "ANALYZE", "result": analysis.to_dict()})
    _save("01-analyze-lemma-star.json", analysis.to_dict())
    if analysis.status != "HYPOTHESIS":
        summary["errors"].append("expected status HYPOTHESIS")
    if analysis.blocker != "PRODUCT-BLOCK":
        summary["errors"].append("expected blocker PRODUCT-BLOCK")

    # 2. Screen Lemma★ welds
    lemma_screen = screen_lemma_star()
    summary["steps"].append({"op": "SCREEN_LEMMA_STAR", "result": lemma_screen})
    _save("02-screen-lemma-star.json", lemma_screen)

    ns_screen = screen("NS")
    summary["steps"].append({"op": "SCREEN_NS", "result": ns_screen.to_dict()})
    _save("03-screen-ns.json", ns_screen.to_dict())

    # 3. Shape-compare vs SND-C and NS-B
    shapes = compare_lemma_star_shapes()
    summary["steps"].append({"op": "SHAPE_COMPARE", "result": shapes})
    _save("04-shape-compare.json", shapes)

    # 4. PRODUCT-BLOCK incompleteness
    block = product_block_incompleteness()
    summary["steps"].append({"op": "PRODUCT_BLOCK", "result": block})
    _save("05-product-block.json", block)

    # 5. INSERT PRODUCT-BLOCK candidate
    insert_res = insert_product_block_candidate()
    summary["steps"].append({"op": "INSERT_PRODUCT_BLOCK", "result": insert_res.to_dict()})
    _save("06-insert-product-block.json", insert_res.to_dict())

    # 6. Attempt EXPRESS as proved → refuse
    proved = express_lemma_star_as_proved()
    summary["steps"].append({"op": "EXPRESS_AS_PROVED", "result": proved})
    _save("07-express-as-proved-refused.json", proved)
    if not proved.get("refused_proved"):
        summary["errors"].append("expected EXPRESS-as-proved to refuse")

    express_direct = express("DA-NS-1")
    summary["steps"].append({"op": "EXPRESS_DA-NS-1", "result": express_direct.to_dict()})
    _save("08-express-da-ns-1.json", express_direct.to_dict())
    if express_direct.success:
        summary["errors"].append("EXPRESS DA-NS-1 must not succeed/green")

    refuse = refuse_proved_lemma_star(
        "Lemma★ proved; closes Clay Statement B / global regularity"
    )
    summary["steps"].append({"op": "REFUSE_PROVED", "result": refuse})
    _save("09-refuse-proved.json", refuse)

    # 7. Navigate
    nav = navigate_lemma_star()
    summary["steps"].append({"op": "NAVIGATE", "result": nav})
    _save("10-navigate-da-ns-1.json", nav)

    summary["ok"] = not summary["errors"]
    _save("00-summary.json", summary)

    # Human-readable report
    report_lines = [
        summary["title"],
        "=" * 60,
        summary["honesty"],
        "",
        analysis.narrative(),
        "",
        lemma_screen["statement"],
        "",
        block["headline"],
        f"  need: {block['need']}",
        f"  ordinary 3D: {block['ordinary_3d']}",
        "",
        "Top attack routes:",
    ]
    for route in block["attack_routes"][:2]:
        report_lines.append(f"  {route['rank']}. {route['title']}: {route['move']}")
    report_lines.extend(
        [
            "",
            f"EXPRESS as proved refused: {proved['refused_proved']}",
            f"EXPRESS DA-NS-1 success={express_direct.success}",
            f"demo ok: {summary['ok']}",
        ]
    )
    report_text = "\n".join(report_lines) + "\n"
    (ARTIFACT_DIR / "README.txt").write_text(report_text)
    print(report_text)

    if summary["errors"]:
        print("ERRORS:", summary["errors"], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
