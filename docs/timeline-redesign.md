# BiGH — Timeline-led homepage redesign

September 17, 2026. This is the current homepage direction, replacing the first green/copper draft.

## Mo's direction

Mo requested a complete redo using Timeline's information organization and overall design feel as the main reference. All Design Vault references are eligible inspiration while there is no named BiGH vault project. The references listed below are the strongest influences for this iteration, not a restriction on the rest of the vault.

The archived old website was not used.

## References and decisions

- Timeline live homepage, Science, and About were reviewed.
- Design #004: clear navigation. BiGH keeps larger type and tap targets, as requested in #045.
- Design #005: approachable scientist introduction, with Dr. Liu prominent and Iris text-only.
- Design #006: short, strong typography and a close connection between the product and message.
- Design #010 and the science scroll sequence: three chapters, with a sticky illustration that changes as each chapter enters view.
- Design #014: a direct mission and spacious editorial layout.
- Design #030: clear science organization and generous spacing. No competitor statistics, claims, videos, or reviews were transferred.
- Design #031: filterable research rows, expandable explanations, source labels, and links to the original material.
- Design #013: a message-led footer with orderly links.

Original BiGH direction: warm white, cobalt blue, muted lemon, DM Sans headings/body, and regular Instrument Serif for editorial text. No Timeline images, logos, proprietary copy, or product claims are reused.

## New structure

1. Human-focused opening with the working tagline and two clear actions.
2. Scientists and the planned Ask BiGH Science benefit.
3. Cellular science in three scroll-linked chapters.
4. NuriCell spotlight and the four other core products.
5. Research and education, filterable and expandable.
6. Purpose and customer commitments.
7. Short science reads, a small customer-story placeholder, and a clear footer.

Purchasing, accounts, actual question submissions, and live support remain future integrations. Details still open in accessible dialogs. The preview retains no-index metadata and robots rules.

## Image provenance

Original lifestyle image: [life-in-full.png](../public/images/life-in-full.png).
Generated with the built-in image-generation tool, not an external API script.
The depicted person is fictional illustrative imagery, not a customer, scientist, or testimonial.
The selected original was copied from the generated-images folder; the original remains there.

Exact prompt:

> Use case: photorealistic-natural. Asset type: editorial lifestyle photograph for the new BiGH cellular health website. Create one premium natural, candid photograph, landscape 3:2. A healthy-looking East Asian woman around 55 with subtle gray in her short dark hair and real smile lines, wearing an unbranded white cotton t-shirt and open light cobalt-blue linen overshirt, standing outdoors on a quiet California coastal trail. Waist-up portrait, body turned a little, looking toward the sea to her left, unposed and thoughtful, soft genuine smile. Subject occupies the right-center two thirds, no cropped head. Ocean, cream dry grasses, softly blurred coastline, pale blue sky. Late afternoon clean directional sunlight, lifelike skin texture and fabric, restrained cinematic color, fine analog grain. Inviting, alive, understated, aspirational without athletic performance claims. No product, no pills, no text, no typography, no logo, no watermark. This is an illustrative fictional person, not a customer testimonial or a scientist.

The product bottles and Dr. Liu portrait retain the provenance and launch checks in [the first-preview notes](homepage-preview.md). The first generated abstract hero remains on disk but is no longer used by the homepage.

## Verification

- ESLint and TypeScript completed with exit 0.
- Formatting applied to all changed source files; git diff whitespace check passed.
- Browser checks at measured desktop width 1280 and phone widths 390 and 320.
- No horizontal page overflow at 390 or 320; no broken loaded images.
- Science navigation opened and closed. All three scroll-story chapters switched the illustration.
- Phone chapter positioning was adjusted and rechecked: at 390 px, the illustration ends at 428 px and the next title starts at 521 px.
- Research filters returned two education entries or all four entries. A study expanded and displayed its source.
- Phone menu closed after choosing Products. NuriCell and scientist details opened; Ask BiGH Science showed its planned status.
- Dialog Escape restored focus to the initiating button and restored body scrolling.
- Reduced-motion CSS is included; operating-system reduced-motion emulation was not tested.
- No customer checkout or representative-user accessibility study was performed.

## Remote preview

Current preview: https://bigh-website-jr0e4tvyq-sarkuseq1999s-projects.vercel.app

Deployment `dpl_5WxCgYGJFuPQei9zgrGthb8p3dRw` is READY. Vercel's build compiled successfully, completed TypeScript, and generated 10 pages. Production has not been promoted. Access settings remain unchanged; the direct preview URL requires Vercel login.

The hosted homepage was opened and inspected on desktop and at 390 px phone width. The hero image loaded, NuriCell details opened, the phone Science menu navigated correctly, and the Research filter returned two entries. The phone page measured 375 px content width and 375 px scroll width, with no horizontal overflow. No browser console errors were recorded. All matched files passed the formatting check.
