# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Last updated:** October 27, 2026, by Claude Code (the tablet menu's crane fix put live on its
  own, `main` `5fe0846`). Earlier the same day: About's bigger circle merged into studio (local);
  the product openings' release notes, the Title face entry below marked live. October 26:
  NuriCell research, tap a book (local, not pushed). Earlier the same day: Science, one place per
  screen, put live on its own.
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **Local, not live (October 26): About, a bigger circle and no gold leaf (Mo picked A twice).**
  The opening circle fills the first screen and "Be in Good Health." is written inside it (on a
  phone the title sits inside on three lines, the lead under the circle). The gold leaf that fell
  onto the circle is gone (Mo found its fall and shine cartoonish; the opening's gold is the sunlit
  hilltop). Layout B, a bigger circle with the words under it, was built at a temporary
  `/about-below` to compare and removed after Mo's pick. `circle.module.css`, `about-ink.tsx`,
  `let-the-circle-go.ts`; mockups and the built shots `reference/ink-pages/mockups/about-circle-size/`,
  artifact `CC6pZFonqYvRfZnJEB6g57`. Merged into studio October 27 on top of 598d10a and
  re-checked on the built site (`npm run build` + `next start`): `qa_about` 404/404 (new
  `circle_layout` section), `qa_home_ink` 282/282, `qa_nav` 326/326; lint and type-check clean.
  `qa_fda` stops at Turmerific, which never goes network-idle on a local `next start` (old, not
  this change).
- **Local, not live (October 26): NuriCell research, Mo's pick A, "tap a book, read its study"**
  (mockup and the built page's shots `reference/ink-pages/mockups/nuricell-research/`, artifact
  `UFqCskQg1VCPiKy8ZTTVLk`; the draft rounds in `codes/bigh-archive/nuricell-research-mockup-2026-10-26/`).
  Mo asked for the research list to be more fun to read and found the small "The research" label
  odd. Each of the seven books in the painting is a button (a clip-path over the painting, grown
  around the far books): tap one and its study opens, the other books fade under a little paper
  (`books-mask-v1-*.png`, cut by `reference/ink-pages/nuricell/find_books.py`). The studies are six
  plain questions with short answers written from each paper's abstract; the two 2003 reviews
  share "Scientists disagree" and light two books. On a phone a tapped book brings its question up
  under the menu bar. No label, no "Show all"; without scripts every answer shows. The note is
  shorter in `nuricell.ts`. New words translated as drafts (m930-m961), including the chapter's
  heading, which was English in every language on all five product pages until now. On the built
  site at db2b938 (`npm run build` + `next start`): `qa_nuricell_ink` 443/443 (a new research
  section), `qa_questions` 403/403, `qa_home_ink` 282/282, `qa_nav` 326/326; the other four
  products' language checks 16/16 each on the build just before (without the product questions).
  Open: native check of m930-m961; the far books are small
  to tap on a phone (the questions are the easy tap).
- **Local, not live (October 26): NuriCell Dr. Liu, "the view west"** (Mo picked idea A, the
  Berkeley story, then A2 of two mockups, then round 2 of A2; mockups and the built page's shots
  `reference/ink-pages/mockups/nuricell-liu/`, artifact `W7qmqUj4RNiCVLmtk94j5a`). His real
  portrait (liu-v1) stands on the Berkeley hills over the bay, the Golden Gate in the fog, painted
  in grey ink, dry grass in front of his foot. From 960px one painting runs across the chapter
  (as wide as the window, at most 1.8 × (window height - 140px), centred) and his name and words
  sit in its sky, ending above its land; phones get their own framing (`paintingPhone`, Next art
  direction in `ink-chapter.tsx`'s `FramedPicture`). No label over his name; a lead, one line on
  the 2002 study (told as published from Ames's lab: his years there were 1994-1997) and the note
  "An animal study, not a test of NuriCell." (m907-m910, drafts). Plates `liu-berkeley-v3`,
  `liu-berkeley-phone-v3` from `build_nuricell.py`'s `berkeley()` (Codex originals
  `liu-berkeley-west-ink-v2b`, `liu-berkeley-grass-v1`; v2a a spare). Nature Calm keeps its plain
  portrait and label. Built site (`npm run build` + `next start`, combined with the questions work
  at d15db52): `qa_nuricell_ink` 430/430, `qa_nature_calm_ink` 159/159; earlier build `qa_home_ink`
  282/282, `qa_nav` 315/316 (the tablet crane jump, since fixed in f9c1132). Not pushed.
- **Live (October 27): the tablet menu's crane eases with the fold** (Mo said to fix the jump,
  then to push "only that fix"; before/after page `J5z9H46J76J8t2uM7nZqkf`). Released alone from
  live `main`: `main` `5fe0846` (the code of `f9c1132`), production `dpl_9WQV7zjP…`, demo alias
  → it; public `qa_nav` 326/326, `qa_home_ink` 282/282 (`docs/public-demo.md`). On a tablet the
  crane takes the room left under the menu's words (130px to 230px), so it changes size as Products folds. Left to the
  layout it followed only the slice of the fold where that room lies between its two sizes:
  folding Products away at 834x1112 it grew 54px in 0.12s (up to 13px a frame) and stopped dead;
  at 768x1024, 100px in 0.07s (25px a frame). Now `useCraneRoom` in `nav-inscription.tsx`
  works out the crane's end size as a part starts to fold and, on every change of the folds'
  size (a ResizeObserver, before the frame is drawn), holds it as far from its old size to its
  new one as the folds are through theirs; when the fold's transition ends the layout has it
  again. Biggest step now 4px a frame at 834x1112, 8px at 768x1024 and 1024x768; phones and
  1024x1366 unchanged. `qa_nav` films the fold at all three tablets and checks the size is let
  go after. Built site (`npm run build` + `next start`, studio `c947fcf` plus this): `qa_nav`
  326/326, `qa_home_ink` 282/282; lint and type-check clean. Separately, still open:
  `scripts/qa/qa_science_links.py` still clicks the Science drop-down switched off this morning.
