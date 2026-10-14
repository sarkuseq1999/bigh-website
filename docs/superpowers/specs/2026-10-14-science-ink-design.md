# Science in Ink & Gold: the handscroll

October 14, 2026. Branch `science-ink` (worktree `codes/bigh-science-ink`), from `origin/main` c31650f,
fast-forwarded to c62661b. The next page in the site-wide restyle (`2026-10-05-ink-pages-design.md`),
after About C (live October 8) and NuriCell (live October 10). This spec replaces that file's
"Science (stage 4)" plan and the October 5 Science mockups (`reference/ink-pages/mockups/science-top.jpg`,
`science-bottom.jpg`): they reused the homepage's mitochondrion, its brush line with stations and its
crane, and Mo ruled on October 6 that each page shares the theme only and has its own design.

## Decisions (Mo, October 13 and 14, 2026)

- Three ideas were mocked on the live site (A the handscroll, B through the lens, C where your cells
  work). Mo picked **A** ("Design A looks good"), then approved the whole page and its phone opening
  ("Yeah, looks good. Let's build it."). Review page: https://claude.ai/artifact/Rvr98DEWPLUWDighZgVSGv
  (version 2). Approved screens: `reference/ink-pages/mockups/science-ink/`.
- Today's Science words stay (`science/science-content.ts`). Dr. Liu is his real photograph, never a
  generated face. Dr. Iris Wang appears in words only.
- Titles use the homepage's title face, Ysabeau (live on the homepage since October 13; Mo: the other
  pages follow). Everything else stays Switzer.
