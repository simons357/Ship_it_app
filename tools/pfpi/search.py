"""Search PFPI SQLite FTS5 index."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from tools.pfpi.ingest import connect
from tools.pfpi.paths import DEFAULT_DB


@dataclass
class SearchHit:
    doc_id: str
    title: str
    snippet: str
    source_type: str
    source_uri: str | None
    da_status: str | None
    keep_cut: str | None
    tags: list[str]
    file_path: str | None
    rank: float
    warning: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _build_fts_query(q: str) -> str:
    """Turn user query into FTS5 AND-joined tokens."""
    tokens = [t for t in q.replace('"', " ").split() if t.strip()]
    if not tokens:
        return ""
    escaped = []
    for tok in tokens:
        tok = tok.replace('"', '""')
        escaped.append(f'"{tok}"*')
    return " AND ".join(escaped)


def _warning_for_hit(keep_cut: str | None, da_status: str | None) -> str | None:
    if keep_cut == "CUT":
        return "CUT — do not cite as proof"
    if da_status == "KILLED":
        return "KILLED — false as stated"
    if da_status == "LEAD":
        return "LEAD — structural rhyme, not proved"
    return None


def search(
    query: str,
    *,
    db_path: Path = DEFAULT_DB,
    limit: int = 20,
    da_status: str | None = None,
    keep_cut: str | None = None,
    source_type: str | None = None,
    include_cut: bool = False,
) -> list[SearchHit]:
    fts_q = _build_fts_query(query)
    if not fts_q:
        return []

    conn = connect(db_path)
    sql = """
        SELECT
            d.doc_id, d.title, d.body_text, d.source_type, d.source_uri,
            d.da_status, d.keep_cut, d.tags, d.file_path,
            bm25(docs_fts) AS rank
        FROM docs_fts
        JOIN docs d ON d.rowid = docs_fts.rowid
        WHERE docs_fts MATCH ?
    """
    params: list[Any] = [fts_q]

    filters: list[str] = []
    if da_status:
        filters.append("d.da_status = ?")
        params.append(da_status)
    if keep_cut:
        filters.append("d.keep_cut = ?")
        params.append(keep_cut)
    if source_type:
        filters.append("d.source_type = ?")
        params.append(source_type)
    if not include_cut:
        filters.append("(d.keep_cut IS NULL OR d.keep_cut != 'CUT')")

    if filters:
        sql += " AND " + " AND ".join(filters)
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    hits: list[SearchHit] = []
    for row in rows:
        body = row["body_text"] or ""
        snippet = body[:240].replace("\n", " ")
        tags = [t for t in (row["tags"] or "").split(",") if t]
        hits.append(
            SearchHit(
                doc_id=row["doc_id"],
                title=row["title"] or row["doc_id"],
                snippet=snippet,
                source_type=row["source_type"] or "",
                source_uri=row["source_uri"],
                da_status=row["da_status"],
                keep_cut=row["keep_cut"],
                tags=tags,
                file_path=row["file_path"],
                rank=float(row["rank"]),
                warning=_warning_for_hit(row["keep_cut"], row["da_status"]),
            )
        )
    return hits


def search_json(query: str, **kwargs: Any) -> str:
    return json.dumps({"query": query, "hits": [h.to_dict() for h in search(query, **kwargs)]}, indent=2)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Search PFPI index")
    parser.add_argument("query", nargs="+", help="Search terms")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--status", dest="da_status", default=None, help="Filter da_status")
    parser.add_argument("--keep-cut", default=None, help="Filter keep_cut")
    parser.add_argument("--source-type", default=None)
    parser.add_argument("--include-cut", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    q = " ".join(args.query)
    hits = search(
        q,
        db_path=args.db,
        limit=args.limit,
        da_status=args.da_status,
        keep_cut=args.keep_cut,
        source_type=args.source_type,
        include_cut=args.include_cut,
    )

    if args.json:
        print(search_json(q, db_path=args.db, limit=args.limit, da_status=args.da_status,
                          keep_cut=args.keep_cut, source_type=args.source_type,
                          include_cut=args.include_cut))
        return

    if not hits:
        print("No results.")
        return

    for i, hit in enumerate(hits, 1):
        warn = f" [{hit.warning}]" if hit.warning else ""
        print(f"{i}. {hit.title}{warn}")
        print(f"   {hit.doc_id} | {hit.source_type} | rank={hit.rank:.3f}")
        if hit.file_path:
            print(f"   path: {hit.file_path}")
        print(f"   {hit.snippet[:200]}...")
        print()


if __name__ == "__main__":
    main()
