# NuriCell in Ink & Gold: the product page, its own way

October 9, 2026. Branch `nuricell-ink` (worktree `codes/bigh-nuricell-ink`), from `origin/main` db5d247.
The next page in the site-wide restyle (`2026-10-05-ink-pages-design.md`), after About C went live on
October 8. This spec replaces that file's "Product template and NuriCell (stage 2)" section: that
section's brush-line stations, ink mitochondrion and capsule bands are the homepage's devices, and Mo
ruled on October 6 that each page shares the theme only and has its own design.

## Decisions (Mo, October 9, 2026)

- Three ideas were mocked (A the lantern, B the capsule opens, C the plates). Mo picked **A**, then
  shaped it over eleven mockup rounds. Approved screens: `reference/ink-pages/mockups/nuricell-ink/`.
- **One painting per chapter, each chapter its own.** The lantern lives only in "Why it matters";
  a lantern pinned beside every chapter was boring, beside Dr. Liu's photo busy, beside the bottle
  crammed (round 3).
- **Painted, not drawn.** Loose sumi-e brushwork like the homepage's resting crane; realistic
  drawings read as boring (round 5).
- **No lab glassware** (reads as "chemicals you eat"), **no black-and-white portrait of a living
  person** (in Asia it signals the person has died), **no gold halo behind the bottle** (round 4).
- **Dr. Liu as a painting** (Mo's idea, round 9; chosen face: the bolder repaint, round 11). This is a
  deliberate exception, for this page, to the real-assets rule that his face is never generated. Mo
  chose to show it without waiting for Dr. Liu's approval; showing him first is still advised.
- **The other four product pages keep today's template** until each gets its own paintings (1A).
- **The floating chapter index goes** (2B).

## Shared, and its own

Shared with the homepage and About (the theme): the kit's rice paper, sumi ink, gold leaf only for
energy, Switzer, the site menu bar (`SiteHeader`, current "Products"), the footer that closes on the
crane at rest (`SiteFooter` + `ClosingCrane`), the ink bloom, the honesty captions, the one breath and
its ease, reduced motion complete and still. `DESIGN.md` applies unless named here.

Its own: the chapter layout below, its paintings, and its signature moment (the lantern's light comes
on). No brush line, no stations, no enso, no reused homepage or About painting (the bottle's ink pool
is the kit's shared Ink Pool, not a painting).

## The page, top to bottom

Every chapter is **one painting on one side, its words on the other** (desktop, from 960px), the
painting on the left, at about the same size in every chapter, filling its column. Phones (one
column): the painting first, then its words. Chapter ids stay (`overview`, `why`, `inside`,
`research`, `people`, `daily`, `buy`) so deep links keep working. Every word in `nuricell.ts` stays.

| #   | Chapter        | Painting (left)                                                                                                                                 | Words (right)                                                                                                                                                                                                            |
| --- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Overview       | No painting: the giant name parts round the **real bottle** (`nuricell.png`) standing in the kit's ink pool, as today's "Big name" but on paper | eyebrow, headline lines, purpose, highlights, Add to cart, serving supply                                                                                                                                                |
| 2   | Why it matters | **The lantern**: a tall paper lantern on its cord, unlit, then lit from within by gold leaf                                                     | label, title, lines, the two facts (2% / 20%) as large thin numerals counting up, the comparison, the source                                                                                                             |
| 3   | What's inside  | **The capsule opens**: its halves and four powder heaps on one line, heaps sized by amount, gold sparks rising                                  | "Inside every capsule, four ingredients.", the four rows (amount, name, role), `notes.label`, other ingredients, `notes.science`; then "Why these four work together" as three numbered pairs on hairlines with its note |
| 4   | The research   | **Stepping stones of seven books** across a calm stream (seven studies)                                                                         | heading, `notes.research`, the studies on hairlines, each opening with its round toggle, "Show all 7"                                                                                                                    |
| 5   | The people     | **Dr. Liu, painted** in ink and colour, his suit in loose wet strokes                                                                           | his name at headline size, title, his two paragraphs                                                                                                                                                                     |
| 6   | How to take it | **Breakfast**: a soft-boiled egg whose yolk is gold leaf, a dish of three capsules                                                              | "One bottle, one month.", the sum **3 × 30 = 90** painted with a brush, a caption under each number, `serving.use`                                                                                                       |
| 7   | Buy            | **The real bottle on one bold brush stroke**                                                                                                    | eyebrow, name, focus, how to take it, in each bottle, Add to cart, credit                                                                                                                                                |

Then, full width on paper: **Questions** (hairlines, round toggles), **More from BiGH** (the other
four real bottles, small, each in a pale pool, linking to its page), the small **caution and FDA
notes**, then the shared footer.

Where a chapter's words run longer than its painting (What's inside with the pairs, The research
with a study open), the painting stays put in its column while the words scroll (sticky), and
leaves with its chapter.

Gold appears only where energy is meant: the lantern's light, the capsule's sparks, the yolk (food
becoming energy). The research, Dr. Liu and the buy stroke carry none, so the eye rests between.

## Motion

- **Signature: the light comes on.** As "Why it matters" arrives, the unlit lantern blooms into the
  paper (kit bloom), then its light comes on over one breath: the lit painting fades up over the unlit
  one and a soft warm haze spreads behind it (inside the painting, not a UI gradient). Once, on
  arrival. The facts count up as they arrive.
- Every other painting blooms as it arrives (kit `useBloom`). Gold leaf takes the kit's glint once
  bloomed.
- Opening: the words settle as on the homepage; the bottle rises onto its pool.
- Reduced motion: everything complete and still from the first paint, the lantern already lit.
- No WebGL, no 3D, no scroll-scrubbed film on this page.

## Data and template

- The route picks the template per product: a product with ink paintings in its data
  (`ProductPage.ink`) gets the ink page inside `InkPage` (shared header and footer); the others keep
  `ProductPageView` exactly as today. Only NuriCell has `ink` in this branch.
- `ink` names each chapter's painting (file, size, alt text, optional gold mask, optional lit layer
  for "why"), the daily picture and its brushed sum, the buy stroke, and a painting for a person
  (`people[].painting`), so the other four can fill theirs later without template changes.
