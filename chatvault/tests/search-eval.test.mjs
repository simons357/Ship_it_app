import { test } from "node:test";
import assert from "node:assert/strict";
import { ingestPaste } from "../js/engine.mjs";
import { searchVault, ndcgAt, mrr } from "../js/search.mjs";

/**
 * Graded retrieval set. These are fixtures, not Jonathan’s research corpus.
 * Grades: 3 = the intended record, 2 = useful, 1 = incidental mention, 0 = absent.
 */
function evalCorpus() {
  const euler = ingestPaste(
    [
      "TITLE: Euler identity as a definitional fact",
      "SOURCE_AI: Grok",
      "PROJECT: mathematics",
      "BOOK: Research & Ideas",
      "TAG: euler",
      "CLAIM: e^{iπ} + 1 = 0 is a definitional identity in complex analysis, not an empirical discovery.",
      "THEOREM: Euler's formula e^{iθ} = cos θ + i sin θ for real θ.",
      "GAP: This vault does not treat Euler's identity as a research open problem.",
      "SUMMARY: Fixture used to show raw text is kept beside an optional summary.",
      "",
      "The identity e^{iπ} + 1 = 0 remains a definitional Euler identity.",
    ].join("\n")
  );
  const ns = ingestPaste(
    [
      "TITLE: Spectral regularity for Navier–Stokes — status of the claim",
      "SOURCE_AI: Claude",
      "PROJECT: fluids",
      "BOOK: Research & Ideas",
      "TAG: navier-stokes",
      "CLAIM: Global regularity of 3D Navier–Stokes on T³ is not established in this vault.",
      "GAP: A complete a-priori bound preventing finite-time blow-up is missing.",
      "SUMMARY: Research-memory fixture. Do not market as a solved Millennium problem.",
      "",
      "Raw note: any spectral non-concentration argument remains conditional.",
    ].join("\n")
  );
  const limiter = ingestPaste(
    [
      "TITLE: Token bucket rate limiter notes",
      "SOURCE_AI: ChatGPT",
      "PROJECT: saas",
      "TAG: rate-limiter",
      "CLAIM: A token bucket is a traffic-shaping algorithm, not a research theorem.",
      "",
      "Implement the rate limiter before the investor deck.",
    ].join("\n")
  );
  const logistics = ingestPaste(
    [
      "TITLE: Weekly lab logistics",
      "SOURCE_AI: ChatGPT",
      "PROJECT: operations",
      "",
      "Someone mentioned Euler in passing while booking the seminar room. No identity was proved.",
    ].join("\n")
  );
  const party = ingestPaste(
    [
      "TITLE: Birthday blow-up plans",
      "SOURCE_AI: human",
      "PROJECT: personal",
      "",
      "Party blow-up balloons. This is not Navier–Stokes.",
    ].join("\n")
  );
  const clinical = ingestPaste(
    [
      "TITLE: Private clinical teaching fragment",
      "SOURCE_AI: human",
      "VISIBILITY: private",
      "TAG: teaching",
      "",
      "Private: a teaching mnemonic from OR debrief.",
    ].join("\n")
  );
  const investor = ingestPaste(
    [
      "TITLE: Investor deck outline",
      "SOURCE_AI: ChatGPT",
      "PROJECT: saas",
      "",
      "Slide 4 mentions a rate limiter only as a reliability talking point.",
    ].join("\n")
  );
  euler.stable = "euler";
  ns.stable = "ns";
  limiter.stable = "limiter";
  logistics.stable = "logistics";
  party.stable = "party";
  clinical.stable = "clinical";
  investor.stable = "investor";
  return { euler, ns, limiter, logistics, party, clinical, investor };
}

function topics(corpus) {
  return [
    {
      name: "euler identity ranks the definitional record first",
      query: "euler identity",
      grades: { euler: 3, logistics: 1 },
    },
    {
      name: "exact blow-up phrase is the Navier–Stokes gap",
      query: '"finite-time blow-up"',
      grades: { ns: 3 },
    },
    {
      name: "fielded claim: stays inside claims",
      query: "claim:definitional",
      grades: { euler: 3 },
    },
    {
      name: "fielded gap: ignores birthday blow-up",
      query: "gap:blow-up",
      grades: { ns: 3 },
    },
    {
      name: "rate limiter prefers the dedicated note over a slide mention",
      query: "rate limiter",
      grades: { limiter: 3, investor: 1 },
    },
    {
      name: "OR retrieves both research fixtures",
      query: "euler OR navier-stokes",
      grades: { euler: 3, ns: 3, logistics: 1 },
    },
    {
      name: "ai:Claude is provenance, not a vibe match",
      query: "ai:Claude",
      grades: { ns: 3 },
    },
  ];
}

function booleanOrder(entries, query) {
  const { hits } = searchVault(entries, query);
  const wanted = new Set(hits.map((h) => h.entry.id));
  return entries.filter((e) => wanted.has(e.id)).map((e) => e.stable);
}

test("BM25F mean nDCG@5 clears 0.90 on the graded vault fixture", () => {
  const corpus = evalCorpus();
  const entries = Object.values(corpus);
  const byStable = Object.fromEntries(entries.map((e) => [e.id, e.stable]));
  const rows = [];
  for (const topic of topics(corpus)) {
    const result = searchVault(entries, topic.query);
    const ranked = result.hits.map((h) => byStable[h.entry.id]);
    const ndcg = ndcgAt(ranked, topic.grades, 5);
    const recip = mrr(ranked, topic.grades);
    rows.push({ name: topic.name, query: topic.query, ranked, ndcg, mrr: recip });
    assert.equal(ranked[0] && (topic.grades[ranked[0]] || 0) >= 3, true, `${topic.name}: first hit should be grade 3, got ${ranked[0]}`);
    assert.ok(ndcg >= 0.9, `${topic.name}: nDCG@5 ${ndcg}`);
  }
  const mean = rows.reduce((s, r) => s + r.ndcg, 0) / rows.length;
  const meanMrr = rows.reduce((s, r) => s + r.mrr, 0) / rows.length;
  assert.ok(mean >= 0.9, `mean nDCG@5 ${mean}`);
  assert.ok(meanMrr >= 0.9, `mean MRR ${meanMrr}`);
});

test("BM25F beats store-order boolean on title vs incidental mention", () => {
  const corpus = evalCorpus();
  const entries = [corpus.logistics, corpus.investor, corpus.euler, corpus.limiter];
  const bm25 = searchVault(entries, "euler identity").hits.map((h) => h.entry.stable);
  const boolean = booleanOrder(entries, "euler identity");
  assert.equal(bm25[0], "euler");
  assert.equal(boolean[0], "logistics");
  assert.ok(boolean.includes("euler"));
});

test("professional visibility filter cannot leak the clinical mnemonic", () => {
  const corpus = evalCorpus();
  const hits = searchVault(Object.values(corpus), "mnemonic", { visibility: "professional" });
  assert.equal(hits.total, 0);
});
