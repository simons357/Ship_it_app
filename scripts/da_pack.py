#!/usr/bin/env python3
"""
DA pack: reprint what sits, mark the rest open.

The operator asked to close what can close, then
hand the named leftovers as a PDF. Poincaré sits
(literature). Theorem A sits for this Q1 PDE.
Every other WRITE stays open. This is not prize
packaging and not a QED certificate.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_proof import CLAIMS as PROOF_CLAIMS  # noqa: E402
from da_proof import PROBLEMS, _chain, _status_line  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def rec(
    hid: str,
    name: str,
    statement: str,
    verdict: str,
    why: str,
) -> dict:
    return {
        "id": hid,
        "name": name,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }


CLAIMS = [
    rec(
        "P1",
        "pack_is_status",
        "The PDF pack is the status of each seated chain",
        "pass",
        "Have / write / sits. That is what can be handed over.",
    ),
    rec(
        "P2",
        "pack_closes_leftovers",
        "The PDF pack closes the open WRITE lines",
        "fail",
        "A reprint is not leftover (6). Open stays open.",
    ),
    rec(
        "P3",
        "sfe_hodge_paper",
        "The SFE Hodge note is leftover (6)",
        "fail",
        "SFE is shelved. Coherence is not an algebraic cycle.",
    ),
    rec(
        "P4",
        "prize_packaging",
        "This pack is prize packaging of the named leftovers",
        "fail",
        "Shelf rule. Status is allowed. A committee PDF is not.",
    ),
]


SITS = (
    "Poincaré — Perelman 2002–2003. Literature. This desk reprints.",
    "A this PDE — Theorem A at eps>0, beta>=1/2. Different equation from classical NS.",
)

OPEN = (
    "B / smoothness and existence — WRITE (6) all-data R / A1 / A2 / killing field",
    "A uniform H1 — WRITE (7) as eps->0. This PDE sitting is not that write.",
    "RH — WRITE (6) every zero on Re s = 1/2. Q is not that write.",
    "YM — WRITE (4) mass gap. SM block is not the gap.",
    "BSD — WRITE (6) rank / Sha / leading term. DA did not close this.",
    "Hodge — WRITE (6) every rational Hodge class algebraic. SFE is not that write.",
    "P vs NP — WRITE (5) TM proof. SFE H(x) is not a Turing machine.",
)


def is_pack_ask(ask: str) -> bool:
    """PDF / close-what-sits pack, not a leftover QED."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bpdf\b|pdf form|"
            r"give them to me in like a|"
            r"close out what you can|"
            r"\bda pack\b|\bstatus pack\b",
            text,
        )
    )


def _wrap(text: str, width: int = 86) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines = [words[0]]
    for w in words[1:]:
        if len(lines[-1]) + 1 + len(w) <= width:
            lines[-1] += " " + w
        else:
            lines.append(w)
    return lines


def _paginate(lines: list[str], per_page: int = 52) -> list[list[str]]:
    if not lines:
        return [[]]
    return [lines[i : i + per_page] for i in range(0, len(lines), per_page)]