- **Local, not live (October 26): product questions, Mo's pick A, "a painting for each answer"**
  (mockups `reference/ink-pages/mockups/nuricell-questions/`, artifact `MceTcmgqxFuQPtLHrJ8xfE`;
  the built pages in `.../built/`, artifact `S4ttkdJhyASQLXjr8uYigt`). All five ink product pages
  (`questions.tsx`, shared): from 960px the questions on the left and the picked one's painting and
  answer on the right (the first picked as the page opens, the menu bar's pale wash behind it, a
  round "+" on the others; the old answer fades out before the new one fades in); on a phone each
  question opens in place with its painting. 28 Codex paintings, one per question, true to each
  label (capsule count and colour, 30 squares a month), cut to 3:2 by
  `reference/ink-pages/questions/build_questions.py` (README there: what was repainted and why).
  Propolis's old questions grid (heading left, list right) is gone; its heading keeps its own
  face. No new words. On the built site (`npm run build` + `next start`) on top of studio 598cab0:
  `qa_questions` 403/403 (new: all five pages, wide and phone, no script, four languages),
  `qa_nuricell_ink` 430/430, `qa_opc_ink` 185/185, `qa_propolis_ink` 273/273,
  `qa_turmerific_ink` 155/155, `qa_nature_calm_ink` 159/159, `qa_home_ink` 282/282, `qa_nav`
  315/316 (the known tablet crane jump). The product QA scripts now pick each question to read its
  answer (only the picked one is shown).
