# The leftover object

A small local app that shows the Lemma★ shape.
**NS not solved. Bound open.** Not a prize page.

```bash
python3 scripts/ns_attacks/build_object_gallery.py
python3 -m http.server 8765 --directory apps/the-object
```

Then open `http://127.0.0.1:8765/`.

The folder is the release: `index.html`, `app.js`,
`style.css`, `data.js`, `stills/`. Drag it, zip it,
host it. The picture is the object. The bound is
still the hole.

Numbers come from `ns_lemma_star_core.py`. Live
`stokes_moments.py` is not used. A finite K is not
C0. An aligned closer recovers K. An orthogonal
closer does not.
