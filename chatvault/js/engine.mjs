/**
 * ChatVault engine — local-first knowledge capture.
 *
 * This is the competitive core: provenance, immutable raw text,
 * CLAIM_LEDGER statuses that never auto-promote to PROVED, and
 * fielded search (AND / OR / phrase). It is not a truth engine.
 */

export const SCHEMA_VERSION = "chatvault-engine-0.1.0";

export const LEDGER_STATUSES = Object.freeze([
  "UNREVIEWED",
  "OPEN",
  "CONJECTURAL",
  "NUMERICAL",
  "CONDITIONAL",
  "PROVED",
  "WITHDRAWN",
]);

export const SOURCE_AIS = Object.freeze([
  "ChatGPT",
  "Claude",
  "Grok",
  "Base44",
  "human",
  "unknown",
]);

export const SOURCE_TYPES = Object.freeze([
  "conversation",
  "markdown",
  "json",
  "pdf",
  "docx",
  "image",
  "csv",
  "code",
  "other",
]);

export const VISIBILITY = Object.freeze(["private", "professional"]);

function nowIso() {
  return new Date().toISOString();
}

function uid(prefix = "cv") {
  return `${prefix}_${Math.random().toString(36).slice(2, 10)}${Date.now().toString(36)}`;
}

function asArray(value) {
  if (Array.isArray(value)) return value.filter((v) => v != null && String(v).trim() !== "");
  if (value == null || String(value).trim() === "") return [];
  return [String(value)];
}

function asString(value, fallback = "") {
  if (value == null) return fallback;
  return String(value);
}

export function normalizeStatus(status) {
  const s = String(status || "UNREVIEWED").toUpperCase();
  return LEDGER_STATUSES.includes(s) ? s : "UNREVIEWED";
}

export function ledgerItem(text, status = "UNREVIEWED") {
  return {
    id: uid("lg"),
    text: asString(text).trim(),
    status: normalizeStatus(status),
    human_reviewed: normalizeStatus(status) === "PROVED",
  };
}

/**
 * Ingest and automatic extractors may never mark PROVED.
 * Only an explicit human review path may.
 */
export function assertNotAutoProved(status, { humanReviewed } = {}) {
  const s = normalizeStatus(status);
  if (s === "PROVED" && !humanReviewed) {
    return "UNREVIEWED";
  }
  return s;
}

export function emptyEntry(partial = {}) {
  const ingested = asString(partial.ingested_at, nowIso());
  return {
    schema_version: SCHEMA_VERSION,
    id: asString(partial.id, uid("ent")),
    title: asString(partial.title, "Untitled"),
    source_type: SOURCE_TYPES.includes(partial.source_type) ? partial.source_type : "conversation",
    source_ai: SOURCE_AIS.includes(partial.source_ai) ? partial.source_ai : "unknown",
    source_file: asString(partial.source_file),
    project_tags: asArray(partial.project_tags),
    project_category: asString(partial.project_category),
    content_text: asString(partial.content_text),
    raw_content: asString(partial.raw_content, asString(partial.content_text)),
    summary: asString(partial.summary),
    file_url: asString(partial.file_url),
    key_claims: (partial.key_claims || []).map((c) =>
      typeof c === "string" ? ledgerItem(c, "UNREVIEWED") : { ...ledgerItem(c.text, c.status), ...c, status: assertNotAutoProved(c.status, { humanReviewed: c.human_reviewed }) }
    ),
    theorems: (partial.theorems || []).map((c) =>
      typeof c === "string" ? ledgerItem(c, "UNREVIEWED") : { ...ledgerItem(c.text, c.status), ...c, status: assertNotAutoProved(c.status, { humanReviewed: c.human_reviewed }) }
    ),
    open_gaps: (partial.open_gaps || []).map((c) =>
      typeof c === "string" ? ledgerItem(c, "OPEN") : { ...ledgerItem(c.text, c.status || "OPEN"), ...c }
    ),
    action_items: asArray(partial.action_items),
    open_questions: asArray(partial.open_questions),
    related_projects: asArray(partial.related_projects),
    related_entities: asArray(partial.related_entities),
    search_tags: asArray(partial.search_tags),
    linked_files: asArray(partial.linked_files),
    extraction_types: asArray(partial.extraction_types),
    item_date: asString(partial.item_date, ingested.slice(0, 10)),
    ingested_at: ingested,
    updated_at: asString(partial.updated_at, ingested),
    visibility: VISIBILITY.includes(partial.visibility) ? partial.visibility : "professional",
    starred: Boolean(partial.starred),
    archived: Boolean(partial.archived),
  };
}

