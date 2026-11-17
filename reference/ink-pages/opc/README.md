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

## The opening: a vineyard at harvest (Mo picked B, November 16, 2026)

Mo's goal that day: every product page superb. OPC's first screen was the template's bottle on bare
paper, the same as Turmerific's and Nature Calm's. Three seasons of one California vineyard were
painted by Codex (`paint_opening.sh`, `prompts/opening-{spring,harvest,autumn}-1.txt`; takes `a`
and `b`, each with the homepage's Big Sur close as the painter's hand, the `h` takes) and mocked on
the live page by script (`../mockups/opc-opening/`: `mock.py`, `mock_sky.js`, `prep.py`; review
page https://claude.ai/artifact/Ta1qo8Jp8V8cMbkuoJe4e7): A spring with yellow mustard between
young vines, B late summer before harvest (golden hills, oaks, ripe dark grapes), C autumn colour.
Mo picked **B** (take `opening-harvest-ah`), Claude's pick: the grapes say where OPCs come from.

Built as NuriCell's clear day is built (`build_opc_opening.py` → `opening-vines-*-v1.webp`,
`src/components/product/ink/opc-opening-art.ts`; first `opc-opening.tsx` and `opc.module.css`,
the same day made `painted-opening.tsx` and `painted-opening.module.css`, shared with
Turmerific's field; the art carries `base`, "Formula"'s baseline at 60% of the bottle's box, and
`lift`, 0.1): the
painting lies in the bottle's box, scaled so the hills under the name (row 650) meet the letters'
baseline and the ground (row 795, in the dry grass) the glass's foot; the name lifted 0.1 of its
size off the hills; the painting's own dry grass laid in front of the bottle's foot; in a window
wider than that (about 1600px and up, or a short one) the painting drawn as wide as the window,
still on the glass's foot, so its hills rise a little behind the name (side pieces mirrored at its
edges were tried first and made a "V" of vine posts at the joint); on a phone the painting drawn
closer (two bands of bare slope beside the bottle taken out) so a bunch of grapes stands on each
side. Checks: `qa_opc_ink` section `vineyard`. The other five takes (spring, autumn and the `b`
takes) are in `codes/bigh-archive/opc-opening-unused-2026-11-16/`.

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
