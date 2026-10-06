# Menu bar "Inscription": critique and 10-round plan

October 5, 2026. A fresh review of the live bar (branch `nav-options`, production build on
http://localhost:3028), and a plan for ten rounds of improvement. Written by a reviewer who did
not build it.

All pictures are in `scripts/qa/out/nav-critic/` (zoomed crops in `zoom/`, motion frame strips
named `motion-*.png`, outside references in `refs/`). The capture scripts were run with
Playwright for Python, Chromium, `--use-angle=d3d11`.

What was looked at: 1536x900, 1280x800, 1920x1080, 1101x800, 1366x657 and 1280x720 (top, scrolled
to three depths, every link hovered, Products open, Science open, moving between them, Tab
through the bar); phone 390x844 (top, scrolled, menu, Products, Science, menu foot); tablets
834x1112 and 768x1024; Vietnamese and Japanese at 1101, 1280, 1536 and on the phone; reduced
motion. Motion was slowed to one fifth with the browser's animation clock, and the Science
opening was also filmed at real speed.

---

## 1. Scores

| Part                      | Score | In one line                                                                                                                                                           |
| ------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (a) First glance, desktop | 7/10  | Clean, large, centred, calm. But plain at the top, and the left pair is visibly heavier than the right.                                                               |
| (b) Drop-downs            | 6/10  | Big, readable, real bottles, a lovely torn edge. Spoiled by a white-box flash, a blank moment when switching, and four mismatched pictures.                           |
| (c) Scrolled bar          | 4/10  | The bar is see-through: page headlines ghost behind the words. The "brush" rule reads as a grey loading bar and strikes through text under it.                        |
| (d) Phone and tablet menu | 7/10  | Calm, centred, big words, and the crane at rest is a real moment. But the bottle row is cut off on purpose, and the tablet menu has a hollow gap.                     |
| (e) Long languages        | 6/10  | Nothing overlaps. But in Japanese the account group runs into the links, and Vietnamese wraps unevenly.                                                               |
| (f) Motion                | 6/10  | The unroll is beautiful. The rule sweep, the switch, the flash and a popping crane are not.                                                                           |
| (g) Older visitors        | 7/10  | 18–20px words, 48px targets, clear focus rings, Escape works. But "Sign up" is a dead button that looks live, and the ghost text lowers contrast in the scrolled bar. |

---

## 2. What already works (keep it)

- The centred mark is the right idea. Over the painting it really does read as the title of a
  scroll (`d1536-01-top.png`, `d1920-01-top.png`).
- Type size is right for the audience: 20px links at 1536, 18px at 1101, all targets 48px.
- The torn rice-paper edge is well made. At 2x it has real fibres (`zoom/d1536-science-tornedge-left-x2.png`).
- The unroll itself (paper revealed top to bottom, contents settling left to right) is calm and
  crafted (`motion-unroll-products.png`).
- The phone menu's crane at rest under the lines is the best single moment in the whole bar
  (`p390-03-menu.png`).
- Keyboard: Tab order follows the line, Enter opens, Tab steps into the scroll, Escape hands focus
  back (`d1536-07-tab*.png`).
- Reduced motion is complete and still (`rm1536-02-products-250ms.png`).

---

## 3. Defects a first-time visitor could read as a mistake

Ordered by how bad they look.

1. **The scrolled bar is see-through.** The paper is at 93%, so page text shows through behind the
   bar's own words. At 1920 the headline "A big part of" sits in grey right behind "English" and
   "Products". It happens at every size and on the phone.
   `d1920-05-scrolled.png`, `zoom/d1920-scrolled-ghost-x2.png`, `d1536-05-scrolled.png`
   ("cells can use." behind "English"), `zoom/scrolled-bars-strip.png` (eight positions; "In their
   own words", "Good questions deserve clear answers.", "of the science" all ghosting),
   `zoom/p390-scrolled-bar.png` (phone: a whole paragraph behind "Menu BiGH English"). The page's
   own vertical brush line also shows through the bar, right behind the mark.
2. **The rule strikes through text.** Under the bar the paper fades out over 9px, so a line of the
   page that sits at the bar's edge is crossed by the ink rule. On a tablet "Explore cellular
   health" looks deleted. `zoom/t768-scrolled-bar-x2.png`. Same at 1280 with "Illustration" and
   a story byline (`zoom/scrolled-bars-strip.png`, rows 3–4).
3. **Science opens with white boxes.** For about 0.8 seconds after Science opens (filmed at real
   speed: from about 560ms to 1330ms), the cell, the reading still life and the inkstone sit on
   white rectangles, then snap onto the paper. Cause: the settle animation runs on the picture's
   frame, which isolates the picture's multiply blend until the animation ends.
   `motion-science-flash-realtime.png`, `motion-switch-science.png`. Static screenshots taken
   after 1.6s never show it, which is why it was missed.
4. **The rule is not a brush.** The asset is drawn by a script: a round blob for a head, an even
   7px grey body, and a tail of rectangular pixel dashes. At 1536 it reads as a heavy grey bar,
   and while it draws left to right over 1.1s it looks exactly like a page-loading progress bar.
   `zoom/asset-rule.png`, `zoom/d1536-scrolled-left-x2.png`, `motion-scroll-settle.png`.
5. **Switching shows a blank scroll and sideways arrows.** About 200ms after moving from Products
   to Science, both panels are faded to ghosts, both words are underlined, and both chevrons are
   half-turned so they point left like "back" arrows. `d1536-04a-switch-200ms.png`.
6. **The torn edge slices page headlines.** The scroll ends across the opening's headline, so a
   visitor sees half of "your cells." under the paper (1280, 1101), or half a line of body text
   (1366x657). The 22% wash is too light to push it back. `d1280-03-products.png`,
   `d1101-03-products.png`, `d1366x657-products.png`.
7. **The phone menu's third bottle and its name are cut off.** "Advar / OPC Fo" at the right edge,
   and after a swipe "anced / Formula" at the left. It is meant as a swipe hint, but by Mo's own
   rule ("on purpose that looks broken is a defect") it fails. `p390-04-menu-products.png`,
   `p390-04b-menu-products-swiped.png`, `p390vn-04-menu-products.png`.
8. **Japanese loses its three groups.** The gap between サポート (Support) and ログイン (Log in) is
   24px at 1280 and 30px at 1101, the same as between links, while the left side has 150–200px of
   empty paper. The account group reads as two more links. `jp1280-01-top-bar.png`,
   `jp1101-01-top-bar.png`, `zoom/lang-bars.png`.
9. **"Sign up" is a dead button that looks alive.** It is disabled (no link yet), but it has full
   ink, the normal cursor and no hover. A visitor clicks and nothing happens. (Measured: disabled,
   cursor default, opacity 1.)
10. **The Science pictures do not match.** A small photo print (115px wide), a heavy dark cell, a
    pale grey sketch and a heavy inkstone. The row reads as four unrelated pictures, and Dr. Liu,
    the most important one, is the smallest. `d1536-04-science.png`.
11. **The bottles stand on a grey rod.** The painted ground is a real stroke squashed to 16px tall
    and 1136px wide, so it becomes a flat grey bar like a shelf, and the bottles' pools vanish.
    `zoom/d1536-products-bottles-x2.png`, `zoom/asset-brush-5.png` (the stroke before squashing).
12. **Uneven name wrapping.** "Advanced OPC Formula" breaks onto two lines at 1280 and 1101 while
    the others stay on one, so its focus line drops below its neighbours'. In Vietnamese at 1101,
    two Science names wrap and two do not. `d1280-03-products.png`, `vn1101-03-science.png`.
13. **The tablet menu has a hollow.** With a part unfolded at 834x1112, there are about 200px of
    empty paper between Support and Log in, and no crane. `t834-05-menu-science.png`.
14. **The left pair is heavier than the right.** Products ▾ Science ▾ spans 241px, About Support
    170px. From the mark's centre the line reaches 355px left and 284px right, so the whole line
    looks shifted left of the mark. `d1536-01-top-bar.png`.
15. **The mark fills the small bar edge to edge.** Scrolled at 1536 the leaf is about 10px from the
    top and the letters about 11px above the rule. `zoom/d1536-scrolled-centre-x2.png`.
16. **Small things.** The mark's focus ring cuts through its leaf (`d1536-07-tab05-BiGHhome.png`).
    The language focus ring leaves the globe outside (`d1536-07-tab02-Chooselanguage.png`). The
    menu's crane disappears instantly when Products unfolds, no fade (`motion-phone-fold.png`).
    The short marks between menu lines read as tildes at phone size (`p390-03-menu.png`). In
    Vietnamese on the phone, "Khám phá sản phẩm của chúng tôi." wraps and its arrow floats alone at
    the far right (`p390vn-04-menu-products.png`).

---

## 4. Craft notes from the references

Screenshots at 1440 wide and on the phone, in `refs/`. Aesop blocked automation, and Byredo and
Ippodo covered their menus with pop-ups, so only their bars were usable.

- **Timeline** (`timeline-1440-menu-Shop.png`, `timeline-1440-menu-Science.png`). A big list on
  the left in about 36px type, and pictures with captions and arrows on the right. The big list is
  the real target and the pictures support it. The current section is marked by an underline.
  The header hides while you read down (`timeline-1440-scrolled.png`). Its tiny letter-spaced
  capitals are the part Mo rejected.
- **Seed** (`seed-1440-menu-Shop.png`, `seed-390-menu.png`). Products are rows: a picture on the
  left, the name in large type on the right. On the phone every product is fully visible. Nothing
  is cut off as a swipe hint.
- **Ippodo** (`ippodo-1440-top-clean.png`). Five links spread evenly across the full width in a
  calm serif at a readable size. The top band and the painting both have a hand-torn paper edge.
  So the torn edge is a proven move for a crafted tea brand, and ours is better made.
- **Byredo** (`byredo-1440-top.png`). The thinnest utility line (Menu left, Cart right) over a
  huge centred wordmark. It is the closest cousin of "Inscription", and it shows the risk:
  everything except the mark is tiny. We must not drift that way.
- **Kinto** (`kinto-1440-top.png`). Tiny capitals in one line. An example of what not to do for
  older visitors.

What to borrow in spirit: big words as the main targets inside a drop-down (Timeline); products as
rows on the phone (Seed); one honest edge (Ippodo); a mark that is the title (Byredo), without
shrinking everything else.

What not to borrow: hiding the bar on scroll. It is common (Timeline, Seed), but it confuses older
visitors who look up for the menu and find it gone.

---

## 5. The 10 rounds

Each round builds on the last. Biggest visible wins first. Every round ends with screenshots on
the production build (`npm run build` then `next start` on :3028), looked at full size, plus
`scripts/qa/qa_nav.py` and, where the round touches the page, `scripts/qa/qa_home_ink.py`.
Files below are under `src/components/home-v2/nav/` unless a path is given.

Three of the rounds carry genuinely new ideas, marked **New idea**: round 3 (the rule parts for
the mark and is written by the scroll), round 4 (the products showroom), round 6 (the current page
inked with a real brush stroke). Round 7 (the menu ends on the finale) and round 9 (the title
settles with the scroll) are new behaviours too.

### Round 1. A solid bar with a clean edge

**Goal:** once the page moves, the bar hides everything behind it, and nothing touches its rule.

Changes (`nav-inscription.module.css`):

- `.root[data-ground="solid"] .ground`: opacity `0.93` → `1`.
- Let the paper run on past the rule, then fade: ground height `calc(var(--h) + 14px)`, mask
  `linear-gradient(#000 calc(100% - 14px), transparent)`. So a line of text at the bar's edge is
  covered by paper, never crossed by ink.
- Give the mark room in the small bar: `--small: clamp(74px, 5.3vw, 82px)`, and in the small state
  lower `.left, .right` margin-top from `0.134` to about `0.1` of the mark, so the mark's letters
  stand at least 16px above the rule.

Check (screenshots `d1920-05-scrolled*.png`, `d1536-05-scrolled*.png`, `d1280-*`, `d1101-*`,
`p390-02-scrolled.png`, `t768-02-scrolled.png`, retaken):

- No letter of the page is visible above the rule at any of the three scroll depths, on any size.
  A pixel test: inside the bar band, away from the bar's own words, nothing darker than the paper
  by more than 6 levels.
- On the tablet, "Explore cellular health" is no longer crossed. No page glyph touches the rule's
  ink anywhere.
- The mark's letters at least 16px above the rule at 1536 (measure from the crop).

Risk: low. The bar may feel a touch heavier. Check that the fade below the rule still lets
paintings run up softly to the edge (the cell at 1536 and 1920).

### Round 2. No boxes, no blanks, no sideways arrows

**Goal:** opening and switching drop-downs never shows a white box, an empty scroll, or an arrow
pointing the wrong way.

Changes (`nav-inscription.module.css`):

- Move the settle animation from `.frame` to the elements that blend: `.painting` and `.mat`.
  `.frame` gets no animation, so it never isolates the multiply.
- A true cross-dissolve: the incoming panel gets `z-index: 1` and fades in over 0.4s with no
  delay. The outgoing panel stays fully visible underneath and hides only after 0.45s
  (visibility delay). The scroll is never empty.
- Chevrons flip instead of turning: replace `rotate: 180deg` with `scale: 1 -1` over 0.4s, so a
  chevron passes through a flat line, never a sideways "<".
- Only the open button keeps its underline during a switch (the leaving one drops its line at
  once).

Check:

- Film Science opening at real speed (the method in `motion-science-flash-realtime.png`): at
  300, 600, 900 and 1200ms the corner pixels of the three painting frames are within 4 levels of
  the scroll's paper.
- Slowed switch strip (`motion-switch-science.png` retaken): every frame shows one panel at
  least 60% visible; no frame shows a sideways chevron; only one word underlined.

Risk: low.

### Round 3. A real brush rule that parts for the mark (New idea)

**Goal:** the scrolled bar's edge reads at once as ink brushwork, and it frames the mark like a
title on a scroll.

The idea: two real painted strokes, not one machine-made bar. One runs from the left edge of the
column toward the mark, one from the right edge toward it (the left one mirrored). Each lands
loaded at its outer end and dries out into flying-white as it nears the mark, lifting off about
28px before the mark's edge. The mark stands in the gap, the way a title interrupts the line
under it. They are drawn by the reader's scroll (from both outer ends inward), the same way the
page's own brush line draws as you read, instead of a timed left-to-right sweep that looks like a
loading bar.

New asset (GPT Image 2.5 via the Higgsfield API, about $0.05 a picture; allow 2 tries, $0.10).
Landscape, the widest size the model offers. Prompt:

> Four very long, thin horizontal brush lines of black sumi ink on plain white paper, stacked
> with wide white space between them, each running almost the full width of the picture. Each
> is one light, quick stroke from a fine round calligraphy brush held nearly upright: it lands
> with a small loaded press at the left, travels right thin and even with a faint natural waver,
> and dries out over its last third into broken flying-white streaks, lifting off to nothing at
> the right end. Lightly loaded, about as thick as a pencil line in the middle. Ragged
> paper-tooth edges, a faint bleed into the fibres. Pure white background, no text, no seal, no
> signature, no shadows, no paper texture, flat even lighting, photographed straight from above,
> high contrast, crisp detail.

Save the original in `reference/nav/originals/` and the prompt in `reference/nav/prompts/`.
Cut the best line with the alpha method in `reference/nav/make_inscription_assets.py` into
`public/images/home-v2/nav/inscription/rule-half.webp` (new filename, so no stale cache).

Changes (`nav-inscription.tsx`, `.module.css`):

- Replace `<span className={styles.rule}>` with two spans, `ruleLeft` and `ruleRight`
  (`scale: -1 1` on the right). Each spans from the column edge to `50% - var(--mark)/2 - 28px`.
- Height so the stroke's body is 2–4px at 1536 (lighter than today's 7px); opacity about 0.75.
- Scroll-drawn where supported: `@supports (animation-timeline: scroll())` reveal each half with
  `clip-path` from its outer end, `animation-timeline: scroll(root)`, range about 60px to 280px.
  Without support: the current timed reveal, but from both outer ends at once, over 1.4s.
- Reduced motion: fully drawn.

Check:

- `zoom/` crop of the scrolled bar at 2x (1536, 1280, phone): bristle texture visible, no round
  blob, no rectangular dashes. Gap left and right of the mark equal within 2px.
- Scroll strip at 0, 60, 120, 180, 240, 300px: the two lines grow from the outer ends toward the
  mark with the scroll. No frame looks like a progress bar.
- Show Mo two crops side by side: one continuous painted rule, and the parted pair. She picks.

Risk: medium. A parted line can read as broken. The taper into dry streaks toward the mark is
what makes it read as on purpose; if it still reads broken at first glance, keep one continuous
real stroke (still a big win over today's).

### Round 4. Products: a calmer, bigger showroom (New idea)

**Goal:** the Products scroll is something a 62-year-old can read from the sofa, and it looks like
the homepage's showroom, not a shop strip.

Build two variants on a branch and let Mo pick by looking:

- **4A, the row, done properly.** Keep the five in a centred row. Remove the squashed grey rod.
  Each bottle stands on its own pool and contact pool, as on the homepage (`pool.webp`,
  `pool-foot.webp`, gathered to about 0.55 opacity). Stands larger: `--stand: clamp(180px, 13vw,
220px)`. Names 21px, focus lines 17px. Names reserve two lines (a grid row of fixed height), so
  every focus line starts on the same line even when "Advanced OPC Formula" wraps.
- **4B, the showroom (Timeline's pattern in our language).** The scroll holds two parts. On the
  left, the five names in the headline voice (28–32px), each with its focus line (17px Ink Grey)
  under it, 72px apart: these are the big targets. On the right, the shown product's bottle large
  (about 300px tall at 1536) on its gathered pool, with "Discover NuriCell →" under it. Pointing at
  a name, or reaching it by keyboard, shows that bottle (cross-fade 0.5s, pool gathers 0.9s), the
  same behaviour as the homepage picker. Clicking a name goes to its page. NuriCell is shown first.
  "Explore our products." sits under the list. This breaks the scroll's centred symmetry on
  purpose: the bar stays centred, the scroll reads like a page.

No new assets (product PNGs in `public/images/products/`, the two pool paintings).

Check:

- `d1536-03-products.png`, `d1280-*`, `d1101-*`, `d1366x657-products.png` retaken for both
  variants: names at least 21px (4A) or 28px (4B); no name or focus line misaligned with its
  neighbours by more than 2px; the scroll ends above the window's foot at 1366x657.
- 4B only: Tab reaches every name; the shown bottle follows focus; touch on a laptop screen opens
  the page on the first tap (no preview-only tap).

Risk: 4B is the bigger change and needs Mo's eye. A preview that changes under the pointer can
confuse some visitors; that is why the names themselves are the links, and the picture only
follows.

### Round 5. Science: four pictures of one weight

**Goal:** the four Science parts read as one set, and Dr. Liu is no longer the smallest.

Changes:

- Same height for all four pictures: frame `clamp(170px, 12.5vw, 200px)`.
- Dr. Liu's print fills that height on its mat (today it is about 70% of the frame).
- Each picture stands in a pale ink halo (reuse `public/images/home-v2/ink/halo.webp`, multiplied,
  about 0.35), the same treatment as his print on the homepage. The halo gives the pale reading
  still life a body and quiets the heavy ones.
- The reading still life: first try a contrast lift on the existing `story-reading-v2.webp`
  (for example `filter: contrast(1.25) brightness(0.96)`). Only if it still reads pale, generate
  a denser plate (GPT Image 2.5, 1–3 tries, up to $0.15): "A small still life in sumi ink wash on
  plain white paper: an open book with a pair of reading glasses on it and a small tea cup
  beside it, painted with confident dark strokes and pale washes, the same weight as a bold ink
  painting of an inkstone, no background, no text, no seal, no shadows, flat even lighting,
  photographed from above at a slight angle." Cut it out like the other plates (paper divided
  out) into a new filename.
- Names in a fixed two-line row, captions in a fixed two-line row, so all four align.

Check:

- `d1536-04-science.png`, `d1101-04-science.png`, `vn1101-03-science.png` retaken: names on one
  baseline within 1px; captions start on one line; mean ink of each picture's frame within ±25%
  of the others (measure in the crop).
- Real-speed film from round 2 still clean (no boxes).

Risk: low to medium. The halo must stay pale enough not to read as a grey disc. Look at it at 1920.

### Round 6. The current page, inked (New idea)

**Goal:** on every page other than home, the bar shows where you are with a real brush mark, and
the bar's details feel hand-made.

Context: Mo picked the site-wide ink restyle ("A. Full match"), so this bar will soon sit on the
product pages, Science and About. Today the current page gets the same 2px CSS line as hover.

Changes:

- The current page's word gets a short painted stroke under it, cut from the existing real
  strokes (`reference/nav/originals/gpt25-brush-strokes.png`, one of the short ones), about 0.9
  times the word's width, 8–9px tall, 85% ink, laid from the left over 0.9s when the page opens.
  New asset file, no generation needed.
- Hover stays a fine ink line (1.5px), drawn from the middle (0.5s). The open drop-down's button
  keeps a 2px line. So: fine line = "you are pointing", brush stroke = "you are here".
- Desktop chevrons: test them off. Timeline and Seed have none, and without them the two pairs
  balance (left 199px, right 170px, instead of 241 and 170). The scroll still opens on hover,
  click and Enter, and screen readers keep `aria-expanded`. If Mo prefers them, keep them at 16px
  with a 1.75 stroke.
- Wire `current` from each page that adopts the bar.

Check:

- Screenshots of the bar on the About page and a product page (once they use it) at 1536 and
  1101: the stroke sits centred under its word, never touching the chevron or the next word.
- Two crops of the home bar for Mo: chevrons on and off.

Risk: low. A brush mark can look like a smudge if too wide; keep it shorter than the word.

### Round 7. The phone menu ends on the finale (new behaviour)

**Goal:** on a phone, every product is fully visible, and the menu ends with the page's own last
picture: the crane at rest on its brush ground.

Changes:

- Products unfold as five rows (Seed's pattern, Mo's LIKE): the bottle on its pool at the left
  (stand 76px), the name (20px) and focus line (16px) at the right, rows about 92px tall, in a
  centred column about 320px wide. No sideways scrolling, nothing cut off.
- Science unfolds as four rows the same way: its small picture (56px; Dr. Liu's print, the cell,
  the reading still life, the inkstone) and its name. The phone then shows what the desktop
  shows.
- The menu's foot: the crane at rest (`crane-rest-v2.webp`) standing on one short loaded brush
  stroke (cut from `gpt25-brush-strokes.png`), with Log in and Sign up under it. This is the
  footer's finale in miniature: the menu ends where the page ends.
- When a part unfolds, the crane fades and sinks away over 0.5s instead of vanishing.
- Tablet (700px and wider): keep the five in a row (they fit), and show the crane in the space
  under Support whenever there is room (fixes the 200px hollow).
- The marks between lines: a straighter short stroke (72x10), so they read as brush, not as "~".
- The Vietnamese "Khám phá sản phẩm của chúng tôi. →": keep the arrow with the last word
  (`white-space: nowrap` on the last word plus the arrow, `text-wrap: balance`).

Check:

- `p390-04-menu-products.png`, `p390vn-*`, `p390jp-*` retaken: all five names fully visible, no
  clipped word anywhere, no horizontal scroll inside the menu.
- `t834-05-menu-science.png`, `t768-*`: no empty band taller than 120px between Support and the
  foot.
- Frame strip of the fold (like `motion-phone-fold.png`): the crane fades, never pops.

Risk: medium. Rows make the Products part taller; on a 390x844 phone the menu will scroll. That
is fine if the top of the list shows at once. Check on 360x640 as well.

### Round 8. Long languages keep their three groups

**Goal:** in Japanese and Vietnamese the bar still reads as language | two links, mark, two links |
account, at every width.

Changes (the 1101–1400px language block in `.module.css`):

- A wider gap between the last link and the account group than between links: at least
  `max(44px, 1.6 * var(--gap))`. Mirror it on the left (language to the first link).
- Pay for it where it costs least: at 1101–1300px in Japanese and Vietnamese, Sign up becomes a
  text link with its 2px line (no pill), which frees about 32px.
- If it still does not fit at 1101 in Japanese, raise the menu breakpoint for Japanese only to
  1180px (the phone/tablet menu is a good bar, not a fallback).

Check:

- `jp1101-01-top-bar.png`, `jp1280-*`, `jp1536-*`, `vn*` retaken: Support-to-Log in gap at least
  1.5 times the gap between links; nothing past the window edge; nothing under 18px.
- `qa_nav.py` language checks extended to 1536 and to the group gaps.

Risk: low.

### Round 9. The title settles with the scroll (new behaviour)

**Goal:** the change from title (over the painting) to bar (over the page) is tied to the reader's
hand, not a timed snap at 48px.

Changes:

- Where scroll-driven animation is supported (`@supports (animation-timeline: scroll())`): the
  mark's width goes from `--mark-tall` to `--mark-small`, the bar from tall to small, and the
  paper from clear to full, all across the first 0–220px of scroll. The rule from round 3 draws
  across about 60–280px. One continuous gesture.
- Fallback (no support): today's timed change, but at the breath's pace (0.9s, the site's ease).
- The wash under an open scroll: 22% → 30%, so a page headline under the torn edge recedes and
  no longer competes (`d1280-03-products.png` problem).
- The scroll's leading edge: if the panel's foot falls across a headline, that is acceptable once
  the wash is stronger; do not try to measure the page.

Check:

- Scroll strip at 0, 40, 80, 120, 160, 200, 240px (1536 and 1280): the mark's width changes
  smoothly and only one way; in no frame do the crane's wings sit behind link words on less than
  60% paper (today's first frame of `motion-scroll-settle.png` has the wings behind "Products").
- Scroll back up: the same frames in reverse, no jump.
- Check in the browsers Mo's visitors use (Chrome, Safari, Edge); the fallback must look
  finished on its own.

Risk: medium. Lenis smooth scrolling is on the page; scroll-driven timelines follow the real scroll
position, so it should work, but this must be filmed, not assumed.

### Round 10. Nothing dead, nothing small, then the full audit

**Goal:** every control says what it does, and the whole bar passes a visitor's look at every size.

Changes:

- "Sign up": ask Mo. Either give it its real link, or until then hide it, or make it open a short
  sheet ("Sign up opens soon"). Never a button that looks alive and does nothing.
- The mark's focus ring wraps the leaf (pad the link at the top, `outline-offset` 4px). The
  language focus ring includes the globe (ring the label, not the select).
- Product focus lines and Science captions to 17px in the scroll (16px today).
- Update `DESIGN.md` ("Navigation" and "Menu") to describe what shipped, and `qa_nav.py`:
  - a ghost-text check (round 1),
  - a no-white-box check at 600ms after Science opens (round 2),
  - a rule-shape check (two halves, symmetric about the mark) (round 3),
  - name-alignment checks (rounds 4–5),
  - the phone "nothing clipped" check (round 7),
  - the language group-gap check (round 8).
- Run `qa_nav.py` and `qa_home_ink.py` on the production build, then retake this review's full set
  of pictures and look at every one at full size.

Check: all 44 existing nav checks plus the new ones pass; `qa_home_ink.py` passes; the defects
list in section 3 is walked one by one with a new picture for each.

Risk: low.

---

## 6. Budget

| Round   | Picture                                                                              | Cost              |
| ------- | ------------------------------------------------------------------------------------ | ----------------- |
| 3       | Sheet of long thin brush lines (2 tries)                                             | $0.10             |
| 5       | Denser reading still life, only if the contrast lift fails (up to 3 tries)           | up to $0.15       |
| 6, 7    | Short strokes and the ground stroke: cut from the existing `gpt25-brush-strokes.png` | $0                |
| 4, 5, 7 | Pools, halo, crane at rest, product photos: existing                                 | $0                |
|         | **Planned total**                                                                    | **$0.25** (of $5) |

The rest stays in reserve for retries Mo asks for.

---

## 7. Rules every round keeps

No gold on any UI element. No red, seals, drop shadows (Dr. Liu's photo mount is the one
sanctioned exception), gradient fills, glassy cards or tiny text. Sentence case. Motion on the
site's ease; reduced motion is still. The centred mark stays. Navigation words at least 18px (20px
at 1536), targets at least 48px. Judge on the production build, at full size, scrolled like a
visitor.
