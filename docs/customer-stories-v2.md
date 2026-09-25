# Customer stories: three new designs (September 24, 2026)

**Decision (September 24, later): Mo chose Round 3's Still life.** "Option number one is okay, not the best, but we can work on this a little bit more later to polish." The review bar is removed and the section always shows Still life. Daylight, Showroom and the earlier pictures stay available through `StoriesPortraits`' `visual` prop. Polish is deferred to a later pass.

Mo rejected the September 23 choices (Daybook, Story Wall, Spotlight) and asked for three new designs from scratch. Claude Code built them. They are live for comparison at https://bigh-website-demo.vercel.app/#stories with the sticky 1 / 2 / 3 bar.

**Decision (September 24): Mo chose direction 1, Portraits, drawn in style C, ink and color.** She liked the look and the product link. She can't use customers' personal photos, and fake photos don't look genuine, so the people are clearly drawn illustrations with their faces shown (her choice A over hidden faces). A real customer's own quote will be used with permission. Style C won a three-way comparison on the same person: A flat illustration, B gouache, C ink and color (review page: https://claude.ai/artifact/Fs2BDcTraA4g784LmeRpRt, private to Mo).

Now live on the demo (no review bar; the section shows Portraits only):

- All three people are redrawn in the ink-and-color style (`public/images/stories/v2/ink-*.webp`, face crops `ink-face-*.webp`). For consistent style, Michael and Susan used two references each: their earlier portrait and the chosen Lisa.
- Fixes from an independent finish review (disposition "fix"; it also ranked Portraits first). On phones, the three face buttons now sit in one row above the drawing, so a tap changes what's right below. "Illustrative portrait" is now a horizontal 14px label in the byline, next to "Fictional sample".
- Moments and Scroll story remain in the code as `design="moments"` / `design="light"` on `CustomerStories`, but are not rendered. Their review items (the germ-like book image, faint unlit words, card dead space) were not fixed, because they weren't chosen.

Not saved to GitHub yet (Mo: "not yet — we'll keep working on it"). The last commit on `main` is `40d715d`.

## Round 3 (September 24): livelier ways to stage the objects

Mo picked the Objects direction from round 2 but found it plain: "a mug and an orange on a plain green circle". She asked for three more appealing, fun options and allowed any tool, including three.js and GSAP. They are live on the demo (`?stories=1`, `2`, `3`). The Portraits layout is unchanged: cobalt, a big serif quote, a product link, and object-thumbnail selectors. New quotes now rise in word by word behind a mask (GSAP SplitText) in every option.

1. **Still life** (`stories-stilllife.tsx`, GSAP). Each story is an arrangement of four or five real-looking pieces around the real product bottle. Lisa has toast, a mug, a clementine, and keys. Michael has tea, the book, and a magnifier. Susan has a bee, the hat, honeycomb, and a sprig. The pieces float at different depths inside two slow orbit rings, drift against the cursor, bob gently, and scatter and regather between stories. The idea comes from Mo's Seed capsule "opening" reference.
2. **Daylight** (`stories-daylight.tsx`, GSAP). An arched window onto one day. Lisa is Morning, Michael is Afternoon, Susan is Golden hour. The sun travels its arc, the sky colors tween (CSS variables), soft clouds drift, and the object rests on the sill while its shadow swings with the sun.
3. **Showroom** (`stories-showroom.tsx`, three.js). A real 3D turntable: a pale plinth with a lime rim and the three objects as camera-facing sprites with contact shadows. Choosing a person turns their object to the front, and dragging spins the stand and snaps to the nearest story. three.js is imported dynamically, only when this option is on the page. It renders only while visible. Reduced motion or no WebGL shows a still version.

The nine new pieces were made with GPT Image 2.5, max quality, transparent. The sprig's white halo was removed. The product bottles are trimmed copies of the approved PNGs (`bottle-*.webp`); the originals are untouched. Every GSAP entrance and exit has a timeout failsafe (`progress(1)`), because a throttled tab can stall requestAnimationFrame. One bug was found and fixed during QA: Daylight's object swap was killing the sky timeline mid-way.

Verification: type-check, lint, Prettier, the build, and Impeccable's detector (0 findings) pass. Round-3 checks passed 14 of 14 locally in English and Korean at 1440 and 390 wide. That covers render, switching to Michael (pieces visible, sun at its afternoon spot, WebGL ready), no overflow, no errors or 404s, the turntable drag snapping to another story and updating the quote, and reduced motion using the still Showroom. The same set passed 8 of 8 on the public demo.

## Round 2 (September 24): picture choices for the Portraits layout

After seeing the ink drawings live, Mo said drawn people don't fit, because the rest of the site uses real photos. The layout stays: cobalt field, a big serif quote, the product link, and a person selector. The demo now compares three pictures for it (`?stories=1`, `2`, `3`, sticky 1/2/3 bar):

1. **Hands**: a tall arched window with the looping hands-only moment and a Pause videos control. Michael's scene was remade (`moment-reading-v2`, `loop-reading-v2.mp4`) with botanical drawings only. The earlier book showed round specimens that could read as germs, which the brand bans.
2. **Objects**: one real-looking everyday object on a lime disc (a blue-flowered mug with a clementine, an open botanical book with reading glasses, a straw hat with a sprig). GPT Image 2.5, transparent (`object-*.webp`, thumbnails `object-thumb-*.webp`).
3. **Words**: no picture. A centered pull-quote with a large lime quote mark.

The selector thumbnails match each choice (scene crops, object thumbnails, or text only). Labels: "Illustrative video" or "Illustrative photo" beside "Fictional sample". The ink drawings stay available as `visual="drawing"`. New strings (Hands, Objects, Words, Illustrative photo) come from `reference/customer-stories/v2/translations-round2.cjs`.

Verification: type-check, lint, Prettier, the build, and Impeccable's detector (0 findings) pass. 18 of 18 checks passed locally and again on the public demo: all three choices in English and Korean at 1440 and 390 wide (correct choice selected, media loaded, the video playing, no overflow, no errors or 404s), the v2 book loop, pause, switching keeps the selected person, the product dialog, and reduced motion keeping the loop still.

`?stories=1`, `?stories=2`, or `?stories=3` opens a specific design, for example https://bigh-website-demo.vercel.app/?stories=3#stories.

## What guided them

Mo's Design Vault notes, in her words: testimonials that "combine customer pictures or videos with a very easy-to-read version of what each person said" (Timeline, Design #044); a full-page hero that is "not too busy" with one animated person as the "clear main object", "lively, fun, and alive" (Pear, #054); a subtle looping video that looks "like a $10,000 website" (#055); consistent circle crops (Seed, #042). All three designs use the existing homepage palette (cobalt `#284da8`, navy `#102b50` / `#041328`, lime `#e2ed94`) and Instrument Serif. Text is 17–21px with 13px minimum labels, and every control is at least 44px, for older readers.

## The three designs

1. **Portraits** (`stories-portraits.tsx`): a drenched cobalt field with one large painted, full-length person at a time (Pear-style), a big serif quote, and round painted-face buttons to switch people. The figure drifts slightly with the mouse. Stories switch with a soft slide.
2. **Moments** (`stories-moments.tsx`): a lime reel that bleeds off the right edge. Each story pairs a 5-second looping video of a hands-only everyday moment with a colored quote card (navy, paper, cobalt). It has a Pause videos control, arrow buttons, and a progress bar, and it swipes on phones. Videos play only while on screen.
3. **Scroll story** (`stories-light.tsx`): night navy. Each story pins while the visitor scrolls, and a warm gold "wave of light" moves through the quote word by word while the round photo brightens. On phones and short screens it does not pin; the words still light as the story scrolls past. Chinese and Japanese are split into words with `Intl.Segmenter`.

The shell (`customer-stories.tsx`) holds the review bar and picks the design. Shared data lives in `stories-data.ts`; `use-reduced-motion.ts` reads the motion preference. Every CSS rule is scoped under its design's root class, because the homepage's `.site p` / `.site button` resets otherwise override single-class rules.

## Honesty labels

The sample stories and reviewer names are unchanged and still fictional. Each design shows the section-wide fictional-sample notice, a "Fictional sample" tag per story, and an image label ("Illustrative portrait", "Illustrative video", or "Illustrative scene"). The painted portraits are obviously artwork, and the photos and videos show hands only, no identifiable person. There are no star ratings or verified-buyer badges.

**Before launch:** replace the samples with sourced, permissioned customer stories. For Portraits, the natural route is a painted portrait made from each real customer's own photo, with their permission. For Moments, use their own short clips or photos.

## Assets and provenance

Generated on Mo's Higgsfield plan (134.5 credits):

- Portraits: **GPT Image 2.5**, max quality, 2k, 2:3, transparent background. A side-by-side with GPT Image 2 on Lisa showed 2.5 looking more clearly painted. Susan's cut-out had a built-in white halo, which was removed by clearing light semi-transparent edge pixels (`portrait-susan-clean.png`).
- Scenes: GPT Image 2.5, max, 2k, 9:16, hands only.
- Videos: **Seedance 2.0**, 5 seconds, 720p, 9:16, no audio, with the same frame as start and end so the loop is seamless. Re-encoded to H.264 CRF 25 (430–560 KB each).

Web files: `public/images/stories/v2/` (portraits, face crops, scene stills) and `public/media/stories/`. Originals, exact prompts (`*.json` sidecars next to each original), and the translation script are in `reference/customer-stories/v2/`. The September 23 component is preserved in `reference/customer-stories/2026-09-24-daybook-wall-spotlight/`.

New strings (design names, image labels, video controls, scroll hint) were added in all five languages with `reference/customer-stories/v2/translations.cjs` (keys m347–m355).

## Verification

- Type-check, ESLint, Prettier, and `npm run build` pass (10 pages). Impeccable's detector reported 0 findings.
- Screenshots at 1440 and 390 wide in all five languages: no sideways overflow and no console or page errors. Korean, Chinese, and Japanese quote titles are set about 20% smaller than English, so they fit on two lines.
- Interaction checks: 19 of 19 passed on the local server and again on the public demo. They cover people buttons and arrow keys, video pause/play, reel scrolling, the product dialogs opening and closing with Escape, and reduced motion (plain fully-lit text; videos stay still).
