"""Ingest any source into the ChatVault repo inbox.

Browser localStorage is not the git repo. This module writes
``chatvault-export`` JSON sidecars under ``chatvault/inbox/`` and copies
binaries into ``chatvault/inbox/media/`` when they are under the copy cap.

A movie or sound is a human record, not a theorem. CLAIM_LEDGER stays
UNREVIEWED. Domain Architect does not prove Navier–Stokes or Riemann.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import re
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .chatvault_bridge import CHATVAULT_EXPORT_FORMAT, CHATVAULT_SCHEMA_VERSION

REPO = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = REPO / "chatvault" / "inbox"
COPY_CAP_BYTES = 100 * 1024 * 1024
TINY_IMAGE_BYTES = 32 * 1024
MAX_PASTE_CHARS = 50_000_000
SKIP_DIR_NAMES = frozenset(
    {
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".pytest_cache",
    }
)
SOURCE_AIS = frozenset(
    {"ChatGPT", "Claude", "Grok", "Base44", "DomainArchitect", "human", "unknown"}
)
SOURCE_TYPES = frozenset(
    {
        "conversation",
        "transcript",
        "markdown",
        "json",
        "csv",
        "code",
        "html",
        "letter",
        "paper",
        "app",
        "picture",
        "movie",
        "audio",
        "image",
        "pdf",
        "docx",
        "da_audit",
        "other",
    }
)
TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".markdown",
    ".json",
    ".csv",
    ".html",
    ".htm",
    ".xml",
    ".rtf",
    ".log",
}
PICTURE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tif", ".tiff"}
MOVIE_SUFFIXES = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}
AUDIO_SUFFIXES = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma"}
SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def classify_filename(filename: str, mime: str = "") -> str:
    lower = str(filename or "").lower()
    type_ = str(mime or "").lower()
    suffix = Path(lower).suffix
    if suffix in PICTURE_SUFFIXES or type_.startswith("image/"):
        return "picture"
    if suffix in MOVIE_SUFFIXES or type_.startswith("video/"):
        return "movie"
    if suffix in AUDIO_SUFFIXES or type_.startswith("audio/"):
        return "audio"
    if suffix == ".pdf" or type_ == "application/pdf":
        return "pdf"
    if suffix in {".doc", ".docx", ".odt"} or "wordprocessingml" in type_ or "msword" in type_:
        return "docx"
    if suffix in TEXT_SUFFIXES or type_.startswith("text/") or type_ == "application/json":
        return "text"
    return "other"


def looks_like_chatgpt_conversation(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("mapping"), dict)


def looks_like_chatgpt_export(value: Any) -> bool:
    if not isinstance(value, (dict, list)):
        return False
    if isinstance(value, list):
        return any(looks_like_chatgpt_conversation(item) for item in value)
    if isinstance(value.get("conversations"), list):
        return any(looks_like_chatgpt_conversation(item) for item in value["conversations"])
    return looks_like_chatgpt_conversation(value)


def looks_like_da_audit(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    if value.get("source") == "domain-architect" and value.get("format") == CHATVAULT_EXPORT_FORMAT:
        return True
    return isinstance(value.get("input_expression"), str) and "canonical_sfe_status" in value


def conversations_from_export(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if looks_like_chatgpt_conversation(item)]
    if isinstance(value, dict) and isinstance(value.get("conversations"), list):
        return [item for item in value["conversations"] if looks_like_chatgpt_conversation(item)]
    if looks_like_chatgpt_conversation(value):
        return [value]
    return []


def _message_text(node: dict[str, Any]) -> str:
    msg = node.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, dict):
        parts = content.get("parts")
        if isinstance(parts, list):
            bits = []
            for part in parts:
                if isinstance(part, str):
                    bits.append(part)
                elif isinstance(part, dict) and part.get("text"):
                    bits.append(str(part["text"]))
            return "\n".join(bit for bit in bits if bit).strip()
        if isinstance(content.get("text"), str):
            return content["text"].strip()
    return ""


def conversation_body(conv: dict[str, Any]) -> str:
    mapping = conv.get("mapping") or {}
    lines: list[str] = []

    def emit(node: dict[str, Any]) -> None:
        msg = node.get("message") or {}
        author = msg.get("author") or {}
        role = author.get("role") or msg.get("role") or ""
        if not role or role == "system":
            return
        text = _message_text(node)
        if text:
            lines.append(f"{str(role).upper()}:\n{text}")

    current = conv.get("current_node")
    if current and current in mapping:
        chain = []
        seen: set[str] = set()
        node_id = current
        while node_id and node_id in mapping and node_id not in seen:
            seen.add(node_id)
            chain.append(mapping[node_id])
            node_id = mapping[node_id].get("parent")
        chain.reverse()
        for node in chain:
            emit(node)
        if lines:
            return "\n\n".join(lines)
    for node in mapping.values():
        if isinstance(node, dict):
            emit(node)
    return "\n\n".join(lines)


def _uid(prefix: str = "cv") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}{uuid.uuid4().hex[:6]}"


def _safe_filename(name: str) -> str:
    base = Path(name or "media.bin").name
    cleaned = SAFE_NAME.sub("_", base).strip("._")[:80]
    return cleaned or "media.bin"


def empty_entry(partial: dict[str, Any] | None = None) -> dict[str, Any]:
    data = dict(partial or {})
    ingested = str(data.get("ingested_at") or _now())
    source_type = data.get("source_type") if data.get("source_type") in SOURCE_TYPES else "other"
    source_ai = data.get("source_ai") if data.get("source_ai") in SOURCE_AIS else "human"
    origin = data.get("origin_class")
    if origin not in {"ai_generated", "human_record"}:
        origin = "ai_generated" if source_type in {"conversation", "transcript"} else "human_record"
        if source_ai == "human" or source_type in {
            "letter",
            "paper",
            "picture",
            "movie",
            "audio",
            "pdf",
            "docx",
            "da_audit",
        }:
            origin = "human_record"
    raw = str(data.get("raw_content") or data.get("content_text") or "")
    return {
        "schema_version": CHATVAULT_SCHEMA_VERSION,
        "id": str(data.get("id") or _uid("ent")),
        "title": str(data.get("title") or "Untitled")[:120],
        "source_type": source_type,
        "source_ai": source_ai,
        "origin_class": origin,
        "source_file": str(data.get("source_file") or ""),
        "project_tags": list(data.get("project_tags") or []),
        "project_category": str(data.get("project_category") or ""),
        "content_text": str(data.get("content_text") or raw),
        "raw_content": raw,
        "summary": str(data.get("summary") or ""),
        "file_url": str(data.get("file_url") or ""),
        "media_path": str(data.get("media_path") or ""),
        "key_claims": list(data.get("key_claims") or []),
        "theorems": list(data.get("theorems") or []),
        "open_gaps": list(data.get("open_gaps") or []),
        "action_items": list(data.get("action_items") or []),
        "open_questions": list(data.get("open_questions") or []),
        "related_projects": list(data.get("related_projects") or []),
        "related_entities": list(data.get("related_entities") or []),
        "search_tags": list(data.get("search_tags") or []),
        "linked_files": list(data.get("linked_files") or []),
        "extraction_types": list(data.get("extraction_types") or []),
        "item_date": str(data.get("item_date") or ingested[:10]),
        "ingested_at": ingested,
        "updated_at": str(data.get("updated_at") or ingested),
        "visibility": data.get("visibility") if data.get("visibility") in {"private", "professional"} else "professional",
        "starred": bool(data.get("starred")),
        "archived": bool(data.get("archived")),
        "harmonic_note": str(data.get("harmonic_note") or ""),
    }


def export_bundle(entries: list[dict[str, Any]], *, source: str = "chatvault-inbox") -> dict[str, Any]:
    payload = [empty_entry(entry) for entry in entries]
    return {
        "format": CHATVAULT_EXPORT_FORMAT,
        "schema_version": CHATVAULT_SCHEMA_VERSION,
        "source": source,
        "exported_at": _now(),
        "count": len(payload),
        "entries": payload,
    }


def text_source_type(filename: str) -> str:
    lower = str(filename or "").lower()
    if lower.endswith(".md") or lower.endswith(".markdown"):
        return "markdown"
    if lower.endswith(".json"):
        return "json"
    if lower.endswith(".csv"):
        return "csv"
    if lower.endswith(".html") or lower.endswith(".htm"):
        return "html"
    if lower.endswith(".txt") or lower.endswith(".rtf") or lower.endswith(".log"):
        return "letter"
    return "other"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path, *, size: int) -> str:
    if size <= COPY_CAP_BYTES:
        return _sha256_bytes(path.read_bytes())
    digest = hashlib.sha256()
    digest.update(f"size={size}\n".encode("utf-8"))
    with path.open("rb") as handle:
        digest.update(handle.read(65536))
    return digest.hexdigest()


def _guess_mime(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


def media_stub_entry(
    *,
    filename: str,
    mime: str,
    size: int,
    kind: str,
    media_path: str = "",
    sha256: str = "",
    data_url: str = "",
    copied: bool = False,
    over_cap: bool = False,
) -> dict[str, Any]:
    stored = "data-url" if data_url else "repo-media" if media_path else "metadata-only"
    lines = [
        f"REAL {kind.upper()} {'STUB ' if not data_url else ''}{filename}",
        f"mime={mime or 'unknown'}",
        f"size={size}",
        f"stored={stored}",
    ]
    if media_path:
        lines.append(f"media_path={media_path}")
    if sha256:
        lines.append(f"sha256={sha256}")
    if over_cap:
        lines.append(f"copy_cap={COPY_CAP_BYTES}")
        lines.append("Binary not copied (over 100MB copy cap). JSON sidecar still written.")
    if not data_url:
        lines.append(
            "The binary is not stored in ChatVault raw_content. Title + filename + mime only."
        )
    raw = "\n".join(lines) + "\n"
    tags = ["real-record", kind, "inbox"]
    if mime:
        tags.append(mime)
    summary = (
        f"Real {kind} stored as a data URL ({size} bytes)."
        if data_url
        else f"Real {kind} stub with repo media at {media_path} ({size} bytes). Not a theorem."
        if media_path
        else f"Real {kind} stub — filename, type, and size only ({size} bytes). Not a theorem."
    )
    return empty_entry(
        {
            "id": f"cv_{sha256[:12]}" if sha256 else _uid("ent"),
            "title": filename,
            "source_type": kind if kind in SOURCE_TYPES else "other",
            "source_ai": "human",
            "origin_class": "human_record",
            "source_file": filename,
            "file_url": data_url,
            "media_path": media_path,
            "linked_files": [media_path] if media_path else [],
            "raw_content": raw,
            "content_text": raw,
            "summary": summary,
            "search_tags": tags,
        }
    )


def _copy_media(src: Path, inbox: Path, sha256: str) -> tuple[str, Path]:
    media_dir = inbox / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    dest_name = _safe_filename(src.name)
    stem = Path(dest_name).stem
    suffix = Path(dest_name).suffix
    dest = media_dir / dest_name
    if dest.exists():
        dest = media_dir / f"{stem}-{sha256[:8]}{suffix}"
    shutil.copy2(src, dest)
    rel = f"chatvault/inbox/media/{dest.name}"
    return rel, dest


def _ingest_chatgpt(value: Any, filename: str) -> list[dict[str, Any]]:
    entries = []
    for conv in conversations_from_export(value):
        body = conversation_body(conv)
        if not body:
            continue
        if len(body) > MAX_PASTE_CHARS:
            body = body[:MAX_PASTE_CHARS]
        created = conv.get("create_time")
        ingested = _now()
        if isinstance(created, (int, float)):
            ingested = datetime.fromtimestamp(created, tz=timezone.utc).isoformat()
        entries.append(
            empty_entry(
                {
                    "title": str(conv.get("title") or "ChatGPT conversation")[:120],
                    "source_ai": "ChatGPT",
                    "source_type": "transcript",
                    "origin_class": "ai_generated",
                    "source_file": filename,
                    "raw_content": body,
                    "content_text": body,
                    "search_tags": ["chatgpt-export", "ai-conversation", "inbox"],
                    "ingested_at": ingested,
                    "item_date": ingested[:10],
                }
            )
        )
    if not entries:
        raise ValueError("No ChatGPT conversations with text were found in that JSON.")
    return entries


def _ingest_text(path: Path, text: str) -> list[dict[str, Any]]:
    if len(text) > MAX_PASTE_CHARS:
        raise ValueError(f"{path.name} exceeds {MAX_PASTE_CHARS} characters.")
    source_type = text_source_type(path.name)
    return [
        empty_entry(
            {
                "title": path.name,
                "source_ai": "human",
                "source_type": source_type,
                "origin_class": "human_record",
                "source_file": path.name,
                "raw_content": text,
                "content_text": text,
                "summary": f"Filed from repo inbox ingest ({path.name}).",
                "search_tags": ["inbox", source_type, "human_record"],
            }
        )
    ]


def ingest_file(path: Path, inbox: Path, *, copy_cap: int = COPY_CAP_BYTES) -> list[dict[str, Any]]:
    """Turn one source file into ChatVault entries. Never treats wav as ChatGPT."""
    src = path.resolve()
    mime = _guess_mime(src)
    kind = classify_filename(src.name, mime)
    size = src.stat().st_size

    if kind in {"picture", "movie", "audio", "pdf", "docx"}:
        sha256 = _sha256_file(src, size=size)
        media_path = ""
        data_url = ""
        over_cap = size > copy_cap
        if not over_cap:
            media_path, _ = _copy_media(src, inbox, sha256)
            if kind == "picture" and size <= TINY_IMAGE_BYTES:
                import base64

                encoded = base64.b64encode(src.read_bytes()).decode("ascii")
                data_url = f"data:{mime};base64,{encoded}"
        return [
            media_stub_entry(
                filename=src.name,
                mime=mime,
                size=size,
                kind=kind,
                media_path=media_path,
                sha256=sha256,
                data_url=data_url,
                copied=bool(media_path),
                over_cap=over_cap,
            )
        ]

    if kind == "text" or src.suffix.lower() in TEXT_SUFFIXES:
        raw = src.read_text(encoding="utf-8", errors="replace")
        if src.suffix.lower() == ".json" or mime == "application/json":
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, dict) and parsed.get("format") == CHATVAULT_EXPORT_FORMAT:
                return [empty_entry(entry) for entry in (parsed.get("entries") or [])]
            if parsed is not None and looks_like_da_audit(parsed):
                if parsed.get("format") == CHATVAULT_EXPORT_FORMAT:
                    return [empty_entry(entry) for entry in (parsed.get("entries") or [])]
                # Raw FRA JSON (not a live re-audit). File the narrative as a human record.
                narrative = str(parsed.get("narrative") or json.dumps(parsed, indent=2))
                expression = str(parsed.get("input_expression") or src.name)
                return [
                    empty_entry(
                        {
                            "title": f"DA audit: {expression[:72]}",
                            "source_type": "da_audit",
                            "source_ai": "DomainArchitect",
                            "origin_class": "human_record",
                            "source_file": src.name,
                            "raw_content": narrative,
                            "content_text": narrative,
                            "summary": (
                                "Domain Architect FRA audit. "
                                f"Canonical SFE status: {parsed.get('canonical_sfe_status') or 'unresolved'}. "
                                "Not a proof."
                            ),
                            "search_tags": ["domain-architect", "fra", "da_audit", "inbox"],
                            "related_projects": ["Domain Architect"],
                            "project_category": "Domain Architect",
                        }
                    )
                ]
            if parsed is not None and looks_like_chatgpt_export(parsed):
                return _ingest_chatgpt(parsed, src.name)
        return _ingest_text(src, raw)

    sha256 = _sha256_file(src, size=size)
    media_path = ""
    over_cap = size > copy_cap
    if not over_cap:
        media_path, _ = _copy_media(src, inbox, sha256)
    return [
        media_stub_entry(
            filename=src.name,
            mime=mime or "application/octet-stream",
            size=size,
            kind="other",
            media_path=media_path,
            sha256=sha256,
            over_cap=over_cap,
        )
    ]


def _is_inbox_bookkeeping(path: Path, inbox: Path) -> bool:
    try:
        path.resolve().relative_to(inbox.resolve())
    except ValueError:
        return False
    name = path.name
    if name in {"README.md", ".gitkeep", "index.json"}:
        return True
    return False


def iter_sources(path: Path, inbox: Path) -> Iterable[Path]:
    src = path.resolve()
    if src.is_file():
        yield src
        return
    skip_inbox = src != inbox.resolve()
    for root, dirs, files in os.walk(src):
        dirs[:] = [name for name in dirs if name not in SKIP_DIR_NAMES]
        root_path = Path(root)
        if skip_inbox:
            dirs[:] = [
                name
                for name in dirs
                if not (name == "inbox" and root_path.name == "chatvault")
                and not (name == "media" and root_path.name == "inbox")
            ]
        for name in files:
            candidate = root_path / name
            if _is_inbox_bookkeeping(candidate, inbox):
                continue
            yield candidate


def write_inbox_export(entries: list[dict[str, Any]], inbox: Path, *, stem: str | None = None) -> Path:
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / "media").mkdir(parents=True, exist_ok=True)
    payload = export_bundle(entries)
    first_id = payload["entries"][0]["id"] if payload["entries"] else _uid("box")
    name = _safe_filename(f"{stem or first_id}.json")
    if not name.endswith(".json"):
        name = f"{name}.json"
    dest = inbox / name
    if dest.exists():
        dest = inbox / f"{Path(name).stem}-{first_id[-8:]}.json"
    dest.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return dest


def write_inbox_payload(payload: dict[str, Any], inbox: Path) -> list[Path]:
    """Write a chatvault-export (or a single entry) as inbox JSON. No binary upload."""
    if not isinstance(payload, dict):
        raise ValueError("Inbox POST must be a JSON object.")
    if payload.get("format") == CHATVAULT_EXPORT_FORMAT:
        entries = [empty_entry(entry) for entry in (payload.get("entries") or [])]
    elif payload.get("id") or payload.get("raw_content") or payload.get("title"):
        entries = [empty_entry(payload)]
    else:
        raise ValueError("Body must be a chatvault-export or a ChatVault entry.")
    if not entries:
        raise ValueError("No entries to file.")
    written = []
    for entry in entries:
        written.append(write_inbox_export([entry], inbox, stem=entry["id"]))
    refresh_index(inbox)
    return written


def list_inbox_files(inbox: Path) -> list[dict[str, str]]:
    if not inbox.is_dir():
        return []
    files = []
    for path in sorted(inbox.glob("*.json")):
        if path.name == "index.json":
            continue
        files.append(
            {
                "name": path.name,
                "url": f"/chatvault/inbox/{path.name}",
            }
        )
    return files


def refresh_index(inbox: Path) -> Path:
    inbox.mkdir(parents=True, exist_ok=True)
    files = list_inbox_files(inbox)
    payload = {
        "format": "chatvault-inbox-index",
        "schema_version": CHATVAULT_SCHEMA_VERSION,
        "updated_at": _now(),
        "count": len(files),
        "files": [item["name"] for item in files],
    }
    dest = inbox / "index.json"
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest


@dataclass
class IngestResult:
    written: list[Path] = field(default_factory=list)
    entries: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.entries)


def ingest_path(
    source: str | Path,
    inbox: str | Path | None = None,
    *,
    copy_cap: int = COPY_CAP_BYTES,
) -> IngestResult:
    src = Path(source)
    dest = Path(inbox) if inbox else DEFAULT_INBOX
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "media").mkdir(parents=True, exist_ok=True)
    if not src.exists():
        raise FileNotFoundError(f"Path not found: {src}")
    result = IngestResult()
    for file_path in iter_sources(src, dest):
        try:
            entries = ingest_file(file_path, dest, copy_cap=copy_cap)
        except (ValueError, OSError) as err:
            result.skipped.append(f"{file_path}: {err}")
            continue
        for entry in entries:
            size = file_path.stat().st_size if file_path.is_file() else 0
            if size > copy_cap and classify_filename(file_path.name) in {
                "picture",
                "movie",
                "audio",
                "pdf",
                "docx",
                "other",
            }:
                result.warnings.append(
                    f"{file_path.name}: {size} bytes over {copy_cap} copy cap; JSON written, binary not copied."
                )
        sidecar = write_inbox_export(entries, dest, stem=entries[0]["id"] if entries else file_path.stem)
        result.written.append(sidecar)
        result.entries.extend(entries)
    refresh_index(dest)
    return result
