# The Science page's paintings (October 13-14, 2026)

GPT Image 2.5 ("Marketing Studio Image 2.5 Flare" on the Higgsfield API), 21:9, 2k, quality high,
with the homepage's resting crane as the brushwork reference. Mo gave $3 on October 13; 15 jobs
used (about $0.75, at most $1.05 before refunds). Ledger:
`%LOCALAPPDATA%/HiggsfieldAPI/bigh-science-mock/ledger-science-mock.jsonl`.

| Picture          | Original                              | Note                                                                                                                                     |
| ---------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| The handscroll   | `S-panel-1`, `S-panel-2`, `S-panel-3` | Three panels to one horizon, joined in their mist by `build_science.py`; style reference `A-scroll` (the mockup's single-picture scroll) |
| The research     | `R-scrolls`                           | A shelf of rolled scrolls; three lie pulled forward (the three key studies)                                                              |
| Health explained | `S-health-poppy`                      | An edit of `R-health`: California poppies instead of the plum branch (Mo, October 14)                                                    |
| Ask BiGH Science | `S-mugs`                              | An edit of `R-tea`: two mugs instead of the tea set (Mo, October 14)                                                                     |

Build: `python -X utf8 reference/ink-pages/science/build_science.py`, then
`python -X utf8 reference/ink-pages/science/check_science_art.py`.

## One place per screen (October 26, 2026)

Mo found the handscroll's sideways travel read as a draft and picked B: his path going down the
page, one place per screen. No new paintings and no spend: `places()` in `build_science.py` cuts
four places from the joined band (`PLACES`, band pixels, by eye, then checked on the page), each
with a tighter phone cut: `place-okayama`, `place-berkeley`, `place-salzburg`, `place-today`
(`-phone`), v1. The sea and the hills of 2002 are left out. The band itself no longer ships
(`scroll-v2`, `scroll-phone-v2` deleted); it is kept as `plates/band.png` for the contact sheet,
which marks each cut (red wide, blue phone). Mockups and the review page's shots:
`reference/ink-pages/mockups/science-path/2026-10-26/`.

## Round 3: "Our science starts in the cell" (November 4, 2026)

Mo: start broader (what science BiGH focuses on, and why), keep the water paint, turn from an
Asian feel to California; then "do the best you can ... I will come and critique". Spec:
`docs/superpowers/specs/2026-11-04-science-california-design.md`. Every picture is a Codex
painting on Mo's ChatGPT plan (no API spend), sent by `paint.sh` with the homepage close
(`home-purpose/originals/ink-long-1.png`, Mo's pick 1B) as the hand; the style block is
`prompts/_style-ca.txt`. The first takes read as tidy illustrations, so each was painted again far
more loosely (`prompts/loose.txt`, `prompts/town-loose-1.txt`); the loose takes ship.

| Picture                   | Ships                                                | Painted from          | Note                                                                                                                    |
| ------------------------- | ---------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Opening                   | `loose-desk-window-2-1`                              | `desk-window-2`       | A desk at an open window over golden hills: brass microscope, notebook, glasses, poppies                                |
| Why start with the cell?  | `town-loose-1`, lit `lit-town-loose-1`               | `town-dusk-1`         | San Francisco's houses at dusk; the lit take is an edit of the loose one (`prompts/town-lit.txt`)                       |
| Berkeley, Salzburg, Today | `wash-berkeley-1`, `wash-salzburg-1`, `wash-today-1` | the handscroll's cuts | Light washes over the October paintings (`prompts/place-wash-1.txt`); Today keeps the handscroll's own gold sun (`SUN`) |
| The research              | `loose-journals-1-1`                                 | `journals-1`          | Bound journals along a library table, three laid open (the three studies to start with)                                 |
| Ask BiGH Science          | `loose-picnic-1-1`                                   | `picnic-1`            | Two enamel camp mugs on a redwood picnic table                                                                          |

The takes that were not used (`desk-window-1`, `town-dusk-2`, `town-lit-1`, `town-lit-1b`,
`town-loose-2`, `lit2-town-loose-1`) are in
`C:\Users\mcbig\Documents\codes\bigh-archive\science-round3-unused-2026-11-04\`, outside the
public repo.

The town's lamps: `build_science.py` registers the lit take onto the unlit one, finds the panes
where the lit take is warm and the unlit one bare paper (209 panes), lays them in the homepage
sun's own gold leaf (`sun.webp`, random tiles of its solid middle) and splits them into six
shuffled groups, each an RGBA layer the town's size (`town-lamps-<n>-v3.webp`), feathered at the
outer edge as the town is. The page lights the groups one after another (`why.module.css`); phones
fade in one lit cut (`town-phone-lit-v3`). The lit town itself is a lossless plate only
(`plates/town-lit-v3.png`): `check_science_art.py` lays the six layers over the town's plate and
compares. Okayama's castle, the scrolls, the health scenes and the mugs no longer ship (their
pictures are deleted from `public/`; their originals stay here as `gpt25-*`).

## Other pictures for "Why start with the cell?" (November 6, 2026)

Mo kept the opening line and asked for other picture ideas to compare with the town. Each was
painted (`monarchs-1`, `sunflowers-1`, `cheek-cells-1`), painted again loosely (`loose-*-1-1`), then
gilded by an edit (`paint.sh gild-*`, `prompts/gild-<key>.txt`: only the parts that light turn
golden). `reference/ink-pages/mockups/science-why/build_why_mocks.py` turns each pair into the
town's own layers (gold leaf in six groups; one butterfly, flower or cell lights at once), and
`shoot_why_mocks.py` films them in the real page in place of the town. The sunflowers' gilded edit
moved the flowers, so there the gilded take is the drawing and its petals are washed pale for the
resting picture. Compare page for Mo: `mockups/science-why/page/`.

Mo picked A: the town stays. The nine takes (`monarchs-1`, `sunflowers-1`, `cheek-cells-1`, their
`loose-*-1-1` and `gild-loose-*-1-1`) moved to
`C:\Users\mcbig\Documents\codes\bigh-archive\science-why-unused-2026-11-06\`, outside the public
repo; copy them back into `originals/` to rerun `build_why_mocks.py`. Their prompts stay here.

## The zoom opening (November 9, 2026)

Mo found the first screen plain and the town unrelated to "cell", and picked a slow zoom (AGENTS.md
"Science opening: one slow zoom"). Codex paintings on Mo's ChatGPT plan, no API spend, sent by
`paint.sh` with the Big Sur close as the hand:

| Picture   | Original       | Note                                                                                           |
| --------- | -------------- | ---------------------------------------------------------------------------------------------- |
| The walk  | `zoom-hills-1` | A walker on a trail in golden hills, open sky at the upper left for the h1                     |
| The hand  | `zoom-hand-2`  | The walker's hand in the dry grass, loose; take 1 drew every knuckle and nail                  |
| One cell  | `zoom-cell-2`  | A wet wash, a dark blue nucleus, slender gold slivers; takes 1 and 3 were diagrams with beans  |
| (dropped) | `zoom-tissue-1`| A patch of cells like flagstones: read as peanuts in dishes                                    |

`zoom()` in `build_science.py` ships the walk and the hand whole (3:2, 1536px: they fill the window,
so no feathered edge) and the cell cropped to its ink. The desk and the town (with its lamp
layers) no longer ship; their originals stay. `shoot_zoom.py <base-url>` takes the page at eight
scroll depths on six window sizes, and with reduced motion. New lines have draft translations
m1120-m1122 (`translations-science-zoom.cjs`, not native-reviewed). The sample Mo saw:
`reference/ink-pages/mockups/science-zoom/` (`build_zoom_mock.py`, artifact
`UwMjAd5Zpbm8yzXowNLYSq`). The unused takes (`zoom-cell-1`, `zoom-cell-3`, `zoom-hand-1`,
`zoom-tissue-1`) are in `bigh-archive\science-zoom-unused-2026-11-09\`; their prompts stay in `prompts/`.

## First-screen ideas (November 10, 2026): Mo picked A, start inside the cell

A day after the zoom went live Mo asked for more or better ideas for the first screen, then to see
them. Four ideas were mocked on the real page without touching `src/`:
`mockups/science-hero/` (`ideas.py` is injected into the dev server's page by `shoot_hero.py`,
`split_gold.py` lifts a painting's gold slivers so they can drift, `gild_dabs.py` gilds idea B's
dabs, `make_loops.py` makes the films; review page `review/`, artifact `5rauLXYKSbXSi9VhTg9aem`).
Codex paintings on Mo's ChatGPT plan, no API spend. Claude's scores: A 8, C 8, D 8, B 7.

| Idea                         | Original        | Note                                                                                  |
| ---------------------------- | --------------- | ------------------------------------------------------------------------------------- |
| A. Start inside the cell     | `zoom-inside-1` | Mo's pick (it was `hero-inside-1`): the view from inside one cell; the zoom pulls back |
| (A, not used)                | `hero-inside-2` | The nucleus read as a boulder in mist                                                  |
| (A, not used)                | `hero-inside-3` | Paler, "clear water"; read as a sky with clouds                                        |
| B. Made of cells             | `hero-dabs-1`   | The walker in dabs, some gilded by `gild_dabs.py`; can read as pebbles                 |
| (B, not used)                | `hero-dabs-2`   | The same facing us: a patterned suit                                                   |
| (B, rejected)                | `hero-walker-1` | Gold slivers laid on a clothed walker: scratches across the face, chest and legs       |
| (B, rejected)                | `hero-walker-2` | A see-through body with gold inside: a ghost                                           |
| C. The gold dot              | (none)          | Words very large, the full stop in gold leaf, the page's own cell below                |
| D. Today's scene, walker big | `hero-near-2`   | The walker about three times larger; `hero-near-1` was too tall (hat under the menu)   |

Mo picked A ("Go with A"). Built on the branch `science-inside` (AGENTS.md "Science opening: it
starts inside the cell"): `zoom()` in `build_science.py` now ships four views in the page's order.
`lifted()` takes the gold slivers off `zoom-inside-1` (the painting is filled in behind them, in
two rounds, and a sliver is what differs from that and is warm), `pieces()` packs them into one
picture (`zoom-inside-gold-v3.webp`) and fixes each one's drift, so `zoom.tsx` can lay each sliver
where it was painted and let it drift on its own. The whole cell (`zoom-cell-2`) is now a view on
the way out, between the inside view and the hand. One new string, the first picture's
description: draft translation m1223 (`translations-science-inside.cjs`, not native-reviewed).
`check_science_art.py` and `qa_science_ink.py` follow the new order. The eight unused `hero-*`
originals (`hero-inside-2`, `-3`, `hero-walker-1`, `-2`, `hero-dabs-1`, `-2`, `hero-near-1`,
`-2`) are in `bigh-archive\science-hero-unused-2026-11-10\`; their prompts stay in `prompts/`,
and `gild_dabs.py` and the mock scripts need them copied back to run again.

## The last view: hand in hand (November 10, 2026)

Mo saw A built and found the picture the zoom pulls back to (one small walker on empty hills)
plain. Four last pictures were set in the built page's last view without touching `src/`
(`mockups/science-hero/shoot_last.py`, pictures `review/last-*.jpg`); he picked 1 (AGENTS.md
"Science opening, the last view: hand in hand"). `film_built.py` films the built page scrolling
for the review page; its two films are not kept in the repo (about 4 MB each; they are on the
artifact), only their first and last frames.

| Choice                   | Original           | Note                                                                    |
| ------------------------ | ------------------ | ----------------------------------------------------------------------- |
| 1. Hand in hand          | `zoom-pair-1`      | Mo's pick (it was `out-pair-2`): a grandfather and a grandchild         |
| 2. The orange grove      | `out-grove-2`      | The most colour; the tree crowded the menu bar on desktop               |
| 3. The surfer            | `out-surf-1`       | Says California fastest; fewer customers surf than walk                 |
| 4. The same walker, big  | `out-near-1`       | The walker three times bigger (it was `hero-near-2`): still one hiker   |
| (left out)               | `out-painter-1/-2` | A painter at her easel: busy under the words                            |

Built on it, each a Codex painting made from `zoom-pair-1` so the people match (`paint.sh`
attaches the pair first, the Big Sur hand second; `prompts/zoom-hands-1.txt`,
`zoom-pair-phone-1.txt`, `zoom-hands-phone-1.txt`):

| Picture                    | Original             | Note                                                          |
| -------------------------- | -------------------- | ------------------------------------------------------------- |
| The joined hands           | `zoom-hands-3`       | The loosest of three; no nails, creases or veins              |
| The pair, tall             | `zoom-pair-phone-2`  | For upright windows (1024 x 1536); the trail winds to the oak |
| The joined hands, tall     | `zoom-hands-phone-1` | Painted from `zoom-hands-3`; a wide cut showed only knuckles  |

`zoom()` ships them as `zoom-hands-v3`, `zoom-hands-phone-v3`, `zoom-pair-v3` and
`zoom-pair-phone-v3` (new names: the walker's and his hand's were live and are cached by name;
`zoom-hills-v3` and `zoom-hand-v3` are deleted, their originals stay). The page's layers keep
their names (`hand`, `hills`). `zoom.tsx` picks the tall paintings with
`<source media="(orientation: portrait)">` and starts the walk where the hands just seen stood
(`slide`) and about as large (`NEAR`). One more new string, the last picture's description: draft
translation m1224. The unused takes (`out-pair-1`, `out-grove-1/-2`, `out-surf-1/-2`,
`out-painter-1/-2`, `out-near-1`, `zoom-hands-1/-2`, `zoom-pair-phone-1/-3`,
`zoom-hands-phone-2/-3`) are in `bigh-archive\science-hero-unused-2026-11-10\`; their prompts
stay in `prompts/`.
