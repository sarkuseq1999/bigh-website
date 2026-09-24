# Selected product lineup — September 23, 2026

**Later feedback:** Mo requested a more creative heading and removal of the repeated collection label and bottle badge. The [three heading options](products-heading-options.md) now replace the introduction below. The Lineup remains selected; the newly visible 1–2–3 controls compare headings only.

Mo selected choice 2, The Lineup, and requested stronger content and a more polished design. The active homepage now uses `design="lineup"` on `ProductsSection`.

## Presentation

- White section, five approved bottles, NuriCell larger in the center on desktop and first on phones.
- Soft product-colored light and shadows, restrained hover movement, concise purpose/origin labels, and a clear selected state.
- Selecting a bottle reveals its story below. NuriCell is the initial selection. The story background matches the selected product's accent.
- Previous/next controls also browse the five stories. On phones, choosing a product scrolls to its story. Reduced-motion preferences disable the smooth scroll and transitions.
- Each story's Discover button opens the existing corresponding product-preview dialog.
- The design-review 1–2–3 switcher is no longer shown on the active page.

## Content

The story panels use the previously approved copy recorded in `BRAND-CHEATSHEET.md`: NuriCell's mitochondrial focus and joint formulator credit; Green Bee Propolis's Minas Gerais origin; Advanced OPC's botanical antioxidants and free-radical explanation; the Longvida ingredient's UCLA development story; and Nature Calm's cellular-stress research story. No new clinical efficacy or blood-brain-barrier claim was introduced. Dr. Iris Wang is identified only by her public name.

Sixteen added strings cover the stories, short labels, and controls in English, Simplified Chinese, Korean, Vietnamese, and Japanese. Existing product names, approved PNG assets, and preview-dialog contents are preserved. Translations remain working copy, not a native-language editorial review.

## Preservation

- The earlier Gallery, Lineup, and Editorial implementations remain intact in `products-collection-comparison.tsx` and its CSS module. Set `design="comparison"` to restore all three choices.
- `design="spotlight"` and `design="original"` still restore the earlier presentations.
- New component: `src/components/home/products-lineup.tsx` and `products-lineup.module.css`.
- Before screenshot: `reference/products-section/lineup-before-refinement.png`.
- Final desktop screenshot: `reference/products-section/lineup-final-desktop.png`.
- Phone interaction screenshot: `reference/products-section/lineup-mobile-selected.png`.

## Verification

- Browser checks across all five languages at 320, 390, 768, and 1440px; also inspected the English layout at 1024px. All five story panels render without horizontal page overflow.
- Found and fixed a Korean desktop heading/navigation overlap, then rechecked it.
- Visually inspected English desktop, tablet, and phone views, the OPC story, and Korean/Vietnamese phone layouts.
- All five Discover buttons open the correct dialog; Escape closes each and returns focus to its trigger.
- Arrow keys, Home, and End select the correct product and move focus in visual shelf order. Previous/next controls wrap correctly. One panel and one selected tab are active at a time.
- Phone bottle selection brings its story to 150px below the viewport top, respecting the existing page scroll padding, and focuses the panel.
- Reduced motion reports zero product-section animations and a zero-second image transition. All five bottle images load. The section's computed background remains pure white.
- Final changed-code lint and formatting passed. The production build compiled, passed TypeScript, and generated all 10 static pages.
- The refreshed local page reported no console errors. Development-only image-loading hints appeared when opening directly at the section anchor; these are below-the-fold images in the normal homepage flow.
- Browser checks used desktop Chromium viewport emulation, not physical phones or Safari.

Public demo: https://bigh-website-demo.vercel.app/#products. See `public-demo.md` for the current deployment and anonymous access verification.

Published preview `dpl_HzoE7Dy7QR7dac3Qy6xEq536Cp7j` reported READY. The stable public alias was updated and verified in a fresh unauthenticated context: HTTP 200, all five story selections, working NuriCell preview dialog, phone selection/scrolling, no horizontal overflow, and zero page or console errors. Public desktop and phone screenshots are saved alongside the local reference captures.
