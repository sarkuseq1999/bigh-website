# Turmerific product page (September 29 to October 2, 2026)

Branch `product-turmerific`, worktree `C:\Users\mcbig\Documents\codes\bigh-turmerific`, preview
`bigh-turmerific` on port 3012. Main is merged in; the branch is not pushed.

## What is here

- `src/components/product/products/turmerific.ts`: the page's data. Six chapters: overview, why,
  inside, research, daily, buy. The range credit, "Developed under the direction and guidance of
  Dr. Jiankang Liu and Dr. Iris Wang.", is one line under Add to cart (no People chapter). The giant
  name parts as "Turm | erific" (`nameHalves`; "Turme | rific" was 1.9 times as wide on the left).
- Label facts: BiGH's own 2020 label from the old website (facts panel
  `bighnow.com/wp-content/uploads/2020/04/Supplement_facts_Turmerific_v2.jpg`, back
  `.../2020/03/1140_1183_Turmerific2.png`, left side `.../2020/04/Turmerific_Leftv2.png`). Mo confirmed
  it is current on September 29. The back label names the ingredient's maker: never copy that line.
- Studies: Cox 2015 and Nelson 2017 from the homepage list, plus Gota 2010, Santos-Parker 2017 and
  2018, and Cox 2020, each read at PubMed on September 28. The 2018 trial found no change; it is shown
  on purpose. Several Longvida mouse papers by Maiti and colleagues are retracted; never cite them.
- Why: one picture per line (`why.scenes`), like Timeline's How it works (Design Vault #019-#029):
  the cut roots light up gold under the first line, turmeric powder sinks in a glass of water, golden
  oil droplets, then the lit roots again under the title. The photos hand over with a liquid wash
  drawn in WebGL on their own pixels (`signature/why-scenes.ts`). Gemini renders and prompts are in
  `reference/product-pages/turmerific/originals/`; `scripts/product-pages/why_turmerific.py` makes
  the page's pictures (flat night ground, each subject at the chapter's focus, nothing under the
  words).
- 3D bottle: `scripts/product-3d/build_bottle.py turmerific`. Two script changes: the cap now starts
  below its rounded top edge (Turmerific's cap read as ending 20 rows down), and `PLAIN_BACK` gives
  Turmerific a plain orange back instead of streaks of its label's edges. Every other bottle rebuilds
  byte-identical.
- Template additions, optional and unused by the other products: `ProductPage.nameHalves`,
  `ProductWhy.scenes` (with the light coming on under the first line), and the Why checker's
  `light_first`.
- Green Bee Propolis now shows the same credit line under Add to cart (Mo, October 2).

## Checks

`qa_turmerific.py http://localhost:3012 --gpu` (94 checks), `qa_why_chapter.py
http://localhost:3012 --product=turmerific` (53), `qa_green_bee_propolis.py` (34, with the credit).

## Decided (October 2, 2026)

Mo: "A yes, B yes, C yes, D 1, E 1, Propolis yes". The Why story, the eyebrow "From turmeric root"
and the Why source line stay. The range credit is one line under Add to cart, with no People
chapter, on Turmerific and Green Bee Propolis. The page goes live without the liver-safety answer;
Mo adds it after her own research (NCCIH, April 2025).

## Still open

- The liver-safety answer, after Mo's research.
- Translations: the page, like the other product pages, is in English in every language. The credit
  line has no translation yet either (the Science page shows it in English too).
