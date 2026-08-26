/**
 * ChatVault drain + fat ingest.
 *
 * AI chats, Domain Architect audits, and real-world records (papers,
 * letters, pictures, movies) all land in the same vault. Origin class
 * tells them apart. This is OS for your AI — not a note-taking brand.
 *
 * Domain Architect is a math auditor. It is not ChatVault’s brain and
 * it does not prove Navier–Stokes or Riemann.
 */

import {
  emptyEntry,
  importVault,
  ingestPaste,
  ingestTextFile,
} from "./engine.mjs";

export const DRAIN_PROTOCOL = "chatvault-drain-0.1.0";
export const DA_DRAIN_URLS = Object.freeze([
  "http://127.0.0.1:7847",
  "http://localhost:7847",
]);

export function drainOrigins() {
  const extra = [];
  if (typeof location !== "undefined" && location.origin && location.origin !== "null") {
    extra.push(`${location.origin}/api/drain`);
  }
  return [...extra, ...DA_DRAIN_URLS];
}
export const MAX_IMAGE_BYTES = 12 * 1024 * 1024;

const TEXT_NAME = /\.(txt|md|markdown|json|csv|html|htm|xml|rtf|log)$/i;

export function classifyFilename(filename, mime = "") {
  const lower = String(filename || "").toLowerCase();
  const type = String(mime || "").toLowerCase();
  if (/\.(png|jpe?g|gif|webp|svg|heic|bmp|tiff?)$/i.test(lower) || type.startsWith("image/")) {
    return "picture";
  }
  if (/\.(mp4|mov|webm|mkv|avi|m4v)$/i.test(lower) || type.startsWith("video/")) return "movie";
  if (/\.(mp3|wav|m4a|aac|flac|ogg)$/i.test(lower) || type.startsWith("audio/")) return "audio";
  if (/\.pdf$/i.test(lower) || type === "application/pdf") return "pdf";
  if (/\.(docx?|odt)$/i.test(lower) || type.includes("wordprocessingml") || type.includes("msword")) {
    return "docx";
  }
  if (TEXT_NAME.test(lower) || type.startsWith("text/") || type === "application/json") return "text";
  return "other";
}

function messageText(node) {
  const msg = node?.message;
  if (!msg) return "";
  const content = msg.content;
  if (typeof content === "string") return content.trim();
  if (Array.isArray(content?.parts)) {
    return content.parts
      .map((part) => (typeof part === "string" ? part : part?.text || ""))
      .filter(Boolean)
      .join("\n")
      .trim();
  }
  if (typeof content?.text === "string") return content.text.trim();
  return "";
}

function formatNodes(nodes) {
  const lines = [];
  for (const node of nodes || []) {
    const role = node?.message?.author?.role || node?.message?.role || "";
    if (!role || role === "system") continue;
    const text = messageText(node);
    if (!text) continue;
    lines.push(`${String(role).toUpperCase()}:\n${text}`);
  }
  return lines.join("\n\n");
}

export function looksLikeChatGptConversation(value) {
  return Boolean(value && typeof value === "object" && value.mapping && typeof value.mapping === "object");
}

export function looksLikeChatGptExport(value) {
  if (!value || typeof value !== "object") return false;
  if (Array.isArray(value)) return value.some(looksLikeChatGptConversation);
  if (Array.isArray(value.conversations)) return value.conversations.some(looksLikeChatGptConversation);
  return looksLikeChatGptConversation(value);
}

function conversationBody(conv) {
  const mapping = conv.mapping || {};
  if (conv.current_node && mapping[conv.current_node]) {
    const chain = [];
    let id = conv.current_node;
    const seen = new Set();
    while (id && mapping[id] && !seen.has(id)) {
      seen.add(id);
      chain.push(mapping[id]);
      id = mapping[id].parent;
    }
    chain.reverse();
    const selected = formatNodes(chain);
    if (selected) return selected;
  }
  const roots = Object.keys(mapping).filter((id) => !mapping[id]?.parent || !mapping[mapping[id].parent]);
  const seen = new Set();
  const nodes = [];
  const walk = (id) => {
    if (!id || seen.has(id) || !mapping[id]) return;
    seen.add(id);
    nodes.push(mapping[id]);
    for (const child of mapping[id].children || []) walk(child);
  };
  for (const root of roots) walk(root);
  for (const id of Object.keys(mapping)) {
    if (!seen.has(id)) walk(id);
  }
  return formatNodes(nodes);
}

export function conversationsFromExport(value) {
  if (Array.isArray(value)) return value.filter(looksLikeChatGptConversation);
  if (Array.isArray(value?.conversations)) return value.conversations.filter(looksLikeChatGptConversation);
  if (looksLikeChatGptConversation(value)) return [value];
  return [];
}

export function ingestChatGptExport(value, overrides = {}) {
  const conversations = conversationsFromExport(value);
  const entries = [];
  const errors = [];
  conversations.forEach((conv, index) => {
    const body = conversationBody(conv);
    if (!body) {
      errors.push({ index, message: "Conversation had no user/assistant text." });
      return;
    }
    const created =
      typeof conv.create_time === "number"
        ? new Date(conv.create_time * 1000).toISOString()
        : undefined;
    try {
      entries.push(
        ingestPaste(body, {
          title: String(conv.title || "ChatGPT conversation").slice(0, 120),
          source_ai: "ChatGPT",
          source_type: "transcript",
          origin_class: "ai_generated",
          item_date: created ? created.slice(0, 10) : undefined,
          ingested_at: created,
          search_tags: ["chatgpt-export", "ai-conversation"],
          ...overrides,
          origin_class: "ai_generated",
          source_ai: overrides.source_ai && overrides.source_ai !== "unknown" ? overrides.source_ai : "ChatGPT",
          source_type: overrides.source_type || "transcript",
        })
      );
    } catch (err) {
      errors.push({ index, message: err.message || String(err) });
    }
  });
  if (!entries.length) {
    throw new Error("No ChatGPT conversations with text were found in that JSON.");
  }
  return { kind: "chatgpt", entries, errors };
}

