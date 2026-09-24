# Unified product collection — September 22, 2026

**Update, September 23:** Mo selected choice 2, The Lineup. The [refined lineup](products-lineup-refinement.md) is now active, with the design switcher hidden. All three implementations documented below are preserved as the earlier comparison, available through `design="comparison"`.

Mo requested three designs combining flagship NuriCell and the four other products in one large white section. This replaces the active spotlight-plus-separate-collection presentation. The approved Deep Space hero, white Dr. Liu section and original dark Inside the cell section remain first, second and third.

## Three designs for review

1. **Gallery:** NuriCell's headline, large bottle and short story on the left, with the four other products in a two-by-two gallery on the right. Pale circles, soft bottle shadows and subtle hover movement give each product a distinct presentation.
2. **The Lineup:** all five bottles across a shared white shelf, with NuriCell larger in the centre. The flagship story follows beneath the bottles. Phone layouts put NuriCell and its explanation first, followed by the other four bottles in two columns.
3. **Editorial:** a spacious flagship story, oversized NuriCell bottle and a compact four-product index. Tablet and phone layouts stack the feature and move the index below it.

The bottom-right 1–2–3 switcher appears while the section is in view. Arrow keys, Home and End also change designs. Switching from farther down a design returns the viewport to the section's beginning. Option 1 is the initial view only; Mo has not selected a winner. The controls are for design review and should be removed after selection.

## Content and assets

- All five approved transparent PNGs from `public/images/products/` are used without changes or generated replacements. Product-dialog images now use these same approved assets.
- The accepted NuriCell headline, mitochondrial-health description and joint credit to Dr. Jian Kang Liu and Dr. Iris Wang are unchanged. No ingredient list appears in the feature.
- The four companion products use their approved short headlines, including the Minas Gerais origin for Green Bee Propolis. Their existing product-preview dialogs retain the longer descriptions.
- All product buttons open the correct existing preview dialog. Complete product pages and checkout are still outside this design task.

## Files and restoration

- `src/components/home/products-collection-comparison.tsx` and its CSS module contain the three new designs and switcher.
- `src/components/home/products-section.tsx` retains all three presentation modes.
- `src/components/home/homepage.tsx` selects `design="comparison"` and supplies the existing dialog handler.

Set that prop to `design="spotlight"` to restore the previous white flagship feature and separate range, or `design="original"` to restore the original products layout. No whole-page rollback is needed. The original source, styles and images remain backed up in `reference/products-section/2026-09-22-original/`. The original `homepage.module.css` hash remains `2618A6FAF201FC571C6B216F906CD26DA62EFA8C608B184AEF03AD8DBB35F72F`.

## Verification

- Checked all three layouts at 320, 390, 760, 761, 1024, 1101 and 1440px. Each loads five bottle images, reports a white section background, keeps exactly one design selected and has no horizontal page overflow.
- Inspected screenshots of all three designs at desktop, tablet and phone widths. Fixed a missing space between the two introductory sentences in The Lineup and improved the flagship image's responsive size hint.
- Tested all five product dialogs in each design, including loaded images, correct headings, Escape dismissal and focus restoration. Also checked The Lineup's second NuriCell button and phone keyboard activation.
- Checked arrow-key/Home/End selection, returning to the section top when switching from below, controls hiding at the hero, and the original first-four-section order.
- Reduced-motion mode reports zero animations in the collection. Final local browser console: zero errors or warnings.
- Lint, TypeScript, changed-code formatting and the local production build passed. The build generated all 10 pages.
- Screenshots: `reference/products-section/collection-comparison-qa/`. Responsive checks used a desktop browser, not a physical phone or Safari.

## Preview

Protected preview: https://bigh-website-qks7l30up-sarkuseq1999s-projects.vercel.app/#products

Deployment `dpl_FBxBrd7kWWLp6qd5zz2xeasewDAd` reported READY. Its hosted build compiled, passed TypeScript and generated all 10 pages. The preview still redirects to the Vercel login gate; protection was not disabled and production was not promoted. Browser layout and interaction checks above were local; the hosted design was not visually checked behind the login gate.
