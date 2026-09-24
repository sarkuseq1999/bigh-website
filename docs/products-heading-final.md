# Chosen product introduction and refined stories — September 23, 2026

Mo approved this wording after explaining that different countries may carry different product lineups:

**Explore our products.**  
_Find your starting point._

“Discover the science, ingredients, and purpose behind each BiGH product.”

The heading does not promise a particular number of products. It is now the single active introduction, with the same centered Elegant typography. The temporary 1–2–3 comparison controls and their React state are removed. The existing five demo products remain; country-specific assortments have not been specified or implemented. The story counter now derives its total from the collection instead of hard-coding 05.

## New NuriCell artwork

The NuriCell story no longer repeats the mitochondrion image used in the preceding science section. It now shows a woman in midlife walking along a coastal trail. This is illustrative generated lifestyle artwork, not a customer testimonial or evidence of an effect from taking the product.

- Mode: **built-in image_gen**, one generation call.
- Served asset: `public/images/products/stories/nuricell-coast-v1.webp` (1200 × 800, 158,686 bytes).
- Full-resolution original: `reference/products-section/story-image-originals/nuricell-coast-v1.png`.
- Full final prompt and saved paths: [nuricell-coast-prompt.json](../reference/products-section/nuricell-coast-prompt.json).
- The original also remains in Codex’s generated-images folder. Sharp was used only to resize and compress the served copy.
- NuriCell's focal position is adjusted so the walker remains visible in the narrower tablet crop. Other product story images and all approved bottle PNGs remain unchanged.

## Story-panel refinement

The right-hand side now uses a short lead, two icon highlights, a separate supporting detail or scientist credit, and the existing Discover button. A fine dot texture and soft white-to-product-color shading add depth. NuriCell's highlights are “Mitochondrial health” and “Mental energy.” Companion highlights summarize existing product information, with no new clinical or blood-brain-barrier claims.

Propolis, Turmerific, and Nature Calm copy is rearranged into this shorter structure. Longvida’s UCLA development credit refers to the ingredient, not the whole Turmerific product. Dr. Iris Wang’s public name is preserved. Eighteen strings were added or reused across all five languages; translations remain drafts without native editorial review.

The earlier source files are saved in `reference/products-section/2026-09-23-before-product-heading-final/`. The reduced bottle dimensions, central NuriCell placement, and understated flagship caption remain.

## Local verification

- Changed-code lint and formatting passed. The production build compiled, passed TypeScript, and generated all 10 static pages.
- Checked 75 combinations: five products × five languages × 320, 768, and 1440px. All story images loaded, each story showed exactly two highlights, and no page, headline, or highlight-card overflow was detected. Comparison buttons were absent.
- Inspected all five desktop story panels plus NuriCell at tablet and phone widths. A tablet crop correction keeps the walker's full face visible.
- A fresh 390px browser verified next/previous product controls, opening the NuriCell dialog, Escape dismissal, and no page errors. Client and scroll widths both measured 375px, including the browser scrollbar.
- Local screenshots are in `reference/products-section/products-final-*.png`. Checks use Chromium viewport emulation rather than physical phones or Safari.

Public address remains https://bigh-website-demo.vercel.app/#products. See [public-demo.md](public-demo.md) for deployment and anonymous-access verification.
