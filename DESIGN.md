---
name: BiGH — Ink & Gold
description: The long life you want and the cell that powers it, painted in one breath of ink on rice paper, with a single gold leaf for energy.
colors:
  gold-leaf: "#c49a3a"
  sumi-ink: "#0c0b0a"
  brush-ink: "#141311"
  ink-grey: "#514e48"
  rice-paper: "#f8f3ea"
  mount-paper: "#fbf9f4"
  hairline: "rgba(28, 27, 25, 0.16)"
  hairline-strong: "rgba(28, 27, 25, 0.28)"
  pill-hover: "#3a3833"
  selection-gold: "#ead9ad"
typography:
  display-opening:
    fontFamily: "Switzer, DM Sans, Arial, sans-serif"
    fontSize: "calc(99 * min(100vw / 1536, 100svh / 1000))"
    fontWeight: 500
    lineHeight: 0.905
    letterSpacing: "-0.03em"
  display:
    fontFamily: "Switzer, DM Sans, Arial, sans-serif"
    fontSize: "clamp(40px, 3.9vw, 62px)"
    fontWeight: 500
    lineHeight: 1.04
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Switzer, DM Sans, Arial, sans-serif"
    fontSize: "clamp(30px, 2.8vw, 42px)"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-0.022em"
  body:
    fontFamily: "Switzer, DM Sans, Arial, Helvetica, sans-serif"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Switzer, DM Sans, Arial, Helvetica, sans-serif"
    fontSize: "19px"
    fontWeight: 450
    lineHeight: 1.3
  station:
    fontFamily: "Switzer, DM Sans, Arial, Helvetica, sans-serif"
    fontSize: "17px"
    fontWeight: 450
    lineHeight: 1.3
  caption:
    fontFamily: "Switzer, DM Sans, Arial, Helvetica, sans-serif"
    fontSize: "15px"
    fontWeight: 450
    lineHeight: 1.4
rounded:
  pill: "999px"
spacing:
  gutter: "clamp(22px, 7.7vw, 132px)"
  wide: "1300px"
  section: "clamp(64px, 7vw, 112px)"
components:
  button-primary:
    backgroundColor: "{colors.sumi-ink}"
    textColor: "{colors.rice-paper}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0 28px"
    height: "54px"
  button-primary-hover:
    backgroundColor: "{colors.pill-hover}"
    textColor: "{colors.rice-paper}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.sumi-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0 28px"
    height: "54px"
  filter-chip:
    backgroundColor: "transparent"
    textColor: "{colors.sumi-ink}"
    rounded: "{rounded.pill}"
    padding: "0 18px"
    height: "48px"
  filter-chip-selected:
    backgroundColor: "{colors.sumi-ink}"
    textColor: "{colors.rice-paper}"
  honesty-tag:
    backgroundColor: "transparent"
    textColor: "{colors.ink-grey}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: "0 12px"
    height: "30px"
---

# Design System: BiGH — Ink & Gold

## Overview

**Creative North Star: "One Breath of Ink"**

The page is an East Asian ink-wash painting on warm rice paper. Paintings, paper, type and one continuous brush line carry everything; there are no cards, no gradient fills, no red and no seals. A single gold leaf appears only where energy is meant: the sun, and the two folds inside the mitochondrion where energy is made. Switzer sets the words large and calm, in sentence case, beside paintings that bloom into the paper as they arrive.

The signature is the brush line. It leaves the crane's trailing legs (or the cell's foot), draws itself down the page as the visitor reads, and pins each section's label to itself with a fine leader line, so the page reads as one timeline painted in one stroke. Density is low: one idea per screen, generous paper, nothing boxed.

Every motion breathes at the same slow pace (`--breath: 2.4s`, ease `cubic-bezier(0.22, 0.61, 0.36, 1)`). With reduced motion the page is complete and still from the first frame, the whole brush line already painted.

**Key Characteristics:**
- Rice paper with real fibre (a tiled 800px paper texture over the paper colour), never flat white.
- Sumi ink and ink-wash greys for everything; gold leaf only inside paintings, only for energy.
- Paintings have their paper divided out and multiply onto the page's own paper.
- One continuous calligraphic brush line on desktop; stations pinned to it by hairline leaders.
- Switzer at 400/450/500, sentence case, never letter-spaced capitals.
- Large type and 48px+ targets for older readers.
- Honesty labels on every illustration and sample, set quietly but never hidden.

## Colors

