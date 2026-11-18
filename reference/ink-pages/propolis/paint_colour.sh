#!/usr/bin/env bash
# Green Bee Propolis's grey ink chapter paintings in colour (Mo, November 17-18, 2026: the other
# product pages the same way as Advanced OPC, page by page: the same pictures in color). Codex
# repaints each October painting with its composition kept; the page's own dish of green propolis
# and its buy scene (alecrim and golden ipê blossoms) are the colour reference.
#   bash reference/ink-pages/propolis/paint_colour.sh <key>-<take> [...]
#   key: hive (the bee tree with its cracks in gold, from plates/colour/why-hive-gold.png; portrait)
#        hiveopen (an EDIT of originals/$HIVE.png: the cracks open again, so the two Why layers stay
#                  in register; set HIVE, e.g. HIVE=hive-colour-a; portrait)
#        specimen (the alecrim specimen sheet, from plates/colour/research-specimen.png; square)
#        mug (the mug of tea and its capsule, from plates/colour/daily-mug-v2.png; square)
# The October takes are padded with their own paper (plates/colour/, git-ignored).
# Out: originals/<key>-colour-<take>.png. stdin must be /dev/null, or codex exec waits on it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
RESIN="$HERE/originals/gpt25-inside-resin-dish.png"
SCENE="$HERE/originals/gpt25-buy-painted-empty.png"
mkdir -p "$LOGS" "$HERE/originals"
for name in "$@"; do
  key="${name%-*}"
  take="${name##*-}"
  out="$key-colour-$take"
  case "$key" in
    hive) refs=(-i "$HERE/plates/colour/why-hive-gold.png" -i "$RESIN" -i "$SCENE"); size="portrait 1024x1536" ;;
    hiveopen) refs=(-i "$HERE/originals/${HIVE:?set HIVE to the hive take to edit}.png"); size="portrait 1024x1536" ;;
    specimen) refs=(-i "$HERE/plates/colour/research-specimen.png" -i "$RESIN" -i "$SCENE"); size="square 1024x1024" ;;
    mug) refs=(-i "$HERE/plates/colour/daily-mug-v2.png" -i "$RESIN" -i "$SCENE"); size="square 1024x1024" ;;
    *) echo "unknown key $key" >&2; continue ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$out.txt" "${refs[@]}" -- \
    "Read the picture order in prompts/$key-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture ($size), using the first attached picture as the image to repaint or edit. Copy the generated PNG into originals/ as $out.png. Reply with its full path." \
    < /dev/null > "$LOGS/$out.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep colour- | tail -n 20
