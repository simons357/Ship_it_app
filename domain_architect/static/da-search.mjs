/**
 * Pure helpers for the Domain Architect homepage search dock.
 * No DOM. ChatVault is the site search; the web is a hunt in a new tab.
 */

export const SNIPPET_SOURCE_TYPES = Object.freeze(["other", "letter", "paper", "conversation"]);

export function defaultSearchMode({ stored, standalone } = {}) {
  if (standalone) return "here";
  if (stored === "here" || stored === "open") return stored;
  return "here";
}

export function parseShareTarget(params) {
  const get = (key) => {
    if (!params) return "";
    if (typeof params.get === "function") return String(params.get(key) || "").trim();
    return String(params[key] || "").trim();
  };
  const title = get("title");
  const text = get("text");
  const url = get("url");
  if (!title && !text && !url) {
    return { snippet: "", autoIndex: false, title: "", url: "", text: "" };
  }
  const parts = [];
  if (title) parts.push(title);
  if (text && text !== title && text !== url) parts.push(text);
  if (url && url !== text) parts.push(url);
  const snippet = parts.join("\n\n");
  return {
    snippet,
    autoIndex: Boolean(snippet),
    title: title || (url ? `Shared: ${url.slice(0, 60)}` : "Shared snippet"),
    url,
    text,
  };
}

export function snippetIngestOverrides({ originClass, sourceType } = {}) {
  const origin = originClass === "ai_generated" ? "ai_generated" : "human_record";
  const type = SNIPPET_SOURCE_TYPES.includes(sourceType) ? sourceType : "other";
  return {
    origin_class: origin,
    source_ai: origin === "ai_generated" ? "unknown" : "human",
    source_type: type,
    search_tags: ["quick-capture"],
  };
}

export function shareIngestOverrides(share = {}) {
  return {
    title: String(share.title || "Shared snippet").slice(0, 120),
    source_ai: "human",
    origin_class: "human_record",
    source_type: "other",
    search_tags: ["share-target", "quick-capture"],
    summary: "Shared into Domain Architect. Not a ChatGPT conversation dump.",
  };
}

export function deepDiveLinks(query) {
  const q = String(query || "").trim() || "ChatVault OS for your AI";
  const enc = encodeURIComponent(q);
  return [
    { id: "ddg", label: "DuckDuckGo", href: `https://duckduckgo.com/?q=${enc}` },
    { id: "wiki", label: "Wikipedia", href: `https://en.wikipedia.org/w/index.php?search=${enc}` },
    { id: "scholar", label: "Semantic Scholar", href: `https://www.semanticscholar.org/search?q=${enc}` },
    { id: "gscholar", label: "Google Scholar", href: `https://scholar.google.com/scholar?q=${enc}` },
  ];
}

export function filedSearchPayload(query) {
  const q = String(query || "").trim();
  if (!q) throw new Error("Type a search to file.");
  return {
    raw: `Search: ${q}\n\n${q}`,
    overrides: {
      title: `Search: ${q}`.slice(0, 120),
      source_ai: "human",
      origin_class: "human_record",
      source_type: "other",
      search_tags: ["filed-search", "web-hunt"],
      summary: "Filed search query. Not a conversation dump.",
    },
  };
}

export function filedHuntPayload(query, links) {
  const q = String(query || "").trim();
  if (!q) throw new Error("Type a query to file this hunt.");
  const rows = (links && links.length ? links : deepDiveLinks(q))
    .map((link) => `${link.label}: ${link.href}`)
    .join("\n");
  return {
    raw: [
      `Web hunt: ${q}`,
      "",
      "Vault is local. These URLs were opened as a hunt in a new tab — ChatVault does not crawl the web.",
      "",
      rows,
    ].join("\n"),
    overrides: {
      title: `Web hunt: ${q}`.slice(0, 120),
      source_ai: "human",
      origin_class: "human_record",
      source_type: "other",
      search_tags: ["web-hunt"],
      summary: "Filed web hunt (new-tab URLs only). Not a web index.",
    },
  };
}

export function shouldHandleFetchInDaWorker(method, pathname) {
  if (String(method || "GET").toUpperCase() !== "GET") return false;
  const path = String(pathname || "");
  if (path.startsWith("/chatvault/")) return false;
  if (path.startsWith("/api/")) return false;
  return true;
}
