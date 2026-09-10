# BiGH — blank start

A fresh website canvas using the existing stack. The homepage is intentionally blank.

## Run locally

```sh
npm ci
npm run dev
```

Open http://localhost:3000. Build for production with `npm run build`, then run it with `npm start`.

## Stack kept

- Next.js 16.2.6, React 19.2.4, TypeScript 5, and Tailwind CSS 4.
- shadcn/Base UI components, Lucide icons, GSAP, Motion, Three.js, and next-themes remain installed.
- next-intl keeps the existing language routes: `/`, `/kr`, `/jp`, `/cns`, `/hken`, `/vn`.
- Every dependency and its locked version is unchanged.

## Start building here

- `src/app/[locale]/page.tsx`: blank homepage.
- `src/app/[locale]/layout.tsx`: document and language provider.
- `src/app/globals.css`: neutral base styles.
- `src/components/ui/`: reusable UI primitives.
- `messages/`: empty translation dictionaries; missing keys can fall back to English.
- `public/`: add new public assets here.
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

`reference/` is separate and reserved for new reference materials. It starts empty
apart from `.gitkeep`, which lets Git preserve the folder. Reference materials are
also excluded from code checks and are not served by the website.

Old pages, menus, animations, contact form, redirects, sitemap, and asset-copy build
hooks have been removed from the active site. No deployment was performed.

The blank draft asks search engines not to index it. Revisit the metadata and
`robots.ts`, and restore appropriate redirects and a sitemap before launching the
rebuilt website.
