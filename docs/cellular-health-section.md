# Cellular-health section — September 22, 2026

**Superseded by the [six-design website comparison](cellular-health-comparison.md).** Use that document for the current implementation and preview. This document preserves the first section implementation.

Mo approved the redesigned Deep Space hero motion and authorized building the next section. The new section explains why cellular health matters using the exact approved working copy. Mo subsequently rejected this first section design as visually plain and the mitochondrion image as boring. Three new still concepts are saved in `reference/cellular-health/concepts/`, with prompts and provenance in `prompts-v1.txt`. They are unselected proposals; the website preview still shows the first implementation documented below.

## Implementation

Design constraint added by Mo after the first concept comparison: alternate colored and light sections. This section must be white or near-white to contrast with the deep-blue hero. The image and layout still need a substantial redesign; retain the approved wording. The earlier three colored concepts are unselected references. Three additional light concepts are saved in `reference/cellular-health/concepts/`: 4 — Pearl sculpture, 5 — A closer look, and 6 — Ivory editorial. Exact prompts and provenance: `prompts-white-v1.txt`. The rendered copy and composition were visually inspected. All remain still concepts awaiting selection, not implemented designs or animations.

- Page order: Deep Space hero → cellular health → Dr. Liu → products. Removed the old intro strip and replaced the previous scrolling science story. The approved hero is unchanged.
- Headline: “Tiny power plants. A big part of your health.”
- Copy: “Inside many of your body’s cells are mitochondria—tiny power plants that turn energy from food into a form your cells can use.” Then: “That energy helps your brain think, your heart beat, and your muscles move.” Closing: “It’s one reason good health starts with your cells.”
- A body → cell → mitochondria diagram introduces a blue and amber mitochondrion cutaway. It is explicitly labeled as simplified and not to scale. A calm light background gives the text a clear contrast with the dark hero.
- “Explore cellular health” opens the existing introductory science dialog. The Science navigation and footer link target this section.
- Desktop uses an illustration/text split; phone stacks the headline, illustration, copy and button. There is no looping movement in this section. The button's hover transition respects reduced motion.
- Component: `src/components/home/cellular-health.tsx`; styles: `cellular-health.module.css`; integration: `homepage.tsx`.

## Asset and source notes

Original illustration generated with the built-in image tool, visually inspected and copied to `public/images/science/mitochondrion-cutaway-v1.png` (1254 × 1254). Exact prompt, source path and verified SHA-256 are in [the asset record](../reference/cellular-health/mitochondrion-cutaway-v1.txt).

The approved language is consistent with [NHGRI's mitochondria glossary](https://www.genome.gov/genetics-glossary/Mitochondria) and [NIGMS's mitochondria explainer](https://nigms.nih.gov/biobeat/2020/05/the-maternal-magic-of-mitochondria). “Many” deliberately avoids saying all cells have mitochondria. The illustration is explanatory artwork and makes no supplement efficacy claim.

## Verification

- Local browser screenshots inspected at 320, 390, 768 and 1440 pixels; also checked 1024 pixels. No horizontal overflow. New image loads and decodes.
- Exactly one cellular-health anchor, immediately after the hero and before the scientists section.
- Explore button opens “Energy starts small.” Its source link points to NHGRI. Escape dismisses the dialog and returns focus to the button.
- Keyboard Enter opens the same dialog. Science navigation lands at the new section with the existing 150px header offset. The hero plays at native 1× speed and pauses when offscreen.
- Final lint, TypeScript, changed-code Prettier check and production build passed. The build generated all 10 pages. One intermediate anchor check timed out because its expected position omitted the site's 150px scroll padding; the browser's measured final position confirmed the anchor is correct.
- Screenshots: `reference/cellular-health/qa/section-320.png`, `section-390.png`, `section-768.png`, `section-1440.png`.
- Browser showed no errors. One development-only LCP warning identified the existing, below-fold NuriCell product image; this section does not change that image.
- Responsive checks use a desktop browser, not a physical phone or Safari.

## Protected preview

Current preview: https://bigh-website-8134jdbug-sarkuseq1999s-projects.vercel.app/#cellular-health

Deployment `dpl_4sFSfpbHVZcvW8j8EVAQsMDZcnpv` reported READY. The hosted build compiled, completed TypeScript and generated all 10 pages. This is a preview deployment under the existing Vercel login protection; production was not promoted. Local interaction and visual checks are described above. The hosted page itself was not visually rechecked behind the login gate.
