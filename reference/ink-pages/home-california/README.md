# Homepage opening: California ideas (October 28, 2026)

Mo's colleagues (meeting of October 27) love the homepage opening, its watercolour and its gold
sun, but say it feels Chinese, "made in China". What reads Chinese, biggest first: the tall misty
peaks with pines (classic Chinese landscape painting), the red-crowned crane (an Asian bird, a
Chinese sign of long life), the black-ink accents. Mo said yes to painting three California
scenes on the real page:

- **A. Big Sur sunset** (Claude's pick, 8.5/10): the sun sets over the Pacific, a gold path on the
  water, Highway 1 and its arch bridge along the cliffs. Painted with more detail than the rest of
  the site; sandhill cranes live inland, not on the coast.
- **B. Golden hills** (8.5/10): low summer hills, a valley oak, a ranch fence. Both About test
  openings (`/about-a`, `/about-b`) are golden hills too, so the pages would look alike.
- **C. Yosemite** (7.5/10): El Capitan, Half Dome under the sun, a waterfall, valley mist. Misty
  cliffs and pines are the closest to today's look; on a wide screen the sun floats in empty sky.

All three keep the gold sun, the words and the layout, and swap the crane for a **sandhill
crane** (grey, a small red cap; it winters in California's Central Valley), painted over the live
crane's original in the same pose so the brush line would still leave from its legs.

Nothing in `src/` changed. If one is picked, the homepage's closing painting (the same peaks and
two cranes) and the footer's crane by the park sign would change to match, the brush line would
be routed again for the new scene, and the "California, not Asian" rule in AGENTS.md and DESIGN.md
(which still calls the page "an East Asian ink-wash painting") would need updating.

## D. Giant sequoias in the morning (October 28, 2026)

Mo liked the outlook but asked how a scene relates to "Good health starts with your cells." The
honest answer: no scene says "cells" by itself; the gold does (the sun and "cells." are the same
gold, and on this site gold means energy). The old crane carried "long life", but only in Chinese
tradition, and A's Pacific sun can only be a setting one ("the end of the day" for a brand about
aging). Of three ways on, Mo picked 2: a California sign of long life in a morning sun, giant
sequoias (they live more than 3,000 years).

- **D** (9/10, `sequoia-2`): a grove of giant sequoias, cinnamon trunks rising out of the
  picture, ferns and a fallen log, morning light slanting in; the sun in the open haze beside
  them. Painted with more detail than the rest of the site; sandhill cranes winter in the valley
  below, not in the groves.
- Painted as the whole first screen, not the landscape band, so the trunks can rise out of it:
  `sequoia-1`, `-2` (live opening attached), `-3` (words only; a blue wash at its top). Codex put
  a far trunk at 71-76% across, where the sun was asked to go, so the mockup moves the sun left
  (53% of the column at 1440, at most 833 px in) and fades the trunks' tops into the light, clear
  of the menu's words. On a phone the whole painting shows at the picture's height, its right
  two-thirds in the window, the sun moved left and a little smaller, the crane a little lower.

## D, round 2: the sun fixed, three birds (October 28, 2026)

Mo liked D overall but found the sun "strange or cramped" (the mockup had squeezed it left,
between the crane and two far trunks) and asked whether the crane still suits; he likes the
stroke that goes down. Claude's view: the crane flying past a gold sun is the last Asian echo
left, even in grey. Mo said "paint both" of the two birds offered.

- The sun: Codex edited sequoia-2 into `sequoia-2-clear-1`, `-2`: the two far trunks gone, an
  open clearing of morning light, one giant trunk left on the right. The sun is back in its own
  place at 1440 (held at most 1000 px in from the column's start on wider windows so it stays in
  the clearing); on a phone it sits in the clearing's middle at its own size. Shown: clear-1.
