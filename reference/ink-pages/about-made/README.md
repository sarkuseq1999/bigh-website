# About: "Proudly made in California." without the bottles (mockups, November 6, 2026)

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
Spend: none.
