import { test } from "node:test";
import assert from "node:assert/strict";
import { importVault } from "../js/engine.mjs";
import {
  inquiryOrigins,
  inquiryPayload,
  inquiryNarrative,
  postInquiry,
} from "../js/inquiry.mjs";

test("inquiry payload is FRA, not a search query object", () => {
  assert.throws(() => inquiryPayload("  "));
  const body = inquiryPayload("∇²Φ = 4π G ρ", { drain: true });
  assert.equal(body.inquiry, "∇²Φ = 4π G ρ");
  assert.equal(body.expression, body.inquiry);
  assert.equal(body.drain, true);
});

test("inquiry origins prefer this page then loopback DA site", () => {
  const origins = inquiryOrigins();
  assert.ok(origins.includes("http://127.0.0.1:8765"));
  assert.ok(origins.includes("http://localhost:8765"));
});

test("inquiry narrative reads the FRA report, not a vault hit list", () => {
  assert.equal(inquiryNarrative({}), "");
  assert.equal(
    inquiryNarrative({ audit: { narrative: "Domain Architect — Functional Role Analysis report" } }),
    "Domain Architect — Functional Role Analysis report"
  );
});

test("postInquiry hits /api/inquiry and files a ChatVault export when drain=true", async () => {
  const calls = [];
  const drain = {
    format: "chatvault-export",
    schema_version: "chatvault-engine-0.3.0",
    entries: [
      {
        id: "da_test",
        title: "DA audit: x = y",
        origin_class: "human_record",
        source_type: "da_audit",
        source_ai: "DomainArchitect",
        raw_content: "FRA",
        key_claims: [],
        theorems: [],
      },
    ],
  };
  const fetchImpl = async (url, opts) => {
    calls.push({ url, opts });
    return {
      ok: true,
      json: async () => ({
        lane: "inquiry",
        inquiry: "x = y",
        audit: { narrative: "roles only", canonical_sfe_status: "unresolved" },
        drain,
      }),
    };
  };
  const result = await postInquiry("x = y", { drain: true, fetchImpl });
  assert.equal(result.lane, "inquiry");
  assert.match(calls[0].url, /\/api\/inquiry$/);
  assert.equal(JSON.parse(calls[0].opts.body).drain, true);
  const entries = importVault(result.drain);
  assert.equal(entries[0].origin_class, "human_record");
  assert.equal(entries[0].source_type, "da_audit");
  assert.equal(entries.every((e) => (e.key_claims || []).every((c) => c.status !== "PROVED")), true);
});