- **1. Anna's hummingbird** (Claude's pick, 8.5/10, `hummingbird-1`): ties to the headline (it
  burns energy faster for its size than almost any animal; its flight muscles are packed with
  mitochondria). Its wings came out too big and feathery for a hummingbird; a build would repaint
  them narrow and blurred. Its pink throat is a second colour beside the gold.
- **2. Golden eagle** (8/10, `golden-eagle-1`): the most American; reads as strength and power,
  a little like a bank's logo; the heaviest painting on the screen.
- **3. Sandhill crane** (7.5/10 against the brief): calmest and least work, still the Asian echo.
- Each bird was painted by Codex over the live crane's original, in its place, so the page's
  stroke (shown again in these mockups, as routed today) leaves from the bird's tail.

## Mo's pick: the hummingbird (October 28, 2026)

Mo picked 1, the hummingbird (recorded in AGENTS.md). Its wings were repainted true: Codex
edited `hummingbird-1` to change only the wings, `hummingbird-wings-1` and `-2` (long, narrow,
pointed, a blur of speed); `hummingbird-3` was painted again over the crane's original (better,
still a little feathery). Shown: `hummingbird-wings-1` (h1), 9/10 for the first screen. Still to
do in a build: route the stroke along the forest floor (it still crosses the clearing and the big
trunk as drawn for the mountains); the pink throat stays a second colour beside the gold.

## Built: first screen only (October 28, 2026)

