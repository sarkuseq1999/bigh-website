#!/usr/bin/env bash
# Send the "Good questions" picture orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/home-ask/paint.sh [name ...]
# Each order is prompts/<name>.txt; the picture lands in originals/<name>.png, Codex's log in
# plates/logs/ (git-ignored). Every order gets the old flying crane as the reference for the hand,
# and from round 2 the homepage's loose Allen's hummingbird too.
# stdin must be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
HAND="$HERE/../../home-v2/ink/originals/gpt25-crane-paint-a.png"
LOOSE="$HERE/../home-california/originals/allens-few-body-1.png"
mkdir -p "$LOGS" "$HERE/originals"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=(mailbox-4 gold-pan-3 field-book-3)
for name in "${names[@]}"; do
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$HAND" -i "$LOOSE" -- \
    "Read the picture order in prompts/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture (landscape 1536x1024). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
