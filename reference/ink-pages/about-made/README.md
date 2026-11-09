# About: "Proudly made in California." without the bottles (Mo picked F, November 9, 2026)

Mo on the draft's Our home part (the five real bottles standing in a painted Southern California
morning): "this section just doesn't look good when you put the product bottles in that image. I'd
rather not have the product bottle there", and asked for design ideas. "Made in California" also
goes back into the promise list when the picked idea is built.

Three ideas, built on the real page behind `/about?made=a|b|c`
(`src/components/about/made-mockups.tsx`, English only, mockup code; plain `/about` still shows
the draft with the bottles):

- **A, the crate label**: an old California fruit-crate end, its label an orange grove under the
  Sierra with a gold-leaf sun; "Be in Good Health" set in its banner by the page (SVG text in
  Ysabeau, multiplied). `crate-1-a`.
- **B, the record book** (my pick): an open batch record on a redwood table, a pressed California
  poppy in its gutter and a gold-leaf ribbon. The page writes the chapter's words on the book's
  empty ruled lines (SVG text, the lines found at y 212, 288, 362, 436, 512, 586, 660, 733 of
  1536 x 1024), one entry after another as it comes into view. Under 900px only the right page
  shows (the three rules), its cut fading into the paper. `ledger-1-a`.
- **C, the Golden State**: California painted alone over its real outline (`render_state.py`
  draws us-atlas 3.0.1 `states-10m`, US Census 1:10m, as `ref/state-guide.png`), the Central
  Valley in gold leaf, with a light mask for the kit's glint. `state-1-a`.

Takes `-b` of each were painted too (kept in `originals/`, not used): the crate's label had a red
rule round it, the book's ribbon crossed the right page's lines, the state was much the same.

Pictures: `paint.sh` (Codex, ChatGPT plan, no spend), `build_about_made.py` ->
`public/images/about-made/` and `src/components/about/made-art.ts`. Review page:
`reference/ink-pages/mockups/about-made/about-made.html` (Artifact Tye45mScMvZEoGSRxjZih9).

**Round 2 (Mo asked for more ideas the same day):** `/about?made=d|e|f`.

- **D, the checks in the sun**: a clipboard on a sunlit Southern California stucco wall, a palm's
  shadow across it; the page brushes a gold tick into each of its three boxes, one after another
  (`wall-1-a`; the boxes' places are `WALL_BOXES` in the build script). 8/10.
- **E, the gold pan**: a Gold Rush pan at the edge of a Sierra creek with gold caught in it
  (`pan-1-b`, then `pan-2-a` closer and paler). 7/10: the gold too small and its link to "checked"
  a stretch. Built behind `?made=e` but left off the review page (under the 8/10 bar).
- **F, the valley at dawn**: one painting across the chapter, the Central Valley in first light,
  some fields in gold leaf, the heading in its empty sky and the three rules in a row under it
  (`valley-1-b`; `valley-1-a` came back with a transparent sky). 8/10: farmland says "grown" more
  than "made", and its oaks echo the page's own oak.

My pick of the five shown stays B, the record book (9/10).

Spend: none.

**Mo picked F, the valley at dawn (November 9, 2026).** Built for real as
`src/components/about/made-in-california.tsx` (`made.module.css`); the mockup switch and the other
ideas are gone. Their paintings, prompts, `render_state.py` and the mockup code went to
`bigh-archive/about-unpicked-2026-11-09/`. `build_about_made.py` now builds the valley alone
(`valley-1-b`, uncropped so its sky holds the words). "Made in California." is back in the promise
list, first of four.
