/**
 * ChatVault retrieval — hybrid ranker.
 *
 * Pipeline:
 *   1. Fielded inverted index
 *   2. BM25F (Robertson / Zaragoza) on words, stems, and one-edit typos
 *   3. Character 3-gram BM25 (hyphens, misspellings)
 *   4. Field-weighted TF-IDF cosine (second vector signal)
 *   5. Reciprocal Rank Fusion, k=60
 *   6. RM3 expansion from the top hits, fused again
 *
 * Boolean syntax is only the match gate (AND / OR / phrase / field:).
 * Ledger status is displayed and is never a ranking signal.
 * `harmonic_note` (Base44 Harmonic Watch copy) is never indexed or scored.
 * E8 / lattice ranking is not implemented.
 *
 * This is the strongest stack that stays local, offline, and model-free.
 * A MiniLM/E5 + cross-encoder layer can plug into the same RRF later;
 * an LLM “semantic” toggle that invents ranks is a regression.
 */

export const SEARCH_ENGINE_VERSION = "chatvault-hybrid-0.2.0";

export const K1 = 1.2;
export const RRF_K = 60;

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
  origin: { boost: 2.4, b: 0.2 },
});

/** Unfielded rank uses these. `status:` and `origin:` are designations, not quality boosts. */
export const RANK_FIELDS = Object.freeze(
  Object.fromEntries(
    Object.entries(SEARCH_FIELDS).filter(([name]) => name !== "status" && name !== "origin")
  )
);

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
  real: "origin",
  designation: "origin",
});

const PHRASE_BONUS = 2.4;
const SUBSTRING_TF = 0.4;
const STEM_TF = 0.85;
const FUZZY_TF = 0.65;
const SNIPPET_WINDOW = 220;
const NGRAM = 3;

export function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .split(/[^a-z0-9π∞=+\-*/^_{}()[\]|]+/i)
    .filter((t) => t.length > 0);
}

export function stem(word) {
  let w = String(word || "").toLowerCase();
  if (w.length <= 4) return w;
  if (w.endsWith("ational") && w.length > 9) return `${w.slice(0, -7)}ate`;
  if (w.endsWith("tional") && w.length > 8) return `${w.slice(0, -6)}tion`;
  if (w.endsWith("ies") && w.length > 5) w = `${w.slice(0, -3)}y`;
  else if (w.endsWith("sses")) w = w.slice(0, -2);
  else if (w.endsWith("s") && !w.endsWith("ss") && w.length > 4) w = w.slice(0, -1);
  if (w.endsWith("ing") && w.length > 6) {
    w = w.slice(0, -3);
    if (/(.)\1$/.test(w) && w.length > 3) w = w.slice(0, -1);
  } else if (w.endsWith("ed") && w.length > 5) {
    w = w.slice(0, -2);
    if (/(.)\1$/.test(w) && w.length > 3) w = w.slice(0, -1);
  }
  if (w.endsWith("er") && w.length > 6) w = w.slice(0, -2);
  return w;
}

export function editDistanceAtMost(a, b, max = 1) {
  const s = String(a);
  const t = String(b);
  if (s === t) return true;
  if (Math.abs(s.length - t.length) > max) return false;
  if (max === 1) {
    if (s.length === t.length) {
      let diff = 0;
      for (let i = 0; i < s.length; i += 1) {
        if (s[i] !== t[i] && ++diff > 1) return false;
      }
      return diff === 1;
    }
    const longer = s.length > t.length ? s : t;
    const shorter = s.length > t.length ? t : s;
    let i = 0;
    let j = 0;
    let skipped = 0;
    while (i < longer.length && j < shorter.length) {
      if (longer[i] === shorter[j]) {
        i += 1;
        j += 1;
      } else {
        skipped += 1;
        if (skipped > 1) return false;
        i += 1;
      }
    }
    return true;
  }
  const prev = new Array(t.length + 1);
  for (let j = 0; j <= t.length; j += 1) prev[j] = j;
  for (let i = 1; i <= s.length; i += 1) {
    let last = prev[0];
    prev[0] = i;
    let rowMin = prev[0];
    for (let j = 1; j <= t.length; j += 1) {
      const cur = s[i - 1] === t[j - 1] ? last : Math.min(last, prev[j], prev[j - 1]) + 1;
      last = prev[j];
      prev[j] = cur;
      if (cur < rowMin) rowMin = cur;
    }
    if (rowMin > max) return false;
  }
  return prev[t.length] <= max;
}

