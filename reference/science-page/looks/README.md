# Science page looks that were not chosen (September 25, 2026)

Mo picked look D, "Golden hour" (`src/components/science/look-golden.tsx`). These are the other five, kept
as they were when he chose, so any of them can come back.

| Look | Files | What it was |
| ---- | ----- | ----------- |
| A · Portrait (round 1) | `look-portrait.*` | Centered photo that comes into focus, three big numbers. Mo liked its portrait. |
| B · Life's work (round 1) | `look-path.*` | Pinned sideways career path with a gold line. Mo liked the timeline. |
| C · From the dark (round 1) | `look-dark.*` | Dark hero; the dark glass cell answering three questions. |
| E · Night sky (round 2) | `look-sky.*`, `sky-scene.ts`, `qa/qa_science_e.py` | three.js stars; his papers fill the sky along a constellation path. Close second. |
| F · Glass (round 2) | `look-glass.*`, `glass-scene.ts`, `qa/qa_science_f.py` | Live three.js glass mitochondrion; frosted glass cards. |
| Switcher | `look-switcher.*` | The review control that switched looks. |

To bring one back: move its files into `src/components/science/`, add it to the page in `science-page.tsx`,
and restore its color tokens (see git history of `science-page.module.css` for `.page[data-look=…]`).
Look C and E use `public/images/science-page/dark-cell.webp`'s original,
`reference/science-page/originals/sp-dark-cell.png`. Details of each round: `docs/science-page.md`.