export function looksLikeDaAudit(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  if (value.source === "domain-architect" && value.format === "chatvault-export") return true;
  return (
    typeof value.input_expression === "string" &&
    Object.prototype.hasOwnProperty.call(value, "canonical_sfe_status")
  );
}

export function ingestDaAudit(obj, overrides = {}) {
  if (obj.format === "chatvault-export") {
    return { kind: "bundle", entries: importVault(obj), errors: [] };
  }
  const expression = String(obj.input_expression || "expression");
  const narrative = String(obj.narrative || JSON.stringify(obj, null, 2));
  const evidence = obj.highest_evidence_label || "n/a";
  const status = obj.canonical_sfe_status || "unresolved";
  const entry = ingestPaste(narrative, {
    title: `DA audit: ${expression.slice(0, 72)}`,
    source_type: "da_audit",
    source_ai: "DomainArchitect",
    origin_class: "human_record",
    summary: `Domain Architect FRA audit. Evidence: ${evidence}. Canonical SFE status: ${status}. Not a proof.`,
    search_tags: ["domain-architect", "fra", "da_audit"],
    project_category: "Domain Architect",
    related_projects: ["Domain Architect"],
    ...overrides,
    origin_class: "human_record",
    source_ai: "DomainArchitect",
    source_type: "da_audit",
  });
  return { kind: "da_audit", entries: [entry], errors: [] };
}

export function ingestMediaStub({ filename, mime, size, dataUrl }, overrides = {}) {
  const kind = classifyFilename(filename, mime);
  const stored = Boolean(dataUrl) && kind === "picture";
  const raw = stored
    ? `REAL ${kind.toUpperCase()} ${filename}\nmime=${mime || "unknown"}\nsize=${size || 0}\nstored=data-url\n`
    : `REAL ${kind.toUpperCase()} STUB ${filename}\nmime=${mime || "unknown"}\nsize=${size || 0}\nstored=metadata-only\nThe binary is not in this vault. ChatVault indexes a searchable stub so you can look it up next to AI chats.\n`;
  const entry = emptyEntry({
    title: String(filename || kind),
    source_type: kind === "other" ? "other" : kind,
    source_ai: "human",
    origin_class: "human_record",
    source_file: filename,
    file_url: stored ? dataUrl : "",
    raw_content: raw,
    content_text: raw,
    summary: stored
      ? `Real ${kind} stored as a data URL (${size || 0} bytes).`
      : `Real ${kind} stub — filename, type, and size only (${size || 0} bytes). Not a media locker.`,
    search_tags: ["real-record", kind],
    ...overrides,
    origin_class: "human_record",
    source_ai: overrides.source_ai && overrides.source_ai !== "unknown" ? overrides.source_ai : "human",
    source_type: overrides.source_type || (kind === "other" ? "other" : kind),
  });
  return { kind: "media", entries: [entry], errors: [] };
}

function tryJsonSpecial(text, filename, overrides) {
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    return null;
  }
  if (parsed && parsed.format === "chatvault-export") {
    return { kind: "bundle", entries: importVault(parsed), errors: [] };
  }
  if (looksLikeDaAudit(parsed)) return ingestDaAudit(parsed, { source_file: filename, ...overrides });
  if (looksLikeChatGptExport(parsed)) {
    const result = ingestChatGptExport(parsed, { source_file: filename, ...overrides });
    return result;
  }
  return null;
}

export function ingestNamedSource(filename, payload = {}, overrides = {}) {
  const name = String(filename || "untitled");
  const mime = payload.mime || "";
  const size = payload.size || (payload.text ? payload.text.length : 0);
  const kind = classifyFilename(name, mime);

  if (kind === "picture" && payload.dataUrl && size <= MAX_IMAGE_BYTES) {
    return ingestMediaStub({ filename: name, mime, size, dataUrl: payload.dataUrl }, overrides);
  }
  if (kind === "picture" || kind === "movie" || kind === "audio" || kind === "pdf" || kind === "docx") {
    return ingestMediaStub({ filename: name, mime, size, dataUrl: "" }, overrides);
  }
  if (payload.text != null) {
    const special = String(name).toLowerCase().endsWith(".json") || mime === "application/json"
      ? tryJsonSpecial(payload.text, name, overrides)
      : null;
    if (special) return special;
    if (TEXT_NAME.test(name) || kind === "text") {
      return ingestTextFile(name, payload.text, overrides);
    }
    return {
      kind: "entry",
      entries: [
        ingestPaste(payload.text, {
          ...overrides,
          source_file: name,
          source_type: overrides.source_type || "other",
        }),
      ],
      errors: [],
    };
  }
  return ingestMediaStub({ filename: name, mime, size, dataUrl: payload.dataUrl || "" }, overrides);
}

export async function pullDaDrain(fetchImpl = fetch) {
  let lastErr = new Error("Domain Architect drain is not running on 127.0.0.1:7847.");
  for (const origin of drainOrigins()) {
    try {
      const res = await fetchImpl(`${origin}/queue`);
      if (!res.ok) {
        lastErr = new Error(`Drain ${origin} returned ${res.status}.`);
        continue;
      }
      const payload = await res.json();
      if (!payload || payload.format !== "chatvault-export") {
        lastErr = new Error("Drain did not return a ChatVault export.");
        continue;
      }
      return { origin, entries: importVault(payload), count: (payload.entries || []).length };
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr;
}
