# Customer stories: three visual choices

September 23, 2026. Mo found the original paper-card section dull and asked for three more visually appealing, fun designs. These replace the active presentation for review; no new design has been chosen yet.

## Compare on the website

Open https://bigh-website-demo.vercel.app/#stories and use the sticky 1 / 2 / 3 controls:

1. **Daybook:** warm peach backdrop, a tilted photo with tape, botanical flower details, a floating product cutout, and a large editorial quote. Three image selectors and previous/next buttons browse the samples.
2. **Story Wall:** a lavender backdrop with all three stories visible on staggered peach, cream, and sage cards. Each has a different image, numbered sticker, full quote, and product link. Cards lift on hover/focus and stack on phones.
3. **Spotlight:** deep forest green, oversized circular photography, lime details, subtle orbit lines, and larger quote typography. Image selectors and previous/next buttons browse the samples.

Daybook is initially shown. Switching design preserves the selected story and brings the section's introduction back into view. The controls stay reachable while scrolling the tall mobile gallery. They are temporary review controls, not a final customer-facing feature.

## Content and assets

The previously accepted sample stories are unchanged: Lisa M. and Michael R. for NuriCell, Susan L. for Green Bee Propolis. The section-wide fictional-sample notice and each story's sample/reviewer labels remain visible in all five languages. No ratings, verified-purchase badges, or fabricated customer portraits were added.

Three new decorative still-life scenes were generated with the **built-in image_gen tool**. They illustrate morning routines, curiosity, and botanical origins; they do not depict actual customers or document a product's source or ingredients. The section labels the scenes as illustrative.

Website assets:

- `public/images/stories/morning-v1.webp`
- `public/images/stories/curiosity-v1.webp`
- `public/images/stories/botanical-v1.webp`

The PNG originals are preserved under `reference/customer-stories/artwork/`. The exact final prompt set is saved in [artwork-prompts.json](../reference/customer-stories/artwork-prompts.json). WebP files are 1000×1000, about 174/76/171 KB respectively. Product cutouts are the existing approved PNGs; their labels were not regenerated.

The previous component and stylesheet are preserved in `reference/customer-stories/2026-09-23-paper-version/`. Its original [implementation notes](customer-stories.md) remain available. Products and the other homepage sections are unchanged.

## Verification

Desktop and phone screenshots of all three designs were visually inspected. Browser checks covered all five languages at 320px and 1440px. After adjusting the comparison controls on narrow screens, all 15 language/design combinations at 320px had exactly one design selected, no clipped controls, and no horizontal visible-text overflow. The screen-reader-only status is deliberately clipped.

Clicked the story controls and tested keyboard selection. Product links opened the expected NuriCell or Green Bee Propolis dialog in every layout. Escape closed the dialog and restored focus. The sticky comparison controls remained available at the bottom of the mobile gallery; switching returned the introduction to view. Reduced-motion mode disabled the entrance animation. Changed-file ESLint passed; the production build compiled, passed TypeScript, and generated all 10 pages.

Hosted verification is recorded in [public-demo.md](public-demo.md).
