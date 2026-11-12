# About: "Our experience" ideas (November 11, 2026)

Mo: the site's look has turned more American, more California and more colourful, so the About
page's last three parts (Our experience, Our promise, "Curious about the science?") should
reflect that; one part at a time. This is the first: "Our experience" ("Our flagship formula is
older than BiGH." and its three numbers). Today's painting is the grey ink giant sequoia beside a
young one (`about-bc/sequoia-v1`): now the page's darkest picture, and giant sequoias are also the
homepage's opening.

Three ideas, mocked on the real page (the words and numbers unchanged; A and B add one short line
under the painting, new words Mo has not approved):

- **A, the parent tree** (my pick, 8/10): one old orange tree behind a low iron fence, young
  groves running out behind it to the snowy San Gabriel Mountains, gold leaf on some of the old
  tree's oranges. `orchard-1-a` (`-b`'s gold came out as pale lemon discs). Line: "Riverside's
  parent navel orange tree was planted in 1873. The groves came after it, and it still bears
  fruit." Checked: California State Parks, landmark 20 (two young trees sent to Riverside in
  1873); one still stands, kept alive by inarching (1918, 1951), and bears fruit (UCANR). Not
  claimed: that every navel orange descends from it. Holding it back: at page size the gold
  oranges read as pale yellow fruit; the page's second big tree after the oak.
- **B, the mother dough** (7.5/10): a San Francisco sourdough loaf, the baker's crock of starter,
  Victorian houses and the bay in the window; gold leaf on the crust's burst ridge.
  `sourdough-1-a`. Line: "One San Francisco bakery says it still bakes every loaf from the starter
  it began in 1849." (Boudin's own claim, hence "says".) Holding it back: needs its line; food on a
  supplement page; more detailed than the site's loose hand.
- **C, the old carousel** (7.5/10): an old carousel on a seaside pier, children riding, a
  grandparent helping, its canopy's trim in gold leaf. `carousel-1-a`. Holding it back: the
  weakest link to the heading; storybook; an amusement ride for a health brand.

Ruled out before painting: the sequoia repainted in colour (it would read as the homepage), a
redwood (NuriCell's chapter 6 is a redwood round), old vines (wine on a health page), a house
built round an old tree (repeats the purpose oak with its family).

Pictures: `paint.sh` (Codex, ChatGPT plan, no spend; the hand's references are the valley at
dawn, the poppy meadow, the sunny oak and the homepage's Big Sur close). Mockups: `cut_mockups.py`
divides the paper out, `shoot_mockups.py` swaps each painting in for the sequoia on the live About
page (injected; the painting is lazy and far down the page, so the swap sets it eager first),
`pack_review.py` packs the shots. Review page:
`reference/ink-pages/mockups/about-experience/about-experience.html`
(Artifact https://claude.ai/artifact/5ovTaXUGkaFShrw2jp7D8A).

## Round 2: the sequoia, a little coloured

Mo: "I think the sequoia tree is a good idea. Maybe just make it a little bit colored." (A, B and
C set aside.) Three versions, mocked on the real page:

- **1, same painting, tinted** (7.5/10): `tint_sequoia.py` tints the shipped
  `public/images/about-bc/sequoia-v1.webp` stroke for stroke (ink as pigment, the homepage's
  recolour kit): the trunk (a hand-drawn soft mask) cinnamon brown, the rest sage to pale
  blue-green. `sequoia-tint-light` (strength 0.55; `-touch`, 0.35, looked almost the same).
  Holding it back: the colour sits on top like a tint; the bark reads dusty.
- **2, repainted in colour** (8.5/10): `paint_colour.sh` gives Codex the shipped sequoia as the
  picture to repaint, with `prompts/sequoia-colour.txt`. `sequoia-colour-b` (`-a` is nearly the
  same, a little more orange). Same tree, layout and gold spot, new brushwork. More than "a
  little" colour.
- **3, repainted, softer** (8.5/10, my pick): `sequoia-colour-b` mixed 35% toward its own grey,
  the gold patch kept at full colour (a quick mock mask that also kept a few orange bark streaks
  beside the patch; a build needs a proper gold mask). `sequoia-colour-b-soft`.

The phone shots now start the part under the sticky menu bar (its top was hidden in round 1's,
today's too). Review page as before (version 2), round 1 folded at its foot.

## Built: 3, the softer repaint (Mo, November 11, 2026)

Mo picked 3. `build_about_experience.py` makes the site's picture from `originals/sequoia-colour-b`:
the colour mixed 35% toward its own grey (`SOFT`), the gold leaf kept at full colour, the paper
divided out (it multiplies onto the page like the other paintings), and the leaf's light mask for
the kit's glint. The leaf is cut properly now (the mock's quick mask also kept a few orange bark
streaks beside it): its clearest yellow as a core, then OpenCV's GrabCut grows it to the leaf's
shape against the bark. Out: `public/images/about-experience/sequoia-soft-v1.webp` (1022 x 1024,
the ink sequoia's shape, 0.998, so the page's sizes did not change), `sequoia-soft-v1-gold.webp`
and `src/components/about/experience-art.ts`.

On the page the kit's band of light stood on the leaf as the painting rested in the middle of the
window and washed it to cream (red over blue 87, where the plain leaf holds about 115): the
purpose oak's trouble of November 10. The sequoia takes the oak's range (`circle.module.css`):
the light crosses the leaf as the painting comes up and has left it at rest.

The description is new (`m1250`, `translations-experience.cjs`, draft translations, not
native-reviewed): "An ancient giant sequoia rising from mist beside a young sequoia, painted in
soft watercolour, a patch of gold leaf on its trunk". The ink sequoia's (`m591`) stays in the
catalogs, unused, like the old oak's. `qa_about.py` has an `experience` group.

Unused takes (round 1's orchard, sourdough and carousel, `sequoia-colour-a`, the two tints) are in
`C:\Users\mcbig\Documents\codes\bigh-archive\about-experience-unused-2026-11-11\`.

Spend: none.
