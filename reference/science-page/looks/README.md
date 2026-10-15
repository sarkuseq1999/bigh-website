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

- film/ — "Scroll film" (Mo's pick, September 28, 2026), live until the ink handscroll replaced it (October 2026); its QA: film/qa_science_film.py.

To bring one back: move its files into `src/components/science/`, add it to the page in `science-page.tsx`,
and restore its color tokens (see git history of `science-page.module.css` for `.page[data-look=…]`).
Look C and E use `public/images/science-page/dark-cell.webp`'s original,
`reference/science-page/originals/sp-dark-cell.png`. Details of each round: `docs/science-page.md`.

To bring the film back (October 14, 2026): move `film/*.ts`, `*.tsx` and `*.module.css` back into
`src/components/science/` (`science-page.tsx` is its page) and `film/qa_science_film.py` back into
`scripts/qa/`; point `src/app/[locale]/science/page.tsx` at `SciencePage` again; and restore the
pictures it used, removed from `public/images/science-page/` in commit 6aa001d (`git checkout 6aa001d~1 --
public/images/science-page/`; originals in `reference/science-page/originals/` and `.../originals/film/`).
The looks above also need `science-page.tsx` from `film/`, since the old page now lives there.
The film and the looks also read `liuStory` and `opening.titleLead` / `opening.titleAccent`, removed
from `src/components/science/science-content.ts` on October 14, 2026 (unused by the ink page): take
them back from `git show 8cc9238:src/components/science/science-content.ts`.
