"""Build SQLite FTS5 index over docs corpus and Zenodo mirror."""

from __future__ import annotations

import html
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from tools.pfpi.doi_status import lookup_doi
from tools.pfpi.paths import (
    DEFAULT_DB,
    DOCS_ROOT,
    REPO_ROOT,
    SPELL_REGISTRY,
    TEXT_EXTENSIONS,
    ZENODO_INDEX,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS docs (
    rowid INTEGER PRIMARY KEY,
    doc_id TEXT UNIQUE NOT NULL,
    title TEXT,
    body_text TEXT,
    source_type TEXT,
    source_uri TEXT,
    da_status TEXT,
    keep_cut TEXT,
    tags TEXT,
    file_path TEXT,
    updated_at TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
    title,
    body_text,
    tags,
    content='docs',
    content_rowid='rowid',
    tokenize='porter'
);

CREATE TRIGGER IF NOT EXISTS docs_ai AFTER INSERT ON docs BEGIN
    INSERT INTO docs_fts(rowid, title, body_text, tags)
    VALUES (new.rowid, new.title, new.body_text, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS docs_ad AFTER DELETE ON docs BEGIN
    INSERT INTO docs_fts(docs_fts, rowid, title, body_text, tags)
    VALUES ('delete', old.rowid, old.title, old.body_text, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS docs_au AFTER UPDATE ON docs BEGIN
    INSERT INTO docs_fts(docs_fts, rowid, title, body_text, tags)
    VALUES ('delete', old.rowid, old.title, old.body_text, old.tags);
    INSERT INTO docs_fts(rowid, title, body_text, tags)
    VALUES (new.rowid, new.title, new.body_text, new.tags);
END;
"""


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def _read_text(path: Path, max_chars: int = 500_000) -> str:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return raw[:max_chars]


def _title_from_path(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ")
    return stem.title()


def connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def clear_index(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM docs")
    conn.commit()


def upsert_doc(
    conn: sqlite3.Connection,
    *,
    doc_id: str,
    title: str,
    body_text: str,
    source_type: str,
    source_uri: str | None = None,
    da_status: str | None = None,
    keep_cut: str | None = None,
    tags: list[str] | None = None,
    file_path: str | None = None,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    tag_str = ",".join(tags or [])
    conn.execute(
        """
        INSERT INTO docs (
            doc_id, title, body_text, source_type, source_uri,
            da_status, keep_cut, tags, file_path, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(doc_id) DO UPDATE SET
            title=excluded.title,
            body_text=excluded.body_text,
            source_type=excluded.source_type,
            source_uri=excluded.source_uri,
            da_status=excluded.da_status,
            keep_cut=excluded.keep_cut,
            tags=excluded.tags,
            file_path=excluded.file_path,
            updated_at=excluded.updated_at
        """,
        (
            doc_id,
            title,
            body_text,
            source_type,
            source_uri,
            da_status,
            keep_cut,
            tag_str,
            file_path,
            now,
        ),
    )


def iter_doc_files(root: Path = DOCS_ROOT) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if "zenodo-spectral" in path.parts and path.name == "INDEX.json":
            continue
        yield path


def ingest_markdown_corpus(conn: sqlite3.Connection, root: Path = DOCS_ROOT) -> int:
    count = 0
    for path in iter_doc_files(root):
        rel = path.relative_to(REPO_ROOT).as_posix()
        body = _read_text(path)
        if not body.strip():
            continue
        tags: list[str] = []
        if path.suffix == ".tex":
            tags.append("format:tex")
        if "math" in path.parts:
            tags.append("domain:math")
        if "products" in path.parts:
            tags.append("domain:products")
        upsert_doc(
            conn,
            doc_id=f"file:{rel}",
            title=_title_from_path(path),
            body_text=body,
            source_type="markdown" if path.suffix == ".md" else path.suffix.lstrip("."),
            source_uri=rel,
            tags=tags,
            file_path=rel,
        )
        count += 1
    return count


def ingest_zenodo_index(conn: sqlite3.Connection, index_path: Path = ZENODO_INDEX) -> int:
    if not index_path.exists():
        return 0
    records: list[dict[str, Any]] = json.loads(index_path.read_text(encoding="utf-8"))
    count = 0
    for rec in records:
        doi = rec.get("doi") or ""
        status = lookup_doi(doi)
        keywords = rec.get("keywords") or []
        if isinstance(keywords, list):
            kw_text = ", ".join(str(k) for k in keywords)
        else:
            kw_text = str(keywords)
        desc = _strip_html(rec.get("desc") or "")
        body = f"{desc}\n\nKeywords: {kw_text}".strip()
        tags = ["source:zenodo", f"zenodo:{rec.get('id')}"]
        upsert_doc(
            conn,
            doc_id=f"zenodo:{rec.get('id')}",
            title=rec.get("title") or f"Zenodo {rec.get('id')}",
            body_text=body,
            source_type="zenodo",
            source_uri=f"https://doi.org/{doi}" if doi else None,
            da_status=status.get("da_status"),
            keep_cut=status.get("keep_cut"),
            tags=tags,
            file_path=f"docs/papers/zenodo-spectral/{rec.get('id')}/",
        )
        count += 1
    return count


def ingest_spell_registry(conn: sqlite3.Connection, registry_path: Path = SPELL_REGISTRY) -> int:
    if not registry_path.exists():
        return 0
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    count = 0
    for spell_id, entry in data.get("spells", {}).items():
        script = entry.get("script", "")
        script_path = REPO_ROOT / script
        doc_path = REPO_ROOT / entry.get("doc", "")
        parts = [entry.get("name", spell_id)]
        if script_path.exists():
            parts.append(_read_text(script_path, max_chars=8000))
        if doc_path.exists():
            parts.append(_read_text(doc_path, max_chars=4000))
        body = "\n\n".join(parts)
        tags = list(entry.get("tags") or []) + [f"spell:{spell_id}"]
        upsert_doc(
            conn,
            doc_id=f"spell:{spell_id}",
            title=entry.get("name") or spell_id,
            body_text=body,
            source_type="spell",
            source_uri=script,
            tags=tags,
            file_path=script,
        )
        count += 1
    return count


def ingest_ledger(conn: sqlite3.Connection, ledger_path: Path) -> int:
    if not ledger_path.exists():
        return 0
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    count = 0
    for entry in data.get("entries", []):
        entry_id = entry["id"]
        body = f"{entry.get('claim', '')}\n\n{entry.get('notes', '')}".strip()
        tags = [f"status:{entry.get('status')}", f"ledger:{entry_id}"]
        if entry.get("tags"):
            tags.extend(entry["tags"])
        upsert_doc(
            conn,
            doc_id=f"ledger:{entry_id}",
            title=entry.get("claim", entry_id)[:120],
            body_text=body,
            source_type="ledger",
            source_uri=entry.get("where"),
            da_status=entry.get("status"),
            keep_cut=entry.get("keep_cut"),
            tags=tags,
            file_path=entry.get("where"),
        )
        count += 1
    return count


def ingest_all(
    db_path: Path = DEFAULT_DB,
    *,
    clear: bool = True,
    ledger_path: Path | None = None,
) -> dict[str, int]:
    from tools.pfpi.paths import LEDGER_JSON

    ledger = ledger_path or LEDGER_JSON
    conn = connect(db_path)
    if clear:
        clear_index(conn)
    stats = {
        "markdown": ingest_markdown_corpus(conn),
        "zenodo": ingest_zenodo_index(conn),
        "spells": ingest_spell_registry(conn),
        "ledger": ingest_ledger(conn, ledger),
    }
    total = sum(stats.values())
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        ("ingested_at", datetime.now(timezone.utc).isoformat()),
    )
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        ("doc_count", str(total)),
    )
    conn.commit()
    conn.close()
    stats["total"] = total
    return stats


def doc_count(db_path: Path = DEFAULT_DB) -> int:
    if not db_path.exists():
        return 0
    conn = connect(db_path)
    row = conn.execute("SELECT COUNT(*) AS n FROM docs").fetchone()
    conn.close()
    return int(row["n"]) if row else 0


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Ingest corpus into PFPI SQLite FTS5 index")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="SQLite database path")
    parser.add_argument("--no-clear", action="store_true", help="Append without clearing")
    parser.add_argument("--ledger", type=Path, default=None, help="ledger.json path")
    args = parser.parse_args()

    stats = ingest_all(args.db, clear=not args.no_clear, ledger_path=args.ledger)
    print(f"PFPI ingest complete → {args.db}")
    for key, val in stats.items():
        print(f"  {key}: {val}")


if __name__ == "__main__":
    main()