- **Live (October 26): Science, Mo's pick B, "one place per screen"** (Mo: "Science only, not the
  other sessions' unreleased work"). Released from a copy of live `main` with only the Science
  commits, rebased once onto `78ae1d6` (product openings, pushed meanwhile): `main` `e6e7e36`,
  production `dpl_DAZ7E1Tfs5ubFa8w4nfLvu3yod2t`, the demo alias points to it; public demo
  `qa_science_ink` 633/633, `qa_home_ink` 282/282, `qa_nav` 315/316 (the known tablet check)
  (`docs/public-demo.md`). On `main` the Science commits are `d9d0010`, `a2554f4`, `e6e7e36`
  (the same content as `studio`'s `8f7b99d`, `500873d`, `3a5cd0d`). `studio` has not merged
  `origin/main` since: a trial merge conflicted in 13 files (NuriCell, the catalogs,
  `copy-keys.json`, HANDOFF, AGENTS), so the next full release from `studio` must merge
  `origin/main` first. Before that: (mockups and the
  built page's shots `reference/ink-pages/mockups/science-path/2026-10-26/` and `.../built/`,
  artifact `9jBznqoXRwUacxeKv2P8AP`). Mo liked the paintings but found the sideways handscroll
  "feels like a draft". The page opens on the title and Dr. Liu (photo, name, intro; his numbers
  row is gone, his path tells it), then his path down the page: Okayama (painting left), Berkeley
  1994 (right, with the 2002 study), Salzburg 2025 (left), Today (wide, one line in the sky by the
  gold sun); then research, health explained, the formulas (moved down), Ask. Paintings cut from
  the old band by `build_science.py` (`PLACES`, phone cuts too); `path.tsx`; the handscroll's
  `journey.tsx` and `use-journey.ts` are deleted. Berkeley says 1994, not the mockup's 1994-2002
  (the faculty profile dates his time in Ames's lab 1994-1997). The path's words are English in
  every language, as the old stops were. `qa_science_ink` rewritten for the path (its journey,
  rooms and last-resort checks are gone). On the built site (`npm run build` + `next start`):
  `qa_science_ink` 633/633, `check_science_art.py` all pass, `qa_nav` 315/316 (the known tablet
  crane jump), `qa_home_ink` 282/282. `qa_science_links.py` crashes before checking anything: it still
  clicks the Science drop-down that became a plain link earlier on October 26 (not this change;
  not fixed).
- **Live (October 26): product openings, the words under the name, Mo's pick C "Title face"**
  (mockups `reference/ink-pages/mockups/nuricell-hero-left/`, artifact `1TNAN8z5fW6P14w7kv3QZz`).
  NuriCell, OPC, Nature Calm and Turmerific (the shared opening; Green Bee Propolis keeps its own):
  the headline in Ysabeau (560; Korean, Japanese and Chinese keep the title weight), the purpose a
  large lead in ink with no side line, and from 960px the two sit together and end where Add to cart
  ends (the refund line sits in a subgrid row of its own). Mo turned down Dr. Liu's photo there:
  pages without him would look lesser. On the built site (`npm run build` + `next start`) at 59585a0
  (on top of the lighthouse and What's inside): `qa_nuricell_ink` 429/429 (its opening check now
  tests the new look), `qa_opc_ink` 185/185, `qa_turmerific_ink` 155/155, `qa_nature_calm_ink`
  158/159 (its older front-layer pixel check, in the Buy chapter); a build before the last two small
  fixes (the dash kept with its word, the CJK weight) also passed `qa_propolis_ink` 273/273,
  `qa_home_ink` 282/282, `qa_nav` 315/316 (the known tablet crane jump). Released on its own from a
  copy of live `main` (`af7faf3`) with only this change cherry-picked: `main` `78ae1d6` (the same
  content as `studio`'s `59585a0`), production `dpl_92LiEZJuxbddWQY2mQNmcV8Jw2mG`; public demo
  `qa_nuricell_ink` 404/404, `qa_opc_ink` 185/185, `qa_nature_calm_ink` 159/159, `qa_turmerific_ink`
  155/155, `qa_propolis_ink` 273/273, `qa_home_ink` 282/282, `qa_nav` 315/316 (the known tablet
  crane jump). The Science release (`e6e7e36`) went on top minutes later and the demo alias moved
  there, with the new openings still in it (`docs/public-demo.md`). Open: on Turmerific at 1440x900
  the refund line ends on the window's bottom edge; on a phone its purpose runs six lines.
- **Local, not live (October 26): NuriCell "Tiny power plants", Mo's pick B, the lighthouse**
  (mockups and the built page `reference/ink-pages/mockups/nuricell-why/`, artifact
  `LiWF3jKo2tdLH4otM1SrRc`). Mo first picked A (a Gold Rush miner's lantern), saw it built beside
  the lighthouse sample, and switched to B the same day; the lantern's pictures are gone and its
  originals are in `codes/bigh-archive/nuricell-why-unused-2026-10-26/goldrush-built-a/`. A
  lighthouse on a California cliff replaces the paper lantern (it read as Asian); its lamp and
  beam still come on as you scroll. Codex paintings: the lit take (`why-lighthouse-a2`), then the
  unlit take as an edit of it, of which only the light is used (`build_nuricell.py`,
  `lantern()`). Below 960px it is drawn at 55% of the window (the template's 46%), so on a phone
  it spans the column. No label over the heading, one lead-in line with no indent, the 2% small
  beside a big 20% (stacked on phones); the section's six lines translated as drafts
  (m901–m906). On the built site: `qa_nuricell_ink` 429/429, `qa_home_ink` 282/282, `qa_nav`
  315/316 (the known tablet crane jump), `check_nuricell_art.py` all pass.
- **Live (October 26): NuriCell "What's inside", Mo's pick 1A** (mockups
  `reference/ink-pages/mockups/nuricell-inside/`, artifact `Bnhi2oV5MB9eoDusAmdiC2`; the built
  page recorded in `built.html`, artifact `UbeHphVKjW9BqEs2jXh8Fr`). The capsule painting's gold
  leaf rises out of the powder and settles where it is painted, then each flake keeps turning,
  catching the light (`nuricell-leaf.tsx`: one canvas over the painting without its leaf; the leaf
  as painted for reduced motion and no script). No label over the heading; "per serving of 3
  capsules" right under it; the label's other lines as a card; the research note said once at
  the chapter's end (NuriCell's synergy note now says what notes.science said). "Why these four
  work together" is three scenes (`nuricell-scenes.tsx`): each pair's two powder heaps and its
  gold (lit; kept in reserve; two halves made one), each with Play again. Pictures:
  `reference/ink-pages/nuricell/build_nuricell_gold.py` (capsule-ink, capsule-gold, capsule-leaf,
  `heap-*`). NuriCell only; the other four product pages are unchanged. On the built site
  (`npm run build` + `next start`): `qa_nuricell_ink` 404/404 (new sections plate, gold,
  scenes), `qa_home_ink` 282/282, `qa_propolis_ink` 273/273, `qa_opc_ink` 185/185,
  `qa_nature_calm_ink` 158/159 (its older front-layer pixel check), `qa_nav` 315/316 (the
  upright tablet's crane jump, recorded with the Science-link change above).
  The new words ("Also on the label", the card's lines, the merged note) are English in every
  language, like the rest of this chapter's product words. On Mo's yes Claude pushed `main` to
  `c944a72` (this, the Science link and the footer's copyright line below, merged with the
  homepage science peek `75fb88e`); production `dpl_4e5NFHzU2WD5VdsJAosxQVZZp6vf`, the demo alias
  points to it; public demo `qa_nuricell_ink` 404/404, `qa_home_ink` 282/282, `qa_fda` 232/232,
  `qa_nav` 315/316 (the tablet crane jump). "Tiny power plants" above was not pushed.
- **Live (October 26, with "What's inside"): the footer's copyright line comes last** (`75c6190`;
  AGENTS.md "Footer: the copyright line comes last").
- **Live (October 26, with "What's inside"): Science is a plain link in the menu bar** (Mo: the Science page
  is one page, and the drop-down's four doors into it made the site look short of content; keep
  the design for later). On the bar and in the phone's menu Science goes straight to `/science`,
  like About and Support; on the Science page its word carries the painted stroke. The drop-down
  is switched off, not deleted: `navScienceMenu` in `src/components/ink/nav/nav-data.ts`, and
  `SCIENCE_MENU` in `scripts/qa/qa_nav.py` (its drop-down checks skip; new Science-link checks
  run). `qa_home_ink`, `qa_science_ink`, `qa_about` and `home_snapshot.py` now expect the plain
  link. Built site (`npm run build` + `next start`): `qa_nav` 315/316, `qa_home_ink` 282/282,
  `qa_science_ink` 1279/1279, `qa_about` 353/353 (dev: `qa_nav` 315/316); lint and type-check
  clean. Mo's before/after page: https://claude.ai/artifact/DEE11nzfSvHRMeSgmFFfCC. The one
  failure was old, newly checked: the tablet menu's crane jumping as Products folds away (fixed
  later the same day, live October 27 in `5fe0846`: "the tablet menu's crane eases with the
  fold" at the top). Live in `c944a72`.
- **Live (October 24-25, latest): homepage science on phones, the tabs over the picture and a
  finger swipe** (Mo picked A on October 23, then asked to swipe from one topic to the next and
  said to put it live). Under 900px the three tabs sit right above the picture; the three topics
  (picture, line, words) sit side by side in a strip as wide as the window that snaps to one
  topic; the tabs glide it and follow the swipe; the age slider still drags sideways.
  `science.tsx` (`.slides`, `.slide`). Claude pushed `main` to `28a87db` (a fast-forward from
  `53913a3`); production `dpl_7vTcT4734Sht8EkW36E3sSwnyGa8`, the demo alias points to it; public
  demo `qa_home_ink` 282/282, `qa_nav` 440/440. That public test found a short drag sometimes
  left the strip 40 to 110px off a topic (11 of 48), so on October 25, on Mo's yes, Claude pushed
  the fix `3537053` (the strip glides to the nearest topic once it is still with no finger on it):
  `main` `4d27258`, production `dpl_6BGC8Py9pvpEnCqtW2yzj1guNNFb`, the demo alias points to it;
  public demo 0 of 48 short drags off a topic, touch test passed, `qa_home_ink` 282/282,
  `qa_nav` 440/440. Tested with synthesized touch in Chrome, not on a real phone.
- **Live (October 23): the homepage's flying crane between B and C** (Mo found C, half
  size, too small; of B, a size between and C on `reference/ink-pages/mockups/home-crane-size/` he
  picked the size between and said to push it in place of C). Desktop: 57.5% of the comp's crane,
  shrunk toward the point its brush line leaves from, then lifted 60 comp px and moved 50 left
  with its flight stroke. Phones: 63.4vw (66% of the old 96vw), the line unchanged.
  `opening.module.css`; `qa_home_ink`'s phone check now expects the bird at about 41% of the
  window. On the built site (`next start`), the crane's box at 1920x1080, 1440x900 and 390x844
  within 1px of the mockup. Claude pushed `main` to `116c22f` (a fast-forward from `eac92d8`);
  production `dpl_GihZFmN8MjwBSwmjk1SujhiXWgKr`, and the demo alias pointed to it; public demo
  `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`).
- **Live (October 23): Free radicals shows the harm** (Mo picked A of three and said to put it
  live): the few sparks that slip past the chimney's screen burn black holes in the roof. See
  "Homepage science section" below. Claude pushed `main` to `eac92d8` (a fast-forward from
  `619e77d`); production `dpl_GNdZYehqzkfJc1Gbq1HUgjxeNgrW`, and the demo alias pointed to it;
  public demo `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`). The crane push
  above is built on it.
- **Live (October 23): Switzer is served from the site itself** (Mo said to host it
  ourselves, saw the before/after, `reference/ink-pages/mockups/switzer-self-host/`, and said to
  push it). Fontshare's stylesheet kept dropping the
  connection (the bullet below). Its licence (ITF Free Font License 2.0) allows self-hosting but
  not sharing the files through a public repository, and this one is public, so
  `scripts/fetch-fonts.mjs` fetches the two official variable files (upright 42 KB, italic 33 KB,
  unchanged) from Fontshare's CDN before every `npm run build` and `npm run dev` into the
  git-ignored `public/fonts/switzer/`; if it cannot, the build stops. `globals.css` declares them
  as "Switzer" (so every existing stack and check still names it), the locale layout preloads the
  upright one (not on `/vn`), and `next.config.ts` caches `/fonts/*` for a year (a new file gets
  a new name). No page asks Fontshare for anything any more. Never commit the font files. On the
  built site (`npm run build` + `next start`): every page's first paragraph drawn in "Switzer
  Variable", the file 200 with the year-long cache, no request to Fontshare, `/vn` in Be Vietnam
  Pro without the preload; `qa_home_ink` 282/282, `qa_nav` 440/440, `qa_fda` 220/220, `qa_about`
  353/353, `qa_nuricell_ink` 355/355, `qa_propolis_ink` 273/273, `qa_opc_ink` 185/185,
  `qa_science_ink` 1279/1279, `qa_support` 341/341. Two that fail for older reasons:
  `qa_nature_calm_ink` 158/159 (the front-layer pixel check: on this computer the scene repaints
  hundreds of pixels between two identical screenshots, with Switzer or with it blocked; 159/159
  on the live site) and `qa_vn_font` 37/43 (the same six fail on the live site: the Ysabeau menu
  words and NuriCell's line heights). `qa_turmerific_ink` not run locally (it hangs on
  `next start`). Claude pushed `main` to `faf70af`, whose build failed (`MODULE_NOT_FOUND`:
  `.vercelignore` skipped all of `scripts/`; production stayed as it was), then let the one script
  through and pushed `619e77d`; its build log shows both files fetched (42 KB, 33 KB). Production
  `dpl_3zWtHArBcvgNMjpdAs1BnMwNXfK9`, the demo alias points to it; public demo: the font file 200
  with the year-long cache, no request to Fontshare, every page check passes (`qa_turmerific_ink`
  155/155 and `qa_nature_calm_ink` 159/159 included) but `qa_vn_font`'s six older failures
  (`docs/public-demo.md`).
- **Live (October 23): the homepage science powerhouse** (Mo picked D of six power
  plant ideas and said to put it live). See "Homepage science section" below. Claude pushed
  `main` to `5f800a8` (a fast-forward from `10ef0c5`); production
  `dpl_DMQiiuemFPhNiqRgyRX2HNMVuYvS`, the demo alias points to it; public demo `qa_home_ink` 282/282, `qa_nav` 440/440 (a first run's one failure was `ERR_NO_BUFFER_SPACE` on the checking computer)
  (`docs/public-demo.md`).
- **Live (October 22): the homepage's flying crane at half size (C)**. After B (below)
  went live, Mo asked to try C, then said to push C live in its place. Desktop: half the comp's
  crane, shrunk toward the point its brush line leaves from, then lifted 70 comp px and moved 60
  left with its flight stroke. Phones: 57.6vw (60% of the old 96vw), the line unchanged.
  `opening.module.css`; `qa_home_ink`'s phone check now expects the bird at about 37% of the
  window. Built in a scratch worktree (branch `home-crane-c`), then fast-forwarded here. On the
  built site (`next start`): `qa_home_ink` 282/282, `qa_nav` 440/440; desktop 1920 and 1440,
  phone, tablet, 2560 and Korean looked at (on a tablet, mid-wingbeat, the bird gets small).
  Claude pushed `main` to `10ef0c5` (a fast-forward from `28ee762`); production
  `dpl_CgS1YYUsbc1vtCWQeL69crspWZtJ`, the demo alias points to it; public demo `qa_home_ink`
  282/282, `qa_nav` 439/440 (the font host, below; `docs/public-demo.md`).
- **Fixed by the bullet at the top (October 23): the Switzer font host drops connections.** Switzer's stylesheet came from
  `api.fontshare.com`; from this computer the browser's request was reset
  (`net::ERR_CONNECTION_RESET`) in 5 of 6 loads of the demo and 3 of 6 of a local `next start`,
  and the page then falls back to another face (`qa_nav`'s "no console errors" fails on it).
  `curl` and a direct visit got 200. Not checked from another network. Self-hosting Switzer would
  remove the dependency; not done (not asked).
- **Live (October 22): the homepage science's "Aging cells" shows a brain cell**
  in place of the steam engine (Mo: an engine growing old did not relate to the age slider; he
  picked B, the cell up close, of two painted ideas; mockup
  `reference/ink-pages/mockups/home-science-cell/`). Its branches thin and its six gold power
  plants go out (6, 3, 1) as the age goes up. The first two topics keep the engine. Pictures
  `cell-<age>-v2.webp` from `reference/ink-pages/home-science/build_cell.py`; new caption lines
  `science.peekAge` (English only, like the others); DESIGN.md "The Science Stage Rule". Built in
  a separate worktree while another session pushed the crane, then merged here. On the built site
  (`next start`): `qa_home_ink` 282/282, `qa_nav` 440/440; laptop 1440 and 1280 and phone looked
  at, ages 35, 45 and 70 and the fade. Mo said to push it: Claude pushed `main` to `28ee762` (a
  fast-forward from `7ca818d`); production `dpl_C5C7DQ72sYC5jJTy6JH4zA8b3KAX`, the demo alias
  points to it; public demo `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`).
- **Was live (October 22), replaced by C above: the homepage's flying crane smaller and higher** (Mo
  found it a little big, picked B of 80%, 65% and 50%, and said to push it; mockups
  `reference/ink-pages/mockups/home-crane-size/`). Desktop: 65% of the comp's crane, shrunk
  toward the point its brush line leaves from, then lifted 50 comp px and moved 40 left with its
  flight stroke. Phones: 69vw (72% of the old 96vw), the line unchanged. `opening.module.css`;
  `qa_home_ink`'s phone check now expects the bird at about 45% of the window. On the built site
  (`next start`): `qa_home_ink` 282/282, `qa_nav` 440/440; desktop 1920 and 1440, phone, tablet,
  2560 and Korean looked at. Claude pushed `main` to `7ca818d` (a fast-forward from `7895696`);
  production `dpl_GZa6NHXg59Qc8D1u9zJBUyXqqtW3`, the demo alias points to it; public demo
  `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`).
