#!/usr/bin/env bash
# Round 2 of the Dr. Liu mockups (Mo, November 11, 2026: for mockups his picture may be redrawn; he
# will have Dr. Liu check and approve before anything like it goes live). Sends picture orders with
# Dr. Liu IN them to Codex (Mo's ChatGPT plan, no API spend), all at once:
#   bash reference/ink-pages/mockups/science-liu/paint_liu.sh <name> [name ...]
# An order is the Science style (prompts/_style-ca.txt) + prompts/<base>-<take>.txt, or
# prompts/<base>-1.txt when that take has no order of its own. Three pictures go with it: his
# photograph, his shipped painted portrait, and the homepage's Big Sur close as the hand.
# The picture lands in reference/ink-pages/science/originals/<name>.png, Codex's log in
# plates/logs/ (git-ignored). stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCIENCE="$(cd "$HERE/../../science" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
LOGS="$SCIENCE/plates/logs"
HAND="$SCIENCE/../home-purpose/originals/ink-long-1.png"
PHOTO="$REPO/public/images/jiankang-liu.jpg"
PAINTED="$SCIENCE/plates/liu/liu-v1.png"
mkdir -p "$LOGS" "$SCIENCE/originals" "$SCIENCE/plates/orders" "$SCIENCE/plates/liu"
# Codex takes PNG and JPEG: the shipped portrait is a webp. Python on Windows needs Windows paths
# (Git Bash's /c/... opened nothing, and two orders came back "the second reference is missing").
[ -f "$PAINTED" ] || (cd "$REPO" && python -X utf8 -c "from PIL import Image; Image.open('public/images/products/nuricell/ink/liu-v1.webp').convert('RGB').save('reference/ink-pages/science/plates/liu/liu-v1.png')")
[ -f "$PAINTED" ] || { echo "no painted portrait at $PAINTED"; exit 1; }
for name in "$@"; do
  order="$SCIENCE/plates/orders/$name.txt"
  base="${name%-*}"
  shape="${SHAPE:-landscape 1536x1024}"
  cat "$SCIENCE/prompts/_style-ca.txt" > "$order"
  printf '\n' >> "$order"
  cat "$SCIENCE/prompts/$base-${name##*-}.txt" >> "$order" 2>/dev/null || cat "$SCIENCE/prompts/$base-1.txt" >> "$order"
  codex exec --skip-git-repo-check -C "$SCIENCE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$PHOTO" -i "$PAINTED" -i "$HAND" -- \
    "Read the picture order in plates/orders/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture ($shape), giving it the three attached pictures as references. Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$SCIENCE/originals" | grep -E "liu-(scope|planes)" || true
