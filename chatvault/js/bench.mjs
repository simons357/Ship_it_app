/**
 * Frozen retrieval eval. Additions to the ranker must beat or match BASELINE.
 * Memory context is scored in a separate column and must not hide a regression.
 */

import { DEMO_ENTRIES } from "./engine.mjs";
import { SEARCH_ENGINE_VERSION, searchVault, ndcgAt, mrr } from "./search.mjs";

export const BENCH_VERSION = "chatvault-bench-0.1.0";

export const BENCH_CASES = Object.freeze([
  { id: "euler-and", q: "euler identity", title: /Euler identity/i },
  { id: "phrase-blowup", q: '"finite-time blow-up"', title: /Navier/i },
  { id: "claim-field", q: "claim:definitional", title: /Euler/i },
  { id: "gap-field", q: "gap:blow-up", title: /Navier/i },
  { id: "ai-claude", q: "ai:Claude", title: /Navier|CLAIM_LEDGER/i },
  { id: "or-query", q: "euler OR navier-stokes", title: /Euler|Navier/i },
]);

/** Floors. A drop below these is a failed addition, not a vibe. */
export const BASELINE = Object.freeze({
  engine: SEARCH_ENGINE_VERSION,
  mean_ndcg5: 1,
  mean_mrr: 1,
  mean_took_ms_max: 250,
  cases_must_hit: BENCH_CASES.map((c) => c.id),
});

function gradesFor(corpus, titleRe) {
  const grades = {};
  for (const entry of corpus) {
    grades[entry.id] = titleRe.test(entry.title) ? 3 : 0;
  }
  return grades;
}

export function runBench(corpus = DEMO_ENTRIES, searchFn = searchVault) {
  const rows = BENCH_CASES.map((c) => {
    const result = searchFn(corpus, c.q);
    const rankedIds = result.hits.map((h) => h.entry.id);
    const grades = gradesFor(corpus, c.title);
    const top = result.hits[0]?.entry;
    const hit = Boolean(top && c.title.test(top.title));
    return {
      id: c.id,
      q: c.q,
      top: top?.title || "",
      hit,
      ndcg5: ndcgAt(rankedIds, grades, 5),
      mrr: mrr(rankedIds, grades),
      took_ms: result.took_ms,
      total: result.total,
    };
  });
  const mean = (key) => rows.reduce((s, r) => s + r[key], 0) / rows.length;
  const summary = {
    version: BENCH_VERSION,
    engine: SEARCH_ENGINE_VERSION,
    at: new Date().toISOString(),
    mean_ndcg5: mean("ndcg5"),
    mean_mrr: mean("mrr"),
    mean_took_ms: mean("took_ms"),
    hits: rows.filter((r) => r.hit).length,
    cases: rows.length,
    rows,
  };
  summary.pass =
    summary.mean_ndcg5 + 1e-9 >= BASELINE.mean_ndcg5 &&
    summary.mean_mrr + 1e-9 >= BASELINE.mean_mrr &&
    summary.mean_took_ms <= BASELINE.mean_took_ms_max &&
    rows.every((r) => r.hit);
  return summary;
}

export function formatBenchReport(summary, previous) {
  const delta = previous
    ? `nDCG ${summary.mean_ndcg5.toFixed(3)} (was ${previous.mean_ndcg5.toFixed(3)}) · MRR ${summary.mean_mrr.toFixed(3)} (was ${previous.mean_mrr.toFixed(3)}) · ${summary.mean_took_ms.toFixed(1)} ms (was ${previous.mean_took_ms.toFixed(1)})`
    : `nDCG ${summary.mean_ndcg5.toFixed(3)} · MRR ${summary.mean_mrr.toFixed(3)} · ${summary.mean_took_ms.toFixed(1)} ms mean`;
  const lines = [
    `# ChatVault weekly search bench`,
    ``,
    `**At:** ${summary.at}`,
    `**Engine:** ${summary.engine}`,
    `**Result:** ${summary.pass ? "PASS" : "FAIL"} — ${delta}`,
    ``,
    `| Case | Query | Top hit | nDCG@5 | MRR | ms | Hit |`,
    `| --- | --- | --- | --- | --- | --- | --- |`,
    ...summary.rows.map(
      (r) =>
        `| ${r.id} | \`${r.q}\` | ${r.top.replace(/\|/g, " ")} | ${r.ndcg5.toFixed(2)} | ${r.mrr.toFixed(2)} | ${r.took_ms.toFixed(1)} | ${r.hit ? "yes" : "NO"} |`
    ),
    ``,
    `Fixture corpus only. A pass here is not a pass on Jonathan’s live chats.`,
    `Memory/context boost is not in this number. Ranker regressions cannot hide behind memory.`,
  ];
  return lines.join("\n");
}
