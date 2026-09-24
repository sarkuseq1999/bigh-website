# Cellular hero preview — September 21, 2026

This document records the earlier single animated-cell trial. The current preview is the [three-version hero comparison](hero-comparison.md), added September 22, 2026. Its artwork, styles and numbered switcher supersede the earlier hero in the active homepage; the original component and media are preserved.

Mo accepted the first cell animation for a layout trial and asked to build the complete hero on desktop and phone.

Mo then requested a weightless, space-like background and a more fluid cell motion inspired by a jellyfish. The second motion revision is now implemented locally and awaiting his review.

## Current preview

Remote preview, uploaded with Mo's explicit approval on September 22, 2026: https://bigh-website-71gk915d0-sarkuseq1999s-projects.vercel.app

Use this remote URL when reviewing from Mo's work MacBook or another computer. Vercel login protection is unchanged; sign in with the account that owns the BiGH project. Deployment `dpl_4cUGt46HQ8RMSeQ1jj4susEuiuTM` reported `READY`; the hosted build compiled, completed TypeScript, and generated all 10 pages. An unauthenticated browser visit was verified to reach Vercel login, so the hosted page itself was not visually rechecked in that browser. Local visual and motion verification is recorded below. This is a preview deployment; production was not promoted.

Run `npm run dev -- --hostname localhost --port 3000` and open http://localhost:3000/.
Use `localhost` consistently: starting this dev server with `127.0.0.1` caused the default-locale rewrite to redirect back to itself. Restarting with the documented `localhost` hostname resolved the loop without a routing-code change.

The new hero appears at the top of the existing homepage. Later sections and the existing navigation are from the earlier preview. The rest of the newly approved homepage copy is not yet implemented.

## Content and presentation

- Exact approved headline: “Good health starts with your cells.”
- Exact approved introduction: “Developed by scientists with deep expertise in cellular health and aging, BiGH’s key formulas share one purpose: helping you stay sharp, stay active, and live fully.”
- “Discover NuriCell” opens the existing product-preview dialog. A dedicated product page and shopping flow remain future work.
- “Meet our scientists” links to the existing scientist section.
- Desktop: large left-aligned headline, supporting copy and actions, with the translucent cell on the right. Warm ivory, blue-gray text, and the existing typefaces complement the supplied artwork. These design choices remain open for review.
- Phone/tablet: centered headline, cell artwork, supporting copy, then actions. Narrow phones may require a short scroll to reach the secondary action.
- Muted inline video loops, with a keyboard-accessible pause/play control. A visitor's pause choice survives scrolling away and back.
- Motion revision 2: a new ten-second cell video adds visible membrane flexing and internal movement. Two broad layers of pastel light drift across the entire hero, with ten small floating lights and a slight rise, drift, and tilt of the cell artwork. Feathered masks blend the video into the surrounding atmosphere at desktop and phone sizes. Headline, copy, and actions stay still.
- The same pause/play control stops the video and all thirteen CSS animations together. The backgrounds also pause offscreen or on video failure; reduced-motion visitors receive no CSS animation.
- Playback pauses offscreen and when the browser document is hidden.
- Reduced-motion visitors see the still image without downloading the video. A failed video request also leaves the still image and hides the unavailable motion control.

## Files

- `src/components/home/cellular-hero.tsx` and `cellular-hero.module.css`: self-contained hero component and styles.
- `src/components/home/homepage.tsx`: integrates the new hero with existing actions.
- `public/media/hero/cell-sculpture-v1.png`: exact copy of the original generated cell still.
- `public/media/hero/cell-sculpture-motion-v2.mp4`: current video, an exact copy of the H.264 animation from `reference/hero-concepts/cell-sculpture-motion-v2-web.mp4` (3,465,865 bytes, 1920 × 1080, 24 fps, 10.041667 seconds, no audio).
- Source generation prompts, job IDs, result URLs, and media remain in `reference/hero-concepts/cell-sculpture-motion-v1.txt` and `cell-sculpture-motion-v2.txt`. Both original generations and the first served video are preserved. Served-copy hashes matched.

## Verification

### Motion revision 2

- Full lint, TypeScript, formatting of both changed code files, and the final production build passed; the build generated all 10 pages.
- Both new media files fully decoded without errors. The six-frame review sheet shows the cell intact with a changing membrane outline and internal folds.
- Browser checks confirmed that the current source is v2, muted playback works, the video loops, and the headline stays in the same position as the artwork moves.
- Pausing froze the video and all 13 CSS animations. A visitor pause persisted after scrolling away and back; ordinary offscreen pause and resume also worked.
- A fresh reduced-motion visit made zero MP4 requests and had zero CSS animations. An intentionally blocked MP4 request left the still image, removed the motion control, and paused the surrounding atmosphere.
- No horizontal overflow at 320, 390, 768, 1024, or 1440 CSS pixels. The final desktop and phone screenshots were visually inspected: `reference/hero-concepts/qa/hero-preview-v2-desktop.png` and `hero-preview-v2-phone.png`.
- Loop restart was verified. Perfect visual continuity at the generated clip's seam has not been established. The diffuse reflection in the source remains, softened by the hero mask.

### Initial layout trial

- Full ESLint, TypeScript check, formatting of the three changed code files, and final production build passed. The build generated all 10 pages.
- Opened and visually inspected the actual local site at desktop and phone widths.
- No horizontal overflow at 320, 390, 768, 1024, 1280, or 1440 CSS pixels.
- Browser checks confirmed muted playback, pause/play time progression, loop restart, offscreen pause/resume, persistence of a visitor pause, the product dialog and Escape dismissal, the scientist link, and the phone menu.
- A fresh reduced-motion visit made no MP4 request. An intentionally blocked MP4 request displayed the still fallback and removed the motion control.
- The normal preview had no browser console errors. Loop restart was verified; perfect visual continuity at the seam has not been established.
- Visual reference screenshots are saved under `reference/hero-concepts/qa/hero-preview-*.png`.

The checks used a desktop browser at responsive viewport sizes. This is a local design preview awaiting Mo's feedback.
