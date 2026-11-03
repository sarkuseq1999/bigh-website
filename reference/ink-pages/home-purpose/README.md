# Homepage closing painting, "Our purpose is simple." (October 30 - November 2, 2026)

Part 4 of the homepage's California follow-ups: the old pine on its rock, the misty peaks and the two
red-crowned cranes read as Chinese. Mockup only; nothing in `src/` has changed.

- Pictures by Codex (`paint.sh`, ChatGPT plan, no API spend), the opening's sequoia painting as the
  hand. Each scene was asked with its top 55% bare sky, the horizon level and the sun's spot clear.
- `shoot_purpose.py` cuts each one from its paper, sets the opening's own gold-leaf sun on its
  horizon (`sun.webp`, the closing sun's size, cut level where sea or land stands in front), lays
  the pelicans where the cranes fly, and swaps them into the live homepage's `<img>`. The band is
  2:1, not 7:3: at 7:3 the land rose into the words.
- Page for Mo: `make_purpose_mockup.py` (`../mockups/home-purpose/`): A Big Sur at evening 8.5,
  B an evening walk on the ridge 9 (my pick), C a surfer at low tide 8.

Mo tried A and B live (`/home-a`, `/home-b`, main `c32fefb`) and found the walk on the ridge "doesn't
give the vibe of California" (November 2). Round 2, the same walk made Californian (same page, v2):
1 on the Big Sur coast 9 (my pick; on a phone a wider frame, from 26% across, keeps the walkers and
the sun), 2 among a valley oak, poppies and lupine 8.5 (echoes About's poppy hills and oak), 3 under
palms by the Pacific 8.

Mo picked 1, the coast walk; it went live as `main` `4d5f59e`. Then he found it "a little bit simple"
next to the old pine painting. Round 3 (same page, v3), richer Big Sur paintings with the old one
as the reference for finish only (`_style_rich.txt`; each sun on its own glitter path, `sun_x`):
1 the long view down the coast with Bixby Bridge 9 (my pick), 2 today's view painted richer 8.5,
3 McWay Falls 9.

Mo tried 1 and 3 live (`/home-1`, `/home-3`, main `648e44d`) and found them "more picture like"
(November 2): they read as photos with a watercolour filter. Round 4 (same page, v4), the same two
places painted loosely: fresh Codex paintings with the round-3 painting as place and layout only.
A, a loose watercolour (the old flying crane as the hand; `wash-*`), B, ink and wash (the old pine
painting's ink as the hand; `ink-*`). 1A 8.5, 1B 9 (my pick), 3A 8.5 (the first take's hills came
out bright orange and fought the gold sun; `wash-falls-2` asks for calm colours), 3B 8.5. The page
shows a full-size close-up of each beside today's.
Codex could not decode the crane picture for the McWay Falls watercolours ("Unknown filter method"
in `plates/logs/`), so `wash-falls-2` follows the words and the round-3 painting only.

Unused takes: `bigh-archive/home-purpose/`.

When building: `purposePainting`, `purposeCranes` and `gold.purpose` in `assets.ts`; their tinted
twins in `ink-color.tsx`; `purpose.module.css` (the 2400/1029 ratio on the sun's light, the phone
frame's 0.195 margin and 81% sun line); `brush-route.ts` (`purpose-painting` stations);
`qa_home_ink.py` (`PURPOSE_FRAME`, the cranes); a new gold mask for the sun's light.
