# Product heading review — September 23, 2026

**Later decision:** Mo selected the Elegant direction and requested stronger wording plus greater flagship emphasis. The [three elegant variations](products-elegant-variants.md) now replace these three earlier options. A snapshot of this implementation is saved in `reference/products-section/2026-09-23-before-elegant-variants/`.

Mo asked to remove the repeated “THE BIGH COLLECTION” label, replace “Meet the BiGH collection” and its introduction, and remove the “OUR FLAGSHIP” badge above NuriCell. He requested more creative design directions and allowed multiple choices.

The selected five-bottle Lineup remains in place. Only the introduction and the unnecessary flagship labels changed. NuriCell still leads through its central position, larger bottle, and initial story selection. Its story label now simply reads “NuriCell”; its approved description and joint formulator credit are unchanged.

## Three live options

1. **Bold — “Good science. For real life.”** Large left-aligned headline, blue italic second line, and a short introduction on the right with a fine vertical rule. A divider connects it to the bottles below. This is the initial option for review, not an approved winner.
2. **Elegant — “Small beginnings. Fuller lives.”** Centered composition with a smaller opening line and larger italic second line. A short cellular-health introduction sits beneath it.
3. **Expressive — “Your daily dose of possibility.”** Oversized blue serif emphasis with a hand-drawn underline and a conversational introduction.

The bottom-right 1–2–3 controls now compare these **headings**, not the original three product layouts. They appear only while the products section is in view. Choosing from farther down the section brings the heading back into view. Arrow keys, Home, and End also change the option. All copy and control labels are included in the five language catalogs.

## Implementation and preservation

- `src/components/home/products-lineup-intro.tsx` and its CSS module contain the options and temporary review controls.
- `products-lineup.tsx` renders the new introduction. Its bottle tabs, product stories, and preview-dialog triggers are preserved.
- Previous lineup source and CSS are saved in `reference/products-section/2026-09-23-lineup-before-heading-review/`.
- The earlier Gallery/Lineup/Editorial comparison is still intact and remains available via `design="comparison"` on `ProductsSection`.
- All five approved product images are unchanged. No dependencies, scientific claims, product formulas, or checkout behavior were changed.

## Verification

- Compared all three options visually on English desktop and phone views; inspected Korean and Vietnamese phone views.
- Checked all three designs in all five languages at 320, 760, and 1440px: 45 combinations, with no horizontal page overflow or heading/description/underline overlaps. English was also inspected at 390px.
- Confirmed the visible repeated label, old heading/subheading, bottle badge, and redundant flagship story label are gone.
- Keyboard selection reports exactly one pressed option; controls hide at the hero and return to the heading when used from below.
- All five bottle selections still show their matching story. The Nature Calm dialog opens and closes with Escape.
- Reduced-motion mode was used for comparison captures; the new heading options do not add animation.
- Changed-file lint and formatting passed. The production build compiled, passed TypeScript, and generated all 10 pages.
- Screenshots: `reference/products-section/heading-{1,2,3}-desktop.png`, `heading-{1,2,3}-phone.png`, and translated phone captures. These use desktop Chromium emulation, not physical phones or Safari.

Public review address: https://bigh-website-demo.vercel.app/#products. Deployment and anonymous access verification are recorded in `public-demo.md`.

Deployment `dpl_A2c5EE4oqh8rGLdtgdEBWBSGsMuM` reported READY and is now assigned to that public alias. A fresh anonymous browser received HTTP 200, switched all three headings, confirmed the requested removals and five loaded bottles, and opened the NuriCell dialog from a phone-sized viewport. No page or console errors occurred. Hosted desktop and phone screenshots were captured and visually inspected.
