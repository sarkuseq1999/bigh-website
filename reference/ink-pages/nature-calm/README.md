# Nature Calm in Ink & Gold

October 16, 2026. Branch `nature-calm-ink` (worktree `codes/bigh-nature-calm-ink`), from `origin/main`
934d313. NuriCell's ink template (`docs/superpowers/specs/2026-10-09-nuricell-ink-design.md`) with
Nature Calm's own paintings in every chapter and its own signature moment in "Why it matters".

## Mo's picks (October 16: "All A")

| Chapter        | Painting                                                                                        | Take(s)                                  |
| -------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Opening        | The real bottle between "Nature" and "Calm" (the name set to fit; phones stack it)              | (no painting)                            |
| Why it matters | **Still water.** A lake ruffled by wind, its gold reflection scattered; as you arrive the water stills and the light gathers into one line (the lantern's cross-fade, this painting's own meaning) | `why-water-still` (lit), `why-water-ripple` (unlit, its edit) |
| What's inside  | A sugar pine cone: many scales, one calm natural form; three beads of gold resin                 | `inside-cone`                            |
| The research   | The Big Dipper: seven gold stars over one dark ridge (seven studies, the stars you steer by)     | `research-stars-v2` (v1's stars too small) |
| The people     | Dr. Liu: NuriCell's painting of him, reused (Mo's A; nothing new generated)                     | (NuriCell's `liu-v1`)                    |
| How to take it | A glass of water, three capsules, the moon's phases above, the full moon in gold (one bottle, one month); no painted sum (3 × 30 = 90 is NuriCell's) | `daily-moon`                             |
| Buy            | The real bottle standing between lavender rows (a California farm), stalks in front of its foot | `buy-lavender`                           |

Round 1 also painted, not chosen: `why-storm-clear` + `why-storm-dark` (an oak, the storm passes),
`inside-cairn`, `research-lighthouse`, `daily-plate`, `buy-beach`, `buy-oak`, `research-stars` (v1).
Their originals (54 MB) are kept out of the public repo in
`codes/bigh-archive/nature-calm-ink-unused-originals-2026-10-16/`; `originals/` holds the six takes the page
uses. Capsules are painted pale (their real colour unconfirmed).

## Lake Tahoe (November 16, 2026, for launch)

The grey misty lake read as an East Asian ink landscape, out of step with the site's California
turn. Codex repainted it at Lake Tahoe with a little colour, keeping its meaning (wind-ruffled
water and scattered gold that still into one gold line): warm granite boulders in clear shallows,
a band of conifers, the snowy Sierra. Round 1 (`paint_tahoe.sh`, `prompts/why-tahoe-still.txt`,
takes a-c) came out as smooth postcard watercolour; round 2 (`PROMPT=loose`,
`prompts/why-tahoe-loose.txt`) asked for ink lines and uneven washes with paper between them, and
take **loose-e** is the still lake. Its ruffled twin is an edit of it (`paint_tahoe_ripple.sh`,
`prompts/why-tahoe-ripple.txt`, take **ripple-a**). Built as `tahoe-still-v1` / `tahoe-ruffled-v1`
(colour washes, so no deepening). Unused takes: `codes/bigh-archive/nature-calm-tahoe-unused-2026-11-16/`.

## The opening: the high meadow (Mo picked A, November 16, 2026)

