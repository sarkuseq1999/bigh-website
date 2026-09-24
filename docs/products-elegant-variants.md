# Three elegant product variations — September 23, 2026

**Superseded later September 23:** Mo rejected enlarging NuriCell and requested the previous bottle proportions. The current [story imagery and copy review](products-story-imagery.md) restores those proportions, keeps the subtle flagship caption, and offers three new copy options in the shared Elegant style. This document preserves the earlier experiment.

Mo selected the earlier **Elegant** heading direction, requested three new designs within that style with more interesting wording, and asked for NuriCell to stand out more clearly as the flagship. The selected five-bottle Lineup remains the foundation.

## Variations for review

1. **Signature:** “More life. In every day.” Centered typography and a pale blue arched backdrop behind NuriCell.
2. **Spotlight:** “Your next chapter starts within.” Blue italic emphasis, diffuse light, and a small raised display base beneath NuriCell.
3. **Portrait:** “The art of living. The science within.” A muted blue-gray headline, fine warm accent line, and double oval frame around NuriCell.

Every variation keeps the white section background and gives NuriCell a wider central column, a substantially larger bottle, a larger product name, and an unboxed **“BiGH’s flagship formula”** caption beneath its name. The caption also remains on phones, where NuriCell is the first full-width product. The previously rejected badge above the bottle is not restored. The introductions clearly identify NuriCell and its role, with the third variation highlighting its two formulators.

The bottom-right 1–2–3 controls now change the **heading and NuriCell presentation together**. Option 1 is the initial review state, not an approved winner. All three retain the centered, spacious, serif treatment Mo liked in Elegant. Mobile controls are condensed into one smaller row.

## Files and preservation

- `products-lineup.tsx` owns the selected design and passes it to `products-lineup-intro.tsx`. The corresponding CSS modules style the shared lineup and the three variations.
- Sixteen strings were added or reused across English, Simplified Chinese, Korean, Vietnamese, and Japanese. Translations remain draft copy without native editorial review.
- The immediately preceding heading review and lineup files are preserved in `reference/products-section/2026-09-23-before-elegant-variants/`.
- Earlier original, spotlight, and full-collection comparisons remain available through the modes on `ProductsSection`.
- The approved bottle images, product stories, dialog content, and scientist names were preserved. Public copy uses only Dr. Iris Wang's public name.
- Switching designs preserves the selected product story. NuriCell's frame/lighting and flagship caption remain visible even when a companion story is selected.

## Verification

- Inspected all three English desktop and phone screenshots plus the 768px tablet layout. Captures: `reference/products-section/elegant-{1,2,3}-desktop.png`, `elegant-{1,2,3}-phone.png`, and `elegant-tablet.png`.
- Checked 45 combinations: three designs, five languages, and widths of 320, 768, and 1440px. No horizontal page overflow or heading/description overlap; the flagship image element is at least 1.4 times the height of a companion image throughout those checks.
- Arrow keys, Home, and End update the heading and bottle treatment together with exactly one selected design button.
- Switching from a story brings the heading back into view after the new layout is applied. Controls disappear at the hero.
- All five product dialogs open correctly. Escape closes them and restores focus to the trigger. On phones, bottle selection focuses the corresponding story at the existing 150px scroll offset.
- Changed-code lint and formatting passed. The production build compiled, passed TypeScript, and generated all 10 static pages.
- Browser verification used desktop Chromium viewport emulation, not physical phones or Safari. Reduced-motion mode was used for the stable visual captures.

Public review address: https://bigh-website-demo.vercel.app/#products. See `public-demo.md` for the current deployment and anonymous access verification.

Published deployment `dpl_5Y7TBD5CPAvyZdo1F8eXkHvimdhq` reported READY and is assigned to the stable public alias. A fresh unauthenticated browser received HTTP 200, switched all three synchronized designs, confirmed the explicit flagship caption, loaded all five bottles, and opened the NuriCell dialog. The phone layout has no horizontal overflow and its compact controls measure 52px high. There were no page or console errors. Hosted captures `elegant-public-desktop.png` and `elegant-public-phone.png` were visually inspected.
