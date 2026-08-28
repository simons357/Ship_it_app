"""DOI → keep_cut / da_status mapping for Zenodo mirror records."""

from __future__ import annotations

DOI_STATUS: dict[str, dict[str, str | None]] = {
    "10.5281/zenodo.20405404": {"keep_cut": "KEEP", "da_status": "CLOSED"},
    "10.5281/zenodo.19842060": {"keep_cut": "KEEP", "da_status": "CLOSED"},
    "10.5281/zenodo.20518388": {"keep_cut": "KEEP", "da_status": "conditional"},
    "10.5281/zenodo.20552400": {"keep_cut": "CUT", "da_status": "KILLED"},
    "10.5281/zenodo.20552171": {"keep_cut": "CUT", "da_status": "KILLED"},
    "10.5281/zenodo.20269843": {"keep_cut": "CUT", "da_status": "KILLED"},
    "10.5281/zenodo.20518057": {"keep_cut": "KEEP", "da_status": "conditional"},
    "10.5281/zenodo.20405526": {"keep_cut": "KEEP", "da_status": "conditional"},
    "10.5281/zenodo.20552080": {"keep_cut": "KEEP", "da_status": "conditional"},
    "10.5281/zenodo.20405589": {"keep_cut": "KEEP", "da_status": "conditional"},
    "10.5281/zenodo.20405593": {"keep_cut": "KEEP", "da_status": "conditional"},
    "10.5281/zenodo.20405585": {"keep_cut": "KEEP", "da_status": "CLOSED"},
    "10.5281/zenodo.20405597": {"keep_cut": "KEEP", "da_status": "CLOSED"},
    "10.5281/zenodo.20272545": {"keep_cut": "KEEP", "da_status": "conditional"},
}


def lookup_doi(doi: str) -> dict[str, str | None]:
    return DOI_STATUS.get(doi, {"keep_cut": None, "da_status": None})
