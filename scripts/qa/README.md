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
| `record_product_page.py`   | Videos of the product page: `opening.mp4` and `page.mp4` (needs ffmpeg; `--only page` redoes one)                                    |
| `qa_vn_font.py`            | Vietnamese type: faces drawn (DevTools) on `/vn` pages and other languages; no tone mark touching the next line                      |

Notes: the scripts launch Chromium with SwiftShader flags so WebGL works headless. The site scrolls
smoothly, so they set `scrollBehavior` to `auto` before measuring. Full-page screenshots break the
`svh`-based layouts; capture the viewport and stitch instead. After a deploy, alias it and run the
QA scripts against `https://bigh-website-demo.vercel.app` before reporting.
