/**
 * ChatVault engine — local-first knowledge capture.
 *
 * Competitive core: provenance, immutable raw text, CLAIM_LEDGER
 * statuses that never auto-promote to PROVED, and BM25F fielded
 * retrieval (AND / OR / phrase / field:). This is not a truth engine
 * and not an LLM.
 */

export {
  SEARCH_ENGINE_VERSION,
  searchEntries,
  searchVault,
  parseQuery,
  tokenize,
  buildIndex,
  ndcgAt,
} from "./search.mjs";

export const SCHEMA_VERSION = "chatvault-engine-0.2.0";

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
  "html",
  "other",
]);

export const VISIBILITY = Object.freeze(["private", "professional"]);

const SAFE_ID = /^[A-Za-z0-9._-]{1,80}$/;
const TEXT_FILE = /\.(txt|md|markdown|json|csv|html|htm)$/i;

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

export function safeId(value, prefix = "id") {
  const s = asString(value).trim();
  return SAFE_ID.test(s) ? s : uid(prefix);
}

export function normalizeStatus(status) {
  const s = String(status || "UNREVIEWED").toUpperCase();
  return LEDGER_STATUSES.includes(s) ? s : "UNREVIEWED";
}

export function statusClass(status) {
  return normalizeStatus(status).toLowerCase();
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

export function ledgerItem(text, status = "UNREVIEWED", { humanReviewed } = {}) {
  const normalized = assertNotAutoProved(status, { humanReviewed });
  return {
    id: uid("lg"),
    text: asString(text).trim(),
    status: normalized,
    human_reviewed: Boolean(humanReviewed && normalized === "PROVED"),
  };
}

function normalizeLedgerObject(item, defaultStatus = "UNREVIEWED") {
  if (typeof item === "string") {
    return ledgerItem(item, defaultStatus, { humanReviewed: false });
  }
  const humanReviewed = Boolean(item && item.human_reviewed);
  const next = ledgerItem(
    item?.text,
    item?.status || defaultStatus,
    { humanReviewed }
  );
  if (item?.id) next.id = safeId(item.id, "lg");
  return next;
}

export function emptyEntry(partial = {}) {
  const ingested = asString(partial.ingested_at, nowIso());
  return {
    schema_version: SCHEMA_VERSION,
    id: safeId(partial.id, "ent"),
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
    key_claims: (partial.key_claims || []).map((c) => normalizeLedgerObject(c, "UNREVIEWED")),
    theorems: (partial.theorems || []).map((c) => normalizeLedgerObject(c, "UNREVIEWED")),
    open_gaps: (partial.open_gaps || []).map((c) => normalizeLedgerObject(c, "OPEN")),
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

const STRUCTURED_LINE =
  /^(CLAIM|THEOREM|GAP|ACTION|QUESTION|TAG|BOOK|SOURCE_AI|SOURCE_TYPE|SOURCE_FILE|VISIBILITY|PROJECT|SUMMARY|TITLE|STATUS)\s*:\s*(.+)$/i;

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
    related_projects: [],
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
    else if (kind === "SOURCE_TYPE" && SOURCE_TYPES.includes(value.toLowerCase())) {
      extracted.source_type = value.toLowerCase();
    } else if (kind === "SOURCE_FILE") extracted.source_file = value;
    else if (kind === "VISIBILITY" && VISIBILITY.includes(value.toLowerCase())) {
      extracted.visibility = value.toLowerCase();
    } else if (kind === "PROJECT") extracted.project_category = value;
    else if (kind === "TAG") extracted.search_tags.push(value);
    else if (kind === "BOOK") extracted.related_projects.push(value);
    else if (kind === "CLAIM") extracted.key_claims.push(ledgerItem(value, "UNREVIEWED"));
    else if (kind === "THEOREM") extracted.theorems.push(ledgerItem(value, "UNREVIEWED"));
    else if (kind === "GAP") extracted.open_gaps.push(ledgerItem(value, "OPEN"));
    else if (kind === "ACTION") extracted.action_items.push(value);
    else if (kind === "QUESTION") extracted.open_questions.push(value);
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
  const sourceAi =
    overrides.source_ai && overrides.source_ai !== "unknown"
      ? overrides.source_ai
      : parsed.source_ai;
  const visibility = overrides.visibility || parsed.visibility;
  return emptyEntry({
    ...parsed,
    ...overrides,
    title,
    summary,
    source_ai: sourceAi,
    visibility,
    raw_content: rawText,
    content_text: parsed.body || rawText,
    related_projects: overrides.related_projects || parsed.related_projects,
    search_tags: [...parsed.search_tags, ...asArray(overrides.search_tags)],
    extraction_types: [
      parsed.key_claims.length && "claims",
      parsed.theorems.length && "theorems",
      parsed.open_gaps.length && "gaps",
      parsed.action_items.length && "actions",
    ].filter(Boolean),
  });
}

export function ingestBulk(raw, overrides = {}) {
  const chunks = String(raw || "").split(/\n(?:---+|===+)\n/);
  const entries = [];
  const errors = [];
  chunks.forEach((chunk, index) => {
    if (!String(chunk).trim()) return;
    try {
      entries.push(ingestPaste(chunk, overrides));
    } catch (err) {
      errors.push({ index, message: err.message || String(err) });
    }
  });
  if (!entries.length) {
    throw new Error("Bulk ingest found no usable chunks. Separate records with a line of ---.");
  }
  return { entries, errors };
}

function sourceTypeFromName(filename) {
  const lower = asString(filename).toLowerCase();
  if (lower.endsWith(".md") || lower.endsWith(".markdown")) return "markdown";
  if (lower.endsWith(".json")) return "json";
  if (lower.endsWith(".csv")) return "csv";
  if (lower.endsWith(".html") || lower.endsWith(".htm")) return "html";
  return "conversation";
}

export function ingestTextFile(filename, text, overrides = {}) {
  const name = asString(filename);
  if (!TEXT_FILE.test(name)) {
    throw new Error(`Unsupported file type: ${name || "(unnamed)"}. Use txt, md, json, csv, or html.`);
  }
  const trimmed = asString(text);
  if (name.toLowerCase().endsWith(".json")) {
    try {
      const parsed = JSON.parse(trimmed);
      if (parsed && parsed.format === "chatvault-export") {
        return { kind: "bundle", entries: importVault(parsed), errors: [] };
      }
    } catch (err) {
      if (err && err.message && err.message.startsWith("Not a ChatVault")) throw err;
      /* fall through: treat as a pasted JSON conversation */
    }
  }
  return {
    kind: "entry",
    entries: [
      ingestPaste(trimmed, {
        ...overrides,
        source_file: name,
        source_type: overrides.source_type || sourceTypeFromName(name),
      }),
    ],
    errors: [],
  };
}

export function reviewLedgerItem(entry, field, itemId, status, { humanReviewed = true } = {}) {
  const nextStatus = humanReviewed
    ? normalizeStatus(status)
    : assertNotAutoProved(status, { humanReviewed: false });
  const list = (entry[field] || []).map((item) => {
    if (item.id !== itemId) return item;
    return {
      ...item,
      status: nextStatus,
      human_reviewed: Boolean(humanReviewed && nextStatus === "PROVED"),
    };
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

export function listTags(entries) {
  const map = new Map();
  for (const entry of entries || []) {
    for (const tag of [...(entry.search_tags || []), ...(entry.project_tags || [])]) {
      const key = String(tag).trim();
      if (!key) continue;
      const rec = map.get(key.toLowerCase()) || { tag: key, count: 0, ids: [] };
      rec.count += 1;
      rec.ids.push(entry.id);
      map.set(key.toLowerCase(), rec);
    }
  }
  return [...map.values()].sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
}

export function listBooks(entries) {
  const map = new Map();
  for (const entry of entries || []) {
    const books = (entry.related_projects || []).map((b) => String(b).trim()).filter(Boolean);
    if (!books.length) {
      const rec = map.get("(unfiled)") || { name: "(unfiled)", count: 0, ids: [] };
      rec.count += 1;
      rec.ids.push(entry.id);
      map.set("(unfiled)", rec);
      continue;
    }
    for (const name of books) {
      const rec = map.get(name.toLowerCase()) || { name, count: 0, ids: [] };
      rec.count += 1;
      rec.ids.push(entry.id);
      map.set(name.toLowerCase(), rec);
    }
  }
  return [...map.values()].sort((a, b) => {
    if (a.name === "(unfiled)") return 1;
    if (b.name === "(unfiled)") return -1;
    return b.count - a.count || a.name.localeCompare(b.name);
  });
}

export function listArtifacts(entries) {
  const out = [];
  for (const entry of entries || []) {
    for (const [kind, field] of [
      ["claim", "key_claims"],
      ["theorem", "theorems"],
      ["gap", "open_gaps"],
    ]) {
      for (const item of entry[field] || []) {
        out.push({
          id: item.id,
          kind,
          text: item.text,
          status: item.status,
          entry_id: entry.id,
          entry_title: entry.title,
          source_ai: entry.source_ai,
        });
      }
    }
    (entry.action_items || []).forEach((text, index) => {
      out.push({
        id: `${entry.id}-action-${index}`,
        kind: "action",
        text,
        status: "OPEN",
        entry_id: entry.id,
        entry_title: entry.title,
        source_ai: entry.source_ai,
      });
    });
  }
  return out;
}

export function vaultStats(entries) {
  const list = entries || [];
  const by_ai = {};
  const by_status = {};
  const by_visibility = { private: 0, professional: 0 };
  const by_project = {};
  let starred = 0;
  let claims = 0;
  let theorems = 0;
  let gaps = 0;
  for (const entry of list) {
    by_ai[entry.source_ai] = (by_ai[entry.source_ai] || 0) + 1;
    by_visibility[entry.visibility] = (by_visibility[entry.visibility] || 0) + 1;
    if (entry.starred) starred += 1;
    if (entry.project_category) {
      by_project[entry.project_category] = (by_project[entry.project_category] || 0) + 1;
    }
    for (const item of [...(entry.key_claims || []), ...(entry.theorems || []), ...(entry.open_gaps || [])]) {
      by_status[item.status] = (by_status[item.status] || 0) + 1;
    }
    claims += (entry.key_claims || []).length;
    theorems += (entry.theorems || []).length;
    gaps += (entry.open_gaps || []).length;
  }
  return {
    total: list.length,
    starred,
    private: by_visibility.private || 0,
    professional: by_visibility.professional || 0,
    claims,
    theorems,
    gaps,
    tags: listTags(list).length,
    books: listBooks(list).filter((b) => b.name !== "(unfiled)").length,
    artifacts: listArtifacts(list).length,
    by_ai,
    by_status,
    by_visibility,
    by_project,
  };
}

export function uniqueProjects(entries) {
  return [...new Set((entries || []).map((e) => e.project_category).filter(Boolean))].sort();
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
    addMany(list) {
      const next = (list || []).map((e) => emptyEntry(e));
      entries = [...next, ...entries];
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
      "BOOK: Research & Ideas",
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
      "BOOK: Research & Ideas",
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
      "BOOK: Clinical Notes",
      "TAG: teaching",
      "VISIBILITY: private",
      "SUMMARY: Example of the private plane. Not for professional export.",
      "",
      "Private: a teaching mnemonic from OR debrief. Keep this off professional export.",
    ].join("\n")
  ),
];

DEMO_ENTRIES[0] = updateEntry(DEMO_ENTRIES[0], { starred: true });
DEMO_ENTRIES[1] = reviewLedgerItem(
  DEMO_ENTRIES[1],
  "key_claims",
  DEMO_ENTRIES[1].key_claims[0].id,
  "CONJECTURAL",
  { humanReviewed: true }
);
