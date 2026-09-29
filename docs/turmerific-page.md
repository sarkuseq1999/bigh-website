# Turmerific product page (September 29, 2026)

Branch `product-turmerific`, worktree `C:\Users\mcbig\Documents\codes\bigh-turmerific`, preview port 3012.
Not merged, not pushed.

## What is here

- `src/components/product/products/turmerific.ts`: the page's data. Six chapters: overview, why,
  inside, research, daily, buy. No credit line or People chapter yet: Mo's September 28 range credit
  gives Turmerific "Developed under the direction and guidance of Dr. Jiankang Liu and Dr. Iris Wang."
  (the Science page shows it); how this page shows it is waiting on Mo.
- Label facts: BiGH's own 2020 label from the old website (facts panel
  `bighnow.com/wp-content/uploads/2020/04/Supplement_facts_Turmerific_v2.jpg`, back
  `.../2020/03/1140_1183_Turmerific2.png`, left side `.../2020/04/Turmerific_Leftv2.png`). Mo confirmed
  it is current on September 29. The back label names the ingredient's maker: never copy that line.
- Studies: Cox 2015 and Nelson 2017 from the homepage list, plus Gota 2010, Santos-Parker 2017 and
  2018, and Cox 2020, each read at PubMed on September 28. The 2018 trial found no change; it is shown
  on purpose.
- 3D bottle: `scripts/product-3d/build_bottle.py turmerific`. Two script changes: the cap now starts
  below its rounded top edge (Turmerific's cap read as ending 20 rows down), and `PLAIN_BACK` gives
  Turmerific a plain orange back instead of streaks of its label's edges. NuriCell's output is
  byte-identical.
- Why picture: a Gemini render of cut turmeric roots (prompt in
  `reference/product-pages/turmerific/originals/`), made into the lit and unlit pictures by
  `scripts/product-pages/why_turmerific.py`: flattened ground, roots at 74% so the words never touch
  them, and the unlit version from the same pixels.
- Cherry-picked from the other product branches: `5ad4310` (bottles draw after a fast jump) and
  `6380cf9` (a single ingredient shows its amount large).

## Checks

`python -X utf8 scripts/qa/qa_turmerific.py http://localhost:3012 --gpu`: 81/81 on September 29.
NuriCell on this branch: why 53/53, research/daily 73/73, hero/cutaway 72/72 twice (one earlier run
had 71/72: the capsule cutaway's timed "intro shows" check).

## Still open for Mo

- New since her approval: the eyebrow "From turmeric root" (the buy chapter showed "Advanced
  curcumin" above and below the name), the Why picture, and its source line.
- A liver-safety answer, after her own research (NCCIH, April 2025).
