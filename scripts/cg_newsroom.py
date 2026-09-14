#!/usr/bin/env python3
"""Cosmic Graffiti newsroom: named desks, not a swarm and not Skynet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESKS = ROOT / "docs" / "cosmic-graffiti" / "desks.json"


def load_roster() -> dict:
    return json.loads(DESKS.read_text(encoding="utf-8"))


def status() -> int:
    roster = load_roster()
    print(f"Magazine: {roster['magazine']}")
    print("This is a desk roster. It is not Skynet.")
    print()
    missing = 0
    for desk in roster["desks"]:
        print(f"{desk['id']:10}  {desk['title']}")
        print(f"            {desk['job']}")
        for rel in desk["owns"]:
            path = ROOT / rel
            mark = "present" if path.is_file() else "missing in this checkout"
            if not path.is_file():
                missing += 1
            print(f"            {rel}  [{mark}]")
        print()
    print(
        "Missing files are normal until sibling magazine branches merge. "
        "Do not invent a second Cosmic Graffiti to fill a hole."
    )
    return 0 if missing == 0 else 2


def why() -> int:
    print(
        "\n".join(
            [
                "Why the agent network did not run:",
                "1. Agents got their own git branches and fought the same folder.",
                "2. There was no desk roster, so everyone rewrote the masthead.",
                "3. 'Ten thousand agents' was someone else's NS compute, not our staff.",
                "4. ElevenLabs never had a key here, so VAL8000 never spoke.",
                "5. Nothing posted to Substack or Skool from the desks.",
                "",
                "Fix: named desks in docs/cosmic-graffiti/desks.json, one file each.",
                "Skynet stays a punchline.",
            ]
        )
    )
    return 0


def table() -> int:
    roster = load_roster()
    rundown = ROOT / roster.get(
        "rundown", "docs/cosmic-graffiti/writers-room/RUNDOWN.md"
    )
    print(f"Show: {roster.get('show', roster['magazine'])}")
    print(f"Analogy: {roster.get('analogy', 'writers table')}")
    print(f"Showrunner: {roster.get('showrunner', 'Jon')}")
    print("One rundown. Writers get slots. They do not get private magazines.")
    print()
    for desk in roster["desks"]:
        role = desk.get("snl_role", "")
        print(f"{desk['id']:10}  {role}")
        print(f"            {desk['job']}")
    print()
    if rundown.is_file():
        print(f"Rundown: {rundown.relative_to(ROOT)}")
        print(rundown.read_text(encoding="utf-8").splitlines()[0])
    else:
        print("Rundown missing. Do not invent a second show.")
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "why", "table"))
    args = parser.parse_args(argv)
    if args.command == "status":
        return status()
    if args.command == "table":
        return table()
    return why()


if __name__ == "__main__":
    sys.exit(main())
