# ChatVault feature matrix

One row per feature. Columns are builds we could actually reach.  
`W` = works (exercised) · `P` = partial · `B` = broken · `A` = absent · `U` = unreachable here.

| Feature | A landing+Drive `6a58f25d…` | B glass `6a58e103…` | C paper `6a362391…` | Claude original | git `chatvault/` engine |
| --- | --- | --- | --- | --- | --- |
| Morph-glass “OS for your AI” UI | P (tagline, not glass vault) | W | A | U | A (look lock reversed; Steel/Ink/Signal/Day skins; glass not selectable) |
| Conversation vault grid | A | W | A | U | W |
| Paper/document vault | A | A | W (empty) | U | A |
| Marketing landing | W | A | A | U | A |
| Google Drive import | P (OAuth wall) | P (Connect Drive) | A | U | A |
| Paste ingest | A | W | A | U | W |
| Bulk paste | A | W | A | U | W |
| Media ingest | A | P (UI present) | A | U | P (pictures ≤12MB data URL; movies/audio metadata stubs) |
| PDF/DOCX/OCR | A | A | P (upload copy) | U | P (searchable stub; no text extract / OCR) |
| Immutable raw text | A | B (`raw_content` null on export) | U | U | W |
| AI summary | A | W | P (Supreme Search) | U | P (optional; never replaces raw) |
| Source AI provenance | A | P (`pasted` only) | A | U | W |
| ChatVaultEntry claims/theorems/gaps | A | A | A | U | W |
| CLAIM_LEDGER / no auto-PROVED | A | A | A | U | W |
| Books / collections | A | W | A | U | W (`related_projects`) |
| Tags | A | W | A | U | W |
| Artifacts extraction | A | B (0 items) | A | U | W (derived from ledger; no LLM) |
| Plain search | A | W | P | U | W (BM25F match gate) |
| Ranked BM25F + inverted index | A | A | A | U | W |
| Hybrid RRF (BM25F + n-gram + TF-IDF + RM3) | A | A | A | U | W |
| Typo / stem recall | A | A | A | U | W |
| Highlighted snippets | A | A | A | U | W |
| Search eval (nDCG / MRR) | A | A | A | U | W |
| Semantic / LLM search | A | W | W (copy) | U | A (dense model later; no LLM rank toggle) |
| Harmonic Watch / `harmonic_note` | A | W (panel prints ingest string; **not a ranker**) | A | U | P (stored as notes; **never a score**) |
| OR / phrase / field search | A | A | A | U | W |
| Private vs professional | A | A | A | U | W |
| Per-item JSON export | A | W | A | U | W |
| Bulk export | A | A | A | U | W |
| Export omits private | A | A | A | U | W |
| Auth / RLS / two-account isolation | A | B (public preview is world-writable) | U | U | A (local-only) |
| Pagination / virtualization | A | B (list 200/500, no windowing) | U | U | W (50/page) |
| Error boundary / failed-load ≠ empty | A | P | P (empty copy) | U | W |
| Mobile 390px | U | W (preview) | U | U | W |
| Editor opens on phone | B (login/freeze) | B (login/freeze) | B | U | n/a |
| Published `*.base44.app` | B 404 | B 404 | B 404 | n/a | n/a |
| Stripe | A | A (Recharts “stripe”, not billing) | A | U | A |
| PWA | A | P (manifest warnings) | A | U | W (manifest + service worker v0.6.0; CSP loopback drain) |
| Origin AI vs real (`origin_class`) | A | A | A | U | W (`origin:ai` / `origin:human`; not a rank boost) |
| ChatGPT export / DA drain | A | A | A | U | W (file drop or `127.0.0.1:7847`; DA is FRA, not a proof) |
| Real user research corpus | U | Unproven (looks like seed) | Empty | U | Fixtures only |

**IDs**

- A: https://preview--6a58f25d90370ad28d426a88.base44.app/
- B: https://preview--6a58e103fedcde66a0a7710e.base44.app/
- C: https://preview--6a36239133fe30857adcef89.base44.app/
- Engine: `chatvault/` in this repo (local `python3 -m http.server 4173`)
