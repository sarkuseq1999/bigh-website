# Round 3 looks that were not chosen (September 28, 2026)

Mo chose look B, "Scroll film" (`src/components/science/look-film.tsx`). Kept here as they were:

| Look | Files | What it was |
| ---- | ----- | ----------- |
| A · Liquid light | `look-light.*`, `light-scene.ts`, `light-fonts.ts`, `qa/qa_science_light.py` | A WebGL liquid-light shader (Altos Labs mood), Host Grotesk, bright airy page. |
| C · Journal | `look-journal.*`, `journal-cite.tsx`, `journal-motion.ts`, `journal-fonts.ts`, `qa/qa_science_journal.py` | A science-magazine feature: Newsreader + Schibsted Grotesk, figure plates, inline citations. |
| D · Golden hour (round 2's pick) | `look-golden.*`, `qa/qa_science_d.py` | Includes the light baby-blue recolor Mo asked for on September 25 (never committed before). |
| Shared sections D used | `key-studies.*`, `health-doors.*`, `ask-science.*`, `use-reveal.ts`, `qa/qa_science.py` | Round 2's research cards, round health doors and Ask section. |
| Switcher | `look-switcher.*` | The A/B/C review control. |

All three round-3 looks follow `src/components/science/look-types.ts` (a look renders the whole page and
exports a `LookTheme`). To bring one back: move its files into `src/components/science/` and render it in
`science-page.tsx` with its theme tokens, as the film look is.