const STRUCTURED_LINE = /^(CLAIM|THEOREM|GAP|ACTION|QUESTION|TAG|SOURCE_AI|SOURCE_TYPE|SOURCE_FILE|VISIBILITY|PROJECT|SUMMARY|TITLE|STATUS)\s*:\s*(.+)$/i;

export function parseStructuredPaste(raw) {
  const lines = String(raw || "").split(/\r?\n/);
  const extracted = {
    title: "",
    summary: "",
    source_ai: "unknown",
    source_type: "conversation",
    source_file: "",
    visibility: "professional",
    project_category: "",
    key_claims: [],
    theorems: [],
    open_gaps: [],
    action_items: [],
    open_questions: [],
    search_tags: [],
  };
  const body = [];
  for (const line of lines) {
    const m = line.match(STRUCTURED_LINE);
    if (!m) {
      body.push(line);
      continue;
    }
    const kind = m[1].toUpperCase();
    const value = m[2].trim();
    if (kind === "TITLE") extracted.title = value;
    else if (kind === "SUMMARY") extracted.summary = value;
    else if (kind === "SOURCE_AI" && SOURCE_AIS.includes(value)) extracted.source_ai = value;
    else if (kind === "SOURCE_TYPE" && SOURCE_TYPES.includes(value.toLowerCase())) extracted.source_type = value.toLowerCase();
    else if (kind === "SOURCE_FILE") extracted.source_file = value;
    else if (kind === "VISIBILITY" && VISIBILITY.includes(value.toLowerCase())) extracted.visibility = value.toLowerCase();
    else if (kind === "PROJECT") extracted.project_category = value;
    else if (kind === "TAG") extracted.search_tags.push(value);
    else if (kind === "CLAIM") extracted.key_claims.push(ledgerItem(value, "UNREVIEWED"));
    else if (kind === "THEOREM") extracted.theorems.push(ledgerItem(value, "UNREVIEWED"));
    else if (kind === "GAP") extracted.open_gaps.push(ledgerItem(value, "OPEN"));
    else if (kind === "ACTION") extracted.action_items.push(value);
    else if (kind === "QUESTION") extracted.open_questions.push(value);
    else if (kind === "STATUS") {
      /* status on a following item is ignored here; use reviewEntryItem */
    }
  }
  return { ...extracted, body: body.join("\n").trim() };
}

export function ingestPaste(raw, overrides = {}) {
  const rawText = asString(raw);
  if (!rawText.trim()) {
    throw new Error("Cannot ingest empty text. Raw content is required.");
  }
  const parsed = parseStructuredPaste(rawText);
  const title =
    overrides.title ||
    parsed.title ||
    rawText.split(/\r?\n/).find((l) => l.trim() && !STRUCTURED_LINE.test(l))?.slice(0, 80) ||
    "Untitled";
  const summary = overrides.summary || parsed.summary;
  if (summary && summary === rawText) {
    throw new Error("Summary must not replace raw content.");
  }
  return emptyEntry({
    ...parsed,
    ...overrides,
    title,
    summary,
    raw_content: rawText,
    content_text: parsed.body || rawText,
    extraction_types: [
      parsed.key_claims.length && "claims",
      parsed.theorems.length && "theorems",
      parsed.open_gaps.length && "gaps",
      parsed.action_items.length && "actions",
    ].filter(Boolean),
  });
}

export function reviewLedgerItem(entry, field, itemId, status, { humanReviewed = true } = {}) {
  const nextStatus = humanReviewed ? normalizeStatus(status) : assertNotAutoProved(status, { humanReviewed: false });
  const list = (entry[field] || []).map((item) => {
    if (item.id !== itemId) return item;
    return { ...item, status: nextStatus, human_reviewed: Boolean(humanReviewed && nextStatus === "PROVED") };
  });
  return { ...entry, [field]: list, updated_at: nowIso() };
}