- **Live (October 22): the homepage's brush line twice as heavy, and Sign up's stroke drawn
  bigger** (Mo said to push both). The line: Mo picked B of 1.5×, 2× and 2.5× (mockups
  `reference/ink-pages/mockups/home-brush-weight/`); the running line takes the whole weight, the
  bottle's ground and the closing stroke only a little, the crane's opening stroke none; the
  dry-brush streaks keep their old size (`WEIGHT` and `heavy` in `src/components/ink/brush.tsx`).
  On phones only the three rules and the closing stroke change. Sign up: Mo picked C of three
  fuller versions of the same painting (`35e26bb`, another session; DESIGN.md has the details),
  replacing the note below that the stroke stays as it is. Claude merged `main` (the steam
  train) into `studio` and pushed `main` to `7895696`; production
  `dpl_B9XcdfSd5XJS2R4L4UoondvxQcuk`, the demo alias points to it; public demo `qa_home_ink`
  282/282, `qa_nav` 440/440 (`docs/public-demo.md`). The smaller crane above went live after it.
- **Live (October 21): the homepage science steam train** (Mo said to put it live). See
  "Homepage science section" below. Claude pushed `main` to `7a042ce` (a fast-forward from
  `d9c8c34`); production `dpl_CJt1fJcyGvX3aocGj47Wi3AjVg7V`, the demo alias points to it; public
  demo `qa_home_ink` 282/282 and `qa_nav` 440/440 (`docs/public-demo.md`).
