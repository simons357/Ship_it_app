#!/usr/bin/env python3
"""Print the house doors and catalog. Does not charge anyone."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "house" / "catalog.json"


def load() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def doors() -> int:
    data = load()
    print(f"{data['title']}")
    print(f"Live lab: {data['live_lab']}")
    print(f"Magazine: {data['magazine']}")
    print(f"Paywall: {data['paywall']}")
    print()
    for name, door in data["doors"].items():
        print(
            f"{name:8}  ${door['price_usd']:<4}  {door['status']:12}  {door['who']}"
        )
    print()
    print("Studio $99 is a plan. This command does not take a card.")
    return 0


def catalog() -> int:
    data = load()
    for item in data["items"]:
        print(
            f"{item['door']:8}  {item['status']:12}  {item['name']}  ({item['where']})"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("doors", "catalog"))
    args = parser.parse_args(argv)
    if args.command == "doors":
        return doors()
    return catalog()


if __name__ == "__main__":
    sys.exit(main())
