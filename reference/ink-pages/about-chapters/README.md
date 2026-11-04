# About: two new chapters (DRAFT, November 4, 2026)

Mo asked for more on the About page: "our key formula began with our scientists" (already the
Our scientific roots chapter), "our ingredients are selected around the world, from the part of
the world best for their natural growth", and "all of our products are proudly made in
California, by GMP or cGMP certified manufacturers". Then: "make up your own ideas … enhance it …
I will comment and critique once you're done."

Built on branch `about-chapters` (not on `studio`, not live):

- **Our ingredients: "Each plant, from where it grows best."** The botanist's four specimens
  (green propolis with a honeybee, turmeric, grapes, pine cone and bark), a key beside them two
  by two: plant, place, product. Only the propolis origin is on file (Minas Gerais, Brazil,
  RESEARCH-NOTES.md); turmeric, grape seed and pine bark show "Place to confirm" until Mo gives
  the real places (one supplier listing gives India for Longvida's turmeric: not confirmed). The
  chapter speaks of plants only: NuriCell's four nutrients are made, not grown.
- **Our home: "Proudly made in California."** The five real approved bottles (only scaled)
  standing on a painted Southern California morning (fan palms, blue-grey mountains, golden
  grass, lupines), with "Every bottle we sell is made here, by GMP-certified manufacturers." and
  GMP said in plain words (21 CFR 111: ingredients checked, a written recipe, every batch
  recorded). "GMP-certified" is Mo's fact of September 25; he said "GMP or cGMP" on November 4.
- **Our promise: three, not four.** Made in California and the propolis line became chapters;
  new: "Honest about the research. We show you the studies, and say what they don't prove."

New words are English only (the catalogs fall back to the English) until Mo approves them.

## Pictures

Codex (ChatGPT plan, no API spend), `paint.sh prompt@take …`, the About oak and sequoia and the
homepage's loose hummingbird as the hand's reference:

- `plants-1` (a, b): colourful, careful, like a greeting card. Not used (moved with the other
  unused takes, `plants-2-b` and `home-1-b`, to `codes/bigh-archive/about-chapters-unused-2026-11-04/`).
- `plants-2` (a, b): "ink first, colour second". **a ships** (`plants-v1.webp`).
- `home-1` (a, b): the scene with an empty ground. **a ships**.
- `front-1` (a): the grass and lupine strip; its upper part is painted into the scene behind the
  bottles, its lowest blades lie in front of their feet (`home-front-v2.webp`), so no blade is
  painted twice.

`build_about_chapters.py` divides the paper out, stands the bottles (five, NuriCell in the
middle, 33% of the scene's height), cuts the empty sky, and writes
`public/images/about-chapters/*.webp` and `src/components/about/chapters-art.ts`. The home's
layers are `-v2`: the image optimizer had cached the first, smaller bottles under `-v1`.

Review page for Mo: `../mockups/about-chapters/about-chapters.html`.
