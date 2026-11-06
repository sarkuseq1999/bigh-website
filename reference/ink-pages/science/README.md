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
