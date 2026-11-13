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
#   zoom-hands-<n>      the zoom's pair (originals/zoom-pair-1.png) seen close: the joined hands
#   zoom-pair-phone-<n> the zoom's pair painted again as a tall picture for phones (1024x1536)
#   zoom-hands-phone-<n> the joined hands (originals/zoom-hands-3.png) again as a tall picture
#   last-<idea>-<n>     a new last view with the same pair (originals/zoom-pair-1.png attached
#                       first): prompts/_last-pair.txt + prompts/last-<idea>-<n>.txt (or -1)
#   end-<idea>-<n>      a new last view of any kind: prompts/_end.txt + prompts/end-<idea>-<n>.txt
#   climb-hand-<n>      the climber's hand on the rock (originals/end-climb-3.png attached first):
#                       prompts/climb-hand-<n>.txt (or -1); its tall twin is tall-climb-hand-<n>-<m>
#   tall-<src>-<n>      originals/<src>.png painted again as a tall picture for phones (1024x1536):
#                       prompts/tall-<idea>-1.txt, <idea> = <src> without "loose-" and its takes
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
    zoom-hands-*|zoom-pair-phone-*)
      # A view of the pair painting: its people and colours (first attachment), the hand second.
      # The tall hands are painted from the wide hands instead.
      base="${name%-*}"
      first="$HERE/originals/zoom-pair-1.png"
      case "$name" in
        zoom-hands-phone-*) shape="portrait 1024x1536"; first="$HERE/originals/zoom-hands-3.png" ;;
        zoom-pair-phone-*) shape="portrait 1024x1536" ;;
      esac
      ref=(-i "$first" -i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf '\n' >> "$order"; cat "$HERE/prompts/$base-1.txt" >> "$order"
      ;;
    climb-hand-*)
      # Mo picked the climber (November 12, 2026): the zoom's hand view is her hand on the rock.
      # The climber painting first (her colours, the granite), the Big Sur hand second.
      base="${name%-*}"
      ref=(-i "$HERE/originals/end-climb-3.png" -i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf '\n' >> "$order"
      cat "$HERE/prompts/$base-${name##*-}.txt" >> "$order" 2>/dev/null || cat "$HERE/prompts/$base-1.txt" >> "$order"
      ;;
    end-*)
      # Mo, November 12, 2026 ("think freely"): a new last view of any kind. The style, the
      # last view's brief (prompts/_end.txt), then prompts/end-<idea>-<n>.txt (or -1).
      base="${name%-*}"
      ref=(-i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf '\n' >> "$order"
      cat "$HERE/prompts/_end.txt" >> "$order"; printf '\n' >> "$order"
      cat "$HERE/prompts/$base-${name##*-}.txt" >> "$order" 2>/dev/null || cat "$HERE/prompts/$base-1.txt" >> "$order"
      ;;
    tall-*)
      src="${name#tall-}"; src="${src%-*}"
      idea="${src#loose-}"; idea="${idea%%-[0-9]*}"
      shape="portrait 1024x1536"
      ref=(-i "$HERE/originals/$src.png" -i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf '\n' >> "$order"
      cat "$HERE/prompts/tall-$idea-1.txt" >> "$order"
      ;;
    last-*)
      # Mo, November 12, 2026: the last view's pair, in a scene where something happens. The
      # pair painting first (its people), the Big Sur hand second.
      base="${name%-*}"
      ref=(-i "$HERE/originals/zoom-pair-1.png" -i "$HAND")
      cat "$HERE/prompts/_style-ca.txt" > "$order"; printf '\n' >> "$order"
      cat "$HERE/prompts/_last-pair.txt" >> "$order"; printf '\n' >> "$order"
      cat "$HERE/prompts/$base-${name##*-}.txt" >> "$order" 2>/dev/null || cat "$HERE/prompts/$base-1.txt" >> "$order"
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