A near-monochrome of sumi ink on warm paper, with one gold that belongs to the paintings, not the interface.

### Primary
- **Gold Leaf** (gold-leaf): the energy colour. It lives in the painted plates (the gold-leaf sun, the gold folds of the mitochondrion, the low sun of the closing landscape) and in nothing else. No button, rule, link or label is gold.

### Neutral
- **Sumi Ink** (sumi-ink): headlines, body ink for key lines, the solid pill, active underlines, focus rings, leader lines (at 62% mix).
- **Brush Ink** (brush-ink): the brush line's own ink, a touch warmer and lighter than type so stroke and words read as different materials.
- **Ink Grey** (ink-grey): body copy, captions, idle tab and product names, honesty tags. About 7.6:1 on rice paper.
- **Rice Paper** (rice-paper): the page, under the paper-fibre texture; also the text colour on solid ink.
- **Mount Paper** (mount-paper): the paper mat around Dr. Liu's real photograph, the only lighter-than-page surface.
- **Hairline** (hairline) and **Strong Hairline** (hairline-strong): rules between numbered lines and tabs; outlined chips and text-link underlines.
- **Pill Hover** (pill-hover): the solid pill's hover, ink thinned with water.
- **Selection Gold** (selection-gold): text selection only, a pale wash of the gold.

### Named Rules
**The One Gold Leaf Rule.** Gold is energy and only appears painted into the plates. If you are reaching for gold on a UI element, use sumi ink instead.

**The No Red, No Seal Rule.** The genre's red seal is refused on purpose: no red anywhere, no stamps, no chops. This is a confirmed brand departure from the ink tradition, not an oversight.

## Typography

**Display Font:** Switzer (with DM Sans, Arial)
**Body Font:** Switzer (with DM Sans, Arial, Helvetica)

**Character:** One pinned brand face (Switzer, site-wide by brand commitment) used in three weights. Headlines are large, tight and calm at 500; reading text and controls sit at 400 and 450, which keeps labels firm without bolding.

### Hierarchy
- **Opening display** (500, 99 comp px scaled by the opening unit, 0.905): the three-line opening headline only. Phones: clamp(40px, 12vw, 56px) at 0.96.
- **Display** (500, clamp(40px, 3.9vw, 62px), 1.04, -0.03em, balanced): every section headline.
- **Headline** (500, clamp(30px, 2.8vw, 42px), 1.12): the chosen product's headline; sample-story quotes run larger, clamp(34px, 3.4vw, 54px) at 1.08.
- **Body** (400, 19px, 1.6, Ink Grey): reading text. 18px on phones in the opening.
- **Label** (450, 19px, 1.3): pills, text links, small headings. Tabs run 21px, product names 20px.
- **Station** (450, 17px, 1.3, Sumi Ink): section labels on the brush line.
- **Caption** (450, 15px, 1.4, Ink Grey): figure captions and honesty tags; the floor for any text.

### Named Rules
**The Sentence Case Rule.** Labels, stations, captions, footer headings: sentence case at normal tracking. Never small letter-spaced capitals.

**The CJK Room Rule.** Korean, Japanese and Chinese headlines take line-height 1.22, tracking -0.01em, `word-break: keep-all`; the opening headline drops to 86 comp px so it stays clear of the crane.

## Layout

Content sits in a 1300px measure inside a fluid gutter (clamp(22px, 7.7vw, 132px); the cell opening uses clamp(22px, 5.7vw, 100px)). Sections breathe on clamp-based vertical padding of roughly 64–140px; nothing is boxed, so space and hairlines do the separating.

The openings are measured from their approved 1536×1000 comps. One unit (`min(100vw / 1536, opening height / 1000)`) scales every painting and line of type so the comp holds from 1280 to 1600 wide and on short windows, while text never drops below reading size. The opening is one viewport tall (100svh, 680–1180px), and never much taller than the comp at its width (76vw: a tablet held upright gets a compact opening, with the next block in the same window). Above 1536px wide the page's column centres; the opening's words stay on its left edge (under the logo), and the crane, the sun and the stroke move in with them on a frame that stops stretching at 1812px.

Breakpoints: 900px (two-column blocks collapse, stations leave the margin), 720px (phone layouts: the opening becomes a stacked picture then words, bottles become a swipeable snap row), 560px (product grid to two columns where the row is not swiping).