- **Live (October 21): two phone fixes** (Mo said to fix and push them). The homepage's
  warm sky was cut flat under the menu bar on phones (the opening's picture now clips only its
  sides, `opening.module.css`: a 12-level step, now under 1); and "✕ Close" was squeezed against
  the mark in the phone bar (from 400px down the bar's sides come out to 16px, the ✕ steps aside,
  the stroke is never shorter than clamp(78px, 26vw - 8px, 86px), CJK words at 17px: 15px or more
  to the mark from 360px in every language). Claude pushed `main` to `d9c8c34`; production
  `dpl_FF2NdyPy2e95UY2tYzJ96CcBzpjD`, the demo alias points to it (`docs/public-demo.md`). Not
  fixed: on a 320px phone, Japanese "メニュー" runs onto the stroke's dry tail, 8px from the mark.
- **Sign up's stroke kept, then drawn bigger (Mo, October 21).** He looked at three other strokes
  (clean, painted pill, dry brush; `reference/ink-pages/mockups/nav/2026-10-21-signup/`, originals
  `reference/nav/originals/codex-signup-*.png`) and kept the painting itself: at the size people
  see it, it reads as one quick brush gesture. Then he picked it a little fuller (C of three,
  `mockups/nav/2026-10-21-signup-fuller/`): the same painting drawn bigger, live since October 22
  (see above).
