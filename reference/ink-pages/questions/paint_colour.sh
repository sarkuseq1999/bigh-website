#!/usr/bin/env bash
# Question paintings in colour (Mo picked A for Advanced OPC, November 17, 2026: the same pictures in
# color, the capsule one repainted as two closed capsules on a leaf, no powder; then the other
# products the same way, page by page).
#   bash reference/ink-pages/questions/paint_colour.sh <product> <key>-<take> [...]
#   product: opc (refs: OPC's grapes and plants) or turmerific (refs: its spoon and plant)
#   key: a question key; OPC's capsule is a new picture (prompts/opc-capsule-colour.txt)
# The first attached picture is the October painting padded with its own paper to 1536 x 1024
# (plates/colour/<product>-<key>.png, git-ignored; a new picture takes the lunch's framing).
# Out: originals/<product>-<key>-colour-<take>.png. stdin must be /dev/null, or codex exec waits.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
product="$1"
shift
case "$product" in
  opc) REF1="$HERE/../opc/originals/why-seedsbig-ah.png"; REF2="$HERE/../opc/originals/inside-nine-ah.png" ;;
  turmerific) REF1="$HERE/../turmerific/originals/gpt25-inside-scoop.png"; REF2="$HERE/../turmerific/originals/gpt25-buy-plant.png" ;;
  *) echo "unknown product $product" >&2; exit 1 ;;
esac
mkdir -p "$LOGS" "$HERE/originals"
for name in "$@"; do
  key="${name%-*}"
  take="${name##*-}"
  out="$product-$key-colour-$take"
  src="$HERE/plates/colour/$product-$key.png"
  [ -f "$src" ] || src="$HERE/plates/colour/$product-take.png"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$out.txt" -i "$src" -i "$REF1" -i "$REF2" -- \
    "Read the picture order in prompts/$product-$key-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $out.png. Reply with its full path." \
    < /dev/null > "$LOGS/$out.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep colour- | tail -n 20
