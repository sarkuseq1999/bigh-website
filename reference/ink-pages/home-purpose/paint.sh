#!/usr/bin/env bash
# Send the closing painting's orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/home-purpose/paint.sh [name ...]
# Each order is prompts/<name>.txt; the picture lands in originals/<name>.png, Codex's log in
# plates/logs/ (git-ignored). Every order gets the homepage's opening painting as the hand; the
# pelicans get the loose hummingbird too. stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
CA="$HERE/../home-california/originals"
mkdir -p "$LOGS" "$HERE/originals"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=(coast-walk-1 oak-walk-1 palm-walk-2)
for name in "${names[@]}"; do
  ref=(-i "$CA/sequoia-2-clear-1.png")
  [[ "$name" == pelicans-* ]] && ref+=(-i "$CA/allens-few-body-1.png")
  # Mo (November 2): the walk on the ridge "doesn't give the vibe of California": the same walk
  # on the Big Sur coast, among oaks and poppies, and under palms by the Pacific.
  [[ "$name" == coast-walk-* ]] && ref+=(-i "$HERE/originals/big-sur-1.png" -i "$HERE/originals/ridge-2.png")
  [[ "$name" == oak-walk-* || "$name" == palm-walk-* ]] && ref+=(-i "$HERE/originals/ridge-2.png")
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in prompts/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
