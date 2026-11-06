# About: "Each plant, from where it grows best" (mockups, November 6, 2026)

Mo liked the idea of the plants part but not its design (four specimens beside a 2 x 2 key with
"Place to confirm" in three spots). Three new ideas, built on the real page behind
`/about?plants=a|b|c` (`src/components/about/plants-mockups.tsx`, English only, mockup code):

- **A, the map home**: the world painted in ink (Codex over the real land: `render_land.py` draws
  Natural Earth 1:50m from the `world-atlas` npm package in a Miller projection, `ref/land-guide.png`),
  the four plants cut from `specimens-1-a` standing at their places, gold dotted routes to California
  drawn by the page.
- **B, four homes**: one small landscape per plant (`minas`, `turmeric`, `grape`, `pine`), stepping
  up and down from 960px, swiped on phones.
- **C, one plant all the way**: the Minas Gerais painting alone, the one place on file.

Only Minas Gerais, Brazil is on file. India, Italy and France are stand-ins in the mockups.

Pictures: `paint.sh` (Codex, ChatGPT plan, no spend), `build_about_plants.py` ->
`public/images/about-plants/` and `src/components/about/plants-art.ts`. Review page:
`reference/ink-pages/mockups/about-plants/about-plants.html` (Artifact CRNzLrmV8DbRdX7ZcAc5SP).
Spend: none.
