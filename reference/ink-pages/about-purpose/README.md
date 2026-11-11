# About: "Our purpose", the oak on a sunny afternoon (Mo picked A, November 10, 2026)

Mo on the purpose part's oak (the October 19 valley oak in black ink, a rope swing, a gold light
in its roots): "this tree looks a little dark or scary, almost", and asked for ideas, "maybe some
kind of redesign", that fit the About page and the site. Why it read scary: black ink right after
the sunny poppy meadow, bare roots hanging in empty paper, and an empty swing (the words say "a
full life", and nobody was in the picture). The page's newer paintings (the meadow, the globe, the
valley at dawn) are soft colour; the oak was the darkest thing on it.

Three ideas in words, then Mo: "Paint all three". The words do not change in any of them.

- **A, the oak on a sunny afternoon** (my pick, 8.5/10; **Mo's pick**): the same oak in the valley
  painting's soft colour, a child on the swing, a grandmother pushing, a dog, a picnic; the roots
  inside a slice of warm earth, a patch of gold leaf among them. `oak-1-b` (`oak-1-a` was more of
  a storybook picture). Holding it back: the gold patch is small and could read as buried
  treasure; "Made in California" also has oaks.
- **B, Monterey Bay above and below** (8.5/10): a sea otter, a pelican and a paddle-boarder on
  the water, a kelp forest in gold leaf under it. `bay-1-b`. Holding it back: the link to "your
  cells" is looser; an otter and kelp could say ocean charity, or that BiGH sells seaweed.
- **C, the cable car** (8/10): a San Francisco cable car with a family on board, the street cut
  open to show the hidden cable in gold leaf. `cable-2-b`. Round 1's takes (`cable-1-*`, 7.5/10)
  had the gold as a stripe that read as a line painted on the road, and brass poles as yellow as
  the gold; `cable-2` opens a tunnel with pulleys and a grip, and makes the poles dark. Holding it
  back: a city and a machine on a page of nature; the busiest picture.

Pictures: `paint.sh` (Codex, ChatGPT plan, no spend; the references for the hand are the valley
at dawn, the poppy meadow and the homepage's Big Sur close, not the dark oak). Mockups:
`cut_mockups.py` divides the paper out, `shoot_mockups.py` swaps each painting in for the oak on
the live About page (injected, nothing in `src/` changes), `pack_review.py` packs the shots.
Review page: `reference/ink-pages/mockups/about-purpose/about-purpose.html`
(Artifact https://claude.ai/artifact/8dvh62Mg1w7xtgNrYMz9Yp).

## Built (Mo: "Yes, go live", November 10, 2026)

`build_about_purpose.py` -> `public/images/about-purpose/oak-afternoon-v1.webp` (1024 x 1020, the
paper divided out), its gold-leaf light mask `oak-afternoon-v1-gold.webp`, and
`src/components/about/purpose-art.ts`. The kit's `gold_mask` finds gold by colour alone; here the
dry grass and the earth are warm and saturated too, so the build looks for the leaf only in a box
under the trunk (`LEAF_BOX`), by its yellower hue and stronger colour than the earth round it.

On the page (`about-ink.tsx`, `circle.module.css`): the painting keeps the oak's larger size (1.72
plain heights; nearly square now, so 566px wide at 1440px where the old oak was 521px) and its
place left of the words. Its description is new (`translations-purpose.cjs`, m1230, draft
translations, not native-reviewed; the old oak's m900 stays in the catalogs, unused).

**The gold at rest.** First built with the kit's glint as it is, the band of light stood on the
patch exactly when the painting rested in the middle of the window (the patch is small, solid and
in the painting's middle) and washed the gold to a pale cream that read as a hole in the paint.
Now the band's range is `cover 22% cover 52%` for this painting: the light crosses the leaf as
the painting comes up and has left it before the painting is centred. Browsers without
scroll-driven animation get no band here (the kit's timed one would turn the patch pale every few
breaths).

The unpicked takes (`oak-1-a`, `bay-1-*`, `cable-1-*`, `cable-2-*`) and their prompts went to
`bigh-archive/about-purpose-unpicked-2026-11-10/`; `cut_mockups.py` and `shoot_mockups.py` need
them back in `originals/` to remake the mockups. The mockups' pictures on the review page are in
`reference/ink-pages/mockups/about-purpose/web/`.

Checked on the built site (`npm run build` + `npm start`, November 10): `qa_about` 453/453 (a
new `purpose` group: the painting, its description, and the leaf plain gold at rest at 1440x900,
390x844 and with reduced motion), `qa_home_ink` 288/288, `qa_nav` 326/326; lint, type-check and
prettier clean. Looked at 1440x900, 1920x1000, 768x1024 and 390x844 (`shoot_built.py`): 8.5/10.

**Live November 10, 2026:** `main` `a3bfad5` (this commit on top of `4d846c7`, NuriCell's clear
day, which another session put live while this was being checked; rebuilt and re-checked on top
of it: 453/453, 288/288, 326/326), production `dpl_2ptufqJCHjqrP86VxnXgjem5sjGr`. On the public
demo: `qa_about` 453/453, `qa_home_ink` 288/288, `qa_nav` 326/326 (`docs/public-demo.md`).

Noted for later, not asked for: the sequoia in "Our experience" (and the grey pool behind
Dr. Liu, the promise dots, the glasses) are in the same grey ink as the old oak; the sequoia is
now the page's darkest painting. One part at a time.

Spend: none.
