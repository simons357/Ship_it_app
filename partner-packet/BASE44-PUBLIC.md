# Base44 public access — broken (2026-07-21)

## What’s happening

Visitors (and cold-email recipients) see:

> **Couldn't load the app**  
> You may not have permissions to access it.  
> Please refresh or reach out to support

Checked apps are returning Base44 **platform** config (`APP_FLAVOR: "platform"`) instead of a published public app shell. That means the URL looks alive (HTTP 200) but the runtime asks for owner / workspace permissions.

## Affected (do not cold-send until republished public)

| App | URL |
| --- | --- |
| Maritime Coherence Dashboard | https://maritime-coherence-dashboard-100b68c0.base44.app/ |
| Harmonic Insights / Resources | same host `/HarmonicInsights` · `/Resources` |
| ExoRatio | https://exo-ratio-014dea2d.base44.app/ |
| Primefield Explorer | https://sfe-rh-explorer-v1-07f8121c.base44.app/ |
| Solenne | https://solenne.base44.app/ |
| primefield.tech (company + ChatVault / Field Lock routes) | https://primefield.tech/ |

## Still safe to cold-send (Replit)

| App | URL |
| --- | --- |
| **Field Lock** Learning Kiosk | https://field-lock.replit.app/ |
| **NAV-42** Adaptive Lattice | https://nav-42.replit.app/ |

## Fix (you, in Base44)

1. Open each app in **Base44** while logged in as owner.  
2. **Publish** / set visibility to **Public** (not “private / workspace only”).  
3. Confirm in an **incognito / logged-out** browser that the real app loads — not “Couldn't load the app.”  
4. Paste working public URLs back into `ADDRESSES.md` and tell the showcase they can go live again.

Until then: cold outreach = **Field Lock + NAV-42 only** (plus optional third once a Base44 app is confirmed public).
