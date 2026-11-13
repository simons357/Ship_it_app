# QStack — snapshot

This directory is a **retrieval**, not a rewrite and not a proof engine.

Hunt date: **13 November 2026**. Request: Jonathan sent **qstack** twice. Get it if it exists. Do not invent.

**Workshop lock:** ChatVault is **OS for your AI**. This snapshot does **not** claim RH or NS regularity. Documents below that talk about Clay / RH / “proved” are **his artifacts as retrieved**. They are not adopted as workshop results.

## Found?

**Yes.** Jonathan’s QStack exists in several real places. There is **no** `simons357` GitHub repo named qstack. Public `simons357` repos remain `Ship_it_app`, `ship-it-code`, `kyrana-oracle`.

| Sense | Found? | Where |
| --- | --- | --- |
| Live product page | **Yes** | https://primefield.tech/qstack — title `Qstack \| Prime Field Technologies` (HTTP 200, Base44 shell) |
| Base44 app (source) | **Yes** | **QStack Reference** `6a19046b717521480f6b9543` · published https://qstack-spectral-flow.base44.app · GitHub `base44dev/qstack-spectral-flow` (private / not cloneable from this VM) |
| Replit paper (sent twice) | **Yes** | https://replit.com/@simonsmedicalin/QStack-Resonant-Framework · live https://q-stack-resonant-framework.replit.app/ · Gmail: two Replit publish receipts 28 Mar 2026 12:27 UTC and 19:22 UTC |
| Private research whitepaper | **Yes** | `simons357/research` `whitepaper/QStack_WhitePaper.md` (GitHub API; `gh clone` 404 from this token) |
| Drive one-pagers | **Yes** | Google Doc `QStack_One_Pagers` |
| Workshop archive PDF | **Yes** | git `3daa92cd` `docs/archive/qstack/qstack_regularity_paper.pdf` (not on this branch until this snapshot) |
| ChatVault search consumer | **No** | QStack is a spectral / CFD product, not a vault. Do not merge products. Hook recipe: [`SEARCHVAULT-HOOK.md`](SEARCHVAULT-HOOK.md) |

## What it is (from his own product copy, not this workshop)

LinkedIn (29 Oct 2026, Prime Field): *“QStack: a modular framework for targeted damping in flow and transport simulations.”* Seeks CFD teams; technical working paper available.

August 2026 portfolio (`docs/portfolio/APP-PORTFOLIO-2026-08.md` on other commits): row **14 \| Q-Stack \| Hosted experiment \| primefield.tech/qstack**.

Base44 QStack Reference description: *interactive mathematical reference and visualization platform for the QStack spectral operator framework*.

## What is in this snapshot

| Path | What |
| --- | --- |
| `snapshot/primefield-qstack.html` | Live GET of https://primefield.tech/qstack (SPA shell) |
| `snapshot/qstack-spectral-flow.html` | Live GET of https://qstack-spectral-flow.base44.app (SPA shell, title QStack Reference) |
| `snapshot/replit-qstack-paper.html` | Live GET of https://q-stack-resonant-framework.replit.app/ (SPA shell, title QStack Paper) |
| `snapshot/gh-pages-qstack.html` | `origin/gh-pages` `apps/primefield/qstack/index.html` (company hub card shell) |
| `source/QStackDashboard.jsx` | Retrieved Base44 main page (operator tabs). **Not** rewritten. |
| `source/OperatorPanel.jsx` | Retrieved Q1/Q3/Q6/Q-N operator cards. **Not** rewritten. |
| `docs/QStack_WhitePaper.md` | Verbatim copy from private `simons357/research` via GitHub API |
| `docs/QStack_One_Pagers.md` | Retrieved Google Doc text |
| `docs/replit-attached-paste.txt` | Replit `attached_assets` paste that seeded the paper app |
| `archive/` | March 2026 Q1-approximation PDF already hashed in workshop git. Archive only. |

Minified vendor JS/CSS (~1 MB Replit bundle, Base44 `/assets/*.js`) stays in `/tmp/qstack-hunt/` on this VM, same as Field Lock. Not re-vendored here.

## Hashes (13 Nov 2026 fetch)

```
2bf28f7314503dc36f44e5c7c1ef3c3dfcca6970893ca49235a68de5fa5425e8  snapshot/primefield-qstack.html
2294d64260bdebe98065e881f367bc267dbfbfc10498999ffc4ebe7220c9f730  snapshot/qstack-spectral-flow.html
24dc8d172753189fa71515ced762e7a6c2b586ac1774777095e7a3e5aeb585d1  snapshot/replit-qstack-paper.html
67ce64d29586e256927b26e61e72b7391e3aaab55accba98d42bed63c351f346  snapshot/gh-pages-qstack.html
3ea9a93ac39d35e773f550c12b6f1e643f6fd65247ccf9b094d108789e7f96e8  archive/qstack_regularity_paper.pdf
```

Replit published assets (hashed in `/tmp/qstack-hunt/live/replit-assets/`, not copied):

```
99993a902502d4c38e0acd175831ac909456a65a2c1bc28137199e525d805f40  assets/index-CJc0--au.js
cf259e3e8a2b0908c58e9a2b3738da3be67f4c295ddc73e13c3f4b68272358ed  assets/index-kEkrByjt.css
76a513205a172cf4d5f659eb7914c654875eb96ce481f30746ef1ba9066a5436  images/fluid-flow.png
```

## Other QStack-named apps (his, not snapshotted as engines)

| App | ID / URL | Note |
| --- | --- | --- |
| Base44 **QStack Insight** | `69e3fb761bccedecaf393b70` | Unpublished. Internal NS/QStack status report UI (April 2026). Not a CFD SDK. |
| Base44 **QStack War Board** | `6a2225c86f3f040d6f17e1a7` | Unpublished. Empty routes (PageNotFound only). |
| Replit **Qsyack Paper** | `4b00d20b-7dc2-4717-9508-55c267f2b1a1` | Name typo. Generic pnpm workspace; **no** `qstack-paper` artifact. |
| Drive **Navier-stokes** doc | Google Doc | Same resonant-regularity paste as the Replit attached asset. |

## Not this

- Unrelated public GitHub/Wikipedia **Qstack** (Greenqloud cloud manager, Saint Louis test-automation company, quantum-compiler paper by Paz/Grossman).
- ChatVault PWA, CLAIM_LEDGER, Domain Architect.
- Desktop path `DIGEST_ChatGPT_*_coherence_Q.md` — not on this VM.
- `RH_Proof_Chain` as a cloneable product — not found as a repo or app. Workshop git already rejects Q-stack as constitutive NS (`15a456af` and related).

## Full clone on this hunt VM

`/tmp/qstack-hunt/` — live HTML, Replit assets, archive PDF. Research git clone failed (`gh`/`git` 404 for private `simons357/research`; file read succeeded via GitHub API).
