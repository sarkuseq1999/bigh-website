#!/usr/bin/env bash
# Send Advanced OPC Formula's "Why antioxidants matter" picture orders (November 17, 2026: the
# grapes in California colour, without the glow) to Codex (Mo's ChatGPT plan, no API spend).
#   bash reference/ink-pages/opc/paint_why.sh <name> [name ...]
# <name> is <order>-<take>: the order is prompts/<order>-1.txt (why-ripe, why-seeds), the take any
# letter or number. A take ending in "h" also gets the homepage's mailbox (ink, thin watercolour
# and flat gold leaf, Mo's pick of October 30) as the painter's hand.
# The picture lands in originals/<name>.png, Codex's log in plates/logs/ (git-ignored). stdin must
# be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
HAND="$HERE/../home-ask/originals/mailbox-4.png"
mkdir -p "$LOGS" "$HERE/originals" "$HERE/plates/orders"
for name in "$@"; do
  base="${name%-*}"
  order="$HERE/plates/orders/$name.txt"
  cp "$HERE/prompts/$base-1.txt" "$order"
  ref=()
  case "$name" in
    *h)
      ref=(-i "$HAND")
      printf '\nThe attached painting shows only the way of painting (the same painter): take its brushwork, its thin washes and its flat gold leaf, not its subject, its mailbox, its poppies or its grass.\n' >> "$order"
      ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in plates/orders/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (portrait 1024x1536). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep why- | tail -n 20
