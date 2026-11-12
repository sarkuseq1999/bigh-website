# Menu bar, California (November 12, 2026)

Mo: the site has moved from an Asian feel to California; should the menu bar change a little? Claude's
read: the bar is mostly neutral; the one strongly Asian note is the heavy black calligraphy stroke
behind Sign up (and Menu on phones), and the bar's pure black ink now looks like the old site next to
the colourful paintings. Three ideas were offered in chat (A warm ink, B golden ridge, C a little
redwood park-sign button, which borrows the footer's sign); Mo asked to see A and B.

Review page: https://claude.ai/artifact/UtGCL7ex63HdX7gyxYM5Wx (`page/`). Not decided yet.

- **A, warm ink.** Same bar. Every black brush mark turns warm umber (`#5e4535`): the rule, the
  current-page stroke, the pointing wash and the menu sheet's marks; Sign up and Menu take a loaded
  umber, `linear-gradient(90deg, #4a3226, #5e4232 45%, #7a5640)` (the cream letters about 8:1 where
  they sit, 5.9:1 even at the lightest end). The words and the mark stay as they are. Claude's score 8/10: Sign up keeps the
  calligraphy shape; the pages' own buttons stay black.
- **B, golden ridge.** A, plus the rule becomes a low ridge of far-off golden hills: Codex painting
  `reference/nav/originals/codex-ridge-3.png` (prompt beside it), cut by `cut_ridge.py`
  (`CHROMA=0.62 cut_ridge.py ridge-3.png ridge-strip.png 0.8 220 30`: paper divided out, wash kept
  30 rows under the ridge, squashed to 0.8, ends tapered over 220 px), drawn at 0.78 opacity with its
  ridge line on the bar's foot; the settled bar's paper runs 34 px past the foot (22 today) so the
  page never shows through the hills. Claude's score 7.5/10: it repeats on every page; on About the
  hills sit right above the meadow's hills, on the homepage above the sun. A first take with two
  oaks (they read as green bugs at this size) and a stronger gold were dropped; those takes and every
  raw shot are in `bigh-archive\nav-california-2026-11-12\`.

**Round 2 (same day).** Mo: "it doesn't have to be just changing the color ... think freely". Added to
the same review page (Version 2), and Claude's pick moved from A to C:

- **C, poppy.** Sign up on a watercolour swatch of California-poppy orange with ink letters (Codex
  `codex-poppy-swatch-1.png`, calmed to 0.8 chroma by `cut_pieces.py`); the current page marked by a
  soft poppy dash (`codex-poppy-dash-1.png`, the top dash); everything else A's warm umber, Menu/Close
  included (two orange patches on the phone made Close as loud as Sign up). Score 8/10: the
  calligraphy swash is gone and the one bright thing is the button to press; on About it matches
  the poppy meadow. Held back: a new colour, brighter than the pages' black buttons.
- **E, open air.** CSS only: the mark at the left (`.left`/`.right` as `display: contents`, flex
  order), all links to its right, the language and the account at the end, a 1px sepia hairline,
  a 2px ink underline for the current page, Sign up and Menu as ink pills like "Discover NuriCell".
  Score 7.5/10: calmest and most American, but it loses the painted feel.
- **D, sky strip (dropped, not shown).** The bar as a slim painted California morning (Codex
  sky-strip-2, the sky squashed, the hills kept): two landscapes stacked on every page, an oak stood
  on top of the homepage's redwood, and the settled bar chopped the hills. Paintings and shots in the
  archive folder.

**Round 3 (same day).** Mo: "This doesn't look really good. Give me some more ideas." Claude pulled
the menu bars Mo saved in his design vault (#004 Timeline's bar, "very simple and not boring, clear
navigation"; #045 Timeline's header as an avoid: too small for older readers; #039 Seed's rounded
frosted drop-down) and built two new layouts from them. The review page (Version 3) shows only Today,
F and G; A to E stay in this folder's git history (`page/` at a674ae8).

- **F, masthead** (from #004, made large). The mark centred alone on the top row (132px), the language
  and Log in / an outlined Sign up pill at its two ends, all four links centred on a second row, a
  fine sepia dotted line under the bar (`--tall` 142px; pages start 38px lower, mocked as
  `main { margin-top: 38px }`). Once the page moves on it folds into one row: mark left, links in
  the middle, language and account right. A 2px ink underline for the current page. Score 8.5/10;
  Claude's pick.
- **G, floating paper** (from #039). The bar is one rounded sheet of frosted rice paper (95%, blur 14px,
  soft shadow) floating 16px from the top: mark (114px) left, links in the middle, language, Log in
  and an ink Sign up pill right; a paper fade at the window's top so text fades before it slides
  under the sheet. Score 8/10: tidy and modern, but more app than painting.

How the shots were made: `shoot.py` opens the public demo in Playwright and lays the mock CSS over the
built page (no site code changed; the CSS-module hash `KMPmia` is the demo build's; `nav_classes.py`
lists the current ones). `pack.py` turns the shots into the page's webp files.
