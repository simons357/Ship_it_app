# Lemma★ SoT → Desktop sync bundle

Cloud agents **cannot** write Jonathan’s Mac Desktop. This folder is the
one-command sync pack for:

`~/Desktop/Harmonic Universe Book/`

## Files (source of truth)

Copied from branch `cursor/ns-five-lane-lemma-star-1390` paths:

- `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`
- `docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`
- `docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md`

PR: https://github.com/simons357/Ship_it_app/pull/48

## Mac: one command

From a checkout of this branch:

```bash
cd /path/to/Ship_it_app
git fetch origin
git checkout cursor/ns-five-lane-lemma-star-1390
chmod +x jonathan-handoff/GROK-HEAVY/01-swirl-publishing/lemma-star-sot/SYNC_TO_DESKTOP.sh
./jonathan-handoff/GROK-HEAVY/01-swirl-publishing/lemma-star-sot/SYNC_TO_DESKTOP.sh
```

Or explicit `cp` (backs up with `.bak` first):

```bash
BOOK="$HOME/Desktop/Harmonic Universe Book"
SRC="jonathan-handoff/GROK-HEAVY/01-swirl-publishing/lemma-star-sot"

cp "$BOOK/LEMMA_STAR_SHAPE_FORM.md" "$BOOK/LEMMA_STAR_SHAPE_FORM.md.bak"
cp "$BOOK/LEMMA_STAR_EXACT_FORMULAS.md" "$BOOK/LEMMA_STAR_EXACT_FORMULAS.md.bak"
cp "$BOOK/LEMMA_STAR_CANONICAL.md" "$BOOK/LEMMA_STAR_CANONICAL.md.bak"

cp "$SRC/LEMMA_STAR_SHAPE_FORM.md" "$BOOK/"
cp "$SRC/LEMMA_STAR_EXACT_FORMULAS.md" "$BOOK/"
cp "$SRC/LEMMA_STAR_CANONICAL.md" "$BOOK/"
```

Override destination if needed:

```bash
HARMONIC_BOOK_DIR="/path/to/Harmonic Universe Book" ./SYNC_TO_DESKTOP.sh
```
