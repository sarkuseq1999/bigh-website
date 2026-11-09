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

**Mo picked A, the map (November 6, 2026).** Built for real as `src/components/about/plants-map.tsx`
(the mockup switch and ideas B and C are gone; their paintings, prompts and mockup code went to
`bigh-archive/about-plants-unpicked-2026-11-06/`). The page lays the trails home as gold-leaf dabs,
one plant after another, once, as the map comes into view; each trail arcs to its own height so
they fan out. The two European plants stand one over the other in the North Atlantic (side by
side, the grapes stood on Morocco). The places other than Minas Gerais are still stand-ins
(`confirmed: false` in `about-content.ts`).

**No place names (Mo, November 9, 2026).** Mo is still finding out where the pine bark and grape
seed come from, and asked that the map not name places at all: only the feeling that each plant
comes from the region of the world best for its natural growth. Each plant gets the kind of place
it thrives in ("Warm, wild hillsides", "Hot, rainy fields", "Sunny slopes", "Old pine forests"),
true of the plant wherever it is bought. Mockups behind `/about?map=a|b|c`
(`src/components/about/map-mockups.tsx`):

- **A, plants at sea**: the same map, no dots or names, each plant in a different sea. 8/10: a plant
  near a coast can still read as from there.
- **B, the globe** (my pick, 9/10): a Codex globe over the real land (`render_globe.py`, orthographic,
  centre -98, 24, `ref/globe-guide.png`; `globe-1-a`), the plants just past its rim, the trails over
  it to California. Phones clip the trails to the globe, so they start at its edge.
- **C, four kinds of place**: the round-1 landscapes (`home-*-v1`, back from bigh-archive) with one
  gold road under them. 7.5/10, left off the review page: the paintings still hint at countries.

Review page: `reference/ink-pages/mockups/about-plants/no-places/` (Artifact CRNzLrmV8DbRdX7ZcAc5SP,
version 2).
