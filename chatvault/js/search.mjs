/**
 * ChatVault retrieval — BM25F over a fielded inverted index.
 *
 * This is the search engine. Boolean filter lives only as the hard
 * match gate (AND / OR / phrase / field:). Ranking is BM25F with
 * field boosts. Ledger status is displayed, never used as a score.
 *
 * Robertson / Zaragoza BM25F:
 *   tfw(t) = Σ_f  boost_f * tf_{f,t} / ((1-b_f) + b_f * (len_f / avglen_f))
 *   score  = Σ_t  idf(t) * tfw(t) * (k1+1) / (tfw(t) + k1)
 *
 * Not copied from other public “ChatVault” repos. Jonathan’s Replit
 * `search_engine.py` is still missing from this environment.
 */

export const SEARCH_ENGINE_VERSION = "chatvault-bm25f-0.1.0";

export const K1 = 1.2;

export const SEARCH_FIELDS = Object.freeze({
  title: { boost: 4.0, b: 0.4 },
  claim: { boost: 3.6, b: 0.5 },
  theorem: { boost: 3.6, b: 0.5 },
  gap: { boost: 3.2, b: 0.5 },
  question: { boost: 2.4, b: 0.5 },
  action: { boost: 2.0, b: 0.5 },
  tag: { boost: 3.0, b: 0.3 },
  book: { boost: 2.2, b: 0.3 },
  summary: { boost: 1.6, b: 0.7 },
  content: { boost: 1.0, b: 0.75 },
  ai: { boost: 2.8, b: 0.2 },
  status: { boost: 2.4, b: 0.2 },
  source: { boost: 1.4, b: 0.3 },
});

const FIELD_ALIASES = Object.freeze({
  raw: "content",
  body: "content",
  text: "content",
  all: "all",
  claims: "claim",
  theorems: "theorem",
  gaps: "gap",
  questions: "question",
  actions: "action",
  tags: "tag",
  books: "book",
  visibility: "visibility",
});

const PHRASE_BONUS = 2.4;
const SUBSTRING_TF = 0.4;
const SNIPPET_WINDOW = 220;

export function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .split(/[^a-z0-9π∞=+\-*/^_{}()[\]|]+/i)
    .filter((t) => t.length > 0);
}

function asLower(value) {
  return String(value || "").toLowerCase();
}

function ledgerText(items) {
  return (items || []).map((c) => c.text).join(" ");
}

export function fieldText(entry, field) {
  const key = FIELD_ALIASES[field] || field;
  if (key === "content") return `${entry.raw_content || ""}\n${entry.content_text || ""}`;
  if (key === "title") return entry.title || "";
  if (key === "summary") return entry.summary || "";
  if (key === "tag") return [...(entry.search_tags || []), ...(entry.project_tags || [])].join(" ");
  if (key === "claim") return ledgerText(entry.key_claims);
  if (key === "theorem") return ledgerText(entry.theorems);
  if (key === "gap") return ledgerText(entry.open_gaps);
  if (key === "question") return (entry.open_questions || []).join(" ");
  if (key === "action") return (entry.action_items || []).join(" ");
  if (key === "book") return (entry.related_projects || []).join(" ");
  if (key === "source") return `${entry.source_type || ""} ${entry.source_file || ""}`;
  if (key === "ai") return entry.source_ai || "";
  if (key === "status") {
    return [...(entry.key_claims || []), ...(entry.theorems || []), ...(entry.open_gaps || [])]
      .map((c) => c.status)
      .join(" ");
  }
  if (key === "visibility") return entry.visibility || "";
  if (key === "all") {
    return [
      fieldText(entry, "title"),
      fieldText(entry, "content"),
      fieldText(entry, "summary"),
      fieldText(entry, "ai"),
      fieldText(entry, "source"),
      fieldText(entry, "tag"),
      fieldText(entry, "claim"),
      fieldText(entry, "theorem"),
      fieldText(entry, "gap"),
      fieldText(entry, "question"),
      fieldText(entry, "action"),
      fieldText(entry, "book"),
    ].join("\n");
  }
  return fieldText(entry, "all");
}

export function entryFields(entry) {
  const fields = {};
  for (const name of Object.keys(SEARCH_FIELDS)) {
    fields[name] = fieldText(entry, name);
  }
  return fields;
}

function resolveField(name) {
  const raw = asLower(name || "all");
  return FIELD_ALIASES[raw] || raw;
}

export function parseQuery(q) {
  const raw = String(q || "").trim();
  if (!raw) return { mode: "empty", raw };
  const orParts = raw.split(/\s+OR\s+|\s+\|\s+/i);
  if (orParts.length > 1) {
    return { mode: "or", raw, clauses: orParts.map(parseAndClause) };
  }
  return { mode: "and", raw, ...parseAndClause(raw) };
}

