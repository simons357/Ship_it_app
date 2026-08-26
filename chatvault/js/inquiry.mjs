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
  return String(payload?.audit?.narrative || "");
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