- **Live before that (October 21): the menu bar "Signed with one stroke"** (Mo picked A of three
  painted ideas and said to push it): the bar's words in Ysabeau (CJK keep their own letters), the
  painted rule under the bar from the first frame (laid once as the page opens), Sign up and the
  phone's Menu in paper on a black Codex-painted brushstroke (`inscription/swash-v1.webp`), a pale
  wash behind a pointed-at word (`inscription/wash-v1.webp`); `reference/nav/make_signed_strokes.py`
  cuts both. Ysabeau loads from the root layout (not preloaded: a preload would go unused on CJK
  pages). The Science eyebrow sits 22px under the rule from 1101px (`journey.module.css`).
  `qa_nav.py` updated (rule there from the start, the wash, text on the stroke). Claude pushed
  `main` to `849e26d` (a fast-forward); production `dpl_CuSdqu5hCtTLHH2tLy6m3ozDB38J`. Public
  demo then: all eleven page checks pass (`docs/public-demo.md`). Mockups,
  the three ideas and the built screenshots: `reference/ink-pages/mockups/nav/2026-10-21/`.
- **The homepage-science sketches seen here on October 21** (hiker and cell paintings, a README
  edit) were Claude Code's, for the science section (below). They were moved out of this folder
  the same day; the kept ones are committed with the steam train.
