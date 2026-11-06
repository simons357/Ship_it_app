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

export {
  SEARCH_ENGINE_VERSION,
  searchVault,
  searchEntries,
  buildIndex,
  parseQuery,
} from "./search.mjs";

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
  ingestPaste(
    [
      "TITLE: ChatVault is a constellation, not a notebook",
      "SOURCE_AI: Grok",
      "SOURCE_TYPE: markdown",
      "PROJECT: product",
      "TAG: chatvault",
      "TAG: atlas",
      "CLAIM: The product surface is a ranked sky of records, not an Evernote notebook stack.",
      "GAP: Pixel-perfect morph-glass from Base44 is not copied into this engine.",
      "ACTION: Keep search as BM25F + n-grams + cosine fused by RRF. Do not add an LLM that invents ranks.",
      "VISIBILITY: professional",
      "SUMMARY: Fixture describing the UI contract. Not a shipped store listing.",
      "",
      "Notebooks hide structure. ChatVault shows claims, theorems, and gaps as mass on a star. Shared tags draw edges. Search is a beam, not a filter chip.",
    ].join("\n")
  ),
  ingestPaste(
    [
      "TITLE: Apple 4.2 — PWA first, no Base44 wrapper",
      "SOURCE_AI: human",
      "SOURCE_TYPE: markdown",
      "PROJECT: apple",
      "TAG: pwa",
      "TAG: guideline-4-2",
      "CLAIM: A full-screen WebView of a remote Base44 URL will be rejected under Guideline 4.2.",
      "ACTION: Safari Share then Add to Home Screen. No App Store submission on this personal vault.",
      "VISIBILITY: professional",
      "SUMMARY: Product-policy fixture. Apple Developer membership exists; listing does not.",
      "",
      "Membership is not permission to wrap preview--6a58e103fedcde66a0a7710e.base44.app. Private TestFlight only after a genuine native layer.",
    ].join("\n")
  ),
  ingestPaste(
    [
      "TITLE: CLAIM_LEDGER never auto-PROVED",
      "SOURCE_AI: Claude",
      "SOURCE_TYPE: conversation",
      "PROJECT: product",
      "TAG: ledger",
      "TAG: chatvault",
      "CLAIM: Ingest and extractors may not mark PROVED. Only an explicit human review path may.",
      "THEOREM: Status is a designation, never a ranking signal.",
      "GAP: Dense MiniLM/E5 + cross-encoder is not in this build; RRF has a slot for it later.",
      "VISIBILITY: professional",
      "SUMMARY: Engine invariant fixture.",
      "",
      "Ledger status, harmonic notes, and lattice scores are display. Retrieval is lexical hybrid search. That split is the product.",
    ].join("\n")
  ),
  ingestPaste(
    [
      "TITLE: No-hassle personal vault",
      "SOURCE_AI: human",
      "SOURCE_TYPE: markdown",
      "PROJECT: policy",
      "TAG: privacy",
      "TAG: pwa",
      "CLAIM: ChatVault stays local-first with no support inbox and no public store listing.",
      "ACTION: Do not circulate the Base44 preview URL; it is world-writable.",
      "VISIBILITY: private",
      "SUMMARY: Policy fixture on the private plane.",
      "",
      "Owner constraint: I don’t want people hassling me. That forbids Stripe, App Store pages, and a contact form.",
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