export function charNgrams(text, n = NGRAM) {
  const s = ` ${String(text || "").toLowerCase().replace(/\s+/g, " ").trim()} `;
  if (s.length <= n) return s.trim() ? [s] : [];
  const out = [];
  for (let i = 0; i <= s.length - n; i += 1) out.push(s.slice(i, i + n));
  return out;
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
  if (key === "origin") return entry.origin_class || "";
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

function normalizeFieldTerm(field, term) {
  if (field !== "origin") return term;
  if (term === "ai" || term === "generated" || term === "ai_generated") return "ai_generated";
  if (term === "human" || term === "real" || term === "record" || term === "human_record") {
    return "human_record";
  }
  return term;
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
    if (phrase) phrases.push({ field, phrase: normalizeFieldTerm(field, phrase.toLowerCase()) });
    else if (term) terms.push({ field, term: normalizeFieldTerm(field, term.toLowerCase()) });
  }
  return { terms, phrases };
}

function fieldHaystack(doc, field) {
  if (field === "all") return doc.allText;
  return asLower(doc.fields[field] || fieldText(doc.entry, field));
}

function tokenSet(doc, field) {
  if (field === "all") return doc.allTokens;
  return doc.fieldTokens[field] || new Set();
}

function termPresent(doc, field, term) {
  const hay = fieldHaystack(doc, field);
  if (hay.includes(term)) return true;
  const tokens = tokenSet(doc, field);
  if (tokens.has(term)) return true;
  const wanted = stem(term);
  if (wanted.length >= 4) {
    for (const tok of tokens) {
      if (stem(tok) === wanted) return true;
    }
  }
  if (term.length >= 4) {
    for (const tok of tokens) {
      if (Math.abs(tok.length - term.length) > 1) continue;
      if (editDistanceAtMost(term, tok, 1)) return true;
    }
  }
  return false;
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
  if (filters.origin_class && entry.origin_class !== filters.origin_class) return false;
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
  if (tfMap[term]) return { tf: tfMap[term], weight: 1, matched: term };
  let n = 0;
  for (const tok of Object.keys(tfMap)) {
    if (tok.includes(term)) n += 1;
  }
  if (n) return { tf: n * SUBSTRING_TF, weight: SUBSTRING_TF, matched: term };
  const wanted = stem(term);
  if (wanted.length >= 4) {
    let stemTf = 0;
    let matched = term;
    for (const [tok, tf] of Object.entries(tfMap)) {
      if (stem(tok) === wanted) {
        stemTf += tf;
        matched = tok;
      }
    }
    if (stemTf) return { tf: stemTf * STEM_TF, weight: STEM_TF, matched };
  }
  if (term.length >= 4) {
    for (const [tok, tf] of Object.entries(tfMap)) {
      if (Math.abs(tok.length - term.length) > 1) continue;
      if (editDistanceAtMost(term, tok, 1)) {
        return { tf: tf * FUZZY_TF, weight: FUZZY_TF, matched: tok };
      }
    }
  }
  return { tf: 0, weight: 0, matched: term };
}

export function idf(term, index) {
  const n = index.df.get(term) || index.stemDf.get(stem(term)) || 0;
  return Math.log(1 + (index.N - n + 0.5) / (n + 0.5));
}

function ngramIdf(gram, index) {
  const n = index.ngramDf.get(gram) || 0;
  return Math.log(1 + (index.N - n + 0.5) / (n + 0.5));
}

function weightedTf(doc, index, term, allowedFields) {
  let tfw = 0;
  for (const field of allowedFields) {
    const cfg = SEARCH_FIELDS[field];
    if (!cfg) continue;
    const { tf } = fieldTermFrequency(doc, field, term);
    if (!tf) continue;
    const len = doc.lengths[field] || 0;
    const avg = index.avgLen[field] || 1;
    const norm = 1 - cfg.b + cfg.b * (len / Math.max(avg, 1e-9));
    tfw += (cfg.boost * tf) / Math.max(norm, 1e-9);
  }
  return tfw;
}