function parseAndClause(text) {
  const terms = [];
  const phrases = [];
  const re = /(?:(\w+):)?(?:"([^"]+)"|(\S+))/g;
  let m;
  while ((m = re.exec(text))) {
    const field = resolveField(m[1] || "all");
    const phrase = m[2];
    const term = m[3];
    if (phrase) phrases.push({ field, phrase: phrase.toLowerCase() });
    else if (term) terms.push({ field, term: term.toLowerCase() });
  }
  return { terms, phrases };
}

function fieldHaystack(doc, field) {
  if (field === "all") return doc.allText;
  return asLower(doc.fields[field] || fieldText(doc.entry, field));
}

function termPresent(doc, field, term) {
  const hay = fieldHaystack(doc, field);
  if (hay.includes(term)) return true;
  const tokens = field === "all" ? doc.allTokens : doc.fieldTokens[field] || tokenize(hay);
  return tokens.has ? tokens.has(term) : tokens.includes(term);
}

function clauseMatches(doc, clause) {
  for (const p of clause.phrases) {
    if (!fieldHaystack(doc, p.field).includes(p.phrase)) return false;
  }
  for (const t of clause.terms) {
    if (!termPresent(doc, t.field, t.term)) return false;
  }
  return true;
}

function queryMatches(doc, parsed) {
  if (parsed.mode === "empty") return true;
  if (parsed.mode === "or") return parsed.clauses.some((c) => clauseMatches(doc, c));
  return clauseMatches(doc, parsed);
}

function passesFilters(entry, filters = {}) {
  if (entry.archived && !filters.includeArchived) return false;
  if (filters.visibility && entry.visibility !== filters.visibility) return false;
  if (filters.source_ai && entry.source_ai !== filters.source_ai) return false;
  if (filters.source_type && entry.source_type !== filters.source_type) return false;
  if (filters.project && entry.project_category !== filters.project) return false;
  if (filters.starred && !entry.starred) return false;
  const tagFilter = filters.tag ? String(filters.tag).toLowerCase() : "";
  if (tagFilter) {
    const tags = [...(entry.search_tags || []), ...(entry.project_tags || [])].map((t) =>
      String(t).toLowerCase()
    );
    if (!tags.includes(tagFilter)) return false;
  }
  const bookFilter = filters.book ? String(filters.book).toLowerCase() : "";
  if (bookFilter) {
    const books = (entry.related_projects || []).map((b) => String(b).toLowerCase());
    if (bookFilter === "(unfiled)") {
      if (books.length) return false;
    } else if (!books.includes(bookFilter)) {
      return false;
    }
  }
  return true;
}

function fieldTermFrequency(doc, field, term) {
  const tfMap = doc.fieldTfs[field] || {};
  if (tfMap[term]) return tfMap[term];
  let n = 0;
  for (const tok of Object.keys(tfMap)) {
    if (tok.includes(term)) n += 1;
  }
  return n ? n * SUBSTRING_TF : 0;
}

export function idf(term, index) {
  const n = index.df.get(term) || 0;
  return Math.log(1 + (index.N - n + 0.5) / (n + 0.5));
}

function weightedTf(doc, index, term, allowedFields) {
  let tfw = 0;
  for (const field of allowedFields) {
    const cfg = SEARCH_FIELDS[field];
    if (!cfg) continue;
    const tf = fieldTermFrequency(doc, field, term);
    if (!tf) continue;
    const len = doc.lengths[field] || 0;
    const avg = index.avgLen[field] || 1;
    const norm = 1 - cfg.b + cfg.b * (len / Math.max(avg, 1e-9));
    tfw += (cfg.boost * tf) / Math.max(norm, 1e-9);
  }
  return tfw;
}

function fieldsForTerm(field) {
  if (!field || field === "all") return Object.keys(SEARCH_FIELDS);
  return SEARCH_FIELDS[field] ? [field] : Object.keys(SEARCH_FIELDS);
}

function scoreClause(doc, index, clause) {
  let score = 0;
  const matched = new Set();
  for (const t of clause.terms) {
    const fields = fieldsForTerm(t.field);
    const tfw = weightedTf(doc, index, t.term, fields);
    if (tfw > 0) {
      score += idf(t.term, index) * ((tfw * (K1 + 1)) / (tfw + K1));
      for (const f of fields) {
        if (fieldTermFrequency(doc, f, t.term) > 0) matched.add(f);
      }
    }
  }
  for (const p of clause.phrases) {
    const fields = fieldsForTerm(p.field);
    const phraseTokens = tokenize(p.phrase);
    let phraseTfw = 0;
    for (const field of fields) {
      const hay = asLower(doc.fields[field] || "");
      if (!hay.includes(p.phrase)) continue;
      matched.add(field);
      const cfg = SEARCH_FIELDS[field];
      const len = doc.lengths[field] || 0;
      const avg = index.avgLen[field] || 1;
      const norm = 1 - cfg.b + cfg.b * (len / Math.max(avg, 1e-9));
      phraseTfw += cfg.boost / Math.max(norm, 1e-9);
    }
    if (phraseTfw > 0) {
      const pivot = phraseTokens[0] || p.phrase;
      score += PHRASE_BONUS * idf(pivot, index) * ((phraseTfw * (K1 + 1)) / (phraseTfw + K1));
    }
    for (const tok of phraseTokens) {
      const fields = fieldsForTerm(p.field);
      const tfw = weightedTf(doc, index, tok, fields);
      if (tfw > 0) score += idf(tok, index) * ((tfw * (K1 + 1)) / (tfw + K1));
    }
  }
  return { score, matched_fields: [...matched] };
}

