#!/usr/bin/env bash
# Send the footer animal's orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/footer-crane/paint.sh [name ...]
# Each order is prompts/<name>.txt; the picture lands in originals/<name>.png, Codex's log in
# plates/logs/ (git-ignored). Every order gets the footer's crane today (its hand and layout) and
# the park sign it stands by. stdin must be /dev/null, or codex exec waits on it forever.
# Mo (November 3, 2026, part 5 of the homepage's California pass): the red-crowned crane by the
# park sign reads as Chinese, like the opening's crane and the old close's cranes did.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
mkdir -p "$LOGS" "$HERE/originals"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=(quail-2 tortoise-2 bear-1)
for name in "${names[@]}"; do
  ref=(-i "$HERE/originals/crane-sign-c1.png" -i "$HERE/../fda-sign/originals/sign-park-full-c5.png")
  # Mo (November 3): the quail and the bear cub "a little more painting like". Fresh paintings:
  # the picked take gives only the animal and layout; the hand is a painting Mo already picked,
  # the homepage's hummingbird in a few wet washes (*-wash-*) or the Big Sur close in ink and
  # wash (*-ink-*).
  [[ "$name" == quail-wash-* || "$name" == quail-ink-* ]] && ref=(-i "$HERE/originals/quail-2.png")
  [[ "$name" == bear-wash-* || "$name" == bear-ink-* ]] && ref=(-i "$HERE/originals/bear-1.png")
  # The first looser takes copied the layout picture's outlines and speckle: from the second, the
  # hand alone, the animal and its pose told in words.
  [[ "$name" == *-wash-[2-9] || "$name" == *-ink-[2-9] ]] && ref=()
  [[ "$name" == *-wash-* ]] && ref+=(-i "$HERE/../home-california/originals/allens-few-1.png")
  [[ "$name" == *-ink-* ]] && ref+=(-i "$HERE/../home-purpose/originals/ink-long-1.png")
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in prompts/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
