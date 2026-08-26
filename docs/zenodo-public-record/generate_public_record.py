#!/usr/bin/env python3
"""Build honest public-facing PDFs for the Zenodo restore.

Layout locked by the owner:
  page 1  — public-facing paper (clean title, live stack, why August happened)
  page 2  — errata (walked-back prize language; files were never tombstoned)
  page 3+ — original June draft, if wrapping a record that has a PDF

This script does not log into Zenodo. The owner uploads the PDFs and
restores titles in the Zenodo UI, or later PATCHes metadata with a
personal access token (never a password).
"""
from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

PACK = Path(__file__).resolve().parent
SRC = PACK / "sources"
OUT = PACK / "out"
TITLES_PATH = PACK / "titles.json"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

DOI_ROUTE_C = "10.5281/zenodo.22050963"
DOI_PHI = "10.5281/zenodo.22050974"
DOI_STATUS = "10.5281/zenodo.22050978"
DOI_Q6 = "10.5281/zenodo.22050962"

STATUS_TITLE = (
    "August 2026 status note: live stack and walked-back prize language"
)

# Page 1 must not contain the crime-tape prefixes. Name the event; do not
# reprint the stamp strings on the public face.
WHY_AUGUST = (
    "In August 2026, prize-claim language on several June 2026 records was "
    "walked back. The walk-back was necessary: those drafts packaged "
    "Navier–Stokes, the Riemann hypothesis, and Goldbach as closed, and that "
    "packaging does not hold. The walk-back was executed badly. Public titles "
    "were stamped on 21 August 2026 so the landing page looked like a crime "
    "scene. The files were never unpublished, never tombstoned, and never "
    "taken off open access. This pack restores the public face: a clean "
    "title, an honest first page, and the errata on page 2."
)

WHAT_STANDS = [
    (
        "Φ-renormalization (fluids).",
        f"Q₁-augmented swirl / Φ-renormalization. Live DOI {DOI_PHI}. "
        "Not a Clay Navier–Stokes proof.",
    ),
    (
        "Route C (RH, exploratory).",
        "Operator 1/(gcd(i,j)·√(ij)), conditional on two named analytic gaps. "
        f"Live DOI {DOI_ROUTE_C}. Not a proof of the Riemann hypothesis.",
    ),
    (
        "Ring + SND (Goldbach, conditional).",
        "The Goldbach statement remains conditional on the strong night-driver "
        "hypothesis. It is not a theorem.",
    ),
    (
        "T2 under SND, and Bridge*.",
        "These stay as named conditional / derived objects. They are not "
        "Millennium closures.",
    ),
    (
        "Inverse-GCD / Q_N note (restricted).",
        f"Definitions and a restricted Rayleigh bound. Live DOI {DOI_Q6}. "
        "Not a full-spectrum floor and not a proof of RH.",
    ),
]

WALKED_BACK = [
    (
        "Clay Statement B / Navier–Stokes millennium packaging.",
        "The June drafts treated a regularity claim as closed. That language "
        "is walked back. The Φ-renormalization note is the live fluids object.",
    ),
    (
        "Quantum Lens / Q6 Goldbach as a theorem.",
        "Goldbach stays conditional on SND. Q6 is not a proof.",
    ),
    (
        "Montgomery–Dyson / pair correlation as a finished RH argument.",
        "That packaging is walked back. Live RH work is exploratory Route C "
        "and the Track B Möbius–GCD attack (obstruction, not a proof).",
    ),
    (
        "Three-in-one / SND ≡ GNC ≡ Bridge as closures.",
        "Those identities were used as if they closed NS, RH, and Goldbach. "
        "They do not. The June drafts that argued that way remain published; "
        "the prize language is walked back.",
    ),
    (
        "Full-spectrum λ_min(Q_N) > −1/2 as a RH proof.",
        "That bound is not a proof of RH. Inverse-GCD 1/gcd is not the live "
        "Route C operator.",
    ),
]


def load_titles() -> dict:
    return json.loads(TITLES_PATH.read_text(encoding="utf-8"))


