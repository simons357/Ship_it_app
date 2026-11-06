# ChatVault hybrid search — license unit

**File:** `js/search.mjs`  
**Version:** `chatvault-hybrid-0.2.0`  
**No DOM. No network. No localStorage.**

```js
import { searchVault, searchEntries, SEARCH_ENGINE_VERSION } from "./search.mjs";
```

`searchVault(records, query, filters?)` → `{ engine, parsed, took_ms, total, hits }`  
Each hit: `{ entry, score, snippets, matched_fields, signals }`.

Pipeline: parse AND/OR/`"phrase"`/`field:` → inverted index → hard filters →
boolean gate → BM25F (K1=1.2) → char 3-gram BM25 → field-weighted TF-IDF cosine
→ RRF k=60 → optional RM3.

Unfielded rank uses title, claim, theorem, gap, question, action, tag, book,
summary, content, ai, source. `status:` and `origin:` are designations, not
quality boosts. Ledger status is never a ranking signal.

This is not Evernote search. It is a fielded research ranker over a claim ledger.