### Named Rules
**The Desktop Line Rule.** The page-long brush line exists only where the blocks are two columns (900px and wider): it is routed through the gaps between the columns, and on one column it would run through the words (October 4; it was 720px before, which let it cross the headlines on a tablet held upright). On phones the gutter cannot hold it without crowding the words, so each opening keeps only its own short stroke inside the opening (721–899px: the comp's flight stroke), and stations sit in the flow under their headings with a 22px leader. The three standards' rules and the closing stroke under the footer's promise are on every screen.

## Elevation & Depth

Flat by material, not by shadow. Depth comes from layers of ink: paintings and the brush line multiply onto the paper, the brush layer sits under the paintings and words, and mist dissolves through masks at painting edges so the page continues without a seam.

### Shadow Vocabulary
- **Photo mount** (`box-shadow: 0 22px 44px -22px rgba(12, 11, 10, 0.42), 0 3px 8px rgba(12, 11, 10, 0.1)`): only under the paper mat that holds Dr. Liu's real photograph, so a real print reads as an object on the paper.

### Named Rules
**The Multiply Rule.** Every ink painting ships with its paper divided out and is placed with `mix-blend-mode: multiply`, so the page's own rice paper shows through it. Never place an ink plate on a box or with its own paper colour.

**The Ink Pool Rule.** Products never sit on cards or drop shadows. Each bottle stands in its own ink-wash pool (the painted pool, foreshortened, about 60% of the stand's width, its core just under the base) plus a small dense contact pool (56%) where the base meets the paper, both multiplied. The stand is 146% of its column, up to 340px, so the bottles have presence. A pool is a pale wash (50%) until its bottle is chosen; then the ink gathers under it (92%, 1.1×) over 0.9s.

## Shapes

Form comes from brush and paper, not containers. The only constructed shape is the fully round pill (999px) for buttons, filter chips and honesty tags. Rules are hairlines (1px); active states are 2px ink underlines that grow from zero; leaders are 1px ink lines. Paintings have no frames: their edges dissolve.

## Components

### Buttons
Quiet and sure: a solid sumi pill and its outlined twin.
- **Shape:** fully round pill (999px), 1.5px ink border, min-height 54px (opening: max(48px, 52 comp px)).
- **Primary:** Sumi Ink fill, Rice Paper text, 20px/450, 0 28px padding, trailing arrow.
- **Hover / Focus:** fill eases to Pill Hover over 0.5s; the arrow slides 3px. Focus: 2px ink outline, 4px offset.
- **Ghost:** transparent with the ink border. With a mouse it fills the way a drop of ink spreads in water: a circle of ink grows from the point where the pointer came in (0.75s) and the words turn to paper. Touch keeps a 7% ink wash.

### Text Links
Ink text, 19px/450, with a 1px Strong Hairline underline 8px below that darkens to ink on hover; min-height 48px.

### Chips
- **Style:** filter chips are outlined pills (1px Strong Hairline, 48px tall, 18px/450) with a tabular count.
- **State:** hover darkens the border to ink; selected fills with Sumi Ink and Rice Paper text.

### Tabs
Text tabs on a hairline base, 21px/450, Ink Grey idle; selected turns ink and a 2px ink underline grows from the left over 0.7s.

### Navigation
The shared header starts clear over the opening, so the painting runs to the top of the window, and turns to 93% paper with a hairline under it once the page has scrolled 48px; 80–90px tall; links clamp(18px, 1.302vw, 20px)/450 and never below 18px; no divider before Log in. With a mouse, a 2px ink underline draws from the left under the link you point at (0.5s); the current page keeps its own.

### Brush Line (signature)
One painted stroke, not a traced path: calligraphic width, ragged paper-tooth edges, reloads about every thousand pixels so each stroke lands loaded and tapers, with dry-brush streaks as the ink runs out. It is routed through waypoints pinned to each block's own anchors and re-measured on every layout change. Width at the 1536 comp runs from under 1px to 5.6px, scaled by width/1536 clamped to 0.62–1.15; the brush can lift off the paper. It draws as the reader scrolls (reaching about 78% down the window) and once painted the ink stays. It lifts off in the closing painting's sky, touches down three times as a short, lightly loaded rule over each of the three standards (they have no hairline of their own), travels on to the footer, reloads, and ends as one loaded stroke (about twice the page's usual width) under the footer's promise and the crane at rest beside it: the line that left the crane in flight comes to rest as the ground the crane stands on, under "Stay sharp. Live fully." Reduced motion: the full line from the first frame.

### Stations
A station is a short sentence-case label (17px/450, Sumi Ink) pinned to the brush line by a 1px leader at 62% ink (28–34px long on desktop). It sits in the margin beside its heading with the leader pointing at the line, and appears only when the brush reaches it: the leader draws out over 0.7s, the words fade in over 0.9s. A station exists only where the line passes and carries words that already exist; it is not a heading decoration.

### Cell Labels
In the cell opening, three hairline labels (max(16px, 20 comp px)/450) sit at the ends of leader lines drawn into the painting itself.

### Closing
The footer's promise sets on two lines with the crane at rest standing beside it (ink, multiplied; 88–124px wide), both on the closing brush stroke. The crane opens the page in flight, flies home in the closing painting, and rests here.

### Honesty Labels
Every illustration says so: "Illustration" captions on painted stills (the three story still lifes and the brush on its inkstone beside Ask BiGH Science), "Illustrations" on the science stage, "Illustration, not a measurement" (16px/500, centred) under the age slider, "Illustrative view" on the cell figure, an outlined "Fictional sample" pill (30px, 15px, Ink Grey) in every story byline, and the research limit note. Caption size and Ink Grey, placed on or beside the image; never removed, never smaller than 15px.

### Motion
- **Ink bloom:** each painting spreads into the paper through an ink blot's soft mask, from 0% to 280% over 1.25 breaths, unblurring from 5px over one breath, with optional per-painting delay and origin. Opening paintings are marked waiting from the server so they bloom rather than flash.
- **Breathing:** the crane glides (4 breaths, alternate); the gold folds of the cell glow up to 55% (2 breaths, alternate). Both stop under reduced motion.
- **Settle:** panels enter over 0.9s by fading and rising 8–10px. State transitions run 0.5s; underline and leader growth 0.7s. The opening's words arrive the same way, like ink settling: each headline line, then the intro, then the pills rise 0.24em and sharpen from an 8px blur over 0.75 breaths, 0.14s apart.
- **Mist:** the opening's landscape is drawn on a canvas with two slow banks of mist drifting through it. Mist is bare paper, so it only takes ink away: the far, pale ridges dissolve and return while the near, dark pines hold. The canvas takes the still painting's place once it has bloomed (same pixels, same multiply) and the mist rises over two breaths. No WebGL, a software renderer or reduced motion: the still painting stays.
- **Light on leaf:** gold leaf is metal. A pale, warm band of light (screen) crosses each painting's leaf, held inside the leaf by that painting's own gold mask: every four breaths on the opening's sun; on the cell's two gold folds, the close view's folds and the closing sun it crosses as the painting travels up the window, so the leaf is lit when it is in front of you. This is light inside a painting, not a gradient fill on the interface.
- **Depth:** leaving the opening, the sun sinks behind the ridges and the mountains settle; with a mouse the sun leans a few pixels against the pointer.
- **Wingbeat:** the opening crane is the approved painting brought to life (a Kling loop from the still, cut out frame by frame like the still, shipped as an animated webp). It holds the glide pose, then beats its wings once, slowly, about every four breaths. It is fetched after the still has bloomed and opens on the still's pose, so the two change places unseen. Reduced motion keeps the still.
- **Arrival:** the cell in "Tiny power plants." settles as it comes into view: a tenth smaller and turned five degrees at first, at rest by the time it is centred (scroll-driven; still without it).
- **Flight:** the closing painting's two cranes are their own layer. As the painting rises into the window they fly up from the lower left to their painted place, toward the sun, and ride the air (3 breaths, alternate). Without scroll-driven animation they are simply there, as painted.

## Do's and Don'ts

### Do:
- **Do** set every surface on the rice paper with its fibre texture.
- **Do** multiply every ink painting onto the paper, with its own paper divided out.
- **Do** keep gold inside the paintings and only for energy.
- **Do** run every motion on the one breath (2.4s) and the one ease, and make the reduced-motion page complete and still.
- **Do** keep text at 15px or larger, navigation at 18px or larger, and targets at 48px or taller.
- **Do** label every illustration, sample and research limit in caption type.
- **Do** keep the page-long brush line on desktop only; phones keep the opening's own stroke.

### Don't:
- **Don't** use cards, boxed panels or gradient fills; space, hairlines and paintings separate content.
- **Don't** use red, seals or stamps.
- **Don't** put gold on buttons, rules, links or labels.
- **Don't** set labels in small letter-spaced capitals.
- **Don't** add drop shadows; the photo mount is the only one.
- **Don't** invent a station label to decorate a heading; stations exist only where the brush line passes.
