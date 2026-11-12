#!/usr/bin/env bash
# Mo kept the sequoia (November 11, 2026: "I think the sequoia tree is a good idea. Maybe just make
# it a little bit colored."). Codex repaints the page's own sequoia with a little colour.
#   bash reference/ink-pages/about-experience/paint_colour.sh take [take ...]
# The first attached picture is the page's sequoia (plates/sequoia-v1.png, the site's
# public/images/about-bc/sequoia-v1.webp as PNG); then the valley at dawn and the poppy meadow for
# how the page's newer paintings are coloured. Out: originals/sequoia-colour-<take>.png.
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
SEQUOIA="$HERE/plates/sequoia-v1.png"
VALLEY="$HERE/../about-made/originals/valley-1-b.png"
MEADOW="$HERE/../about-opening/originals/superbloom-a1.png"
mkdir -p "$LOGS" "$HERE/originals"
for take in "$@"; do
  name="sequoia-colour-$take"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$SEQUOIA" -i "$VALLEY" -i "$MEADOW" -- \
    "Read the picture order in prompts/sequoia-colour.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (1024x1024), using the first attached picture as the image to repaint. Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
