# LISTENER — MASTER BUILD SPEC

Source: owner ChatGPT pre-design, ingested 2026-08-30.
Prototype: `inbox/index-2.html`
Reference photo: `inbox/IMG_1058.HEIC`

## Product sentence

Listener is a distributed, wildlife-only acoustic exploration platform that turns phones, AirPods, computers and future sensors into a simple field network.

## Design law

Complex underneath. Obvious on top.

If a normal user must understand networking, routing, synchronization or signal processing to use a feature, the feature is not finished.

## Mark

The LISTENER icon is a home node with rings going out: listening for intelligent life that is **not human** — animals, insects, birds, and the weather they live in.

Same family as Descent: solid black tile, one warm amber handmade glow. Not Descent’s inward spiral. Not a cartoon zoo. Not a photoreal slate. Not SETI chrome.

Assets: `app/icons/home-node.png` (source) and the sized `icon-*.png` / iOS AppIcon set.

## Three doors

- **LISTEN** — One-device wildlife listening. Home Field can designate a stationary device as BASE.
- **SCOUT** — The moving phone. Use its microphone or supported AirPods input. Record GPS breadcrumb, heading, field notes and local evidence. RETURN highlights the recorded trail back to Session Start. It is a safety aid, not a replacement for normal navigation.
- **BROADCAST** — The social room. People can watch, listen to intentionally broadcast content and comment. A Session can run inside a Broadcast. Sensor contribution is a separate explicit opt-in.

## Distributed field

Roles are automatic:

- **HUB:** Mac/desktop or designated coordinator/dashboard.
- **BASE:** stationary Listener phone.
- **SCOUT:** moving Listener phone.
- **NODE/STATION:** additional remote contributor.

Nodes may be nearby or internet-connected. Widely separated nodes contribute independent regional observations; only geometrically relevant nearby synchronized nodes should be used for localization.

## Network behavior

Transport is an implementation detail:

1. usable local network / peer connection
2. internet transport where configured
3. store locally and synchronize later

Every device records authoritative original evidence locally. Exchange lightweight timestamps, fingerprints, detections, location/accuracy and health live. Do not require uninterrupted raw-audio streaming.

## Wildlife-only rule

Listener encounters are for non-human biological signals.

Probable human speech:

- do not transcribe
- do not identify the speaker
- do not create a wildlife encounter
- do not contribute it to the wildlife Signal Library
- discard/exclude it from downstream wildlife analysis as early as practical

Classifiers are fallible, so label the decision as probable-human exclusion internally.

## Data architecture

**Reference Layer:** external licensed/permitted taxonomy, occurrence, habitat, seasonality, conservation and vocalization metadata.

**Listener Signal Library:** opted-in original recordings + derived features + provenance + coarse location + sensor metadata + candidate ID/confidence + validation state + DA/Coh-Rez results when legitimate.

Never silently merge provenance. Track whether a claim came from a reference source, classifier, user, expert validation or Listener measurement.

## Unknowns

UNKNOWN is first-class data. Preserve original evidence and re-run improved models later.

## Core object model

Broadcast → Sessions → Fields/Nodes → Encounters → Field Notes/Media → Listener Cards.

Signal Library stores contributed observations separately from a user’s private Session library.

## Privacy

Private by default:

- exact home/property coordinates
- raw Wander routes
- precise node positions
- private media

Sharing and contributing are distinct permissions.

Public/contributed location defaults to coarse geography unless the user explicitly elects otherwise.

## Maps

Native iOS V1: Apple MapKit imagery behind a MapProvider abstraction.

Modes: FIELD / SATELLITE / HYBRID.

Show: user, Session Start, breadcrumb, Base/Scout/Stations, encounters, probabilistic source regions, GPS degradation.

Never scrape or redistribute map imagery.

## DA / Coh-Rez

COH is a real instrument, never decoration.

If data are insufficient: — / INSUFFICIENT FIELD DATA.

A computed result stores definition, sensors, window, frequency bands, quality/uncertainty and contributing relationships.

Field Color can be a transparent artistic mapping from measured features.

## Sound/X-Ray Lab

Real operations only: ISOLATE · CLEAN · LOOP · STRETCH · PITCH · HARMONICS · COMPARE · LOCALIZE · MATCH · SONIFY · VISUALIZE · SEND TO DA

Preserve original audio and label transformations.

## Signal contribution

CTA: SEND US YOUR LISTENER SIGNALS.

Opt-in contribution should include only allowed non-human evidence and safe metadata.

A user can contribute without publicly sharing.

A user can share a Card without contributing the original to the common library.

## V1 native stack

SwiftUI, MapKit, Core Location, AVFoundation / AVAudioSession, SwiftData or Core Data, PhotosUI/camera, native share sheet.

Backend: authenticated Session/Node presence, event messaging, opt-in Signal Library upload, provenance, coarse-location transformation and Broadcast presence/chat.

Later: Multipeer Connectivity, hydrophones, ultrasonic microphones, external visual sensors.

## Build order

1. local Session database
2. Base / Scout role selection
3. GPS breadcrumb + RETURN
4. MapKit FIELD/SAT/HYBRID
5. microphone route diagnostics and recording
6. Field Notes + media
7. two-device sync and offline reconciliation
8. wildlife event pipeline + human-speech exclusion
9. Listener Cards/share
10. Signal Library contribution/provenance
11. Broadcast viewer experience
12. remote nodes
13. multi-station localization with uncertainty
14. DA/Coh-Rez
15. Sound/X-Ray Lab
16. additional sensors

## Consumer onboarding

Screen 1: LISTENER — What the wild is saying.

Screen 2:

- LISTEN HERE
- GO SCOUT
- START A BROADCAST

If another owned/paired device appears: Another Listener is available. LEAVE AS BASE?

No networking vocabulary unless the user opens diagnostics.

## Failure language

Bad: “Peer socket disconnected / route negotiation failure.”

Good: Scout connection lost. Still recording — we'll sync when you're back.

## Product test

A first-time user with two phones should be able to leave one on a porch and begin scouting with the other in under a minute without understanding the network architecture.
