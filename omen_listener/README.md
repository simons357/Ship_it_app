# OMEN listener

Portable civil-warning code for a safety app. Phones, wearables, and tree-top
sensors listen for a rotor-like harmonic stack. When those listeners produce a
track toward a protected point, the OMEN decision window says where the
contact is and how many seconds are left to decide to get inside.

The window is a shelter clock. It does not name an airframe, and it does not
aim, jam, or intercept anything.

OMEN is the name of that window. An omen is a prediction, and the word by
itself sounds like a bad one. This one is the good prediction: you still have
seconds to get inside. The contact is the bad news. The window is the part
that arrived in time.

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

## What can join

Anything that can hand over an `omen.bundle` can sit on the mesh. Coverage is not the same for each kind.

- AirPods, or any earbuds, are a wearable. They cover the room you are standing in. Apple does not publish a meter range for the Bluetooth 5.3 link; one ordinary room is the practical bubble. The cue they add is "I hear it." They do not aim a bearing. The phone on the table is the computer, and it hears the rotor band (80–250 Hz) more usefully than a voice mic in your ear.
- The coverage sphere is a play model of that room, in `overlay/sphere.html`. AirPods are a 3 m sphere centered at the ear (1.6 m). A phone on listen is a 6 m sphere centered at the pocket (1.0 m). Outdoors the AirPods sphere tops out at 4.6 m. Indoors a 2.7 m ceiling cuts it. Another member with a phone is inside your AirPods sphere only when the mic-to-mic gap is 3 m or less. Handing the bundle across is a separate 10 m phone-to-phone step. The tree line is still the kilometer.
- A pointed phone defaults to 8°. A wearable defaults to 12°. A tree-top pair defaults to 3°, which is what reaches out toward a kilometer.
- A desk, including this screen, can hold the picture, the notes, and the RMSE line with no microphone at all. It speaks the sentence. It does not hear the air.
- A hydrophone is a water listener. Keep it off the shelter clock. A $75 underwater mic is a toy for splashes. The current Aquarian H2d lists at $256 and is the general-purpose piece; the older H2a was advertised nearer $170. Dolphin whistles need a recorder that samples well above this listener's 16 kHz frames. Clicks need on the order of 192 kHz. Listening from shore is the whole lab. Playback into the water is not part of this package.

## Coherence

Listeners that report in the same second as the shared fix are the lit part of the field. Two or more of them, plus a fix, is `locked`. One cue with no shared fix is `partial`. Nothing heard is `quiet`. The overlay draws the locked field in neon yellow. Idle listeners stay dim, because a grey mark is easy to miss and is not the event.

## RMSE

The shelter circle never draws smaller than 20 m. That floor is right for a decision to go inside, and too coarse for a plate. RMSE is the same crossing with the floor left off: the root-mean-square miss of the bearings, in meters.

`picture["rmse"]` is the patch your plate software already knows how to read. `try_plate` is true when the contact is within 40 m of an aiming listener and the RMSE is 12 m or less. The label is one line, for example `RMSE 6 m · 30 m out · plate`. This package does not read a plate, store a plate, or open a camera.

On the overlay the RMSE line is neon yellow whenever a fix exists. The wide shelter circle stays dim when the RMSE patch is tighter, so the eye stays on the patch.

## Field notes

Personal notes stay on this listener until you send them. `send_smart` writes one line from the picture you are looking at (`38s · 1.5 km north of the protected point · field locked`) and puts it on the bundle. When `try_plate` is set, that line also carries the RMSE label, so one tap hands your plate software the patch. Presets are `Inside`, `I hear it`, `I don't hear it`, and `Clear here`. `click_off` removes a note from this listener, including a copy you received.

## Overlay

Open `omen_listener/overlay/index.html` from a local server (the page fetches
`state.json`). It shows the decision time, where the contact is, and the
listeners. "15s later, comms down" is the same track with no new cue.
"Close contact" is a curb pair with the contact about 28 m out, where the RMSE line says plate.
"Open a JSON file" accepts either a picture or a state document.

```bash
python -m http.server 8765
# http://127.0.0.1:8765/omen_listener/overlay/
```

## Tests

```bash
python -m unittest tests.test_omen_listener
```
