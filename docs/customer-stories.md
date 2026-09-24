# Customer stories — September 23, 2026

**Historical first design:** Mo subsequently found this presentation dull and requested three more playful alternatives. The active comparison is documented in [customer-stories-comparison.md](customer-stories-comparison.md); this paper version is preserved in `reference/customer-stories/2026-09-23-paper-version/`.

Mo accepted the current product section for now and asked to continue with the next section. The approved homepage content places customer experiences after Products. This implements that section using the three sample stories accepted on September 21: two about NuriCell and one about Green Bee Propolis.

## Presentation

- A deep-blue background follows the white product section.
- “In their own words.” introduces one large cream paper card, with two subtly rotated sheets behind it.
- Three story selectors emphasize morning routines, the science, and the product's source. Previous/next controls offer another way to browse. Nothing advances automatically.
- The story card includes its short heading, full quote, illustrative reviewer name, and a small approved product image. The product link opens the existing matching product dialog.
- The layout stacks on smaller screens. Controls support the keyboard, announce selection changes, and respect reduced-motion preferences.
- All new interface text is translated into English, Simplified Chinese, Korean, Vietnamese, and Japanese.

The prominent draft notice and each card's “Fictional sample” label remain visible. These are layout samples, not genuine customer feedback. There are no invented ratings, verified-purchase labels, or customer portraits. Replace the samples with permissioned, sourced feedback before presenting them as real reviews. Mo has not yet reviewed this new visual design.

## Files and preservation

- `src/components/home/customer-stories.tsx`
- `src/components/home/customer-stories.module.css`
- `src/components/home/homepage.tsx` places the component immediately after Products and removes the old small “customer stories coming soon” note.
- The previous homepage is preserved at `reference/customer-stories/2026-09-23-before/homepage.tsx`.
- The approved product section and its previous alternatives are unchanged.

## Local verification

The production build compiled, passed TypeScript, and generated all 10 pages. Changed-file ESLint and formatting checks passed. In the browser, all 45 combinations of five languages, three stories, and widths 320/768/1440 had no page or text-content horizontal overflow. The decorative rotated sheets intentionally extend beyond the card; the section clips their outer bounds. Exactly one story selector was pressed and sample labels were present in every combination.

Clicked next/previous controls and verified wraparound. Verified arrow-key, Home, and End selection. All three product links opened the correct dialog (NuriCell, NuriCell, Green Bee Propolis); Escape closed it and returned focus to the link. Reduced-motion mode disabled the story entrance animation. English desktop and phone, plus Korean and Vietnamese phone screenshots, were visually inspected.

Public deployment and anonymous-access verification are recorded in [public-demo.md](public-demo.md). Review the section at the stable demo address with `#stories`.
