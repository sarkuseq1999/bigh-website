# Closing block: "Start with your cells."

The last content block on the homepage, before the footer. It brings the visitor back to the
cellular-health message and gives one clear route: NuriCell, or the full range. The words are Mo's
accepted working copy from September 21, 2026 (BRAND-CHEATSHEET.md): headline "Start with your
cells.", one line about NuriCell, the buttons "Discover NuriCell" (opens the NuriCell product) and
"Explore all products" (jumps to the products block).

## Three looks for review (September 24)

Built in `src/components/home/closing-section.tsx` with `closing-section.module.css` and the copy in
`closing-data.ts`. The look is chosen with `?closing=1|2|3` in the address; the page renders look 1
by default. On the public demo:

- <https://bigh-website-demo.vercel.app/?closing=1#start>
- <https://bigh-website-demo.vercel.app/?closing=2#start>
- <https://bigh-website-demo.vercel.app/?closing=3#start>

1. **Space** (default): the page ends where it began, in the dark. Mo liked this look but not the
   reuse of the hero's cell ("that cell is already from the top of the page"), so the picture is now a
   new GPT Image 2.5 render in the hero's style, made with the hero picture as a style reference: a
   constellation of many cells (`reference/closing-section/originals/close-constellation.png`,
   served as `public/images/closing/space-cells.webp`). One cell opens the page; your many cells
   close it. A second candidate, a cell in the moment of dividing (`close-dividing.png`), is archived
   unused. The picture is centered, its edges softened into the dark, drifting slowly and turning a
   little toward the pointer. White headline with "your cells." in the hero's italic serif; a lime button like the
   hero's. Dark to the footer's grey.
2. **Light**: the NuriCell bottle stands in the science section's warm gold light, with a soft
   reflection and shadow, beside the words. The light comes on and the bottle settles as the block
   arrives; the bottle then tilts gently toward the pointer. Ink button, outlined second button.
3. **Field**: the statement alone, centered, over a living field of tiny cells drawn on a canvas:
   rows on a slow wave, cream-gold far away and warm gold near the front, which brighten and lift
   near the pointer. The field dissolves before the footer.

All three rise into view once as the block arrives (GSAP ScrollTrigger). With reduced motion the
words, picture and field are simply there, still, and the field still lights near the pointer.
In English, "your cells." is set in italic serif by finding it in the translated headline; other
languages keep the line in one voice.

## What changed around it

- The footer's own headline and button ("Stay sharp. Live fully." / "Explore BiGH") stepped aside,
  since the closing block now ends the page. The removed markup is kept in
  `reference/closing-section/2026-09-24-previous-footer-top.tsx.txt`; the strings stay in the
  catalogs.
- The old research list and "Our purpose" block still sit between the science section and this
  block until Mo decides whether they move to the Science and About pages.
- New strings (drafts, five languages): the headline, the description and "Explore all products",
  from `reference/closing-section/translations-closing.cjs`. "Discover NuriCell" already existed.

Higgsfield plan credits for the two candidate renders: 18 (9 each), leaving 19.

## Checks

Type-check, ESLint (including the React hooks rule: the look comes from the address through
`useSyncExternalStore`, not a state set in an effect), Prettier and Impeccable's detector pass.
`qa_closing.py` passed 12 of 12 locally and on the public demo: each look renders in English and
Korean at 1440 and 390 wide, the words are shown, "Discover NuriCell" opens the NuriCell product,
the "Explore all products" target exists, there is no sideways scroll, no errors, and the footer's
old headline is gone. The science section's 21 checks still pass on the same build.

## Decision

Mo liked the Space look (with the new picture) but then had another idea, September 24, late: do
not show this block at all. Keep the two older blocks at the bottom, the research list ("Curiosity,
with references.") and then "Our purpose is simple.", and let the page end on "Our purpose". The
component, its styles, copy, translations and pictures stay in the repo, unrendered (the line in
`homepage.tsx` is commented). The footer's own headline stays removed so the page really ends on
"Our purpose"; it can come back from `reference/closing-section/2026-09-24-previous-footer-top.tsx.txt`.

## After the decision (September 24, late)

Mo asked how the ending felt. Honest answer: calm and right for a science-first brand, but with no route to the product at the very end, and the two older blocks are denser than the new sections. She said "take a look", so: a quiet "Discover NuriCell" text link now sits beside "What matters to us" in "Our purpose" (it opens the NuriCell product, like the hero's button), and the two blocks' labels were renumbered from 04 and 05 to 07 and 08, since they are now the 7th and 8th blocks on the page (values changed in all five catalogs; the copy keys are unchanged). A polish pass on the two older blocks stays on the later list.
