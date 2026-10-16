# Turmerific in Ink & Gold

October 16, 2026. Branch `turmerific-ink` (worktree `codes/bigh-turmerific-ink`), from `origin/main`
934d313. NuriCell's ink template (`docs/superpowers/specs/2026-10-09-nuricell-ink-design.md`) with
Green Bee Propolis's additions (`../propolis/README.md`), and Turmerific's own paintings in every
chapter and its own signature moment in "Why it matters".

## Mo's picks

Round 1 offered two options for Why and for Buy, and one painting for each other chapter. Mo: "Why A
and Buy A" (October 16).

| Chapter        | Painting                                                                                              | Take(s)                             |
| -------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------- |
| Opening        | The real bottle between "Turm" and "erific" (sized to fit; one word on phones)                         | (no painting)                       |
| Why it matters | A turmeric root and a slice cut from it; as you arrive the slice turns gold and the gold soaks out into the paper | `why-soak-lit`, `why-soak-unlit` |
| What's inside  | A wooden spoon of golden curcumin powder and two capsules (made matte in the build: painted glossy)    | `inside-scoop`                      |
| The research   | Reading glasses on an open notebook, a turmeric leaf as a bookmark; no gold, so the eye rests         | `research-glasses`                  |
| How to take it | A glass of water and two gold capsules, and the painted sum 2 × 30 = 60                                | `daily-glass`, `daily-sum`          |
| Buy            | The real bottle standing in the turmeric plant in flower, as the label draws it; gold root slices at its foot | `buy-plant`                  |

No People chapter (the product has no person in its data; the credit line stays under Add to cart).
The card in the opening shows the two capsules from the daily painting. No big number in Why: the
data file has none, and none is invented. The liver question stays out of the questions until Mo has
done her research.

## The signature: the gold soaks in

Absorption is the chapter's point ("A golden compound. A hard one to absorb."), told in the site's
own medium: watercolour soaking into rice paper. The template's new optional `why.soak` mode
(`product-types.ts`, `why.tsx`, `product-ink.module.css`): the build script works out when each
pixel turns gold (its distance from the slice divided by how far the gold reaches in that direction,
so the bloom grows in its own ragged shape, plus a fine noise on the wet edge) and writes ten masks
into one sprite (`soak-v1.webp`). The page stacks nine layers of the lit painting, each through one
mask, under the whole lit painting, and fades them in one after another: quick at first, then slower
as the bloom widens (layer k starts at (k / 10)² of 1.8 breaths). It waits for the same three things
as the lantern and the hive (bloom started, half in view, pictures decoded). Reduced motion and no
script: whole from the first paint. NuriCell's lantern and Propolis's spread are unchanged.

## Not chosen

Why B "tiny drops" (a trail of gold drops for Longvida's "tiny particles of fat": read as a sparkler)
and Buy B "California golden hour" (golden hills and an oak: says California, not turmeric). Their
originals are kept out of the public repo, in
`codes/bigh-archive/turmerific-ink-unused-originals-2026-10-16/`; their prompts stay in `prompts/`.

## Files

- `hf_turmerific.py`: GPT Image 2.5 jobs (ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-turmerific-ink`,
  cap 42 jobs; Mo's $3 of October 16).
- `prompts/make_prompts.py`: writes the prompts (`_<name>.txt` the subject, `<name>.txt` the full
  prompt; `_style.txt` for ink, `_style-color.txt` for the Buy scenes).
- `build_turmerific.py`: originals → `public/images/products/turmerific/ink/` and
  `src/components/product/ink/turmerific-art.ts`.
- `translations-turmerific.cjs`: draft translations, keys m740 onward (Turmerific's range is
  m740-m779; m740-m744 used), not native-reviewed.
- QA: `scripts/qa/qa_turmerific_ink.py`. The old template's `scripts/qa/qa_turmerific.py` no longer
  applies to this page.
