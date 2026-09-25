# The Science page (September 25, 2026)

## Mo picked D, "Golden hour"

"I like design D better." `/science` now always shows look D (`look-golden.*`). The switcher and the other
five looks moved to `reference/science-page/looks/` (with a README and their color tokens), so any of them
can come back. The page's base colors in `science-page.module.css` are now Golden hour's. Checks:
`qa_science.py` (page-wide, 16/16 in English and in Korean at 1440, 1280 and 390 wide) and
`qa_science_d.py` (look D's scenes, 37/37).

Still open: the NuriCell credit (Dr. Liu only, per Mo's note of 9/25, or both, per 9/21 and the homepage);
a words pass on the DRAFT lines; translations (in Korean the headline now mixes a translated first line
with English, because the new lines have no catalog entries yet); the shared header with the product
branch; committing.

## Round 2: looks D, E, F

Mo's notes on round 1: he liked A's portrait and B's sideways timeline; wanted NuriCell credited to
Dr. Liu and Nature Calm to Dr. Liu and Dr. Iris Wang; found 36 research rows overwhelming; found the design
"a little plain" and asked to step it up with any tools. He said "go" to three new looks:

- **D · Golden hour** (`look-golden.*`): warm parchment and espresso; a full-bleed sunset-desk hero; A's
  focus-in portrait; his record in gold numbers; the career as a pinned film strip of golden photos that
  sharpen at the middle; Today with the two bottles and Dr. Iris Wang. Five GPT Image 2.5 illustrations
  (`public/images/science-page/golden-*.webp`, originals and prompts in `reference/science-page/originals/`),
  each labeled "Illustration".
- **E · Night sky** (`look-sky.*`, `sky-scene.ts`): a three.js starfield behind the whole top; the homepage
  hero's words; a gold-ringed portrait; the career as a constellation line with 280 "paper" stars appearing
  (only the final "280+" is shown as a number). Dark all the way down.
- **F · Glass** (`look-glass.*`, `glass-scene.ts`): a live three.js glass mitochondrion on a pearl page; the
  portrait behind frosted glass that clears; the career on frosted glass cards; bottles on glass stands.
  Weak spot: the live cell is simpler and more cartoon-like than the homepage render it copies.

Shared for round 2: `key-studies.*` (three key studies as cards, "See all 36 sources" opens the full list),
per-look color tokens in `science-page.module.css` (`.page[data-look=…]`), tone props on the shared
sections and footer. NuriCell's credit follows Mo's latest words ("Formulated by Dr. Jiankang Liu.");
on September 21 he credited both scientists and the homepage still does: to confirm.

Checks: `qa_science.py … d,e,f` 33/33; `qa_science_d.py` 37/37, `_e.py` 36/36, `_f.py` 34/34 (real GPU via
ANGLE D3D11, 60 fps). Round 1 still 33/33. Higgsfield plan: 2.5 credits left.

## Round 1: three openings A, B, C (reachable by URL)

Built on branch `science-page` in its own worktree (`C:\Users\mcbig\Documents\codes\bigh-science-page`), so it
does not touch the product-page work on `nuricell-page`. Route: `/science` (and `/kr/science`, …). Preview:
the app's "bigh-science" server on port 3008. Nothing is committed, pushed or deployed yet.

## What Mo asked for

Mo chose "A": a rough version of the whole page first, with 2–3 designs of the top part (the scientists).
He asked to use his Design Vault and Timeline, his favourite site, and to make it really nice. He has no
bigger photo of Dr. Liu yet (he will ask for one); the page uses the 512 × 768 photo for now.

## The page, top to bottom (Mo's 9/16 plan: scientists first)

1. **Meet the scientists**, in three looks (`?look=a|b|c`, switcher at the bottom right):
   - **A · Portrait**: Timeline's calm (vault #005, #014, #015). A centered sentence, the photo rising into
     view and coming into focus, his record as three big numbers (280+, 1994, 2025, each with its source),
     then Dr. Iris Wang in words beside the two formulas they made together.
   - **B · Life's work**: his career as a path you scroll sideways (vault #016, "could look better"). A gold
     line fills; each stop lights at the middle of the screen and carries a source. It ends on the formulas
     with Dr. Iris Wang. Phones and reduced motion get the same stops top to bottom.
   - **C · From the dark** (recommended): the homepage's night palette and hero type. His studio photo has a
     near-black ground, so it dissolves into the page. Then "One cell, three questions": a new render of the
     glass mitochondrion on a dark ground lights up Energy, dims into Aging, and in Balance three lime
     antioxidant droplets (the homepage's render) float in beside it. Changes to the cell are changes to its
     own pixels (light, saturation) or second renders beside it, never shapes on top of it.
2. **The research**: the homepage's 36 checked sources laid out like Timeline's "Our Studies" (vault
   #031–#033), in three groups, five rows each with "Show all". Dr. Liu's own papers carry a small tag.
3. **Health explained**: three round doors (vault #042) for the three planned articles, marked "Article
   coming soon" (the articles are not written).
4. **Ask BiGH Science**: what it will be, three example questions (labeled as examples), the three steps,
   and "In development". No form: the service is not open.

Header and footer are the page's own (`site-chrome.tsx`). The product-page branch is growing a shared
header; the two become one when both branches land. The header's Science link on the other branch still
points at the homepage (`/#learn`); point it at `/science`.

## Words

Approved lines are reused word for word (Dr. Liu's section, the three highlights, the formula credits, the
article titles and previews, "Curiosity, with references.", the Ask BiGH Science steps and note), so their
draft translations already exist. New lines are drafts and are marked DRAFT in `science-content.ts`: the
number labels, the path stops, "One cell, three questions." and its three questions, Dr. Iris Wang's line,
group intros, example questions. English only for now; translations after Mo picks a look.

Rules kept: Dr. Iris Wang in words only, with only the credits Mo confirmed; no invented quote for Dr. Liu;
"animal study", never the animal; the line under the research list stays.

## New picture

`public/images/science-page/dark-cell.webp`: GPT Image 2.5 on the Higgsfield plan (2.75 credits, 16.25 left),
image-to-image from the homepage's glass cell. Original and prompt: `reference/science-page/originals/`.

## Checks (September 25)

`python -X utf8 scripts/qa/qa_science.py http://localhost:3008 a,b,c`: 33 of 33 pass, at 1440 × 900 and
390 × 844 for each look, plus reduced motion: the opening renders with the photo and all shared sections;
"Read his story" opens and closes; A's photo comes into focus and 280 counts up; B's path pins and slides
with stops lighting in order (phones: top to bottom); C steps through Energy, Balance, Aging and the header
turns light over the research; no sideways scroll, no errors, and no words cut off at the screen edge. The
cut-off check was proven by putting the old phone bug back in the browser: it named the hidden words.
Type-check, ESLint and Prettier pass. Also looked at 1280 × 720 and 1920 × 1080.

Caught on the way: C's headline read "scientistsbehind" to screen readers; the path check first passed on
bad data (it measured one spot four times) and was rewritten; on phones, C's oversized picture widened its
column and cut off the headline, tabs and text while the page still reported no sideways scroll.