- Nothing shared is deleted: the 3D bottle, capsule cutaway, why scenes and chapter index stay for
  the other four products.

## Paintings and spend

From the approved mockups, kept as finals (originals and prompts in `reference/ink-pages/nuricell/`):
`gpt25-P7-capsule`, `gpt25-P7-stepping-books`, `gpt25-P11-liu-face-bold`, `gpt25-P7-egg-capsules`,
`gpt25-P7-sum`, `gpt25-P5-stroke`. New: **the lantern**, unlit and lit from one composition (the lit
one first, the unlit as an edit of it), 3 to 5 GPT Image 2.5 jobs, about $0.25, inside the $5 Mo gave
on October 9 (65 of the 70-job cap used by the mockups). A build script (on the pattern of
`reference/ink-pages/about-bc/build_bc.py`) divides the paper out, cuts the gold masks, re-spaces the
brushed sum's numbers (the model wrote 30 and = touching), and writes webp files to
`public/images/products/nuricell/ink/` plus a generated data file. Honesty caption "Illustration"
under each painting; Dr. Liu's reads "Portrait painting".

## Words and languages

No words are lost. New strings (alt texts, "Portrait painting", the sum's captions) are drafted in all
five languages via a `translations` script, flagged as drafts for a native check. Most product data
strings are still English-only in every language today; that gap is not part of this work.

## Checks

- A new `scripts/qa/qa_nuricell_ink.py`: every chapter and every `nuricell.ts` string present; each
  painting loads and blooms; the lantern ends lit; no horizontal scroll; phones stack picture first;
  deep links land under the menu bar; reduced motion is still and complete; keyboard reaches every
  toggle and button.
- The other four product pages unchanged (their own QA scripts); homepage gate (`home_snapshot.py`,
  `qa_home_ink.py`) and `qa_about.py` unchanged.
- Sizes 1536, 1440, 1280, 1024x768, 900, 768, 390, 360; dev and `next start` (the built site orders CSS
  differently). Look at every screenshot full size, scrolled like a visitor; 9/10 is the bar; a fresh
  reviewer (`impeccable-finish-reviewer`) before Mo sees it.

## Delivery

Local commits on `nuricell-ink`. Mo sees screenshots first; a Vercel preview only with her yes to
push the branch; main and the demo alias only with her yes. Fetch and merge `origin/main` before any
push (other sessions push).

## Risks

- The painted portrait of a real, living scientist: likeness and his consent.
- The real glossy bottle against soft ink (the homepage's weakest spot too); the pool and the stroke
  help.
- Two templates live side by side until the other four products follow.