def register_fonts() -> None:
    regular = FONT_DIR / "DejaVuSerif.ttf"
    bold = FONT_DIR / "DejaVuSerif-Bold.ttf"
    if not regular.is_file() or not bold.is_file():
        raise FileNotFoundError(
            f"DejaVu Serif not found in {FONT_DIR}. "
            "Install fonts-dejavu-core or point FONT_DIR at DejaVu Serif."
        )
    pdfmetrics.registerFont(TTFont("DejaVuSerif", str(regular)))
    pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", str(bold)))


def styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="DejaVuSerif-Bold",
            fontSize=13,
            leading=16,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="DejaVuSerif-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="DejaVuSerif",
            fontSize=10,
            leading=13,
            spaceAfter=6,
        ),
        "item": ParagraphStyle(
            "item",
            parent=base["BodyText"],
            fontName="DejaVuSerif",
            fontSize=10,
            leading=13,
            leftIndent=12,
            spaceAfter=6,
        ),
        "foot": ParagraphStyle(
            "foot",
            parent=base["BodyText"],
            fontName="DejaVuSerif",
            fontSize=9,
            leading=12,
            spaceBefore=8,
        ),
        "tiny": ParagraphStyle(
            "tiny",
            parent=base["BodyText"],
            fontName="DejaVuSerif",
            fontSize=8,
            leading=10,
            leftIndent=8,
            spaceAfter=1,
        ),
    }


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _p(story: list, key: str, text: str, s: dict) -> None:
    story.append(Paragraph(text, s[key]))


def _item(story: list, title: str, body: str, s: dict) -> None:
    _p(story, "item", f"<b>{_esc(title)}</b> {_esc(body)}", s)


def _doc(path: Path, title: str) -> SimpleDocTemplate:
    path.parent.mkdir(parents=True, exist_ok=True)
    return SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=title,
        author="Jonathan Simons",
    )


def live_stack_compact() -> str:
    return (
        f"Live exploratory stack: Φ-renormalization {DOI_PHI} (not a Clay "
        f"Navier–Stokes proof); Route C {DOI_ROUTE_C} (not a proof of RH); "
        "Ring+SND Goldbach remains conditional on SND; T2 under SND and "
        f"Bridge* stay named derived objects; inverse-GCD note {DOI_Q6} "
        "is a restricted Rayleigh bound, not a full-spectrum floor."
    )


def page1_status(story: list, s: dict, heading: str, lead: str) -> None:
    _p(story, "h1", _esc(heading), s)
    _p(story, "body", lead, s)
    _p(story, "h2", "Why the August 2026 action happened", s)
    _p(story, "body", WHY_AUGUST, s)
    _p(story, "h2", "What still stands (live exploratory stack)", s)
    for title, body in WHAT_STANDS:
        _item(story, title, body, s)


def page1_cover(story: list, s: dict, heading: str, lead: str) -> None:
    """Shorter face so a long scientific title still leaves errata on page 2."""
    _p(story, "h1", _esc(heading), s)
    _p(story, "body", lead, s)
    _p(story, "h2", "Why the August 2026 action happened", s)
    _p(story, "body", WHY_AUGUST, s)
    _p(story, "h2", "Live exploratory stack (cite these, not prize packaging)", s)
    _p(story, "body", live_stack_compact(), s)


def page2_errata(
    story: list,
    s: dict,
    extra_lead: str,
    restore: list | None = None,
) -> None:
    _p(story, "h1", "Errata: prize-claim language walked back", s)
    _p(story, "body", extra_lead, s)
    for title, body in WALKED_BACK:
        _item(story, title, body, s)
    if restore:
        _p(
            story,
            "h2",
            "Records whose public titles must be restored (files stay up)",
            s,
        )
        _p(
            story,
            "body",
            "On 21 August 2026 some public titles were prefixed. Strip those "
            "prefixes and any stray trailing quote. Edit each stamped version "
            "URL (concept URLs often show only the latest version).",
            s,
        )
        for rec in restore:
            line = f"{rec['doi']} — {rec['restore_title']}"
            _p(story, "tiny", _esc(line), s)
    else:
        _p(
            story,
            "body",
            f"The full restore list is page 2 of the status note {DOI_STATUS} "
            "and in titles.json in this pack.",
            s,
        )
    _p(
        story,
        "foot",
        "This page is the errata. It is not a tombstone. No Millennium "
        "problem is claimed. Domain Architect is a local FRA classifier "
        "(inquiry). ChatVault is search. Neither wrote these Zenodo titles.",
        s,
    )


