/**
 * Domain Architect inquiry client.
 *
 * Search box = ChatVault ranker (this vault).
 * Inquiry box = Domain Architect FRA (POST /api/inquiry).
 * They share an origin. They are not the same engine.
 */

export const DA_INQUIRY_HOSTS = Object.freeze([
  "http://127.0.0.1:8765",
  "http://localhost:8765",
]);

export function inquiryOrigins() {
  const extra = [];
  if (typeof location !== "undefined" && location.origin && location.origin !== "null") {
    extra.push(location.origin);
  }
  return [...new Set([...extra, ...DA_INQUIRY_HOSTS])];
}

export function inquiryPayload(text, { drain = false } = {}) {
  const inquiry = String(text || "").trim();
  if (!inquiry) {
    throw new Error("Type an equation or question in the inquiry box.");
  }
  return { inquiry, expression: inquiry, drain: Boolean(drain) };
}

export function inquiryNarrative(payload) {
  const chunks = [];
  const cmp = payload?.swirl_comparison;
  if (cmp && (cmp.with_cancel || cmp.without_cancel)) {
    chunks.push("Swirl comparison (Domain Architect; not a proof; Clay NS not claimed):");
    if (cmp.with_cancel) {
      chunks.push(
        `WITH cancel: ${cmp.with_cancel.operator} [${cmp.with_cancel.status}] ${cmp.with_cancel.pdf_url || ""}`
      );
    }
    if (cmp.without_cancel) {
      chunks.push(
        `WITHOUT cancel: ${cmp.without_cancel.operator} [${cmp.without_cancel.status}] ${cmp.without_cancel.pdf_url || ""}`
      );
    }
    for (const line of cmp.difference || []) {
      chunks.push(`  - ${line}`);
    }
    for (const gap of cmp.gaps || []) {
      chunks.push(`Gap ${gap.id || ""}: UNFILLED. ${gap.statement || ""}`);
      const nxt = gap.next_attempt || {};
      if (nxt.lemma) chunks.push(`  Next attempt: ${nxt.lemma}`);
    }
    chunks.push("");
  }
  if (payload?.ns_unaugmented) {
    chunks.push(
      `Unaugmented NS face: ${payload.ns_unaugmented.operator} [${payload.ns_unaugmented.status}]. Clay NS is not claimed.`
    );
    chunks.push("");
  }
  if (payload?.honest_mistake?.paragraph) {
    chunks.push(payload.honest_mistake.paragraph);
    chunks.push("");
  }
  const realization = payload?.ns_regularity_realization;
  if (realization?.fingers) {
    chunks.push("Hypothesized NS regularity realization. Not endorsed. Not a theorem.");
    chunks.push("Finger classifications:");
    for (const row of realization.fingers) {
      chunks.push(`  - ${row.id}: ${row.classification}`);
    }
    chunks.push("");
  }
  if (payload?.audit?.narrative) chunks.push(payload.audit.narrative);
  return chunks.join("\n");
}

export async function postInquiry(text, { drain = false, fetchImpl = fetch } = {}) {
  const body = JSON.stringify(inquiryPayload(text, { drain }));
  const errors = [];
  for (const origin of inquiryOrigins()) {
    try {
      const res = await fetchImpl(`${origin}/api/inquiry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        errors.push(`${origin}: ${data.error || res.statusText}`);
        continue;
      }
      if (data.lane !== "inquiry" || !data.audit) {
        errors.push(`${origin}: not an inquiry payload.`);
        continue;
      }
      return { ...data, origin };
    } catch (err) {
      errors.push(`${origin}: ${err.message || String(err)}`);
    }
  }
  throw new Error(
    `Domain Architect inquiry is not reachable. Start python3 -m domain_architect --site. Tried: ${errors.join("; ")}`
  );
}
