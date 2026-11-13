#!/usr/bin/env bash
# Send the About "Our promise" round's picture orders to Codex (ChatGPT plan, no API spend), all at
# once (November 12, 2026).
#   bash reference/ink-pages/about-promise/paint.sh prompt@take [prompt@take ...]
# Each order is prompts/<prompt>.txt plus prompts/_style.txt; the picture lands in
# originals/<prompt>-<take>.png, Codex's log in plates/logs/ (git-ignored). Every order gets the
# About page's own valley at dawn, poppy meadow and sunny oak as the reference for the hand and the
# palette. The four grey ink dots this round replaces are deliberately NOT a reference.
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
VALLEY="$HERE/../about-made/originals/valley-1-b.png"
MEADOW="$HERE/../about-opening/originals/superbloom-a1.png"
OAK="$HERE/../about-purpose/originals/oak-1-b.png"
SIZE="1536x1024"
mkdir -p "$LOGS" "$HERE/originals"
for order in "$@"; do
  prompt="${order%@*}"
  take="${order#*@}"
  name="$prompt-$take"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$VALLEY" -i "$MEADOW" -i "$OAK" -- \
    "Read the picture order in prompts/$prompt.txt and the style in prompts/_style.txt, and follow both exactly. Use your built-in image generation tool to make exactly ONE picture ($SIZE, landscape). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
