# Ink pages: About, product pages and Science in the homepage's Ink & Gold look

October 5, 2026. Branch `ink-pages` (worktree `codes/bigh-ink`), from `origin/main` 415c634.

## Decisions (Mo, October 5, 2026)

- The other pages adopt the crane homepage's design. Of three ways offered (A full match, B re-dress
  only, C day and night) Mo chose **A, full match**: every page on rice paper with ink paintings; the
  dark, glossy and 3D looks go.
- Pictures first. Mockups of About, NuriCell (top and bottom) and Science (top and bottom) were made
  and Mo approved all three ("1 ok 2 ok 3 ok"). They are in `reference/ink-pages/mockups/` and are the
  reference for layout and mood. Words in them may be off: the pages keep today's words.
- Support is later and not part of this spec.

## Source of truth

`DESIGN.md` (Ink & Gold, written from the shipped homepage) is the design system for every page.
Its named rules apply unchanged: One Gold Leaf, No Red No Seal, Sentence Case, Set Lines, Rhythm,
Three Sizes, Phone, Desktop Line, Multiply, Ink Pool, the one shadow (photo mount), honesty labels,
the one breath (2.4s) and its ease, reduced motion complete and still. `PRODUCT.md` holds the
audience (midlife readers, 40–65, many older), the claims rules and the real-assets rule.

Where this spec and DESIGN.md disagree, DESIGN.md wins unless the spec names the exception.

## Scope

In: About (`/about`), the product template and all five product pages (`/products/<slug>`),
Science (`/science`), in all five locales. Out: the homepage (must not change), Support, ordering.

## The shared kit (stage 0)

Today the ink pieces live in `src/components/home-v2/` and `look-ink/`, written for one page. They
move to `src/components/ink/` so every page uses the same pieces, and the homepage imports them from
there. **The homepage must look and behave the same before and after**: `qa_home_ink.py` passes in
full on dev and on `next start`, and before/after screenshots at 1536, 1280, 900 and 390 wide match.

Pieces:

- **Paper**: the rice-paper colour and the 800px fibre texture on the page root; tokens from
  DESIGN.md as CSS custom properties in one shared file.
- **InkPicture**: a painting with its paper divided out, placed with multiply, with the ink-blot
  bloom (`useBloom`), the optional `--edge` mask and the light-on-leaf band held inside a gold mask.
- **Brush line**: `BrushLine` takes a route (waypoints pinned to `[data-brush]` anchors) as a prop;
  the homepage passes its current route. Desktop only (900px and wider), as the Desktop Line Rule.
