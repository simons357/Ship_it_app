# OMEN listener

Portable civil-warning code for a safety app. Phones, wearables, and tree-top
sensors listen for a rotor-like harmonic stack. When those listeners produce a
track toward a protected point, the OMEN decision window says where the
contact is and how many seconds are left to decide to get inside.

The window is a shelter clock. It does not name an airframe, and it does not
aim, jam, or intercept anything.

Fans, mowers, and helicopters can make the same sound. Treat a cue as a
prompt to look and to move indoors, not as identification.

## Drop-in

Python, standard library only:

```python
from omen_listener import GeoPoint, ListenerSession

session = ListenerSession("north-oak", GeoPoint(40.0, -74.0), label="north oak")
session.apply_wake({
    "community_id": "north-oak",
    "alert_id": "alert-1",
    "command": "listen",
    "issued_at": now,
    "ttl_s": 600,
    "source": "wearable",
}, now)

session.ingest_pcm(node, samples, 16000, now, azimuth_deg=12)
# or a tree-top box that already computed a bearing:
session.ingest_observation(cue)
# a neighbor's bundle, carried over Bluetooth, a file, or a local radio:
session.ingest_bundle(bundle)

picture = session.picture(now)
picture["omen"]["decision_seconds"]  # seconds left to decide
picture["omen"]["where"]             # where the contact is
picture["layers"]                    # overlay geometry, meters east/north
```

The same `state` document runs in the browser with no build step:

```html
<script src="omen_listener/portable/omen_listener.js"></script>
<script>
  const picture = OmenListener.buildPicture(state);
</script>
```

`python -m omen_listener picture --state state.json` prints the window.
`python -m omen_listener demo --out omen_listener/overlay` rewrites the sample
the overlay page reads.

## What opens the window

A wearable `listen` message wakes the phone microphone. Cues from every
system in the community are merged locally. The window stays closed until
bearings cross into a fix and that fix is moving toward the protected point
inside the watch radius (default 1 km).

The number on the clock is already reduced by two things:

- place error: the bearing circle turned into seconds, at the track's speed
- lead time: default 30 seconds, the time assumed to get inside

What remains is the decision time. At zero, the guidance is to shelter in
place, away from windows.

## Comms down

Nothing in this package opens a socket. Nodes exchange `omen.bundle` JSON.
If cues stop arriving, the last track is projected for 45 seconds and then
held. The picture is marked `comms: "down"`. The overlay draws from meters
east and north of the protected point, so it does not need map tiles.

A `community_token` keeps two neighborhoods from mixing packets by accident.
It is not authentication.

## Several systems

`kind` is `phone`, `wearable`, or `treetop`, and any other string is kept.
A tree-top pair defaults to a 3° bearing, a pointed phone to 8°, a wearable
to 12°. The tighter tree-line bearing is what lets a neighborhood time a
contact while it is still about a kilometer out. Phones that only hear the
sound still show up, so the block can see who has a cue.

A phone with two microphones can pass `array` (`left`, `right`, `spacing_m`,
`heading_deg`) instead of a hand-aimed azimuth.

## Overlay

Open `omen_listener/overlay/index.html` from a local server (the page fetches
`state.json`). It shows the decision time, where the contact is, and the
listeners. "15s later, comms down" is the same track with no new cue.
"Open a JSON file" accepts either a picture or a state document.

```bash
python -m http.server 8765
# http://127.0.0.1:8765/omen_listener/overlay/
```

## Tests

```bash
python -m unittest tests.test_omen_listener
```
