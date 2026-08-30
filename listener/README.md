# LISTENER

What the wild is saying.

A wildlife-only acoustic field instrument. Not Ship It. Not Listener search. Not a generic checklist.

Build from [`MASTER_SPEC.md`](MASTER_SPEC.md). Keep the visual/product behavior in [`inbox/index.html`](inbox/index.html).

## Run the iPhone preview

```bash
cd listener/app
python3 -m http.server 4173
```

Open http://127.0.0.1:4173/ on a phone-sized viewport.

## Native App Store target

```text
listener/ios/Listener.xcodeproj
```

See [`ios/README.md`](ios/README.md) and [`store/APP-STORE.md`](store/APP-STORE.md).

## Tests

```bash
python3 -m unittest listener.tests.test_listener_core
```

or:

```bash
python3 -m unittest discover -s listener/tests
```

## Non-negotiables

- Non-human biological signals only for encounters and the library
- Privacy by default
- No invented animal positions
- No fake COH values
- No forced species IDs
- Originals preserved
- Sharing ≠ contributing
- Offline must not lose the Session
- UI stays simple
