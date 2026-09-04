"""Minimal FastAPI spine for PFPI search and spell execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from packages.shared_core.spell_runner import list_spells, run_spell
from tools.pfpi.ingest import doc_count, ingest_all
from tools.pfpi.ledger import filter_ledger, ledger_summary, load_ledger
from tools.pfpi.paths import DEFAULT_DB
from tools.pfpi.search import search

app = FastAPI(
    title="Prime Field Pattern Index",
    version="0.1.0",
    description="Platform spine API — search corpus, run spells, query DA ledger",
)


class SpellRunRequest(BaseModel):
    name: str
    args: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "doc_count": doc_count(DEFAULT_DB)}


@app.post("/v1/ingest")
def v1_ingest(clear: bool = True) -> dict[str, Any]:
    stats = ingest_all(DEFAULT_DB, clear=clear)
    return {"ok": True, "stats": stats}


@app.get("/v1/search")
def v1_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = Query(None, alias="da_status"),
    keep_cut: str | None = None,
    source_type: str | None = None,
    include_cut: bool = False,
) -> dict[str, Any]:
    hits = search(
        q,
        db_path=DEFAULT_DB,
        limit=limit,
        da_status=status,
        keep_cut=keep_cut,
        source_type=source_type,
        include_cut=include_cut,
    )
    return {"query": q, "count": len(hits), "hits": [h.to_dict() for h in hits]}


@app.get("/v1/ledger")
def v1_ledger(status: str | None = None) -> dict[str, Any]:
    entries = filter_ledger(status=status)
    return {
        "summary": ledger_summary(),
        "count": len(entries),
        "entries": entries,
    }


@app.get("/v1/ledger/full")
def v1_ledger_full() -> dict[str, Any]:
    return load_ledger()


@app.get("/v1/spells")
def v1_spells() -> dict[str, Any]:
    return {"spells": list_spells()}


@app.post("/v1/spells/run")
def v1_spells_run(body: SpellRunRequest) -> dict[str, Any]:
    try:
        result = run_spell(body.name, body.args)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if result["returncode"] != 0:
        raise HTTPException(
            status_code=500,
            detail={"message": "Spell failed", "result": result},
        )
    return result


def main() -> None:
    import uvicorn

    uvicorn.run("tools.pfpi.serve:app", host="127.0.0.1", port=8765, reload=False)


if __name__ == "__main__":
    main()
