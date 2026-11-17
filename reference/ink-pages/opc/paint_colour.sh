#!/usr/bin/env bash
# Mo picked "same pictures, in color" (November 17, 2026) for Advanced OPC Formula's other four
# grey ink paintings: the research lens, Dr. Wang's mortar, the plate and the vine scene by the
# bottle. Codex repaints each with California colour, the composition kept.
#   bash reference/ink-pages/opc/paint_colour.sh <key>-<take> [...]     key: lens mortar plate scene
# The first attached picture is the October painting padded with its own paper to 1024 x 1536
# (plates/colour/<take>.png, git-ignored; the October takes are 1744 x 2336); then the page's new
# grapes (why-seedsbig-ah) and plants (inside-nine-ah) for how its paintings are coloured now.
# Out: originals/<key>-colour-<take>.png. stdin must be /dev/null, or codex exec waits on it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
GRAPES="$HERE/originals/why-seedsbig-ah.png"
PLANTS="$HERE/originals/inside-nine-ah.png"
mkdir -p "$LOGS" "$HERE/originals"
declare -A SRC=([lens]=research-lens [mortar]=people-mortar [plate]=daily-plate [scene]=buy-vines-left)
for name in "$@"; do
  key="${name%-*}"
  take="${name##*-}"
  out="$key-colour-$take"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low"     -o "$LOGS/$out.txt" -i "$HERE/plates/colour/${SRC[$key]}.png" -i "$GRAPES" -i "$PLANTS" --     "Read the picture order in prompts/$key-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (portrait 1024x1536), using the first attached picture as the image to repaint. Copy the generated PNG into originals/ as $out.png. Reply with its full path."     < /dev/null > "$LOGS/$out.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep colour- | tail -n 20