export function updateEntry(entry, patch) {
  const next = emptyEntry({ ...entry, ...patch, id: entry.id, ingested_at: entry.ingested_at });
  if (patch.raw_content != null && patch.raw_content !== entry.raw_content) {
    throw new Error("raw_content is immutable after ingest. Create a new entry instead.");
  }
  next.raw_content = entry.raw_content;
  next.updated_at = nowIso();
  if (next.summary && next.summary === next.raw_content) {
    throw new Error("Summary must not replace raw content.");
  }
  return next;
}

function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .split(/[^a-z0-9π∞=+\-*/^_{}()[\]|]+/i)
    .filter((t) => t.length > 0);
}

function fieldBlob(entry, field) {
  if (field === "raw" || field === "content") return `${entry.raw_content}\n${entry.content_text}`;
  if (field === "title") return entry.title;
  if (field === "summary") return entry.summary;
  if (field === "tag") return [...entry.search_tags, ...entry.project_tags].join(" ");
  if (field === "claim") return (entry.key_claims || []).map((c) => c.text).join(" ");
  if (field === "theorem") return (entry.theorems || []).map((c) => c.text).join(" ");
  if (field === "gap") return (entry.open_gaps || []).map((c) => c.text).join(" ");
  if (field === "question") return (entry.open_questions || []).join(" ");
  if (field === "action") return (entry.action_items || []).join(" ");
  if (field === "source") return `${entry.source_type} ${entry.source_file}`;
  if (field === "ai") return entry.source_ai;
  if (field === "status") {
    return [...(entry.key_claims || []), ...(entry.theorems || []), ...(entry.open_gaps || [])]
      .map((c) => c.status)
      .join(" ");
  }
  if (field === "visibility") return entry.visibility;
  if (field === "all") {
    return [
      entry.title,
      entry.raw_content,
      entry.content_text,
      entry.summary,
      entry.source_ai,
      entry.source_file,
      fieldBlob(entry, "tag"),
      fieldBlob(entry, "claim"),
      fieldBlob(entry, "theorem"),
      fieldBlob(entry, "gap"),
      fieldBlob(entry, "question"),
      fieldBlob(entry, "action"),
    ].join("\n");
  }
  return fieldBlob(entry, "all");
}

function parseQuery(q) {
  const raw = String(q || "").trim();
  if (!raw) return { mode: "empty" };
  const orParts = raw.split(/\s+OR\s+|\s+\|\s+/i);
  if (orParts.length > 1) {
    return { mode: "or", clauses: orParts.map(parseAndClause) };
  }
  return { mode: "and", ...parseAndClause(raw) };
}

function parseAndClause(text) {
  const terms = [];
  const phrases = [];
  const fields = [];
  const re = /(?:(\w+):)?(?:"([^"]+)"|(\S+))/g;
  let m;
  while ((m = re.exec(text))) {
    const field = (m[1] || "all").toLowerCase();
    const phrase = m[2];
    const term = m[3];
    if (phrase) phrases.push({ field, phrase: phrase.toLowerCase() });
    else if (term) terms.push({ field, term: term.toLowerCase() });
  }
  return { terms, phrases };
}

function clauseMatches(entry, clause) {
  for (const p of clause.phrases) {
    const blob = fieldBlob(entry, p.field).toLowerCase();
    if (!blob.includes(p.phrase)) return false;
  }
  for (const t of clause.terms) {
    const blob = fieldBlob(entry, t.field).toLowerCase();
    const tokens = new Set(tokenize(blob));
    if (blob.includes(t.term) || tokens.has(t.term)) continue;
    return false;
  }
  return true;
}

export function searchEntries(entries, query, filters = {}) {
  const parsed = parseQuery(query);
  return (entries || []).filter((entry) => {
    if (entry.archived && !filters.includeArchived) return false;
    if (filters.visibility && entry.visibility !== filters.visibility) return false;
    if (filters.source_ai && entry.source_ai !== filters.source_ai) return false;
    if (filters.source_type && entry.source_type !== filters.source_type) return false;
    if (filters.starred && !entry.starred) return false;
    if (parsed.mode === "empty") return true;
    if (parsed.mode === "or") return parsed.clauses.some((c) => clauseMatches(entry, c));
    return clauseMatches(entry, parsed);
  });
}

