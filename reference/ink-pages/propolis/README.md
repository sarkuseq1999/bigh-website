# Green Bee Propolis in Ink & Gold

October 13-14, 2026. Branch `propolis-ink` (worktree `codes/bigh-propolis-ink`), from `origin/main`
c31650f. NuriCell's ink template (`docs/superpowers/specs/2026-10-09-nuricell-ink-design.md`) with
Propolis's own paintings in every chapter and its own signature moment in "Why it matters".

## Mo's picks

| Chapter        | Painting                                                                                       | Take(s)                                         |
| -------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Opening        | The real bottle between "Green Bee" and "Propolis" (the name set to fit; phones stack it)      | (no painting)                                   |
| Why it matters | An old bee tree; as you arrive, gold runs into its cracks from where they meet (Mo: "1A")      | `why-hive-gold`, `why-hive-open` (its cracks)   |
| What's inside  | Raw green propolis like amber in a porcelain dish, one capsule (tinted yellow, as the real one) | `inside-resin-dish`                             |
| The research   | A pressed alecrim sprig on a specimen sheet; no gold, so the eye rests                          | `research-specimen`                             |
| How to take it | An everyday mug of tea, one gold capsule (an American mug, not a teacup: Mo's California rule)  | `daily-mug-v2`                                  |
| Buy            | The real bottle standing in a watercolour scene: alecrim, fallen golden ipê blossoms, a bee     | `buy-painted-empty` (round 7 A, bottle removed) |

No People chapter (the product has no person in its data). No painted sum: one capsule a day makes
"1 × 60 = 60", which says nothing the heading does not.

## Rules learned on the way

- **The bottle is never redrawn** (Mo, October 14). Only backgrounds are painted; the real
  approved bottle photo stands in them. GPT given the bottle as a reference redraws its label with
  typos.
- **Watercolour, not photographs** (October 14): Aesop-style photo scenes did not match the site.
- **California, not Asian** (October 13): no "kintsugi" wording, no teacup; Brazil's own imagery
  (alecrim, the golden ipê, Minas Gerais) is welcome.
- Buy rounds Mo turned down: brush-like alecrim branch, hive lid, poppy meadow, redwood round, hive
  box, full ipê bough (busy), twig / fallen blossoms / quiet bough, a map of Brazil, a lone ipê on a
  plain, green-and-gold alecrim, two photo scenes, a painted bottle. Their originals (142 MB, kept
  out of the public repo) are in `codes/bigh-archive/propolis-ink-unused-originals-2026-10-14/`;
  `originals/` holds the takes the page uses, plus `buy-painted-bottle`, the source of the Buy
  scene.

## Files

- `hf_propolis.py`: GPT Image 2.5 jobs (ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-propolis-ink`,
  cap 42 jobs; Mo's $3). Prompts in `prompts/` (`_style.txt` + `_<name>.txt` → `<name>.txt`).
- `build_propolis.py`: originals → `public/images/products/green-bee-propolis/ink/` and
  `src/components/product/ink/propolis-art.ts`.
- `translations-propolis.cjs`: draft translations m612-m617 (not native-reviewed).
- QA: `scripts/qa/qa_propolis_ink.py`.
