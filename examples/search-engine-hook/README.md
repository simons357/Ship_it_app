# Search-engine hook (copy this)

**Ranker:** `chatvault/js/search.mjs` (`chatvault-hybrid-0.2.0`).  
**API:** `chatvault/js/ENGINE.md`. Not a license agreement.

```bash
node examples/search-engine-hook/hook.mjs
```

Import the single module (copy the file, or same-origin `/chatvault/js/search.mjs`). Map your docs to `id`, `title`, and `content_text` / `raw_content`. Call `searchVault(records, query)`. You do not get the PWA, localStorage vault, CLAIM_LEDGER, or Domain Architect. Cross-origin module import needs CORS on GET; copying the file does not.
