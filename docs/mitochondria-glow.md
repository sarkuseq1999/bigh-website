# Mitochondria glow — September 22, 2026

Mo requested an animated glow in the orange part of the “Tiny power plants” illustration. He found the first version too subtle, so the current revision uses a much stronger golden bloom.

He then requested background animation too. The artwork and its glow now share one gently drifting layer: a 28-second camera-like movement with a small zoom and rotation. Soft blue light moves independently over 19 seconds, with eight faint floating particles adding depth. Copy, controls, and section layout stay fixed. The image is oversized inside a clipped viewport so moving edges do not appear; the existing base art and glow always move together. The six saved comparison designs are unaffected.

The original dark cellular-health section now overlays the existing artwork with an SVG color filter that isolates warm amber pixels. A bright core, wider golden halo, and an eight-second opacity pulse make the inner folds visibly brighten and fade. Version two increases warm-pixel isolation and intensity, adds a 22px soft halo with amplified alpha, and expands the pulse from near-zero to full intensity. Playback begins partway through the rise so the change is apparent shortly after entering the section. The original image file is unchanged, and the six saved comparison designs are unchanged. No generated video or additional raster asset is required.

Implementation: `src/components/home/mitochondria-glow.tsx` and its CSS module, mounted only by the `original` variant of `CellularHealthComparison`. The component now wraps the base artwork as well as the glow. The overlay matches the original image's cover sizing and mobile object position. The small Pause/Play motion control reuses existing translations in all five languages and controls all scene motion. Animation pauses offscreen and when the tab is hidden. Reduced-motion preference shows a still glow, disables all animation, and hides the floating atmosphere and control.

Verified locally in Chromium:

- Inspected desktop (1440px) and phone (390px) screenshots; the glow follows the orange folds and mobile cropping stays aligned.
- Observed animation time and opacity advance during playback. Pause and Play changed the animation state correctly.
- Reduced-motion mode produced zero section animations and hid the control. Scrolling away paused the animation. No horizontal overflow at the checked desktop and phone widths.
- Explore cellular health still opens its dialog; Escape closes it and restores focus.
- Changed-file ESLint, formatting, and TypeScript checks passed. Browser reported zero warnings or errors.

Screenshots: `reference/cellular-health/glow-desktop.png` and `glow-mobile.png`. These are desktop-browser checks at responsive sizes, not physical iPhone or Safari testing.

Additional alignment and overflow checks passed at 320, 768, 1100 and 1280px.

Version two: inspected low/peak desktop frames and a 390px phone peak frame. Observed opacity rise from 0.37 to 1 during normal playback; pause/resume and reduced-motion behavior still passed, with aligned mobile image bounds and no horizontal overflow. Formatting and changed-file ESLint passed. Screenshots: `glow-v2-peak.png`, `glow-v2-low.png`, and `glow-v2-mobile-peak.png` in the same reference folder.

Background-motion follow-up: observed the image position and scale change over three seconds while the headline bounds stayed identical. The two image layers kept identical bounds. All 11 animations paused/resumed together and paused offscreen. Reduced-motion mode produced zero animations. Inspected desktop and phone screenshots, with no phone overflow. Screenshots: `background-motion-desktop.png` and `background-motion-mobile.png`.

Background-motion formatting, ESLint, TypeScript, and the hosted production build passed. A fresh local browser context had zero console warnings/errors; both images had positioned parents, the education dialog opened, and the paused state persisted through dialog dismissal. An earlier development warning during hot replacement did not recur on a clean page load.

## Online preview

**Public demo: https://bigh-website-demo.vercel.app/** — use this stable address without any share token. See `public-demo.md` for the current public-access configuration. The deployment links below are historical records.

Current animated-background preview: https://bigh-website-3jlprgps0-sarkuseq1999s-projects.vercel.app/#cellular-health

Deployment `dpl_GhtLXWsFgmGxnM2XRdbjuD11vQ3q` reported READY after compiling, passing TypeScript, and generating all 10 pages. Its shareable link returned HTTP 200 in a fresh unauthenticated browser. On the hosted page, the image moved while the headline stayed fixed, all 11 scene animations paused together, and there were zero page errors. Screenshot: `background-motion-hosted.png`. Shareable access is deployment-specific; use the latest complete link from the conversation. Earlier demos remain available and production was not promoted.

Earlier stronger-glow preview: https://bigh-website-85y0gbhxx-sarkuseq1999s-projects.vercel.app/#cellular-health

Deployment `dpl_7wypYr4d44nG57TvnGG1g1yD7dxz` reported READY after compiling, passing TypeScript, and generating all 10 pages. Its new shareable link opened in a fresh unauthenticated browser, returned HTTP 200, loaded the stronger 22px halo, and visibly advanced the glow's opacity. Pause worked on the hosted page. The previous links remain unchanged.

Earlier, subtle-glow preview:

https://bigh-website-hq25zlday-sarkuseq1999s-projects.vercel.app/#cellular-health

Deployment `dpl_9Xb278KneGyeLjhjn65948BeQzGV` reported READY after compiling, passing TypeScript, and generating all 10 pages. A deployment-specific shareable link was created and provided in the conversation; retain its query parameter when sharing. In a fresh unauthenticated browser context, that link returned HTTP 200, loaded both image layers, animated the glow, and correctly paused/resumed. No page errors occurred. Hosted screenshot: `reference/cellular-health/glow-hosted-desktop.png`. Production was not promoted, and the earlier demo remains available.
