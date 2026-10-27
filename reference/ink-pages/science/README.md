# The Science page's paintings (October 13-14, 2026)

GPT Image 2.5 ("Marketing Studio Image 2.5 Flare" on the Higgsfield API), 21:9, 2k, quality high,
with the homepage's resting crane as the brushwork reference. Mo gave $3 on October 13; 15 jobs
used (about $0.75, at most $1.05 before refunds). Ledger:
`%LOCALAPPDATA%/HiggsfieldAPI/bigh-science-mock/ledger-science-mock.jsonl`.

| Picture          | Original                              | Note                                                                                                                                     |
| ---------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| The handscroll   | `S-panel-1`, `S-panel-2`, `S-panel-3` | Three panels to one horizon, joined in their mist by `build_science.py`; style reference `A-scroll` (the mockup's single-picture scroll) |
| The research     | `R-scrolls`                           | A shelf of rolled scrolls; three lie pulled forward (the three key studies)                                                              |
| Health explained | `S-health-poppy`                      | An edit of `R-health`: California poppies instead of the plum branch (Mo, October 14)                                                    |
| Ask BiGH Science | `S-mugs`                              | An edit of `R-tea`: two mugs instead of the tea set (Mo, October 14)                                                                     |

Build: `python -X utf8 reference/ink-pages/science/build_science.py`, then
`python -X utf8 reference/ink-pages/science/check_science_art.py`.

## One place per screen (October 26, 2026)

Mo found the handscroll's sideways travel read as a draft and picked B: his path going down the
page, one place per screen. No new paintings and no spend: `places()` in `build_science.py` cuts
four places from the joined band (`PLACES`, band pixels, by eye, then checked on the page), each
with a tighter phone cut: `place-okayama`, `place-berkeley`, `place-salzburg`, `place-today`
(`-phone`), v1. The sea and the hills of 2002 are left out. The band itself no longer ships
(`scroll-v2`, `scroll-phone-v2` deleted); it is kept as `plates/band.png` for the contact sheet,
which marks each cut (red wide, blue phone). Mockups and the review page's shots:
`reference/ink-pages/mockups/science-path/2026-10-26/`.