export function exportVault(entries, { includePrivate = true } = {}) {
  const payload = (entries || []).filter((e) => includePrivate || e.visibility !== "private");
  return {
    format: "chatvault-export",
    schema_version: SCHEMA_VERSION,
    exported_at: nowIso(),
    count: payload.length,
    entries: payload,
  };
}

export function importVault(payload) {
  if (!payload || payload.format !== "chatvault-export") {
    throw new Error("Not a ChatVault export.");
  }
  return (payload.entries || []).map((e) => emptyEntry(e));
}

export function createStore(initial = []) {
  let entries = initial.map((e) => emptyEntry(e));
  const listeners = new Set();

  function emit() {
    for (const fn of listeners) fn(entries.slice());
  }

  return {
    list() {
      return entries.slice();
    },
    get(id) {
      return entries.find((e) => e.id === id) || null;
    },
    add(entry) {
      const next = emptyEntry(entry);
      entries = [next, ...entries];
      emit();
      return next;
    },
    replaceAfterSuccess(id, next) {
      const idx = entries.findIndex((e) => e.id === id);
      if (idx === -1) throw new Error("Entry not found.");
      entries = entries.slice();
      entries[idx] = next;
      emit();
      return next;
    },
    deleteConfirmed(id) {
      const before = entries.length;
      entries = entries.filter((e) => e.id !== id);
      if (entries.length === before) throw new Error("Delete failed: id not found.");
      emit();
    },
    load(list) {
      entries = (list || []).map((e) => emptyEntry(e));
      emit();
    },
    subscribe(fn) {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
  };
}

export const DEMO_ENTRIES = [
  ingestPaste(
    [
      "TITLE: Euler identity as a definitional fact",
      "SOURCE_AI: Grok",
      "SOURCE_TYPE: conversation",
      "PROJECT: mathematics",
      "TAG: euler",
      "TAG: complex-analysis",
      "CLAIM: e^{iπ} + 1 = 0 is a definitional identity in complex analysis, not an empirical discovery.",
      "THEOREM: Euler's formula e^{iθ} = cos θ + i sin θ for real θ.",
      "GAP: This vault does not treat Euler's identity as a research open problem.",
      "QUESTION: none",
      "SUMMARY: Fixture used to show raw text is kept beside an optional summary.",
      "VISIBILITY: professional",
      "",
      "The identity e^{iπ} + 1 = 0 remains a definitional Euler identity. OPEN question: none.",
    ].join("\n")
  ),
  ingestPaste(
    [
      "TITLE: Spectral regularity for Navier–Stokes — status of the claim",
      "SOURCE_AI: Claude",
      "SOURCE_TYPE: markdown",
      "SOURCE_FILE: ns-notes.md",
      "PROJECT: fluids",
      "TAG: navier-stokes",
      "TAG: millennium",
      "CLAIM: Global regularity of 3D Navier–Stokes on T³ is not established in this vault.",
      "GAP: A complete a-priori bound preventing finite-time blow-up is missing.",
      "ACTION: Keep CLAIM_LEDGER at CONJECTURAL until a human review of a proof.",
      "VISIBILITY: professional",
      "SUMMARY: Research-memory fixture. Do not market as a solved Millennium problem.",
      "",
      "Raw note: any spectral non-concentration argument remains conditional until the analytic gaps are closed. This entry exists so ChatVault can store the claim without promoting it to PROVED.",
    ].join("\n")
  ),
  ingestPaste(
    [
      "TITLE: Private clinical teaching fragment",
      "SOURCE_AI: human",
      "SOURCE_TYPE: conversation",
      "PROJECT: clinical",
      "TAG: teaching",
      "VISIBILITY: private",
      "SUMMARY: Example of the private plane. Not for professional export.",
      "",
      "Private: a teaching mnemonic from OR debrief. Keep this off professional export.",
    ].join("\n")
  ),
];

DEMO_ENTRIES[1] = reviewLedgerItem(
  DEMO_ENTRIES[1],
  "key_claims",
  DEMO_ENTRIES[1].key_claims[0].id,
  "CONJECTURAL",
  { humanReviewed: true }
);
