#!/usr/bin/env bash
# Send the NuriCell opening's sunlight orders (November 11, 2026: Mo asked for "some kind of
# reflection of the sun" in the upper right corner, "California sunshine") to Codex (Mo's ChatGPT
# plan, no API spend), all at once. Each order carries the opening's own painting
# (originals/opening-clearday2-ch.png) so the blue and the hand match the sky it is laid over.
#   bash reference/ink-pages/nuricell/paint_sun.sh <name> [name ...]
# <name> is <order>-<take>: the order is prompts/<order>-1.txt (opening-suncorner, opening-sundisc),
# the take any letter or number. The picture lands in originals/<name>.png, Codex's log in
# plates/logs/ (git-ignored). stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
SKY="$HERE/originals/opening-clearday2-ch.png"
mkdir -p "$LOGS" "$HERE/originals" "$HERE/plates/orders"
for name in "$@"; do
  base="${name%-*}"
  order="$HERE/plates/orders/$name.txt"
  cp "$HERE/prompts/$base-1.txt" "$order"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$SKY" -- \
    "Read the picture order in plates/orders/$name.txt and follow it exactly. The attached image is the painting it refers to. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep opening-sun
