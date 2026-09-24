# Product story imagery and copy review — September 23, 2026

**Superseded later September 23:** Mo selected the count-neutral introduction “Explore our products. Find your starting point.” The [chosen introduction and refined stories](products-heading-final.md) remove the comparison controls, replace the repeated NuriCell science image, and add illustrated highlights to each story. This document preserves the earlier review.

Mo rejected the oversized NuriCell treatments. The active Lineup restores the bottle sizes, central column width, tilts, and soft shadows from `reference/products-section/2026-09-23-before-elegant-variants/`. The arch, pedestal, and oval frames are removed. A quiet “BiGH’s flagship formula” caption remains beneath NuriCell’s name. Approved product PNGs are unchanged.

The white background and centered Elegant typography remain. Bottom-right 1–2–3 controls now compare wording only, preserving the selected product and the bottle sizes. No new option has been approved yet; option 1 is the initial preview.

## Three copy options

1. **Cells — Small cells. Big possibilities.**

   Good health starts small. Meet NuriCell, our flagship for cellular health and mental energy, and explore four more formulas with distinctive stories in science and nature.

2. **Life — Your life is full. Keep it that way.**

   From NuriCell’s focus on cellular health and mental energy to plant-based antioxidant support, explore five formulas made for everyday wellbeing.

3. **Science — The science runs deep. The purpose is you.**

   Our flagship NuriCell was formulated by Dr. Jian Kang Liu and Dr. Iris Wang. Discover it alongside four distinctive formulas, united by BiGH’s focus on everyday wellbeing.

New wording and comparison controls have draft translations in all five languages. Existing approved product stories and dialog copy are preserved. Public copy uses only Dr. Iris Wang’s public name.

## Story panels

Each selected bottle reveals its own full-bleed editorial image on the left with a readable white headline over a dark gradient. The approved description and Discover button sit on a pale product-colored background on the right. On phones the image sits above the copy. Previous/next controls sit at the top-left of the image, clear of the headline comparison controls.

| Product              | Image                              | Asset                                                  |
| -------------------- | ---------------------------------- | ------------------------------------------------------ |
| NuriCell             | Existing stylized mitochondrion    | `public/images/science/comparison/01-inside-cell.webp` |
| Green Bee Propolis   | Bee on a resinous green shoot      | `public/images/products/stories/propolis-v1.webp`      |
| Advanced OPC Formula | Grapes, grape seeds, and pine bark | `public/images/products/stories/opc-v1.webp`           |
| Turmerific           | Turmeric roots and powder          | `public/images/products/stories/turmeric-v1.webp`      |
| Nature Calm          | Quiet misty lake                   | `public/images/products/stories/calm-v1.webp`          |

The four new images were generated with the **built-in image_gen tool**, one call per image. They are illustrative artwork, not documentary photographs of suppliers, harvest sites, or proof of product effects. Nature Calm’s landscape conveys mood without implying unconfirmed ingredients. The reused NuriCell art is a stylized illustration, not a microscopy photograph.

The full final prompts and generation mode are saved in [story-image-prompts.json](../reference/products-section/story-image-prompts.json). Full-resolution originals are preserved as `reference/products-section/story-image-originals/{propolis,opc,turmeric,calm}-v1.png`; the served 1200 × 800 WebP copies total about 347 KiB. Original generated files also remain in Codex’s generated-images folder. Assets were compressed using Sharp; no visual content was edited after generation.

The superseded four source files were preserved in `reference/products-section/2026-09-23-before-story-imagery/`. Earlier comparisons remain available via the existing `ProductsSection` design modes.

## Verification

- Inspected the English desktop and phone layouts and all four new image panels, plus a Korean phone layout.
- Checked all three headlines across five languages at 320, 768, and 1440px. One option is selected at a time and bottle proportions stay constant when switching copy.
- Checked all five stories in all five languages at 320px: all images loaded and the floating navigation did not overlap the title.
- A final screenshot caught a 5px sideways scroll caused by a rotated bottle’s transparent bounds. The product section now clips horizontal paint overflow; verified document scroll width equals client width at 320, 390, 768, and 1440px.
- Actual pointer and keyboard interactions verified next/previous stories, bottle arrow-key navigation, headline arrow-key navigation, and opening/closing the NuriCell dialog.
- Changed-code lint and formatting passed. The production build compiled, passed TypeScript, and generated 10 static pages after allowing Google Fonts network access. An initial sandboxed build could not reach Google Fonts; no code change was needed for that failure.
- Browser checks use Chromium viewport emulation, not physical phones or Safari. Reduced-motion preferences disable the image hover transition.

Public demo: https://bigh-website-demo.vercel.app/#products. Deployment and anonymous access verification are tracked in [public-demo.md](public-demo.md).