Mo: "First screen only": the crane stays in the homepage's closing painting, the footer by the
park sign and the phone menu. `build_home_opening.py` makes `opening-sequoias-v1.webp` (from
`sequoia-2-clear-1`, the whole first screen) and `hummingbird-v1.webp` (from
`hummingbird-wings-1`, in the crane's 1600 x 1062 frame). In the page: the painting covers the
opening (its top dissolves to bare paper under the menu bar, so the bar's words and rule keep a
quiet ground), the sun keeps its place but at most 1000 px into the column (in the clearing on
wide windows), the hummingbird is a still (no wingbeat picture), and the line's second stroke is
pinned to the painting's own box (`opening-land`) so it walks the forest floor left of the giant
trunk at every width. Phones: the whole painting at the picture's height, the sun at 43%, the
bird a little lower, a short dive to the clearing's floor. Built-site checks: `qa_home_ink`
280/280 (its wingbeat checks replaced by: the sequoias and the hummingbird, the sun's room in the
clearing, no ink on the trunk; the designed lift now lands on `opening-land`), `qa_nav` 326/326.

## Files

- Paintings: Codex (ChatGPT plan, no API spend), 8 pictures, two takes each:
  `originals/big-sur-1`, `-2`, `golden-hills-1`, `-2`, `yosemite-1`, `-2`, `sandhill-crane-1`,
  `-2`. Take 1 had the live opening attached as a guide to the hand and colours; take 2 words
  only. Shown: the take 1s (softer, closer to the site) and `sandhill-crane-1`.
- `write_prompts.py` writes `prompts/<name>.txt` (scene + `prompts/_style.txt`) and the attached
  reference pictures into `plates/refs/`; `paint.sh` sends the orders to Codex all at once.
- `cut_california.py` makes the mockup layers in `plates/img/` (git-ignored): a scene becomes the
  live landscape's 2400 x 1029 layer, paper divided out, framed (`FRAME`) so the live sun sits in
  open sky (A: over its path of light; C: over Half Dome, clear of El Capitan), its top and left
  edges dissolved; a crane take is lined up on the live crane (ECC) and cut out.
- `shoot_california.py` swaps them into the public demo's homepage by script and CSS and shoots
  1920 x 1040, 1440 x 900 and 390 x 844 into `plates/shots/`. The mist canvas and the brush line
  are hidden (the line is routed for the live mountains); A's sun is lowered to the sea's horizon
  (and moved over its path on phones).
- Page for Mo: `../mockups/home-california/home-california.html`
  (Artifact https://claude.ai/artifact/XcSw57ecBtwFxZzn7SmqdY).

## Part 2: the bird's look, its wings never still (October 29, 2026)

Mo asked for other hummingbird choices and wings that are "always moving", like a dragonfly's.
Codex edited the live bird's painting (`hummingbird-wings-1`) three ways, all in the same pose and
place so the line still leaves from under the tail: `hummingbird-body-1` (the same bird, its wings
removed), `hummingbird-female-1` (a female Anna's, green and grey) and `allens-1` (Allen's
hummingbird, copper), then removed the wings of the two new looks (`hummingbird-female-body-1`,
`allens-body-1`). A lone painted wing (`hummingbird-one-wing-1`) was tried as the rig's wing and
dropped (it floated off the shoulder); it is in `bigh-archive/home-california/`.

`build_wings.py` lifts each look's painted wings out (the painting minus its wingless edit, the
edit lined up by ECC) and beats them about the shoulder as a wing looks from the side: each
shortens toward the shoulder as it swings toward you and comes out below the body, then back.
Six frames a beat, each blurred over its slice of the beat; the page plays them at 60 a second,
ten beats a second (a real Anna's beats about forty, which a screen cannot show without the wings
appearing to crawl). Out, in `plates/wings/<look>/`: the wingless body, the near wing's and far
wing's six frames side by side, and `rig.json` (the wings' box in the bird's frame).

`make_bird_mockup.py` lays each look into shots of the live first screen with the bird hidden
(laptop 1440 x 900 and a 390 phone, both 2x), its wings beating in the browser as they would on
the site: `../mockups/home-bird/home-bird.html` (Artifact
https://claude.ai/artifact/QUXRzND98STrXfrwPd5iCQ). A. today's Anna's 8/10 (its pink throat a
second bright colour), B. the green female 7/10 (too quiet: pale, it almost vanishes as its
wings come down), C. Allen's 8.5/10, Claude's pick (copper like the redwood bark beside it; it
nests almost only on the California coast). Nothing in `src/` changed.

### Round 2: Allen's, more like a painting (October 29, 2026)

Mo: "Allen's is pretty good. But can we try to make them look more painting-like, a little bit
more painting-like, instead of more realistic?" Edits of `allens-1` in the old crane's hand
(`allens-wash-*`, `allens-sketch-*`) kept its fine speckle, so Codex painted it afresh from words,
with `allens-1` for the pose and colours and the old flying crane
(`reference/home-v2/ink/originals/gpt25-crane-paint-a.png`) for the hand: `allens-loose-2` (a
little looser) and `allens-few-1` (a few wet washes; much more a painting), and removed their
wings (`allens-loose-body-2`, `allens-few-body-1`). The other takes are in `bigh-archive`.
`build_wings.py` lines each fresh painting up on `allens-1` (bill tip and tail tip), gives
`allens-few` its own shoulders and wing split, and calms its orange (saturation 0.72, brightness
0.94), which came out louder than the gold sun. The page (same Artifact, version 2) now shows
A. Allen's as before 8/10, B. a little looser 8/10, C. painted in a few strokes 9/10, Claude's
pick.

Then Mo: "the beak was too realistic" (a crisp, glossy black pin on a loose painting). Codex
repainted only the bill of `allens-few-body-1` as one dry brush stroke of soft grey-black
(`allens-few-bill-2`; take 1, darker and broken, is in `bigh-archive`), and `build_wings.py`
swaps in just that bill, inside a soft band along it; the wings are still lifted against the
original wingless edit. Page version 3.

### Built: C on the homepage (October 29, 2026)

Mo: "Yes, build C". `build_home_opening.py` now runs `build_wings.build("allens-few")` and writes
`hummingbird-v2.webp` (the wingless body, 1600 x 1062, the crane's frame) and
`hummingbird-v2-near.webp`, `-far.webp` (each wing's six frames side by side). The page
(`opening-crane.tsx`, `opening.module.css`) blooms the bird in whole (`.flock`), the far wing
laid before the body and the near one after it, in the wings' box (`openingWings` in
`assets.ts`); the frames step at ten beats a second while the opening is in the window
(`data-beat`, an IntersectionObserver), rest on the first frame off screen and with reduced
motion. `qa_home_ink` checks both wings, several frames within one beat, the pause once the
opening is out of view, and nothing moving with reduced motion.

## Part 3: the wings stay up (November 11, 2026)

Mo sent a frame of the beat with the near wing below the belly: "normally I just see the upper
wings move, not the wing ... around the belly part". He was right. The rig shortened each wing
through the shoulder and out below the body. A hovering hummingbird beats its wings forward and
back in a nearly level figure 8 at shoulder height (Tobalske et al. 2007, "Three-dimensional
kinematics of hummingbird flight", rufous hummingbird, Allen's closest kin: stroke plane about 15
degrees from level in hovering, body about 50 degrees up), and side-view photos of hovering birds
show the wing reaching back level with the shoulder at the end of the stroke.

`build_wings.py` now fans each wing about its shoulder, above the body: from its painted pose
(raised, the top of the beat) to `sweep` degrees at the bottom (near wing 40 back toward the tail,
level with the shoulder; far wing 24 forward, clear of the head), shortened to 0.9 and narrowed
mid-stroke. Never through the shoulder. The blur takes 48 samples a frame (24 left visible steps in the
wider sweep). The first frame, the rest pose, is unchanged. The wings are renamed
`hummingbird-v3-near.webp`, `-far.webp` (the body keeps `hummingbird-v2.webp`); their box in the
bird's frame is now 11.638 / 14.174 / 54.031 / 55.621 (it ends 70% down the frame, the old one
91%), and `qa_home_ink` checks that it ends above the belly. `build_menu_finale.py` reads the v3
wings (the menu's baked bird was not rebuilt: its rest pose is the same). Review page with
before/after films shot on the built homepage: `../mockups/home-bird-wings/` (Artifact
https://claude.ai/artifact/73RrLuccvfzBXFnusPv5vw).

## Part 4: too fast to see (November 12, 2026)

Mo: "the wing needs to move a lot faster ... so fast you can barely see his wings. Right now he's
so slow, it's like a butterfly." The page stepped six poses a beat at ten beats a second, then
slowed to about six and four: every flap could be followed. A hummingbird beats about forty to
fifty times a second; a 60 Hz screen cannot show that, and the eye (or a camera at a normal
shutter) sees a pale fan where the wing sweeps, darkest where the wing turns at each end.

`build_wings.py` now writes 11 frames a wing: 0 the rest pose (unchanged); 1-8 the haze, each the
wing averaged over 0.7 of a beat (96 samples) centred at a different point of the stroke
(`HAZE_PHASES`, an order the eye can't follow); 9-10 the haze folding onto the raised wing
(`SETTLE`, spans 0.45 and 0.24 centred on the top). Frames are 0.55 of the painting's pixels (was
0.7), about 450 px, the wings' largest size on the page on a 2x screen; lossy alpha banded the haze
into contour lines, so the webp keeps lossless alpha (near 252 KB, far 136 KB). Files
`hummingbird-v4-near.webp`, `-far.webp`, box 11.834 / 14.174 / 53.641 / 55.425.

The page (`opening.module.css`): `haze 0.1333s steps(8) 22` (one frame a screen frame, 2.93 s),
then `fold 0.14s steps(2)`, then frame 0. The keyframes are `fold`, not `settle`: that name is
the words' own entrance keyframes later in the same file, and the later one won (the first build
showed no fold). On the built page the near wing changed about 58 times a second for 2.9 s, then
90%, 100%, then rest at 3.06 s (laptop and phone). Review page with films:
`../mockups/home-bird-wings/fast/` (Artifact https://claude.ai/artifact/3doPJvZQtKNgusd7BCa9QZ).
