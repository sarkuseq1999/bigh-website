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
- **Headline** (500, clamp(30px, 2.8vw, 42px), 1.12): sheet titles and names; sample-story quotes are the story block's voice, set to balance its still life: clamp(40px, 4vw, 64px) at 1.08 on two columns (61px at 1536), clamp(34px, 4.4vw, 40px) on one. The chosen product's headline on the products stage is display voice, a touch under the section's own (clamp(40px, 3.7vw, 57px), 1.04), and breaks only between its sentences.
- **Body** (400, 19px, 1.6, Ink Grey): reading text. 18px on phones in the opening.
- **Label** (450, 19px, 1.3): pills, text links, small headings. Tabs run 21px, product names 20px.
- **Station** (450, 17px, 1.3, Sumi Ink): section labels on the brush line.
- **Caption** (450, 15px, 1.4, Ink Grey): figure captions and honesty tags; the floor for any text.

### Named Rules
**The Sentence Case Rule.** Labels, stations, captions, footer headings: sentence case at normal tracking. Never small letter-spaced capitals.

**The CJK Room Rule.** Korean, Japanese and Chinese headlines take line-height 1.22, tracking -0.01em, `word-break: keep-all`; the opening headline drops to 86 comp px so it stays clear of the crane.

**The Set Lines Rule.** Reading text is set with `text-wrap: pretty` from the page's root (no paragraph ends on one short word); headlines and short statements choose `balance`. A paragraph of reading text keeps a measure of about 30em (about 65 characters a line) however wide its column. An opening quotation mark hangs in the margin, so the first letter stands on the same edge as the lines under it. Text links and hover underlines are 1px, 8px below the baseline.

## Layout

Content sits in a 1300px measure inside a fluid gutter (clamp(22px, 7.7vw, 132px); the cell opening uses clamp(22px, 5.7vw, 100px)). Nothing is boxed, so space and hairlines do the separating, on the Rhythm Rule below.

The openings are measured from their approved 1536×1000 comps. One unit (`min(100vw / 1536, opening height / 1000)`) scales every painting and line of type so the comp holds from 1280 to 1600 wide and on short windows, while text never drops below reading size. The opening is one viewport tall (100svh, 680–1180px), and never much taller than the comp at its width (76vw: a tablet held upright gets a compact opening, with the next block in the same window). Above 1536px wide the page's column centres; the opening's words stay on its left edge (under the logo), and the crane, the sun and the stroke move in with them on a frame that stops stretching at 1812px.

