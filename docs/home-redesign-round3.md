# Homepage redesign, round 3 (September 29, 2026, later)

Read `docs/home-redesign.md` and `docs/home-redesign-round2.md` first; everything there still
applies (setup, shared files, Mo's rules, no existing site imagery, checks) unless this page
says otherwise.

## What Mo said about round 2

"These 3 are good but not the vibe BiGH is looking for. Iris is close but that
cell/mitochondria looks really weird ... enhance Iris, and give me 2 more new designs." Mo gave
**$20 of Higgsfield API budget** for this round.

**The lead's read of the BiGH vibe** (from Mo's picks and rejections): light, calm, premium,
science-led and trustworthy, like Timeline (her number one reference), fresh and alive, for
people in midlife and older. Not dark and moody (round 2's Sunrise was rejected), not loud
(Color pop was rejected), not techy-weird. One beautiful hero object or scene per screen,
generous space, Switzer. Honest science.

**Why the round-2 cell looked weird:** it was a live three.js primitive (a lumpy, rubbery
jelly bean with marshmallow folds). The About page taught the same lesson: rich rendered images
brought to life with motion beat live 3D primitives, which read as cartoonish. **Every cell or
mitochondrion this round is a proper render** (a generated still), brought to life with motion
(a Kling loop or a shader on its own pixels), never a live primitive.

## The approved mitochondrion render

`reference/home-v2/iris/originals/bake-qwen.png` (Qwen Image 3, 2k, $0.075) won a 5-model test:
it clearly reads as a mitochondrion (a clear glass outer membrane, golden folded cristae inside,
pastel light). Its prompt is in `bake-qwen.json`. Use this model for renders; use the image as the
reference (`--ref`) for any variation you need (cutaway, closer, aged, other angles), so every
cell on your page is the SAME object.

## Tools and money

Only through `reference/home-v2/hf_run.py` (read its docstring). This round's budgets:
iris $6.00, everyday $6.50, botanical $6.00 (whole round $19 of Mo's $20). `ledger` shows the
spend. Best choices, from the test:

| Need | Model | Price |
| --- | --- | --- |
| Renders, scenes, still lifes | `alibaba/qwen-image-3/text-to-image` `--resolution 2k` | $0.075 |
| A variation of one of your pictures | `alibaba/qwen-image-3/edit` `--ref <png>` (no `--aspect`: pass `--aspect ''`) or `xai/grok-imagine-image-2.0` `--ref` | $0.04–0.07 |
| Photo-real people | `higgsfield-ai/soul/v2/standard` | $0.004 |
| Motion from a still | `kling-video/v3.0/pro/image-to-video` (5 s) with `--last-image` = the same still for a seamless loop | $0.25–0.31 |
| Cheaper motion | `kling-video/v3.0/std/image-to-video` | $0.23 (5 s), $0.46 (10 s) |

Jobs queue 5–15 minutes: run them in the background (several can wait at once; submissions are
serialized by a lock) and keep building. Look at every result at 100 % and reject AI tells. Prompt
video for calm, subtle motion ("slow gentle rotation, soft light shifts, camera almost still").
Encode shipped clips H.264, ≤ 3 MB each, with a poster; crossfade the ends if a loop jumps.

## Bar

9.0 / 10 overall and for the opening, no block under 8.7, judged from your own screenshots
(1440×900, 1280×720, 390×844 and mid-motion frames) against Timeline, Seed, Isomorphic, Apple and
the site's own Science/About/NuriCell pages. The lead re-scores from his own screenshots.