def build_status_pdf(path: Path, restore: list) -> None:
    s = styles()
    doc = _doc(path, STATUS_TITLE)
    story: list = []
    lead = (
        "Jonathan Simons. This note is the public-facing status record for the "
        f"Zenodo corpus. Cite this note as {DOI_STATUS} after the title on that "
        "record is restored. The research line is not paused; this is the "
        "public record to publish."
    )
    page1_status(story, s, STATUS_TITLE, lead)
    story.append(Spacer(1, 8))
    _p(
        story,
        "foot",
        "Page 1 of 2. Errata — walked-back prize language — on the next page. "
        "No Millennium problem is claimed.",
        s,
    )
    story.append(PageBreak())
    extra = (
        "The June 2026 records listed below remain published and open. Nothing "
        "was deleted. What is walked back is the prize-claim language in those "
        "drafts, not the existence of the files. Titles on those records must "
        "be restored to the original wording."
    )
    page2_errata(story, s, extra, restore)
    doc.build(story)


def build_cover_and_errata(
    path: Path,
    paper_title: str,
    this_doi: str,
    tex_only: bool = False,
) -> None:
    s = styles()
    doc = _doc(path, paper_title)
    story: list = []
    if tex_only:
        lead = (
            f"Jonathan Simons. This record ({this_doi}) is a June 2026 "
            "exploratory draft. It remains published and citable. The deposit "
            "currently holds TeX or a webloc, not a public PDF. This two-page "
            "note is the public-facing face to upload as a new version. Leave "
            "the original source files in place. Prize-claim language in the "
            "source is walked back; see page 2. This page is not a retraction "
            "notice."
        )
    else:
        lead = (
            f"Jonathan Simons. This record ({this_doi}) is a June 2026 "
            "exploratory draft. It remains published and citable. Prize-claim "
            "language in the body is walked back; see page 2. This page is the "
            "public-facing face of the record. It is not a retraction notice."
        )
    page1_cover(story, s, paper_title, lead)
    _p(
        story,
        "body",
        f"Full status note: {DOI_STATUS} (restore that record’s title to "
        f"“{_esc(STATUS_TITLE)}” when you upload the replacement PDF).",
        s,
    )
    follow = (
        "Page 1 of this record. Errata on the next page."
        if tex_only
        else "Page 1 of this record. Errata on the next page. Original June "
        "draft follows."
    )
    _p(story, "foot", follow + " No Millennium problem is claimed.", s)
    story.append(PageBreak())
    extra = (
        "Prize-claim language in this draft does not stand. The file stays "
        "published so the walk-back is auditable."
        if tex_only
        else "The pages after this one are the June 2026 draft, unchanged. "
        "They are on the record so the walk-back is auditable. The following "
        "prize-claim language in that draft does not stand."
    )
    page2_errata(story, s, extra, restore=None)
    doc.build(story)


def build_reader_note(path: Path, paper_title: str, this_doi: str) -> None:
    """Optional one-page notice to prepend to live Route C / Phi PDFs."""
    s = styles()
    doc = _doc(path, paper_title)
    story: list = []
    _p(story, "h1", _esc(paper_title), s)
    _p(
        story,
        "body",
        f"Jonathan Simons. This is the live public-facing paper ({this_doi}). "
        "The scientific pages follow. Prize-claim language on related June 2026 "
        "drafts is walked back; those drafts stay published. The errata is page 2 "
        f"of the status note {DOI_STATUS}, not a banner in this title.",
        s,
    )
    _p(story, "h2", "Why the August 2026 action happened", s)
    _p(story, "body", WHY_AUGUST, s)
    _p(
        story,
        "foot",
        "This page is a reader notice. It is not a retraction stamp. The paper "
        "starts on the next page. Uploading this wrap is OPTIONAL — a "
        "description pointer is preferred so the scientific PDF does not look "
        "like a retraction banner.",
        s,
    )
    doc.build(story)


