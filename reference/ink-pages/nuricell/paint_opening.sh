#!/usr/bin/env bash
# Send the NuriCell opening's picture orders (round 6, November 10, 2026) to Codex (Mo's ChatGPT
# plan, no API spend), all at once.
#   bash reference/ink-pages/nuricell/paint_opening.sh <name> [name ...]
# <name> is <order>-<take>: the order is prompts/<order>-1.txt (opening-clearday, opening-bluestroke,
# opening-shade, opening-shade-palm), the take any letter or number. A take ending in "h" also gets
# the homepage's Big Sur close (ink and wash, Mo's pick 1B) as the painter's hand.
# The picture lands in originals/<name>.png, Codex's log in plates/logs/ (git-ignored). stdin must
# be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
HAND="$HERE/../home-purpose/originals/ink-long-1.png"
mkdir -p "$LOGS" "$HERE/originals" "$HERE/plates/orders"
for name in "$@"; do
  base="${name%-*}"
  order="$HERE/plates/orders/$name.txt"
  cp "$HERE/prompts/$base-1.txt" "$order"
  ref=()
  case "$name" in
    *h)
      ref=(-i "$HAND")
      printf '\nThe attached painting shows only the way of painting (the same painter): take its brushwork, not its subject, its bridge, its people or its cliffs.\n' >> "$order"
      ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in plates/orders/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep opening- | tail -n 20