The last product on the shared opening to leave bare paper, after Advanced OPC Formula's vineyard
and Turmerific's field. Three calm California places were painted by Codex (`paint_opening.sh`,
`prompts/opening-{meadow,bay,aspens}-1.txt`; takes `a` and `b`, each with the homepage's Big Sur
close as the painter's hand) and mocked on the live page by script
(`../mockups/nature-calm-opening/`; review page https://claude.ai/artifact/PoveGP1zttXYJyDZdyYZxb):
A Tuolumne Meadows in Yosemite's high country on a calm evening, B Tomales Bay still as a mirror at
dawn (it repeated the Lake Tahoe chapter's still water), C Eastern Sierra aspens in autumn. Mo
picked **A** (take `opening-meadow-bh`, the stream's two curves), Claude's pick.

Built with the shared painted opening (`build_nature_calm_opening.py` → `opening-meadow-*-v1.webp`,
`src/components/product/ink/nature-calm-opening-art.ts`; `painted-opening.tsx`): the pine tops
under the name at row 640, the ground at row 795 (inside the grass), "Calm"'s baseline at 62.2% of
the bottle's box, the name lifted 0.1 of its size. Checks: `qa_nature_calm_ink` section `meadow`.
The other five takes are in `codes/bigh-archive/nature-calm-opening-unused-2026-11-16/`.

## The stars without their glow (November 16, 2026)

Seen at full size, each gold star of the Big Dipper sat in a pale lemon-yellow halo, a fuzzy glow
that the site's rules refuse (gold leaf behaves like real gold, no glow; no fuzzy glows, which read
as germs). The halo is in the take itself (`research-stars-v2`). The build now takes it back to
paper (`dehalo` in `build_nature_calm.py`: a pixel is lifted toward white as far as it is light
and lemon yellow; the leaf is a deep orange-brown and keeps its colour) and ships `stars-v2`. The
halo had also passed the gold detector, so the kit's band of light crossed it: the gold mask fell
from 1.6% to 0.47% of the picture, the leaf alone. `stars-v1` stays in `public/`, unused.

## Rules learned on the way

- A **pale wash dies on the page**: the still lake's water is only 7% darker than its paper, and
  once divided out and multiplied onto the page it vanished (the "after" read as a gold line hanging
  from a hill). The build deepens the wash on both Why layers equally and keeps the whole sheet; the
  standard paper lift (220/245) is replaced by a gentle one (200/252) for wash paintings.
- The kit's **gold detector takes browns and ochres for gold** (the pine cone's scales, an ochre
  hill): the leaf on these takes sits at hue 38-60, so a stricter detector cuts the masks.
- The dev server caches optimized pictures by URL (`.next/dev/cache/images`): a rebuilt file under
  the same name is served stale until that folder is cleared (or the name versioned).
- With the bottle at NuriCell's size (90% of the scene's width) the glass itself is 47% of it: a
  scene must keep its subject at the sides, the foot and above the cap. The lavender rows do.

## Files

- `hf_nature_calm.py`: GPT Image 2.5 jobs (ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-nature-calm-ink`,
  cap 42 jobs; Mo's $3). Prompts in `prompts/` (`_style.txt` + `_<name>.txt` → `<name>.txt`; edits
  carry no style preamble and take the painting they edit as their reference).
- `build_nature_calm.py`: originals → `public/images/products/nature-calm/ink/` and
  `src/components/product/ink/nature-calm-art.ts`.
- `translations-nature-calm.cjs`: draft translations m780-m784 (not native-reviewed).
- QA: `scripts/qa/qa_nature_calm_ink.py`.

## The paintings in colour (Mo, November 17, 2026)

The same way as Advanced OPC and Turmerific: the same pictures in color. Nature Calm's grey ink
chapter paintings were the Big Dipper (research) and the moon (daily); the lake, the cone and the
lavender were already colour. `paint_colour.sh` pads each October take with its own paper to
1024 x 1536 (`plates/colour/`, git-ignored) and has Codex repaint it with the page's lavender field
and sugar pine cone as the colour reference (`prompts/{stars,moon}-colour.txt`). The stars: the
ridge a dusk blue-grey with a faint lavender band over it, the stars plain gold leaf (dehalo still
runs). The moon: its thin crescents, which read as brackets, now clear filled crescents. Both are
lifted to white gently (`gentle` 200/248, so their pale washes stay). Shipped as
`stars-colour-v1`, `moon-colour-v1`; the opening card's capsules still come from the October moon.
Descriptions m781-m783 now say watercolor. The `b` takes are in
`codes/bigh-archive/nature-calm-colour-unused-2026-11-17/`. The questions:
`../questions/README.md`. Before and after: `../mockups/nature-calm-colour/`.

## The Big Dipper at dusk (November 18, 2026)

On bare paper the colour take's seven gold dabs read as scattered coins, not stars. Codex edited
it (`paint_colour.sh dusk-a`, prompt `prompts/dusk-colour.txt`): the same stars and ridge, the sky
painted at dusk, deep twilight blue at the top through violet to a warm apricot glow over the
ridge, its edges dissolving into the paper. `build_nature_calm.py` ships it as `stars-dusk-v1`
(`STARS_TAKE = "dusk-colour-a"`): no dehalo (the stars sit on the dark sky with nothing round
them, and it would lift the glow), the gold deepened and masked only above `STARS_GOLD_ROWS`
(the glow passes the gold test in a few pixels). The other take is in
`bigh-archive\nature-calm-dusk-unused-2026-11-18\`.