- **Stations**: label pinned to the line by a leader, shown when the brush reaches it.
- **Controls**: solid and ghost pills, text link, round toggle, tabs, honesty tag.
- **Header and footer**: one site header for every page (the homepage's `HomeHeader`: clear over an
  opening painting, paper once scrolled; same links on every page, including Support, which the
  product header lacks today). One footer for every page: the finale band ("Stay sharp. Live
  fully." with the crane at rest on the closing stroke), then the second tier. Product, About and
  Science headers and footers (`product/site-header`, `product/page-footer`, `about/site-chrome`,
  `science/site-chrome`) are replaced by these.
- **Sheets**: the homepage's dialog sheet (paper sheet on an ink wash) for anything a page opens.
- **Motion hooks**: `useMotionOk`, `useArrival`, `useInkFill`, settle.

## About (stage 1), redesigned October 6: "The name, on a folded letter"

The first ink About (built October 5 from `about.jpg`, commits up to c30a489) is replaced. Mo,
October 6: it was "a copycat" of the homepage. Pages share the theme (paper, ink, one gold leaf,
type, header, footer and its crane), but each page has its own layout, paintings and signature
moment. Of three concepts (A the name written by hand, B a painting album, C one drop of ink) Mo
asked for a blend and approved it ("1", October 6): mockup
`reference/ink-pages/mockups/about-d.png`. The page keeps its words (`about-content.ts`).

**Idea.** The page is one letter on slightly aged paper, folded and opened again. BiGH is written
large by hand at the top; each brushed letter opens one part of the page: **B**e (our purpose),
**i**n (our scientific roots), **G**ood (our experience and our promise), **H**ealth (Ask BiGH
Science).

**Paper and folds (this page only).** The page's paper is the shared rice paper aged a little:
warmer, softly darker towards the sheet's sides, a few very faint age spots; never dirty. Drawn
in CSS on the page root, so it stays crisp at every size. The folds are CSS too: a horizontal
crease (a soft shadow beside a thin highlight) across the full width between parts, and from
900px up one vertical crease down the middle of the sheet. Phones keep the horizontal creases
only: their one column has no two sides. The folds replace the brush line on this page (no brush
line, no stations: that is the homepage's signature). The header turns to this paper once
scrolled.

**Parts, top to bottom** (desktop; phones stack each part in one column):

1. Opening, centred across the fold: the painted word BiGH (one painting, a calm, steady
   calligrapher's brush, never wild; the dot of the i in gold leaf), then "About BiGH", "Be in Good
   Health." (the acronym treatment stays) and the lead. Under them one long horizontal grey
   watercolor band feathering out to both edges of the sheet.
2. **Be**, our purpose. Left half: the painted B with "e" in the sans. Right half: the label "Our
   purpose", the two lines, the mission.
3. **in**, our scientific roots. The sides swap: left half the label, title, text and "Meet our
   scientists"; right half the painted i (gold-leaf dot) with "n", and Dr. Liu's real photo on its
   paper mat resting on a soft pool of grey watercolor (the photo mount shadow stays).
4. **Good**, our experience. Left half: the painted G with "ood", and below it a painted tree-trunk
   cross-section: at least 20 organic rings, one ring about ten from the bark in gold leaf. Its
   meaning, told in the alt text: the rings inside the gold one are the formula's years before
   BiGH began in 2016. Right half: label, "Our flagship formula is older than BiGH." and the three
   figures (280+, 2016, 20+) as large thin numerals on hairlines, counting up as today. Then, across
   both halves, our promise: label, "What you can count on." and the four promises in a row, each
   under a small round watercolor dot, each dot a different tone from deep ink to pale; the
   greetings stay under the fourth.
5. **Health**, centred across the fold: a very big painted H (about the height of the opening
   word) with "ealth", clear paper under it, then "Curious about the science?", the text, Ask BiGH
   Science (solid pill, opens the sheet) and Explore our products (outlined). Then the shared
   footer with the crane.

The brushed chapter words spell the brand's name, like the logo: they stay in English in every
language and are hidden from screen readers (`aria-hidden`); each part's heading carries the
meaning in the reader's language. Section ids stay (`purpose`, `roots`, `experience`, `promise`,
`closing`) so deep links keep working.

**Signature moment: the name writes itself.** On arrival the four letters of BiGH are painted in
left to right through a soft ink front (a mask with one wide feathered edge that wanders gently;
a bristle edge was tried and read as stripes on screen), within one breath
(2.4s, the shared ease); then the i's gold dot comes up. The watercolor band spreads out from the
middle as the name finishes. Each chapter letter writes itself the same way when it reaches the
reading line; the tree's rings draw outward from the heart and the gold ring lights last; the
pool under Dr. Liu and the four dots bloom through the shared ink-blot mask, the dots one after
another. Reduced motion: everything complete and still from the first paint.

**Paintings** (GPT Image 2.5, paper divided out as for the homepage's paintings; gold leaf as
masks): the word BiGH; the letters B, i, G and H, each painted alone in the same hand (the word's
painting as their reference); the watercolor band; the pool; the tree rings; a sheet of
four dots. About nine pictures, about 25 jobs with retakes, about $1.25, inside the $5 Mo gave on
October 6. Honesty tag "Illustration" on the tree rings (it pictures something); the letters,
band, pool and dots are brushwork like the brush line and carry none. Mockup weak spots to fix in
the real paintings: the i of "in" must read as a letter, not a blot; the rings must look painted,
not machine-drawn.

**Removed from About:** the ink mitochondrion and its gold charge, the inkstone, the halo, the
brush line and its stations (`about-route.ts`), and their styles. `InkPage` takes the brush route
as optional so a page can have none. The homepage must not change (the stage 0 gate applies).

## Product template and NuriCell (stage 2)

Mockups: `nuricell-top.jpg`, `nuricell-bottom.jpg`. The seven chapters and their words stay
(Overview, Why it matters, What's inside, The research, The people, How to take it, Buy), then
Questions and More from BiGH. All on paper; no chapter turns dark.

- Overview: the giant name split round the real bottle (as today), the bottle in its ink pool
  (Ink Pool Rule), and behind it a pale painting of the product's own subject (NuriCell: the cell).
  Words, tags, Add to cart and serving line as today.
- Chapter index: the seven chapters become stations on the brush line, which leaves the bottle's
  pool and runs down the left margin. The current chapter's station is ink, the rest ink grey;
  choosing one glides to it. Phones: stations sit in the flow under each chapter heading.
- Why it matters: the dark photo pair (`visual` + `lit`) becomes an ink painting whose light comes
  on in gold leaf as you scroll (light-on-leaf replaces the lit photo). NuriCell: a round paper
  lantern ("Like a light that never goes out"). Facts count up as large thin numerals, then the
  comparison, lines, title and source, on paper. The WebGL dark scene engine (`why-scenes.ts`) goes.
- What's inside: NuriCell's 3D capsule cutaway (its `signature: "capsule"`, NuriCell only) goes.
  In its place one capsule drawn in ink, divided along its length into four bands, one per
  ingredient, each band as long as its share of a serving and in its own ink tone, pinned by
  hairline leaders to its amount and name. Built from one painted capsule texture with the bands
  masked in code. Molecules go. "Why these four work together" on hairlines, as numbered pairs,
  with its honesty note. Products without the capsule signature keep their ingredient list, set on
  paper and hairlines (Advanced OPC's round pictures become ink, below).
- The research: the homepage's research index (notes pinned to the brush line as a spine).
- The people: Dr. Liu's photo on the mat and halo, his name at headline size. Dr. Iris Wang stays
  text only.
- How to take it: one brush dot per day (30 for NuriCell), painted, from deep ink to pale; built
  from a small set of dot paintings placed in code so any serving count works.
- Buy: the real bottle large in its pool; product name, focus, serving rows on hairlines, Add to
  cart (solid pill), credit. Questions on hairlines with round toggles. More from BiGH: the other
  real bottles small in pale pools.
- Removed: `signature/` (capsule cutaway, hero scene, molecules, rigs, why scenes, bottle stage)
  and the dark chapter styling. Back up before deleting (zip in `codes/bigh-archive`).

## The other four products (stage 3)

Each fills its data file only (`products/<slug>.ts`) plus its paintings. Each gets its own ink
painting for the opening and the Why chapter, replacing today's photo for that chapter:

| Product              | Today's Why photo                           | Ink painting                                                                                                                      |
| -------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Green Bee Propolis   | bee                                         | bees on honeycomb, gold leaf in the honey                                                                                         |
| Advanced OPC Formula | grapes                                      | grapes and pine bark, gold leaf light on the grapes                                                                               |
| Turmerific           | turmeric root (plus glass and drops scenes) | turmeric root, gold leaf in its cut face; the glass and drops scenes are dropped, so every product's Why chapter has one painting |
| Nature Calm          | microscope                                  | still water under the moon, gold leaf on the moon                                                                                 |

Advanced OPC's five round ingredient photos and its plants photo become small ink paintings. Each
product's colour accent (`accent`, `tint`, `ink`) no longer colours the interface (One Gold Leaf
Rule); keep the fields only if something still needs them.

## Science (stage 4)

Mockups: `science-top.jpg`, `science-bottom.jpg`. Sections and words stay.

- The scroll film keeps its engine and its story (scroll is the playhead; push, dissolve, pull
  back), with four ink paintings on paper instead of the dark stills: a leaf with a lens (the lens
  in ink, not brass), the leaf's cells seen through the lens with one cell in gold leaf, the
  mitochondrion with gold folds, a soft field of cells with gold at their hearts. The quad
  multiplies onto the paper instead of drawing a dark ground. Headlines as today.
- Dr. Liu: photo on the mat and halo, name very large, the three figures (280+, 1994, 2025) as
  large thin numerals on hairlines.
- A life in cell science: a sideways handscroll. One long horizontal brush stroke; the five stops
  (Okayama, 1994 Berkeley, 2002, 2025, Today) hang from it on hairlines, each with a small ink
  painting with dissolving edges instead of today's sepia photos. The horizontal scroll behaviour
  stays.
- Formulas row: the five real bottles in ink pools with their credits. Research library and
  "Questions like these" on hairlines with round toggles.
- Removed: the dark film stills and the sepia timeline photos.

## Paintings and spend

New paintings, made the way the homepage's were: GPT Image 2.5 through the Higgsfield API
(`reference/home-v2/r4/hf_unquoted.py`, about $0.05 a picture), then the paper divided out and the
gold masks cut with `reference/home-v2/ink/build_assets.py`. Bottles and Dr. Liu's photo are never
generated. Ledger per stage in `reference/ink-pages/spend.md`.

Estimated new paintings: about 33 (About about 9, see its section; NuriCell 3: lantern, capsule
texture, day dots; four products about 10; Science about 9; a few spares), with retakes about 95
pictures, about $4.75. No video is planned; motion is code. Mo approved $5 for stage 1 on October
5 and another $5 for the About redesign on October 6; later stages ask again.

## Words and languages

No page loses words. New strings (station labels, captions, alt text) are drafted in all five
languages and flagged as drafts for a native check, as with the homepage. CJK headlines keep the
CJK Room Rule.

## Checks

- Per page: the existing Playwright scripts are rewritten for the new pages (`qa_about.py`,
  the product scripts with `--product`, `qa_science_film.py` and the others that test removed
  pieces are replaced, not kept passing by asserting oddities). `qa_home_ink.py` runs after every
  stage.
- Run on dev and on `next start` (the built site orders CSS differently).
- Sizes: 1536, 1440, 1280, 1024x768, 900, 768, 390 and 360 wide; reduced motion; keyboard.
- Look at every screenshot full size, scrolled like a visitor; score honestly; 9/10 is the bar.
- A fresh reviewer (impeccable-finish-reviewer) checks each page against its mockup and DESIGN.md
  before it is shown to Mo.

## Delivery

One stage at a time: build, check, show Mo a preview, push only with her yes, and point the demo
alias only with her yes. Fetch and merge `origin/main` before every push (other sessions push).
Stage 0 can ship with stage 1.

## Risks

- Glossy bottle photos against soft ink, worst on product pages where the bottle is the star.
  Ink pools and contact shadows help; it is already the homepage's weakest spot.
- Moving the homepage's pieces can break the homepage. Stage 0 is gated on the homepage checks.
- More paintings means more weight: keep each page's first screen light and fetch the rest late.
- This replaces work Mo liked earlier (the 3D capsule, the glass cell, the dark film). She chose
  that knowingly (option A).