def _pages() -> list[list[str]]:
    page1 = [
        "DA leftover status pack",
        "5 September 2026",
        "",
        "This is status. It is not QED.",
        "DA reprints what sits. DA does not emit an open WRITE as a close.",
        "Not prize packaging. Not a committee letter.",
        "",
        "SITS",
    ]
    for row in SITS:
        page1.extend("  " + line for line in _wrap(row, 82))
    page1.append("")
    page1.append("OPEN")
    for row in OPEN:
        page1.extend("  " + line for line in _wrap(row, 82))
    page1.extend(
        [
            "",
            "Documented: the operator did not prove BSD. DA did not either.",
            "A certificate that DA closed BSD is the refuse.",
            "SFE does not close Hodge. SFE does not close P vs NP.",
            "Complete-as-written is HAVE / WRITE / THEN. It is not leftover sits.",
            "Naming a WRITE line is not filling it.",
        ]
    )
    page2 = [
        "Seated chains (complete-as-written, not QED)",
        "",
    ]
    for pid in PROBLEMS:
        chain = _chain(pid)
        page2.append(f"{pid}: {_status_line(chain)}")
        page2.extend("  " + line for line in _wrap(chain["theorem"]["aimed"], 82))
        for L in chain["lines"]:
            tag = {"have": "HAVE", "write": "WRITE", "follows": "THEN"}[L["status"]]
            page2.extend(
                f"  ({L['n']}) [{tag}] {part}"
                if i == 0
                else f"         {part}"
                for i, part in enumerate(_wrap(L["text"], 74))
            )
        page2.append("")
    page3 = [
        "Scored",
        "",
    ]
    for c in CLAIMS:
        page3.append(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    page3.append("")
    page3.append("Proof claims that stay fail")
    for c in PROOF_CLAIMS:
        if c["id"] in ("C17", "C18", "C19") or c["verdict"] == "fail":
            if c["id"] in ("C17", "C18", "C19", "C12", "C15"):
                page3.append(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    page3.extend(
        [
            "",
            "Write-up: docs/DA-PACK.md",
            "Status: docs/DA-COMPLETE.md",
            "BSD refuse: docs/BSD-PROOF-CHAIN.md (Documented)",
            "Hodge refuse: docs/HODGE-PROOF-CHAIN.md (Documented)",
        ]
    )
    return _paginate(page1) + _paginate(page2) + _paginate(page3)


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_pdf(path: Path, pages: list[list[str]]) -> None:
    """Minimal PDF 1.4 text pages. Helvetica. No extra library."""
    font_size = 10
    leading = 13
    left = 50
    top = 742
    content_objs = []
    for lines in pages:
        y = top
        chunks = ["BT", f"/F1 {font_size} Tf", f"{left} {y} Td"]
        first = True
        for line in lines:
            shown = _pdf_escape(line)
            if first:
                chunks.append(f"({shown}) Tj")
                first = False
            else:
                chunks.append(f"0 -{leading} Td ({shown}) Tj")
        chunks.append("ET")
        stream = "\n".join(chunks).encode("latin-1", "replace")
        content_objs.append(stream)

    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{3 + i} 0 R" for i in range(len(pages)))
    objects.append(
        f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode()
    )
    for i, stream in enumerate(content_objs):
        page_n = 3 + i
        content_n = 3 + len(pages) + i
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Contents {content_n} 0 R "
                f"/Resources << /Font << /F1 {3 + 2 * len(pages)} 0 R >> >> >>"
            ).encode()
        )
    for stream in content_objs:
        objects.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode()
            + stream
            + b"\nendstream"
        )
    objects.append(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    )

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode())
        out.extend(obj)
        out.extend(b"\nendobj\n")
    xref_at = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode())
    out.extend(
        (
            f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_at}\n%%EOF\n"
        ).encode()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out)


def run(out: Path | None = None) -> dict:
    pages = _pages()
    pdf = ROOT / "docs" / "DA-STATUS-PACK.pdf"
    write_pdf(pdf, pages)
    artifact = Path("/opt/cursor/artifacts/assets/da-status-pack.pdf")
    try:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(pdf.read_bytes())
        artifact_wrote = str(artifact)
    except OSError:
        artifact_wrote = None
    payload = {
        "meta": {
            "question": "close what sits; hand the rest as status, not QED",
            "writeup": "docs/DA-PACK.md",
            "pdf": str(pdf.relative_to(ROOT)),
            "emit_is_not_qed": True,
            "not_prize_packaging": True,
            "da_did_not_close_bsd": True,
            "sfe_is_not_hodge": True,
        },
        "sits": list(SITS),
        "open": list(OPEN),
        "status": [
            {
                "problem": pid,
                "line": _status_line(_chain(pid)),
                "write_n": _chain(pid)["write_n"],
                "leftover_sits": _chain(pid)["completion"]["leftover_sits"],
            }
            for pid in PROBLEMS
        ],
        "claims": CLAIMS,
        "counts": {
            "sits": len(SITS),
            "open": len(OPEN),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
        },
        "next_da_move": (
            "Read the PDF as status. Poincaré and A this PDE sit. "
            "Every other WRITE stays open. Do not cash the pack as a close."
        ),
        "artifact": artifact_wrote,
    }
    dest = Path(out) if out is not None else Path("results/da_pack.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    payload["_pdf"] = str(pdf)
    return payload


def print_pack(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("PACK  (what sits, then status; not QED)")
    print()
    print("SITS")
    for row in payload["sits"]:
        print(f"  {row}")
    print()
    print("OPEN")
    for row in payload["open"]:
        print(f"  {row}")
    print()
    print("STATUS")
    for row in payload["status"]:
        print(f"  {row['problem']}: {row['line']}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"pdf {payload['_pdf']}")
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_pack()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
