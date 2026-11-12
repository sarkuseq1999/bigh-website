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

How the shots were made: `shoot.py` opens the public demo in Playwright and lays the mock CSS over the
built page (no site code changed; the CSS-module hash `KMPmia` is the demo build's; `nav_classes.py`
lists the current ones). `pack.py` turns the shots into the page's webp files.
