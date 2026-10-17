# BiGH website

**Public demo: https://bigh-website-demo.vercel.app/** — opens without a login or access code. Use this same address for future demo updates; see [publishing instructions](docs/public-demo.md).

**Building this site (Claude Code or Codex)? Start with [`AGENTS.md`](AGENTS.md), the shared rulebook, and [`docs/HANDOFF.md`](docs/HANDOFF.md), the current state.**

The new BiGH website in its "Ink & Gold" look: hand-painted ink on rice paper, one gold leaf where energy is meant, calm type for older readers. It has a homepage, About, Science, Support and a page for each of the five products (NuriCell, Green Bee Propolis, Advanced OPC Formula, Turmerific, Nature Calm), in English, Korean, Japanese, Simplified Chinese and Vietnamese.

- [`DESIGN.md`](DESIGN.md): the design system.
- [`PRODUCT.md`](PRODUCT.md): products, credits, brand commitments and honesty rules.
- [`BRAND-CHEATSHEET.md`](BRAND-CHEATSHEET.md): product facts and Dr. Liu's story. Its design notes describe the September site that Ink & Gold replaced.
- `docs/`: notes for each piece of work. Notes dated before October 2026 mostly describe designs that were later replaced.

## Run locally

```sh
npm ci
npm run dev -- --hostname localhost --port 3007
```

Open http://localhost:3007. Build for production with `npm run build`, then run it with `npm start -- --hostname localhost --port 3006`. Browser checks live in [`scripts/qa/`](scripts/qa/README.md).

## Stack kept

- Next.js 16.2.6, React 19.2.4, TypeScript 5, and Tailwind CSS 4.
- shadcn/Base UI components, Lucide icons, GSAP, Motion, Three.js, and next-themes remain installed.
- next-intl keeps the existing language routes: `/`, `/kr`, `/jp`, `/cns`, `/hken`, `/vn`.

## Start building here

- `src/app/[locale]/page.tsx`: homepage entry; the homepage itself is `src/components/home-v2/look-ink/`.
- `src/components/ink/`: the shared Ink & Gold kit (menu bar, footer, dialogs).
- `src/components/product/`: the product page template; each product's content is one file in `src/components/product/products/`.
- `src/components/about/`, `src/components/science/`, `src/components/support/`: the other pages.
- `src/app/globals.css`: shared base styles.
- `messages/`: translations.
- `public/images/`: the pictures the site shows; `reference/ink-pages/`: their originals, prompts and build scripts.

Run `npm run lint`, `npm run type-check`, `npx prettier --check <changed files>`, and `npm run build` to check changes.

## Previous website

The original website remains on `golden-hour-home` at commit `c2fae2e`.

Old source, copy, images, screenshots, scripts, and design documents are saved in
`old-storage/previous-site/`. This is storage only. Do not use the old design,
content, or product assumptions unless Mo explicitly asks. The archive is excluded
from TypeScript, lint, formatting, and Tailwind source scanning. Its images are not
served by the website.

`reference/` holds reference materials for the new website. Reference materials are
excluded from code checks and are not served by the website.

The preview asks search engines not to index it. Revisit the metadata and
`robots.ts`, and restore appropriate redirects and a sitemap before launching the
rebuilt website.
