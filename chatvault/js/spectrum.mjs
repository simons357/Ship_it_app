/**
 * Ledger spectrum — a status mix, not a truth meter.
 * PROVED means a person marked it inside this vault.
 */

import { LEDGER_STATUSES } from "./engine.mjs";

export const SPECTRUM_VERSION = "chatvault-spectrum-0.1.0";

export function ledgerSpectrum(entries) {
  const counts = Object.fromEntries(LEDGER_STATUSES.map((s) => [s, 0]));
  let total = 0;
  for (const entry of entries || []) {
    const rows = [...(entry.key_claims || []), ...(entry.theorems || []), ...(entry.open_gaps || [])];
    for (const row of rows) {
      const status = LEDGER_STATUSES.includes(row.status) ? row.status : "UNREVIEWED";
      counts[status] += 1;
      total += 1;
    }
  }
  const bands = LEDGER_STATUSES.map((status) => ({
    status,
    count: counts[status],
    share: total ? counts[status] / total : 0,
  })).filter((b) => b.count > 0);
  return {
    version: SPECTRUM_VERSION,
    total,
    counts,
    bands,
    provedShare: total ? counts.PROVED / total : 0,
    caption:
      "Ledger spectrum. PROVED is a human mark in this vault, not a proof, journal, or court.",
  };
}
