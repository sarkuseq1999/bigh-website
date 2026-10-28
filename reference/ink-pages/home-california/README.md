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
