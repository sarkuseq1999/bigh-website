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
