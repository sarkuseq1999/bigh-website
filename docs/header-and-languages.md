# Account controls and five languages — September 22, 2026

Mo requested Log in, Sign up and a language selector in the upper right, with English, Chinese, Korean, Vietnamese and Japanese.

## Implemented

- Desktop: understated Log in link, outlined Sign up button and globe/language selector in the top-right header. At intermediate widths navigation moves to a second row; phones use a compact utility row above the logo and menu.
- The selector offers English, 简体中文, 한국어, Tiếng Việt and 日本語. Chinese uses Simplified Chinese, matching the existing `/cns` route. Existing URL codes are retained: `/`, `/cns`, `/kr`, `/vn`, `/jp`.
- The previous `/hken` route redirects to `/cns`. It is not a sixth visible language or a Traditional Chinese translation.
- The active homepage, all three current product-collection options, product/scientist/education/help dialogs, account previews, motion controls, accessibility labels and page metadata use the selected language. Product names, approved bottle packaging, research journal names and external source pages remain as provided.
- Existing locale navigation preserves query/hash when switching, records the selected locale through next-intl's cookie and updates the document language tags to `en`, `zh-Hans`, `ko`, `vi` or `ja`.
- Language-specific headline sizing and system font fallbacks keep Japanese/Korean/Chinese readable; Vietnamese uses DM Sans with the supported Latin Extended subset and Times New Roman for serif accents. The existing animation and approved product imagery are unchanged.

## Account scope

Mo initially requested placeholders, then supplied `https://bigh-vn-demo.vercel.app` for Log in.

Log in is now a standard link to that exact external destination, opening in the same tab in every language. Sign up remains a disabled placeholder until Mo supplies its link. Neither control opens an account pop-up. The earlier `account-preview` component and its translations remain unused for reference.

## Translation maintenance

`src/i18n/use-copy.ts` wraps next-intl. `copy-keys.json` maps readable English source strings to stable message IDs in the five `messages/*.json` catalogs. There are 244 matching entries per active language, including named placeholders, after Mo requested removal of the 2002 animal-study paragraph from Dr. Liu’s profile. Components render translated strings directly; no runtime DOM replacement or third-party translation widget is used.

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
