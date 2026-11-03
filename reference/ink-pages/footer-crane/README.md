# Footer crane by the park sign

Mo asked for ideas for the footer's "Stay sharp. Live fully." and its crane (October 26, 2026) and
picked B, "end of the trail": the crane leaves the promise and stands in the grass beside the FDA
park sign; the promise stands alone, a size smaller. Of three poses he picked C, the crane bending
toward the sign's poppy (Claude's recommendation).

- Paintings: three poses by Codex (ChatGPT plan, no API spend), each given the homepage crane at
  rest (`reference/home-v2/ink/originals/gpt25-crane-rest-v2.png`) and the redwood park sign
  (`reference/ink-pages/fda-sign/originals/sign-park-full-c5.png`) as references.
  `originals/crane-sign-a1.png` (tall, facing the sign), `b1` (on one leg), `c1` (bending toward
  the sign's poppy, the one built); prompts in `prompts/`.
- `cut_cranes.py` divides out the paper and trims each painting into
  `../mockups/footer-crane/img/`, with a red-crowned copy for the homepage's "green spring".
- `shoot_mockups.py` lays a crane over the live footer (dev server) and shoots the homepage and
  Science at 1440 x 900 and 390 x 844. Page: `../mockups/footer-crane/crane-by-sign.html`
  (Artifact https://claude.ai/artifact/Sa1u9LjcJRrHDxuKPPtvRy).
- Built: `build_footer_crane.py` makes `public/images/home-v2/ink/crane-poppy-v1.webp` (gold
  crown) and `spring/crane-poppy-v1.webp` (red crown, homepage) and prints the measurements the
  CSS places the crane by (`src/components/ink/ink.module.css`, `.look .rest`).
- On a phone the sign narrows to give the crane room (7 lines instead of 5, `text-wrap: pretty`);
  the crane draws smaller there, and the sign and crane a little smaller again under 390 px.

## Part 5: a California animal in the crane's place (November 3, 2026)

The red-crowned crane reads as Chinese, like the homepage's old opening crane and the old close's
cranes did. Mo asked for part 5 of the homepage's California pass, one part at a time. Three
California animals, each looking at the sign's poppy as the crane does, painted by Codex with the
crane's painting (`originals/crane-sign-c1.png`, its hand and layout) and the park sign as
references (`paint.sh`, prompts in `prompts/`):

- A, California quail (the state bird): the covey's lookout stands tall, the other bends to the
  poppy. `originals/quail-2.png` (a looser second take; the first was a detailed field-guide bird).
- B, desert tortoise (the state reptile, among the Mojave's poppies): `originals/tortoise-2.png`
  (the first came out a Galapagos giant).
- C, black bear cub (state parks; the bear on the flag): `originals/bear-1.png` (the second take's
  back read as a pale stripe).

The unused takes are in `bigh-archive/footer-crane/`. `shoot_animals.py` swaps the built site's
crane for each animal, placed as `.look .rest` places the crane (feet on the sign's ground, a gap
right of the sign, all in the sign's `--k`), and shoots the homepage and Science at 1440 x 900 and
390 x 844; on phones each keeps the sign at seven lines. `make_animals_mockup.py` cuts the shots
and writes `../mockups/footer-crane/animals/footer-animal.html` (Artifact
https://claude.ai/artifact/EHcCHzYJaB9jpPDvAhAKLb). Claude's pick: A.
