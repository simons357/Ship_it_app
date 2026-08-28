"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .gap_closure import (
    diagnose_gap,
    ranked_top_closures,
    snd_c_vs_snd_u_compare,
)
from .hb_loop import compare_reports
from .incompleteness import sketch_from_roles
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION
from .sfe_compare import compare_sfe_pair, list_sfe_candidates
from .snd_claims import anatomize_claim
from .theory_splicer import (
    cut,
    express,
    insert,
    list_millennium_problems,
    screen,
    splice,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=PRODUCT_DESCRIPTION,
    )
    parser.add_argument(
        "expression",
        nargs="?",
        help="equation or term to audit",
    )
    parser.add_argument(
        "expression_b",
        nargs="?",
        help="optional second equation for --compare / --sfe-compare",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--registry",
        action="store_true",
        help="print equation provenance and conflict summary",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="side-by-side HB map compare of two expressions",
    )
    parser.add_argument(
        "--sfe-compare",
        action="store_true",
        help=(
            "put SFE in twice: audit two registry ids (e.g. SFE-H001 SFE-H002) "
            "or two expressions; show conflict/compare; SFE stays unresolved"
        ),
    )
    parser.add_argument(
        "--list-sfe",
        action="store_true",
        help="list historical SFE registry candidates",
    )
    parser.add_argument(
        "--tuning-json",
        action="store_true",
        help="emit only the auto tuning/control-variable export as JSON",
    )
    parser.add_argument(
        "--incompleteness-json",
        action="store_true",
        help="emit only the incompleteness / candidate-completion report as JSON",
    )
    parser.add_argument(
        "--decompose-json",
        action="store_true",
        help="emit only the recursive drill-down / recompose tree as JSON",
    )
    parser.add_argument(
        "--roles-sketch",
        action="store_true",
        help=(
            "roles-in → candidate equation sketch; pass comma-separated roles "
            "as the expression argument (e.g. 'admissibility,interaction,state')"
        ),
    )
    parser.add_argument(
        "--gap-closure",
        action="store_true",
        help=(
            "diagnose NS/SND/Theorem-H broken welds and print "
            "'Broken weld: … Suggested closure: …' (refuses unconditional Clay glue)"
        ),
    )
    parser.add_argument(
        "--snd-dual",
        action="store_true",
        help="dual compare SND-C (X≤M) vs SND-U (claimed unconditional); marks INCOMPATIBLE",
    )
    parser.add_argument(
        "--list-closures",
        action="store_true",
        help="list ranked top closure moves for Theorem-H / SND gaps",
    )
    parser.add_argument(
        "--snd-claim",
        action="store_true",
        help="anatomize SND/Clay claim language via inventory (refuse overclaims)",
    )
    parser.add_argument(
        "--list-millennium",
        action="store_true",
        help="list Clay Millennium problems and honest status (not proved)",
    )
    parser.add_argument(
        "--splice-screen",
        metavar="MILLENNIUM_ID",
        help="screen all welds in a millennium problem book (NS, RH, …)",
    )
    parser.add_argument(
        "--splice-cut",
        nargs=2,
        metavar=("BOOK", "CLAIM_ID"),
        help="CUT — remove a claim from a theory book",
    )
    parser.add_argument(
        "--splice-insert",
        nargs=3,
        metavar=("BOOK", "ROLE", "CANDIDATE"),
        help="INSERT — add candidate completion at incompleteness gap",
    )
    parser.add_argument(
        "--splice-join",
        nargs=2,
        metavar=("BOOK_A", "BOOK_B"),
        help="SPLICE — attempt to join two books (refuse if incompatible)",
    )
    parser.add_argument(
        "--theory-express",
        metavar="BOOK",
        help="EXPRESS — reconstruct book from roles and check closure",
    )
    args = parser.parse_args(argv)

    if args.list_millennium:
        items = list_millennium_problems()
        if args.json:
            json.dump({"millennium_problems": items}, sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print("Millennium problems (honest status — DA does not prove these):")
            for item in items:
                print(
                    f"  {item['id']}: {item['clay_name']} — {item['status']}"
                )
                print(f"    {item['honest_note']}")
                print(f"    books: {', '.join(item['books'])}")
        return 0

    if args.splice_screen:
        report = screen(args.splice_screen)
        if args.json:
            json.dump(report.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(f"Theory splicer — SCREEN {report.millennium_id}")
            print(report.statement)
            print(f"bullshit_destroyed: {report.bullshit_destroyed}")
            for w in report.welds:
                print(
                    f"  [{w.get('screen_verdict', '?')}] {w['weld_id']}: "
                    f"{w['relation']} — {w['evidence'][:80]}"
                )
        return 2 if report.bullshit_destroyed else 0

    if args.splice_cut:
        book, claim = args.splice_cut
        result = cut(book, claim)
        if args.json:
            json.dump(result.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(f"{result.operation}: success={result.success}")
            print(f"  bullshit_destroyed={result.bullshit_destroyed}")
            print(f"  {result.message}")
            if result.bullshit_flags:
                for f in result.bullshit_flags:
                    print(f"  flag: {f}")
            if result.suggested_fix:
                print(f"  fix: {result.suggested_fix}")
        return 0 if result.success else 2

    if args.splice_insert:
        book, role, candidate = args.splice_insert
        result = insert(book, role, candidate)
        if args.json:
            json.dump(result.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(f"{result.operation}: success={result.success}")
            print(f"  bullshit_destroyed={result.bullshit_destroyed}")
            print(f"  {result.message}")
            if result.suggested_fix:
                print(f"  fix: {result.suggested_fix}")
        return 0 if result.success else 2

    if args.splice_join:
        book_a, book_b = args.splice_join
        result = splice(book_a, book_b)
        if args.json:
            json.dump(result.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(f"{result.operation}: success={result.success}")
            print(f"  weld_id={result.weld_id}")
            print(f"  bullshit_destroyed={result.bullshit_destroyed}")
            print(f"  {result.message}")
            if result.bullshit_flags:
                for f in result.bullshit_flags:
                    print(f"  flag: {f}")
            if result.suggested_fix:
                print(f"  fix: {result.suggested_fix}")
        return 0 if result.success else 2

    if args.theory_express:
        result = express(args.theory_express)
        if args.json:
            json.dump(result.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(f"{result.operation}: success={result.success}")
            print(f"  bullshit_destroyed={result.bullshit_destroyed}")
            print(f"  {result.message}")
            if result.bullshit_flags:
                for f in result.bullshit_flags:
                    print(f"  flag: {f}")
            if result.suggested_fix:
                print(f"  fix: {result.suggested_fix}")
        return 0 if result.success else 2

    if args.snd_claim:
        if not args.expression:
            parser.error("--snd-claim requires a claim string")
        audit = anatomize_claim(args.expression)
        if args.json:
            json.dump(audit.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print("SND / Clay claim anatomizer")
            print(f"  refused: {audit.refused}")
            print(f"  allowed_routing: {audit.allowed_routing}")
            for reason in audit.refusal_reasons:
                print(f"  {reason}")
            for hit in audit.hits:
                print(
                    f"  hit {hit.claim_id}: status={hit.status} "
                    f"({hit.status_detail}) markers={hit.matched_markers}"
                )
            for note in audit.notes:
                print(f"  note: {note}")
        return 2 if audit.refused else 0

    if args.list_closures:
        moves = ranked_top_closures(5)
        payload = {
            "canonical_sfe_status": CANONICAL_SFE_STATUS,
            "closures": [m.to_dict() for m in moves],
        }
        if args.json:
            json.dump(payload, sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print("Ranked closure moves (tractable first):")
            for m in moves:
                print(f"  {m.tractability_rank}. [{m.kind}] {m.headline()}")
                print(f"     Patch: {m.patch_sketch}")
        return 0

    if args.snd_dual:
        dual = snd_c_vs_snd_u_compare()
        if args.json:
            json.dump(dual, sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(dual["narrative"])
            print()
            print(f"Relation: {dual['relation']}")
            print(f"Why: {dual['why_incompatible']}")
            print(f"Suggested closure: {dual['suggested_closure']}")
            print()
            right = dual["right"]
            print(
                f"SND-U refuses unconditional Clay: "
                f"{right.get('refuses_unconditional_clay')}"
            )
            for f in right.get("findings") or []:
                print(f"  {f.get('narrative')}")
        return 0

    if args.gap_closure:
        if not args.expression:
            parser.error("--gap-closure requires an expression / claim string")
        gap = diagnose_gap(args.expression)
        if args.json or args.incompleteness_json:
            json.dump(gap.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(gap.narrative())
        # Non-zero exit when refusing Clay glue — forces honest CI routing.
        return 2 if gap.refuses_unconditional_clay else 0

    if args.list_sfe:
        items = list_sfe_candidates()
        if args.json:
            json.dump({"canonical_sfe_status": CANONICAL_SFE_STATUS, "sfe": items}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
            print(f"Historical SFE candidates: {len(items)}")
            for item in items:
                print(
                    f"  {item['equation_id']} [{item['disposition']}] "
                    f"{item['expression'][:72]}"
                )
        return 0

    if args.registry:
        registry = EquationRegistry.load_default()
        payload = registry.export()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"Canonical SFE status: {payload['canonical_sfe_status']}")
            print(f"Historical equations: {len(payload['equations'])}")
            print(f"Conflicts: {len(payload['conflicts'])}")
            print(f"Null / counterexample records: {len(payload['nulls'])}")
            for eq in payload["equations"]:
                print(
                    f"  {eq['equation_id']} [{eq['audit_disposition']}] "
                    f"{eq['original_expression']}"
                )
        return 0

    if args.roles_sketch:
        if not args.expression:
            parser.error("--roles-sketch requires a comma-separated role list")
        roles = [r.strip() for r in args.expression.split(",") if r.strip()]
        book = args.expression_b  # optional book override as 2nd positional
        inc = sketch_from_roles(roles, book=book)
        if args.json or args.incompleteness_json:
            json.dump(inc.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(inc.narrative())
        return 0

    if args.sfe_compare:
        if not args.expression or not args.expression_b:
            parser.error("--sfe-compare requires two registry ids or expressions")
        dual = compare_sfe_pair(args.expression, args.expression_b)
        if args.json:
            json.dump(dual.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(dual.narrative())
        return 0

    if args.compare:
        if not args.expression or not args.expression_b:
            parser.error("--compare requires two expressions")
        left = audit_expression(args.expression)
        right = audit_expression(args.expression_b)
        cmp = compare_reports(left, right)
        if args.json:
            json.dump(
                {
                    "compare": cmp.to_dict(),
                    "left_audit": left.to_dict(),
                    "right_audit": right.to_dict(),
                },
                sys.stdout,
                indent=2,
                default=str,
            )
            sys.stdout.write("\n")
        else:
            print(cmp.narrative())
            print()
            print("--- left reconstruction ---")
            print(left.reconstruction)
            print("--- right reconstruction ---")
            print(right.reconstruction)
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if not args.expression:
        parser.error("expression is required unless --registry / --list-sfe is set")

    report = audit_expression(args.expression)
    if args.tuning_json:
        json.dump(report.tuning_export or {}, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    if args.incompleteness_json:
        json.dump(report.incompleteness or {}, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    if args.decompose_json:
        json.dump(report.decomposition or {}, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    if args.json:
        json.dump(report.to_dict(), sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(report.narrative())
        print()
        print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
