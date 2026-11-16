#!/usr/bin/env bash
# The ruffled twin of the chosen Tahoe still take (Nature Calm "Why it matters"): an edit that
# changes only the water. The build registers it to the still take.
#   bash reference/ink-pages/nature-calm/paint_tahoe_ripple.sh <still-take-name> a b
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
STILL="$HERE/originals/$1.png"
shift
for take in "$@"; do
  name="why-tahoe-ripple-$take"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$STILL" -- \
    "Read the picture order in prompts/why-tahoe-ripple.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture in portrait format (1024x1536), editing the attached picture. Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | grep ripple
