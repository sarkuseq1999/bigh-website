# Advanced OPC Formula in Ink & Gold

October 16, 2026. Branch `opc-ink` (worktree `codes/bigh-opc-ink`), from `origin/main` 934d313.
NuriCell's ink template (`docs/superpowers/specs/2026-10-09-nuricell-ink-design.md`) with Advanced
OPC Formula's own paintings in every chapter and its own signature moment in "Why it matters", the
way Green Bee Propolis went (`../propolis/README.md`). The page leans on the vine: grape seed and
red wine are the formula's headline sources, and wine country is California's.

## Mo's picks (October 16, "1C 2A 3A2, nothing else to change")

| Chapter        | Painting                                                                                                      | Take(s)                               |
| -------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Opening        | The real bottle between "Advanced" small over "OPC" and "Formula" (name C; `nameHalves` + `nameLead`)           | (no painting)                         |
| Why it matters | A bunch of grapes on the vine; as you arrive, gold light spreads through the berries from the middle (Why A)    | `why-grapes-gold`, `why-grapes-ink`   |
| What's inside  | Six of the nine plants in two calm rows: grapes, pine bark, bilberries, tea leaves, an orange slice, a marigold | `inside-row`                          |
| The research   | A hand lens over a few grape seeds and a sliver of pine bark; no gold, so the eye rests                        | `research-lens`                       |
| The people     | Dr. Iris Wang, no face ever: a stone mortar and pestle with marigold petals stands for her formulation guidance | `people-mortar`                       |
| How to take it | A plate after the meal, knife and fork laid together, a glass of water, two capsules; the sum 2 × 60 = 120     | `daily-plate`, `sum`                  |
| Buy            | The real bottle standing in a vine scene, the bunch low at the far left (Buy A2: an edit of the first take)    | `buy-vines-left` (edit of `buy-vines`) |

The opening's "One bottle" card shows the two capsules cut from the plate painting. Not chosen:
Why B (a vineyard at sunrise, `why-vineyard-gold` / `-ink`), Buy A1 (`buy-vines`, the bunch half
hidden behind the bottle), Buy B (`buy-stroke`, NuriCell's device). Their originals stay here.

## Rules kept

- The bottle is never redrawn (Mo, October 14): the real photo stands in the painting; its width
  and NuriCell's size come from the template (`nameFit`, `InkScene`).
- Watercolour and ink, no photo scenes; nothing Asian-coded (no "kintsugi" wording, no teacup).
- Gold leaf only where it means something: the light inside the grapes. The capsules stay plain
  grey (their real colour is not known).
- Facts only from the data file and label; the alt texts and the sum captions are drafts for Mo.

## Template additions (optional; NuriCell and Green Bee Propolis unchanged)

- `ProductPage.nameLead`: a short first word set small over the first half, as wide as it
  (opening.tsx `--lead-scale`, `[data-lead]`; phones keep a word space between the halves).
- `ProductPerson.paintingOf: "work"`: a painting of the person's work is captioned "Illustration"
  (the default stays "Portrait painting").
- Counts as words up to thirteen (`WORDS` in template-chapters-model.ts): "Inside every capsule,
  thirteen ingredients."

## Files

- `hf_opc.py`: GPT Image 2.5 jobs (ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-opc-ink`, cap 42
  jobs; Mo's $3). Prompts in `prompts/` (`_style.txt`, `_style-land.txt`, `_style-sum.txt` +
  `_<name>.txt` → `<name>.txt`, joined by `prompts/compose.py`).
- `build_opc.py`: originals → `public/images/products/advanced-opc/ink/` and
  `src/components/product/ink/opc-art.ts`.
- `translations-opc.cjs`: draft translations m700-m705 (not native-reviewed).
- QA: `scripts/qa/qa_opc_ink.py`.
