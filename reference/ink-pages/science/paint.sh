#!/usr/bin/env bash
# Send the Science page's picture orders to Codex (Mo's ChatGPT plan, no API spend), all at once.
#   bash reference/ink-pages/science/paint.sh <name> [name ...]
# A new painting's order is prompts/_style-ca.txt + prompts/<base>.txt (<name> minus its "-<n>"
# take number) and gets the homepage's Big Sur close (ink and wash, Mo's pick 1B) as the hand.
# Special names:
#   town-lit-<n>        an edit of originals/town-dusk-<n>.png: every window lit (prompts/town-lit.txt)
#   lit-<src>, lit2-<src>  the same edit of originals/<src>.png (two takes)
#   town-loose-<n>      town-dusk-1 painted again, far looser (prompts/town-loose-1.txt)
#   loose-<src>-<n>     originals/<src>.png painted again, far looser (prompts/loose.txt)
#   wash-<place>-<n>    an edit of the shipped place painting: light washes (prompts/place-wash-1.txt)
# The picture lands in originals/<name>.png, Codex's log in plates/logs/ (git-ignored). stdin must
# be /dev/null, or codex exec waits on it forever.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
LOGS="$HERE/plates/logs"
HAND="$HERE/../home-purpose/originals/ink-long-1.png"
mkdir -p "$LOGS" "$HERE/originals" "$HERE/plates/orders"
for name in "$@"; do
  order="$HERE/plates/orders/$name.txt"
  ref=()
  shape="landscape 1536x1024"
  case "$name" in
    town-loose-*)
      ref=(-i "$HERE/originals/town-dusk-1.png" -i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf "
" >> "$order"; cat "$HERE/prompts/town-loose-1.txt" >> "$order"
      ;;
    loose-*)
      src="${name#loose-}"; src="${src%-*}"
      ref=(-i "$HERE/originals/$src.png" -i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf '
' >> "$order"; cat "$HERE/prompts/loose.txt" >> "$order"
      ;;
    lit-*|lit2-*)
      src="${name#lit-}"; src="${src#lit2-}"
      ref=(-i "$HERE/originals/$src.png")
      cp "$HERE/prompts/town-lit.txt" "$order"
      ;;
    town-lit-*)
      n="${name#town-lit-}"
      ref=(-i "$HERE/originals/town-dusk-${n%%[a-z]*}.png")
      cp "$HERE/prompts/town-lit.txt" "$order"
      ;;
    gild-*)
      # gild-<src>: originals/<src>.png with its lightable parts in gold (prompts/gild-<key>.txt,
      # <key> = the first word of <src> after any "loose-": monarchs, sunflowers, cheek).
      src="${name#gild-}"; key="${src#loose-}"; key="${key%%-*}"
      ref=(-i "$HERE/originals/$src.png")
      cp "$HERE/prompts/gild-$key.txt" "$order"
      ;;
    wash-*)
      place="${name#wash-}"; place="${place%-*}"
      src="$HERE/plates/place-$place.png"
      ref=(-i "$src" -i "$HAND")
      cp "$HERE/prompts/place-wash-1.txt" "$order"
      ;;
    *)
      base="${name%-*}"
      ref=(-i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"
      printf '\n' >> "$order"
      cat "$HERE/prompts/$base-${name##*-}.txt" >> "$order" 2>/dev/null || cat "$HERE/prompts/$base-1.txt" >> "$order"
      ;;
  esac
  codex exec --skip-git-repo-check -C "$HERE" -s workspace-write -c model_reasoning_effort="low" \
    -o "$LOGS/$name.txt" "${ref[@]}" -- \
    "Read the picture order in plates/orders/$name.txt and follow it exactly. Use your built-in image generation tool to make exactly ONE picture ($shape). Copy the generated PNG into originals/ as $name.png. Reply with its full path." \
    < /dev/null > "$LOGS/$name.out" 2>&1 &
  sleep 2
done
wait
ls -la "$HERE/originals" | tail -n 20
