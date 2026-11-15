# California science paintings: actual homepage, November 14, 2026

Mo asked to put the complete set on the actual webpage to review on computer and phone.
These are captures of the real production build, not a mockup board or a browser-side asset swap.

- The initial preview was the production build on this PC's private Tailscale address.
  Mo then authorized publishing to https://bigh-website-demo.vercel.app/#science on November 14.
  Public verification is recorded separately in `docs/public-demo.md`.
- C's ranch workshop, the matching chimney/sparks, and all three cell ages are integrated.
- Existing desktop scroll story, phone swipe/tabs, captions, age thresholds and words remain.
- The Illustrations label has 28px of paper above the painting. Opaque white CSS behind each
  RGBA cell image, inside the multiplied group, prevents older cells showing younger cells beneath.
- No new image generation or spending in this implementation round.

## Captures

Widths: 1440, 1024, 390 and 360. `WIDTH-topic-0.jpg` is Mitochondria,
`WIDTH-topic-1.jpg` Free radicals and `WIDTH-topic-2.jpg` Aging cells at its default age 45.
`WIDTH-age-30/45/80.jpg` shows all three cell stages. `*-moving.jpg` captures each topic's
arrival. Phone `*-section.jpg` captures the entire section, including words and actions below
the viewport, but the sticky header appears in the middle of those tall captures: use the
normal viewport captures for review. The first 1440 opening capture is poorly framed and is
not a review image; use the topic captures.

Viewed at full size: desktop and phone topics, moving states, laptop and small-phone samples.
Visual score: **9/10**. The matching copper chimney connects the first two paintings; the cell
uses the same muted blue, sage and gold. Limitation: the worker and the gold cell parts are
small on phones. The existing long explanatory text continues below the picture.

## Verification

- `npm run build`, lint, type-check and formatting of the changed source files passed.
- `check.py` passed at 1440x1000, 1024x768, 390x844 and 360x800: all three topics select,
  correct new assets decode at 1448px, labels clear the paintings, no horizontal overflow,
  no page errors, and ages 30/42/43/67/68/80/45 show the correct cell.
- The old cell was compared with the same frame with younger layers hidden. Desktop matched
  exactly; mobile was within one 8-bit channel value of GPU compositing rounding. This checks
  the new transparent assets do not leak younger branches through at rest.
- Full required checks, run sequentially on the same production build: `qa_home_ink`
  **290/290 passed** (`qa-home.log`), `qa_nav` **326/326 passed** (`qa-nav.log`).
- `git diff --check` passed. No runtime source edits after the verified build.

Source assets and encoding: [painting notes](../../../home-science/README.md).

`check.py` accepts optional viewport widths (`1440 390`, for example). Set `SCIENCE_PREVIEW_URL`
and `SCIENCE_CAPTURE_DIR` to reuse the same feature checks on the public demo without replacing
the local evidence; the default URL is `http://localhost:3007`.
