# Science, the Dr. Liu part: mockups

November 11, 2026 (Claude Code). Mo sent a screenshot of the Dr. Liu part (he took it for About's;
it is the Science page's, `src/components/science/ink/people.tsx`) and found it "pretty plain or
just a little boring". He asked for ideas, then said "Yes, all three" to mockups.

Review page: https://claude.ai/artifact/Une7FkzNpQuqCt4uyvdXQu (`review.html` + `review/`; version 2
shows round 2 first).
**Mo picked C (November 11), and C is built on `studio`** (AGENTS.md "Science, Dr. Liu";
`reference/ink-pages/science/README.md`, "Dr. Liu"; `build_liu.py`). `shoot_built.py` shoots the
built part at seven window sizes (`review/built-*.jpg`).

## Round 2 (the same day)

Mo: "C is good ... one of the good ideas we could potentially use", but its cell repeats the page's
opening; two more ideas, please. And for mockups Dr. Liu's picture may be changed: "you can make
different kinds of designs and changes to it since we're just building the site right now ... I
will have him check and approve later" (now in `AGENTS.md`, "Real people"). So D and E are Codex
paintings WITH him in them, painted from his photograph (`paint_liu.sh`: his photo, the shipped
painted portrait and the Big Sur hand go with each order). Neither goes live until Mo says Dr. Liu
has approved the picture.

- **D, "Still looking"**: he looks up from a brass microscope, sleeves rolled, a window on a
  eucalyptus and golden hills behind him; one fleck of gold on the stage. `liu-scope-2` (take 1 is
  a spare: livelier washes, a rounder face, less like him). No new words. Score 9, Claude's pick:
  the warmest; a familiar picture, and the calmest.
- **E, "280 papers"**: a joke on "papers": he sends them out as paper planes, three of them gold,
  with a gold "280+" and one new line ("scientific papers, sent out into the world.", a draft).
  `liu-planes-2` (take 1 a spare, fewer planes). Score 8.5: the most fun; playful for a senior
  scientist, his face less like him than in D, dry grass and poppies a small echo of About.
- Left out before painting: a tower of journals taller than he is (the Research part already has
  bound journals), a picnic table (the Ask part has one), an hourglass (reads as time running out).
- Both poses keep his head turned as in the photograph, so his real painted head (`liu-v1`) could
  be set onto either if Dr. Liu prefers his real face.
- The four paintings of the redrawn Dr. Liu and every shot of D and E are kept outside this public
  repository, in `bigh-archive\science-liu-2026-11-11\` (`originals/`, `shots/`, `review/`).
  `review.html` still names them: copy `review/d-*.jpg` and `review/e-*.jpg` back beside it before
  publishing that page again. `plates.py` needs the originals back in
  `reference/ink-pages/science/originals/` to rebuild B's, D's and E's plates (the takes not built,
  `liu-office-1/-2/-3` and `liu-cell-2`, are in that archive too).
- `paint_liu.sh` first ran with a `/c/...` path that Python on Windows could not open: the painted
  portrait was missing and two orders came back with no picture. Fixed in the script.

## What was wrong

- The only part of the page with no painting, colour, gold or motion.
- A small dark studio photograph (a black box on the paper), while NuriCell already shows him as
  the light painted portrait `liu-v1`.
- Vague words ("Recognized internationally" twice; approved September 21, 2026); his real record
  is told lower, in his path.

## The three ideas

Every idea uses the shipped painted portrait (`public/images/products/nuricell/ink/liu-v1.webp`:
his real face, never generated). The paintings were ordered with no person in them.

- **A, "In his own words"** (after Mo's design vault piece #005, Timeline's scientist with a
  quote): the portrait about twice as large, a gold-leaf quote mark, one sentence of his own in the
  title face, his name, role and three facts. The sentence shown is a stand-in: no quote is ever
  invented for Dr. Liu, so A needs a real one from him. Claude's score 8.
- **B, "Office hours"**: he leans on a desk; behind him a blackboard with a chalk mitochondrion, its
  folds in gold (to draw itself once as it arrives). Codex painting `liu-office-3` (take 2 with the
  drawing redrawn). The desk's own front is laid back over him so his hands rest on its top; a
  phone gets its own plate (the board smaller, up on the right). Score 8: a little storybook next
  to his suit; the drawing is very simple.
- **C, "The gold he studies"**: he sits in front of one huge cell, its mitochondria slivers of gold
  (to drift slowly, as on the first screen), with one new line, "In gold: mitochondria. He has
  studied them since 1994." (a draft). Codex painting `liu-cell-1`. Score 8.5, Claude's pick: the
  best looking on desktop and phone; more abstract, and the page's third cell painting.

Motion is described on the review page, not shown (still pictures only).

## Files

- `plates.py`: composes B's and C's plates (wide and phone) into
  `reference/ink-pages/science/plates/liu/` (git-ignored). `figure_cover()` keeps his body solid
  but follows the paint toward his outline: a solid outline left white patches on the desk.
- `shoot.py <base-url> [now] [a] [b] [c]`: opens the real page, puts an idea into `#liu` in the
  browser, and shoots 1440x900, 1280x720 and 390x844 into `shots/` (smaller copies in `review/`).
- Paintings: `reference/ink-pages/science/originals/liu-cell-1.png` (the one built); the others
  are in `bigh-archive\science-liu-2026-11-11\originals\`. Orders
  `reference/ink-pages/science/prompts/liu-office-1.txt`, `liu-office-3.txt`, `liu-cell-1.txt`
  (painted through `paint.sh`; `liu-office-3` by a direct `codex exec` edit of take 2),
  `liu-scope-1.txt` and `liu-planes-1.txt` (`paint_liu.sh`). Nine Codex pictures on Mo's ChatGPT
  plan, no API spend.
- `film_built.py` films the built part's drift for the review page (its two films are not kept
  in the repo; they are on the review page).

## Notes for the build

- Asked twice for separate finger-like folds in the chalk mitochondrion, Codex drew one wavy line
  both times (it matches the homepage's own mitochondrion, one folded band). If B is built, the
  drawing has to be its own layer anyway, to draw itself.
- C's words must end clear of the cell's edge (about 46% across a wide window): at 1280px a 47%
  column ran into it; 42% does not.
- A's portrait is held to the window's height less the menu bar, so he fits a 720px-high laptop.
