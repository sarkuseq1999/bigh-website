# BiGH — homepage preview

**Public demo: https://bigh-website-demo.vercel.app/** — opens without a login or access code. Use this same address for future demo updates; see [publishing instructions](docs/public-demo.md).

**Driving the build from this repo? Start with the [handoff of September 24, 2026](docs/handoff-2026-09-24.md).**

A fresh homepage using the existing stack. Mo selected Deep Space for the opening hero on September 22, 2026. It uses the approved cellular-health copy, a redesigned cell animation with subtle local movement. See [the current animation and preview](docs/deep-space-natural-motion.md), plus [the earlier comparison history](docs/hero-comparison.md). The [earlier animated-cell trial](docs/cellular-hero-preview.md) is preserved.
The [current section-order trial](docs/cellular-health-comparison.md) places Dr. Jiankang Liu's existing white section second and the original dark “Inside the cell” design third. Comparison controls are hidden so Mo can review the full-page flow. All six comparison designs and the [first implementation](docs/cellular-health-section.md) are preserved for reference.
That dark illustration now has [slow background drift and glowing orange folds](docs/mitochondria-glow.md), with soft blue light, floating particles, one pause control, and a still version for reduced-motion preferences.
Mo accepted that order and selected **choice 2, The Lineup**, on September 23. Section four now uses the [refined white product lineup](docs/products-lineup-refinement.md): NuriCell leads the five-bottle collection, and selecting any bottle reveals its approved product story. The design switcher is hidden. The [three comparison designs](docs/products-collection-comparison.md) remain available through `design="comparison"`; the [previous NuriCell spotlight](docs/nuricell-spotlight.md) and original layout remain available through `design="spotlight"` and `design="original"` on `ProductsSection`.
The [earlier redesign notes](docs/timeline-redesign.md) cover the rest of the existing preview, its asset sources, interactions, and verification.
Mo approved the count-neutral introduction **“Explore our products. Find your starting point.”** The [current product section](docs/products-heading-final.md) keeps the earlier bottle proportions, Elegant typography, and subtle flagship caption. The comparison controls are removed. NuriCell now has its own coastal-walk artwork, and every product story has two illustrated highlights with a separate supporting detail or scientist credit. The white Lineup remains selected; the [earlier story review](docs/products-story-imagery.md), [elegant variations](docs/products-elegant-variants.md), and [heading choices](docs/products-heading-options.md) are preserved.
Customer stories follow Products. After three rounds of designs, **Mo chose Still life** on September 24: everyday objects float around the real product bottle on a cobalt field, beside a big serif quote and a product link. No customer photos or drawn people are used. She called it "okay for this section" and plans to polish it later. The approved two NuriCell samples and one Green Bee Propolis sample remain visibly labeled as fictional in all five languages. See [the stories rounds and decisions](docs/customer-stories-v2.md). Genuine reviews still need sourcing.
"Make sense of the science." now follows the stories, as in Mo's approved homepage plan. After two rounds, **Mo chose the [Glass cell](docs/science-section.md)**: a warm-gold glass mitochondrion with real 3D depth, after Timeline, her favorite reference. Topic tabs (Mitochondria, Free radicals, Aging cells) show where you are, and each topic has its own picture: energy flowing out, antioxidant droplets catching free radicals inside the glass, and an age slider that turns the cell into a second render of itself grown old. The older research list and "Our purpose" block remain below it until Mo decides whether they move to the Science and About pages. The closing block, ["Start with your cells."](docs/closing-section.md), was built in three looks and then set aside at Mo's request: the page ends on the research list and "Our purpose", and the block stays in the repo unrendered. The research list grew from 4 to 36 checked sources with three filters (Science, Ingredients, Guides); see [research list candidates](docs/research-list-candidates.md).
The [first-preview notes](docs/homepage-preview.md) retain earlier provenance and pending launch content.
The [header and language update](docs/header-and-languages.md) adds Log in, Sign up, and a five-language selector at the upper right. English, Simplified Chinese, Korean, Vietnamese and Japanese now have homepage translations, including the product and help dialogs. Log in links to `https://bigh-vn-demo.vercel.app`, as supplied by Mo. Sign up remains a placeholder until he provides its link. Shopping and live question submission are not connected.

For the current brand direction, audience, markets, and open decisions, see the
[BiGH brand & website cheat sheet](BRAND-CHEATSHEET.md).

## Run locally

```sh
npm ci
npm run dev -- --hostname localhost --port 3000
```

Open http://localhost:3000. Build for production with `npm run build`, then run it with `npm start`.

## Stack kept

- Next.js 16.2.6, React 19.2.4, TypeScript 5, and Tailwind CSS 4.
- shadcn/Base UI components, Lucide icons, GSAP, Motion, Three.js, and next-themes remain installed.
- next-intl keeps the existing language routes: `/`, `/kr`, `/jp`, `/cns`, `/hken`, `/vn`.
- Every dependency and its locked version is unchanged.

## Start building here

- `src/app/[locale]/page.tsx`: homepage entry.
- `src/components/home/`: homepage content, interactions, and responsive styles.
- `src/app/[locale]/layout.tsx`: document and language provider.
- `src/app/globals.css`: shared base styles.
- `src/components/ui/`: reusable UI primitives.
- `messages/`: empty translation dictionaries; missing keys can fall back to English.
- `public/images/`: original hero artwork and referenced product/scientist images.
- `reference/`: reserved for new reference materials for this fresh website.

Run `npm run lint`, `npm run type-check`, `npm run format:check`, and `npm run build` to check changes.

## Previous website

The original website remains on `golden-hour-home` at commit `c2fae2e`.
This restart is on `codex/blank-start`.

Old source, copy, images, screenshots, scripts, and design documents are saved in
`old-storage/previous-site/`. This is storage only. Do not use the old design,
content, or product assumptions unless Mo explicitly asks. The archive is excluded
from TypeScript, lint, formatting, and Tailwind source scanning. Its images are not
served by the new website.

`reference/` is separate and reserved for new reference materials. It contains the
new MotionSites reference recordings and notes. Reference materials are
also excluded from code checks and are not served by the website.

Old pages, menus, animations, contact form, redirects, sitemap, and asset-copy build
hooks have been removed from the active site. A separate Vercel preview was deployed
with Mo's approval; its URL and access requirements are in the preview notes above.

The preview asks search engines not to index it. Revisit the metadata and
`robots.ts`, and restore appropriate redirects and a sitemap before launching the
rebuilt website.
