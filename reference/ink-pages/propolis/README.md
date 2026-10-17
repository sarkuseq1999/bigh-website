# Green Bee Propolis in Ink & Gold

October 13-14, 2026. Branch `propolis-ink` (worktree `codes/bigh-propolis-ink`), from `origin/main`
c31650f. NuriCell's ink template (`docs/superpowers/specs/2026-10-09-nuricell-ink-design.md`) with
Propolis's own paintings in every chapter and its own signature moment in "Why it matters".

## Mo's picks

| Chapter        | Painting                                                                                        | Take(s)                                         |
| -------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Opening        | The real bottle between "Green Bee" and "Propolis" (the name set to fit; phones stack it)       | (no painting)                                   |
| Why it matters | An old bee tree; as you arrive, gold runs into its cracks from where they meet (Mo: "1A")       | `why-hive-gold`, `why-hive-open` (its cracks)   |
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

## Local design refinement — October 16, 2026

Mo asked Codex to improve the page's design and keep reviewing real desktop and phone screenshots.
This is a **local proposal, not yet published or approved as a new brand rule**. Two opening
mockups are saved in `reference/ink-pages/mockups/propolis-refinement/`: A, a botanical editorial,
and B, the existing split name in lighter type. Codex recommended and developed A.

- A readable two-line product name in Ysabeau beside the unchanged approved bottle. The opening's
  purchase details sit openly on the paper, with the existing supply, refund promise and preview
  checkout behavior.
- Four numbered chapter links. The source, extract, research and daily ritual alternate painting
  and words on desktop; each painting precedes its words on a phone. The tree keeps its gold-filling
  animation in the source chapter only.
- The chapter shortcuts opt in to a heading target in the shared scroll controller. They use the
  real document position after native focus scrolling, update the URL, and move keyboard focus to
  the destination. Touch and reduced motion have a native browser fallback. Other site links keep
  their existing path through the controller.
- Clearer ingredient hierarchy, larger study titles, and years above study titles on phones.
  Questions have a separate heading column on desktop.
- Existing paintings, product facts, study summaries, cautions, translations, real bottle pixels,
  shared menu and footer are preserved. No generation or spending.
- Changes are scoped to Propolis in `propolis-opening.tsx` and `propolis.module.css`. The product
  route supplies Ysabeau without preloading it on the other products.
- The QA script now checks readable, non-overlapping titles and working chapter navigation instead
  of the old split-name geometry. It checks both real bottles for distortion and cropping instead
  of requiring an exact match to NuriCell's dimensions. All painting, motion, copy, language,
  research and deep-link checks remain.

`scripts/qa/capture_propolis_design.py` records viewport screenshots, the tree's moving states,
questions and footer. Raw captures and check logs live in `scripts/qa/out/propolis-design/`
(ignored). `build_review.py` makes the phone-friendly screenshot review at
`reference/ink-pages/mockups/propolis-refinement/index.html` after the final built capture.

### Final local validation

- Production build, lint, TypeScript and changed-file formatting passed.
- Built-site browser checks: Propolis 217/217, homepage 282/282, navigation 436/436. The final
  Propolis run includes 27 chapter-navigation checks for mouse, keyboard and touch. The shared
  homepage/navigation suites ran before the final opt-in shortcut correction; the existing
  homepage chapter link was also checked afterward in the final build.
- Inspected desktop and phone viewport captures through the footer, including the tree arriving,
  filling and at rest. No horizontal overflow or broken images in the responsive review gallery.
- Design assessment: 9/10. The remaining limitation is dense research copy on small phones.
- No public update. Automatic approval review blocked a network-visible phone gallery because it
  would expose unpublished designs to other devices. The review is served only on this PC at
  `http://localhost:3008/`; the built page is at
  `http://localhost:3006/products/green-bee-propolis`.
