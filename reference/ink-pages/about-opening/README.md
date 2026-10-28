# About opening: new ideas (October 27, 2026)

Mo found the About page's big ink circle (live since October 27, title inside it) scary: "the
more I look at it, the more it reminds me of the movie The Ring". He asked for more concepts and
said yes to painting all three as mockups:

- **A. Superbloom:** golden hills in spring poppies fill the first screen, the title in the sky;
  the poppies would bloom as the page opens. 8/10: the yellow is brighter and wider than the
  site's one touch of gold, and the poppies are painted more carefully than the site's loose ink.
- **B. Morning walk** (Claude's pick): a trail over golden hills in the morning, one person and a
  dog walking away from us, the sunlit ridge the only gold. 8.5/10: the walker, with a backpack,
  reads as a young hiker rather than an older reader.
- **C. The name, painted:** no new picture; the title's capitals B, i, G, H brushed (the October 6
  letter paintings in `../about/originals/gpt25-letter-*-v1.png`), the hills kept. 7/10: close to
  the painted BiGH Mo turned down on October 7, and the brush letters beside the heavy type look
  like two fonts.

Nothing in `src/` changed; the live page still shows the circle.

- Paintings: Codex (ChatGPT plan, no API spend), two takes each, `originals/superbloom-a1`, `a2`,
  `walk-b1`, `b2`; prompts `prompts/superbloom-a.txt`, `prompts/walk-b.txt`. Shown: a1 and b1.
- `cut_mockups.py` turns the paper to transparency into `plates/img/` (git-ignored).
- `shoot_mockups.py` lays each idea over the public demo's About page by injected CSS and shoots
  1440 x 900, 1920 x 1000 and 390 x 844, each also scrolled 70% of a screen, into `plates/shots/`.
  On a phone B1 is framed at 33% across so the walker sits near the middle.
- Page for Mo: `../mockups/about-opening/about-opening.html`
  (Artifact https://claude.ai/artifact/6hnK43uNUsZ3R1tFSPvy6N).