- **Live before that (October 19, latest then):** About's opening circle is now circle A, "heavy
  to dry" (a wet, heavy start that thins into dry streaks and lifts before it closes), and its
  gold leaf floats down onto the stroke like a real flake, then settles and catches the light; the
  spark of light that ran round the old circle is gone. Mo picked it from three new circles; Claude
  pushed `main` to `6e8aaca` (`ea13c93` plus that one commit). Production
  `dpl_6eTzh1tqkEpWqmBV1nM9w3YfxVJ7`. Public demo then: `qa_about` 353/353, `qa_home_ink`
  282/282, `qa_nav` 436/436.
- **Live before that (October 19):** all of `studio`, which Mo pushed as `ea13c93` (NuriCell layout
  B, About's oak, the redwood park sign in every page's footer and the homepage science section).
  Public demo then: `qa_home_ink` 282, `qa_nav` 436, `qa_fda` 220, `qa_about` 353,
  `qa_propolis_ink` 273, `qa_opc_ink` 185, `qa_nuricell_ink` 355, `qa_turmerific_ink` 155,
  `qa_nature_calm_ink` 159, `qa_science_ink` 1279, `qa_support` 341, all passing.
- **State:** `main` is `116c22f` (live: the powerhouse, Free radicals and the brain cell, the
  bigger Sign up stroke, the brush line's 2×, the crane at 57.5% and the self-hosted Switzer);
  `studio` adds only these release notes, so the next push is a fast-forward.
- **Turmerific on a local server:** the page never finishes loading under `next start` (its
  `soak-v1.webp` sprite and three link prefetches stay open, filling HTTP/1.1's six connections),
  so `qa_turmerific_ink` and the end of `qa_fda` time out locally. The live site shows the same open
  requests but finishes over HTTP/2, and both checks pass there. Not fixed; worth a look.
- **NuriCell layout B (Mo picked from mockups, October 19):** from 960px the lantern hangs right of
  its words, the capsule stands in the middle of its four ingredients, the books run in from the
  page edge, Dr. Liu stands right, the brushed 3 × 30 = 90 goes across the page. Phones keep one
  column. NuriCell only; Mo said leave the other four product pages as they are for now.
- **About (Mo picked both from mockups, October 19):** "Our purpose" shows a big painted valley
  oak (rope swing, gold light in the roots) in place of the seedling, larger than the page's other
  paintings on purpose; the mission line is a step under the heading, in ink. The opening circle's
  gold leaf lands as a spark of gold light runs once round the stroke, then glints now and then.
  The oak was painted with Codex's image tool (no API spend); notes in `reference/ink-pages/spend.md`.
  Its description is a draft translation (m900).
- **About checks (live):** on the built release copy `qa_about` 353/353, `qa_home_ink` 282/282,
  `qa_nav` 436/436; on the public demo the same plus `qa_nuricell_ink` 355/355. Desktop, phone and
  the four other languages inspected; the circle filmed frame by frame on dev, the built site and
  the demo. `qa_about`'s allowance for Next's "preloaded but not used" CSS warning now accepts
  Vercel's `?dpl=…` on CSS addresses (it counted that harmless warning on the first public run).
  A local `next start` once hung on one image resize under heavy load (NuriCell's unlit lantern at
  640px): restarting the server cleared it; Vercel's own image service served it fine.
- **Customers:** `bighnow.com` is still the old WordPress site (checked October 18). Nothing in
  this repo reaches it yet.
- **Homepage science section (Claude Code).** "Make sense of the science." shows, with a line
  under each picture tying it to the words: Mitochondria and Free radicals, an old powerhouse
  with its front left open (a worker feeding the gold fire, its steam turning the wheel, power
  out along the wire), Mo's pick D of six power plant ideas on October 22; for Free radicals its
  chimney opened up, the screen catching most sparks and the few that slip past burning black
  holes in the roof (Mo's pick A, October 23, after the caught sparks alone showed no harm;
  `build_plant.py`); Aging
  cells, a brain cell up close at three ages (`build_cell.py`). Before: the October 19
  hummingbird, apple and Joshua tree (decorative), a hiker with a window into a cell (dropped),
  the October 21 steam train. The caption lines (`science.peek`, `science.peekAge` in
  `content.ts`) are English in every language for now. Notes:
  `reference/ink-pages/home-science/README.md`; rule: DESIGN.md "The Science Stage Rule".
  On phones and tablets (under 900px) the tabs sit right above the picture and the three topics
  swipe sideways in a strip (DESIGN.md "The Scroll Story Rule"). Touch test:
  `scripts/qa/qa_home_ink.py` covers the tabs; finger swipes were tested through Chrome's
  DevTools protocol (`Input.dispatchTouchEvent`; `synthesizeScrollGesture` does nothing headless).
- **In progress:** None. **Next:** Mo's call.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the production build of `main`
at `849e26d`, the same build as <https://bigh-website.vercel.app/> (everything below, with the
October 21 menu bar). `bighnow.com` is still the old WordPress site.

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 21)        |
| Menu bar             | "Inscription", signed with one stroke (Oct 21); all five bottles in Products             | `qa_nav` 440/440 (Oct 21)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 21)             |
| About                | Design C, "circle"                                                                       | `qa_about` 353/353 (Oct 21)           |
| NuriCell             | Paper lantern that lights; each painting in its own place (layout B, Oct 19)             | `qa_nuricell_ink` 355/355 (Oct 21)    |
| Green Bee Propolis   | Bold Signature desktop; Editorial pair mobile; gold flowing into the bee tree            | `qa_propolis_ink` 273/273 (Oct 21)    |
| Advanced OPC Formula | Grapes lit from inside                                                                   | `qa_opc_ink` 185/185 (Oct 21)         |
| Turmerific           | Gold soaking into the paper                                                              | `qa_turmerific_ink` 155/155 (Oct 21)  |
| Nature Calm          | Still lake whose gold gathers into one line                                              | `qa_nature_calm_ink` 159/159 (Oct 21) |
| Science              | Dr. Liu's life as a handscroll (local: his path, one place per screen, Oct 26)           | `qa_science_ink` 1279/1279 (Oct 21)   |
| Support              | "Pull up a chair" porch; the form is a preview and sends nothing                         | `qa_support` 341/341 (Oct 21)         |

