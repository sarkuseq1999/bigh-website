#!/usr/bin/env bash
# Send the phone menu's closing painting orders to Codex (ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/menu-finale/paint.sh [name ...]
# Each order is prompts/<name>.txt (a take -N reuses the order of take -1); the picture lands in
# originals/<name>.png, Codex's log in plates/logs/ (git-ignored). Every order gets the footer's
# quail (Mo picked A1 on November 3, 2026) as the hand, or REF=<picture> instead (the hummingbird
# orders get the opening's Allen's). stdin must be /dev/null, or codex exec waits on it forever.
# Mo (November 3, 2026, part 6 of the homepage's California pass): the crane at rest at the foot of
# the phone menu, the footer's finale in miniature, is the last crane on the site.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="$HERE/plates/logs"
mkdir -p "$LOGS" "$HERE/originals"
REF="${REF:-$HERE/../footer-crane/originals/quail-wash-2.png}"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=(menu-quail-1 menu-quail-2 menu-poppy-1 menu-poppy-2)
for name in "${names[@]}"; do
  order="prompts/${name%-*}-1.txt"
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" -i "$REF" -- \
    "Read the picture order in $order and follow it exactly. Use your built-in image generation tool to make exactly ONE picture, in the format the order asks for. Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals"
