# Browser checks (Playwright for Python)

Run from the repo root with the dev server up (port 3007) or against the public demo. Pictures
land in `scripts/qa/out/` (ignored by git). Each script takes the base URL first and, for the QA
scripts, a comma-separated list of locales (`""` is English).

```bash
python -X utf8 scripts/qa/qa_glass.py http://localhost:3007 ",kr"
python -X utf8 scripts/qa/qa_research.py http://localhost:3007 ",kr"
python -X utf8 scripts/qa/qa_closing.py http://localhost:3007 ",kr"
python -X utf8 scripts/qa/qa_stories.py http://localhost:3007
```

| Script                 | Checks                                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| `qa_glass.py`          | Science section: 21 checks (topics on scroll, age slider, free-radical steps, tabs, explainers, reduced motion) |
| `qa_research.py`       | Research list: 36 sources, three filters with counts, show more, rows open, safe links                          |
| `qa_closing.py`        | Closing block's three looks (only when the block is rendered again)                                             |
| `qa_stories.py`        | Customer stories                                                                                                |
| `shoot_glass3.py`      | Captures the free-radical steps and the slider at 20/50/80                                                      |
| `shoot_age_strip.py`   | The cell at 20/35/50/65/80 in one strip, plus the gap before the closing button                                 |
| `shoot_phone_stage.py` | Full phone screens of topics 2 and 3 with fit measurements (`<base> <WxH> [locale]`)                            |
| `shoot_closing.py`     | Captures the closing block's looks                                                                              |

Notes: the scripts launch Chromium with SwiftShader flags so WebGL works headless. The site scrolls
smoothly, so they set `scrollBehavior` to `auto` before measuring. Full-page screenshots break the
`svh`-based layouts; capture the viewport and stitch instead. After a deploy, alias it and run the
QA scripts against `https://bigh-website-demo.vercel.app` before reporting.
