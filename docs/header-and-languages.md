# Account controls and five languages — September 22, 2026

Mo requested Log in, Sign up and a language selector in the upper right, with English, Chinese, Korean, Vietnamese and Japanese.

## Implemented

- Desktop: understated Log in link, outlined Sign up button and globe/language selector in the top-right header. At intermediate widths navigation moves to a second row; phones use a compact utility row above the logo and menu.
- The selector offers English, 简体中文, 한국어, Tiếng Việt and 日本語. Chinese uses Simplified Chinese, matching the existing `/cns` route. Existing URL codes are retained: `/`, `/cns`, `/kr`, `/vn`, `/jp`.
- The previous `/hken` route redirects to `/cns`. It is not a sixth visible language or a Traditional Chinese translation.
- The active homepage, all three current product-collection options, product/scientist/education/help dialogs, account previews, motion controls, accessibility labels and page metadata use the selected language. Product names, approved bottle packaging, research journal names and external source pages remain as provided.
- Existing locale navigation preserves query/hash when switching, records the selected locale through next-intl's cookie and updates the document language tags to `en`, `zh-Hans`, `ko`, `vi` or `ja`.
- Language-specific headline sizing and system font fallbacks keep Japanese/Korean/Chinese readable; Vietnamese uses DM Sans with the supported Latin Extended subset and Times New Roman for serif accents (superseded on September 28, 2026: see "Vietnamese type" below). The existing animation and approved product imagery are unchanged.

## Vietnamese type — September 28, 2026

Mo chose **Be Vietnam Pro** for Vietnamese. Every other language stays on Switzer.

