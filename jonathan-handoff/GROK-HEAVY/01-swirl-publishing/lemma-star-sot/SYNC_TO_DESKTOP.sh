#!/usr/bin/env bash
# Sync corrected Lemma★ SoT markdown into Desktop Harmonic Universe Book.
# Run on Jonathan's Mac (Desktop is not mounted in the cloud VM).
#
# Usage (from this directory, after checkout of cursor/ns-five-lane-lemma-star-1390):
#   chmod +x SYNC_TO_DESKTOP.sh && ./SYNC_TO_DESKTOP.sh
#
# Or one-liner from repo root:
#   bash jonathan-handoff/GROK-HEAVY/01-swirl-publishing/lemma-star-sot/SYNC_TO_DESKTOP.sh

set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${HARMONIC_BOOK_DIR:-$HOME/Desktop/Harmonic Universe Book}"

FILES=(
  LEMMA_STAR_SHAPE_FORM.md
  LEMMA_STAR_EXACT_FORMULAS.md
  LEMMA_STAR_CANONICAL.md
)

# Optional Desktop naming variants for exact-formulas (backup+overwrite if present)
VARIANTS=(
  LEMMA_STAR_EXACT_FORMULAS.md
  "LEMMA_STAR_EXACT FORMULAS.md"
  LEMMA_STAR_EXACT.md
)

if [[ ! -d "$DEST" ]]; then
  echo "ERROR: Desktop book folder not found: $DEST" >&2
  echo "Create it, or set HARMONIC_BOOK_DIR=/path/to/folder and re-run." >&2
  exit 1
fi

for f in "${FILES[@]}"; do
  if [[ ! -f "$SRC/$f" ]]; then
    echo "ERROR: missing source file: $SRC/$f" >&2
    exit 1
  fi
done

TS="$(date +%Y%m%d-%H%M%S)"
echo "Source: $SRC"
echo "Dest:   $DEST"
echo "Backup suffix: .bak.$TS"
echo

for f in "${FILES[@]}"; do
  if [[ -f "$DEST/$f" ]]; then
    cp "$DEST/$f" "$DEST/$f.bak.$TS"
    echo "backed up  $f -> $f.bak.$TS"
  else
    echo "no prior   $f (will create)"
  fi
  cp "$SRC/$f" "$DEST/$f"
  echo "synced     $f"
done

# If Desktop has an alternate exact-formulas filename, refresh it from EXACT_FORMULAS
for alt in "${VARIANTS[@]}"; do
  if [[ "$alt" == "LEMMA_STAR_EXACT_FORMULAS.md" ]]; then
    continue
  fi
  if [[ -f "$DEST/$alt" ]]; then
    cp "$DEST/$alt" "$DEST/$alt.bak.$TS"
    cp "$SRC/LEMMA_STAR_EXACT_FORMULAS.md" "$DEST/$alt"
    echo "synced alt $alt (from LEMMA_STAR_EXACT_FORMULAS.md)"
  fi
done

echo
echo "Done. Verify:"
echo "  ls -la \"$DEST\"/LEMMA_STAR_*.md"
echo "  shasum -a 256 \"$DEST\"/LEMMA_STAR_{SHAPE_FORM,EXACT_FORMULAS,CANONICAL}.md"
