# BiGH product enhancement review

Created September 18, 2026 using the built-in image generation tool in edit mode. The exact first-pass prompts are in `prompts.md`. No API/CLI image fallback was used.

## Approval

Mo reviewed all five enhanced versions and approved them for future product images on September 18, 2026. Verified identical copies are now saved in `public/images/products/`, with the canonical mapping in `docs/brand-assets.md`. The original files, comparison page, generation history, and review limitations below remain available for reference.

## Selected deliverables

- `public/experiments/green-bee-propolis-enhanced-transparent.png`
- `public/experiments/advanced-opc-enhanced-transparent.png`
- `public/experiments/turmerific-enhanced-transparent.png`
- `public/experiments/nature-calm-enhanced-transparent.png`
- The earlier approved `public/experiments/nuricell-enhanced-transparent.png` is also included.
- Review page: `public/experiments/products.html`
- Download bundle: `public/experiments/bigh-enhanced-product-pngs.zip`

The four new delivered PNGs are exact copies of the first-pass generated files. Their native alpha is preserved. Original product files and homepage product references have not been changed.

## Transparency checks

The tool's inline image viewer displayed nearly transparent white pixels as conspicuous white remnants. A targeted cleanup pass was attempted, but not selected because direct browser rendering showed the first-pass files correctly. For example, the apparent white area above the Green Bee cap had alpha 1/255, while the cap was 253/255. The generated alpha remains untouched. White cap, shoulder, label, and base samples are 252–254/255; backgrounds contain over 838,000 fully transparent pixels per new image. All four were visually inspected on dark browser backgrounds, and Turmerific was also checked against a checkerboard at phone width.

The comparison display uses bounds above alpha 8/255 to align the visible bottles, excluding almost invisible exterior pixels. This is CSS framing only; downloads retain every original generated pixel. The read-only image inspection and manifest builder is `build-comparison-data.mjs`.

## Review limitations

These are generated review concepts, not exact reproductions of every label pixel. Product names and front capsule counts were visually checked: Green Bee 60, Advanced OPC 120, Turmerific 60, Nature Calm 90. Small side-panel print has not been verified character by character and should not be treated as accurate label artwork.

- Green Bee: lighting is more dimensional; honeycomb geometry and small print differ. The source phrase “Strengths Body Defenses” is retained.
- Advanced OPC: fruit artwork and small curved printing differ; review the curved text particularly closely.
- Turmerific: illustration and small benefit badges differ. Main front benefit lines and 60-capsule count remain visible.
- Nature Calm: connected circles and meditation artwork differ slightly; green is stronger.
- NuriCell: the previously disclosed circuit-art and label-geometry differences remain.

## Website checks

Opened all five pairs in the browser. Verified 10 loaded images, shared 250% zoom transforms on every bottle, dark/checkered background controls, working product anchors, and two columns without horizontal overflow at 390px phone width. The ZIP contains all five enhanced PNGs and the local download URL returned HTTP 200. Formatting was checked with Prettier.

## Hosted preview

https://bigh-website-4j6jy61te-sarkuseq1999s-projects.vercel.app/experiments/products.html

Vercel preview deployment `dpl_FifAzimPLK8Sib7Agt6WTS8AkCAd` completed successfully. Opened this hosted page and verified all 10 images loaded, with the Green Bee pair visibly displayed against a checkerboard. Existing Vercel sign-in protection remains enabled.