- **Why.** Switzer (Fontshare) lacks 92 of the 134 Vietnamese letters (ơ, ư, every dot-below and hook-above form), and DM Sans, next in the stacks, has no Vietnamese subset. Chrome filled the missing letters from Arial one by one, so Vietnamese words looked patchy on `/vn`, `/vn/products/nuricell` and `/vn/about`.
- **Licence.** Be Vietnam Pro is SIL Open Font License, so `next/font/google` self-hosts it (files served from `/_next/static/media`, no request to Google). Switzer is different: its licence forbids redistributing the files, so it keeps loading from Fontshare's stylesheet and must never be committed.
- **How it works.** One token, `--font-brand`, sits at the top of the three page shells' stacks (`homepage.module.css`, `product-page.module.css`, `about-page.module.css`: `--display-font`, `--sans`, `font-family`). `globals.css` sets it to `"Switzer"` on `:root` and to `var(--font-be-vietnam-pro)` on `html:lang(vi) body`. It must be set on `body` (or higher), because next/font's variable class is on `body` and a `var()` inside a custom property is resolved where it is declared; the shells, below `body`, then resolve to Be Vietnam Pro. The locale layout loads the font and adds its variable class for `vn` only.
- **Weights.** Be Vietnam Pro is static on Google Fonts; the layout loads 300, 400, 500, 600 and 700, upright and italic. Switzer's headline weights (450, 460) map to **400**: measured stems, 400 is 0.095–0.098 em against Switzer 460's 0.098–0.105 em, while 500 (0.115 em) is visibly bolder. The browser would pick 500 for 450/460, so `globals.css` sets `--font-brand-display-weight: 400` for Vietnamese and the headline rules read it with Switzer's value as the fallback (`--display-weight` in the three shells, the homepage's base `h1`–`h4` weight and the cellular title). Other weights map as usual: 500 labels, nav and the homepage hero title draw Medium; 550 draws SemiBold (600).
- **Size.** Not scaled. The x-heights match (0.53 em in both), so Vietnamese reads at the same size as English. Be Vietnam Pro's capitals are taller (0.75 vs 0.69 em) and it runs about 9% wider (median over the ~50 headings of the three pages), which adds a line to a few headings. The wrap fixes, all Vietnamese-only: `text-wrap: pretty` on `html:lang(vi) body` (inherited; rules that choose `balance` keep it), because Vietnamese spaces every syllable and the wider face left some alone at a line's end ("…của chúng / tôi"); the same on the homepage cellular title, whose rule resets wrapping ("tí / hon."); on the product page at phone widths, a smaller nav gap (`site-header.module.css`, so "Trang chủ" and the other links stay on one line at 375 px and up) and a 16px eyebrow (`template-chapters-hero.module.css`, so it keeps one line and clears the giant name); and on the About page's closing buttons, less side padding with centred, balanced lines. The lineup's "Sống / trọn vẹn." on phones ("Live / fully") was left as it is. Below 375 px the product nav and eyebrow still take two lines, as they already did in Switzer.
- **Known, not fixed.** On the product page at phone width, tabbing to a study's "Read the study" link leaves the top of its card (the year) about 27px above the screen, because the Vietnamese card is one line taller. `qa_research_daily.py` flags it on `/vn` (2 checks); it passes with Switzer. It only affects keyboard use on a phone; the fix belongs to the research chapter's focus scrolling. Many homepage headings are sized in `vw` rather than through `--display-size`, so a size factor on that token would have shrunk only some of them.
- **English words on a Vietnamese page** stay Switzer: `html:lang(vi) body [lang|="en"]` sets the Switzer stack. That covers the About page's h1 ("Be in Good Health.", `lang="en"`), which also keeps Switzer's weight (`--switzer-weight`). Product names inside Vietnamese text ("NuriCell") follow Be Vietnam Pro, and so does copy that is still in English but not marked `lang="en"` (for example the NuriCell page's untranslated chapters).
- **Loading.** `preload: false`: English, Korean, Japanese and Chinese pages never download it (checked: no Be Vietnam Pro face loaded there). Vietnamese pages fetch the faces they use once the CSS applies, with next/font's metric-matched Arial fallback during the swap. The "↑" in "Back to top" is not in Be Vietnam Pro and falls back to that Arial fallback.
- **Checks.** `python -X utf8 scripts/qa/qa_vn_font.py http://localhost:3009` asks Chrome (DevTools protocol, `CSS.getPlatformFontsForNode`) which faces drew every text on the three `/vn` pages and on English, Korean and Japanese pages; `--dump file.json` writes the counts, `--shots tag` takes viewport shots into `scripts/qa/out/vn-font/`. `qa_about.py` checks the same on `/vn/about` and that the glass still clears the English title.

## Account scope

Mo initially requested placeholders, then supplied `https://bigh-vn-demo.vercel.app` for Log in.

Log in is now a standard link to that exact external destination, opening in the same tab in every language. Sign up remains a disabled placeholder until Mo supplies its link. Neither control opens an account pop-up. The earlier `account-preview` component and its translations remain unused for reference.

## Translation maintenance

`src/i18n/use-copy.ts` wraps next-intl. `copy-keys.json` maps readable English source strings to stable message IDs in the five `messages/*.json` catalogs. There are 565 matching entries per active language (September 28, 2026, after the About page's 30 new keys, m545–m574; see `docs/about-page.md`), including named placeholders. Key numbers are never reused, so a few gaps remain from removed copy, such as the 2002 animal-study paragraph Mo asked to remove from Dr. Liu’s profile. `messages/hken.json` is `{}` on purpose: it falls back to English, and `/hken` redirects to `/cns`. Components render translated strings directly; no runtime DOM replacement or third-party translation widget is used.

Add new copy to the source map and all five catalogs together. Keep product names unchanged and use only Dr. Iris Wang's public name. The non-English text is a draft translation of the existing preview, not independently reviewed by native speakers. This work does not approve new health claims or translate external research papers. The historical `original` and `spotlight` product modes remain preserved; their archived layouts were not separately localized.

The first-party [next-intl navigation documentation](https://next-intl.dev/docs/routing/navigation) and [translation documentation](https://next-intl.dev/docs/usage/translations), plus the installed Next.js internationalization, Link and font guides, informed the implementation. Context7 tools were unavailable in this session.

## Verification

- Login-link follow-up: checked the exact URL and disabled Sign up at 390px and 1440px with no horizontal overflow. Activated Log in using Enter and reached `https://bigh-vn-demo.vercel.app/`, titled “BiGH Việt Nam — Member portal.” Only navigation was checked; no account sign-in was attempted. Changed-file ESLint and formatting passed.
- After Mo clarified the placeholder requirement, checked 390px and 1440px: Log in and Sign up are disabled, the language selector remains enabled, and no horizontal overflow occurs. Switching to Japanese still translates the header; no account dialog opens. The earlier account-dialog checks below describe the initial implementation, which is now disconnected.
- All five languages switched the page text and valid document language tag in the local browser. The page title is translated too.
- Verified the language survives refresh and a return to `/`, query/hash preservation, and the `/hken` redirect.
- Checked all five at 320, 390, 1024 and 1440px: no horizontal overflow, no header/hero overlap, and no offscreen controls. Checked Japanese, Korean and Vietnamese at the 901/1181px header breakpoints: no overlapping controls.
- Checked all three product layouts on phone widths in all five languages, with no horizontal overflow. Inspected desktop/phone screenshots and adjusted longer headline sizes and Vietnamese font handling.
- Opened both account previews in all five languages. Correct titles and field counts appeared; all fields were disabled. Escape closed each dialog and focus returned to its trigger. Mobile navigation opened and closed in all five languages.
- Opened NuriCell details in every language and confirmed translated content. Existing product handlers are preserved.
- Catalog validation found 245 keys per locale, no missing or extra keys and no placeholder mismatches.
- Lint and changed-file formatting passed. The standalone type check found an unsupported font subset name; this was corrected to `latin-ext`. The final production build then compiled, passed TypeScript and generated all 10 pages.
- Final local browser check reported zero errors and one unused-font-preload advisory on the Vietnamese page, which intentionally uses a different serif font. Screenshots are saved under `reference/header-languages/`. Checks used a desktop browser at responsive sizes, not physical phones or Safari.

## Preview

Latest preview with the supplied Log in link: https://bigh-website-11ihz6z1d-sarkuseq1999s-projects.vercel.app/

Deployment `dpl_EtjCWCRcWbXV5JyzY8yCY8b8Y2CF` reported READY after compiling, passing TypeScript and generating all 10 pages. The link was exercised locally with keyboard activation and reached the supplied member portal. Existing preview protection was retained; production was not promoted. Earlier deployments below are historical.

Latest placeholder-only preview: https://bigh-website-58j7r4aei-sarkuseq1999s-projects.vercel.app/

Deployment `dpl_FEmpPqp1s7D373Xku1f1X5sMiaJH` reported READY after compiling, passing TypeScript and generating all 10 pages. Local lint, type checks and browser placeholder checks passed. Login protection was retained; production was not promoted. The URL below records the preceding implementation.

Protected preview: https://bigh-website-mmin9lakl-sarkuseq1999s-projects.vercel.app/

Deployment `dpl_GdBkwykQoEE5HwDseN9JSLF7yQwk` reported READY. Its hosted build compiled, passed TypeScript and generated all 10 pages. Visiting the URL confirmed the existing Vercel login protection remains in place. Production was not promoted. Layout and interaction checks above were local; the hosted design was not visually checked behind the login gate.
