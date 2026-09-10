#!/usr/bin/env python3
"""Shape–Texture navigation demo: NS then RH through the library.

Saves artifacts to /opt/cursor/artifacts/da-shape-texture/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running as script from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain_architect.library_index import inventory_summary, scan_library
from domain_architect.shape_texture import (
    extract_shape,
    extract_texture,
    navigate_millennium,
    shape_match,
    texture_translate,
)
from domain_architect.theory_splicer import cut, screen, splice

ARTIFACT_DIR = Path("/opt/cursor/artifacts/da-shape-texture")


def _save(name: str, payload: dict) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACT_DIR / name
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return path


def run_library_scan() -> dict:
    manifest = scan_library(write_manifest=True)
    _save("00-library-manifest-summary.json", {
        "summary": inventory_summary(manifest),
        "object_count": manifest.get("object_count"),
        "keep_count": manifest.get("keep_count"),
        "millennium_coverage": manifest.get("millennium_coverage"),
        "coverage_gaps": manifest.get("coverage_gaps"),
    })
    return manifest


def run_ns_navigation(manifest: dict) -> dict:
    results: dict = {"section": "NS", "steps": []}

    # Shape extracts from key NS books
    for book in ("NS-B", "SND-C", "BOOT-M", "SND-U"):
        shape = extract_shape(book)
        texture = extract_texture(book)
        results["steps"].append({
            "book": book,
            "shape_id": shape.shape_id,
            "fingers": shape.fingers,
            "texture": texture.to_dict(),
        })
    _save("01-ns-shape-textures.json", results)

    # J/X vs lambda_min/lambda_max conflation (tweet texture mismatch)
    jx = "inf_t J(t)/X(t) >= c_* > 0"
    bypass = (
        "inf_{t>=0} lambda_min(tilde_H_N[u(t)]) / lambda_max(tilde_H_N[u(t)]) > -1/2"
    )
    match = shape_match(jx, bypass)
    translation = texture_translate(jx, bypass)
    conflation = {
        "match": match.to_dict(),
        "translation": translation.to_dict(),
        "note": "Tweet conflation: J/X SND-U texture vs shell-helical lambda ratio.",
    }
    results["steps"].append({"op": "TEXTURE_MISMATCH", "result": conflation})
    _save("02-ns-jx-vs-lambda-texture.json", conflation)

    # Navigate NS through library
    nav = navigate_millennium("NS", manifest=manifest.get("objects"))
    results["navigation"] = nav.to_dict()
    _save("03-ns-navigation.json", nav.to_dict())

    # Theory splicer integration: screen + cut + splice
    screen_report = screen("NS")
    cut_result = cut("SND-C", "THM-D-CLAY")
    boot_sndc = splice("BOOT-M", "SND-C")
    results["splicer"] = {
        "screen": screen_report.to_dict(),
        "cut_thm_d": cut_result.to_dict(),
        "splice_boot_sndc": boot_sndc.to_dict(),
    }
    _save("04-ns-splicer-integration.json", results["splicer"])

    # Shape compare SND-C vs BOOT-M (compatible distinct)
    snd_boot = shape_match("SND-C", "BOOT-M")
    results["snd_boot_match"] = snd_boot.to_dict()
    _save("05-ns-sndc-boot-shape-match.json", snd_boot.to_dict())

    results["jx_lambda_conflation"] = conflation
    return results


def run_rh_navigation(manifest: dict) -> dict:
    results: dict = {"section": "RH", "steps": []}

    for book in ("Q6", "RH-ROUTE-C", "RH-MD"):
        shape = extract_shape(book)
        texture = extract_texture(book)
        results["steps"].append({
            "book": book,
            "shape_id": shape.shape_id,
            "fingers": shape.fingers,
            "texture": texture.to_dict(),
        })
    _save("06-rh-shape-textures.json", results)

    nav = navigate_millennium("RH", manifest=manifest.get("objects"))
    results["navigation"] = nav.to_dict()
    _save("07-rh-navigation.json", nav.to_dict())

    q6_rh = shape_match("Q6", "RH-ROUTE-C")
    q6_ns = shape_match("Q6", "NS-B")
    results["comparisons"] = {
        "Q6_vs_RH": q6_rh.to_dict(),
        "Q6_vs_NS": q6_ns.to_dict(),
    }
    _save("08-rh-shape-comparisons.json", results["comparisons"])

    rh_screen = screen("RH")
    q6_splice = splice("Q6", "RH-ROUTE-C")
    results["splicer"] = {
        "screen": rh_screen.to_dict(),
        "q6_rh_splice": q6_splice.to_dict(),
    }
    _save("09-rh-splicer-integration.json", results["splicer"])

    return results


def main() -> int:
    print("Domain Architect — Shape–Texture Navigation Demo")
    print("=" * 55)
    print("The object is there (shape); textures are coordinate charts.")
    print("DA navigates the library — does NOT prove Millennium problems.")
    print()

    manifest = run_library_scan()
    print(inventory_summary(manifest))
    print()

    ns = run_ns_navigation(manifest)
    nav_ns = ns["navigation"]
    print(f"NS: {nav_ns['statement']}")
    print(f"  matching objects: {len(nav_ns.get('matching_objects', []))}")
    print(f"  texture mismatches: {len(nav_ns.get('texture_mismatches', []))}")
    print()

    rh = run_rh_navigation(manifest)
    nav_rh = rh["navigation"]
    print(f"RH: {nav_rh['statement']}")
    print(f"  matching objects: {len(nav_rh.get('matching_objects', []))}")
    print()

    conflation = ns.get("jx_lambda_conflation", {})
    verdict = (conflation.get("match") or {}).get("verdict", "")
    print(f"J/X vs lambda_min/lambda_max: {verdict}")
    print()

    summary = {
        "title": "DA Shape–Texture Navigation Demo",
        "manifest": inventory_summary(manifest),
        "ns_navigation": nav_ns.get("statement"),
        "rh_navigation": nav_rh.get("statement"),
        "artifact_dir": str(ARTIFACT_DIR),
    }
    _save("10-summary.json", summary)
    print(f"Artifacts saved to {ARTIFACT_DIR}")

    ok = manifest.get("object_count", 0) > 0
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
