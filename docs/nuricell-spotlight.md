# NuriCell homepage spotlight — September 22, 2026

This design is preserved as `ProductsSection design="spotlight"`. The active page now shows the [three unified white collection designs](products-collection-comparison.md) requested next by Mo. The description and verification below record the earlier spotlight implementation.

Mo accepted the first three sections in their new order and authorized building the NuriCell section. He also explicitly asked to preserve the existing products design so it can be restored later.

## Current design

The fourth section introduces NuriCell on a white background after the dark Inside the cell section. A large approved bottle sits on the left over a pale blue circle and oversized NuriCell lettering. The approved headline and short product explanation sit on the right. On phones and smaller tablets, the heading, bottle and description stack. The four existing collection cards follow beneath it with their previous presentation and content.

Exact approved wording:

- Label: **MEET NURICELL**
- Headline: **Stay sharp. Live fully.**
- Description: **Our flagship supplement focuses on the health of your mitochondria—the tiny power plants that supply energy for your brain and body.**
- Credit: **Formulated by mitochondrial researcher Dr. Jian Kang Liu and Dr. Iris Wang.**
- Button: **Discover NuriCell**

The feature does not list ingredients or add new efficacy claims. The button opens the existing product-preview dialog; a complete product page and shopping are still outside this section's scope. The NuriCell dialog now uses the same approved bottle image. Ingredient details remain in that dialog.

## Files and restoration

- `src/components/home/nuricell-spotlight.tsx` and `.module.css`: new feature and responsive styles.
- `src/components/home/products-section.tsx`: extracted products section with `original` and `spotlight` modes. `homepage.tsx` currently passes `design="spotlight"`.
- `public/images/products/nuricell.png`: existing approved transparent image, 1230 × 1278. It was not edited or regenerated; its proportions and transparency are preserved. CSS provides the circle, lettering, tilt and shadow.
- The original `homepage.module.css` remains byte-for-byte unchanged.

To restore the previous products design, change that one prop to `design="original"`. The original version is still implemented. [Backup, screenshots, asset hashes and restore instructions](../reference/products-section/2026-09-22-original/README.md) are saved under `reference/products-section/2026-09-22-original/`. The backup includes complete original source/styles, extracted section markup, all five original bottle images and desktop/phone screenshots. No git reset or whole-page rollback is needed.

## Verification

- Mounted the original mode and checked its prior heading, visual layout and five buttons before selecting the spotlight. Original source/style and five asset copies were hash-verified. The original stylesheet's hash remains unchanged.
- Checked the new section at 320, 390, 768, 800, 801, 1024, 1440 and 1920px. Approved description and formulator credit match exactly; images load; the button stays within the viewport; no ingredient list appears in the feature; no horizontal overflow remains. The first four sections stay `home`, `scientists`, `cellular-health`, `products`.
- Found and fixed narrow-screen overflow caused by the rotated image's transparent bounds. Refined the tablet circle so it remains round instead of clipping at the top/bottom. Inspected desktop, phone and tablet screenshots; the tablet refinement was rechecked.
- All five product buttons open the correct dialogs, with loaded images, Escape dismissal and focus restoration. Phone keyboard activation works. Reduced-motion mode reports zero animations in the NuriCell feature.
- Lint, TypeScript, changed-code formatting and the final local production build passed; all 10 pages were generated. Final local browser console: zero errors and warnings.
- Screenshots: `reference/products-section/nuricell-spotlight-qa/`. Checks used a desktop browser at responsive widths, not a physical phone or Safari.

## Preview

Current protected preview: https://bigh-website-cam6dvk4o-sarkuseq1999s-projects.vercel.app/#products

Deployment `dpl_n2dzVotA3Cxc1c2DhsBosE6WRPQB` reported READY. The hosted build compiled, completed TypeScript and generated all 10 pages. Visual and interaction checks above were local. The preview retains its existing login protection; production was not promoted. The hosted page was not visually checked behind the login gate.
