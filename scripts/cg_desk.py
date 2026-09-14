#!/usr/bin/env python3
"""Cosmic Graffiti assembly desk — print paste-ready copy.

One rundown. Three outs (magazine / Substack / Skool).
VAL8000 comments after the news, never the lead.

  python3 scripts/cg_desk.py list
  python3 scripts/cg_desk.py show issue-1
  python3 scripts/cg_desk.py substack issue-1
  python3 scripts/cg_desk.py skool issue-1
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESK = ROOT / "docs" / "cosmic-graffiti" / "desk"
RUNDOWN_PATH = DESK / "rundown.json"


def load_rundown() -> dict:
    if not RUNDOWN_PATH.is_file():
        raise SystemExit(f"Missing rundown: {RUNDOWN_PATH}")
    return json.loads(RUNDOWN_PATH.read_text(encoding="utf-8"))


def entries_by_slug(data: dict) -> dict:
    return {row["slug"]: row for row in data["entries"]}


def entry_dir(slug: str) -> Path:
    return DESK / "entries" / slug


def read_out(slug: str, name: str) -> str:
    path = entry_dir(slug) / f"{name}.md"
    if not path.is_file():
        raise SystemExit(f"No {name} out for {slug}: {path}")
    return path.read_text(encoding="utf-8").rstrip() + "\n"


def rule(title: str) -> str:
    bar = "─" * 56
    return f"\n{bar}\n{title}\n{bar}\n"


def cmd_list(data: dict) -> int:
    print("Cosmic Graffiti · assembly desk")
    print("One rundown. Three outs. VAL after the news.")
    print(f"Live magazine: {data['live_site']}")
    print(f"Substack:      {data['substack']}")
    print(f"Paywall:       {data['paywall']}")
    print()
    print(f"{'STATUS':<8} {'SLUG':<24} TITLE")
    print(f"{'------':<8} {'----':<24} -----")
    for row in data["entries"]:
        status = str(row.get("status", "?")).upper()
        slug = row["slug"]
        title = row["title"]
        mark = " ●" if row.get("seeded") else ""
        print(f"{status:<8} {slug:<24} {title}{mark}")
    print()
    print("● seeded card (three outs ready)")
    print("Trays are empty on purpose. Add a folder when you have copy.")
    print()
    print("Next: python3 scripts/cg_desk.py show issue-1")
    return 0


def cmd_show(data: dict, slug: str) -> int:
    rows = entries_by_slug(data)
    if slug not in rows:
        raise SystemExit(f"Unknown slug {slug!r}. Try: python3 scripts/cg_desk.py list")
    row = rows[slug]
    print(rule(f"SHOW  {row.get('kicker', '')}  ·  {row['title']}"))
    print(f"status: {row.get('status')}    slug: {slug}")
    print(row.get("dek", ""))
    if row.get("kind") == "tray-file":
        path = DESK / row["path"]
        print()
        print(path.read_text(encoding="utf-8"))
        return 0
    print(read_out(slug, "magazine"))
    val_path = entry_dir(slug) / "val.md"
    if row.get("val") and val_path.is_file():
        print(rule("VAL8000  ·  after the news  ·  not the lead"))
        print(val_path.read_text(encoding="utf-8").rstrip() + "\n")
    return 0


def _image_block(row: dict) -> str:
    images = row.get("images") or []
    if not images:
        return ""
    lines = ["Images / alt text", ""]
    for i, img in enumerate(images, 1):
        lines.append(f"{i}. {img['file']}")
        lines.append(f"   Alt: {img.get('alt', '').strip()}")
        if img.get("caption"):
            lines.append(f"   Caption: {img['caption']}")
        lines.append("")
    return "\n".join(lines)


def cmd_substack(data: dict, slug: str) -> int:
    rows = entries_by_slug(data)
    if slug not in rows:
        raise SystemExit(f"Unknown slug {slug!r}. Try: python3 scripts/cg_desk.py list")
    row = rows[slug]
    print(rule(f"SUBSTACK PASTE  ·  {row['title']}"))
    print(f"Paste into: {data['substack']}")
    print("Not the education-policy namesake.")
    print(f"Paywall: {data['paywall']}")
    print()
    print(_image_block(row))
    if row.get("kind") == "tray-file":
        print((DESK / row["path"]).read_text(encoding="utf-8"))
        return 0
    print(read_out(slug, "substack"))
    val_path = entry_dir(slug) / "val.md"
    if row.get("val") and val_path.is_file():
        print(rule("VAL8000 BOX — paste after the body"))
        print(val_path.read_text(encoding="utf-8").rstrip() + "\n")
    return 0


def cmd_skool(data: dict, slug: str) -> int:
    rows = entries_by_slug(data)
    if slug not in rows:
        raise SystemExit(f"Unknown slug {slug!r}. Try: python3 scripts/cg_desk.py list")
    row = rows[slug]
    print(rule(f"SKOOL PASTE  ·  {row['title']}"))
    print()
    print(_image_block(row))
    if row.get("kind") == "tray-file":
        print((DESK / row["path"]).read_text(encoding="utf-8"))
        return 0
    print(read_out(slug, "skool"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cg_desk.py",
        description="Cosmic Graffiti assembly desk — list cards or print paste-ready outs.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="One rundown of every card")
    show = sub.add_parser("show", help="Magazine copy, then VAL after the news")
    show.add_argument("slug")
    substack = sub.add_parser("substack", help="Paste-ready Substack (title, dek, body, images, alt)")
    substack.add_argument("slug")
    skool = sub.add_parser("skool", help="Paste-ready Skool (hook, images, ask in this thread)")
    skool.add_argument("slug")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    data = load_rundown()
    if args.cmd == "list":
        return cmd_list(data)
    if args.cmd == "show":
        return cmd_show(data, args.slug)
    if args.cmd == "substack":
        return cmd_substack(data, args.slug)
    if args.cmd == "skool":
        return cmd_skool(data, args.slug)
    return 2


if __name__ == "__main__":
    sys.exit(main())
