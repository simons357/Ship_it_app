# Subjects — keep-up index

One page to see **what this repo is about** and **where each thread lives**.

Update this file when a subject changes status (merge, park, abandon, or rename).  
Last reviewed: **2026-10-01** (transfer-lemma kill lock filed).

---

## How to read this

| Status | Meaning |
| --- | --- |
| **On main** | Merged — start here |
| **Active drafts** | Open PRs still moving |
| **Parked** | Keep for reference; don’t extend unless asked |
| **Abandoned** | Do not revive |

---

## Active subjects

### 1. Domain Architect (DA)

| | |
| --- | --- |
| **What** | Equation / model auditing — roles, conflicts, registry. Not a unified physics theory. |
| **Status** | **On main** |
| **Start here** | [`docs/domain-architect/README.md`](domain-architect/README.md) · package `domain_architect/` |
| **Also see** | Open DA / SoT / NS-adjacent drafts (many PRs) |

### 2. Navier–Stokes close plan (DA-NS / unaugmented NS)

| | |
| --- | --- |
| **What** | Unaugmented 3-D NS proof pathway, gates, audits, teaching packs. |
| **Status** | **Active drafts** (largest open pile) |
| **Start here** | Newest open: [#145](https://github.com/simons357/Ship_it_app/pull/145) audit package · [#142](https://github.com/simons357/Ship_it_app/pull/142) Sprint 01 |
| **Related gate stack** | Gates / SAG / lemmas / Fourier-triangle / MIN-CYCLE / channel algebra — dozens of open PRs (see GitHub “Open”) |

### 3. Phi-renorm / swirl papers

| | |
| --- | --- |
| **What** | Φ-renorm swirl TeX/PDF + Aug 22 audit KEEP routing. |
| **Status** | **On main** (papers + ns-review notes) |
| **Start here** | [`docs/ns-review/README.md`](ns-review/README.md) · [`docs/papers/swirl/`](papers/swirl/) · [`docs/papers/phi-renorm/`](papers/phi-renorm/) |

### 4. Harmonic Blueprint / ringdown (HB Experiment 01)

| | |
| --- | --- |
| **What** | Cross-event QNM spectral selection test. |
| **Status** | **On main** — **closed** (held-out TEST did not reject H0) |
| **Start here** | [`HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](HB-RINGDOWN-EXPERIMENT-01-REPORT.md) · [`results/SUMMARY.md`](../results/SUMMARY.md) |

### 5. Zenodo inventory

| | |
| --- | --- |
| **What** | Live vs stale deposit inventory correction + deposit metadata. |
| **Status** | **On main** |
| **Start here** | [`docs/zenodo/INVENTORY-CORRECTION-2026.md`](zenodo/INVENTORY-CORRECTION-2026.md) · `data/zenodo/` |

### 6. Process / measurements console

| | |
| --- | --- |
| **What** | How results are stamped (e.g. INCONCLUSIVE), unfinished measurements. |
| **Status** | **Active drafts** |
| **Start here** | [#136](https://github.com/simons357/Ship_it_app/pull/136) · [#135](https://github.com/simons357/Ship_it_app/pull/135) |

### 7. RH / Q₆ / transfer lemma (Mertens bridge)

| | |
| --- | --- |
| **What** | Inverse-GCD / Möbius–GCD \(Q_6\) arithmetic is real. The arrow from a locked spectrum to \(M(x)=O(x^{1/2+\varepsilon})\) is **not**. |
| **Status** | **OPEN** — kill lock filed 14 Sep 2026. **Not an RH proof.** |
| **Start here** | [`docs/rh/TRANSFER_LEMMA_OPEN.md`](rh/TRANSFER_LEMMA_OPEN.md) |
| **Calc draft** | [#86](https://github.com/simons357/Ship_it_app/pull/86) (`Q6_MERTENS_TRANSFER.md`) |
| **Do not** | Paste SFE / Explorer cosine sums / Route C “RH proved” language into this lane |

---

## Other threads (draft / judgment)

These are **not** the main science stack. Review only if you still care:

| Subject | Typical PRs / notes | Status |
| --- | --- | --- |
| Cursor / workspace setup | Foundation / setup-advisor drafts | Optional |
| Portfolio / LinkedIn / Prime Field / TITAN-X | Business / intro packets | Draft judgment |
| AquaQuartz | Brochure / investor plain plan | Draft judgment |
| Anesthesia / Operator Assist | Older abandon-PR lane | Draft judgment |
| Tarot / Harmonic Tarot | Product lock drafts | Parked / judgment |

---

## Abandoned (do not revive)

| Subject | Note |
| --- | --- |
| **Ship it** (app) | Early Next.js / send-path / GitHub helper — dead. Repo *name* is historical only. |
| **Planet Hunter** / ExoRatio-as-app | Dead |
| **Scallion** logo / branding | Dead |

---

## Quick “what should I open?” 

1. Science software on disk → **Domain Architect** + README  
2. Big open proof fight → **Navier–Stokes** open PRs (sort by recently updated)  
3. Papers already filed → **Phi-renorm / swirl** under `docs/papers/`  
4. Closed null experiment → **HB Experiment 01**  
5. Deposits list → **Zenodo**  
6. RH status (bridge still missing) → **Transfer lemma OPEN** kill lock  


To refresh the open-PR pile yourself:

```bash
gh pr list --state open --limit 30
```

---

## Edit checklist (when you or an agent update this)

- [ ] Change **Status** if something merged or died  
- [ ] Point **Start here** at the best single entry file or PR  
- [ ] Bump **Last reviewed** date at the top  
- [ ] Do **not** list every gate PR — keep buckets, not a dump  
