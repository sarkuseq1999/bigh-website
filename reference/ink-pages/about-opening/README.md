# About opening: new ideas (October 27, 2026)

Mo found the About page's big ink circle (live since October 27, title inside it) scary: "the
more I look at it, the more it reminds me of the movie The Ring". He asked for more concepts and
said yes to painting all three as mockups:

- **A. Superbloom:** golden hills in spring poppies fill the first screen, the title in the sky;
  the poppies would bloom as the page opens. 8/10: the yellow is brighter and wider than the
  site's one touch of gold, and the poppies are painted more carefully than the site's loose ink.
- **B. Morning walk** (Claude's pick): a trail over golden hills in the morning, one person and a
  dog walking away from us, the sunlit ridge the only gold. 8.5/10: the walker, with a backpack,
  reads as a young hiker rather than an older reader.
- **C. The name, painted:** no new picture; the title's capitals B, i, G, H brushed (the October 6
  letter paintings in `../about/originals/gpt25-letter-*-v1.png`), the hills kept. 7/10: close to
  the painted BiGH Mo turned down on October 7, and the brush letters beside the heavy type look
  like two fonts.

Nothing in `src/` changed; the live page still shows the circle.

- Paintings: Codex (ChatGPT plan, no API spend), two takes each, `originals/superbloom-a1`, `a2`,
  `walk-b1`, `b2`; prompts `prompts/superbloom-a.txt`, `prompts/walk-b.txt`. Shown: a1 and b1.
- `cut_mockups.py` turns the paper to transparency into `plates/img/` (git-ignored).
- `shoot_mockups.py` lays each idea over the public demo's About page by injected CSS and shoots
  1440 x 900, 1920 x 1000 and 390 x 844, each also scrolled 70% of a screen, into `plates/shots/`.
  On a phone B1 is framed at 33% across so the walker sits near the middle.
- Page for Mo: `../mockups/about-opening/about-opening.html`
  (Artifact https://claude.ai/artifact/6hnK43uNUsZ3R1tFSPvy6N).

## A and B on the real site (October 27, 2026)

Mo asked to compare A and B on the live site. Both are built as temporary test pages, `/about-a`
(superbloom) and `/about-b` (morning walk); `/about` keeps the circle until he picks
(`src/components/about/scene.module.css`, `scene-art.ts`, `SceneOpening` in `about-ink.tsx`).

- `build_about_opening.py` writes `public/images/about-opening/<name>-v1.webp` (the painting with
  its gold taken down to a pale grey ghost) and `<name>-gold-v1.webp` (the gold alone), paper made
  transparent, the foot feathered out. Gold is told by chroma (34 to 80 on the paper-divided
  picture).
- On the page the gold arrives once its picture is in: A's poppies bloom out from the foot of the
  hills (3.4 s), B's ridge catches the morning light from the right (2.4 s). Reduced motion: gold
  at once.
- On a phone B is framed on the walker (33% across), so its gold ridge is off screen there: no gold
  and no movement on phones.

## Where A's meadow ends (October 28, 2026)

Mo picked A, but found that its first screen and the next section (Our purpose, the oak) "don't
transition well". The painting stopped in a straight line with its biggest poppies on it (on a
1920 x 1000 screen the 14% feather is cropped away entirely), then blank paper and the small grey
oak. Two painted ends, the first screen unchanged in both:

- **A. The meadow thins out** (Claude's pick, 8.5/10): the poppies run on past the fold, fewer and
  smaller, then a few last ones and dry grass, then bare paper, then the oak. Costs about half a
  screen of scrolling (two-thirds at 1920 wide); a few grass strokes at the very end are scratchy.
- **B. Into the morning fog** (7.5/10): the meadow sinks into low valley fog. On a phone the fog
  reads as a grey smudge, and it is gloomy after the bright meadow.

- `join_foot.py canvas` makes the picture Codex edits (the painting's bottom half over bare
  paper); Codex (ChatGPT plan) continued it: `originals/superbloom-foot-thin2.png` (A),
  `superbloom-foot-fog1.png` (B), prompts `prompts/superbloom-foot-*.txt`. A third take,
  thin1, is in `bigh-archive/about-opening/`. Codex kept the top half pixel for pixel (shift 0).
- `join_foot.py join <take>` joins it under the painting (a 60-row cross-fade at the old foot):
  1536 x 1536, painted down to row 1391, and cuts the two layers into `plates/join/`.
- `shoot_join.py <take>` lays it over the public demo's /about-a (painting width
  max(100vw, 150svh), its sky cut 30% of the excess as now, Purpose pushed down by what is painted
  below the fold) and shoots it into `plates/join-shots/`.
- Page for Mo: `../mockups/about-opening-join/about-opening-join.html`
  (Artifact https://claude.ai/artifact/8fXZZqa9W5tFaPLY9cNnQo). Nothing in `src/` changed.

## Built (October 28, 2026)

Mo picked A, "the meadow thins out". The meadow replaced the circle on `/about`; the test pages
`/about-a` and `/about-b` and B's pictures are gone. `build_about_opening.py` now builds only the
meadow, `superbloom-v2.webp` and `superbloom-gold-v2.webp` (1536 x 1439: the joined painting cut
48 rows under its last stroke and eased out over them). On the page the painting is
max(100%, 150svh) wide, its sky cut 30% of the excess, and the opening ends where the painting
ends (`src/components/about/meadow.module.css`). `scripts/qa/qa_about.py` checks it
(`meadow_layout`, `motion`).
