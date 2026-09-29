# Advanced OPC Formula product page (September 28, 2026)

Branch `product-opc`, worktree `bigh-opc`, preview `bigh-opc` (port 3011). The page is the NuriCell
template filled with Advanced OPC Formula's data: `src/components/product/products/advanced-opc.ts`,
its 3D bottle (`bottles/advanced-opc.json`, `public/images/products/3d/advanced-opc-label.webp`) and
its pictures in `public/images/products/advanced-opc/`. No catalog or homepage file changed.

Three template changes, safe for every product:

- From the Nature Calm branch (`fc99a96`, cherry-picked as is): two-word names keep their space on
  phones ("AdvancedOPC Formula" before).
- From the Green Bee Propolis branch (`5ad4310`, cherry-picked as is): 3D bottles start drawing
  after a fast jump (the IntersectionObserver's newest entry decides).
- Mo's "A" (September 28): `ProductIngredient.picture`, a small round photo leading an ingredient's
  row (`template-chapters-inside.tsx`, `.ingredientPicture` in `template-chapters.module.css`). Only
  when some ingredient has one; rows without keep an empty slot so names line up. NuriCell and
  every product without pictures render exactly as before.

## Chapters

1. Overview: the "Big name" opening with the 3D bottle; approved headline and purpose.
2. Why it matters: a photo moment (a still life of the plant sources, "Nine plant extracts. One
   formula.") then the night stage: a bunch of grapes, dark for the free-radical line, lit when the
   antioxidants arrive; title "A balance worth keeping."
3. What's inside: the 13 label ingredients, plants first with a round photo each, vitamins and
   selenium last (Mo, September 21: vitamins C and E must not lead). No capsule cutaway.
4. The research: five studies, oldest first (2008 pine bark and memory, 2010 pine bark null trial,
   2011 grape seed meta-analysis, 2020 Cochrane pine bark review, 2024 Halliwell antioxidants review).
5. The people: Dr. Iris Wang, text only (she asked for no photograph).
6. How to take it: "One bottle, two months." (2 capsules a day, 120 capsules).
7. Buy, with the credit "Formulated under the guidance of Dr. Iris Wang."

## Facts and where they come from

- Label: the 2019 supplement facts and usage card from the old site
  (`old-storage/previous-site/content/harvest/assets/uploads/2019/04/sup_opc.png`, `ser_opc.png`),
  confirmed current by Mo on September 28, 2026. Serving 2 capsules, 60 servings, 120 vegetarian
  capsules; "take 1-2 capsules with or after a meal, once per day". The label photos hold no
  warnings panel, so the caution line is general advice, not label text.
- Credit: Mo, September 28: "Formulated by the guidance of Dr. Iris Wang", worded "under the
  guidance" on the page (recorded in BRAND-CHEATSHEET.md).
- Approved words reused: headline, purpose (homepage card); "Making energy also makes a few free
  radicals", "free radicals—unstable molecules that can damage cells", "Antioxidants keep them in
  balance", "Your body also makes its own antioxidants" (homepage card and science section).
- Every other sentence is a draft for Mo. Sources for the drafts: NIH ODS fact sheets (vitamin C,
  vitamin E, selenium, vitamin A for lutein in the retina), NCCIH (grape seed extract, bilberry,
  noni, antioxidant supplements), MedlinePlus (antioxidants), the Cochrane pine bark review 2020
  (pine bark is rich in proanthocyanidins, which are antioxidants), RESEARCH-NOTES.md (Dr. Wang's
  animal studies of oxidative damage with Dr. Liu). The two new studies were read at PubMed on
  September 28 (18701642, 32990945).

## Pictures

Made with Gemini (`reference/product-pages/advanced-opc/originals/`, prompts in the `.json`
sidecars). The grapes' "off" frame is the "on" photo's own pixels, dimmed and cooled, so the two
line up exactly; their dark ground is moved to the page's night (#061625). The still life's
highlights are toned down a little so its cream line stays at least 3:1. The nine ingredient photos
share one prompt; each is cropped around its subject and its background set to one exact pink
(#f3e2e4).

## Bottle

`build_bottle.py` gained `clean_edges`, used only for the slugs in `STRAY_EDGE_ART`
(`advanced-opc`): the label's grape leaf and side lettering run off the photo's edge and were
smeared round the whole back as a yellow band. NuriCell's label rebuilds byte for byte as before
(checked).

## Checks

`python -X utf8 scripts/qa/qa_advanced_opc.py http://localhost:3011 --gpu`: 110 checks at 1440x900
and 390x844, with and without motion (words in order, grapes dark then lit, no words over the
grapes, contrast, no photo edge, the name's space and the eyebrow clear of it, 13 label amounts,
the nine round photos, studies, Dr. Wang text only, calendar, credit, buy, the Buy bottle after a
fast jump, questions, no sideways
scroll, no console errors, Korean route, homepage link). NuriCell's `qa_research_daily.py`,
`qa_why_chapter.py` and `qa_hero_cutaway.py --gpu` pass on this branch.

## Open for Mo

- The drafts (numbered on the review page).
- On phones the hero's eyebrow has room for one line only (the name sits a fixed 50px below it).
  "From nature" fits down to 360px wide; a longer eyebrow or a translation would run into the name.
  A template fix (eyebrow in the flow on phones) would make any length safe.