- California, not Asian (Mo's October 13 rule; "1 yes", October 14): the plum branch becomes a
  California poppy and the Asian tea set becomes two simple mugs. The handscroll itself stays: it is
  his real path, and it ends in California.
- Final paintings ("2 yes", October 14): about $0.50 more from the $3 Mo gave on October 13.

## Shared, and its own

Shared (the theme): the kit's rice paper, sumi ink, gold leaf only for energy, the site menu bar
(`SiteHeader`, current "Science"), the footer (`SiteFooter` + `ClosingCrane`, now with the California
trail sign), the ink bloom, honesty captions, the one breath and its ease, reduced motion complete and
still. `DESIGN.md` applies unless named here.

Its own: the **handscroll** (a painting that travels sideways as you scroll down) and the **strip
rhythm** below it (a header row, one wide painting, its words in three columns underneath). No brush
line, no stations, no ensō, no lantern, no reused homepage, About or NuriCell painting.

## The page, top to bottom

| #   | Part             | Picture                                                                                                                                    | Words                                                                                                                                                                               |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Opening + scroll | **The handscroll**: Okayama castle → the ocean → Berkeley's bell tower among eucalyptus → Salzburg → California oaks and one gold-leaf sun | eyebrow "Science", the title, the lead; under the painting the five stops (`pathStops`): Okayama, 1994, 2002, 2025, Today                                                           |
| 2   | Dr. Liu          | His real photo on its paper mount                                                                                                          | role, name, headline, intro, the three numbers (280+, 1994, 2025, each with its source), "Read his story" (the kit's scientist sheet)                                               |
| 3   | The formulas     | The five real bottles in one row, NuriCell a little larger                                                                                 | "Every BiGH formula was developed by our scientists…", Dr. Iris Wang's line, each bottle's name and credit; each bottle links to its product page                                   |
| 4   | The research     | **A rack of rolled scrolls**; three lie pulled forward (the three key studies)                                                             | "Curiosity, with references.", the lead, the three key studies (year · kind · journal, title, text, "Read the study", "Dr. Liu's work" tag), "See all 36 sources", the honesty line |
| 5   | Health explained | **One painting, three scenes**: an oil lamp with a gold-leaf flame, balanced stones, California poppies                                    | "Make sense of the science.", the lead, the three article titles and previews; each opens the kit's short explainer sheet                                                           |
| 6   | Ask BiGH Science | **Two mugs** with steam rising, on a low wooden table                                                                                      | the title, lead and text, the three steps (numbered: a real sequence), "In development", the note                                                                                   |

Then the shared footer. Section ids: `scientists` (opening and scroll), `liu`, `formulas`, `research`,
`health`, `ask`; the menu's and footer's Science links (`/science#scientists`, `#research`, `#health`,
`#ask`) keep landing under the menu bar.

Below Dr. Liu every part has the same rhythm: a header row (title left, lead right), one wide painting
at content width with soft ends, the words in three columns under it (the health scenes stand over
their three columns). Gold appears twice on the whole page: the sun at the scroll's end and the lamp's
flame. The rest rests in ink.

## The handscroll

- **Desktop and tablet (from 960px):** the scroll part is pinned under the menu bar while the page
  scrolls; the painting travels from right to left, so scrolling down reads the scroll from Okayama to
  Today. Under the painting a fine line runs the width of the page with five dots, one under each
  place; the line inks itself up to the place in view, and that stop shows its title and sentence (the
  others show only their mark and title). The scroll lets go once "Today" and its sun are fully in view.
- **Phones (under 960px):** the same travel, with a shorter painting band (about 300px tall), the
  five dots in a row, and only the current stop's words under them.
- **Reduced motion:** nothing pins or travels. The whole scroll is shown at once, scaled to the
  page's width, with all five stops in a row (desktop) or a list (phones) under it.
- **No script:** the same as reduced motion.
- The painting has one alt text describing the journey; the stops are an ordered list in the page's
  text, so screen readers get the whole path. Keyboard users scroll past it like any part.
- Scrolling stays native (the kit's smooth scroll); no scroll hijacking, no snapping.

## Paintings and spend

Kept from the mockups (originals and prompts move from the session scratchpad to
`reference/ink-pages/science/`): `gpt25-R-scrolls`. New:

- **The handscroll, longer and looser.** The mockup painting is one 21:9 picture, only about 1.4
  screens wide at its band height, so it barely travels, and its brushwork is more detailed than the
  rest of the site. The final is three 21:9 panels painted to one horizon with mist at their ends
  (1: Okayama and the ocean, 2: the ocean, Berkeley, the hills of 2002, 3: Salzburg, California, the
  sun), each with the mockup scroll and the homepage crane as style references, joined in their mist
  by the build script (a darken blend, so ink stays ink and paper stays paper). About four screens of
  travel at 1440px.
- The two California swaps, each an edit of its mockup painting: poppies for the plum branch
  (`R-health`), two mugs for the tea set (`R-tea`). One or two jobs each.

About 6 to 10 GPT Image 2.5 jobs, about $0.30 to $0.50, from the $3 Mo gave on October 13 (10 jobs,
about $0.50, used by the mockups). Ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-science-mock` (cap 40).

A build script (`reference/ink-pages/science/build_science.py`, on the NuriCell pattern) divides the
paper out, joins the scroll panels, cuts the gold masks (sun, flame), cuts phone crops of the strips
(the three health scenes become three pictures, one over each article; the scroll rack and the tea
table are cropped to their middle), and writes webp files to `public/images/science/ink/` plus a
generated data file. Honesty caption "Illustration" under each painting.

## Motion

- Signature: the scroll travels (above).
- Every other painting blooms as it arrives (kit `useBloom`); gold leaf takes the kit's glint once
  bloomed. Words settle as on the other ink pages.
- No WebGL, no 3D, no scroll-scrubbed film.

## Code

- `/science` renders the new page inside `InkPage` (current "science"), `SiteDialogs` and
  `ProductPagesProvider`, like About. `/hken/science` still redirects to `/cns/science`.
- New components in `src/components/science/ink/`; words stay in `science-content.ts`.
- Ysabeau loads on this route the way the homepage loads it (`next/font`, preload off).
- Today's film page (`look-film`, `film-scene`, `site-chrome`, `science-page`, `look-types`) moves to
  `reference/science-page/looks/film/`, as earlier rounds' looks did. `smooth-scroll.ts` stays (the
  kit imports it). Film pictures in `public/images/science-page/` leave `public/` only if nothing
  else references them (the menu's Science drop-down and the footer links are checked first); their
  originals stay in `reference/science-page/originals/`.
- Nothing on the homepage, About, NuriCell, the other product pages, the menu bar or the footer
  changes.

## Words and languages

No words are lost. New strings (the scroll hint, alt texts, "Read the study", the formulas eyebrow)
get draft translations in all five languages, flagged for a native check. New copy keys start at
`m650` so they cannot collide with the Propolis session working in parallel (its keys continue from
`m612`).

## Checks

- A new `scripts/qa/qa_science_ink.py`: every part and every `science-content.ts` string present; each
  painting loads and blooms; the scroll pins, travels from Okayama to Today and lets go, with the
  right stop lit at each point; reduced motion and no-script show the whole scroll still; no horizontal
  page scroll; deep links land under the menu bar; "Read his story", "See all 36 sources" and the
  explainer sheets open and close; bottles link to their pages; keyboard reaches every control;
  Korean, Japanese, Chinese and Vietnamese pages load with no clipped words.
- Unchanged: homepage gate (`home_snapshot.py`, `qa_home_ink.py`), `qa_about.py`,
  `qa_nuricell_ink.py`, `qa_nav.py`, `qa_fda.py`. The film's `qa_science_film.py` retires with it.
- Sizes 1920, 1536, 1440, 1280, 1024x768, 900, 768, 390, 360; dev (port 3050) and `next start` (port
  3051). Look at every screenshot full size, scrolled like a visitor; 9/10 is the bar; a fresh
  reviewer (`impeccable-finish-reviewer`) before Mo sees it.

## Delivery

Local commits on `science-ink`. Mo sees screenshots first; a Vercel preview only with her yes to push
the branch; main and the demo alias only with her yes. Fetch and merge `origin/main` before any push
(several sessions push to main within minutes).

## Risks

- Joining three paintings into one scroll without a visible seam; the mist at the panel ends is the
  plan, and a fourth job repaints a panel if a join shows.
- A long pinned part on phones: about four screens of scrolling to reach Dr. Liu. If it feels long on
  a real phone, the phone band travels faster (less scroll per screen of painting).
- The real glossy bottles against soft ink (7.5/10 in the mockup, the page's weakest part).
- The fortress town is Salzburg, where the academy that elected him is based; he did not live there.
  The stop says only "An academy honor".
