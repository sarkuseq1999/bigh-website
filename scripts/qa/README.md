# Browser checks (Playwright for Python)

Run from the repo root with the dev server up (port 3007) or against the public demo. Pictures
land in `scripts/qa/out/` (ignored by git). Each script takes the base URL first and, for the QA
scripts, a comma-separated list of locales (`""` is English).

```bash
python -X utf8 scripts/qa/qa_glass.py http://localhost:3007 ",kr"
python -X utf8 scripts/qa/qa_research.py http://localhost:3007 ",kr"
python -X utf8 scripts/qa/qa_closing.py http://localhost:3007 ",kr"
python -X utf8 scripts/qa/qa_stories.py http://localhost:3007
python -X utf8 scripts/qa/qa_hero_cutaway.py http://localhost:3007 --gpu
python -X utf8 scripts/qa/qa_why_chapter.py http://localhost:3007
python -X utf8 scripts/qa/qa_research_daily.py http://localhost:3007
python -X utf8 scripts/qa/qa_vn_font.py http://localhost:3007
python -X utf8 scripts/qa/qa_green_bee_propolis.py http://localhost:3010
python -X utf8 scripts/qa/qa_why_chapter.py http://localhost:3010 --product=green-bee-propolis
python -X utf8 scripts/qa/qa_research_daily.py http://localhost:3010 --product=green-bee-propolis
python -X utf8 scripts/qa/qa_turmerific.py http://localhost:3012 --gpu
python -X utf8 scripts/qa/qa_why_chapter.py http://localhost:3012 --product=turmerific
python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3034 --only=layout,deep_links
```

`qa_why_chapter.py` and `qa_research_daily.py` check NuriCell unless given `--product=<slug>`; each
product's expected words and numbers are in the script's `PRODUCTS` table.

| Script                     | Checks                                                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `qa_glass.py`              | Science section: 21 checks (topics on scroll, age slider, free-radical steps, tabs, explainers, reduced motion)                      |
| `qa_research.py`           | Research list: 36 sources, three filters with counts, show more, rows open, safe links                                               |
| `qa_closing.py`            | Closing block's three looks (only when the block is rendered again)                                                                  |
| `qa_stories.py`            | Customer stories                                                                                                                     |
| `shoot_glass3.py`          | Captures the free-radical steps and the slider at 20/50/80                                                                           |
| `shoot_age_strip.py`       | The cell at 20/35/50/65/80 in one strip, plus the gap before the closing button                                                      |
| `shoot_phone_stage.py`     | Full phone screens of topics 2 and 3 with fit measurements (`<base> <WxH> [locale]`)                                                 |
| `shoot_closing.py`         | Captures the closing block's looks                                                                                                   |
| `qa_hero_cutaway.py`       | Product page: the "Big name" opening (name clear of the bottle, header, sideways scroll) and the capsule cutaway                     |
| `qa_why_chapter.py`        | Product page: the Why chapter (bulb beats, contrast behind every line, no words over the bulb)                                       |
| `qa_research_daily.py`     | Product page: the research timeline and the month calendar, plus the development-only `?chapters-fixture=`                           |
| `qa_green_bee_propolis.py` | Green Bee Propolis's own facts: headline, name around the amber 3D bottle, 200 mg shown large, the full label, buy, questions, links |
| `qa_turmerific.py`         | Turmerific's own facts: chapters, 3D bottle, both Why pictures, 1,000 mg shown large, six studies, calendar, banned words, sizes     |
| `record_product_page.py`   | Videos of the product page: `opening.mp4` and `page.mp4` (needs ffmpeg; `--only page` redoes one)                                    |
| `qa_vn_font.py`            | Vietnamese type: faces drawn (DevTools) on `/vn` pages and other languages; no tone mark touching the next line                      |

- `qa_nuricell_ink.py [base] [--only=...]` — NuriCell's ink page (October 9, 2026): the ink look and
  menu bar, the other four products on today's template, every painting multiplying with no box,
  the lantern's light coming on (no lighter flash; lit with reduced motion and without script),
  every word of nuricell.ts, sticky paintings inside their chapters, the painted sum and its
  captions, nine sizes, deep links, and the new strings in kr/jp/cns/vn. Pictures in
  `out/nuricell-ink/`. On a built site (`next start` or the demo) the dev-only `?ink-sum` fixtures
  are skipped (the page shows the painted sum for each). Known dev-only false positive: `next dev`
  may log "Image with src /images/products/nuricell.png was detected as the Largest Contentful
  Paint"; its check keeps one entry per picture URL and the last `<Image>` wins, and the menu bar's
  thumbnails and the Buy chapter's bottle (both lazy) share the opening bottle's URL. The opening
  bottle itself is eager with high priority; production builds do not run that check. Also dev-only:
  the four old-template product pages log a 404 for a chunk preload — a Turbopack dev bug (wrong
  chunk hash in the dev loadable manifest for next/dynamic entries with nested dynamic imports,
  fixed after Next 16.2.6); the QA ignores it on dev only (prints a NOTE) and a Next upgrade removes it.

Notes: the scripts launch Chromium with SwiftShader flags so WebGL works headless. The site scrolls
smoothly, so they set `scrollBehavior` to `auto` before measuring. Full-page screenshots break the
`svh`-based layouts; capture the viewport and stitch instead. After a deploy, alias it and run the
QA scripts against `https://bigh-website-demo.vercel.app` before reporting.