def prepend(cover: Path, original: Path, dest: Path, title: str) -> None:
    writer = PdfWriter()
    writer.append(str(cover))
    writer.append(str(original))
    writer.add_metadata(
        {
            "/Title": title,
            "/Author": "Jonathan Simons",
        }
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    writer.write(str(dest))
    writer.close()


def write_paste_sheet(path: Path, data: dict) -> None:
    lines = [
        "# Paste-ready Zenodo titles",
        "",
        "Log in as the record owner. Open each **version** URL. Edit → "
        "replace Title → Publish.",
        "",
        f"**Status note title:** {data['status_note']['restore_title']}",
        "",
        "## Restore (strip prefix; exact original wording)",
        "",
    ]
    for rec in data["restore"]:
        lines.append(f"- `{rec['record_url']}`")
        lines.append(f"  - **Paste:** {rec['restore_title']}")
        lines.append("")
    lines.append("## Status note rename")
    lines.append("")
    st = data["status_note"]
    lines.append(f"- `{st['record_url']}` and `{st['also_edit_urls'][0]}`")
    lines.append(f"  - **Paste:** {st['restore_title']}")
    lines.append("")
    lines.append("## Calm description pointer (replace screaming August paragraphs)")
    lines.append("")
    lines.append(data["calm_pointer_html"])
    lines.append("")
    lines.append("## Optional rename")
    lines.append("")
    for rec in data.get("optional_rename", []):
        lines.append(f"- `{rec['record_url']}`")
        lines.append(f"  - **Paste:** {rec['restore_title']}")
        lines.append(f"  - {rec.get('note', '')}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    register_fonts()
    data = load_titles()
    restore = data["restore"]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "notices").mkdir(parents=True, exist_ok=True)
    (OUT / "optional").mkdir(parents=True, exist_ok=True)

    status = OUT / "status_note_public_facing.pdf"
    build_status_pdf(status, restore)

    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)

    for rec in restore:
        kind = rec["kind"]
        title = rec["restore_title"]
        doi = rec["doi"]
        if kind == "wrap":
            source = SRC / rec["source_pdf"]
            if not source.is_file():
                raise FileNotFoundError(f"missing source PDF: {source}")
            cover = tmp / f"cover_{rec['id']}.pdf"
            dest = OUT / rec["upload_pdf"]
            build_cover_and_errata(cover, title, doi, tex_only=False)
            prepend(cover, source, dest, title)
            cover.unlink()
        elif kind == "notice":
            dest = OUT / rec["upload_pdf"]
            build_cover_and_errata(dest, title, doi, tex_only=True)
        else:
            raise ValueError(f"unknown kind {kind} for {rec['id']}")

    # Optional reader notices for live Route C / Phi (titles already clean).
    live = {row["id"]: row for row in data["live_clean"]}
    rc = live[22050963]
    phi = live[22050974]
    rc_note = tmp / "note_route_c.pdf"
    phi_note = tmp / "note_phi.pdf"
    build_reader_note(rc_note, rc["title"], rc["doi"])
    build_reader_note(phi_note, phi["title"], phi["doi"])
    prepend(
        rc_note,
        SRC / "22050963_05_route_c_conditional.pdf",
        OUT / rc["optional_upload_pdf"],
        rc["title"],
    )
    prepend(
        phi_note,
        SRC / "22050974_01_phi_renormalization.pdf",
        OUT / phi["optional_upload_pdf"],
        phi["title"],
    )
    rc_note.unlink()
    phi_note.unlink()
    tmp.rmdir()

    write_paste_sheet(OUT / "PASTE_TITLES.md", data)

    manifest = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            manifest.append(f"{p.relative_to(OUT)}\t{p.stat().st_size}")
    (OUT / "MANIFEST.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
