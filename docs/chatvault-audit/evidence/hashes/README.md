# Hash freeze notes

`SHA256SUMS.txt` records files in this packet plus the live Base44 preview bundles hashed on 24 August 2026.

Lines whose path starts with `/tmp/chatvault-probe/bundles/` are **not in git**. They are the minified JS (and matching HTML) fetched from:

- `https://preview--6a58e103fedcde66a0a7710e.base44.app/assets/index-DXcRcOPA.js`
- `https://preview--6a58f25d90370ad28d426a88.base44.app/assets/index-oJLKHp-g.js`
- `https://preview--6a36239133fe30857adcef89.base44.app/assets/index-CcQAsgPf.js`

Re-fetch those URLs and compare SHA-256 before any legal, product-repo, or App Store action. If the hash moved, this audit’s freeze is stale.

HTML snapshots under `evidence/html-snapshots/` are committed copies of the preview documents (same hashes as the `/tmp/...html` lines).
