# bighnow.com Clone Rebuild — Design Spec

**Date:** 2026-07-01 · **Approved by Mo in chat** (bigh-skills session)

## Goal

Replace the hacked WordPress site (mega888 spam injected on all 147 pages) with a
clean 1-to-1 content clone on this repo's stack, deployed to Vercel (Pro), then cut
the domain over safely. The separate brand-redesign project (NuriCell hero, Dr. Liu —
see Dropbox `bigh-website/_PROJECT-STATUS.md`) builds on top of this later.

## Scope

- **In:** same pages, same content (spam-stripped, worst disease claims removed),
  modernized look ("enhance license" from Mo), mobile-first, fast images, hreflang,
  301 redirects from old URLs, iMatrix link-outs preserved verbatim.
- **Out:** new branding/copy, checkout/login (stays on iMatrix/office2office),
  mainland-China delivery, Bluehost directory move (Phase 5, later decision).

## Facts (verified 2026-07-01)

- Site = brochure only; all commerce links out to
  `backoffice.office2office.com/...` with per-product cart params (captured in harvest).
- 147 pages across 6 locales: en 26, cns 25, hken 25, jp 25, kr 25, vn 21
  (VN genuinely has fewer pages). ~25 page types; 12 products.
- Product page "content" is largely brochure PNGs (text baked into images) + a Buy Now link.
- Spam pattern: hidden off-screen `<a>` (left:-4741px, "mega888" → free3d.org),
  2 per page, all 147 pages. Stripped during harvest; 0 leftovers verified.
- Old URL scheme: suffixes (`/nuricell_kr`) + locale homes (`/kr`). New scheme:
  `/[locale]/[slug]` via next-intl. Redirect map needed for SEO.

## Architecture

1. **Harvest** (`scripts/harvest_bighnow.py`) → `content/harvest/<locale>/<slug>.md`
   (JSON frontmatter: source_url, title, images, external_links) + `content/harvest/assets/`
   (100 wp-content images) + `_manifest.json` (audit incl. every spam removal). ✅ DONE
2. **Build**: Next.js 16 + next-intl `[locale]` routes reading harvested content;
   shared header/footer/lang-switcher; product template; `next.config.ts` redirects
   for every old URL; hreflang metadata; next/image for all assets (moved to `public/`).
3. **Review**: Vercel preview URL → Mo iterates.
4. **Cutover**: record ALL Bluehost DNS records first (MX = Microsoft 365 — must not change);
   keep nameservers at Bluehost; point website A/CNAME to Vercel only. Rollback = restore A record.
5. **Aftercare**: Google Search Console re-crawl + spam-URL cleanup; later: directory move
   + Bluehost cancellation (separate decision with Mo).

## Risks / notes

- Email: only touched if nameservers move (they don't in Phase 4).
- Disease claims: strip worst offenders during build (light pass; full rewrite = redesign project).
- Vercel Hobby forbids commercial use → Mo upgrades to Pro before cutover.
- `messages/*.json` in repo have uncommitted edits from the earlier homepage experiment — untouched.
