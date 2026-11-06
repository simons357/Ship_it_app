/**
 * Any kind of address on any record: URL, DOI, path, coordinates,
 * postal, ISBN, handle, or free text. Each locator gets a short code.
 */

export const LOCATOR_KINDS = Object.freeze([
  "url",
  "doi",
  "path",
  "geo",
  "postal",
  "isbn",
  "handle",
  "other",
]);

export function classifyLocator(raw) {
  const v = String(raw || "").trim();
  if (!v) return "other";
  if (/^10\.\d{4,}\/\S+/i.test(v) || /doi\.org\//i.test(v)) return "doi";
  if (/^https?:\/\//i.test(v) || /^www\./i.test(v)) return "url";
  if (/^-?\d{1,3}(\.\d+)?\s*,\s*-?\d{1,3}(\.\d+)?$/.test(v)) return "geo";
  if (/^(978|979)[-0-9]{10,}/.test(v) || /^[0-9]{9}[0-9Xx]$/.test(v)) return "isbn";
  if (/^[\\/]/.test(v) || /^[a-zA-Z]:[\\/]/.test(v) || /\.(pdf|md|txt|json|docx|html)$/i.test(v)) {
    return "path";
  }
  if (/^@[\w.-]+/.test(v) || /^[a-z0-9-]{2,}\.[a-z]{2,}(\/.*)?$/i.test(v)) return "handle";
  if (/\b(\d{5}(-\d{4})?|[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b/i.test(v) || /\b(street|st\.|ave|avenue|rd\.|road|blvd)\b/i.test(v)) {
    return "postal";
  }
  return "other";
}

export function locatorCode(value) {
  let h = 2166136261;
  for (const ch of String(value)) {
    h ^= ch.charCodeAt(0);
    h = Math.imul(h, 16777619);
  }
  return `a_${(h >>> 0).toString(36).padStart(7, "0").slice(0, 7)}`;
}

export function makeLocator(value, kind = "auto") {
  const v = String(value || "").trim();
  if (!v) return null;
  const resolved =
    kind && kind !== "auto" && LOCATOR_KINDS.includes(kind) ? kind : classifyLocator(v);
  return { code: locatorCode(v), kind: resolved, value: v };
}

export function mergeLocators(list, fallbackValue) {
  const out = [];
  const seen = new Set();
  const extra = fallbackValue ? [makeLocator(fallbackValue)] : [];
  for (const item of [...(list || []), ...extra]) {
    if (!item) continue;
    const loc = item.value != null ? makeLocator(item.value, item.kind) : makeLocator(item);
    if (!loc || seen.has(loc.value)) continue;
    seen.add(loc.value);
    out.push(loc);
  }
  return out;
}

export function locatorBlob(entry) {
  const locs = entry?.locators || [];
  return [
    entry?.source_file || "",
    ...locs.map((l) => `${l.kind} ${l.value} ${l.code}`),
  ].join(" ");
}
