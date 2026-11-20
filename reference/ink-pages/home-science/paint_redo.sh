#!/usr/bin/env bash
# Send the November 20 science redesign picture orders to Codex (Mo's ChatGPT plan, no API spend).
#   bash reference/ink-pages/home-science/paint_redo.sh <name> [-- <reference.png> ...]
# The order is plates/orders/<name>.txt (written from prompts/<name>.txt). The mailbox is always
# attached as the brush hand; extra references after "--" are attached before it.
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
HAND="$HERE/../home-ask/originals/mailbox-4.png"
mkdir -p "$LOGS" "$HERE/originals" "$HERE/plates/orders"
names=(); refs=(); seen=0
for a in "$@"; do
  if [ "$a" = "--" ]; then seen=1; continue; fi
  if [ $seen = 1 ]; then refs+=(-i "$a"); else names+=("$a"); fi
done
for name in "${names[@]}"; do
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${refs[@]}" -i "$HAND" -- \
    "Read the picture order in plates/orders/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep redo
