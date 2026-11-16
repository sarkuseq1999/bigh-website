#!/usr/bin/env bash
# Nature Calm's "Why it matters" lake set at Lake Tahoe with a little colour (November 16, 2026, for
# launch: the grey misty lake read as an East Asian ink landscape). Codex repaints the page's still
# lake; the ruffled take is then an edit of the chosen still take (paint_tahoe_ripple.sh).
#   bash reference/ink-pages/nature-calm/paint_tahoe.sh a b
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
PROMPT="${PROMPT:-still}"
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
STILL="$HERE/plates/why-water-still-ref.png"
VALLEY="$HERE/../about-made/originals/valley-1-b.png"
SEQUOIA="$HERE/../home-purpose/originals/ink-long-1.png"
mkdir -p "$LOGS" "$HERE/originals"
for take in "$@"; do
  name="why-tahoe-$PROMPT-$take"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$STILL" -i "$VALLEY" -i "$SEQUOIA" -- \
    "Read the picture order in prompts/why-tahoe-$PROMPT.txt and follow it exactly. The second and third attached pictures show only how lightly the site's newer paintings are coloured; copy nothing else from them. Use your built-in image generation tool to make exactly ONE picture in portrait format (1024x1536), using the first attached picture as the image to repaint. Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep tahoe
