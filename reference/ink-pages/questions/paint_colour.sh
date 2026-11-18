#!/usr/bin/env bash
# Advanced OPC Formula's six question paintings in colour (Mo picked A, November 17, 2026: the same
# pictures in color, and the capsule one repainted as two closed capsules on a leaf, no powder).
#   bash reference/ink-pages/questions/paint_colour.sh <key>-<take> [...]
#   key: what take month studied doctor (repaints) capsule (a new picture)
# The first attached picture is the October painting padded with its own paper to 1536 x 1024
# (plates/colour/opc-<key>.png, git-ignored; the capsule takes the lunch's framing); then the OPC
# page's new grapes and plants for how its paintings are coloured now.
# Out: originals/opc-<key>-colour-<take>.png. stdin must be /dev/null, or codex exec waits on it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
OPC="$HERE/../opc/originals"
mkdir -p "$LOGS" "$HERE/originals"
for name in "$@"; do
  key="${name%-*}"
  take="${name##*-}"
  out="opc-$key-colour-$take"
  src="$HERE/plates/colour/opc-$key.png"
  [ -f "$src" ] || src="$HERE/plates/colour/opc-take.png"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$out.txt" -i "$src" -i "$OPC/why-seedsbig-ah.png" -i "$OPC/inside-nine-ah.png" -- \
    "Read the picture order in prompts/opc-$key-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $out.png. Reply with its full path." \
    < /dev/null > "$LOGS/$out.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep colour- | tail -n 20
