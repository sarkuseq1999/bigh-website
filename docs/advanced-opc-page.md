# Advanced OPC Formula product page (September 28, 2026)

Branch `product-opc`, worktree `bigh-opc`, preview `bigh-opc` (port 3011). The page is the NuriCell
template filled with Advanced OPC Formula's data: `src/components/product/products/advanced-opc.ts`,
its 3D bottle (`bottles/advanced-opc.json`, `public/images/products/3d/advanced-opc-label.webp`) and
three pictures in `public/images/products/advanced-opc/`. One template fix, taken as is from the Nature Calm
branch (`fc99a96`, cherry-picked): two-word names keep their space on phones ("AdvancedOPC Formula"
before). No catalog or homepage file changed.

## Chapters

1. Overview: the "Big name" opening with the 3D bottle; approved headline and purpose.
2. Why it matters: a photo moment (a still life of the plant sources, "Nine plant extracts. One
   formula.") then the night stage: a bunch of grapes, dark for the free-radical line, lit when the
   antioxidants arrive; title "A balance worth keeping."
3. What's inside: the 13 label ingredients, plants first, vitamins last (Mo, September 21: vitamins
   C and E must not lead). No signature moment (the capsule cutaway is NuriCell's).
4. The research: five studies, oldest first (2008 pine bark and memory, 2010 pine bark null trial,
   2011 grape seed meta-analysis, 2020 Cochrane pine bark review, 2024 Halliwell antioxidants review).
5. How to take it: "One bottle, two months." (2 capsules a day, 120 capsules).
6. Buy. No "The people" chapter: the formulation credit is still open.

## Facts and where they come from

- Label: the 2019 supplement facts and usage card from the old site
  (`old-storage/previous-site/content/harvest/assets/uploads/2019/04/sup_opc.png`, `ser_opc.png`).
  NOT yet confirmed current by Mo. Serving 2 capsules, 60 servings, 120 vegetarian capsules;
  "take 1-2 capsules with or after a meal, once per day". The label photos hold no warnings panel,
  so the caution line is general advice, not label text.
- Approved words reused: headline, purpose (homepage card); "Making energy also makes a few free
  radicals", "free radicals—unstable molecules that can damage cells", "Antioxidants keep them in
  balance", "Your body also makes its own antioxidants" (homepage card and science section).
- Every other sentence is a draft for Mo. Sources for the drafts: NIH ODS fact sheets (vitamin C,
  vitamin E, selenium, vitamin A for lutein in the retina), NCCIH (grape seed extract, bilberry,
  noni, antioxidant supplements), MedlinePlus (antioxidants), the Cochrane pine bark review 2020
  (pine bark is rich in proanthocyanidins, which are antioxidants). The two new studies were read
  at PubMed on September 28 (18701642, 32990945).

## Pictures

Made with Gemini (`reference/product-pages/advanced-opc/originals/*.jpeg`, prompts in the `.json`
sidecars). The grapes' "off" frame is the "on" photo's own pixels, dimmed and cooled, so the two
line up exactly; their dark ground is moved to the page's night (#061625). The still life's
highlights are toned down a little so its cream line stays at least 3:1.

## Bottle

`build_bottle.py` gained `clean_edges`, used only for the slugs in `STRAY_EDGE_ART`
(`advanced-opc`): the label's grape leaf and side lettering run off the photo's edge and were
smeared round the whole back as a yellow band. NuriCell's label rebuilds byte for byte as before
(checked).

## Checks

`python -X utf8 scripts/qa/qa_advanced_opc.py http://localhost:3011 --gpu`: 92 checks at 1440x900
and 390x844, with and without motion (words in order, grapes dark then lit, no words over the
grapes, contrast, no photo edge, 13 label amounts, studies, calendar, buy, questions, no sideways
scroll, no console errors, Korean route, homepage link).

## Open for Mo

- Formulation credit (none shown until decided).
- Is the 2019 label still current? (NuriCell's was confirmed; this one was not.)
- The drafts (listed in the session report).
- "What's inside" has no picture moment of its own; adding one needs a small template change.
- On phones the hero's eyebrow has room for one line only (the name sits a fixed 50px below it).
  "From nature" fits down to 360px wide; a longer eyebrow or a translation would run into the name.
  A template fix (eyebrow in the flow on phones) would make any length safe.
