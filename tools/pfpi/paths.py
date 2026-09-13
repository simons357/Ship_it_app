"""Shared paths for PFPI tools."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "tools" / "pfpi" / "pfpi.db"
LEDGER_JSON = REPO_ROOT / "tools" / "pfpi" / "ledger.json"
ZENODO_INDEX = REPO_ROOT / "docs" / "papers" / "zenodo-spectral" / "INDEX.json"
DOCS_ROOT = REPO_ROOT / "docs"
SPELL_REGISTRY = REPO_ROOT / "packages" / "shared_core" / "spell_registry.json"

TEXT_EXTENSIONS = {".md", ".tex", ".html", ".txt", ".json"}