function scoreDocument(doc, index, parsed) {
  if (parsed.mode === "empty") return { score: 0, matched_fields: [] };
  if (parsed.mode === "or") {
    let best = { score: 0, matched_fields: [] };
    for (const clause of parsed.clauses) {
      if (!clauseMatches(doc, clause)) continue;
      const next = scoreClause(doc, index, clause);
      if (next.score > best.score) best = next;
    }
    return best;
  }
  return scoreClause(doc, index, parsed);
}

function collectNeedles(parsed) {
  const needles = [];
  const clauses = parsed.mode === "or" ? parsed.clauses : parsed.mode === "and" ? [parsed] : [];
  for (const clause of clauses) {
    for (const t of clause.terms || []) needles.push(t.term);
    for (const p of clause.phrases || []) needles.push(p.phrase);
  }
  return [...new Set(needles.filter((n) => n && n.length > 1 || n === "e" || n === "π"))].filter(Boolean);
}

function locateAll(hay, needle) {
  const hits = [];
  if (!needle) return hits;
  let from = 0;
  while (from < hay.length) {
    const i = hay.indexOf(needle, from);
    if (i === -1) break;
    hits.push([i, i + needle.length]);
    from = i + Math.max(needle.length, 1);
  }
  return hits;
}

export function bestWindow(text, needles, window = SNIPPET_WINDOW) {
  const raw = String(text || "");
  const hay = raw.toLowerCase();
  const hits = [];
  for (const n of needles) {
    hits.push(...locateAll(hay, n));
  }
  if (!hits.length) {
    const slice = raw.slice(0, window);
    return { text: slice, marks: [] };
  }
  hits.sort((a, b) => a[0] - b[0]);
  let bestStart = Math.max(0, hits[0][0] - 36);
  let bestCount = -1;
  for (const [start] of hits) {
    const winStart = Math.max(0, start - 36);
    const winEnd = winStart + window;
    const count = hits.filter((h) => h[0] >= winStart && h[1] <= winEnd).length;
    if (count > bestCount) {
      bestCount = count;
      bestStart = winStart;
    }
  }
  const end = Math.min(raw.length, bestStart + window);
  if (end - bestStart < window && raw.length > window) {
    bestStart = Math.max(0, raw.length - window);
  }
  const slice = raw.slice(bestStart, Math.min(raw.length, bestStart + window));
  const marks = [];
  const sliceHay = slice.toLowerCase();
  for (const n of needles) {
    for (const [s, e] of locateAll(sliceHay, n)) marks.push([s, e]);
  }
  marks.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const prefix = bestStart > 0 ? "…" : "";
  const suffix = bestStart + slice.length < raw.length ? "…" : "";
  const shifted = marks.map(([s, e]) => [s + prefix.length, e + prefix.length]);
  return { text: `${prefix}${slice}${suffix}`, marks: shifted };
}

function ledgerSnippets(items, field, needles) {
  const out = [];
  for (const item of items || []) {
    const text = item.text || "";
    if (!needles.some((n) => text.toLowerCase().includes(n))) continue;
    const win = bestWindow(text, needles);
    out.push({
      field,
      text: win.text,
      marks: win.marks,
      ledger_status: item.status || null,
    });
  }
  return out;
}

function buildSnippets(entry, needles) {
  if (!needles.length) return [];
  const snippets = [];
  snippets.push(...ledgerSnippets(entry.key_claims, "claim", needles));
  snippets.push(...ledgerSnippets(entry.theorems, "theorem", needles));
  snippets.push(...ledgerSnippets(entry.open_gaps, "gap", needles));
  const plain = [
    ["title", entry.title],
    ["summary", entry.summary],
    ["content", `${entry.content_text || ""}\n${entry.raw_content || ""}`],
    ["tag", [...(entry.search_tags || []), ...(entry.project_tags || [])].join(" ")],
    ["question", (entry.open_questions || []).join(" ")],
    ["action", (entry.action_items || []).join(" ")],
  ];
  for (const [field, text] of plain) {
    if (!text) continue;
    const lower = text.toLowerCase();
    if (!needles.some((n) => lower.includes(n))) continue;
    const win = bestWindow(text, needles);
    snippets.push({ field, text: win.text, marks: win.marks, ledger_status: null });
  }
  const rank = (s) => (SEARCH_FIELDS[s.field]?.boost || 1) * (1 + s.marks.length) + (s.ledger_status ? 0.25 : 0);
  snippets.sort((a, b) => rank(b) - rank(a));
  const seen = new Set();
  const unique = [];
  for (const s of snippets) {
    const key = `${s.field}:${s.text}`;
    if (seen.has(key)) continue;
    seen.add(key);
    unique.push(s);
    if (unique.length === 2) break;
  }
  return unique;
}