Breakpoints: 900px (two-column blocks collapse, stations leave the margin), 720px (phone layouts: the opening becomes a stacked picture then words, the products' picker becomes a swipeable snap row).

### Named Rules
**The Rhythm Rule.** The page breathes on four measures of blank paper, counted from the last ink of one thing to the first ink of the next (round 6, October 4; at 1536, scaling with the width, about 6% less at 1440): about 215px of silence before a chapter (the scientists, the products, the purpose and the finale), 160px between the other blocks (the cell after the opening, the stories, the science, the research), about 110px between the parts of a block (Dr. Liu's record and what his work asks; the purpose's painting, its statement and its standards) and 70–100px inside a part (a heading and its body, the stage and the picker). The one exception is the pause: Ask BiGH Science, the end of the scientists block, is the page's one centred moment, its small painting centred with the headline (two lines, no word alone), words and button centred under it, about 175px of paper above it and the products' chapter silence below; the brush line passes it in the left margin, clear of the painting and the words. On a phone: 120px before a chapter, 104px between blocks, about 96px above the pause, 32–64px inside a block. On a short desktop window (860px tall or less) the footer's second tier draws in and the crane at rest stands at most a third of the window tall, and (round 10) on any window it also gives way to the footer's room (down to 150px), so the last screen shows the whole crane clear of the header (1280x720, 1366x657 and 1536x864 included).

**The Three Sizes Rule.** The middle of the page keeps a rhythm of scale, not one beat repeated: huge, large, small. Huge is the cell in "Tiny power plants.", the page's biggest painting after the opening: on two columns it starts in the column gap (its paper corner only, at most 80px in) and runs off the window's right edge, which falls at 78% of its width, past the gold folds (about 1085px wide at 1536, never past 1280px), and it runs 8% of its width into the block's padding above and below; on one column it runs off both edges of the screen (124vw, centred on its body). Large are Dr. Liu's print, the products' stage bottle, the science stage and the story still life; the still life ends at its column's edge and runs off the window's left edge, which falls at 14% of its width (about half the window, never past 860px), and on one column it runs to both edges of the screen; beside it the heading stands level with its top and the sample's words level with its base. Small is the inkstone over Ask BiGH Science (26vw, at most 400px; about 70vw on a phone), centred in the page's one pause; the contrast is the point. A painting that runs off the window is clipped by the page's root (`overflow-x: clip`), so nothing scrolls sideways; on a very wide window it stops growing and stays beside its words. Its label stays at its column's edge, inside the window. The brush line keeps to the gaps beside the big paintings: down between the cell and its words, then above the still life and down between it and its words, past the story's names.

**The Phone Rule.** A phone is a design of its own, not a squeezed desktop (round 5, October 4). The opening is a painting first: its picture about 46% of the window's height (never under 88% of its width, at most 480px), the crane's picture 96vw (the bird about 62% of the window, the full wingbeat picture on a 2x screen), the sun at the upper right, the two pills one over the other at the column's full width (54px). On one column the closing painting is framed for the window, since it cannot keep both the pine and the sun: it is set at 220% of the window (to 1500px) and moved until the sun's centre stands at 76% of the window, so the two cranes fly home to the gold sun over the mist, on their own flying layer, with the light on the leaf; its open sky lies under the statement. The stories open with their heading, then the still life, then the sample (no rule above it). The science topics sit on one line (17px, never under 15px) and the age slider takes no room until its topic. The scientists' record sets each figure and its words on one hairline across the column.

**The Desktop Line Rule.** The page-long brush line exists only where the blocks are two columns (900px and wider): it is routed through the gaps between the columns, and on one column it would run through the words (October 4; it was 720px before, which let it cross the headlines on a tablet held upright). On phones the gutter cannot hold it without crowding the words, so each opening keeps only its own short stroke inside the opening (721–899px: the comp's flight stroke), and stations sit in the flow under their headings with a 22px leader. The three standards' rules and the closing stroke under the footer's promise are on every screen.

## Elevation & Depth

Flat by material, not by shadow. Depth comes from layers of ink: paintings and the brush line multiply onto the paper, the brush layer sits under the paintings and words, and mist dissolves through masks at painting edges so the page continues without a seam.

### Shadow Vocabulary
- **Photo mount** (`box-shadow: 0 22px 44px -22px rgba(12, 11, 10, 0.42), 0 3px 8px rgba(12, 11, 10, 0.1)`): only under the paper mat that holds Dr. Liu's real photograph, so a real print reads as an object on the paper. The print is the scientists block's centre of gravity: on two columns the photograph is 24.75vw wide up to 380px (never past its own 512 pixels), 260px on a phone, on an ink halo about 1.84 times its width; his name under it at headline size (clamp(30px, 2.6vw, 42px), display weight) with role and field at 19px Ink Grey; the headline, intro and record sit beside the print's lower part, the record's last line on the mat's lower edge. The page's brush line runs down beside the mat, never under it.

### Named Rules
**The Multiply Rule.** Every ink painting ships with its paper divided out and is placed with `mix-blend-mode: multiply`, so the page's own rice paper shows through it. Never place an ink plate on a box or with its own paper colour.

**The Ink Pool Rule.** Products never sit on cards or drop shadows. Each bottle stands in its own ink-wash pool (the painted pool, foreshortened, about 60% of the stand's width, its core just under the base) plus a small dense contact pool (56%) where the base meets the paper, both multiplied; the pools scale with the stand.

**The Showroom Rule.** The products block is a stage, not a shelf. On two columns (the scientists' 5/7 columns and gap, so the brush line runs straight on down the same gap) the chosen bottle stands large at the left (its picture the column's width up to 490px: the bottle about 470px tall at 1536) in its gathered pool (92%, 1.1×), on the brush line, which reloads beside it and lays one stroke under it as its ground (and runs on, unbroken, under the picker's first two and down into the stories in one S); its words sit at the right (headline, focus, highlights, description, credit, Discover), held at the tallest product's height so nothing moves while you preview. NuriCell is chosen first. Under the stage the five stand small in a quiet picker row (about 136px stands, names under them at 18px; the chosen one has the 2px ink underline and the gathered pool, the rest a pale wash at 50%). Pointing at a picker bottle or reaching it with the keyboard previews it; click, tap or Enter chooses it. The stage bottle cross-fades in 0.5s (the new one over the last), its pool gathers again over 0.9s and the words settle. The arrival (round 10): as the stage comes into view the big bottle rises 10px onto its ground while its pool gathers from the pale wash and its contact shadow darkens (one breath), and as the picker's row comes into view its five bottles follow, rising 10px out of a paler ink, 70ms apart; out of view they wait visibly, never invisible, and a page opened with them in view does not wait. The big bottle and Discover go to the shown product's page; the picker only chooses. The headline sits at the left with its station on the line beside it and the intro under the station. One column: the big bottle (70vw on a phone), the picker straight under it (a swipeable snap row on a phone), then the words, so what you tap and what changes share the window. Reduced motion: every change is instant.

**The Scroll Story Rule.** "Make sense of the science." explains its science one idea per screen, as Timeline does (round 7, October 4). From 900px up, with motion, the block is about two windows tall: the headline and intro start it; the painting is pinned (sticky) in its column, centred in the window under the header, and the three topics follow one another down the words' column under the index, each standing alone with only the next heading peeking in at the foot of the window. The tabs stay at the top of the words as the index, pinned level with the painting's top; the current topic carries the 2px ink underline, and choosing one glides the page to it (about 1.2s, easing out), the topic chosen at once. As a topic's heading reaches the reading line (78% down the window, where the brush line draws), just as the last topic has dissolved, the painting blooms into that topic's state through the ink blot while the last one dissolves (0.6 breath); the age slider and its honesty line come with the third. The words are never gone and never without their heading. A topic leaving its place dissolves whole, with its heading (never a paragraph left without one), before its heading reaches the index, so nothing passes under it; the last topic ends level with the painting, so the index, the last topic and the painting leave together, without a jump. Where a topic is taller than the room under the index (a narrow window such as 1024x768) the block is the tabbed one instead (round 10), tried again when the window's width changes; only a change of the window's height while the story runs keeps the index where it is, nothing dissolving. From 900 to 1179px the index spreads its three topics across the words' column on one line (17-21px); on a short window the painting gives way so all of it, the slider and its honesty line stay in the window while pinned. The light crosses the close view's gold folds while its topic is read. The pinned painting is its own group, so the group multiplies onto the paper. The brush line keeps to the far margin beside the painting's column, top to bottom, and turns in only under it. Each topic keeps its own Explore pill and explainer. Phones and reduced motion keep the three tabs.

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
- **Style:** filter chips are outlined pills (1px Strong Hairline, 48px tall, 18px/450) with a tabular count; they sit on one line where they fit and break two and two where they do not (never one alone on a row).
- **State:** hover darkens the border to ink; selected fills with Sumi Ink and Rice Paper text.

### Tabs
Text tabs on a hairline base, 21px/450, Ink Grey idle; selected turns ink and a 2px ink underline grows from the left over 0.7s.

### Navigation
The shared header starts clear over the opening, so the painting runs to the top of the window, and turns to 93% paper with a hairline under it once the page has scrolled 48px; 80–90px tall; links clamp(18px, 1.302vw, 20px)/450 and never below 18px; no divider before Log in. With a mouse, a 2px ink underline draws from the left under the link you point at (0.5s); the current page keeps its own.

Log in, Sign up and the language picker are a component shared with the other pages; the homepage restyles them from its own stylesheet only (never the shared one): the navigation's weight, Sign up as the outlined pill (1.5px, 48px), an ink focus ring, the picker as wide as the language it shows. Where the browser lets a page draw a select's list, the languages open on a hairline sheet of the page's paper (48px lines, the chosen one ticked). Just above the menu's breakpoint (1101–1220px) Vietnamese and Japanese have no room for every link on one line, so the current page's own link steps aside there. The first Tab stop is "Skip to content" (the solid pill, over the logo), which puts focus at the page's words.

### Menu (1100px and narrower)
A full sheet of the page's paper under the bar, the page locked under it. One link to a line in the display voice (30px on phones, up to 44px on a tablet held upright; 64–96px lines on hairlines), the current page underlined in ink; Log in, Sign up and the language rest at the foot of the sheet (the language on its own line on phones). The sheet clears in 0.3s and each line settles 70ms after the one above; reduced motion: it is simply there. Its button comes before it in the page, so Tab goes from the button into the links; Escape closes it and hands focus back; tabbing out of it closes it.

### Sheets (everything the page opens)
Dr. Liu, Ask BiGH Science, Support and the three explainers open as one sheet: the page's own rice paper with its fibre, square paper corners, no shadow, up to 680px wide, laid on a wash of thinned ink (a warm grey, `rgb(96 91 83 / 0.64)`, nothing blurred). The wash spreads from the middle of the window through the paintings' ink-blot mask in one breath while the sheet settles (rising 10px over 0.9s); both leave in 0.3s; reduced motion: there at once, gone at once. The label (17px, Ink Grey) and the close button (the outlined pill's round twin, 48px) stay at the top while the words scroll under, with a hairline once they have moved. Inside: the page's own pieces and nothing boxed. Headline scale title, 19px Ink Grey reading text with key lines in ink, numbered lines on hairlines (as in "Tiny power plants."), questions on hairlines with the round toggle (as in the research list), the text link, and what is not ready yet said under a hairline with the outlined honesty tag ("In development"). Focus moves into the sheet, stays there, and returns to the button that opened it; the wheel scrolls the sheet, never the page under it.

### Brush Line (signature)
One painted stroke, not a traced path: calligraphic width, ragged paper-tooth edges, reloads where something begins (beside a station, under the big bottle, where the brush lands again: about every thousand pixels) so each stroke lands loaded at a place that means something and tapers, pressing a little wider on its turns, with dry-brush streaks as the ink runs out. It is routed through waypoints pinned to each block's own anchors and re-measured on every layout change. It is one gesture, not a path that dodges: below the opening it is one long, quiet vertical down the gap between the page's two columns, with only a few authored moments (leaving the crane, a calm lean beside Dr. Liu's print, one bracket-like bow beside the centred pause, the ground under the big bottle and the S under the picker's first two, the research index's spine, the lift into the closing sky). It never threads round a block's words: it passes on the block's other side. Round the products it stays on the paper and draws one calm S (October 5; round 9's lift over the picker read as a broken line): after the ground under the big bottle it bows down in the margin past the left of the picker, reloads and lays a second ground from left to right under the first two small bottles, below their names (20px or more under the chosen name's underline), then sweeps on in one broad bend, wider than it is tall, down into the gap beside the stories' heading (40px or more clear of it); no return, no hairpin. On the two-column page it lifts only where designed (over the far ridges in the opening, into the closing sky, to the three rules and to the footer); the checks hold it to that list. Width at the 1536 comp runs from under 1px to 5.6px, scaled by width/1536 clamped to 0.62–1.15; the brush can lift off the paper. It draws as the reader scrolls (reaching about 78% down the window) and once painted the ink stays. It lifts off in the closing painting's sky, touches down three times as a short, lightly loaded rule over each of the three standards (they have no hairline of their own), travels on to the footer, reloads, and ends as one loaded stroke (about twice the page's usual width) under the footer's promise and the crane at rest beside it: the line that left the crane in flight comes to rest as the ground the crane stands on, under "Stay sharp. Live fully." Reduced motion: the full line from the first frame.

### Stations
A station is a short sentence-case label (17px/450, Sumi Ink) pinned to the brush line by a 1px leader at 62% ink (28–34px long on desktop). It sits in the margin beside its heading with the leader pointing at the line, and appears only when the brush reaches it: the leader draws out over 0.7s, the words fade in over 0.9s. A station exists only where the line passes and carries words that already exist; it is not a heading decoration.

### Research Index
"Curiosity, with references." is a set of notes pinned to the brush line, which runs down the middle of them as the index's spine (900px and wider). A note is its year (24px/300, tabular figures; a guide has a word in the year's place, set as a 17px/450 sentence-case label), its title (20px at the headline weight, balanced) and two caption lines (the kind of source, where it was published), with the round toggle (44px). The year, the toggle and a 1px leader to the spine share one line, and there are no rules between pinned notes. From 1200px the year sits beside the title on one baseline; narrower, it heads the note so the title has the whole width. A note that is pointed at, reached with the keyboard or open answers on its leader: ink draws out from the note to the spine (0.7s). What a source tells us settles in (0.9s) above the page's text link; rows that arrive with a filter or "show all" settle in 55ms apart, and "show fewer" keeps its button under the pointer. One column (under 900px): no spine, so the notes sit on hairlines and ease open to their own height. Reduced motion: all of it at once.

### Cell Labels
In the cell opening, three hairline labels (max(16px, 20 comp px)/450) sit at the ends of leader lines drawn into the painting itself.

### Closing
The finale is the footer's first band, before its links: the promise at display size (clamp(56px, 6vw, 96px), 500, line-height 1; phones clamp(34px, 12vw, 52px), 47px at 390), one sentence to a line ("Stay sharp." / "Live fully."), with the crane at rest standing beside it, facing it, its head well over the words (ink, multiplied; clamp(208px, 20.8vw, 340px) tall, about 320px at 1536; 34vw on a phone, about 133px at 390), both on the closing brush stroke, on generous paper above and below. The crane is the page's last painting: it opens the page in flight, flies home in the closing painting, and rests here; it blooms only once all of it is in the window, low on the bird first, while the brush lays its ground. A hairline closes the band; the logo (136px, 116px on phones), the link columns and the legal lines follow as a calmer second tier. Where the words and the crane cannot share a line (Korean, Japanese and Vietnamese on a phone), the crane stands under the words, at the right.

### Honesty Labels
Every illustration says so: "Illustration" captions on painted stills (the three story still lifes and the brush on its inkstone over Ask BiGH Science), "Illustrations" on the science stage, "Illustration, not a measurement" (16px/500, centred) under the age slider, "Illustrative view" on the cell figure, an outlined "Fictional sample" pill (30px, 15px, Ink Grey) in every story byline, and the research limit note. Caption size and Ink Grey, placed on or beside the image; never removed, never smaller than 15px.

### Motion
- **Ink bloom:** each painting spreads into the paper through an ink blot's soft mask, from 0% to 280% over 1.25 breaths, unblurring from 5px over one breath, with optional per-painting delay and origin (an origin between 28% and 73% on each axis, so the full-grown blot still covers the whole painting). Opening paintings are marked waiting from the server so they bloom rather than flash. A painting whose edges dissolve through its own mask (the opening's landscape, the closing painting) names it `--edge`; the blot is intersected with it, so no painting shows a hard edge before, during or after its bloom.
- **Print laid down:** as Dr. Liu's halo blooms, his print rises 12px into place while the mount's shadow grows from nothing, in one breath. Reduced motion: there, still.
- **Breathing:** the crane glides (4 breaths, alternate); the gold folds of the cell glow up to 55% (2 breaths, alternate). Both stop under reduced motion.
- **Settle:** panels enter over 0.9s by fading and rising 8–10px. State transitions run 0.5s; underline and leader growth 0.7s. The opening's words arrive the same way, like ink settling: each headline line, then the intro, then the pills rise 0.24em and sharpen from an 8px blur over 0.75 breaths, 0.14s apart.
- **Mist:** the opening's landscape is drawn on a canvas with two slow banks of mist drifting through it. Mist is bare paper, so it only takes ink away: the far, pale ridges dissolve and return while the near, dark pines hold. The canvas takes the still painting's place once it has bloomed (same pixels, same multiply) and the mist rises over two breaths. No WebGL, a software renderer or reduced motion: the still painting stays.
- **Light on leaf:** gold leaf is metal. A pale, warm band of light (screen) crosses each painting's leaf, held inside the leaf by that painting's own gold mask: every four breaths on the opening's sun; on the cell's two gold folds, the close view's folds and the closing sun it crosses as the painting travels up the window, so the leaf is lit when it is in front of you. This is light inside a painting, not a gradient fill on the interface.
- **Depth:** leaving the opening, the sun sinks behind the ridges and the mountains settle; with a mouse the sun leans a few pixels against the pointer.
- **Wingbeat:** the opening crane is the approved painting brought to life (a Kling loop from the still, cut out frame by frame like the still, shipped as an animated webp). It holds the glide pose, then beats its wings once, slowly, about every four breaths. It is fetched after the still has bloomed and opens on the still's pose, so the two change places unseen. Reduced motion keeps the still.
- **Arrival:** the cell in "Tiny power plants." settles as it comes into view: a tenth smaller and turned five degrees at first (about its body, so the turn is never cut by anything but the window's edge), at rest by the time it is centred (scroll-driven; still without it).
- **Story change:** changing the story (its names or arrows) blooms the new still life through the same ink blot, laid over its own dissolving edges, while the last one dissolves over 0.6 breath and the quote settles; the first still life arrives with the figure's own bloom. Reduced motion: an instant swap.
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
- **Don't** add drop shadows; the photo mount is the only one (a sheet sits on an ink wash instead).
- **Don't** invent a station label to decorate a heading; stations exist only where the brush line passes.
