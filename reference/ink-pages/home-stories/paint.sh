#!/usr/bin/env bash
# Send the homepage stories' still-life orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/home-stories/paint.sh [name ...]
# Each order is prompts/_style.txt plus prompts/<name>.txt; the picture lands in
# originals/<name>.png, Codex's log in plates/logs/ (git-ignored). Every order gets two paintings
# Mo already picked as the hand: the Big Sur close in ink and wash (its brush drawing) and the
# country mailbox (its few wet washes). stdin must be /dev/null, or codex exec waits on it forever.
# Mo (November 6, 2026, part 9 of the homepage's California pass): "In their own words." still
# lifes were painted as East Asian ink still lifes (plum blossom in a vase, tea bowls, a low
# table) and read as Asian.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
mkdir -p "$LOGS" "$HERE/originals"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=(kitchen-1 porch-1 counter-1)
for name in "${names[@]}"; do
  ref=(-i "$HERE/../home-purpose/originals/ink-long-1.png" -i "$HERE/../home-ask/originals/mailbox-4.png")
  # Round 2 (November 6, on the live page): the left of each painting runs off a laptop's window
  # and its empty top left a bare corner; each take's first draft leads, as the hand to keep.
  [[ "$name" == kitchen-[2-9] ]] && ref=(-i "$HERE/originals/kitchen-1.png" "${ref[@]}")
  [[ "$name" == porch-[2-9] ]] && ref=(-i "$HERE/originals/porch-1.png" "${ref[@]}")
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in prompts/_style.txt and then prompts/$name.txt, and follow both exactly. Use your built-in image generation tool to make exactly ONE picture (square 1024x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
