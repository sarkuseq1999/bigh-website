#!/usr/bin/env bash
# Send the About plants round's picture orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/about-plants/paint.sh prompt@take [prompt@take ...]
# Each order is prompts/<prompt>.txt; the picture lands in originals/<prompt>-<take>.png, Codex's
# log in plates/logs/ (git-ignored). Every order gets the About page's own oak and sequoia and the
# homepage's loose Allen's hummingbird as the reference for the hand; the map also gets the real
# land as a grey silhouette (ref/land-guide.png, from render_land.py over Natural Earth 1:50m).
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
OAK="$HERE/../about-bc/originals/codex-oak-v1.png"
SEQUOIA="$HERE/../about-bc/originals/gpt25-sequoia-v1.png"
LOOSE="$HERE/../home-california/originals/allens-few-body-1.png"
mkdir -p "$LOGS" "$HERE/originals"
for order in "$@"; do
  prompt="${order%@*}"
  take="${order#*@}"
  name="$prompt-$take"
  size="1536x1024"
  extra=()
  case "$prompt" in
    specimens*) size="1024x1024" ;;
    map*) extra=(-i "$HERE/ref/land-guide.png") ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$OAK" -i "$SEQUOIA" -i "$LOOSE" "${extra[@]}" -- \
    "Read the picture order in prompts/$prompt.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture ($size). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
