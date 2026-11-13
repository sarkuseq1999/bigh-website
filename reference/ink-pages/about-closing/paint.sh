#!/usr/bin/env bash
# Send the About "Curious about the science?" round's picture orders to Codex (ChatGPT plan, no API
# spend), all at once (November 13, 2026). Mo asked for About's last three parts to take the site's
# California colour, one part at a time; this is the third, the grey ink glasses on a notebook.
#   bash reference/ink-pages/about-closing/paint.sh prompt@take [prompt@take ...]
# Each order is prompts/<prompt>.txt plus prompts/_style.txt; the picture lands in
# originals/<prompt>-<take>.png, Codex's log in plates/logs/ (git-ignored). Every order gets the
# About page's own valley at dawn, poppy meadow and sunny oak as the reference for the hand and the
# palette; glasses-colour also gets the page's glasses (first) as the picture to repaint.
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
GLASSES="$HERE/../about-bc/plates/glasses-v1.png"
VALLEY="$HERE/../about-made/originals/valley-1-b.png"
MEADOW="$HERE/../about-opening/originals/superbloom-a1.png"
OAK="$HERE/../about-purpose/originals/oak-1-b.png"
SIZE="1536x1024"
mkdir -p "$LOGS" "$HERE/originals"
for order in "$@"; do
  prompt="${order%@*}"
  take="${order#*@}"
  name="$prompt-$take"
  if [ "$prompt" = "glasses-colour" ]; then
    refs=(-i "$GLASSES" -i "$VALLEY" -i "$MEADOW")
    task="Read the picture order in prompts/$prompt.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture ($SIZE, landscape), using the first attached picture as the image to repaint."
  else
    refs=(-i "$VALLEY" -i "$MEADOW" -i "$OAK")
    task="Read the picture order in prompts/$prompt.txt and the style in prompts/_style.txt, and follow both exactly. Use your built-in image generation tool to make exactly ONE picture ($SIZE, landscape)."
  fi
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${refs[@]}" -- \
    "$task Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
