#!/usr/bin/env bash
# Turmerific's grey ink chapter paintings in colour (Mo, November 17, 2026: the other product pages
# the same way as Advanced OPC, page by page: the same pictures in color). Codex repaints each
# October painting with its composition kept; the page's own spoon and plant are the colour
# reference.
#   bash reference/ink-pages/turmerific/paint_colour.sh <key>-<take> [...]
#   key: lit (the Why root with its gold, from plates/colour/why-soak-lit.png)
#        notebook (the research notebook, from plates/colour/research-glasses.png)
#        glass (the daily glass of water, its heavy ink softened, from plates/colour/daily-glass.png)
#        unlit (an EDIT of originals/$LIT.png: the gold taken off, so the two Why layers stay in
#               register; set LIT, e.g. LIT=lit-colour-a)
# The October takes are padded with their own paper to 1024 x 1536 (plates/colour/, git-ignored).
# Out: originals/<key>-colour-<take>.png. stdin must be /dev/null, or codex exec waits on it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
SPOON="$HERE/originals/gpt25-inside-scoop.png"
PLANT="$HERE/originals/gpt25-buy-plant.png"
mkdir -p "$LOGS" "$HERE/originals"
for name in "$@"; do
  key="${name%-*}"
  take="${name##*-}"
  out="$key-colour-$take"
  case "$key" in
    lit) refs=(-i "$HERE/plates/colour/why-soak-lit.png" -i "$SPOON" -i "$PLANT") ;;
    notebook) refs=(-i "$HERE/plates/colour/research-glasses.png" -i "$SPOON" -i "$PLANT") ;;
    unlit) refs=(-i "$HERE/originals/${LIT:?set LIT to the lit take to edit}.png") ;;
    glass) refs=(-i "$HERE/plates/colour/daily-glass.png" -i "$SPOON" -i "$PLANT") ;;
    *) echo "unknown key $key" >&2; continue ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$out.txt" "${refs[@]}" -- \
    "Read the picture order in prompts/$key-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (portrait 1024x1536), using the first attached picture as the image to repaint or edit. Copy the generated PNG into originals/ as $out.png. Reply with its full path." \
    < /dev/null > "$LOGS/$out.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep colour- | tail -n 20