export function buildIndex(entries) {
  const docs = [];
  const df = new Map();
  const fieldLens = {};
  const fieldCounts = {};

  for (const entry of entries || []) {
    const fields = entryFields(entry);
    const fieldTfs = {};
    const fieldTokens = {};
    const lengths = {};
    const unique = new Set();
    for (const [field, text] of Object.entries(fields)) {
      const tokens = tokenize(text);
      lengths[field] = tokens.length;
      fieldLens[field] = (fieldLens[field] || 0) + tokens.length;
      fieldCounts[field] = (fieldCounts[field] || 0) + 1;
      const tf = {};
      for (const tok of tokens) {
        tf[tok] = (tf[tok] || 0) + 1;
        unique.add(tok);
      }
      fieldTfs[field] = tf;
      fieldTokens[field] = new Set(tokens);
    }
    for (const tok of unique) {
      df.set(tok, (df.get(tok) || 0) + 1);
    }
    const allText = asLower(fieldText(entry, "all"));
    docs.push({
      entry,
      fields,
      fieldTfs,
      fieldTokens,
      lengths,
      allText,
      allTokens: new Set(tokenize(allText)),
    });
  }

  const avgLen = {};
  for (const field of Object.keys(SEARCH_FIELDS)) {
    avgLen[field] = (fieldLens[field] || 0) / Math.max(1, fieldCounts[field] || 1);
  }

  return { N: docs.length, docs, df, avgLen, built_at: Date.now() };
}

function tieBreak(entry) {
  const t = Date.parse(entry.ingested_at || "") || 0;
  return t / 1e15;
}

export function searchVault(entries, query, filters = {}, { index } = {}) {
  const started = nowMs();
  const parsed = parseQuery(query);
  const idx = index || buildIndex(entries || []);
  const needles = collectNeedles(parsed);
  const hits = [];
  for (const doc of idx.docs) {
    if (!passesFilters(doc.entry, filters)) continue;
    if (!queryMatches(doc, parsed)) continue;
    const { score, matched_fields } = scoreDocument(doc, idx, parsed);
    hits.push({
      entry: doc.entry,
      score: parsed.mode === "empty" ? 0 : score + tieBreak(doc.entry),
      snippets: parsed.mode === "empty" ? [] : buildSnippets(doc.entry, needles),
      matched_fields,
    });
  }
  if (parsed.mode === "empty") {
    /* preserve store order */
  } else {
    hits.sort((a, b) => b.score - a.score || String(a.entry.title).localeCompare(String(b.entry.title)));
  }
  return {
    engine: SEARCH_ENGINE_VERSION,
    parsed,
    took_ms: Math.max(0, nowMs() - started),
    total: hits.length,
    hits,
  };
}

export function searchEntries(entries, query, filters = {}, options) {
  return searchVault(entries, query, filters, options).hits.map((h) => h.entry);
}

export function ndcgAt(rankedIds, grades, k = 5) {
  const limit = Math.min(k, rankedIds.length);
  let dcg = 0;
  for (let i = 0; i < limit; i += 1) {
    const rel = grades[rankedIds[i]] || 0;
    dcg += (2 ** rel - 1) / Math.log2(i + 2);
  }
  const ideal = Object.values(grades)
    .filter((g) => g > 0)
    .sort((a, b) => b - a)
    .slice(0, k);
  let idcg = 0;
  for (let i = 0; i < ideal.length; i += 1) {
    idcg += (2 ** ideal[i] - 1) / Math.log2(i + 2);
  }
  return idcg === 0 ? 0 : dcg / idcg;
}

export function mrr(rankedIds, grades) {
  for (let i = 0; i < rankedIds.length; i += 1) {
    if ((grades[rankedIds[i]] || 0) >= 3) return 1 / (i + 1);
  }
  for (let i = 0; i < rankedIds.length; i += 1) {
    if ((grades[rankedIds[i]] || 0) > 0) return 1 / (i + 1);
  }
  return 0;
}

function nowMs() {
  return typeof performance !== "undefined" && performance.now ? performance.now() : Date.now();
}
