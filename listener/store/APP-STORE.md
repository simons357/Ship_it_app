# LISTENER — App Store pack

Owner: Jonathan Simons  
Bundle ID: `tech.primefield.listener`  
Display name: LISTENER  
Category: Navigation (primary) / Lifestyle (secondary)  
Age rating: 4+ (no user-generated public chat required for V1; Broadcast watching is local)

## Honest status

This pack is listing copy and a Mac/Xcode checklist. **We cannot enroll in the Apple Developer Program ($99/year) or upload a binary from the Linux cloud VM.** Open `listener/ios/Listener.xcodeproj` on a Mac to archive and send to TestFlight.

## Privacy nutrition (App Store Connect)

| Data | Collected | Linked to identity | Used for tracking | Purpose |
| --- | --- | --- | --- | --- |
| Precise location | Yes, on device | No | No | App functionality (Session Start, breadcrumb, RETURN) |
| Coarse location | Only if the user contributes | No | No | App functionality |
| Audio | Yes, on device | No | No | App functionality (wildlife evidence). Not transcribed. No speaker ID. |
| Photos | Only if the user attaches a field-note photo | No | No | App functionality |
| Product interaction | Optional local session log | No | No | App functionality |

Default: exact home coordinates, raw Wander routes, precise node positions, and private media stay on the phone.

Sharing a Listener Card is **not** contributing the original to the Signal Library.

Privacy policy (host this file on HTTPS before review): `listener/app/privacy.html`

## Usage strings (already in Info.plist)

- Microphone: Listener uses the microphone to record wildlife sounds around you. Recordings stay on this phone until you choose to share or contribute.
- Location: Listener uses your location to mark where you started, draw your wander, and help you find your way back. Exact location stays private unless you choose otherwise.
- Camera / Photos: Listener can attach a photo to a field note.

## Review notes

LISTENER is a wildlife-only field instrument. Probable human speech does not create a wildlife encounter and cannot be contributed. Field Coherence (DA) shows an em dash and **INSUFFICIENT FIELD DATA** until two or more nearby synchronized nodes produce a real measurement. RETURN highlights a recorded trail back to Session Start. It is a safety aid, not a replacement for Maps.

Map modes FIELD / SATELLITE / HYBRID use MapKit on iPhone. The web preview does not scrape or redistribute Apple or Google tiles.

## Screenshots to capture on an iPhone

1. Onboarding — “What the wild is saying.”
2. Three doors — LISTEN HERE / GO SCOUT / START A BROADCAST
3. Field with BASE, instrument showing —, RETURN off
4. Field note sheet (SAW / HEARD / PHOTO / MYSTERY)
5. SIGNALS library + **SEND US YOUR LISTENER SIGNALS**
6. Broadcast watch vs join-as-node

## Mac upload steps

See `listener/ios/README.md`. Short version: paid Apple Developer team → Archive → App Store Connect → TestFlight → submit.