Details of each go-live are in [`public-demo.md`](public-demo.md). Each page's notes, prompts and
spend are in `reference/ink-pages/<page>/`.

## Unfinished or waiting on Mo

- **Translations:** new lines are drafts and need a native speaker's check: NuriCell m594–m609,
  Science m650–m661 (some older Science lines are still English in four languages), OPC m700–m705,
  Turmerific m740–m744, Nature Calm m780–m784, About's oak m900, NuriCell's tidied "Tiny power
  plants" words and its lighthouse m901–m906 (m904, the picture's alt text, rewritten for the
  lighthouse). Support is English only for now
  (its keys start at m618).
- **Support form:** sends nothing yet. Real email needs an email service and domain setup (Mo's call
  and spend).
- **Capsule colours:** unknown for Turmerific (painted gold) and Nature Calm (painted pale). Ask Mo.
- **Turmerific:** a liver question for the FAQ waits on Mo's research.
- **Green spring on other pages:** only the homepage has the watercolour tint. Mo hasn't been asked.
- **Homepage:** a font for Chinese, Japanese and Korean titles is still open.
- **Not connected yet:** Sign up (placeholder until Mo gives the link), the store and checkout.
- **Customer stories** are labelled fictional samples until real reviews exist.
- **Dr. Liu** hasn't seen his NuriCell painting yet.

## How this was checked (this setup)

- `studio` was cut from the newest `origin/main` (`bf4cb84`). `npm ci` installed cleanly.
- `npm run build` passed (after moving an old, git-ignored experiment, `scripts/qa/out/editorial-build/`,
  out to `C:\Users\mcbig\Documents\codes\bigh-archive\main-folder-leftovers-2026-10-16\`; its stray
  `homepage.tsx` broke the type check).
- On the built site (:3006): `qa_home_ink` 282/282, `qa_opc_ink` 185/185, `qa_nav` 436/436.
- Codex, run read-only in this folder, answered from this rulebook: branch `studio`, read this note
  first, originals and prompts in `reference/ink-pages/<page>/`, commit and update **Now** before
  switching.

## How to run the preview

```sh
npm ci                                              # after a pull that changed package.json
npm run dev -- --hostname localhost --port 3007     # dev server: http://localhost:3007
npm run build                                       # production build
npm start -- --hostname localhost --port 3006       # built site: http://localhost:3006
python -X utf8 scripts/qa/qa_home_ink.py http://localhost:3006
```

Claude Code: the previews "bigh-website" (:3007) and "bigh-website-prod" (:3006). Locales live at
`/`, `/kr`, `/jp`, `/cns`, `/vn`.

## Old folders

About 30 other copies sit in `C:\Users\mcbig\Documents\codes\bigh-*` (one per past task), plus one in
Codex's own worktrees folder. All their finished work is on `main`. A few hold leftovers that never
went live: old demo-notes commits (`support-page`, `home-gold-word`, `product-turmerific`), the
rejected About B design (`about-b`), the About comparison preview (`about-compare`), a June experiment
(`for-real`, with unsaved files) and unsaved files in `bigh-home`, `bigh-main-preview` and
`.claude/worktrees/hero-section-redesign`. Don't work in them. Ask Mo before deleting any.
