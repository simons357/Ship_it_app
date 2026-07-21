# Field Lock — presence-bound keys

**Live demo (Learning Kiosk):** https://field-lock.replit.app/  
**Not this:** `https://primefield.tech/field-lock` — empty Base44 shell; do not cold-send.

**One-liner:** Field Lock creates a **brand-new, single-use key** only when **real-world presence conditions** are met — so access stays bound to who is actually there.

---

## What the public kiosk teaches (safe to send)

| Idea | Plain language |
| --- | --- |
| **Presence & quorum** | UWB time-of-flight, BLE RSSI, motion — N-of-M people must be physically there. Presence tokens TTL ≤ ~15 s. |
| **Attestation** | Module proves boot / firmware / policy before it will mint a key. |
| **Replay resistance** | Keys exist for seconds; recorded traffic has no persistent secret to steal later. |
| **PQC complement** | Works alongside post-quantum session crypto — Field Lock binds *when/who* the session keys can be born. |

SpectraLock = spectral locking naming lane in the same presence / encryption family.

---

## Hardware / entropy spine — PUF + CTW

You also have a **PUF** (physically unclonable function) path — silicon / device fingerprint that is not stored as a conventional key — and **CTW** (Context Tree Weighting) as the entropy / predictability analysis method used with PUF responses in the literature and in your materials.

| Piece | Role | Public say |
| --- | --- | --- |
| **PUF** | Device-unique physical fingerprint → key material regenerated, not parked in flash | “Hardware root that can’t be cloned off a dump” |
| **CTW** | Entropy / secrecy-rate style analysis of PUF responses (incl. spatial correlation awareness) | “How we measure that the fingerprint is actually unpredictable” |
| **Presence bind** | Soft + hard presence signals gate *when* a key may exist | “Key only while the rightful party is there” |
| **PUF picture** | Visual for partners | Slot below — **re-upload required** |

**Guardrail:** Recipe, challenge–response tables, CTW parameters, and claim numbers stay **NDA / vault**. Cold send = kiosk + one-liner + (when ready) the PUF photo.

### PUF image slot

| Item | Status |
| --- | --- |
| Intended asset | PUF hardware / response visualization photo |
| Found in repo | `assets/46fb5932-9b74-4d0e-acc4-7685bcf3187c_1 3.JPG` |
| Usable? | **No** — file is UTF-8–mangled (binary → replacement characters). Not a valid JPEG. |
| Action | Re-drop a clean `.jpg` / `.png` into `assets/` (e.g. `assets/field-lock-puf.jpg`) and paste path here: _______________ |

---

## Cold outreach — include Field Lock again

1. **Field Lock** — https://field-lock.replit.app/  
2. Maritime Coherence Dashboard — https://maritime-coherence-dashboard-100b68c0.base44.app/  
3. NAV-42 — https://nav-42.replit.app/

Optional on call / NDA: “Same lane includes a PUF + CTW entropy spine; I’ll send the photo and eval pack under NDA.”

---

## Open slots

| Item | Value |
| --- | --- |
| Clean PUF image path | _______________ |
| Separate PUF/CTW lab note or paper URL | _______________ |
| Hardware SKU / module name | _______________ |
| Provisional / filing # | _______________ |
