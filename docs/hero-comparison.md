# Selected hero: Deep Space — September 22, 2026

**Animation update:** Mo approved animating the selected cell. The [Deep Space animation](deep-space-animation.md) now supersedes the gentle still-image drift described below. Use that document for the current preview. This page preserves the selection and comparison history.

Mo chose option 2: “The deep space one is better. Let's use this one.” Deep Space is now the only mounted hero. The 1 / 2 / 3 switcher is removed, the official white logo is used, and only the selected background is loaded and preloaded. Approved copy and both actions are unchanged. Mobile bottom spacing no longer reserves room for the comparison controls.

Motion remains the existing gentle CSS drift, with pause/play, offscreen pausing, and reduced-motion support. A new cell video has not been generated. Other artwork, mockups, and previous deployments are preserved.

Earlier selected-still preview: https://bigh-website-keyjfda8o-sarkuseq1999s-projects.vercel.app

Deployment `dpl_3HHWmEfzY4zAKdbaeFAyYi7idAzj` reported READY. The final local and Vercel builds both generated all 10 pages. Vercel login protection is unchanged; production was not promoted. UI verification was local; the remote page remains behind the existing login gate.

## Selected hero verification

- Local browser checks at 320, 390, 768, and 1440 pixels: one loaded hero image, Deep Space on first load, no comparison controls, and no horizontal overflow.
- Desktop and phone screenshots visually inspected: `reference/hero-concepts/qa/deep-space-selected-desktop.png` and `deep-space-selected-phone.png`.
- Pause/play, product dialog, Escape dismissal, and reduced motion checked. No browser console warnings or errors after reload.
- Lint, TypeScript, and formatting passed. Both final production builds passed; Vercel reported READY.

## Historical comparison

The following records the earlier three-option preview and its behavior before Mo selected Deep Space.

### Three-version hero comparison — September 22, 2026

Mo requested the three complete mockups as website versions, selectable with 1 / 2 / 3 at the bottom right.

Archived comparison preview: https://bigh-website-oa8nlcfvw-sarkuseq1999s-projects.vercel.app

Deployment `dpl_3fHS8DYG8kAEDdDh5hZnGJNJxzH8` reported READY. Both the local and Vercel builds compiled, completed TypeScript, and generated 10 pages. Existing Vercel sign-in protection is unchanged; production was not promoted.

## What the comparison controls did

1. Pearl: ivory and cool blue, cell on the right, dark text.
2. Deep Space: midnight blue, glowing cell on the right, light text and the official white logo.
3. Warm & Organic: cream and champagne, large cell on the left and copy on the right on desktop.

The fixed bottom-right switcher labels the selected design and marks the active numbered button. Buttons support keyboard activation and use `aria-pressed`. Choosing a version while scrolled down returns to the hero. The page starts on Pearl after a reload; choosing a version is a temporary comparison, not a saved design approval.

Each version uses real responsive text, the unchanged official logo file with the existing tagline crop, working product/scientist actions, and the existing navigation. The header now sits over the hero as one row. On smaller screens the headline, artwork, copy and actions stack. The menu retains its open/close behavior.

Clean background artwork was made from each mockup using the built-in image generator. Exact prompts, source paths and served paths: [background-prompts.md](../reference/hero-concepts/complete-hero-mockups/background-prompts.md). The three images are saved under `public/media/hero/` as `pearl-background-v1.png`, `deep-space-background-v1.png`, and `warm-organic-background-v1.png`. Copies matched the source hashes.

These are three visual directions with a gentle CSS drift. They are not three newly generated cell videos. Pause/play, offscreen pausing and reduced-motion behavior are included. The earlier `cellular-hero.tsx`, its original image and both videos remain preserved; that hero is not currently mounted. Once Mo chooses a direction, create its full cell animation.

## Implementation and verification

- `src/components/home/hero-comparison.tsx` and `hero-comparison.module.css` implement the new hero and switcher. `homepage.tsx` owns selection state; `homepage.module.css` adds the integrated header styles.
- All three variants were clicked and checked at 320, 390, 768, 1024 and 1440 pixels: no horizontal overflow, all images loaded, one selected control and the switcher within the viewport.
- Visually inspected all three desktop and phone variants. Screenshots: `reference/hero-concepts/qa/comparison-*-desktop.png` and `comparison-*-phone*.png`.
- Verified keyboard selection, product-dialog opening and Escape dismissal, scientist navigation, return to the hero from the fixed switcher, phone menu opening and closing, and desktop/phone pause/play.
- Reduced-motion emulation produced zero hero animations and hid the motion control. Ordinary offscreen movement paused the artwork.
- Final lint, TypeScript and changed-code formatting checks passed. No browser console errors were reported during local verification.
- The hosted preview retains its login gate. An unauthenticated visit reaches Vercel login; the hosted UI was not rechecked beyond that gate. The full interaction checks above were local.

Later homepage sections remain the previous draft. This comparison does not implement the rest of the accepted homepage copy or select a final design.
