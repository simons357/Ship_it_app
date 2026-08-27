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

test("swirl comparison narrative prints UNFILLED gaps and the next-attempt lemma", () => {
  const text = inquiryNarrative({
    swirl_comparison: {
      with_cancel: {
        operator: "r^{-4} ∂z(Γ²) = ∂z(Φ²)",
        status: "q1_augmented_algebraic_identity",
        pdf_url: "/faces/01_phi_renormalization.pdf",
      },
      without_cancel: {
        operator: "D_t Ω = (1/r^4) ∂z(Γ²) + ν L_cyl Ω",
        status: "open_axis_obstruction",
        pdf_url: "/faces/swirl_without_cancel.pdf",
      },
      difference: ["WITHOUT keeps the 1/r^4 axis term."],
      gaps: [
        {
          id: "GAP-SWIRL-AXIS",
          statement: "Danchin (2007) names the 1/r^4 hole; naming it does not cancel it.",
          next_attempt: { lemma: "Chen–Fang–Zhang L^∞_t L^3_x swirl criterion" },
        },
        {
          id: "GAP-Q1-CLASSICAL",
          statement: "Q1 ≠ classical. LPS bootstraps the augmented PDE only.",
          next_attempt: { lemma: "ε-independence of C(ε)=2 sup_t ‖u^r_ε/r‖_∞" },
        },
      ],
    },
  });
  assert.match(text, /UNFILLED/);
  assert.match(text, /GAP-SWIRL-AXIS/);
  assert.match(text, /Danchin/);
  assert.match(text, /Chen/);
  assert.match(text, /Q1 ≠ classical/);
  assert.doesNotMatch(text, /Clay NS is proved/);
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
