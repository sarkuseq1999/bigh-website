#!/usr/bin/env bash
# Nature Calm's grey ink chapter paintings in colour (Mo, November 17, 2026: the other product
# pages the same way as Advanced OPC, page by page: the same pictures in color). Codex repaints
# each October painting with its composition kept; the page's own lavender field and sugar pine
# cone are the colour reference.
#   bash reference/ink-pages/nature-calm/paint_colour.sh <key>-<take> [...]
#   key: stars (the Big Dipper over its ridge, from plates/colour/research-stars-v2.png)
#        moon (the glass, three capsules and the moon's phases, from plates/colour/daily-moon.png;
#              its thin crescents painted as clear crescents, not brackets)
#        dusk (November 18: the colour stars take with its sky painted at dusk, the stars and the
#              ridge kept, from originals/stars-colour-a.png)
# The October takes are padded with their own paper to 1024 x 1536 (plates/colour/, git-ignored).
# Out: originals/<key>-colour-<take>.png. stdin must be /dev/null, or codex exec waits on it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
LAVENDER="$HERE/originals/gpt25-buy-lavender.png"
CONE="$HERE/originals/gpt25-inside-cone.png"
mkdir -p "$LOGS" "$HERE/originals"
for name in "$@"; do
  key="${name%-*}"
  take="${name##*-}"
  out="$key-colour-$take"
  case "$key" in
    stars) src="$HERE/plates/colour/research-stars-v2.png" ;;
    moon) src="$HERE/plates/colour/daily-moon.png" ;;
    dusk) src="$HERE/originals/stars-colour-a.png" ;;
    *) echo "unknown key $key" >&2; continue ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$out.txt" -i "$src" -i "$LAVENDER" -i "$CONE" -- \
    "Read the picture order in prompts/$key-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (portrait 1024x1536), using the first attached picture as the image to repaint. Copy the generated PNG into originals/ as $out.png. Reply with its full path." \
    < /dev/null > "$LOGS/$out.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep colour- | tail -n 20