function fieldsForTerm(field) {
  if (!field || field === "all") return Object.keys(RANK_FIELDS);
  if (field === "status") return ["status"];
  return SEARCH_FIELDS[field] ? [field] : Object.keys(RANK_FIELDS);
}

function bm25FromTfw(tfw, term, index) {
  if (tfw <= 0) return 0;
  return idf(term, index) * ((tfw * (K1 + 1)) / (tfw + K1));
}

function scoreClause(doc, index, clause) {
  let score = 0;
  const matched = new Set();
  for (const t of clause.terms) {
    const fields = fieldsForTerm(t.field);
    const tfw = weightedTf(doc, index, t.term, fields);
    if (tfw > 0) {
      score += bm25FromTfw(tfw, t.term, index);
      for (const f of fields) {
        if (fieldTermFrequency(doc, f, t.term).tf > 0) matched.add(f);
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
      const tfw = weightedTf(doc, index, tok, fields);
      if (tfw > 0) score += bm25FromTfw(tfw, tok, index);
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

function clauseNgrams(clause) {
  const grams = [];
  for (const t of clause.terms) grams.push(...charNgrams(t.term));
  for (const p of clause.phrases) grams.push(...charNgrams(p.phrase));
  return grams;
}

function scoreNgrams(doc, index, parsed) {
  const clauses = parsed.mode === "or" ? parsed.clauses : parsed.mode === "and" ? [parsed] : [];
  let best = 0;
  for (const clause of clauses) {
    const grams = clauseNgrams(clause);
    if (!grams.length) continue;
    const fields = clause.terms[0]
      ? fieldsForTerm(clause.terms[0].field)
      : clause.phrases[0]
      ? fieldsForTerm(clause.phrases[0].field)
      : Object.keys(RANK_FIELDS);
    let score = 0;
    for (const gram of grams) {
      let tfw = 0;
      for (const field of fields) {
        const tf = doc.fieldNgramTfs[field]?.[gram] || 0;
        if (!tf) continue;
        const cfg = SEARCH_FIELDS[field];
        const len = doc.ngramLengths[field] || 0;
        const avg = index.avgNgramLen[field] || 1;
        const norm = 1 - cfg.b + cfg.b * (len / Math.max(avg, 1e-9));
        tfw += (cfg.boost * tf) / Math.max(norm, 1e-9);
      }
      if (tfw > 0) score += ngramIdf(gram, index) * ((tfw * (K1 + 1)) / (tfw + K1));
    }
    if (score > best) best = score;
  }
  return best;
}

function boostedTermWeight(doc, term) {
  let w = 0;
  for (const [field, cfg] of Object.entries(RANK_FIELDS)) {
    const { tf } = fieldTermFrequency(doc, field, term);
    if (tf) w += cfg.boost * tf;
  }
  return w;
}

function queryTerms(parsed) {
  const clauses = parsed.mode === "or" ? parsed.clauses : parsed.mode === "and" ? [parsed] : [];
  const terms = [];
  for (const clause of clauses) {
    for (const t of clause.terms || []) terms.push(t.term);
    for (const p of clause.phrases || []) terms.push(...tokenize(p.phrase));
  }
  return terms;
}

function tfidfCosine(doc, index, parsed) {
  const terms = queryTerms(parsed);
  if (!terms.length) return 0;
  let dot = 0;
  let qss = 0;
  let dss = doc.tfidfNorm || 0;
  const seen = new Set();
  for (const term of terms) {
    if (seen.has(term)) continue;
    seen.add(term);
    const q = idf(term, index);
    qss += q * q;
    const d = (doc.tfidf.get(term) || 0) + (doc.tfidf.get(stem(term)) || 0) * 0.85;
    dot += q * d;
  }
  if (!qss || !dss) return 0;
  return dot / (Math.sqrt(qss) * Math.sqrt(dss));
}

export function reciprocalRankFusion(rankedIdLists, k = RRF_K) {
  const scores = new Map();
  for (const list of rankedIdLists) {
    list.forEach((id, idx) => {
      scores.set(id, (scores.get(id) || 0) + 1 / (k + idx + 1));
    });
  }
  return scores;
}

function rankIds(rows, key) {
  return rows
    .slice()
    .sort((a, b) => b[key] - a[key] || String(a.id).localeCompare(String(b.id)))
    .map((r) => r.id);
}

function rm3Terms(topDocs, index, parsed, limit = 3) {
  const query = new Set(queryTerms(parsed));
  const scored = new Map();
  for (const doc of topDocs) {
    for (const [term, tf] of Object.entries(doc.fieldTfs.content || {})) {
      if (term.length < 4 || query.has(term)) continue;
      const df = index.df.get(term) || 1;
      if (df > Math.max(2, index.N * 0.5)) continue;
      scored.set(term, (scored.get(term) || 0) + tf * idf(term, index));
    }
    for (const [term, tf] of Object.entries(doc.fieldTfs.claim || {})) {
      if (term.length < 4 || query.has(term)) continue;
      scored.set(term, (scored.get(term) || 0) + tf * idf(term, index) * 1.4);
    }
  }
  return [...scored.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([term]) => term);
}

function collectNeedles(parsed, extra = []) {
  const needles = [...extra];
  const clauses = parsed.mode === "or" ? parsed.clauses : parsed.mode === "and" ? [parsed] : [];
  for (const clause of clauses) {
    for (const t of clause.terms || []) needles.push(t.term);
    for (const p of clause.phrases || []) needles.push(p.phrase);
  }
  return [...new Set(needles.filter((n) => n && (n.length > 1 || n === "e" || n === "π")))];
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
  if (bestStart + window > raw.length && raw.length > window) {
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
  const stemDf = new Map();
  const ngramDf = new Map();
  const fieldLens = {};
  const fieldCounts = {};
  const ngramLens = {};
  const vocab = new Set();

  for (const entry of entries || []) {
    const fields = entryFields(entry);
    const fieldTfs = {};
    const fieldTokens = {};
    const fieldNgramTfs = {};
    const ngramLengths = {};
    const lengths = {};
    const unique = new Set();
    const uniqueGrams = new Set();
    const uniqueStems = new Set();
    const tfidf = new Map();
    for (const [field, text] of Object.entries(fields)) {
      const tokens = tokenize(text);
      lengths[field] = tokens.length;
      fieldLens[field] = (fieldLens[field] || 0) + tokens.length;
      fieldCounts[field] = (fieldCounts[field] || 0) + 1;
      const tf = {};
      for (const tok of tokens) {
        tf[tok] = (tf[tok] || 0) + 1;
        unique.add(tok);
        vocab.add(tok);
        uniqueStems.add(stem(tok));
      }
      fieldTfs[field] = tf;
      fieldTokens[field] = new Set(tokens);
      const grams = charNgrams(text);
      ngramLengths[field] = grams.length;
      ngramLens[field] = (ngramLens[field] || 0) + grams.length;
      const gtf = {};
      for (const g of grams) {
        gtf[g] = (gtf[g] || 0) + 1;
        uniqueGrams.add(g);
      }
      fieldNgramTfs[field] = gtf;
    }
    for (const tok of unique) df.set(tok, (df.get(tok) || 0) + 1);
    for (const st of uniqueStems) stemDf.set(st, (stemDf.get(st) || 0) + 1);
    for (const g of uniqueGrams) ngramDf.set(g, (ngramDf.get(g) || 0) + 1);
    const allText = asLower(fieldText(entry, "all"));
    docs.push({
      entry,
      fields,
      fieldTfs,
      fieldTokens,
      fieldNgramTfs,
      ngramLengths,
      lengths,
      tfidf,
      allText,
      allTokens: new Set(tokenize(allText)),
    });
  }

  const avgLen = {};
  const avgNgramLen = {};
  for (const field of Object.keys(SEARCH_FIELDS)) {
    avgLen[field] = (fieldLens[field] || 0) / Math.max(1, fieldCounts[field] || 1);
    avgNgramLen[field] = (ngramLens[field] || 0) / Math.max(1, fieldCounts[field] || 1);
  }

  const index = {
    N: docs.length,
    docs,
    df,
    stemDf,
    ngramDf,
    avgLen,
    avgNgramLen,
    vocab,
    built_at: Date.now(),
  };

  for (const doc of docs) {
    let norm = 0;
    for (const term of doc.allTokens) {
      const w = boostedTermWeight(doc, term) * idf(term, index);
      if (!w) continue;
      doc.tfidf.set(term, (doc.tfidf.get(term) || 0) + w);
      doc.tfidf.set(stem(term), (doc.tfidf.get(stem(term)) || 0) + w * 0.5);
      norm += w * w;
    }
    doc.tfidfNorm = norm;
  }

  return index;
}

function tieBreak(entry) {
  const t = Date.parse(entry.ingested_at || "") || 0;
  return t / 1e15;
}

function scoreExpanded(doc, index, extraTerms) {
  let score = 0;
  for (const term of extraTerms) {
    const tfw = weightedTf(doc, index, term, Object.keys(RANK_FIELDS));
    score += bm25FromTfw(tfw, term, index);
  }
  return score;
}

export function searchVault(entries, query, filters = {}, { index } = {}) {
  const started = nowMs();
  const parsed = parseQuery(query);
  const idx = index || buildIndex(entries || []);
  if (parsed.mode === "empty") {
    const hits = [];
    for (const doc of idx.docs) {
      if (!passesFilters(doc.entry, filters)) continue;
      hits.push({
        entry: doc.entry,
        score: 0,
        snippets: [],
        matched_fields: [],
        signals: { bm25: 0, ngram: 0, cosine: 0, rrf: 0 },
      });
    }
    return {
      engine: SEARCH_ENGINE_VERSION,
      parsed,
      took_ms: Math.max(0, nowMs() - started),
      total: hits.length,
      hits,
    };
  }

  const rows = [];
  for (const doc of idx.docs) {
    if (!passesFilters(doc.entry, filters)) continue;
    if (!queryMatches(doc, parsed)) continue;
    const lex = scoreDocument(doc, idx, parsed);
    rows.push({
      id: doc.entry.id,
      doc,
      bm25: lex.score,
      ngram: scoreNgrams(doc, idx, parsed),
      cosine: tfidfCosine(doc, idx, parsed),
      matched_fields: lex.matched_fields,
    });
  }

  const fused = reciprocalRankFusion(
    [rankIds(rows, "bm25"), rankIds(rows, "ngram"), rankIds(rows, "cosine")],
    RRF_K
  );

  rows.sort((a, b) => (fused.get(b.id) || 0) - (fused.get(a.id) || 0));
  const top = rows.filter((r) => r.bm25 >= (rows[0]?.bm25 || 0) * 0.6).slice(0, 2);
  const extra = rm3Terms(
    top.map((r) => r.doc),
    idx,
    parsed
  );
  if (extra.length) {
    for (const row of rows) {
      row.expanded = scoreExpanded(row.doc, idx, extra);
    }
    const again = reciprocalRankFusion(
      [rankIds(rows, "bm25"), rankIds(rows, "ngram"), rankIds(rows, "cosine"), rankIds(rows, "expanded")],
      RRF_K
    );
    for (const row of rows) {
      fused.set(row.id, again.get(row.id) || 0);
    }
  }

  const needles = collectNeedles(parsed);
  const hits = rows
    .map((row) => {
      const rrf = fused.get(row.id) || 0;
      return {
        entry: row.doc.entry,
        score: rrf * 100 + tieBreak(row.doc.entry),
        snippets: buildSnippets(row.doc.entry, needles),
        matched_fields: row.matched_fields,
        signals: {
          bm25: row.bm25,
          ngram: row.ngram,
          cosine: row.cosine,
          rrf,
          expanded: extra,
        },
      };
    })
    .sort((a, b) => b.score - a.score || String(a.entry.title).localeCompare(String(b.entry.title)));

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
