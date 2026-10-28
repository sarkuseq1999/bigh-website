#!/usr/bin/env bash
# Send the California opening picture orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/home-california/paint.sh [name ...]
# Each order is prompts/<name>.txt; the picture lands in originals/<name>.png, Codex's log in
# plates/logs/ (git-ignored). Take 1 of a scene gets the live opening attached, the crane gets
# the live crane (both made by write_prompts.py into plates/refs/). stdin must be /dev/null, or
# codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
REFS="$HERE/plates/refs"
mkdir -p "$LOGS" "$HERE/originals"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=(big-sur-1 big-sur-2 golden-hills-1 golden-hills-2 yosemite-1 yosemite-2 sandhill-crane-1 sandhill-crane-2)
for name in "${names[@]}"; do
  ref=()
  case "$name" in
    *-1 | sequoia-2) [[ "$name" == sandhill-* ]] || ref=(-i "$REFS/current-opening.png") ;;
  esac
  [[ "$name" == sandhill-* || "$name" == hummingbird-* || "$name" == golden-eagle-* ]] && ref=(-i "$REFS/current-crane.png")
  [[ "$name" == sequoia-2-clear-* ]] && ref=(-i "$HERE/originals/sequoia-2.png")
  [[ "$name" == hummingbird-wings-* ]] && ref=(-i "$HERE/originals/hummingbird-1.png")
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in prompts/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024 unless the order edits an attached picture). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
